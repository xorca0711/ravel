"""Measured plots for the frozen relative-rank endpoint."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def export(fig, output, stem):
    fig.savefig(output / (stem + '.png'), dpi=300, bbox_inches='tight')
    fig.savefig(output / (stem + '.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def density(ax, x, y, xlabel, ylabel, title):
    span = max(float(np.max(np.abs(x))), float(np.max(np.abs(y))), 1) * 1.04
    ax.hexbin(x, y, gridsize=55, mincnt=1, bins='log', cmap='cividis', extent=(-span, span, -span, span))
    ax.plot([-span, span], [-span, span], '--', color='#777777', linewidth=.7)
    ax.axhline(0, color='#888888', linewidth=.5); ax.axvline(0, color='#888888', linewidth=.5)
    ax.set(xlim=(-span, span), ylim=(-span, span), xlabel=xlabel, ylabel=ylabel, title=title)
    ax.set_aspect('equal', adjustable='box')


def plot(output, effects, cases):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.titlesize': 10,
                         'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})
    p = effects.loc[effects.flank == 1000].set_index('anchor_id')
    s = effects.loc[effects.flank == 2000].set_index('anchor_id').loc[p.index]
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), layout='constrained')
    fig.suptitle('S3: relative ordering near annotation-based protein-coding TSS proxies\nFinite deposited libraries; rank shifts are not absolute accessibility or original memory domains', fontsize=12)
    density(axes[0, 0], p.D6_delta.to_numpy(), p.D30_delta.to_numpy(), 'D6 history − control (percentile points)',
            'D30 history − control (percentile points)', f'Primary ±1 kb; {len(p):,} unique windows')
    for phase, color in [('D6', '#2676a5'), ('D30', '#b65a22')]:
        x = np.sort(np.abs(p[phase + '_delta'].to_numpy()))
        axes[0, 1].plot(x, np.arange(1, len(x) + 1) / len(x), color=color, label=f'{phase}; median {np.median(x):.2f}')
    axes[0, 1].set(xlabel='Absolute rank contrast (percentile points)', ylabel='Fraction of fixed windows',
                    title='Primary absolute displacement distribution', ylim=(0, 1))
    axes[0, 1].legend(frameon=False)
    for ax, phase in zip(axes[1], ['D6', 'D30']):
        density(ax, p[phase + '_delta'].to_numpy(), s[phase + '_delta'].to_numpy(), '±1 kb contrast (percentile points)',
                '±2 kb contrast (percentile points)', phase + ': window-width sensitivity')
    export(fig, output, 'fig01_relative_rank_overview')
    fig, axes = plt.subplots(4, 2, figsize=(11, 12), layout='constrained')
    fig.suptitle('Fixed published/RNA examples: every library, both window widths\nFilled circles: ±1 kb; open diamonds: ±2 kb. No matched trajectories or new target selection.', fontsize=12)
    gsms = ['GSM' + str(i) for i in range(2441001, 2441009)]
    x = np.repeat(np.arange(4), 2) + np.tile([-.12, .12], 4)
    for ax, slot in zip(axes.flat, range(1, 8)):
        rows = cases.loc[cases.plot_slot == slot]; first = rows.iloc[0]
        if not bool(first.eligible):
            ax.text(.5, .5, first.gene_name + '\nUnassayed in this protein-coding universe\nNo zero accessibility value assigned', ha='center', va='center', transform=ax.transAxes)
            ax.set_axis_off(); continue
        for flank, shift, marker, face in [(1000, -.025, 'o', '#2676a5'), (2000, .025, 'D', 'none')]:
            row = rows.loc[rows.flank == flank].iloc[0]
            y = [row[gsm + '__percentile'] for gsm in gsms]
            ax.scatter(x + shift, y, s=28, marker=marker, facecolors=face, edgecolors='#2676a5', linewidths=.8, zorder=3)
        primary = rows.loc[rows.flank == 1000].iloc[0]
        ax.axhline(50, color='#aaaaaa', linewidth=.5)
        ax.set(xticks=range(4), xticklabels=['D6 C', 'D6 H', 'D30 C', 'D30 H'], ylim=(-2, 102), ylabel='Within-library percentile',
               title=f'{first.gene_name}\nPrimary Δ6 {primary.D6_delta:.2f}; Δ30 {primary.D30_delta:.2f} pp')
    axes.flat[-1].set_axis_off()
    export(fig, output, 'fig02_fixed_examples')
