"""Nb4 formal figure gallery: embeddings, PCA and exploratory enrichment."""
from datetime import datetime, timezone
import importlib.util
import textwrap
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import PACKAGE, REPO, read_json, write_json, new_run, finish_record, sha256


def main():
    out=new_run(PACKAGE/'figures/extended_v2');run=PACKAGE/'runs/extended_visual_v1';inputs={}
    def read(name):
        path=run/name;inputs[name]=sha256(path);return pd.read_csv(path,sep='\t')
    def save(fig,name):
        panel=0
        for ax in fig.axes:
            if ax.get_label()!='<colorbar>':
                ax.text(.0,1.04,chr(97+panel),transform=ax.transAxes,fontweight='bold',fontsize=13);panel+=1
        for ext in ['png','svg','pdf']:fig.savefig(out/(name+'.'+ext),dpi=300,facecolor='white')
        plt.close(fig)
    def cats(ax,data,x,y,field,palette=None):
        groups=sorted(data[field].unique());colors=palette or dict(zip(groups,plt.get_cmap('tab10').colors))
        for label in groups:
            d=data[data[field]==label];ax.scatter(d[x],d[y],s=2,c=[colors[label]],label=label,alpha=.65,rasterized=True,linewidths=0)
        ax.set(xticks=[],yticks=[],xlabel=x.replace('1',' 1'),ylabel=y.replace('2',' 2'))
        ax.spines[['top','right']].set_visible(False)
        return ax.get_legend_handles_labels()
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    t=read('deposited_tsne.tsv');assert np.isfinite(t[['tSNE1','tSNE2']]).all().all()
    fig,axes=plt.subplots(1,2,figsize=(12,6))
    for ax,field,title in zip(axes,['source_compartment','donor_id'],['Author compartment','Sequenced donor']):
        cats(ax,t,'tSNE1','tSNE2',field);ax.set_title(title);ax.legend(markerscale=4,frameon=False,loc='upper right')
    fig.suptitle('Deposited atlas t-SNE | 60,993 normal-lung 10x cells',fontsize=15)
    fig.text(.5,.025,'Original deposited coordinates, with blood excluded. Capture and sorting prevent interpreting point fractions as tissue prevalence.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.08,1,.94));save(fig,'06_deposited_atlas_tsne')
    u=read('stromal_umap.tsv');fig,axes=plt.subplots(2,2,figsize=(14,11))
    ax=axes[0,0];handles,labels=cats(ax,u,'UMAP1','UMAP2','author_cell_type');ax.set_title('Author stromal identity')
    ax.legend(handles,labels,markerscale=4,frameon=False,loc='center left',bbox_to_anchor=(1, .5),fontsize=8)
    for ax,field,title in [(axes[0,1],'donor_id','Donor'),(axes[1,0],'anatomical_region','Anatomical region')]:
        cats(ax,u,'UMAP1','UMAP2',field);ax.set_title(title);ax.legend(markerscale=4,frameon=False,loc='upper right')
    ax=axes[1,1];ordered=u.sort_values('log1p_C3_CP10K');s=ax.scatter(ordered.UMAP1,ordered.UMAP2,c=ordered.log1p_C3_CP10K,cmap='viridis',s=3,rasterized=True,linewidths=0)
    ax.set(title='C3 expression',xlabel='UMAP 1',ylabel='UMAP 2',xticks=[],yticks=[]);fig.colorbar(s,ax=ax,label='log(1 + CP10K)',pad=.02)
    fig.suptitle('New stromal UMAP | 5,033 cells, 1,500 variable genes, 30 PCs',fontsize=15)
    fig.text(.5,.015,'Seed 20261002; 30 neighbours; minimum distance 0.4. Same coordinates in all panels; no batch correction or trajectory inference.\nDonor and regional structure remain visible; author labels were not used to fit the embedding.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.09,1,.94),w_pad=6);save(fig,'07_stromal_umap')
    pca=read('pseudobulk_pca.tsv');models=read_json(run/'pseudobulk_pca_models.json');fig,axes=plt.subplots(1,2,figsize=(12,5.8))
    for ax,cohort in zip(axes,['source','external']):
        sub=pca[pca.cohort==cohort]
        for donor,d in sub.groupby('donor_id'):
            ax.plot(d.PC1,d.PC2,c='#aaa',lw=1,zorder=1)
            for row in d.itertuples():
                ax.scatter(row.PC1,row.PC2,c='#247a9b' if row.subtype=='alveolar' else '#c87b24',marker='o' if row.subtype=='alveolar' else 's',s=65,zorder=2)
                ax.annotate(row.donor_id,(row.PC1,row.PC2),xytext=(4,5),textcoords='offset points',fontsize=9)
        ratio=models[cohort]['variance_ratio'];ax.set(title=('Travaglini 10x | 2 donors' if cohort=='source' else 'Madissoon cells | 4 donors'),xlabel=f'PC1 ({ratio[0]:.1%} variance)',ylabel=f'PC2 ({ratio[1]:.1%} variance)');ax.margins(.18)
    handles=[plt.Line2D([],[],c='#247a9b',marker='o',ls='',label='Alveolar'),plt.Line2D([],[],c='#c87b24',marker='s',ls='',label='Adventitial')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.09),ncol=2,frameon=False)
    fig.suptitle('Donor-level fibroblast PCA in separate cohorts',fontsize=15)
    fig.text(.5,.015,'Primary cell floor 20 per arm. Lines join the same donor; external profiles average eligible matched strata.\nTop 2,000 variable genes per cohort within the shared expressed universe; axes are fitted separately.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.2,1,.93));save(fig,'08_donor_pca')
    source=read('source_gene_ranking.tsv');external=read('external_gene_ranking.tsv');joined=source.merge(external,on='gene',suffixes=('_source','_external'))
    rho=float(spearmanr(joined.mean_delta_source,joined.mean_delta_external).statistic)
    fig,ax=plt.subplots(figsize=(8,7));ax.hexbin(joined.mean_delta_source,joined.mean_delta_external,gridsize=65,mincnt=1,bins='log',cmap='Greys',linewidths=0,rasterized=True)
    shifts={'C3':(6,6),'CXCL2':(6,-15),'IL32':(6,6),'CCL2':(6,-15),'CXCL12':(6,6),'SPINT2':(6,6),'SFRP2':(6,6),'PI16':(6,6),'GPC3':(6,6)}
    for gene,offset in shifts.items():
        row=joined[joined.gene==gene].iloc[0];ax.scatter(row.mean_delta_source,row.mean_delta_external,c='#247a9b',s=32);ax.annotate(gene,(row.mean_delta_source,row.mean_delta_external),xytext=offset,textcoords='offset points',fontsize=9,fontstyle='italic')
    ax.axhline(0,c='#bbb',lw=.8);ax.axvline(0,c='#bbb',lw=.8);ax.set(xlabel='Travaglini 10x: mean paired difference',ylabel='Madissoon cells: mean paired difference',title=f'11,113 shared genes | descriptive Spearman r = {rho:.2f}')
    fig.suptitle('Cross-cohort fibroblast expression contrasts',fontsize=15)
    fig.text(.5,.02,'Alveolar − adventitial log2(CPM + 1); source n=2 and external n=4 donors.\nHighlighted genes were selected before this genome-wide fit. Correlation is across genes, not donors.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.1,1,.93));save(fig,'09_genomewide_transfer')
    write_json(out/'genomewide_concordance.json',{'genes':len(joined),'spearman_across_genes':rho,'interpretation':'descriptive dependence across genes; no population p-value'})
    gsea=read('hallmark_gsea.tsv');s=gsea[gsea.cohort=='source'].sort_values('NES');terms=list(s[s.NES<0].head(5).Term)+list(s[s.NES>0].tail(5).Term)
    fig,ax=plt.subplots(figsize=(12,7))
    for cohort,color,offset in [('source','#247a9b',-.12),('external','#c87b24',.12)]:
        d=gsea[gsea.cohort==cohort].set_index('Term').loc[terms]
        for j,(_,row) in enumerate(d.iterrows()):
            ax.scatter(row.NES,j+offset,s=60,c=color,marker='o' if row['FDR q-val']<=.05 else 'x')
        ax.scatter([],[],c=color,label=cohort.capitalize(),s=50)
    ax.set(yticks=range(len(terms)),yticklabels=[t.replace('HALLMARK_','').replace('_',' ').capitalize() for t in terms],xlabel='Normalized enrichment score (NES)')
    ax.axvline(0,c='#aaa',lw=.8);ax.legend(frameon=False,loc='lower right');ax.invert_yaxis()
    fig.suptitle('Hallmark GSEA of genome-wide fibroblast contrasts',fontsize=15)
    fig.text(.5,.02,'Five strongest positive and negative source NES, with external estimates retained. Circles: gene-set FDR ≤0.05; crosses: >0.05.\n1,000 gene-set permutations; these q-values are not donor-level biological significance tests. All size-eligible sets are tabulated.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.12,1,.93));save(fig,'10_hallmark_gsea')
    go=read('go_bp_ora.tsv');fig,axes=plt.subplots(1,2,figsize=(17,11));selection=[]
    for ax,cohort in zip(axes,['source','external']):
        frames=[go[(go.cohort==cohort)&(go.direction==d)].sort_values(['q_BH_cohort_both_directions','term']).head(5) for d in ['alveolar','adventitial']]
        selected=pd.concat(frames).reset_index(drop=True);selection.append(selected)
        for j,row in selected.iterrows():
            ax.scatter(row.gene_ratio,j,s=30+row.overlap*1.5,c=[min(-np.log10(max(row.q_BH_cohort_both_directions,1e-300)),8)],cmap='viridis',vmin=0,vmax=8,marker='o' if row.direction=='alveolar' else '^')
        labels=['\n'.join(textwrap.wrap(t.replace('GOBP_','').replace('_',' ').capitalize(),38)) for t in selected.term]
        ax.set(yticks=range(len(selected)),yticklabels=labels,xlabel='Overlap / effect-selected foreground',title=cohort.capitalize()+' | GO biological process');ax.invert_yaxis();ax.tick_params(axis='y',labelsize=9);ax.margins(y=.08,x=.2)
    scalar=plt.cm.ScalarMappable(norm=plt.Normalize(0,8),cmap='viridis')
    fig.subplots_adjust(left=.22,right=.91,bottom=.12,top=.9,wspace=1.25)
    cax=fig.add_axes([.94,.3,.015,.4],label='<colorbar>');fig.colorbar(scalar,cax=cax,label='−log10(BH q), capped at 8')
    fig.suptitle('GO annotation of consistent, effect-selected fibroblast genes',fontsize=15)
    fig.text(.5,.025,'Circles: alveolar-up; triangles: adventitial-up; area scales with overlap count. Top five terms per direction/cohort; related GO terms overlap.\nForeground: |mean paired difference| ≥1, same sign in 2/2 source or ≥3/4 external donors. Background: 11,113 expressed genes.\nBH correction covers all eligible terms and both directions within cohort. This is annotation enrichment, not a DE-gene significance test.',ha='center',fontsize=10)
    save(fig,'11_go_biological_process');pd.concat(selection).to_csv(out/'GO_display_selection.tsv',sep='\t',index=False)
    curves=read('complement_running_curves.tsv');matched=read('complement_matched_null.tsv');fig,axes=plt.subplots(1,2,figsize=(12,5.7),sharey=True)
    for ax,cohort,color in zip(axes,['source','external'],['#247a9b','#c87b24']):
        d=curves[curves.cohort==cohort];ax.plot(d['rank'],d.running_ES,c=color,lw=1.8)
        hits=d.loc[d.hit,'rank'];ax.vlines(hits,-.44,-.40,color=color,lw=.5,alpha=.6)
        row=gsea[(gsea.cohort==cohort)&(gsea.Term=='HALLMARK_COMPLEMENT')].iloc[0];p=matched[matched.cohort==cohort].expression_matched_two_sided_p.iloc[0]
        ax.axhline(0,c='#aaa',lw=.8);ax.set(title=f'{cohort.capitalize()} | NES {row.NES:.2f}; gene-set q {row["FDR q-val"]:.2f}',xlabel='Rank: alveolar-enriched → adventitial-enriched',ylabel='Running enrichment score',ylim=(-.47,.45))
        ax.text(.02,.92,f'Expression-matched random-set p = {p:.3f}',transform=ax.transAxes,fontsize=9)
    fig.suptitle('C3 direction does not generalize to the entire complement gene set',fontsize=15)
    fig.text(.5,.02,'HALLMARK_COMPLEMENT selected before enrichment; 141 genes overlap the common universe. Ticks show set-member ranks.\nOpposite enrichment directions and non-small adjusted q-values retain the whole-program claim on hold.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.13,1,.93));save(fig,'12_complement_running_enrichment')
    # Inspect the concrete ambiguity flagged by GSEA: tied input scores.
    helper=REPO/'Research Article/gate1_01_niethamer_2025/trials/gsea_utils.py';spec=importlib.util.spec_from_file_location('gu',helper);gu=importlib.util.module_from_spec(spec);spec.loader.exec_module(gu)
    sets=gu.read_gmt(REPO/'raw_data/msigdb/h.all.v2024.1.Hs.symbols.gmt');tie_rows=[]
    for cohort,rank in [('source',source),('external',external)]:
        reverse=rank.sort_values(['mean_delta','gene'],ascending=[False,False],kind='stable')
        for term,genes in sets.items():
            if term not in set(gsea.loc[gsea.cohort==cohort,'Term']):continue
            original=gu.enrichment_score(rank.mean_delta.to_numpy(),rank.gene.isin(genes).to_numpy());flipped=gu.enrichment_score(reverse.mean_delta.to_numpy(),reverse.gene.isin(genes).to_numpy())
            deposited=float(gsea[(gsea.cohort==cohort)&(gsea.Term==term)].ES.iloc[0])
            tie_rows.append({'cohort':cohort,'term':term,'tied_score_fraction':float(rank.mean_delta.duplicated().mean()),'input_order_ES':original,'engine_ES':deposited,'reverse_tie_ES':flipped,'absolute_tie_change':abs(original-flipped),'engine_input_difference':abs(original-deposited)})
    pd.DataFrame(tie_rows).to_csv(out/'gsea_tie_diagnostic.tsv',sep='\t',index=False,float_format='%.8g')
    write_json(out/'figure_inputs.json',inputs)
    finish_record(out,{'schema':'Nb4-extended-figures/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'seven PNG/SVG/PDF figures; GO display selection and GSEA tie diagnostics retained'})
    print('Generated Nb4 figures 6–12 and tie-order diagnostics.')


if __name__=='__main__':main()
