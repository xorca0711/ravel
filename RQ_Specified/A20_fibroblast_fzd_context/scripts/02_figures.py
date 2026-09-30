"""Render A20 observed-sample figures; no simulated outcomes or cell-level inference."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
BASE=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
pairs=pd.read_csv(BASE/'tables/paired_differences.tsv',sep='\t');primary=pairs[pairs['mode'].eq('doublets_removed')&pairs.cell_floor.eq(50)]
units=sorted(primary.unit.unique());colors=dict(zip(units,plt.get_cmap('tab10').colors));records=[]
def save(fig,name):
 for ext in ['png','pdf','svg']:
  p=BASE/'figures'/f'{name}.{ext}';fig.savefig(p,bbox_inches='tight',facecolor='white');records.append(dict(file=str(p.relative_to(BASE)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 plt.close(fig)
def paired(ax,gene,label):
 z=primary[primary.feature.eq(gene)].set_index('unit')
 for unit,r in z.iterrows():ax.plot([0,1],[r.value_AF1,r.value_AF2],'-o',color=colors[unit],lw=1,ms=4,alpha=.9)
 ax.set_xticks([0,1],['AF1','AF2']);ax.set_xlim(-.25,1.25);ax.set_ylabel('log2(CPM + 1)');ax.set_title(label,loc='left',fontweight='bold');ax.grid(axis='y',alpha=.15)
fig,axs=plt.subplots(2,3,figsize=(10,6.5));fig.subplots_adjust(hspace=.55,wspace=.45,bottom=.21,top=.88)
for ax,gene,letter in zip(axs.flat,['Pdgfra','Pdgfrb','Col13a1','Col14a1','Fzd1','Fzd2'],'ABCDEF'):paired(ax,gene,letter+'  '+gene)
fig.suptitle('A20 | Independent identity probes and receptor context',fontweight='bold',y=.98)
handles=[Line2D([0],[0],color=colors[u],marker='o',lw=1,label=u+' | '+str(primary[primary.unit.eq(u)]['round'].iloc[0])) for u in units]
fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.04),ncol=3,frameon=False,fontsize=8)
fig.text(.5,.005,'GSE262927, day 42; 5 paired source samples; doublets removed; >=50 cells/subtype. Lines join the same sample.',ha='center',fontsize=8)
save(fig,'A20_F1_identity_receptors')
fig,axs=plt.subplots(1,2,figsize=(11.2,6.6),gridspec_kw={'width_ratios':[1,1.35]});fig.subplots_adjust(wspace=.6,bottom=.18,top=.84)
for ax,genes,title in [(axs[0],['Wnt2','Fgf7','Fgf10','Hgf','Vegfa'],'A  Candidate support-ligand RNA'),(axs[1],['Col1a1','Col1a2','Col3a1','Col5a1','Col5a2','Col6a1','Col6a2','Col6a3','Cthrc1','Lrrc15'],'B  Matrix-associated RNA')]:
 for i,g in enumerate(genes):
  z=primary[primary.feature.eq(g)].set_index('unit');v=z.delta
  ax.plot([v.min(),v.max()],[i,i],color='#bac0c6',lw=1.5,zorder=1)
  for j,u in enumerate(units):ax.scatter(z.loc[u,'delta'],i+(j-2)*.09,color=colors[u],s=22,zorder=3)
  ax.scatter(v.median(),i,marker='|',s=150,color='black',zorder=4)
 ax.axvline(0,color='#555555',lw=.9,ls='--');ax.set_yticks(range(len(genes)),genes);ax.invert_yaxis();ax.set_xlabel('AF1 - AF2: difference in log2(CPM + 1)');ax.set_title(title,loc='left',fontweight='bold');ax.grid(axis='x',alpha=.12)
fig.suptitle('A20 | Gene-level patterns separate niche RNA from matrix RNA',fontweight='bold',y=.96)
fig.text(.5,.07,'Each colored point is one paired source sample (n=5). Black tick: median; grey line: observed range, not a confidence interval.',ha='center',fontsize=8)
fig.text(.5,.025,'Same day-42 samples as F1. RNA abundance does not measure secretion, deposited matrix, or mature epithelial output.',ha='center',fontsize=8)
save(fig,'A20_F2_support_matrix')
fig,axs=plt.subplots(1,3,figsize=(11.5,4.9));fig.subplots_adjust(wspace=.55,bottom=.23,top=.78)
conditions=[('doublets_removed',20),('doublets_removed',50),('doublets_removed',100),('author_labels',20),('author_labels',50),('author_labels',100)]
for ax,panel,title in zip(axs,['support_existing','ECM_existing','collagen_source'],['A  Support panel (4 genes)','B  Earlier ECM panel (4 genes)','C  Collagen panel (8 genes)']):
 for i,(mode,floor) in enumerate(conditions):
  z=pairs[pairs['mode'].eq(mode)&pairs.cell_floor.eq(floor)&pairs.feature.eq(panel)].delta
  if len(z):
   ax.plot([z.min(),z.max()],[i,i],color='#687c90',lw=2);ax.plot(z.median(),i,'o',color='#233e55',ms=5);ax.annotate('n='+str(len(z)),(z.max(),i),xytext=(5,0),textcoords='offset points',va='center',fontsize=8)
  else:ax.text(.02,i,'No eligible pairs',transform=ax.get_yaxis_transform(),va='center',fontsize=8,color='#7a4a28')
 ax.axvline(0,color='#666666',lw=.8,ls='--');ax.set_yticks(range(6),[('Remove' if m=='doublets_removed' else 'Retain')+f' | {f}' for m,f in conditions],fontsize=8);ax.invert_yaxis();ax.set_ylim(5.6,-.6);ax.set_title(title,loc='left',fontweight='bold');ax.set_xlabel('AF1 - AF2: mean gene log2(CPM + 1)');ax.margins(x=.4)
axs[0].set_ylabel('Predicted doublets | cell floor')
fig.suptitle('A20 | Fixed eligibility and gene-panel sensitivity',fontweight='bold',y=.95)
fig.text(.5,.09,'Points: paired medians. Lines: observed sample ranges. Panels have distinct gene sets and cannot be compared as quantities of function.',ha='center',fontsize=8)
fig.text(.5,.04,'Day 42 only. A higher cell floor changes which samples qualify; it does not add biological replication.',ha='center',fontsize=8)
save(fig,'A20_S1_coverage_sensitivity')
(BASE/'reports/figure_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'{len(records)} figure exports written.')
