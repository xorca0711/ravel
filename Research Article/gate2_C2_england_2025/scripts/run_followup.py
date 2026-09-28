"""England follow-up FU_A-FU_E and FU_T. Frozen rules: config/followup_contract.json (commit 71f8ba0).

FU_A depth control of the CD177 secondary associations (4 prespecified methods + frozen decision rule)
FU_B AT1 module gate calibrated on Niethamer author labels, then applied to England
FU_E two-round epithelial subclustering, UMAP, PAGA connectivity, diffusion ordering (undirected)
FU_C within-subcluster CD177 contrast
FU_T tests of the paper's reversible-transition model: T1 topology, T2 intermediate density,
     T3 composition stationarity, T4 cycling equipotency
FU_D library-quality variance model

No direction of state conversion is computed or claimed. Outputs: trials/followup/*.csv + run_record.json.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform, random, gc
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); p.add_argument('--niethamer', type=Path, required=True); a = p.parse_args()
os.environ.setdefault('NUMBA_NUM_THREADS', '4'); os.environ.setdefault('OMP_NUM_THREADS', '4'); os.environ['JOBLIB_MULTIPROCESSING'] = '0'
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
os.environ.setdefault('NUMBA_CACHE_DIR', str(HERE / 'processed/continuation/numba_cache'))
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, scipy.sparse as sp, scanpy as sc, anndata as ad, igraph as ig
import importlib.metadata as im
CONTRACT = HERE / 'config/followup_contract.json'; CONT = HERE / 'config/continuation_contract.json'
fc = json.loads(CONTRACT.read_text(encoding='utf-8')); cfg = json.loads(CONT.read_text(encoding='utf-8'))
OUT = HERE / 'trials/followup'; PROC = HERE / 'processed/continuation'; FPROC = HERE / 'processed/followup'
OUT.mkdir(parents=True, exist_ok=True); FPROC.mkdir(parents=True, exist_ok=True)
assert not (OUT / 'run_record.json').exists(), 'Refuse overwrite of completed run'
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def git_head(root):
    g = root / '.git'; gd = Path(g.read_text().split(':', 1)[1].strip()) if g.is_file() else g
    ref = (gd / 'HEAD').read_text().strip()[5:]
    common = (gd / (gd / 'commondir').read_text().strip()).resolve() if (gd / 'commondir').exists() else gd
    f = common / ref
    return f.read_text().strip() if f.exists() else [l.split()[0] for l in (common / 'packed-refs').read_text().splitlines() if l.endswith(' ' + ref)][0]
MIN, MINBIN, GMIN = cfg['min_group_cells'], cfg['min_bin_cells_per_side'], cfg['gate_min_detected']
gates, modules, genes_ind = cfg['gates'], cfg['modules'], cfg['individual_genes']
anchors, immune, nonepi = cfg['epithelial_anchors'], cfg['immune_panel'], cfg['non_epithelial_panels']
SEED_T, SEED_F = 20260928, 20260930
record = {'stage': 'FU_A-FU_E, FU_T follow-up', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'followup_contract_sha256': digest(CONTRACT), 'continuation_contract_sha256': digest(CONT), 'script_sha256': digest(Path(__file__)),
          'git_head': git_head(ROOT), 'interpreter': sys.executable, 'python': platform.python_version(),
          'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy', 'scanpy', 'anndata', 'igraph', 'scikit-learn']},
          'exposure': fc['exposure'], 'inputs': [], 'interpretation': 'exploratory follow-up on fully exposed data; no direction of state conversion is computed or claimed'}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')
cells = pd.read_csv(PROC / 'cells_table.csv.gz', low_memory=False); record['inputs'].append({'path': 'processed/continuation/cells_table.csv.gz', 'sha256': digest(PROC / 'cells_table.csv.gz')})
manifest = pd.read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
features = pd.read_csv(PROC / 'matrices/features.csv', keep_default_na=False)
symbols = features.gene_symbol.astype(str).to_numpy().astype(str); present = set(symbols.tolist())
def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 2 or len(y) < 2: return np.nan
    sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2))
    return float((x.mean() - y.mean()) / sd) if sd > 0 else np.nan
EPS = ['cycling', 'priming_associated', 'AT2_identity', 'AT1_identity', 'Itga2', 'transition_RNA', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'hypoxia_control', 'P53_RNA_control']
col_of = lambda ep, pre='raw_': f'{pre}{ep}' if ep in modules else f'{pre}{ep}_log1p'
LIBS = ['GSM7890835', 'GSM7890836']

# ============ FU_A depth control ============
fu_a = []
for gsm in LIBS:
    z = np.load(PROC / f'cells/{gsm}_named_counts.npz', allow_pickle=False); genes = z['genes'].astype(str); gi = {g: i for i, g in enumerate(genes)}
    C, tot, bc = z['counts'], z['totals'].astype(float), z['barcodes'].astype(str)
    c = cells[cells.gsm == gsm].set_index('barcode').loc[bc]
    m = (c.primary_include & c.gate_transition).to_numpy()
    Cs, tots, cs = C[m], tot[m], c[m]
    pos = (Cs[:, gi['Cd177']] >= 1)
    base = {'library': gsm, 'n_pos': int(pos.sum()), 'n_neg': int((~pos).sum())}
    # method 1: unadjusted (reference)
    for ep in EPS: fu_a.append({**base, 'method': 'unadjusted', 'endpoint': ep, 'smd': smd(cs[col_of(ep)][pos], cs[col_of(ep)][~pos])})
    # method 2: within-transition thinning to 3000 UMIs
    ok = tots >= 3000; rng = np.random.default_rng(SEED_F)
    zf = np.load(PROC / f'matrices/{gsm}_sourceQC.npz'); X = sp.load_npz(PROC / f'matrices/{gsm}_sourceQC.npz').tocsr()
    bc_all = np.load(PROC / f'matrices/{gsm}_barcodes.npy', allow_pickle=False).astype(str)
    idx_all = pd.Index(bc_all).get_indexer(bc[m]); map_sel = np.array([gi.get(s, -1) for s in symbols], dtype=int)
    D = np.zeros_like(Cs)
    for i in np.where(ok)[0]:
        r_ = idx_all[i]; s0, s1 = X.indptr[r_:r_ + 2]; vals = X.data[s0:s1].astype(np.int64); ixs = X.indices[s0:s1]
        draw = rng.multivariate_hypergeometric(vals, 3000); sel = map_sel[ixs]; v = sel >= 0; np.add.at(D[i], sel[v], draw[v])
    logd = np.log1p(D / 3000.0 * 1e4)
    def dscore(ep):
        gl = modules.get(ep, [ep]); valid = [gi[g] for g in gl if g in present]; return logd[:, valid].mean(1)
    posd = (D[:, gi['Cd177']] >= 1) & ok
    negd = (D[:, gi['Cd177']] < 1) & ok
    base3 = {'library': gsm, 'n_pos': int(posd.sum()), 'n_neg': int(negd.sum()), 'n_below_budget': int((~ok).sum())}
    for ep in EPS: fu_a.append({**base3, 'method': 'thinned_3000_UMI', 'endpoint': ep, 'smd': smd(dscore(ep)[posd], dscore(ep)[negd]) if posd.sum() >= MIN and negd.sum() >= MIN else np.nan})
    # method 3: rank-biserial within library
    for ep in EPS:
        r_ = pd.Series(cs[col_of(ep)].to_numpy()).rank().to_numpy(); n1, n0 = pos.sum(), (~pos).sum()
        u = r_[pos].sum() - n1 * (n1 + 1) / 2
        fu_a.append({**base, 'method': 'rank_biserial', 'endpoint': ep, 'smd': float(2 * u / (n1 * n0) - 1)})
    # method 4: residual on log10 depth + detected genes
    Xd = np.column_stack([np.ones(len(cs)), np.log10(cs.total_umis.to_numpy(float)), cs.n_genes.to_numpy(float)])
    for ep in EPS:
        yv = cs[col_of(ep)].to_numpy(float); beta, *_ = np.linalg.lstsq(Xd, yv, rcond=None); res = yv - Xd @ beta
        fu_a.append({**base, 'method': 'depth_residualized', 'endpoint': ep, 'smd': smd(res[pos], res[~pos])})
    # method 5: depth-decile stratified
    dec = pd.qcut(cs.total_umis.rank(method='first'), 10, labels=False)
    for ep in EPS:
        num = den = 0.0; npos = nneg = 0; used = 0
        for d_ in range(10):
            s_ = dec == d_; x, y = cs[col_of(ep)][s_ & pos], cs[col_of(ep)][s_ & ~pos]
            if len(x) < MINBIN or len(y) < MINBIN: continue
            e = smd(x, y)
            if np.isnan(e): continue
            w = min(len(x), len(y)); num += w * e; den += w; npos += len(x); nneg += len(y); used += 1
        fu_a.append({**base, 'method': 'depth_decile_stratified', 'endpoint': ep, 'strata_used': used, 'n_pos_matched': npos, 'n_neg_matched': nneg, 'smd': float(num / den) if den > 0 else np.nan})
    del X, C, D; gc.collect()
A = pd.DataFrame(fu_a); A.to_csv(OUT / 'FU_A_depth_control.csv', index=False)
# frozen decision rule
verdicts = []
for ep in EPS:
    sub = A[A.endpoint == ep]; ok_all = True; detail = {}
    for lib in LIBS:
        u = sub[(sub.library == lib) & (sub.method == 'unadjusted')].smd.iloc[0]; detail[f'{lib}_unadjusted'] = u
        for meth in ['thinned_3000_UMI', 'rank_biserial', 'depth_residualized', 'depth_decile_stratified']:
            v = sub[(sub.library == lib) & (sub.method == meth)].smd
            v = v.iloc[0] if len(v) else np.nan; detail[f'{lib}_{meth}'] = v
            if np.isnan(v) or np.sign(v) != np.sign(u) or u == 0: ok_all = False
        r_ = detail[f'{lib}_depth_residualized']
        if np.isnan(r_) or abs(r_) < 0.5 * abs(u): ok_all = False
    verdicts.append({'endpoint': ep, 'verdict': 'depth_robust' if ok_all else 'depth_dependent_or_inconclusive', **{k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in detail.items()}})
pd.DataFrame(verdicts).to_csv(OUT / 'FU_A_verdicts.csv', index=False)
print('FU_A done:', {v['endpoint']: v['verdict'] for v in verdicts}, flush=True)

# ============ FU_B AT1 module gate calibrated on Niethamer ============
nh = ad.read_h5ad(a.niethamer); Xn = sp.csr_matrix(nh.layers['counts']); sym_n = nh.var['gene_symbol'].astype(str).to_numpy(); obs_n = nh.obs.copy()
record['inputs'].append({'path': str(a.niethamer), 'sha256': digest(a.niethamer)})
gi_n = {}
for j, g in enumerate(sym_n): gi_n.setdefault(g, []).append(j)
tot_n = np.asarray(Xn.sum(1)).ravel().astype(float)
def mod_score(X, gidx, tot, genes):
    cols = [j for g in genes if g in gidx for j in gidx[g]]
    sub = np.asarray(X[:, cols].todense()).astype(float) if len(cols) else np.zeros((X.shape[0], 1))
    per = np.column_stack([np.asarray(X[:, gidx[g]].sum(1)).ravel() for g in genes if g in gidx])
    return np.log1p(per / tot[:, None] * 1e4).mean(1)
at1_n = mod_score(Xn, gi_n, tot_n, modules['AT1_identity'])
lab_n = obs_n['author_celltype'].astype(str).to_numpy()
mask = np.isin(lab_n, ['AT1', 'AT2']); y = (lab_n[mask] == 'AT1').astype(int); s = at1_n[mask]
cands = np.quantile(s, np.linspace(0.01, 0.99, 197)); best = max(cands, key=lambda t: ( (s[y == 1] >= t).mean() + (s[y == 0] < t).mean() - 1 ))
sens = float((s[y == 1] >= best).mean()); spec = float((s[y == 0] < best).mean())
pd.DataFrame([{'threshold_mean_log1p_CP10k': float(best), 'youden_J': sens + spec - 1, 'sensitivity_AT1': sens, 'specificity_AT2': spec,
               'n_AT1': int((y == 1).sum()), 'n_AT2': int((y == 0).sum()), 'calibrated_on': 'Niethamer author_celltype, 25-sample atlas'}]).to_csv(OUT / 'FU_B_at1_gate_calibration.csv', index=False)
del nh, Xn; gc.collect()
cells['at1_module_gate'] = cells['raw_AT1_identity'] >= best
def excl(at2, tr, at1):
    s_ = np.full(len(at2), 'unresolved', dtype=object); s_[at2] = 'AT2'; s_[at1] = 'AT1'; s_[tr] = 'transition'; s_[tr & at1] = 'transition_AT1'; s_[at2 & at1] = 'mixed'; return s_
cells['state_moduleAT1'] = excl(cells.gate_AT2.to_numpy(), cells.gate_transition.to_numpy(), cells.at1_module_gate.to_numpy())
rows = []
for gsm, g in cells[cells.primary_include].groupby('gsm'):
    meta = manifest.set_index('gsm').loc[gsm]
    for defn, col in [('detection_gate_Ager_Hopx_Clic5', 'state'), ('module_gate_Pdpn_Cav1_Aqp5_Spock2', 'state_moduleAT1')]:
        vc = g[col].value_counts()
        for st in ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed', 'unresolved']:
            rows.append({'gsm': gsm, 'experiment': meta.experiment, 'population': meta.population, 'il1r1_status': meta.il1r1_status, 'collection_day': meta.collection_day,
                         'definition': defn, 'state': st, 'n_cells': int(vc.get(st, 0)), 'denominator': len(g), 'fraction': float(vc.get(st, 0) / len(g))})
pd.DataFrame(rows).to_csv(OUT / 'FU_B_state_composition_both_definitions.csv', index=False)
print(f'FU_B done: AT1 module threshold {best:.3f} (sens {sens:.2f}, spec {spec:.2f})', flush=True)

# ============ FU_E two-round subclustering, UMAP, PAGA, diffusion ============
CONT_PANELS = {'immune': 'Ptprc', 'endothelial': 'Pecam1', 'mesenchymal': 'Col1a1', 'ciliated': 'Foxj1'}
water, clu_rows, paga_rows, dpt_rows, t2_rows = [], [], [], [], []
adatas = {}
for exp in (1, 2):
    libs = manifest[manifest.experiment == exp]
    mats, obs = [], []
    for _, row in libs.iterrows():
        X = sp.load_npz(PROC / f'matrices/{row.gsm}_sourceQC.npz').tocsr(); bc = np.load(PROC / f'matrices/{row.gsm}_barcodes.npy', allow_pickle=False).astype(str)
        mats.append(X); obs.append(pd.DataFrame({'gsm': row.gsm, 'barcode': bc}))
    X = sp.vstack(mats, format='csr'); del mats; gc.collect()
    ob = pd.concat(obs, ignore_index=True).merge(cells, on=['gsm', 'barcode'], how='left', validate='one_to_one')
    lab1 = pd.read_csv(PROC / f'clustering/experiment{exp}_cluster_labels.csv.gz')
    ob = ob.merge(lab1, on=['gsm', 'barcode'], how='left', validate='one_to_one'); assert ob['louvain_r1.0'].notna().all()
    ad_all = ad.AnnData(X=X.astype(np.float32), obs=ob.set_index(ob.gsm + ':' + ob.barcode)); ad_all.var_names = features.gene_id.astype(str).to_numpy(); ad_all.var['symbol'] = symbols
    # contaminant rule on round-1 r=1.0 clusters
    disc = []
    for c_ in sorted(ad_all.obs['louvain_r1.0'].unique()):
        m = (ad_all.obs['louvain_r1.0'] == c_).to_numpy(); sub = ad_all[m]
        det = {k: float((np.asarray(sub[:, sub.var.symbol == gname].X.sum(1)).ravel() > 0).mean()) if (sub.var.symbol == gname).any() else 0.0 for k, gname in CONT_PANELS.items()}
        anch = np.column_stack([np.asarray(sub[:, sub.var.symbol == gname].X.sum(1)).ravel() > 0 for gname in anchors if (sub.var.symbol == gname).any()]).sum(1)
        keep = not (max(det.values()) >= 0.25 and (anch >= 2).mean() < 0.5)
        water.append({'experiment': exp, 'round1_cluster_r1.0': int(c_), 'n_cells': int(m.sum()), **{f'detect_{k}': v for k, v in det.items()}, 'epithelial_anchor_ge2_fraction': float((anch >= 2).mean()), 'retained': keep})
        if not keep: disc.append(c_)
    keepm = ~ad_all.obs['louvain_r1.0'].isin(disc).to_numpy()
    A2 = ad_all[keepm].copy(); del ad_all, X; gc.collect()
    nonmt = ~np.char.startswith(A2.var['symbol'].to_numpy().astype(str), 'mt-'); det3 = np.asarray((A2.X > 0).sum(0)).ravel() >= 3
    A2 = A2[:, nonmt & det3].copy()
    sc.pp.normalize_total(A2, target_sum=1e4); sc.pp.log1p(A2)
    sc.pp.highly_variable_genes(A2, flavor='seurat', n_top_genes=cfg['clustering']['HVG'])
    sc.pp.pca(A2, n_comps=30, mask_var='highly_variable', zero_center=True, random_state=SEED_T)
    sc.pp.neighbors(A2, n_neighbors=15, n_pcs=30, random_state=SEED_T)
    W = A2.obsp['connectivities'].tocoo(); mk = W.row < W.col
    g = ig.Graph(n=A2.n_obs, edges=list(zip(W.row[mk].tolist(), W.col[mk].tolist())), directed=False); g.es['weight'] = W.data[mk].tolist()
    for res in cfg['clustering']['resolutions']:
        random.seed(SEED_T); ig.set_random_number_generator(random)
        A2.obs[f'sub_r{res}'] = pd.Categorical(g.community_multilevel(weights='weight', resolution=res).membership)
    sc.tl.umap(A2, min_dist=0.3, spread=1.0, random_state=SEED_T)
    sc.tl.paga(A2, groups='sub_r1.0'); sc.tl.diffmap(A2, n_comps=15)
    at2m = (A2.obs.state == 'AT2').to_numpy(); root_pool = np.where(at2m)[0]
    root = int(root_pool[np.argmax(A2.obs.raw_AT2_identity.to_numpy()[root_pool])]); A2.uns['iroot'] = root
    sc.tl.dpt(A2)
    A2.obs[['gsm', 'barcode', 'sub_r0.5', 'sub_r1.0', 'sub_r1.5', 'dpt_pseudotime']].assign(umap1=A2.obsm['X_umap'][:, 0], umap2=A2.obsm['X_umap'][:, 1]).to_csv(FPROC / f'experiment{exp}_round2.csv.gz', index=False)
    conn = A2.uns['paga']['connectivities'].toarray(); groups = list(A2.obs['sub_r1.0'].cat.categories)
    mut = A2.obs.population.eq('mutant_RFP').to_numpy()
    for i_, gi_ in enumerate(groups):
        for j_ in range(i_ + 1, len(groups)):
            paga_rows.append({'experiment': exp, 'cluster_a': int(gi_), 'cluster_b': int(groups[j_]), 'connectivity': float(conn[i_, j_]),
                              'mutant_fraction_a': float(mut[(A2.obs['sub_r1.0'] == gi_).to_numpy()].mean()), 'mutant_fraction_b': float(mut[(A2.obs['sub_r1.0'] == groups[j_]).to_numpy()].mean())})
    for c_ in groups:
        m = (A2.obs['sub_r1.0'] == c_).to_numpy(); o = A2.obs[m]
        clu_rows.append({'experiment': exp, 'cluster': int(c_), 'n_cells': int(m.sum()), 'mutant_fraction': float(mut[m].mean()),
                         'gate_AT2_frac': float(o.gate_AT2.mean()), 'gate_transition_frac': float(o.gate_transition.mean()), 'gate_AT1_frac': float(o.gate_AT1.mean()),
                         'at1_module_gate_frac': float(o.at1_module_gate.mean()), 'Cd177_ge1_frac': float((o.Cd177_umi >= 1).mean()), 'Itga2_ge1_frac': float((o.Itga2_umi >= 1).mean()),
                         'cycling_ge2_frac': float((o.cycling_markers_detected >= 2).mean()), 'median_umis': float(o.total_umis.median()), 'doublet_fraction': float(o.doublet_flag.mean()),
                         'mean_AT2_identity': float(o.raw_AT2_identity.mean()), 'mean_AT1_identity': float(o.raw_AT1_identity.mean()), 'mean_transition_RNA': float(o.raw_transition_RNA.mean()), 'mean_cycling': float(o.raw_cycling.mean()),
                         'dpt_median': float(o.dpt_pseudotime.median())})
        dpt_rows.append({'experiment': exp, 'cluster': int(c_), 'n_cells': int(m.sum()), 'dpt_q10': float(o.dpt_pseudotime.quantile(.1)), 'dpt_median': float(o.dpt_pseudotime.median()), 'dpt_q90': float(o.dpt_pseudotime.quantile(.9))})
    # T2 intermediate density between mutant-dominated clusters (>=100 cells, >=50% mutant)
    PC = A2.obsm['X_pca']; big = [c_ for c_ in groups if ((A2.obs['sub_r1.0'] == c_).sum() >= 100 and mut[(A2.obs['sub_r1.0'] == c_).to_numpy()].mean() >= 0.5)]
    for i_ in range(len(big)):
        for j_ in range(i_ + 1, len(big)):
            ca, cb = big[i_], big[j_]; ma = (A2.obs['sub_r1.0'] == ca).to_numpy(); mb = (A2.obs['sub_r1.0'] == cb).to_numpy()
            va, vb = PC[ma].mean(0), PC[mb].mean(0); d = vb - va; nrm = float(np.dot(d, d))
            t = ((PC - va) @ d) / nrm; inside = (t >= 0) & (t <= 1)
            for variant, sel in [('all_cells', inside), ('doublets_removed', inside & ~A2.obs.doublet_flag.to_numpy())]:
                h, _ = np.histogram(t[sel], bins=10, range=(0, 1))
                ends = h[0] + h[9]; mid = h[3:7].sum()
                t2_rows.append({'experiment': exp, 'cluster_a': int(ca), 'cluster_b': int(cb), 'variant': variant, 'n_between': int(sel.sum()), 'n_end_bins': int(ends), 'n_middle_bins': int(mid),
                                'filled_valley_ratio': float(mid / ends) if ends else np.nan, 'bins': json.dumps(h.tolist())})
    adatas[exp] = A2.obs[['gsm', 'barcode', 'sub_r1.0', 'dpt_pseudotime']].copy()
    print(f'FU_E exp{exp}: round2 {A2.n_obs} cells, {len(groups)} clusters at r=1.0', flush=True)
    del A2, g, W, PC; gc.collect()
pd.DataFrame(water).to_csv(OUT / 'FU_E_round1_contaminant_waterfall.csv', index=False)
pd.DataFrame(clu_rows).to_csv(OUT / 'FU_E_round2_clusters.csv', index=False)
pd.DataFrame(paga_rows).to_csv(OUT / 'FU_T1_paga_connectivity.csv', index=False)
pd.DataFrame(dpt_rows).to_csv(OUT / 'FU_E_diffusion_ordering.csv', index=False)
pd.DataFrame(t2_rows).to_csv(OUT / 'FU_T2_intermediate_density.csv', index=False)

# ============ FU_C within-subcluster CD177 ============
fu_c = []
for exp in (1, 2):
    lab = adatas[exp].merge(cells, on=['gsm', 'barcode'], how='left')
    for c_, g in lab[lab.primary_include].groupby('sub_r1.0'):
        pos, neg = g[g.Cd177_umi >= 1], g[g.Cd177_umi < 1]
        row = {'experiment': exp, 'cluster': int(c_), 'n_cells': len(g), 'n_pos': len(pos), 'n_neg': len(neg)}
        if len(pos) < MIN or len(neg) < MIN: fu_c.append({**row, 'status': 'unavailable'}); continue
        for ep in EPS: fu_c.append({**row, 'status': 'estimated', 'endpoint': ep, 'smd': smd(pos[col_of(ep)], neg[col_of(ep)])})
pd.DataFrame(fu_c).to_csv(OUT / 'FU_C_within_subcluster_cd177.csv', index=False)

# ============ FU_T3 composition stationarity ============
t3 = []
comp = pd.DataFrame(rows); comp = comp[comp.definition == 'detection_gate_Ager_Hopx_Clic5']
for label, sel_a, sel_b in [('Exp1 mutant RFP day 4 -> day 14', (comp.experiment == 1) & (comp.population == 'mutant_RFP') & (comp.collection_day.astype(str) == '4'), (comp.experiment == 1) & (comp.population == 'mutant_RFP') & (comp.collection_day.astype(str) == '14')),
                            ('Exp2 Il1r1 het mutant RFP day 14 -> day 84', (comp.experiment == 2) & (comp.il1r1_status == 'heterozygous') & (comp.collection_day.astype(str) == '14'), (comp.experiment == 2) & (comp.il1r1_status == 'heterozygous') & (comp.collection_day.astype(str) == '84'))]:
    A_, B_ = comp[sel_a], comp[sel_b]
    ma = A_.groupby('state').fraction.mean(); mb = B_.groupby('state').fraction.mean()
    tv = 0.5 * float((mb - ma).abs().sum())
    within_a = 0.5 * float(A_.pivot_table(index='state', columns='gsm', values='fraction').diff(axis=1).iloc[:, -1].abs().sum())
    within_b = 0.5 * float(B_.pivot_table(index='state', columns='gsm', values='fraction').diff(axis=1).iloc[:, -1].abs().sum())
    t3.append({'comparison': label, 'total_variation_between_timepoints': tv, 'within_timepoint_TV_first': within_a, 'within_timepoint_TV_second': within_b,
               'between_exceeds_within': bool(tv > max(within_a, within_b)), **{f'mean_{k}_t1': float(ma.get(k, 0)) for k in ma.index}, **{f'mean_{k}_t2': float(mb.get(k, 0)) for k in mb.index}})
pd.DataFrame(t3).to_csv(OUT / 'FU_T3_composition_stationarity.csv', index=False)

# ============ FU_T4 cycling equipotency across states ============
t4 = []
mut_libs = manifest[manifest.population == 'mutant_RFP'].gsm.tolist()
for gsm in mut_libs:
    g = cells[(cells.gsm == gsm) & cells.primary_include]
    states = [s for s in ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed'] if (g.state == s).sum() >= MIN]
    dec = pd.qcut(g.total_umis.rank(method='first'), 10, labels=False)
    for i_ in range(len(states)):
        for j_ in range(i_ + 1, len(states)):
            sa, sb = states[i_], states[j_]; A_ = g[g.state == sa]; B_ = g[g.state == sb]
            num = den = 0.0; used = 0
            for d_ in range(10):
                x = g[(g.state == sa) & (dec == d_).to_numpy()].raw_cycling; y = g[(g.state == sb) & (dec == d_).to_numpy()].raw_cycling
                if len(x) < MINBIN or len(y) < MINBIN: continue
                e = smd(x, y)
                if np.isnan(e): continue
                w = min(len(x), len(y)); num += w * e; den += w; used += 1
            t4.append({'gsm': gsm, 'state_a': sa, 'state_b': sb, 'n_a': len(A_), 'n_b': len(B_),
                       'cycling_ge2_frac_a': float((A_.cycling_markers_detected >= 2).mean()), 'cycling_ge2_frac_b': float((B_.cycling_markers_detected >= 2).mean()),
                       'smd_unadjusted': smd(A_.raw_cycling, B_.raw_cycling), 'smd_depth_matched': float(num / den) if den > 0 else np.nan, 'strata_used': used})
pd.DataFrame(t4).to_csv(OUT / 'FU_T4_cycling_equipotency.csv', index=False)

# ============ FU_D library-quality variance model ============
thr = cells[cells.gsm.isin(['GSM7890829', 'GSM7890830']) & cells.primary_include].raw_TNFA_NFKB_RNA_disjoint.quantile(.9)
q = []
for gsm, g in cells[cells.primary_include].groupby('gsm'):
    meta = manifest.set_index('gsm').loc[gsm]
    q.append({'gsm': gsm, 'experiment': meta.experiment, 'population': meta.population, 'il1r1_status': meta.il1r1_status, 'collection_day': meta.collection_day,
              'response_high_fraction': float((g.raw_TNFA_NFKB_RNA_disjoint > thr).mean()), 'median_log10_umis': float(np.log10(g.total_umis).median()),
              'median_genes': float(g.n_genes.median()), 'median_mito_percent': float(g.mito_percent.median()), 'doublet_fraction': float(g.doublet_flag.mean()),
              'immune_high_fraction': float((g.n_immune_markers >= 2).mean())})
Q = pd.DataFrame(q); preds = ['median_log10_umis', 'median_genes', 'median_mito_percent', 'doublet_fraction', 'immune_high_fraction']
Xq = np.column_stack([np.ones(len(Q))] + [Q[c].to_numpy(float) for c in preds]); yq = Q.response_high_fraction.to_numpy(float)
beta, *_ = np.linalg.lstsq(Xq, yq, rcond=None); fit = Xq @ beta; ss_res = float(((yq - fit) ** 2).sum()); ss_tot = float(((yq - yq.mean()) ** 2).sum())
Q['fitted'] = fit; Q['residual'] = yq - fit; Q.to_csv(OUT / 'FU_D_library_quality_model.csv', index=False)
pd.DataFrame([{'n_libraries': len(Q), 'r_squared': 1 - ss_res / ss_tot, 'adj_r_squared': 1 - (ss_res / (len(Q) - len(preds) - 1)) / (ss_tot / (len(Q) - 1)), 'threshold_used': float(thr),
               **{f'coef_{c}': float(b) for c, b in zip(['intercept'] + preds, beta)}}]).to_csv(OUT / 'FU_D_model_summary.csv', index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), at1_module_threshold=float(best),
              outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv'))])
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2, default=str) + '\n')
print('follow-up completed', flush=True)
