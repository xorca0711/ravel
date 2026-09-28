"""Dependency-free independent verification from saved cells, PCs and matching edges."""
import csv, hashlib, json, math, statistics, subprocess
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE.parents[2]; OUT=BASE/'tables/corrected_c1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read_json(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(name):
    with (OUT/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
def close(a,b,tol=1e-10):
    assert abs(float(a)-float(b))<=tol,(a,b)
run=read_json(OUT/'run_record.json'); checks=[]
assert run['status']=='corrected_C1_exploratory_complete' and run['biological_units_available']==0 and not run['formal_inference']
for file,digest in run['output_sha256'].items(): assert sha(OUT/file)==digest,file
assert sha(BASE/'scripts/02_run_corrected_c1.py')==run['script_sha256']
assert sha(BASE/'scripts/c1_invariants.py')==run['helper_sha256']; checks.append('runner_and_all_output_hashes')
for file,digest in run['original_stage1_hashes'].items(): assert sha(ROOT/file)==digest,file
assert run['original_stage1_unchanged']; checks.append('original_Stage1_preserved')
spec=BASE/'config/corrected_c1_specification.json'
blob=subprocess.check_output(['git','show',run['specification_commit']+':'+spec.relative_to(ROOT).as_posix()],cwd=ROOT)
assert hashlib.sha256(blob).hexdigest()==sha(spec)==run['specification_sha256']; checks.append('committed_amendment_identity')
excluded=set(r['gene'] for r in csv.DictReader((BASE/'config/excluded_genes.tsv').open(),delimiter='\t'))
features=rows('latent_features.csv')
assert len(excluded)==660 and len(features)==4000
assert all(r['gene'] not in excluded and not r['gene'].lower().startswith('mt-') for r in features)
assert len({(r['library'],r['original_feature_index']) for r in features})==len(features); checks.append('gene_exclusion_and_unique_feature_rows')
cells=rows('cell_outcomes.csv'); cell={(r['library'],r['barcode']):r for r in cells}; assert len(cell)==len(cells)==1532
coords={}
for gsm in run['libraries']:
    cc=rows(gsm+'_coordinates.csv')
    for row in cc:
        key=(gsm,row['barcode']); assert key in cell and row['depth_quartile']==cell[key]['depth_quartile']; close(row['remaining_gene_umis'],cell[key]['remaining_gene_umis'])
        coords[key]=[float(row['PC'+str(j)]) for j in range(1,21)]
    assert len(cc)==run['libraries'][gsm]['cells']
    assert hashlib.sha256('\n'.join(row['barcode'] for row in cc).encode()).hexdigest()==run['libraries'][gsm]['fixed_barcode_sha256']
assert set(coords)==set(cell); checks.append('same_fixed_population_for_coordinates_and_outcomes')
edge_groups=defaultdict(list)
for edge in rows('matched_edges.csv'):
    gsm,k=edge['library'],int(edge['k']); p=(gsm,edge['positive_barcode']); n=(gsm,edge['negative_barcode'])
    assert p in cell and n in cell and cell[p]['positive']=='True' and cell[n]['positive']=='False'
    assert cell[p]['depth_quartile']==cell[n]['depth_quartile']==edge['depth_quartile']
    actual=math.dist(coords[p],coords[n]); close(actual,edge['distance'],1e-8)
    edge_groups[(gsm,k)].append(edge)
assert len(edge_groups)==6; checks.append('within_library_depth_matches_and_distances')
quality={(r['library'],int(r['k'])):r for r in rows('matching_quality.csv')}
effects_table={(r['library'],int(r['k']),r['endpoint']):r for r in rows('effects.csv')}
assert len(effects_table)==42
max_error=0.0
for (gsm,k),edges in edge_groups.items():
    library=[r for r in cells if r['library']==gsm]; positives={r['barcode'] for r in library if r['positive']=='True'}; negative=[r for r in library if r['positive']=='False']
    by_positive=defaultdict(list)
    for e in edges: by_positive[e['positive_barcode']].append(e['negative_barcode'])
    assert set(by_positive)==positives and all(len(v)==len(set(v))==k for v in by_positive.values())
    counts=Counter(e['negative_barcode'] for e in edges); q=quality[(gsm,k)]
    assert len(counts)>=30 and len(counts)==int(q['unique_matched_negatives'])
    weights=[v/len(edges) for v in counts.values()]
    close(1/sum(w*w for w in weights),q['negative_weight_ESS'])
    assert len(positives)==int(q['fixed_positives'])==int(q['matched_positives'])
    # Verify the saved controls are the actual deterministic nearest negatives.
    for p,chosen in by_positive.items():
        key=(gsm,p); candidates=[n for n in negative if n['depth_quartile']==cell[key]['depth_quartile']]
        nearest=sorted(candidates,key=lambda n:(math.dist(coords[key],coords[(gsm,n['barcode'])]),n['barcode']))[:k]
        assert chosen==[n['barcode'] for n in nearest]
    for ep in ['priming_associated','AT2_identity','AT1_identity','Itga2','cycling','shared_gate_cycle_stress_disjoint','lesion_gate_cycle_stress_disjoint']:
        pos_values=[float(cell[(gsm,p)][ep]) for p in sorted(positives)]; neg_values=[float(r[ep]) for r in negative]
        marginal=statistics.mean(pos_values)-statistics.mean(neg_values)
        matched=statistics.mean(float(cell[(gsm,p)][ep])-statistics.mean(float(cell[(gsm,n)][ep]) for n in by_positive[p]) for p in sorted(positives))
        sd=statistics.stdev(float(r[ep]) for r in library)
        actual={'marginal_raw':marginal,'matched_raw':matched,'fixed_population_sd':sd,'marginal_standardized':marginal/sd,'matched_standardized':matched/sd}
        saved=effects_table[(gsm,k,ep)]
        for field,value in actual.items():
            error=abs(value-float(saved[field])); max_error=max(max_error,error); assert error<1e-10,(gsm,k,ep,field,error)
checks+=['all_fixed_positives_retained_and_control_reuse_accounted','deterministic_nearest_controls_recomputed','42_effects_recomputed_on_common_scale']
parity=rows('instrument_parity.csv'); assert len(parity)==14 and max(float(r['max_abs_score_error']) for r in parity)<=1e-8
assert all(r['totals_and_gate_parity']=='True' for r in parity); checks.append('raw_instrument_parity_gate_saved')
record={'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'n_checks':len(checks),'verifier_sha256':sha(Path(__file__)),'run_record_sha256':sha(OUT/'run_record.json'),'effect_rows_recomputed':42,'maximum_effect_recalculation_error':max_error,'fixed_cells':1532,'library_k_comparisons':6,'inference':False,'dependencies':'Python standard library only'}
(BASE/'tables/correction_verification.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['status','n_checks','effect_rows_recomputed','maximum_effect_recalculation_error']}))
