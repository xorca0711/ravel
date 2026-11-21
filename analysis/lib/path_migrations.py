"""Exact, byte-preserving archive relocations; never directory aliases or replay."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

MANIFEST = 'analysis/research/path_migrations.json'

# The second leg is available only for a previously accepted Damani file.
DAMANI_PATHS = tuple('Research Article/' + folder + '/' for folder in (
    'gate2_DY1_damani_yokota_2026', 'ungated_damani_yokota_2026',
    'gate4M_04_damani_yokota_2026'))


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
        required = {'from', 'to', 'sha256', 'source_revision'}
        if not isinstance(item, dict) or not required <= set(item) <= required | {'source_eol', 'continues_from'}:
            raise ValueError('Invalid path migration entry')
        if 'source_eol' in item and item['source_eol'] != 'crlf':
            raise ValueError('Unsupported historical checkout line ending')
        for key in ('from', 'to'):
            validate_relative(item[key])
        for key, size in (('sha256', 64), ('source_revision', 40)):
            if not isinstance(item[key], str) or re.fullmatch('[0-9a-f]{'+str(size)+'}', item[key]) is None:
                raise ValueError(f'Invalid migration {key}')
        if item['from'] in old or item['to'] in new:
            raise ValueError('Duplicate migration source or destination')
        old.add(item['from']); new.add(item['to'])
    parents = {r['to']: r for r in value['files']}
    for item in value['files']:
        parent = parents.get(item['from'])
        if parent is None and 'continues_from' not in item:
            continue
        first, middle, last = DAMANI_PATHS
        if (not parent or 'continues_from' in parent
                or parent['from'] != item.get('continues_from')
                or not parent['from'].startswith(first)
                or not item['from'].startswith(middle)
                or item['to'] != last + item['from'][len(middle):]
                or parent['sha256'] != item['sha256']):
            raise ValueError('Unverified, chained or self-referencing migration')
    return value['files']


def final_destinations(records: list[dict]) -> dict[str, dict]:
    """Index verified paths, including an explicitly witnessed second leg."""
    by_source = {item['from']: item for item in records}
    return {source: by_source.get(item['to'], item) for source, item in by_source.items()}


def resolve_historical(root: Path, relative: str) -> Path | None:
    """Only exact missing-file references can resolve, with unchanged bytes."""
    validate_relative(relative)
    item = final_destinations(entries(root)).get(relative)
    if item:
        if safe_path(root, relative).exists():
            raise ValueError(f'Migrated source reappeared: {relative}')
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
        witnesses = {}
        verified_ancestry = set()
        by_source = {item['from']: item for item in records}
        destinations = final_destinations(records)
        for item in records:
            try:
                revision = item['source_revision']
                if revision not in revisions:
                    git('merge-base', '--is-ancestor', revision, base or 'HEAD')
                    revisions.add(revision)
                saved = git('show', revision+':'+item['from'])
                if 'source_eol' in item:
                    # Some frozen contracts hash an explicitly selected CRLF checkout.
                    # Verify the old revision's attributes before reconstructing those bytes.
                    attrs = git('check-attr', '--source='+revision, '-z', 'text', 'eol',
                                '--', item['from']).split(b'\0')
                    if attrs[1:3] != [b'text', b'set'] or attrs[4:6] != [b'eol', b'crlf']:
                        raise ValueError(f'Unverified historical checkout attributes: {item["from"]}')
                    if b'\r' in saved or b'\0' in saved:
                        raise ValueError(f'Expected canonical LF text in Git: {item["from"]}')
                    saved = saved.replace(b'\n', b'\r\n')
                if hashlib.sha256(saved).hexdigest() != item['sha256']:
                    raise ValueError(f'Migration source hash differs from Git: {item["from"]}')
                if 'continues_from' in item:
                    if revision not in witnesses:
                        witnesses[revision] = json.loads(git('show', revision+':'+MANIFEST))['files']
                    parent = by_source[item['continues_from']]
                    if parent not in witnesses[revision]:
                        raise ValueError('First relocation missing from the second source revision')
                    transition = (parent['source_revision'], revision)
                    if transition not in verified_ancestry:
                        git('merge-base', '--is-ancestor', *transition)
                        verified_ancestry.add(transition)
                if safe_path(root, item['from']).exists():
                    raise ValueError(f'Migrated source reappeared: {item["from"]}')
                resolve_entry(root, destinations[item['from']])
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
