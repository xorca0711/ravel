"""RQ2: MYRF reference specificity and the independent mature-endpoint gate."""
import re
import numpy as np
import pandas as pd
import h5py
import scipy.sparse as sp
from rq_common import *


def decode(values):
    return np.asarray([v.decode() if isinstance(v,bytes) else str(v) for v in values])


def murthy(root,genes,receipt):
    items=CFG['murthy_inputs']
    paths=[checked(root,item,receipt) for item in items]
    meta_path=next(p for p in paths if p.suffix=='.csv')
    m=pd.read_csv(meta_path).rename(columns={'Unnamed: 0':'cell_id'})
    if 'cell_id' not in m: m=m.rename(columns={m.columns[0]:'cell_id'})
    if not m.cell_id.is_unique:raise ValueError('Duplicate Murthy cell keys')
    m['donor_id']=m.sample_id
    m['subtype']=m.proposed_cell_type.map({'AT1 (candidate)':'Alveolar Epithelial Type 1',
        'AT2 (candidate)':'Alveolar Epithelial Type 2','Mesothelium (candidate)':'Mesothelial'}).fillna('other')
    m['cohort']='Murthy';m['assay']='Murthy 10x';m['keep']=True
    m['stratum']=[json.dumps([s,'candidate epithelial subset']) for s in m.sample_id]
    counts=np.full((len(m),len(genes)),np.nan);totals=np.full(len(m),np.nan);maps=[]
    for path in paths:
        if path.suffix!='.h5':continue
        sample=re.search(r'GSM\d+_(DD\d+[A-Z])',path.name).group(1)
        with h5py.File(path,'r') as f:
            g=f['matrix'];names=decode(g['features/name'][:]);barcodes=decode(g['barcodes'][:])
            feature_type=decode(g['features/feature_type'][:])
            if not np.all(feature_type=='Gene Expression'):raise ValueError('Unexpected feature type')
            raw=sp.csc_matrix((g['data'][:].astype(float),g['indices'][:],g['indptr'][:]),shape=tuple(g['shape'][:]))
            if np.any(~np.isfinite(raw.data)) or np.any(raw.data<0) or np.any(abs(raw.data-np.rint(raw.data))>1e-6):
                raise ValueError('Murthy count domain invalid')
            all_ids=pd.Index(sample+'_'+barcodes);ids=np.flatnonzero((m.sample_id==sample).to_numpy())
            positions=all_ids.get_indexer(m.loc[ids,'cell_id'])
            if np.any(positions<0):raise ValueError('Murthy label/count join failed')
            block=raw[:,positions];totals[ids]=np.asarray(block.sum(axis=0)).ravel()
            mapping={}
            for j,gene in enumerate(genes):
                idx=np.flatnonzero(names==gene);mapping[gene]=len(idx)
                if len(idx):counts[ids,j]=np.asarray(block[idx,:].sum(axis=0)).ravel()
            maps.append({'sample_id':sample,'mapping':mapping,'joined_cells':len(ids)})
    if np.any(~np.isfinite(totals)) or np.any(totals<=0):raise ValueError('Missing Murthy cells or invalid library')
    return m,counts,totals,maps


def main():
    options=args();previous='rq1b_endpoint_v1';out=begin('rq2_myrf_v1',previous)
    genes=CFG['myrf_reference_genes'];receipt={};rows=[];coverage=[];maps=[]
    def consume(m,counts,totals,mapping):
        for comparator in ['Alveolar Epithelial Type 2','Mesothelial']:
            for key,a,b in strata(m,'Alveolar Epithelial Type 1',comparator):
                coverage.append(key|{'comparator':comparator})
                for floor in CFG['cell_floors']:
                    if min(len(a),len(b))<floor:continue
                    for j,gene in enumerate(genes):
                        present=bool(np.all(np.isfinite(counts[np.r_[a,b],j])))
                        x=np.log2(counts[a,j].sum()/totals[a].sum()*1e6+1) if present else np.nan
                        y=np.log2(counts[b,j].sum()/totals[b].sum()*1e6+1) if present else np.nan
                        rows.append(key|{'cell_floor':floor,'comparator':comparator,'gene':gene,'available':present,
                            'left_log2CPM':x,'right_log2CPM':y,'delta_log2CPM':x-y,
                            'delta_detection':float((counts[a,j]>0).mean()-(counts[b,j]>0).mean()) if present else np.nan})
    for m,counts,totals,mapping in atlases(options.source_root,genes,receipt,external=False):
        maps.append({'cohort':m.cohort.iloc[0],'assay':m.assay.iloc[0],'mapping':mapping})
        consume(m,counts,totals,mapping)
    m,counts,totals,mapping=murthy(options.source_root,genes,receipt)
    maps.append({'cohort':'Murthy','mapping':mapping});consume(m,counts,totals,mapping)
    frame=pd.DataFrame(rows);save(frame,out,'stratum_effects.tsv');save(pd.DataFrame(coverage),out,'coverage.tsv')
    donor=donor_average(frame,['left_log2CPM','right_log2CPM','delta_log2CPM','delta_detection'],['comparator','gene'])
    save(donor,out,'donor_effects.tsv');write_json(out/'gene_mapping.json',maps)
    summary=[]
    for key,part in donor.groupby(['cohort','assay','cell_floor','comparator','gene'],sort=True):
        v=part.delta_log2CPM.dropna()
        summary.append(dict(zip(['cohort','assay','cell_floor','comparator','gene'],key))|{
            'n_donors':len(v),'mean_delta':v.mean(),'min_delta':v.min(),'max_delta':v.max(),
            'positive_donors':int((v>0).sum()),'negative_donors':int((v<0).sum()),
            'replicated_description_eligible':len(v)>=CFG['minimum_donors_for_replicated_description']})
    summary=pd.DataFrame(summary);save(summary,out,'cohort_summary.tsv')
    gate=[{'cohort':c,'linked_non_RNA_mature_endpoint':False,'maturation_fit_performed':False,
           'decision':'reference diagnostics only; A8 endpoint gate held'} for c in ['Travaglini','Murthy']]
    write_json(out/'endpoint_gate.json',gate)
    finish(out,receipt,'MYRF reference diagnostics complete; independent mature-outcome gate held',previous)
    print(summary[(summary.gene=='MYRF')&(summary.cell_floor==20)].to_string(index=False),flush=True)


if __name__=='__main__':main()
