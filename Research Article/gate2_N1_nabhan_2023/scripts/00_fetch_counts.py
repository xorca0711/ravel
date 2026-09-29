"""Restore missing public bulk counts/annotation against the recorded source hashes."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT=Path(__file__).resolve().parents[1]


def main():
    records=json.loads((ROOT/'metadata/count_download_manifest.json').read_text())['files']
    annotation=next(r for r in json.loads((ROOT/'metadata/additional_source_intake.json').read_text()) if r['name'].endswith('.gtf.gz'))
    records=records+[dict(annotation,path='raw/'+annotation['name'])]
    restored=0
    for row in records:
        path=ROOT/row['path'];path.parent.mkdir(exist_ok=True)
        if path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],f'Existing source hash differs: {path}'
            continue
        with urllib.request.urlopen(row['url'],timeout=90) as response: data=response.read()
        assert hashlib.sha256(data).hexdigest()==row['sha256'],'Remote content changed; do not overwrite source contract'
        path.write_bytes(data);restored+=1
    print(f'PASS: {len(records)} source hashes; {restored} missing files restored')


if __name__=='__main__':main()
