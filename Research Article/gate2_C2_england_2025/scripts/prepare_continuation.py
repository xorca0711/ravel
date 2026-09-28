"""England continuation, shared preparation (EN0 matrix checks + per-cell measurements).

Frozen rules: config/continuation_contract.json and config/continuation_amendments.json (CA3).
Reads the 20 GSE247505 triplets one library at a time, applies source QC, asserts the cell
set equals batch1's, joins batch1 Scrublet flags by barcode (CA3), applies the primary and
strict inclusion rules, calls the three independent gates and the exclusive state rule,
and computes per-cell module scores from counts with the mapped-gene denominator
(log1p CP10k; full-transcriptome totals). Two exact 1,000-UMI thinnings (seeds in contract).
Nothing here inherits batch1 module scores. No statistics, no group contrasts.

Outputs (worktree):
  processed/continuation/matrices/{gsm}_sourceQC.npz + _barcodes.npy   full source-QC CSR (ignored, for EN1)
  processed/continuation/matrices/features.csv                          shared feature table
  processed/continuation/cells/{gsm}_named_counts.npz                   named-gene raw + thinned counts
  processed/continuation/cells_table.csv.gz                             per-cell table (all libraries)
  trials/continuation/prep/QC_by_library.csv, gate_occupancy_by_library.csv,
      module_coverage.csv, matrix_checks.json, run_record.json
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, importlib.util, datetime, platform
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); a = p.parse_args()
os.environ.setdefault('NUMBA_NUM_THREADS', '4'); os.environ.setdefault('OMP_NUM_THREADS', '4')
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
os.environ.setdefault('NUMBA_CACHE_DIR', str(HERE / 'processed/continuation/numba_cache'))
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np
import pandas as pd
import scipy.sparse as sp
import importlib.metadata as im

spec = importlib.util.spec_from_file_location('shared_trial_utils', ROOT / 'Research Article/gate1_04_sikkema_2023_hlca/trials/trial_utils.py')
u = importlib.util.module_from_spec(spec); spec.loader.exec_module(u)

CONTRACT = HERE / 'config/continuation_contract.json'; AMEND = HERE / 'config/continuation_amendments.json'
cfg = json.loads(CONTRACT.read_text(encoding='utf-8'))
OUT = HERE / 'trials/continuation/prep'; PROC = HERE / 'processed/continuation'
MAT = PROC / 'matrices'; CELLS = PROC / 'cells'
for d in (OUT, MAT, CELLS): d.mkdir(parents=True, exist_ok=True)
assert not (OUT / 'run_record.json').exists(), 'Refuse overwrite of completed run'


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''): h.update(b)
    return h.hexdigest()


def git_head(root: Path) -> str:
    """Resolve HEAD by reading ref files (git CLI is unavailable in the sandbox)."""
    g = root / '.git'
    gitdir = Path(g.read_text().split(':', 1)[1].strip()) if g.is_file() else g
    head = (gitdir / 'HEAD').read_text().strip()
    if not head.startswith('ref: '): return head
    ref = head[5:]
    common = gitdir
    cd = gitdir / 'commondir'
    if cd.exists(): common = (gitdir / cd.read_text().strip()).resolve()
    f = common / ref
    if f.exists(): return f.read_text().strip()
    for line in (common / 'packed-refs').read_text().splitlines():
        if line.endswith(' ' + ref): return line.split()[0]
    raise RuntimeError('cannot resolve HEAD')


record = {
    'stage': 'continuation preparation (EN0 matrix checks, per-cell measurements)',
    'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'contract_sha256': digest(CONTRACT), 'amendments_sha256': digest(AMEND), 'script_sha256': digest(Path(__file__)),
    'git_head': git_head(ROOT),
    'interpreter': sys.executable, 'python': platform.python_version(), 'machine': platform.machine(),
    'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy', 'scanpy', 'anndata']},
    'package_paths': {m: os.path.dirname(__import__(m).__file__) for m in ['numpy', 'pandas', 'scipy']},
    'inputs': [], 'seeds': cfg['sensitivities'][2],
    'interpretation': 'descriptive per-cell measurements; biological pool and pairing identities unknown; Cd177 RNA is not surface protein',
}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')

manifest = pd.read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
meta_keys = ['gsm', 'experiment', 'reporter', 'il1r1_status', 'population', 'collection_day', 'reported_replicate_token']
gates = cfg['gates']; modules = cfg['modules']; genes_ind = cfg['individual_genes']
anchors = cfg['epithelial_anchors']; immune = cfg['immune_panel']; nonepi = cfg['non_epithelial_panels']
needed = sorted(set(sum(gates.values(), []) + sum(modules.values(), []) + genes_ind + anchors + immune + sum(nonepi.values(), [])))
gi = {g: i for i, g in enumerate(needed)}
SEEDS = [20260928, 20260929]
THRESH = cfg['Cd177_thresholds_UMI']; GMIN = cfg['gate_min_detected']

qcs, occupancy, coverage, cell_frames = [], [], [], []
checks = {'features_identical_across_libraries': True, 'feature_sha256': None, 'reporter_features_present': None,
          'duplicate_symbols': None, 'duplicate_barcodes_within_library': {}, 'nonnegative_integer_counts': True,
          'batch1_cell_set_identical': {}, 'genes_total': None}
present_genes = None


def gate_calls(C):
    det = C > 0
    return {k: det[:, [gi[g] for g in v]].sum(1) >= GMIN for k, v in gates.items()}


def exclusive_state(g):
    s = np.full(len(g['AT2']), 'unresolved', dtype=object)
    s[g['AT2']] = 'AT2'; s[g['AT1']] = 'AT1'; s[g['transition']] = 'transition'
    s[g['transition'] & g['AT1']] = 'transition_AT1'; s[g['AT2'] & g['AT1']] = 'mixed'
    return s


def scores(C, totals, prefix):
    """Per-cell mean log1p(CP10k) over mapped genes only (contract denominator)."""
    log = np.log1p(C / totals[:, None] * 1e4)
    out = {}
    for k, genes in modules.items():
        valid = [gi[g] for g in genes if g in present_genes]
        out[f'{prefix}{k}'] = log[:, valid].mean(1) if valid else np.full(len(totals), np.nan)
    for g in genes_ind:
        out[f'{prefix}{g}_log1p'] = log[:, gi[g]] if g in present_genes else np.full(len(totals), np.nan)
    return out


for _, row in manifest.iterrows():
    meta = {k: row[k] for k in meta_keys}; gsm = row.gsm
    matrix = a.data_root / row.matrix_path; prefix = matrix.name.removesuffix('_matrix.mtx.gz')
    features = matrix.with_name(prefix + '_features.tsv.gz'); barcodes = matrix.with_name(prefix + '_barcodes.tsv.gz')
    X, var, bc = u.read_mtx_triplet(matrix, features, barcodes)
    import gzip as _gz
    fsha = hashlib.sha256(_gz.open(features, 'rb').read()).hexdigest()  # decompressed content; gz headers differ per file
    if checks['feature_sha256'] is None:
        checks['feature_sha256'] = fsha; checks['genes_total'] = int(len(var))
        symbols_all = var.gene_symbol.astype(str).to_numpy()
        checks['duplicate_symbols'] = int(pd.Series(symbols_all).duplicated().sum())
        reporter_tokens = {'yfp', 'eyfp', 'rfp', 'gfp', 'egfp', 'tdtomato', 'tdtom', 'mcherry', 'confetti', 'cre', 'creert2', 'brainbow'}
        rep = [s for s in symbols_all if s.lower() in reporter_tokens or s.lower().startswith(('tdtomato', 'confetti', 'brainbow'))]
        checks['reporter_features_present'] = bool(rep); checks['reporter_like_symbols'] = rep
        var.to_csv(MAT / 'features.csv', index=False)
    elif fsha != checks['feature_sha256']:
        checks['features_identical_across_libraries'] = False
    if not (np.all(X.data >= 0) and np.all(X.data == np.floor(X.data))): checks['nonnegative_integer_counts'] = False
    checks['duplicate_barcodes_within_library'][gsm] = int(pd.Series(bc).duplicated().sum())
    symbols = var.gene_symbol.astype(str).to_numpy().astype(str); present_genes = set(symbols.tolist())
    totals = np.asarray(X.sum(1)).ravel(); ng = X.getnnz(1)
    mt = np.char.startswith(symbols, 'mt-'); mt_pct = np.asarray(X[:, mt].sum(1)).ravel() / np.maximum(totals, 1) * 100
    keep = (ng >= 1000) & (totals <= 50000) & (mt_pct <= 15)
    before = X.shape[0]; X = X[keep].tocsr(); totals = totals[keep]; ng = ng[keep]; mt_pct = mt_pct[keep]; bc = bc[keep]
    X.data = X.data.astype(np.int32); X.indices = X.indices.astype(np.int32)
    n = len(totals)
    # CA3: batch1 cell set identity and doublet flags joined by barcode
    b1 = pd.read_csv(HERE / f'processed/batch1/rna/{gsm}_QC_cells.csv.gz')
    same = (len(b1) == n) and (set(b1.barcode) == set(bc))
    checks['batch1_cell_set_identical'][gsm] = bool(same)
    assert same, f'{gsm}: source-QC cell set differs from batch1; CA3 join refused'
    b1 = b1.set_index('barcode').loc[bc]
    doublet = b1.doublet_flag.to_numpy().astype(bool); dscore = b1.doublet_score.to_numpy()
    # full matrix for EN1 (ignored cache)
    sp.save_npz(MAT / f'{gsm}_sourceQC.npz', X, compressed=True); np.save(MAT / f'{gsm}_barcodes.npy', bc.astype(str))
    # named-gene counts, aggregating duplicated symbols
    rr, cc = [], []
    for j, g in enumerate(symbols):
        if g in gi: rr.append(j); cc.append(gi[g])
    agg = sp.csr_matrix((np.ones(len(rr), dtype=np.int64), (rr, cc)), shape=(len(symbols), len(needed)))
    C = np.asarray((X @ agg).todense()).astype(np.int64)
    det = C > 0
    n_anchor = det[:, [gi[g] for g in anchors]].sum(1); n_imm = det[:, [gi[g] for g in immune]].sum(1)
    nonepi_hit = np.zeros(n, bool)
    for genes in nonepi.values(): nonepi_hit |= det[:, [gi[g] for g in genes]].sum(1) >= 2
    immune_low_anchor = (n_imm >= 2) & (n_anchor < 2)
    primary = ~doublet & ~immune_low_anchor
    strict = primary & ~(n_imm >= 2) & ~(nonepi_hit & (n_anchor < 2))
    g = gate_calls(C); state = exclusive_state(g)
    tab = pd.DataFrame({**{k: [v] * n for k, v in meta.items()}, 'barcode': bc, 'n_genes': ng, 'total_umis': totals, 'mito_percent': mt_pct,
                        'doublet_score': dscore, 'doublet_flag': doublet, 'n_epithelial_anchors': n_anchor, 'n_immune_markers': n_imm,
                        'nonepithelial_panel_hit': nonepi_hit, 'primary_include': primary, 'strict_include': strict,
                        'gate_AT2': g['AT2'], 'gate_transition': g['transition'], 'gate_AT1': g['AT1'], 'state': state,
                        'Cd177_umi': C[:, gi['Cd177']], 'Itga2_umi': C[:, gi['Itga2']], 'Mki67_umi': C[:, gi['Mki67']],
                        'cycling_markers_detected': det[:, [gi[x] for x in modules['cycling']]].sum(1)})
    tab = tab.assign(**scores(C, totals.astype(np.float64), 'raw_'))
    # exact 1,000-UMI thinning of the full row, then named-gene extraction
    map_sel = np.array([gi.get(s, -1) for s in symbols], dtype=int)
    thinned = {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed); D = np.zeros_like(C)
        for i in range(n):
            s0, s1 = X.indptr[i:i + 2]; vals = X.data[s0:s1].astype(np.int64); ix = X.indices[s0:s1]
            draw = rng.multivariate_hypergeometric(vals, 1000)
            sel = map_sel[ix]; ok = sel >= 0
            np.add.at(D[i], sel[ok], draw[ok])
        thinned[seed] = D
        gd = gate_calls(D)
        tab[f'd{seed}_gate_AT2'] = gd['AT2']; tab[f'd{seed}_gate_transition'] = gd['transition']; tab[f'd{seed}_gate_AT1'] = gd['AT1']
        tab[f'd{seed}_state'] = exclusive_state(gd); tab[f'd{seed}_Cd177_umi'] = D[:, gi['Cd177']]; tab[f'd{seed}_Itga2_umi'] = D[:, gi['Itga2']]
        tab[f'd{seed}_cycling_markers_detected'] = (D[:, [gi[x] for x in modules['cycling']]] > 0).sum(1)
        tab = tab.assign(**scores(D, np.full(n, 1000.0), f'd{seed}_'))
    np.savez_compressed(CELLS / f'{gsm}_named_counts.npz', counts=C, totals=totals, genes=np.array(needed), barcodes=bc.astype(str),
                        **{f'thinned_{s}': thinned[s] for s in SEEDS})
    cell_frames.append(tab)
    qcs.append({**meta, 'input_barcodes': before, 'source_QC_cells': n, 'median_genes': float(np.median(ng)), 'median_umis': float(np.median(totals)),
                'median_mito_percent': float(np.median(mt_pct)), 'batch1_doublets_joined': int(doublet.sum()), 'immune_low_anchor_excluded': int(immune_low_anchor.sum()),
                'primary_include': int(primary.sum()), 'strict_include': int(strict.sum()), 'source_gate_exact': 'genes>=1000;UMI<=50000;mito<=15%'})
    for variant, mask in [('all_sourceQC', np.ones(n, bool)), ('primary', primary), ('strict', strict)]:
        for gate_name, gm in [('AT2', g['AT2']), ('transition', g['transition']), ('AT1', g['AT1'])] + [(f'state_{s}', state == s) for s in ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed', 'unresolved']]:
            occupancy.append({**meta, 'variant': variant, 'group': gate_name, 'n_cells': int((gm & mask).sum()), 'denominator': int(mask.sum())})
        for t in THRESH:
            occupancy.append({**meta, 'variant': variant, 'group': f'transition_Cd177_ge{t}', 'n_cells': int((g['transition'] & mask & (C[:, gi['Cd177']] >= t)).sum()), 'denominator': int((g['transition'] & mask).sum())})
    for k, genes in modules.items():
        coverage.append({'gsm': gsm, 'module': k, 'genes': len(genes), 'mapped': len(set(genes) & present_genes), 'fraction': len(set(genes) & present_genes) / len(genes)})
    for f in [matrix, features, barcodes]:
        record['inputs'].append({'path': str(f.relative_to(a.data_root)).replace('\\', '/'), 'bytes': f.stat().st_size, 'sha256': digest(f)})
    record['inputs'].append({'path': f'processed/batch1/rna/{gsm}_QC_cells.csv.gz', 'sha256': digest(HERE / f'processed/batch1/rna/{gsm}_QC_cells.csv.gz'), 'role': 'CA3 doublet flags'})
    print(f'{gsm}: {before} -> {n} source-QC; primary {int(primary.sum())}; strict {int(strict.sum())}; transition {int(g["transition"].sum())}; Cd177>=1 in transition {int((g["transition"] & (C[:, gi["Cd177"]] >= 1)).sum())}', flush=True)
    del X, C, thinned

cells = pd.concat(cell_frames, ignore_index=True)
cells.to_csv(PROC / 'cells_table.csv.gz', index=False)
pd.DataFrame(qcs).to_csv(OUT / 'QC_by_library.csv', index=False)
pd.DataFrame(occupancy).to_csv(OUT / 'gate_occupancy_by_library.csv', index=False)
cov = pd.DataFrame(coverage); cov.to_csv(OUT / 'module_coverage.csv', index=False)
checks['modules_below_coverage_floor'] = sorted(cov[cov.fraction < cfg['coverage_floor']].module.unique().tolist())
checks['cells_table_rows'] = int(len(cells)); checks['cells_table_sha256'] = digest(PROC / 'cells_table.csv.gz')
(OUT / 'matrix_checks.json').write_text(json.dumps(checks, indent=2) + '\n')
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), libraries=len(qcs), source_QC_cells=int(cells.shape[0]),
              primary_include=int(cells.primary_include.sum()), strict_include=int(cells.strict_include.sum()),
              outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv')) + [OUT / 'matrix_checks.json']],
              ignored_outputs={'cells_table.csv.gz': checks['cells_table_sha256'], 'matrices': len(list(MAT.glob('*_sourceQC.npz'))), 'named_counts': len(list(CELLS.glob('*.npz')))})
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n')
print('preparation completed', record['source_QC_cells'], record['primary_include'], record['strict_include'], flush=True)
