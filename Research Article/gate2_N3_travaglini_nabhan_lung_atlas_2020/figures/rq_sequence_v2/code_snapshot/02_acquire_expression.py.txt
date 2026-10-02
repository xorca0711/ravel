"""Download the two explicitly selected public, versioned CELLxGENE objects."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
from common import REPO, PACKAGE, read_json, write_json

DEST = REPO / 'raw_data/travaglini_nabhan_2020/cellxgene'
ASSETS = [
    ('SS2', 'e04daea4-4412-45b5-989e-76a9be070a89', 'c0ee0004-7bd1-4986-9b66-8a9d3593c0e6', 186675192),
    ('10x', '8c42cfd0-0b0a-46d5-910c-fc833d83c45e', 'f5568ea3-c249-4e4e-91f8-46abc30a5612', 596270115),
]


def fetch(asset):
    assay, dataset, version, expected_size = asset
    path = DEST / (version + '.h5ad')
    record_path = DEST / (assay + '_download.json')
    if path.exists():
        raise ValueError(f'Input exists; use its recorded hash instead of re-downloading: {path.name}')
    partial = path.with_suffix('.h5ad.part')
    if partial.exists():
        raise ValueError(f'Partial transfer exists; inspect first: {partial.name}')
    url = f'https://datasets.cellxgene.cziscience.com/{version}.h5ad'
    digest = hashlib.sha256(); size = 0; last_tick = 0
    with urllib.request.urlopen(url, timeout=90) as response, partial.open('xb') as handle:
        while block := response.read(4 * 1024 * 1024):
            handle.write(block); digest.update(block); size += len(block)
            if size > expected_size:
                raise ValueError('Asset size exceeds pinned metadata')
            if size - last_tick >= 128 * 1024 * 1024:
                print(f'{assay}: {size // (1024 * 1024)} MiB downloaded', flush=True); last_tick = size
    if size != expected_size:
        raise ValueError(f'Incomplete asset: {assay}, {size}')
    partial.rename(path)
    record = {'assay': assay, 'dataset_id': dataset, 'dataset_version_id': version, 'collection_id': '5d445965-6f1a-4b68-ba3a-b8f765155d3a', 'url': url, 'bytes': size, 'sha256': digest.hexdigest(), 'cache_path': path.relative_to(REPO).as_posix(), 'downloaded_at_utc': datetime.now(timezone.utc).isoformat(), 'source_role': 'curated public mirror of source study, not independent replication'}
    write_json(record_path, record)
    print(f'{assay}: complete, {size} bytes', flush=True)
    return record


if __name__ == '__main__':
    DEST.mkdir(exist_ok=True, parents=True)
    if shutil.disk_usage(DEST).free < 2 * 1024**3:
        raise RuntimeError('Need at least 2 GiB available before acquisition')
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(fetch, ASSETS))
    out = PACKAGE / 'config/expression_sources_v1.json'
    if out.exists():
        raise ValueError('Refusing to overwrite expression manifest')
    write_json(out, {'schema': 'TN2020-expression-sources/v1', 'files': records, 'access_limits': 'Anonymous Synapse file GET returned 403. Public CELLxGENE collection supplies separately curated source objects; no access controls were bypassed.'})
