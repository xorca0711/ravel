"""Byte-preserve diagnostic and source records; no biological computation."""
import argparse,hashlib,json,shutil
from pathlib import Path

FAILED=Path('analysis/research/runs/DY1_external_human_qualification_v1')
SOURCE=Path('Research Article/gate2_DY1_damani_yokota_2026/source_metadata/external_human_v1')
SOURCES=['independent_human_candidates.json','GSE135893_candidate.txt','GSE122960_candidate.txt','GSE135893_readme_for_ILD_annotated_fullsize.rds.txt']

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main(out):
    receipt=json.loads((FAILED/'receipt.json').read_text())
    if receipt['status']!='execution_failed' or receipt['exit_code']!=1 or receipt['outputs']!=[]:raise ValueError('Original failure identity changed')
    if set(p.name for p in FAILED.iterdir())!={'receipt.json','stdout.log','stderr.log'}:raise ValueError('Unexpected failed-run files: preserve every file explicitly')
    if 'Historical preparation code changed' not in (FAILED/'stderr.log').read_text():raise ValueError('Failure cause changed')
    records=json.loads((SOURCE/'independent_human_candidates.json').read_text())
    if {r['accession'] for r in records}!={'GSE135893','GSE122960'}:raise ValueError('Discovery accession set changed')
    pairs=[(FAILED/'receipt.json','failed_receipt.json'),(FAILED/'stdout.log','failed_stdout.log'),(FAILED/'stderr.log','failed_stderr.log')]+[(SOURCE/name,name) for name in SOURCES]
    mapping=[]
    for src,name in pairs:
        before=digest(src);shutil.copyfile(src,out/name)
        if before!=digest(out/name) or before!=digest(src):raise ValueError('Byte preservation failed')
        mapping.append(dict(original_path=src.as_posix(),archive_file=name,sha256=before,bytes=src.stat().st_size))
    record=dict(original_status='execution_failed',archive_status='byte_preservation_verified',preserved_files=len(mapping),original_failure_commit='9982774',discovery_copy_commit='d4ee3cb',files=mapping,interpretation='Success applies only to exact archival copying. Failed qualification remains failed; source discovery is not an assay or biological result. Original local bytes and Git history remain preserved. No validator changes or scientific acceptance.')
    (out/'preservation.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'preserved_files':len(mapping),'original_status':'execution_failed','archive_status':'byte_preservation_verified'}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
