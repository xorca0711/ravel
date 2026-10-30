"""Independent dataframe arithmetic for neutral source-file QC."""
from pathlib import Path
import numpy as np
import pandas as pd

def verify(manifest,exon_records,summary_records,peak_records,universe):
    checks=0;feature_sets=[];zero_sets=[]
    def equal(a,b):
        nonlocal checks
        if a!=b:raise ValueError(f'Independent QC mismatch: {a} versus {b}')
        checks+=1
    er={r['file']:r for r in exon_records};pr={r['file']:r for r in peak_records}
    for item in manifest['files']:
        p=Path(item['path']);d=pd.read_csv(p,sep='\t',header=None,dtype=str,keep_default_na=False)
        if item['kind']=='exon_counts':
            r=er[p.name];equal(d.shape[1],2);equal(len(d),r['rows']);equal(d[0].nunique(),r['unique_ids']);equal(int(d[0].duplicated().sum()),r['duplicate_id_occurrences'])
            values=pd.to_numeric(d[1],errors='coerce');valid=d[1].str.strip().str.fullmatch(r'[+-]?\d+');feature=~d[0].str.startswith('_')
            equal(int((~valid).sum()),r['invalid_integer']);equal(int((values<0).sum()),r['negative_counts']);equal(int(feature.sum()),r['feature_rows']);equal(int(values[feature].sum()),r['feature_count_sum']);equal(int(values[~feature].sum()),r['summary_count_sum']);equal(int((feature&(values==0)).sum()),r['zero_feature_rows'])
            for s in [x for x in summary_records if x['file']==p.name]:equal(int(values[d[0]==s['category']].iloc[0]),s['count'])
            feature_sets.append(set(d.loc[feature,0]));zero_sets.append(set(d.loc[feature&(values==0),0]))
        else:
            r=pr[p.name];equal(d.shape[1],10);equal(len(d),r['rows'])
            start=pd.to_numeric(d[1]);end=pd.to_numeric(d[2]);summit=pd.to_numeric(d[9]);width=end-start
            equal(int((d[0].eq('')|(start<0)|(end<=start)).sum()),r['invalid_coordinates']);equal(int(((summit!=-1)&((summit<0)|(summit>=width))).sum()),r['invalid_summit']);equal(int((~d[5].isin(['.','+','-'])).sum()),r['invalid_strand'])
            equal(int(pd.DataFrame({'chrom':d[0],'start':start,'end':end}).duplicated().sum()),r['duplicate_interval_occurrences']);equal(int(d[0].nunique()),r['chromosome_labels']);equal(float(width.min()),r['width_min']);equal(float(width.median()),r['width_median']);equal(float(width.max()),r['width_max'])
            bad=0
            for col,key in [(4,None),(6,'missing_signal'),(7,'missing_p_field'),(8,'missing_q_field')]:
                missing=(d[col].str.strip().str.lower().isin(['','na','nan'])|pd.to_numeric(d[col],errors='coerce').eq(-1)) if key else pd.Series(False,index=d.index)
                if key:equal(int(missing.sum()),r[key])
                val=pd.to_numeric(d.loc[~missing,col],errors='coerce');bad+=int((~np.isfinite(val)|(val<0)).sum())
            equal(bad,r['invalid_numeric_fields'])
    equal(len(set.union(*feature_sets)),universe['union_features']);equal(len(set.intersection(*feature_sets)),universe['intersection_features'])
    if universe['all_zero_feature_ids'] is not None:equal(len(set.intersection(*zero_sets)),universe['all_zero_feature_ids'])
    return dict(ok=True,checks=checks,method='Independent pandas parsing versus streaming csv/integer/set production; feature/count/summary, interval/width and missing-field arithmetic.',limit='Same deposited files; verifies computation, not biological units, assay equivalence or independent replication.')
