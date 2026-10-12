"""Restore hash-locked public Ravel outputs; never execute or overwrite them.

Run before research_gate.py. This supplies bytes; the research validator still
checks the unchanged scientific receipt, code, contract and output set.
"""
import argparse
import hashlib
import json
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener
import zipfile


class RestoreError(ValueError):
    pass


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_path(root, name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or '..' in path.parts or '\\' in name
            or ':' in name or path.as_posix() != name):
        raise RestoreError('Unsafe or noncanonical member path')
    root = Path(root).resolve()
    dest = root.joinpath(*path.parts)
    for component in (dest, *dest.parents):
        if component == root:
            break
        if component.is_symlink():
            raise RestoreError('Symlink destination refused')
    if not dest.resolve().is_relative_to(root):
        raise RestoreError('Destination escapes root')
    return dest


class ReleaseRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = urlsplit(newurl)
        if url.scheme != 'https' or url.hostname not in {
                'github.com', 'release-assets.githubusercontent.com',
                'objects.githubusercontent.com'}:
            raise RestoreError('Unexpected release redirect host')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(lock, target):
    url = urlsplit(lock['url'])
    if (url.scheme != 'https' or url.hostname != 'github.com' or url.query
            or not url.path.startswith('/xorca0711/ravel/releases/download/')):
        raise RestoreError('Only locked Ravel release assets may be downloaded')
    size = 0
    with build_opener(ReleaseRedirects()).open(lock['url'], timeout=60) as response, target.open('xb') as out:
        while chunk := response.read(1024 * 1024):
            size += len(chunk)
            if size > lock['bytes']:
                raise RestoreError('Download exceeds locked byte size')
            out.write(chunk)
    if size != lock['bytes']:
        raise RestoreError('Download size differs from lock')


def restore(root, lock, archive):
    """Validate the whole archive and every destination before installing files."""
    root, archive = Path(root).resolve(), Path(archive)
    if archive.stat().st_size != lock['bytes'] or sha256(archive) != lock['sha256']:
        raise RestoreError('Archive size/hash mismatch')
    members = lock['members']
    names = [item['path'] for item in members]
    if not members or len(set(n.casefold() for n in names)) != len(names):
        raise RestoreError('Duplicate locked member')
    targets = {name: safe_path(root, name) for name in names}
    if 'publication-manifest.json' in targets:
        raise RestoreError('Manifest is not an output destination')
    with zipfile.ZipFile(archive) as bundle:
        entries = bundle.infolist()
        entry_names = [i.filename for i in entries]
        expected = set(names) | {'publication-manifest.json'}
        if len(entries) != len(expected) or set(entry_names) != expected:
            raise RestoreError('Archive member set differs from lock')
        for item in entries:
            safe_path(root, item.filename)
            mode = stat.S_IFMT(item.external_attr >> 16)
            if item.is_dir() or mode not in (0, stat.S_IFREG):
                raise RestoreError('Non-regular archive member')
        manifest_info = bundle.getinfo('publication-manifest.json')
        if manifest_info.file_size != lock['manifest_bytes']:
            raise RestoreError('Manifest size mismatch')
        manifest_bytes = bundle.read(manifest_info)
        if hashlib.sha256(manifest_bytes).hexdigest() != lock['manifest_sha256']:
            raise RestoreError('Manifest hash mismatch')
        if json.loads(manifest_bytes)['members'] != members:
            raise RestoreError('Manifest member inventory mismatch')
        for item in members:
            info = bundle.getinfo(item['path'])
            if info.file_size != item['bytes']:
                raise RestoreError('Member size mismatch')
            with bundle.open(info) as src:
                if hashlib.file_digest(src, 'sha256').hexdigest() != item['sha256']:
                    raise RestoreError('Member hash mismatch')
            dest = targets[item['path']]
            if dest.exists() and (not dest.is_file() or sha256(dest) != item['sha256']):
                raise RestoreError('Existing output differs; refusing overwrite')
        # All validation above precedes any destination mutation. Exclusive writes
        # also refuse a racing creator; no existing output is replaced.
        created = 0
        for item in members:
            dest = safe_path(root, item['path'])
            if dest.exists():
                if not dest.is_file() or sha256(dest) != item['sha256']:
                    raise RestoreError('Destination changed after validation')
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            safe_path(root, item['path'])
            with bundle.open(item['path']) as src, dest.open('xb') as out:
                shutil.copyfileobj(src, out)
            if sha256(dest) != item['sha256']:
                raise RestoreError('Installed output hash mismatch')
            created += 1
    return {'ok': True, 'verified_members': len(members), 'created': created,
            'analysis_rerun': False, 'scientific_acceptance': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--lock', type=Path, default=Path(__file__).resolve().parents[1] / 'research/published_outputs/choi_figure1_v1.json')
    parser.add_argument('--archive', type=Path, help='Verify an existing archive without downloading')
    args = parser.parse_args()
    lock = json.loads(args.lock.read_text(encoding='utf-8'))
    if args.archive:
        result = restore(args.root, lock, args.archive)
    else:
        # TemporaryDirectory owns only a freshly generated directory below the
        # resolved system temp root. No repository or user directory is removed.
        with tempfile.TemporaryDirectory(prefix='ravel-output-restore-') as directory:
            temp = Path(directory).resolve()
            if not temp.is_relative_to(Path(tempfile.gettempdir()).resolve()):
                raise RestoreError('Temporary directory outside intended root')
            archive = temp / 'outputs.zip'
            download(lock, archive)
            result = restore(args.root, lock, archive)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
