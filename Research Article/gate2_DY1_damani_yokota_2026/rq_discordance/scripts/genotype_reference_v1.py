"""F4: separate source-labelled cKO-minus-WT descriptive contrasts."""
import argparse
import json
import math
from pathlib import Path
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, t

RAW=Path('raw_data/DY1_P02_reference_source_v1')
QUAL=Path('analysis/research/runs/DY1_P02_reference_source_v1')
CONFIG=Path('Research Article/gate2_DY1_damani_yokota_2026/rq_discordance/config/genotype_reference_parameters_v1.json')


def welch(wt,ko):
    if wt.ndim!=2 or ko.ndim!=2 or wt.shape[0]!=ko.shape[0] or min(wt.shape[1],ko.shape[1])<2:
        raise ValueError('Two groups, same feature rows, each n >=2 required')
    if not np.isfinite(wt).all() or not np.isfinite(ko).all():raise ValueError('Nonfinite observations')
    n,m=wt.shape[1],ko.shape[1]
    vx,vy=wt.var(axis=1,ddof=1),ko.var(axis=1,ddof=1)
    a,b=vx/n,vy/m;se=np.sqrt(a+b)
    df=np.full(len(se),np.nan);den=a*a/(n-1)+b*b/(m-1)
    np.divide((a+b)**2,den,out=df,where=(se>1e-12)&(den>0))
    delta=ko.mean(axis=1)-wt.mean(axis=1);half=t.isf(.025,df)*se
    return pd.DataFrame(dict(wt_n=n,cko_n=m,wt_mean=wt.mean(axis=1),cko_mean=ko.mean(axis=1),
        wt_sd=np.sqrt(vx),cko_sd=np.sqrt(vy),mean_delta=delta,se=se,welch_df=df,
        conditional_lower=delta-half,conditional_upper=delta+half,degenerate=~np.isfinite(half)))


def scalar_check(counts,totals,ci,ti,result):
    checks=0
    for pos in np.unique(np.linspace(0,len(counts)-1,min(40,len(counts)),dtype=int)):
        x=[math.log2(1+1e6*int(counts[pos,j])/int(totals[j])) for j in ci]
        y=[math.log2(1+1e6*int(counts[pos,j])/int(totals[j])) for j in ti]
        a,b=statistics.variance(x)/len(x),statistics.variance(y)/len(y)
        se=math.sqrt(a+b);delta=statistics.mean(y)-statistics.mean(x)
        vals={'mean_delta':delta,'wt_mean':statistics.mean(x),'cko_mean':statistics.mean(y),
              'wt_sd':statistics.stdev(x),'cko_sd':statistics.stdev(y),'se':se}
        if se>1e-12:
            df=(a+b)**2/(a*a/(len(x)-1)+b*b/(len(y)-1));h=float(t.isf(.025,df))*se
            vals.update(welch_df=df,conditional_lower=delta-h,conditional_upper=delta+h)
        else:
            assert bool(result.iloc[pos].degenerate);checks+=1
        for k,v in vals.items():
            if not math.isclose(float(result.iloc[pos][k]),v,rel_tol=1e-9,abs_tol=1e-10):raise ValueError('Scalar disagreement: '+k)
            checks+=1
    return checks


def summarize(r,a,genes):
    x,y=r.mean_delta.to_numpy(),a.mean_delta.to_numpy()
    cls=np.where((x==0)|(y==0),0,np.where(np.sign(x)==np.sign(y),1,-1))
    by_gene=pd.DataFrame({'gene':genes,'same':cls==1}).groupby('gene').same.mean()
    rho=float(spearmanr(x,y).statistic) if len(np.unique(x))>1 and len(np.unique(y))>1 else None
    directional=(~r.degenerate.to_numpy())&(~a.degenerate.to_numpy())&((r.conditional_lower.to_numpy()>0)|(r.conditional_upper.to_numpy()<0))&((a.conditional_lower.to_numpy()>0)|(a.conditional_upper.to_numpy()<0))
    return dict(pair_rows=len(x),unique_genes=len(by_gene),same=int((cls==1).sum()),opposite=int((cls==-1).sum()),zero=int((cls==0).sum()),
        pair_weighted_same=float((cls==1).mean()),equal_gene_same=float(by_gene.mean()),mapped_row_spearman=rho,
        both_conditional_intervals_exclude_zero=int(directional.sum()))


def main(out):
    out.mkdir(parents=True,exist_ok=True);cfg=json.loads(CONFIG.read_text())
    samples=pd.read_csv(QUAL/'sample_map.tsv',sep='\t',keep_default_na=False)
    selected=samples[samples.condition.isin(['IL4','CTRL'])&samples.genotype.isin(['WT','KO'])].copy()
    expected=cfg['sample_columns']
    for study,g in selected.groupby('study'):
        if sorted(g.matrix_column)!=sorted(expected[study]):raise ValueError('Sample selection mismatch')
    selected.to_csv(out/'selected_source_samples.tsv',sep='\t',index=False)
    rna=pd.read_csv(RAW/'GSE247223_countMatrixUpdated.tsv.gz',sep='\t',keep_default_na=False)
    atac=pd.read_csv(RAW/'GSE248042_Chinenov_Deochand_submission_ATACseq_peak_count_matrix.csv.gz',keep_default_na=False)
    annotation=pd.read_csv(QUAL/'author_annotation_map.tsv',sep='\t',keep_default_na=False)
    effects={};eligibility=[];denominators=[];checks=0;feature_summaries=[]
    for assay,study,frame,key in [('RNA','GSE247223',rna,'ensembl_id'),('ATAC','GSE248042',atac,'peak_id')]:
        if frame[key].duplicated().any():raise ValueError('Duplicate feature ID')
        group=selected[selected.study==study];cols=group.matrix_column.tolist()
        raw=frame[cols].to_numpy(dtype=float)
        if not np.isfinite(raw).all() or (raw<0).any() or not np.equal(raw,np.floor(raw)).all():raise ValueError('Invalid counts')
        counts=raw.astype(np.int64);totals=counts.sum(axis=0)
        if (totals<=0).any():raise ValueError('Empty library')
        keep=(counts>0).any(axis=1);counts=counts[keep];ids=frame.loc[keep,key].to_numpy()
        transformed=np.log2(1+1e6*counts/totals[None,:])
        for col,total in zip(cols,totals):denominators.append(dict(assay=assay,column=col,all_source_feature_counts=int(total)))
        for condition in ['IL4','CTRL']:
            ci=np.flatnonzero(((group.condition==condition)&(group.genotype=='WT')).to_numpy())
            ti=np.flatnonzero(((group.condition==condition)&(group.genotype=='KO')).to_numpy())
            expected_n=cfg['group_sizes'][assay][condition]
            if [len(ci),len(ti)]!=expected_n:raise ValueError('Group n mismatch')
            result=welch(transformed[:,ci],transformed[:,ti]);checks+=scalar_check(counts,totals,ci,ti,result)
            result.insert(0,'feature_id',ids);result.insert(1,'condition',condition)
            result['all_zero_in_this_condition']=(counts[:,np.r_[ci,ti]]==0).all(axis=1)
            effects[(assay,condition)]=result.set_index('feature_id',drop=False)
            eligibility.append(dict(assay=assay,condition=condition,source_features=len(frame),common_eligible_features=int(keep.sum()),
                all_zero_all_four_groups=int((~keep).sum()),retained_all_zero_this_condition=int(result.all_zero_in_this_condition.sum()),wt_n=len(ci),cko_n=len(ti)))
            feature_summaries.append(dict(assay=assay,condition=condition,features=len(result),positive=int((result.mean_delta>0).sum()),negative=int((result.mean_delta<0).sum()),zero=int((result.mean_delta==0).sum()),degenerate=int(result.degenerate.sum()),median_delta=float(result.mean_delta.median())))
        combined=pd.concat([effects[(assay,c)] for c in ['IL4','CTRL']],ignore_index=True).sort_values(['feature_id','condition'])
        combined.to_csv(out/f'{assay.lower()}_genotype_effects.tsv.gz',sep='\t',index=False,compression={'method':'gzip','mtime':0},na_rep='NA')
    if rna.gene_name.duplicated().any():raise ValueError('Ambiguous nearest-symbol mapping')
    symbols=dict(zip(rna.gene_name,rna.ensembl_id));mapping=[];summaries=[]
    for rule in ['author_ensembl','author_nearest_tss_symbol']:
        genes=annotation.ensemble_id if rule=='author_ensembl' else annotation.nearest_tss_symbol.map(symbols)
        pairs=pd.DataFrame({'peak_id':annotation.peak_id,'gene_id':genes,'dist_to_tss':pd.to_numeric(annotation.dist_to_tss,errors='coerce')})
        for subset in ['all_author_annotated','within_2kb_of_nearest_tss']:
            candidate=pairs if subset=='all_author_annotated' else pairs[pairs.dist_to_tss.abs()<=2000]
            for condition in ['IL4','CTRL']:
                re,ae=effects[('RNA',condition)],effects[('ATAC',condition)]
                joined=candidate[candidate.gene_id.isin(re.index)&candidate.peak_id.isin(ae.index)]
                if joined.empty or joined.peak_id.duplicated().any():raise ValueError('Invalid mapping')
                rp,ap=re.loc[joined.gene_id],ae.loc[joined.peak_id]
                stat=summarize(rp,ap,joined.gene_id.to_numpy())
                # Independent scalar sign partition and rank-Pearson Spearman check.
                counts=[0,0,0]
                for x,y in zip(rp.mean_delta,ap.mean_delta):counts[2 if x==0 or y==0 else (0 if (x>0)==(y>0) else 1)]+=1
                assert counts==[stat['same'],stat['opposite'],stat['zero']];checks+=3
                rx=rp.mean_delta.rank(method='average').to_numpy();ry=ap.mean_delta.rank(method='average').to_numpy()
                if stat['mapped_row_spearman'] is not None:
                    assert math.isclose(float(np.corrcoef(rx,ry)[0,1]),stat['mapped_row_spearman'],abs_tol=1e-12);checks+=1
                summaries.append(dict(condition=condition,mapping_rule=rule,distance_subset=subset,candidate_regions=len(candidate),**stat))
                if condition=='IL4':mapping.append(joined.assign(mapping_rule=rule,distance_subset=subset))
    pd.concat(mapping,ignore_index=True).to_csv(out/'mapping_membership.tsv.gz',sep='\t',index=False,compression={'method':'gzip','mtime':0})
    for n,rows in [('feature_eligibility.tsv',eligibility),('library_denominators.tsv',denominators),('feature_summary.tsv',feature_summaries),('mapping_summary.tsv',summaries)]:
        pd.DataFrame(rows).to_csv(out/n,sep='\t',index=False)
    fig,ax=plt.subplots(1,2,figsize=(11,5),layout='constrained')
    for axis,condition in zip(ax,['IL4','CTRL']):
        s=pd.DataFrame(summaries);s=s[s.condition==condition];x=np.arange(len(s))
        axis.bar(x,s.same/s.pair_rows,label='Same nonzero sign');axis.bar(x,s.opposite/s.pair_rows,bottom=s.same/s.pair_rows,label='Opposite nonzero sign')
        axis.bar(x,s.zero/s.pair_rows,bottom=(s.same+s.opposite)/s.pair_rows,label='One or both zero')
        axis.set(ylim=(0,1),xticks=x,xticklabels=['Ensembl\nall','Ensembl\n<=2 kb','Nearest\nall','Nearest\n<=2 kb'],title=condition+' source labels',ylabel='Fraction of mapped dependent rows')
    ax[1].legend(fontsize=8,loc='lower right');fig.suptitle('External reference: cKO minus WT within each condition\nSeparate assays; descriptive direction comparison, no interaction estimate',fontsize=11)
    fig.savefig(out/'genotype_reference.png',dpi=150);plt.close(fig)
    (out/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'method':'Fixed 40 source-order rows/assay/condition scalar logCPM, means, variances and unequal-n Welch; all mapping partitions and rank correlations'},indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps({'analysis_id':'DY1-P02.genotype_reference_v1','offset':1,'contrast':'cKO minus WT separately within source-labelled IL4 and CTRL','intervals':'95% independent-normal-observation Welch conditional intervals; unknown dependence and batches remain','source_discrepancy':'Fig5c broadly cKO n4; deposited IL4 RNA only rep1,rep2,rep4; no fourth imputed','scientific_acceptance':'not_assessed'},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
