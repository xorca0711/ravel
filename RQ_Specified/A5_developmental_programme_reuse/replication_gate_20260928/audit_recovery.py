"""Reproduce metadata-only A5 recovery inventory and fail-closed candidate gates.

No expression matrix is opened; no cell-state arm size or programme score is computed.
The notebook's published QC output is extracted, not recomputed from expression.
"""
import csv, gzip, hashlib, json, re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCES = HERE / 'sources'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None; self.cell=None
    def handle_starttag(self, tag, attrs):
        if tag=='tr': self.row=[]
        if tag in ('th','td'): self.cell=[]
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('th','td') and self.cell is not None:
            self.row.append(''.join(self.cell).strip());self.cell=None
        if tag=='tr' and self.row is not None:
            self.rows.append(self.row);self.row=None

# Verify original A5 instrument/modules, without any biological expression score.
frozen = read_json(HERE/'frozen_input_hashes.json')
assert all(digest(REPO / row['path'])==row['sha256'] for row in frozen)
modules=read_json(HERE.parent/'tables/external_test_modules.json')['modules']
module_sizes={k:len(modules[k]) for k in ['Guo_AT1_AT2_external','Guo_minus_identity','Guo_minus_identity_and_controls']}
assert list(module_sizes.values()) == [99,57,53]
config=read_json(HERE.parent/'config/strunz_test_contract.json')
assert (config['day_min'],config['day_max'],config['depth_umi'],config['cell_floor'],config['unit_floor'],config['coverage_floor']) == (2,21,500,30,3,0.7)

notebook=read_json(SOURCES/'GSE303646_code_markers.txt')
cell=notebook['cells'][8]
assert '20250506_QC_metrics_BleoAging.txt' in ''.join(cell['source'])
html=''.join(cell['outputs'][0]['data']['text/html'])
parser=Tables();parser.feed(html)
headers=parser.rows[0];records=[dict(zip(headers,row)) for row in parser.rows[1:]]
assert all(len(row)==len(headers) for row in parser.rows)
assert '...' in headers
fields=['identifier','age','day','timepoints','sex','treatment','n_counts','n_genes','percent_mito','n_cells']
assert all(field in headers for field in fields)
qc=[{k:row[k] for k in fields} for row in records]
assert len({row['identifier'] for row in qc})==len(qc)==56
with (HERE/'GSE303646_author_qc_metadata.tsv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.DictWriter(stream,fieldnames=fields,delimiter='\t');writer.writeheader();writer.writerows(qc)

geo_path=REPO/'docs/roadmap_runs/2026-09-27-followthrough/metadata/GSE303646.json'
geo=read_json(geo_path)
by_id={s['!Sample_title'][0].split('_')[0].lower():s for s in geo['samples']}
assert set(by_id)=={row['identifier'] for row in qc}
matched=[];mismatches=[]
for row in qc:
    sample=by_id[row['identifier']]
    title=sample['!Sample_title'][0]
    expected=[row['age'],row['day'], 'control' if row['treatment']=='control' else 'bleo']
    if not all(token in title.lower().split('_') for token in expected):
        mismatches.append({'identifier':row['identifier'],'title':title,'author':row})
    matched.append({'identifier':row['identifier'],'geo_accession':sample['accession'],'geo_title':title,
                    'age':row['age'],'day':row['day'],'sex':row['sex'],'treatment':row['treatment'],
                    'mouse_id':'UNRESOLVED','author_state_map':'UNRECOVERED'})
with (HERE/'GSE303646_library_crosswalk.tsv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(matched[0]),delimiter='\t');writer.writeheader();writer.writerows(matched)

summary=gzip.decompress((SOURCES/'GSE303646_sample_GSM9131916_dge_summary.txt').read_bytes()).decode()
summary_header=next(s for s in summary.splitlines() if s.startswith('CELL_BARCODE'))
assert summary_header.split('\t')==['CELL_BARCODE','NUM_GENIC_READS','NUM_TRANSCRIPTS','NUM_GENES']
assert 'OUTPUT_READS_INSTEAD=false' in summary and 'MOLECULAR_BARCODE_TAG=XM' in summary

code=read_json(SOURCES/'GSE303646_code_targeted_nichenet.txt')
label_cell=''.join(code['cells'][5]['source'])
assert all('"'+label+'"' in label_cell for label in ['AT2_activated','AT2','Krt8-ADI'])
tree=read_json(SOURCES/'GSE303646_github_tree_master.txt')
assert not tree.get('truncated')
assert not any(p['path'].endswith(('.h5ad','.rds','.RData')) for p in tree['tree'])
source_rows=read_json(HERE/'source_ledger.json')
assert all(digest(HERE/r['path'])==r['sha256'] for r in source_rows if r['status']=='downloaded')

within=[row for row in qc if row['treatment']=='bleo' and 2<=int(row['day'][1:])<=21]
inventory={
    'kind':'author_reported_library_inventory_not_mouse_or_paired_cell_eligibility',
    'qc_notebook_cell':8,'qc_source_output':'text/html; epithelial columns elided',
    'author_qc_libraries':len(qc),'geo_libraries':len(geo['samples']),
    'paper_stated_mice':55,'paper_library_discrepancy_resolved':False,
    'author_reported_retained_cells_sum':sum(int(r['n_cells']) for r in qc),
    'fixed_window_library_inventory':len(within),
    'fixed_window_inventory_by_age_day':dict(sorted(Counter(r['age']+'_'+r['day'] for r in within).items())),
    'geo_author_age_day_treatment_mismatches':mismatches,
    'recovered_author_label_vocabulary':['Krt8-ADI','AT2_activated','AT2'],
    'label_vocabulary_is_barcode_map':False,
    'author_object_required':'230111_Bleo_Ageing_annotated_final.h5ad',
    'author_qc_export_referenced_but_not_deposited':'20250506_QC_metrics_BleoAging.txt',
    'author_obs_fields_referenced':['identifier','name','cell_type','meta_label','day','age','sex','treatment'],
    'raw_umi_metadata_evidence':{'sample':'GSM9131916','library':'muc26501','OUTPUT_READS_INSTEAD':False,'MOLECULAR_BARCODE_TAG':'XM','summary_columns':summary_header.split('\t'),'applies_to_all_libraries':False,'matrix_integrity_and_alignment':'not_assessed'},
    'source_revision':tree['sha'], 'expression_matrices_downloaded':0,
    'paired_arm_counts_computed':False,'module_coverage_computed':False,'expression_scores_computed':False,
}
save_json('GSE303646_recovered_evidence.json',inventory)

def gate(status,reason):return {'status':status,'reason':reason}
verdicts={
 'schema':'a5-external-replication-recovery-gates/v1','date':'2026-09-28',
 'recovery_spec_checkpoint':'f3950253ae229f062dbae94551b04a908a8e5ade',
 'unchanged_module_sizes':module_sizes,
 'expression_matrices_downloaded':0,'new_expression_scores':False,
 'candidates':[
  {'candidate':'GSE303646','overall':'blocked_missing_metadata',
   'gates':{
    'sterile_mouse_scope':gate('pass','Author paper and GEO identify mouse bleomycin repair; days 3/10/20 are inside fixed day 2-21.'),
    'external_cohort_independence':gate('unresolved','Separate study/accession and a 2021 DGE processing header support a distinct cohort, but no animal-level provenance establishes no reuse of prior Strunz animals/cells. Existing A5 and author cohort results have been seen; this is not blind validation.'),
    'mouse_identity':gate('unresolved','56 GEO libraries align with 56 author QC identifiers; paper says 55 mice. Author donor field name is referenced but unavailable. No barcode-to-verified-mouse mapping or technical-split/pooling reconciliation recovered.'),
    'author_state_vocabulary':gate('pass','Pinned author NicheNet notebook explicitly includes Krt8-ADI and AT2_activated (plus AT2). Their existence is now confirmed, not absent.'),
    'programme_independent_barcode_state_map':gate('unresolved','Author cell_type/meta_label live in a referenced local h5ad, not recovered from GEO, code tree or public browser entry page. Canonical-marker author annotation is described, but exact classification dependency and barcode map cannot be audited. No Guo-module relabelling performed.'),
    'raw_umi_provenance':gate('unresolved','One downloaded in-window DGE summary explicitly uses molecule mode and a molecular barcode tag. Full-cohort raw-integer matrix provenance, absence of SoupX/normalization substitution, gene universe and exact barcode alignment remain untested.'),
    'fixed_module_coverage':gate('not_assessed','Metadata prerequisites do not pass; no new gene-universe/matrix download or 99/57/53 coverage count.'),
    'paired_depth_cell_mouse_floors':gate('not_assessed','No verified mouse/state map, so no 500-UMI/30-cell/three-mouse eligibility count and no scores.')},
   'required_enabling_fields':['raw_cell_barcode','GEO_library_or_identifier','biological_mouse_id','pool_or_technical_split_id','injury_day','age','treatment','author_cell_type','author_annotation_method_and_version','raw_UMI_matrix_correspondence'],
   'specific_enabling_artifact':'Author export of obs from 230111_Bleo_Ageing_annotated_final.h5ad, preserving identifier/name/cell_type, plus animal provenance reconciliation and raw DGE alignment.'},
  {'candidate':'GSE202325','overall':'not_assessed_out_of_scope',
   'gates':{'scope':gate('not_assessed','Existing GEO title identifies infection cohort; no further primary-source/protocol/expression analysis under the frozen non-pathogen recovery scope.'),'author_state_map':gate('not_assessed','Previous audit reported broad AT2 labels and missing exact activated/transitional map. This is inherited evidence, not a new biological ineligibility finding.')},
   'missing_for_unchanged_validation_in_prior_audit':['programme-independent per-barcode transitional/activated-AT2 labels','verified per-barcode mouse provenance'],
   'source':'docs/roadmap_runs/2026-09-27-followthrough/metadata/GSE202325.json; EXPANDED_CANDIDATE_AUDIT.md'},
  {'candidate':'Hippo_LOX / Zenodo 14229565','overall':'fails_unchanged_mouse_cohort_scope',
   'gates':{'scope':gate('fail','Primary paper separates mouse perturbation experiments from the newly deposited single-nucleus data, which are human PCLS from two donor lungs. Zenodo names LT106/LT107 preparations. These are not mouse repair cohorts for unchanged A5.'),'mouse_state_and_count_gates':gate('not_assessed','Stop after species/experimental-unit mismatch; no deposited expression matrices downloaded.')},
   'source':'https://www.nature.com/articles/s41467-025-61795-x; https://zenodo.org/records/14229565'}],
 'stop_reason':'Bounded named-candidate plus one source-led alternative search completed. GSE303646 is an access/identity block; absence of state labels in recovered files does not prove absence of the states.',
}
save_json('candidate_verdicts.json',verdicts)
# Title-only sanitized record; never reproduce infection methods in recovery outputs.
g202_path=REPO/'docs/roadmap_runs/2026-09-27-followthrough/metadata/GSE202325.json'
g202=read_json(g202_path)
save_json('GSE202325_scope_record.json',{'accession':g202['accession'],'title':g202['series']['!Series_title'][0],'status':'not_assessed_out_of_scope','source_path':str(g202_path.relative_to(REPO)).replace('\\','/'),'source_sha256':digest(g202_path)})
save_json('verification.json',{'frozen_input_hashes_match':True,'module_sizes':module_sizes,'download_hashes_match':True,'qc_library_identifiers_unique':True,'qc_and_geo_identifiers_exact_match':True,'geo_qc_characteristics_match':not mismatches,'author_epithelial_counts_elided':True,'raw_umi_summary_metadata_valid':True,'author_state_names_present':True,'no_new_expression_scores':True,'script_sha256':digest(Path(__file__))})
print(json.dumps({'libraries_recovered':len(qc),'window_libraries_not_eligible_mice':len(within),'characteristic_mismatches':len(mismatches),'state_names_confirmed':inventory['recovered_author_label_vocabulary'],'scoring':'not_run','verdict':'blocked_missing_metadata'}))
