"""Follow-up figures FU_F01-FU_F04. Reads saved follow-up tables and the round-2 embedding only.
No arrows of state conversion are drawn: PAGA connectivity and diffusion ordering are undirected."""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
PAL = json.loads((ROOT / 'analysis/config/palette.json').read_text(encoding='utf-8')); CAT = list(PAL['categorical'].values())
INK, INK2, MUTED, GRID, AXIS, DEEMPH = PAL['ink'], PAL['ink_2'], PAL['muted'], PAL['grid'], PAL['axis'], PAL['deemph']
plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'axes.titleweight': 'normal', 'axes.titlelocation': 'left',
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': AXIS, 'xtick.color': INK2, 'ytick.color': INK2, 'legend.frameon': False,
                     'figure.facecolor': 'white', 'savefig.dpi': 300, 'font.family': 'DejaVu Sans'})
FU = HERE / 'trials/followup'; FPROC = HERE / 'processed/followup'; FIG = FU / 'figures'; FIG.mkdir(exist_ok=True)
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def letter(ax, s, dx=-0.14, dy=1.06): ax.text(dx, dy, s, transform=ax.transAxes, fontsize=10, fontweight='bold', va='bottom', ha='left')
rec = {'rendered_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'figures': {}}

# ---------------- FU_F01 round-2 UMAP with overlays
cl = pd.read_csv(FU / 'FU_E_round2_clusters.csv')
fig, axes = plt.subplots(2, 4, figsize=(9.2, 4.8), gridspec_kw={'wspace': 0.08, 'hspace': 0.22, 'top': 0.84})
for r_, exp in enumerate([1, 2]):
    e = pd.read_csv(FPROC / f'experiment{exp}_round2.csv.gz')
    U = e[['umap1', 'umap2']].to_numpy(); n = len(e)
    sub = pd.read_csv(HERE / 'processed/continuation/cells_table.csv.gz', usecols=['gsm', 'barcode', 'state', 'Cd177_umi', 'Itga2_umi', 'population', 'cycling_markers_detected'], low_memory=False)
    e = e.merge(sub, on=['gsm', 'barcode'], how='left')
    order = np.random.default_rng(0).permutation(n)
    SC = {'AT2': CAT[0], 'transition': CAT[1], 'transition_AT1': '#f2a07b', 'AT1': CAT[2], 'mixed': CAT[3], 'unresolved': DEEMPH}
    ax = axes[r_, 0]
    for s_, c_ in SC.items():
        m = (e.state == s_).to_numpy()[order]
        ax.scatter(U[order][m, 0], U[order][m, 1], s=0.6, c=c_, linewidths=0, rasterized=True)
    ax.set_title(f'Experiment {exp}: gate state', fontsize=7); letter(ax, 'ab'[r_], dx=-0.08)
    for k, (col, ttl, cmapname) in enumerate([('Cd177_umi', 'Cd177 UMIs', 'Blues'), ('Itga2_umi', 'Itga2 UMIs', 'Oranges'), ('cycling_markers_detected', 'cycling markers', 'Greens')]):
        ax = axes[r_, k + 1]; v = np.log1p(e[col].to_numpy(float))[order]
        ax.scatter(U[order][v <= 0, 0], U[order][v <= 0, 1], s=0.5, c=DEEMPH, linewidths=0, rasterized=True)
        sc_ = ax.scatter(U[order][v > 0, 0], U[order][v > 0, 1], s=1.6, c=v[v > 0], cmap=cmapname, linewidths=0, rasterized=True, vmin=0)
        ax.set_title(f'{ttl} (log1p)', fontsize=7)
        cb = fig.colorbar(sc_, ax=ax, fraction=0.035, pad=0.02); cb.ax.tick_params(labelsize=5)
    for ax in axes[r_]:
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
    axes[r_, 0].annotate('', xy=(0.13, 0.03), xytext=(0.02, 0.03), xycoords='axes fraction', arrowprops=dict(arrowstyle='-|>', color=INK2, lw=0.8))
    axes[r_, 0].annotate('', xy=(0.02, 0.14), xytext=(0.02, 0.03), xycoords='axes fraction', arrowprops=dict(arrowstyle='-|>', color=INK2, lw=0.8))
    axes[r_, 0].text(0.15, 0.02, 'UMAP1', transform=axes[r_, 0].transAxes, fontsize=5, color=INK2); axes[r_, 0].text(0.03, 0.16, 'UMAP2', transform=axes[r_, 0].transAxes, fontsize=5, color=INK2)
fig.legend(handles=[Line2D([], [], marker='o', ls='', ms=4, color=c_, label=s_.replace('_', '+')) for s_, c_ in SC.items()], loc='lower center', ncol=6, bbox_to_anchor=(0.5, -0.04))
fig.suptitle('Two-round epithelial subclustering (paper-style pipeline): Cd177 and Itga2 mark adjacent, partly overlapping regions of the mutant compartment', x=0.01, y=0.99, ha='left', fontsize=8)
f1 = FIG / 'FU_F01_round2_umap.png'; fig.savefig(f1, bbox_inches='tight'); plt.close(fig)

# ---------------- FU_F02 depth control
A = pd.read_csv(FU / 'FU_A_depth_control.csv')
eps = ['priming_associated', 'AT2_identity', 'AT1_identity', 'Itga2', 'transition_RNA', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'cycling', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'hypoxia_control', 'P53_RNA_control']
epn = ['priming', 'AT2 identity', 'AT1 identity', 'Itga2', 'transition RNA', 'shared module', 'lesion module', 'cycling', 'TNF/NF-kB', 'Nfkbia', 'hypoxia ctrl', 'p53 ctrl']
M = {'unadjusted': ('o', 1.0), 'depth_residualized': ('s', 0.85), 'depth_decile_stratified': ('D', 0.7), 'rank_biserial': ('^', 0.55), 'thinned_3000_UMI': ('v', 0.4)}
fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.4), sharey=True, gridspec_kw={'wspace': 0.06, 'top': 0.84, 'bottom': 0.22})
y = np.arange(len(eps))
for ax, lib, col in zip(axes, ['GSM7890835', 'GSM7890836'], [CAT[0], CAT[1]]):
    for meth, (mk, al) in M.items():
        s = A[(A.library == lib) & (A.method == meth)].set_index('endpoint').smd
        ax.scatter([s.get(e, np.nan) for e in eps], y, marker=mk, s=26, color=col, alpha=al, linewidths=0.4, edgecolor='white', label=meth.replace('_', ' '))
    ax.axvline(0, color=AXIS, lw=0.8); ax.set_title(f'{lib} (2-week mutant RFP)')
axes[0].set_yticks(y); axes[0].set_yticklabels(epn); axes[0].invert_yaxis()
axes[0].legend(loc='lower left', fontsize=6, ncol=1)
fig.supxlabel('standardized effect, Cd177-detected minus Cd177-zero cells', fontsize=8, y=0.13)
fig.text(0.5, 0.03, 'Frozen rule: depth-robust requires sign agreement across all methods in BOTH libraries and |residualized| >= half |unadjusted|.\nThe 3,000-UMI thinning leaves GSM7890836 below the 30-cell floor (26 Cd177+ cells), so the frozen rule returns "inconclusive" for every endpoint;\nthe three methods available in both libraries are shown and discussed as a disclosed post-hoc relaxation.', ha='center', fontsize=6, color=INK2)
fig.suptitle('Depth control: the frozen rule returns depth_dependent_or_inconclusive for all 12 endpoints because the\n3,000-UMI arm is unavailable in GSM7890836; in the three adjustments available in both libraries the priming and\nAT2/AT1 identity effects keep sign and at least half their unadjusted magnitude',
                 x=0.01, y=1.02, ha='left', fontsize=8)
f2 = FIG / 'FU_F02_depth_control.png'; fig.savefig(f2, bbox_inches='tight'); plt.close(fig)

# ---------------- FU_F03 topology (undirected) + within-subcluster CD177
t1 = pd.read_csv(FU / 'FU_T1_paga_connectivity.csv'); t2 = pd.read_csv(FU / 'FU_T2_intermediate_density.csv'); c7 = pd.read_csv(FU / 'FU_C_within_subcluster_cd177.csv')
t2['middle_share'] = t2.bins.apply(lambda b: sum(json.loads(b)[3:7]) / max(sum(json.loads(b)), 1))
fig = plt.figure(figsize=(9.2, 3.6)); gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 0.85, 1.5], wspace=0.42, top=0.8, bottom=0.18)
ax = fig.add_subplot(gs[0, 0]); exp = 1
m = t1[(t1.experiment == exp) & (t1.mutant_fraction_a >= 0.5) & (t1.mutant_fraction_b >= 0.5)]
nodes = sorted(set(m.cluster_a) | set(m.cluster_b)); pos = {c_: (np.cos(2 * np.pi * i / len(nodes)), np.sin(2 * np.pi * i / len(nodes))) for i, c_ in enumerate(nodes)}
info = cl[(cl.experiment == exp)].set_index('cluster')
for _, r_ in m.iterrows():
    if r_.connectivity < 0.05: continue
    x1, y1 = pos[r_.cluster_a]; x2, y2 = pos[r_.cluster_b]
    ax.plot([x1, x2], [y1, y2], color=INK2, lw=0.4 + 3.2 * r_.connectivity, alpha=0.35 + 0.5 * r_.connectivity, solid_capstyle='round', zorder=1)
for c_ in nodes:
    x_, y_ = pos[c_]; sz = 60 + 220 * info.loc[c_, 'Cd177_ge1_frac']
    ax.scatter([x_], [y_], s=sz, color=CAT[0] if info.loc[c_, 'gate_transition_frac'] >= 0.3 else DEEMPH, edgecolor=INK, linewidth=0.6, zorder=3)
    ax.text(x_ * 1.28, y_ * 1.28, f"c{c_}", ha='center', va='center', fontsize=6)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Experiment 1 mutant subclusters:\nPAGA connectivity (undirected)', fontsize=7, pad=14); letter(ax, 'a', dx=-0.02, dy=1.12)
ax.text(0.5, -0.06, 'edge width = connectivity; blue = transition-gated >=30%; node size = Cd177+ fraction', transform=ax.transAxes, ha='center', fontsize=5.5, color=INK2)
ax = fig.add_subplot(gs[0, 1])
for k, (e_, col) in enumerate([(1, CAT[0]), (2, CAT[1])]):
    v = t2[(t2.experiment == e_) & (t2.variant == 'doublets_removed')].middle_share.to_numpy()
    ax.scatter(np.full(len(v), k) + np.random.default_rng(1).uniform(-0.12, 0.12, len(v)), v, s=12, color=col, alpha=0.8, linewidths=0)
    ax.plot([k - 0.22, k + 0.22], [np.median(v)] * 2, color=INK, lw=1.4)
ax.set_xticks([0, 1]); ax.set_xticklabels(['Exp 1\n(21 pairs)', 'Exp 2\n(45 pairs)']); ax.set_ylabel('share of cells in the middle 40%\nof the inter-centroid axis')
ax.set_title('Transcriptional intermediates\nbetween mutant subclusters', fontsize=7, pad=14); letter(ax, 'b', dx=-0.3, dy=1.12); ax.set_ylim(0, 1)
ax.text(0.5, -0.30, 'doublet-flagged cells removed; removal changes each value by <=0.002', transform=ax.transAxes, ha='center', fontsize=5.5, color=INK2)
ax = fig.add_subplot(gs[0, 2]); av = c7[c7.status == 'estimated']
piv = av.pivot_table(index='endpoint', columns=['experiment', 'cluster'], values='smd').reindex(eps)
im = ax.imshow(piv.to_numpy(), cmap='RdBu_r', vmin=-1.5, vmax=1.5, aspect='auto')
for i in range(piv.shape[0]):
    for j in range(piv.shape[1]):
        v = piv.to_numpy()[i, j]
        if np.isfinite(v): ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=5, color='white' if abs(v) > 0.9 else INK)
ax.set_yticks(range(len(eps))); ax.set_yticklabels(epn, fontsize=6); ax.set_xticks(range(piv.shape[1]))
ax.set_xticklabels([f'E{e_}c{c_}' for e_, c_ in piv.columns], fontsize=6, rotation=90); ax.tick_params(length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.set_label('SMD, Cd177-detected minus zero', fontsize=6); cb.ax.tick_params(labelsize=5)
ax.set_title('Within subclusters the Cd177 contrast\nretains median |SMD| 0.36 against 1.60-2.17 pooled', fontsize=7, pad=14); letter(ax, 'c', dx=-0.3, dy=1.12)
fig.suptitle('Mutant subclusters form one connected component except cluster 14 (PAGA connectivity 0 to all six others);\ncells occupy the inter-centroid middle 40% at median 0.20-0.25, below a uniform 0.40; the pooled CD177 contrast is\nlargely a between-subcluster difference',
                 x=0.01, y=1.02, ha='left', fontsize=8)
f3 = FIG / 'FU_F03_topology_and_within_cluster.png'; fig.savefig(f3, bbox_inches='tight'); plt.close(fig)

# ---------------- FU_F04 AT1 gate calibration and consequences + cycling equipotency
cal = pd.read_csv(FU / 'FU_B_at1_gate_calibration.csv').iloc[0]; comp = pd.read_csv(FU / 'FU_B_state_composition_both_definitions.csv'); t4 = pd.read_csv(FU / 'FU_T4_cycling_equipotency.csv')
fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.4), gridspec_kw={'wspace': 0.42, 'top': 0.8, 'bottom': 0.2, 'width_ratios': [1, 1.1, 1.1]})
ax = axes[0]
mixed = comp[comp.state == 'mixed'].pivot_table(index='gsm', columns='definition', values='fraction')
ax.scatter(mixed['detection_gate_Ager_Hopx_Clic5'], mixed['module_gate_Pdpn_Cav1_Aqp5_Spock2'], s=22, color=CAT[0], linewidths=0)
lim = [0, max(mixed.max()) * 1.1]; ax.plot(lim, lim, color=AXIS, lw=0.8); ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel('mixed-state fraction\nAger/Hopx/Clic5 detection gate'); ax.set_ylabel('mixed-state fraction\nPdpn/Cav1/Aqp5/Spock2 module gate')
ax.set_title(f'AT1 definition changes the mixed state\n(threshold {cal.threshold_mean_log1p_CP10k:.2f}; sens {cal.sensitivity_AT1:.2f}, spec {cal.specificity_AT2:.2f} on Niethamer)', fontsize=7, pad=14); letter(ax, 'a', dx=-0.3, dy=1.12)
ax = axes[1]
sub = t4[(t4.strata_used >= 3)]
pairs = sub.groupby(['state_a', 'state_b']).filter(lambda g: g.gsm.nunique() >= 4)
labs = sorted(set(zip(pairs.state_a, pairs.state_b)))
for i, (sa, sb) in enumerate(labs):
    v = pairs[(pairs.state_a == sa) & (pairs.state_b == sb)].smd_depth_matched.to_numpy()
    ax.scatter(v, np.full(len(v), i) + np.random.default_rng(2).uniform(-0.1, 0.1, len(v)), s=16, color=CAT[0], alpha=0.8, linewidths=0)
    ax.plot([np.median(v)] * 2, [i - 0.2, i + 0.2], color=INK, lw=1.4)
ax.axvline(0, color=AXIS, lw=0.8); ax.set_yticks(range(len(labs))); ax.set_yticklabels([f'{a_} vs {b_}\n({pairs[(pairs.state_a==a_)&(pairs.state_b==b_)].gsm.nunique()} libraries)' for a_, b_ in labs], fontsize=6)
ax.set_xlabel('depth-matched cycling SMD between states'); ax.set_title('Cycling differences are inconsistent in sign;\nnegligible for AT2 vs mixed, larger for transition', fontsize=7, pad=14); letter(ax, 'b', dx=-0.42, dy=1.12)
ax = axes[2]
d = pd.read_csv(FU / 'FU_D_library_quality_model.csv'); s = pd.read_csv(FU / 'FU_D_model_summary.csv').iloc[0]
for popn, col in zip(sorted(d.population.unique()), CAT):
    m = d.population == popn; ax.scatter(d[m].fitted, d[m].response_high_fraction, s=26, color=col, label=popn.replace('_', ' '), linewidths=0)
lim = [0, max(d.response_high_fraction.max(), d.fitted.max()) * 1.1]; ax.plot(lim, lim, color=AXIS, lw=0.8); ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel('fitted from library quality alone'); ax.set_ylabel('observed response-high fraction')
ax.set_title(f'Technical quality explains much of the\nbetween-library response spread (R2 = {s.r_squared:.2f}, adj {s.adj_r_squared:.2f})', fontsize=7, pad=14); ax.legend(fontsize=6, loc='upper left'); letter(ax, 'c', dx=-0.3, dy=1.12)
fig.suptitle('Gate definition, cycling equivalence and library quality: three controls on the continuation conclusions', x=0.01, y=0.99, ha='left', fontsize=8)
f4 = FIG / 'FU_F04_controls.png'; fig.savefig(f4, bbox_inches='tight'); plt.close(fig)
for f in [f1, f2, f3, f4]: rec['figures'][f.name] = digest(f)
(FIG / 'render_record.json').write_text(json.dumps(rec, indent=2) + '\n'); print('figures rendered', list(rec['figures']), flush=True)
