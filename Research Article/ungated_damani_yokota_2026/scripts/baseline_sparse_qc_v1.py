"""Technical integrity of two baseline triplets; no cell/tag assignments or contrasts."""
import argparse,csv,gzip,hashlib,json,time
from pathlib import Path
import numpy as np
import pandas as pd

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')

def read_labels(features,barcodes):
    with gzip.open(features,'rt',newline='') as f:rows=list(csv.reader(f,delimiter='\t'))
    if any(len(r)!=3 or not all(r) for r in rows):raise ValueError('Invalid feature row')
    with gzip.open(barcodes,'rt') as f:bars=[line.strip() for line in f]
    if not all(bars) or len(bars)!=len(set(bars)):raise ValueError('Empty or duplicate barcode')
    if len({(r[0],r[2]) for r in rows})!=len(rows):raise ValueError('Duplicate feature identity within type')
    kinds=sorted({r[2] for r in rows})
    if kinds!=['Antibody Capture','Gene Expression']:raise ValueError('Unexpected feature-type set')
    tags={i:r[0] for i,r in enumerate(rows) if r[2]=='Antibody Capture'}
    return np.array([kinds.index(r[2]) for r in rows],dtype=np.int8),len(bars),kinds,tags

def audit_matrix(path,type_codes,n_cells,kinds,chunksize=2_000_000,tag_features=None):
    n_features=len(type_codes);n_types=len(kinds);entries=[0]*n_types;counts=[0]*n_types;seen=0;checks=0;start=time.monotonic()
    tag_features=tag_features or {};tag_indices=sorted(tag_features);positive=np.zeros((len(tag_indices),n_cells),dtype=bool)
    tag_counts=[0]*len(tag_indices);tag_entries=[0]*len(tag_indices);tag_max=[0]*len(tag_indices);tag_sets=[set() for _ in tag_indices]
    with gzip.open(path,'rt') as f:
        if next(f).strip()!='%%MatrixMarket matrix coordinate integer general':raise ValueError('Unexpected MatrixMarket convention')
        line=next(f)
        while line.startswith('%'):line=next(f)
        nf,nc,declared=map(int,line.split())
        if (nf,nc)!=(n_features,n_cells):raise ValueError('Matrix dimension/label mismatch')
        for chunk in pd.read_csv(f,sep=r'\s+',header=None,dtype=np.int64,chunksize=chunksize):
            if chunk.shape[1]!=3:raise ValueError('Matrix entry must have exactly three fields')
            chunk.columns=['feature','barcode','count']
            g=chunk.feature.to_numpy()-1;c=chunk.barcode.to_numpy()-1;v=chunk['count'].to_numpy()
            if g.min()<0 or g.max()>=nf or c.min()<0 or c.max()>=nc:raise ValueError('Coordinate out of bounds')
            if v.min()<=0 or v.max()>=2**31:raise ValueError('Count not a positive supported integer')
            t=type_codes[g]
            by_type=chunk.assign(kind=t).groupby('kind')['count'].agg(['size','sum'])
            for k in range(n_types):
                mask=t==k;ne=int(mask.sum());total=int(v[mask].sum(dtype=np.int64))
                other_n=int(by_type.loc[k,'size']) if k in by_type.index else 0;other_total=int(by_type.loc[k,'sum']) if k in by_type.index else 0
                if (ne,total)!=(other_n,other_total):raise ValueError('Independent type-accounting mismatch')
                checks+=2;entries[k]+=ne;counts[k]+=total
            for j,index in enumerate(tag_indices):
                mask=g==index;values=v[mask];cells=c[mask]
                tag_counts[j]+=int(values.sum(dtype=np.int64));tag_entries[j]+=len(values)
                if len(values):tag_max[j]=max(tag_max[j],int(values.max()))
                positive[j,cells]=True;tag_sets[j].update(cells.tolist())
            seen+=len(chunk)
            if seen%20_000_000==0:print(json.dumps({'file':path.name,'stored_entries':seen,'declared_entries':declared,'seconds':round(time.monotonic()-start,1)}),flush=True)
    if seen!=declared or sum(entries)!=declared:raise ValueError('Declared entry count mismatch')
    rows=[dict(file=path.name,feature_type=kind,feature_rows=int((type_codes==k).sum()),stored_entries=entries[k],count_sum=counts[k]) for k,kind in enumerate(kinds)]
    tags=[]
    for j,index in enumerate(tag_indices):
        unique=int(positive[j].sum())
        if unique!=len(tag_sets[j]):raise ValueError('Independent tag-barcode accounting mismatch')
        checks+=1
        tags.append(dict(file=path.name,tag_feature_id=tag_features[index],stored_entries=tag_entries[j],raw_count_sum=tag_counts[j],positive_unique_barcodes=unique,max_stored_entry=tag_max[j],duplicate_stored_tag_coordinates=tag_entries[j]-unique))
    if tag_indices and (sum(tag_counts)!=counts[kinds.index('Antibody Capture')] or sum(tag_entries)!=entries[kinds.index('Antibody Capture')]):raise ValueError('Tag/type accounting mismatch')
    return dict(file=path.name,features=n_features,barcodes=n_cells,barcode_unique=True,declared_entries=declared,observed_entries=seen,positive_integer_and_bounds_checks=True,total_stored_count=sum(counts),accounting_checks=checks),rows,tags

def write(out,name,rows):
    with (out/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

def main(out):
    manifest=json.loads((ARTICLE/'config/baseline_sparse_qc_inputs_v1.json').read_text());libraries=[];accounting=[];tag_inventory=[]
    for item in manifest['libraries']:
        for entry in item['files'].values():
            with Path(entry['path']).open('rb') as f:current=hashlib.file_digest(f,'sha256').hexdigest()
            if current!=entry['sha256']:raise ValueError('Input hash changed')
        codes,nc,kinds,tags=read_labels(Path(item['files']['features']['path']),Path(item['files']['barcodes']['path']))
        r,a,t=audit_matrix(Path(item['files']['matrix']['path']),codes,nc,kinds,tag_features=tags)
        if [r['features'],r['barcodes'],r['declared_entries']]!=item['source_v1_dimensions']:raise ValueError('Historical header dimensions changed')
        libraries.append(r);accounting.extend(a);tag_inventory.extend(t)
        write(out,'libraries.tsv',libraries);write(out,'feature_type_accounting.tsv',accounting);write(out,'cmo_signal_inventory.tsv',tag_inventory)
    verification=dict(ok=True,aggregate_checks=sum(r['accounting_checks'] for r in libraries),method='Numpy mask/integer sums compared per chunk with pandas groupby size/sum; feature/barcode dimensions checked independently of coordinates; tag barcode Boolean occupancy versus sets; one sparse-input parsing pass.',limit='Independent arithmetic on a shared parser and same source; no independent biology or cell assignment. Duplicate stored tag coordinates counted; Gene Expression coordinate duplication not audited.')
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    summary=dict(analysis_id='DY1-P01.baseline_sparse_qc_v1',libraries=len(libraries),stored_entries=sum(r['observed_entries'] for r in libraries),scope='Baseline host-file integrity and per-source CMO signal inventory in the full N.brasiliensis-history/later-IAV-challenge study. No gene/tag ranking, thresholds, cell assignment, biological subsetting or contrast.',inference_limit='Nonzero antibody-tag counts do not establish assigned conditions or animal/pool identities. Barcode uniqueness and tag IDs are library-local. Tag totals sum all stored entries; positive barcode counts deduplicate coordinates; maximum is the maximum stored entry, not a per-cell aggregate. Gene Expression entries are not certified unique coordinates.',scientific_acceptance='not_assessed')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
