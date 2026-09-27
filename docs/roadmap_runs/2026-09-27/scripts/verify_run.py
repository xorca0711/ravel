"""Read-only reproduction of roadmap accounting, joins and eligibility decisions."""
import ast
import collections
import csv
import gzip
import hashlib
import io
import json
import statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parents[1]
def j(path):return json.loads(path.read_text(encoding='utf-8'))
def tab(path,delimiter='\t'):return list(csv.DictReader(path.open(encoding='utf-8-sig',newline=''),delimiter=delimiter))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    status=j(OUT/'status.json')
    assert set(status['packages'])=={f'P{i}' for i in range(6)}
    assert all(v['status']!='pending' for v in status['packages'].values())
    for v in status['packages'].values():assert (OUT/v['report']).is_file()
    outcomes=j(OUT/'rq_outcomes.json')['questions']
    assert {r['rq'] for r in outcomes}=={f'A{i}' for i in range(16)}|{'A12-S1'}
    # These hashes capture then-current living documents, which dated follow-ups can change.
    changed_context=[r['rq'] for r in outcomes if sha(ROOT/r['evidence'].split('#')[0])!=r['evidence_sha256']]
    # Immutable analytical inputs retain strict hash and content checks below.
    parent=ROOT/'RQ_Specified/A5_developmental_programme_reuse/config/strunz_test_contract.json'
    contract=j(OUT/'outcome_contract.json')
    assert contract['frozen_parent_sha256']==sha(parent) and contract['inherited_instrument']==j(parent)
    cross=tab(OUT/'P1_library_crosswalk.tsv')
    old=tab(ROOT/'RQ_Specified/A10_organoid_growth_outcome/tables/well_join.tsv')
    gsm=tab(ROOT/'RQ_Specified/A10_organoid_growth_outcome/tables/followup_v1/diagnostic_geo_sample_fields.tsv')
    assert len(cross)==886 and len({r['library'] for r in cross})==886
    assert {r['library'] for r in cross}=={r['library name'] for r in old}
    lookup={r['library_name']:r for r in gsm}
    for r in cross:assert r['gsm']==lookup[r['library']]['gsm']
    assert sum(r['guide_pool_sha256']=='not_in_plate_design' for r in cross)==30
    for target in ['AREG','EGFR','ERBB2','ERBB3','ERBB4','ITGB6']:
        rr=[r for r in cross if r['target']==target]
        assert len(rr)==4
        assert len({(r['plate'],r['position'],r['guide_pool_sha256']) for r in rr})==1
    diag=j(ROOT/'RQ_Specified/A10_organoid_growth_outcome/tables/followup_v1/diagnostic_run.json')
    for name in ['GSE307112_plate_design.csv.gz','GSE307112_imaging_outputs.csv.gz']:
        assert sha(OUT/'inputs'/name)==diag['inputs'][name]['sha256']
    choi=j(OUT/'GSE145031_sample_metadata.json')['samples']
    assert len(choi)==6 and sum(s['!Sample_title']==['Day14_AT2_Tomato'] for s in choi)==1
    fallback=j(OUT/'GSE113049_sample_metadata.json')['samples']
    injured=[s for s in fallback if 'Injured Mouse' in s['!Sample_title'][0]]
    assert len(injured)==4 and len({s['!Sample_title'][0].split(' Injured')[0] for s in injured})==2
    source=ROOT/'Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_sources/IL1B_source_fractions.csv'
    assert sha(source)==j(OUT/'P4_attribution_spec.json')['sha256']
    grouped=collections.defaultdict(dict)
    for r in tab(source,','):grouped[r['patient'],r['histology'],r['uncertainty']][r['broad']]=float(r['count_sum'])
    bounds=tab(OUT/'P4_source_attribution_bounds.tsv')
    assert len(bounds)==70 and len({r['patient'] for r in bounds})==23
    for r in bounds:
        d=grouped[r['patient'],r['histology'],'0.2'];total=sum(d.values())
        assert abs(float(r['conditional_lower'])-d['Macrophages']/total)<1e-12
        assert abs(float(r['conditional_upper'])-(d['Macrophages']+d['Unassigned'])/total)<1e-12
    counts={}
    for threshold in ['0.2','0.3']:
        values=[v for k,v in grouped.items() if k[2]==threshold]
        counts[threshold]=sum(2*v['Macrophages']<=sum(v.values())<2*(v['Macrophages']+v['Unassigned']) for v in values)
    assert counts=={'0.2':62,'0.3':55}
    for r in j(OUT/'P4_confidence_and_model_readiness.json')['confidence_sensitivity']:
        values=[v for k,v in grouped.items() if k[1]==r['histology'] and k[2]==r['threshold']]
        assert abs(r['median_unassigned']-statistics.median(v['Unassigned']/sum(v.values()) for v in values))<1e-12
    for name,digest in j(OUT/'P3_linkage_audit.json')['files'].items():
        assert sha(ROOT/Path(name.replace('\\','/')))==digest
    p3=j(OUT/'P3_feature_outcome_contract.json')
    assert p3['primary_feature']['end_0based_exclusive']-p3['primary_feature']['start_0based']==2000
    assert 'CAV1' in p3['outcome']['required_criteria']
    p5=j(OUT/'P5_withdrawal_design.json')
    assert len(p5['arms'])==6 and len({r['arm'] for r in p5['arms']})==6
    assert len(p5['contrasts'])==2 and p5['sample_size'] is None
    for path in (OUT/'scripts').glob('*.py'):ast.parse(path.read_text(encoding='utf-8'),filename=path.name)
    print(json.dumps({'status':'passed','RQ_entries':17,'libraries_joined':886,'A5_candidates_checked':2,
                      'IL1B_units':70,'primary_assignment_sensitive':62,'sensitivity_assignment_sensitive':55,
                      'P3_linked_designs':0,'P5_design_arms':6,'new_biological_experiments':0,'living_context_changed_since_snapshot':changed_context}))

if __name__=='__main__':main()
