"""FU_W: growth versus differentiation distance profiles in the deposited spatial pair arrays.

Frozen rules: config/followup_contract.json -> FU_W_growth_differentiation_decoupling, which discloses
that the slope computation was run as scoping before the block was frozen. Pooled rows carry no mouse or
clone identifiers, so nothing here is a mouse-level effect, a significance statement or a causal reading.

Outputs: trials/followup/FU_W_distance_slopes.csv and figures/FU_F05_growth_differentiation.png
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
PAL = json.loads((ROOT / 'analysis/config/palette.json').read_text(encoding='utf-8')); CAT = list(PAL['categorical'].values())
INK, INK2, AXIS, DEEMPH = PAL['ink'], PAL['ink_2'], PAL['axis'], PAL['deemph']
plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6,
                     'axes.titleweight': 'normal', 'axes.titlelocation': 'left', 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': AXIS, 'xtick.color': INK2, 'ytick.color': INK2, 'legend.frameon': False, 'savefig.dpi': 300, 'font.family': 'DejaVu Sans'})
FU = HERE / 'trials/followup'; FIG = FU / 'figures'; FIG.mkdir(parents=True, exist_ok=True)
cfg = json.loads((HERE / 'config/followup_contract.json').read_text(encoding='utf-8'))['FU_W_growth_differentiation_decoupling']
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
src = HERE / 'trials/batch1/clones/spatial_pooled_bin_profiles.csv'
sp = pd.read_csv(src); sp['mid'] = (sp.distance_low_um + sp.distance_high_um) / 2
MINROWS, MAXD = 10, 400
def wslope(x, y, w):
    xb = np.average(x, weights=w); yb = np.average(y, weights=w)
    return float((w * (x - xb) * (y - yb)).sum() / (w * (x - xb) ** 2).sum())
rows = []
for ds, g in sp.groupby('dataset'):
    g = g[(g.pair_rows >= MINROWS) & (g.mid <= MAXD)].sort_values('mid')
    if len(g) < 4: rows.append({'dataset': ds, 'eligible_bins': len(g), 'status': 'unavailable: fewer than 4 eligible bins'}); continue
    w = g.pair_rows.to_numpy(float); x = g.mid.to_numpy(float)
    sz = g.mean_neighbor_size.to_numpy(float); sn = g.mean_neighbor_spc_negative_fraction.to_numpy(float)
    b_sz = np.average(sz[-2:], weights=w[-2:]); b_sn = np.average(sn[-2:], weights=w[-2:])
    dense = g.pair_rows.to_numpy(float) >= 100
    dslopes = {}
    for nm, y in (('size', sz), ('spcneg', sn)):
        if dense.sum() >= 3:
            b = np.average(y[dense][-2:], weights=w[dense][-2:])
            dslopes[f'{nm}_relative_slope_dense_bins'] = wslope(x[dense], y[dense], w[dense]) * 100 / b * 100 if b else np.nan
        else:
            dslopes[f'{nm}_relative_slope_dense_bins'] = np.nan
    rows.append({'dataset': ds, 'context': 'oncogenic Red2Kras' if ds.startswith('kras') else 'homeostatic Confetti', 'status': 'estimated',
                 'eligible_bins': len(g), 'pair_rows': int(w.sum()), 'nearest_bin_um': float(x[0]), 'farthest_bin_um': float(x[-1]),
                 'min_bin_pair_rows': int(w.min()), 'distal_anchor_pair_rows': int(w[-2:].sum()), 'dense_bins_ge100_rows': int(dense.sum()), **dslopes,
                 'size_near': float(sz[0]), 'size_far': float(sz[-1]), 'size_slope_per_100um': wslope(x, sz, w) * 100,
                 'size_relative_slope_pct_per_100um': wslope(x, sz, w) * 100 / b_sz * 100 if b_sz else np.nan,
                 'spcneg_near': float(sn[0]), 'spcneg_far': float(sn[-1]), 'spcneg_slope_per_100um': wslope(x, sn, w) * 100,
                 'spcneg_relative_slope_pct_per_100um': wslope(x, sn, w) * 100 / b_sn * 100 if b_sn else np.nan,
                 'mouse_or_clone_ids_available': False})
R = pd.DataFrame(rows); R.to_csv(FU / 'FU_W_distance_slopes.csv', index=False)
E = R[R.status == 'estimated']
fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.2), gridspec_kw={'wspace': 0.42, 'top': 0.78, 'bottom': 0.26, 'width_ratios': [1.15, 1.15, 1]})
KR = ['kras4d', 'kras1w', 'kras2w', 'kras4w']; CF = [d for d in sp.dataset.unique() if d.startswith('conf')]
for ax, col, ylab, ttl in [(axes[0], 'mean_neighbor_size', 'mean neighbour clone size (cells)', 'Growth: neighbour clone size'),
                           (axes[1], 'mean_neighbor_spc_negative_fraction', 'mean pro-Sftpc-negative fraction', 'Differentiation: pro-Sftpc loss')]:
    for ds in CF:
        g = sp[(sp.dataset == ds) & (sp.pair_rows >= MINROWS) & (sp.mid <= MAXD)].sort_values('mid')
        if len(g) >= 4: ax.plot(g.mid, g[col], '-', color=DEEMPH, lw=0.9, zorder=1)
    for ds, c in zip(KR, CAT):
        g = sp[(sp.dataset == ds) & (sp.pair_rows >= MINROWS) & (sp.mid <= MAXD)].sort_values('mid')
        if len(g) >= 4: ax.plot(g.mid, g[col], '-o', color=c, lw=1.3, ms=3.5, label=ds.replace('kras', 'Red2Kras '), zorder=3)
    ax.set_xlabel('distance from mutant clone (um)'); ax.set_ylabel(ylab); ax.set_title(ttl, fontsize=7.5)
axes[0].legend(fontsize=6, loc='upper right'); axes[0].plot([], [], '-', color=DEEMPH, lw=0.9, label='homeostatic Confetti')
axes[0].legend(fontsize=6, loc='upper right')
ax = axes[2]
for k, (ctx, c) in enumerate([('homeostatic Confetti', DEEMPH), ('oncogenic Red2Kras', CAT[0])]):
    d = E[E.context == ctx]
    ax.scatter(d.size_relative_slope_pct_per_100um, d.spcneg_relative_slope_pct_per_100um, s=30, color=c, linewidths=0.4, edgecolor='white', label=ctx, zorder=3)
ax.axhline(0, color=AXIS, lw=0.8); ax.axvline(0, color=AXIS, lw=0.8)
ax.set_xlabel('size slope (% of distal level per 100 um)'); ax.set_ylabel('pro-Sftpc-negative slope\n(% of distal level per 100 um)')
ax.set_title('The two profiles do not track each other', fontsize=7.5); ax.legend(fontsize=6, loc='lower left')
for _, r_ in E[E.context == 'oncogenic Red2Kras'].iterrows():
    ax.annotate(r_.dataset.replace('kras', ''), (r_.size_relative_slope_pct_per_100um, r_.spcneg_relative_slope_pct_per_100um), textcoords='offset points', xytext=(4, 3), fontsize=5.5, color=INK2)
for i, L in enumerate('abc'): axes[i].text(-0.2 if i < 2 else -0.28, 1.1, L, transform=axes[i].transAxes, fontsize=10, fontweight='bold', va='bottom')
fig.suptitle("The source's own decoupling claim recovered from the deposit: neighbour growth falls with distance, its differentiation proxy does not", x=0.01, y=0.98, ha='left', fontsize=8)
fig.text(0.5, 0.005, 'Reproduces the comparison in Figures 5G-5J and 6E-6F of England et al. 2025 on the deposited pooled pair rows; it is not an independent contrast.\nPair rows collapse with distance (kras1w: 4,953 at 25 um to 13 at 225 um), the limitation the source methods name, so distal anchors and the steepest relative slopes rest on sparse bins.\nNo mouse or clone identifiers are deposited and a neighbour may recur across rows, so no mouse-level effect, significance or causal reading is available. Bins require >=10 pair rows and <=400 um.', ha='center', fontsize=5.6, color=INK2)
f = FIG / 'FU_F05_growth_differentiation.png'; fig.savefig(f, bbox_inches='tight'); plt.close(fig)
(FU / 'FU_W_run_record.json').write_text(json.dumps({'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'input': {'path': str(src.relative_to(HERE)).replace('\\', '/'), 'sha256': digest(src)},
    'script_sha256': digest(Path(__file__)), 'exposure_disclosure': cfg['exposure_disclosure'], 'outputs': {'FU_W_distance_slopes.csv': digest(FU / 'FU_W_distance_slopes.csv'), f.name: digest(f)}}, indent=2) + '\n')
print(E[['dataset', 'context', 'pair_rows', 'size_relative_slope_pct_per_100um', 'spcneg_relative_slope_pct_per_100um']].round(1).to_string(index=False), flush=True)
