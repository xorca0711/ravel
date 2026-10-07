"""Exposed diagnostic: duplicate fixed baseline columns without adding information."""
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit
from a11_paired_prediction_v1 import fit, BASE, ROOT

RUN=ROOT/'analysis/research/runs/g1_a11_paired_prediction_v1'


def verify_v1():
    # Standard-library reconstruction from saved scores and fitted coefficients.
    with (RUN/'module_scores.tsv').open() as h:rows=list(csv.DictReader(h,delimiter='\t'))
    values={(r['patient'],r['arm'],r['module']):float(r['score']) for r in rows}
    with (RUN/'coefficients.tsv').open() as h:coefs=list(csv.DictReader(h,delimiter='\t'))
    groups={}
    for r in coefs:groups.setdefault((r['patient'],float(r['penalty']),r['model']),[]).append(r)
    with (RUN/'heldout_predictions.tsv').open() as h:preds=list(csv.DictReader(h,delimiter='\t'))
    errors=[];losses={}
    for row in preds:
        key=(row['patient'],float(row['penalty']),row['model'])
        z=math.fsum(float(r['coefficient'])*(values[(r['patient'],'lesion',r['feature'])]-values[(r['patient'],'normal',r['feature'])])/float(r['train_scale']) for r in groups[key])
        p=1/(1+math.exp(-z));loss=-math.log(p)
        errors.extend([abs(p-float(row['lesion_pair_probability'])),abs(loss-float(row['log_loss']))])
        losses[key]=loss
    with (RUN/'comparisons.tsv').open() as h:comps=list(csv.DictReader(h,delimiter='\t'))
    patients=sorted(set(r['patient'] for r in rows))
    for row in comps:
        lam=float(row['penalty']);model=row['model']
        gains=[losses[p,lam,'shared_stress']-losses[p,lam,model] for p in patients]
        errors.append(abs(math.fsum(gains)/len(gains)-float(row['mean_log_loss_gain'])))
    if max(errors)>1e-12:raise ValueError('Independent v1 endpoint arithmetic mismatch')
    return {'prior_predictions_checked':len(preds),'prior_comparisons_checked':len(comps),'max_independent_endpoint_error':max(errors)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    verification=verify_v1()
    z=pd.read_csv(RUN/'module_scores.tsv',sep='\t')
    patients=sorted(z.patient.unique())
    x=np.array([[[float(z.loc[(z.patient==p)&(z.arm==a)&(z.module==m),'score'].iloc[0]) for m in BASE] for a in ['normal','lesion']] for p in patients])
    old=pd.read_csv(RUN/'heldout_predictions.tsv',sep='\t')
    rows=[];comparisons=[];errors=[]
    for penalty in [1.,.1,10.]:
        original=old[old.penalty==penalty].pivot(index='patient',columns='model',values='log_loss')
        for duplicate in range(4):
            inds=[0,1,2,3,duplicate];losses=[]
            for held,p in enumerate(patients):
                train=np.delete(x[:,:,inds],held,axis=0)
                w,scale,error=fit(train,penalty);errors.append(error)
                d=(x[held,1,inds]-x[held,0,inds])/scale
                logit=float(w@d);prob=float(expit(logit));loss=-math.log(prob)
                if abs(loss-float(np.logaddexp(0,-logit)))>1e-12:raise ValueError('Duplicate log-loss arithmetic failed')
                losses.append(loss)
                rows.append({'patient':p,'penalty':penalty,'duplicated_feature':BASE[duplicate],'probability':prob,'log_loss':loss,'baseline_log_loss':float(original.loc[p,'shared_stress']),'lesion_log_loss':float(original.loc[p,'add_lesion'])})
            mean=math.fsum(losses)/len(losses)
            comparisons.append({'penalty':penalty,'duplicated_feature':BASE[duplicate],'duplicate_mean_loss':mean,'baseline_mean_loss':float(original.shared_stress.mean()),'lesion_mean_loss':float(original.add_lesion.mean()),'duplicate_gain_over_baseline':float(original.shared_stress.mean())-mean,'lesion_gain_over_duplicate':mean-float(original.add_lesion.mean()),'patients_duplicate_better_than_lesion':sum(loss<float(original.loc[p,'add_lesion']) for p,loss in zip(patients,losses))})
    pd.DataFrame(rows).to_csv(args.output/'duplicate_predictions.tsv',sep='\t',index=False)
    pd.DataFrame(comparisons).to_csv(args.output/'capacity_comparisons.tsv',sep='\t',index=False)
    verification.update({'duplicate_predictions':len(rows),'duplicate_comparisons':len(comparisons),'max_independent_optimizer_error':max(errors),'new_biological_features':0,'primary_penalty':1.})
    (args.output/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    print(json.dumps({'comparisons':comparisons,'verification':verification}))


if __name__=='__main__':main()
