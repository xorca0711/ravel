"""Preserve the actual failed WSL launch byte-for-byte without changing its status."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main(contract_path, output):
    root=Path(__file__).resolve().parents[3]
    contract=json.loads(contract_path.read_text())
    receipt_path=next(root/x['path'] for x in contract['inputs'] if x['path'].endswith('/receipt.json'))
    receipt=json.loads(receipt_path.read_text())
    assert receipt['status']=='execution_failed' and receipt['exit_code']==1
    assert receipt['analysis_id']=='Nk17-P01.s6c_d180_proxy_v1'
    assert not (receipt_path.parent/'header_metadata.json').exists()
    assert not (receipt_path.parent/'window_signal.tsv.gz').exists()
    target_dir=output/'failed_launch_v1';target_dir.mkdir()
    records=[]
    for item in contract['inputs']:
        source=root/item['path'];target=target_dir/source.name
        assert not target.exists()
        shutil.copyfile(source,target)
        original_hash=hashlib.sha256(source.read_bytes()).hexdigest()
        assert original_hash==item['sha256']==hashlib.sha256(target.read_bytes()).hexdigest()
        records.append(dict(original_source=item['path'],archived_file='failed_launch_v1/'+source.name,
                            sha256=original_hash,bytes=source.stat().st_size))
    manifest=dict(archived_status='execution_failed',original_run_id='naik2017_s6c_d180_proxy_v1',
        original_freeze_commit=receipt['git_commit'],original_receipt_rewritten=False,files=records,
        failure='Sandbox Wsl/E_ACCESSDENIED; UTF-16 error output triggered UTF-8 decoding failure at wslpath launch',
        research_window_values_read=False,headers_read=False,
        retry='Same frozen code/contract/inputs, new run ID naik2017_s6c_d180_proxy_v1_retry1 using approved local WSL access',
        operation='Byte-preserving failure archival; not a successful D180 scientific execution')
    (output/'failure_archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='preserved_failed_launch',files=len(records),original_status=receipt['status'])),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--contract',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.contract,a.output)
