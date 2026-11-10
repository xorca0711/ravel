"""Publish byte-identical failed-run evidence without reporting failed science as successful."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
run_ids=['zh26_s0_qualification_v1','zh26_s0_qualification_v2','zh26_s3_block_v1','zh26_s2_enrichment_v1']
records=[]
for run_id in run_ids:
    source=Path('analysis/research/runs')/run_id
    receipt=json.loads((source/'receipt.json').read_text())
    assert receipt['status']=='execution_failed' and receipt['owner']=='Zh26-P01'
    target=out/run_id;target.mkdir()
    for original in sorted(source.iterdir()):
        assert original.is_file()
        dest=target/original.name;shutil.copyfile(original,dest)
        digest=hashlib.sha256(original.read_bytes()).hexdigest()
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
        records.append({'original_path':original.as_posix(),'archive_path':dest.relative_to(out).as_posix(),
                        'sha256':digest,'bytes':original.stat().st_size,
                        'original_status':receipt['status'],'original_freeze_commit':receipt['git_commit']})
(out/'archive_manifest.json').write_text(json.dumps({'operation':'Byte-preserving metadata archive, not successful biological execution.',
    'failed_runs':run_ids,'original_receipts_rewritten':False,'files':records},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'failed_runs_archived':len(run_ids),'exact_file_copies':len(records)}))
