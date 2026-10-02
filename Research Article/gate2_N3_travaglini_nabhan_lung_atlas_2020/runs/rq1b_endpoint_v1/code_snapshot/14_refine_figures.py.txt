"""Readability-only refinements for crowded labels in Nb4 figures 8–10."""
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import PACKAGE, read_json, write_json, new_run, finish_record, sha256


def main():
    out=new_run(PACKAGE/'figures/refinement_v1');run=PACKAGE/'runs/extended_visual_v1';inputs={}
    def read(name):
        inputs[name]=sha256(run/name);return pd.read_csv(run/name,sep='\t')
    def save(fig,name):
        for i,ax in enumerate(fig.axes):
            if ax.get_label()!='<colorbar>':ax.text(0,1.04,chr(97+i),transform=ax.transAxes,fontweight='bold',fontsize=13)
        for ext in ['png','svg','pdf']:fig.savefig(out/(name+'.'+ext),dpi=300,facecolor='white')
        plt.close(fig)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    pca=read('pseudobulk_pca.tsv');models=read_json(run/'pseudobulk_pca_models.json');fig,axes=plt.subplots(1,2,figsize=(12,5.8))
    offsets={('A26','adventitial'):(20,16),('A43','adventitial'):(22,-16),('A44','adventitial'):(-34,14),('A26','alveolar'):(-22,-15),('A44','alveolar'):(-26,8)}
    for ax,cohort in zip(axes,['source','external']):
        for donor,d in pca[pca.cohort==cohort].groupby('donor_id'):
            ax.plot(d.PC1,d.PC2,c='#aaa',lw=1,zorder=1)
            for row in d.itertuples():
                ax.scatter(row.PC1,row.PC2,c='#247a9b' if row.subtype=='alveolar' else '#c87b24',marker='o' if row.subtype=='alveolar' else 's',s=65,zorder=2)
                ax.annotate(row.donor_id,(row.PC1,row.PC2),xytext=offsets.get((row.donor_id,row.subtype),(4,5)),textcoords='offset points',fontsize=9,arrowprops={'arrowstyle':'-','color':'#888','lw':.5})
        r=models[cohort]['variance_ratio'];ax.set(title='Travaglini 10x | 2 donors' if cohort=='source' else 'Madissoon cells | 4 donors',xlabel=f'PC1 ({r[0]:.1%} variance)',ylabel=f'PC2 ({r[1]:.1%} variance)');ax.margins(.2)
    handles=[plt.Line2D([],[],c='#247a9b',marker='o',ls='',label='Alveolar'),plt.Line2D([],[],c='#c87b24',marker='s',ls='',label='Adventitial')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.09),ncol=2,frameon=False);fig.suptitle('Donor-level fibroblast PCA in separate cohorts',fontsize=15)
    fig.text(.5,.015,'Primary cell floor 20 per arm. Lines join the same donor; external profiles average eligible matched strata.\nTop 2,000 variable genes per cohort within the shared expressed universe; axes are fitted separately.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.2,1,.93));save(fig,'08_donor_pca')
    joined=read('source_gene_ranking.tsv').merge(read('external_gene_ranking.tsv'),on='gene',suffixes=('_source','_external'))
    rho=read_json(PACKAGE/'figures/extended_v2/genomewide_concordance.json')['spearman_across_genes']
    fig,ax=plt.subplots(figsize=(8.5,7));density=ax.hexbin(joined.mean_delta_source,joined.mean_delta_external,gridsize=65,mincnt=1,bins='log',cmap='Greys',linewidths=0,rasterized=True)
    shifts={'C3':(8,8),'CXCL2':(6,-18),'IL32':(-48,16),'CCL2':(25,-25),'CXCL12':(22,22),'SPINT2':(6,6),'SFRP2':(6,6),'PI16':(6,6),'GPC3':(6,6)}
    for gene,offset in shifts.items():
        r=joined[joined.gene==gene].iloc[0];ax.scatter(r.mean_delta_source,r.mean_delta_external,c='#247a9b',s=32)
        ax.annotate(gene,(r.mean_delta_source,r.mean_delta_external),xytext=offset,textcoords='offset points',fontsize=9,fontstyle='italic',bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':1},arrowprops={'arrowstyle':'-','lw':.5,'color':'#555'})
    fig.colorbar(density,ax=ax,label='Genes per hexagon',pad=.02,shrink=.6)
    ax.axhline(0,c='#bbb',lw=.8);ax.axvline(0,c='#bbb',lw=.8);ax.set(xlabel='Travaglini 10x: mean paired difference',ylabel='Madissoon cells: mean paired difference',title=f'11,113 shared genes | descriptive Spearman r = {rho:.2f}')
    fig.suptitle('Cross-cohort fibroblast expression contrasts',fontsize=15)
    fig.text(.5,.02,'Alveolar − adventitial log2(CPM + 1); source n=2 and external n=4 donors.\nHighlighted genes were selected before this genome-wide fit. Correlation is across genes, not donors.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.1,1,.93));save(fig,'09_genomewide_transfer')
    gsea=read('hallmark_gsea.tsv');s=gsea[gsea.cohort=='source'].sort_values('NES');terms=list(s[s.NES<0].head(5).Term)+list(s[s.NES>0].tail(5).Term)
    fig,ax=plt.subplots(figsize=(12,7))
    for cohort,color,offset in [('source','#247a9b',-.12),('external','#c87b24',.12)]:
        d=gsea[gsea.cohort==cohort].set_index('Term').loc[terms]
        for j,(_,r) in enumerate(d.iterrows()):ax.scatter(r.NES,j+offset,s=60,c=color,marker='o' if r['FDR q-val']<=.05 else 'x')
        ax.scatter([],[],c=color,label=cohort.capitalize(),s=50)
    ax.set(yticks=range(len(terms)),yticklabels=[t.replace('HALLMARK_','').replace('_',' ').capitalize() for t in terms],xlabel='Normalized enrichment score (NES)');ax.axvline(0,c='#aaa',lw=.8);ax.invert_yaxis()
    fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.63,.08),ncol=2,frameon=False)
    fig.suptitle('Hallmark GSEA of genome-wide fibroblast contrasts',fontsize=15)
    fig.text(.5,.015,'Five strongest positive and negative source NES, with external estimates retained. Circles: gene-set FDR ≤0.05; crosses: >0.05.\n1,000 gene-set permutations; these q-values are not donor-level biological significance tests. All eligible sets are tabulated.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.19,1,.93));save(fig,'10_hallmark_gsea')
    write_json(out/'figure_inputs.json',inputs)
    finish_record(out,{'schema':'Nb4-render-refinement/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'Labels, density legend and GSEA legend refined; no numerical fits changed'})
    print('Refined labels in Figures 8–10.')


if __name__=='__main__':main()
