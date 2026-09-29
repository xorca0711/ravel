"""Render the A16 evidence distributions that the summary panels only asserted.

A16_F03 shows the C3 detection-matched gene null as a distribution per descriptive entry,
with Cd177's own effect marked, and the matching space that explains why control genes are
scarce. Inputs: tables/stage1/A16_C3_control_gene_detail.csv (one row per selected control
gene per unit) and A16_C3_matched_gene_null.csv (Cd177's own values), with the matching bands
read from tables/stage1/run_record.json.

A16_F04 shows the corrected-C1 estimate as the distribution of per-cell matched differences
behind it, and the priming distributions of positives, their matched controls and the full
negative pool. Inputs: correction_20260928/tables/corrected_c1/{cell_outcomes,matched_edges,
effects}.csv.

Every plotted value is a saved column, except the per-positive-cell matched differences in
A16_F04a, which are recomputed from the saved edge list and saved per-cell scores exactly as
the archived verifier does; the script asserts their mean equals the reported matched_raw to
1e-12 before plotting. Run from the repository root:

    python RQ_Specified/A16_cd177_state_attribution/scripts/plot_evidence_distributions.py
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
S1 = HERE / 'tables/stage1'
C1 = HERE / 'correction_20260928/tables/corrected_c1'
FIG = HERE / 'figures'

PRIMARY = 'priming_associated'
CONTROL_FLOOR = 40
K_PRIMARY = 10
LIBRARIES = ['GSM7890835', 'GSM7890836']
LIB_COLOUR = {'GSM7890835': '#2A6B8F', 'GSM7890836': '#B4673C'}
UNIT_LABEL = {
    'GSM7890835': 'GSM7890835', 'GSM7890836': 'GSM7890836',
    'exp1_sub_r1.0=10': 'exp1 sub 10', 'exp1_sub_r1.0=12': 'exp1 sub 12',
    'exp1_sub_r1.0=16': 'exp1 sub 16', 'exp1_sub_r1.0=17': 'exp1 sub 17',
    'exp1_sub_r1.0=18': 'exp1 sub 18', 'exp2_sub_r1.0=10': 'exp2 sub 10',
    'exp2_sub_r1.0=12': 'exp2 sub 12',
}
INK = '#222222'
GREY = '#8A8A8A'
PALE = '#C9D6DE'
CD177 = '#B4553C'


def _style(plt):
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8,
        'axes.titlesize': 8.5, 'axes.labelsize': 8,
        'legend.fontsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': 0.8, 'xtick.major.width': 0.8, 'ytick.major.width': 0.8,
        'axes.titlelocation': 'left', 'figure.dpi': 200,
    })


def figure_three(plt, np, pd, paths):
    detail = pd.read_csv(S1 / 'A16_C3_control_gene_detail.csv')
    null = pd.read_csv(S1 / 'A16_C3_matched_gene_null.csv')
    record = json.loads((S1 / 'run_record.json').read_text(encoding='utf-8'))
    bands = record['matching_bands']
    det_band, exp_band = bands['detection_rate_relative'], bands['mean_log1p_cp10k_relative']

    cd = null[null.endpoint == PRIMARY].set_index('unit')
    order = cd.sort_values('n_control_genes_used', ascending=True).index.tolist()

    fig = plt.figure(figsize=(7.6, 4.6), layout='constrained')
    grid = fig.add_gridspec(1, 2, width_ratios=[1.45, 1.0])
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])

    rng = np.random.default_rng(20260928)
    for y, unit in enumerate(order):
        controls = detail[detail.unit == unit].smd_priming.dropna().to_numpy()
        n_used = int(cd.loc[unit, 'n_control_genes_used'])
        powered = n_used >= CONTROL_FLOOR
        if controls.size:
            ax_a.scatter(controls, y + rng.uniform(-0.17, 0.17, controls.size), s=7,
                         color=PALE if powered else GREY, alpha=0.75, linewidth=0, zorder=2)
            lo, hi = np.percentile(controls, [5, 95])
            ax_a.plot([lo, hi], [y, y], color=GREY, linewidth=0.9, zorder=3)
            ax_a.plot([np.median(controls)] * 2, [y - 0.22, y + 0.22], color=INK,
                      linewidth=1.4, zorder=4)
        value = cd.loc[unit, 'cd177_smd']
        if pd.notna(value):
            ax_a.scatter(value, y, marker='D', s=30, color=CD177, zorder=6,
                         edgecolor='white', linewidth=0.6)
        ax_a.annotate(f'{n_used}', xy=(1.0, y), xycoords=('axes fraction', 'data'),
                      xytext=(4, 0), textcoords='offset points', va='center',
                      fontsize=6.5, color=INK if powered else GREY,
                      annotation_clip=False)
    ax_a.axvline(0, color=INK, linewidth=0.8, zorder=1)
    ax_a.set_yticks(range(len(order)))
    ax_a.set_yticklabels([UNIT_LABEL[u] for u in order])
    ax_a.set_xlabel('Priming-associated standardized mean difference,\nCd177-positive minus negative')
    ax_a.set_title('Only two entries hold a null dense enough\nto place Cd177 in it')
    ax_a.annotate('control genes', xy=(1.0, 1.0), xycoords='axes fraction', xytext=(4, 8),
                  textcoords='offset points', fontsize=6.5, color=INK, annotation_clip=False)
    ax_a.margins(y=0.07)
    ax_a.set_xlim(left=min(-1.2, detail.smd_priming.min() - 0.1))
    ax_a.annotate('Cd177', xy=(cd.loc[order[-1], 'cd177_smd'], len(order) - 1),
                  xytext=(6, 10), textcoords='offset points', fontsize=7, color=CD177,
                  arrowprops=dict(arrowstyle='-', color=CD177, linewidth=0.7))
    ax_a.annotate('median and 5th-95th percentile\nof the selected control genes',
                  xy=(0.03, 0.03), xycoords='axes fraction', fontsize=6.3, color=GREY)

    shown = ['exp1_sub_r1.0=10', 'GSM7890835']
    for unit, marker in zip(shown, ['o', 's']):
        controls = detail[detail.unit == unit]
        ax_b.scatter(100 * controls.detection_rate, controls.mean_log1p_cp10k, s=9,
                     marker=marker, facecolor='none', edgecolor=LIB_COLOUR[LIBRARIES[0]]
                     if unit == shown[0] else LIB_COLOUR[LIBRARIES[1]], linewidth=0.7,
                     alpha=0.8, zorder=2,
                     label=f'{UNIT_LABEL[unit]}  ({len(controls)} controls)')
        x0 = 100 * float(cd.loc[unit, 'cd177_detection_rate'])
        y0 = float(cd.loc[unit, 'cd177_mean_log1p_cp10k'])
        colour = LIB_COLOUR[LIBRARIES[0]] if unit == shown[0] else LIB_COLOUR[LIBRARIES[1]]
        ax_b.add_patch(plt.Rectangle((x0 * (1 - det_band), y0 * (1 - exp_band)),
                                     x0 * 2 * det_band, y0 * 2 * exp_band,
                                     fill=False, edgecolor=colour, linewidth=0.9,
                                     linestyle='--', zorder=3))
        ax_b.scatter(x0, y0, marker='D', s=34, color=CD177, edgecolor='white',
                     linewidth=0.6, zorder=5)
    ax_b.set_xlabel('Detection rate in the entry (% of cells)')
    ax_b.set_ylabel('Mean log1p(CP10k) where detected')
    ax_b.set_title('Few genes match Cd177 on detection\nand expression together')
    ax_b.legend(frameon=False, loc='upper left', fontsize=6.5, handletextpad=0.4)
    ax_b.annotate('dashed box: the frozen matching band\n(detection \u00b125%, expression \u00b135%, relative)',
                  xy=(0.03, 0.03), xycoords='axes fraction', fontsize=6.3, color=GREY)
    ax_b.margins(0.10)

    for ax, letter in ((ax_a, 'a'), (ax_b, 'b')):
        ax.text(-0.16 if ax is ax_a else -0.20, 1.05, letter, transform=ax.transAxes,
                fontweight='bold', fontsize=10, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 evidence distributions'})
    plt.close(fig)


def figure_four(plt, np, pd, paths):
    cells = pd.read_csv(C1 / 'cell_outcomes.csv')
    edges = pd.read_csv(C1 / 'matched_edges.csv')
    effects = pd.read_csv(C1 / 'effects.csv')
    score = cells.set_index(['library', 'barcode'])[PRIMARY]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.6, 3.6), layout='constrained')
    rng = np.random.default_rng(20260928)

    for xi, library in enumerate(LIBRARIES):
        edge = edges[(edges.library == library) & (edges.k == K_PRIMARY)]
        control_mean = (edge.assign(value=[score.loc[(library, b)] for b in edge.negative_barcode])
                        .groupby('positive_barcode').value.mean())
        positive = pd.Series({b: score.loc[(library, b)] for b in control_mean.index})
        differences = (positive - control_mean).to_numpy()
        reported = float(effects[(effects.library == library) & (effects.k == K_PRIMARY)
                                 & (effects.endpoint == PRIMARY)].matched_raw.iloc[0])
        assert abs(differences.mean() - reported) < 1e-12, (library, differences.mean(), reported)

        colour = LIB_COLOUR[library]
        ax_a.scatter(xi + rng.uniform(-0.15, 0.15, differences.size), differences, s=11,
                     facecolor='none', edgecolor=colour, linewidth=0.7, alpha=0.85, zorder=2)
        ax_a.plot([xi - 0.30, xi + 0.30], [reported] * 2, color=colour, linewidth=2.2, zorder=4)
        ax_a.annotate(f'mean {reported:.3f}', xy=(xi + 0.33, reported), fontsize=6.8,
                      va='center', color=colour)
        above = float((differences > 0).mean())
        ax_a.annotate(f'{above:.0%} above zero\nn = {differences.size} cells',
                      xy=(xi, 0.02), xycoords=('data', 'axes fraction'), xytext=(0, 0),
                      textcoords='offset points', ha='center', va='bottom', fontsize=6.5,
                      color=colour)

        if xi == 0:
            all_negative = cells[(cells.library == library) & (~cells.positive)][PRIMARY].to_numpy()
            groups = [('All Cd177-negative\ncells in the entry', all_negative, PALE),
                      ('The matched controls\nactually used', control_mean.to_numpy(), GREY),
                      ('Cd177-positive cells', positive.to_numpy(), colour)]
            for yi, (label, values, shade) in enumerate(groups):
                ax_b.scatter(values, yi + rng.uniform(-0.16, 0.16, values.size), s=8,
                             color=shade, alpha=0.7, linewidth=0, zorder=2)
                ax_b.plot([np.median(values)] * 2, [yi - 0.26, yi + 0.26], color=INK,
                          linewidth=1.5, zorder=4)
                ax_b.annotate(f'median {np.median(values):.2f}  (n = {values.size})',
                              xy=(1.0, yi), xycoords=('axes fraction', 'data'),
                              xytext=(-4, 12), textcoords='offset points', ha='right',
                              fontsize=6.5, color=INK)
            ax_b.set_yticks(range(len(groups)))
            ax_b.set_yticklabels([g[0] for g in groups])

    ax_a.axhline(0, color=INK, linewidth=0.8, zorder=1)
    ax_a.set_xticks(range(len(LIBRARIES)))
    ax_a.set_xticklabels(LIBRARIES)
    ax_a.set_ylabel('Priming score, positive cell minus\nits matched controls (score units)')
    ax_a.set_title('The estimate averages cells that disagree:\nabout one in five runs the other way')
    ax_a.margins(x=0.22, y=0.10)

    ax_b.set_xlabel('Priming-associated score, mean log1p(CP10k)')
    ax_b.set_title('Matching pulls the comparison group\ntoward the positives')
    ax_b.margins(y=0.22)
    ax_b.annotate('GSM7890835 only', xy=(0.02, 0.03), xycoords='axes fraction',
                  fontsize=6.5, color=GREY)

    for ax, letter in ((ax_a, 'a'), (ax_b, 'b')):
        ax.text(-0.18 if ax is ax_a else -0.30, 1.05, letter, transform=ax.transAxes,
                fontweight='bold', fontsize=10, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 evidence distributions'})
    plt.close(fig)


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    FIG.mkdir(exist_ok=True)
    three = [FIG / 'A16_F03_c3_null_distributions.png', FIG / 'A16_F03_c3_null_distributions.svg']
    four = [FIG / 'A16_F04_matched_difference_distributions.png',
            FIG / 'A16_F04_matched_difference_distributions.svg']
    assert not any(p.exists() for p in three + four), 'Refusing to overwrite figures'

    _style(plt)
    figure_three(plt, np, pd, three)
    figure_four(plt, np, pd, four)

    inputs = {
        'tables/stage1/A16_C3_control_gene_detail.csv': S1 / 'A16_C3_control_gene_detail.csv',
        'tables/stage1/A16_C3_matched_gene_null.csv': S1 / 'A16_C3_matched_gene_null.csv',
        'tables/stage1/run_record.json': S1 / 'run_record.json',
        'correction_20260928/tables/corrected_c1/cell_outcomes.csv': C1 / 'cell_outcomes.csv',
        'correction_20260928/tables/corrected_c1/matched_edges.csv': C1 / 'matched_edges.csv',
        'correction_20260928/tables/corrected_c1/effects.csv': C1 / 'effects.csv',
    }
    record = {
        'scope': 'Distributions behind already-reported A16 summaries. No fit, no rescoring, no new '
                 'estimate. Per-positive-cell matched differences in F04a are recomputed from the '
                 'saved edge list and saved per-cell scores, as the archived verifier does, and the '
                 'script asserts their mean equals the reported matched_raw to 1e-12. Arm B entries '
                 'in F03 pool libraries within an experiment and are not within-state contrasts. '
                 'Control-gene strips show the SELECTED controls, not the full candidate universe.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'jitter_seed': 20260928,
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in three + four},
    }
    (FIG / 'figure_run_distributions.json').write_text(json.dumps(record, indent=2) + '\n',
                                                       encoding='utf-8')
    print('Rendered A16_F03_c3_null_distributions and A16_F04_matched_difference_distributions')


if __name__ == '__main__':
    main()
