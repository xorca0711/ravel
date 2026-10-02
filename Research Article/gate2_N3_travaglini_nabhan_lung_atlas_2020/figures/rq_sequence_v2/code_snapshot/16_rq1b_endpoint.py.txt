"""RQ1b: fixed A22 chemokines versus C3 across fibroblast subtype contrasts."""
import numpy as np
import pandas as pd
from rq_common import *


def sign(x):
    return 0 if abs(x) <= 1e-12 else int(np.sign(x))


def main():
    options=args(); previous='rq1_composition_v1'; out=begin('rq1b_endpoint_v1',previous)
    genes=['C3']+CFG['chemokines']; receipt={}; rows=[]; coverage=[]; maps=[]
    for m,counts,totals,mapping in atlases(options.source_root,genes,receipt):
        maps.append({'cohort':m.cohort.iloc[0],'assay':m.assay.iloc[0],'mapping':mapping})
        for key,a,b in strata(m):
            coverage.append(key)
            for floor in CFG['cell_floors']:
                if min(len(a),len(b))<floor: continue
                for j,gene in enumerate(genes):
                    available=bool(mapping[gene])
                    left=np.log2(counts[a,j].sum()/totals[a].sum()*1e6+1) if available else np.nan
                    right=np.log2(counts[b,j].sum()/totals[b].sum()*1e6+1) if available else np.nan
                    rows.append(key|{'cell_floor':floor,'gene':gene,'available':available,
                       'left_log2CPM':left,'right_log2CPM':right,'delta_log2CPM':left-right,
                       'delta_detection':float((counts[a,j]>0).mean()-(counts[b,j]>0).mean()) if available else np.nan})
    frame=pd.DataFrame(rows);save(frame,out,'stratum_effects.tsv');save(pd.DataFrame(coverage),out,'coverage.tsv')
    donor=donor_average(frame,['left_log2CPM','right_log2CPM','delta_log2CPM','delta_detection'],['gene'])
    save(donor,out,'donor_effects.tsv')
    keys=['cohort','assay','donor_id','cell_floor']; panels=[]; agreement=[]
    for key,part in donor.groupby(keys,sort=True):
        base=dict(zip(keys,key)); v=part.set_index('gene').delta_log2CPM
        c3=float(v.get('C3',np.nan)); present=all(g in v and np.isfinite(v[g]) for g in CFG['chemokines'])
        for g in CFG['chemokines']:
            value=float(v.get(g,np.nan)); valid=np.isfinite(value) and np.isfinite(c3)
            agreement.append(base|{'gene':g,'C3_delta':c3,'chemokine_delta':value,
                'direction_status':('uninformative_zero' if sign(c3)==0 or sign(value)==0 else ('same' if sign(c3)==sign(value) else 'opposite')) if valid else 'missing'})
        for omit in ['none']+CFG['chemokines']:
            panel=[g for g in CFG['chemokines'] if g!=omit]
            score=float(v.loc[panel].mean()) if present else np.nan
            panels.append(base|{'omitted_gene':omit,'panel_complete':present,'panel_delta':score,'C3_delta':c3,
                'direction_status':('uninformative_zero' if sign(c3)==0 or sign(score)==0 else ('same' if sign(c3)==sign(score) else 'opposite')) if present and np.isfinite(c3) else 'missing'})
    panel=pd.DataFrame(panels);save(panel,out,'panel_sensitivity.tsv');save(pd.DataFrame(agreement),out,'gene_agreement.tsv')
    summaries=[]
    for key,part in donor.groupby(['cohort','assay','cell_floor','gene'],sort=True):
        v=part.delta_log2CPM.dropna().to_numpy();base=dict(zip(['cohort','assay','cell_floor','gene'],key))
        if not len(v): summaries.append(base|{'n_donors':0});continue
        loo=[float(np.delete(v,i).mean()) for i in range(len(v))] if len(v)>1 else []
        summaries.append(base|{'n_donors':len(v),'mean_delta':v.mean(),'min_delta':v.min(),'max_delta':v.max(),
            'positive_donors':int((v>0).sum()),'negative_donors':int((v<0).sum()),
            'loo_mean_min':min(loo) if loo else np.nan,'loo_mean_max':max(loo) if loo else np.nan})
    save(pd.DataFrame(summaries),out,'cohort_summary.tsv');write_json(out/'gene_mapping.json',maps)
    write_json(out/'decision.json',{'question':'Can C3 substitute for the inherited seven-chemokine subtype contrast?',
        'tested':'sign agreement and fixed/leave-one-gene-out panel diagnostics, not co-regulation',
        'functional_response':'not measured','TMM_reproduction':False,
        'primary_panel_status':panel[(panel.cell_floor==20)&(panel.omitted_gene=='none')].groupby(['assay','direction_status']).size().reset_index(name='donors').to_dict('records')})
    finish(out,receipt,'fixed endpoint comparison complete; secretion/response gates held',previous)
    print(panel[(panel.cell_floor==20)&(panel.omitted_gene=='none')][['assay','donor_id','C3_delta','panel_delta','direction_status']].to_string(index=False),flush=True)


if __name__=='__main__':main()
