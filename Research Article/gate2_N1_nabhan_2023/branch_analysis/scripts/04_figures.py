"""Presentation of completed, prespecified tables; no new model or selection rule."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import *

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
figdir=OUT/'figures'
colors=['#21618c','#b54734','#39734c','#775790','#b47d24']
def save(fig,name):
    fig.savefig(figdir/(name+'.png'),dpi=170,bbox_inches='tight')
    fig.savefig(figdir/(name+'.svg'),bbox_inches='tight');plt.close(fig)

e=load('bulk_program_effects.tsv')
panels=['Wnt_clean','YAP_source','AT2_identity','AT1_associated','transition_associated','ER_stress','Gaona_YT_disjoint']
labels=['Wnt (3 genes)','Source YAP-associated','AT2 identity','AT1-associated','Transition-associated','ER stress','Sustained-YT similarity*']
fig,axes=plt.subplots(1,3,figsize=(13,5.2),sharey=True,layout='constrained')
for ax,contrast in zip(axes,['Fzd5_vs_CHIR','Fzd6_vs_CHIR','withdraw24_vs_withdraw48']):
    q=e[(e.study=='Nb2')&(e.contrast==contrast)].set_index('panel').loc[panels]
    y=np.arange(len(q));ax.hlines(y,q.CI_low,q.CI_high,color='#9da4ad',lw=1.5,label='Conditional 95% CI')
    ax.hlines(y,q.single_drop_min,q.single_drop_max,color=colors[0],lw=5,label='Single-library omission range')
    ax.scatter(q.delta,y,s=28,c='black',zorder=4);ax.axvline(0,c='#777777',ls=':',lw=1)
    ax.set_title(contrast.replace('_vs_',' minus '));ax.set_xlabel('Difference in program score');ax.set_yticks(y,labels)
axes[0].invert_yaxis();fig.legend(*axes[0].get_legend_handles_labels(),loc='outside lower center',fontsize=9,ncol=2)
fig.suptitle('Nb2: stable source-panel shifts do not establish a broad sustained-YAP response',fontsize=13)
save(fig,'01_bulk_influence')

fig,axes=plt.subplots(1,2,figsize=(10,4.8),sharey=True,layout='constrained')
for ax,contrast in zip(axes,['YT_vs_WT_SFFFM','YT_vs_WT_ADM']):
    q=e[(e.study=='Gaona')&(e.contrast==contrast)].set_index('panel').loc[panels]
    y=np.arange(len(q));ax.hlines(y,q.CI_low,q.CI_high,color='#8c939b');ax.scatter(q.delta,y,c=colors[1])
    ax.axvline(0,c='#888',ls=':');ax.set_yticks(y,labels);ax.set_title(contrast.replace('YT_vs_WT_','YT-active minus WT: '));ax.set_xlabel('Within-medium score difference')
axes[0].invert_yaxis();fig.suptitle('Gaona reference: responses depend on culture context\n*Signature was selected in SFFFM; ADM is internal context sensitivity',fontsize=12)
save(fig,'02_reference_context')

r=load('mouse_unit_expression.tsv.gz');p=load('mouse_program_scores.tsv')
r=r[(r['mode']=='doublets_removed')&(r.cells>=50)&(r.day==42)]
p=p[(p['mode']=='doublets_removed')&(p.cells>=50)&(p.day==42)]
def dots(ax,data,feature,states,program=False):
    col='panel' if program else 'gene';val='score' if program else 'cpm'
    for j,state in enumerate(states):
        q=data[(data.state==state)&(data[col]==feature)].sort_values('unit');ys=q[val].to_numpy()
        offsets=np.linspace(-.15,.15,len(ys)) if len(ys)>1 else [0]
        if len(ys):
            ax.scatter(j+np.array(offsets),ys,color=colors[j%len(colors)],s=22,alpha=.85)
            ax.hlines(np.median(ys),j-.24,j+.24,color='black',lw=2)
        ax.text(j,.99,'n='+str(len(ys)),transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8)
    short={'Arterial_endothelium':'Arterial','Venous_endothelium':'Venous','Lymphatic_endothelium':'Lymphatic'}
    ax.set_xticks(range(len(states)),[short.get(s,s.replace('_','\n')) for s in states]);ax.set_title(feature.replace('_',' '));ax.set_ylabel('Mean log2(CPM+1)' if program else 'Pseudobulk CPM')
    lo,hi=ax.get_ylim();ax.set_ylim(lo,hi+.16*(hi-lo))

states=['AT2','Alveolar_transitional','AT1_AT2','AT1']
fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
dots(axes[0],r,'Fzd5',states);dots(axes[1],r,'Fzd6',states);dots(axes[2],p,'Gaona_YT_disjoint',states,True)
axes[2].set_ylabel('Signed mean log2(CPM+1)')
fig.suptitle('Day-42 epithelial context: each dot is a source sample with at least 50 cells',fontsize=12)
save(fig,'03_epithelial_context')

states=['AF1','AF2','Adventitial_fibroblast','Peribronchial_fibroblast']
fig,axes=plt.subplots(2,3,figsize=(13,7),layout='constrained')
for ax,g in zip(axes[0],['Fzd1','Fzd2','Fzd7']): dots(ax,r,g,states)
for ax,g in zip(axes[1,:2],['support_ligands','ECM']): dots(ax,p,g,states,True)
axes[1,2].axis('off');axes[1,2].text(0,.8,'Separate endpoints:\nSupport-ligand RNA is not measured repair.\nECM RNA is not collagen deposition.\nReceptor abundance is not receptor necessity.\n\nSubtype and source day remain fixed.',va='top',linespacing=1.8)
fig.suptitle('Day-42 fibroblasts: compare Fzd1 with Fzd2/7 within subtype',fontsize=12)
save(fig,'04_fibroblast_context')

states=['CAP1','CAP2','Arterial_endothelium','Venous_endothelium','Lymphatic_endothelium']
fig,axes=plt.subplots(1,3,figsize=(14,4.8),layout='constrained')
dots(axes[0],r,'Fzd4',states)
for ax,prog in zip(axes[1:],['endothelial_junction','cycling']):
    for j,state in enumerate(['CAP1','CAP2']):
        a=r[(r.gene=='Fzd4')&(r.state==state)][['unit','cpm']]
        b=p[(p.panel==prog)&(p.state==state)][['unit','score']]
        q=a.merge(b,on='unit',validate='one_to_one').merge(load('mouse_sample_context.tsv')[['unit','round']],on='unit',validate='one_to_one')
        for k,(rnd,qq) in enumerate(q.groupby('round')):
            ax.scatter(qq.cpm,qq.score,color=colors[j],marker=['o','^'][k],label=state+' round'+str(k+1),s=35)
    ax.set_xlabel('Fzd4 pseudobulk CPM');ax.set_ylabel(prog.replace('_',' ')+' score');ax.legend(fontsize=8)
fig.suptitle('Day-42 endothelium: broad Fzd4 expression; cycling association varies by round\nCAP1 within-round Spearman: -0.40 and +1.00 (4 samples each); descriptive only',fontsize=12)
save(fig,'05_endothelial_context')
print('Five PNG/SVG figure pairs rendered from saved tables')
