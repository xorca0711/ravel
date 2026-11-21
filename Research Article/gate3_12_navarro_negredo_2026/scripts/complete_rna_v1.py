"""Preserve supplied provenance and assemble completion facts from verified outputs."""
import argparse,csv,hashlib,json,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
b=Path('Research Article/ungated_navarro_negredo_2026_aged_brain_il10')
r=Path('analysis/research/runs');d=r/'nn26_pooled_rna_description_v1'
archive=out/'source_context';archive.mkdir()
manifest=[]
for source in sorted((b/'source_context').glob('*.json')):
    target=archive/source.name;shutil.copyfile(source,target)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
    manifest.append({'restore_path':str(source),'archive_path':str(target),'sha256':sha,'bytes':source.stat().st_size})
assert len(manifest)==3
(out/'source_archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
verification=json.loads((d/'independent_verification.json').read_text());assert verification['all_checks_passed']
rows=list(csv.DictReader((d/'summaries.tsv').open(),delimiter='\t'))
# Illustrative rows copied without calculating another endpoint; full marker tables remain authoritative.
examples=[x for x in rows if x['scope']!='Microglia' or x['gene'] in ['Stat3','Socs3','Tnf','Cd86','Stat1','Bst2','Isg15','Ifitm3']]
stages=[
 {'step':1,'status':'qualified_with_source_holds','detail':'Earlier source evidence immutable; eight object aliases versus six published libraries unresolved.'},
 {'step':2,'status':'completed_for_executed_stages','detail':'Frozen registered stage contracts, committed code and verified runner receipts; exposure retained.'},
 {'step':3,'status':'previous_desktop_execution_retained','detail':'Animal results imported; not rerun or promoted; original receipts/plots remain on parent branch.'},
 {'step':4,'status':'completed_with_specific_holds','detail':'Sparse RNA normalization, alignment, QC and recovery qualify; no proven donor assignment, extra aliases unmapped.'},
 {'step':5,'status':'completed_bounded_description','detail':'Six eligible aliases, broad microglia and T cells; exact marker vectors, no hallmark score or population inference.'},
 {'step':6,'status':'not_eligible_for_new_acquisition','detail':'No defined unresolved comparison justifies optional objects; optional source conflicts remain and cannot supply D25K replication.'},
 {'step':7,'status':'completed_with_scientific_limits','detail':'RNA, protein, neural markers and behavior remain distinct; new experimental units/design needed for population effects, aging interaction, repair or mediation.'}]
summary={'candidate':'Nn26-P01','integration_base':'471d0c2f8b3b5fef287aea5173325436901fceac',
 'description_freeze_commit':json.loads((d/'receipt.json').read_text())['git_commit'],
 'rds':{'size_bytes':2188161276,'md5':'ce9bf02e41665e00e11cd1b262114506','sha256':'b1fa0ce7c6ff19e5d207caff9548e5ec2dacd5a3cdb4fa0fc01b5874a15d2559'},
 'verification':verification,'scientific_holds':json.loads((d/'scientific_holds.json').read_text()),
 'stages':stages,'illustrative_existing_rows':examples,
 'full_summary_path':str(d/'summaries.tsv'),'full_contrast_path':str(d/'contrasts.tsv'),
 'metadata_qc_names':{'nCount_matches':'maximum absolute discrepancy; zero means exact agreement','nFeature_matches':'maximum absolute discrepancy; zero means exact agreement','threshold_fields':'counts of violations; all zero'},
 'metadata_warnings':'192 identical simpleWarnings: row names were found from a short variable and have been discarded; explicit sample identities and numerical outputs preserved byte-for-byte.',
 'failed_v1_preserved':str(r/'nn26_failure_preservation_v1/failed_v1/receipt.json'),
 'scientific_acceptance':'not_assessed'}
(out/'completion_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
