"""A5 source-fixed descriptive display of immutable member estimates."""
from pathlib import Path
import argparse, hashlib, json, shutil
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
PRE = ROOT / 'docs/research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites'
OLD = ROOT / 'analysis/research/runs/A5_component_attribution_v1_20261103'
MODULES = {'Guo_AT1_AT2_external': ('in_99', 99), 'Guo_minus_identity': ('in_57', 57), 'Guo_minus_identity_and_controls': ('in_53', 53)}
LABELS = {'AT2 activated', 'Krt8+ ADI'}


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(values, mapping, support, units, modules):
    require(not mapping.gene.duplicated().any(), 'Duplicate map gene')
    require(set(values.gene) == set(mapping.gene), 'Changed member roster')
    require(set(values.sample_id) == set(units), 'Changed mouse roster')
    require(not values.duplicated(['sample_id', 'gene']).any(), 'Duplicate mouse/gene')
    require(len(values) == len(units) * len(mapping), 'Missing mouse/gene')
    require(set(mapping.display_order) == set(range(1, len(mapping)+1)), 'Invalid row order')
    require(not support.duplicated(['sample_id', 'label']).any(), 'Duplicate support')
    eligible = support[support.paired_eligible.astype(str).str.lower().eq('true')].copy()
    require(set(eligible.sample_id) == set(units), 'Eligibility mismatch')
    days = {}
    for mouse in units:
        part = eligible[eligible.sample_id.eq(mouse)]
        require(set(part.label) == LABELS and len(part) == 2, 'Unpaired support')
        require(part.day.nunique() == 1, 'Inconsistent day')
        require((part.cells_after_depth >= 30).all(), 'Changed cell floor')
        days[mouse] = int(part.day.iloc[0])
    joined = values.merge(mapping, on='gene', how='left', validate='many_to_one')
    require(np.isfinite(joined.delta_detection_pp).all(), 'Nonfinite endpoint')
    error = 0.0
    for column, (membership, size) in modules.items():
        require(int(mapping[membership].sum()) == size, 'Changed module size')
        expected = joined.delta_detection_pp.to_numpy() * joined[membership].to_numpy() / size
        require(np.isfinite(joined[column]).all(), 'Nonfinite contribution')
        error = max(error, float(np.max(np.abs(joined[column].to_numpy() - expected))))
    require(error <= 1e-10, 'Contribution/nonmember arithmetic mismatch')
    joined['day'] = joined.sample_id.map(days)
    order = sorted(units, key=lambda x: (days[x], x))
    joined['mouse_order'] = joined.sample_id.map({m: i for i,m in enumerate(order)})
    return joined.sort_values(['display_order','mouse_order']), order, days, error


def summarize(joined, modules):
    rows = []
    daily = []
    for gene, part in joined.groupby('gene', sort=False):
        x = part.delta_detection_pp
        row = {'gene': gene, 'display_order': int(part.display_order.iloc[0]), 'display_group': part.display_group.iloc[0], 'n_mice': len(part), 'mean_delta_detection_pp': float(x.mean()), 'min_delta_detection_pp': float(x.min()), 'max_delta_detection_pp': float(x.max()), 'positive_mice': int((x>0).sum()), 'negative_mice': int((x<0).sum()), 'exact_zero_mice': int((x==0).sum())}
        for column,(membership,_) in modules.items():
            included = int(part[membership].iloc[0])
            row[membership] = included
            row['mean_contribution_' + column] = float(part[column].mean()) if included else np.nan
        rows.append(row)
        for day, q in part.groupby('day', sort=True):
            y=q.delta_detection_pp
            daily.append({'gene':gene,'display_order':row['display_order'],'day':int(day),'n_mice':len(q),'mean_delta_detection_pp':float(y.mean()),'min_delta_detection_pp':float(y.min()),'max_delta_detection_pp':float(y.max()),'positive_mice':int((y>0).sum()),'negative_mice':int((y<0).sum()),'exact_zero_mice':int((y==0).sum())})
    return pd.DataFrame(rows), pd.DataFrame(daily)


def heatmap(joined, mapping, mice, days, limit, output, selected):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    chosen = mapping[mapping.candidate_panel.astype(str).str.lower().eq('true')] if selected else mapping
    chosen = chosen.sort_values('display_order')
    data = joined.pivot(index='gene', columns='sample_id', values='delta_detection_pp').loc[chosen.gene, mice]
    require(not data.isna().any().any(), 'Missing plotted value')
    fig, ax = plt.subplots(figsize=(15, max(8, len(chosen)*.25+3)))
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
    fig.subplots_adjust(left=.10,right=.70,bottom=.15,top=.93)
    cax=fig.add_axes([.82,.10,.13,.012]);fig.colorbar(img,cax=cax,orientation='horizontal',label='Detection difference (percentage points)')
    caption='Shared unclipped scale across all 99 genes. Selected 22 are a display, not an exhaustive biological inventory.\nSource roles can overlap; cross-tissue/inferred annotations do not demonstrate function in repair.\nPpl has junction-related keratinocyte/desmosome context; peripheral placement does not mean absent function.'
    fig.text(.10,.025,caption,fontsize=8,va='bottom')
    fig.savefig(output,dpi=160,facecolor='white');plt.close(fig)


def self_test():
    mapping=pd.DataFrame({'gene':['b','a'],'display_order':[2,1],'display_group':['g','g'],'in_99':[1,1],'in_57':[0,1],'in_53':[0,1]})
    values=pd.DataFrame({'sample_id':['late','late','early','early'],'gene':['a','b','a','b'],'delta_detection_pp':[2.,-2.,-1.,0.],'Guo_AT1_AT2_external':[1.,-1.,-.5,0.],'Guo_minus_identity':[2.,0.,-1.,0.],'Guo_minus_identity_and_controls':[2.,0.,-1.,0.]})
    support=pd.DataFrame([{'sample_id':m,'day':d,'label':l,'cells_after_depth':30,'paired_eligible':True} for m,d in [('late',10),('early',2)] for l in LABELS])
    modules={k:(v[0],2 if i==0 else 1) for i,(k,v) in enumerate(MODULES.items())}
    out,order,_,err=validate(values,mapping,support,['late','early'],modules)
    require(order==['early','late'] and out.gene.tolist()==['a','a','b','b'] and err==0,'Ordering fixture failed')
    summary,_=summarize(out,modules)
    require(np.isnan(summary.loc[summary.gene.eq('b'),'mean_contribution_Guo_minus_identity'].iloc[0]),'Excluded member was biological zero')
    require(summary.loc[summary.gene.eq('a'),'mean_delta_detection_pp'].iloc[0]==.5,'Mouse mean fixture')
    failures=[]
    bad=values.copy();bad.loc[1,'Guo_minus_identity']=1
    failures.append((bad,support))
    failures.append((pd.concat([values,values.iloc[[0]]]),support))
    low=support.copy();low.loc[0,'cells_after_depth']=29;failures.append((values,low))
    for v,s in failures:
        try:validate(v,mapping,s,['late','early'],modules)
        except ValueError:pass
        else:raise AssertionError('Invalid fixture accepted')
    print('Synthetic checks passed: joins, exact ordering, mouse means, excluded-member NA, duplicate/floor/arithmetic rejection.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    if args.self_test:self_test();return
    require(args.output is not None,'--output required')
    manifest=json.loads((PRE/'A5_FEATURE_DISPLAY_INPUTS_V1.json').read_text(encoding='utf-8'))
    for relative, expected in manifest['sha256'].items():require(sha(ROOT/relative)==expected,'Input hash mismatch: '+relative)
    mapping=pd.read_csv(PRE/'A5_FEATURE_DISPLAY_MAP_V1.tsv',sep='\t',keep_default_na=False)
    cross=pd.read_csv(PRE/'A5_ROLE_SCOPE_CROSSWALK_V2.tsv',sep='\t',keep_default_na=False)
    prior=json.loads((ROOT/'analysis/research/contracts/A5.component_attribution_v1.json').read_text(encoding='utf-8'))
    units=prior['inputs'][0]['unit_ids'];require(len(units)==24 and len(mapping)==99,'Changed fixed counts')
    require(mapping.set_index('gene').original_v1_roles.to_dict()==cross.set_index('original_gene').v1_roles.to_dict(),'Original role drift')
    require(mapping.candidate_panel.astype(str).str.lower().eq('true').sum()==22,'Changed candidate selection')
    values=pd.read_csv(OLD/'member_contributions.tsv',sep='\t',keep_default_na=False)
    support=pd.read_csv(OLD/'unit_support.tsv',sep='\t',keep_default_na=False)
    merged,mice,days,error=validate(values,mapping,support,units,MODULES)
    require(merged.roles.eq(merged.original_v1_roles).all(),'Existing member role drift')
    summary,daily=summarize(merged,MODULES)
    output=args.output;output.mkdir(parents=True,exist_ok=True)
    expected=['all_member_values.tsv','gene_summary.tsv','gene_day_summary.tsv','support.tsv','source_role_crosswalk.tsv','all_members_by_mouse.png','candidate_features_by_mouse.png','summary.json']
    require(not any((output/n).exists() for n in expected),'Refuse existing output')
    merged.drop(columns=['GO_qualifier_evidence_reference']).to_csv(output/'all_member_values.tsv',sep='\t',index=False,lineterminator='\n')
    summary.to_csv(output/'gene_summary.tsv',sep='\t',index=False,na_rep='NA',lineterminator='\n');daily.to_csv(output/'gene_day_summary.tsv',sep='\t',index=False,lineterminator='\n')
    support['included_in_display']=support.sample_id.isin(units);support.to_csv(output/'support.tsv',sep='\t',index=False,lineterminator='\n');shutil.copyfile(PRE/'A5_ROLE_SCOPE_CROSSWALK_V2.tsv',output/'source_role_crosswalk.tsv')
    limit=float(np.abs(merged.delta_detection_pp).max());limit=limit if limit>0 else 1.0
    heatmap(merged,mapping,mice,days,limit,output/'all_members_by_mouse.png',False);heatmap(merged,mapping,mice,days,limit,output/'candidate_features_by_mouse.png',True)
    result={'analysis_id':'A5.feature_context_display_v1','mice':len(mice),'genes':len(mapping),'candidate_genes':22,'member_mouse_rows':len(merged),'gene_day_rows':len(daily),'mouse_order':mice,'mouse_days':days,'maximum_contribution_parity_error':error,'shared_color_limit_pp':limit,'input_sha256':manifest['sha256'],'source_receipt':'analysis/research/runs/A5_component_attribution_v1_20261103/receipt.json','scope':'Exposed descriptive existing-output view; no causal score, group total, inferential test or biological acceptance'}
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['mice','genes','candidate_genes','member_mouse_rows','maximum_contribution_parity_error']}))


if __name__=='__main__':main()
