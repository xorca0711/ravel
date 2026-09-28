"""A16 Stage 1, analyses C3 and C4: the two analyses that can close the question.

C3 detection-matched gene null  - is the surviving priming association specific to Cd177, or generic
                                  behaviour of any gene with its detection profile?
C4 ambient neutrophil control   - Cd177 is a neutrophil surface protein and the priming module is
                                  inflammation-associated, so ambient RNA would manufacture the
                                  residual with no cell state behind it.

Frozen rules: config/a16_question_contract.json. Population correction: reports/STAGE1_ERRATUM.md,
which is why two arms are run - Arm A the transitional gate per library (the contract's declared
population, the marginal EN5 effect) and Arm B FU_C's own population (the residual under test).

Exposure is FULL: the founding FU_C result was seen before the contract was written and this reuses
the same processed matrices. Nothing here may conclude cell-intrinsic function.

Outputs under tables/stage1/.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--data-root', type=Path, required=True)
ap.add_argument('--n-control-genes', type=int, default=500)
args = ap.parse_args()

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
ENG = ROOT / 'Research Article/gate2_C2_england_2025'
PROC = ENG / 'processed/continuation'
FUP = ENG / 'processed/followup'
OUT = HERE / 'tables/stage1'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(args.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, scipy.sparse as sp
import importlib.metadata as im

SEED = 20260928
PRIMARY = 'priming_associated'
EPS = ['priming_associated', 'AT2_identity', 'AT1_identity', 'Itga2', 'cycling', 'transition_RNA',
       'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint']
DET_TOL, EXP_TOL = 0.25, 0.35          # relative bands for detection rate and mean expression
NEUTRO = ['Ptprc', 'Tyrobp', 'Lst1', 'Fcer1g', 'Ly6g', 'S100a8', 'S100a9', 'Retnlg']


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()


cfgA = json.loads((HERE / 'config/a16_question_contract.json').read_text(encoding='utf-8'))
cfgE = json.loads((ENG / 'config/continuation_contract.json').read_text(encoding='utf-8'))
modules, gates = cfgE['modules'], cfgE['gates']
MIN = cfgE['min_group_cells']

record = {'stage': 'A16 Stage 1 C3+C4', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'a16_contract_sha256': digest(HERE / 'config/a16_question_contract.json'),
          'england_continuation_contract_sha256': digest(ENG / 'config/continuation_contract.json'),
          'erratum_sha256': digest(HERE / 'reports/STAGE1_ERRATUM.md'),
          'script_sha256': digest(Path(__file__)), 'seed': SEED,
          'interpreter': sys.executable, 'python': platform.python_version(),
          'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy']},
          'exposure': cfgA['exposure'], 'n_control_genes_cap': args.n_control_genes,
          'matching_bands': {'detection_rate_relative': DET_TOL, 'mean_log1p_cp10k_relative': EXP_TOL},
          'floor_cells_per_side': MIN, 'primary_endpoint': PRIMARY, 'inputs': []}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')


def add_input(rel: str, path: Path) -> None:
    record['inputs'].append({'path': rel, 'sha256': digest(path)})


cells = pd.read_csv(PROC / 'cells_table.csv.gz', low_memory=False)
add_input('processed/continuation/cells_table.csv.gz', PROC / 'cells_table.csv.gz')
features = pd.read_csv(PROC / 'matrices/features.csv', keep_default_na=False)
add_input('processed/continuation/matrices/features.csv', PROC / 'matrices/features.csv')
symbols = features.gene_symbol.astype(str).to_numpy().astype(str)
gidx = {g: i for i, g in enumerate(symbols)}
assert 'Cd177' in gidx, 'Cd177 absent from the feature table'

r2 = {}
for exp in (1, 2):
    f = FUP / f'experiment{exp}_round2.csv.gz'
    r2[exp] = pd.read_csv(f)
    add_input(f'processed/followup/experiment{exp}_round2.csv.gz', f)

# Genes that may not serve as controls: any member of a frozen gate, module, or the neutrophil panel.
banned = set(NEUTRO) | {'Cd177'}
for d in (gates, modules):
    for v in d.values():
        banned |= set(v)
record['n_banned_control_genes'] = len(banned)

# ---- assemble the cell set both arms need, one library at a time ----
armA_libs = ['GSM7890835', 'GSM7890836']
fuc_units = [(1, 10), (1, 12), (1, 16), (1, 17), (1, 18), (2, 10), (2, 12)]   # FU_C's testable subclusters

need = []
for gsm in armA_libs:
    c = cells[(cells.gsm == gsm) & cells.primary_include & cells.gate_transition]
    need.append(pd.DataFrame({'gsm': gsm, 'barcode': c.barcode}))
for exp, cl in fuc_units:
    lab = r2[exp][r2[exp]['sub_r1.0'] == cl][['gsm', 'barcode']]
    need.append(lab)
need = pd.concat(need, ignore_index=True).drop_duplicates()
print(f'cells needed across both arms: {len(need)}', flush=True)

blocks, rows_meta = [], []
for gsm, want in need.groupby('gsm'):
    mpath = PROC / f'matrices/{gsm}_sourceQC.npz'
    bpath = PROC / f'matrices/{gsm}_barcodes.npy'
    X = sp.load_npz(mpath).tocsr()
    bc = np.load(bpath, allow_pickle=False).astype(str)
    sel = pd.Index(bc).get_indexer(want.barcode.to_numpy())
    assert (sel >= 0).all(), f'{gsm}: barcodes missing from the source matrix'
    blocks.append(X[sel])
    rows_meta.append(pd.DataFrame({'gsm': gsm, 'barcode': want.barcode.to_numpy()}))
    del X
M = sp.vstack(blocks, format='csr')
meta = pd.concat(rows_meta, ignore_index=True)
del blocks, rows_meta
print(f'matrix assembled: {M.shape[0]} cells x {M.shape[1]} genes, {M.nnz} nonzeros', flush=True)

meta = meta.merge(cells, on=['gsm', 'barcode'], how='left', validate='one_to_one')
assert meta.total_umis.notna().all()
row_of = {(g, b): i for i, (g, b) in enumerate(zip(meta.gsm, meta.barcode))}

# log1p(CP10k) with the same convention as every other England score, applied to the sparse data only
L = M.copy().astype(np.float64)
inv = (1e4 / meta.total_umis.to_numpy(float))
L = sp.diags(inv) @ L
L.data = np.log1p(L.data)
L = L.tocsc()
B = (M > 0).astype(np.float64).tocsc()
del M

neutro_cols = [gidx[g] for g in NEUTRO if g in gidx]
record['neutrophil_panel_mapped'] = [g for g in NEUTRO if g in gidx]
meta['neutro_score'] = np.asarray(L[:, neutro_cols].mean(axis=1)).ravel()
meta['cd177_umi_here'] = np.asarray(B[:, [gidx['Cd177']]].todense()).ravel()


def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 2 or len(y) < 2:
        return np.nan
    sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2))
    return float((x.mean() - y.mean()) / sd) if sd > 0 else np.nan


def col_of(ep):
    return f'raw_{ep}' if ep in modules else f'raw_{ep}_log1p'


def vec_smd(Bsub, y):
    """SMD of y between gene-positive and gene-negative cells, for every column of Bsub at once."""
    n = Bsub.shape[0]
    n1 = np.asarray(Bsub.sum(axis=0)).ravel()
    n0 = n - n1
    s1 = np.asarray(Bsub.T @ y).ravel()
    q1 = np.asarray(Bsub.T @ (y * y)).ravel()
    st, qt = y.sum(), (y * y).sum()
    s0, q0 = st - s1, qt - q1
    with np.errstate(divide='ignore', invalid='ignore'):
        m1, m0 = s1 / n1, s0 / n0
        v1 = (q1 - n1 * m1 ** 2) / (n1 - 1)
        v0 = (q0 - n0 * m0 ** 2) / (n0 - 1)
        sd = np.sqrt(((n1 - 1) * v1 + (n0 - 1) * v0) / (n1 + n0 - 2))
        out = (m1 - m0) / sd
    bad = (n1 < MIN) | (n0 < MIN) | ~np.isfinite(sd) | (sd <= 0)
    out = np.where(bad, np.nan, out)
    return out, n1, n0


units = []
for gsm in armA_libs:
    idx = np.array([row_of[(gsm, b)] for b in cells[(cells.gsm == gsm) & cells.primary_include & cells.gate_transition].barcode])
    units.append({'arm': 'A_marginal_transitional_gate', 'unit': gsm, 'experiment': 1,
                  'population': 'transitional gate, primary_include, single library', 'rows': idx})
for exp, cl in fuc_units:
    lab = r2[exp][r2[exp]['sub_r1.0'] == cl]
    idx = np.array([row_of[(g, b)] for g, b in zip(lab.gsm, lab.barcode)])
    keep = meta.primary_include.to_numpy()[idx]
    units.append({'arm': 'B_within_subcluster_FU_C', 'unit': f'exp{exp}_sub_r1.0={cl}', 'experiment': exp,
                  'population': 'all primary_include cells in the subcluster, libraries pooled within experiment',
                  'rows': idx[keep]})

c3_summary, c3_detail, c4_rows = [], [], []
rng = np.random.default_rng(SEED)

for u in units:
    idx = u['rows']
    sub = meta.iloc[idx]
    Bs, Ls = B[idx], L[idx]
    n = len(idx)
    cd_pos = sub.cd177_umi_here.to_numpy() >= 1
    base = {'arm': u['arm'], 'unit': u['unit'], 'experiment': u['experiment'], 'population': u['population'],
            'n_cells': n, 'n_cd177_pos': int(cd_pos.sum()), 'n_cd177_neg': int((~cd_pos).sum()),
            'n_libraries_pooled': int(sub.gsm.nunique()),
            'library_composition': ';'.join(f'{k}:{v}' for k, v in sub.gsm.value_counts().items())}

    # ---------- C3: detection-matched gene null ----------
    det = np.asarray(Bs.sum(axis=0)).ravel() / n
    mexp = np.asarray(Ls.mean(axis=0)).ravel()
    d0, e0 = det[gidx['Cd177']], mexp[gidx['Cd177']]
    cand = np.where((np.abs(det - d0) <= DET_TOL * d0) & (np.abs(mexp - e0) <= EXP_TOL * max(e0, 1e-12)))[0]
    cand = np.array([j for j in cand if symbols[j] not in banned])
    n_cand = len(cand)
    if n_cand > args.n_control_genes:
        cand = np.sort(rng.choice(cand, args.n_control_genes, replace=False))
    meta_c3 = {**base, 'cd177_detection_rate': float(d0), 'cd177_mean_log1p_cp10k': float(e0),
               'n_candidate_genes_in_band': int(n_cand), 'n_control_genes_used': int(len(cand))}

    if base['n_cd177_pos'] < MIN or base['n_cd177_neg'] < MIN:
        c3_summary.append({**meta_c3, 'status': f'not assessed: fewer than {MIN} cells on a side'})
        c4_rows.append({**base, 'status': f'not assessed: fewer than {MIN} cells on a side'})
        continue
    if len(cand) < 20:
        c3_summary.append({**meta_c3, 'status': f'not assessed: only {len(cand)} matched control genes'})

    Bc = Bs[:, cand]
    for ep in EPS:
        y = sub[col_of(ep)].to_numpy(float)
        null, n1, n0 = vec_smd(Bc, y)
        obs = smd(y[cd_pos], y[~cd_pos])
        ok = np.isfinite(null)
        row = {**meta_c3, 'endpoint': ep, 'cd177_smd': obs, 'n_control_genes_estimable': int(ok.sum()),
               'null_median': float(np.median(null[ok])) if ok.any() else np.nan,
               'null_p05': float(np.quantile(null[ok], 0.05)) if ok.any() else np.nan,
               'null_p95': float(np.quantile(null[ok], 0.95)) if ok.any() else np.nan,
               'null_max': float(null[ok].max()) if ok.any() else np.nan,
               'frac_control_ge_cd177': float((null[ok] >= obs).mean()) if ok.any() else np.nan,
               'cd177_quantile_in_null': float((null[ok] < obs).mean()) if ok.any() else np.nan,
               'status': 'estimated' if len(cand) >= 20 else 'estimated_underpowered_null'}
        c3_summary.append(row)
        if ep == PRIMARY:
            for j, g in enumerate(cand):
                c3_detail.append({'arm': u['arm'], 'unit': u['unit'], 'gene': symbols[g],
                                  'detection_rate': float(det[g]), 'mean_log1p_cp10k': float(mexp[g]),
                                  'n_pos': int(n1[j]), 'n_neg': int(n0[j]), 'smd_priming': float(null[j])})

    # ---------- C4: ambient neutrophil-origin control ----------
    ns = sub.neutro_score.to_numpy(float)
    y = sub[col_of(PRIMARY)].to_numpy(float)
    r_ns = pd.Series(ns).rank().to_numpy()
    r_cd = pd.Series(sub.cd177_umi_here.to_numpy(float)).rank().to_numpy()
    spear = float(np.corrcoef(r_ns, r_cd)[0, 1])
    r_y = pd.Series(y).rank().to_numpy()
    c4 = {**base, 'status': 'estimated',
          'smd_priming_unadjusted': smd(y[cd_pos], y[~cd_pos]),
          'smd_neutro_score_cd177_pos_vs_neg': smd(ns[cd_pos], ns[~cd_pos]),
          'spearman_cd177_umi_vs_neutro': spear,
          'spearman_priming_vs_neutro': float(np.corrcoef(r_y, r_ns)[0, 1])}
    Xd = np.column_stack([np.ones(n), ns])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    res = y - Xd @ beta
    c4['smd_priming_residual_on_neutro'] = smd(res[cd_pos], res[~cd_pos])
    Xd2 = np.column_stack([np.ones(n), ns, np.log10(sub.total_umis.to_numpy(float)), sub.n_genes.to_numpy(float)])
    beta2, *_ = np.linalg.lstsq(Xd2, y, rcond=None)
    res2 = y - Xd2 @ beta2
    c4['smd_priming_residual_on_neutro_and_depth'] = smd(res2[cd_pos], res2[~cd_pos])
    q = pd.qcut(pd.Series(ns).rank(method='first'), 4, labels=False).to_numpy()
    num = den = 0.0
    used = npos = nneg = 0
    for k in range(4):
        s_ = q == k
        a_, b_ = y[s_ & cd_pos], y[s_ & ~cd_pos]
        if len(a_) < MIN or len(b_) < MIN:
            continue
        e = smd(a_, b_)
        if not np.isfinite(e):
            continue
        w = min(len(a_), len(b_))
        num += w * e
        den += w
        used += 1
        npos += len(a_)
        nneg += len(b_)
    c4['smd_priming_neutro_quartile_stratified'] = float(num / den) if den > 0 else np.nan
    c4['neutro_strata_used'] = used
    c4['n_pos_stratified'] = npos
    c4['n_neg_stratified'] = nneg
    c4['retained_fraction_after_neutro'] = (float(c4['smd_priming_residual_on_neutro'] / c4['smd_priming_unadjusted'])
                                            if c4['smd_priming_unadjusted'] not in (0, None) and np.isfinite(c4['smd_priming_unadjusted']) and c4['smd_priming_unadjusted'] != 0 else np.nan)
    c4_rows.append(c4)
    print(f"{u['arm']:<30s} {u['unit']:<20s} n={n:<5d} pos={base['n_cd177_pos']:<4d} "
          f"priming={c4['smd_priming_unadjusted']:+.3f} -> neutro-adj {c4['smd_priming_residual_on_neutro']:+.3f} "
          f"| controls={len(cand)}", flush=True)

pd.DataFrame(c3_summary).to_csv(OUT / 'A16_C3_matched_gene_null.csv', index=False)
pd.DataFrame(c3_detail).to_csv(OUT / 'A16_C3_control_gene_detail.csv', index=False)
pd.DataFrame(c4_rows).to_csv(OUT / 'A16_C4_ambient_neutrophil_control.csv', index=False)
record['completed_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
record['outputs'] = {f: digest(OUT / f) for f in ['A16_C3_matched_gene_null.csv', 'A16_C3_control_gene_detail.csv', 'A16_C4_ambient_neutrophil_control.csv']}
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n')
print('\n--- C3 primary endpoint ---', flush=True)
s = pd.DataFrame(c3_summary)
s = s[(s.endpoint == PRIMARY) if 'endpoint' in s else slice(None)]
print(s[['arm', 'unit', 'n_cd177_pos', 'cd177_smd', 'null_median', 'null_p95', 'frac_control_ge_cd177', 'n_control_genes_used']].round(3).to_string(index=False), flush=True)
