"""Measured S4 figures from governed numerical outputs; no inferred pairing."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

BLUE, ORANGE, GREY = '#0072B2', '#D55E00', '#777777'


def save(fig, output, name):
    fig.savefig(output / (name + '.png'), dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output / (name + '.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def scatter_density(ax, x, y, xlabel, ylabel, title, identity=True):
    if not len(x):
        ax.text(.5, .5, 'No qualified genes', transform=ax.transAxes, ha='center'); return
    span = max(float(np.max(np.abs(x))), float(np.max(np.abs(y))), .5) * 1.04
    ax.hexbin(x, y, gridsize=55, mincnt=1, bins='log', cmap='cividis', extent=(-span, span, -span, span))
    if identity: ax.plot([-span, span], [-span, span], '--', color=GREY, linewidth=.8)
    ax.axhline(0, color=GREY, linewidth=.5); ax.axvline(0, color=GREY, linewidth=.5)
    ax.set(xlim=(-span, span), ylim=(-span, span), xlabel=xlabel, ylabel=ylabel, title=title)
    ax.set_aspect('equal', adjustable='box')


def plot_all(output, effects, mor, qc, correlations, markers, cases, summary):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.titlesize': 10,
                         'axes.labelsize': 9, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
                         'pdf.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False})
    labels = qc.short_label.tolist()
    colors = [GREY if role == 'control' else BLUE for role in qc.role]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), layout='constrained')
    fig.suptitle('S4 library and exposed marker QC: 12 libraries, two per group\nB0 = D30 baseline; W6/W12 = hours after wounding; C/H = control/prior history', fontsize=13)
    ax = axes[0, 0]
    ax.bar(labels, qc.gene_count_total / 1e6, color=colors)
    ax.set(title='A  Deposited gene-count totals', ylabel='Sum of gene counts (millions)')
    ax.tick_params(axis='x', rotation=65)
    ax = axes[0, 1]
    x = np.arange(12)
    ax.scatter(x - .07, qc.mor_size_factor, color=BLUE, label='Joint MOR', s=24)
    ax.scatter(x + .07, qc.total_count_size_factor, color=ORANGE, marker='s', label='Joint total count', s=22)
    ax.axhline(1, color=GREY, linewidth=.6, linestyle=':')
    ax.set(xticks=x, xticklabels=labels, ylabel='Factor (geometric mean = 1)', title='B  Common 12-library normalization')
    ax.tick_params(axis='x', rotation=65); ax.legend(frameon=False, fontsize=8)
    ax = axes[1, 0]
    groups, marker_labels = [], []
    for (name, gene), rows in markers.groupby(['requested_name', 'gene_id'], sort=False):
        ordered = rows.set_index('gsm').reindex(qc.gsm)
        groups.append(np.log2(ordered.cpm.to_numpy(dtype=float) + 1))
        marker_labels.append(name + (' [missing]' if gene == 'NA' else ''))
    z = np.asarray(groups)
    shown = ax.imshow(np.ma.masked_invalid(z), aspect='auto', cmap='cividis', vmin=0)
    ax.set(xticks=x, xticklabels=labels, yticks=range(len(marker_labels)), yticklabels=marker_labels,
           title='C  Prespecified markers; no sex assignment/exclusion')
    ax.tick_params(axis='x', rotation=65)
    fig.colorbar(shown, ax=ax, label='log2(CPM + 1)', shrink=.8)
    ax = axes[1, 1]
    shown = ax.imshow(correlations, cmap='cividis', norm=Normalize(vmin=min(float(np.nanmin(correlations)), .999), vmax=1))
    ax.set(xticks=x, xticklabels=labels, yticks=x, yticklabels=labels,
           title='D  Pearson log2(MOR + 1) profile correlation\nGlobal expression-qualified union')
    ax.tick_params(axis='x', rotation=65)
    fig.colorbar(shown, ax=ax, shrink=.8)
    save(fig, output, 'fig01_sample_marker_qc')

    fig, axes = plt.subplots(2, 3, figsize=(15, 9.8), layout='constrained')
    fig.suptitle('S4 relative RNA contrasts: post-wound history difference minus baseline offset\nFinite-library description; shared platform does not establish matched pools or equal compartments', fontsize=13)
    for col, phase in enumerate(['W6', 'W12']):
        f = effects.loc[effects[f'{phase}_union_qualified']]
        scatter_density(axes[0, col], f.B0_log2_effect_mor, f[f'{phase}_log2_effect_mor'],
                        'Baseline H/C log2 effect', f'{phase} H/C log2 effect',
                        f'{"AB"[col]}  {phase} components: union n = {len(f):,}')
        scatter_density(axes[1, col + 1], f[f'{phase}_adjusted_mor'], f[f'{phase}_adjusted_total'],
                        'Joint MOR adjusted effect', 'Joint total-count adjusted effect',
                        f'{"EF"[col]}  {phase} normalization sensitivity')
    f = effects.loc[effects.global_union_qualified]
    scatter_density(axes[0, 2], f.W6_adjusted_mor, f.W12_adjusted_mor,
                    'W6 adjusted log2 effect', 'W12 adjusted log2 effect', f'C  Cross-time profiles: global union n = {len(f):,}')
    profile = summary['cross_time']['global_union']
    def label(value): return 'NA' if value is None else f'{value:.3f}'
    axes[0, 2].text(.03, .98, f'Pearson r: unadjusted {label(profile["pearson_unadjusted"])}\nadjusted {label(profile["pearson_adjusted"])}\nShared baseline can induce correlation',
                    transform=axes[0, 2].transAxes, va='top', fontsize=7,
                    bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': .85})
    ax = axes[1, 0]
    for phase, color in [('W6', BLUE), ('W12', ORANGE)]:
        for flag, style, caption in [('union_qualified', '-', 'union'), ('both_qualified', '--', 'baseline intersection')]:
            v = np.sort(np.abs(effects.loc[effects[f'{phase}_{flag}'], f'{phase}_adjusted_mor'].to_numpy()))
            if len(v): ax.plot(v, np.arange(1, len(v) + 1) / len(v), color=color, linestyle=style, label=f'{phase} {caption} ({len(v):,})')
    ax.set(xlabel='Absolute adjusted log2 effect', ylabel='Fraction of qualified genes', title='D  Expression-qualification sensitivity', ylim=(0, 1.02))
    ax.legend(frameon=False, fontsize=7, loc='lower right')
    save(fig, output, 'fig02_recall_effects')

    fig, axes = plt.subplots(3, 2, figsize=(13, 11), layout='constrained')
    fig.suptitle('Selected S4 examples: all libraries on the common normalization scale\nDots = libraries; bars = transformed count-scale means; no paired trajectories or biological classes', fontsize=13)
    gene_index = {gene: i for i, gene in enumerate(effects.gene_id)}
    for ax in axes.flat: ax.set_visible(False)
    for _, row in cases.iterrows():
        ax = axes.flat[int(row.plot_slot) - 1]; ax.set_visible(True)
        i = gene_index[row.gene_id]
        offset = np.log2(mor[i, :2].mean() + 1)
        points = np.log2(mor[i] + 1) - offset
        for group in range(6):
            pair = points[2 * group:2 * group + 2]
            color = GREY if group % 2 == 0 else BLUE
            ax.scatter([group - .08, group + .08], pair, color=color, s=25)
            mean = np.log2(mor[i, 2 * group:2 * group + 2].mean() + 1) - offset
            ax.plot([group - .18, group + .18], [mean, mean], color='black', linewidth=1)
        ax.axhline(0, color=GREY, linewidth=.6, linestyle=':')
        ax.set(xticks=range(6), xticklabels=['B0 C', 'B0 H', 'W6 C', 'W6 H', 'W12 C', 'W12 H'],
               ylabel='Baseline-control-relative log2 count',
               title=f'{row.gene_name} | {row.gene_id}\n{row.selection_reason}\nB0 H/C {row.B0_log2_effect_mor:.2f}; adjusted W6 {row.W6_adjusted_mor:.2f}, W12 {row.W12_adjusted_mor:.2f}')
        ax.tick_params(axis='x', rotation=15)
    save(fig, output, 'fig03_library_examples')
