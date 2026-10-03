"""Preserve a failed run byte-for-byte; success refers only to archival copying."""
from pathlib import Path
import argparse,json,hashlib,shutil

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
    src=Path('analysis/research/runs/nb5_metadata_v1');names=['animals.tsv','cell_metadata.tsv','coverage.tsv','published_coverage.tsv','receipt.json','stderr.log','stdout.log'];mapping=[]
    assert json.loads((src/'receipt.json').read_text())['status']=='execution_failed'
    for name in names:
        target={'receipt.json':'failed_receipt.json','stdout.log':'failed_stdout.log','stderr.log':'failed_stderr.log'}.get(name,name)
        before=hashlib.sha256((src/name).read_bytes()).hexdigest();shutil.copyfile(src/name,out/target);after=hashlib.sha256((out/target).read_bytes()).hexdigest();assert before==after
        mapping.append({'original_path':(src/name).as_posix(),'archive_file':target,'sha256':after})
    (out/'preservation.json').write_text(json.dumps({'original_status':'execution_failed','archive_status':'byte_preservation_verified','original_run':'nb5_metadata_v1','reason':'Existing registry accepts successful receipts only. This successful archival receipt does not validate the failed scientific run. Original local files remain unchanged; archived copies and source commit preserve every byte.','files':mapping},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'preserved_files':len(mapping),'original_status':'execution_failed'}))

if __name__=='__main__':main()
