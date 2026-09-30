"""Paper-style plots of observed values only; no simulated or inferred fate curves."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parents[1];T=B/'tables/exploratory_v1';F=B/'figures/exploratory_v1'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
COL=['#19768B','#CD6A30','#7357A5','#577D43']
def letter(ax,s):ax.text(-.16,1.10,s,transform=ax.transAxes,fontsize=13,fontweight='bold',va='top')
def export(fig,name):
 for ext in ['png','svg','pdf']:fig.savefig(F/f'{name}.{ext}',dpi=300,bbox_inches='tight')
 plt.close(fig)
def pairs(ax,data,conditions,labels,donors=None):
 donors=donors or sorted(data.donor.unique())
 for i,d in enumerate(donors):
  g=data[data.donor==d].set_index('condition');ys=[-g.loc[c,'delta_ct'] if c in g.index else np.nan for c in conditions];ax.plot(range(len(conditions)),ys,'o-',color=COL[i%4],lw=1.1,ms=4.5,label=d)
 ax.set_xticks(range(len(conditions)),labels);ax.set_xlim(-.25,len(conditions)-.75);ax.set_ylabel('Normalized expression (−ΔCt)');ax.grid(axis='y',color='#E7E9EC',lw=.6);ax.set_axisbelow(True)
def forest(ax,summary,effects,genes):
 ax.axvline(0,color='#AEB5BD',lw=.8)
 for i,gene in enumerate(genes):
  s=summary[summary.gene==gene].iloc[0];g=effects[effects.gene==gene]
  for j,r in enumerate(g.itertuples()):ax.plot(r.effect_log2,i+(j-(len(g)-1)/2)*.12,'o',color=COL[0],ms=4,alpha=.85)
  if np.isfinite(s.ci95_low):ax.plot([s.ci95_low,s.ci95_high],[i,i],color='#262F36',lw=1.2)
  ax.plot(s.mean_log2,i,'|',color='black',ms=10,mew=1.8)
 ax.set_yticks(range(len(genes)),genes);ax.invert_yaxis();ax.set_xlabel('Paired expression change (log2)');ax.grid(axis='x',color='#EEF0F2',lw=.6);ax.set_axisbelow(True)
def main():
 F.mkdir(parents=True,exist_ok=True);raw=pd.read_csv(T/'qpcr_source_rows.tsv',sep='\t');qs=pd.read_csv(T/'qpcr_effect_summary.tsv',sep='\t');qe=pd.read_csv(T/'qpcr_paired_effects.tsv',sep='\t');be=pd.read_csv(T/'bulk_program_effects.tsv',sep='\t');ge=pd.read_csv(T/'bulk_marker_effects.tsv',sep='\t')
 fig,axs=plt.subplots(2,2,figsize=(7.2,6.2));fig.subplots_adjust(wspace=.40,hspace=.82,top=.80,bottom=.17)
 for ax,gene,lab in zip(axs.flat,['SFTPC','FOXJ1','TP63','SCGB1A1'],'ABCD'):
  d=raw[(raw.sheet=='fig4b')&(raw.gene==gene)];pairs(ax,d,['AOM+CHIR','AOM'],['CHIR present','CHIR absent']);ax.set_title(gene,fontstyle='italic',loc='left',x=.13,y=1.16);ax.text(-.02,1.26,lab,transform=ax.transAxes,fontsize=13,fontweight='bold',va='top')
  z=qs[(qs.sheet=='fig4b')&(qs.gene==gene)].iloc[0];ax.text(.02,1.03,f'Mean change: {z.mean_log2:+.2f}',transform=ax.transAxes,va='bottom',fontsize=8)
 handles,labels=axs[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.025),title='Source donor lines (paired within gene)')
 fig.suptitle('CHIR absence changes alveolar and airway identity markers',x=.04,ha='left',fontsize=12)
 export(fig,'A19_F1_identity_context')
 fig=plt.figure(figsize=(9.1,4.7));gs=fig.add_gridspec(1,2,width_ratios=[1,1.35],wspace=.50);a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);fig.subplots_adjust(top=.80,bottom=.23,left=.09,right=.98)
 d=raw[raw.sheet=='fig6a'];pairs(a,d,['P1 AOM','P1 AOM+CHIR','P3 AOM+CHIR'],['P1\nno CHIR','P1\nCHIR','P3\nCHIR']);a.set_title('Airway-derived cultures: SFTPC',loc='left',fontstyle='italic');letter(a,'A');a.legend(frameon=False,fontsize=8,loc='best')
 forest(b,qs[qs.sheet=='fig5c'],qe[qe.sheet=='fig5c'],['GSK3B','SFTPC','FOXJ1','SCGB1A1','TP63','KRT5','SOX2']);b.set_title('Knockdown − control, with CHIR',loc='left');letter(b,'B')
 fig.suptitle('Early SFTPC induction declines despite continued CHIR',x=.04,ha='left',fontsize=12)
 fig.text(.09,.07,'A: donor-coded pooled cultures; passages do not trace individual cells.\nB: three paired donor lines; dots = line effects, bars = conditional 95% t intervals.',fontsize=8)
 export(fig,'A19_F2_persistence_and_input')
 fig=plt.figure(figsize=(9.2,7.2));gs=fig.add_gridspec(2,2,height_ratios=[1.2,.9],width_ratios=[1.2,1],wspace=.58,hspace=.65);a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);c=fig.add_subplot(gs[1,:]);fig.subplots_adjust(top=.87,bottom=.15,left=.20,right=.94)
 cols=[('control',1),('control',2),('GSK3KD',1),('GSK3KD',2)];panels=['AT2_identity','AT1_associated','Airway_differentiation','Canonical_Wnt_targets','Proliferation'];g=be[be.method=='TMM'];m=g.pivot(index='panel',columns=['background','block'],values='absence_effect').reindex(index=panels,columns=pd.MultiIndex.from_tuples(cols));im=a.imshow(m.values,vmin=-5.5,vmax=5.5,cmap='RdBu_r',aspect='auto');a.set_xticks(range(4),['Ctrl\nB1','Ctrl\nB2','KD\nB1','KD\nB2']);a.set_yticks(range(5),['AT2 identity (6/6)','AT1-associated (6/6)','Airway (2/3)','Wnt targets (4/4)','Proliferation (5/5)']);a.set_title('Program responses',loc='left');letter(a,'A')
 for i in range(5):
  for j in range(4):a.text(j,i,f'{m.iloc[i,j]:+.2f}',ha='center',va='center',fontsize=8,color='white' if abs(m.iloc[i,j])>3.2 else '#182129')
 cb=fig.colorbar(im,ax=a,fraction=.05,pad=.04);cb.ax.tick_params(labelsize=7);cb.set_label('CHIR absent − present',fontsize=8)
 genes=['AGER','HOPX','PDPN','CAV1','CLIC5','RTKN2'];z=ge[(ge.method=='TMM')&ge.gene.isin(genes)];b.axvline(0,color='#AEB5BD',lw=.8)
 for j,(bg,block) in enumerate(cols):
  x=z[(z.background==bg)&(z.block==block)].set_index('gene').reindex(genes).absence_effect;b.plot(x,np.arange(6)+(j-1.5)*.13,'o',ms=4,color=COL[j],label=f'{bg}, B{block}')
 b.set_yticks(range(6),genes);b.invert_yaxis();b.set_xlabel('CHIR absent − present\n(log2 normalized CPM change)');b.set_title('Individual AT1-associated genes',loc='left');letter(b,'B');b.legend(fontsize=7,frameon=False,bbox_to_anchor=(1.03,1),loc='upper left')
 labels=[];values=[];colors=[]
 for r in qe[(qe.sheet=='fig4b')&(qe.gene=='SFTPC')].itertuples():labels.append('qPCR '+r.donor);values.append(r.effect_log2);colors.append(COL[0])
 for r in ge[(ge.method=='TMM')&(ge.gene=='SFTPC')&(ge.background=='control')].itertuples():labels.append('Bulk block '+str(r.block));values.append(r.absence_effect);colors.append(COL[1])
 c.axvline(0,color='#AEB5BD',lw=.8);c.scatter(values,range(len(values)),c=colors,s=32);c.set_yticks(range(len(values)),labels);c.invert_yaxis();c.set_xlabel('SFTPC change with CHIR absence (assay-specific log2 scale)');c.set_title('SFTPC direction differs across the two source assays',loc='left');letter(c,'C')
 fig.suptitle('Bulk RNA supports mixed state changes, with assay-dependent SFTPC behavior',x=.04,ha='left',fontsize=12)
 fig.text(.12,.025,'Eight libraries in two source blocks; hairpin and block are confounded. No population tests.\nA: basal panel fails coverage (1/4). C: different preparations/normalization; effects are not pooled.',fontsize=8)
 export(fig,'A19_F3_bulk_response_context')
 fig,axs=plt.subplots(1,2,figsize=(8.5,4.3),gridspec_kw={'width_ratios':[1.2,1]});fig.subplots_adjust(wspace=.60,top=.79,bottom=.25,left=.11,right=.98)
 forest(axs[0],qs[qs.sheet=='fig4e'],qe[qe.sheet=='fig4e'],['TCF4','LEF1','AXIN2','TGFB1']);axs[0].set_title('CHIR absent − present; four donor lines',loc='left');letter(axs[0],'A')
 d=qs[qs.sheet=='fig6c'].pivot(index='gene',columns='comparison',values='n_pairs').reindex(index=['SFTPC','FOXJ1','TP63','SCGB1A1'],columns=['P3','P5']);axs[1].imshow(d,cmap='Blues',vmin=0,vmax=3,aspect='auto');axs[1].set_xticks([0,1],['P3 − P1','P5 − P1']);axs[1].set_yticks(range(4),d.index);axs[1].set_title('Quantified matched donor pairs',loc='left');letter(axs[1],'B')
 for i in range(4):
  for j in range(2):axs[1].text(j,i,str(int(d.iloc[i,j])),ha='center',va='center',color='white' if d.iloc[i,j]>=2 else 'black')
 fig.suptitle('Target-assay heterogeneity and limits of passage comparisons',x=.04,ha='left',fontsize=12)
 fig.text(.11,.065,'A: source assay “TCF4” is not assigned to TCF7L2; intervals are descriptive.\nB: zero means no quantified matched pair, not zero expression. Non-detects are retained.',fontsize=8)
 export(fig,'A19_S1_target_and_pairing')
 record={'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_tables':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in T.glob('*.tsv')},'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in F.iterdir() if p.suffix in ['.png','.svg','.pdf']}}
 (B/'reports/figure_render.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('Rendered four figures as PNG, editable SVG and PDF.')
if __name__=='__main__':main()
