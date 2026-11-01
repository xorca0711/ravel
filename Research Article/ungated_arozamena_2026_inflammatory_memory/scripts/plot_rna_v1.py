"""Two prespecified figure families from saved finite-library RNA contrasts."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

def figures(out,panel,targets,contrasts,cases):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    labels=['GSE302685 | Lgr5-associated','GSE302687 | Krt20-associated','GSE329778 | LGR5','GSE329778 | KRT20']
    lookup={(r['contrast'],r['subset'],r['weighting'],r['target']):float(r['difference_log2_cpm1']) if r['difference_log2_cpm1']!='' else np.nan for r in panel}
    data=np.array([[[lookup[(c,s,w,t)] for s,w in cases] for t in targets] for c,_,_ in contrasts]);finite=np.abs(data[np.isfinite(data)]);limit=max(0.1,float(finite.max())*1.12) if finite.size else 1
    fig,axes=plt.subplots(2,2,figsize=(12,9),sharex=True)
    for i,ax in enumerate(axes.flat):
        values=data[i,:,0];y=np.arange(len(targets));ax.barh(y,values,color=['#bf5b38' if x>=0 else '#367e9e' for x in values],height=.67);ax.axvline(0,color='#555555',lw=.8)
        ax.set_yticks(y,targets);ax.invert_yaxis();ax.set_xlim(-limit,limit);ax.set_title(labels[i],loc='left',weight='bold',fontsize=11)
        ax.set_xlabel('Post-injury minus control: log2(CPM + 1) difference')
        for j,v in enumerate(values):
            if np.isfinite(v):ax.text(v+(limit*.025 if v>=0 else -limit*.025),j,f'{v:+.2f}',va='center',ha='left' if v>=0 else 'right',fontsize=9)
            else:ax.text(0,j,'held',va='center',ha='center')
        ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    fig.suptitle('Selected inflammatory RNA targets: four separate deposited contrasts',fontsize=15,weight='bold',y=.98)
    fig.text(.5,.935,'Primary: all deposited positive-RNA barcodes; pooled CPM over all source RNA genes',ha='center',fontsize=11)
    fig.text(.5,.025,'Finite-library descriptions; no population inference or state attribution. GSE329778 contrasts reuse CTRL.\nA transformed-expression difference is not an unqualified fold change; source sorting/genotype disagreements remain.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.88,bottom=.13,hspace=.40,wspace=.25)
    for ext in ['png','svg']:fig.savefig(out/('figure_01_primary.'+ext),dpi=160,facecolor='white')
    plt.close(fig)
    fig,axes=plt.subplots(1,4,figsize=(14,6.9),sharey=True);vmax=max(float(finite.max()),.1) if finite.size else 1
    norm=TwoSlopeNorm(vmin=-vmax,vcenter=0,vmax=vmax);cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#dddddd')
    for i,ax in enumerate(axes):
        im=ax.imshow(data[i],cmap=cmap,norm=norm,aspect='auto');ax.set_title(labels[i].replace(' | ','\n'),fontsize=11,weight='bold')
        ax.set_xticks(range(4),['All\npooled','All\nequal','RNA QC\npooled','RNA QC\nequal'],fontsize=9);ax.set_yticks(range(len(targets)),targets)
        for y in range(len(targets)):
            for x in range(4):
                v=data[i,y,x];ax.text(x,y,f'{v:+.2f}' if np.isfinite(v) else 'held',ha='center',va='center',fontsize=9,color='white' if np.isfinite(v) and abs(v)>.65*vmax else 'black')
    fig.suptitle('Weighting and RNA-only QC sensitivity of the same eight targets',fontsize=15,weight='bold',y=.98)
    fig.subplots_adjust(left=.07,right=.91,top=.84,bottom=.23,wspace=.12);cax=fig.add_axes([.93,.25,.015,.56]);fig.colorbar(im,cax=cax,label='Post − control: log2(CPM + 1) difference')
    fig.text(.5,.10,'All-source RNA denominators in every case. Equal = mean barcode CPM, then log2(mean CPM + 1).\nRNA QC: 200–2500 detected genes, RNA counts ≥500, mt- fraction ≤0.40; this omits the author’s ATAC QC.\nSame deposited libraries and reused CTRL; these cases are sensitivity checks, not independent replications.',ha='center',fontsize=10)
    for ext in ['png','svg']:fig.savefig(out/('figure_02_sensitivity.'+ext),dpi=160,facecolor='white')
    plt.close(fig)
