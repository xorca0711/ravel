"""Biological extension figures, using verified fixed outputs without refitting."""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import TwoSlopeNorm
from matplotlib.font_manager import FontProperties

AGE={3:'#0072B2',18:'#009E73',24:'#D55E00'}
GENES=['Cdkn2a','Cdkn1a','Lmnb1','Il1b']
TERMS=['composition','within_type','interaction','animal_covariance','difference']
TERM_LABELS=['Composition','Within type','Interaction','Animal\ncovariance','Total']
TISSUES=['Thymus','Spleen','Marrow']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})

def panel(ax,letter,title):
    ax.set_title(title,loc='left',pad=15)
    ax.text(-.15,1.12,letter,transform=ax.transAxes,weight='bold',fontsize=12)

def footer(fig,text):
    w,h=fig.get_size_inches();fig.canvas.draw();r=fig.canvas.get_renderer();font=FontProperties(family='DejaVu Sans',size=9)
    lines=[];line=''
    for word in text.split():
        new=(line+' '+word).strip()
        if line and r.get_text_width_height_descent(new,font,False)[0]>.90*w*fig.dpi:lines.append(line);line=word
        else:line=new
    if line:lines.append(line)
    bottom=min(ax.get_tightbbox(r).y0 for ax in fig.axes)/fig.dpi
    extra=max(0,len(lines)*9*1.3/72+.32-bottom)
    if extra:
        positions=[(ax,ax.get_position().frozen()) for ax in fig.axes];fig.set_size_inches(w,h+extra)
        for ax,pos in positions:ax.set_position([pos.x0,(pos.y0*h+extra)/(h+extra),pos.width,pos.height*h/(h+extra)])
    artist=fig.text(.05,.12/(h+extra),'\n'.join(lines),fontsize=9,ha='left',va='bottom',linespacing=1.3)
    fig.canvas.draw();r=fig.canvas.get_renderer();b=artist.get_window_extent(r)
    qa={'caption_below_panels':bool(b.y1<min(ax.get_tightbbox(r).y0 for ax in fig.axes)),'inside_canvas':bool(b.x0>=0 and b.x1<=w*fig.dpi and b.y0>=0),'lines':len(lines),'words':len(text.split()),'font_points':9}
    assert qa['caption_below_panels'] and qa['inside_canvas'],qa
    fig._caption=text;fig._caption_qa=qa

def matrix(fig,ax,z,rows,cols,label,fmt='.1f'):
    bound=max(float(np.nanmax(np.abs(z))),.01)
    im=ax.imshow(z,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-bound,vcenter=0,vmax=bound),aspect='auto')
    ax.set_xticks(range(len(cols)),cols);ax.set_yticks(range(len(rows)),rows)
    for i in range(len(rows)):
        for j in range(len(cols)):
            ax.text(j,i,format(z[i,j],'+'+fmt),ha='center',va='center',fontsize=8,color='white' if abs(z[i,j])>bound*.65 else '#222')
    fig.colorbar(im,ax=ax,fraction=.045,pad=.035,label=label)

def ageplot(ax,data,value,ylabel):
    for pos,age in enumerate([3,18,24]):
        g=data[data.age_months==age].sort_values('mouse_id');values=100*g[value].to_numpy();offset=np.linspace(-.15,.15,len(g))
        ax.scatter(pos+offset,values,s=27,color=AGE[age],zorder=3)
        ax.plot([pos-.25,pos+.25],[values.mean()]*2,color='black',lw=1.4)
        ax.text(pos,1.02,f'n={len(g)}',ha='center',transform=ax.get_xaxis_transform(),fontsize=8)
    ax.set_xticks(range(3),[3,18,24]);ax.set_xlabel('Age (months; categorical spacing)');ax.set_ylabel(ylabel);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)

def pairs(ax,data,observed,standard,ages,ylabel):
    for i,age in enumerate(ages):
        g=data[data.age_months==age].sort_values('mouse_id')
        for offset,(_,row) in zip(np.linspace(-.13,.13,len(g)),g.iterrows()):
            x=np.array([i*3,i*3+1])+offset;y=100*row[[observed,standard]].to_numpy(dtype=float)
            ax.plot(x,y,color=AGE[age],lw=.7,alpha=.55)
            marker='^' if row.get('sex','')=='female' else 'o'
            ax.scatter(x,y,s=24,marker=marker,facecolors='white' if marker=='^' else AGE[age],edgecolors=AGE[age],zorder=3)
        for j,v in enumerate([observed,standard]):ax.plot([i*3+j-.25,i*3+j+.25],[100*g[v].mean()]*2,color='black',lw=1.2)
        ax.text(i*3+.5,1.025,f'{age} months · n={len(g)}',ha='center',transform=ax.get_xaxis_transform(),fontsize=8)
    ax.set_xticks([i*3+j for i in range(len(ages)) for j in [0,1]],['Observed','Young\nreference']*len(ages));ax.set_ylabel(ylabel);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(exist_ok=True)
    root=Path('analysis/research/runs');c=root/'nb5_composition_biological_v1';p=root/'nb5_repertoire_biological_v1'
    read=lambda folder,name:pd.read_csv(folder/(name+'.tsv'),sep='\t')
    dec=read(c,'decomposition');within=read(c,'within_type');cm=read(c,'composition_mouse');tm=read(p,'tissue_mouse');bm=read(p,'balanced_mouse');bt=read(p,'balanced_tissue');bd=read(p,'balanced_decomposition');summary=read(p,'tissue_summary')
    records=[];pdf=PdfPages(out/'nb5_biological_extensions.pdf',metadata={'Title':'Biological extensions: tissue RNA and compartment-local T-cell clonality'})
    def save(fig,stem,title):
        for ext in ['png','svg','pdf']:fig.savefig(out/(stem+'.'+ext),dpi=300,bbox_inches='tight')
        pdf.savefig(fig,bbox_inches='tight');records.append(dict(stem=stem,title=title,png_dpi=300,caption=fig._caption,caption_layout=fig._caption_qa));plt.close(fig)
    fig,axs=plt.subplots(2,2,figsize=(12,8.2));fig.subplots_adjust(left=.10,right=.96,top=.92,bottom=.16,wspace=.58,hspace=.65)
    for ax,ds,endpoint,letter,title in zip(axs.flat,['Lung_facs','Bladder_droplet']*2,['detected_fraction']*2+['mean_expression']*2,'ABCD',['Lung FACS · detection','Bladder droplet · detection','Lung FACS · mean RNA','Bladder droplet · mean RNA']):
        f=dec[(dec.dataset==ds)&(dec.sex_scope=='all_observed_sexes')&(dec.endpoint==endpoint)].set_index('gene').loc[GENES]
        factor=100 if endpoint=='detected_fraction' else 1;z=f[TERMS].to_numpy()*factor
        matrix(fig,ax,z,GENES,TERM_LABELS,'Difference (percentage points)' if factor==100 else 'RNA / 10,000 difference',fmt='.2f' if factor==100 else '.3f');panel(ax,letter,title)
    footer(fig,'Age-associated RNA differences combine captured composition and within-type changes. Cdkn2a detection rises in lung and falls in bladder. Values are 24 minus 3 months, with equal mouse weighting on common cell types. Four terms sum to the total; they are descriptive accounting, not causal effects. Color scales differ between panels.')
    save(fig,'07_tissue_rna_accounting','Composition and within-type RNA contributions')
    fig,axs=plt.subplots(2,2,figsize=(12,8.6));fig.subplots_adjust(left=.21,right=.96,top=.91,bottom=.14,wspace=.75,hspace=.68)
    for ax,ds,letter,title in zip(axs[0],['Lung_facs','Bladder_droplet'],'AB',['Lung FACS · within-type detection','Bladder droplet · within-type detection']):
        f=within[(within.dataset==ds)&(within.sex_scope=='all_observed_sexes')&(within.endpoint=='detected_fraction')&within.gene.isin(GENES)]
        z=f.pivot(index='cell_type',columns='gene',values='difference').reindex(columns=GENES)*100
        labels=[x.replace('bladder urothelial cell','Urothelial').replace('bladder cell','Mesenchymal') for x in z.index]
        matrix(fig,ax,z.to_numpy(),labels,GENES,'Detection difference (pp)');panel(ax,letter,title)
    for ax,ds,letter,title in zip(axs[1],['Lung_facs','Bladder_droplet'],'CD',['Lung · Cdkn2a detection','Bladder · Cdkn2a detection']):
        f=cm[(cm.dataset==ds)&(cm.sex_scope=='all_observed_sexes')&(cm.endpoint=='detected_fraction')&(cm.gene=='Cdkn2a')]
        pairs(ax,f,'observed_common','young_reference_standardized',[3,24],'Cdkn2a-detected cells (%)');panel(ax,letter,title)
    footer(fig,'Within-type profiles locate age-associated RNA differences; fixed young composition asks whether population redistribution accounts for the tissue summary. A/B: 24 minus 3 months. C/D: connected values from each mouse; black bars, means; triangles, females. Sparse types and finer subtype mixtures remain unresolved. RNA detection does not establish senescence.')
    save(fig,'08_within_type_and_mouse_profiles','Within-type profiles and fixed-composition animal estimates')
    fig,axs=plt.subplots(2,3,figsize=(12,7.8));fig.subplots_adjust(left=.08,right=.97,top=.90,bottom=.14,wspace=.40,hspace=.72)
    for j,t in enumerate(TISSUES):
        f=tm[tm.tissue==t]
        ageplot(axs[0,j],f,'local_clone_fraction','Locally repeated clone cells (%)');panel(axs[0,j],'ABC'[j],t+' · observed')
        depth=int(f.common_depth.dropna().iloc[0]);ageplot(axs[1,j],f,'expected_local_clone_fraction','Expected local repeat fraction (%)');panel(axs[1,j],'DEF'[j],t+f' · {depth} cells / mouse')
    footer(fig,'Local T-cell clone repetition is higher in older thymus and spleen samples; marrow shows a different age pattern. Points are mice and black bars are means. Bottom panels condition on tissue-specific sampling depth, so their magnitudes are not directly comparable across tissues. T-cell subtype, assembly selection and function remain unresolved.')
    save(fig,'09_compartment_local_clonality','Tissue-local T-cell clonality across ages')
    fig,axs=plt.subplots(2,2,figsize=(12,8.2));fig.subplots_adjust(left=.09,right=.95,top=.90,bottom=.15,wspace=.40,hspace=.74)
    ax=axs[0,0];w=bt.groupby(['age_months','tissue']).fraction.mean().unstack().reindex(index=[3,18,24],columns=TISSUES)*100;bottom=np.zeros(3)
    for t,color in zip(TISSUES,['#7293B5','#D8A248','#8469A5']):
        ax.bar(range(3),w[t],bottom=bottom,color=color,label=t,width=.6)
        for i in range(3):ax.text(i,bottom[i]+w[t].iloc[i]/2,t,ha='center',va='center',fontsize=7,color='white' if t=='Marrow' else '#17212B')
        bottom+=w[t].to_numpy()
    ax.set_xticks(range(3),['3\nn=2','18\nn=3','24\nn=4']);ax.set_ylim(0,100);ax.set_ylabel('Reconstructed focal cells (%)');ax.set_xlabel('Age (months)');panel(ax,'A','Tissue representation · balanced mice')
    ax=axs[0,1];pairs(ax,bm,'observed_local_fraction','young_reference_standardized',[3,18,24],'Locally repeated clone cells (%)');panel(ax,'B','Observed and fixed tissue composition')
    ax=axs[1,0]
    for offset,age in zip([-.18,.18],[18,24]):
        row=bd[bd.old_age==age].iloc[0];ax.bar(np.arange(5)+offset,100*row[TERMS].to_numpy(dtype=float),width=.34,color=AGE[age],label=f'{age} − 3 months')
    ax.axhline(0,color='#444',lw=.7);ax.set_xticks(range(5),TERM_LABELS);ax.tick_params(axis='x',labelsize=7);ax.set_ylabel('Local-clone difference (pp)');ax.legend(frameon=False,fontsize=8);panel(ax,'C','Exact tissue-mixture accounting')
    ax=axs[1,1];s=summary[(summary.endpoint=='shared_clone_fraction')&summary.tissue.isin(TISSUES)];z=s.pivot(index='tissue',columns='age_months',values='mean').reindex(index=TISSUES,columns=[3,18,24])*100
    im=ax.imshow(z,cmap='Blues',vmin=0,vmax=max(z.max().max(),1),aspect='auto');ax.set_xticks(range(3),[3,18,24]);ax.set_yticks(range(3),TISSUES);ax.set_xlabel('Age (months)')
    for i in range(3):
        for j in range(3):ax.text(j,i,f'{z.iloc[i,j]:.1f}',ha='center',va='center',color='white' if z.iloc[i,j]>z.max().max()*.65 else '#222',fontsize=9)
    fig.colorbar(im,ax=ax,fraction=.045,pad=.035,label='Cells in shared clones (%)');panel(ax,'D','Cross-tissue clone sharing · all mice')
    footer(fig,'Older local-clone burden persists after fixing tissue representation in the same mice. A–C use mice with thymus, spleen and marrow; D uses all supported mice per tissue. Shared clones indicate observed distribution across tissues, not migration. Only two young mice support the balanced comparison; subtype and reconstruction selection remain alternatives.')
    save(fig,'10_repertoire_compartment_accounting','Compartment representation and cross-tissue clone sharing')
    pdf.close();dump={'figures':records,'inputs':['nb5_composition_biological_v1','nb5_repertoire_biological_v1'],'limits':'Exposed exploratory observations; all panels use frozen outputs, no new model or biological acceptance.'};(out/'figure_manifest.json').write_text(json.dumps(dump,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'figures':len(records),'formats':['PNG 300 dpi','SVG','PDF']}))

if __name__=='__main__':main()
