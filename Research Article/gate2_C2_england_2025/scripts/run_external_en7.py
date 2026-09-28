"""England continuation EN7: the same CD177/transitional question in two already-exposed repair datasets.

Frozen rules: continuation_contract.json['external'] and the shared gates/modules/normalization.
  Choi 2020 (GSE145031, tomato_annotated_d2b.h5ad): PBS, day-14 and day-28 AT2-lineage libraries, each one
  library pooling two mice -> descriptive transfer with single-library units. Author states are context only.
  Niethamer 2025 (alveolar_trajectory.h5ad): author-lineage epithelium, known sacrifice day; only the day-0,
  day-11 and day-25 samples (two animals each) enter the primary descriptive comparisons 0->11 and 11->25.
  Later trace-window cohorts are reported for coverage only and never pooled.
Same independent gates (>=2 of 3), exclusive state rule, Cd177 grouping (>=1 / >=2 UMI, 30-cell floor per side),
mapped-gene per-cell scores (log1p CP10k, full-transcriptome totals) and EN7_library_CPM_v1 pseudobulks.
Primary inclusion: author-called cells minus (>=2 immune markers with <2 epithelial anchors); objects carry no
doublet calls (predicted_doublet all False). One exact 1,000-UMI thinning (seed 20260928) for cells with >=1,000 UMIs.
No integrated injury-cancer axis, no founder inference, no independent validation claim.

Outputs: trials/continuation/EN7/*.csv + run_record.json.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); p.add_argument('--niethamer', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, scipy.sparse as sp, h5py, anndata as ad
import importlib.metadata as im
CONTRACT = HERE / 'config/continuation_contract.json'; cfg = json.loads(CONTRACT.read_text(encoding='utf-8'))
OUT = HERE / 'trials/continuation/EN7'; OUT.mkdir(parents=True, exist_ok=True)
assert not (OUT / 'run_record.json').exists(), 'Refuse overwrite of completed run'
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def git_head(root):
    g = root / '.git'; gitdir = Path(g.read_text().split(':', 1)[1].strip()) if g.is_file() else g
    ref = (gitdir / 'HEAD').read_text().strip()[5:]
    common = (gitdir / (gitdir / 'commondir').read_text().strip()).resolve() if (gitdir / 'commondir').exists() else gitdir
    f = common / ref
    return f.read_text().strip() if f.exists() else [l.split()[0] for l in (common / 'packed-refs').read_text().splitlines() if l.endswith(' ' + ref)][0]
MIN = cfg['min_group_cells']; MINBIN = cfg['min_bin_cells_per_side']; SEED = 20260928; GMIN = cfg['gate_min_detected']
gates, modules, genes_ind = cfg['gates'], cfg['modules'], cfg['individual_genes']; anchors, immune = cfg['epithelial_anchors'], cfg['immune_panel']
needed = sorted(set(sum(gates.values(), []) + sum(modules.values(), []) + genes_ind + anchors + immune)); gi = {g: i for i, g in enumerate(needed)}
endpoint_genes = {**modules, **{g: [g] for g in genes_ind}}
CHOI = a.data_root / 'raw_data/GSE145031/choi_trials/tomato_annotated_d2b.h5ad'
record = {'stage': 'EN7 external transfer (Choi, Niethamer)', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'contract_sha256': digest(CONTRACT), 'script_sha256': digest(Path(__file__)),
          'git_head': git_head(ROOT), 'interpreter': sys.executable, 'python': platform.python_version(), 'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy', 'anndata', 'h5py']},
          'inputs': [{'path': str(CHOI), 'sha256': digest(CHOI)}, {'path': str(a.niethamer), 'sha256': digest(a.niethamer)}], 'normalization': 'EN7_library_CPM_v1 (contract shared_contract_amendment)',
          'interpretation': 'descriptive transfer on already exposed datasets; not independent A11 validation; Cd177 RNA is not surface protein'}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')

def exclusive_state(g):
    s = np.full(len(g['AT2']), 'unresolved', dtype=object); s[g['AT2']] = 'AT2'; s[g['AT1']] = 'AT1'; s[g['transition']] = 'transition'
    s[g['transition'] & g['AT1']] = 'transition_AT1'; s[g['AT2'] & g['AT1']] = 'mixed'; return s
def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2))
    return float((x.mean() - y.mean()) / sd) if sd > 0 else np.nan
def contrast(va, vb):
    va, vb = np.asarray(va, float), np.asarray(vb, float)
    if len(va) == 0 or len(vb) == 0: return {'n_units_A': len(va), 'n_units_B': len(vb), 'status': 'unavailable'}
    d = (va[:, None] - vb[None, :]).ravel()
    return {'n_units_A': len(va), 'n_units_B': len(vb), 'status': 'estimated' if min(len(va), len(vb)) >= 2 else 'single_unit_side', 'difference_of_unit_means': float(va.mean() - vb.mean()),
            'cross_unit_min': float(d.min()), 'cross_unit_max': float(d.max()), 'all_directions_agree': bool((d > 0).all() or (d < 0).all()), 'range_is_confidence_interval': False}

def measure(X, symbols, obs, study, unit_col, context_cols):
    """Per-cell named counts, gates, scores (raw and thinned) for one study. X: CSR cells x genes (integer counts)."""
    present = set(symbols.tolist()); rr, cc = [], []
    for j, g in enumerate(symbols):
        if g in gi: rr.append(j); cc.append(gi[g])
    agg = sp.csr_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(symbols), len(needed)))
    C = np.asarray((X @ agg).todense()).astype(np.int64); totals = np.asarray(X.sum(1)).ravel().astype(np.float64)
    det = C > 0; n_anchor = det[:, [gi[g] for g in anchors]].sum(1); n_imm = det[:, [gi[g] for g in immune]].sum(1)
    primary = ~((n_imm >= 2) & (n_anchor < 2))
    def scores(Cm, tot, pre):
        log = np.log1p(Cm / tot[:, None] * 1e4); out = {}
        for k, genes in modules.items():
            valid = [gi[g] for g in genes if g in present]; out[f'{pre}{k}'] = log[:, valid].mean(1) if valid else np.full(len(tot), np.nan)
        for g in genes_ind: out[f'{pre}{g}_log1p'] = log[:, gi[g]] if g in present else np.full(len(tot), np.nan)
        return out
    g = {k: det[:, [gi[x] for x in v]].sum(1) >= GMIN for k, v in gates.items()}
    tab = pd.DataFrame({'study': study, 'unit': obs[unit_col].astype(str).to_numpy(), **{c: obs[c].astype(str).to_numpy() for c in context_cols}, 'total_umis': totals, 'primary_include': primary,
                        'gate_AT2': g['AT2'], 'gate_transition': g['transition'], 'gate_AT1': g['AT1'], 'state': exclusive_state(g), 'Cd177_umi': C[:, gi['Cd177']], 'Itga2_umi': C[:, gi['Itga2']],
                        'cycling_markers_detected': det[:, [gi[x] for x in modules['cycling']]].sum(1)}, index=obs.index)
    tab = tab.assign(**scores(C, totals, 'raw_'))
    # exact 1,000-UMI thinning for cells with >=1,000 UMIs
    rng = np.random.default_rng(SEED); D = np.zeros_like(C); ok = totals >= 1000; map_sel = np.array([gi.get(s, -1) for s in symbols], dtype=int)
    for i in np.where(ok)[0]:
        s0, s1 = X.indptr[i:i + 2]; vals = X.data[s0:s1].astype(np.int64); ix = X.indices[s0:s1]
        draw = rng.multivariate_hypergeometric(vals, 1000); sel = map_sel[ix]; v = sel >= 0; np.add.at(D[i], sel[v], draw[v])
    dd = D > 0; gd = {k: dd[:, [gi[x] for x in v]].sum(1) >= GMIN for k, v in gates.items()}
    tab['thin_eligible'] = ok; tab['d_gate_transition'] = gd['transition']; tab['d_gate_AT2'] = gd['AT2']; tab['d_gate_AT1'] = gd['AT1']; tab['d_state'] = exclusive_state(gd)
    tab['d_Cd177_umi'] = D[:, gi['Cd177']]; tab['d_cycling_markers_detected'] = dd[:, [gi[x] for x in modules['cycling']]].sum(1)
    tab = tab.assign(**scores(np.where(ok[:, None], D, 0), np.where(ok, 1000.0, np.nan), 'd_'))
    return tab, C, totals, D, present

def analyse(tab, C, totals, D, present, study, unit_order, contrasts, coverage_units=()):
    comp, pb, cd_groups, cd_con, cd_match, con_rows = [], [], [], [], [], []
    for variant, pre, inc, gate_pre, Cm, tot in [('primary', 'raw_', tab.primary_include, '', C, totals), ('depth1000_seed20260928', 'd_', tab.primary_include & tab.thin_eligible, 'd_', D, np.full(len(tab), 1000.0))]:
        for unit in list(unit_order) + list(coverage_units):
            m = (tab.unit == unit) & inc; g = tab[m]; n = int(m.sum()); role = 'primary_unit' if unit in unit_order else 'coverage_only'
            ctx = {c: g[c].iloc[0] for c in g.columns if c in ('day', 'library', 'sacrifice_day', 'tamoxifen_start_day')} if n else {}
            base = {'study': study, 'variant': variant, 'unit': unit, 'unit_role': role, **ctx, 'denominator': n}
            for s in ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed', 'unresolved']: comp.append({**base, 'group': f'state_{s}', 'n_cells': int((g[f'{gate_pre}state'] == s).sum()), 'fraction': float((g[f'{gate_pre}state'] == s).mean()) if n else np.nan})
            comp.append({**base, 'group': 'Cd177_ge1_all', 'n_cells': int((g[f'{gate_pre}Cd177_umi'] >= 1).sum()), 'fraction': float((g[f'{gate_pre}Cd177_umi'] >= 1).mean()) if n else np.nan})
            for s in ['all', 'AT2', 'transition', 'mixed']:
                sub = g if s == 'all' else g[g[f'{gate_pre}state'] == s]
                if len(sub) < MIN: pb.append({**base, 'state': s, 'n_cells': len(sub), 'status': 'unavailable'}); continue
                idx = tab.index.get_indexer(sub.index); lcpm = np.log2(Cm[idx].sum(0) / tot[idx].sum() * 1e6 + 1)
                for k, genes in endpoint_genes.items():
                    valid = [gi[x] for x in genes if x in present]
                    pb.append({**base, 'state': s, 'n_cells': len(sub), 'status': 'estimated', 'endpoint': k, 'pseudobulk_mean_log2_CPM1': float(np.mean(lcpm[valid])) if valid else np.nan,
                               'cell_median_log1p_CP10k': float(sub[f'{pre}{k}' if k in modules else f'{pre}{k}_log1p'].median()), 'detection_fraction': float((sub[f'{pre}{k}' if k in modules else f'{pre}{k}_log1p'] > 0).mean())})
            t = g[g[f'{gate_pre}gate_transition']]
            for thr in cfg['Cd177_thresholds_UMI']:
                pos, neg = t[t[f'{gate_pre}Cd177_umi'] >= thr], t[t[f'{gate_pre}Cd177_umi'] < thr]
                row = {**base, 'n_transition': len(t), 'Cd177_threshold_UMI': thr, 'n_Cd177_pos': len(pos), 'n_Cd177_neg': len(neg), 'Cd177_umi_counts_in_pos': json.dumps({str(int(k)): int(v) for k, v in pos[f'{gate_pre}Cd177_umi'].value_counts().sort_index().items()})}
                avail = len(pos) >= MIN and len(neg) >= MIN; cd_groups.append({**row, 'status': 'available' if avail else 'unavailable'})
                if not avail: continue
                for ep in ['cycling', 'AT2_identity', 'AT1_identity', 'Itga2', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'Tonsl', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'transition_RNA', 'hypoxia_control', 'P53_RNA_control']:
                    col = f'{pre}{ep}' if ep in modules else f'{pre}{ep}_log1p'; x, y = pos[col], neg[col]
                    cd_con.append({**row, 'endpoint': ep, 'role': 'primary' if ep == 'cycling' else 'secondary', 'difference_of_means': float(x.mean() - y.mean()), 'smd': smd(x, y), 'detection_pos': float((x > 0).mean()), 'detection_neg': float((y > 0).mean())})
                tt = t.copy(); tt['pos'] = tt[f'{gate_pre}Cd177_umi'] >= thr; tt['depth_bin'] = pd.qcut(tt.total_umis.rank(method='first'), 4, labels=False); tt['hyp'] = tt[f'{pre}hypoxia_control'] > tt[f'{pre}hypoxia_control'].median(); tt['cyc'] = tt[f'{gate_pre}cycling_markers_detected'] >= 2
                for ep in ['cycling', 'AT2_identity', 'AT1_identity', 'Itga2', 'TNFA_NFKB_RNA_disjoint']:
                    col = f'{pre}{ep}' if ep in modules else f'{pre}{ep}_log1p'; keys = ['depth_bin', 'hyp'] + ([] if ep == 'cycling' else ['cyc']); num = den = 0.0; npos = nneg = 0
                    for _, s_ in tt.groupby(keys):
                        a_, b_ = s_[s_.pos][col], s_[~s_.pos][col]
                        if len(a_) < MINBIN or len(b_) < MINBIN: continue
                        e = smd(a_, b_)
                        if np.isnan(e): continue
                        w = min(len(a_), len(b_)); num += w * e; den += w; npos += len(a_); nneg += len(b_)
                    cd_match.append({**row, 'endpoint': ep, 'strata_design': '+'.join(keys), 'n_pos_matched': npos, 'n_neg_matched': nneg, 'status': 'estimated' if den > 0 and npos >= MIN and nneg >= MIN else 'unavailable', 'weighted_smd': float(num / den) if den > 0 else np.nan})
        # within-study contrasts on unit-level quantities
        Cdf = pd.DataFrame(comp); Cdf = Cdf[(Cdf.variant == variant) & (Cdf.unit_role == 'primary_unit')]; Pdf = pd.DataFrame(pb); Pdf = Pdf[(Pdf.variant == variant) & (Pdf.status == 'estimated') & (Pdf.unit_role == 'primary_unit')]
        for label, A, B in contrasts:
            for grp, s_ in Cdf.groupby('group'): con_rows.append({'study': study, 'variant': variant, 'contrast': label, 'quantity': 'unit fraction', 'group_or_state': grp, 'endpoint': '', **contrast(s_[s_.unit.isin(A)].fraction, s_[s_.unit.isin(B)].fraction)})
            for (st, ep), s_ in Pdf.groupby(['state', 'endpoint']): con_rows.append({'study': study, 'variant': variant, 'contrast': label, 'quantity': 'pseudobulk_mean_log2_CPM1', 'group_or_state': st, 'endpoint': ep, **contrast(s_[s_.unit.isin(A)].pseudobulk_mean_log2_CPM1, s_[s_.unit.isin(B)].pseudobulk_mean_log2_CPM1)})
    return comp, pb, cd_groups, cd_con, cd_match, con_rows

all_out = {k: [] for k in ['composition', 'pseudobulk', 'cd177_groups', 'cd177_contrasts', 'cd177_matched', 'contrasts', 'author_state_crosstab']}
# ---------------- Choi
ch = ad.read_h5ad(CHOI); Xc = sp.csr_matrix(ch.layers['counts']); assert np.all(Xc.data == np.floor(Xc.data)) and Xc.data.min() >= 0
sym_c = np.array(ch.var_names.astype(str)); obs_c = ch.obs.copy(); obs_c['library'] = obs_c['library'].astype(str); obs_c['day'] = obs_c['library'].str.extract(r'(PBS|Day\d+)')[0]
tab_c, Cc, tot_c, Dc, pres_c = measure(Xc, sym_c, obs_c, 'Choi_2020', 'library', ['day', 'state']); del ch
units_c = ['PBS_AT2_Tomato', 'Day14_AT2_Tomato', 'Day28_AT2_Tomato']
res = analyse(tab_c, Cc, tot_c, Dc, pres_c, 'Choi_2020', units_c, [('Day14 minus PBS (single libraries)', ['Day14_AT2_Tomato'], ['PBS_AT2_Tomato']), ('Day28 minus Day14 (single libraries)', ['Day28_AT2_Tomato'], ['Day14_AT2_Tomato'])])
for k, v in zip(list(all_out)[:6], res): all_out[k] += v
xs = tab_c[tab_c.primary_include].assign(author_state=obs_c.loc[tab_c.primary_include, 'state'].astype(str).to_numpy()).groupby(['unit', 'author_state', 'state']).size().reset_index(name='n_cells'); xs['study'] = 'Choi_2020'; all_out['author_state_crosstab'] += xs.to_dict('records')
record['Choi'] = {'cells': int(len(tab_c)), 'primary_include': int(tab_c.primary_include.sum()), 'thin_eligible': int(tab_c.thin_eligible.sum()), 'genes_mapped_of_needed': len(pres_c & set(needed))}
print('Choi done', record['Choi'], flush=True); del Xc
# ---------------- Niethamer
nh = ad.read_h5ad(a.niethamer); Xn = sp.csr_matrix(nh.layers['counts']); assert np.all(Xn.data == np.floor(Xn.data)) and Xn.data.min() >= 0
sym_n = nh.var['gene_symbol'].astype(str).to_numpy(); obs_n = nh.obs.copy()
for c in ['sample_id', 'author_celltype', 'author_lineage']: obs_n[c] = obs_n[c].astype(str)
for c in ['sacrifice_day', 'tamoxifen_start_day']:  # stored as numeric/categorical; normalise to integer strings ('0', '11', '25')
    num = pd.to_numeric(obs_n[c].astype(str), errors='coerce'); obs_n[c] = np.where(num.notna(), num.fillna(-1).astype(int).astype(str), obs_n[c].astype(str))
assert (obs_n.author_lineage == 'Epithelium').all()
assert all(len(obs_n[obs_n.sacrifice_day == d].sample_id.unique()) == 2 for d in ['0', '11', '25']), obs_n.sacrifice_day.value_counts().to_dict()
tab_n, Cn, tot_n, Dn, pres_n = measure(Xn, sym_n, obs_n, 'Niethamer_2025', 'sample_id', ['sacrifice_day', 'tamoxifen_start_day', 'author_celltype']); del nh
day_units = {d: sorted(obs_n[obs_n.sacrifice_day == d].sample_id.unique().tolist()) for d in ['0', '11', '25']}
primary_units = sum(day_units.values(), []); other_units = sorted(set(obs_n.sample_id) - set(primary_units))
res = analyse(tab_n, Cn, tot_n, Dn, pres_n, 'Niethamer_2025', primary_units, [('day 11 minus day 0 (2 animals each)', day_units['11'], day_units['0']), ('day 25 minus day 11 (2 animals each)', day_units['25'], day_units['11'])], coverage_units=other_units)
for k, v in zip(list(all_out)[:6], res): all_out[k] += v
xs = tab_n[tab_n.primary_include].groupby(['unit', 'sacrifice_day', 'author_celltype', 'state']).size().reset_index(name='n_cells'); xs['study'] = 'Niethamer_2025'; all_out['author_state_crosstab'] += xs.to_dict('records')
record['Niethamer'] = {'cells': int(len(tab_n)), 'primary_include': int(tab_n.primary_include.sum()), 'thin_eligible': int(tab_n.thin_eligible.sum()), 'primary_units_day0_11_25': day_units, 'coverage_only_units': len(other_units), 'genes_mapped_of_needed': len(pres_n & set(needed))}
print('Niethamer done', record['Niethamer'], flush=True)
for k, v in all_out.items(): pd.DataFrame(v).to_csv(OUT / f'EN7_{k}.csv', index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv'))])
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2, default=str) + '\n'); print('EN7 completed', flush=True)
