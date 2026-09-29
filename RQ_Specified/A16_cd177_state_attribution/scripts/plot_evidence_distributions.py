"""Render the A16 evidence in the conventional form for each result type.

Each panel uses the display its analysis type is normally reported in, rather than a generic
dot plot:

A16_F03 - the C3 detection-matched gene null as small-multiple histograms of the control-gene
statistic with a vertical line at Cd177's own value, which is the standard rendering of a
resampling or matched null (grey null, line at the observed statistic). One facet per
descriptive entry, shared axis, ordered by control count.

A16_F04 - per-cell scores as violins with an inner box and median, the standard single-cell
display for comparing a signature score across cell groups (Seurat VlnPlot / scanpy
sc.pl.violin), rather than jittered points alone.

A16_F05 - matching balance as a Love plot: absolute standardized mean difference per covariate
before and after matching, ordered by the pre-matching value, with the conventional 0.1
reference. This is the named standard diagnostic for covariate balance after matching
(Love 2004); the 0.1 line is conventional rather than universal and is drawn as a reference,
not a pass mark.

Inputs are tracked tables: tables/stage1/A16_C3_control_gene_detail.csv and
A16_C3_matched_gene_null.csv, and correction_20260928/tables/corrected_c1/{cell_outcomes,
matched_edges,effects,PC_balance}.csv. Every plotted value is a saved column, except the
per-positive-cell matched differences in A16_F04a, which are recomputed from the saved edge
list and saved per-cell scores exactly as the archived verifier does; the script asserts their
mean equals the reported matched_raw to 1e-12 before plotting. Run from the repository root:

    python RQ_Specified/A16_cd177_state_attribution/scripts/plot_evidence_distributions.py
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
S1 = HERE / 'tables/stage1'
C1 = HERE / 'correction_20260928/tables/corrected_c1'
FIG = HERE / 'figures/revision_20260929'

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
OVERLAPS = {}
GREY = '#8A8A8A'
PALE = '#C9D6DE'
PALE_DARK = '#AFC3CE'
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


def _overlap_report(fig, matplotlib, np):
    """Geometric text-collision check (figure-style 9.1). Returns a list of colliding pairs."""
    renderer = fig.canvas.get_renderer()
    texts = [(t, t.get_window_extent(renderer)) for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip() and t.get_visible()]
    ticklabels = {ax: set(ax.get_xticklabels(which='both') + ax.get_yticklabels(which='both'))
                  for ax in fig.axes}
    pairs = []
    for i, (a, ba) in enumerate(texts):
        for b, bb in texts[i + 1:]:
            if ba.overlaps(bb):
                pairs.append((a.get_text()[:28], b.get_text()[:28]))
    for ax in fig.axes:
        for spine in ax.spines.values():
            if not spine.get_visible():
                continue
            bs = spine.get_window_extent(renderer)
            for t, bt in texts:
                if bt.overlaps(bs) and t not in ticklabels.get(ax, set()):
                    pairs.append((t.get_text()[:28], 'spine'))
        for coll in ax.collections:
            try:
                if not coll.get_visible():
                    continue
                try:
                    offsets = coll.get_offsets()
                except Exception:
                    continue
                sizes = np.atleast_1d(np.asarray(coll.get_sizes(), dtype=float))
                if sizes.size == 0:
                    sizes = np.array([26.0])
                offsets = np.asarray(np.atleast_2d(offsets), dtype=float)
                if offsets.shape[-1] != 2:
                    continue
                for j, (ox, oy) in enumerate(offsets):
                    if not np.isfinite([ox, oy]).all():
                        continue
                    px, py = ax.transData.transform((ox, oy))
                    r = 0.5 * float(np.sqrt(sizes[j % sizes.size])) + 1.0
                    bm = matplotlib.transforms.Bbox.from_bounds(px - r, py - r, 2 * r, 2 * r)
                    for t, bt in texts:
                        if bt.overlaps(bm) and t not in ticklabels.get(ax, set()):
                            pairs.append((t.get_text()[:28], 'marker'))
            except Exception:
                continue
        for line in ax.lines:
            if not line.get_visible():
                continue
            bl = line.get_window_extent(renderer)
            if bl.width > 2 and bl.height > 2:
                continue
            for t, bt in texts:
                if bt.overlaps(bl) and t not in ticklabels.get(ax, set()):
                    pairs.append((t.get_text()[:28], 'reference line'))
    return pairs

def figure_three(plt, np, pd, paths):
    """C3 null as small-multiple histograms with a line at the observed statistic."""
    detail = pd.read_csv(S1 / 'A16_C3_control_gene_detail.csv')
    null = pd.read_csv(S1 / 'A16_C3_matched_gene_null.csv')
    cd = null[null.endpoint == PRIMARY].set_index('unit')
    order = cd.sort_values('n_control_genes_used', ascending=False).index.tolist()

    values = detail.smd_priming.dropna()
    lo = min(values.min(), cd.cd177_smd.min()) - 0.15
    hi = max(values.max(), cd.cd177_smd.max()) + 0.15
    bins = np.linspace(lo, hi, 34)

    fig, axes = plt.subplots(3, 3, figsize=(7.4, 5.4), sharex=True, layout='constrained')
    for ax, unit in zip(axes.ravel(), order):
        controls = detail[detail.unit == unit].smd_priming.dropna().to_numpy()
        n_used = int(cd.loc[unit, 'n_control_genes_used'])
        above_floor = n_used >= CONTROL_FLOOR
        if controls.size:
            ax.hist(controls, bins=bins, color=PALE if above_floor else '#E2E2E2',
                    edgecolor=GREY, linewidth=0.35, zorder=2)
        observed = cd.loc[unit, 'cd177_smd']
        if pd.notna(observed):
            ax.axvline(observed, color=CD177, linewidth=1.5, zorder=4)
        exceed = cd.loc[unit, 'frac_control_ge_cd177']
        note = f'{n_used} control gene' + ('s' if n_used != 1 else '')
        if pd.notna(exceed):
            note += f'\n{exceed:.0%} reach Cd177'
        counts, _ = np.histogram(controls, bins=bins) if controls.size else (np.array([0]), None)
        ax.set_ylim(0, max(counts.max(), 1) * 1.42)
        mid = 0.5 * (bins[0] + bins[-1])
        right = pd.notna(observed) and observed < mid
        ax.annotate(note, xy=(0.98 if right else 0.02, 0.97), xycoords='axes fraction',
                    ha='right' if right else 'left', va='top',
                    fontsize=6.2, color=INK if above_floor else GREY)
        ax.set_title(f'{UNIT_LABEL[unit]}' + ('' if above_floor else '  (<40 controls)'),
                     fontsize=7.2, color=INK if above_floor else GREY)
        ax.tick_params(labelsize=6.2)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
    for ax in axes.ravel()[len(order):]:
        ax.set_visible(False)
    for ax in axes[-1]:
        ax.set_xlabel('Priming SMD of a matched\ncontrol gene', fontsize=7)
    fig.suptitle('The two entries with at least 40 controls place Cd177 differently',
                 fontsize=9.5, fontweight='semibold', x=0.01, ha='left')
    fig.supxlabel('Grey: priming effect of each control gene matched to Cd177 on detection and '
                  'expression. Red: Cd177\u2019s own effect. Only exp1 sub 10 (500 genes) and\n'
                  'exp2 sub 12 (284) clear the 40-gene floor. Cd177 sits at the 86th percentile '
                  'of the first null and above every gene in the second. The remaining seven\n'
                  'panels have coarser reference sets; the floor does not establish power or biological replication.',
                  fontsize=6.6, color=GREY, x=0.01, ha='left')
    fig.canvas.draw()
    OVERLAPS['figure_three'] = _overlap_report(fig, plt.matplotlib, np)
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 evidence distributions'})
    plt.close(fig)


def _violin(ax, plt, np, datasets, positions, colours):
    """Violin with an inner box and median, the single-cell convention."""
    parts = ax.violinplot(datasets, positions=positions, widths=0.72,
                          showextrema=False, showmedians=False)
    for body, colour in zip(parts['bodies'], colours):
        body.set_facecolor(colour)
        body.set_edgecolor(colour)
        body.set_alpha(0.32)
        body.set_linewidth(0.7)
    box = ax.boxplot(datasets, positions=positions, widths=0.13,
                     showfliers=False, patch_artist=True, medianprops=dict(color='white',
                     linewidth=1.3), whiskerprops=dict(linewidth=0.8),
                     capprops=dict(linewidth=0.8))
    for patch, colour in zip(box['boxes'], colours):
        patch.set_facecolor(colour)
        patch.set_edgecolor(colour)
        patch.set_linewidth(0.7)
    for element in ('whiskers', 'caps'):
        for artist in box[element]:
            artist.set_color(GREY)


def figure_four(plt, np, pd, paths):
    """Per-cell scores as violins with inner boxes."""
    cells = pd.read_csv(C1 / 'cell_outcomes.csv')
    edges = pd.read_csv(C1 / 'matched_edges.csv')
    effects = pd.read_csv(C1 / 'effects.csv')
    score = cells.set_index(['library', 'barcode'])[PRIMARY]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.4, 3.9), layout='constrained')

    differences, control_means, positives = {}, {}, {}
    for library in LIBRARIES:
        edge = edges[(edges.library == library) & (edges.k == K_PRIMARY)]
        control_mean = (edge.assign(value=[score.loc[(library, b)] for b in edge.negative_barcode])
                        .groupby('positive_barcode').value.mean())
        positive = pd.Series({b: score.loc[(library, b)] for b in control_mean.index})
        diff = (positive - control_mean).to_numpy()
        reported = float(effects[(effects.library == library) & (effects.k == K_PRIMARY)
                                 & (effects.endpoint == PRIMARY)].matched_raw.iloc[0])
        assert abs(diff.mean() - reported) < 1e-12, (library, diff.mean(), reported)
        differences[library] = (diff, reported)
        control_means[library] = control_mean.to_numpy()
        positives[library] = positive.to_numpy()

    data = [differences[lib][0] for lib in LIBRARIES]
    colours = [LIB_COLOUR[lib] for lib in LIBRARIES]
    _violin(ax_a, plt, np, data, [0, 1], colours)
    ax_a.axhline(0, color=INK, linewidth=0.8, zorder=1)
    span = max(d.max() for d in data) - min(d.min() for d in data)
    ax_a.set_ylim(min(d.min() for d in data) - 0.06 * span,
                  max(d.max() for d in data) + 0.42 * span)
    for xi, library in enumerate(LIBRARIES):
        diff, reported = differences[library]
        ax_a.scatter([xi], [reported], marker='D', s=26, color=LIB_COLOUR[library],
                     edgecolor='white', linewidth=0.6, zorder=6)
        ax_a.annotate(f'mean {reported:.3f}\n{(diff > 0).mean():.0%} above zero\n'
                      f'n = {diff.size} cells', xy=(xi, 0.99),
                      xycoords=('data', 'axes fraction'), xytext=(0, -2),
                      textcoords='offset points', ha='center', va='top', fontsize=6.4,
                      color=LIB_COLOUR[library])
    ax_a.set_xticks([0, 1])
    ax_a.set_xticklabels(LIBRARIES, fontsize=7)
    ax_a.set_ylabel('Priming score, positive cell minus\nits matched controls (score units)')
    ax_a.set_title('Positive-minus-control differences vary:\n'
                   'about one in five differences is below zero', fontsize=8.2)
    ax_a.set_xlim(-0.65, 1.65)

    library = LIBRARIES[0]
    groups = [('All negative\ncells', cells[(cells.library == library) & (~cells.positive)][PRIMARY].to_numpy(), '#9BB3C0'),
              ('Control means\n(one/positive cell)', control_means[library], GREY),
              ('Positive\ncells', positives[library], LIB_COLOUR[library])]
    _violin(ax_b, plt, np, [g[1] for g in groups], [0, 1, 2], [g[2] for g in groups])
    for xi, (_, vals, colour) in enumerate(groups):
        ax_b.annotate(f'median {np.median(vals):.2f}\nn = {vals.size}',
                      xy=(xi, 1.0), xycoords=('data', 'axes fraction'), xytext=(0, -4),
                      textcoords='offset points', ha='center', va='top', fontsize=6.4,
                      color=INK if xi == 0 else colour)
    ax_b.set_xticks([0, 1, 2])
    ax_b.set_xticklabels([g[0] for g in groups], fontsize=7)
    ax_b.set_ylabel('Priming-associated score,\nmean log1p(CP10k)')
    ax_b.set_title('Matched-control means are closer to positives\n'
                   'than the full negative pool (GSM7890835)', fontsize=8.2)
    top = max(v.max() for _, v, _ in groups)
    ax_b.set_ylim(-0.12, top * 1.26)

    for ax, letter in ((ax_a, 'a'), (ax_b, 'b')):
        ax.text(-0.19, 1.05, letter, transform=ax.transAxes, fontweight='bold',
                fontsize=10, va='bottom', ha='right')
    fig.supxlabel('Cell-level descriptions in two libraries; controls can be reused. Each middle value is a control mean, not a single cell.', fontsize=6.4)
    fig.canvas.draw()
    OVERLAPS['figure_four'] = _overlap_report(fig, plt.matplotlib, np)
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 evidence distributions'})
    plt.close(fig)


def figure_five(plt, np, pd, paths):
    """Love plot: |SMD| per covariate before and after matching, the standard balance display."""
    balance = pd.read_csv(C1 / 'PC_balance.csv')
    balance = balance[balance.k == K_PRIMARY]
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.6), sharex=True, layout='constrained',
                             gridspec_kw={'wspace': 0.16})
    for ax, library in zip(axes, LIBRARIES):
        frame = balance[balance.library == library].copy()
        frame['before'] = frame.standardized_difference_before.abs()
        frame['after'] = frame.standardized_difference_after.abs()
        frame = frame.sort_values('before')
        y = np.arange(len(frame))
        colour = LIB_COLOUR[library]
        worsened = (frame.after > frame.before).to_numpy()
        ax.hlines(y, frame.after, frame.before, color=GREY, linewidth=0.7, zorder=1)
        ax.scatter(frame.before, y, s=26, facecolor='none', edgecolor=colour,
                   linewidth=1.0, zorder=3, label='Before matching')
        ax.scatter(frame.after[~worsened], y[~worsened], s=26, color=colour, zorder=4,
                   label='After matching, improved')
        ax.scatter(frame.after[worsened], y[worsened], s=34, color=CD177, marker='X',
                   zorder=5, label='After matching, worse')
        ax.axvline(0.1, color=INK, linewidth=0.8, linestyle='--', zorder=2)
        ax.set_yticks(y)
        ax.set_yticklabels([f'PC{int(v)}' for v in frame.PC], fontsize=6.2)
        ax.set_xlabel('Absolute standardized mean difference')
        ax.set_xticks([0.0, 0.5, 1.0, 1.5])
        top = frame.loc[frame.after.idxmax()]
        ax.annotate(f'largest residual {top.after:.2f}',
                    xy=(max(top.after, top.before), float(y[list(frame.PC).index(top.PC)])),
                    xytext=(12, 0), textcoords='offset points',
                    fontsize=6.4, color=INK, va='center', ha='left')
        ax.set_title(f'{library}\n{int((~worsened).sum())} of 20 improved, '
                     f'{int(worsened.sum())} worse, {int((frame.after > 0.1).sum())} still above 0.1',
                     fontsize=7.4)
    axes[1].legend(frameon=False, loc='lower right', fontsize=6.4, handletextpad=0.4)
    fig.supxlabel('One row per component of the library\u2019s local expression space. PC1, the '
                  'leading local expression axis, is less imbalanced but remains above 0.1 in both\n'
                  'libraries; crosses mark components with increased imbalance. Dashed line: the '
                  'matching literature\u2019s conventional 0.1 reference, not a mark adopted here.',
                  fontsize=6.6, color=GREY, x=0.01, ha='left')
    fig.suptitle('The matched comparison is better balanced, but not position-free',
                 fontsize=9.5, fontweight='semibold', x=0.01, ha='left')
    fig.canvas.draw()
    OVERLAPS['figure_five'] = _overlap_report(fig, plt.matplotlib, np)
    for path in paths:
        fig.savefig(path, metadata={'Creator': 'scRNA_seq A16 balance'})
    plt.close(fig)


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    FIG.mkdir(parents=True, exist_ok=True)
    three = [FIG / 'A16_F03_c3_null_histograms.png', FIG / 'A16_F03_c3_null_histograms.svg']
    four = [FIG / 'A16_F04_percell_score_violins.png', FIG / 'A16_F04_percell_score_violins.svg']
    five = [FIG / 'A16_F05_matching_balance_loveplot.png',
            FIG / 'A16_F05_matching_balance_loveplot.svg']
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    assert args.overwrite or not any(p.exists() for p in three + four + five), 'Use --overwrite for presentation revisions'

    _style(plt)
    figure_three(plt, np, pd, three)
    figure_four(plt, np, pd, four)
    figure_five(plt, np, pd, five)

    for path in three + four + five:
        if path.suffix == '.svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n', encoding='utf-8')

    inputs = {
        'tables/stage1/A16_C3_control_gene_detail.csv': S1 / 'A16_C3_control_gene_detail.csv',
        'tables/stage1/A16_C3_matched_gene_null.csv': S1 / 'A16_C3_matched_gene_null.csv',
        'tables/stage1/run_record.json': S1 / 'run_record.json',
        'correction_20260928/tables/corrected_c1/cell_outcomes.csv': C1 / 'cell_outcomes.csv',
        'correction_20260928/tables/corrected_c1/matched_edges.csv': C1 / 'matched_edges.csv',
        'correction_20260928/tables/corrected_c1/effects.csv': C1 / 'effects.csv',
        'correction_20260928/tables/corrected_c1/PC_balance.csv': C1 / 'PC_balance.csv',
    }
    record = {
        'scope': 'Distributions behind already-reported A16 summaries. No fit, no rescoring, no new '
                 'estimate. Per-positive-cell matched differences in F04a are recomputed from the '
                 'saved edge list and saved per-cell scores, as the archived verifier does, and the '
                 'script asserts their mean equals the reported matched_raw to 1e-12. Arm B entries '
                 'in F03 pool libraries within an experiment and are not within-state contrasts. '
                 'Control-gene histograms show the SELECTED controls, not the full candidate '
                 'universe; the 40-control display floor is not a power assessment. F04 compares individual '
                 'scores with per-positive-cell means of controls, which can be reused; these are '
                 'cell-level descriptions, not independent animal replicates. The 0.1 line in the Love plot is the conventional balance reference '
                 'from the matching literature, not a threshold this analysis adopted.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'jitter_seed': 20260928,
        'text_collisions': {k: len(v) for k, v in OVERLAPS.items()},
        'inputs': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
        'outputs': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in three + four + five},
    }
    (FIG / 'figure_run_distributions.json').write_text(json.dumps(record, indent=2) + '\n',
                                                       encoding='utf-8')
    for name, pairs in OVERLAPS.items():
        print(f'{name}: {len(pairs)} text collisions' + (f' -> {pairs}' if pairs else ''))
    print('Rendered A16_F03, A16_F04 and A16_F05')


if __name__ == '__main__':
    main()
