"""Run pinned limma, independently verify WLS contrasts, render pre-RQ evidence."""
import argparse, json, subprocess, shutil
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages

GENES=['ODC1','SRM','SMS','SAT1','SMOX','PGAM1','LDHA','TPI1','FOXP3','RORC','IL17A','KDM6B']
COLORS={'Th17p':'#287DB8','Th17n':'#8657A3','iTreg':'#26866D'}

def verify(out,results):
    errors=[]
    for series in ['GSE162300','GSE162382']:
        d=pd.read_csv(out/f'{series}_design.tsv',sep='\t',index_col=0)
        c=pd.read_csv(out/f'{series}_contrasts.tsv',sep='\t',index_col=0)
        e=pd.read_csv(out/f'{series}_voom_E.tsv.gz',sep='\t',index_col=0)
        w=pd.read_csv(out/f'{series}_voom_weights.tsv.gz',sep='\t',index_col=0)
        assert list(e.columns)==list(d.index)==list(w.columns)
        assert list(d.columns)==list(c.index) and e.index.equals(w.index)
        assert np.linalg.matrix_rank(d)==d.shape[1]
        indices=sorted(set(np.linspace(0,len(e)-1,101,dtype=int))|{e.index.get_loc(g) for g in GENES if g in e.index})
        x=d.to_numpy();C=c.to_numpy();maximum_fc=maximum_se=0.
        for i in indices:
            wt=w.iloc[i].to_numpy();y=e.iloc[i].to_numpy()
            gram=x.T@(wt[:,None]*x);beta=np.linalg.solve(gram,x.T@(wt*y));fc=C.T@beta
            variance=np.sum(C*np.linalg.solve(gram,C),axis=0)
            r=results[(results.series==series)&(results.gene==e.index[i])].set_index('contrast').loc[c.columns]
            se=np.sqrt(variance*r.s2_post.to_numpy())
            maximum_fc=max(maximum_fc,float(np.max(np.abs(fc-r.log2FC.to_numpy()))))
            maximum_se=max(maximum_se,float(np.max(np.abs(se-r.moderated_SE.to_numpy()))))
        assert maximum_fc<1e-8 and maximum_se<1e-8,(maximum_fc,maximum_se)
        errors.append({'series':series,'WLS_genes_checked':len(indices),'maximum_fc_error':maximum_fc,'maximum_SE_error':maximum_se})
    max_p=max_q=max_ci=0.
    for _,r in results.groupby(['series','contrast'],sort=False):
        p=2*student_t.sf(np.abs(r.log2FC/r.moderated_SE),r.df)
        order=np.argsort(p);q=np.empty(len(p));q[order]=np.minimum(1,np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1])
        max_p=max(max_p,float(np.max(np.abs(p-r.p))))
        max_q=max(max_q,float(np.max(np.abs(q-r.q))))
        ci=student_t.ppf(.975,r.df)*r.moderated_SE
        max_ci=max(max_ci,float(np.max(np.abs(r.log2FC-ci-r.lower))),float(np.max(np.abs(r.log2FC+ci-r.upper))))
        expected=(q<=.05)&(np.abs(r.log2FC)>=np.log2(1.5))
        assert np.array_equal(expected,r.DE.to_numpy())
    assert max_p<1e-9 and max_q<1e-9 and max_ci<1e-7
    pd.DataFrame(errors).to_csv(out/'independent_WLS_checks.tsv',sep='\t',index=False)
    (out/'verification.json').write_text(json.dumps({'status':'pass','WLS':errors,'max_p_error':max_p,'max_q_error':max_q,'max_CI_error':max_ci,'tolerances':{'WLS_absolute':1e-8,'p_q_absolute':1e-9,'CI_absolute':1e-7},'limits':'Arithmetic verification uses the same measurements. Empirical Bayes prior and voom weights remain package estimates; biological independence and exact author settings are not verified.'},indent=2)+'\n')

def figures(out,r):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    programs=pd.read_csv(out/'gene_programs.tsv',sep='\t');pc=pd.read_csv(out/'selected_PCA.tsv',sep='\t')
    plates=[]
    fig=plt.figure(figsize=(13,9));gs=fig.add_gridspec(2,3,height_ratios=[1.1,1],left=.08,right=.97,top=.81,bottom=.13,hspace=.55,wspace=.35)
    fig.suptitle('Source-aligned RNA reconstruction: baseline programs and DFMO',x=.045,y=.98,ha='left',fontsize=15,fontweight='bold')
    fig.text(.045,.927,'68-hour mouse CD4 T-cell cultures | TMM + limma-voom | animal-blocked models\nA: 3 WT animals, Th17p / Th17n / iTreg; B: 4 WT + 3 JMJD3 KO, Th17n / iTreg\nSource-aligned reconstruction; exact author gene sets and supplementary-number concordance are unavailable.',va='top',fontsize=10)
    ax=fig.add_subplot(gs[0,:2])
    for (animal,cell),pair in pc.groupby(['animal_id','cell_type']):ax.plot(pair.PC1,pair.PC2,color='#AAAAAA',lw=.6,zorder=1)
    for z in pc.itertuples():ax.scatter(z.PC1,z.PC2,s=40,facecolor=COLORS[z.cell_type] if z.treatment=='DFMO' else 'white',edgecolor=COLORS[z.cell_type],zorder=2)
    ax.set(xlabel=f'PC1 ({pc.PC1_percent.iloc[0]:.1f}% selected-gene variance)',ylabel=f'PC2 ({pc.PC2_percent.iloc[0]:.1f}% selected-gene variance)')
    ax.set_title(f'A  GSE162300: {int(pc.selected_genes.iloc[0]):,} baseline-DE-selected genes',loc='left')
    handles=[Line2D([],[],marker='o',linestyle='',color=v,label=k)for k,v in COLORS.items()]
    handles.extend([Line2D([],[],marker='o',linestyle='',color='#555',markerfacecolor='white',label='Vehicle'),Line2D([],[],marker='o',linestyle='',color='#555',label='DFMO')])
    ax.legend(handles=handles,fontsize=8,ncol=3,loc='best',frameon=False)
    ax=fig.add_subplot(gs[0,2]);ax.axis('off')
    ax.text(0,1,'How to read this plate',va='top',fontweight='bold')
    ax.text(0,.87,'A: genes selected only by vehicle\nlineage contrasts; no gene z-scoring.\nLines connect animal-matched cultures.\n\nB–D: each step is a gene, not an animal.\nPositive x: higher RNA after DFMO.\n\nPrograms use the same study controls.\nB-study primary program balances\nWT and KO baseline contrasts equally.\nNo conversion or fate is measured.',va='top',fontsize=9,linespacing=1.4)
    for ax,series,contrast,label in zip([fig.add_subplot(gs[1,i])for i in range(3)],['GSE162300','GSE162382','GSE162382'],['DFMO_WT_Th17n','DFMO_WT_Th17n','DFMO_JMJD3_KO_Th17n'],['B  A-study: Th17n WT (n=3)','C  B-study: Th17n WT (n=4)','D  B-study: Th17n KO (n=3)']):
        z=r[(r.series==series)&(r.contrast==contrast)].merge(programs[programs.series==series][['gene','primary_program']],on='gene',validate='one_to_one')
        for prog,color in [('Th17','#CE791A'),('Treg','#7851A9')]:
            values=np.sort(z.loc[z.primary_program==prog,'log2FC'].to_numpy());ax.step(values,np.arange(1,len(values)+1)/len(values),where='post',label=f'{prog} (g={len(values):,})',color=color)
        ax.axvline(0,color='#999',lw=.7);ax.set(title=label,xlabel='DFMO − vehicle: fitted log₂ fold change',ylabel='Cumulative fraction of program genes',ylim=(0,1.02));ax.legend(frameon=False,fontsize=8,loc='lower right')
    fig.text(.045,.04,'Gene selection: BH q ≤ 0.05 and |log₂FC| ≥ log₂(1.5). Curves summarize selected-gene distributions, not independent replicates.\nA differs from the published 3,414-gene PCA unless exact source selection is recovered. All tested genes and sensitivity partitions are retained.',fontsize=9)
    plates.append(('figure_6_source_aligned_RNA',fig))
    fig,axes=plt.subplots(1,2,figsize=(13,8.6),sharey=True);fig.subplots_adjust(left=.11,right=.97,top=.76,bottom=.18,wspace=.28)
    fig.suptitle('JMJD3 dependence: direct genotype × DFMO contrasts',x=.055,y=.98,ha='left',fontsize=16,fontweight='bold')
    fig.text(.055,.927,'GSE162382 | 68-hour bulk RNA | 4 WT + 3 conditional-KO animal labels, paired treatment cultures\nEndpoint: (DFMO − vehicle)KO − (DFMO − vehicle)WT on the fitted log₂ RNA-abundance scale.\nDots: estimates; bars: 95% moderated model intervals. Filled dots: BH q ≤ 0.05 across all tested genes in that contrast.',fontsize=10,va='top')
    for ax,cell,letter in zip(axes,['Th17n','iTreg'],'AB'):
        z=r[(r.series=='GSE162382')&(r.contrast==f'interaction_KO_minus_WT_{cell}')].set_index('gene')
        ax.axvline(0,color='#999',lw=.8)
        for i,g in enumerate(GENES):
            if g not in z.index:ax.text(0,i,'filtered',fontsize=8);continue
            q=z.loc[g];ax.plot([q.lower,q.upper],[i,i],color=COLORS[cell],lw=1.5)
            ax.scatter(q.log2FC,i,s=35,edgecolor=COLORS[cell],facecolor=COLORS[cell] if q.q<=.05 else 'white',zorder=3)
        ax.set_yticks(range(len(GENES)),[g.capitalize() for g in GENES]);ax.set_ylim(len(GENES)-.4,-.6);ax.set_title(f'{letter}  {cell}',loc='left');ax.set_xlabel('Difference of DFMO responses (KO − WT), log₂ scale');ax.margins(x=.15)
    fig.text(.055,.065,'Positive: the KO response is more positive (or less negative); negative: more negative (or less positive).\nAn interaction is not a mediation test. Open points do not establish equivalence. Intervals are conditional on this model and source labels;\nphysical specimen independence is unverified. The twelve genes were fixed in the earlier descriptive contract.',fontsize=9)
    plates.append(('figure_7_JMJD3_interactions',fig))
    with PdfPages(out/'Wagner_R3_limma_figures.pdf') as pdf:
        for name,f in plates:
            for ext in ['png','pdf','svg']:f.savefig(out/f'{name}.{ext}',dpi=300,facecolor='white')
            pdf.savefig(f);plt.close(f)
    r[r.gene.isin(GENES)].to_csv(out/'prespecified_gene_models.tsv',sep='\t',index=False,float_format='%.12g')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    exe=Path('.tools/R-4.6.1/bin/Rscript.exe');assert exe.exists()
    subprocess.run([str(exe),'--vanilla',str(Path(__file__).with_suffix('.R')),str(a.output)],check=True)
    r=pd.read_csv(a.output/'all_contrasts.tsv.gz',sep='\t');assert not r[['log2FC','p','q','moderated_SE']].isna().any().any()
    verify(a.output,r);figures(a.output,r)
    print(json.dumps({'status':'verified','model_rows':len(r),'scope':'source-aligned, exposed, descriptive conditional-model reconstruction'}))
if __name__=='__main__':main()
