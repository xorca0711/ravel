"""Exact no-switching source-parameter size-law qualification, not cohort fitting."""
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[4]


def law(net_time,q=.7):
    e=math.exp(-net_time)
    den=q-(1-q)*e
    p0=(1-q)*(1-e)/den
    alpha=q*(1-e)/den
    return p0,alpha,math.exp(net_time)


def quantities(net_time,k):
    p0,a,mean=law(net_time)
    retention=(1-p0)*a**(k-1)
    cells=retention*(k+a/(1-a))
    return p0,retention,cells,mean


def independent_probabilities(early,late,t,q=.7):
    # Backward PGF coefficient ODE, through p4 plus total expectation; no closed-form calls.
    y=np.array([0.,1.,0.,0.,0.,1.])
    def derivative(v,r):
        birth=r*q/(2*q-1);death=r*(1-q)/(2*q-1)
        f=np.empty(6)
        for n in range(5):f[n]=birth*sum(v[i]*v[n-i] for i in range(n+1))-(birth+death)*v[n]+(death if n==0 else 0.)
        f[5]=r*v[5]
        return f
    for duration,r in [(min(t,2.),early),(max(0.,t-2.),late)]:
        steps=max(1,math.ceil(duration/.001));h=duration/steps
        for _ in range(steps):
            a=derivative(y,r);b=derivative(y+h*a/2,r);c=derivative(y+h*b/2,r);d=derivative(y+h*c,r)
            y+=h*(a+2*b+2*c+d)/6
    return y


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    trace=json.loads((ROOT/'docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/mutant_parameter_trace.json').read_text())
    v={row['main_variable']:row['value'] for row in trace['assignments']}
    if v['fss_in']!=.08 or v['r_in']!=.7 or v['q_in']!=.7 or v['tau']!=14:raise ValueError('Source parameter trace changed')
    q=v['r_in'];fast=[v['sigmas_s_in']*7*(2*q-1),v['tausigma_s']*7*(2*q-1)]
    slow=[v['sigmas_p_in']*7*(2*q-1),v['tausigma_p']*7*(2*q-1)]
    rows=[];checks=[]
    variants=[('source_script',.08,slow[0]),('pi_only_sensitivity',.16,slow[0]),('slow_only_sensitivity',.08,1.1),('both_sensitivity',.16,1.1)]
    for variant,pi,early_slow in variants:
        for t in [1.,2.,4.]:
            rates=[fast,[early_slow,slow[1]]]
            laws=[]
            for early,late in rates:
                net=early*min(t,2)+late*max(0,t-2)
                ode=independent_probabilities(early,late,t)
                p0,alpha,mean=law(net)
                errors=[abs(ode[0]-p0),abs(ode[5]-mean)/max(1,mean)]
                for k in [1,2,5]:
                    _,retain,cells,_=quantities(net,k)
                    errors.extend([abs(retain-(1-ode[:k].sum())),abs(cells-(ode[5]-sum(n*ode[n] for n in range(k))))/max(1,cells)])
                checks.append({'variant':variant,'week':t,'early_rate':early,'late_rate':late,'max_error':max(errors)})
                if max(errors)>1e-7:raise ValueError('Independent PGF probability check failed')
                laws.append(net)
            for k in [1,2,5]:
                f=quantities(laws[0],k);s=quantities(laws[1],k)
                rows.append({'variant':variant,'week':t,'minimum_size':k,'founder_fast_fraction':pi,'fast_extinction_probability':f[0],'slow_extinction_probability':s[0],'fast_retention':f[1],'slow_retention':s[1],'fast_fraction_retained_clones':pi*f[1]/(pi*f[1]+(1-pi)*s[1]),'fast_fraction_retained_cells':pi*f[2]/(pi*f[2]+(1-pi)*s[2]),'fast_fraction_all_living_cells':pi*f[3]/(pi*f[3]+(1-pi)*s[3])})
    with (a.output/'ascertainment.tsv').open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
    result={'source_parameters':{'pi':.08,'renewal':q,'fast_net_rates_per_week':fast,'slow_net_rates_per_week':slow,'switch_week':2},'rows':len(rows),'checks':checks,'max_verification_error':max(c['max_error'] for c in checks),'manuscript_variants':'0.16 founder fraction and 1.1 early slow net rate are separate sensitivities; published-curve provenance unresolved','model':'two no-switching linear birth-death founder laws; corrected event semantics; not the literal archived MATLAB implementation','cohort_fit':False}
    (a.output/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'max_verification_error':result['max_verification_error']}))


if __name__=='__main__':main()
