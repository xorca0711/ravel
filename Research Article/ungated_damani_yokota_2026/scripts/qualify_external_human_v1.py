"""Qualify existing external donor aggregates without expression fitting."""
import argparse,gzip,hashlib,json,time
from pathlib import Path
import numpy as np
import pandas as pd

RAW=Path('raw_data/DY1_human_external_v1')

def raw_aggregate(path,cell_units,source_genes,symbols,n_units):
    lookup=np.array([symbols.index(g) if g in symbols else -1 for g in source_genes])
    selected=np.zeros((n_units,len(symbols)),dtype=np.int64);totals=np.zeros(n_units,dtype=np.int64)
    seen=0;start=time.monotonic()
    with gzip.open(path,'rt') as stream:
        if next(stream).strip()!='%%MatrixMarket matrix coordinate integer general':raise ValueError('Matrix convention changed')
        line=next(stream)
        while line.startswith('%'):line=next(stream)
        ng,nc,nnz=map(int,line.split())
        if (ng,nc)!=(len(source_genes),len(cell_units)):raise ValueError('Matrix dimensions changed')
        for chunk in pd.read_csv(stream,sep=r'\s+',header=None,names=['g','c','v'],dtype=np.int64,chunksize=2_000_000):
            g=chunk.g.to_numpy()-1;c=chunk.c.to_numpy()-1;v=chunk.v.to_numpy()
            if g.min()<0 or g.max()>=ng or c.min()<0 or c.max()>=nc or v.min()<=0 or v.max()>=2**31:raise ValueError('Invalid matrix entry')
            u=cell_units[c];keep=u>=0
            totals+=np.bincount(u[keep],weights=v[keep],minlength=n_units).astype(np.int64)
            target=lookup[g];keep=keep&(target>=0)
            np.add.at(selected,(u[keep],target[keep]),v[keep])
            seen+=len(chunk)
            if seen%40_000_000==0:print(json.dumps({'matrix_entries':seen,'total_entries':nnz,'seconds':round(time.monotonic()-start,1)}),flush=True)
    if seen!=nnz:raise ValueError('Matrix entry count mismatch')
    return selected,totals,seen

def main(out):
    meta=pd.read_csv(RAW/'GSE135893_IPF_metadata.csv.gz',dtype={'Sample_Name':str})
    meta=meta.rename(columns={meta.columns[0]:'barcode'})
    with gzip.open(RAW/'GSE135893_barcodes.tsv.gz','rt') as stream:barcodes=[line.strip() for line in stream]
    if meta.barcode.duplicated().any() or len(set(barcodes))!=len(barcodes) or not set(meta.barcode)<=set(barcodes):raise ValueError('External barcode identity conflict')
    if (meta.groupby('Sample_Name').Diagnosis.nunique()!=1).any():raise ValueError('External donor diagnosis conflict')
    donor=meta.groupby(['Sample_Name','Diagnosis','Sample_Source'],dropna=False).agg(n_cells=('barcode','size'),n_libraries=('orig.ident','nunique')).reset_index()
    units=pd.read_csv(RAW/'GSE135893_subtypes_units.csv',dtype={'donor':str})
    data=np.load(RAW/'GSE135893_subtypes.npz',allow_pickle=False);counts=data['counts'];genes=data['genes']
    prep=json.loads(Path('analysis/corrections/statistics/GSE135893_subtypes_preparation.json').read_text())
    if counts.shape!=(len(units),len(genes)) or (counts<0).any() or not np.issubdtype(counts.dtype,np.integer):raise ValueError('Invalid external aggregate array')
    if int(counts.sum())!=prep['total_counts'] or len(units)!=prep['n_units'] or len(genes)!=prep['n_genes']:raise ValueError('Historical aggregate dimensions/totals mismatch')
    with Path('analysis/corrections/statistics/prepare_counts.py').open('rb') as stream:code_hash=hashlib.file_digest(stream,'sha256').hexdigest()
    if code_hash!=prep['preparation_code_sha256']:raise ValueError('Historical preparation code changed')
    # Compare the existing independent serialization before reusing the binary aggregate.
    csv_counts=pd.read_csv(RAW/'GSE135893_subtypes_counts.csv.gz',index_col=0)
    if not np.array_equal(csv_counts.index.astype(str),genes.astype(str)) or not np.array_equal(csv_counts.columns,units.unit_id) or not np.array_equal(csv_counts.to_numpy().T,counts):raise ValueError('Saved aggregate serializations disagree')
    audits=[]
    for i,row in units.iterrows():
        selection=meta[(meta.Sample_Name==row.donor)&(meta.celltype==row.label)]
        diagnosis='Control' if row.disease=='control' else row.disease
        if len(selection)!=row.cells or set(selection.Diagnosis)!={diagnosis}:raise ValueError('External cell-count/diagnosis join mismatch')
        observed=int(counts[i].sum());rna=int(selection.nCount_RNA.sum());sct=int(selection.nCount_SCT.sum())
        audits.append({'donor':row.donor,'label':row.label,'compartment':row.comp,'disease':diagnosis,'cells':row.cells,
                       'aggregate_total':observed,'metadata_RNA_total':rna,'metadata_SCT_total':sct,
                       'matches_RNA':observed==rna,'matches_SCT':observed==sct})
    audit=pd.DataFrame(audits)
    # Exact source gene symbols; no orthologue or annotation substitution.
    primary=json.loads(Path('Research Article/gate2_DY1_damani_yokota_2026/config/human_panels_v1.json').read_text())
    mapping=pd.DataFrame([{'symbol':s,'cache_matches':int((genes==s).sum()),'orthology':'native_human'} for s in primary['symbols']])
    source_genes=pd.read_csv(RAW/'GSE135893_genes.tsv.gz',header=None)[0].astype(str).tolist()
    unit_map={(r.donor,r.label):i for i,r in units.iterrows()}
    if len(unit_map)!=len(units):raise ValueError('Duplicate donor-label aggregate')
    barcode_units={r.barcode:unit_map.get((r.Sample_Name,r.celltype),-1) for r in meta.itertuples()}
    cell_units=np.array([barcode_units.get(b,-1) for b in barcodes],dtype=np.int32)
    direct,totals,nnz=raw_aggregate(RAW/'GSE135893_matrix.mtx.gz',cell_units,source_genes,primary['symbols'],len(units))
    if nnz!=prep['nnz_read']:raise ValueError('Historical raw entry count changed')
    np.savez_compressed(out/'direct_selected_counts.npz',counts=direct,totals=totals,symbols=np.array(primary['symbols']),unit_ids=units.unit_id.to_numpy(dtype=str))
    selected_match=all(np.array_equal(direct[:,j],counts[:,np.flatnonzero(genes==s)[0]]) for j,s in enumerate(primary['symbols']) if (genes==s).sum()==1)
    audit['matches_current_raw_total']=totals==counts.sum(axis=1)
    for name,table in [('donor_coverage.tsv',donor),('aggregate_audit.tsv',audit),('gene_mapping.tsv',mapping)]:table.to_csv(out/name,sep='\t',index=False,lineterminator='\n')
    summary={'source':'GSE135893','donors_by_diagnosis':donor.Diagnosis.value_counts().to_dict(),'source_libraries':int(meta['orig.ident'].nunique()),
             'metadata_cells':len(meta),'matrix_barcodes':len(barcodes),'unannotated_matrix_columns':len(barcodes)-len(meta),
             'cached_units':len(units),'cached_labels_by_compartment':{c:sorted(g.label.unique()) for c,g in units.groupby('comp')},
             'all_cache_units_match_nCount_RNA':bool(audit.matches_RNA.all()),'all_cache_units_match_nCount_SCT':bool(audit.matches_SCT.all()),
             'aggregate_serializations_and_historical_totals_match':True,'preparation_code_hash_verified':True,
             'all_requested_symbols_unique':bool((mapping.cache_matches==1).all()),
             'all_selected_gene_aggregates_match_current_raw':bool(selected_match),'all_aggregate_totals_match_current_raw':bool(audit.matches_current_raw_total.all()),'raw_matrix_entries_verified':nnz,
             'published_independence_evidence':'Habermann2020 final Results describes Adams companion as an entirely separate dataset/pipeline; collection VUMC/NTI. This is published evidence, not a direct patient identity audit.',
             'eligibility':'aggregate RNA description candidate' if audit.matches_RNA.all() and (mapping.cache_matches==1).all() and selected_match and audit.matches_current_raw_total.all() else 'hold: resolve assay or gene mapping',
             'limits':['Historical raw matrix did not have a recorded cryptographic hash; the current raw file is hash-bound and all selected genes plus all-gene unit totals are independently reaggregated and compared. This does not retroactively establish the old raw file hash.',
                       'Cached compartments required at least50cells/donor upstream; below-floor expression is unavailable in this cache.',
                       'Source cell annotations differ; no exact human NAM/marker-proxy reproduction or COPD comparison is available here.',
                       'Other fibrosis diagnoses must not be relabeled IPF. No expression effect has been fitted in this qualification.'],
             'scientific_acceptance':'not_assessed'}
    (out/'qualification.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
