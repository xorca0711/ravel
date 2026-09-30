"""Publication-style descriptive figures; no significance or causal mediation."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
BASE=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.labelsize':10,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,'savefig.facecolor':'white'})
manifest=[]
def load(name):return pd.read_csv(BASE/'tables'/name,sep='\t')
def save(fig,name):
 for ext in ['png','pdf','svg']:
  path=BASE/'figures'/f'{name}.{ext}';fig.savefig(path,dpi=300,bbox_inches='tight');manifest.append(dict(file=path.relative_to(BASE).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 plt.close(fig)
def label(ax,letter):ax.text(-.17,1.10,letter,transform=ax.transAxes,fontweight='bold',fontsize=14,va='top')
def main():
 obs=load('source_observations.tsv');mapping=json.loads((BASE/'config/source_mapping.json').read_text())['panels'];spec={s['panel']:s for s in mapping}
 fig,axes=plt.subplots(2,3,figsize=(12.6,8));fig.subplots_adjust(wspace=.43,hspace=.72,top=.86,bottom=.14)
 titles={'3F':'Foxf1 loss: perfused area','7E':'Fzd4 rescue: receptor expression','7F':'Fzd4 rescue: nuclear beta-catenin','7G':'Fzd4 rescue: basement membrane','7D':'Fzd4 rescue: tumor size'}
 ylabels={'3F':'Lectin+ area / CD31+ area (%)','7E':'Fzd4+ gCap endothelial cells (%)','7F':'Nuclear beta-catenin+ ECs (%)','7G':'Collagen IV+ / CD31+ area (%)','7D':'Tumor size (mm$^3$)'}
 for letter,ax,panel in zip('ABCDE',axes.flat,['3F','7E','7F','7G','7D']):
  s=spec[panel];labels=[]
  for i,(col,name) in enumerate(s['columns'].items()):
   values=obs[obs.panel.eq(panel)&obs.source_column.eq(col)].value.to_numpy();xx=np.linspace(-.11,.11,len(values))+i
   control=name in ['Control','Control-nano-empty','Control tumor empty','Tumor EC'];normal=name=='Lung EC';rescue='nano-fzd4' in name
   color='#6C757D' if control else '#228B70' if normal else '#2166AC' if rescue else '#C26B32'
   ax.scatter(xx,values,s=28,color=color,edgecolor='white',linewidth=.4,zorder=3);ax.plot([i-.23,i+.23],[values.mean()]*2,c='black',lw=1.6,zorder=4)
   labelname='Control' if control else 'Normal\nlung' if normal else 'Het\nFzd4' if rescue else 'Het\nempty' if panel!='3F' else 'Het'
   labels.append(labelname+'\n'+f'n={len(values)}')
  ax.set_xticks(range(len(labels)),labels,fontsize=9);ax.set_ylabel(ylabels[panel]);ax.set_title(titles[panel],loc='left',pad=14);ax.set_ylim(bottom=0);ax.margins(x=.18,y=.15);ax.grid(axis='y',alpha=.16);label(ax,letter)
 axes[1,2].axis('off');axes[1,2].text(0,1,'Interpretation boundary',fontweight='bold',va='top',fontsize=11)
 axes[1,2].text(0,.86,'Het: endothelial Foxf1 heterozygote.\nA: Foxf1-loss perfusion comparator.\nB-E: Fzd4 restoration in tumor vessels.\n\nFzd4-rescue perfusion and normal\ncapillary lineage output were not\nmeasured in these source panels.\n\nDots: source-reported animal values.\nBlack marks: group means.\nAnonymous rows are not joined\nacross outcomes.',va='top',fontsize=10,linespacing=1.45)
 fig.suptitle('FZD4 restoration supports endothelial signaling and vascular structure',fontsize=15,fontweight='bold',x=.51,y=.98)
 fig.text(.5,.925,'Bian et al., EMBO Molecular Medicine (2024) | descriptive source-data reanalysis in a lung tumor model',ha='center',fontsize=10)
 fig.text(.08,.028,'Independent groups within panels; source legends define biological replication. No new P values or inferred mediation.',fontsize=9)
 save(fig,'A21E_F1_vascular_source_evidence')
 sm=load('contrast_summary.tsv');s=sm[sm.cell_floor.eq(20)&sm.contrast.eq('transitional1_minus_gCap0')];genes=[f'Fzd{i}' for i in range(1,11)];days=[0,3,5,7]
 arr=s.pivot(index='gene',columns='day',values='mean').reindex(index=genes,columns=days).to_numpy();det=s.pivot(index='gene',columns='day',values='detected_left').reindex(index=genes,columns=days).to_numpy()
 fig,axes=plt.subplots(1,2,figsize=(11.7,7.8));fig.subplots_adjust(left=.09,right=.94,wspace=.42,top=.82,bottom=.19)
 limit=max(1,float(np.abs(arr).max()));im=axes[0].imshow(arr,cmap='RdBu_r',norm=TwoSlopeNorm(vcenter=0,vmin=-limit,vmax=limit),aspect='auto')
 im2=axes[1].imshow(np.log10(det+1),cmap='Blues',aspect='auto',vmin=0)
 for ax in axes:
  ax.set_xticks(range(4),['Control\nn=3','Day 3\nn=3','Day 5\nn=2','Day 7\nn=3']);ax.set_yticks(range(10),genes);ax.tick_params(length=0)
 for i,g in enumerate(genes):
  for j,day in enumerate(days):
   rec=s[s.gene.eq(g)&s.day.eq(day)].iloc[0];value=arr[i,j]
   axes[0].text(j,i,f'{value:+.2f}\n{int(rec.positive)}/{int(rec.n)} positive',ha='center',va='center',fontsize=8,color='white' if abs(value)>limit*.65 else 'black')
   axes[1].text(j,i,str(int(det[i,j])),ha='center',va='center',fontsize=10,color='white' if np.log10(det[i,j]+1)>np.log10(det.max()+1)*.65 else 'black')
 axes[0].set_title('A  Paired expression difference',loc='left',pad=12);axes[1].set_title('B  Transitional cells detecting each gene',loc='left',pad=12)
 fig.colorbar(im,ax=axes[0],shrink=.7,pad=.04,label='Mean difference in log2(CPM + 1)')
 cb=fig.colorbar(im2,ax=axes[1],shrink=.7,pad=.04);cb.set_label('log10(detected cells + 1)')
 fig.suptitle('No alternative Fzd meets the frozen enrichment criteria',fontsize=15,fontweight='bold',y=.98)
 fig.text(.5,.924,'Author transitional state 1 minus major gCap state 0 | GSE211335 | 20 cells per state and animal',ha='center',fontsize=10)
 fig.text(.09,.048,'A: animal-paired means and positive-pair counts. B: detected cells summed over the same eligible animals.\nZero detection is a sampled RNA result. Enrichment criteria nominate mechanisms; they do not test receptor dependence.',fontsize=9,linespacing=1.6)
 save(fig,'A21E_F2_fzd_family_states')
 pairs=load('paired_differences.tsv');pairs=pairs[pairs.cell_floor.eq(20)&pairs.contrast.eq('transitional1_minus_gCap0')]
 fig,axes=plt.subplots(2,3,figsize=(11.8,7.6));fig.subplots_adjust(left=.09,right=.98,wspace=.4,hspace=.57,top=.83,bottom=.20)
 colors=['#666666','#3E79AD','#BD723D','#3A8D76']
 for letter,ax,gene in zip('ABCDEF',axes.flat,['Foxf1','Fzd4','Lrp6','Axin2','Nkd1','Tspan12']):
  for i,day in enumerate(days):
   v=pairs[pairs.gene.eq(gene)&pairs.day.eq(day)].sort_values('animal').delta.to_numpy();ax.scatter(i+np.linspace(-.12,.12,len(v)),v,s=31,c=colors[i],edgecolor='white',linewidth=.4,zorder=3);ax.plot([i-.24,i+.24],[v.mean()]*2,c='black',lw=1.6)
  ax.axhline(0,c='#777777',lw=.8,ls='--');ax.set_xticks(range(4),['Ctrl\nn=3','D3\nn=3','D5\nn=2','D7\nn=3']);ax.set_ylabel('Paired difference\nlog2(CPM + 1)');ax.set_title(gene,loc='left',fontstyle='italic',pad=12);ax.set_xlim(-.5,3.5);ax.grid(axis='y',alpha=.15);label(ax,letter)
 fig.suptitle('Foxf1, Fzd4 and Lrp6 are lower in transitional gCap states',fontsize=15,fontweight='bold',y=.98)
 fig.text(.5,.922,'Within-animal state contrasts; conditions contain different animals | canonical-response RNA remains descriptive',ha='center',fontsize=10)
 fig.text(.09,.050,'Dots: individual animals; black marks: means. Genes were predefined; panels shown are an exploratory selection.\nSparse Axin2 detection and state labels do not establish pathway activity, a temporal transition or a functional requirement.',fontsize=9,linespacing=1.6)
 save(fig,'A21E_F3_receptor_context')
 (BASE/'reports/figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'figures':3,'exports':len(manifest)}))
if __name__=='__main__':main()
