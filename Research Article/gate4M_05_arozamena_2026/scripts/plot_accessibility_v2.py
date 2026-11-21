"""Primary record-count comparison plus all prespecified sensitivity axes."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

def save(fig,out,stem):
    fig.savefig(out/(stem+'.png'),dpi=160,facecolor='white')
    path=out/(stem+'.svg');fig.savefig(path,facecolor='white')
    # First-generation cleanup only; previously frozen images remain untouched.
    path.write_bytes(('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n').encode())
    plt.close(fig)

def figures(out,rows,targets):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    contrasts=['LGR5_minus_CTRL','KRT20_minus_CTRL'];cases=[('all','pooled'),('all','equal'),('rna_qc','pooled'),('rna_qc','equal')];families=['tss_2kb_union','gene_body']
    lookup={(r['count_definition'],r['contrast'],r['subset'],r['weighting'],r['region_family'],r['target']):r for r in rows}
    def val(d,c,s,w,f,t,key):
        value=lookup[(d,c,s,w,f,t)].get(key)
        return np.nan if value is None else value
    def extent(values,minimum):
        finite=np.abs(np.asarray(values));finite=finite[np.isfinite(finite)]
        return max(minimum,float(finite.max())) if len(finite) else 1
    vmax=extent([r.get(k,np.nan) if r.get(k) is not None else np.nan for r in rows for k in ['rna_difference','fragment_difference']],.1)
    fig,axes=plt.subplots(1,2,figsize=(12,5.9),sharex=True)
    for ax,c in zip(axes,contrasts):
        y=np.arange(len(targets));a=[val('strand_records',c,'all','pooled','tss_2kb_union',t,'rna_difference') for t in targets];b=[val('strand_records',c,'all','pooled','tss_2kb_union',t,'fragment_difference') for t in targets]
        ax.barh(y-.18,a,height=.34,color='#bc653f',label='RNA');ax.barh(y+.18,b,height=.34,color='#397fa5',label='TSS-window source records');ax.axvline(0,color='#555',lw=.8)
        for yy,values in [(y-.18,a),(y+.18,b)]:
            for j,v in enumerate(values):
                if np.isfinite(v):ax.text(v+(vmax*.025 if v>=0 else -vmax*.025),yy[j],f'{v:+.2f}',ha='left' if v>=0 else 'right',va='center',fontsize=9)
                else:ax.text(0,yy[j],'held',ha='center',va='center',fontsize=9)
        ax.set_yticks(y,targets);ax.invert_yaxis();ax.set_xlim(-vmax*1.2,vmax*1.2);ax.set_title('GSE329778 | '+c.replace('_minus_',' − '),weight='bold',fontsize=12);ax.set_xlabel('Post − CTRL: log2(CPM + 1) difference');ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.865),ncol=2,fontsize=9,frameon=False)
    fig.suptitle('Four source-selected loci: paired RNA and fragment-record changes',fontsize=14,weight='bold',y=.97)
    fig.text(.5,.90,'Primary: paired positive depths, pooled summaries, M33 basic-transcript ±2 kb TSS-window unions',ha='center',fontsize=10)
    fig.text(.5,.04,'Source records retain opposite strands; readSupport is not a weight. Each modality has its own total-depth denominator.\nFinite libraries, shared CTRL; overlap counts are not ARC peak cut-site counts or a causal regulatory-memory measure.',ha='center',fontsize=9)
    fig.subplots_adjust(top=.80,bottom=.20,left=.08,right=.98,wspace=.27);save(fig,out,'figure_01_paired_primary')
    defs=[(f,s,w) for f in families for s,w in cases]
    delta_values=[val('coordinate_groups',c,s,w,f,t,'fragment_difference')-val('strand_records',c,s,w,f,t,'fragment_difference') for c in contrasts for f,s,w in defs for t in targets]
    dmax=extent(delta_values,1e-5);norm=TwoSlopeNorm(vmin=-vmax,vcenter=0,vmax=vmax);dnorm=TwoSlopeNorm(vmin=-dmax,vcenter=0,vmax=dmax);cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#ddd')
    fig,axes=plt.subplots(3,2,figsize=(14,12.5))
    for col,c in enumerate(contrasts):
        for row in range(3):
            definitions=[('tss_2kb_union',s,w) for s,w in cases] if row==0 else defs
            key='rna_difference' if row==0 else 'fragment_difference'
            data=np.array([[val('strand_records',c,s,w,f,t,key) if row<2 else val('coordinate_groups',c,s,w,f,t,key)-val('strand_records',c,s,w,f,t,key) for f,s,w in definitions] for t in targets])
            ax=axes[row,col];im=ax.imshow(data,norm=dnorm if row==2 else norm,cmap=cmap,aspect='auto');ax.set_yticks(range(len(targets)),targets)
            labels=[('All' if s=='all' else 'RNA QC')+'\n'+w for f,s,w in definitions];ax.set_xticks(range(len(definitions)),labels,fontsize=9)
            title=['RNA: same paired sets; shown once','Primary source records: TSS (left) | body (right)','Grouping sensitivity: grouped − record differences'][row]+'\n'+c.replace('_minus_',' − ');ax.set_title(title,fontsize=11,weight='bold')
            if row:ax.axvline(3.5,color='black',lw=1.4)
            for y in range(len(targets)):
                for x in range(len(definitions)):
                    v=data[y,x];label=(f'{v:+.4f}' if row==2 else f'{v:+.2f}') if np.isfinite(v) else 'held';ax.text(x,y,label,ha='center',va='center',fontsize=8 if row==2 else 9,color='white' if np.isfinite(v) and abs(v)>.65*(dmax if row==2 else vmax) else 'black')
            if row==1:primary_image=im
            if row==2:delta_image=im
    fig.suptitle('Region, RNA-QC, weighting and counting-definition sensitivity',fontsize=15,weight='bold',y=.98)
    fig.subplots_adjust(left=.06,right=.90,top=.90,bottom=.14,hspace=.55,wspace=.22)
    cax=fig.add_axes([.925,.43,.013,.43]);fig.colorbar(primary_image,cax=cax,label='Post − CTRL: log2(CPM + 1) difference')
    cax=fig.add_axes([.925,.16,.013,.20]);fig.colorbar(delta_image,cax=cax,label='Change in difference (separate scale)')
    fig.text(.5,.035,'Equal = mean barcode CPM, then log2(mean CPM + 1). RNA is reused across region/count definitions, not replicated.\nGrouping counts each coordinate/barcode group once in both locus numerator and total-depth denominator.\nNeither count definition certifies physical molecules. All 128 paired cases and 64 grouping deltas are retained.',ha='center',fontsize=9)
    save(fig,out,'figure_02_paired_sensitivity')
