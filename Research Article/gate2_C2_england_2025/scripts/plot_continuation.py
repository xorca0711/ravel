"""Figures for the England continuation (EN_C01-EN_C06). Reads only saved trial tables; computes nothing new.
Palette from analysis/config/palette.json. Writes trials/continuation/figures/*.png + render_record.json."""
from __future__ import annotations
import argparse, os, sys, json, hashlib, datetime
from pathlib import Path
p = argparse.ArgumentParser(); p.add_argument('--data-root', type=Path, required=True); p.add_argument('--figures', nargs='+', choices=['EN_C01','EN_C02','EN_C03','EN_C04','EN_C05','EN_C06'], default=['EN_C01','EN_C02','EN_C03','EN_C04','EN_C05','EN_C06']); a = p.parse_args()
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
sys.path.insert(0, str(a.data_root / '.venv-x64/Lib/site-packages'))
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
PAL = json.loads((ROOT / 'analysis/config/palette.json').read_text(encoding='utf-8')); CAT = list(PAL['categorical'].values()); INK, INK2, MUTED, GRID, AXIS = PAL['ink'], PAL['ink_2'], PAL['muted'], PAL['grid'], PAL['axis']
plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8, 'legend.fontsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'axes.titleweight': 'normal', 'axes.titlelocation': 'left',
                     'xtick.direction': 'out', 'ytick.direction': 'out', 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': AXIS, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2,
                     'legend.frameon': False, 'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.dpi': 300, 'font.family': 'DejaVu Sans'})
T = HERE / 'trials/continuation'; FIG = T / 'figures'; FIG.mkdir(exist_ok=True)
def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
read_inputs = {}
def read_csv(path, **kwargs):
    read_inputs[Path(path).relative_to(HERE).as_posix()] = digest(path)
    return pd.read_csv(path, **kwargs)

def letter(ax, s): ax.text(-0.12, 1.08, s, transform=ax.transAxes, fontsize=10, fontweight='bold', va='bottom', ha='left')
manifest = read_csv(HERE / 'metadata/geo_library_manifest.csv', keep_default_na=False)
def lib_label(r):
    pop = {'WT_baseline': 'WT baseline', 'WT_in_oncogenic_tissue': 'WT-in-onc YFP', 'mutant_RFP': 'mutant RFP'}[r.population]; g = {'heterozygous': ' Il1r1 het', 'homozygous_deletion': ' Il1r1 KO'}.get(r.il1r1_status, '')
    return f"E{r.experiment} d{r.collection_day}{g} {pop} {r.gsm[-2:]}"
manifest['label'] = manifest.apply(lib_label, axis=1); order = manifest.sort_values(['experiment', 'collection_day', 'population', 'il1r1_status', 'gsm']).gsm.tolist(); lab = manifest.set_index('gsm').label
STATE_COL = {'AT2': CAT[0], 'transition': CAT[1], 'transition_AT1': '#f2a07b', 'AT1': CAT[2], 'mixed': CAT[3], 'unresolved': PAL['deemph']}
previous_record = json.loads((FIG / 'render_record.json').read_text())
record = {'rendered_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'palette_sha256': digest(ROOT / 'analysis/config/palette.json'), 'figures': dict(previous_record.get('figures', {}))}

if 'EN_C01' in a.figures:
    # ---------------- EN_C01: exclusive-state occupancy per library, primary vs thinned
    comp = read_csv(T / 'EN2_5/EN2_composition.csv')
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.8), sharey=True, gridspec_kw={'wspace': 0.18, 'bottom': 0.2, 'top': 0.9, 'left': 0.24})
    for ax, v, ttl in zip(axes, ['primary', 'depth1000_seed20260928'], ['Raw depth, primary inclusion', 'Exact 1,000-UMI thinning (seed 20260928)']):
        d = comp[(comp.variant == v) & comp.group.str.startswith('state_')].pivot(index='gsm', columns='group', values='fraction').loc[order]
        left = np.zeros(len(order))
        for s in ['AT2', 'mixed', 'transition', 'transition_AT1', 'AT1', 'unresolved']:
            ax.barh(range(len(order)), d[f'state_{s}'].to_numpy(), left=left, color=STATE_COL[s], label=s.replace('_', '+'), height=0.8); left += d[f'state_{s}'].to_numpy()
        ax.set_yticks(range(len(order))); ax.set_yticklabels([lab[g] for g in order]); ax.set_xlim(0, 1); ax.set_xlabel('fraction of included cells'); ax.set_title(ttl); ax.invert_yaxis()
    h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=6, title='exclusive gate state', bbox_to_anchor=(0.55, 0.0)); letter(axes[0], 'a'); letter(axes[1], 'b')
    fig.suptitle('Gate states are dominated by AT2 and AT2+AT1 co-detection; transition occupancy clears the\n30-cell floor only in mutant RFP libraries (non-mutant libraries hold 0-10 such cells) and is depth-sensitive',
                     x=0.01, y=1.06, ha='left', fontsize=8)
    f1 = FIG / 'EN_C01_state_occupancy.png'; fig.savefig(f1, bbox_inches='tight'); plt.close(fig)

if 'EN_C02' in a.figures:
    # ---------------- EN_C02: EN1 cluster x gate heatmap (r = 0.5)
    cx = read_csv(T / 'EN1/cluster_gate_crosstab.csv'); mk = read_csv(T / 'EN1/cluster_marker_panels.csv')
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.8), gridspec_kw={'width_ratios': [13, 17], 'wspace': 0.3, 'top': 0.82})
    cols = ['gate_AT2_frac', 'gate_transition_frac', 'gate_AT1_frac', 'Cd177_ge1_frac', 'cycling_ge2_frac']; names = ['AT2 gate', 'transition gate', 'AT1 gate', 'Cd177 >=1 UMI', 'cycling >=2 markers']
    for ax, exp, L in zip(axes, [1, 2], ['a', 'b']):
        d = cx[(cx.experiment == exp) & (cx.resolution == 0.5)].sort_values('n_cells', ascending=False); m = mk[(mk.experiment == exp) & (mk.resolution == 0.5)].set_index('cluster').top_panel_by_detection
        M = d[cols].to_numpy().T; im = ax.imshow(M, cmap='Blues', vmin=0, vmax=1, aspect='auto')
        for i in range(M.shape[0]):
            for j in range(M.shape[1]): ax.text(j, i, f'{M[i, j]:.2f}'.lstrip('0') if M[i, j] >= 0.005 else '0', ha='center', va='center', fontsize=5, color='white' if M[i, j] > 0.6 else INK)
        ax.set_yticks(range(len(cols))); ax.set_yticklabels(names if exp == 1 else []); ax.set_xticks(range(len(d)))
        ax.set_xticklabels([f"c{c} {n/1000:.1f}k {m[c].replace('_gate', '').replace('nonepi_', '')}" for c, n in zip(d.cluster, d.n_cells)], rotation=90, fontsize=5)
        ax.set_title(f'Experiment {exp}, r = 0.5 (n cells, top panel)', pad=12); ax.text(-0.02, 1.12, L, transform=ax.transAxes, fontsize=10, fontweight='bold', va='bottom', ha='left'); ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02); cb.set_label('fraction of cluster cells')
    fig.suptitle('Transition-gate and Cd177+ cells concentrate in one to three mutant clusters per experiment;\nAT1-gated cells occur in 8/8 top-AT2 clusters in Experiment 1 and 5/7 in Experiment 2',
                     x=0.01, y=1.02, ha='left', fontsize=8)
    f2 = FIG / 'EN_C02_cluster_gate_crosstab.png'; fig.savefig(f2, bbox_inches='tight'); plt.close(fig)

if 'EN_C03' in a.figures:
    # ---------------- EN_C03: CD177 within transition-gated cells (two eligible libraries)
    con = read_csv(T / 'EN2_5/EN5_cd177_contrasts.csv'); mat = read_csv(T / 'EN2_5/EN5_cd177_matched.csv'); grp = read_csv(T / 'EN2_5/EN5_cd177_groups.csv')
    eps = ['cycling', 'priming_associated', 'AT2_identity', 'AT1_identity', 'Itga2', 'transition_RNA', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'Tonsl', 'hypoxia_control', 'P53_RNA_control']
    epn = ['cycling (primary)', 'priming (Lcn2/Lrg1/Retnla/Ptgs1)', 'AT2 identity', 'AT1 identity', 'Itga2', 'transition RNA', 'shared module (disjoint)', 'lesion module (disjoint)', 'TNF/NF-kB response (disjoint)', 'Nfkbia', 'Tonsl', 'hypoxia control', 'p53 control']
    libs = ['GSM7890835', 'GSM7890836']; lc = {libs[0]: CAT[0], libs[1]: CAT[1]}
    fig = plt.figure(figsize=(7.6, 5.6)); gs = fig.add_gridspec(2, 2, width_ratios=[3, 2], height_ratios=[1, 1], hspace=0.55, wspace=0.45, top=0.88)
    ax = fig.add_subplot(gs[:, 0]); y = np.arange(len(eps))
    for k, g in enumerate(libs):
        c = con[(con.variant == 'primary') & (con.gsm == g) & (con.Cd177_threshold_UMI == 1) & (con.stratum == 'all transition cells') & (con.role.isin(['primary', 'secondary']))].set_index('endpoint').smd
        s2 = con[(con.variant == 'primary') & (con.gsm == g) & (con.Cd177_threshold_UMI == 2) & (con.stratum == 'all transition cells') & (con.role.isin(['primary', 'secondary']))].set_index('endpoint').smd
        mm = mat[(mat.variant == 'primary') & (mat.gsm == g) & (mat.Cd177_threshold_UMI == 1) & (mat.status == 'estimated')].set_index('endpoint').weighted_smd
        off = -0.18 if k == 0 else 0.18
        ax.scatter([c.get(e, np.nan) for e in eps], y + off, color=lc[g], s=22, zorder=3, label=f'{g} (>=1 UMI, unmatched)')
        ax.scatter([s2.get(e, np.nan) for e in eps], y + off, facecolor='none', edgecolor=lc[g], s=22, zorder=3, label=f'{g} (>=2 UMI)')
        ax.scatter([mm.get(e, np.nan) for e in eps], y + off, marker='D', color=lc[g], s=26, zorder=4, edgecolor=INK, linewidth=0.5, label=f'{g} depth x hypoxia matched')
    ax.axvline(0, color=AXIS, lw=0.8, zorder=1); ax.set_yticks(y); ax.set_yticklabels(epn); ax.invert_yaxis(); ax.set_xlabel('SMD, Cd177-detected minus Cd177-zero cells (within one library)')
    ax.set_title('Cd177 detection tracks priming and identity RNA\nin both libraries; cycling differs by library'); hh, ll = ax.get_legend_handles_labels(); fig.legend(hh, ll, loc='lower center', ncol=3, fontsize=6, bbox_to_anchor=(0.5, -0.06)); letter(ax, 'a'); ax.margins(y=0.04); ax.set_xlim(-1.7, 2.6)
    ax2 = fig.add_subplot(gs[0, 1])
    for k, g in enumerate(libs):
        r = con[(con.variant == 'primary') & (con.gsm == g) & (con.Cd177_threshold_UMI == 1) & (con.endpoint == 'cycling_markers_ge2_fraction')].iloc[0]
        ax2.bar([k - 0.18, k + 0.18], [r.mean_neg, r.mean_pos], width=0.34, color=[PAL['deemph'], lc[g]]); ax2.text(k + 0.18, r.mean_pos + 0.01, f'{r.mean_pos:.2f}', ha='center', fontsize=6); ax2.text(k - 0.18, r.mean_neg + 0.01, f'{r.mean_neg:.2f}', ha='center', fontsize=6)
    gg = grp[(grp.variant == 'primary') & (grp.Cd177_threshold_UMI == 1) & (grp.status == 'available')].set_index('gsm')
    ax2.set_xticks([0, 1]); ax2.set_xticklabels([f'{g}\nn={int(gg.loc[g].n_Cd177_neg)} / {int(gg.loc[g].n_Cd177_pos)}' for g in libs]); ax2.set_ylabel('fraction with >=2 cycling markers'); ax2.set_ylim(0, 0.65)
    ax2.set_title('Cycling fraction:\nCd177-zero (grey) vs detected'); letter(ax2, 'b')
    ax3 = fig.add_subplot(gs[1, 1])
    for k, g in enumerate(libs):
        d = json.loads(gg.loc[g].Cd177_umi_counts_in_pos); xs = np.array(sorted(int(x) for x in d)); ys = np.array([d[str(x)] for x in xs])
        ax3.step(np.r_[xs, xs[-1] + 1], np.r_[np.cumsum(ys) / ys.sum(), 1], where='post', color=lc[g], label=g)
    ax3.set_xscale('log'); ax3.set_xticks([1, 2, 5, 10, 20, 50]); ax3.set_xticklabels(['1', '2', '5', '10', '20', '50']); ax3.set_xlabel('Cd177 UMIs per detected cell'); ax3.set_ylabel('cumulative fraction'); ax3.set_title('Cd177 counts in detected cells spread without a break'); ax3.legend(loc='lower right'); letter(ax3, 'c')
    fig.suptitle('EN5: only the two 2-week mutant RFP libraries meet the 30-cell floor on both Cd177 sides', x=0.01, y=0.99, ha='left', fontsize=8)
    f3 = FIG / 'EN_C03_cd177_transition.png'; fig.savefig(f3, bbox_inches='tight'); plt.close(fig)

if 'EN_C04' in a.figures:
    # ---------------- EN_C04: Il1r1 genotype contrasts (composition and within-state)
    cc = read_csv(T / 'EN2_5/EN2_composition_contrasts.csv'); wc = read_csv(T / 'EN2_5/EN2_within_state_contrasts.csv')
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.0), gridspec_kw={'width_ratios': [1, 1.4], 'wspace': 0.55, 'bottom': 0.25})
    ax = axes[0]; groups = ['state_AT2', 'state_mixed', 'gate_transition', 'Cd177_ge1_all']; gn = ['AT2 state', 'mixed state', 'transition gate', 'Cd177 >=1 (all cells)']; y = np.arange(len(groups))
    for k, (v, mkr) in enumerate([('primary', 'o'), ('depth1000_seed20260928', 's')]):
        for j, day in enumerate(['14', '84']):
            d = cc[(cc.variant == v) & (cc.collection_day.astype(str) == day)].set_index('group'); off = (-0.25 + 0.5 * j) + (0.1 if k else -0.1)
            ax.errorbar([d.loc[g].difference_of_library_means for g in groups], y + off, xerr=[[d.loc[g].difference_of_library_means - d.loc[g].cross_library_min for g in groups], [d.loc[g].cross_library_max - d.loc[g].difference_of_library_means for g in groups]],
                        fmt=mkr, color=CAT[j], mfc=CAT[j] if k == 0 else 'white', ms=4, lw=0.8, capsize=0, label=f"{'2 wk' if day == '14' else '12 wk'}, {'raw' if k == 0 else '1,000 UMI'}")
    ax.axvline(0, color=AXIS, lw=0.8); ax.set_yticks(y); ax.set_yticklabels(gn); ax.invert_yaxis(); ax.set_xlabel('difference of library fractions, Il1r1 KO minus het\n(bar = range of the 2x2 cross-library differences)'); ax.legend(fontsize=6, loc='upper center', bbox_to_anchor=(.5, -.25), ncol=2); letter(ax, 'a'); ax.set_title('Composition')
    ax = axes[1]; eps4 = ['Cd177', 'transition_RNA', 'priming_associated', 'AT1_identity', 'AT2_identity', 'cycling', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia', 'Tonsl']; y = np.arange(len(eps4))
    for j, day in enumerate(['14', '84']):
        for k, st in enumerate(['AT2', 'mixed']):
            d = wc[(wc.variant == 'primary') & (wc.collection_day.astype(str) == day) & (wc.state == st) & (wc.status == 'estimated')].set_index('endpoint'); off = (-0.25 + 0.5 * j) + (0.1 if k else -0.1)
            xs = [d.difference_of_library_means.get(e, np.nan) for e in eps4]
            ax.errorbar(xs, y + off, xerr=[[d.difference_of_library_means.get(e, np.nan) - d.cross_library_min.get(e, np.nan) for e in eps4], [d.cross_library_max.get(e, np.nan) - d.difference_of_library_means.get(e, np.nan) for e in eps4]],
                        fmt='o' if k == 0 else 's', color=CAT[j], mfc=CAT[j] if k == 0 else 'white', ms=4, lw=0.8, capsize=0, label=f"{'2 wk' if day == '14' else '12 wk'}, within {st} state")
    ax.axvline(0, color=AXIS, lw=0.8); ax.set_yticks(y); ax.set_yticklabels(['Cd177', 'transition RNA', 'priming', 'AT1 identity', 'AT2 identity', 'cycling', 'TNF/NF-kB response', 'Nfkbia', 'Tonsl']); ax.invert_yaxis(); ax.set_xlabel('difference of library pseudobulk means, log2(CPM+1), KO minus het'); ax.legend(fontsize=6, loc='upper center', bbox_to_anchor=(.5, -.25), ncol=2); letter(ax, 'b'); ax.set_title('Within-state expression (transition state unavailable)')
    fig.suptitle('Deletion libraries have lower transition occupancy and within-state Cd177 RNA; AT1-identity contrasts are negative\nTwo libraries per genotype/time; ranges are cross-library differences, not confidence intervals; pools unknown', x=0.01, y=1.04, ha='left', fontsize=8)
    f4 = FIG / 'EN_C04_genotype_contrasts.png'; fig.savefig(f4, bbox_inches='tight'); plt.close(fig)

if 'EN_C05' in a.figures:
    # ---------------- EN_C05: simulator implementations
    cc6 = read_csv(T / 'EN6/simulation_ccdf.csv'); an = read_csv(T / 'EN6/analytic_birth_death_check.csv'); dif = read_csv(T / 'EN6/implementation_differences.csv')
    IMPL = {'literal': (INK, '-', 'literal'), 'literal_fixed_branch': (CAT[1], '--', 'fixed S-loss (CA1)'), 'gillespie': (CAT[0], ':', 'Gillespie')}
    panels = [('Red2Kras_RFP', 7), ('Red2Kras_RFP', 14), ('Red2Kras_RFP', 28), ('Red2Kras_YFP', 28), ('Confetti', 504)]
    fig, axes = plt.subplots(1, 6, figsize=(7.6, 3.1), gridspec_kw={'wspace': 0.14, 'width_ratios': [1, 1, 1, 1, 1, 1.15], 'top': 0.78, 'bottom': 0.2})
    for ax, (blk, t), L in zip(axes[:5], panels, 'abcde'):
        for impl, (col, ls, name) in IMPL.items():
            d = cc6[(cc6.block == blk) & (cc6.time_days == t) & (cc6.implementation == impl) & (cc6.seed == 20260928)]; d = d[d.ccdf_mean_P_N_gt_n > 1e-4]
            ax.plot(d.size_n, d.ccdf_mean_P_N_gt_n, color=col, ls=ls, lw=1.1, label=name)
        ax.set_xscale('log'); ax.set_yscale('log'); ax.set_ylim(1e-4, 1.1); ax.set_xticks([2, 10, 100, 1000]); ax.set_xticklabels(['2', '10', '100', '1k'])
        ks = dif[(dif.block == blk) & (dif.time_days == t) & (dif.comparison == 'literal vs literal_fixed_branch')].ks_distance_conditional_ge2.iloc[0]
        ax.set_title(f"{blk.replace('Red2Kras_', 'Kras ').replace('_', ' ')} {t // 7} wk\nKS lit. vs fixed {ks:.2f}", fontsize=6.5, pad=10); ax.text(-0.05, 1.18, L, transform=ax.transAxes, fontsize=10, fontweight='bold', va='bottom', ha='left')
        if ax is not axes[0]: ax.set_yticklabels([])
    axes[0].set_ylabel('P(N > n | N >= 2)\nmean of 100 replicates'); axes[2].set_xlabel('clone size n (cells)'); axes[0].legend(fontsize=5.5, loc='lower left', handlelength=1.6)
    ax = axes[5]; ax.scatter(an.P0_analytic, an.P0_empirical, color=CAT[2], s=18, zorder=3); ax.plot([0.3, 1], [0.3, 1], color=AXIS, lw=0.8); ax.set_xlabel('analytic P(extinct)'); ax.set_ylabel('simulated P(extinct)'); ax.set_title('Gillespie vs analytic\nbirth-death (4 settings)', fontsize=6.5, pad=10); ax.text(-0.05, 1.18, 'f', transform=ax.transAxes, fontsize=10, fontweight='bold', va='bottom', ha='left'); ax.set_xlim(0.3, 1); ax.set_ylim(0.3, 1)
    fig.suptitle("EN6: the deposited script's S-loss branch changes the Kras RFP (q=0.7) clone-size law; q=0.5 blocks are unaffected", x=0.01, y=0.99, ha='left', fontsize=8)
    f5 = FIG / 'EN_C05_simulator_implementations.png'; fig.savefig(f5, bbox_inches='tight'); plt.close(fig)

if 'EN_C06' in a.figures:
    # ---------------- EN_C06: repair transfer, unit-level pseudobulks
    pb = read_csv(T / 'EN7/EN7_pseudobulk.csv'); pb = pb[(pb.variant == 'primary') & (pb.state == 'all') & (pb.status == 'estimated')]
    eps7 = ['cycling', 'transition_RNA', 'shared_gate_cycle_stress_disjoint', 'lesion_gate_cycle_stress_disjoint', 'Itga2', 'Cd177', 'TNFA_NFKB_RNA_disjoint', 'Nfkbia']
    epn7 = ['cycling', 'transition RNA', 'shared module', 'lesion module', 'Itga2', 'Cd177', 'TNF/NF-kB', 'Nfkbia']
    fig, axes = plt.subplots(2, len(eps7), figsize=(12.4, 4.8), gridspec_kw={'hspace': 0.7, 'wspace': 0.75, 'top': 0.80, 'bottom': 0.22})
    choi_units = ['PBS_AT2_Tomato', 'Day14_AT2_Tomato', 'Day28_AT2_Tomato']
    for j, (e, n) in enumerate(zip(eps7, epn7)):
        ax = axes[0, j]; d = pb[(pb.study == 'Choi_2020') & (pb.endpoint == e)].set_index('unit').pseudobulk_mean_log2_CPM1.reindex(choi_units)
        ax.plot([0, 14, 28], d.to_numpy(), '-o', color=CAT[0], ms=4, lw=1); ax.set_xticks([0, 14, 28]); ax.set_xticklabels(['PBS', 'd14', 'd28']); ax.set_title(n, fontsize=6.5)
        ax = axes[1, j]; d = pb[(pb.study == 'Niethamer_2025') & (pb.endpoint == e) & (pb.unit_role == 'primary_unit')]
        for u, g in d.groupby('unit'): ax.scatter([int(float(g.sacrifice_day.iloc[0]))], g.pseudobulk_mean_log2_CPM1, color=CAT[1], s=14, zorder=3)
        means = d.assign(day=d.sacrifice_day.astype(float).astype(int)).groupby('day').pseudobulk_mean_log2_CPM1.mean(); ax.plot(means.index, means.to_numpy(), '-', color=CAT[1], lw=1); ax.set_xticks([0, 11, 25]); ax.set_xticklabels(['d0', 'd11', 'd25'])
    axes[0, 0].set_ylabel('Choi 2020\nlog2(CPM+1)'); axes[1, 0].set_ylabel('Niethamer 2025\nlog2(CPM+1)'); axes[0, 0].text(-.38, 1.12, 'a', transform=axes[0, 0].transAxes, fontsize=10, fontweight='bold'); axes[1, 0].text(-.38, 1.12, 'b', transform=axes[1, 0].transAxes, fontsize=10, fontweight='bold')
    fig.suptitle('Shared-module RNA peaks at the middle sampled time in both repair studies', x=0.01, ha='left', fontsize=10)
    fig.text(.01, .89, 'Choi: one deposited pseudobulk unit per condition. Niethamer: two library units per time; lines join condition means.', fontsize=8)
    fig.text(.5, .025, 'Points are deposited units, not longitudinal measurements of the same cells. Shared-module RNA is not a fate measurement.\nCd177 transition groups remain below the 30-cell floor; no biological uncertainty or state-conversion rate is estimated.', ha='center', fontsize=7)
    f6 = FIG / 'EN_C06_repair_transfer.png'; fig.savefig(f6, bbox_inches='tight'); plt.close(fig)
for f in [globals()['f' + str(int(n[-1]))] for n in a.figures]: record['figures'][f.name] = digest(f)
record['inputs'] = read_inputs
record['selected_figures'] = a.figures
record['render_details'] = dict(previous_record.get('render_details', {}))
for selected in a.figures:
    f = globals()['f' + str(int(selected[-1]))]
    record['render_details'][f.name] = {'script_sha256':digest(Path(__file__)), 'rendered_utc':record['rendered_utc']}
record['carry_forward_note'] = 'Hashes of unselected figures refer to their previous render.'
record['script_sha256'] = digest(Path(__file__))
(FIG / 'render_record.json').write_text(json.dumps(record, indent=2) + '\n'); print('figures rendered', a.figures, flush=True)
