"""Audit A16 readiness using hashes and file inventories only; never calculate outcomes."""
import argparse, hashlib, json
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE.parents[2]
PAPER=Path('Research Article/gate2_C2_england_2025')
LIBRARIES=['GSM7890835','GSM7890836']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(8<<20),b''): h.update(block)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-root',type=Path,required=True); ap.add_argument('--cache-root',type=Path); args=ap.parse_args()
    prep_path=ROOT/PAPER/'trials/continuation/prep/run_record.json'; prep=json.loads(prep_path.read_text())
    cache_root=args.cache_root or args.data_root/PAPER
    rows=[]
    for record in prep['inputs']:
        if not any(gsm in record['path'] for gsm in LIBRARIES): continue
        p=(args.data_root/record['path']) if record['path'].startswith('raw_data/') else (cache_root/record['path'])
        exists=p.is_file(); actual=sha(p) if exists else None
        rows.append({'path':str(p),'role':'raw_count_provenance' if record['path'].startswith('raw_data/') else 'original_doublet_flags','exists':exists,'expected_sha256':record['sha256'],'actual_sha256':actual,'matches':actual==record['sha256'] if exists else None,'bytes':p.stat().st_size if exists else None})
    cell_path=cache_root/'processed/continuation/cells_table.csv.gz'; cell_hash=prep['ignored_outputs']['cells_table.csv.gz']
    cell_exists=cell_path.is_file(); actual=sha(cell_path) if cell_exists else None
    rows.append({'path':str(cell_path),'role':'original_cells_table_inclusion_and_gates','exists':cell_exists,'expected_sha256':cell_hash,'actual_sha256':actual,'matches':actual==cell_hash if cell_exists else None,'bytes':cell_path.stat().st_size if cell_exists else None})
    for gsm in LIBRARIES:
        for suffix in ['_sourceQC.npz','_barcodes.npy']:
            p=cache_root/'processed/continuation/matrices'/f'{gsm}{suffix}'
            rows.append({'path':str(p),'role':'recoverable_cache_not_required_if_original_cells_table_verified','exists':p.is_file(),'expected_sha256':None,'actual_sha256':sha(p) if p.is_file() else None,'matches':None,'bytes':p.stat().st_size if p.is_file() else None})
    raw=[r for r in rows if r['role']=='raw_count_provenance']; flags=[r for r in rows if r['role']=='original_doublet_flags']
    raw_verified=len(raw)==6 and all(r['matches'] for r in raw)
    cells_verified=cell_exists and actual==cell_hash
    flags_verified=len(flags)==2 and all(r['matches'] for r in flags)
    status='ready_for_specification_review' if raw_verified and (cells_verified or flags_verified) else 'blocked_original_fixed_population_unavailable'
    record={'status':status,'checked_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':sha(Path(__file__)),'data_root':str(args.data_root),'cache_root':str(cache_root),'libraries':LIBRARIES,'raw_files_verified':sum(bool(r['matches']) for r in raw),'original_cells_table_verified':bool(cells_verified),'original_doublet_flags_verified':bool(flags_verified),'historical_prep_record':str(prep_path),'historical_prep_sha256':sha(prep_path),'inputs':rows,'outcomes_opened':False,'matrix_values_parsed':False,'counts_hashed_only':True,'readiness_rule':'Need six raw files plus original hash-verified cell table or both original hash-verified batch1 QC flags; raw triplets alone do not preserve primary_include.','blocker':None if status.startswith('ready_') else 'Original per-cell primary_include requires historical doublet flags. No source cache or original QC flag files found at the specified cache root. Re-estimating flags would change the frozen population.','next_action':'Recover the original byte-identified cell table or both QC files. Restore read-only cache access; do not regenerate doublet flags or replace inclusion.'}
    (BASE/'tables/readiness.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:record[k] for k in ['status','raw_files_verified','original_cells_table_verified','original_doublet_flags_verified','outcomes_opened']}))
if __name__=='__main__': main()
