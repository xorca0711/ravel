"""Independent numerical/provenance verification of the England continuation outputs.

Recomputes, from the cached named counts and cluster labels (not from the analysis scripts' code paths):
gates, exclusive states, mapped-gene module scores, inclusion rules, thinning totals, EN2 composition and
pseudobulks, EN5 group counts / SMDs / matched weighted SMD, EN1 cross-tabulation, EN6 internal consistency
and analytic check, EN7 Choi/Niethamer composition from the source objects. Checks contract/script/output
hashes recorded in each run record. Writes trials/continuation/verification.json. Checks saved outputs;
it does not establish biological validity or independent pool replication.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); p.add_argument('--niethamer', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, scipy.sparse as sp, anndata as ad
cfg = json.loads((HERE / 'config/continuation_contract.json').read_text(encoding='utf-8'))
T = HERE / 'trials/continuation'; PROC = HERE / 'processed/continuation'
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
checks = []; maxdisc = 0.0
def check(name, ok, detail=None, disc=None):
    global maxdisc
    checks.append({'check': name, 'passed': bool(ok), **({'detail': detail} if detail is not None else {})})
    if disc is not None and np.isfinite(disc): maxdisc = max(maxdisc, float(disc))
def close(x, y, tol=1e-9): 
    x, y = np.asarray(x, float), np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y); d = float(np.abs(x[m] - y[m]).max()) if m.any() else 0.0
    return d <= tol and (np.isfinite(x) == np.isfinite(y)).all(), d
gates, modules, genes_ind, anchors, immune, nonepi = cfg['gates'], cfg['modules'], cfg['individual_genes'], cfg['epithelial_anchors'], cfg['immune_panel'], cfg['non_epithelial_panels']
features = pd.read_csv(PROC / 'matrices/features.csv', keep_default_na=False); present = set(features.gene_symbol.astype(str))
# ---------------- hashes
csha, asha = digest(HERE / 'config/continuation_contract.json'), digest(HERE / 'config/continuation_amendments.json')
for stage in ['prep', 'EN1', 'EN2_5', 'EN6', 'EN7']:
    rp = T / stage / 'run_record.json'
    if not rp.exists(): check(f'{stage}: run_record present', False); continue
    rec = json.loads(rp.read_text()); check(f'{stage}: contract hash matches', rec.get('contract_sha256') == csha)
    if 'amendments_sha256' in rec: check(f'{stage}: amendments hash matches', rec['amendments_sha256'] == asha)
    for o in rec.get('outputs', []): check(f'{stage}: output hash {o["file"]}', (T / stage / o['file']).exists() and digest(T / stage / o['file']) == o['sha256'])
prep = json.loads((T / 'prep/run_record.json').read_text()); check('prep: cells_table hash', digest(PROC / 'cells_table.csv.gz') == prep['ignored_outputs']['cells_table.csv.gz'])
# ---------------- prep recomputation from named counts
cells = pd.read_csv(PROC / 'cells_table.csv.gz', low_memory=False); manifest = pd.read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
qc = pd.read_csv(T / 'prep/QC_by_library.csv'); occ = pd.read_csv(T / 'prep/gate_occupancy_by_library.csv')
check('prep: source-QC total 44,196', len(cells) == 44196 and int(qc.source_QC_cells.sum()) == 44196)
for gsm in manifest.gsm:
    z = np.load(PROC / f'cells/{gsm}_named_counts.npz', allow_pickle=False); genes = z['genes'].astype(str); gi = {g: i for i, g in enumerate(genes)}
    C, tot, bc = z['counts'], z['totals'].astype(float), z['barcodes'].astype(str); c = cells[cells.gsm == gsm].set_index('barcode').loc[bc]
    det = C > 0
    for k, v in gates.items(): check(f'prep {gsm}: gate_{k}', (c[f'gate_{k}'].to_numpy() == (det[:, [gi[x] for x in v]].sum(1) >= 2)).all())
    g = {k: det[:, [gi[x] for x in v]].sum(1) >= 2 for k, v in gates.items()}
    st = np.full(len(bc), 'unresolved', dtype=object); st[g['AT2']] = 'AT2'; st[g['AT1']] = 'AT1'; st[g['transition']] = 'transition'; st[g['transition'] & g['AT1']] = 'transition_AT1'; st[g['AT2'] & g['AT1']] = 'mixed'
    check(f'prep {gsm}: exclusive state', (c.state.to_numpy() == st).all()); check(f'prep {gsm}: Cd177 umi', (c.Cd177_umi.to_numpy() == C[:, gi['Cd177']]).all())
    log = np.log1p(C / tot[:, None] * 1e4)
    for k, v in modules.items():
        valid = [gi[x] for x in v if x in present]; ok, d = close(c[f'raw_{k}'], log[:, valid].mean(1)); check(f'prep {gsm}: score {k}', ok, disc=d)
    n_anchor = det[:, [gi[x] for x in anchors]].sum(1); n_imm = det[:, [gi[x] for x in immune]].sum(1)
    check(f'prep {gsm}: primary rule', (c.primary_include.to_numpy() == (~c.doublet_flag.to_numpy() & ~((n_imm >= 2) & (n_anchor < 2)))).all())
    ne = np.zeros(len(bc), bool)
    for v in nonepi.values(): ne |= det[:, [gi[x] for x in v]].sum(1) >= 2
    check(f'prep {gsm}: strict rule', (c.strict_include.to_numpy() == (c.primary_include.to_numpy() & ~(n_imm >= 2) & ~(ne & (n_anchor < 2)))).all())
    D = z['thinned_20260928']; check(f'prep {gsm}: thinned counts <= 1000 and <= raw', (D.sum(1) <= 1000).all() and (D <= C).all() and (D >= 0).all())
    check(f'prep {gsm}: thinned Cd177 column', (c.d20260928_Cd177_umi.to_numpy() == D[:, gi['Cd177']]).all())
    o = occ[(occ.gsm == gsm) & (occ.variant == 'primary')].set_index('group').n_cells; pm = c.primary_include.to_numpy()
    check(f'prep {gsm}: occupancy transition/primary', int(o['transition']) == int((g['transition'] & pm).sum()) and int(o['transition_Cd177_ge1']) == int((g['transition'] & pm & (C[:, gi['Cd177']] >= 1)).sum()))
# ---------------- EN1 cross-tab recomputation (r=0.5)
cx = pd.read_csv(T / 'EN1/cluster_gate_crosstab.csv'); sizes = pd.read_csv(T / 'EN1/cluster_sizes.csv')
for exp in (1, 2):
    lab = pd.read_csv(PROC / f'clustering/experiment{exp}_cluster_labels.csv.gz').merge(cells[['gsm', 'barcode', 'state', 'gate_AT1', 'Cd177_umi']], on=['gsm', 'barcode'])
    check(f'EN1 exp{exp}: label rows = source-QC cells', len(lab) == int(qc[qc.experiment == exp].source_QC_cells.sum()))
    for res in (0.5, 1.0, 1.5):
        vc = lab[f'louvain_r{res}'].value_counts(); s = sizes[(sizes.experiment == exp) & (sizes.resolution == res)].set_index('cluster').n_cells
        check(f'EN1 exp{exp} r{res}: cluster sizes', all(int(vc[c]) == int(s[c]) for c in s.index) and len(vc) == len(s))
    sub = cx[(cx.experiment == exp) & (cx.resolution == 0.5)].set_index('cluster')
    for c_ in sub.index:
        g = lab[lab['louvain_r0.5'] == c_]
        check(f'EN1 exp{exp} cluster {c_}: state_mixed & AT1 gate frac', int(sub.loc[c_, 'state_mixed']) == int((g.state == 'mixed').sum()) and abs(sub.loc[c_, 'gate_AT1_frac'] - g.gate_AT1.mean()) < 1e-9)
# ---------------- EN2 composition and pseudobulk recomputation (primary variant)
comp = pd.read_csv(T / 'EN2_5/EN2_composition.csv'); ws = pd.read_csv(T / 'EN2_5/EN2_within_state_pseudobulk.csv')
prim = cells[cells.primary_include]
for gsm, g in prim.groupby('gsm'):
    row = comp[(comp.variant == 'primary') & (comp.gsm == gsm)].set_index('group')
    check(f'EN2 {gsm}: composition denominators/states', int(row.denominator.iloc[0]) == len(g) and all(int(row.loc[f'state_{s}', 'n_cells']) == int((g.state == s).sum()) for s in ['AT2', 'transition', 'mixed']))
    z = np.load(PROC / f'cells/{gsm}_named_counts.npz', allow_pickle=False); genes = z['genes'].astype(str); gi = {x: i for i, x in enumerate(genes)}; sel = pd.Index(z['barcodes'].astype(str)).get_indexer(g.barcode)
    lcpm = np.log2(z['counts'][sel].sum(0) / z['totals'][sel].sum() * 1e6 + 1)
    w = ws[(ws.variant == 'primary') & (ws.gsm == gsm) & (ws.state == 'all') & (ws.status == 'estimated')].set_index('endpoint').pseudobulk_mean_log2_CPM1
    for k, v in {**modules, **{x: [x] for x in genes_ind}}.items():
        valid = [gi[x] for x in v if x in present]; ok, d = close(w[k], lcpm[valid].mean()); check(f'EN2 {gsm}: pseudobulk {k}', ok, disc=d)
# ---------------- EN5 recomputation (primary variant, threshold 1)
grp = pd.read_csv(T / 'EN2_5/EN5_cd177_groups.csv'); con = pd.read_csv(T / 'EN2_5/EN5_cd177_contrasts.csv'); mat = pd.read_csv(T / 'EN2_5/EN5_cd177_matched.csv')
def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2)); return (x.mean() - y.mean()) / sd
avail = grp[(grp.variant == 'primary') & (grp.Cd177_threshold_UMI == 1) & (grp.status == 'available')]
check('EN5: available primary libraries are GSM7890835 and GSM7890836 only', sorted(avail.gsm) == ['GSM7890835', 'GSM7890836'])
for gsm in avail.gsm:
    t = prim[(prim.gsm == gsm) & prim.gate_transition]; pos, neg = t[t.Cd177_umi >= 1], t[t.Cd177_umi < 1]
    r_ = avail[avail.gsm == gsm].iloc[0]; check(f'EN5 {gsm}: group counts', int(r_.n_Cd177_pos) == len(pos) and int(r_.n_Cd177_neg) == len(neg))
    cyc = con[(con.variant == 'primary') & (con.gsm == gsm) & (con.Cd177_threshold_UMI == 1) & (con.endpoint == 'cycling') & (con.role == 'primary')].iloc[0]
    ok, d = close([cyc.smd], [smd(pos.raw_cycling, neg.raw_cycling)]); check(f'EN5 {gsm}: primary cycling SMD', ok, disc=d)
    for ep in ['AT2_identity', 'priming_associated', 'Itga2_log1p']:
        col = ep if ep in modules else ep; r2 = con[(con.variant == 'primary') & (con.gsm == gsm) & (con.Cd177_threshold_UMI == 1) & (con.endpoint == ep.replace('_log1p', '')) & (con.role == 'secondary')].iloc[0]
        ok, d = close([r2.smd], [smd(pos[f'raw_{col}'], neg[f'raw_{col}'])]); check(f'EN5 {gsm}: secondary SMD {ep}', ok, disc=d)
    # matched weighted SMD for cycling: 4 depth bins x hypoxia half, >=10 per side per stratum, weights min(n)
    tt = t.copy(); tt['pos'] = tt.Cd177_umi >= 1; tt['db'] = pd.qcut(tt.total_umis.astype(float).rank(method='first'), 4, labels=False); tt['hy'] = tt.raw_hypoxia_control > tt.raw_hypoxia_control.median()
    num = den = 0.0
    for _, s in tt.groupby(['db', 'hy']):
        x, y = s[s.pos].raw_cycling, s[~s.pos].raw_cycling
        if len(x) >= 10 and len(y) >= 10: w_ = min(len(x), len(y)); num += w_ * smd(x, y); den += w_
    m_ = mat[(mat.variant == 'primary') & (mat.gsm == gsm) & (mat.Cd177_threshold_UMI == 1) & (mat.endpoint == 'cycling')].iloc[0]
    ok, d = close([m_.weighted_smd], [num / den]); check(f'EN5 {gsm}: matched weighted SMD cycling', ok, disc=d)
check('EN5: no thinned variant has an available group', grp[(grp.variant.str.startswith('depth1000')) & (grp.status == 'available')].empty)
# ---------------- EN6 internal consistency
if (T / 'EN6/simulation_ccdf.csv').exists():
    cc = pd.read_csv(T / 'EN6/simulation_ccdf.csv'); sm = pd.read_csv(T / 'EN6/simulation_summary.csv'); an = pd.read_csv(T / 'EN6/analytic_birth_death_check.csv')
    mono = all((g.sort_values('size_n').ccdf_mean_P_N_gt_n.diff().dropna() <= 1e-12).all() for _, g in cc.groupby(['block', 'time_days', 'implementation', 'seed']))
    check('EN6: CCDF monotone nonincreasing and within [0,1]', mono and cc.ccdf_mean_P_N_gt_n.between(-1e-12, 1 + 1e-12).all())
    fs = {'Confetti': 0.16, 'Red2Kras_YFP': 0.12, 'Red2Kras_RFP': 0.08}
    for _, r_ in sm.iterrows():
        exp_f = int(np.floor(fs[r_.block] * 1000)) + 1 if r_.implementation != 'gillespie' else int(round(fs[r_.block] * 1000))
        check(f'EN6 {r_.block} t{int(r_.time_days)} {r_.implementation} s{int(r_.seed)}: F founders {exp_f}', int(r_.F_founders_per_replicate) == exp_f * 100 or int(r_.F_founders_per_replicate) == exp_f)
    check('EN6: analytic birth-death P0 within 0.005 and CCDF within 0.01', (np.abs(an.P0_analytic - an.P0_empirical) < 0.005).all() and (an['max_abs_ccdf_ge2_error_where_P_gt_1e-6'] < 0.01).all(), detail=an[['birth', 'death', 't', 'P0_analytic', 'P0_empirical']].round(4).to_dict('records'))
    check('EN6: Confetti and Red2Kras_YFP (q=0.5) literal vs fixed-branch identical in distribution (KS<0.01)', (pd.read_csv(T / 'EN6/implementation_differences.csv').query("comparison=='literal vs literal_fixed_branch' and block!='Red2Kras_RFP'").ks_distance_conditional_ge2 < 0.01).all())
else: check('EN6: outputs present', False)
# ---------------- EN7 recomputation of composition from source objects (primary variant)
if (T / 'EN7/EN7_composition.csv').exists():
    e7 = pd.read_csv(T / 'EN7/EN7_composition.csv'); e7 = e7[(e7.variant == 'primary')]
    def gate_states(X, symbols):
        gi = {}; 
        for j, g in enumerate(symbols): gi.setdefault(g, []).append(j)
        # detection per gene symbol: duplicated symbols are summed first (as in the analysis scripts), then > 0
        dg = {k: np.column_stack([np.asarray(X[:, gi[x]].sum(1)).ravel() > 0 for x in v if x in gi]) if any(x in gi for x in v) else np.zeros((X.shape[0], 0), bool) for k, v in {**gates, 'anchors': anchors, 'immune': immune}.items()}
        g = {k: dg[k].sum(1) >= 2 for k in gates}; st = np.full(X.shape[0], 'unresolved', dtype=object); st[g['AT2']] = 'AT2'; st[g['AT1']] = 'AT1'; st[g['transition']] = 'transition'; st[g['transition'] & g['AT1']] = 'transition_AT1'; st[g['AT2'] & g['AT1']] = 'mixed'
        primary = ~((dg['immune'].sum(1) >= 2) & (dg['anchors'].sum(1) < 2)); return st, primary, g
    ch = ad.read_h5ad(a.data_root / 'raw_data/GSE145031/choi_trials/tomato_annotated_d2b.h5ad'); Xc = sp.csr_matrix(ch.layers['counts']); st, pm, g = gate_states(Xc, np.array(ch.var_names.astype(str))); lib = ch.obs['library'].astype(str).to_numpy()
    for u in ['PBS_AT2_Tomato', 'Day14_AT2_Tomato', 'Day28_AT2_Tomato']:
        m = (lib == u) & pm; row = e7[(e7.study == 'Choi_2020') & (e7.unit == u)].set_index('group')
        check(f'EN7 Choi {u}: denominator and transition/mixed counts', int(row.denominator.iloc[0]) == int(m.sum()) and int(row.loc['state_transition', 'n_cells']) == int((st[m] == 'transition').sum()) and int(row.loc['state_mixed', 'n_cells']) == int((st[m] == 'mixed').sum()))
    del ch, Xc
    nh = ad.read_h5ad(a.niethamer); Xn = sp.csr_matrix(nh.layers['counts']); st, pm, g = gate_states(Xn, nh.var['gene_symbol'].astype(str).to_numpy()); sid = nh.obs['sample_id'].astype(str).to_numpy()
    for u in e7[(e7.study == 'Niethamer_2025') & (e7.unit_role == 'primary_unit')].unit.unique():
        m = (sid == u) & pm; row = e7[(e7.study == 'Niethamer_2025') & (e7.unit == u)].set_index('group')
        check(f'EN7 Niethamer {u}: denominator and transition counts', int(row.denominator.iloc[0]) == int(m.sum()) and int(row.loc['state_transition', 'n_cells']) == int((st[m] == 'transition').sum()))
else: check('EN7: outputs present', False)
n_pass = sum(c['passed'] for c in checks); n_fail = len(checks) - n_pass
out = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'checks_total': len(checks), 'checks_passed': n_pass, 'checks_failed': n_fail, 'max_abs_discrepancy': maxdisc,
       'failed': [c for c in checks if not c['passed']], 'scope': 'saved outputs and recomputation from cached counts; not biological validity, not pool independence', 'script_sha256': digest(Path(__file__)),
       'details_sample': [c for c in checks if 'detail' in c]}
(T / 'verification.json').write_text(json.dumps(out, indent=2, default=str) + '\n'); print(f'verification: {n_pass}/{len(checks)} passed; max discrepancy {maxdisc:.2e}; failed {n_fail}', flush=True)
for c in out['failed'][:20]: print('FAIL', c['check'])
