"""England continuation EN2-EN5: independent-gate composition, within-state contrasts, separated RNA
axes, WT-YFP context and the CD177 transitional-state contrasts. Frozen rules: continuation_contract.json.

Units are libraries (descriptive; biological pools unknown; no p values). Cells are never treated as
replicates: within-library cell-level summaries are effect descriptions only. Missing or under-floor
groups are written as 'unavailable' rows, never as zero expression.

Variants: all_sourceQC, primary, strict (raw counts) and depth1000_seed20260928/20260929 (exact thinning,
primary inclusion). Gates, states and Cd177 grouping use the counts of the same variant.

Outputs: trials/continuation/EN2_5/*.csv + run_record.json.
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime, platform
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd
import importlib.metadata as im
CONTRACT = HERE / 'config/continuation_contract.json'; cfg = json.loads(CONTRACT.read_text(encoding='utf-8'))
OUT = HERE / 'trials/continuation/EN2_5'; PROC = HERE / 'processed/continuation'; OUT.mkdir(parents=True, exist_ok=True)
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
MIN = cfg['min_group_cells']; MINBIN = cfg['min_bin_cells_per_side']; SEEDS = [20260928, 20260929]
record = {'stage': 'EN2-EN5 RNA endpoints', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'contract_sha256': digest(CONTRACT),
          'script_sha256': digest(Path(__file__)), 'git_head': git_head(ROOT), 'interpreter': sys.executable, 'python': platform.python_version(),
          'versions': {m: im.version(m) for m in ['numpy', 'pandas', 'scipy']}, 'inputs': [], 'declared_rules_at_run': {
              'EN3_tail_threshold': 'per endpoint and variant, the pooled 90th percentile of per-cell scores in the two Experiment-1 WT baseline libraries (GSM7890829, GSM7890830); fixed, then applied to every library',
              'SMD': 'difference of group means divided by pooled SD (cells); descriptive effect size, not a test',
              'unavailable': 'group below the 30-cell floor on either side, or a required library missing'},
          'interpretation': 'library-level descriptive estimates; Cd177 RNA is not surface protein; associations are not causal or lineage evidence'}
(OUT / 'started.json').write_text(json.dumps(record, indent=2) + '\n')
cells = pd.read_csv(PROC / 'cells_table.csv.gz', low_memory=False); record['inputs'].append({'path': 'processed/continuation/cells_table.csv.gz', 'sha256': digest(PROC / 'cells_table.csv.gz'), 'rows': int(len(cells))})
manifest = pd.read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
features = pd.read_csv(PROC / 'matrices/features.csv', keep_default_na=False); present = set(features.gene_symbol.astype(str))
modules = cfg['modules']; genes_ind = cfg['individual_genes']
meta_cols = ['gsm', 'experiment', 'reporter', 'il1r1_status', 'population', 'collection_day']
lib_meta = manifest.set_index('gsm')[meta_cols[1:]]
VARIANTS = {'all_sourceQC': ('raw_', None), 'primary': ('raw_', 'primary_include'), 'strict': ('raw_', 'strict_include'),
            **{f'depth1000_seed{s}': (f'd{s}_', 'primary_include') for s in SEEDS}}
STATES = ['AT2', 'transition', 'transition_AT1', 'AT1', 'mixed', 'unresolved']
score_cols = lambda pre: {**{m: f'{pre}{m}' for m in modules}, **{g: f'{pre}{g}_log1p' for g in genes_ind}}
# named counts for pseudobulks
named = {}
for gsm in manifest.gsm:
    z = np.load(PROC / f'cells/{gsm}_named_counts.npz', allow_pickle=False)
    named[gsm] = {'genes': z['genes'].astype(str), 'barcodes': z['barcodes'].astype(str), 'counts': z['counts'], 'totals': z['totals'].astype(np.float64), **{f'thinned_{s}': z[f'thinned_{s}'] for s in SEEDS}}
    record['inputs'].append({'path': f'processed/continuation/cells/{gsm}_named_counts.npz', 'sha256': digest(PROC / f'cells/{gsm}_named_counts.npz')})
gidx = {g: i for i, g in enumerate(named[manifest.gsm[0]]['genes'])}
endpoint_genes = {**modules, **{g: [g] for g in genes_ind}}

def variant_frame(v):
    pre, inc = VARIANTS[v]; d = cells if inc is None else cells[cells[inc]]
    d = d.copy(); d['v_state'] = d[f'{pre}state' if pre != 'raw_' else 'state']
    for g in ['AT2', 'transition', 'AT1']: d[f'v_gate_{g}'] = d[f'{pre}gate_{g}' if pre != 'raw_' else f'gate_{g}']
    d['v_Cd177'] = d[f'{pre}Cd177_umi' if pre != 'raw_' else 'Cd177_umi']; d['v_cyc_det'] = d[f'{pre}cycling_markers_detected' if pre != 'raw_' else 'cycling_markers_detected']
    d['v_depth'] = 1000.0 if pre != 'raw_' else d['total_umis'].astype(float)
    sc = score_cols(pre); d = d.rename(columns={vv: f'ep_{k}' for k, vv in sc.items()})
    return d

def pseudobulk(gsm, barcodes, variant):
    """log2(CPM+1) per gene from summed counts with full-transcriptome totals; module mean over mapped genes."""
    nd = named[gsm]; sel = pd.Index(nd['barcodes']).get_indexer(barcodes); assert (sel >= 0).all()
    pre = VARIANTS[variant][0]
    C = nd['counts'][sel] if pre == 'raw_' else nd[f'thinned_{pre[1:-1]}'][sel]; tot = nd['totals'][sel].sum() if pre == 'raw_' else 1000.0 * len(sel)
    lcpm = np.log2(C.sum(0) / tot * 1e6 + 1)
    return {k: float(np.mean([lcpm[gidx[g]] for g in genes if g in present])) for k, genes in endpoint_genes.items()}

def contrast(rows_a, rows_b, value):
    va, vb = np.asarray(rows_a[value], float), np.asarray(rows_b[value], float)
    if len(va) == 0 or len(vb) == 0: return {'n_libraries_A': len(va), 'n_libraries_B': len(vb), 'status': 'unavailable'}
    diffs = (va[:, None] - vb[None, :]).ravel()
    return {'n_libraries_A': len(va), 'n_libraries_B': len(vb), 'status': 'estimated' if len(va) >= 2 and len(vb) >= 2 else 'single_library_side',
            'difference_of_library_means': float(va.mean() - vb.mean()), 'cross_library_min': float(diffs.min()), 'cross_library_max': float(diffs.max()),
            'all_cross_library_directions_agree': bool((diffs > 0).all() or (diffs < 0).all()), 'range_is_confidence_interval': False}

def smd(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); sd = np.sqrt((x.var(ddof=1) * (len(x) - 1) + y.var(ddof=1) * (len(y) - 1)) / (len(x) + len(y) - 2))
    return float((x.mean() - y.mean()) / sd) if sd > 0 else np.nan

comp, comp_con, ws, ws_con, axes, tails, en4, cd_groups, cd_con, cd_match, cd_null = [], [], [], [], [], [], [], [], [], [], []
EP = list(endpoint_genes)
for v in VARIANTS:
    d = variant_frame(v)
    # ---------------- EN2 composition and within-state pseudobulks
    for gsm, g in d.groupby('gsm'):
        n = len(g); m = {'variant': v, 'gsm': gsm, **lib_meta.loc[gsm].to_dict(), 'denominator': n}
        for s in STATES: comp.append({**m, 'group': f'state_{s}', 'n_cells': int((g.v_state == s).sum()), 'fraction': float((g.v_state == s).mean())})
        for gt in ['AT2', 'transition', 'AT1']: comp.append({**m, 'group': f'gate_{gt}', 'n_cells': int(g[f'v_gate_{gt}'].sum()), 'fraction': float(g[f'v_gate_{gt}'].mean())})
        comp.append({**m, 'group': 'Cd177_ge1_all', 'n_cells': int((g.v_Cd177 >= 1).sum()), 'fraction': float((g.v_Cd177 >= 1).mean())})
        for s in ['all'] + STATES:
            sub = g if s == 'all' else g[g.v_state == s]
            if len(sub) < MIN:
                ws.append({**m, 'state': s, 'n_cells': len(sub), 'status': 'unavailable'}); continue
            pb = pseudobulk(gsm, sub.barcode.to_numpy(), v)
            for k, val in pb.items(): ws.append({**m, 'state': s, 'n_cells': len(sub), 'status': 'estimated', 'endpoint': k, 'pseudobulk_mean_log2_CPM1': val,
                                                 'cell_median_log1p_CP10k': float(sub[f'ep_{k}'].median()), 'cell_q90_log1p_CP10k': float(sub[f'ep_{k}'].quantile(.9)), 'detection_fraction': float((sub[f'ep_{k}'] > 0).mean())})
    C = pd.DataFrame(comp); C = C[C.variant == v]; W = pd.DataFrame(ws); W = W[(W.variant == v) & (W.status == 'estimated')]
    for day in ['14', '84']:
        sub = C[(C.experiment == 2) & (C.collection_day.astype(str) == day)]
        for grp, s in sub.groupby('group'):
            comp_con.append({'variant': v, 'experiment': 2, 'collection_day': day, 'contrast': 'homozygous_deletion minus heterozygous', 'group': grp, 'quantity': 'library fraction',
                             **contrast(s[s.il1r1_status == 'homozygous_deletion'], s[s.il1r1_status == 'heterozygous'], 'fraction')})
        subw = W[(W.experiment == 2) & (W.collection_day.astype(str) == day)]
        for (state, ep), s in subw.groupby(['state', 'endpoint']):
            ws_con.append({'variant': v, 'experiment': 2, 'collection_day': day, 'contrast': 'homozygous_deletion minus heterozygous', 'state': state, 'endpoint': ep, 'quantity': 'pseudobulk_mean_log2_CPM1',
                           **contrast(s[s.il1r1_status == 'homozygous_deletion'], s[s.il1r1_status == 'heterozygous'], 'pseudobulk_mean_log2_CPM1')})
    # ---------------- EN3 separated axes, per library and per state, with declared tail threshold from WT baseline
    axes_ep = ['TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'Tonsl', 'cycling', 'AT2_identity', 'AT1_identity', 'transition_RNA', 'priming_associated', 'P53_RNA_control', 'hypoxia_control', 'Cd177', 'Itga2']
    base = d[d.gsm.isin(['GSM7890829', 'GSM7890830'])]
    thr = {k: float(base[f'ep_{k}'].quantile(.9)) for k in axes_ep}
    for gsm, g in d.groupby('gsm'):
        for s in ['all', 'transition', 'AT2', 'mixed']:
            sub = g if s == 'all' else g[g.v_state == s]; m = {'variant': v, 'gsm': gsm, **lib_meta.loc[gsm].to_dict(), 'state': s, 'n_cells': len(sub)}
            if len(sub) < MIN:
                axes.append({**m, 'status': 'unavailable'}); continue
            for k in axes_ep:
                x = sub[f'ep_{k}']
                axes.append({**m, 'status': 'estimated', 'endpoint': k, 'median': float(x.median()), 'q10': float(x.quantile(.1)), 'q90': float(x.quantile(.9)), 'mean': float(x.mean()), 'detection_fraction': float((x > 0).mean()),
                             'wt_baseline_q90_threshold': thr[k], 'fraction_above_threshold': float((x > thr[k]).mean())})
            # joint: response vs feedback, and AT2 vs AT1 identity (Spearman within library, cells)
            axes.append({**m, 'status': 'estimated', 'endpoint': 'spearman_response_vs_Nfkbia', 'mean': float(sub['ep_TNFA_NFKB_RNA_disjoint'].corr(sub['ep_Nfkbia'], method='spearman'))})
            axes.append({**m, 'status': 'estimated', 'endpoint': 'spearman_AT2_vs_AT1_identity', 'mean': float(sub['ep_AT2_identity'].corr(sub['ep_AT1_identity'], method='spearman'))})
            both = (sub['ep_TNFA_NFKB_RNA_disjoint'] > thr['TNFA_NFKB_RNA_disjoint']) & (sub['ep_Nfkbia'] <= sub['ep_Nfkbia'].median()) & (sub.v_state == 'mixed') if s == 'all' else None
            if both is not None: tails.append({**m, 'candidate': 'response_high & Nfkbia_at_or_below_library_median & mixed_state', 'n_cells': int(both.sum()), 'fraction': float(both.mean())})
    # ---------------- EN4 WT-YFP context at 2 weeks (14 d); 4-day arm has no matched baseline
    lib_pb = W[W.state == 'all'].set_index(['gsm', 'endpoint']).pseudobulk_mean_log2_CPM1
    def libval(gsms, ep): return pd.DataFrame({'x': [lib_pb.get((g, ep), np.nan) for g in gsms]}).dropna()
    for ep in EP:
        en4.append({'variant': v, 'collection_day': '14', 'contrast': 'WT_in_oncogenic_tissue YFP minus Confetti YFP baseline (single library)', 'endpoint': ep, **contrast(libval(['GSM7890837', 'GSM7890838'], ep), libval(['GSM7890830'], ep), 'x')})
        en4.append({'variant': v, 'collection_day': '14', 'contrast': 'mutant RFP minus WT_in_oncogenic_tissue YFP (unpaired libraries)', 'endpoint': ep, **contrast(libval(['GSM7890835', 'GSM7890836'], ep), libval(['GSM7890837', 'GSM7890838'], ep), 'x')})
        en4.append({'variant': v, 'collection_day': '4', 'contrast': 'WT_in_oncogenic_tissue YFP minus time-matched baseline', 'endpoint': ep, 'n_libraries_A': 2, 'n_libraries_B': 0, 'status': 'unavailable: no deposited 4-day Confetti arm'})
    # ---------------- EN5 CD177 within transition-gated cells
    cd_ep_primary = 'cycling'; cd_ep_secondary = ['AT2_identity', 'AT1_identity', 'Itga2', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'Tonsl', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'transition_RNA', 'priming_associated', 'hypoxia_control', 'P53_RNA_control']
    for gsm, g in d.groupby('gsm'):
        t = g[g.v_gate_transition]; m = {'variant': v, 'gsm': gsm, **lib_meta.loc[gsm].to_dict(), 'n_transition': len(t), 'n_primary_denominator': len(g)}
        for thr_u in cfg['Cd177_thresholds_UMI']:
            pos, neg = t[t.v_Cd177 >= thr_u], t[t.v_Cd177 < thr_u]
            row = {**m, 'Cd177_threshold_UMI': thr_u, 'n_Cd177_pos': len(pos), 'n_Cd177_neg': len(neg), 'Cd177_umi_counts_in_pos': json.dumps({str(int(k)): int(c) for k, c in pos.v_Cd177.value_counts().sort_index().items()})}
            cd_groups.append({**row, 'status': 'available' if len(pos) >= MIN and len(neg) >= MIN else 'unavailable'})
            if len(pos) < MIN or len(neg) < MIN: continue
            for ep, role in [(cd_ep_primary, 'primary')] + [(e, 'secondary') for e in cd_ep_secondary]:
                x, y = pos[f'ep_{ep}'], neg[f'ep_{ep}']
                cd_con.append({**row, 'endpoint': ep, 'role': role, 'stratum': 'all transition cells', 'mean_pos': float(x.mean()), 'mean_neg': float(y.mean()), 'difference_of_means': float(x.mean() - y.mean()),
                               'median_difference': float(x.median() - y.median()), 'smd': smd(x, y), 'detection_pos': float((x > 0).mean()), 'detection_neg': float((y > 0).mean())})
                if ep == 'cycling':
                    cd_con.append({**row, 'endpoint': 'cycling_markers_ge2_fraction', 'role': 'primary_binary', 'stratum': 'all transition cells', 'mean_pos': float((pos.v_cyc_det >= 2).mean()), 'mean_neg': float((neg.v_cyc_det >= 2).mean()),
                                   'difference_of_means': float((pos.v_cyc_det >= 2).mean() - (neg.v_cyc_det >= 2).mean())})
                else:  # cycling-stratified secondary contrasts
                    for lab, cm in [('cycling_markers<2', lambda z: z.v_cyc_det < 2), ('cycling_markers>=2', lambda z: z.v_cyc_det >= 2)]:
                        xs, ys = pos[cm(pos)][f'ep_{ep}'], neg[cm(neg)][f'ep_{ep}']
                        if len(xs) >= MINBIN and len(ys) >= MINBIN: cd_con.append({**row, 'endpoint': ep, 'role': 'secondary_cycling_stratified', 'stratum': lab, 'n_pos_stratum': len(xs), 'n_neg_stratum': len(ys), 'difference_of_means': float(xs.mean() - ys.mean()), 'smd': smd(xs, ys)})
            # matched contrast: 4 depth bins x hypoxia half (x cycling binary for non-cycling endpoints); weights min(n_pos, n_neg)
            tt = t.copy(); tt['pos'] = tt.v_Cd177 >= thr_u
            tt['depth_bin'] = pd.qcut(tt.v_depth.rank(method='first'), 4, labels=False) if tt.v_depth.nunique() > 4 else 0
            tt['hyp_high'] = tt['ep_hypoxia_control'] > tt['ep_hypoxia_control'].median(); tt['cyc'] = tt.v_cyc_det >= 2
            for ep in [cd_ep_primary] + cd_ep_secondary:
                keys = ['depth_bin', 'hyp_high'] + ([] if ep == 'cycling' else ['cyc'])
                num = den = 0.0; npos = nneg = 0; used = 0
                for _, s in tt.groupby(keys):
                    a_, b_ = s[s.pos][f'ep_{ep}'], s[~s.pos][f'ep_{ep}']
                    if len(a_) < MINBIN or len(b_) < MINBIN: continue
                    w = min(len(a_), len(b_)); e = smd(a_, b_)
                    if np.isnan(e): continue
                    num += w * e; den += w; npos += len(a_); nneg += len(b_); used += 1
                cd_match.append({**row, 'endpoint': ep, 'strata_design': '+'.join(keys), 'strata_used': used, 'n_pos_matched': npos, 'n_neg_matched': nneg,
                                 'status': 'estimated' if den > 0 and npos >= MIN and nneg >= MIN else 'unavailable', 'weighted_smd': float(num / den) if den > 0 else np.nan})
    # ---------------- co-detection null (1000-UMI seed 1 only): AT2&AT1 within transition cells vs permuted AT1 gate within hypoxia x cycling strata
    if v == f'depth1000_seed{SEEDS[0]}':
        rng = np.random.default_rng(SEEDS[0])
        for gsm, g in d.groupby('gsm'):
            t = g[g.v_gate_transition].copy()
            if len(t) < MIN: cd_null.append({'variant': v, 'gsm': gsm, **lib_meta.loc[gsm].to_dict(), 'n_transition': len(t), 'status': 'unavailable'}); continue
            t['hyp_high'] = t['ep_hypoxia_control'] > t['ep_hypoxia_control'].median(); t['cyc'] = t.v_cyc_det >= 2
            obs = int((t.v_gate_AT2 & t.v_gate_AT1).sum()); perm = np.zeros(200)
            for i in range(200):
                tot = 0
                for _, s in t.groupby(['hyp_high', 'cyc']):
                    at1 = rng.permutation(s.v_gate_AT1.to_numpy()); tot += int((s.v_gate_AT2.to_numpy() & at1).sum())
                perm[i] = tot
            cd_null.append({'variant': v, 'gsm': gsm, **lib_meta.loc[gsm].to_dict(), 'n_transition': len(t), 'status': 'estimated', 'observed_AT2_and_AT1': obs, 'permutation_mean': float(perm.mean()), 'permutation_sd': float(perm.std(ddof=1)),
                            'fraction_permutations_ge_observed': float((perm >= obs).mean()), 'n_permutations': 200, 'note': 'conditional descriptive null; no biological p value; no ambient correction'})
    print(f'variant {v} done', flush=True)
for name, rows in [('EN2_composition', comp), ('EN2_composition_contrasts', comp_con), ('EN2_within_state_pseudobulk', ws), ('EN2_within_state_contrasts', ws_con), ('EN3_axes_by_library', axes),
                   ('EN3_candidate_tail_occupancy', tails), ('EN4_wt_yfp_contrasts', en4), ('EN5_cd177_groups', cd_groups), ('EN5_cd177_contrasts', cd_con), ('EN5_cd177_matched', cd_match), ('EN5_codetection_null', cd_null)]:
    pd.DataFrame(rows).to_csv(OUT / f'{name}.csv', index=False)
record.update(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), outputs=[{'file': f.name, 'sha256': digest(f)} for f in sorted(OUT.glob('*.csv'))])
(OUT / 'run_record.json').write_text(json.dumps(record, indent=2) + '\n'); print('EN2-EN5 completed', flush=True)
