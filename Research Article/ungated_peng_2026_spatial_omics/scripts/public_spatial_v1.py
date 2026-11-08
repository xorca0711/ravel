"""Bounded descriptive graph organization of public Visium RNA; no spot tests."""
import argparse, gc, gzip, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import mmread
from scipy.sparse.csgraph import connected_components
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[3]
PAPER=ROOT/'Research Article/ungated_peng_2026_spatial_omics'
GENES=['IL1B','CLDN4','C1QA','COL1A1','KRT8']
OFFSETS=[(0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)]
MODES=['centered','depth','depth_composition']

def adjacency(rows,cols):
    lookup={(int(r),int(c)):i for i,(r,c) in enumerate(zip(rows,cols))}
    assert len(lookup)==len(rows)
    edges=[(i,lookup[(r+dr,c+dc)]) for (r,c),i in lookup.items() for dr,dc in OFFSETS if (r+dr,c+dc) in lookup]
    if not edges:return sparse.csr_matrix((len(rows),len(rows)),dtype=float)
    i,j=zip(*edges);return sparse.csr_matrix((np.ones(len(i)),(i,j)),shape=(len(rows),len(rows)))

def rownorm(a):
    degree=np.asarray(a.sum(axis=1)).ravel()
    return sparse.diags(np.divide(1,degree,out=np.zeros_like(degree,dtype=float),where=degree>0))@a

def residuals(frame,mode,labels):
    values=frame[['IL1B','CLDN4']].to_numpy();res=np.zeros_like(values)
    for label in np.unique(labels):
        ix=np.flatnonzero(labels==label);a=frame.iloc[ix];x=[np.ones(len(ix))]
        if mode!='centered':x += [np.log1p(a.total_counts),np.log1p(a.detected_genes)]
        if mode=='depth_composition':x += [a[g].to_numpy() for g in ['C1QA','COL1A1','KRT8']]
        design=np.column_stack(x);beta=np.linalg.lstsq(design,values[ix],rcond=None)[0];res[ix]=values[ix]-design@beta
    scale=np.sqrt((res**2).mean(axis=0))
    if np.any(scale<1e-12):return None
    return res/scale

def statistics(z,a):
    w=rownorm(a);two=(a@a).astype(bool).astype(float);two.setdiag(0);two=two-two.multiply(a);two.eliminate_zeros();w2=rownorm(two)
    x,y=z.T;lagx=w@x;lagy=w@y;cross=(x*lagy+y*lagx)/2
    degree=np.asarray(a.sum(axis=1)).ravel();interior=degree==6
    return dict(same_spot=float(np.mean(x*y)),lag1=float(cross.mean()),lag2=float(np.mean((x*(w2@y)+y*(w2@x))/2)),lag1_minus_lag2=float(cross.mean()-np.mean((x*(w2@y)+y*(w2@x))/2)),moran_IL1B=float(np.mean(x*lagx)),moran_CLDN4=float(np.mean(y*lagy)),interior_lag1=float(cross[interior].mean()) if interior.any() else np.nan,interior_spots=int(interior.sum())),cross

def read_section(item):
    f={Path(v['path']).name:ROOT/v['path'] for v in item['files']}
    features=pd.read_csv(f['features.tsv.gz'],sep='\t',header=None);genes=features[1].astype(str).tolist()
    barcodes=pd.read_csv(f['barcodes.tsv.gz'],sep='\t',header=None)[0].astype(str)
    assert barcodes.is_unique and len(genes)==len(set(genes))
    assert all(genes.count(g)==1 for g in GENES)
    with threadpool_limits(limits=2),gzip.open(f['matrix.mtx.gz'],'rb') as stream:m=mmread(stream)
    assert m.shape==(len(genes),len(barcodes)) and np.all(np.isfinite(m.data)) and np.all(m.data>0) and np.all(m.data==np.floor(m.data))
    nnz=m.nnz;m=m.T.tocsr();assert m.nnz==nnz
    total=np.asarray(m.sum(axis=1)).ravel();detected=np.diff(m.indptr)
    mt=np.asarray(m[:,[i for i,g in enumerate(genes) if g.upper().startswith('MT-')]].sum(axis=1)).ravel()/np.maximum(total,1)*100
    positions=pd.read_csv(f['tissue_positions.csv']);old=pd.read_csv(f['tissue_positions_list.csv'],header=None,names=positions.columns)
    assert positions.barcode.is_unique and old.barcode.is_unique
    positions=positions.set_index('barcode');old=old.set_index('barcode')
    assert set(positions.index)==set(old.index) and np.array_equal(positions.sort_index().to_numpy(),old.sort_index().to_numpy())
    a=positions.loc[barcodes].copy();a['total_counts']=total;a['detected_genes']=detected;a['pct_counts_mt']=mt
    qc=a.in_tissue.eq(1)&(total>=500)&(detected>=200)&(mt<=15);a['qc_pass']=qc
    prior=pd.read_csv(f['spot_qc_and_coordinates.csv.gz']).set_index('barcode').loc[barcodes]
    for col in a.columns:
        assert np.allclose(a[col],prior[col],rtol=0,atol=1e-9),col
    selected=m[:,[genes.index(g) for g in GENES]].toarray();values=np.log1p(selected*10000/np.maximum(total,1)[:,None]);a[GENES]=values
    a=a.loc[qc].copy();display=pd.read_csv(f['spatial_display_values.csv.gz']).set_index('barcode').loc[a.index]
    assert len(display)==len(a)
    error=max(float(np.max(np.abs(a[g].to_numpy()-display['GENE_'+g].to_numpy()))) for g in GENES)
    assert error<1e-10
    q=dict(gsm=item['gsm'],patient=int(item['patient']),histology=item['histology'],input_spots=len(barcodes),qc_spots=len(a),genes=len(genes),cached_value_max_error=error,coordinate_versions_equal=True)
    del m,selected;gc.collect()
    return a.reset_index(),q

def aggregate(section):
    metrics=['same_spot','lag1','lag2','lag1_minus_lag2','moran_IL1B','moran_CLDN4','interior_lag1']
    rows=[]
    for (mode,patient,hist),g in section.groupby(['mode','patient','histology']):
        for weighting in ['equal_section','spot_weighted']:
            for metric in metrics:
                valid=g[metric].notna();h=g.loc[valid];weights=np.ones(len(h)) if weighting=='equal_section' else h.retained_spots.to_numpy()
                rows.append(dict(mode=mode,patient=int(patient),histology=hist,weighting=weighting,metric=metric,sections=len(h),value=float(np.average(h[metric],weights=weights)) if len(h) else np.nan))
    patient=pd.DataFrame(rows);pairs=[]
    for (mode,pid,weight,metric),g in patient.groupby(['mode','patient','weighting','metric']):
        h=g.set_index('histology')
        for comparison in ['AAH','AIS','MIA']:
            if {'LUAD',comparison}<=set(h.index):pairs.append(dict(mode=mode,patient=int(pid),weighting=weight,metric=metric,comparison='LUAD-'+comparison,LUAD=h.loc['LUAD','value'],reference=h.loc[comparison,'value'],delta=h.loc['LUAD','value']-h.loc[comparison,'value'],LUAD_sections=int(h.loc['LUAD','sections']),reference_sections=int(h.loc[comparison,'sections'])))
    paired=pd.DataFrame(pairs);summary=[]
    for keys,g in paired.groupby(['mode','weighting','metric','comparison']):
        v=g.delta.dropna().to_numpy();n=len(v)
        summary.append(dict(zip(['mode','weighting','metric','comparison'],keys),n=n,mean=v.mean() if n else np.nan,median=np.median(v) if n else np.nan,min=v.min() if n else np.nan,max=v.max() if n else np.nan,positive=int((v>0).sum()),loo_mean_min=min((v.sum()-v)/(n-1)) if n>1 else np.nan,loo_mean_max=max((v.sum()-v)/(n-1)) if n>1 else np.nan))
    return patient,paired,pd.DataFrame(summary)

def plots(out,items,section,paired):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axes=plt.subplots(1,3,figsize=(11,4),layout='constrained')
    for ax,comparison in zip(axes,['LUAD-AAH','LUAD-AIS','LUAD-MIA']):
        for i,mode in enumerate(MODES):
            z=paired[(paired['mode']==mode)&(paired.weighting=='equal_section')&(paired.metric=='lag1')&(paired.comparison==comparison)]
            ax.scatter(i+np.linspace(-.15,.15,len(z)),z.delta,s=23,color='#0072B2',alpha=.7)
            if len(z):ax.plot([i-.25,i+.25],[z.delta.mean()]*2,color='#D55E00',lw=2)
        ax.set_xticks(range(3),['Centered','Depth','Depth + RNA\ncomposition'],rotation=20);ax.axhline(0,color='.5',lw=.8);ax.set_title(comparison+(' (primary)' if comparison=='LUAD-AAH' else ' (secondary)'));ax.set_ylabel('Paired one-hop cross-product difference')
    fig.suptitle('IL1B–CLDN4 spatial RNA organization\nDots are patients, repeated sections averaged; no spot-based p-values',fontsize=12)
    for ext in ['png','pdf']:fig.savefig(out/f'spatial_paired.{ext}',dpi=300)
    plt.close(fig)
    # All patient maps retained; the first two matched patients are fixed by metadata.
    roster=pd.DataFrame([{k:v for k,v in x.items() if k!='files'} for x in items]);roster.patient=roster.patient.astype(int)
    matched=sorted(p for p,g in roster.groupby('patient') if {'AAH','LUAD'}<=set(g.histology));examples=matched[:2]
    with PdfPages(out/'spatial_all_patients.pdf') as pdf:
        for pid,group in roster.groupby('patient',sort=True):
            group=group.sort_values(['histology','gsm']);fig,axes=plt.subplots(len(group),2,figsize=(8,3*len(group)),squeeze=False,layout='constrained')
            for row,item in enumerate(group.itertuples()):
                a=pd.read_csv(out/'spots'/f'{item.gsm}.csv.gz')
                for col,gene in enumerate(['IL1B','CLDN4']):
                    ax=axes[row,col];v=a[gene];im=ax.scatter(a.array_col/2,-a.array_row*np.sqrt(3)/2,c=v,s=2,cmap='viridis',vmin=0,vmax=3,rasterized=True)
                    ax.set_aspect('equal');ax.set_title(f'{item.gsm} | {item.histology} | {gene}');ax.set_xlabel('Lattice coordinate (not micrometers)');ax.set_ylabel('Lattice coordinate');fig.colorbar(im,ax=ax,label='log1p(count / library × 10,000)',shrink=.7)
            fig.suptitle(f'Patient {pid}: measured QC tissue spots; no pathology or cell identities',fontsize=12)
            pdf.savefig(fig,dpi=120)
            if pid in examples:fig.savefig(out/f'spatial_example_P{pid}.png',dpi=180)
            plt.close(fig)
    # A separate rationale panel: measurements, rival explanations and missing evidence.
    fig,ax=plt.subplots(figsize=(11,6));ax.set(xlim=(0,11),ylim=(0,6));ax.axis('off')
    boxes=[(.3,3.55,3.1,1.65,'A12: measured barcode RNA\nFixed IL1R1 / IL1RAP and context genes\nDetection, positive-cell intensity,\nco-detection; paired patient units','#DCEAF4'),(3.95,3.55,3.1,1.65,'Pg1-P01: measured spatial RNA\nIL1B / CLDN4 in lattice neighbors\nSame-spot and cross-spot quantities\nremain separate','#DCEAF4'),(7.6,3.55,3.1,1.65,'Descriptive question\nWhich parts of aggregate RNA change\nreflect detection or broad spatial\norganization?','#E4EFE9'),(.3,.6,4.95,1.9,'Alternative explanations retained\nRNA depth • transferred-label selection • mixtures\nAmbient RNA • tissue geometry • other inflammatory inputs\nSensitivity checks assess dependence; they do not remove all bias.','#FFF0DA'),(5.75,.6,4.95,1.9,'Biological hypothesis still untested\nDoes recipient configuration alter functional IL-1 response?\nNeeds independent state identity and protein/functional assays.\nRNA co-detection ≠ receptor assembly or signaling.','#F0E9F5')]
    for x,y,w,h,label,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06',facecolor=color,edgecolor='#55616B'));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=10,linespacing=1.5)
    for start,end in [((3.45,4.4),(3.85,4.4)),((7.1,4.4),(7.5,4.4)),((2.8,2.6),(2,3.4)),((8.2,3.4),(8.2,2.6))]:ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=15,color='#66717A',linestyle='--'))
    ax.text(5.5,5.65,'Public-data rationale: observations, alternatives and the next biological discriminator',ha='center',fontsize=13,weight='bold')
    ax.text(5.5,.15,'Same source lineage; exposed exploration. Dashed arrows indicate reasoning, not demonstrated causation.',ha='center',fontsize=9)
    for ext in ['png','pdf']:fig.savefig(out/f'public_data_rationale.{ext}',dpi=300,bbox_inches='tight')
    plt.close(fig)

def main(out):
    items=json.loads((PAPER/'sources/public_spatial_manifest_v1.json').read_text())['sections'];(out/'spots').mkdir()
    quality=[];components=[];rows=[];verifications=[]
    from verify_public_spatial_v1 import verify_section,verify_aggregation
    for number,item in enumerate(items,1):
        frame,q=read_section(item);a=adjacency(frame.array_row,frame.array_col);assert (a-a.T).nnz==0 and not a.diagonal().any()
        nc,labels=connected_components(a,directed=False);sizes=np.bincount(labels);keep=sizes[labels]>=20
        frame['component']=labels;frame['endpoint_included']=keep
        for j,n in enumerate(sizes):components.append(dict(gsm=item['gsm'],component=j,spots=int(n),included=bool(n>=20)))
        q.update(components=int(nc),isolates=int((sizes==1).sum()),retained_spots=int(keep.sum()),retained_fraction=float(keep.mean()),status='estimated' if keep.sum()>=100 else 'insufficient_support')
        ar=a[keep][:,keep];selected=frame.loc[keep].copy();cl=labels[keep]
        if keep.sum()>=100:
            for mode in MODES:
                z=residuals(selected,mode,cl)
                if z is None:
                    q['status']='zero_residual_variance';continue
                stats,local=statistics(z,ar);rows.append(dict(gsm=item['gsm'],patient=int(item['patient']),histology=item['histology'],mode=mode,retained_spots=len(z),**stats))
                frame.loc[keep,mode+'_z_IL1B']=z[:,0];frame.loc[keep,mode+'_z_CLDN4']=z[:,1];frame.loc[keep,mode+'_local_cross']=local
        frame.to_csv(out/'spots'/f"{item['gsm']}.csv.gz",index=False,compression={'method':'gzip','mtime':0})
        vr=verify_section(frame,[r for r in rows if r['gsm']==item['gsm']]);verifications.append(vr);assert not vr['failures'],vr
        quality.append(q);print('qualified and verified spatial section',number,item['gsm'],len(frame),flush=True)
    section=pd.DataFrame(rows);patient,paired,summary=aggregate(section)
    pd.DataFrame(quality).to_csv(out/'source_qualification.csv',index=False);pd.DataFrame(components).to_csv(out/'graph_components.csv',index=False)
    section.to_csv(out/'section_statistics.csv',index=False);patient.to_csv(out/'patient_statistics.csv',index=False);paired.to_csv(out/'paired_deltas.csv',index=False);summary.to_csv(out/'paired_summary.csv',index=False)
    av=verify_aggregation(section,patient,paired);verifications.append(av)
    verification={'checks':sum(x['checks'] for x in verifications),'failures':[f for x in verifications for f in x['failures']],'max_absolute_error':max(x['max_absolute_error'] for x in verifications),'method':'Independent coordinate-neighbor lists and scalar edge arithmetic for every section/mode; patient aggregation and paired contrasts','biological_replication':False}
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n');assert not verification['failures']
    plots(out,items,section,paired)
    (out/'summary.json').write_text(json.dumps({'sections':len(items),'patients':len(set(x['patient'] for x in items)),'QC_spots':sum(x['qc_spots'] for x in quality),'retained_spots':sum(x['retained_spots'] for x in quality),'verification_checks':verification['checks'],'endpoint':'IL1B-CLDN4 symmetric lattice-neighbor cross-product, not contact or signaling','physical_scale':'unqualified; lattice hops only'},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();main(args.output)
