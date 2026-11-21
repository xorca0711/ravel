"""Two fixed paired-modality figure families; first-write SVG cleanup only."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

def save(fig,out,stem):
    fig.savefig(out/(stem+'.png'),dpi=160,facecolor='white')
    path=out/(stem+'.svg');fig.savefig(path,facecolor='white')
    # Part of this prospective generation; never applied to any previous artifact.
    path.write_bytes(('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n').encode())
    plt.close(fig)

def figures(out,rows,targets):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    contrasts=['LGR5_minus_CTRL','KRT20_minus_CTRL'];cases=[('all','pooled'),('all','equal'),('rna_qc','pooled'),('rna_qc','equal')];families=['tss_2kb_union','gene_body']
    lookup={(r['contrast'],r['subset'],r['weighting'],r['region_family'],r['target']):r for r in rows}
    def val(c,s,w,f,t,key):
        value=lookup[(c,s,w,f,t)].get(key)
        return np.nan if value is None else value
    all_values=np.array([r.get(k) if r.get(k) is not None else np.nan for r in rows for k in ['rna_difference','fragment_difference']]);finite=np.abs(all_values[np.isfinite(all_values)]);vmax=max(.1,float(finite.max())) if len(finite) else 1
    fig,axes=plt.subplots(1,2,figsize=(12,5.9),sharex=True)
    for i,(ax,c) in enumerate(zip(axes,contrasts)):
        y=np.arange(len(targets));a=[val(c,'all','pooled','tss_2kb_union',t,'rna_difference') for t in targets];b=[val(c,'all','pooled','tss_2kb_union',t,'fragment_difference') for t in targets]
        ax.barh(y-.18,a,height=.34,color='#bc653f',label='RNA');ax.barh(y+.18,b,height=.34,color='#397fa5',label='TSS-window fragments');ax.axvline(0,color='#555',lw=.8)
        for yy,values in [(y-.18,a),(y+.18,b)]:
            for j,v in enumerate(values):
                if np.isfinite(v):ax.text(v+(vmax*.025 if v>=0 else -vmax*.025),yy[j],f'{v:+.2f}',ha='left' if v>=0 else 'right',va='center',fontsize=9)
                else:ax.text(0,yy[j],'held',ha='center',va='center',fontsize=9)
        ax.set_yticks(y,targets);ax.invert_yaxis();ax.set_xlim(-vmax*1.2,vmax*1.2);ax.set_title('GSE329778 | '+c.replace('_minus_',' − '),weight='bold',fontsize=12);ax.set_xlabel('Post − CTRL: log2(CPM + 1) difference');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.865),ncol=2,fontsize=9,frameon=False)
    fig.suptitle('Four source-selected loci: RNA and common-region fragment changes',fontsize=14,weight='bold',y=.97)
    fig.text(.5,.90,'Primary: paired positive-depth barcodes, pooled summaries, M33 basic-transcript ±2 kb TSS-window unions',ha='center',fontsize=10)
    fig.text(.5,.04,'Each modality uses its own all-RNA or canonical-nuclear-fragment denominator on identical barcodes.\nFinite-library GRCm39 adaptation; shared CTRL, no state attribution or causal regulatory-memory claim.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.80,bottom=.20,left=.08,right=.98,wspace=.27);save(fig,out,'figure_01_paired_primary')
    fig,axes=plt.subplots(2,2,figsize=(14,9));norm=TwoSlopeNorm(vmin=-vmax,vcenter=0,vmax=vmax);cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#ddd')
    for col,c in enumerate(contrasts):
        for row,key in enumerate(['rna_difference','fragment_difference']):
            defs=[('tss_2kb_union',s,w) for s,w in cases] if row==0 else [(f,s,w) for f in families for s,w in cases]
            data=np.array([[val(c,s,w,f,t,key) for f,s,w in defs] for t in targets]);ax=axes[row,col];im=ax.imshow(data,norm=norm,cmap=cmap,aspect='auto');ax.set_yticks(range(len(targets)),targets)
            labels=[('All' if s=='all' else 'RNA QC')+'\n'+w for f,s,w in defs];ax.set_xticks(range(len(defs)),labels,fontsize=9)
            title=('RNA, same paired sets' if row==0 else 'Fragments: TSS windows (left) | gene bodies (right)')+'\n'+c.replace('_minus_',' − ');ax.set_title(title,fontsize=11,weight='bold')
            if row:ax.axvline(3.5,color='black',lw=1.4)
            for y in range(len(targets)):
                for x in range(len(defs)):
                    v=data[y,x];ax.text(x,y,f'{v:+.2f}' if np.isfinite(v) else 'held',ha='center',va='center',fontsize=9,color='white' if np.isfinite(v) and abs(v)>.65*vmax else 'black')
    fig.suptitle('Region, barcode-QC and depth-weighting sensitivity',fontsize=15,weight='bold',y=.98)
    fig.subplots_adjust(left=.06,right=.91,top=.86,bottom=.15,hspace=.48,wspace=.22);cax=fig.add_axes([.93,.18,.015,.65]);fig.colorbar(im,cax=cax,label='Post − CTRL: log2(CPM + 1) difference')
    fig.text(.5,.04,'Equal = mean barcode CPM, then log2(mean CPM + 1). RNA appears once because region definitions do not change RNA.\nRNA-QC uses the prior frozen rule. Region overlap is not promoter validation; signs and small changes alone do not establish biological meaning.',ha='center',fontsize=9)
    save(fig,out,'figure_02_paired_sensitivity')
