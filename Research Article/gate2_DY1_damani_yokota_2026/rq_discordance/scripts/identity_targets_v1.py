"""Complete fixed-target view of frozen effects; no count-model fitting."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    out=Path(ap.parse_args().output)
    cfg=json.loads(Path('Research Article/gate2_DY1_damani_yokota_2026/rq_discordance/config/identity_targets_spec_v1.json').read_text())
    ids=pd.read_csv(cfg['identifier_source'],sep='\t',usecols=['ensembl_id','gene_name'])
    ids=ids[ids.gene_name.isin(cfg['targets'])].copy()
    assert len(ids)==len(cfg['targets']) and ids.ensembl_id.is_unique and ids.gene_name.is_unique
    assert set(ids.gene_name)==set(cfg['targets'])
    lookup=ids.set_index('ensembl_id').gene_name.to_dict()
    ids.to_csv(out/'target_identifiers.tsv',sep='\t',index=False)
    rnas=[];regions=[];summaries=[];checks=0
    conditions=[('WT_IL4_minus_CTRL','benchmark',None),('cKO_minus_WT_IL4','genotype','IL4'),('cKO_minus_WT_CTRL','genotype','CTRL')]
    for contrast,kind,cond in conditions:
        root=Path(cfg[kind])
        rna_name='rna_descriptive_effects.tsv.gz' if kind=='benchmark' else 'rna_genotype_effects.tsv.gz'
        atac_name='atac_descriptive_effects.tsv.gz' if kind=='benchmark' else 'atac_genotype_effects.tsv.gz'
        rna=pd.read_csv(root/rna_name,sep='\t');atac=pd.read_csv(root/atac_name,sep='\t')
        if kind=='benchmark':rna=rna[rna.offset==cfg['offset']];atac=atac[atac.offset==cfg['offset']]
        else:rna=rna[rna.condition==cond];atac=atac[atac.condition==cond]
        assert rna.feature_id.is_unique and atac.feature_id.is_unique
        q=rna[rna.feature_id.isin(lookup)].copy()
        assert set(q.feature_id)==set(lookup)
        q.insert(0,'gene',q.feature_id.map(lookup));q.insert(0,'contrast',contrast)
        q['source_file']=(root/rna_name).as_posix()
        q['display_lower']=q.sensitivity_lower if kind=='benchmark' else q.conditional_lower
        q['display_upper']=q.sensitivity_upper if kind=='benchmark' else q.conditional_upper
        q['uncertainty_kind']='declared-dependence sensitivity envelope' if kind=='benchmark' else 'independence-conditional Welch interval'
        rnas.append(q)
        member=pd.read_csv(root/'mapping_membership.tsv.gz',sep='\t')
        assert not member.duplicated(['peak_id','gene_id','mapping_rule','distance_subset']).any()
        selected=member[member.gene_id.isin(lookup)].copy()
        z=selected.merge(atac,left_on='peak_id',right_on='feature_id',validate='many_to_one')
        assert len(z)==len(selected)
        z.insert(0,'gene',z.gene_id.map(lookup));z.insert(0,'contrast',contrast)
        z['source_file']=(root/atac_name).as_posix();regions.append(z)
        for rule,sub in member[['mapping_rule','distance_subset']].drop_duplicates().itertuples(index=False,name=None):
            for gene in cfg['targets']:
                v=z[(z.gene==gene)&(z.mapping_rule==rule)&(z.distance_subset==sub)]
                d=v.mean_delta
                summaries.append(dict(contrast=contrast,gene=gene,mapping_rule=rule,distance_subset=sub,n_regions=len(v),positive=int((d>0).sum()),negative=int((d<0).sum()),zero=int((d==0).sum()),min_delta=float(d.min()) if len(v) else None,max_delta=float(d.max()) if len(v) else None))
                assert int((d>0).sum()+(d<0).sum()+(d==0).sum())==len(v);checks+=1
        # Verify every copied field against its exact immutable source row.
        for original,target,join_col in [(rna,q,'feature_id'),(atac,z,'feature_id')]:
            expected=original.set_index('feature_id').loc[target[join_col]]
            for column in original.columns.drop('feature_id'):
                a=expected[column].reset_index(drop=True);b=target[column].reset_index(drop=True)
                pd.testing.assert_series_equal(a,b,check_names=False);checks+=len(a)
    rnas=pd.concat(rnas,ignore_index=True);regions=pd.concat(regions,ignore_index=True);summaries=pd.DataFrame(summaries)
    rnas.to_csv(out/'target_rna_effects.tsv',sep='\t',index=False)
    regions.to_csv(out/'target_region_effects.tsv',sep='\t',index=False)
    summaries.to_csv(out/'target_region_summary.tsv',sep='\t',index=False)
    fig,axes=plt.subplots(2,3,figsize=(15,8),sharey=True)
    yy=np.arange(len(cfg['targets']))
    for col,(contrast,_,_) in enumerate(conditions):
        q=rnas[rnas.contrast==contrast].set_index('gene').loc[cfg['targets']]
        ax=axes[0,col]
        for j,row in enumerate(q.itertuples()):
            if np.isfinite(row.display_lower) and np.isfinite(row.display_upper):ax.plot([row.display_lower,row.display_upper],[j,j],color='#5d6d7e',lw=2)
            ax.plot(row.mean_delta,j,'o',color='#21618c')
        ax.set_title(contrast.replace('_',' ')+'\nRNA (inherited conditional uncertainty)')
        ax=axes[1,col]
        # All broad author-Ensembl regions; full second mapping and proximal subset in tables.
        rules=regions.mapping_rule.unique().tolist()
        rule=next(x for x in rules if 'ensembl' in x.lower())
        subsets=regions.distance_subset.unique().tolist();broad=next(x for x in subsets if 'all' in x.lower())
        for j,gene in enumerate(cfg['targets']):
            q=regions[(regions.contrast==contrast)&(regions.gene==gene)&(regions.mapping_rule==rule)&(regions.distance_subset==broad)]
            jitter=np.linspace(-.15,.15,len(q)) if len(q)>1 else np.zeros(len(q))
            ax.scatter(q.mean_delta,j+jitter,s=15,color='#a04000',alpha=.65)
        ax.set_title('ATAC point estimates: broad author-Ensembl regions')
        for ax in axes[:,col]:ax.axvline(0,color='grey',lw=.8);ax.set_xlabel('Difference in mean log2(1 + CPM)');ax.grid(axis='x',alpha=.2)
    axes[0,0].set_yticks(yy,cfg['targets']);axes[0,0].invert_yaxis()
    fig.suptitle('Non-infectious reference: fixed identity-target RNA and accessibility',fontsize=16)
    fig.text(.5,.015,'Separate assay scales; region dots are dependent features. No NAM mechanism, regulon activity, occupancy, memory or population-CI claim.',ha='center',fontsize=10)
    fig.tight_layout(rect=[0,.05,1,.94]);fig.savefig(out/'identity_targets.png',dpi=170);plt.close(fig)
    info={'verification_passed':True,'copied_value_checks':checks,'targets':cfg['targets'],'rna_rows':len(rnas),'region_rows_with_mapping_subsets':len(regions),'summary_rows':len(summaries),'source_reused':True,'inference':'Conditional descriptive reference only; no new population or causal inference.'}
    (out/'verification.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))

if __name__=='__main__':main()
