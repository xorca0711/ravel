"""Exposed fixed-panel source description; no population or functional inference."""
import argparse,csv,gzip,json
from pathlib import Path
import numpy as np
from plot_v1 import render
ROOT=Path(__file__).resolve().parents[3]
PKG=Path(__file__).resolve().parents[1]
LIBS=['Unt_1','Unt_2','BS30_1','BS30_2','BS65_1','BS65_2','BS45_1','BS45_2']
GROUPS=np.array(['PBS','PBS','WT','WT','DE','DE','SUPER','SUPER'])
METRICS=['WT-PBS','DE-PBS','SUPER-PBS','DE-WT','SUPER-WT']

def write(path,rows,fields=None):
    if fields is None:fields=list(rows[0])
    with path.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

def median_ratio_denominators(counts):
    positive=(counts>0).all(axis=1)
    assert positive.any()
    z=counts[positive]; geo=np.exp(np.log(z).mean(axis=1))
    sf=np.median(z/geo[:,None],axis=0);sf/=np.exp(np.log(sf).mean())
    den=sf*np.exp(np.log(counts.sum(axis=0)).mean())
    assert np.isfinite(den).all() and (den>0).all()
    return den,sf,int(positive.sum())

def contrast_values(expr,groups):
    means={g:expr[:,groups==g].mean(axis=1) for g in ['PBS','WT','DE','SUPER']}
    return {m:means[m.split('-')[0]]-means[m.split('-')[1]] for m in METRICS}

def load():
    tables=[]
    for k in ['readcount','fpkm']:
        with gzip.open(ROOT/f'raw_data/Sx10/GSE160332_070720_10_{k}_genename.txt.gz','rt',encoding='utf-8') as f:tables.append(list(csv.DictReader(f,delimiter='\t')))
    ids=[r['gene_id'] for r in tables[0]];fmap={r['gene_id']:r for r in tables[1]}
    assert len(set(ids))==len(ids)==len(fmap) and set(ids)==set(fmap)
    tables[1]=[fmap[g] for g in ids]
    ann=[{k:v for k,v in r.items() if k not in LIBS} for r in tables[0]]
    assert ann==[{k:v for k,v in r.items() if k not in LIBS} for r in tables[1]]
    arrays=[np.asarray([[float(r[l]) for l in LIBS] for r in t]) for t in tables]
    assert all(np.isfinite(a).all() and (a>=0).all() for a in arrays)
    assert np.equal(arrays[0],np.floor(arrays[0])).all()
    return ann,*arrays

def main(out):
    ann,counts,fpkm=load();sizes=counts.sum(axis=0);assert (sizes>0).all()
    cpm=counts/sizes*1e6;eligible=(cpm>=1).sum(axis=1)>=2
    panels=json.loads((PKG/'sources/figure5_memberships_v1.json').read_text())['panels']
    members=list(dict.fromkeys(s for ss in panels.values() for s in ss));idx={}
    for s in members:
        ix=[i for i,r in enumerate(ann) if r['gene_name']==s]
        assert len(ix)==1, 'Mapping changed since qualification'
        idx[s]=ix[0]
    background=eligible.copy();background[list(idx.values())]=False
    assert background.any()
    panel_idx={p:[idx[s] for s in ss if eligible[idx[s]]] for p,ss in panels.items()}
    tested=[];panel_rows=[];fits=[];norm=[];target_values=[];full_contrasts=None
    for view in ['full']+['omit_'+l for l in LIBS]:
        keep=np.array([view!='omit_'+l for l in LIBS]);kept=[l for l,k in zip(LIBS,keep) if k]
        mrden,sf,npositive=median_ratio_denominators(counts[:,keep])
        for j,lib in enumerate(kept):norm.append(dict(view=view,library=lib,count_sum=float(sizes[keep][j]),median_ratio_factor=float(sf[j]),effective_library_size=float(mrden[j]),positive_reference_rows=npositive))
        for scale,abundance in [('CPM',cpm[:,keep]),('MR_CPM',counts[:,keep]/mrden*1e6),('FPKM',fpkm[:,keep])]:
            expr=np.log2(abundance+1);cv=contrast_values(expr,GROUPS[keep]);x=cv['WT-PBS'];xx=float(np.dot(x[background],x[background]));assert xx>0
            betas={}
            for variant in ['DE','SUPER']:
                y=cv[variant+'-PBS'];beta=float(np.dot(x[background],y[background])/xx);betas[variant]=beta
                cv[variant+'_residual']=y-beta*x
                fits.append(dict(scale=scale,view=view,variant=variant,background_rows=int(background.sum()),beta=beta,sum_x_squared=xx,sum_xy=float(np.dot(x[background],y[background])),rms_residual=float(np.sqrt(np.mean((y[background]-beta*x[background])**2)))))
            for s,i in idx.items():
                tested.append(dict(symbol=s,gene_id=ann[i]['gene_id'],eligible=bool(eligible[i]),scale=scale,view=view,**{k:float(v[i]) for k,v in cv.items()}))
                if view=='full':
                    for j,lib in enumerate(kept):target_values.append(dict(symbol=s,gene_id=ann[i]['gene_id'],eligible=bool(eligible[i]),scale=scale,library=lib,arm=GROUPS[keep][j],abundance=float(abundance[i,j]),log2_plus_1=float(expr[i,j])))
            for panel,ii in panel_idx.items():
                for variant in ['DE','SUPER']:
                    y=cv[variant+'-PBS'];same=x[ii]*y[ii]>0
                    panel_rows.append(dict(panel=panel,scale=scale,view=view,variant=variant,source_members=len(panels[panel]),eligible_members=len(ii),median_WT_PBS=float(np.median(x[ii])),median_variant_PBS=float(np.median(y[ii])),median_direct=float(np.median(cv[variant+'-WT'][ii])),median_residual=float(np.median(cv[variant+'_residual'][ii])),closer_to_PBS=int(np.sum(np.abs(y[ii])<np.abs(x[ii]))),same_direction=int(same.sum()),weaker_same_direction=int(np.sum(same&(np.abs(y[ii])<np.abs(x[ii])))),opposite_direction=int(np.sum(x[ii]*y[ii]<0))))
            if view=='full' and scale=='CPM':
                full_contrasts=cv.copy()
                write(out/'all_gene_primary.csv',(dict(gene_id=r['gene_id'],symbol=r['gene_name'],eligible=bool(eligible[i]),background=bool(background[i]),**{l+'_log2_CPM_plus_1':float(expr[i,j]) for j,l in enumerate(LIBS)},**{k:float(v[i]) for k,v in cv.items()}) for i,r in enumerate(ann)),['gene_id','symbol','eligible','background']+[l+'_log2_CPM_plus_1' for l in LIBS]+list(cv))
    ranges=[]
    for s in members:
        for scale in ['CPM','MR_CPM','FPKM']:
            rows=[r for r in tested if r['symbol']==s and r['scale']==scale]
            for metric in METRICS+['DE_residual','SUPER_residual']:
                ranges.append(dict(symbol=s,eligible=bool(eligible[idx[s]]),scale=scale,metric=metric,full=next(r[metric] for r in rows if r['view']=='full'),omission_min=min(r[metric] for r in rows if r['view']!='full'),omission_max=max(r[metric] for r in rows if r['view']!='full')))
    write(out/'normalization_factors.csv',norm);write(out/'target_library_values.csv',target_values);write(out/'target_sensitivity.csv',tested);write(out/'target_ranges.csv',ranges);write(out/'panel_summaries.csv',panel_rows);write(out/'amplitude_fits.csv',fits)
    summary=dict(rows=len(ann),eligible_rows=int(eligible.sum()),background_rows=int(background.sum()),unique_targets=len(members),eligible_targets=int(eligible[list(idx.values())].sum()),scales=['CPM','MR_CPM','FPKM'],views=9,panel_overlap='Figure5B is wholly contained in Figure5A; no independent replication',unmeasured='Donor population effects, STAT mediation, myeloid suppression, secretion and protection')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    render(out,panels,target_values,tested,ranges,fits,full_contrasts,background)
    print(json.dumps(summary))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);main(a.parse_args().output)
