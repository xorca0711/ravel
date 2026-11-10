"""Archive the failed qualification bytes; archival success is not analysis success."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
a=argparse.ArgumentParser();a.add_argument('--output',required=True,type=Path);out=a.parse_args().output
source=ROOT/'analysis/research/runs/sx10_qualification_v1';records=[]
for name in ['receipt.json','sample_crosswalk.csv','stdout.log','stderr.log']:
    data=(source/name).read_bytes();dest='failed_'+name
    with (out/dest).open('xb') as f:f.write(data)
    records.append(dict(source=(source/name).relative_to(ROOT).as_posix(),archive=dest,sha256=hashlib.sha256(data).hexdigest()))
assert json.loads((out/'failed_receipt.json').read_text())['status']=='execution_failed'
(out/'preservation.json').write_text(json.dumps({'original_status':'execution_failed','purpose':'Exact archival preservation only; no scientific success or acceptance','files':records},indent=2)+'\n',encoding='utf-8',newline='\n')
