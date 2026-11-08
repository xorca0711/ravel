"""Fixed Osmr extraction from immutable source output; no population inference."""
import argparse
import csv
import gzip
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'analysis/research/runs/sx22_program_description_v1'
LIBS = ['PBS_1','PBS_2','LH5_1','LH5_2','LH30_1','LH30_2']
GROUP = ['PBS','PBS','WT','WT','B3','B3']
ID = 'ENSMUSG00000022146'

def read(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def write(path, rows):
    with open(path,'x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n'); w.writeheader(); w.writerows(rows)

def main(out):
    inv=[r for r in read(OLD/'gene_inventory.csv') if r['Gene_name']=='Osmr']
    assert len(inv)==1 and inv[0]['geneID']==ID and inv[0]['primary_eligible']=='True'
    primary=[r for r in read(OLD/'primary_gene_expression.csv') if r['geneID']==ID][0]
    counts=[r for r in read(OLD/'counts_for_tmm.csv') if r['geneID']==ID][0]
    factors=read(OLD/'normalization_factors.csv')
    with gzip.open(ROOT/'raw_data/Sx22/GSE160217_060120_22_fpkm_genename.xls.gz','rt',encoding='utf-8') as f:
        target=[r for r in csv.DictReader(f,delimiter='\t') if r['geneID']==ID]
    assert len(target)==1 and target[0]['Gene_name']=='Osmr'
    vals=[]; contrasts=[]
    for scale in ['CPM','TMM','FPKM']:
        for view in ['full']+['omit_'+l for l in LIBS]:
            keep=[l for l in LIBS if view!='omit_'+l]
            expr={}
            for lib in keep:
                if scale=='CPM': value=float(primary[lib+'_CPM'])
                elif scale=='FPKM': value=float(target[0][lib])
                else:
                    f=[r for r in factors if r['view']==view and r['library']==lib]; assert len(f)==1
                    value=float(counts[lib])*1e6/float(f[0]['effective_library_size'])
                assert np.isfinite(value) and value>=0
                expr[lib]=float(np.log2(value+1))
                vals.append(dict(geneID=ID,symbol='Osmr',scale=scale,view=view,library=lib,group=GROUP[LIBS.index(lib)],abundance=value,log2_plus_1=expr[lib]))
            means={g:float(np.mean([expr[l] for l in keep if GROUP[LIBS.index(l)]==g])) for g in ['PBS','WT','B3']}
            for a,b in [('WT','PBS'),('B3','PBS'),('B3','WT')]:
                contrasts.append(dict(scale=scale,view=view,contrast=a+'-'+b,value=means[a]-means[b]))
    ranges=[]
    for scale in ['CPM','TMM','FPKM']:
        for con in ['WT-PBS','B3-PBS','B3-WT']:
            rows=[r for r in contrasts if r['scale']==scale and r['contrast']==con]
            ranges.append(dict(scale=scale,contrast=con,full=next(r['value'] for r in rows if r['view']=='full'),omission_min=min(r['value'] for r in rows if r['view']!='full'),omission_max=max(r['value'] for r in rows if r['view']!='full')))
    write(out/'mapping.csv',inv); write(out/'library_values.csv',vals); write(out/'contrasts.csv',contrasts); write(out/'ranges.csv',ranges)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained',gridspec_kw={'width_ratios':[1,1.5]})
    colors=['#777777','#0072B2','#D55E00']
    for i,g in enumerate(['PBS','WT','B3']):
        rows=[r for r in vals if r['scale']=='CPM' and r['view']=='full' and r['group']==g]
        for j,r in enumerate(rows):
            axs[0].scatter(i+(-.08 if j==0 else .08),r['log2_plus_1'],color=colors[i],marker=['o','^'][j],s=55)
        axs[0].plot([i-.2,i+.2],[np.mean([r['log2_plus_1'] for r in rows])]*2,color=colors[i])
    axs[0].set(xticks=range(3),xticklabels=['PBS','WT','22-B3'],ylabel='Osmr log2(CPM + 1)',title='A  All six deposited libraries')
    for s,scale in enumerate(['CPM','TMM','FPKM']):
        for i,con in enumerate(['WT-PBS','B3-PBS','B3-WT']):
            r=next(r for r in ranges if r['scale']==scale and r['contrast']==con); y=i+(s-1)*.22
            axs[1].plot([r['omission_min'],r['omission_max']],[y,y],color=colors[s],lw=2)
            axs[1].scatter(r['full'],y,color=colors[s],marker=['o','s','^'][s],label=scale if i==0 else None,zorder=3)
    axs[1].axvline(0,color='#aaaaaa',lw=.8); axs[1].invert_yaxis()
    axs[1].set(yticks=range(3),yticklabels=['WT − PBS','B3 − PBS','B3 − WT'],xlabel='Difference of mean log2(expression + 1)',title='B  Full values and single-library omission ranges')
    axs[1].legend(loc='best',frameon=False)
    fig.suptitle('Acute whole-colon Osmr RNA • six hours • library description')
    fig.savefig(out/'osmr.png',dpi=300); fig.savefig(out/'osmr.pdf'); plt.close(fig)
    (out/'summary.json').write_text(json.dumps({'target':ID,'eligible':True,'primary':ranges[:3],'limits':'No animal-level inference, epithelial localization, OSM responsiveness, protection or chronic-risk measurement.'},indent=2)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
