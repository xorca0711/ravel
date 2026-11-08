"""Independently review metadata arithmetic and source/code alias evidence."""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
out=Path(a.output);runs=Path('analysis/research/runs')
meta=runs/'nn26_rds_metadata_review_v1';prior=runs/'nn26_rds_metadata_v2'
base=Path('Research Article/ungated_navarro_negredo_2026_aged_brain_il10')
read=lambda path:json.loads(path.read_text())
write=lambda name,x:(out/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
qc=read(meta/'qc.json');norm=read(meta/'normalization.json');alignment=read(meta/'alignment.json')
captions=read(base/'source_context/figure_captions.json')['captions']
assert 'Figures 3, 4' in captions['F3'] and '0.02 mg/mL' in captions['F3'] and 'Stat3 (E)' in captions['F3']
source_crosswalk=read(runs/'nn26_source_qualification_v1/source_crosswalk.json')
main_sources=[r for r in source_crosswalk if r['sample_accession']=='SAMN53298933']
assert len(main_sources)==6
for name in ['qc.json','alignment.json','object_inventory.json','recovery.tsv','normalization_samples.tsv','normalization.json']:
    assert (meta/name).read_bytes()==(prior/name).read_bytes(),name
warnings=read(meta/'captured_warnings.json')
assert warnings['count']==norm['sample_cells']==192
assert all(w['message']=='row names were found from a short variable and have been discarded' and w['call'].startswith('data.frame(cell = colnames(counts)[j]') for w in warnings['records'])
assert all(alignment[k] for k in list(alignment)[:6])
assert alignment['missing_condition']==alignment['missing_annotation']==0
assert qc['nCount_matches']==qc['nFeature_matches']==0
assert all(v==0 for v in qc['thresholds'].values())
assert qc['sparse_counts']['negative']==qc['sparse_counts']['noninteger']==qc['sparse_counts']['nonfinite']==0
with (meta/'normalization_samples.tsv').open() as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
errors=[];keys=set()
for row in rows:
    key=(row['cell'],row['gene']);assert key not in keys;keys.add(key)
    raw=float(row['raw_count']);total=float(row['library_total']);stored=float(row['stored'])
    expected=math.log1p(raw/total*norm['scale_factor'])
    assert all(math.isfinite(v) for v in [raw,total,stored,expected]) and total>0
    errors.append(abs(stored-expected))
assert max(errors)<=1e-10 and len(rows)==norm['sample_entries']
with (meta/'recovery.tsv').open() as f: recovery=list(csv.DictReader(f,delimiter='\t'))
totals=collections.Counter()
for row in recovery:totals[row['condition']]+=int(row['cells'])
assert dict(totals)==qc['conditions'] and sum(totals.values())==qc['cells']
with zipfile.ZipFile('raw_data/navarro_2026/source_v1/code_v1.zip') as archive:
    names=archive.namelist()
    member=next(n for n in names if n.endswith('IL10/2.Microglia.R'))
    content=archive.read(member);source=content.decode('utf-8-sig')
    vectors={}
    for name,expected_len in [('il10',28),('ifng',20)]:
        match=re.search(r'\b'+name+r'\s*<-\s*c\((.*?)\)',source,re.S)
        assert match
        genes=re.findall(r'"([^"]+)"',match.group(1));assert len(genes)==expected_len and len(set(genes))==len(genes)
        vectors[name]={'genes':genes,'source_member':member,'source_sha256':hashlib.sha256(content).hexdigest(),
          'line_start':source[:match.start()].count('\n')+1,'line_end':source[:match.end()].count('\n')+1,
          'interpretation':'Individual transcript markers; no combined score or common favorable direction.'}
    hallmark_present=any(n.endswith('mouse.gene.hallmark.kegg.reactome.rda') for n in names)
    assert not hallmark_present
    assert 'gene <- "Socs3"' in source and '##Figure 3E' in source
vectors['tcell_primary']={'genes':['Ifng','Gzmb'],'source_member':next(n for n in names if n.endswith('IL10/3.Tcells.R')),
                        'source_locator':'gene vector line 40; Gzmb-positive selection lines 66-70; published Fig.3K',
                        'interpretation':'All original T_cells; separately report Gzmb-positive subset with all-T denominator.'}
write('marker_manifest.json',{'vectors':vectors,'hallmark_rda_present':False,
      'hallmark_limit':'Exact Fig.4C hallmark score is not reproduced or replaced with a current gene set.',
      'Figure3E_discrepancy':'Code plots Socs3; supplied published caption names Stat3. Both remain separate explicit markers.'})
crosswalk=[]
for alias,n in qc['conditions'].items():
    d={'object_alias':alias,'recovered_cells':n,'accession_barcode_join_verified':False,
       'dose_directly_attached_to_cells':False,'true_mouse_key':None}
    if alias in ['Control','Young']:
        d.update(role='old_vehicle' if alias=='Control' else 'young_vehicle',comparison_eligible=True,
          evidence_strength='source/code control-label correspondence; no molecular accession join',caption_associated_dose_mg_per_ml=None)
    elif alias in ['WT5','Mut5']:
        d.update(role='WT' if alias=='WT5' else 'D25K (author Mut alias)',pair='WT5/Mut5',comparison_eligible=True,
          caption_associated_dose_mg_per_ml=0.02,evidence_strength='Figure-linked: IL10/2.Microglia.R lines 49-61 selects WT5/Mut5 for main Fig.3; caption Fig.3B states 0.02 mg/mL. Indirect alias-dose cross-reference, not barcode proof.')
    elif alias in ['WT1','Mut1']:
        d.update(role='WT' if alias=='WT1' else 'D25K (author Mut alias)',pair='WT1/Mut1',comparison_eligible=True,
          caption_associated_dose_mg_per_ml=None,possible_other_published_dose_mg_per_ml=0.1,
          evidence_strength='Other-concentration pair in author code lines 107-110. 0.1 mg/mL is a remaining-dose inference, not a verified numerical cell-dose join.')
    else:
        d.update(role='unresolved additional author-code condition',comparison_eligible=False,caption_associated_dose_mg_per_ml=None,
          evidence_strength='WT50/Mut50 are genuinely retained; no established numeric dose, accession or pool-size mapping to the six reported main RNA libraries.')
    crosswalk.append(d)
write('alias_crosswalk.json',crosswalk)
write('independent_verification.json',{'normalization_entries_checked':len(rows),'max_absolute_error_python':max(errors),
  'tolerance':1e-10,'unique_cell_gene_pairs':len(keys),'recovery_total_checked':sum(totals.values()),
  'v2_review_numeric_and_inventory_files_byte_identical':True,
  'warnings':{'count':warnings['count'],'message_counts':dict(collections.Counter(w['message'] for w in warnings['records'])),
      'assessment':'Named scalar library totals supplied an unused data.frame row name; R discarded only these implicit row names. Explicit cell/gene/condition columns are retained, keys unique, all independent arithmetic passes. No annotation or object validity warning occurred.'},
  'qc_field_definitions':{'nCount_matches':'maximum absolute difference, reconstructed counts sum minus metadata; zero is exact agreement',
      'nFeature_matches':'maximum absolute difference, reconstructed positive features minus metadata; zero is exact agreement',
      'thresholds':'counts of cells violating each published threshold; all zero'},
  'independent_biological_replication':False})
write('qualification.json',{'qualified_for':'Finite-pool alias-pair description on RNA LogNormalize(10000), original broad annotations',
  'eligible_aliases':['Young','Control','WT5','Mut5','WT1','Mut1'],'held_aliases':['WT50','Mut50'],
  'comparison_pairs':[['WT5','Mut5'],['WT1','Mut1']],
  'normalization_verified':True,'marker_vectors_frozen_in_output':True,
  'donor_assignment_established':False,'reported_source_libraries':6,'observed_object_conditions':8,
  'broad_microglia_equal_author_downstream_plot_population':False,
  'downstream_Micro_types_present':qc['downstream_Micro_types_present'],
  'filename_discrepancy':'Deposited main file lacks _IL10 suffix used by downstream scripts; source and object are qualified for broad-annotation description, not proven identical to that downstream file.',
  'numeric_dose_mapping':'Use alias pairs as primary identifiers; main pair is caption-associated with 0.02 mg/mL, other pair is not numerically verified.',
  'optional_sources':'Not eligible for automatic acquisition: no concrete comparison requires them for this bounded description; they cannot repair pooled units or the unresolved extra aliases.',
  'scientific_acceptance':'not_assessed'})
