"""Exposed, mouse-level CD4/CD8 repertoire contrasts after exact source joining."""
from pathlib import Path
import argparse, importlib.util, itertools, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def module(filename,name):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
bio=module('09_biological_extensions_v1.py','prior_bio')
figstyle=module('11_extension_figures_v2.py','prior_style')
AGES=[3,18,24]
TYPES={'CD4':'CD4-positive, alpha-beta T cell','CD8':'CD8-positive, alpha-beta T cell'}
TISSUES=['Thymus','Spleen','Marrow']

def main(out):
    d=pd.read_csv(ROOT/'analysis/research/runs/nb5_completion_metadata_v2/repertoire_annotation_join.tsv',sep='\t',keep_default_na=False)
    # Keep the prior biological cohort exactly; newly bridged formerly unassigned rows
    # are qualification evidence, not a silent expansion of this contrast.
    d=d[d.mouse_id!=''].copy();assert len(d)==6000
    d['clone_key']=['source:'+str(g) if str(g) else 'singleton:'+str(c) for g,c in zip(d.clonal_group,d.cell_name)]
    global_n=d.groupby(['age_months','mouse_id','clone_key']).cell_name.transform('size')
    assert (global_n==d.within_mouse_clone_size).all()
    coverage=d.groupby(['age_months','mouse_id','tissue','join_rule','official_cell_ontology_class'],dropna=False).size().rename('cells').reset_index()
    rows=[];support=[];counts={}
    for tissue,subtype in itertools.product(TISSUES,TYPES):
        cells=d[(d.tissue==tissue)&(d.official_cell_ontology_class==TYPES[subtype])]
        per=[]
        for (age,mouse),g in cells.groupby(['age_months','mouse_id']):
            sizes=g.groupby('clone_key').size().tolist()
            n=sum(sizes);repeated=sum(k for k in sizes if k>1)
            independently=int((g.groupby('clone_key').cell_name.transform('size')>1).sum())
            assert repeated==independently
            row=dict(tissue=tissue,subtype=subtype,age_months=int(age),mouse_id=mouse,cells=n,clone_cells=repeated,local_fraction=repeated/n)
            per.append(row);counts[(tissue,subtype,int(age),mouse)]=sizes
        depth=min((x['cells'] for x in per),default=0)
        animal_counts={a:sum(x['age_months']==a for x in per) for a in AGES}
        eligible=all(animal_counts[a]>=2 for a in AGES) and depth>=2
        for age in AGES:
            a=[x for x in per if x['age_months']==age]
            support.append(dict(tissue=tissue,subtype=subtype,age_months=age,mice=len(a),cells=sum(x['cells'] for x in a),depth=depth,eligible=eligible,reason='supported descriptive comparison' if eligible else 'missing age support, fewer than two mice, or depth below two'))
        for row in per:
            row['eligible']=eligible;row['depth']=depth if eligible else np.nan
            row['common_depth_fraction']=bio.rarefaction(counts[(tissue,subtype,row['age_months'],row['mouse_id'])],depth) if eligible else np.nan
            if eligible: assert 0<=row['common_depth_fraction']<=row['local_fraction']+1e-12
            rows.append(row)
    mice=pd.DataFrame(rows);support=pd.DataFrame(support)
    summaries=[];contrasts=[];deletions=[]
    for (tissue,subtype),group in mice[mice.eligible].groupby(['tissue','subtype']):
        for endpoint in ['local_fraction','common_depth_fraction']:
            means=group.groupby('age_months')[endpoint].mean()
            for age,g in group.groupby('age_months'):
                summaries.append(dict(tissue=tissue,subtype=subtype,endpoint=endpoint,age_months=int(age),mice=len(g),mean=float(g[endpoint].mean()),min=float(g[endpoint].min()),max=float(g[endpoint].max()),depth=int(g.depth.iloc[0])))
            for age in [18,24]:
                contrast=100*(means[age]-means[3])
                contrasts.append(dict(tissue=tissue,subtype=subtype,endpoint=endpoint,age_months=age,difference_pp=float(contrast)))
                selected=group[group.age_months.isin([3,age])]
                for _,row in selected.iterrows():
                    remain=selected[selected.mouse_id!=row.mouse_id]
                    # Frozen all-mouse depth is retained across deletions.
                    m=remain.groupby('age_months')[endpoint].mean()
                    deletions.append(dict(tissue=tissue,subtype=subtype,endpoint=endpoint,age_months=age,omitted_mouse=row.mouse_id,omitted_age=int(row.age_months),difference_pp=float(100*(m[age]-m[3]))))
    contrasts=pd.DataFrame(contrasts)
    for name,table in [('cohort_annotation_coverage',coverage),('subtype_support',support),('subtype_mouse',mice),('subtype_summary',pd.DataFrame(summaries)),('subtype_contrasts',contrasts),('leave_one_mouse_out',pd.DataFrame(deletions))]:
        table.to_csv(out/(name+'.tsv'),sep='\t',index=False,lineterminator='\n')
    bio.toy_checks()
    # Independent finite enumeration validates the conditional endpoint at >1 depth.
    toy=[0,0,0,1,1,2]
    for depth in [2,3,4]:
        expected=np.mean([sum(s.count(x)>1 for x in s)/depth for s in itertools.combinations(toy,depth)])
        assert np.isclose(expected,bio.rarefaction([3,2,1],depth))
    eligible=support[support.eligible][['tissue','subtype']].drop_duplicates()
    figure_manifest={'eligible_strata':eligible.to_dict('records'),'files':[]}
    if len(eligible):
        fig,axes=plt.subplots(2,len(eligible),figsize=(4.0*len(eligible),7.0),squeeze=False)
        fig.subplots_adjust(left=.075,right=.98,top=.91,bottom=.18,hspace=.65,wspace=.42)
        for i,row in enumerate(eligible.itertuples()):
            g=mice[(mice.tissue==row.tissue)&(mice.subtype==row.subtype)]
            for j,endpoint in enumerate(['local_fraction','common_depth_fraction']):
                ax=axes[j,i];figstyle.ageplot(ax,g,endpoint,'Cells in repeated clones (%)')
                title=f'{row.tissue} {row.subtype}' + (' | observed' if j==0 else f' | depth {int(g.depth.iloc[0])}')
                figstyle.panel(ax,chr(65+j*len(eligible)+i),title)
        spleen=contrasts.query("tissue == 'Spleen' and endpoint == 'common_depth_fraction' and age_months == 24").set_index('subtype')
        result=', '.join(f'{s} {spleen.loc[s,"difference_pp"]:+.1f}' for s in TYPES if s in spleen.index)
        caption=f'Figure 11. Subtype restriction tests whether older clone concentration reflects CD4/CD8 mixture. Fixed-depth spleen contrasts at 24 versus 3 months are {result} percentage points. Points are mice; bars are means. Source annotations, sparse strata and unmeasured receptor recovery limit biological interpretation.'
        figstyle.footer(fig,caption)
        for ext in ['png','svg','pdf']:
            name='11_subtype_repertoire.'+ext;fig.savefig(out/name,dpi=300);figure_manifest['files'].append(name)
        figure_manifest.update(caption=caption,layout=fig._caption_qa)
        plt.close(fig)
    (out/'figure_manifest.json').write_text(json.dumps(figure_manifest,indent=2)+'\n',encoding='utf-8')
    checks={'passed':True,'prior_cohort_cells':len(d),'eligible_comparisons':len(eligible),'checks':['Exact prior within-mouse clone-size reconstruction','Independent repeated-cell numerator calculation','Conditional common-depth bounds','Exhaustive sampling checks for three depths','Prior analytic decomposition and rarefaction toys'],'limit':'Repeated reconstructed sequences conditional on source annotation and recovery; no immune-function, absolute-expansion or independent-validation claim.'}
    (out/'verification.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
