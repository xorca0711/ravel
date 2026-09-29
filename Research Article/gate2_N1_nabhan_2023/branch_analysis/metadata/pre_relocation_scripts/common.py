from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPER = REPO / 'Research Article/gate2_N1_nabhan_2023'
OUT = ROOT / 'trials/extension_v1'
CONFIG = json.loads((ROOT/'config/extension_v1.json').read_text())

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''): h.update(b)
    return h.hexdigest()

def now(): return datetime.now(timezone.utc).isoformat()
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
