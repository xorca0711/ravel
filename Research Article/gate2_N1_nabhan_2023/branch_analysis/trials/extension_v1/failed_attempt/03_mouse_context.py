import argparse
import json
import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import spearmanr
from common import *

p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,required=True);args=p.parse_args()
guard('mouse_complete.json')
panels=json.loads((OUT/'derived_panels.json').read_text())
genes=sorted(set(sum(panels.values(),[])+CONFIG['additional_genes']))
path=args.data_root/'Research Article/gate1_01_niethamer_2025/GSE262927/processed/final_clustered.h5ad'
with h5py.File(path,'r') as f:
    obs=ad.io.read_elem(f['obs']);var=ad.io.read_elem(f['var'])
    symbols=pd.Index(var.gene_symbol.map(canon));assert symbols.is_unique
    match=symbols.get_indexer(genes);present=match>=0
    write(pd.DataFrame(dict(gene=genes,index=match,mapped=present)),'mouse_gene_mapping.tsv')
    layer=f['layers/counts'];assert layer.attrs['encoding-type']=='csr_matrix'
    ptr=layer['indptr'][:];nc=len(obs);ng=len(var)
    x=np.zeros((nc,len(genes)),dtype=np.int64);total=np.zeros(nc,dtype=np.int64)
    for start in range(0,nc,4096):
        stop=min(start+4096,nc);lo,hi=ptr[start],ptr[stop];values=layer['data'][lo:hi]
        assert np.all(values>=0) and np.equal(values,np.floor(values)).all()
        block=sparse.csr_matrix((values,layer['indices'][lo:hi],ptr[start:stop+1]-lo),shape=(stop-start,ng))
        total[start:stop]=np.asarray(block.sum(axis=1)).ravel().astype(np.int64)
        x[start:stop,present]=block[:,match[present]].toarray().astype(np.int64)
assert np.array_equal(total,obs.total_counts.to_numpy()),'Existing counts depth differs'
meta=pd.DataFrame(dict(unit=obs.sample_id.astype(str).to_numpy(),state=obs.author_celltype.astype(str).to_numpy(),
    lineage=obs.author_lineage.astype(str).to_numpy(),day=obs.sacrifice_day.to_numpy(),condition=obs.condition.astype(str).to_numpy(),
    doublet=obs.predicted_doublet.to_numpy(),sex=obs.sex.astype(str).to_numpy(),idx=np.arange(nc)))
valid=~meta.state.isin(['NA','nan','None','unannotated']) & meta.condition.ne('unannotated') & (total>0)
rows=[];coverage=[];ps=[]
for mode in ['doublets_removed','author_labels']:
    mm=meta[valid & (~meta.doublet if mode=='doublets_removed' else True)]
    for key,frame in mm.groupby(['unit','state','lineage','day','condition','sex'],dropna=False,observed=True):
        ii=frame.idx.to_numpy();xx=x[ii];tt=total[ii];counts=xx.sum(axis=0);cpm=counts/tt.sum()*1e6
        info=dict(mode=mode,unit=key[0],state=key[1],lineage=key[2],day=key[3],condition=key[4],sex=key[5],cells=len(ii),total_umi=int(tt.sum()))
        coverage.append(info)
        rows.extend(dict(**info,gene=g,counts=int(counts[j]),cpm=cpm[j],detection=float((xx[:,j]>0).mean())) for j,g in enumerate(genes) if present[j])
        vv=pd.Series(np.log2(cpm+1),index=genes);scores={}
        for panel,gs in panels.items():
            if panel.startswith('Gaona') and key[2]!='Epithelium': continue
            mapped=[g for g in gs if present[genes.index(g)]]
            if len(mapped)<max(5 if panel.startswith('Gaona') else 2,np.ceil(.6*len(gs))): continue
            scores[panel]=float(vv.loc[mapped].mean())
            ps.append(dict(**info,panel=panel,score=scores[panel],genes=len(mapped)))
        for label in ['Gaona_YT','Gaona_YT_disjoint']:
            if label+'_up' in scores and label+'_down' in scores:
                ps.append(dict(**info,panel=label,score=scores[label+'_up']-scores[label+'_down'],genes=len(panels[label+'_up'])+len(panels[label+'_down'])))
r=pd.DataFrame(rows);c=pd.DataFrame(coverage);p=pd.DataFrame(ps)
write(r,'mouse_unit_expression.tsv.gz');write(c,'mouse_unit_coverage.tsv');write(p,'mouse_program_scores.tsv')
# Gene and program features remain on explicitly distinct scales.
gene_features=r[r.gene.isin(CONFIG['additional_genes'])].rename(columns={'gene':'feature','cpm':'value'});gene_features['scale']='CPM'
program_features=p.rename(columns={'panel':'feature','score':'value'});program_features['scale']='mean_log2_CPM_plus1'
features=pd.concat([gene_features,program_features],ignore_index=True)
summaries=[];paired=[];associations=[]
for floor in [20,50,100]:
    f=features[features.cells.ge(floor)]
    sm=f.groupby(['mode','condition','day','state','lineage','feature','scale'],observed=True).agg(units=('unit','nunique'),median=('value','median'),low=('value','min'),high=('value','max')).reset_index()
    sm['cell_floor']=floor;sm['cohort_eligible']=sm.units>=3;summaries.append(sm)
    for mode in ['doublets_removed','author_labels']:
        fm=f[f['mode'].eq(mode)]
        for sa,sb in [('AT1','AT2'),('Alveolar_transitional','AT2'),('AT1_AT2','AT2'),('AF1','AF2'),('CAP1','CAP2')]:
            aa=fm[fm.state.eq(sa)];bb=fm[fm.state.eq(sb)]
            both=aa.merge(bb,on=['unit','day','condition','feature','scale'],suffixes=('_a','_b'))
            for rec in both.to_dict('records'):
                paired.append(dict(mode=mode,cell_floor=floor,unit=rec['unit'],day=rec['day'],condition=rec['condition'],comparison=sa+'-minus-'+sb,feature=rec['feature'],scale=rec['scale'],value_a=rec['value_a'],value_b=rec['value_b'],delta=rec['value_a']-rec['value_b']))
        day=fm[fm.day.eq(42)]
        for state,ff in day.groupby('state'):
            fib=state in ['AF1','AF2','Adventitial_fibroblast','Peribronchial_fibroblast']
            endo=state in ['CAP1','CAP2','Arterial_endothelium','Venous_endothelium','Lymphatic_endothelium']
            if not (fib or endo): continue
            wide=ff.pivot(index='unit',columns='feature',values='value')
            for receptor in (['Fzd1','Fzd2','Fzd7'] if fib else ['Fzd4']):
                for prog in (['support_ligands','ECM'] if fib else ['cycling','endothelial_junction','injury_cap_context']):
                    if receptor not in wide or prog not in wide: continue
                    w=wide[[receptor,prog]].dropna()
                    if len(w)<5 or w[receptor].nunique()<2 or w[prog].nunique()<2: continue
                    rho=spearmanr(w[receptor],w[prog]).statistic
                    loo=[spearmanr(w.drop(i)[receptor],w.drop(i)[prog]).statistic for i in w.index]
                    associations.append(dict(mode=mode,cell_floor=floor,day=42,state=state,receptor=receptor,program=prog,units=len(w),rho=rho,leave_one_min=min(loo),leave_one_max=max(loo),interpretation='descriptive; no mechanistic or population significance claim'))
write(pd.concat(summaries),'mouse_context_summary.tsv');pr=pd.DataFrame(paired);write(pr,'mouse_within_unit_differences.tsv')
sp=pr.groupby(['mode','cell_floor','condition','day','comparison','feature','scale'],observed=True).agg(units=('unit','nunique'),median=('delta','median'),low=('delta','min'),high=('delta','max'),positive=('delta',lambda s:int((s>0).sum()))).reset_index()
sp['cohort_eligible']=sp.units>=3;write(sp,'mouse_paired_summary.tsv');write(pd.DataFrame(associations),'mouse_day42_associations.tsv')
samplemap=args.data_root/'Research Article/gate1_01_niethamer_2025/GSE262927/myeloid_focus/batch_sensitivity/tables/sample_infection_round.csv'
sm=pd.read_csv(samplemap);unit=c[c['mode'].eq('doublets_removed')][['unit','condition','day','sex']].drop_duplicates()
write(unit.merge(sm,left_on='unit',right_on='sample_id',how='left',validate='one_to_one'),'mouse_sample_context.tsv')
done('mouse_complete.json',source_cells=nc,annotated_cells=int(valid.sum()),source_depth_match=True,mapped_genes=int(present.sum()),requested_genes=len(genes),unit_gene_rows=len(r),program_rows=len(p),scope='descriptive context; no fate or drug-response model')
print('Mouse context complete:',len(r),'gene rows;',len(associations),'descriptive associations')
