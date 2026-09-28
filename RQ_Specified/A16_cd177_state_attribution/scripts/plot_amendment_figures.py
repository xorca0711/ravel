"""Render the two A16 amendment panels from tracked tables; no fit, no rescoring.

Figure 1 plots the corrected C1 comparison (correction_20260928/tables/corrected_c1/):
per-endpoint marginal and matched raw differences, the predeclared k sensitivity for the
primary endpoint, and residual per-PC standardized imbalance after matching.

Figure 2 plots the C3 detection-matched gene null (tables/stage1/): matched control genes
available per unit against the 40-gene readability floor, and Cd177's position in each
unit's control distribution, with underpowered units drawn as open markers.

Both figures read tracked CSV files only. Nothing here estimates a new quantity: every
plotted value is a column of a saved table. Run from the repository root:

    python RQ_Specified/A16_cd177_state_attribution/scripts/plot_amendment_figures.py
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
C1 = HERE / 'correction_20260928/tables/corrected_c1'
S1 = HERE / 'tables/stage1'
FIG = HERE / 'figures'

LIBRARIES = ['GSM7890835', 'GSM7890836']
LIBRARY_COLOR = {'GSM7890835': '#3B769D', 'GSM7890836': '#B86A42'}
PRIMARY = 'priming_associated'
ENDPOINT_LABEL = {
    'priming_associated': 'Priming-associated RNA',
    'AT2_identity': 'AT2 identity',
    'AT1_identity': 'AT1 identity',
    'Itga2': 'Itga2',
    'cycling': 'Cycling RNA',
    'shared_gate_cycle_stress_disjoint': 'Shared remodelling',
    'lesion_gate_cycle_stress_disjoint': 'Lesion remodelling',
}
UNIT_LABEL = {
    'GSM7890835': 'GSM7890835',
    'GSM7890836': 'GSM7890836',
    'exp1_sub_r1.0=10': 'exp1 sub 10',
    'exp1_sub_r1.0=12': 'exp1 sub 12',
    'exp1_sub_r1.0=16': 'exp1 sub 16',
    'exp1_sub_r1.0=17': 'exp1 sub 17',
    'exp1_sub_r1.0=18': 'exp1 sub 18',
    'exp2_sub_r1.0=10': 'exp2 sub 10',
    'exp2_sub_r1.0=12': 'exp2 sub 12',
}
CONTROL_FLOOR = 40
META_GREY = '#5A5A5A'


def _style(plt):
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8,
        'axes.titlesize': 8, 'axes.labelsize': 8,
        'legend.fontsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.titlelocation': 'left', 'figure.dpi': 170,
    })


def figure_one(plt, np, pd, paths):
    effects = pd.read_csv(C1 / 'effects.csv')
    balance = pd.read_csv(C1 / 'PC_balance.csv')
    assert set(effects.status) == {'assessed'}, 'unexpected effect status in tracked table'

    fig = plt.figure(figsize=(7.2, 5.4), layout='constrained')
    grid = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0])
    ax_a = fig.add_subplot(grid[0, :])
    ax_b = fig.add_subplot(grid[1, 0])
    ax_c = fig.add_subplot(grid[1, 1])

    # Panel A: marginal -> matched raw difference, k = 10, per endpoint and library.
    k10 = effects[effects.k == 10]
    order = list(ENDPOINT_LABEL)
    for row_index, endpoint in enumerate(order):
        for sign, library in zip((0.16, -0.16), LIBRARIES):
            record = k10[(k10.library == library) & (k10.endpoint == endpoint)]
            assert len(record) == 1, (library, endpoint)
            record = record.iloc[0]
            y = row_index + sign
            colour = LIBRARY_COLOR[library]
            ax_a.plot([record.marginal_raw, record.matched_raw], [y, y],
                      color=colour, linewidth=1.0, alpha=0.55, zorder=1,
                      solid_capstyle='butt')
            ax_a.scatter(record.marginal_raw, y, s=26, facecolor='white',
                         edgecolor=colour, linewidth=1.1, zorder=3,
                         label='Marginal' if row_index == 0 and sign > 0 else None)
            ax_a.scatter(record.matched_raw, y, s=26, color=colour, zorder=3,
                         label='Matched, k = 10' if row_index == 0 and sign > 0 else None)
    ax_a.axvline(0, color='black', linewidth=0.8, zorder=0)
    ax_a.set_yticks(range(len(order)))
    ax_a.set_yticklabels([ENDPOINT_LABEL[e] for e in order])
    ax_a.invert_yaxis()
    ax_a.set_xlabel('Cd177-positive minus Cd177-negative, score units (log1p CP10k)')
    ax_a.set_title('Matching on local position removes most of each marginal difference;\n'
                   'the priming difference is the one that stays clearly positive')
    ax_a.margins(x=0.10, y=0.04)
    handles, labels = ax_a.get_legend_handles_labels()
    library_handles = [plt.Line2D([], [], color=LIBRARY_COLOR[lib], marker='o',
                                  linestyle='-', markersize=4.5, label=lib)
                       for lib in LIBRARIES]
    ax_a.legend(handles=handles + library_handles, frameon=False, loc='lower right',
                ncol=2, handletextpad=0.5, columnspacing=1.2)
    for spine in ('top', 'right'):
        ax_a.spines[spine].set_visible(False)

    # Panel B: predeclared k sensitivity, primary endpoint only.
    primary = effects[effects.endpoint == PRIMARY].sort_values('k')
    ks = sorted(primary.k.unique())
    for library in LIBRARIES:
        frame = primary[primary.library == library]
        ax_b.plot(frame.k, frame.matched_raw, marker='o', markersize=4,
                  color=LIBRARY_COLOR[library], linewidth=1.2)
        marginal = frame.marginal_raw.iloc[0]
        ax_b.axhline(marginal, color=LIBRARY_COLOR[library], linewidth=0.9,
                     linestyle=':', alpha=0.9)
        ax_b.annotate(f'marginal {marginal:.2f}', xy=(ks[-1], marginal),
                      xytext=(-2, 2), textcoords='offset points', ha='right',
                      va='bottom', fontsize=6, color=LIBRARY_COLOR[library])
    ax_b.axhline(0, color='black', linewidth=0.8)
    ax_b.set_xticks(ks)
    ax_b.set_xlabel('Matched neighbours per positive cell (k)')
    ax_b.set_ylabel('Matched raw difference')
    ax_b.set_title('Attenuation is not a choice of k')
    ax_b.margins(x=0.12, y=0.10)

    # Panel C: residual per-PC imbalance at k = 10.
    k10_balance = balance[balance.k == 10]
    for library in LIBRARIES:
        frame = k10_balance[k10_balance.library == library]
        before = frame.standardized_difference_before.abs()
        after = frame.standardized_difference_after.abs()
        ax_c.scatter(before, after, s=18, facecolor='none',
                     edgecolor=LIBRARY_COLOR[library], linewidth=1.0)
        worst = frame.loc[after.idxmax()]
        ax_c.annotate(f'PC{int(worst.PC)}: {abs(worst.standardized_difference_after):.2f}',
                      xy=(abs(worst.standardized_difference_before),
                          abs(worst.standardized_difference_after)),
                      xytext=(4, 2), textcoords='offset points', fontsize=6,
                      color=LIBRARY_COLOR[library])
    limit = max(k10_balance.standardized_difference_before.abs().max(), 1.0) * 1.12
    ax_c.plot([0, limit], [0, limit], color=META_GREY, linewidth=0.8, linestyle='--')
    ax_c.annotate('no improvement', xy=(limit * 0.62, limit * 0.62), xytext=(0, 4),
                  textcoords='offset points', fontsize=6, color=META_GREY, rotation=45)
    ax_c.set_xlim(0, limit)
    ax_c.set_ylim(0, limit)
    ax_c.set_xlabel('|standardized difference| before')
    ax_c.set_ylabel('after matching')
    ax_c.set_title('Residual positional imbalance stays substantial')

    for axis, letter in ((ax_a, 'a'), (ax_b, 'b'), (ax_c, 'c')):
        axis.text(-0.02 if axis is ax_a else -0.20, 1.02, letter, transform=axis.transAxes,
                  fontweight='bold', fontsize=9, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 amendment'})
    plt.close(fig)


def figure_two(plt, np, pd, paths):
    null = pd.read_csv(S1 / 'A16_C3_matched_gene_null.csv')
    primary = null[(null.endpoint == PRIMARY)].copy()
    assert len(primary) == 9, f'expected 9 descriptive entries, found {len(primary)}'
    primary['arm_label'] = np.where(primary.arm.str.startswith('A_'),
                                    'Arm A: transitional gate, single library',
                                    'Arm B: FU_C subcluster, libraries pooled')
    primary = primary.sort_values(['arm', 'n_control_genes_used'], ascending=[True, False])
    primary['label'] = primary.unit.map(UNIT_LABEL)
    powered = primary.n_control_genes_used >= CONTROL_FLOOR

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.2, 3.1), layout='constrained')
    y = np.arange(len(primary))[::-1]

    # Panel A: matched control genes available per unit.
    for offset, (_, row) in zip(y, primary.iterrows()):
        colour = '#3B769D' if row.arm.startswith('A_') else '#397F6D'
        filled = row.n_control_genes_used >= CONTROL_FLOOR
        ax_a.plot([1, row.n_control_genes_used], [offset, offset], color=colour,
                  linewidth=1.0, alpha=0.55)
        ax_a.scatter(row.n_control_genes_used, offset, s=28, color=colour if filled else 'white',
                     edgecolor=colour, linewidth=1.1, zorder=3)
        ax_a.annotate(f'{int(row.n_control_genes_used)}',
                      xy=(row.n_control_genes_used, offset), xytext=(5, 0),
                      textcoords='offset points', va='center', fontsize=6, color=colour)
    ax_a.axvline(CONTROL_FLOOR, color=META_GREY, linewidth=0.9, linestyle=':')
    ax_a.annotate(f'{CONTROL_FLOOR}-gene floor', xy=(CONTROL_FLOOR, y.max()),
                  xytext=(3, -2), textcoords='offset points', fontsize=6, color=META_GREY)
    ax_a.set_xscale('log')
    ax_a.set_xlim(0.8, 1400)
    ax_a.set_xticks([1, 10, 100, 1000])
    ax_a.set_xticklabels(['1', '10', '100', '1k'])
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(primary.label)
    ax_a.set_xlabel('Matched control genes used (log scale)')
    ax_a.set_title(f'{int((~powered).sum())} of 9 entries hold fewer than\n{CONTROL_FLOOR} detection-matched control genes')
    ax_a.margins(y=0.06)

    # Panel B: Cd177's position in each unit's control distribution.
    for offset, (_, row) in zip(y, primary.iterrows()):
        colour = '#3B769D' if row.arm.startswith('A_') else '#397F6D'
        filled = row.n_control_genes_used >= CONTROL_FLOOR
        fraction = 100.0 * row.frac_control_ge_cd177
        ax_b.plot([0, fraction], [offset, offset], color=colour, linewidth=1.0, alpha=0.55)
        ax_b.scatter(fraction, offset, s=28, color=colour if filled else 'white',
                     edgecolor=colour, linewidth=1.1, zorder=3)
        ax_b.annotate(f'{fraction:.1f}%', xy=(fraction, offset), xytext=(5, 0),
                      textcoords='offset points', va='center', fontsize=6, color=colour)
    ax_b.set_xlim(-3, 118)
    ax_b.set_yticks(y)
    ax_b.set_yticklabels([])
    ax_b.set_xlabel('Control genes reaching Cd177\u2019s effect (%)')
    ax_b.set_title('Exceptional in 4 entries, unexceptional in the\nbest-powered one: the null cannot decide')
    ax_b.margins(y=0.06)

    legend = [
        plt.Line2D([], [], marker='o', color='#3B769D', linestyle='', markersize=5,
                   label='Arm A: transitional gate, per library'),
        plt.Line2D([], [], marker='o', color='#397F6D', linestyle='', markersize=5,
                   label='Arm B: FU_C subcluster, pooled (not a within-state contrast)'),
        plt.Line2D([], [], marker='o', color=META_GREY, markerfacecolor='white', linestyle='',
                   markersize=5, label=f'open marker: fewer than {CONTROL_FLOOR} controls'),
    ]
    fig.legend(handles=legend, frameon=False, loc='outside lower center', ncol=1,
               fontsize=6.5, handletextpad=0.5)
    for axis, letter in ((ax_a, 'a'), (ax_b, 'b')):
        axis.text(-0.30 if axis is ax_a else -0.02, 1.02, letter, transform=axis.transAxes,
                  fontweight='bold', fontsize=9, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 amendment'})
    plt.close(fig)


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    FIG.mkdir(exist_ok=True)
    one = [FIG / 'A16_F01_corrected_c1_attenuation.png', FIG / 'A16_F01_corrected_c1_attenuation.svg']
    two = [FIG / 'A16_F02_c3_specificity_power.png', FIG / 'A16_F02_c3_specificity_power.svg']
    assert not any(p.exists() for p in one + two), 'Refusing to overwrite figures'

    _style(plt)
    figure_one(plt, np, pd, one)
    figure_two(plt, np, pd, two)

    inputs = {
        'correction_20260928/tables/corrected_c1/effects.csv': C1 / 'effects.csv',
        'correction_20260928/tables/corrected_c1/PC_balance.csv': C1 / 'PC_balance.csv',
        'tables/stage1/A16_C3_matched_gene_null.csv': S1 / 'A16_C3_matched_gene_null.csv',
    }
    record = {
        'scope': 'Plots tracked table columns only. No fit, no rescoring, no new estimate. '
                 'Arm B entries pool libraries within an experiment and are not within-state '
                 'contrasts; open markers flag entries below the 40-control readability floor.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest()
                   for name, path in inputs.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in one + two},
    }
    (FIG / 'figure_run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Rendered A16_F01_corrected_c1_attenuation and A16_F02_c3_specificity_power')


if __name__ == '__main__':
    main()
