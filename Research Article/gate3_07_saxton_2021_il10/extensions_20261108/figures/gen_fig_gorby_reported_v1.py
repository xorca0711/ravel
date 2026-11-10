"""Render fixed source estimates; dots are source blocks, not technical repeats."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def rows(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def main(run):
    source=rows(run/'source_estimates.csv');contrasts=rows(run/'block_contrasts.csv');summaries=rows(run/'summaries.csv')
    blocks=['D85','D93','D36'];colors=['#0072B2','#E69F00','#009E73'];genes=['IFNG','GZMB','IL18RAP']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axs=plt.subplots(2,3,figsize=(12,7.4))
    for j,gene in enumerate(genes):
        a,b=axs[:,j];a.set_title(gene,fontweight='bold')
        for block,color in zip(blocks,colors):
            for dose,start in [(0.1,0),(50.,3)]:
                rs=[next(r for r in source if r['gene']==gene and r['source_block']==block and float(r['dose_nM'])==dose and r['ligand']==ligand) for ligand in ['WTD','R5D']]
                a.plot([start,start+1],[float(r['reported_log2foldchange']) for r in rs],'-o',color=color,alpha=.8,label=block if start==0 else None,linewidth=1)
            ys=[float(next(r['difference'] for r in contrasts if r['gene']==gene and r['source_block']==block and float(r['dose_nM'])==dose and r['measure']=='reported_log2foldchange')) for dose in [.1,50.]]
            b.plot([0,1],ys,'-o',color=color,alpha=.8,linewidth=1)
        for k,dose in enumerate([.1,50.]):
            for measure,marker,offset,color in [('reported_log2foldchange','D',0,'black'),('log2_positive_pair_ratio','x',.09,'#777777')]:
                r=next(r for r in summaries if r['gene']==gene and float(r['dose_nM'])==dose and r['measure']==measure and r['omitted']=='none')
                if r['supported']=='True':b.scatter([k+offset],[float(r['mean_difference'])],marker=marker,color=color,s=48,zorder=6)
        a.set_xticks([0,1,3,4],['WT\n0.1 nM','R5A11D\n0.1 nM','WT\n50 nM','R5A11D\n50 nM'])
        b.set_xticks([0,1],['0.1 nM','50 nM']);b.set_xlim(-.2,1.25)
        for ax in [a,b]:ax.axhline(0,color='#555555',linestyle='--',linewidth=.7);ax.grid(axis='y',alpha=.15)
    axs[0,0].set_ylabel('Deposited log2 response estimate\n(ligand versus its control)')
    axs[1,0].set_ylabel('Difference of response estimates\n(R5A11D minus WT)')
    axs[0,0].legend(title='Source block',fontsize=9)
    fig.suptitle('Gorby CD8 source: target responses across two ligand doses',fontsize=15,fontweight='bold')
    fig.text(.5,.935,'GSE146438 | six-day culture context | three author-donor codes; identity crosswalk unresolved',ha='center',fontsize=10)
    fig.text(.5,.025,'Colored dots/lines: source blocks. Black diamonds: mean reported-estimate difference. Gray x: mean positive-pair-ratio difference.\nNo confidence intervals or population tests. Repeated control values differ across source comparisons; common-matrix contrast remains held.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.085,1,.92])
    fig.savefig(run/'gorby_responses.png',dpi=300);fig.savefig(run/'gorby_responses.pdf');plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);main(p.parse_args().run)
