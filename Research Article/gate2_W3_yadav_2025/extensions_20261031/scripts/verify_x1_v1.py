"""Independent standard-library arithmetic on frozen CSVs; no main-analysis import."""
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def close(a,b):
    assert math.isclose(float(a),float(b),rel_tol=1e-11,abs_tol=1e-12),(a,b)
def verify(out):
    ann=ROOT/'analysis/research/runs/Yd1_annotation_v1';rna=ROOT/'analysis/research/runs/Yd1_rna_endpoints_v1'
    cells=read(rna/'cell_endpoints.csv')
    original=json.loads((ROOT/'Research Article/gate2_W3_yadav_2025/config/rna_endpoints_spec_v1.json').read_text())
    summaries=read(out/'library_endpoints.csv');lookup={}
    nchecks=0
    for row in summaries:
        allowed={row['cell_class']}
        if row['inclusion_set']=='core_plus_mixed':allowed.add('mixed_fibroblast_macrophage')
        selected=[c for c in cells if c['gsm']==row['gsm'] and c['qc_'+row['qc_mode']]=='1' and c['label'] in allowed]
        assert len(selected)==int(row['n_cells'])
        if row['core_eligible']=='1':
            x=[int(c[row['gene']+'_counts']) for c in selected];den=[int(c['total_counts']) for c in selected];n=len(x)
            normalized=[a*10000/b for a,b in zip(x,den)]
            values={'gene_counts':sum(x),'total_counts':sum(den),'detection_fraction':sum(v>0 for v in x)/n,'mean_per10k':math.fsum(normalized)/n,'mean_log1p_per10k':math.fsum(math.log1p(v) for v in normalized)/n,'pseudobulk_cpm':sum(x)*1e6/sum(den)}
            for key,val in values.items():close(row[key],val);nchecks+=1
            lookup[(row['gsm'],row['qc_mode'],row['endpoint'],row['inclusion_set'])]=values
    attribution=read(out/'target_attribution.csv')
    for row in attribution:
        kept=[c for c in cells if c['gsm']==row['gsm'] and c['qc_'+row['qc_mode']]=='1']
        selected=[c for c in kept if c['label']==row['label']]
        x=[int(c[row['gene']+'_counts']) for c in selected];total=sum(int(c[row['gene']+'_counts']) for c in kept)
        assert int(row['n_cells'])==len(x) and int(row['target_count_total'])==sum(x) and int(row['detected_cells'])==sum(v>0 for v in x)
        if x:close(row['detection_fraction'],sum(v>0 for v in x)/len(x))
        else:assert row['detection_fraction']==''
        assert int(row['all_qc_target_counts'])==total
        if total:close(row['share_all_qc_target_counts'],sum(x)/total)
        else:assert row['share_all_qc_target_counts']=='' and row['share_status']=='undefined_zero_target_total'
    for gsm in {c['gsm'] for c in cells}:
        for mode in original['qc_modes']:
            for gene in ['Arg1','Il6']:
                rows=[r for r in attribution if (r['gsm'],r['qc_mode'],r['gene'])==(gsm,mode,gene)]
                assert len(rows)==5
                assert sum(int(r['target_count_total']) for r in rows)==int(rows[0]['all_qc_target_counts'])
                if int(rows[0]['all_qc_target_counts']):close(math.fsum(float(r['share_all_qc_target_counts']) for r in rows),1)
    comps={c['id']:c for c in original['comparisons']}
    contrasts=read(out/'condition_contrasts.csv');crossed=read(out/'crossed_library_differences.csv')
    expected_cross={}
    for r in contrasts:
        comp=comps[r['comparison']];m=r['metric'];mode=r['qc_mode'];inc=r['inclusion_set']
        aa=original['conditions'][comp['target']];bb=original['conditions'][comp['reference']]
        if r['eligible']=='1':
            av=[lookup[(g,mode,comp['endpoint'],inc)][m] for g in aa];bv=[lookup[(g,mode,comp['endpoint'],inc)][m] for g in bb]
            close(r['equal_library_mean_difference'],math.fsum(av)/2-math.fsum(bv)/2)
            diffs=[]
            for ga,x in zip(aa,av):
                for gb,y in zip(bb,bv):expected_cross[(mode,r['comparison'],inc,m,ga,gb)]=x-y;diffs.append(x-y)
            close(r['crossed_difference_min'],min(diffs));close(r['crossed_difference_max'],max(diffs))
    for r in crossed:
        close(r['difference'],expected_cross[(r['qc_mode'],r['comparison'],r['inclusion_set'],r['metric'],r['target_library'],r['reference_library'])])
    assert len(summaries)==48 and len(attribution)==120 and len(contrasts)==48 and len(crossed)==len(expected_cross)==192
    members=read(out/'barcode_membership.csv')
    assert len(members)==len(cells)==12519
    ck={(c['gsm'],c['barcode']):c for c in cells}
    for r in members:
        c=ck[(r['gsm'],r['barcode'])]
        assert all(r[k]==c[k] for k in ['label','qc_primary','qc_broad'])
        for prefix,label in [('mac','macrophage_like'),('fib','fibroblast_like')]:
            assert int(r['in_'+prefix+'_core'])==int(c['label']==label)
            assert int(r['in_'+prefix+'_plus_mixed'])==int(c['label'] in {label,'mixed_fibroblast_macrophage'})
    return dict(method='Separate CSV reads and Python integers/math.fsum/log1p; no NumPy or main-analysis function reuse',library_values_checked=nchecks,attribution_rows_checked=len(attribution),contrasts_checked=len(contrasts),crossed_differences_checked=len(crossed),all_barcode_memberships_checked=len(members),passed=True,replication=False)
if __name__=='__main__':
    import sys
    print(json.dumps(verify(Path(sys.argv[1])),indent=2))
