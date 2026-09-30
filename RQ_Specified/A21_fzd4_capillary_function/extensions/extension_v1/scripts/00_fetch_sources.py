"""Restore immutable publisher source archives; parent script restores RNA matrices."""
from pathlib import Path
import hashlib,json,urllib.request
BASE=Path(__file__).resolve().parents[1]
needed={'44321_2024_64_MOESM4_ESM.zip','44321_2024_64_MOESM8_ESM.zip','44321_2024_64_MOESM1_ESM.pdf'}
for rec in json.loads((BASE/'metadata/intake.json').read_text()):
 if rec['file'] not in needed or rec['status']!='retrieved':continue
 path=BASE/'cache'/rec['file'];path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  temp=path.with_suffix(path.suffix+'.part')
  with urllib.request.urlopen(rec['url'],timeout=60) as source,temp.open('wb') as dest:
   for block in iter(lambda:source.read(1024*1024),b''):dest.write(block)
  assert hashlib.sha256(temp.read_bytes()).hexdigest()==rec['sha256'],'Changed source: version intake before analysis'
  temp.replace(path)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==rec['sha256']
 print('Verified '+path.name)
