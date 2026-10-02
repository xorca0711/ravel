"""Prespecified, region/protocol-matched fibroblast transfer in an independent atlas."""
from datetime import datetime, timezone
import importlib.util
import numpy as np
import pandas as pd
import anndata as ad
import h5py
from common import PACKAGE, REPO, read_json, write_json, sha256, new_run, finish_record


def main():
    cfg=read_json(PACKAGE/'config/external_pilot_v1.json');source=read_json(PACKAGE/'config/external_source_v1.json')
    path=REPO/source['cache_path']
    if sha256(path)!=source['sha256']:raise ValueError('External input hash mismatch')
    out=new_run(PACKAGE/'runs/external_pilot_v1')
    obj=ad.read_h5ad(path,backed='r');m=obj.obs.copy().reset_index(names='cell_id')
    if not m.cell_id.is_unique:raise ValueError('Duplicate external cells')
    names=obj.raw.var.feature_name.astype(str);genes=cfg['genes'];lookup={g:np.where(names.to_numpy()==g)[0] for g in genes}
    if any(len(v)!=1 for v in lookup.values()):raise ValueError('External target gene missing or nonunique')
    spec=importlib.util.spec_from_file_location('reproduction',PACKAGE/'scripts/04_expression_reproduction.py');rep=importlib.util.module_from_spec(spec);spec.loader.exec_module(rep)
    counts=np.zeros((len(m),len(genes)));totals=np.zeros(len(m));integer_errors=0
    with h5py.File(path,'r') as handle:
        for start in range(0,len(m),1024):
            end=min(start+1024,len(m));block=rep.csr_block(handle['raw/X'],start,end)
            integer_errors+=int(np.sum(abs(block.data-np.rint(block.data))>1e-6))
            if np.any(~np.isfinite(block.data)) or np.any(block.data<0):raise ValueError('External count domain invalid')
            totals[start:end]=np.asarray(block.sum(axis=1)).ravel()
            for j,g in enumerate(genes):counts[start:end,j]=np.asarray(block[:,lookup[g]].sum(axis=1)).ravel()
    if integer_errors or np.any(totals<=0):raise ValueError('External count semantics failed')
    keep=m.Location_long.isin(['Lower Left Lobe','Upper left lobe']) & (m.disease=='normal') & m.Celltypes.isin([cfg['left_label'],cfg['right_label']])
    grouping=cfg['matching_fields'];effects=[];coverage=[]
    for key,ids in m[keep].groupby(grouping,observed=True,sort=True).groups.items():
        ids=np.asarray(list(ids));left=ids[(m.loc[ids,'Celltypes']==cfg['left_label']).to_numpy()];right=ids[(m.loc[ids,'Celltypes']==cfg['right_label']).to_numpy()]
        row=dict(zip(grouping,key));coverage.append(row|{'n_left':len(left),'n_right':len(right),'primary_eligible':min(len(left),len(right))>=20})
        if min(len(left),len(right))<10:continue
        values=[np.log2(counts[group].sum(axis=0)/totals[group].sum()*1e6+1) for group in [left,right]]
        detect=[(counts[group]>0).mean(axis=0) for group in [left,right]]
        for j,gene in enumerate(genes):effects.append(row|{'gene':gene,'n_left':len(left),'n_right':len(right),'delta_log2CPM':values[0][j]-values[1][j],'delta_detection':detect[0][j]-detect[1][j]})
    effects=pd.DataFrame(effects);pd.DataFrame(coverage).to_csv(out/'stratum_coverage.tsv',sep='\t',index=False)
    if effects.empty:raise ValueError('No external stratum meets the sensitivity floor')
    effects.to_csv(out/'stratum_effects.tsv',sep='\t',index=False,float_format='%.8g')
    donors=[]
    for floor in [20,10]:
        eligible=effects[(effects.n_left>=floor)&(effects.n_right>=floor)]
        for (donor,suspension,gene),frame in eligible.groupby(['donor_id','suspension_type','gene'],observed=True):
            donors.append({'donor_id':donor,'suspension_type':suspension,'gene':gene,'cell_floor':floor,'n_strata':len(frame),'mean_delta_log2CPM':frame.delta_log2CPM.mean(),'min_stratum_delta':frame.delta_log2CPM.min(),'max_stratum_delta':frame.delta_log2CPM.max(),'mean_delta_detection':frame.delta_detection.mean()})
    donor_frame=pd.DataFrame(donors);donor_frame.to_csv(out/'donor_effects.tsv',sep='\t',index=False,float_format='%.8g')
    summary=[]
    for (suspension,gene,floor),frame in donor_frame.groupby(['suspension_type','gene','cell_floor']):
        summary.append({'suspension_type':suspension,'gene':gene,'cell_floor':floor,'n_donors':len(frame),'mean_delta_log2CPM':frame.mean_delta_log2CPM.mean(),'min_donor_delta':frame.mean_delta_log2CPM.min(),'max_donor_delta':frame.mean_delta_log2CPM.max(),'positive_donors':int((frame.mean_delta_log2CPM>0).sum()),'negative_donors':int((frame.mean_delta_log2CPM<0).sum())})
    pd.DataFrame(summary).to_csv(out/'summary.tsv',sep='\t',index=False,float_format='%.8g')
    m.groupby(['donor_id','suspension_type','Location_long','Celltypes'],observed=True).size().rename('n_cells').reset_index().to_csv(out/'all_metadata_coverage.tsv',sep='\t',index=False)
    write_json(out/'design_record.json',{'n_cells_nuclei':len(m),'n_genes':len(names),'raw_integer_errors':integer_errors,'donors_in_object':sorted(m.donor_id.unique()),'donor_aliases':m[['donor_id','donor_id_2']].drop_duplicates().to_dict('records'),'excluded_mix_or_airway_or_other_subtype':int((~keep).sum()),'gene_mapping':{g:list(names.index[lookup[g]]) for g in genes},'cohort_independence':'Madissoon organ-donor study has distinct recruitment and source identifiers from Travaglini surgical P1-P3; no record linkage beyond published design and deposited identifiers; nuclear pools remain assigned to demultiplexed donor labels','annotation_dependence':'Author fibroblast labels are retained; related identity markers inform annotations. No independent annotation validation is claimed.'})
    obj.file.close()
    finish_record(out,{'schema':'TN2020-external-pilot-run/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'external descriptive transfer complete','expression_analysis_run':True,'source_sha256':source['sha256']})
    print(pd.DataFrame(summary).query('cell_floor==20 and suspension_type=="cell"').to_string(index=False))


if __name__=='__main__':main()
