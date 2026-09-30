"""Retrieve frozen input; optionally restore inspected public literature payloads."""
from pathlib import Path
import argparse,hashlib,json,urllib.request
BASE=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--literature',action='store_true');args=p.parse_args()
records=json.loads((BASE/'metadata/intake.json').read_text());out=[]
for r in records:
 if r['status']!='retrieved' or r.get('method'):continue
 if r['file']!='ng2019_expression.tsv' and not args.literature:continue
 path=BASE/'cache'/r['file'];path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  data=urllib.request.urlopen(r['url'],timeout=60).read()
  assert hashlib.sha256(data).hexdigest()==r['sha256'], 'Public payload changed; record/version intake before analysis: '+r['file']
  path.write_bytes(data)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
 out.append(r['file'])
print('Verified cached inputs: '+', '.join(out))
