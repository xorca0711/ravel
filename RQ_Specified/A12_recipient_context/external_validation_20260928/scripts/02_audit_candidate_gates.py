"""Metadata-only A12 gate recovery. Expression matrices are never opened."""
import argparse, csv, gzip, hashlib, json, math, re, subprocess, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
SPEC = BASE/'config/prospective_gate_specification.json'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_tsv(name, rows, fields=None):
    with (BASE/'tables'/name).open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields or list(rows[0]),delimiter='\t')
        writer.writeheader(); writer.writerows(rows)

def patient_table(path):
    # Author workbook has a malformed custom property. Parse original XML without altering it.
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as book:
        shared=[''.join(t.text or '' for t in si.iter('{%s}t'%ns['m'])) for si in ET.fromstring(book.read('xl/sharedStrings.xml')).findall('m:si',ns)]
        rows=[]
        for row in ET.fromstring(book.read('xl/worksheets/sheet1.xml')).iter('{%s}row'%ns['m']):
            values={}
            for cell in row.findall('m:c',ns):
                col=re.match(r'[A-Z]+',cell.get('r')).group(0); value=cell.find('m:v',ns)
                values[col]='' if value is None else (shared[int(value.text)] if cell.get('t')=='s' else value.text)
            rows.append(values)
    header=next(r for r in rows if 'Patient id' in r.values()); keys={v:k for k,v in header.items()}
    return [{'patient':r[keys['Patient id']],'sample':r[keys['Samples']],'origin':r[keys['Tissue origins']],'histology':r.get(keys['Histology'],''),'stage':r.get(keys['Stages'],'')} for r in rows if re.fullmatch(r'LUNG_[NT]\d+',r.get(keys['Samples'],'') or '')]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-root',type=Path,required=True); args=ap.parse_args()
    spec=json.loads(SPEC.read_text(encoding='utf-8-sig'))
    assert spec['fixed_instrument']['cells_per_arm_per_compartment_minimum']==50
    data=args.data_root/'raw_data/GSE131907'
    annotation=data/'GSE131907_Lung_Cancer_cell_annotation.txt.gz'
    workbook=data/'GSE131907_Lung_Cancer_Feature_Summary.xlsx'
    historical=ROOT/'RQ_Specified/A11_lesion_programme_addition/tables/gates_run.json'
    previous=json.loads(historical.read_text())['inputs']
    for path in (annotation,workbook):
        record=next(v for k,v in previous.items() if Path(k).name==path.name)
        assert sha(path)==record['sha256'] and path.stat().st_size==record['bytes']
    samples=patient_table(workbook); assert len({s['sample'] for s in samples})==len(samples)
    geo=json.loads((BASE/'sources/GSE131907_metadata.json').read_text())
    accession={s['title'][0]:s['accession'] for s in geo['samples']}
    for sample in samples:
        sample['accession']=accession[sample['sample']]
    write_tsv('kim_sample_crosswalk.tsv',samples)
    counts=Counter(); origin_counts=Counter(); seen=set(); ncells=0
    with gzip.open(annotation,'rt',encoding='utf-8') as handle:
        for row in csv.DictReader(handle,delimiter='\t'):
            assert row['Index'] not in seen; seen.add(row['Index']); ncells+=1
            counts[(row['Sample'],row['Cell_subtype'])]+=1
            origin_counts[(row['Sample_Origin'],row['Cell_subtype'])]+=1
    write_tsv('kim_annotation_inventory.tsv',[{'origin':origin,'author_subtype':label,'cells':count} for (origin,label),count in sorted(origin_counts.items())])
    by_patient=defaultdict(dict)
    for sample in samples:
        assert sample['origin'] not in by_patient[sample['patient']]
        by_patient[sample['patient']][sample['origin']]=sample
    macrophage_labels=['Alveolar Mac','mo-Mac','Pleural Mac']
    pairs=[]
    for patient,arms in sorted(by_patient.items()):
        if not {'nLung','tLung'}<=arms.keys(): continue
        row={'patient':patient,'histology':arms['tLung']['histology'],'normal_sample':arms['nLung']['sample'],'tumour_sample':arms['tLung']['sample']}
        for arm,origin in [('normal','nLung'),('tumour','tLung')]:
            sample=arms[origin]['sample']
            row[arm+'_AT2_cells']=counts[(sample,'AT2')]
            row[arm+'_candidate_macrophage_cells']=sum(counts[(sample,label)] for label in macrophage_labels)
            row[arm+'_mo_Mac_cells']=counts[(sample,'mo-Mac')]
        row['AT2_both_50']=all(row[arm+'_AT2_cells']>=50 for arm in ['normal','tumour'])
        row['candidate_source_both_50']=all(row[arm+'_candidate_macrophage_cells']>=50 for arm in ['normal','tumour'])
        row['count_intersection_both_50']=row['AT2_both_50'] and row['candidate_source_both_50']
        row['fixed_state_admitted']=False
        row['exclusion']='zero tumour AT2 label; pilot correspondence/confidence not independently adjudicated'
        pairs.append(row)
    write_tsv('kim_patient_intersection.tsv',pairs)
    prior_pairs=list(csv.DictReader((ROOT/'RQ_Specified/A11_lesion_programme_addition/tables/kim_pairing.tsv').open(),delimiter='\t'))
    assert {(p['patient'],p['normal_sample'],p['tumour_sample']) for p in pairs}=={(p['patient'],p['normal_sample'],p['tumour_sample']) for p in prior_pairs}
    assert ncells==208506
    assert sum(origin_counts[(origin,'AT2')] for origin in ['tLung','tL/B'])==0
    assert all(p['tumour_AT2_cells']==0 for p in pairs)
    # Recover the actual submitted 17-sample manifest, without trusting '17 donors' as patient count.
    laugh=json.loads((BASE/'sources/GSE123902_metadata.json').read_text())
    manifest=[]; patient_samples=defaultdict(dict)
    for s in laugh['samples']:
        title=s['title'][0]; match=re.fullmatch(r'MSK_(LX\w+)_(PRIMARY_TUMOUR|NORMAL|METASTASIS)',title); assert match
        token,kind=match.groups()
        characteristics=dict(item.split(': ',1) for item in s['characteristics_ch1'])
        row={'accession':s['accession'],'title':title,'patient_token_from_title':token,'arm':kind,'diagnosis':characteristics.get('diagnosis',''),'chemotherapy':characteristics.get('chemotherapy',''),'stage':characteristics.get('Stage',''),'patient_mapping_provenance':'matched title token; no explicit donor-ID field in GEO'}
        manifest.append(row); assert kind not in patient_samples[token]; patient_samples[token][kind]=row
    write_tsv('laughney_sample_manifest.tsv',manifest)
    laugh_pairs=[]
    for token,arms in sorted(patient_samples.items()):
        if {'PRIMARY_TUMOUR','NORMAL'}<=arms.keys():
            normal,tumour=arms['NORMAL'],arms['PRIMARY_TUMOUR']
            laugh_pairs.append({'patient_token':token,'normal_accession':normal['accession'],'tumour_accession':tumour['accession'],'normal_chemotherapy':normal['chemotherapy'],'tumour_chemotherapy':tumour['chemotherapy'],'source_recipient_cell_intersection':'unknown_not_retrieved_after_unit_ceiling_failure','eligible_for_fit':False})
    write_tsv('laughney_title_pair_intersection.tsv',laugh_pairs)
    normal_count=sum(s['arm']=='NORMAL' for s in manifest)
    assert len(laugh_pairs)==3 and normal_count==4 and len(manifest)==17
    # All Wu biopsies are tumour-derived, as stated in primary-paper Figure 1e.
    wu=json.loads((BASE/'sources/GSE148071_metadata.json').read_text())
    wu_rows=[{'accession':s['accession'],'submitted_sample_title':s['title'][0],'submitted_source':s['source_name_ch1'][0],'clinical_arm':'primary_tumour_biopsy','arm_provenance':'Wu et al. Nature Communications 2021 Figure 1e','normal_arm_available':False,'source_recipient_intersection':'not_applicable_no_normal_arm'} for s in wu['samples']]
    assert len(wu_rows)==42 and len({s['submitted_sample_title'] for s in wu_rows})==42
    write_tsv('wu_sample_manifest.tsv',wu_rows)
    decisions=[
      {'cohort':'GSE131907','series_samples':58,'candidate_primary_lung_normal_samples':sum(s['origin']=='nLung' for s in samples),'paired_metadata_units':len(pairs),'paired_units_kind':'author patient IDs from original workbook','source_both_50_candidate':sum(p['candidate_source_both_50'] for p in pairs),'recipient_AT2_both_50':sum(p['AT2_both_50'] for p in pairs),'paired_source_recipient_count_intersection':sum(p['count_intersection_both_50'] for p in pairs),'admitted_fixed_state_units':0,'decision':'ineligible_state_and_coverage','decisive_reason':'No author AT2 cells in tumour lung; no unchanged AT2 paired units. Macrophage synonym counts are a diagnostic proxy, not an admitted mapping.','unresolved':'No independent pilot-state correspondence/confidence mapping; source attribution remains assignment-conditional.','precision_gate':'fail_zero_eligible_units','response_opened':False},
      {'cohort':'GSE123902','series_samples':17,'candidate_primary_lung_normal_samples':normal_count,'paired_metadata_units':len(laugh_pairs),'paired_units_kind':'matching GEO title tokens; donor-field discrepancy retained','source_both_50_candidate':None,'recipient_AT2_both_50':None,'paired_source_recipient_count_intersection':None,'admitted_fixed_state_units':None,'decision':'ineligible_unit_ceiling','decisive_reason':'Three title-matched untreated primary tumour/normal pairs; only four normal specimens overall, so at most four pairs before state gates, below ten.','unresolved':'GEO says 17 donors but titles imply 14 distinct tokens. No donor table or cell-label mapping recovered after decisive unit ceiling; unknown counts are not zero.','precision_gate':'fail_at_most_four_units','response_opened':False},
      {'cohort':'GSE148071','series_samples':42,'candidate_primary_lung_normal_samples':0,'paired_metadata_units':0,'paired_units_kind':'no normal tissue arm in primary-paper design','source_both_50_candidate':None,'recipient_AT2_both_50':None,'paired_source_recipient_count_intersection':0,'admitted_fixed_state_units':0,'decision':'ineligible_no_paired_normal','decisive_reason':'All 42 biopsies were primary tumours. AT2-like cells inside tumour biopsies cannot supply the separate paired normal tissue arm.','unresolved':'GEO has no patient-linked subtype annotation table; cell counts and confidence/mixture correspondence not recovered after design failure.','precision_gate':'fail_zero_pairs','response_opened':False}
    ]
    (BASE/'tables/candidate_gate_ledger.json').write_text(json.dumps(decisions,indent=2)+'\n',encoding='utf-8')
    write_tsv('candidate_gate_summary.tsv',[{k:d[k] for k in ['cohort','series_samples','paired_metadata_units','paired_source_recipient_count_intersection','decision','precision_gate','response_opened']} for d in decisions])
    import scipy
    from scipy.stats import t
    halfwidth=float(t.ppf(.975,45)/math.sqrt(46)); assert halfwidth<=.30 and t.ppf(.975,44)/math.sqrt(45)>.30
    freeze='f3950253ae229f062dbae94551b04a908a8e5ade'
    frozen=subprocess.check_output(['git','show',freeze+':'+str(SPEC.relative_to(ROOT)).replace('\\','/')],cwd=ROOT)
    assert hashlib.sha256(frozen).hexdigest()==sha(SPEC)
    outputs=list((BASE/'tables').glob('*.tsv'))+[BASE/'tables/candidate_gate_ledger.json']
    run={'status':'bounded_metadata_recovery_complete_no_external_fit','completed_utc':datetime.now(timezone.utc).isoformat(),'preregistration_commit':freeze,'specification_sha256':sha(SPEC),'script_sha256':sha(Path(__file__)),'inputs':{str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in [annotation,workbook,historical,BASE/'sources/retrieval_manifest.json']},'output_sha256':{str(p.relative_to(BASE)).replace('\\','/'):sha(p) for p in outputs},'kim_annotation_rows':ncells,'kim_paired_patients':len(pairs),'kim_source_candidate_both_50':sum(p['candidate_source_both_50'] for p in pairs),'kim_normal_AT2_50':sum(p['normal_AT2_cells']>=50 for p in pairs),'kim_tumour_AT2_cells':sum(p['tumour_AT2_cells'] for p in pairs),'kim_complete_count_intersection':0,'laughney_title_pairs':[p['patient_token'] for p in laugh_pairs],'laughney_normal_specimen_upper_bound':normal_count,'wu_normal_tissue_arms':0,'precision_calculation':{'independent_fixed_model_losses':True,'n':46,'df':45,'standardized_95_t_halfwidth':halfwidth,'scipy_version':scipy.__version__,'interpretation':'pragmatic standardized planning precision, not substantive power or a biological margin'},'external_expression_opened':False,'external_scores_produced':False,'model_fits':0,'main_checkout_writes':False,'source_attribution':'conditional; diagnostic source counts do not adjudicate biological origin'}
    (BASE/'tables/recovery_run.json').write_text(json.dumps(run,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:run[k] for k in ['status','kim_paired_patients','kim_source_candidate_both_50','kim_normal_AT2_50','kim_tumour_AT2_cells','laughney_title_pairs','model_fits']}))

if __name__=='__main__': main()
