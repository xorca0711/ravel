"""Restore hash-verified public inputs; source payloads stay in ignored cache."""
from pathlib import Path
import argparse,hashlib,json,urllib.request
BASE=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--literature',action='store_true');args=p.parse_args()
primary={'GSE211335_RAW.tar','godoy_samples.txt.gz','godoy_endothelial_metadata.csv.gz'}
records=json.loads((BASE/'metadata/intake.json').read_text())
for r in records:
 if r['status']!='retrieved' or (not args.literature and r['file'] not in primary):continue
 path=BASE/'cache'/r['file'];path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  with urllib.request.urlopen(r['url'],timeout=60) as src,path.open('wb') as dest:
   for block in iter(lambda:src.read(1024*1024),b''):dest.write(block)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'],r['file']+' changed; version the intake before proceeding'
 print('Verified '+r['file'])

# Restore only the three verified named matrix members needed by the audit.
import tarfile
expected={r['file']:r['sha256'] for r in json.loads((BASE/'metadata/matrix_manifest.json').read_text())}
with tarfile.open(BASE/'cache/GSE211335_RAW.tar') as tar:
 assert {m.name for m in tar.getmembers()}==set(expected)
 for member in tar.getmembers():
  assert Path(member.name).name==member.name
  path=BASE/'cache'/member.name
  if not path.exists():path.write_bytes(tar.extractfile(member).read())
  assert hashlib.sha256(path.read_bytes()).hexdigest()==expected[member.name]
print('Verified three matrix members.')
