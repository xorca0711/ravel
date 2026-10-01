"""Nb3 R1: declared source-informed, technical-well imaging reconstruction."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
from scipy import stats

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]


def sha(path):
    with path.open('rb') as h: return hashlib.file_digest(h,'sha256').hexdigest()


def bh(values):
    a=np.asarray(values,float); order=np.argsort(a); ranked=a[order]
    adjusted=np.minimum.accumulate((ranked*len(a)/np.arange(1,len(a)+1))[::-1])[::-1]
    result=np.empty_like(a); result[order]=np.minimum(adjusted,1); return result


def contrast(a,b):
    n,m=len(a),len(b); df=n+m-2
    effect=float(np.mean(a)-np.mean(b))
    variance=((n-1)*np.var(a,ddof=1)+(m-1)*np.var(b,ddof=1))/df
    se=float(np.sqrt(variance*(1/n+1/m)))
    if se==0: return effect,se,np.nan,np.nan,np.nan
    p=float(2*stats.t.sf(abs(effect/se),df)); margin=stats.t.ppf(.975,df)*se
    # Independent implementation verifies the two-group OLS statistic.
    check=stats.ttest_ind(a,b,equal_var=True)
    assert np.isclose(p,check.pvalue,rtol=1e-10,atol=1e-12)
    return effect,se,float(effect-margin),float(effect+margin),p


if __name__=='__main__':
    out=HERE/'runs/R1_v1'
    if out.exists(): raise SystemExit('Refusing to overwrite R1_v1')
    cfgpath=HERE/'config/Nb3_execution_v1.json'; cfg=json.loads(cfgpath.read_text()); spec=cfg['R1']
    source=ROOT/cfg['inputs']['imaging']['path']; assert sha(source)==cfg['inputs']['imaging']['sha256']
    frame=pd.read_csv(source); frame['target']=frame.crispr_target.str.upper()
    assert not frame.duplicated(['plate','plate_replicate','well','day','segmentation_model']).any()
    assert frame.segmentation_model.nunique()==1
    rows=[]
    for variant in ['all_wells_scaling','exclude_tdTomato_scaling']:
        for day in spec['days']:
            d=frame[frame.day==day].copy()
            for endpoint in spec['endpoints']:
                scaling=d if variant=='all_wells_scaling' else d[d.target!='TDTOMATO']
                moments=scaling.groupby('plate')[endpoint].agg(['mean','std'])
                z=(d[endpoint]-d.plate.map(moments['mean']))/d.plate.map(moments['std'])
                assert (moments['std']>0).all()
                for target in sorted(set(d.target)-set(spec['exclude_targets'])):
                    plates=set(d.loc[d.target==target,'plate'])
                    a=z[(d.target==target)&z.notna()].to_numpy()
                    b=z[d.plate.isin(plates)&(d.target=='TIGIT')&z.notna()].to_numpy()
                    row={'variant':variant,'day':day,'endpoint':endpoint,'target':target,
                         'target_wells':len(a),'control_wells':len(b),'plates':','.join(sorted(plates))}
                    if len(a)<spec['minimum_target_wells'] or len(b)<spec['minimum_control_wells']:
                        row['status']='not_estimable_under_declared_floor'
                    else:
                        effect,se,low,high,p=contrast(a,b)
                        row.update(status='technical_well_model',effect=effect,se=se,ci_low=low,ci_high=high,p=p)
                    rows.append(row)
    result=pd.DataFrame(rows); result['q']=np.nan
    for _,idx in result[result.p.notna()].groupby(['variant','day','endpoint']).groups.items():
        result.loc[idx,'q']=bh(result.loc[idx,'p'])
    out.mkdir(parents=True); result.to_csv(out/'imaging_effects.tsv',sep='\t',index=False)
    counts=result[result.q<.05].groupby(['variant','day','endpoint']).target.nunique()
    summary={'analysis_id':'Nb3_R1','source_rows':len(frame),'targets':frame.target.nunique(),
             'source_days':sorted(frame.day.unique()),'eligible_models':int(result.p.notna().sum()),
             'technical_q_lt_005_counts':{'|'.join(k):int(v) for k,v in counts.items()},
             'source_choice_uncertainties':spec['source_uncertainties'],
             'biological_inference':'Not established: split wells and unresolved preparations',
             'script_sha256':sha(Path(__file__)),'config_sha256':sha(cfgpath),'input_sha256':sha(source),
             'output_sha256':sha(out/'imaging_effects.tsv'),'python':sys.version.split()[0]}
    (out/'run_record.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['source_rows','targets','eligible_models','technical_q_lt_005_counts']}))
