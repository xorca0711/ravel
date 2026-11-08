"""Prospective diagnostic amendment: exact label distribution with tied ranks."""
import argparse
import csv
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, permutation_test

RUN = Path('analysis/research/runs/nn26_animal_reproduction_v1')


def distribution(values, n):
    # Doubled average ranks are integral, even with ties; each observation retains
    # its multiplicity. DP counts all C(N,n) equally weighted label allocations.
    ranks = [int(round(2*r)) for r in rankdata(values)]
    counts = [{0: 1}] + [dict() for _ in range(n)]
    for i, rank in enumerate(ranks):
        for k in range(min(i+1,n), 0, -1):
            for s, count in list(counts[k-1].items()):
                counts[k][s+rank] = counts[k].get(s+rank,0)+count
    assert sum(counts[n].values()) == math.comb(len(values),n)
    return ranks, counts[n]


def exact(a,b):
    ranks, counts = distribution(a+b,len(a))
    observed = sum(ranks[:len(a)])
    total = sum(counts.values())
    lower = sum(v for s,v in counts.items() if s <= observed)
    upper = sum(v for s,v in counts.items() if s >= observed)
    center = len(a)*(len(a)+len(b)+1)
    extreme = sum(v for s,v in counts.items() if abs(s-center)>=abs(observed-center))
    return min(1.,2*min(lower,upper)/total), extreme/total, ranks, counts


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    observations=list(csv.DictReader((RUN/'observations.csv').open()))
    contrasts=list(csv.DictReader((RUN/'contrasts.csv').open()))
    output=[];enumeration_checks=0;scipy_checks=0
    for c in contrasts:
        if c['scope']!='all' or c['p_reported']=='': continue
        a,b=c['comparison'].split('-')
        groups=[[float(r['value']) for r in observations if r['endpoint']==c['endpoint'] and r['group']==g] for g in [a,b]]
        x,y=groups; p,absolute,ranks,counts=exact(x,y)
        if math.comb(len(x)+len(y),len(x))<=50000:
            brute=Counter(sum(ranks[i] for i in indices) for indices in itertools.combinations(range(len(ranks)),len(x)))
            assert brute==counts
            enumeration_checks+=1
            # Separate SciPy permutation implementation on rank sums.
            sx=np.array(ranks[:len(x)],dtype=float);sy=np.array(ranks[len(x):],dtype=float)
            ref=permutation_test((sx,sy),lambda a,b:np.sum(a),n_resamples=np.inf,
                                 alternative='two-sided',vectorized=False).pvalue
            assert abs(ref-p)<1e-12
            scipy_checks+=1
        reported=float(c['p_reported'])
        output.append(dict(endpoint=c['endpoint'],comparison=c['comparison'],n_a=len(x),n_b=len(y),
            p_reported=reported,p_v1=float(c['p_primary']),p_exact_tied_doubled_tail=p,
            p_exact_tied_absolute_tail=absolute,delta_exact_reported=p-reported,
            within_0_0001=abs(p-reported)<.0001,source=c['reported_locator']))
    with (out/'exact_rank_reconciliation.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    report={'analysis':'Nn26-P01.tie_diagnostic_v2','status':'executed',
        'method':'Exact fixed pooled-rank label distribution including ties; two-sided doubled smaller inclusive tail; absolute-tail alternative retained.',
        'all_comparisons':len(output),'brute_enumeration_checks':enumeration_checks,'scipy_permutation_checks':scipy_checks,
        'residual_differences_over_0_001':[r for r in output if abs(r['delta_exact_reported'])>.001],
        'interpretation':'Method reconciliation after v1 exposure, not selection of a significance-favoring analysis. Original v1 retained. No new population claim or acceptance.'}
    (out/'diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',newline='\n')
    print(json.dumps({k:report[k] for k in ['all_comparisons','brute_enumeration_checks','scipy_permutation_checks']}))


if __name__=='__main__': main()
