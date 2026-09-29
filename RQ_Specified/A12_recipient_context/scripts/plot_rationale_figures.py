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
    panels = [
        ('A12, AT2 recipient', 'A12', 'AT2', MODEL_ORDER),
        ('A12, alveolar fibroblast recipient', 'A12', 'Alveolar fibroblasts', MODEL_ORDER),
        ('A13, fibroblast programme', 'A13', None, A13_MODEL_ORDER),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 7.2), layout='constrained',
                             gridspec_kw={'height_ratios': [1, 1.35]})
    checks = {}
    for col, (title, pilot, recipient, order) in enumerate(panels):
        def primary(frame):
            sel = frame[(frame.alpha == PRIMARY_ALPHA) & (frame.cell_floor == PRIMARY_FLOOR)
                        & (frame.uncertainty == PRIMARY_UNCERTAINTY)]
            if recipient is not None:
                sel = sel[sel.recipient == recipient]
            return sel
        frame = primary(pd.read_csv(FT / f'{pilot}_model_metrics.csv'))
        frame = frame[frame.status == 'fit'].set_index('model')
        held = primary(pd.read_csv(FT / f'{pilot}_heldout_predictions.csv'))
        assert not held.duplicated(['model', 'patient']).any()
        for model in order:
            pred = held[held.model == model]
            assert len(pred) == int(frame.loc[model, 'n'])
            assert np.allclose((pred.observed - pred.predicted)**2, pred.squared_error)
            assert np.isclose(np.sqrt(pred.squared_error.mean()), frame.loc[model, 'RMSE'],
                              rtol=0, atol=1e-9)
        ax = axes[0, col]
        baseline = float(frame.loc['mean', 'RMSE'])
        x = np.arange(len(order))
        for xi, model in zip(x, order):
            value = float(frame.loc[model, 'RMSE'])
            colour = BASELINE if model == 'mean' else (FOCAL if model == 'joint' else MUTED)
            ax.plot([xi, xi], [baseline, value], color=colour, linewidth=1, alpha=0.6)
            ax.scatter(xi, value, s=34, color=colour, zorder=3)
        ax.axhline(baseline, color=BASELINE, linewidth=0.9, linestyle=':')
        delta = float(frame.loc['joint', 'RMSE'] - frame.loc['alternative', 'RMSE'])
        ax.set_xticks(x, [LABELS[m] for m in order], rotation=90, fontsize=6.5)
        ax.set_title(f'{title}\nJoint minus alternative RMSE: {delta:+.4f}', pad=12)
        ax.margins(y=0.20)
        ax.set_ylabel('Held-out RMSE' if col == 0 else '')
        alt = held[held.model == 'alternative'].set_index('patient').sort_index()
        joint = held[held.model == 'joint'].set_index('patient').sort_index()
        assert alt.index.equals(joint.index)
        assert np.allclose(alt.observed, joint.observed)
        ea, ej = np.sqrt(alt.squared_error), np.sqrt(joint.squared_error)
        better = int((ej < ea).sum())
        ax = axes[1, col]
        y = np.arange(len(alt))
        ax.hlines(y, ea, ej, color='#CCCCCC', linewidth=1, zorder=1)
        ax.scatter(ea, y, s=25, facecolor='white', edgecolor=BASELINE,
                   label='Source + TNF (alternative)', zorder=3)
        ax.scatter(ej, y, s=25, color=FOCAL, label='Joint (added term)', zorder=4)
        ax.set_yticks(y, alt.index.astype(str), fontsize=6.5)
        ax.invert_yaxis()
        ax.set_xlim(left=0)
        ax.set_xlabel('Absolute held-out error (lower is better)')
        ax.set_ylabel('Patient' if col == 0 else '')
        ax.set_title(f'Joint lowers error in {better}/{len(alt)} patients', pad=10)
        checks[title] = {'patients': len(alt), 'joint_lower_error': better,
                         'joint_minus_alternative_RMSE': delta}
    handles, labels = axes[1, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower center', ncol=2, frameon=False)
    fig.suptitle('Saved primary comparisons: alpha = 1, 50-cell floor, uncertainty = 0.2\n'
                 'Top: aggregate error; dotted line = training mean. Bottom: the same 12 held-out patients.\n'
                 'LUAD-minus-normal score units; overlapping LOPO training sets; no fold-based intervals.',
                 fontsize=10)
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A12/A13 rationale'})
    plt.close(fig)
    return checks


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
    ax.annotate('half of the recovered counts', xy=(0.02, 50), xycoords=('axes fraction', 'data'),
                xytext=(2, 3), textcoords='offset points', fontsize=6, color=BASELINE)
    ax.set_xticks(range(len(HISTOLOGY_ORDER)))
    ax.set_xticklabels([f'{h}\nn = {int((frame.histology == h).sum())}' for h in HISTOLOGY_ORDER])
    ax.set_ylabel('IL1B counts in cells without a confident\nlabel (% of patient-histology counts)')
    ax.set_ylim(0, 100)
    ax.set_title('The median patient in every histology carries most recovered IL1B RNA\n'
                 'in cells the reference cannot confidently label '
                 f'({below}/{len(frame)} patient-histology observations below half)')
    ax.annotate(f'{frame.patient.nunique()} patients recur across histologies; bars: interquartile range', xy=(0.98, 0.03), xycoords='axes fraction',
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    assert args.overwrite or not any(p.exists() for p in one + two), 'Use --overwrite to replace presentations'

    _style(plt)
    checks = figure_one(plt, np, pd, one)
    figure_two(plt, np, pd, two)

    for path in one + two:
        if path.suffix == '.svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n', encoding='utf-8')

    inputs = {
        **{f'docs/roadmap_runs/2026-09-27-followthrough/{pilot}_heldout_predictions.csv': FT / f'{pilot}_heldout_predictions.csv' for pilot in ('A12', 'A13')},
        'docs/roadmap_runs/2026-09-27-followthrough/A12_model_metrics.csv': FT / 'A12_model_metrics.csv',
        'docs/roadmap_runs/2026-09-27-followthrough/A13_model_metrics.csv': FT / 'A13_model_metrics.csv',
        'Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_sources/IL1B_source_fractions.csv':
            SRC / 'IL1B_source_fractions.csv',
    }
    record = {
        'scope': 'Plots tracked values and derived absolute errors; no predictive model fit or rescoring. Both '
                 'pilots are exploratory on reused data; the ladders are held-out RMSE at the '
                 'primary settings (alpha=1, 50-cell floor, confidence 0.2) and carry no interval '
                 'because leave-one-patient-out fold losses are dependent. Figure 2 shows an RNA '
                 'count allocation among recovered cells, not a secretion fraction and not a '
                 'tissue-composition correction.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'point_offsets': 'Deterministic evenly spaced offsets, -0.13 to +0.13, ordered by value.',
        'paired_error_checks': checks,
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in one + two},
    }
    (FIG / 'figure_run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print('Rendered A12_F01_heldout_model_ladder and A12_F02_il1b_source_allocation')


if __name__ == '__main__':
    main()
