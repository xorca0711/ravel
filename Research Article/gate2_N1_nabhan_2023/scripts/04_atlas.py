"""Frozen descriptive receptor audit; cells are aggregated to source sample x label.

Stream existing counts once. Do not integrate studies or reinterpret author labels.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.special import gammaln

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'trials/atlas_v1'
GENES = [f'Fzd{i}' for i in range(1,11)] + ['Lrp5','Lrp6','Axin2','Il1r1',
 'Cthrc1','Lrrc15','Col1a1','Col3a1','Ccn1','Ccn2','Amotl2','Tgfb2','Sftpc',
 'Etv5','Ager','Hopx','Krt8','Krt17','Krt5','Scgb1a1','Scgb3a2','Foxj1',
 'Pecam1','Emcn','Car4','Ednrb','Aplnr','Kit','Wnt2','Wnt5a','Wnt7b']


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''): h.update(b)
    return h.hexdigest()


def write(tab,name):
    tab.to_csv(OUT/'tables'/name,sep='\t',index=False)


def mapping(symbols,human):
    symbols=pd.Index(symbols)
    assert symbols.is_unique
    aliases={'CCN1':'CYR61','CCN2':'CTGF'} if human else {'Ccn1':'Cyr61','Ccn2':'Ctgf'}
    records=[]
    for g in GENES:
        query=g.upper() if human else g
        mapped=query if query in symbols else aliases.get(query,query)
        records.append(dict(gene=g,source_symbol=mapped,index=int(symbols.get_indexer([mapped])[0])))
    return pd.DataFrame(records)


def human_counts(base):
    p=base/'raw_data/GSE135893'
    symbols=pd.read_csv(p/'GSE135893_genes.tsv.gz',header=None,sep='\t')[0]
    barcodes=pd.read_csv(p/'GSE135893_barcodes.tsv.gz',header=None,sep='\t')[0]
    meta=pd.read_csv(p/'GSE135893_IPF_metadata.csv.gz').rename(columns={'Unnamed: 0':'barcode'})
    assert meta.barcode.is_unique and barcodes.is_unique and set(meta.barcode)<=set(barcodes)
    annotated=barcodes.isin(meta.barcode).to_numpy()
    meta=meta.set_index('barcode').loc[barcodes[annotated]].reset_index()
    match=mapping(symbols,True);write(match,'human_gene_mapping.tsv')
    lookup=np.full(len(symbols),-1,dtype=int)
    for j,row in match.iterrows():
        if row['index']>=0: lookup[row['index']]=j
    x=np.zeros((len(barcodes),len(GENES)),dtype=np.int64);tot=np.zeros(len(barcodes),dtype=np.int64)
    nnz=0
    with gzip.open(p/'GSE135893_matrix.mtx.gz','rt') as f:
        line=f.readline()
        assert 'coordinate' in line and 'integer' in line
        while True:
            line=f.readline()
            if not line.startswith('%'): break
        ng,nc,expected=map(int,line.split());assert (ng,nc)==(len(symbols),len(barcodes))
        for chunk in pd.read_csv(f,sep=' ',header=None,names=['g','c','n'],dtype=np.int64,chunksize=2_000_000):
            g=chunk.g.to_numpy()-1;c=chunk.c.to_numpy()-1;n=chunk.n.to_numpy()
            assert n.min()>0 and g.min()>=0 and g.max()<ng and c.min()>=0 and c.max()<nc
            tot+=np.bincount(c,weights=n,minlength=nc).astype(np.int64)
            ix=lookup[g];ok=ix>=0;np.add.at(x,(c[ok],ix[ok]),n[ok]);nnz+=len(chunk)
    assert nnz==expected
    # Source RNA depth is an independent alignment check, not our denominator.
    unannotated=int((~annotated).sum());tot=tot[annotated];x=x[annotated]
    assert np.array_equal(tot,meta.nCount_RNA.to_numpy()),'Matrix/metadata depths differ'
    meta=pd.DataFrame(dict(unit=meta.Sample_Name,condition=meta.Diagnosis,state=meta.celltype.str.strip(),
        lineage=meta.population.str.strip(),day='not_applicable',doublet=False,eligible=True))
    return meta,x,tot,match,dict(matrix_cells=nc,cells=len(meta),unannotated_excluded=unannotated,genes=ng,nonzeros=nnz,metadata_depth_match=True)


def mouse_counts(base):
    path=base/'Research Article/gate1_01_niethamer_2025/GSE262927/processed/final_clustered.h5ad'
    a=ad.read_h5ad(path,backed='r');obs=a.obs.copy();match=mapping(a.var.gene_symbol,False)
    write(match,'mouse_gene_mapping.tsv');nc,ng=a.shape;a.file.close()
    x=np.zeros((nc,len(GENES)),dtype=np.int64);tot=np.zeros(nc,dtype=np.int64)
    valid=match['index']>=0;idx=match.loc[valid,'index'].to_numpy()
    with h5py.File(path,'r') as f:
        layer=f['layers/counts'];assert layer.attrs['encoding-type']=='csr_matrix'
        ptr=layer['indptr'][:]
        for start in range(0,nc,4096):
            stop=min(start+4096,nc);lo,hi=ptr[start],ptr[stop]
            values=layer['data'][lo:hi];assert np.all(values>=0) and np.equal(values,np.floor(values)).all()
            block=sparse.csr_matrix((values,layer['indices'][lo:hi],ptr[start:stop+1]-lo),shape=(stop-start,ng))
            tot[start:stop]=np.asarray(block.sum(axis=1)).ravel().astype(np.int64)
            x[start:stop,valid]=block[:,idx].toarray().astype(np.int64)
    valid_labels=~obs.author_celltype.astype(str).isin(['NA','nan','None','unannotated'])
    meta=pd.DataFrame(dict(unit=obs.sample_id.astype(str).to_numpy(),condition=obs.condition.astype(str).to_numpy(),
         state=obs.author_celltype.astype(str).to_numpy(),lineage=obs.author_lineage.astype(str).to_numpy(),
         day=obs.sacrifice_day.to_numpy(),doublet=obs.predicted_doublet.to_numpy().astype(bool),
         eligible=(valid_labels & obs.condition.astype(str).ne('unannotated')).to_numpy()))
    return meta,x,tot,match,dict(cells=nc,genes=ng,source='existing author-annotated object; raw counts layer',
      original_unknown_labels=int((~valid_labels).sum()),missing_condition=int(meta.condition.eq('unannotated').sum()))


def aggregate(meta,x,tot,match,dataset):
    rows=[];coverage=[]
    for mode in ['author_labels','doublets_removed'] if dataset=='Niethamer2025' else ['author_labels']:
        mask=meta.eligible.to_numpy() & (tot>0)
        if mode=='doublets_removed': mask &= ~meta.doublet.to_numpy()
        mm=meta.loc[mask].copy();mm['_index']=np.flatnonzero(mask)
        for keys,group in mm.groupby(['unit','condition','state','lineage','day'],dropna=False,observed=True):
            ii=group['_index'].to_numpy();n=tot[ii];xx=x[ii];deep=n>=500
            info=dict(dataset=dataset,mode=mode,unit=keys[0],condition=keys[1],state=keys[2],lineage=keys[3],day=keys[4])
            coverage.append(dict(**info,cells=len(ii),median_umi=float(np.median(n)),cells_depth500=int(deep.sum()),
                                 depth_eligible_fraction=float(deep.mean())))
            # Expected detection after sampling exactly500 molecules, without replacement.
            nd=n[deep,None].astype(float);cc=xx[deep].astype(float)
            with np.errstate(invalid='ignore'):
                logzero=gammaln(nd-cc+1)+gammaln(nd-500+1)-gammaln(nd-cc-500+1)-gammaln(nd+1)
                detect=np.clip(-np.expm1(np.minimum(logzero,0)),0,1)
            detect=np.where(nd-cc<500,1,detect)
            for j,g in enumerate(GENES):
                if match.iloc[j]['index']<0: continue
                rows.append(dict(**info,gene=g,cells=len(ii),total_umi=int(n.sum()),gene_counts=int(xx[:,j].sum()),
                   cpm=float(1e6*xx[:,j].sum()/n.sum()),detection=float((xx[:,j]>0).mean()),
                   cells_depth500=int(deep.sum()),detection_depth500=float(detect[:,j].mean()) if deep.any() else np.nan,
                   detection_same_cells=float((xx[deep,j]>0).mean()) if deep.any() else np.nan,
                   cpm_same_cells=float(1e6*xx[deep,j].sum()/n[deep].sum()) if deep.any() else np.nan))
    return pd.DataFrame(rows),pd.DataFrame(coverage)


def main():
    p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True)
    p.add_argument('--resume-schema-fix',action='store_true');args=p.parse_args();base=args.data_root
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'tables').mkdir(exist_ok=True)
    contract=OUT/'contract.json'
    assert not (OUT/'run_complete.json').exists(),'Completed run cannot be overwritten'
    assert not contract.exists() or args.resume_schema_fix,'Frozen run exists; choose a new version for reruns'
    files=[base/'raw_data/GSE135893'/n for n in ['GSE135893_genes.tsv.gz','GSE135893_barcodes.tsv.gz','GSE135893_IPF_metadata.csv.gz','GSE135893_matrix.mtx.gz']]
    files += [base/'Research Article/gate1_01_niethamer_2025/GSE262927/processed/final_clustered.h5ad',
              base/'Research Article/gate1_01_niethamer_2025/GSE262927/myeloid_focus/batch_sensitivity/tables/sample_infection_round.csv']
    if args.resume_schema_fix:
        original=json.loads(contract.read_text())
        assert original['code_sha256']==sha(OUT/'failed_attempt/04_atlas.py')
        for item in original['input_files']:
            assert Path(item['path']).stat().st_size==item['bytes']
        (OUT/'schema_amendment.json').write_text(json.dumps(dict(at_utc=datetime.now(timezone.utc).isoformat(),
            reason='First attempt stopped at barcode-set assertion before expression extraction; source matrix has220213 barcodes, annotations114396, all annotation barcodes present. Restrict to source annotated subset after counting.',
            original_code_sha256=original['code_sha256'],resumed_code_sha256=sha(__file__),
            endpoints_changed=False,source_files_unchanged=True),indent=2)+'\n')
    else:
      record=dict(namespace='Nb2',run='atlas_v1',frozen_utc=datetime.now(timezone.utc).isoformat(),code_sha256=sha(__file__),
        genes=GENES,input_files=[dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f)) for f in files],
        exposure='Paper/owner notes and existing repo atlas results already seen; targeted Nb2 summaries not inspected',
        role={'Habermann2020':'source reused by Nabhan2023; original author labels; not independent validation',
              'Niethamer2025':'cross-paper mouse extension; previously used repository data; not source reproduction or independent validation'},
        original_healthy_atlas='Travaglini Synapse processed syn21560510 v1; metadata syn21560409 endpoint403; not substituted as exact reproduction',
        units='Human Sample_Name source participant labels; mouse sample_id linked to existing sample metadata; cells never independent units',
        inclusion='All human source labels, all diagnoses retained; mouse author labels and known condition only; no relabeling',
        primary='Human source labels; mouse predicted doublets removed; retained-doublet sensitivity; marker profiles reported without data-dependent relabeling',
        coverage='Primary>=50 cells/unit/state; sensitivity>=20 and>=100. Binary detection maximal binomial SE about7% at50; biological uncertainty separate. Same floors apply to depth500 subset.',
        normalization='CPM from summed raw counts and all-gene UMI denominator per unit/state; detection fraction; no integration or cross-species absolute comparison',
        depth='Analytic hypergeometric expectation at500 UMIs/cell, eligible cells>=500; report eligible subset original detection and CPM alongside standardized detection',
        summaries='Median/min/max across eligible source units by condition/state/gene; no cell-level p-values; no disease adjustment, no causal or functional inference',
        uncertainty='Unit range and number of contributing units; <3 units too sparse for cohort pattern; no calibrated donor CI in this initial descriptive atlas pass',
        disease='IPF versus control profiles only within human study/state; diagnoses not pooled as IPF',
        mouse='Day-specific descriptive source samples; injury day, sex, genotype and batch may be confounded; CAP1/CAP2 retained without functional gCap/aCap conversion',
        limitations='Human ambient RNA/doublets not newly resolved; marker profiles are checks not lineage tracing; receptor RNA not protein, ligand engagement or signaling activity')
      contract.write_text(json.dumps(record,indent=2)+'\n')
    tables=[];coverage=[];audits={}
    for label,reader in [('Habermann2020',human_counts),('Niethamer2025',mouse_counts)]:
        meta,x,tot,match,audit=reader(base)
        assert np.all(tot>=x.sum(axis=1))
        a,c=aggregate(meta,x,tot,match,label);tables.append(a);coverage.append(c);audits[label]=audit
        print(label,'complete;',len(a),'unit/gene rows',flush=True)
    a=pd.concat(tables,ignore_index=True);c=pd.concat(coverage,ignore_index=True)
    write(a,'unit_receptor_context.tsv.gz');write(c,'unit_coverage.tsv')
    summaries=[]
    for floor in [20,50,100]:
        z=a.loc[a.cells.ge(floor)]
        keys=['dataset','mode','condition','day','state','lineage','gene']
        s=z.groupby(keys,dropna=False,observed=True).agg(units=('unit','nunique'),median_cpm=('cpm','median'),
             min_cpm=('cpm','min'),max_cpm=('cpm','max'),median_detection=('detection','median'),min_detection=('detection','min'),max_detection=('detection','max')).reset_index()
        deep=z.loc[z.cells_depth500.ge(floor)].groupby(keys,dropna=False,observed=True).agg(depth_units=('unit','nunique'),median_depth500=('detection_depth500','median'),median_same_cells_detection=('detection_same_cells','median')).reset_index()
        s=s.merge(deep,on=keys,how='left');s['cell_floor']=floor;summaries.append(s)
    write(pd.concat(summaries,ignore_index=True),'state_summary.tsv.gz')
    pd.DataFrame([dict(dataset=k,**v) for k,v in audits.items()]).to_json(OUT/'extraction_audit.json',orient='records',indent=2)
    (OUT/'run_complete.json').write_text(json.dumps(dict(finished_utc=datetime.now(timezone.utc).isoformat(),
        unit_gene_rows=len(a),coverage_rows=len(c),contract_sha256=sha(contract),scope='descriptive partial atlas analysis; no inferential or functional validation'),indent=2)+'\n')


if __name__=='__main__': main()
