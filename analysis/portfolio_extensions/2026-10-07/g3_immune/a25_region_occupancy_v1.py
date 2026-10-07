"""Describe all exposed source clusters by mouse/region; never infer a new state."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

REGIONS=['Cerebellum','Cortex','Hippocampus','Striatum']
FLOOR=20

def calculate(cells):
    clusters=sorted(cells.leiden.unique(),key=lambda x:int(x))
    mice=cells[['mouse_id','age_months','sex']].drop_duplicates()
    assert not mice.mouse_id.duplicated().any()
    rows,support=[],[]
    for m in mice.itertuples(index=False):
        x=cells[cells.mouse_id==m.mouse_id]
        valid=[]
        for region in REGIONS:
            r=x[x.region==region]; n=len(r); eligible=n>=FLOOR
            support.append(dict(mouse_id=m.mouse_id,age_months=m.age_months,sex=m.sex,region=region,cells=n,eligible=eligible))
            if not eligible: continue
            valid.append(region)
            counts=r.leiden.value_counts()
            for cluster in clusters:
                rows.append(dict(mouse_id=m.mouse_id,age_months=m.age_months,sex=m.sex,basis=region,cluster=cluster,
                                 fraction=float(counts.get(cluster,0)/n),cells=n))
        counts=x.leiden.value_counts()
        for cluster in clusters:
            rows.append(dict(mouse_id=m.mouse_id,age_months=m.age_months,sex=m.sex,basis='pooled_all',cluster=cluster,
                             fraction=float(counts.get(cluster,0)/len(x)),cells=len(x)))
        if len(valid)==4:
            for cluster in clusters:
                pooled=float(counts.get(cluster,0)/len(x))
                equal=float(np.mean([r['fraction'] for r in rows if r['mouse_id']==m.mouse_id and r['cluster']==cluster and r['basis'] in REGIONS]))
                for basis,value in [('pooled_complete',pooled),('equal_region',equal)]:
                    rows.append(dict(mouse_id=m.mouse_id,age_months=m.age_months,sex=m.sex,basis=basis,cluster=cluster,fraction=value,cells=len(x)))
    estimates=pd.DataFrame(rows); supp=pd.DataFrame(support); contrasts=[]
    for sex in ['all','male','female']:
        sx=estimates if sex=='all' else estimates[estimates.sex==sex]
        for basis in REGIONS+['pooled_all','pooled_complete','equal_region']:
            for older in [18,24]:
                for cluster in clusters:
                    ss=sx[(sx.basis==basis)&(sx.cluster==cluster)]
                    a=ss[ss.age_months==3]; b=ss[ss.age_months==older]
                    rec=dict(sex_scope=sex,basis=basis,older_months=older,cluster=cluster,n_young=len(a),n_older=len(b),
                             status='eligible' if min(len(a),len(b))>=2 else 'held_fewer_than_two_mice')
                    if rec['status']=='eligible':
                        av,bv=a.fraction.to_numpy(),b.fraction.to_numpy()
                        deletions=[float(bv.mean()-np.delete(av,i).mean()) for i in range(len(av))]+[float(np.delete(bv,i).mean()-av.mean()) for i in range(len(bv))]
                        rec.update(young_mean=float(av.mean()),older_mean=float(bv.mean()),difference=float(bv.mean()-av.mean()),
                                   deletion_low=min(deletions),deletion_high=max(deletions))
                    contrasts.append(rec)
    return supp,estimates,pd.DataFrame(contrasts)

def verify(cells,estimates):
    counts=Counter((r.mouse_id,r.region,str(r.leiden)) for r in cells.itertuples(index=False))
    totals=Counter((r.mouse_id,r.region) for r in cells.itertuples(index=False))
    worst=0.; checks=0
    for r in estimates.itertuples(index=False):
        if r.basis in REGIONS:
            expected=counts[(r.mouse_id,r.basis,str(r.cluster))]/totals[(r.mouse_id,r.basis)]
        elif r.basis=='equal_region':
            expected=sum(counts[(r.mouse_id,reg,str(r.cluster))]/totals[(r.mouse_id,reg)] for reg in REGIONS)/4
        else:
            expected=sum(counts[(r.mouse_id,reg,str(r.cluster))] for reg in REGIONS)/sum(totals[(r.mouse_id,reg)] for reg in REGIONS)
        error=abs(expected-r.fraction); assert error<1e-12; worst=max(worst,error);checks+=1
    assert np.allclose(estimates.groupby(['mouse_id','basis']).fraction.sum(),1)
    return dict(passed=True,arithmetic_checks=checks,maximum_error=worst,scope='Independent cell counters and fraction sum checks; same source data, not replication.')

def synthetic_test():
    rows=[]
    for mouse,age in [('y1',3),('y2',3),('o1',24),('o2',24)]:
        for region in REGIONS:
            n=80 if region=='Cortex' and age==24 else 20
            for i in range(n): rows.append(dict(mouse_id=mouse,age_months=age,sex='male',region=region,leiden='1' if region=='Cortex' else '0'))
    x=pd.DataFrame(rows); s,e,c=calculate(x);verify(x,e)
    f=c[(c.sex_scope=='male')&(c.older_months==24)&(c.cluster=='1')]
    assert abs(float(f[f.basis=='equal_region'].difference.iloc[0]))<1e-12
    assert float(f[f.basis=='pooled_complete'].difference.iloc[0])>0
    assert (c[c.sex_scope=='female'].status!='eligible').all()
    print('synthetic region-mixture and missing-sex checks passed')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input');ap.add_argument('--output');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    if a.self_test: synthetic_test();return
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    full=pd.read_csv(a.input,sep='\t',dtype={'leiden':str})
    assert not full.cell_id.duplicated().any()
    x=full[full.cell_ontology_class=='microglial cell'].copy()
    assert len(x)==13130 and x.source_index.notna().all()
    for left,right in [('age','official_age'),('mouse_id','official_mouse.id'),('sex','official_sex'),('subtissue','official_subtissue')]:
        assert (x[left].astype(str).str.strip()==x[right].astype(str).str.strip()).all(),(left,right)
    assert (x.official_cell_ontology_class=='microglial cell').all()
    x['region']=x.subtissue.str.strip(); x['age_months']=x.age.str.replace('m','',regex=False).astype(int)
    assert set(x.region)==set(REGIONS) and set(x.age_months)=={3,18,24}
    support,estimates,contrasts=calculate(x);checks=verify(x,estimates)
    for name,frame in [('region_support',support),('mouse_cluster_fractions',estimates),('age_contrasts',contrasts)]:frame.to_csv(out/(name+'.csv'),index=False)
    (out/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
    result=dict(unit='mouse; regions and cells nested',cells=len(x),mice=int(x.mouse_id.nunique()),source_clusters=sorted(x.leiden.unique(),key=int),
                complete_region_mice=estimates[estimates.basis=='equal_region'][['mouse_id','age_months','sex']].drop_duplicates().to_dict('records'),
                held_comparisons=contrasts[contrasts.status!='eligible'][['sex_scope','basis','older_months','n_young','n_older']].drop_duplicates().to_dict('records'),
                limit='Source Leiden occupancy, not final-paper state correspondence, state discovery, within-cell transition, absolute abundance, sex-adjusted age effect, distinct-state model test, disease mechanism or function.')
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,axes=plt.subplots(2,2,figsize=(13,7),layout='constrained')
    for ax,(sex,age) in zip(axes.flat,[('all',18),('all',24),('male',18),('male',24)]):
        sl=contrasts[(contrasts.sex_scope==sex)&(contrasts.older_months==age)]
        table=sl.pivot(index='cluster',columns='basis',values='difference').reindex(columns=REGIONS+['pooled_complete','equal_region'])
        table=table.reindex(sorted(table.index,key=int)); vals=100*table.to_numpy()
        im=ax.imshow(vals,aspect='auto',cmap='RdBu_r',vmin=-50,vmax=50)
        ax.set_xticks(range(len(table.columns)),['Cb','Ctx','Hip','Str','Pooled*','Equal region'],rotation=20)
        ax.set_yticks(range(len(table.index)),table.index);ax.set_ylabel('Deposited cluster ID')
        ax.set_title(f'{sex}: {age} minus 3 months (percentage points)')
    fig.colorbar(im,ax=axes.ravel().tolist(),label='Captured cluster fraction difference (pp)',shrink=.75)
    fig.suptitle('A25 region context: all deposited microglial clusters retained')
    fig.supxlabel('*Pooled and equal-region use the same complete-region mice. Blank = held support; cluster IDs are not biological state names.',fontsize=9)
    fig.savefig(out/'region_occupancy.png',dpi=200);fig.savefig(out/'region_occupancy.svg');plt.close(fig)
    print(json.dumps(dict(cells=len(x),mice=int(x.mouse_id.nunique()),verification=checks)))

if __name__=='__main__':main()
