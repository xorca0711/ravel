"""Frozen synthetic numerical qualification; never fits a biological cohort."""
import argparse
import json
import math
from pathlib import Path
import random
from a17_branching_kernel_v1 import birth_death_reference, simulate

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    cfg=json.loads(args.config.read_text())
    target=args.output/'qualification.json'
    if target.exists():
        raise FileExistsError('Refusing output overwrite')
    results=[]
    for case in cfg['cases']:
        for seed in cfg['seeds']:
            rng=random.Random(seed)
            sizes=[sum(simulate(tuple(case['initial']),case['schedule'],rng)) for _ in range(cfg['replicates'])]
            mean=sum(sizes)/len(sizes)
            p0=sum(n==0 for n in sizes)/len(sizes)
            ref_mean,ref_var,ref_p0=birth_death_reference(case['reference_birth'],case['reference_death'],case['reference_time'])
            mean_tolerance=cfg['standard_errors']*math.sqrt(ref_var/len(sizes))
            extinction_tolerance=cfg['standard_errors']*math.sqrt(ref_p0*(1-ref_p0)/len(sizes))
            result={'case':case['name'],'seed':seed,'replicates':len(sizes),'mean':mean,'reference_mean':ref_mean,'mean_tolerance':mean_tolerance,'extinction':p0,'reference_extinction':ref_p0,'extinction_tolerance':extinction_tolerance}
            result['passed']=abs(mean-ref_mean)<=max(mean_tolerance,1e-12) and abs(p0-ref_p0)<=max(extinction_tolerance,1e-12)
            results.append(result)
    args.output.mkdir(parents=True,exist_ok=True)
    report={'scope':'Synthetic numerical checks only; no biological fit, model selection or parameter identifiability claim','results':results,'passed':all(x['passed'] for x in results)}
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'checks':len(results)}))
    if not report['passed']:
        raise RuntimeError('Synthetic numerical qualification failed; retain this attempt')

if __name__=='__main__':
    main()
