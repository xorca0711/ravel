"""Check the dated figure-audit snapshot against tracked assets, without loading scientific data.

PNG/PDF hashes are exact bytes; SVG hashes normalize CRLF to LF to survive Git checkout
line-ending conversion. The inventory records audit depth, not blanket claim validation.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/FIGURE_AUDIT_CONSOLIDATED.csv'
IMAGE_SUFFIXES = {'.png', '.svg', '.jpg', '.jpeg', '.webp', '.gif', '.tif', '.tiff', '.eps'}


def main():
    files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    assets = {p for p in files if Path(p).suffix.lower() in IMAGE_SUFFIXES
              or (Path(p).suffix.lower() == '.pdf' and 'figures/' in p)}
    groups = collections.defaultdict(set)
    for p in assets:
        groups[Path(p).with_suffix('').as_posix()].add(Path(p).suffix[1:])
    with MANIFEST.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    names = [r['figure'] for r in rows]
    assert len(names) == len(set(names)), 'Duplicate inventory family'
    assert set(names) == set(groups), {'missing': sorted(set(groups) - set(names)),
                                      'stale': sorted(set(names) - set(groups))}
    for r in rows:
        formats = set(r['formats'].split('|'))
        assert formats == groups[r['figure']], r['figure']
        assert len(formats) == int(r['asset_count']), r['figure']
        hashes = json.loads(r['asset_sha256'])
        assert set(hashes) == formats, r['figure']
        for ext, expected in hashes.items():
            p = ROOT / (r['figure'] + '.' + ext)
            blob = p.read_bytes()
            if ext == 'svg':
                blob = blob.replace(b'\r\n', b'\n')
            assert hashlib.sha256(blob).hexdigest() == expected, str(p)
        for field in ('status', 'review_depth', 'evidence', 'findings', 'next_action'):
            assert r[field].strip(), (r['figure'], field)
    print(f'Figure audit verified: {len(rows)} families, {len(assets)} tracked assets; coverage and hashes match.')
    print(json.dumps(dict(collections.Counter(r['status'] for r in rows)), sort_keys=True))


if __name__ == '__main__':
    main()
