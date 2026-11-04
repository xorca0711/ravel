"""Attribution of fixed early/late AT1 panels with original ES1 joint draws."""
import argparse,importlib.util,json
from pathlib import Path
import anndata as ad
import h5py
import numpy as np
import pandas as pd

BASE=Path('Research Article/epithelial_state_specificity')
PRE=Path('docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A8_INPUT_MAP_V1.json')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    spec=json.loads(PRE.read_text());cfg=json.loads((BASE/'modules.json').read_text());modules=spec['module_definitions']
    loader=importlib.util.spec_from_file_location('frozen_es1_reader',BASE/'run_es1.py');old=importlib.util.module_from_spec(loader);loader.loader.exec_module(old);old.OUT=out
    genes=sorted(set(g for m in cfg['modules'] for g in m['genes'])|set(old.AIRWAY+old.ALVEOLAR+old.LABELS))
    if genes!=spec['sampling_gene_order'] or len(genes)!=1503:raise ValueError('Full joint sampling order changed')
    if [m for m in cfg['modules'] if m['name'] in {x['name'] for x in modules}]!=modules:raise ValueError('Panel membership changed')
    pos={g:i for i,g in enumerate(genes)};display=[g for m in modules for g in m['genes']];saved=list(dict.fromkeys(display+old.LABELS));ids={};rows=[];gene_rows=[];filters=[];draws=[];retention=[]
    def score(counts,totals,genes,present,meta,unused,unused_rows,unused_genes,unused_retention):
        barcodes=ids[meta['unit']]
        if len(barcodes)!=len(totals) or len(set(barcodes))!=len(barcodes):raise ValueError('Cell identity/order conflict')
        airway=counts[[pos[g] for g in old.AIRWAY]].sum(axis=0);alv=counts[[pos[g] for g in old.ALVEOLAR]].sum(axis=0);keep=(totals>=2000)&(airway<=alv)
        f=pd.DataFrame(dict(unit=meta['unit'],cell=barcodes,within_unit_row=np.arange(len(totals)),library=totals,airway_count=airway,alveolar_count=alv,retained=keep));filters.append(f)
        retention.append(dict(meta,n_input=len(totals),n_retained=int(keep.sum())))
        for seed in (17,29):
            ds=old.joint_sample(counts[:,keep],totals[keep],2000,seed);trans=(ds[pos['Cldn4']]>0)&(ds[pos['Krt8']]>0);ref=(ds[pos['Sftpc']]>0)&~trans
            masks={'two_marker':trans,'reference':ref};d=f.loc[keep,['unit','cell','within_unit_row']].copy();d['seed']=seed;d['group']=np.where(trans,'two_marker',np.where(ref,'reference','neither'));d['sampled_universe_total']=ds.sum(axis=0);d['sampled_residual']=2000-d.sampled_universe_total
            for g in saved:d[g]=ds[pos[g]]
            draws.append(d)
            for group,mask in masks.items():
                n=int(mask.sum())
                for m in modules:
                    members=[g for g in m['genes'] if g in present];coverage=len(members)/len(m['genes']);ok=n>=30 and coverage>=.8
                    detections=[]
                    for g in m['genes']:
                        nd=int((ds[pos[g],mask]>0).sum());det=nd/n if n and g in present else np.nan;detections.append(det)
                        gene_rows.append(dict(meta,seed=seed,group=group,module=m['name'],gene=g,n_cells=n,present=g in present,n_detected=nd,detection=det,contribution=det/len(members) if members else np.nan,interpretable=ok))
                    value=float(np.mean([detections[m['genes'].index(g)] for g in members])) if members else np.nan
                    rows.append(dict(meta,seed=seed,group=group,module=m['name'],n_cells=n,n_genes=len(members),total_genes=len(m['genes']),coverage=coverage,score=value,interpretable=ok))
    old.score_unit=score
    descriptors=[('GSE247130','P9',['P9_control','P9_Cebpa_mutant'],['control','Cebpa_mutant'],'uninjured'),('GSE247130','7wk',['7wk_control','7wk_Cebpa_mutant'],['control','Cebpa_mutant'],'uninjured'),('GSE247130','adult_14dpi',['SeV_control','SeV_Cebpa_mutant'],['control','Cebpa_mutant'],'SeV'),('GSE310539','adult',['wildtype_PBS','wildtype_SeV','AP1mut_PBS','AP1mut_SeV'],['wildtype','wildtype','AP1mut','AP1mut'],None)]
    for src,desc in zip(spec['source_inputs'][:4],descriptors):
        dep,stage,units,genotypes,inj=desc;path=Path(src['path']);print('Reading',path.name,flush=True)
        with h5py.File(path,'r') as h:
            names=np.array([old.decode(x) for x in h['matrix/features/name'][:]]);barcodes=np.array([old.decode(x) for x in h['matrix/barcodes'][:]])
            if {g:np.flatnonzero(names==g).tolist() for g in display}!=src['feature_map']:raise ValueError('Source feature map changed')
        counts,totals,suffix,present=old.read_10x(path,genes)
        for i,(unit,genotype) in enumerate(zip(units,genotypes),1):
            sel=suffix==str(i);ids[unit]=barcodes[sel];meta=dict(cohort=dep,unit=unit,unit_type='pooled_library',genotype=genotype,stage=stage,injury=inj or ('SeV' if unit.endswith('_SeV') else 'uninjured'))
            score(counts[:,sel],totals[sel],genes,present,meta,modules,[],[],[])
        del counts
    src=spec['source_inputs'][4]
    with h5py.File(src['path'],'r') as h:
        obs=ad.io.read_elem(h['obs']);names=ad.io.read_elem(h['var']).index.astype(str).to_numpy()
        if {g:np.flatnonzero(names==g).tolist() for g in display}!=src['feature_map']:raise ValueError('External feature map changed')
        sub=obs[obs.has_author_metadata.astype(bool)&obs.author_celltype.astype(str).isin({'AT1','AT2','AT1_AT2','Alveolar_transitional'})]
        for animal,idx in sub.groupby('sample_id',observed=True).indices.items():ids[str(animal)]=sub.iloc[idx].index.astype(str).to_numpy()
    ext=old.external(genes,modules,[],[],[],[])
    scores=pd.DataFrame(rows);members=pd.DataFrame(gene_rows);keys=['unit','seed','module']
    effects=scores[scores.group.eq('two_marker')].merge(scores[scores.group.eq('reference')],on=keys,suffixes=('_two_marker','_reference'),validate='one_to_one');effects['difference']=effects.score_two_marker-effects.score_reference;effects['interpretable']=effects.interpretable_two_marker&effects.interpretable_reference
    contributions=members[members.group.eq('two_marker')].merge(members[members.group.eq('reference')],on=keys+['gene'],suffixes=('_two_marker','_reference'),validate='one_to_one');contributions['delta_detection']=contributions.detection_two_marker-contributions.detection_reference;contributions['delta_contribution']=contributions.contribution_two_marker-contributions.contribution_reference;contributions['interpretable']=contributions.interpretable_two_marker&contributions.interpretable_reference
    checks=[];error=0.0
    for name,new,ks,cols in [('module_scores.csv',scores,keys+['group'],['n_cells','n_genes','total_genes','coverage','score','interpretable']),('within_unit_effects.csv',effects,keys,['difference','interpretable'])]:
        olddf=pd.read_csv(BASE/'results'/name);olddf=olddf[olddf.module.isin([m['name'] for m in modules])];joined=new.merge(olddf,on=ks,how='outer',suffixes=('_new','_old'),indicator=True,validate='one_to_one')
        if not joined['_merge'].eq('both').all():raise ValueError('Original row roster mismatch')
        for c in cols:
            a=joined[c+'_new'].astype(float).to_numpy();b=joined[c+'_old'].astype(float).to_numpy()
            if not np.array_equal(np.isnan(a),np.isnan(b)):raise ValueError('Original missingness mismatch')
            diff=np.abs(a-b);e=float(np.nanmax(diff)) if np.isfinite(diff).any() else 0.0;error=max(error,e)
            if e>1e-10:raise ValueError('Original score/support parity failure: '+c)
            checks.append(dict(table=name,field=c,n=len(a),max_error=e))
    for frame,name in [(scores,'module_scores.tsv'),(members,'member_detection.tsv'),(effects,'within_unit_effects.tsv'),(contributions,'member_contrasts.tsv'),(pd.DataFrame(retention),'retention.tsv'),(pd.DataFrame(checks),'original_parity.tsv')]:frame.to_csv(out/name,sep='\t',index=False)
    for frame,name in [(pd.concat(filters),'cell_filter_primitives.tsv.gz'),(pd.concat(draws),'cell_draw_primitives.tsv.gz')]:frame.to_csv(out/name,sep='\t',index=False,compression={'method':'gzip','mtime':0})
    result=dict(ok=True,sampling_genes=len(genes),units=int(scores.unit.nunique()),external=ext,group_module_rows=len(scores),member_rows=len(members),attempted_module_contrasts=len(effects),interpretable_module_contrasts=int(effects.interpretable.sum()),parity_scalar_checks=sum(c['n'] for c in checks),max_parity_error=error,seeds=[17,29],limit='Fixed panel attribution; pooled libraries and technical seeds are not biological replicates; RNA detection is not maturation, fate or AT1 contribution.')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
