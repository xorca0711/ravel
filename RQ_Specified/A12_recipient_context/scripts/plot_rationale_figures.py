"""Render the A12/A13 rationale panels from tracked tables; no fit, no rescoring.

Figure 1 plots the held-out model ladder of both exploratory pilots against their own
training-mean baselines, from the tracked metrics tables in
docs/roadmap_runs/2026-09-27-followthrough/. The primary comparison in each pilot is the
joint model against the source-plus-TNF alternative on identical held-out patients.

Figure 2 plots the per-patient fraction of observed IL1B counts carried by cells without a
confident finest-level label, by histology, from the A12-S1 source table in
Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_sources/.

Both figures plot saved table columns only. Run from the repository root:

    python RQ_Specified/A12_recipient_context/scripts/plot_rationale_figures.py
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
FT = ROOT / 'docs/roadmap_runs/2026-09-27-followthrough'
SRC = ROOT / 'Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_sources'
FIG = Path(__file__).resolve().parents[1] / 'figures'

PRIMARY_ALPHA = 1.0
PRIMARY_FLOOR = 50
PRIMARY_UNCERTAINTY = 0.2
MODEL_ORDER = ['mean', 'source', 'recipient', 'alternative', 'joint']
A13_MODEL_ORDER = ['mean', 'source', 'source_fibroblast', 'alternative', 'joint']
LABELS = {
    'mean': 'Training mean\n(no predictors)',
    'source': 'Source ligand\n+ mixture',
    'recipient': '+ recipient\nreceptor index',
    'source_fibroblast': '+ fibroblast\nTGF-beta programme',
    'alternative': '+ TNF\n(alternative ligand)',
    'joint': 'Joint\n(TNF + added term)',
}
FOCAL = '#2A6B8F'
MUTED = '#9FB6C4'
WORSE = '#B4553C'
BASELINE = '#5A5A5A'
HISTOLOGY_ORDER = ['normal', 'AAH', 'AIS', 'MIA', 'LUAD']


def _style(plt):
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8,
        'axes.titlesize': 8, 'axes.labelsize': 8,
        'legend.fontsize': 7, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.titlelocation': 'left', 'figure.dpi': 170,
    })


def figure_one(plt, np, pd, paths):
    a12 = pd.read_csv(FT / 'A12_model_metrics.csv')
    a13 = pd.read_csv(FT / 'A13_model_metrics.csv')

    def primary(frame, **extra):
        sel = frame[(frame.alpha == PRIMARY_ALPHA) & (frame.cell_floor == PRIMARY_FLOOR)
                    & (frame.uncertainty == PRIMARY_UNCERTAINTY) & (frame.status == 'fit')]
        for key, value in extra.items():
            sel = sel[sel[key] == value]
        return sel.set_index('model')

    panels = [
        ('A12, AT2 recipient', primary(a12, recipient='AT2'), MODEL_ORDER,
         'the recipient index lowers held-out error'),
        ('A12, alveolar fibroblast recipient', primary(a12, recipient='Alveolar fibroblasts'),
         MODEL_ORDER, 'no gain over source + TNF'),
        ('A13, fibroblast programme', primary(a13), A13_MODEL_ORDER,
         'no model beats the training mean'),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.6), layout='constrained')
    for ax, (title, frame, order, verdict) in zip(axes, panels):
        present = [m for m in order if m in frame.index]
        baseline = float(frame.loc['mean', 'RMSE'])
        n = int(frame.loc['mean', 'n'])
        x = np.arange(len(present))
        for xi, model in zip(x, present):
            value = float(frame.loc[model, 'RMSE'])
            colour = BASELINE if model == 'mean' else (FOCAL if model == 'joint' else MUTED)
            ax.plot([xi, xi], [baseline, value], color=colour, linewidth=1.0, alpha=0.6, zorder=1)
            ax.scatter(xi, value, s=34, color=colour, zorder=3)
        ax.axhline(baseline, color=BASELINE, linewidth=0.9, linestyle=':', zorder=0)
        if 'alternative' in present and 'joint' in present:
            ia, ij = present.index('alternative'), present.index('joint')
            va, vj = float(frame.loc['alternative', 'RMSE']), float(frame.loc['joint', 'RMSE'])
            better = vj < va
            ax.annotate('', xy=(ij, vj), xytext=(ia, va),
                        arrowprops=dict(arrowstyle='->', color=FOCAL if better else WORSE,
                                        linewidth=1.1, shrinkA=7, shrinkB=7))
            ax.annotate(f'{vj - va:+.4f}', xy=((ia + ij) / 2.0, (va + vj) / 2.0),
                        xytext=(0, 10 if better else -14), textcoords='offset points',
                        ha='center', fontsize=6.5, color=FOCAL if better else WORSE)
        ax.set_xticks(x)
        ax.set_xticklabels([LABELS[m] for m in present], fontsize=6)
        ax.tick_params(axis='x', rotation=90)
        ax.set_title(f'{title}\n{verdict}', fontsize=7.5, pad=14)
        ax.margins(y=0.18)
        ax.annotate(f'n = {n} paired patients', xy=(0.97, 0.97), xycoords='axes fraction',
                    ha='right', va='top', fontsize=6, color=BASELINE)
    axes[0].set_ylabel('Held-out RMSE\n(paired LUAD-normal score units)')
    axes[0].annotate('lower = better; dotted line = training mean', xy=(0.03, 0.03),
                     xycoords='axes fraction', fontsize=6, color=BASELINE)
    for ax, letter in zip(axes, 'abc'):
        ax.text(-0.10, 1.19, letter, transform=ax.transAxes, fontweight='bold',
                fontsize=9, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A12/A13 rationale'})
    plt.close(fig)


def figure_two(plt, np, pd, paths):
    frame = pd.read_csv(SRC / 'IL1B_source_fractions.csv')
    frame = frame[(frame.uncertainty == PRIMARY_UNCERTAINTY) & (frame.broad == 'Unassigned')]
    fig, ax = plt.subplots(figsize=(6.2, 3.3), layout='constrained')
    below = 0
    for xi, histology in enumerate(HISTOLOGY_ORDER):
        values = 100.0 * frame[frame.histology == histology].fraction_of_observed_IL1B_counts.to_numpy()
        values = np.sort(values)
        below += int((values < 50).sum())
        # Deterministic symmetric offsets: at n = 4-23 per group a random jitter adds no
        # information and is not reproducible across renders.
        off = np.linspace(-0.13, 0.13, values.size) if values.size > 1 else np.zeros(1)
        ax.scatter(xi + off, values, s=20, facecolor='none', edgecolor=FOCAL,
                   linewidth=0.9, zorder=2)
        q1, median, q3 = (float(np.percentile(values, q)) for q in (25, 50, 75))
        ax.plot([xi - 0.30, xi - 0.30], [q1, q3], color=FOCAL, linewidth=1.2,
                solid_capstyle='butt', zorder=3)
        ax.plot([xi - 0.26, xi + 0.26], [median, median], color=FOCAL, linewidth=2.0, zorder=3)
        # Place the median label away from the 50% reference line.
        ax.annotate(f'{median:.1f}%', xy=(xi + 0.30, median),
                    xytext=(0, 7 if abs(median - 50) < 6 else 0), textcoords='offset points',
                    fontsize=6.5, va='center', color=FOCAL)
    ax.axhline(50, color=BASELINE, linewidth=0.8, linestyle=':')
    ax.annotate('half of the recovered counts', xy=(0.02, 0.5), xycoords=('axes fraction', 'data'),
                xytext=(2, 3), textcoords='offset points', fontsize=6, color=BASELINE)
    ax.set_xticks(range(len(HISTOLOGY_ORDER)))
    ax.set_xticklabels([f'{h}\nn = {int((frame.histology == h).sum())}' for h in HISTOLOGY_ORDER])
    ax.set_ylabel('IL1B counts in cells without a confident\nlabel (% of that patient\u2019s counts)')
    ax.set_ylim(0, 100)
    ax.set_title('The median patient in every histology carries most recovered IL1B RNA\n'
                 'in cells the reference cannot confidently label '
                 f'({below} of {len(frame)} patients fall below half)')
    ax.annotate('bars: interquartile range', xy=(0.98, 0.03), xycoords='axes fraction',
                ha='right', fontsize=6, color=BASELINE)
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A12-S1 source allocation'})
    plt.close(fig)


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    FIG.mkdir(exist_ok=True)
    one = [FIG / 'A12_F01_heldout_model_ladder.png', FIG / 'A12_F01_heldout_model_ladder.svg']
    two = [FIG / 'A12_F02_il1b_source_allocation.png', FIG / 'A12_F02_il1b_source_allocation.svg']
    assert not any(p.exists() for p in one + two), 'Refusing to overwrite figures'

    _style(plt)
    figure_one(plt, np, pd, one)
    figure_two(plt, np, pd, two)

    inputs = {
        'docs/roadmap_runs/2026-09-27-followthrough/A12_model_metrics.csv': FT / 'A12_model_metrics.csv',
        'docs/roadmap_runs/2026-09-27-followthrough/A13_model_metrics.csv': FT / 'A13_model_metrics.csv',
        'Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_sources/IL1B_source_fractions.csv':
            SRC / 'IL1B_source_fractions.csv',
    }
    record = {
        'scope': 'Plots tracked table columns only. No fit, no rescoring, no new estimate. Both '
                 'pilots are exploratory on reused data; the ladders are held-out RMSE at the '
                 'primary settings (alpha=1, 50-cell floor, confidence 0.2) and carry no interval '
                 'because leave-one-patient-out fold losses are dependent. Figure 2 shows an RNA '
                 'count allocation among recovered cells, not a secretion fraction and not a '
                 'tissue-composition correction.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'jitter_seed': 20260928,
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in one + two},
    }
    (FIG / 'figure_run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Rendered A12_F01_heldout_model_ladder and A12_F02_il1b_source_allocation')


if __name__ == '__main__':
    main()
