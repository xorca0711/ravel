"""Recover only the 18 public workbooks/library-metadata inputs needed for TN0."""
import argparse
from pathlib import Path
import urllib.request
from common import PACKAGE, REPO, read_json, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', help='Fetch missing inputs; default prints missing IDs only')
    args = parser.parse_args()
    manifest = read_json(PACKAGE / 'config/source_manifest.json')
    needed = [x for x in manifest['files'] if x['id'].startswith('library_metadata_') or x['cache_path'].endswith('.xlsx')]
    missing = 0
    for item in needed:
        path = (REPO / item['cache_path']).resolve()
        if not path.is_relative_to(REPO / 'raw_data/travaglini_nabhan_2020'):
            raise ValueError('Invalid cache path')
        if path.exists():
            if sha256(path) != item['sha256']:
                raise ValueError(f'Changed local input; preserve and investigate: {item["id"]}')
            continue
        missing += 1
        if not args.download:
            print(f'Missing: {item["id"]}')
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + '.download')
        if temporary.exists():
            raise ValueError(f'Partial download exists; inspect first: {temporary}')
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'TN2020-source-intake/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read(item['bytes'] + 1)
        if len(payload) != item['bytes']:
            raise ValueError(f'Source size changed: {item["id"]}')
        temporary.write_bytes(payload)
        if sha256(temporary) != item['sha256']:
            raise ValueError(f'Source hash changed; retained .download for review: {item["id"]}')
        temporary.rename(path)
        print(f'Recovered: {item["id"]}')
    print(f'{len(needed)} portable inputs; {missing} missing at start. Private notes and large matrices are not fetched.')


if __name__ == '__main__':
    main()
