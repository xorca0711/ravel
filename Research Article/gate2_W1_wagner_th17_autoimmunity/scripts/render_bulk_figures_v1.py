"""Layout-only rendering from frozen R3 tables; no biological calculation."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from bulk_paired_descriptive_v2 import SERIES, GENES, DISPLAY, COLORS, GROUPS

def make_figures(data,selected,pca,output):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.titlesize':11,'axes.labelsize':9,'svg.fonttype':'none','pdf.fonttype':42})
    figures=[]
    fig,axes=plt.subplots(1,2,figsize=(11.8,5.5))
    fig.subplots_adjust(top=.77,bottom=.29,wspace=.32)
    fig.suptitle('Bulk RNA context after source-library qualification',x=.06,ha='left',y=.98,fontsize=15,fontweight='bold')
    fig.text(.06,.915,'68-hour in-vitro mouse CD4 T-cell cultures | untreated control versus DFMO\nPCA of all nonconstant deposited genes on log₂(deposited-gene CPM + 1)',fontsize=10,va='top')
    for ax,series,letter in zip(axes,SERIES,'AB'):
        d=pca[pca.series==series]
        for (_,cell),pair in d.groupby(['animal_id','cell_type'],sort=False):
            if len(pair)!=2:raise ValueError('PCA pair incomplete')
            ax.plot(pair.PC1,pair.PC2,color='#999999',linewidth=.6,zorder=1,alpha=.6)
        for row in d.itertuples():
            color=COLORS[row.cell_type]
            ax.scatter(row.PC1,row.PC2,s=44,marker='o' if row.genotype=='WT' else '^',
                       facecolor=color if row.treatment=='DFMO' else 'white',edgecolor=color,linewidth=1.2,zorder=2)
        exp=data[series]['explained']
        ax.set(xlabel=f'PC1 ({exp[0]*100:.1f}% variance)',ylabel=f'PC2 ({exp[1]*100:.1f}% variance)')
        ax.set_title(f'{letter}   {series}\n'+('3 WT animals; 18 libraries' if series==SERIES[0] else '4 WT + 3 KO animals; 28 libraries'),loc='left')
        ax.margins(.14)
    handles=[Line2D([],[],color=c,marker='o',linestyle='',label=k) for k,c in COLORS.items()]
    handles += [Line2D([],[],color='#555555',marker='o',markerfacecolor='white',linestyle='',label='Control (open)'),
                Line2D([],[],color='#555555',marker='o',linestyle='',label='DFMO (filled)'),
                Line2D([],[],color='#555555',marker='^',linestyle='',label='JMJD3 KO (triangle)')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.073),ncol=3,frameon=False)
    fig.text(.06,.018,'Lines connect paired cultures from the same source animal. Studies are analyzed separately; axes are not shared. No DEG-selected PCA or fate inference.',fontsize=8)
    figures.append(('figure_4_bulk_context',fig))

    fig,axes=plt.subplots(3,4,figsize=(14,10.8))
    fig.subplots_adjust(left=.135,right=.98,top=.855,bottom=.1,wspace=.23,hspace=.47)
    fig.suptitle('Prespecified genes: paired response to DFMO',x=.035,ha='left',y=.985,fontsize=16,fontweight='bold')
    fig.text(.035,.942,'Each circle is one source animal’s DFMO − control difference; black diamonds are unweighted means.\nA = GSE162300 (3 WT); B = GSE162382 (4 WT, 3 JMJD3 KO). Lineages and genotypes remain separate.\nEndpoint: Δlog₂(deposited-gene CPM + 1), 68-hour bulk RNA. No p values, DEG calls or biological importance cutoff.',fontsize=10,va='top')
    labels=[x[0]+(' (n=4)' if x[1]==SERIES[1] and x[3]=='WT' else ' (n=3)') for x in GROUPS]
    for index,(ax,gene) in enumerate(zip(axes.flat,GENES)):
        part=selected[selected.gene==gene]
        ax.axvline(0,color='#9CA3AF',linewidth=.7)
        ax.axhline(2.5,color='#D6D6D6',linewidth=.8)
        for row,(label,series,cell,genotype) in enumerate(GROUPS):
            values=part[(part.series==series)&(part.cell_type==cell)&(part.genotype==genotype)].sort_values('animal_id').delta.to_numpy()
            ax.scatter(values,row+np.linspace(-.13,.13,len(values)),s=23,color=COLORS[cell],alpha=.82,zorder=2)
            ax.scatter([values.mean()],[row],s=29,marker='D',color='#111111',zorder=3)
        ax.set_yticks(range(7),labels if index%4==0 else ['']*7)
        ax.set_ylim(6.6,-.6);ax.tick_params(axis='y',length=0,labelsize=8)
        ax.set_title(f'{chr(65+index)}  {DISPLAY[gene]}',loc='left',fontstyle='italic',fontweight='bold')
        ax.set_xlabel('Δlog₂(CPM + 1)',fontsize=8);ax.tick_params(axis='x',labelsize=8)
        ax.margins(x=.18)
    fig.text(.035,.03,'Positive: greater normalized abundance after DFMO. Negative: lower after DFMO. Panel x-axis ranges differ.\nCounts from two technical runs are summed in A. Bulk abundance cannot separate within-cell change from selection, survival or mixture changes.',fontsize=9)
    figures.append(('figure_5_bulk_paired_genes',fig))
    with PdfPages(output/'Wagner_R3_initial_figures.pdf') as pdf:
        for name,fig in figures:
            for ext in ['png','pdf','svg']:fig.savefig(output/f'{name}.{ext}',dpi=300,facecolor='white')
            pdf.savefig(fig,facecolor='white');plt.close(fig)

def main(source,output):
    results=json.loads((source/'results.json').read_text())
    selected=pd.read_csv(source/'prespecified_gene_animal_changes.tsv',sep='\t',float_precision='round_trip')
    pca=pd.read_csv(source/'pca_coordinates.tsv',sep='\t',float_precision='round_trip')
    if len(selected)!=276 or len(pca)!=46:raise ValueError('Frozen figure-table size changed')
    make_figures(results['series'],selected,pca,output)
    (output/'CAPTIONS.md').write_bytes((source/'CAPTIONS.md').read_bytes())
    report={'source':'wg_bulk_paired_descriptive_v2','scope':'Layout-only render: increase Figure 4 bottom margin to separate x-axis label and legend; Figure 5 design unchanged.',
            'selected_animal_change_rows':len(selected),'pca_library_rows':len(pca),'numerical_analysis_rerun':False,
            'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.suffix in ['.png','.pdf','.svg']}}
    (output/'figure_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='files'}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.source,a.output)
