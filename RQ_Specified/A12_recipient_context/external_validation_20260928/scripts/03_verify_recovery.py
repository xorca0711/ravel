"""Verify A12 recovery integrity and eligibility arithmetic, without expression access."""
import csv, gzip, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[2]
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def table(name):
    with (BASE/'tables'/name).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
run=read(BASE/'tables/recovery_run.json'); checks=[]
assert run['model_fits']==0 and not run['external_scores_produced'] and not run['external_expression_opened']; checks.append('no_external_score_or_fit')
spec=BASE/'config/prospective_gate_specification.json'
assert sha(spec)==run['specification_sha256']
frozen=subprocess.check_output(['git','show',run['preregistration_commit']+':'+spec.relative_to(ROOT).as_posix()],cwd=ROOT)
assert hashlib.sha256(frozen).hexdigest()==sha(spec); checks.append('committed_prospective_specification')
for key,value in run['inputs'].items():
    path=Path(key); assert sha(path)==value['sha256'] and path.stat().st_size==value['bytes']
for key,value in run['output_sha256'].items(): assert sha(BASE/key)==value
assert sha(BASE/'scripts/02_audit_candidate_gates.py')==run['script_sha256']; checks.append('metadata_inputs_and_audit_outputs_hashes')
manifest=read(BASE/'sources/retrieval_manifest.json'); assert len(manifest['records'])==3 and not manifest['expression_opened']
for record in manifest['records']:
    path=BASE/record['metadata_file']; assert sha(path)==record['sha256'] and path.stat().st_size==record['bytes']
    assert '^SERIES = '+record['accession'] in gzip.decompress(path.read_bytes()).decode()
    metadata=BASE/'sources'/f"{record['accession']}_metadata.json"; assert sha(metadata)==record['extracted_sha256']
    assert len(read(metadata)['samples'])==record['samples']
checks.append('three_complete_GEO_metadata_manifests')
pairs=table('kim_patient_intersection.tsv'); assert len(pairs)==10
assert all(int(p['normal_AT2_cells'])>=50 and int(p['tumour_AT2_cells'])==0 for p in pairs)
assert all(int(p[a+'_candidate_macrophage_cells'])>=50 for p in pairs for a in ['normal','tumour'])
assert all(p['count_intersection_both_50']=='False' and p['fixed_state_admitted']=='False' for p in pairs)
assert len(table('kim_sample_crosswalk.tsv'))==22; checks.append('Kim_ten_pairs_zero_AT2_intersection')
laugh=table('laughney_sample_manifest.tsv'); lpair=table('laughney_title_pair_intersection.tsv')
assert len(laugh)==17 and sum(r['arm']=='NORMAL' for r in laugh)==4
assert {r['patient_token'] for r in lpair}=={'LX675','LX682','LX684'}
assert all(r['normal_chemotherapy']==r['tumour_chemotherapy']=='No' for r in lpair); checks.append('Laughney_three_title_pairs_four_normal_upper_bound')
wu=table('wu_sample_manifest.tsv'); assert len(wu)==42 and all(r['normal_arm_available']=='False' for r in wu)
evidence=read(BASE/'sources/primary_source_evidence.json'); wu_source=next(r for r in evidence['records'] if r['cohort']=='GSE148071')
assert wu_source['paper_url']=='https://www.nature.com/articles/s41467-021-22801-0' and 'primary lung tumors' in wu_source['short_verbatim_excerpt']; checks.append('Wu_zero_normal_arms_with_primary_paper_provenance')
ledger=read(BASE/'tables/candidate_gate_ledger.json'); assert len(ledger)==3 and all(r['decision'].startswith('ineligible_') for r in ledger)
assert ledger[0]['paired_source_recipient_count_intersection']==0 and ledger[1]['paired_source_recipient_count_intersection'] is None and ledger[2]['paired_source_recipient_count_intersection']==0
assert all(not row['response_opened'] for row in ledger); checks.append('unknown_counts_distinguished_from_zero_units')
record={'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'n_checks':len(checks),'verifier_sha256':sha(Path(__file__)),'recovery_run_sha256':sha(BASE/'tables/recovery_run.json'),'primary_source_evidence_sha256':sha(BASE/'sources/primary_source_evidence.json'),'report_sha256':sha(BASE/'reports/RECOVERY_REPORT.md'),'candidates':3,'external_scores':0,'model_fits':0}
(BASE/'tables/verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':record['status'],'checks':record['n_checks'],'candidates':3,'external_scores':0}))
