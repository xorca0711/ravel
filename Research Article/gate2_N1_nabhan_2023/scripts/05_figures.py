"""Render archived bulk and descriptive atlas measurements without refitting."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':170})
COLORS=['#737373','#253b56','#5ba7a3','#dc9b2c','#8456ad','#247cba']
ARMS=['Wnt','withdraw48','withdraw24','CHIR','Fzd5','Fzd6']
LABELS=['Wnt','48h off','24h off','CHIR','Fzd5','Fzd6']


def save(fig,path):
    fig.savefig(path,bbox_inches='tight',facecolor='white');plt.close(fig)


def bulk():
    root=ROOT/'trials/bulk_v1';t=root/'tables';out=root/'figures'
    a=pd.read_csv(t/'source_panel_expression.tsv',sep='\t');b=pd.read_csv(t/'panel_sample_scores.tsv',sep='\t')
    panels=['Wnt','proliferation','AT2','AT1','Hippo_associated']
    fig,axes=plt.subplots(2,5,figsize=(15,7.5),sharey=True)
    for j,p in enumerate(panels):
        for i,arm in enumerate(ARMS):
            z=a[(a.panel==p)&(a.arm==arm)].groupby('source_symbol').gene_z.mean()
            y=b[(b.panel==p)&(b.arm==arm)].mean_gene_z
            for ax,values in [(axes[0,j],z),(axes[1,j],y)]:
                ax.scatter(i+np.linspace(-.14,.14,len(values)),values,color=COLORS[i],s=28,alpha=.9)
                ax.plot([i-.23,i+.23],[values.mean()]*2,color='black',lw=1.3)
                ax.axhline(0,color='#ddd',lw=.7,zorder=0)
        axes[0,j].set_title(p.replace('_associated','*').capitalize())
        for ax in axes[:,j]:
            ax.set_xticks(range(6),LABELS,rotation=65,ha='right');ax.set_ylim(-2.5,3.4)
    axes[0,0].set_ylabel('Gene dots: mean of 3 libraries\nGene-wise z across all 18 libraries')
    axes[1,0].set_ylabel('Library dots: mean across panel genes\n3 deposited libraries per condition')
    fig.suptitle('Nb2 | Figure 4 panel directions, with genes and libraries displayed separately',fontsize=15,y=1.01)
    fig.text(.01,-.04,'*Hippo-associated panel uses Ccn1, Ccn2 and Amotl2; source Crim2 unresolved. These are RNA summaries, not signaling activity or cell fate.\nBlack ticks show means. The source culture/preparation map is unresolved; z-scores are descriptive displays.',fontsize=10)
    fig.tight_layout();save(fig,out/'01_source_panels.png')
    z=pd.read_csv(t/'pca_coordinates.tsv',sep='\t');fig,ax=plt.subplots(figsize=(8.5,5.4))
    for arm,c in zip(ARMS,COLORS):
        q=z[z.arm==arm];ax.scatter(q.PC1,q.PC2,label=LABELS[ARMS.index(arm)],s=60,c=c)
    for _,r in z[z.accession.isin(['GSM6369139','GSM6369143','GSM6369144'])].iterrows():
        left=r.accession=='GSM6369144'
        ax.annotate(r.accession,(r.PC1,r.PC2),xytext=(-8 if left else 6,12),ha='right' if left else 'left',textcoords='offset points',fontsize=9)
    ax.set(xlabel='PC1 (49.96% variance)',ylabel='PC2 (17.32% variance)',title='Nb2 | Bulk library heterogeneity: no libraries excluded')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=3,frameon=False)
    fig.text(.01,-.09,'TMM–voom log2CPM; 2,000 highest-variance genes. Labels identify separated libraries, not proven technical failures.',fontsize=9)
    fig.tight_layout();save(fig,out/'02_bulk_pca.png')
    e=pd.read_csv(t/'source_and_lead_effects.tsv',sep='\t')
    genes=['Axin2','Mki67','Sftpd','Sftpa1','Etv5','Ager','Hopx','Cav1','Ccn1','Ccn2','Amotl2','Tgfb2','Zbtb16']
    contrasts=['Fzd5_vs_CHIR','Fzd6_vs_CHIR','Fzd6_vs_Fzd5']
    fig,axes=plt.subplots(1,3,figsize=(13,6),sharey=True)
    for j,(ax,contrast) in enumerate(zip(axes,contrasts)):
        q=e[e.contrast==contrast].set_index('symbol').loc[genes]
        y=np.arange(len(genes));ax.errorbar(q.log2FC,y,xerr=[q.log2FC-q.CI_low,q.CI_high-q.log2FC],fmt='o',color=COLORS[4+j%2],capsize=2)
        limits=e[e.symbol.isin(genes)&e.contrast.isin(contrasts)]
        ax.axvline(0,c='#888',lw=1);ax.set_title(contrast.replace('_vs_',' − '));ax.set_xlabel('Model log2 fold change');ax.set_xlim(min(-3,limits.CI_low.min())-.35,max(3,limits.CI_high.max())+.35)
    axes[0].set_yticks(np.arange(len(genes)),genes);axes[0].invert_yaxis()
    fig.suptitle('Nb2 | Direct gene effects with conditional 95% intervals',y=1.01,fontsize=15)
    fig.text(.01,-.02,'Assumes independent source libraries, which public metadata do not independently verify. Intervals are gene-wise; FDR values are in the full tables.\nGenes shown are prespecified source panels/leads. No equivalence margin or later fate endpoint is available.',fontsize=10)
    fig.tight_layout();save(fig,out/'03_direct_effects.png')
    fixed=pd.read_csv(t/'camera_all_sets.tsv.gz',sep='\t');estimated=pd.read_csv(t/'hallmark_estimated_correlation.tsv',sep='\t')
    sets=['HALLMARK_OXIDATIVE_PHOSPHORYLATION','HALLMARK_MYC_TARGETS_V1','HALLMARK_MYC_TARGETS_V2','HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION','HALLMARK_WNT_BETA_CATENIN_SIGNALING','HALLMARK_TGF_BETA_SIGNALING']
    # Both settings compared within the same50-set Hallmark BH family for a fair sensitivity display.
    from scipy.stats import false_discovery_control
    h=fixed[fixed['set'].str.startswith('HALLMARK_')].copy()
    h['FDR_hallmark']=h.groupby('contrast').PValue.transform(lambda x:false_discovery_control(x.to_numpy()))
    fig,axes=plt.subplots(1,3,figsize=(13,4.9),sharey=True)
    rows=[]
    for ax,contrast in zip(axes,contrasts):
        q=h[h.contrast==contrast].set_index('set').loc[sets];r=estimated[estimated.contrast==contrast].set_index('set').loc[sets]
        for i,s in enumerate(sets):
            rows.append(dict(set=s,contrast=contrast,FDR_fixed_hallmark=q.loc[s,'FDR_hallmark'],FDR_estimated_hallmark=r.loc[s,'FDR'],estimated_correlation=r.loc[s,'Correlation']))
        ax.scatter(-np.log10(q.FDR_hallmark),range(6),s=35,label='Correlation = 0.01',color='#dc9b2c')
        ax.scatter(-np.log10(r.FDR),range(6),s=40,marker='x',label='Estimated correlation',color='#253b56')
        ax.axvline(-np.log10(.05),c='#aaa',ls='--');ax.set(title=contrast.replace('_vs_',' − '),xlabel='−log10 FDR (50 Hallmark sets)')
    axes[0].set_yticks(range(6),['Oxidative phosphorylation','MYC targets V1','MYC targets V2','EMT-associated genes','Wnt / beta-catenin','TGF-beta']);axes[0].invert_yaxis()
    axes[-1].legend(loc='upper center',bbox_to_anchor=(.4,-.22),frameon=False)
    fig.suptitle('Nb2 | Gene correlation changes enrichment confidence',fontsize=15,y=1.02)
    fig.text(.01,-.1,'Competitive gene-set tests; RNA enrichment is not metabolic flux, EMT, or pathway activity. Both displays use the same Hallmark multiplicity family.\nBulk replicate-independence caveat also applies. Selected pathways are illustrative; all 3,640 tested sets are retained.',fontsize=9)
    fig.tight_layout();save(fig,out/'04_enrichment_sensitivity.png')
    pd.DataFrame(rows).to_csv(t/'hallmark_comparable_sensitivity.tsv',sep='\t',index=False)


def atlas():
    root=ROOT/'trials/atlas_v1';out=root/'figures';out.mkdir(exist_ok=True)
    data=pd.read_csv(root/'tables/state_summary.tsv.gz',sep='\t')
    receptors=[f'Fzd{i}' for i in range(1,11)]+['Lrp5','Lrp6']
    settings=[('Habermann2020','author_labels','Control','not_applicable','Human control'),
              ('Habermann2020','author_labels','IPF','not_applicable','Human IPF'),
              ('Niethamer2025','doublets_removed','H1N1_infected',42.,'Mouse injury, day 42'),
              ('Niethamer2025','doublets_removed','H1N1_infected',90.,'Mouse injury, day 90')]
    human=['AT2','Transitional AT2','AT1','KRT5-/KRT17+','Basal','Ciliated','SCGB3A2+','Fibroblasts','Myofibroblasts','HAS1 High Fibroblasts','PLIN2+ Fibroblasts','Endothelial Cells','Lymphatic Endothelial Cells']
    mouse=['AT2','Alveolar_transitional','AT1_AT2','AT1','Krt5','Secretory','Ciliated','AF1','AF2','Adventitial_fibroblast','CAP1','CAP2','Arterial_endothelium','Venous_endothelium','Lymphatic_endothelium']
    for depth in [False,True]:
        fig,axes=plt.subplots(2,2,figsize=(14,11),constrained_layout=True)
        for ax,(dataset,mode,condition,day,title) in zip(axes.flat,settings):
            s=data[(data.dataset==dataset)&(data['mode']==mode)&(data.condition==condition)&(data.cell_floor==50)]
            if dataset=='Niethamer2025': s=s[pd.to_numeric(s.day,errors='coerce').eq(day)]
            wanted=human if dataset=='Habermann2020' else mouse
            # Use exact author labels, case/space tolerant only for presentation lookup.
            available={str(a).replace(' ','').lower():a for a in s.state.unique()}
            states=[available.get(v.replace(' ','').lower(),v) for v in wanted]
            value='median_depth500' if depth else 'median_detection';units='depth_units' if depth else 'units'
            for iy,state in enumerate(states):
                for ix,g in enumerate(receptors):
                    r=s[(s.state==state)&(s.gene==g)]
                    if r.empty or r.iloc[0][units]<3 or pd.isna(r.iloc[0][value]):
                        ax.scatter(ix,iy,c='#bcbcbc',marker='x',s=12);continue
                    r=r.iloc[0];ax.scatter(ix,iy,s=15+250*r[value],c=np.log10(1+r.median_cpm),cmap='viridis',vmin=0,vmax=3.5)
            ax.set_xticks(range(12),receptors,rotation=55,ha='right');ax.set_yticks(range(len(states)),states);ax.invert_yaxis();ax.set_title(title)
            ax.set_xlim(-.7,11.7);ax.grid(axis='y',color='#eee',lw=.6);ax.set_axisbelow(True)
        kind='Expected detection at 500 UMIs' if depth else 'Observed RNA detection'
        fig.suptitle('Nb2 | '+kind+' across source-defined compartments\nDots require ≥50 cells per unit and ≥3 units; gray × = insufficient coverage',fontsize=15)
        sm=plt.cm.ScalarMappable(cmap='viridis',norm=plt.Normalize(0,3.5));fig.colorbar(sm,ax=axes.ravel().tolist(),shrink=.45,label='Color: log10(1 + median unit CPM)')
        for frac in [.05,.25,.75]: axes[1,1].scatter([],[],s=15+250*frac,c='#888',label=f'{100*frac:g}% detection')
        axes[1,1].legend(loc='lower left',bbox_to_anchor=(0,-.45),ncol=3,frameon=False)
        fig.supxlabel('Human and mouse scales are descriptive within study. Source labels retained; CAP1/CAP2 do not establish regenerative function.\n'+('Size: depth-standardized detection; color retains original CPM. Eligibility can change after depth filtering.' if depth else 'Size: median detection across units; color: median unit CPM. Donor/cell ranges and cell-floor sensitivities are in tables.'),fontsize=10)
        save(fig,out/('02_receptor_depth500.png' if depth else '01_receptor_context.png'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--section',choices=['bulk','atlas','all'],default='all');args=p.parse_args()
    if args.section in ['bulk','all']: bulk()
    if args.section in ['atlas','all']: atlas()
