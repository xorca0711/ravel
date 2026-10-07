"""Exposed A30 extension: observed state support and continuous activation sensitivity."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCORES = ['proinflammatory_authors', 'proregulatory_authors', 'activation_disjoint']
TISSUES = ['CSF', 'PBMCs']
FLOORS = [5, 20, 50]

def slopes(x, y):
    xc = np.asarray(x) - np.mean(x)
    if float(xc @ xc) < 1e-10:
        return None
    return float(xc @ (np.asarray(y) - np.mean(y)) / (xc @ xc))

def target_in_support(a, b):
    xa, xb = a.activation_disjoint.to_numpy(), b.activation_disjoint.to_numpy()
    target = float((xa.mean()+xb.mean())/2)
    return bool(xa.min() <= target <= xa.max() and xb.min() <= target <= xb.max())

def state_contrast(a, b, adjust):
    """Common linear standardization point is inside both observed activation ranges."""
    xa, xb = a.activation_disjoint.to_numpy(), b.activation_disjoint.to_numpy()
    target = float((xa.mean() + xb.mean()) / 2)
    if adjust:
        assert target_in_support(a,b), 'Linear prediction would extrapolate beyond observed support.'
    out = {}
    for score in SCORES:
        ya, yb = a[score].to_numpy(), b[score].to_numpy()
        if adjust:
            sa, sb = slopes(xa, ya), slopes(xb, yb)
            if sa is None or sb is None:
                return None
            estimate = ya.mean() + sa*(target-xa.mean()) - yb.mean() - sb*(target-xb.mean())
        else:
            estimate = ya.mean()-yb.mean()
        out[score] = float(estimate)
    return out

def calculate(df):
    paired = sorted(d for d,s in df.groupby('donor') if set(s.tissue)==set(TISSUES))
    support, state_rows, donor_rows = [], [], []
    for donor in paired:
        sub = df[df.donor==donor]
        total = sub.groupby('tissue').size()
        for score in SCORES:
            donor_rows.append(dict(donor=donor, mode='original_pooled', floor=0, score=score,
                                   estimate=float(sub[sub.tissue=='CSF'][score].mean()-sub[sub.tissue=='PBMCs'][score].mean()),
                                   n_states=int(sub.state.nunique()), csf_coverage=1., blood_coverage=1.,
                                   activation_gap=float(sub[sub.tissue=='CSF'].activation_disjoint.mean()-sub[sub.tissue=='PBMCs'].activation_disjoint.mean())))
        for floor in FLOORS:
            for mode in ['common_state', 'activation_overlap', 'activation_linear']:
                rows = []
                for state, cells in sub.groupby('state', sort=True):
                    a,b = [cells[cells.tissue==t].copy() for t in TISSUES]
                    original_a, original_b = len(a), len(b)
                    low, high = np.nan, np.nan
                    reason = 'eligible'
                    if min(len(a),len(b))<floor:
                        reason = 'state_cell_floor'
                    elif mode!='common_state':
                        low=max(float(a.activation_disjoint.quantile(.05)),float(b.activation_disjoint.quantile(.05)))
                        high=min(float(a.activation_disjoint.quantile(.95)),float(b.activation_disjoint.quantile(.95)))
                        a=a[a.activation_disjoint.between(low,high)]
                        b=b[b.activation_disjoint.between(low,high)]
                        if high<=low or min(len(a),len(b))<floor:
                            reason='activation_support_floor'
                    if reason=='eligible' and mode=='activation_linear' and not target_in_support(a,b):
                        reason='linear_target_outside_observed_support'
                    vals = state_contrast(a,b,mode=='activation_linear') if reason=='eligible' else None
                    if vals is None and reason=='eligible': reason='zero_activation_variance'
                    sr=dict(donor=donor,state=state,mode=mode,floor=floor,original_csf=original_a,original_blood=original_b,
                            retained_csf=len(a),retained_blood=len(b),activation_low=low,activation_high=high,status=reason)
                    support.append(sr)
                    if reason!='eligible': continue
                    row={**sr,**vals,'weight_raw':min(len(a),len(b)),
                         'activation_gap':float(a.activation_disjoint.mean()-b.activation_disjoint.mean())}
                    rows.append(row)
                if not rows: continue
                w=np.asarray([r['weight_raw'] for r in rows],float); w/=w.sum()
                cov_a=sum(r['retained_csf'] for r in rows)/total['CSF']
                cov_b=sum(r['retained_blood'] for r in rows)/total['PBMCs']
                gap=float(sum(wi*r['activation_gap'] for wi,r in zip(w,rows)))
                for wi,r in zip(w,rows):
                    for score in SCORES:
                        state_rows.append({k:r[k] for k in ['donor','state','mode','floor','retained_csf','retained_blood','activation_gap']} |
                                          dict(score=score,estimate=r[score],weight=float(wi)))
                for score in SCORES:
                    donor_rows.append(dict(donor=donor,mode=mode,floor=floor,score=score,
                                           estimate=float(sum(wi*r[score] for wi,r in zip(w,rows))),
                                           n_states=len(rows),csf_coverage=float(cov_a),blood_coverage=float(cov_b),activation_gap=gap))
    return pd.DataFrame(support),pd.DataFrame(state_rows),pd.DataFrame(donor_rows),paired

def summarize(donors):
    rng=np.random.default_rng(20261007)
    rows=[]
    for (mode,floor,score),s in donors.groupby(['mode','floor','score'],sort=True):
        v=s.estimate.to_numpy(); n=len(v)
        boot=np.median(v[rng.integers(0,n,size=(5000,n))],axis=1)
        loo=[float(np.median(np.delete(v,i))) for i in range(n)] if n>1 else [np.nan]
        rows.append(dict(mode=mode,floor=int(floor),score=score,n_donors=n,median=float(np.median(v)),positive=int(sum(v>0)),
                         bootstrap_low=float(np.quantile(boot,.025)),bootstrap_high=float(np.quantile(boot,.975)),
                         loo_low=float(np.nanmin(loo)),loo_high=float(np.nanmax(loo)),
                         median_csf_coverage=float(s.csf_coverage.median()),median_blood_coverage=float(s.blood_coverage.median()),
                         minimum_csf_coverage=float(s.csf_coverage.min()),minimum_blood_coverage=float(s.blood_coverage.min()),
                         median_activation_gap=float(s.activation_gap.median())))
    return pd.DataFrame(rows)

def check_independent(df, states, donors):
    """Independent raw-row accumulation plus direct least-squares normal equations."""
    checks=0; worst=0.
    for row in states.itertuples(index=False):
        sl=df[(df.donor==row.donor)&(df.state==row.state)]
        aa,bb=[sl[sl.tissue==t] for t in TISSUES]
        if row.mode!='common_state':
            lo=max(np.percentile(aa.activation_disjoint,5),np.percentile(bb.activation_disjoint,5))
            hi=min(np.percentile(aa.activation_disjoint,95),np.percentile(bb.activation_disjoint,95))
            aa,bb=[s[(s.activation_disjoint>=lo)&(s.activation_disjoint<=hi)] for s in [aa,bb]]
        if row.mode=='activation_linear':
            target=(sum(aa.activation_disjoint)/len(aa)+sum(bb.activation_disjoint)/len(bb))/2
            preds=[]
            for s in [aa,bb]:
                X=np.column_stack([np.ones(len(s)),s.activation_disjoint.to_numpy()-target])
                preds.append(float(np.linalg.lstsq(X,s[row.score].to_numpy(),rcond=None)[0][0]))
            expected=preds[0]-preds[1]
        else:
            expected=sum(aa[row.score])/len(aa)-sum(bb[row.score])/len(bb)
        err=abs(expected-row.estimate); worst=max(worst,err); assert err<1e-10; checks+=1
    for row in donors[donors['mode']!='original_pooled'].itertuples(index=False):
        sl=states[(states.donor==row.donor)&(states['mode']==row.mode)&(states.floor==row.floor)&(states.score==row.score)]
        assert abs(sum(sl.weight)-1)<1e-12
        expected=sum(r.weight*r.estimate for r in sl.itertuples(index=False))
        assert abs(expected-row.estimate)<1e-10; checks+=1
    return dict(checks=checks,maximum_absolute_error=worst,passed=True,
                scope='Independent sums and least-squares predictions from the same saved cells; arithmetic verification, not replication or new raw-QC audit.')

def synthetic_test():
    rows=[]
    # Different activation distributions with an exact common slope and tissue offset.
    for tissue,shift,offset in [('CSF',.3,2),('PBMCs',0,0)]:
        for x in np.linspace(-2,2,100)+shift:
            rows.append(dict(donor='test',tissue=tissue,state=0,activation_disjoint=x,
                             proinflammatory_authors=3*x+offset,proregulatory_authors=-x+offset))
    frame=pd.DataFrame(rows); sup,states,donors,paired=calculate(frame)
    selected=donors[(donors['mode']=='activation_linear')&(donors.floor==20)]
    for s in ['proinflammatory_authors','proregulatory_authors']:
        assert abs(float(selected[selected.score==s].estimate.iloc[0])-2)<1e-10
    check_independent(frame,states,donors)
    # A one-compartment state never receives an imputed opposite-compartment mean.
    extra=frame[(frame.tissue=='CSF')].copy(); extra['state']=1
    sup,_,_,_=calculate(pd.concat([frame,extra],ignore_index=True))
    assert (sup[sup.state==1].status=='state_cell_floor').all()
    # Nominal percentile-bound overlap can leave separated observed values after trimming.
    aa=pd.DataFrame({'activation_disjoint':np.r_[np.zeros(10),np.linspace(3,3.5,80),np.full(10,10.)]})
    bb=pd.DataFrame({'activation_disjoint':np.r_[np.full(10,2.),np.linspace(7,7.5,80),np.full(10,8.)]})
    for s,t in [(aa,'CSF'),(bb,'PBMCs')]:
        s['donor']='gapped'; s['tissue']=t; s['state']=0
        s['proinflammatory_authors']=s.activation_disjoint; s['proregulatory_authors']=s.activation_disjoint
    sup,_,_,_=calculate(pd.concat([aa,bb],ignore_index=True))
    assert (sup[(sup['mode']=='activation_linear')&(sup.floor==20)].status=='linear_target_outside_observed_support').all()
    print('synthetic checks passed')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input'); ap.add_argument('--output'); ap.add_argument('--self-test',action='store_true'); a=ap.parse_args()
    if a.self_test: synthetic_test(); return
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(a.input); assert set(df.tissue)==set(TISSUES)
    assert df[['donor','state','tissue']+SCORES].notna().all().all()
    assert np.isfinite(df[SCORES].to_numpy()).all()
    sup,states,donors,paired=calculate(df)
    assert len(paired)==10, 'Unexpected paired-donor universe; stop for source review.'
    summary=summarize(donors); verification=check_independent(df,states,donors)
    for name,frame in [('state_support',sup),('state_estimates',states),('donor_estimates',donors),('summary',summary)]: frame.to_csv(out/(name+'.csv'),index=False)
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    result=dict(question='A30 observed common-state association and activation sensitivity',paired_donors=paired,
                n_saved_cells=len(df),primary_floor=20,floor_sensitivities=[5,50],bootstrap_draws=5000,
                limits='Restricted observed support changes the target population. State labels and RNA scores are reused exposed measurements. No barcode join, raw QC rerun, doublet detection, calibrated gene null, causality, protein function or independent replication.',
                held_donor_modes=[dict(donor=d,mode=m,floor=f) for d in paired for m in ['common_state','activation_overlap','activation_linear'] for f in FLOORS if donors[(donors.donor==d)&(donors['mode']==m)&(donors.floor==f)].empty])
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,axes=plt.subplots(1,3,figsize=(14,5),layout='constrained')
    modes=['original_pooled','common_state','activation_overlap','activation_linear']
    labels=['Pooled','Shared states','Activation\noverlap','Linear\nstandardized']
    for ax,score,title in zip(axes,SCORES,['Inflammatory RNA','Regulatory RNA','Measured activation']):
        sl=donors[(donors.score==score)&donors.floor.isin([0,20])]
        for d in paired:
            vals=sl[sl.donor==d].set_index('mode').estimate.reindex(modes)
            ax.plot(range(4),vals,marker='o',ms=3,alpha=.55,linewidth=.8)
        ax.axhline(0,color='black',lw=.8); ax.set_xticks(range(4),labels,rotation=15); ax.set_title(title); ax.set_ylabel('CSF minus blood score')
    fig.suptitle('A30: observed common states and activation sensitivity | paired donors')
    fig.supxlabel('Floor 20 cells per compartment/state; restricted populations differ. RNA association, not function or causal effect.',fontsize=9)
    fig.savefig(out/'common_support.png',dpi=200); fig.savefig(out/'common_support.svg'); plt.close(fig)
    print(json.dumps({'paired_donors':len(paired),'verification':verification,'outputs':8}))

if __name__=='__main__': main()
