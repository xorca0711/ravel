"""Bounded A12 independent-source qualification; no prediction or expression use."""
import argparse,json,csv,collections
from pathlib import Path

def main(out):
    out.mkdir(exist_ok=True);src=Path('raw_data/cut_fill_20261103')
    rows=list(csv.DictReader((src/'E-MTAB-13526.sdrf.txt').open(),delimiter='\t'))
    fields=['Source Name','Characteristics[individual]','Characteristics[disease]','Characteristics[FACS]','Characteristics[sampling site]']
    samples={}
    for r in rows:
        v={k:r[k] for k in fields};name=v['Source Name']
        assert name not in samples or samples[name]==v;samples[name]=v
    with (out/'de_zuani_samples.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(samples.values())
    units=collections.defaultdict(list)
    for r in samples.values():units[r['Characteristics[individual]']].append(r)
    luad={k:v for k,v in units.items() if {r['Characteristics[disease]'] for r in v}=={'lung adenocarcinoma'}}
    eligible=[]
    for patient,ss in luad.items():
        sites={r['Characteristics[sampling site]'] for r in ss if r['Characteristics[FACS]']=='CD235a-'}
        if {'tumor','normal tissue adjacent to tumor'}<=sites:eligible.append(patient)
    attempts={f.name:json.loads(f.read_text()) for f in sorted((src/'a12_remote_obs').glob('*json'))}
    assert len(luad)==12 and len(eligible)==5
    assert all('metadata_file' not in v for k,v in attempts.items() if k.endswith('obs_acquisition.json'))
    result={'candidate':'E-MTAB-13526','sample_records':len(samples),'deposited_patients':len([x for x in units if x.startswith('Patient ')]),'deposited_luad_patients':len(luad),'luad_patients_with_paired_CD235a_depleted_libraries':eligible,'paired_CD235a_depleted_patient_count':len(eligible),'all_unit_ids':sorted(units),'source_discrepancy':'IDF says 24 patients and SDRF has 24; publication describes25 (13LUAD), while deposited SDRF identifies12LUAD. No missing patient identity invented.','gate':'HOLD: only5 LUAD patients have intended nonimmune-inclusive libraries in both arms; AT2 coverage in immune-enriched libraries is unverified, not assumed zero. Required author-state/count/patient join and >=10 eligible pairs not established. Annotation object headers accessible by HTTP206; row metadata requests timed out.','other_candidates':[{'source':'GSE304587','verdict':'Reject for unchanged minimum-unit gate: primary GEO design has two patients, no qualified10 paired units.'},{'source':'Han et al Nature2024 DOI10.1038/s41586-024-07113-9','verdict':'Not qualified for joint source-recipient replication: epithelial-enriched primary cohort lacks a qualified paired macrophage source export; methods and abstract inspected, no matrices.'}],'prediction_executed':False,'limits':'No claim that no eligible cohort exists elsewhere. Preserve Kim/Laughney/Wu failures and closed GSE308103 pilot. Fixed-procedure replication selected; no serialized pilot fitting, index/alpha/endpoint/state retuning.'}
    (out/'qualification.json').write_text(json.dumps(result,indent=2))
    (out/'access_attempts.json').write_text(json.dumps(attempts,indent=2))
    (out/'verification.json').write_text(json.dumps({'passed':True,'technical_FASTQ_rows_deduplicated_by_source_name':True,'conflicting_source_records':0,'state_counts_not_inferred_from_sample_names':True,'full_expression_values_unopened':True},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);main(ap.parse_args().output)
