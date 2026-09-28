"""Small invariant helpers for corrected C1; standard library only."""
from math import isfinite, sqrt

def freeze_population(rows, library):
    selected=[r for r in rows if r['gsm']==library and r['primary_include'] and r['gate_transition']]
    keys=[r['barcode'] for r in selected]
    if len(keys)!=len(set(keys)): raise ValueError('Duplicated fixed-population barcode')
    return sorted(selected,key=lambda r:r['barcode'])

def remaining_columns(symbols, excluded):
    return [i for i,g in enumerate(symbols) if g not in excluded and not g.lower().startswith('mt-')]

def quartiles(depth,barcodes):
    if len(depth)!=len(barcodes) or len(barcodes)!=len(set(barcodes)): raise ValueError('Invalid depth/barcode join')
    order=sorted(range(len(depth)),key=lambda i:(depth[i],barcodes[i]))
    bins=[None]*len(order)
    for rank,i in enumerate(order): bins[i]=min(3,4*rank//len(order))
    return bins

def eligibility(positive, strata, k, matched_negative_indices=None, floor=30):
    npos=sum(positive); nneg=len(positive)-npos
    if npos<floor or nneg<floor: return 'not_assessed_group_floor'
    for q in set(strata):
        if any(p and s==q for p,s in zip(positive,strata)) and sum((not p) and s==q for p,s in zip(positive,strata))<k:
            return 'not_assessed_all_positives_not_matchable'
    if matched_negative_indices is not None and len(set(matched_negative_indices))<floor:
        return 'not_assessed_unique_negative_floor'
    return 'assessed'

def effects(positive_values,negative_values,matched_control_means,fixed_population_values):
    if len(positive_values)!=len(matched_control_means): raise ValueError('Dropping positives changes the estimand')
    if not all(isfinite(float(x)) for x in fixed_population_values): raise ValueError('Nonfinite outcomes')
    mean=lambda x:sum(x)/len(x)
    m=mean(fixed_population_values)
    sd=sqrt(sum((x-m)**2 for x in fixed_population_values)/(len(fixed_population_values)-1))
    marginal=mean(positive_values)-mean(negative_values)
    matched=mean([p-n for p,n in zip(positive_values,matched_control_means)])
    return {'marginal_raw':marginal,'matched_raw':matched,'fixed_population_sd':sd,'marginal_standardized':marginal/sd if sd else None,'matched_standardized':matched/sd if sd else None}
