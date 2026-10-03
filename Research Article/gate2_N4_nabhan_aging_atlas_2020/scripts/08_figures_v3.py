"""Article-style figures from verified Nb5 descriptive outputs only."""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import TwoSlopeNorm
from matplotlib.font_manager import FontProperties
from nb5_captions_v3 import CAPTIONS

AGE={1:'#666666',3:'#0072B2',18:'#009E73',21:'#CC79A7',24:'#D55E00',30:'#E69F00'}
DS=['Bladder_droplet','Kidney_droplet','Lung_droplet','Lung_facs','Brain_Myeloid_facs','facs.Brain_Myeloid.clustered_diversity']
LABEL=['Bladder · droplet','Kidney · droplet','Lung · droplet','Lung · FACS','Brain · general FACS','Brain · Fig. 4 FACS']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'axes.linewidth':0.7,'savefig.facecolor':'white'})

def panel(ax,letter,title):
    ax.set_title(title,loc='left',pad=12)
    ax.text(-.16,1.09,letter,transform=ax.transAxes,weight='bold',fontsize=12)
def ageplot(ax,d,value,label,ages=None,percent=False):
    ages=ages or sorted(d.age_months.unique());factor=100 if percent else 1
    for pos,age in enumerate(ages):
        g=d[d.age_months==age].sort_values('mouse_id');v=g[value].to_numpy()*factor;offset=np.linspace(-.14,.14,len(g)) if len(g)>1 else [0]
        for x,(_,row),y in zip(offset,g.iterrows(),v):
            if not np.isfinite(y):continue
            marker='^' if row.get('sex','male')=='female' else 'o'
            ax.scatter(pos+x,y,s=25,marker=marker,facecolors='white' if marker=='^' else AGE[age],edgecolors=AGE[age],linewidth=.8,zorder=3)
        if np.isfinite(v).any():ax.plot([pos-.23,pos+.23],[np.nanmean(v)]*2,color='black',lw=1.3,zorder=4)
        ax.text(pos,1.025,'n='+str(np.isfinite(v).sum()),ha='center',fontsize=7,transform=ax.get_xaxis_transform())
    ax.set_xticks(range(len(ages)),[str(x) for x in ages]);ax.set_xlabel('Age (months; categorical spacing)');ax.set_ylabel(label);ax.grid(axis='y',alpha=.16,lw=.5);ax.set_axisbelow(True)
    if percent:ax.set_ylim(bottom=0,top=min(100,max(1,ax.get_ylim()[1]*1.10)))
_caption_index = 0

def footer(fig,text):
    """Fit a compact footer beneath unchanged panels, following Nb2/Nb4 style."""
    global _caption_index
    caption=CAPTIONS[_caption_index];_caption_index+=1
    width,height=fig.get_size_inches();fig.canvas.draw();renderer=fig.canvas.get_renderer()
    prop=FontProperties(family='DejaVu Sans',size=9)
    lines=[];line=''
    for word in caption.split():
        candidate=(line+' '+word).strip()
        if line and renderer.get_text_width_height_descent(candidate,prop,False)[0]>.90*width*fig.dpi:
            lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    body='\n'.join(lines)
    body_h=len(lines)*9*1.30/72
    plot_bottom=min(ax.get_tightbbox(renderer).y0 for ax in fig.axes)/fig.dpi
    added=max(0,body_h+.30-plot_bottom)
    if added:
        positions=[(ax,ax.get_position().frozen()) for ax in fig.axes]
        fig.set_size_inches(width,height+added)
        for ax,pos in positions:
            ax.set_position([pos.x0,(pos.y0*height+added)/(height+added),pos.width,pos.height*height/(height+added)])
    artist=fig.text(.05,.12/(height+added),body,fontsize=9,ha='left',va='bottom',linespacing=1.30)
    fig.canvas.draw();renderer=fig.canvas.get_renderer();box=artist.get_window_extent(renderer)
    plot_bottom=min(ax.get_tightbbox(renderer).y0 for ax in fig.axes)
    qa={'caption_below_panels':bool(box.y1<plot_bottom),'text_inside_canvas':bool(box.x0>=0 and box.x1<=width*fig.dpi and box.y0>=0),'font_points':9,'lines':len(lines),'words':len(caption.split()),'added_height_inches':float(added)}
    assert qa['caption_below_panels'] and qa['text_inside_canvas'],qa
    fig._nb5_caption=caption;fig._nb5_caption_qa=qa


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--repertoire',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();inp=Path(args.input);out=Path(args.output);out.mkdir(exist_ok=True)
    read=lambda n:pd.read_csv(inp/n,sep='\t')
    design=read('design_units.tsv');release=read('release_concordance.tsv');comp=read('composition_mouse.tsv');expr=read('expression_mouse.tsv');states=read('microglia_state_mouse.tsv');emb=read('microglia_umap.tsv');ce=read('microglia_source_expression.tsv');rep=pd.read_csv(Path(args.repertoire)/'repertoire_mouse.tsv',sep='\t');pooled=pd.read_csv(Path(args.repertoire)/'repertoire_source.tsv',sep='\t');account=read('lung_accounting.tsv');contrast=read('expression_contrasts.tsv')
    records=[];pdf=PdfPages(out/'nb5_figure_set.pdf',metadata={'Title':'Tabula Muris Senis: bounded reproduction and exploratory analysis','Author':'scRNA_seq repository'})
    def save(fig,name,title):
        for ext in ['png','svg','pdf']:fig.savefig(out/(name+'.'+ext),dpi=300,bbox_inches='tight')
        pdf.savefig(fig,bbox_inches='tight');records.append({'stem':name,'title':title,'size_inches':list(fig.get_size_inches()),'png_dpi':300,'caption':fig._nb5_caption,'caption_layout':fig._nb5_caption_qa});plt.close(fig)
    # 1. Design and release qualification, retaining pooled-label warnings.
    fig,axs=plt.subplots(2,1,figsize=(10.2,7.4),gridspec_kw={'height_ratios':[1.2,1]});fig.subplots_adjust(left=.24,right=.96,top=.92,bottom=.14,hspace=.7)
    ax=axs[0];ages=[1,3,18,21,24,30];cols=[(a,s) for a in ages for s in ['female','male']];z=np.zeros((len(DS),len(cols)))
    for i,ds in enumerate(DS):
        for j,(age,sex) in enumerate(cols):z[i,j]=len(design[(design.dataset==ds)&(design.age_months==age)&(design.sex==sex)&(design.unit_kind=='deposited_mouse')])
    ax.imshow(z,cmap='Blues',aspect='auto',vmin=0,vmax=max(z.max(),1))
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):ax.text(j,i,str(int(z[i,j])),ha='center',va='center',color='white' if z[i,j]>z.max()*.55 else '#222',fontsize=8)
    ax.set_xticks(range(len(cols)),[f'{a}\n'+('F' if s=='female' else 'M') for a,s in cols]);ax.set_yticks(range(len(DS)),LABEL);ax.set_xlabel('Age (months) and recorded sex');panel(ax,'A','Deposited individual-mouse labels per tissue and assay')
    ax=axs[1]
    for i,ds in enumerate(DS):
        d=release[release.dataset==ds];v=100*d.cell_difference/d.source_cells;offset=np.linspace(-.17,.17,len(d))
        ax.scatter(i+offset,v,s=19,color='#536878',alpha=.85)
    ax.axhline(0,color='black',lw=.8);ax.set_xticks(range(len(DS)),['Bladder\ndroplet','Kidney\ndroplet','Lung\ndroplet','Lung\nFACS','Brain\ngeneral','Brain\nFig. 4']);ax.set_ylabel('Released − source cells\n(% of source table count)');panel(ax,'B','Cell-count concordance with supplementary Tables 1a and 2a')
    footer(fig,'A: numbers are source mouse labels, not independent cross-tissue replicates. Two pooled young lung libraries are excluded.\nB: each point is one deposited tissue–mouse record. General and Figure 4 brain releases overlap.')
    save(fig,'01_design_and_release','Design support and source-release concordance')
    # 2. Per-animal captured composition, no relabeling of broad bladder annotation.
    fig,axs=plt.subplots(2,2,figsize=(10.2,7.8));fig.subplots_adjust(left=.10,right=.96,top=.91,bottom=.14,hspace=.70,wspace=.40)
    targets=[('Bladder_droplet','bladder urothelial cell','Urothelial cells'),('Bladder_droplet','bladder cell','Mesenchymal cells (source annotations)'),('Kidney_droplet','kidney loop of Henle thick ascending limb epithelial cell','Renal thick ascending limb epithelium')]
    for ax,(ds,ct,title),letter in zip([axs[0,0],axs[0,1],axs[1,0]],targets,'ABC'):
        d=comp[(comp.dataset==ds)&(comp.cell_type==ct)];ageplot(ax,d,'fraction','Captured cells (%)',percent=True);panel(ax,letter,title)
    ax=axs[1,1];types=['bladder urothelial cell','bladder cell'];positions=np.arange(4)
    for j,(age,ct) in enumerate([(a,c) for a in [3,24] for c in types]):
        d=comp[(comp.dataset=='Bladder_droplet')&(comp.age_months==age)&(comp.cell_type==ct)];equal=100*d.fraction.mean();weighted=100*d.cells.sum()/d.total_cells.sum()
        ax.scatter(j-.08,equal,marker='o',s=38,color=AGE[age],label='Equal mouse weight' if j==0 else None);ax.scatter(j+.08,weighted,marker='s',s=38,facecolors='white',edgecolors=AGE[age],label='Pooled cell weight' if j==0 else None);ax.plot([j-.08,j+.08],[equal,weighted],color='#999',lw=.8)
    ax.set_xticks(positions,['3m\nurothelial','3m\nbladder','24m\nurothelial','24m\nbladder']);ax.set_ylabel('Captured cells (%)');ax.set_ylim(0,100);ax.legend(frameon=False,fontsize=7,loc='upper left');panel(ax,'D','Sensitivity to unequal cell sampling')
    footer(fig,'Points: individual mice; triangles: female; circles: male; black bars: arithmetic mouse means. n is shown above each age.\nFractions describe captured cells, not absolute tissue abundance. One month is developmental; age is cross-sectional.')
    save(fig,'02_captured_composition','Captured-cell composition and sampling sensitivity')
    # 3. Deposited UMAP + source-defined occupancy, deliberately no inferred trajectory.
    fig,axs=plt.subplots(2,3,figsize=(12.2,7.5));fig.subplots_adjust(left=.07,right=.95,top=.92,bottom=.14,hspace=.62,wspace=.44)
    colors={'source_1_6':'#0072B2','source_10_12_14':'#D55E00','other_source_clusters':'#c7c7c7'}
    for ax,age,letter in zip(axs[0],[3,18,24],'ABC'):
        d=emb[emb.age_months==age]
        for state in ['other_source_clusters','source_1_6','source_10_12_14']:
            g=d[d.state==state];ax.scatter(g.umap1,g.umap2,s=2,c=colors[state],alpha=.55,rasterized=True,linewidths=0)
        ax.set_xlim(emb.umap1.min()-1,emb.umap1.max()+1);ax.set_ylim(emb.umap2.min()-1,emb.umap2.max()+1);ax.set_xticks([]);ax.set_yticks([]);ax.set_xlabel('Deposited UMAP 1');ax.set_ylabel('Deposited UMAP 2');panel(ax,letter,f'{age} months · {d.mouse_id.nunique()} mice · {len(d):,} cells')
    for ax,state,title,letter in [(axs[1,0],'source_1_6','Deposited clusters 1 and 6','D'),(axs[1,1],'source_10_12_14','Deposited clusters 10, 12 and 14','E')]:ageplot(ax,states[states.state==state],'fraction','Source-annotated microglia (%)',percent=True);panel(ax,letter,title)
    ax=axs[1,2];genes=['H2-K1','B2m','Ifit3','Ifitm3','P2ry12','Apoe'];d=ce[(ce.cell_type=='microglial cell')&ce.gene.isin(genes)];z=d.groupby(['gene','age_months']).detected_fraction.mean().unstack().reindex(index=genes,columns=[3,18,24])*100
    im=ax.imshow(z,cmap='viridis',vmin=0,vmax=100,aspect='auto');ax.set_xticks([0,1,2],[3,18,24]);ax.set_yticks(range(len(genes)),genes);ax.set_xlabel('Age (months)');panel(ax,'F','Marker detection: equal mouse means');fig.colorbar(im,ax=ax,fraction=.045,pad=.03,label='Detected cells (%)')
    footer(fig,'UMAP and labels are from the author deposit; final-paper cluster correspondence is unresolved. Blue: clusters 1/6; orange: clusters 10/12/14; grey: remaining clusters.\nD–E: mouse points and means. F: nonzero deposited X; no back-transformation. These panels do not establish a transition or distinct intermediate state.')
    save(fig,'03_microglial_source_states','Deposited microglial cluster-label audit and animal-level occupancy')
    # 4. Keep three mathematically different RNA endpoints separate.
    fig,axs=plt.subplots(2,3,figsize=(12.2,7.7));fig.subplots_adjust(left=.08,right=.97,top=.91,bottom=.15,hspace=.70,wspace=.54)
    d=expr[(expr.dataset=='Lung_facs')&(expr.cell_type=='ALL')&(expr.gene=='Cdkn2a')]
    for ax,field,yl,title,letter,pct in zip(axs[0],['detected_fraction','positive_mean','mean_expression'],['Cells with detected RNA (%)','Mean RNA / 10,000\n(positive cells only)','Mean RNA / 10,000\n(all captured cells)'],['Cdkn2a: detection frequency','Cdkn2a: conditional expression','Cdkn2a: unconditional expression'],'ABC',[True,False,False]):ageplot(ax,d,field,yl,percent=pct);panel(ax,letter,title)
    ax=axs[1,0];a=account[(account.dataset=='Lung_facs')&(account.gene=='Cdkn2a')]
    for i,age in enumerate([3,24]):
        g=a[a.age_months==age].sort_values('mouse_id')
        for j,(_,row) in enumerate(g.iterrows()):
            off=(j-(len(g)-1)/2)*.035;ax.plot([i*2+off,i*2+1+off],[row.observed_mean,row.equal_type_mean],color=AGE[age],alpha=.55,lw=.75);ax.scatter([i*2+off,i*2+1+off],[row.observed_mean,row.equal_type_mean],color=AGE[age],s=18)
    ax.set_xticks(range(4),['3m\nobserved','3m\nequal type','24m\nobserved','24m\nequal type']);ax.set_ylabel('Mean normalized Cdkn2a RNA');panel(ax,'D','Lung FACS: composition accounting')
    for ax,ds,title,letter in [(axs[1,1],'Kidney_droplet','Kidney macrophages: Il1b','E'),(axs[1,2],'Lung_facs','Lung macrophages: Il1b','F')]:
        d=expr[(expr.dataset==ds)&(expr.cell_type=='macrophage')&(expr.gene=='Il1b')];ageplot(ax,d,'detected_fraction','Cells with detected RNA (%)',percent=True);panel(ax,letter,title)
    footer(fig,'Mouse points and arithmetic means; triangles denote females. Normalized per-cell RNA is used, not raw counts.\nD: equal weighting of cell types present in every retained mouse; see coverage table. RNA detection does not establish senescence or cytokine secretion.')
    save(fig,'04_marker_endpoints','Marker frequency, conditional expression and composition accounting')
    # 5. Exact rarefaction expectation conditions on reconstructed receptors and source labels.
    fig,axs=plt.subplots(2,2,figsize=(10.2,7.6));fig.subplots_adjust(left=.10,right=.96,top=.91,bottom=.14,hspace=.65,wspace=.42)
    ax=axs[0,0]
    for i,row in pooled.iterrows():ax.bar(i,row.pooled_fraction*100,color=AGE[int(row.age_months)],width=.6);ax.text(i,row.pooled_fraction*100+1,f'{int(row.source_clone_cells)}/{int(row.mapped_rows)}',ha='center',fontsize=8)
    ax.set_xticks(range(len(pooled)),pooled.age_months.astype(int));ax.set_ylim(0,max(32,pooled.pooled_fraction.max()*100+8));ax.set_xlabel('Age (months)');ax.set_ylabel('Matched cells in a clonal family (%)');panel(ax,'A','Matched source-table arithmetic')
    ageplot(axs[0,1],rep,'source_clone_fraction','Reconstructed cells in source clones (%)',percent=True);panel(axs[0,1],'B','Within-mouse source clone groups')
    ax=axs[1,0];depth=int(rep.common_depth.iloc[0])
    ageplot(ax,rep,'expected_fraction_at_common_depth','Expected nonsingleton cells (%)',percent=True);panel(ax,'C',f'Common-depth expectation · {depth} cells / mouse')
    ax=axs[1,1];ageplot(ax,rep,'reconstructed_cells','Reconstructed T cells per mouse');ax.set_yscale('log');panel(ax,'D','Unequal reconstruction denominators')
    footer(fig,'Source Table 9, matched reconstructed T cells only. Points: mouse; bars: equal mouse means; sexes are not encoded in these panels.\nC: exact hypergeometric expectation using within-mouse observed clone labels. Tissue mixture and reconstruction selection remain unresolved.')
    save(fig,'05_repertoire_sampling','T-cell clonal-family fractions and sampling sensitivity')
    # 6. Fixed marker family subset, not a screen for the largest effects.
    genes=['Cdkn2a','Cdkn1a','Lmnb1','Il1b','H2-K1','Ifit3','P2ry12','Apoe'];targets=[('Brain_Myeloid_facs','microglial cell','Brain microglia'),('Lung_facs','macrophage','Lung macrophages'),('Kidney_droplet','macrophage','Kidney macrophages')]
    fig,axs=plt.subplots(2,1,figsize=(10.8,6.5));fig.subplots_adjust(left=.23,right=.90,top=.91,bottom=.18,hspace=.65)
    for ax,scope,letter,title in zip(axs,['all_observed_sexes','male_only'],'AB',['All observed sexes','Male-only sensitivity']):
        z=np.full((3,len(genes)),np.nan);labels=[]
        for i,(ds,ct,label) in enumerate(targets):
            d=contrast[(contrast.dataset==ds)&(contrast.cell_type==ct)&(contrast.sex_scope==scope)&(contrast.endpoint=='detected_fraction')]
            labels.append(label+('  n='+str(int(d.iloc[0].n_3m))+'/'+str(int(d.iloc[0].n_24m)) if len(d) else '  unavailable'))
            for j,gene in enumerate(genes):
                f=d[d.gene==gene]
                if len(f):z[i,j]=float(f.iloc[0].difference_24_minus_3)*100
        im=ax.imshow(z,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-100,vcenter=0,vmax=100),aspect='auto');ax.set_xticks(range(len(genes)),genes);ax.set_yticks(range(3),labels)
        for i in range(3):
            for j in range(len(genes)):
                if np.isfinite(z[i,j]):ax.text(j,i,f'{z[i,j]:+.1f}',ha='center',va='center',fontsize=8,color='white' if abs(z[i,j])>55 else '#222')
        panel(ax,letter,title)
    cb=fig.add_axes([.93,.30,.018,.43]);fig.colorbar(im,cax=cb,label='24m − 3m detection (percentage points)')
    footer(fig,'Equal mouse means; n labels are young/old animals. Complete fixed-marker family is retained in the source table; this subset was fixed for display.\nResident populations and assays differ. Shared direction is context, not a conserved mechanism or independent organ replication; no interaction test.')
    save(fig,'06_fixed_marker_context','Within-population marker differences and sex sensitivity')
    pdf.close();(out/'figure_manifest.json').write_text(json.dumps({'figures':records,'source_run':str(inp),'style_reference':'Nb4 rq_sequence_v2: white background, labeled panels, mouse points, vector exports; no significance stars','limits':'Version 3 replaces long v2 captions with compact purpose/result/limit footers; extended explanations remain in the gallery. All numerical panels are unchanged; prior editions remain archived. No scientific acceptance.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'figures':len(records),'formats':['300-dpi PNG','SVG','PDF'],'combined_pdf':'nb5_figure_set.pdf'}))

if __name__=='__main__':main()
