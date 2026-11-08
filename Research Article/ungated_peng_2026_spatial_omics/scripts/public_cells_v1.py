"""Fixed A12 barcode RNA description. Source files are always read-only."""
import argparse, json, math
from pathlib import Path
import h5py
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'Research Article/ungated_peng_2026_spatial_omics'
GENES = ['IL1R1','IL1RAP','IL1R2','IL1RN','SIGIRR','MYD88','IRAK1','IRAK4','NFKBIA','TNFAIP3']
PAIRS = [('IL1R1',g) for g in ['IL1RAP','IL1R2','IL1RN','SIGIRR']]
PATIENTS = [4,5,6,7,14,17,18,19,21,22,24,25]

def load_library(item):
    paths = {Path(x['path']).name:ROOT/x['path'] for x in item['files']}
    a = pd.read_csv(paths['cell_annotations.csv.gz'])
    with h5py.File(paths['raw_counts.csc.h5'],'r') as h:
        assert h.attrs['format']=='review_gene_row_CSC_v1'
        n, ng = h.attrs['shape']; genes=h['genes'].asstr()[:].tolist()
        assert len(genes)==len(set(genes))==ng
        ix=a.source_cell_index.to_numpy(dtype=int)
        assert len(np.unique(ix))==len(ix) and np.all((ix>=0)&(ix<n))
        assert a.cell_id.tolist()==[item['gsm']+':'+b for b in h['barcodes'].asstr()[:][ix]]
        assert a.gsm.eq(item['gsm']).all() and a.patient.eq(int(item['patient'])).all()
        assert a.histology.eq(item['histology']).all()
        total=h['full_library_size'][:]; detected=h['n_genes_by_counts'][:]
        mt=100*h['mitochondrial_counts'][:]/np.maximum(total,1)
        qc=(total>=1000)&(detected>=500)&(mt<20)
        assert np.array_equal(np.sort(ix),np.flatnonzero(qc)) and a.qc_pass.all()
        assert np.array_equal(total[ix],a.full_library_size) and np.array_equal(detected[ix],a.n_genes_by_counts)
        assert np.allclose(mt[ix],a.pct_counts_mt,rtol=0,atol=1e-10)
        ptr=h['indptr'][:]; counts=np.zeros((len(a),len(GENES)),dtype=np.int64)
        for k,g in enumerate(GENES):
            assert genes.count(g)==1
            j=genes.index(g); lo,hi=int(ptr[j]),int(ptr[j+1]); ind=h['indices'][lo:hi]; val=h['data'][lo:hi]
            assert len(np.unique(ind))==len(ind) and np.all((ind>=0)&(ind<n)) and np.all(val>0)
            whole=np.zeros(n,dtype=np.int64);whole[ind]=val;counts[:,k]=whole[ix]
        assert np.all(counts.sum(axis=1)<=total[ix])
    a[GENES]=counts
    return a,dict(gsm=item['gsm'],patient=int(item['patient']),histology=item['histology'],raw_cells=int(n),qc_cells=len(a),genes=int(ng),join_checks='passed')

def masks(a):
    u=a.ann_finest_level_uncertainty; at=a.ann_finest_level.eq('AT2'); ep=a.ann_level_1.eq('Epithelial')
    assert u.notna().all() and u.between(0,1).all()
    return {'AT2_u20':at&(u<=.2),'AT2_u30':at&(u<=.3),'AT2_allQC':at,
            'Epithelial_u20':ep&(u<=.2),'Epithelial_allQC':ep}

def measurements(a, meta):
    out=[]; pairs=[]; n=len(a)
    if not n:return out,pairs
    den=a.full_library_size.to_numpy(dtype=float); counts=a[GENES].to_numpy(dtype=np.int64)
    log=np.log2(1+10000*counts/den[:,None])
    for k,g in enumerate(GENES):
        pos=counts[:,k]>0; nd=int(pos.sum()); cs=int(counts[:,k].sum())
        out.append(dict(**meta,gene=g,cells=n,library_total=int(den.sum()),count_sum=cs,detected=nd,
            fraction_detected=nd/n,mean_count=cs/n,mean_log=log[:,k].mean(),
            positive_mean_log=log[pos,k].mean() if nd else np.nan,pseudobulk_logCPM=np.log2(1+1e6*cs/den.sum()),
            median_library=float(np.median(den)),median_genes=float(a.n_genes_by_counts.median())))
    for x,y in PAIRS:
        px=a[x].to_numpy()>0; py=a[y].to_numpy()>0
        c=[int(((px==i)&(py==j)).sum()) for i,j in [(0,0),(1,0),(0,1),(1,1)]]
        pairs.append(dict(**meta,pair=x+'__'+y,cells=n,n00=c[0],n10=c[1],n01=c[2],n11=c[3],
            joint_fraction=c[3]/n,conditional_on_IL1R1=c[3]/int(px.sum()) if px.any() else np.nan,
            marginal_product=float(px.mean()*py.mean())))
    return out,pairs

def summarize_pairs(table,features,key,metrics):
    records=[]
    for (population,patient,feature),g in table.groupby(['population','patient',key]):
        if int(patient) not in PATIENTS:continue
        gg=g.set_index('histology')
        if not {'normal','LUAD'}<=set(gg.index):continue
        if min(gg.loc['normal','cells'],gg.loc['LUAD','cells'])<50:continue
        for m in metrics:
            records.append(dict(population=population,patient=int(patient),feature=feature,metric=m,
                normal=gg.loc['normal',m],LUAD=gg.loc['LUAD',m],delta=gg.loc['LUAD',m]-gg.loc['normal',m]))
    return records

def plot_results(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    d=pd.read_csv(out/'paired_deltas.csv');p=d[d.population.eq('AT2_u20')]
    fig,axes=plt.subplots(1,3,figsize=(11,4.2),layout='constrained')
    for ax,metric,title in zip(axes,['fraction_detected','positive_mean_log','joint_fraction'],['Detection fraction','Intensity among detected nuclei','IL1R1 / IL1RAP co-detection']):
        z=p[p.metric.eq(metric)]
        features=GENES[:5] if metric!='joint_fraction' else ['IL1R1__IL1RAP']
        for i,g in enumerate(features):
            v=z[z.feature.eq(g)].sort_values('patient');xx=i+np.linspace(-.16,.16,len(v))
            ax.scatter(xx,v.delta,color='#0072B2',s=19,alpha=.75)
            if len(v):ax.plot([i-.25,i+.25],[v.delta.mean()]*2,color='#D55E00',lw=2)
        ax.axhline(0,color='.5',lw=.8);ax.set_xticks(range(len(features)),[x.replace('__',' / ') for x in features],rotation=45,ha='right');ax.set_title(title)
        ax.set_ylabel('LUAD minus normal'+('\nlog2(1 + normalized RNA)' if metric=='positive_mean_log' else ''))
    fig.suptitle('A12: fixed candidate AT2 labels, 12 paired patients\nDots are patients; orange bars are equal-patient means',fontsize=12)
    for ext in ['png','pdf']:fig.savefig(out/f'cell_components.{ext}',dpi=300)
    plt.close(fig)
    s=d[(d.feature.isin(['IL1R1','IL1RAP','IL1R1__IL1RAP']))&d.metric.isin(['fraction_detected','joint_fraction'])]
    depth=pd.read_csv(out/'depth_standardized_deltas.csv');fig,axes=plt.subplots(1,3,figsize=(11,4),layout='constrained')
    pops=['AT2_u20','AT2_u30','AT2_allQC','Epithelial_u20','Epithelial_allQC']
    for ax,g in zip(axes,['IL1R1','IL1RAP','IL1R1__IL1RAP']):
        z=s[s.feature.eq(g)]
        for i,pop in enumerate(pops):
            v=z[z.population.eq(pop)].delta.dropna();ax.scatter(np.full(len(v),i),v,s=13,alpha=.5,color='#0072B2')
            if len(v):ax.plot([i-.22,i+.22],[v.mean()]*2,color='#D55E00',lw=2)
        v=depth[depth.feature.eq(g)].delta.dropna();ax.scatter(np.full(len(v),5),v,s=13,color='#009E73',alpha=.6)
        if len(v):ax.plot([4.78,5.22],[v.mean()]*2,color='#D55E00',lw=2)
        ax.set_xticks(range(6),['AT2 .2','AT2 .3','AT2 all','Epi .2','Epi all','Depth'],rotation=45,ha='right');ax.axhline(0,color='.5',lw=.8);ax.set_title(g.replace('__',' / '));ax.set_ylabel('Paired fraction difference')
    fig.suptitle('Candidate selection and depth sensitivity\nSame original patient roster; missing support remains missing',fontsize=12)
    for ext in ['png','pdf']:fig.savefig(out/f'cell_sensitivity.{ext}',dpi=300)
    plt.close(fig)

def main(out):
    manifest=json.loads((PAPER/'sources/public_cells_manifest_v1.json').read_text())
    allcells=[];qual=[];inventory=[];librows=[];libpairs=[]
    for i,item in enumerate(manifest['libraries']):
        a,q=load_library(item);allcells.append(a);qual.append(q)
        a['confidence_band']=pd.cut(a.ann_finest_level_uncertainty,[-np.inf,.2,.3,np.inf],labels=['<=0.2','(0.2,0.3]','>0.3'])
        inv=a.groupby(['gsm','patient','histology','ann_level_1','ann_finest_level','confidence_band'],observed=True,dropna=False).size().reset_index(name='cells');inventory.extend(inv.to_dict('records'))
        for pop,mask in masks(a).items():
            r,p=measurements(a.loc[mask],dict(gsm=item['gsm'],patient=int(item['patient']),histology=item['histology'],population=pop));librows+=r;libpairs+=p
        if (i+1)%15==0:print('qualified libraries',i+1,flush=True)
    a=pd.concat(allcells,ignore_index=True);rows=[];pairs=[]
    for pop,mask in masks(a).items():
        for (patient,hist),group in a.loc[mask].groupby(['patient','histology']):
            r,p=measurements(group,dict(patient=int(patient),histology=hist,population=pop));rows+=r;pairs+=p
    gene=pd.DataFrame(rows);pair=pd.DataFrame(pairs)
    primary=gene[gene.population.eq('AT2_u20')&gene.patient.isin(PATIENTS)&gene.histology.isin(['normal','LUAD'])]
    assert len(primary)==240 and primary.cells.ge(50).all()
    pd.DataFrame(qual).to_csv(out/'source_qualification.csv',index=False)
    pd.DataFrame(inventory).to_csv(out/'label_confidence_inventory.csv',index=False)
    pd.DataFrame(librows).to_csv(out/'library_gene_components.csv',index=False)
    pd.DataFrame(libpairs).to_csv(out/'library_codetection.csv',index=False)
    gene.to_csv(out/'patient_gene_components.csv',index=False);pair.to_csv(out/'patient_codetection.csv',index=False)
    deltas=summarize_pairs(gene,GENES,'gene',['fraction_detected','mean_log','positive_mean_log','pseudobulk_logCPM'])
    deltas+=summarize_pairs(pair,PAIRS,'pair',['joint_fraction','conditional_on_IL1R1'])
    d=pd.DataFrame(deltas);d.to_csv(out/'paired_deltas.csv',index=False)
    summary=[]
    for key,g in d.groupby(['population','feature','metric']):
        v=g.delta.dropna().to_numpy();n=len(v)
        summary.append(dict(zip(['population','feature','metric'],key),n=n,mean=v.mean() if n else np.nan,median=np.median(v) if n else np.nan,min=v.min() if n else np.nan,max=v.max() if n else np.nan,positive=int((v>0).sum()),loo_mean_min=min((v.sum()-v)/(n-1)) if n>1 else np.nan,loo_mean_max=max((v.sum()-v)/(n-1)) if n>1 else np.nan))
    pd.DataFrame(summary).to_csv(out/'paired_summary.csv',index=False)
    # Equal-block view preserves within-patient nesting; never calls blocks independent.
    lg=pd.DataFrame(librows).groupby(['population','patient','histology','gene'],as_index=False).agg(cells=('cells','sum'),fraction_detected=('fraction_detected','mean'),mean_log=('mean_log','mean'),positive_mean_log=('positive_mean_log','mean'))
    lp=pd.DataFrame(libpairs).groupby(['population','patient','histology','pair'],as_index=False).agg(cells=('cells','sum'),joint_fraction=('joint_fraction','mean'))
    block=summarize_pairs(lg,GENES,'gene',['fraction_detected','mean_log','positive_mean_log'])+summarize_pairs(lp,PAIRS,'pair',['joint_fraction'])
    pd.DataFrame(block).to_csv(out/'equal_block_deltas.csv',index=False)
    # Frozen joint depth strata, common support only.
    z=a.loc[masks(a)['AT2_u20']&a.patient.isin(PATIENTS)&a.histology.isin(['normal','LUAD'])].copy()
    z['depth_bin']=np.searchsorted([2000,4000,8000],z.full_library_size,side='right')
    z['gene_bin']=np.searchsorted([1000,2000,4000],z.n_genes_by_counts,side='right')
    ds=[];support=[]
    for patient,g in z.groupby('patient'):
        ns=g.groupby(['depth_bin','gene_bin','histology']).size().unstack(fill_value=0).reindex(columns=['normal','LUAD'],fill_value=0)
        valid=ns.min(axis=1)>=5; weights=ns.sum(axis=1).loc[valid];weights=weights/weights.sum()
        for bins,row in ns.iterrows():support.append(dict(patient=int(patient),depth_bin=bins[0],gene_bin=bins[1],normal=int(row['normal']),LUAD=int(row['LUAD']),included=bool(valid.loc[bins]),weight=float(weights.get(bins,0))))
        for feature in GENES+[x+'__'+y for x,y in PAIRS]:
            vals={}
            for hist in ['normal','LUAD']:
                v=0.
                for bins,w in weights.items():
                    h=g[(g.histology==hist)&(g.depth_bin==bins[0])&(g.gene_bin==bins[1])]
                    present=np.ones(len(h),dtype=bool)
                    for name in feature.split('__'):present &= h[name].to_numpy()>0
                    v+=w*present.mean()
                vals[hist]=v if len(weights) else np.nan
            ds.append(dict(patient=int(patient),feature=feature,normal=vals['normal'],LUAD=vals['LUAD'],delta=vals['LUAD']-vals['normal'],common_bins=int(valid.sum()),normal_retained_fraction=ns.loc[valid,'normal'].sum()/ns['normal'].sum(),LUAD_retained_fraction=ns.loc[valid,'LUAD'].sum()/ns['LUAD'].sum()))
    pd.DataFrame(support).to_csv(out/'depth_support.csv',index=False);pd.DataFrame(ds).to_csv(out/'depth_standardized_deltas.csv',index=False)
    from verify_public_cells_v1 import verify
    verification=verify(ROOT,manifest,out)
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    assert verification['failures']==[]
    plot_results(out)
    (out/'summary.json').write_text(json.dumps({'libraries':len(qual),'QC_nuclei':len(a),'primary_patients':PATIENTS,'primary_units':24,'primary_AT2_nuclei':int(primary.drop_duplicates(['patient','histology']).cells.sum()),'verification_checks':verification['checks'],'scope':'same-source descriptive candidate compartments; no state/causal/protein or predictive inference'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();main(args.output)
