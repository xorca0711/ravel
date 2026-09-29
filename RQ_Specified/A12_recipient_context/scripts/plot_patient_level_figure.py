"""Render the A12 patient-level panels behind the held-out summary.

A12_F03 shows the twelve paired patients themselves: the marginal relationship between the
recipient receptor index and the inflammatory response, and the held-out predictions of the
two models in the primary comparison against what was observed. Inputs are the tracked
A12_model_inputs.csv and A12_heldout_predictions.csv in
docs/roadmap_runs/2026-09-27-followthrough/.

Every plotted value is a saved column. The Pearson correlation printed in panel a is computed
from the plotted points and is descriptive at twelve patients. Panel b reports descriptive
OLS slopes of saved predictions against observations; no predictive model is refitted, and no
interval or p value is reported. Run from the repository root:

    python RQ_Specified/A12_recipient_context/scripts/plot_patient_level_figure.py
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
FT = ROOT / 'docs/roadmap_runs/2026-09-27-followthrough'
FIG = Path(__file__).resolve().parents[1] / 'figures'

ALPHA = 1.0
FLOOR = 50
UNCERTAINTY = 0.2
RECIPIENT = 'AT2'
JOINT = '#2A6B8F'
ALT = '#9FB6C4'
INK = '#222222'
GREY = '#8A8A8A'


def _style(plt):
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8,
        'axes.titlesize': 8.5, 'axes.labelsize': 8,
        'legend.fontsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': 0.8, 'axes.titlelocation': 'left', 'figure.dpi': 200,
    })


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    FIG.mkdir(exist_ok=True)
    paths = [FIG / 'A12_F03_patient_level.png', FIG / 'A12_F03_patient_level.svg']
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    assert args.overwrite or not any(p.exists() for p in paths), 'Use --overwrite to replace presentations'

    inputs = pd.read_csv(FT / 'A12_model_inputs.csv')
    preds = pd.read_csv(FT / 'A12_heldout_predictions.csv')
    frame = inputs[(inputs.recipient == RECIPIENT) & (inputs.cell_floor == FLOOR)
                   & (inputs.uncertainty == UNCERTAINTY)]
    assert len(frame) == 12, len(frame)
    held = preds[(preds.recipient == RECIPIENT) & (preds.cell_floor == FLOOR)
                 & (preds.uncertainty == UNCERTAINTY) & (preds.alpha == ALPHA)]

    _style(plt)
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.0, 3.5), layout='constrained')

    # Panel a: the marginal relationship, one point per patient.
    ax_a.axhline(0, color=GREY, linewidth=0.7, zorder=1)
    ax_a.axvline(0, color=GREY, linewidth=0.7, zorder=1)
    ax_a.scatter(frame.recipient_index, frame.response, s=38, facecolor='none',
                 edgecolor=JOINT, linewidth=1.2, zorder=3)
    r = float(np.corrcoef(frame.recipient_index, frame.response)[0, 1])
    ax_a.annotate(f'r = {r:.2f} across {len(frame)} patients\n(descriptive; no line fitted)',
                  xy=(0.03, 0.03), xycoords='axes fraction', va='bottom', fontsize=6.8, color=INK)
    ax_a.set_xlabel('Recipient receptor index\n(LUAD minus normal, score units)')
    ax_a.set_ylabel('Inflammatory response\n(LUAD minus normal, score units)')
    ax_a.set_title('Marginal association of the receptor index\nwith the inflammatory response')
    ax_a.margins(0.12)

    # Panel b: observed against held-out predicted, both models in the primary comparison.
    limits = []
    for model, colour, label in (('alternative', ALT, 'Source + TNF'),
                                 ('joint', JOINT, 'Source + TNF + recipient index')):
        sub = held[held.model == model]
        ax_b.scatter(sub.observed, sub.predicted, s=34, facecolor='none', edgecolor=colour,
                     linewidth=1.2, zorder=3, label=label)
        limits += [sub.observed.min(), sub.observed.max(), sub.predicted.min(), sub.predicted.max()]
    lo, hi = min(limits), max(limits)
    pad = 0.09 * (hi - lo)
    ax_b.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color=GREY, linewidth=0.8,
              linestyle='--', zorder=1)
    ax_b.annotate('perfect prediction', xy=(hi, hi), xytext=(-6, -14), textcoords='offset points',
                  ha='right', fontsize=6.3, color=GREY, rotation=45)
    ax_b.set_xlim(lo - pad, hi + pad)
    ax_b.set_ylim(lo - pad, hi + pad)
    ax_b.set_aspect('equal')
    ax_b.set_xlabel('Observed response')
    ax_b.set_ylabel('Held-out prediction')
    # Verified against A12_heldout_predictions.csv: both predicted ranges are WIDER than the
    # observed range, so the earlier "both models compress the range" wording was false.
    _obs = held[held.model == 'joint'].observed.to_numpy()
    _obs_w = float(_obs.max() - _obs.min())
    _sl, _wid = {}, {}
    for _m in ('alternative', 'joint'):
        _s = held[held.model == _m]
        _sl[_m] = float(np.polyfit(_s.observed.to_numpy(), _s.predicted.to_numpy(), 1)[0])
        _wid[_m] = float(_s.predicted.max() - _s.predicted.min())
    _n_wider = sum(1 for _m in _sl if _wid[_m] > _obs_w)
    _tail = ('both predicted ranges wider than observed' if _n_wider == 2
             else f'{_n_wider} of 2 predicted ranges wider than observed')
    ax_b.set_title(f'Predicted-versus-observed OLS slopes:\n'
                   f'{_sl["alternative"]:.2f} (alternative), {_sl["joint"]:.2f} (joint)')
    ax_b.annotate(_tail, xy=(0.03, 0.03), xycoords='axes fraction', fontsize=6.4, color=GREY)
    ax_b.legend(frameon=False, loc='upper left', fontsize=6.5, handletextpad=0.4)

    for ax, letter in ((ax_a, 'a'), (ax_b, 'b')):
        ax.text(-0.22, 1.06, letter, transform=ax.transAxes, fontweight='bold',
                fontsize=10, va='bottom', ha='right')
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A12 patient-level'})
    plt.close(fig)

    for path in paths:
        if path.suffix == '.svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n', encoding='utf-8')

    used = {
        'docs/roadmap_runs/2026-09-27-followthrough/A12_model_inputs.csv': FT / 'A12_model_inputs.csv',
        'docs/roadmap_runs/2026-09-27-followthrough/A12_heldout_predictions.csv': FT / 'A12_heldout_predictions.csv',
    }
    record = {
        'scope': 'Patient-level values behind the A12 held-out summary. No predictive model is refitted '
                 'or rescored. The panel-a correlation and panel-b descriptive OLS slopes are computed '
                 'from saved points. The correlation is '
                 'descriptive at twelve patients, with no line, interval or p value. Predictions are '
                 'the saved leave-one-patient-out values at the primary settings (alpha=1, 50-cell '
                 'floor, confidence 0.2) for the AT2 recipient.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'panel_a_pearson_r': round(r, 6),
        'predicted_versus_observed_slopes': _sl,
        'prediction_range_widths': _wid,
        'observed_range_width': _obs_w,
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in used.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    }
    (FIG / 'figure_run_patient_level.json').write_text(json.dumps(record, indent=2) + '\n',
                                                       encoding='utf-8')
    print(f'Rendered A12_F03_patient_level (panel a r = {r:.4f})')


if __name__ == '__main__':
    main()
