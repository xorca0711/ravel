"""Render frozen R1 tables; no new tests, feature selection or model fitting."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import textwrap
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

BLUE = '#0072B2'
PURPLE = '#A64D79'
GREY = '#B4BAC0'
INK = '#20262C'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':8,
    'axes.titlesize':9, 'axes.labelsize':8, 'xtick.labelsize':7,
    'ytick.labelsize':7, 'axes.spines.top':False, 'axes.spines.right':False,
    'axes.linewidth':.6, 'xtick.major.width':.6, 'ytick.major.width':.6,
    'pdf.fonttype':42, 'ps.fonttype':42, 'svg.fonttype':'none',
    'savefig.facecolor':'white', 'text.color':INK, 'axes.labelcolor':INK})

CAPTIONS = {
'figure_1': ('Source-defined reaction contrasts',
    'A, Standardized Th17p-minus-Th17n score differences for all 14 source-named reactions declared before execution. Filled circles indicate source-cell BH q < 0.1; open circles indicate q >= 0.1. Grey diamonds show the individual-reaction route, while circles show the metareaction route. B, Each point is one distinct metareaction within the indicated core pathway; black lines show unweighted medians. The amino-acid panel pools the 16 source-listed subsystems and deduplicates groups. The same metareaction may occur in several pathways. Higher scores indicate lower Compass penalties, not measured flux. Cell-level q values reconstruct the source convention and do not establish animal-level evidence.'),
'figure_2': ('Pathway summaries conceal mixed reaction associations',
    'All 53 source-display pathways are shown. Left, one point per distinct metareaction per pathway, with black median marks. Blue and purple indicate positive and negative effects with source-cell BH q < 0.1; grey indicates other groups. Right, counts of groups meeting that source threshold in each direction. Rows are ordered by the unweighted median effect; this display order is descriptive. Pathways require more than five core reaction members and exclude the source transport/exchange/other categories. Shared groups across pathways are not independent tests. Medians are summaries of inferred scores, not pathway flux or activity measurements.'),
'figure_3': ('Cell-score distributions for the prespecified reactions',
    'All 14 prespecified reactions are shown without selecting for effect size. Each dot is one source cell; the deterministic horizontal jitter is visual only. Boxes show the median and interquartile range, with whiskers extending to the most extreme points within 1.5 interquartile ranges. Each panel contains 151 Th17n and 139 Th17p observations. Scores are the saved metareaction values, so reactions sharing a group have identical distributions. Vertical scales differ between panels. These cells are nested in unresolved animals or preparations; boxes and points are descriptive and no biological confidence interval is supplied.'),
'figure_S1': ('Source nesting and reconstruction diagnostics',
    'A, Cell counts by deposited single-cell batch label and condition. A batch label is not a verified biological replicate; batch 9 contains only Th17n cells. B, Number of reaction members in each formed metareaction, including groups later excluded by the score-range rule. C, Individual-reaction versus metareaction standardized effects for core reaction members available in both routes; multiple members can share the same group estimate. D, Declared reconstruction counts compared with counts stated in the paper. The reconstruction forms 1,912 nonconstant groups and retains 784 groups containing a core member, compared with 1,911 total and 784 core groups reported in the paper. Matching one count does not establish exact historical reproduction. The reference labels and selection conventions differ in qualification depth; no count was used to tune the clustering.')}

AMINO = ['Alanine and aspartate metabolism','Arginine and Proline Metabolism',
    'beta-Alanine metabolism','Cysteine Metabolism','D-alanine metabolism',
    'Folate metabolism','Glutamate metabolism','Glycine, serine, alanine and threonine metabolism',
    'Histidine metabolism','Lysine metabolism','Methionine and cysteine metabolism',
    'Taurine and hypotaurine metabolism','Tryptophan metabolism','Tyrosine metabolism',
    'Urea cycle','Valine, leucine, and isoleucine metabolism']

def colors(rows):
    return np.where(rows.q_source.ge(.1), GREY, np.where(rows.cohens_d.gt(0), BLUE, PURPLE))

def panel(ax, letter, title):
    ax.set_title(title, loc='left', pad=10)
    ax.text(-.10, 1.055, letter, transform=ax.transAxes, fontsize=12, fontweight='bold')

def footer(fig, title):
    fig.suptitle(title, x=.04, ha='left', y=.985, fontsize=11, fontweight='bold')
    fig.text(.04,.014,'Wagner source reconstruction | 139 Th17p / 151 Th17n cells | Biological replication unresolved',fontsize=7,color='#535D65')

def effect_axis(ax):
    ax.axvline(0,color='#8B9297',lw=.7,zorder=0)
    ax.set_xlabel("Standardized score difference (Cohen's d)\nTh17n higher  ←                         →  Th17p higher")
    ax.grid(axis='x',color='#E8EBED',lw=.5,zorder=0)

def main(source, output):
    environment={'python':sys.version,'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','statsmodels','matplotlib']}}
    if environment != json.loads((source/'environment.json').read_text()):
        raise ValueError('Figure runtime differs from the qualified analysis environment')
    verification=json.loads((source/'verification.json').read_text())
    if not verification['passed']: raise ValueError('Numerical verification must pass before figure rendering')
    summary=json.loads((source/'summary.json').read_text())
    ex=pd.read_csv(source/'expanded_metareaction_statistics.tsv',sep='\t',index_col=0)
    direct=pd.read_csv(source/'reaction_statistics.tsv',sep='\t',index_col=0)
    sel=pd.read_csv(source/'selected_reactions.tsv',sep='\t',index_col=0)
    cells=pd.read_csv(source/'selected_cell_scores.tsv',sep='\t',index_col=0)
    paths=pd.read_csv(source/'pathway_summary.tsv',sep='\t')
    members=pd.read_csv(source/'metareaction_membership.tsv',sep='\t')
    core=ex[ex.core]
    assert len(sel)==14 and sel.available.all() and len(paths)==53 and len(cells)==290
    figures=[]

    fig,(a,b)=plt.subplots(1,2,figsize=(10.2,6.4),gridspec_kw={'width_ratios':[1.2,1]})
    fig.subplots_adjust(left=.26,right=.97,bottom=.17,top=.87,wspace=.62)
    y=np.arange(len(sel))
    a.scatter(sel.direct_cohens_d,y,marker='D',s=13,color='#B6BDC2',label='Individual reaction',zorder=2)
    for n,(_,r) in enumerate(sel.iterrows()):
        color=BLUE if r.cohens_d>0 else PURPLE
        a.scatter(r.cohens_d,n,s=39,facecolor=color if r.q_source<.1 else 'white',edgecolor=color,lw=.9,zorder=3)
    a.set_yticks(y,[f'{r.display_name}\n{k}' for k,r in sel.iterrows()],fontsize=7)
    a.invert_yaxis();a.set_ylim(len(sel)-.4,-.6);effect_axis(a)
    a.set_xlim(min(-1.35,float(sel.cohens_d.min())-.12),max(.8,float(sel.cohens_d.max())+.1))
    panel(a,'A','Prespecified reaction effects')
    sets=[('Glycolysis',core.subsystem.eq('Glycolysis/gluconeogenesis')),
          ('TCA (mitochondrial)',core.subsystem.eq('Citric acid cycle')),
          ('Fatty acid oxidation',core.subsystem.eq('Fatty acid oxidation')),
          ('Amino-acid subsystems',core.subsystem.isin(AMINO))]
    rng=np.random.default_rng(471)
    for i,(name,mask) in enumerate(sets):
        rows=core[mask].drop_duplicates('metareaction_id')
        b.scatter(rows.cohens_d,i+rng.uniform(-.20,.20,len(rows)),s=15,c=colors(rows),alpha=.75,lw=0)
        b.plot([rows.cohens_d.median()]*2,[i-.28,i+.28],color=INK,lw=2)
        b.text(.99,i+.30,f'{len(rows)} groups',transform=b.get_yaxis_transform(),ha='right',fontsize=7,color='#606970')
    b.set_yticks(range(4),[s[0] for s in sets]);b.set_ylim(3.7,-.65);effect_axis(b)
    panel(b,'B','Core metareaction distributions')
    handles=[Line2D([],[],marker='o',color=BLUE,lw=0,label='Th17p higher; source q < 0.1'),
             Line2D([],[],marker='o',color=PURPLE,lw=0,label='Th17n higher; source q < 0.1'),
             Line2D([],[],marker='o',color=GREY,lw=0,label='Source q ≥ 0.1'),
             Line2D([],[],marker='D',color='#B6BDC2',lw=0,label='Individual-reaction effect (A)')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.049),ncol=2,frameon=False,fontsize=7)
    footer(fig,CAPTIONS['figure_1'][0]);figures.append(('figure_1',fig))

    ordered=paths.sort_values(['median_metareaction_d','subsystem'],ascending=[False,True]).reset_index(drop=True)
    fig,(a,b)=plt.subplots(1,2,figsize=(10.6,13.8),gridspec_kw={'width_ratios':[2.1,1]})
    fig.subplots_adjust(left=.40,right=.98,bottom=.09,top=.93,wspace=.22)
    for i,row in ordered.iterrows():
        rows=core[core.subsystem.eq(row.subsystem)].drop_duplicates('metareaction_id')
        a.scatter(rows.cohens_d,i+rng.uniform(-.21,.21,len(rows)),s=7,c=colors(rows),alpha=.7,lw=0)
        a.plot([row.median_metareaction_d]*2,[i-.28,i+.28],color=INK,lw=1.3)
    a.set_yticks(range(len(ordered)),ordered.subsystem,fontsize=7)
    b.barh(range(len(ordered)),ordered.negative_q_lt_0_1,color=PURPLE,height=.62)
    b.barh(range(len(ordered)),ordered.positive_q_lt_0_1,left=ordered.negative_q_lt_0_1,color=BLUE,height=.62)
    for i,row in ordered.iterrows():
        b.text(row.negative_q_lt_0_1+row.positive_q_lt_0_1+.5,i,f'{row.negative_q_lt_0_1}/{row.positive_q_lt_0_1}',va='center',fontsize=6)
    for ax in [a,b]: ax.set_ylim(len(ordered)-.4,-.7)
    b.set_yticks([]);b.set_xlabel('Groups with source q < 0.1\nLabels: Th17n higher / Th17p higher')
    b.set_xlim(0,(ordered.positive_q_lt_0_1+ordered.negative_q_lt_0_1).max()*1.29)
    effect_axis(a);panel(a,'A','Within-pathway effects');panel(b,'B','Directional group counts')
    fig.legend(handles=handles[:3],loc='lower center',bbox_to_anchor=(.55,.038),ncol=3,frameon=False,fontsize=7)
    footer(fig,CAPTIONS['figure_2'][0]);figures.append(('figure_2',fig))

    fig,axes=plt.subplots(4,4,figsize=(10.3,9.6))
    fig.subplots_adjust(left=.075,right=.985,bottom=.09,top=.91,wspace=.48,hspace=.75)
    for i,((reaction,row),ax) in enumerate(zip(sel.iterrows(),axes.flat)):
        arrays=[cells.loc[cells.cell_type.eq(c),reaction].to_numpy() for c in ['Th17n','Th17p']]
        for j,(values,color) in enumerate(zip(arrays,[PURPLE,BLUE])):
            ax.scatter(j+rng.uniform(-.19,.19,len(values)),values,s=5,c=color,alpha=.35,lw=0)
        ax.boxplot(arrays,positions=[0,1],widths=.42,showfliers=False,medianprops={'color':INK,'linewidth':1.2},boxprops={'linewidth':.8},whiskerprops={'linewidth':.7},capprops={'linewidth':.7})
        ax.set_xticks([0,1],['Th17n\n151 cells','Th17p\n139 cells']);ax.set_xlim(-.55,1.55)
        ax.set_title('\n'.join(textwrap.wrap(row.display_name,24))+'\n'+reaction,fontsize=8,loc='left')
        ax.text(-.27,1.16,chr(65+i),transform=ax.transAxes,fontweight='bold',fontsize=10)
        ax.ticklabel_format(axis='y',style='plain',useOffset=False)
        if i%4==0:ax.set_ylabel('Transformed score')
    for ax in list(axes.flat)[14:]:ax.axis('off')
    axes[3,2].text(0,.75,'Dots: individual source cells\nBoxes: median and interquartile range\nPanel-specific vertical scales\nNo animal-level confidence intervals',transform=axes[3,2].transAxes,fontsize=8,linespacing=1.6)
    footer(fig,CAPTIONS['figure_3'][0]);figures.append(('figure_3',fig))

    fig,axes=plt.subplots(2,2,figsize=(8.6,7.1))
    fig.subplots_adjust(left=.10,right=.97,bottom=.12,top=.88,wspace=.39,hspace=.52)
    a,b,c,d=axes.flat
    batch=cells.source_label.str.extract(r'batch (\d+)')[0]
    tab=pd.crosstab(batch,cells.cell_type).reindex(columns=['Th17n','Th17p'],fill_value=0)
    a.bar(tab.index,tab.Th17n,color=PURPLE,label='Th17n');a.bar(tab.index,tab.Th17p,bottom=tab.Th17n,color=BLUE,label='Th17p')
    for i,(_,row) in enumerate(tab.iterrows()):
        a.text(i,row.Th17n/2,str(row.Th17n),ha='center',va='center',color='white',fontsize=8)
        if row.Th17p:a.text(i,row.Th17n+row.Th17p/2,str(row.Th17p),ha='center',va='center',color='white',fontsize=8)
    a.set_xlabel('Deposited single-cell batch label');a.set_ylabel('Cells');a.legend(frameon=False,fontsize=7)
    panel(a,'A','Condition composition by source batch')
    sizes=members.groupby('metareaction_id').size()
    b.hist(sizes,bins=np.geomspace(1,sizes.max()+1,18),color='#667988',edgecolor='white',lw=.4)
    b.set_xscale('log');b.set_yscale('log');b.set_xlabel('Reaction members per metareaction');b.set_ylabel('Metareactions');panel(b,'B','Group-size distribution')
    joined=core.join(direct[['cohens_d']],rsuffix='_direct',how='inner')
    c.scatter(joined.cohens_d_direct,joined.cohens_d,s=7,color='#667988',alpha=.35,lw=0)
    lim=[min(joined.cohens_d.min(),joined.cohens_d_direct.min())-.06,max(joined.cohens_d.max(),joined.cohens_d_direct.max())+.06]
    c.plot(lim,lim,color=INK,lw=.7,ls='--');c.set_xlim(lim);c.set_ylim(lim)
    c.set_xlabel("Individual-reaction Cohen's d");c.set_ylabel("Metareaction Cohen's d");panel(c,'C','Grouping sensitivity (core members)')
    x=np.arange(2)
    v=[summary['formed_metareactions'],summary['core_metareactions_any_core_member']]
    ref=[summary['source_paper_reported_metareactions'],summary['source_paper_reported_core_metareactions']]
    d.bar(x-.18,v,.34,color='#667988',label='Reconstructed');d.bar(x+.18,ref,.34,color='#CFD4D8',label='Paper-reported')
    for offset,counts in [(-.18,v),(.18,ref)]:
        for k,n in enumerate(counts):d.text(k+offset,n+38,str(n),ha='center',fontsize=7)
    d.set_xticks(x,['Formed groups','Groups with core member']);d.set_ylim(0,max(v)*1.18);d.set_ylabel('Metareactions');d.legend(frameon=False,fontsize=7)
    panel(d,'D','Source-count comparison');footer(fig,CAPTIONS['figure_S1'][0]);figures.append(('figure_S1',fig))

    manifest={'source_run':source.as_posix(),'scope':'Rendering of frozen descriptive outputs; no new fit or inferential test','figures':[]}
    with PdfPages(output/'Wagner_R1_figures.pdf') as book:
        for stem,fig in figures:
            fig.canvas.draw()
            for extension in ['pdf','svg','png']:
                path=output/(stem+'.'+extension)
                fig.savefig(path,dpi=300)
                manifest['figures'].append({'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
            book.savefig(fig);plt.close(fig)
    text='# Wagner R1 figure captions\n\nAll figures: exposed descriptive reconstruction of author-provided Compass penalties; independent biological units remain unknown.\n\n'
    for stem,(title,caption) in CAPTIONS.items():text+=f'## {stem.replace("_"," ")}: {title}\n\n{caption}\n\n'
    (output/'CAPTIONS.md').write_text(text,encoding='utf-8')
    (output/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'figure_plates':len(figures),'individual_files':len(manifest['figures']),'source_verification':True}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.source,a.output)
