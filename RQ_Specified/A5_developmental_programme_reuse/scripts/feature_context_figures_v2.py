"""Rendering-only correction; no biological recalculation."""
from pathlib import Path
import argparse,json,hashlib
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'analysis/research/runs/A5_feature_context_display_v1_20261104'
PRE=ROOT/'docs/research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites'
def require(value,message):
    if not value:raise ValueError(message)
def heatmap(joined, mapping, mice, days, limit, output, selected):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    chosen = mapping[mapping.candidate_panel.astype(str).str.lower().eq('true')] if selected else mapping
    chosen = chosen.sort_values('display_order')
    data = joined.pivot(index='gene', columns='sample_id', values='delta_detection_pp').loc[chosen.gene, mice]
    require(not data.isna().any().any(), 'Missing plotted value')
    fig, ax = plt.subplots(figsize=(15, max(9.5 if selected else 8, len(chosen)*.25+3)))
    img=ax.imshow(data.to_numpy(), aspect='auto', cmap='RdBu_r', vmin=-limit, vmax=limit, interpolation='nearest')
    ax.set_yticks(range(len(chosen)), chosen.gene.tolist(), fontsize=9)
    ax.set_xticks(range(len(mice)), [f'{m}\nd{days[m]}' for m in mice], rotation=90, fontsize=8)
    labels={'junction_polarity_candidate':'Junction / polarity','basement_membrane_material_candidate':'Basement-membrane material','adhesion_signaling_interface':'Adhesion / signaling interface','original_receptor_ligand':'Original 5 receptor / ligand','original_specialized_transport':'Original 4 transport','peripheral_architecture_context':'Peripheral architecture context','original_gene_expression_regulation':'Original 6 regulators','remaining_member_context':'Other members / unresolved context'}
    for _, block in chosen.reset_index(drop=True).groupby('display_group_order', sort=False):
        lo, hi = int(block.index.min()), int(block.index.max())
        ax.axhline(lo-.5,color='#222222',linewidth=.6)
        ax.text(1.015,(lo+hi)/2,labels[block.display_group.iloc[0]],transform=ax.get_yaxis_transform(),va='center',fontsize=9)
    for i in range(1,len(mice)):
        if days[mice[i]]!=days[mice[i-1]]:ax.axvline(i-.5,color='#222222',linewidth=.5)
    ax.set_title(('Selected 22-gene display' if selected else 'All 99 fixed component members')+'\nKrt8+ ADI minus activated AT2 | original 24 mice',loc='left',fontsize=14,pad=14)
    ax.set_xlabel('Original mouse and sampling day; columns are animals, not cells')
    fig.subplots_adjust(left=.10,right=.70,bottom=.24 if selected else .15,top=.93)
    cax=fig.add_axes([.82,.10,.13,.012]);fig.colorbar(img,cax=cax,orientation='horizontal',label='Detection difference (percentage points)')
    caption='Shared unclipped scale across all 99 genes. Selected 22 are a display, not an exhaustive biological inventory.\nSource roles can overlap; cross-tissue/inferred annotations do not demonstrate function in repair.\nPpl has junction-related keratinocyte/desmosome context; peripheral placement does not mean absent function.'
    fig.text(.10,.025,caption,fontsize=8,va='bottom')
    fig.savefig(output,dpi=160,facecolor='white');plt.close(fig)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    values=pd.read_csv(OLD/'all_member_values.tsv',sep='\t',keep_default_na=False)
    mapping=pd.read_csv(PRE/'A5_FEATURE_DISPLAY_MAP_V1.tsv',sep='\t',keep_default_na=False)
    summary=json.loads((OLD/'summary.json').read_text(encoding='utf-8'))
    limit=summary['shared_color_limit_pp'];require(limit==25.536807215314504,'Scale drift')
    require(len(values)==2376 and len(mapping)==99,'Display input drift')
    args.output.mkdir(parents=True,exist_ok=True)
    names=['all_members_by_mouse_v2.png','candidate_features_by_mouse_v2.png','render_metadata.json']
    require(not any((args.output/n).exists() for n in names),'Refuse existing output')
    heatmap(values,mapping,summary['mouse_order'],summary['mouse_days'],limit,args.output/names[0],False)
    heatmap(values,mapping,summary['mouse_order'],summary['mouse_days'],limit,args.output/names[1],True)
    record={'supersedes_figures_in':'analysis/research/runs/A5_feature_context_display_v1_20261104','change':'Candidate height9.5in and bottom margin0.24 prevent xlabel/caption collision; all-member drawing unchanged','shared_color_limit_pp':limit,'mouse_order':summary['mouse_order'],'genes':99,'selected_genes':22,'values_sha256':hashlib.sha256((OLD/'all_member_values.tsv').read_bytes()).hexdigest(),'scope':'Rendering only; no biological recalculation or selection'}
    (args.output/names[2]).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('Rendered two corrected-layout figures from immutable v1 values.')
if __name__=='__main__':main()
