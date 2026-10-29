"""Donor-level descriptive statistics; no cell-level population inference."""
import numpy as np
from scipy.stats import rankdata


def log_cpm(counts, total):
    counts=np.asarray(counts,dtype=float);total=np.asarray(total,dtype=float)
    if np.any(total<=0) or np.any(counts<0) or np.any(counts.sum(axis=-1)>total):
        raise ValueError('Invalid all-gene CPM denominator')
    return np.log2(1+counts/total[...,None]*1e6)


def mean_difference(a,b,rng,repetitions=2000):
    a=np.asarray(a,float);b=np.asarray(b,float)
    result={'ci_low':np.nan,'ci_high':np.nan,'bootstrap_requested':repetitions,'bootstrap_valid_replicates':0,
            'bootstrap_constant_replicates':0,'ci_status':'fewer_than_3_donors'}
    if min(len(a),len(b))<3:return result
    aa=a[rng.integers(len(a),size=(repetitions,len(a)))];bb=b[rng.integers(len(b),size=(repetitions,len(b)))]
    samples=aa.mean(axis=1)-bb.mean(axis=1)
    result['bootstrap_valid_replicates']=repetitions
    result['bootstrap_constant_replicates']=int(((np.ptp(aa,axis=1)==0)&(np.ptp(bb,axis=1)==0)).sum())
    if np.ptp(samples)==0:return dict(result,ci_status='constant_bootstrap_distribution')
    result['ci_low'],result['ci_high']=np.quantile(samples,[.025,.975])
    return dict(result,ci_status='pointwise_percentile')


def rank_corr(x,y):
    x=rankdata(x);y=rankdata(y)
    if np.ptp(x)==0 or np.ptp(y)==0:return np.nan
    return float(np.corrcoef(x,y)[0,1])


def correlation_summary(x,y,covariates,rng,repetitions=1000):
    x=np.asarray(x,float);y=np.asarray(y,float);n=len(x)
    result={'n_donors':n,'rho':np.nan,'ci_low':np.nan,'ci_high':np.nan,'bootstrap_valid_fraction':np.nan,
            'bootstrap_requested':repetitions,'bootstrap_valid_replicates':0,'bootstrap_constant_replicates':0,'ci_status':'not_evaluated',
            'partial_rho':np.nan,'partial_status':'not_evaluated','partial_residual_df':0}
    if n<8:return dict(result,status='fewer_than_8_donors')
    if np.ptp(x)==0 or np.ptp(y)==0:return dict(result,status='constant_variable')
    result['rho']=rank_corr(x,y)
    indices=rng.integers(n,size=(repetitions,n))
    a=rankdata(x[indices],axis=1);b=rankdata(y[indices],axis=1)
    a-=a.mean(axis=1,keepdims=True);b-=b.mean(axis=1,keepdims=True)
    denom=np.sqrt((a*a).sum(axis=1)*(b*b).sum(axis=1))
    valid=denom>0;result['bootstrap_valid_fraction']=float(valid.mean())
    result['bootstrap_valid_replicates']=int(valid.sum());result['bootstrap_constant_replicates']=int((~valid).sum())
    result['ci_status']='too_many_undefined_resamples'
    if valid.mean()>=.95:
        result['ci_low'],result['ci_high']=np.quantile((a*b).sum(axis=1)[valid]/denom[valid],[.025,.975])
        result['ci_status']='pointwise_percentile'
    z=np.column_stack([np.ones(n),np.asarray(covariates,float)])
    # Standardization changes neither residuals nor rank; improves numerical conditioning.
    if z.shape[1]>1:
        sd=z[:,1:].std(axis=0)
        if (sd==0).any():return dict(result,status='estimated',partial_status='constant_covariate')
        z[:,1:]=(z[:,1:]-z[:,1:].mean(axis=0))/sd
    rank=np.linalg.matrix_rank(z);result['partial_residual_df']=int(n-rank-1)
    if rank<z.shape[1]:result['partial_status']='rank_deficient'
    elif n-rank-1<6:result['partial_status']='fewer_than_6_residual_df'
    else:
        a=rankdata(x);b=rankdata(y)
        a-=z@np.linalg.lstsq(z,a,rcond=None)[0];b-=z@np.linalg.lstsq(z,b,rcond=None)[0]
        if np.linalg.norm(a)<1e-10 or np.linalg.norm(b)<1e-10:result['partial_status']='constant_residual'
        else:result['partial_rho']=float(np.corrcoef(a,b)[0,1]);result['partial_status']='estimated_no_interval'
    return dict(result,status='estimated')
