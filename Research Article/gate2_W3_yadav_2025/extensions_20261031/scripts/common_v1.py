"""Shared I/O only; no biological transformations."""
import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
EXT = ROOT / 'Research Article/gate2_W3_yadav_2025/extensions_20261031'
RUNS = ROOT / 'analysis/research/runs'
CACHE = ROOT / 'raw_data/Yd1_extension_20261031'
def read_csv(path, delimiter=','):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter=delimiter))
def save_csv(path, rows):
    assert rows
    with path.open('x', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
def save_json(path, obj):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(obj, indent=2, allow_nan=False) + '\n')
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()
