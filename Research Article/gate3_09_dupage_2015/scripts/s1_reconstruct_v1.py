"""Adapted descriptive reconstruction of qualified DuPage FPKM; no inference."""
import argparse,csv,gzip,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

S0=Path('analysis/research/runs/dupage_s0_qualification_v1')
GROUPS=['HET_hi','HET_lo','KO_hi','KO_lo']
COLORS=['#0072B2','#56B4E9','#D55E00','#E69F00']

def read(path):
    with path.open(newline='') as f: return list(csv.DictReader(f,delimiter='\t'))

def write(path,rows):
    with path.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)

def pca(x):
    centered=x-x.mean(axis=0)
    u,s,_=np.linalg.svd(centered,full_matrices=False)
    return u[:,:2]*s[:2],s*s/(s*s).sum()

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);out=a.parse_args().output
    manifest=[m for m in read(S0/'sample_manifest.tsv') if m['retained']=='True']
    gsms=[m['gsm'] for m in manifest]; group=[m['genotype']+'_'+m['state'] for m in manifest]
    source=read(S0/'common_fpkm.tsv')
    good=[r for r in source if all(r[g+'_status']=='OK' for g in gsms)]
    raw=np.array([[float(r[g+'_FPKM']) for g in gsms] for r in good])
    keep=(raw>=1).any(axis=1); selected=[r for r,k in zip(good,keep) if k];raw=raw[keep]
    log=np.log2(raw+1)
    means=np.array([log[:,np.array(group)==g].mean(axis=1) for g in GROUPS]).T
    contrasts=np.column_stack([means[:,1]-means[:,0],means[:,3]-means[:,2],means[:,2]-means[:,0],means[:,3]-means[:,1]])
    names=['activation_HET','activation_KO','delta_high','delta_low']
    results=[]
    for i,r in enumerate(selected):
        row={k:r[k] for k in ['gene_id','gene_short_name','locus']}
        row.update({g+'_mean_log2_fpkm1':float(means[i,j]) for j,g in enumerate(GROUPS)})
        row.update({g:float(contrasts[i,j]) for j,g in enumerate(names)});results.append(row)
    pcs,var=pca(log.T)
    sample_qc=[]
    for j,m in enumerate(manifest):
        sample_qc.append({'gsm':m['gsm'],'group':group[j],'source_replicate_label':m['source_replicate_label'],
                          'median_log2_fpkm1':float(np.median(log[:,j])), 'zero_fraction_eligible':float(np.mean(raw[:,j]==0)),
                          'PC1':float(pcs[j,0]),'PC2':float(pcs[j,1])})
    with gzip.open('raw_data/dupage_20261107/GSE58998_FPKM_all_samples_merged.txt.gz','rt') as f:
        merged=list(csv.DictReader(f,delimiter='\t'))
    mg=['Het_hi','Het_lo','KO_hi','KO_lo']
    eligible_merged=[r for r in merged if all(r[g+'_status']=='OK' for g in mg)
                     and all(np.isfinite(float(r[g+'_FPKM'])) and float(r[g+'_FPKM'])>=0 for g in mg)
                     and any(float(r[g+'_FPKM'])>=1 for g in mg)]
    mx=np.log2(np.array([[float(r[g+'_FPKM']) for g in mg] for r in eligible_merged])+1)
    mp,mv=pca(mx.T)
    merged_pca=[{'group':g,'PC1':float(mp[i,0]),'PC2':float(mp[i,1])} for i,g in enumerate(GROUPS)]
    stats={'eligible_loci':len(selected),'status_ok_loci':len(good),'retained_libraries':len(manifest),
           'transform':'log2(FPKM+1); means of transformed retained libraries; genes centered, not scaled for PCA',
           'pca_explained_variance':var.tolist(),'merged_eligible_loci':len(mx),'merged_pca_explained_variance':mv.tolist(),
           'contrast_summary':{n:{'rms':float(np.sqrt(np.mean(contrasts[:,j]**2))),
                                  'median_absolute':float(np.median(abs(contrasts[:,j])))} for j,n in enumerate(names)},
           'scope':'No p-values, confidence intervals, DEG calls or exact published PCA claim.'}
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axs=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    for i,g in enumerate(GROUPS):
        ix=np.array(group)==g;axs[0,0].scatter(pcs[ix,0],pcs[ix,1],color=COLORS[i],label=g,s=55)
        axs[0,1].scatter(mp[i,0],mp[i,1],color=COLORS[i],s=65)
        axs[0,1].annotate(g,mp[i],xytext=(4,5),textcoords='offset points')
    for j,m in enumerate(manifest): axs[0,0].annotate(m['source_replicate_label'],pcs[j],xytext=(3,4),textcoords='offset points',fontsize=8)
    axs[0,0].legend(fontsize=8)
    for ax,v,title in [(axs[0,0],var,'Retained libraries (2/3/3/3)'),(axs[0,1],mv,'Deposited merged estimates (four groups)')]:
        ax.set(xlabel=f'PC1 ({v[0]:.1%})',ylabel=f'PC2 ({v[1]:.1%})',title=title);ax.margins(.2)
    axs[1,0].hexbin(contrasts[:,2],contrasts[:,3],gridsize=65,mincnt=1,cmap='viridis',bins='log')
    axs[1,0].set(xlabel='KO − HET, CD62L-high',ylabel='KO − HET, CD62L-low',title='State-specific genotype contrasts')
    axs[1,1].hexbin(contrasts[:,0],contrasts[:,1],gridsize=65,mincnt=1,cmap='viridis',bins='log')
    axs[1,1].set(xlabel='Low − high, HET',ylabel='Low − high, KO',title='Activation-associated contrasts')
    for ax in axs[1]:
        lim=max(abs(np.array(ax.get_xlim()+ax.get_ylim())));ax.plot([-lim,lim],[-lim,lim],color='gray',lw=.7)
        ax.axhline(0,color='gray',lw=.5);ax.axvline(0,color='gray',lw=.5)
    fig.suptitle('Dp1-S1 · Adapted descriptive reconstruction\nLog₂(FPKM + 1); selected Foxp3-positive Tregs; HET is not WT',fontsize=13)
    fig.savefig(out/'reconstruction.png',dpi=180);fig.savefig(out/'reconstruction.pdf');plt.close(fig)
    write(out/'gene_contrasts.tsv',results);write(out/'sample_qc_pca.tsv',sample_qc);write(out/'merged_pca.tsv',merged_pca)
    (out/'summary.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf8')
    print(json.dumps(stats))

if __name__=='__main__':main()
