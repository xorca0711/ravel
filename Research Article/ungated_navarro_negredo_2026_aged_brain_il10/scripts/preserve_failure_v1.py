"""Archive the actual failed run byte-for-byte; do not relabel it as executed."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
source=Path('raw_data/navarro_2026/failed_metadata_v1')
out=Path(a.output);dest=out/'failed_v1';dest.mkdir()
receipt=json.loads((source/'receipt.json').read_text())
assert receipt['status']=='execution_failed' and receipt['exit_code']==1
assert receipt['analysis_id']=='Nn26-P01.rds_metadata_v1'
records=[]
for name in ['receipt.json','load_status.json','resource_usage.json','stdout.log','stderr.log']:
    original=source/name;target=dest/name
    shutil.copyfile(original,target)
    digest=hashlib.sha256(original.read_bytes()).hexdigest()
    assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
    records.append({'file':name,'sha256':digest,'size_bytes':original.stat().st_size})
(out/'failure_archive_manifest.json').write_text(json.dumps({
    'archived_status':'execution_failed','original_run_id':'nn26_rds_metadata_v1',
    'original_freeze_commit':receipt['git_commit'],'files':records,
    'operation':'Byte-for-byte preservation of failure, not successful biological execution.',
    'original_receipt_rewritten':False},indent=2)+'\n')
