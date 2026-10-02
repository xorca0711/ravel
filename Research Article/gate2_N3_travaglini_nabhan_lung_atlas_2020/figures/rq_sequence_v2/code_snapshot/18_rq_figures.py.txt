"""Render three RQ diagnostics and append them to the existing Nb4 PDF atlas."""
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfWriter, PdfReader
from common import PACKAGE, new_run, finish_record, write_json, sha256

COLORS={'10x':'#2A708E','SS2':'#CF8044','Madissoon cell':'#4B9370','Madissoon nucleus':'#8979AA','Murthy 10x':'#A2566D'}
ASSAYS=['10x','SS2','Madissoon cell','Madissoon nucleus']


def main():
    if not (PACKAGE/'runs/rq2_myrf_v1/run_record.json').exists():
        raise ValueError('Sequential analyses are not complete')
    out=new_run(PACKAGE/'figures/rq_sequence_v2'); inputs={}
    def table(rel):
        p=PACKAGE/rel;inputs[rel]=sha256(p);return pd.read_csv(p,sep='\t')
    def save(fig,name):
        fig.savefig(out/(name+'.png'),dpi=300,facecolor='white')
        fig.savefig(out/(name+'.svg'),facecolor='white')
        fig.savefig(out/(name+'.pdf'),facecolor='white')
        plt.close(fig)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
        'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
    comp=table('runs/rq1_composition_v1/donor_accounting.tsv').query('cell_floor == 20')
    fig,axes=plt.subplots(2,2,figsize=(11,7),layout='constrained')
    for panel,(ax,assay) in enumerate(zip(axes.ravel(),ASSAYS)):
        df=comp[comp.assay==assay].sort_values('donor_id')
        for y,row in enumerate(df.itertuples()):
            ax.plot([row.observed_cell_CPM,row.equal_subtype_cell_CPM],[y,y],color='#AAAAAA',lw=1.7)
            ax.scatter(row.observed_cell_CPM,y,color=COLORS[assay],s=58,zorder=3,label='Captured mixture' if y==0 else None)
            ax.scatter(row.equal_subtype_cell_CPM,y,facecolors='white',edgecolors='#D38B35',linewidths=1.8,s=64,zorder=3,label='Equal-subtype reference' if y==0 else None)
            ax.annotate(f'{row.captured_adventitial_fraction:.0%} adventitial',(row.observed_cell_CPM,y),xytext=(0,10),textcoords='offset points',ha='center',fontsize=8,color='#666666')
        ax.set_yticks(range(len(df)),df.donor_id);ax.set_ylim(-.5,len(df)-.2)
        ax.set_title(assay);ax.set_xlabel('C3 mean per-cell CPM');ax.grid(axis='x',alpha=.15)
        ax.text(-.12,1.06,chr(97+panel),transform=ax.transAxes,fontweight='bold',fontsize=13)
        if panel==0:ax.legend(fontsize=8,loc='lower right')
    save(fig,'13_composition_accounting')
    effects=table('runs/rq1b_endpoint_v1/donor_effects.tsv').query('cell_floor == 20 or (cell_floor == 10 and assay == \"10x\" and donor_id == \"P2\")')
    panels=table('runs/rq1b_endpoint_v1/panel_sensitivity.tsv').query('cell_floor == 20 or (cell_floor == 10 and assay == \"10x\" and donor_id == \"P2\")')
    fig,(ax,hax)=plt.subplots(1,2,figsize=(13,6),gridspec_kw={'width_ratios':[1,1.45]},layout='constrained')
    for assay in ASSAYS:
        for row in panels[(panels.assay==assay)&(panels.omitted_gene=='none')].itertuples():
            sensitivity=panels[(panels.assay==assay)&(panels.donor_id==row.donor_id)&(panels.omitted_gene!='none')].panel_delta.dropna()
            if not np.isfinite(row.panel_delta):continue
            if len(sensitivity):ax.vlines(row.C3_delta,sensitivity.min(),sensitivity.max(),color=COLORS[assay],alpha=.6,lw=2)
            ax.scatter(row.C3_delta,row.panel_delta,color=COLORS[assay],s=48,marker='^' if row.cell_floor==10 else 'o')
            offset={('10x','P3'):(6,11),('Madissoon cell','A26'):(-25,-12),('Madissoon cell','A44'):(5,-10)}.get((assay,row.donor_id),(4,4))
            ax.annotate(row.donor_id+('†' if row.cell_floor==10 else ''),(row.C3_delta,row.panel_delta),xytext=offset,textcoords='offset points',fontsize=8)
    for assay in ASSAYS:ax.scatter([],[],color=COLORS[assay],label=assay)
    ax.axhline(0,color='#777777',lw=.8);ax.axvline(0,color='#777777',lw=.8)
    ax.set_xlabel('C3: alveolar − adventitial Δ log2(CPM + 1)');ax.set_ylabel('Fixed panel: mean Δ log2(CPM + 1)')
    ax.text(.02,.98,'† P2: lower cell-floor sensitivity',transform=ax.transAxes,va='top',fontsize=8,color='#666666')
    ax.set_title('Endpoint direction and gene omission');ax.legend(fontsize=8,loc='best')
    genes=['C3','CCL2','CXCL1','CXCL2','CXCL3','CXCL6','CXCL8','CXCL12']
    wide=effects.pivot(index=['assay','donor_id'],columns='gene',values='delta_log2CPM').reindex(columns=genes)
    index=[idx for assay in ASSAYS for idx in wide.index if idx[0]==assay];wide=wide.loc[index]
    vmax=max(abs(wide.to_numpy()[np.isfinite(wide.to_numpy())]));cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#EEEEEE')
    im=hax.imshow(wide.to_numpy(),cmap=cmap,vmin=-vmax,vmax=vmax,aspect='auto')
    hax.set_xticks(range(len(genes)),genes,rotation=45,ha='right')
    hax.set_yticks(range(len(wide)),[a+' · '+d+('†' if a=='10x' and d=='P2' else '') for a,d in wide.index],fontsize=8)
    hax.set_title('Individual endpoints by donor')
    fig.colorbar(im,ax=hax,shrink=.7,label='Δ log2(CPM + 1)')
    for label,axis in zip('ab',[ax,hax]):axis.text(-.10,1.04,label,transform=axis.transAxes,fontweight='bold',fontsize=13)
    save(fig,'14_endpoint_separation')
    myrf=table('runs/rq2_myrf_v1/donor_effects.tsv').query('cell_floor == 20 and gene == "MYRF"')
    coverage=table('runs/rq2_myrf_v1/coverage.tsv')
    fig,axes=plt.subplots(1,2,figsize=(12,6),sharey=True,layout='constrained')
    keys=[]
    for assay in ['10x','SS2','Murthy 10x']:
        keys.extend((assay,d) for d in sorted(coverage[coverage.assay==assay].donor_id.unique()))
    for panel,(ax,comparator) in enumerate(zip(axes,['Alveolar Epithelial Type 2','Mesothelial'])):
        selected=myrf[myrf.comparator==comparator].set_index(['assay','donor_id'])
        for y,key in enumerate(keys):
            if key in selected.index:
                ax.scatter(selected.loc[key,'delta_log2CPM'],y,color=COLORS[key[0]],s=55)
            else:
                ax.text(3.5,y,'coverage not met',fontsize=8,color='#999999',va='center',ha='center')
        ax.set_yticks(range(len(keys)),[a+' · '+d for a,d in keys],fontsize=9)
        ax.set_xlim(-.5,8.4);ax.set_ylim(-.6,len(keys)-.4)
        ax.axvline(0,color='#777777',lw=.8)
        ax.set_xlabel('MYRF Δ log2(CPM + 1)')
        ax.set_title('AT1 versus '+('AT2' if panel==0 else 'mesothelium'))
        ax.grid(axis='x',alpha=.15);ax.text(-.12,1.05,chr(97+panel),transform=ax.transAxes,fontweight='bold',fontsize=13)
    save(fig,'15_myrf_reference')
    original=PACKAGE/'figures/gallery_v2/Nb4_figure_atlas.pdf'
    inputs[original.relative_to(PACKAGE).as_posix()]=sha256(original)
    writer=PdfWriter();writer.append(original)
    for name in ['13_composition_accounting','14_endpoint_separation','15_myrf_reference']:
        writer.append(out/(name+'.pdf'))
    writer.write(out/'Nb4_complete_atlas.pdf')
    pages=len(PdfReader(out/'Nb4_complete_atlas.pdf').pages)
    if pages!=15:raise ValueError('Expected 15 pages')
    write_json(out/'figure_inputs.json',inputs)
    finish_record(out,{'schema':'Nb4-rq-figures/v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'status':'three RQ figures rendered; complete atlas assembled','pages':pages})
    print('Rendered figures 13–15 and the complete 15-page atlas.')


if __name__=='__main__':main()
