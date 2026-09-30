"""A21 animal-level context figures from frozen deposited estimates."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
BASE=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'savefig.dpi':300})
p=pd.read_csv(BASE/'tables/paired_differences.tsv',sep='\t')
s=pd.read_csv(BASE/'tables/contrast_summary.tsv',sep='\t')
c=pd.read_csv(BASE/'tables/coverage.tsv',sep='\t')
r=pd.read_csv(BASE/'tables/within_day_associations.tsv',sep='\t')
days=[0,3,5,7];cols=['#0072B2','#E69F00','#009E73'];exports=[]
def save(fig,name):
 for ext in ['png','pdf','svg']:
  path=BASE/'figures'/f'{name}.{ext}';fig.savefig(path,bbox_inches='tight',facecolor='white')
  exports.append(dict(file=path.relative_to(BASE).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(9,6.8),sharey=True);fig.subplots_adjust(hspace=.45,wspace=.25,bottom=.13,top=.86)
q=p[(p.cell_floor==20)&p.contrast.eq('gCap_minus_aCap')&p.feature.eq('Fzd4')]
for ax,day,letter in zip(axs.flat,days,'ABCD'):
 z=q[q.day.eq(day)].sort_values('animal')
 for _,v in z.iterrows():
  k=(int(v.animal)-1)//4;ax.plot([0,1],[v.value_right,v.value_left],'-o',color=cols[k],lw=1.1,ms=5,label=f'Animal {int(v.animal)}')
 ax.set_xticks([0,1],['Aerocyte','gCap']);ax.set_xlim(-.18,1.18);ax.set_ylabel('Fzd4 log2(CPM + 1)')
 ax.set_title(f'{letter}  '+('Control' if day==0 else f'Day {day}')+f' | {len(z)} paired '+('animal' if len(z)==1 else 'animals'),loc='left',fontweight='bold')
 ax.grid(axis='y',alpha=.15);ax.legend(frameon=False,fontsize=8,loc='best')
fig.suptitle('A21 | Fzd4 enrichment recurs in an independent capillary dataset',fontweight='bold')
fig.text(.5,.03,'GSE211335: 12 animals, 3 per condition. Pairs require >=20 cells per state; lines join states within the same animal.\nSeven pairs qualify. RNA enrichment does not establish renewal, receptor engagement or vascular function.',ha='center',fontsize=8)
save(fig,'A21_F1_capillary_context')
fig,axs=plt.subplots(2,2,figsize=(11.5,8));fig.subplots_adjust(hspace=.64,wspace=.33,bottom=.16,top=.88)
for ax,feature,letter,title in [(axs[0,0],'Fzd4','A','Fzd4 RNA'),(axs[0,1],'cycling','B','Cycling-panel RNA')]:
 z=p[(p.cell_floor==20)&p.contrast.eq('transitional1_minus_gCap0')&p.feature.eq(feature)]
 for x,day in enumerate(days):
  w=z[z.day.eq(day)].sort_values('animal')
  ax.plot([x,x],[w.delta.min(),w.delta.max()],color='#777777',lw=1)
  for k,(_,v) in enumerate(w.iterrows()):ax.scatter(x+(k-(len(w)-1)/2)*.10,v.delta,s=30,color=cols[(int(v.animal)-1)//4])
  ax.plot(x,w.delta.mean(),'_',color='black',ms=13,mew=2)
 ax.axhline(0,color='#777777',ls='--',lw=.8);ax.set_xticks(range(4),['Control\nn=3','Day 3\nn=3','Day 5\nn=2','Day 7\nn=3'])
 ax.set_ylabel('Transitional state 1 minus major gCap state 0\nDifference on log2(CPM + 1) scale')
 ax.set_title(f'{letter}  {title}',loc='left',fontweight='bold');ax.grid(axis='y',alpha=.12)
ax=axs[1,0];z=r[r.cell_floor.eq(20)];names=['gCap','gCap_0'];vals=z.pivot(index='state',columns='day',values='rho').reindex(index=names,columns=days)
cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#eeeeee');ax.imshow(vals,aspect='auto',cmap=cmap,vmin=-1,vmax=1)
for i,state in enumerate(names):
 for j,day in enumerate(days):
  row=z[(z.state==state)&(z.day==day)].iloc[0];v=row.rho
  text=f'{v:+.2f}\nn={int(row.animals)}' if pd.notna(v) else f'Not estimated\nn={int(row.animals)}'
  ax.text(j,i,text,ha='center',va='center',fontsize=8,color='white' if pd.notna(v) and abs(v)>.7 else '#222222')
ax.set_yticks(range(2),['All gCap states','Major gCap state 0']);ax.set_xticks(range(4),['Control','Day 3','Day 5','Day 7']);ax.tick_params(length=0)
ax.set_title('C  Within-condition Fzd4-cycling rank correlation',loc='left',fontweight='bold',pad=12)
ax=axs[1,1]
for dayx,day in enumerate(days):
 z=c[(c.kind=='cluster')&(c.state=='gCap_cycling_7')&(c.day==day)].sort_values('animal')
 # Explicit zero only for no cells assigned to this state in an otherwise sampled animal.
 animals=[dayx+1,dayx+5,dayx+9]
 for k,animal in enumerate(animals):
  q=z[z.animal.eq(animal)];value=int(q.cells.iloc[0]) if len(q) else 0
  ax.scatter(dayx+(k-1)*.1,value,color=cols[k],s=28)
ax.axhline(20,color='#555555',ls='--',lw=1);ax.text(.03,.91,'Primary floor: 20 cells',transform=ax.transAxes,fontsize=8)
ax.set_xticks(range(4),['Control','Day 3','Day 5','Day 7']);ax.set_ylim(-1,24);ax.set_ylabel('Sampled cells per animal in state 7');ax.set_title('D  Cycling state lacks primary coverage',loc='left',fontweight='bold')
fig.suptitle('A21 | Fzd4 is lower in the author-defined transitional state',fontweight='bold')
fig.text(.5,.07,'A-B: all qualifying animal pairs; black marks are means and lines are observed ranges, not confidence intervals.\nC: three-animal correlations are descriptive and cannot establish population direction. D: no state-7 comparison meets the primary floor.',ha='center',fontsize=8)
fig.text(.5,.025,'Author-defined states are expression contexts, not traced transitions. No Fzd4 perturbation was performed in this dataset.',ha='center',fontsize=8)
save(fig,'A21_F2_substate_and_cycling')
old=pd.read_csv(BASE/'tables/prior_day42_cohort.tsv',sep='\t').sort_values(['round','tracing_label_day'])
fig,(ax,bx)=plt.subplots(1,2,figsize=(12,5),gridspec_kw={'width_ratios':[1.55,1]});fig.subplots_adjust(wspace=.28,bottom=.21,top=.83)
rows=[]
for _,v in old.iterrows():
 rows.append([v.unit.replace('EEM-scRNA-',''),v['round'][:4],str(int(v.tracing_label_day)),v.sex_y,'Cre/Cre' if 'Cre/Cre' in v.genotype else 'Cre/+'])
ax.axis('off');tab=ax.table(cellText=rows,colLabels=['Source mouse','Round','Label cohort','Sex','Ki67 reporter'],cellLoc='center',loc='center',bbox=[0,.07,1,.8]);tab.auto_set_font_size(False);tab.set_fontsize(9)
for (i,j),cell in tab.get_celld().items():
 cell.set_edgecolor('#dddddd');cell.set_linewidth(.4)
 if i==0:cell.set_facecolor('#e8edf2');cell.set_text_props(weight='bold')
 elif i<=4:cell.set_facecolor('#eef5fb')
 else:cell.set_facecolor('#fff7e8')
ax.set_title('A  Existing day-42 cohort, resolved metadata',loc='left',fontweight='bold')
for k,(round,z) in enumerate(old.groupby('round')):
 bx.scatter(z.cpm,z.cycling_panel,color=cols[k],s=40,label=f'{round} (n=4)')
 for _,v in z.iterrows():bx.annotate(v.unit[-3:],(v.cpm,v.cycling_panel),xytext=(4,4),textcoords='offset points',fontsize=7)
bx.set_xlabel('CAP1 Fzd4 CPM');bx.set_ylabel('Original cycling-panel score')
bx.set_title('B  Original Nb2 association, reused evidence',loc='left',fontweight='bold')
bx.legend(frameon=False,fontsize=8,loc='upper left')
bx.text(.04,.65,'Pooled rho = +0.738\n2021 rho = -0.400\n2022 rho = +1.000',transform=bx.transAxes,fontsize=9)
fig.suptitle('A21 | Cohort identity qualifies the original expression lead',fontweight='bold')
fig.text(.5,.075,'Each label cohort occurs in both rounds; reporter genotype and sex are imbalanced. These are Ki67 reporter genotypes, not Fzd4 perturbations.\nEight mouse samples and original estimates are reused from Nb2. Resolving metadata does not create independent replication.',ha='center',fontsize=8)
save(fig,'A21_S1_prior_cohort')
(BASE/'reports/figure_manifest.json').write_text(json.dumps(exports,indent=2)+'\n')
print(f'{len(exports)} figure exports saved.')
