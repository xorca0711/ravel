"""Acquire only the public fibroblast subset of the nominated independent atlas."""
from datetime import datetime, timezone
import hashlib
import urllib.request
from common import PACKAGE, REPO, read_json, write_json


if __name__=='__main__':
    cache=REPO/'raw_data/travaglini_nabhan_2020/external'
    collection=read_json(cache/'madissoon_collection.json')
    item=next(d for d in collection['datasets'] if d['dataset_id']=='e871881f-b42d-4500-906d-0972a14ba47d')
    asset=next(a for a in item['assets'] if a['filetype']=='H5AD')
    path=cache/(item['dataset_version_id']+'.h5ad');partial=path.with_suffix('.h5ad.part')
    if path.exists() or partial.exists():raise ValueError('External payload exists; inspect/reuse instead of overwriting')
    digest=hashlib.sha256();size=0
    with urllib.request.urlopen(asset['url'],timeout=90) as response,partial.open('xb') as handle:
        while block:=response.read(4*1024*1024):
            handle.write(block);digest.update(block);size+=len(block)
            if size>asset['filesize']:raise ValueError('Unexpected file size')
    if size!=asset['filesize']:raise ValueError('Incomplete transfer')
    partial.rename(path)
    record={'schema':'TN2020-external-source/v1','doi':'10.1038/s41588-022-01243-4','collection_id':collection['collection_id'],'dataset_id':item['dataset_id'],'dataset_version_id':item['dataset_version_id'],'title':item['title'],'url':asset['url'],'cache_path':path.relative_to(REPO).as_posix(),'sha256':digest.hexdigest(),'bytes':size,'cells_reported':item['cell_count'],'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'selection':'Fibroblast subset chosen by published study, compartment and explicit source follow-up; no external expression effects inspected before acquisition'}
    out=PACKAGE/'config/external_source_v1.json'
    if out.exists():raise ValueError('External manifest exists')
    write_json(out,record);print(f'External fibroblasts: {size} bytes, {item["cell_count"]} cells/nuclei reported.')
