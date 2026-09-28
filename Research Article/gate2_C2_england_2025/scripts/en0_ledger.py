"""EN0 continuation: source/identity availability ledger.

Combines the unit map (20 libraries, 68 ENA runs), the intake record, batch1's spatial
identity gate and the preparation run's matrix checks into one ledger that states, for
each identity the plan needs, whether it is available, unknown or absent. It invents no
replicate structure. Deterministic; no data matrices are read here.
"""
from __future__ import annotations
import json, hashlib, sys, datetime
from pathlib import Path
sys.path.insert(0, 'X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages')
import pandas as pd
HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'trials/continuation/prep'
um = pd.read_csv(HERE / 'metadata/analysis_unit_map.csv', keep_default_na=False)
intake = json.loads((HERE / 'metadata/continuation_intake.json').read_text(encoding='utf-8'))
checks = json.loads((OUT / 'matrix_checks.json').read_text(encoding='utf-8'))
spatial = pd.read_csv(HERE / 'trials/batch1/clones/spatial_identity_gate.csv')
qc = pd.read_csv(OUT / 'QC_by_library.csv')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def field_status(col):
    v = um[col].astype(str)
    return {'known': int((~v.isin(['unknown', 'False', 'not recovered from inspected deposits', ''])).sum()), 'total': int(len(v)), 'values': sorted(v.unique().tolist())[:6]}

exp1 = um[um.experiment == 1]
ledger = {
    'stage': 'EN0 continuation ledger', 'written_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'inputs_sha256': {'analysis_unit_map.csv': sha(HERE / 'metadata/analysis_unit_map.csv'), 'continuation_intake.json': sha(HERE / 'metadata/continuation_intake.json'),
                      'matrix_checks.json': sha(OUT / 'matrix_checks.json'), 'spatial_identity_gate.csv': sha(HERE / 'trials/batch1/clones/spatial_identity_gate.csv')},
    'sequencing_records': {'GEO_libraries': int(um.gsm.nunique()), 'ENA_runs': int(um.ena_run_count.astype(int).sum()), 'BioSamples': int(um.biosample.nunique()),
                           'runs_per_library': um.groupby('experiment').ena_run_count.apply(lambda s: sorted(s.astype(int).unique().tolist())).to_dict(),
                           'note': 'runs are sequencing records of the same library, not additional mice'},
    'experiment1_library_accounting': {'deposited_GSMs': int(len(exp1)), 'paper_states': 13, 'resolved': False, 'note': 'no deposit or public record explains the 13-versus-10 difference'},
    'identities': {
        'biological_pool_id': {**field_status('biological_pool_id'), 'status': 'unknown', 'consequence': 'library estimates are descriptive; no biological p values'},
        'reporter_pair_id': {**field_status('reporter_pair_id'), 'status': 'unknown', 'consequence': 'RFP/YFP same-r libraries are not treated as paired mice'},
        'independence_verified': {**field_status('independence_verified'), 'status': 'not verified', 'consequence': 'minimum two lungs pooled per library (paper); pool overlap between libraries unknown'},
        'processing_batch': {**field_status('processing_batch'), 'status': 'unknown'},
        'author_cell_annotation': {'status': 'absent from inspected deposits', 'source': intake['github']['url'], 'tree_sha': intake['github']['tree_sha'],
                                    'consequence': 'EN1 clustering is source-inspired, never an author-label reproduction'},
        'reporter_features_in_matrix': {'status': 'absent' if not checks['reporter_features_present'] else 'present', 'consequence': 'reporter identity is library metadata only; no per-cell reporter call'},
        'spatial_mouse_and_clone_ids': {'status': 'absent', 'datasets': int(len(spatial)), 'mouse_id_available': bool(spatial.mouse_id_available.any()), 'unique_clone_id_available': bool(spatial.unique_clone_id_available.any()),
                                         'consequence': 'joint mouse-level spatial analysis (EN6c) stays unavailable'},
        'mendeley_figure1_pdf': {'status': 'not inspected', 'download': intake['mendeley']['download_status']},
    },
    'matrix_checks': {k: checks[k] for k in ['features_identical_across_libraries', 'genes_total', 'duplicate_symbols', 'nonnegative_integer_counts', 'batch1_cell_set_identical', 'modules_below_coverage_floor']},
    'duplicate_barcodes_within_library_max': max(checks['duplicate_barcodes_within_library'].values()),
    'cells': {'source_QC': int(qc.source_QC_cells.sum()), 'primary_include': int(qc.primary_include.sum()), 'strict_include': int(qc.strict_include.sum()),
              'by_experiment': qc.groupby('experiment')[['source_QC_cells', 'primary_include', 'strict_include']].sum().to_dict(orient='index')},
    'trial_verdicts': {
        'EN1': 'run-ready (source-inspired clustering, per experiment; no six-state target)',
        'EN2': 'run-ready as descriptive library contrasts; within-state estimates only where >=30 cells per library',
        'EN3': 'run-ready; snapshot RNA, no activity or duration inference',
        'EN4': 'limited: 2-week Confetti-YFP is a single baseline library; 4-day arm has no matched baseline',
        'EN5_CD177': 'run-ready where transition-gated groups reach 30 cells on both Cd177 sides; otherwise unavailable',
        'EN6_simulation': 'run-ready from verified archive; EN6c spatial joint analysis blocked (no IDs)',
        'EN7': 'run-ready as descriptive transfer (Choi pooled libraries; Niethamer 25-sample atlas, known days)',
    },
}
(OUT / 'EN0_availability_ledger.json').write_text(json.dumps(ledger, indent=2, default=str) + '\n')
print(json.dumps({k: ledger['identities'][k]['status'] for k in ledger['identities']}, indent=1))
print(ledger['cells'])
