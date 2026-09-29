from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parent
REPO = PAPER.parents[1]
OUT = ROOT / 'trials/extension_v1'
CONFIG = json.loads((ROOT/'config/extension_v1.json').read_text())

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''): h.update(b)
    return h.hexdigest()

def now(): return datetime.now(timezone.utc).isoformat()
def historical_input(path):
    """Resolve a frozen input path through the documented relocation only."""
    path = Path(path)
    record = ROOT / 'metadata/relocation.json'
    if record.exists():
        old_root = Path(json.loads(record.read_text())['old_root'])
        if path.is_relative_to(old_root):
            return ROOT / path.relative_to(old_root)
    return path

def frozen_script(path):
    """Original bytes remain available when path plumbing has been amended."""
    record = ROOT / 'metadata/relocation.json'
    if record.exists():
        item = json.loads(record.read_text())['archived_scripts'].get(path)
        if item:
            return ROOT / item['path']
    return ROOT / path

def write(df, name): df.to_csv(OUT/'tables'/name, sep='\t', index=False)
def load(name): return pd.read_csv(OUT/'tables'/name, sep='\t')
def canon(s): return CONFIG['aliases'].get(s, s)
def symbol_matrix(frame):
    frame=frame.dropna(subset=['symbol']).copy();frame['symbol']=frame.symbol.map(canon)
    # Ambiguous mappings are excluded, never resolved by expression strength.
    frame=frame.loc[~frame.symbol.duplicated(keep=False)]
    return frame.set_index('symbol').drop(columns='gene_id')
def guard(name):
    assert (OUT/'contract.json').exists(), 'Freeze first'
    assert not (OUT/name).exists(), 'Completed stage cannot be overwritten; use a new run'
def done(name, **kwargs):
    (OUT/name).write_text(json.dumps(dict(finished_utc=now(),**kwargs),indent=2)+'\n')
