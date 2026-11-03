"""A17 observation recoverability: complete size partition, no empirical fitting."""
import argparse,json,csv
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

K=64
TIMES=[1,2,4]
CASES=[('persistent_script',.08,0.,0.,.9),('persistent_manuscript_variant',.16,0.,0.,1.1),('switching_S_start',0.,.1,.2,.9),('switching_F_start',1.,.2,.1,.9),('combined',.08,.1,.2,.9)]

def law(t,pi,kfs,ksf,slow,K=K,tol=1e-10):
    y=np.zeros((2,K+1));y[:,1]=1
    def rhs(net):
        b=np.array(net)*.7/.4;d=np.array(net)*.3/.4
        def f(_,flat):
            z=flat.reshape(2,K+1); ans=np.empty_like(z)
            for i,k in enumerate([kfs,ksf]):
                ans[i]=b[i]*(np.convolve(z[i],z[i])[:K+1]-z[i])-d[i]*z[i]+k*(z[1-i]-z[i]);ans[i,0]+=d[i]
            return ans.ravel()
        return f
    # Backward PGF composition: integrate the terminal regime first.
    stages=([(t-2,[.5,.01])] if t>2 else [])+[(min(t,2),[3.1,slow])]
    for duration,net in stages:
        sol=solve_ivp(rhs(net),(0,duration),y.ravel(),method='DOP853',rtol=tol,atol=tol*.01)
        assert sol.success;y=sol.y[:,-1].reshape(2,K+1)
    full=pi*y[0]+(1-pi)*y[1]
    assert np.min(full)>-1e-9 and full.sum()<=1+1e-8
    p=np.r_[full[2:],1-full.sum()];q=p/(1-full[:2].sum())
    assert np.min(q)>0 and abs(q.sum()-1)<1e-8
    return q,full[:2]

def main(out):
    out.mkdir(exist_ok=True)
    manifest=list(csv.DictReader(open('docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/primary_cohort_manifest.csv')))
    # Actual counts are passed through from the hash-bound source manifest.
    fields=list(manifest[0]);print('manifest fields',fields)
    results={};laws={};maxerr=0
    for t in TIMES:
        qs=[]
        for name,pi,kfs,ksf,slow in CASES:
            q,p01=law(t,pi,kfs,ksf,slow);q2,_=law(t,pi,kfs,ksf,slow,K=128,tol=2e-12)
            check=np.r_[q2[:K-1],q2[K-1:].sum()];maxerr=max(maxerr,float(np.max(abs(q-check))))
            assert np.max(abs(q-check))<2e-7
            laws[f'{name}_week{t}']={'q':q.tolist(),'p_zero_one':p01.tolist()};qs.append(q)
        qs=np.array(qs); common=np.min(qs,axis=0); weights=common/qs; target=common/common.sum()
        selected=qs*weights;selected/=selected.sum(axis=1)[:,None]
        assert np.all((weights>0)&(weights<=1))
        tv=.5*np.abs(selected-target).sum(axis=1)
        # Fixed-law separability under uniform detection is distinct from identification.
        kl=np.array([[sum(a*np.log(a/b)) for b in qs] for a in qs])
        results[str(t)]={'uniform_detection_pairwise_KL':kl.tolist(),'common_selected_law':target.tolist(),'retained_detection_weights':weights.tolist(),'maximum_total_variation_after_detection':float(tv.max()),'relative_retention':common.sum()}
    # Independent scalar birth/death PGF check on no-switching, infinite-tail laws.
    def pgf(z,net,duration):
        b=net*.7/.4;d=net*.3/.4;e=np.exp(-net*duration)
        p0=d*(1-e)/(b-d*e);a=b*(1-e)/(b-d*e)
        return p0+(1-p0)*(1-a)*z/(1-a*z)
    for t in TIMES:
        for z in [0.,.2,.7]:
            for pi,slow in [(.08,.9),(.16,1.1)]:
                expected=0.
                for weight,early,late in [(pi,3.1,.5),(1-pi,slow,.01)]:
                    zz=pgf(z,late,t-2) if t>2 else z; expected+=weight*pgf(zz,early,min(t,2))
                q,p01=law(t,pi,0,0,slow,K=128)
                approx=p01[0]+z*p01[1]+(1-p01.sum())*sum(q[:-1]*z**np.arange(2,129))
                maxerr=max(maxerr,abs(expected-approx));assert abs(expected-approx)<2e-7
    # Synthetic finite-sample recoverability on the actual 4/4/3 mouse schedule.
    # Same observed law for every family after admissible detection: no classifier
    # on these observations can discriminate the family labels.
    rng=np.random.default_rng(20261103); finite=[]
    for name,*_ in CASES:
        for replicate in range(200):
            loss=[]
            for m in manifest:
                week=str(int(float(m['week_as_archived'])));n=int(m['clones_ge2']);target=np.array(results[week]['common_selected_law'])
                sampled=rng.multinomial(n,target);loss.append(float(-(sampled*np.log(target)).sum()/n))
            finite.append({'generating_family':name,'replicate':replicate,'equal_mouse_nll':float(np.mean(loss))})
    with (out/'synthetic_recoverability.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(finite[0]));w.writeheader();w.writerows(finite)
    (out/'probabilities.json').write_text(json.dumps(laws,indent=2))
    (out/'recoverability.json').write_text(json.dumps({'cases':[x[0] for x in CASES],'weeks':results,'source_mouse_manifest':manifest,'observation_partition':'sizes 2..64 and >=65; zero/one excluded only by conditional observation','finding':'Distinct candidate laws can produce exactly the same retained binned distribution under admissible unknown size/time-specific detection. Uniform-detection KL contrasts do not qualify actual ascertainment. No cohort fit or mechanism selection.','limit':'This is an observation-model counterexample, not proof that fixed uniform-detection models are indistinguishable or a fitted detection process.'},indent=2))
    (out/'verification.json').write_text(json.dumps({'passed':True,'maximum_probability_error':maxerr,'method':'K64 versus K128 regrouping and independent scalar infinite-tail PGF composition; complete probability partition; no rerun of prior stochastic kernel checks'},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);main(ap.parse_args().output)
