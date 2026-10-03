"""Outcome-exposed, mouse-level biological extensions from frozen Nb5 tables."""
from pathlib import Path
from itertools import combinations
import argparse, json
import numpy as np
import pandas as pd
from scipy.stats import hypergeom

DATASETS = ['Lung_facs', 'Bladder_droplet']
FOCAL_TISSUES = ['Thymus', 'Spleen', 'Marrow']
ENDPOINTS = ['mean_expression', 'detected_fraction']
DISPLAY_GENES = ['Cdkn2a', 'Cdkn1a', 'Lmnb1', 'Il1b']

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def write(path, rows, columns=None):
    pd.DataFrame(rows, columns=columns).to_csv(path, sep='\t', index=False, float_format='%.15g')

def decomposition(p, x, age):
    """Exact difference of equal-mouse sums, including within-age covariance."""
    y = age == 3; o = age == 24
    py, po = p[y].mean(0), p[o].mean(0)
    ey, eo = x[y].mean(0), x[o].mean(0)
    my, mo = (p[y]*x[y]).sum(1).mean(), (p[o]*x[o]).sum(1).mean()
    comp = (po-py)*ey
    within = py*(eo-ey)
    interaction = (po-py)*(eo-ey)
    covariance = ((p[o]*x[o]).mean(0)-po*eo) - ((p[y]*x[y]).mean(0)-py*ey)
    assert np.isclose(mo-my, (comp+within+interaction+covariance).sum(), atol=1e-10)
    return dict(young=float(my), old=float(mo), difference=float(mo-my),
                composition=float(comp.sum()), within_type=float(within.sum()),
                interaction=float(interaction.sum()), animal_covariance=float(covariance.sum())), (comp, within, interaction, covariance)

def toy_checks():
    a,_ = decomposition(np.array([[.8,.2],[.5,.5]]),np.array([[1.,4.],[3.,5.]]),np.array([3,24]))
    assert np.allclose([a[k] for k in ['difference','composition','within_type','interaction','animal_covariance']], [2.4,.9,1.8,-.3,0])
    a,_ = decomposition(np.array([[.8,.2],[.2,.8],[.6,.4],[.4,.6]]),np.array([[1.,10.],[3.,4.],[2.,8.],[4.,6.]]),np.array([3,3,24,24]))
    assert np.allclose([a[k] for k in ['difference','composition','within_type','interaction','animal_covariance']], [1.5,0,.5,0,1.])
    draws=list(combinations([0,0,0,1],2))
    exact=np.mean([float(a==b) for a,b in draws])
    assert np.isclose(rarefaction([3,1],2),exact) and np.isclose(exact,.5)

def composition(root,out):
    source=root/'analysis/research/runs/nb5_descriptive_v1'
    c=pd.read_csv(source/'composition_mouse.tsv',sep='\t')
    e=pd.read_csv(source/'expression_mouse.tsv',sep='\t')
    c=c[(c.unit_kind=='deposited_mouse')&c.age_months.isin([3,24])].copy()
    e=e[(e.unit_kind=='deposited_mouse')&e.age_months.isin([3,24])&(e.cell_type!='ALL')].copy()
    assert not c.duplicated(['dataset','mouse_id','cell_type']).any()
    assert not e.duplicated(['dataset','mouse_id','cell_type','gene']).any()
    universe=[]; coverage=[]; mice=[]; contrasts=[]; terms=[]; within=[]; loo=[]
    for ds in DATASETS+['Kidney_droplet']:
        d=c[c.dataset==ds]; metadata=d[['mouse_id','age_months','sex']].drop_duplicates().sort_values('mouse_id')
        count=d.pivot(index='mouse_id',columns='cell_type',values='cells').reindex(metadata.mouse_id).fillna(0)
        common=count.columns[(count>0).all(0)].tolist()
        for ct in count.columns:
            universe.append(dict(dataset=ds,cell_type=ct,in_common=ct in common,minimum_cells=int(count[ct].min()),stage='executed' if ds in DATASETS else 'held_whole_kidney_not_supported'))
        for m in metadata.itertuples(index=False):
            g=d[d.mouse_id==m.mouse_id];n=int(g.cells.sum());covered=int(g[g.cell_type.isin(common)].cells.sum())
            coverage.append(dict(dataset=ds,mouse_id=m.mouse_id,age_months=int(m.age_months),sex=m.sex,total_cells=n,common_cells=covered,covered_fraction=covered/n,omitted_cells=n-covered,n_common_types=len(common)))
        if ds not in DATASETS: continue
        assert common
        genes=sorted(e[e.dataset==ds].gene.unique())
        for scope in ['all_observed_sexes','male_only']:
            meta=metadata if scope=='all_observed_sexes' else metadata[metadata.sex=='male']
            ids=meta.mouse_id.tolist();ages=meta.age_months.to_numpy(); assert min((ages==3).sum(),(ages==24).sum())>=2
            n=count.loc[ids,common].to_numpy(float);p=n/n.sum(1,keepdims=True)
            ref=p[ages==3].mean(0)
            for gene in genes:
                eg=e[(e.dataset==ds)&(e.gene==gene)]
                for endpoint in ENDPOINTS:
                    x=eg.pivot(index='mouse_id',columns='cell_type',values=endpoint).reindex(index=ids,columns=common).to_numpy(float)
                    assert np.isfinite(x).all()
                    s,parts=decomposition(p,x,ages)
                    base=dict(dataset=ds,sex_scope=scope,gene=gene,endpoint=endpoint)
                    contrasts.append(dict(**base,n_3m=int((ages==3).sum()),n_24m=int((ages==24).sum()),n_common_types=len(common),**s))
                    for j,ct in enumerate(common):
                        within.append(dict(**base,cell_type=ct,n_3m=int((ages==3).sum()),n_24m=int((ages==24).sum()),mean_3m=float(x[ages==3,j].mean()),mean_24m=float(x[ages==24,j].mean()),difference=float(x[ages==24,j].mean()-x[ages==3,j].mean()),min_cells_3m=int(n[ages==3,j].min()),min_cells_24m=int(n[ages==24,j].min())))
                        terms.append(dict(**base,cell_type=ct,young_reference_weight=float(ref[j]),composition=float(parts[0][j]),within_type=float(parts[1][j]),interaction=float(parts[2][j]),animal_covariance=float(parts[3][j])))
                    for i,m in enumerate(meta.itertuples(index=False)):
                        observed=float(p[i]@x[i]);standard=float(ref@x[i])
                        raw=eg[(eg.mouse_id==m.mouse_id)&eg.cell_type.isin(common)]
                        direct=float(np.dot(raw.cells,raw[endpoint])/raw.cells.sum())
                        assert np.isclose(observed,direct,atol=1e-10)
                        if endpoint=='detected_fraction':assert np.isclose(observed,raw.positive_cells.sum()/raw.cells.sum(),atol=1e-10)
                        mice.append(dict(**base,mouse_id=m.mouse_id,age_months=int(m.age_months),sex=m.sex,common_cells=int(n[i].sum()),observed_common=observed,young_reference_standardized=standard))
                        keep=np.arange(len(ids))!=i
                        leave,_=decomposition(p[keep],x[keep],ages[keep])
                        loo.append(dict(**base,omitted_mouse=m.mouse_id,omitted_age=int(m.age_months),**leave))
    for name,rows in [('common_type_support',universe),('coverage',coverage),('composition_mouse',mice),('decomposition',contrasts),('decomposition_by_type',terms),('within_type',within),('leave_one_mouse_out',loo)]:write(out/(name+'.tsv'),rows)
    dump(out/'verification.json',{'passed':True,'checks':['Two hand-calculated decomposition cases, including nonzero interaction and animal covariance','Exact four-term reconstruction for every full and leave-one-mouse-out contrast','Independent count-weighted mean reconstruction for every animal and endpoint','Detection proportion independently reconstructed from positive-cell counts'],'primary_datasets':DATASETS,'display_genes':DISPLAY_GENES,'contrasts':len(contrasts),'biological_limit':'Within annotation is not necessarily cell intrinsic; no absolute abundance, senescence or secretion inference. Kidney held for whole-organ interpretation; its common universe is immune only.'})

def rarefaction(sizes,depth):
    n=sum(sizes)
    if depth<2 or n<2: return np.nan
    assert depth<=n
    return float(sum(k/n*(1-hypergeom.pmf(0,n-1,k-1,depth-1)) for k in sizes))

def repertoire(root,out):
    d=pd.read_csv(root/'analysis/research/runs/nb5_repertoire_v2/repertoire_cells.tsv',sep='\t')
    unmatched=d[d.mouse_id.isna()].copy();d=d[d.mouse_id.notna()].copy()
    assert not d.duplicated(['age_months','cell_name']).any() and d.tissue.notna().all()
    d['clone_key']=['source:'+str(g) if pd.notna(g) else 'singleton:'+str(c) for g,c in zip(d.clonal_group,d.cell_name)]
    keys=['age_months','mouse_id','clone_key']
    d['global_n']=d.groupby(keys).cell_name.transform('size')
    d['tissue_n']=d.groupby(keys).tissue.transform('nunique')
    d['local_n']=d.groupby(keys+['tissue']).cell_name.transform('size')
    assert (d.global_n==d.within_mouse_clone_size).all()
    d['category']=np.select([d.global_n==1,(d.global_n>1)&(d.local_n==1),(d.local_n>1)&(d.tissue_n==1)],['singleton_in_mouse','shared_only_singleton_here','local_repeat_one_tissue'],default='local_repeat_shared_clone')
    rows=[];clone_rows=[];support=[]
    for (age,m,cl),g in d.groupby(keys):
        clone_rows.append(dict(age_months=int(age),mouse_id=m,clone_key=cl,cells=len(g),n_tissues=g.tissue.nunique(),tissues=';'.join(sorted(g.tissue.unique()))))
    for (age,m,t),g in d.groupby(['age_months','mouse_id','tissue']):
        cats=g.category.value_counts();size=g.groupby('clone_key').size().tolist()
        row=dict(age_months=int(age),mouse_id=m,tissue=t,reconstructed_cells=len(g),local_clone_cells=int((g.local_n>1).sum()),global_clone_cells=int((g.global_n>1).sum()),shared_clone_cells=int((g.tissue_n>1).sum()),local_clone_fraction=float((g.local_n>1).mean()),global_clone_fraction=float((g.global_n>1).mean()),shared_clone_fraction=float((g.tissue_n>1).mean()))
        for cat in ['singleton_in_mouse','shared_only_singleton_here','local_repeat_one_tissue','local_repeat_shared_clone']:row[cat]=int(cats.get(cat,0))
        assert sum(row[cat] for cat in ['singleton_in_mouse','shared_only_singleton_here','local_repeat_one_tissue','local_repeat_shared_clone'])==len(g)
        assert sum(k for k in size if k>1)==row['local_clone_cells']
        rows.append(row)
    m=pd.DataFrame(rows)
    for t,g in m.groupby('tissue'):
        n=g.groupby('age_months').mouse_id.nunique().to_dict();depth=int(g.reconstructed_cells.min())
        eligible=all(n.get(a,0)>=2 for a in [3,18,24]) and depth>=2
        for age in [3,18,24]:
            a=g[g.age_months==age];support.append(dict(tissue=t,age_months=age,mice=len(a),min_cells=int(a.reconstructed_cells.min()) if len(a) else 0,max_cells=int(a.reconstructed_cells.max()) if len(a) else 0,focal=t in FOCAL_TISSUES,depth=depth,common_depth_eligible=eligible))
        if eligible:
            for idx,row in g.iterrows():
                sub=d[(d.age_months==row.age_months)&(d.mouse_id==row.mouse_id)&(d.tissue==t)]
                value=rarefaction(sub.groupby('clone_key').size().tolist(),depth)
                assert 0<=value<=row.local_clone_fraction+1e-12
                m.loc[idx,'common_depth']=depth;m.loc[idx,'expected_local_clone_fraction']=value
    summaries=[]
    for (t,age),g in m.groupby(['tissue','age_months']):
        for endpoint in ['local_clone_fraction','global_clone_fraction','shared_clone_fraction','expected_local_clone_fraction']:
            a=g[endpoint].dropna();summaries.append(dict(tissue=t,age_months=int(age),endpoint=endpoint,n_mice=len(a),mean=float(a.mean()) if len(a) else np.nan,min=float(a.min()) if len(a) else np.nan,max=float(a.max()) if len(a) else np.nan))
    # Balanced analysis uses exactly the same three tissues within each included mouse.
    focal=m[m.tissue.isin(FOCAL_TISSUES)]
    complete=focal.groupby(['age_months','mouse_id']).tissue.nunique();idx=complete[complete==len(FOCAL_TISSUES)].index
    selected=focal.set_index(['age_months','mouse_id']).loc[idx].reset_index()
    metadata=selected[['age_months','mouse_id']].drop_duplicates().sort_values(['age_months','mouse_id'])
    ids=pd.MultiIndex.from_frame(metadata[['age_months','mouse_id']])
    N=selected.pivot(index=['age_months','mouse_id'],columns='tissue',values='reconstructed_cells').reindex(index=ids,columns=FOCAL_TISSUES).to_numpy(float)
    q=selected.pivot(index=['age_months','mouse_id'],columns='tissue',values='local_clone_fraction').reindex(index=ids,columns=FOCAL_TISSUES).to_numpy(float)
    p=N/N.sum(1,keepdims=True);ages=metadata.age_months.to_numpy();assert (ages==3).sum()>=2
    ref=p[ages==3].mean(0);balanced=[];dec=[];bt=[];sensitivity=[]
    for i,row in enumerate(metadata.itertuples(index=False)):
        observed=float(p[i]@q[i]);direct=selected[(selected.mouse_id==row.mouse_id)&(selected.age_months==row.age_months)]
        assert np.isclose(observed,direct.local_clone_cells.sum()/direct.reconstructed_cells.sum())
        balanced.append(dict(age_months=int(row.age_months),mouse_id=row.mouse_id,total_focal_cells=int(N[i].sum()),observed_local_fraction=observed,young_reference_standardized=float(ref@q[i]),equal_tissue_fraction=float(q[i].mean())))
        for j,t in enumerate(FOCAL_TISSUES):bt.append(dict(age_months=int(row.age_months),mouse_id=row.mouse_id,tissue=t,fraction=float(p[i,j]),local_clone_fraction=float(q[i,j]),young_reference_weight=float(ref[j])))
    for old in [18,24]:
        keep=np.isin(ages,[3,old]);agecode=np.where(ages[keep]==3,3,24)
        assert (agecode==24).sum()>=2
        z,_=decomposition(p[keep],q[keep],agecode);dec.append(dict(old_age=old,n_young=int((agecode==3).sum()),n_old=int((agecode==24).sum()),**z))
        selectedmeta=metadata.loc[keep]
        for i,row in enumerate(selectedmeta.itertuples(index=False)):
            k=np.arange(keep.sum())!=i;v,_=decomposition(p[keep][k],q[keep][k],agecode[k]);sensitivity.append(dict(old_age=old,omitted_mouse=row.mouse_id,omitted_age=int(row.age_months),**v))
    write(out/'tissue_mouse.tsv',m);write(out/'tissue_summary.tsv',summaries);write(out/'tissue_support.tsv',support)
    write(out/'clone_distribution.tsv',clone_rows);write(out/'balanced_mouse.tsv',balanced);write(out/'balanced_tissue.tsv',bt);write(out/'balanced_decomposition.tsv',dec);write(out/'leave_one_mouse_out.tsv',sensitivity)
    write(out/'unmatched_source_rows.tsv',unmatched)
    dump(out/'verification.json',{'passed':True,'matched_rows':len(d),'unmatched_rows':len(unmatched),'focal_tissues':FOCAL_TISSUES,'balanced_mice_by_age':{str(k):int(v) for k,v in metadata.groupby('age_months').size().items()},'checks':['Independent clone-size partition reproduces frozen within-mouse sizes','Four cell categories partition every tissue-mouse sample','Common-depth expectation agrees with exhaustive toy enumeration and never exceeds observed local fraction','Balanced tissue-weighted fraction equals direct numerator/denominator','Exact four-term decomposition including animal covariance for both contrasts and all deletions'],'limits':'T-cell subtype and receptor-assembly selection remain unresolved. Within-tissue restriction is not subset matching. Shared clones do not prove migration; clone size does not measure proliferation, antigen specificity or immune competence.'})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--branch',choices=['composition','repertoire'],required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True);toy_checks()
    (composition if args.branch=='composition' else repertoire)(Path.cwd(),out)
    print(json.dumps({'branch':args.branch,'completed':True,'scientific_acceptance':'not_assessed'}))

if __name__=='__main__':main()
