"""A31 fixed eight-partner conditional context on unchanged source cell primitives."""
import argparse,itertools,json,math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PRE=Path('docs/research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites')
OLD=Path('analysis/research/runs/A31_partner_context_v1_20261103')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    spec=json.loads((PRE/'A31_CONDITIONING_MAP_V1.json').read_bytes());keys=spec['keys'];labels=spec['labels'];partners=spec['fixed_partners'];genes=['GRIA1']+partners;data=pd.read_csv(spec['source'],sep='\t')
    if len(data)!=14142 or data.duplicated(['cohort','assay','cell']).any() or data[keys+['cell_type','count_unit']].isna().any().any():raise ValueError('Source identity conflict')
    for col in genes+['library']:
        a=data[col].to_numpy()
        if not (np.isfinite(a).all() and (a>=0).all() and (a==np.floor(a)).all()):raise ValueError('Invalid count domain')
    if not data.library.gt(0).all():raise ValueError('Invalid library')
    if (data[genes].sum(axis=1)>data.library).any():raise ValueError('Targets exceed library')
    # Reconstruct the original immutable all-depth source primitives, without historical code.
    previous=pd.read_csv(OLD/'stratum_gene.tsv',sep='\t');parity=[]
    for kk,g in data.groupby(keys+['cell_type'],sort=True):
        select=previous
        for k,v in zip(keys+['cell_type'],kk):select=select[select[k].eq(v)]
        if set(select.gene)!=set(genes):raise ValueError('Original target roster conflict')
        for gene in genes:
            r=select[select.gene.eq(gene)].iloc[0];vals={'n_cells':len(g),'library':int(g.library.sum()),'sum_count':int(g[gene].sum()),'n_detected':int(g[gene].gt(0).sum())}
            for field,value in vals.items():
                if value!=r[field]:raise ValueError('Original primitive mismatch')
            parity.append(dict(zip(keys+['cell_type'],kk))|dict(gene=gene,**vals))
    pd.DataFrame(parity).to_csv(out/'original_primitive_parity.tsv',sep='\t',index=False)
    use=data[data.cell_type.isin(labels)&(((data.cohort.eq('Travaglini'))&data.region.eq('distal'))|((data.cohort.eq('Madissoon'))&data.region.isin(['Lower Left Lobe','Upper left lobe'])))].copy()
    saved=pd.read_csv(PRE/'A31_DEPTH_SUPPORT_V1.tsv',sep='\t');oldpairs=pd.read_csv(OLD/'paired_strata.tsv',sep='\t');oldpairs=oldpairs[oldpairs.gene.eq('GRIA1')]
    rows=[];strata=[];support=[]
    for kk,g in use.groupby(keys,sort=True):
        common=dict(zip(keys,kk));original=oldpairs
        for k,v in common.items():original=original[original[k].eq(v)]
        if len(original)!=1:raise ValueError('Original attempted stratum roster conflict')
        if g.count_unit.nunique()!=1:raise ValueError('Mixed count units')
        for width in [.5,1.0]:
            block=g.copy();block['depth_bin']=np.floor(np.log2(block.library)/width).astype(int);tab=block.groupby(['depth_bin','cell_type']).size().unstack(fill_value=0).reindex(columns=labels,fill_value=0);kept=tab.index[(tab[labels]>=5).all(axis=1)];nn=[int(g.cell_type.eq(x).sum()) for x in labels];ret=[int((block.cell_type.eq(x)&block.depth_bin.isin(kept)).sum()) for x in labels];ok=min(nn)>=20 and min(ret)>=20
            expected=saved[saved.width_log2.eq(width)]
            for k,v in common.items():expected=expected[expected[k].eq(v)]
            if len(expected)!=1:raise ValueError('Frozen support key conflict')
            s=expected.iloc[0]
            if [*nn,*ret,len(kept),min(nn)>=20,ok]!=[s.n_alveolar,s.n_adventitial,s.common_n_alveolar,s.common_n_adventitial,s.common_bins,s.original_support,s.conditional_support]:raise ValueError('Frozen depth support changed')
            if bool(original.iloc[0].eligible)!=(min(nn)>=20):raise ValueError('Original support changed')
            weights={int(b):int(min(tab.loc[b,labels])) for b in kept};den=sum(weights.values());weights={b:n/den for b,n in weights.items()} if den else {}
            if weights and abs(sum(weights.values())-1)>1e-12:raise ValueError('Weights do not sum to one')
            support.append(common|dict(width_log2=width,primary=width==.5,n_alveolar=nn[0],n_adventitial=nn[1],retained_alveolar=ret[0],retained_adventitial=ret[1],fraction_retained_alveolar=ret[0]/nn[0] if nn[0] else np.nan,fraction_retained_adventitial=ret[1]/nn[1] if nn[1] else np.nan,common_bins=len(kept),eligible=ok,count_unit=g.count_unit.iloc[0]))
            for partner in partners:
                standardized={}
                for label in labels:
                    values=[]
                    for binid in tab.index:
                        z=block[block.cell_type.eq(label)&block.depth_bin.eq(binid)];n=len(z);a=int(z.GRIA1.gt(0).sum());b=int(z[partner].gt(0).sum());j=int((z.GRIA1.gt(0)&z[partner].gt(0)).sum())
                        if not max(0,a+b-n)<=j<=min(a,b):raise ValueError('Joint set bound failure')
                        observed=j/n if n else np.nan;expected_joint=a*b/(n*n) if n else np.nan;residual=observed-expected_joint;w=weights.get(int(binid),0.0)
                        row=common|dict(width_log2=width,partner=partner,cell_type=label,depth_bin=int(binid),depth_lower=2**(int(binid)*width),depth_upper=2**((int(binid)+1)*width),n_cells=n,n_gria1=a,n_partner=b,n_joint=j,p_gria1=a/n if n else np.nan,p_partner=b/n if n else np.nan,observed_joint=observed,expected_joint=expected_joint,residual=residual,shared_bin=binid in kept,weight=w,eligible_stratum=ok,count_unit=g.count_unit.iloc[0]);rows.append(row)
                        if w:values.append((w,row))
                    if ok:
                        standardized[label]={f:sum(w*r[f] for w,r in values) for f in ['p_gria1','p_partner','observed_joint','expected_joint','residual']}
                        independent=sum(r['weight']*(r['n_joint']/r['n_cells']-(r['n_gria1']/r['n_cells'])*(r['n_partner']/r['n_cells'])) for w,r in values)
                        if abs(independent-standardized[label]['residual'])>1e-12:raise ValueError('Scalar residual mismatch')
                row=common|dict(width_log2=width,primary=width==.5,partner=partner,eligible=ok,status='estimated' if ok else 'unestimated_common_depth_support',n_alveolar=nn[0],n_adventitial=nn[1],retained_alveolar=ret[0],retained_adventitial=ret[1],count_unit=g.count_unit.iloc[0])
                for label,short in zip(labels,['alveolar','adventitial']):
                    for f in ['p_gria1','p_partner','observed_joint','expected_joint','residual']:row[short+'_'+f]=standardized[label][f] if ok else np.nan
                row['delta_residual']=row['alveolar_residual']-row['adventitial_residual'];strata.append(row)
    support=pd.DataFrame(support);bins=pd.DataFrame(rows);strata=pd.DataFrame(strata)
    if len(support)!=58 or len(strata)!=464 or support.groupby('width_log2').size().to_dict()!={.5:29,1.0:29}:raise ValueError('Incomplete attempted scope')
    metrics=[x for x in strata.columns if x.startswith(('alveolar_','adventitial_'))]+['delta_residual'];dkeys=['cohort','assay','donor','width_log2','partner'];donor_rows=[]
    for kk,g in strata.groupby(dkeys,sort=True):
        q=g[g.eligible];row=dict(zip(dkeys,kk));row.update(person_key=str(kk[0])+':'+str(kk[2]),eligible=bool(len(q)),n_attempted_strata=len(g),n_eligible_strata=len(q),eligible_stratum_roster=';'.join(q.region.astype(str)+'|'+q.protocol.astype(str)))
        for field in metrics:row[field]=float(q[field].mean()) if len(q) else np.nan
        donor_rows.append(row)
    donors=pd.DataFrame(donor_rows);influence=[]
    for kk,g in donors.groupby(['cohort','assay','width_log2','partner'],sort=True):
        eligible=g[g.eligible]
        for omitted in g.donor:
            remain=eligible[eligible.donor.ne(omitted)];ok=len(eligible)>=2 and omitted in set(eligible.donor)
            influence.append(dict(zip(['cohort','assay','width_log2','partner'],kk))|dict(omitted_donor=omitted,n_original_eligible=len(eligible),n_remaining=len(remain),eligible=ok,full_mean_delta=float(eligible.delta_residual.mean()) if len(eligible) else np.nan,leave_one_out_mean=float(remain.delta_residual.mean()) if ok else np.nan))
    # Finite fixed-margin enumeration validates expected joint detection.
    toy_error=0.0
    for n,a,b in [(5,2,3),(6,1,4),(6,0,3)]:
        reference=set(range(a));mean=np.mean([len(reference&set(choice))/n for choice in itertools.combinations(range(n),b)]);toy_error=max(toy_error,abs(mean-a*b/(n*n)))
    if toy_error>1e-12:raise ValueError('Fixed-margin expectation check failed')
    for frame,name in [(support,'depth_support.tsv'),(bins,'bin_partner_primitives.tsv'),(strata,'stratum_standardized_context.tsv'),(donors,'donor_context.tsv'),(pd.DataFrame(influence),'donor_influence.tsv')]:frame.to_csv(out/name,sep='\t',index=False)
    # All partners and assay contexts; no ranking or selected favorable subset.
    primary=donors[donors.width_log2.eq(.5)&donors.eligible];contexts=list(donors[['cohort','assay']].drop_duplicates().itertuples(index=False,name=None));fig,axes=plt.subplots(len(contexts),len(partners),figsize=(24,3.3*len(contexts)),squeeze=False)
    for i,(cohort,assay) in enumerate(contexts):
        for j,partner in enumerate(partners):
            ax=axes[i,j];g=primary[primary.cohort.eq(cohort)&primary.assay.eq(assay)&primary.partner.eq(partner)]
            for label,marker in [('alveolar','o'),('adventitial','x')]:ax.scatter(100*g[label+'_expected_joint'],100*g[label+'_observed_joint'],marker=marker,label=label,s=25)
            limit=max([1.0]+[float(100*g[c].max()) for c in ['alveolar_expected_joint','adventitial_expected_joint','alveolar_observed_joint','adventitial_observed_joint'] if len(g)]);ax.plot([0,limit],[0,limit],color='grey',lw=.7);ax.set_title(partner+' | '+cohort+' '+assay,fontsize=8);ax.set_xlabel('Marginal-expected joint (%)',fontsize=7);ax.set_ylabel('Observed joint (%)',fontsize=7)
            if not len(g):ax.text(.5,.5,'Unestimated',transform=ax.transAxes,ha='center')
    axes[0,0].legend(fontsize=6);fig.suptitle('A31 primary shared-depth RNA context; points are linked donor/assay summaries, not receptor function',fontsize=12);fig.tight_layout(rect=[0,0,1,.97]);fig.savefig(out/'observed_expected_all_partners.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(2,4,figsize=(16,8),squeeze=False)
    for ax,partner in zip(axes.flat,partners):
        g=primary[primary.partner.eq(partner)];labels_plot=g.cohort+'/'+g.assay+'/'+g.donor;ax.barh(np.arange(len(g)),100*g.delta_residual);ax.set_yticks(np.arange(len(g)),labels_plot,fontsize=6);ax.axvline(0,color='grey',lw=.8);ax.set_title(partner);ax.set_xlabel('Alveolar - adventitial residual (pp)')
    fig.suptitle('All eight fixed partners; residual magnitude depends on both marginal prevalences',fontsize=11);fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(out/'donor_context_all_partners.png',dpi=150);plt.close(fig)
    result=dict(ok=True,original_cells=len(data),original_gene_strata=len(parity),original_primitive_scalar_checks=4*len(parity),attempted_strata_per_width=29,primary_supported_strata=int(support[support.primary].eligible.sum()),coarse_supported_strata=int(support[~support.primary].eligible.sum()),partners=partners,attempted_partner_strata=len(strata),supported_primary_partner_strata=int(strata[strata.primary].eligible.sum()),max_fixed_margin_toy_error=toy_error,limit='Depth-binned conditional RNA association; prevalence-dependent residuals, linked donors, no physical receptor assembly or biological independence claim.')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
