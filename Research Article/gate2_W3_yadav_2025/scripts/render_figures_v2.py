"""Display-only v2 figures from immutable functional and QC tables."""
import argparse,csv,json,sys,textwrap
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter,LogLocator,LogFormatterMathtext
ROOT=Path(__file__).resolve().parents[3];ART=ROOT/'Research Article/gate2_W3_yadav_2025';RUNS=ROOT/'analysis/research/runs'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8')))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output;out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    for job in range(1,6):
        spec=json.loads((ART/f'config/functional_f{job}_spec_v1.json').read_text())
        src=RUNS/f'Yd1_functional_f{job}_v1';obs=read(src/'observations.csv');summaries=read(src/'group_summaries.csv');contrasts=read(src/'contrasts.csv')
        lookup={(r['panel'],r['donor'],r['condition']):r for r in summaries}
        n=len(spec['panels']);nr=(n+1)//2
        fig,axes=plt.subplots(nr,2,figsize=(12,4.4*nr+1.3),squeeze=False);colors=['#226B96','#C65E27']
        for ax,panel in zip(axes.flat,spec['panels']):
            ids=list(dict.fromkeys(g['id'] for g in panel['groups']));donors=list(dict.fromkeys(g['donor'] for g in panel['groups']))
            labels={g['id']:g['label'] for g in panel['groups']}
            if job==2:
                for key in labels:
                    labels[key]=labels[key].replace('Fib alone','Fib\nalone').replace('Coculture','Co-\nculture').replace('Tocilizumab','Co +\ntocilizumab').replace('P2RX4\ninhibitor','Co + P2RX4\ninhibitor')
            largest=0
            for di,donor in enumerate(donors):
                offset=(di-(len(donors)-1)/2)*.26
                for i,gid in enumerate(ids):
                    row=lookup[(panel['id'],donor,gid)]
                    values=[float(r['value']) for r in obs if r['panel']==panel['id'] and r['donor']==donor and r['condition']==gid and r['status']=='observed']
                    assert len(values)==int(row['n_observed']);largest=max(largest,max(values))
                    x=i+offset
                    ax.scatter(x+np.linspace(-.055,.055,len(values)),values,s=27,color=colors[di],edgecolor='white',linewidth=.45,label=donor if i==0 and donor!='source' else None,zorder=3)
                    ax.hlines(float(row['mean']),x-.12,x+.12,color=colors[di],linewidth=2.6,zorder=4)
            title=panel['title']
            if spec.get('welch'):
                c=next(r for r in contrasts if r['panel']==panel['id'])
                title+=f"\nDifference: {float(c['mean_difference']):.3g}; 95% interval [{float(c['ci95_lower']):.3g}, {float(c['ci95_upper']):.3g}]"
            if panel['id']=='5D':title+='\nDonor 1 / Fib alone: 2 supplied values; D2 blank'
            ax.set_title(title,loc='left',fontsize=10,pad=12)
            ax.set_xticks(range(len(ids)),[labels[k] for k in ids],fontsize=9);ax.set_ylabel(panel['unit'])
            ax.set_xlim(-.5,len(ids)-.5);ax.set_ylim(-largest*.04,largest*1.18);ax.grid(axis='y',alpha=.17)
            if len(donors)>1:ax.legend(frameon=False,fontsize=8,loc='upper left')
        for ax in list(axes.flat)[n:]:ax.axis('off')
        title=spec['title']
        if job==2:title='Human cocultures: source values by donor combination'
        if job==4:title='Mouse cultures: rescue, genotype and distinct endpoints'
        fig.suptitle(title,x=.06,ha='left',fontsize=14,fontweight='bold')
        foot='\n'.join(textwrap.wrap(spec['footnote'],125))
        foot+='\nSource: Yadav et al., JCI 2025;135:e188734, official Supporting Data Values. Exposed source reconstruction.'
        if job==2:foot+='\nFig. 6G is a separate endpoint; overlap of its donor combinations with Fig. 5D-F is unknown.'
        fig.text(.06,.015,foot,fontsize=8)
        fig.tight_layout(rect=(.015,.11,.99,.92),h_pad=3,w_pad=3)
        fig.savefig(out/f'f{job}.png',dpi=200,bbox_inches='tight');fig.savefig(out/f'f{job}.pdf',bbox_inches='tight');plt.close(fig)
    cells=read(RUNS/'Yd1_count_integrity_v1/cell_qc.csv')
    libraries=read(RUNS/'Yd1_count_integrity_v1/library_integrity.csv')
    fig,axes=plt.subplots(2,3,figsize=(12,8))
    for ax,s in zip(axes.flat,libraries):
        rows=[r for r in cells if r['gsm']==s['gsm']]
        assert len(rows)==int(s['barcodes'])
        x=[int(r['total_counts']) for r in rows];y=[int(r['detected_genes']) for r in rows];c=[float(r['mitochondrial_percent']) for r in rows]
        sc=ax.scatter(x,y,c=c,s=3,cmap='viridis',vmin=0,vmax=10,rasterized=True)
        ax.set_xscale('log');ax.set_yscale('log')
        for axis in [ax.xaxis,ax.yaxis]:
            axis.set_major_locator(LogLocator(base=10,subs=(1.0,),numticks=5));axis.set_major_formatter(LogFormatterMathtext(base=10));axis.set_minor_formatter(NullFormatter())
        ax.set_title(s['title'],fontsize=11);ax.set_xlabel('Total deposited counts');ax.set_ylabel('Detected genes')
    fig.subplots_adjust(left=.075,right=.88,top=.86,bottom=.18,wspace=.46,hspace=.6)
    cax=fig.add_axes([.92,.24,.015,.56]);fig.colorbar(sc,cax=cax,label='Mitochondrial counts (%)',extend='max')
    fig.suptitle('Six libraries: technical QC before annotation',x=.075,ha='left',fontsize=14)
    fig.text(.075,.035,'All deposited barcodes are retained. Log axes; colors saturate at 10% for display only.\nNo values, QC thresholds or annotations changed. Source: GSE242510; cells are not independent preparations.',fontsize=8)
    fig.savefig(out/'qc.png',dpi=200,bbox_inches='tight');fig.savefig(out/'qc.pdf',bbox_inches='tight');plt.close(fig)
    (out/'runtime.json').write_text(json.dumps(dict(python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,display_only=True,
        supersedes='Only the display of F1-F5 figure.png/pdf and count-integrity qc.png/pdf; all v1 outputs and numerical tables remain immutable.'),indent=2)+'\n',encoding='utf-8')
    print('Six display-only figure pairs written from frozen tables; no biological analysis rerun.')
if __name__=='__main__':main()
