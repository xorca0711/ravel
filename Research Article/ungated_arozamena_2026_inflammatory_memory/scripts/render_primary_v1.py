"""Render-only spacing correction from immutable v2 paired contrasts."""
import argparse,csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plot_accessibility_v2 import save

ROOT=Path(__file__).resolve().parents[3]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);out=Path(parser.parse_args().output).resolve()
    assert out.parent==ROOT/'analysis/research/runs' and out.is_dir() and all(p.name in ['receipt.json','stdout.log','stderr.log'] for p in out.iterdir())
    source=ROOT/'analysis/research/runs/arz1_accessibility_description_v2/paired_contrasts.csv'
    with source.open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==128 and all(r['status']=='defined' for r in rows)
    targets=['Cd74','Tiam1','Cd83','Ciita'];contrasts=['LGR5_minus_CTRL','KRT20_minus_CTRL']
    selected=[r for r in rows if r['count_definition']=='strand_records' and r['subset']=='all' and r['weighting']=='pooled' and r['region_family']=='tss_2kb_union']
    lookup={(r['contrast'],r['target']):r for r in selected};assert len(selected)==len(lookup)==8
    # Preserve original plotted values, signs, labels and axis extent.
    vmax=max(.1,max(abs(float(r[k])) for r in rows for k in ['rna_difference','fragment_difference']))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,6.5),sharex=True)
    for ax,c in zip(axes,contrasts):
        y=np.arange(len(targets));a=[float(lookup[(c,t)]['rna_difference']) for t in targets];b=[float(lookup[(c,t)]['fragment_difference']) for t in targets]
        ax.barh(y-.18,a,height=.34,color='#bc653f',label='RNA');ax.barh(y+.18,b,height=.34,color='#397fa5',label='TSS-window source records');ax.axvline(0,color='#555',lw=.8)
        for yy,values in [(y-.18,a),(y+.18,b)]:
            for j,v in enumerate(values):ax.text(v+(vmax*.025 if v>=0 else -vmax*.025),yy[j],f'{v:+.2f}',ha='left' if v>=0 else 'right',va='center',fontsize=9)
        ax.set_yticks(y,targets);ax.invert_yaxis();ax.set_xlim(-vmax*1.2,vmax*1.2);ax.set_title('GSE329778 | '+c.replace('_minus_',' − '),weight='bold',fontsize=12);ax.set_xlabel('Post − CTRL: log2(CPM + 1) difference');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.855),ncol=2,fontsize=9,frameon=False)
    fig.suptitle('Four source-selected loci: paired RNA and fragment-record changes',fontsize=14,weight='bold',y=.97)
    fig.text(.5,.90,'Primary: paired positive depths, pooled summaries, M33 basic-transcript ±2 kb TSS-window unions',ha='center',fontsize=10)
    fig.text(.5,.035,'Source records retain opposite strands; readSupport is not a weight. Each modality has its own total-depth denominator.\nFinite libraries, shared CTRL; overlap counts are not ARC peak cut-site counts or a causal regulatory-memory measure.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.72,bottom=.20,left=.08,right=.98,wspace=.27)
    save(fig,out,'figure_01_paired_primary_corrected')
    print(json.dumps(dict(render_only=True,source=source.relative_to(ROOT).as_posix(),source_paired_rows=len(rows),primary_cases=len(selected),changed_measurements=False,changed_layout='Taller canvas and dedicated legend band; axes top moved to 0.72')),flush=True)

if __name__=='__main__':main()
