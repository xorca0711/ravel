"""Independent read-only numerical check. Imports no production analysis code."""
from pathlib import Path
from collections import defaultdict
import csv
import gzip
import hashlib
import json
import math
import statistics
import sys
import xml.etree.ElementTree as ET
import numpy as np

ROOT=Path(__file__).resolve().parents[4]
PACKAGE=Path(__file__).resolve().parents[1]
LIBS=['PBS_1','PBS_2','LH5_1','LH5_2','LH30_1','LH30_2']
METRICS=['WT_minus_PBS','B3_minus_PBS','B3_minus_WT','amplitude_residual']


def check(value,message):
    if not value: raise AssertionError(message)


def near(actual,expected):
    if expected is None: check(actual=='','Unavailable value must stay blank')
    else: check(math.isclose(float(actual),float(expected),rel_tol=1e-10,abs_tol=1e-10),f'Numeric mismatch: {actual} versus {expected}')


def table(path):
    with path.open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))


def main():
    run=Path(sys.argv[1]).resolve()
    receipt=json.loads((run/'receipt.json').read_text());check(receipt['status']=='executed','Run did not execute')
    contract=json.loads((ROOT/receipt['contract']).read_text())
    check(hashlib.sha256((ROOT/receipt['contract']).read_bytes()).hexdigest()==receipt['contract_sha256'],'Contract hash')
    for binding in receipt['inputs']+receipt['code']+receipt['outputs']:
        check(hashlib.sha256((ROOT/binding['path']).read_bytes()).hexdigest()==binding['sha256'],binding['path'])
    source=[]
    for kind in ['readcount','fpkm']:
        with gzip.open(ROOT/f'raw_data/Sx22/GSE160217_060120_22_{kind}_genename.xls.gz','rt',newline='') as f:
            source.append(list(csv.DictReader(f,delimiter='\t')))
    counts=np.array([[float(r[l]) for l in LIBS] for r in source[0]])
    fpkm=np.array([[float(r[l]) for l in LIBS] for r in source[1]])
    check(counts.shape==(35275,6),'Source dimensions')
    ids=[r['geneID'] for r in source[0]];by_id={v:i for i,v in enumerate(ids)}
    check(len(by_id)==len(ids),'Stable IDs not unique')
    for a,b in zip(*source): check(all(a[k]==b[k] for k in a if k not in LIBS),'Source annotation mismatch')
    sizes=np.array([math.fsum(counts[:,j]) for j in range(6)])
    cpm=counts*1e6/sizes
    eligible=np.count_nonzero(cpm>=1,axis=1)>=2
    by_symbol=defaultdict(list)
    for i,r in enumerate(source[0]): by_symbol[r['Gene_name']].append(i)
    manifest=json.loads((PACKAGE/'sources/memberships_v1.json').read_text())
    members={r['id']:r['members'] for r in manifest['panels']}
    for line in (PACKAGE/'sources/mh.all.v2026.1.Mm.symbols.gmt').read_text().splitlines():
        fields=line.split('\t')
        if fields[0] in manifest['external_sets']: members[fields[0]]=fields[2:]
    check(len(members)==10,'Membership family')
    expected_mapping=[(name,symbol) for name,syms in members.items() for symbol in syms]
    mapping=table(run/'member_mapping.csv')
    check([(r['membership'],r['symbol']) for r in mapping]==expected_mapping,'Membership order/coverage')
    tested={i for syms in members.values() for sym in syms for i in by_symbol[sym]}
    chosen={name:[by_symbol[s][0] for s in syms if len(by_symbol[s])==1 and eligible[by_symbol[s][0]]] for name,syms in members.items()}
    unique={name:{by_symbol[s][0] for s in syms if len(by_symbol[s])==1} for name,syms in members.items()}
    background=[i for i in range(len(ids)) if eligible[i] and i not in tested]
    for r in mapping:
        hits=by_symbol[r['symbol']];status='unique' if len(hits)==1 else 'unmapped' if not hits else 'ambiguous'
        check(r['status']==status and r['stable_ids']==';'.join(ids[i] for i in hits),'Exact membership mapping')
        check(r['eligible_for_summary']==str(len(hits)==1 and bool(eligible[hits[0]])),'Membership inclusion')
    inventory=table(run/'gene_inventory.csv');check([r['geneID'] for r in inventory]==ids,'Inventory rows/order')
    for i,r in enumerate(inventory):
        check(all(r[k]==v for k,v in source[0][i].items() if k not in LIBS),'Inventory annotation')
        check(r['primary_eligible']==str(bool(eligible[i])) and r['tested_membership_row']==str(i in tested),'Inventory flags')
        check(r['amplitude_background']==str(bool(eligible[i]) and i not in tested),'Fixed background')
    count_copy=table(run/'counts_for_tmm.csv');check([r['geneID'] for r in count_copy]==ids,'TMM source IDs')
    np.testing.assert_array_equal(np.array([[int(r[l]) for l in LIBS] for r in count_copy]),counts)
    overlap=table(run/'membership_overlap.csv');check(len(overlap)==100,'Overlap cardinality')
    for r in overlap:
        a,b=r['first'],r['second']
        check(int(r['shared_source_symbols'])==len(set(members[a])&set(members[b])),'Symbol overlap')
        check(int(r['shared_unique_rows'])==len(unique[a]&unique[b]),'Unique overlap')
        check(int(r['shared_eligible_rows'])==len(set(chosen[a])&set(chosen[b])),'Eligible overlap')
    factor_rows=table(run/'normalization_factors.csv')
    factors={(r['view'],r['library']):float(r['tmm_factor']) for r in factor_rows}
    for r in factor_rows:
        near(r['library_size'],sizes[LIBS.index(r['library'])]);near(r['effective_library_size'],float(r['library_size'])*float(r['tmm_factor']))
        check(r['edgeR_version']=='4.10.5','TMM version')
    views=['full']+['omit_'+l for l in LIBS]
    tmm_ok=json.loads((run/'summary.json').read_text())['tmm']['status']=='qualified'
    if tmm_ok:
        check(len(factor_rows)==36 and len(factors)==36,'TMM coverage')
        for view in views: near(math.fsum(math.log(factors[view,l]) for l in LIBS if view!='omit_'+l),0)
    fits=table(run/'amplitude_fits.csv');summaries=table(run/'panel_set_summaries.csv')
    tested_values=table(run/'tested_gene_sensitivity.csv')
    check(len(fits)==21 and len(summaries)==210,'Case coverage')
    observed={(r['scale'],r['view'],r['geneID']):r for r in tested_values}
    computed={};max_direct_error=0
    for scale in ['CPM','TMM','FPKM']:
        for view in views:
            keep=[j for j,l in enumerate(LIBS) if view!='omit_'+l]
            fit=next(r for r in fits if (r['scale'],r['view'])==(scale,view))
            check(int(fit['n_background'])==len(background),'Fixed fit background')
            if scale=='TMM' and not tmm_ok:
                check(fit['status']=='held_TMM_runtime','TMM local hold')
                for name in members: computed[scale,view,name]=[None]*4
                continue
            norm=(cpm[:,keep] if scale=='CPM' else fpkm[:,keep] if scale=='FPKM' else
                  counts[:,keep]*1e6/np.array([sizes[j]*factors[view,LIBS[j]] for j in keep]))
            transformed=np.log1p(norm)/math.log(2)
            group_means=[np.mean(transformed[:,[k for k,j in enumerate(keep) if j//2==g]],axis=1) for g in range(3)]
            x=group_means[1]-group_means[0];y=group_means[2]-group_means[0];direct=group_means[2]-group_means[1]
            max_direct_error=max(max_direct_error,float(np.max(np.abs(y-x-direct))))
            den=math.fsum(float(x[i])**2 for i in background);num=math.fsum(float(x[i])*float(y[i]) for i in background)
            beta=num/den if den else None;residual=y-beta*x if beta is not None else None
            near(fit['sum_x_squared'],den);near(fit['sum_x_y'],num);near(fit['beta'],beta)
            for i in tested:
                row=observed[scale,view,ids[i]]
                for key,value in zip(METRICS,[x[i],y[i],direct[i],residual[i] if residual is not None else None]): near(row[key],value)
            for name,indices in chosen.items():
                expected=[statistics.median(arr[indices]) if len(indices) and arr is not None else None for arr in [x,y,direct,residual]]
                row=next(r for r in summaries if (r['scale'],r['view'],r['membership'])==(scale,view,name))
                check(int(row['n_eligible'])==len(indices),'Fixed summary membership')
                for key,value in zip(METRICS,expected): near(row[key],value)
                computed[scale,view,name]=expected
            if scale=='CPM' and view=='full':
                primary=table(run/'primary_gene_expression.csv');check([r['geneID'] for r in primary]==ids,'Primary row inventory')
                for i,row in enumerate(primary):
                    for j,l in enumerate(LIBS): near(row[l+'_CPM'],cpm[i,j]);near(row[l+'_log2_CPM_plus_1'],transformed[i,j])
                    for key,value in zip(METRICS,[x[i],y[i],direct[i],residual[i] if residual is not None else None]): near(row[key],value)
    check(len(observed)==len(tested)*(21 if tmm_ok else 14),'Tested gene case coverage')
    ranges=table(run/'sensitivity_ranges.csv');check(len(ranges)==120,'Range coverage')
    for row in ranges:
        scale,name,key=row['scale'],row['membership'],row['metric'];j=METRICS.index(key)
        near(row['full_data'],computed[scale,'full',name][j])
        values=[computed[scale,v,name][j] for v in views[1:] if computed[scale,v,name][j] is not None]
        check(int(row['n_omission_views'])==len(values),'Range omissions')
        near(row['omission_min'],min(values) if values else None);near(row['omission_max'],max(values) if values else None)
    for svg in run.glob('*.svg'):
        ET.parse(svg);check(all(l==l.rstrip() for l in svg.read_text(encoding='utf-8').splitlines()),'SVG trailing whitespace')
    print(json.dumps(dict(status='passed',input_code_output_bindings=len(receipt['inputs']+receipt['code']+receipt['outputs']),
        source_rows=len(ids),mapping_rows=len(mapping),fit_cases=len(fits),membership_cases=len(summaries),
        tested_gene_cases=len(tested_values),range_cases=len(ranges),direct_contrast_identity_max_error=max_direct_error,
        limitation='Numerical verification only; recorded TMM factors checked for coverage/version/denominator consistency, not an independent TMM algorithm implementation.')))


if __name__=='__main__':main()
