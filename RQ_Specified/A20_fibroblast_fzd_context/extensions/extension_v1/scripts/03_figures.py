"""Scientific figures from frozen donor-level extension estimates."""
from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
BASE=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'savefig.dpi':300})
s=pd.read_csv(BASE/'tables/contrast_summary.tsv',sep='\t');s=s[s.normalization.eq('TMM')]
d=pd.read_csv(BASE/'tables/donor_contrasts.tsv',sep='\t');d=d[d.normalization.eq('TMM')]
c=pd.read_csv(BASE/'tables/gene_coverage.tsv',sep='\t').set_index('gene');colors=['#0072B2','#E69F00','#009E73','#CC79A7'];exports=[]
def save(fig,name):
 for ext in ['png','pdf','svg']:
  p=BASE/'figures'/f'{name}.{ext}';fig.savefig(p,bbox_inches='tight',facecolor='white');exports.append(dict(file=p.relative_to(BASE).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 plt.close(fig)
def heat(ax,genes,contrasts,labels,title,limit=3):
 z=s.pivot(index='feature',columns='contrast',values='mean').reindex(index=genes,columns=contrasts)
 cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#ededed');im=ax.imshow(z,aspect='auto',cmap=cmap,vmin=-limit,vmax=limit)
 ax.set_yticks(range(len(genes)),[g+('*' if g in c.index and c.loc[g,'mapped']==True and c.loc[g,'adequately_detected']!=True else '') for g in genes]);ax.set_xticks(range(len(contrasts)),labels,fontsize=8);ax.set_title(title,loc='left',fontweight='bold',pad=15)
 for i in range(len(genes)):
  for j in range(len(contrasts)):
   v=z.iloc[i,j];ax.text(j,i,'NA' if pd.isna(v) else f'{v:+.2f}',ha='center',va='center',fontsize=8,color='white' if pd.notna(v) and abs(v)>limit*.7 else '#222222')
 ax.tick_params(length=0);return im
contrasts=['CHIR_without_TGF','CHIR_with_TGF','TGF_without_CHIR','TGF_with_CHIR','interaction'];labels=['CHIR\nwithout TGF','CHIR\nwith TGF','TGF\nwithout CHIR','TGF\nwith CHIR','Interaction']
fig,(a,b)=plt.subplots(1,2,figsize=(12,7),gridspec_kw={'width_ratios':[1.5,1]});fig.subplots_adjust(wspace=.42,bottom=.22,top=.82)
genes=[f'FZD{i}' for i in range(1,11)];im=heat(a,genes,contrasts,labels,'A  Mean donor contrasts',2.5)
for i,g in enumerate(genes):
 z=d[d.feature.eq(g)&d.contrast.eq('interaction')]
 if z.empty:b.text(.02,i,'Unavailable in source table',transform=b.get_yaxis_transform(),va='center',fontsize=8);continue
 b.plot([z.delta.min(),z.delta.max()],[i,i],color='#bbbbbb',lw=1)
 for _,r in z.iterrows():b.scatter(r.delta,i+(r.donor-2.5)*.07,s=24,color=colors[int(r.donor)-1])
 b.plot(z.delta.mean(),i,'|',ms=11,color='black')
b.axvline(0,color='#555555',lw=.8,ls='--');b.set_yticks(range(10),[g+('*' if g in ['FZD3','FZD5','FZD8','FZD9'] else '') for g in genes]);b.set_ylim(9.5,-.5);b.set_xlabel('Within-donor interaction\nDifference of log2(CPM + 1) differences');b.set_title('B  All four donor interactions',loc='left',fontweight='bold',pad=15)
fig.colorbar(im,ax=a,location='bottom',fraction=.065,pad=.19,label='Mean difference on log2(CPM + 1) scale')
fig.suptitle('A20 extension | Concurrent inputs reshape FZD-family RNA',fontweight='bold',y=.97)
fig.legend([Line2D([0],[0],marker='o',ls='',color=colors[i]) for i in range(4)],[f'Donor {i}' for i in range(1,5)],loc='lower center',bbox_to_anchor=(.75,.11),ncol=4,frameon=False,fontsize=8)
fig.text(.5,.045,'* Low detection: fewer than 4 libraries with >=10 counts. FZD10 is absent from the source table; NA is not zero expression.',ha='center',fontsize=8)
fig.text(.5,.015,'Four matched human fibroblast donors; concurrent TGF-beta x CHIR. RNA responses do not establish receptor activity or subtype dependence.',ha='center',fontsize=8)
save(fig,'A20_EXT_F1_fzd_family')
fig,axs=plt.subplots(2,2,figsize=(10.5,7));fig.subplots_adjust(hspace=.55,wspace=.35,bottom=.17,top=.86)
for ax,feature,title in zip(axs.flat,['canonical_response','support','collagen','TGF_response'],['A  Canonical-response RNA','B  Selected support-ligand RNA','C  Collagen RNA','D  TGF-response RNA']):
 z=d[d.feature.eq(feature)].pivot(index='donor',columns='contrast',values='delta')
 for donor,r in z.iterrows():ax.plot([0,1],[r.CHIR_without_TGF,r.CHIR_with_TGF],'-o',lw=1,color=colors[int(donor)-1],ms=4)
 ax.axhline(0,color='#777777',lw=.7,ls='--');ax.set_xticks([0,1],['CHIR effect\nwithout TGF','CHIR effect\nwith TGF']);ax.set_xlim(-.2,1.2);ax.set_ylabel('Mean-gene log2(CPM + 1) difference');ax.set_title(title,loc='left',fontweight='bold');v=z.interaction;ax.grid(axis='y',alpha=.12)
fig.suptitle('A20 extension | Canonical-response RNA and support RNA diverge',fontweight='bold',y=.96)
fig.legend([Line2D([0],[0],marker='o',color=colors[i]) for i in range(4)],[f'Donor {i}' for i in range(1,5)],loc='lower center',bbox_to_anchor=(.5,.07),ncol=4,frameon=False,fontsize=8)
fig.text(.5,.025,'Each line joins responses from the same donor. Fixed panels have different genes and do not measure comparable quantities of function.',ha='center',fontsize=8)
save(fig,'A20_EXT_F2_input_context')
fig,(a,b)=plt.subplots(1,2,figsize=(12,7),gridspec_kw={'width_ratios':[1,1]});fig.subplots_adjust(wspace=.4,bottom=.21,top=.85)
im=heat(a,['WNT2','FGF7','FGF10','HGF'],contrasts,labels,'A  Support genes',3)
heat(b,['COL1A1','COL1A2','COL3A1','COL5A1','COL5A2','COL6A1','COL6A2','COL6A3'],contrasts,labels,'B  Collagen genes',3)
fig.colorbar(im,ax=[a,b],location='bottom',fraction=.06,pad=.17,label='Mean donor contrast: log2(CPM + 1) scale')
fig.suptitle('A20 extension | Individual genes qualify the panel averages',fontweight='bold',y=.96)
fig.text(.5,.045,'Mean of four donor contrasts; no significance labels. TGF raises WNT2 while lowering the other three selected support genes on average.',ha='center',fontsize=8)
fig.text(.5,.015,'TMM normalization shown. 15 of 240 gene/panel contrast directions change under total-count normalization; complete sensitivity table retained.',ha='center',fontsize=8)
save(fig,'A20_EXT_S1_gene_responses')
(BASE/'reports/figure_manifest.json').write_text(json.dumps(exports,indent=2)+'\n');print(f'{len(exports)} exports saved.')
