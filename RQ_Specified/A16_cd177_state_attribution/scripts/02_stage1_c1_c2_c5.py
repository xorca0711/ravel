"""A16 Stage 1, analyses C1, C2 and C5, run after C3 and C4 left the residual partly standing.

C1 continuous neighbourhood matching - condition on position itself instead of on cluster boundaries.
C2 resolution ladder                 - is the residual an artefact of one clustering resolution?
C5 threshold sensitivity             - the positive call is a cut on a continuum, 1 to 53 UMIs.

CONTRACT DEVIATION, declared: C1 as frozen asks for k nearest neighbours in the round-2 *integrated*
embedding. That embedding was not persisted by the England follow-up - only the UMAP coordinates,
the sub_r* labels and the diffusion ordering were. This script therefore runs C1 in UMAP space,
which is a local-neighbourhood proxy: UMAP preserves local neighbour relations far better than
global distance, and kNN matching only uses local relations, but it is not the frozen space. The
integrated-space version stays deferred and is named in the report.

Exposure is FULL and C3/C4 results were seen before this ran. Nothing here may conclude
cell-intrinsic function.

Outputs under tables/stage1/.
"""
from __future__ import annotations
import argparse, sys, json, hashlib, datetime, platform
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--data-root', type=Path, required=True)
args = ap.parse_args()

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
ENG = ROOT / 'Research Article/gate2_C2_england_2025'
PROC = ENG / 'processed/continuation'
FUP = ENG / 'processed/followup'
OUT = HERE / 'tables/stage1'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(args.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd
from scipy.spatial import cKDTree
import importlib.metadata as im

PRIMARY = 'priming_associated'
EPS = ['priming_associated', 'AT2_identity', 'AT1_identity', 'Itga2', 'cycling']
KS = (5, 10, 20)
RESOLUTIONS = ('sub_r0.5', 'sub_r1.0', 'sub_r1.5')
ARM_A_LIBS = ['GSM7890835', 'GSM7890836']


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()


cfgA = json.loads((HERE / 'config/a16_question_contract.json').read_text(encoding='utf-8'))
cfgE = json.loads((ENG / 'config/continuation_contract.json').read_text(encoding='utf-8'))
modules = cfgE['modules']
MIN = cfgE['min_group_cells']
col_of = lambda ep: f'raw_{ep}' if ep in modules else f'raw_{ep}_log1p'

record = {'stage': 'A16 Stage 1 C1+C2+C5', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'a16_contract_sha256': digest(HERE / 'config/a16_question_contract.json'),
          'script_sha256': digest(Path(__file__)), 'interpreter': sys.executable,
          'python': platform.python_version(), 'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy']},
          'exposure': cfgA['exposure'],
          'contract_deviation': 'C1 uses UMAP-space kNN because the round-2 integrated embedding was not persisted; the integrated-space version is deferred',
          'floor_cells_per_side': MIN, 'ks': list(KS), 'resolutions': list(RESOLUTIONS), 'inputs': []}
(OUT / 'started_c1_c2_c5.json').write_text(json.dumps(record, indent=2) + '\n')

cells = pd.read_csv(PROC / 'cells_table.csv.gz', low_memory=False)
record['inputs'].append({'path': 'processed/continuation/cells_table.csv.gz', 'sha256': digest(PROC / 'cells_table.csv.gz')})
lab = {}
for exp in (1, 2):
    f = FUP / f'experiment{exp}_round2.csv.gz'
    lab[exp] = pd.read_csv(f).merge(cells, on=['gsm', 'barcode'], how='left', validate='one_to_one')
    record['inputs'].append({'path': f'processed/followup/experiment{exp}_round2.csv.gz', 'sha256': digest(f)})


def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 2 or len(y) < 2:
        return np.nan
    sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2))
    return float((x.mean() - y.mean()) / sd) if sd > 0 else np.nan


# ============ C1: neighbourhood-matched contrast (UMAP-space proxy) ============
def matched(df, tag, extra):
    rows = []
    d = df[df.primary_include].copy()
    if len(d) < 4 * MIN:
        return [{**extra, 'analysis': 'C1', 'scope': tag, 'status': f'not assessed: {len(d)} cells'}]
    d['depth_q'] = pd.qcut(d.total_umis.rank(method='first'), 4, labels=False)
    pos_all = d.Cd177_umi.to_numpy() >= 1
    if pos_all.sum() < MIN or (~pos_all).sum() < MIN:
        return [{**extra, 'analysis': 'C1', 'scope': tag, 'status': f'not assessed: {int(pos_all.sum())} positive cells'}]
    for k in KS:
        diffs = {ep: [] for ep in EPS}
        n_used = n_skipped = 0
        for q in range(4):
            s = d[d.depth_q == q]
            p = s[s.Cd177_umi >= 1]
            n = s[s.Cd177_umi < 1]
            if len(p) < 1 or len(n) < k:
                n_skipped += len(p)
                continue
            tree = cKDTree(n[['umap1', 'umap2']].to_numpy())
            _, nn = tree.query(p[['umap1', 'umap2']].to_numpy(), k=k)
            nn = np.atleast_2d(nn)
            for ep in EPS:
                yv_n = n[col_of(ep)].to_numpy(float)
                yv_p = p[col_of(ep)].to_numpy(float)
                diffs[ep].append(yv_p - yv_n[nn].mean(axis=1))
            n_used += len(p)
        if n_used < MIN:
            rows.append({**extra, 'analysis': 'C1', 'scope': tag, 'k': k, 'status': f'not assessed: {n_used} matched positives'})
            continue
        for ep in EPS:
            v = np.concatenate(diffs[ep])
            sd = float(np.std(v, ddof=1))
            rows.append({**extra, 'analysis': 'C1', 'scope': tag, 'k': k, 'status': 'estimated', 'endpoint': ep,
                         'n_matched_positives': n_used, 'n_positives_unmatched': n_skipped,
                         'mean_matched_difference': float(v.mean()),
                         'standardised_matched_difference': float(v.mean() / sd) if sd > 0 else np.nan})
    return rows


c1 = []
for gsm in ARM_A_LIBS:
    exp = 1
    d = lab[exp][(lab[exp].gsm == gsm) & lab[exp].gate_transition]
    c1 += matched(d, 'transitional gate, single library', {'arm': 'A_marginal_transitional_gate', 'unit': gsm, 'experiment': exp})
for exp, cl in [(1, 10), (1, 12), (1, 16), (1, 17), (1, 18), (2, 10), (2, 12)]:
    d = lab[exp][lab[exp]['sub_r1.0'] == cl]
    c1 += matched(d, 'all primary_include cells in the subcluster', {'arm': 'B_within_subcluster_FU_C', 'unit': f'exp{exp}_sub_r1.0={cl}', 'experiment': exp})
pd.DataFrame(c1).to_csv(OUT / 'A16_C1_neighbourhood_matched.csv', index=False)

# ============ C2: resolution ladder ============
c2 = []
for exp in (1, 2):
    d = lab[exp][lab[exp].primary_include]
    for res in RESOLUTIONS:
        num = den = 0.0
        used = 0
        vals = []
        for cl, g in d.groupby(res):
            p, n = g[g.Cd177_umi >= 1], g[g.Cd177_umi < 1]
            if len(p) < MIN or len(n) < MIN:
                continue
            e = smd(p[col_of(PRIMARY)], n[col_of(PRIMARY)])
            if not np.isfinite(e):
                continue
            w = min(len(p), len(n))
            num += w * e
            den += w
            used += 1
            vals.append(e)
        c2.append({'experiment': exp, 'resolution': res, 'n_clusters_total': int(d[res].nunique()),
                   'n_clusters_testable': used, 'cells': int(len(d)),
                   'pooled_weighted_priming_smd': float(num / den) if den > 0 else np.nan,
                   'min_cluster_smd': float(np.min(vals)) if vals else np.nan,
                   'max_cluster_smd': float(np.max(vals)) if vals else np.nan,
                   'n_clusters_positive': int(np.sum(np.array(vals) > 0)) if vals else 0,
                   'status': 'estimated' if used else 'not assessed: no cluster clears the floor'})
    p, n = d[d.Cd177_umi >= 1], d[d.Cd177_umi < 1]
    c2.append({'experiment': exp, 'resolution': 'marginal_no_conditioning', 'n_clusters_total': 1, 'n_clusters_testable': 1,
               'cells': int(len(d)), 'pooled_weighted_priming_smd': smd(p[col_of(PRIMARY)], n[col_of(PRIMARY)]),
               'status': 'estimated'})
pd.DataFrame(c2).to_csv(OUT / 'A16_C2_resolution_ladder.csv', index=False)

# ============ C5: threshold and marker-quality sensitivity ============
c5 = []
defs = [('Cd177_umi', 1, 'full depth, >=1 UMI'), ('Cd177_umi', 2, 'full depth, >=2 UMI'), ('Cd177_umi', 3, 'full depth, >=3 UMI'),
        ('d20260928_Cd177_umi', 1, 'thinned to 1000 UMI, seed 20260928, >=1'),
        ('d20260929_Cd177_umi', 1, 'thinned to 1000 UMI, seed 20260929, >=1')]
scopes = [('A_marginal_transitional_gate', gsm, lab[1][(lab[1].gsm == gsm) & lab[1].gate_transition & lab[1].primary_include]) for gsm in ARM_A_LIBS]
scopes += [('B_within_subcluster_FU_C', f'exp{e}_sub_r1.0={c}', lab[e][(lab[e]['sub_r1.0'] == c) & lab[e].primary_include]) for e, c in [(1, 10), (1, 12), (1, 16), (1, 17), (1, 18), (2, 10), (2, 12)]]
for arm, unit, d in scopes:
    for col, thr, tag in defs:
        if col not in d:
            continue
        v = d[col].to_numpy(float)
        p, n = d[v >= thr], d[v < thr]
        row = {'arm': arm, 'unit': unit, 'definition': tag, 'threshold': thr, 'column': col,
               'n_pos': len(p), 'n_neg': len(n)}
        if len(p) < MIN or len(n) < MIN:
            c5.append({**row, 'status': f'not assessed: fewer than {MIN} cells on a side'})
            continue
        c5.append({**row, 'status': 'estimated', **{f'smd_{ep}': smd(p[col_of(ep)], n[col_of(ep)]) for ep in EPS}})
pd.DataFrame(c5).to_csv(OUT / 'A16_C5_threshold_sensitivity.csv', index=False)

record['completed_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
record['outputs'] = {f: digest(OUT / f) for f in ['A16_C1_neighbourhood_matched.csv', 'A16_C2_resolution_ladder.csv', 'A16_C5_threshold_sensitivity.csv']}
(OUT / 'run_record_c1_c2_c5.json').write_text(json.dumps(record, indent=2) + '\n')

C1 = pd.DataFrame(c1)
print('--- C1 primary endpoint, k=10 ---', flush=True)
q = C1[(C1.get('endpoint') == PRIMARY) & (C1.k == 10)] if 'endpoint' in C1 else C1
print(q[['arm', 'unit', 'n_matched_positives', 'mean_matched_difference', 'standardised_matched_difference']].round(3).to_string(index=False), flush=True)
print('\n--- C2 resolution ladder ---', flush=True)
print(pd.DataFrame(c2)[['experiment', 'resolution', 'n_clusters_testable', 'pooled_weighted_priming_smd', 'n_clusters_positive']].round(3).to_string(index=False), flush=True)
print('\n--- C5 threshold sensitivity, priming ---', flush=True)
C5 = pd.DataFrame(c5)
print(C5[C5.status == 'estimated'][['arm', 'unit', 'definition', 'n_pos', 'smd_priming_associated']].round(3).to_string(index=False), flush=True)
