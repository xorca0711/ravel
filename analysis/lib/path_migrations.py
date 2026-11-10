"""Exact, byte-preserving archive relocations; never directory aliases or replay."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

MANIFEST = 'analysis/research/path_migrations.json'


def validate_relative(relative: str) -> None:
    if (not isinstance(relative, str) or not relative or '\\' in relative
            or ':' in relative or PurePosixPath(relative).is_absolute()
            or '..' in PurePosixPath(relative).parts
            or PurePosixPath(relative).as_posix() != relative):
        raise ValueError(f'Unsafe migration path: {relative!r}')


def safe_path(root: Path, relative: str) -> Path:
    validate_relative(relative)
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Migration path escapes root: {relative}')
    return path


def entries(root: Path) -> list[dict]:
    path = root / MANIFEST
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding='utf-8-sig'))
    if (not isinstance(value, dict) or set(value) != {'schema_version', 'files'}
            or value['schema_version'] != 1 or not isinstance(value['files'], list)):
        raise ValueError('Invalid path migration manifest')
    old, new = set(), set()
    for item in value['files']:
        if not isinstance(item, dict) or set(item) != {'from', 'to', 'sha256', 'source_revision'}:
            raise ValueError('Invalid path migration entry')
        for key in ('from', 'to'):
            validate_relative(item[key])
        for key, size in (('sha256', 64), ('source_revision', 40)):
            if not isinstance(item[key], str) or re.fullmatch('[0-9a-f]{'+str(size)+'}', item[key]) is None:
                raise ValueError(f'Invalid migration {key}')
        if item['from'] in old or item['to'] in new:
            raise ValueError('Duplicate migration source or destination')
        old.add(item['from']); new.add(item['to'])
    if old & new:
        raise ValueError('Chained or self-referencing migrations are forbidden')
    return value['files']


def resolve_historical(root: Path, relative: str) -> Path | None:
    """Only exact missing-file references can resolve, with unchanged bytes."""
    validate_relative(relative)
    for item in entries(root):
        if item['from'] == relative:
            return resolve_entry(root, item)
    return None


def resolve_entry(root: Path, item: dict) -> Path:
    if safe_path(root, item['from']).exists():
        raise ValueError(f'Migrated source reappeared: {item["from"]}')
    target = safe_path(root, item['to'])
    if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError(f'Migrated file missing or changed: {item["to"]}')
    return target


def migration_errors(root: Path, base: str | None = None) -> list[str]:
    """Bind relocations to Git history and retain every previously accepted map."""
    errors = []
    try:
        records = entries(root)
        def git(*args):
            return subprocess.run(['git', '-C', str(root), *args], check=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        revisions = set()
        for item in records:
            try:
                revision = item['source_revision']
                if revision not in revisions:
                    git('merge-base', '--is-ancestor', revision, base or 'HEAD')
                    revisions.add(revision)
                saved = git('show', revision+':'+item['from'])
                if hashlib.sha256(saved).hexdigest() != item['sha256']:
                    raise ValueError(f'Migration source hash differs from Git: {item["from"]}')
                resolve_entry(root, item)
            except (ValueError, OSError, subprocess.CalledProcessError) as exc:
                errors.append(f'Invalid migration: {exc}')
        if base:
            # A missing manifest is allowed only before the first migration.
            tree = git('ls-tree', '--name-only', base, '--', MANIFEST).decode().strip()
            if tree:
                prior = json.loads(git('show', base+':'+MANIFEST))
                if any(item not in records for item in prior['files']):
                    errors.append('Accepted path migrations are immutable; retain every prior entry')
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        errors.append(f'Invalid migration manifest: {exc}')
    return errors
