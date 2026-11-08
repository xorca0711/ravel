"""Register exact input manifests as configuration; verify existing identity/receipt joins."""
import argparse,csv,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'Research Article/ungated_peng_2026_spatial_omics'

def main(out):
    with (ROOT/'analysis/research/runs/Pg1_metadata_v3_20261108/samples.csv').open(newline='',encoding='utf-8') as f:geo=list(csv.DictReader(f))
    lookup={r['GSM']:r for r in geo};assert len(lookup)==len(geo)
    checks=1;rows=[]
    jobs=[('public_cells_manifest_v1.json','libraries','GSE308103',75,'A12_public_cells_v1_20261108'),('public_spatial_manifest_v1.json','sections','GSE307534',56,'Pg1_public_spatial_v3_20261108')]
    for filename,key,study,n,run in jobs:
        manifest=json.loads((PAPER/'sources'/filename).read_text());receipt=json.loads((ROOT/'analysis/research/runs'/run/'receipt.json').read_text())
        assert receipt['status']=='executed';checks+=1
        inputs={x['path']:x for x in receipt['inputs']};items=manifest[key]
        assert len(items)==n and len({x['gsm'] for x in items})==n;checks+=1
        assert {x['gsm'] for x in items}=={x['GSM'] for x in geo if x['GSE']==study};checks+=1
        for item in items:
            source=lookup[item['gsm']]
            assert source['GSE']==study and int(source['patient_id_author'])==int(item['patient']);checks+=1
            assert source['histology_deposited'].casefold()==item['histology'].casefold();checks+=1
            paths=set()
            for f in item['files']:
                assert f['path'] not in paths;paths.add(f['path']);checks+=1
                assert re.fullmatch('[0-9a-f]{64}',f['sha256']);checks+=1
                assert inputs[f['path']]['sha256']==f['sha256'] and inputs[f['path']]['study_id']==study;checks+=1
                assert inputs[f['path']]['unit_ids']==[item['patient']];checks+=1
                original=Path(f['source_repository_path']);local=Path(f['path'])
                assert original.parent.name==local.parent.name==item['gsm'] and original.name==local.name;checks+=1
                rows.append(dict(study=study,gsm=item['gsm'],patient=item['patient'],histology=item['histology'],GEO_record_id=source['record_id'],manifest=filename,path=f['path'],source_repository_path=f['source_repository_path'],sha256=f['sha256'],verified_run=run,join_level='deposited library; no exact block/section or genotype claim'))
    with (out/'source_bindings.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'verification.json').write_text(json.dumps({'checks':checks,'failures':[],'libraries_or_sections':131,'source_files':len(rows),'method':'Exact manifest identities against prior qualified GEO records and immutable successful runner input hashes; no matrix reanalysis or new independence claim'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();main(args.output)
