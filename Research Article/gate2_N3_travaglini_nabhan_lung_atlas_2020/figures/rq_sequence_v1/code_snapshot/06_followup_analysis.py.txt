"""Bounded post-reproduction sensitivity branches; no population significance tests."""
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy.special import gammaln
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def expected_detection(counts, totals, budget):
    """P(at least one molecule) for a hypergeometric draw; exact conditional expectation."""
    N=totals[:,None]; k=counts
    if np.any(N<budget) or np.any(k<0) or np.any(k>N):raise ValueError('Invalid finite-population sampling counts')
    forced=N-k<budget
    safe=np.maximum(N-k-budget+1,1)
    log_zero=gammaln(N-k+1)-gammaln(safe)+gammaln(N-budget+1)-gammaln(N+1)
    p=-np.expm1(np.minimum(log_zero,0))
    p[forced]=1; p[k==0]=0
    return np.clip(p,0,1)


def main():
    follow=read_json(PACKAGE/'config/followup_v1.json');cfg=read_json(PACKAGE/'config/execution_v1.json')
    out=new_run(PACKAGE/'runs/followup_v1')
    effects=pd.read_csv(PACKAGE/'runs/reproduction_v1/paired_effects.tsv',sep='\t')
    floors=[]
    for floor in [10,20,30,50]:
        eligible=effects[(effects.n_left>=floor)&(effects.n_right>=floor)]
        for key,g in eligible.groupby(['contrast','assay','anatomical_region','gene'],sort=True):
            values=g.delta_log2CPM.to_numpy();n=len(values)
            omitted=[np.delete(values,i).mean() for i in range(n)] if n>1 else []
            floors.append(dict(zip(['contrast','assay','anatomical_region','gene'],key))|{'cell_floor':floor,'n_donors':n,'mean_delta_log2CPM':values.mean(),'min_delta':values.min(),'max_delta':values.max(),'leave_one_donor_out_min':min(omitted) if omitted else np.nan,'leave_one_donor_out_max':max(omitted) if omitted else np.nan,'coverage_status':'three_donor_description' if n>=3 else 'coverage_hold'})
    pd.DataFrame(floors).to_csv(out/'floor_and_donor_sensitivity.tsv',sep='\t',index=False,float_format='%.8g')
    e=effects[(effects.n_left>=10)&(effects.n_right>=10)]
    paired=e[e.assay=='10x'].merge(e[e.assay=='SS2'],on=['contrast','donor_id','anatomical_region','gene'],suffixes=('_10x','_SS2'))
    paired['direction_agrees']=np.sign(paired.delta_log2CPM_10x)==np.sign(paired.delta_log2CPM_SS2)
    paired.to_csv(out/'matched_assay_directions.tsv',sep='\t',index=False,float_format='%.8g')
    cache=REPO/'raw_data/travaglini_nabhan_2020/prepared';meta=pd.read_csv(cache/'cell_metadata.tsv',sep='\t',keep_default_na=False)
    specificity=[];depth=[];sampling=[]
    for assay in ['10x','SS2']:
        bundle=np.load(cache/f'{assay}_selected_counts.npz')
        counts=bundle['counts'];totals=bundle['totals'];genes=list(bundle['genes']);m=meta[meta.assay==assay].reset_index(drop=True)
        if not np.array_equal(m.cell_id.to_numpy(dtype=str),bundle['cell_ids']):raise ValueError('Cached cell order changed')
        source_record=read_json(PACKAGE/'runs/reproduction_v1/run_record.json')
        if sha256(cache/f'{assay}_selected_counts.npz')!=source_record['cache_hashes'][f'{assay}_selected_counts.npz']:raise ValueError('Expression cache changed')
        for (donor,region),ids in m[m.tissue=='lung'].groupby(['donor_id','anatomical_region']).groups.items():
            ids=np.asarray(list(ids));labels=m.loc[ids,'author_cell_type'];comp=m.loc[ids,'source_compartment']
            for gene,target,comparators in [('MYRF','Alveolar Epithelial Type 1',['Alveolar Epithelial Type 2','Club','other epithelial']),('TBX5','Pericyte',['Alveolar Fibroblast','Vascular Smooth Muscle','other stromal'])]:
                col=genes.index(gene);left=ids[(labels==target).to_numpy()]
                for comparator in comparators:
                    if comparator=='other epithelial':mask=comp.isin(['epithelial','epithelium'])&(labels!=target)
                    elif comparator=='other stromal':mask=comp.isin(['stromal','stroma'])&(labels!=target)
                    else:mask=labels==comparator
                    right=ids[mask.to_numpy()]
                    if min(len(left),len(right))<20:continue
                    values=[]
                    for group in [left,right]:values.append(float(np.log2(counts[group,col].sum()/totals[group].sum()*1e6+1)))
                    specificity.append({'assay':assay,'donor_id':donor,'anatomical_region':region,'gene':gene,'target':target,'comparator':comparator,'n_target':len(left),'n_comparator':len(right),'delta_log2CPM':values[0]-values[1],'delta_detection':float((counts[left,col]>0).mean()-(counts[right,col]>0).mean())})
        if assay=='10x':
            eligible=(totals>=follow['depth_budget'])&(m.tissue.to_numpy()=='lung')
            selected=np.flatnonzero(eligible);expect=expected_detection(counts[selected],totals[selected],follow['depth_budget'])
            lookup={int(idx):i for i,idx in enumerate(selected)}
            sampling.append({'assay':assay,'budget':follow['depth_budget'],'lung_cells_before':int((m.tissue=='lung').sum()),'lung_cells_retained':int(eligible.sum()),'method':'exact hypergeometric detection expectation; no Monte Carlo seeds required'})
            for contrast in cfg['contrasts']:
                panel=set(g for p in contrast['panels'] for g in cfg['panels'][p])
                for (donor,region),ids in m[eligible].groupby(['donor_id','anatomical_region']).groups.items():
                    left=[lookup[i] for i in ids if m.loc[i,'author_cell_type']==contrast['left']]
                    right=[lookup[i] for i in ids if m.loc[i,'author_cell_type']==contrast['right']]
                    if min(len(left),len(right))<10:continue
                    original_left=selected[left];original_right=selected[right]
                    for j,gene in enumerate(genes):
                        if gene not in panel:continue
                        depth.append({'contrast':contrast['id'],'assay':assay,'donor_id':donor,'anatomical_region':region,'gene':gene,'n_left':len(left),'n_right':len(right),'delta_observed_detection':float((counts[original_left,j]>0).mean()-(counts[original_right,j]>0).mean()),'delta_expected_detection_at_1000':float(expect[left,j].mean()-expect[right,j].mean()),'primary_count_eligible':min(len(left),len(right))>=20})
    pd.DataFrame(specificity).to_csv(out/'alternative_comparators.tsv',sep='\t',index=False,float_format='%.8g')
    pd.DataFrame(depth).to_csv(out/'depth_standardized_detection.tsv',sep='\t',index=False,float_format='%.8g')
    write_json(out/'depth_sampling_record.json',sampling)
    finish_record(out,{'schema':'TN2020-followup-run/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'B1-B4 complete; exploratory diagnostics, not independent replication','expression_analysis_run':True,'row_counts':{'floor_summaries':len(floors),'matched_assay_pairs':len(paired),'alternative_comparators':len(specificity),'depth_effects':len(depth)}})
    print(f'Follow-ups: {len(floors)} floor/donor summaries, {len(paired)} matched assay effects, {len(specificity)} alternate comparators, {len(depth)} depth effects.')


if __name__=='__main__':main()
