"""Measured S2 figures; called by the hash-bound numerical entrypoint."""
from pathlib import Path
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ORANGE, BLUE, GREY = '#D55E00', '#0072B2', '#777777'


def save(fig, folder, name):
    fig.savefig(folder / (name + '.png'), dpi=300, facecolor='white')
    fig.savefig(folder / (name + '.pdf'), facecolor='white', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def density(ax, x, y, xlabel, ylabel, title):
    limit = max(1., float(np.ceil(max(np.max(np.abs(x)), np.max(np.abs(y))))))
    hexbins = ax.hexbin(x, y, gridsize=65, mincnt=1, bins='log', cmap='cividis',
                        extent=(-limit, limit, -limit, limit), linewidths=0)
    ax.plot([-limit, limit], [-limit, limit], color=GREY, lw=.8, ls='--', zorder=0)
    ax.axvline(0, color=GREY, lw=.5); ax.axhline(0, color=GREY, lw=.5)
    ax.set(xlim=(-limit, limit), ylim=(-limit, limit), xlabel=xlabel, ylabel=ylabel, title=title)
    ax.set_aspect('equal', adjustable='box')
    return hexbins


def plot_all(folder: Path, effects, mor, qc, correlations, cases):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.titlesize': 11, 'axes.labelsize': 10,
                         'legend.fontsize': 9, 'legend.frameon': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'savefig.bbox': 'tight', 'lines.linewidth': 1.5})
    labels = qc.short_label.tolist()
    colors = [GREY if x.role == 'control' else ORANGE if x.time == 'D6' else BLUE for x in qc.itertuples()]
    x = np.arange(8)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout='constrained')
    axes[0, 0].bar(x, qc.gene_count_total / 1e6, color=colors)
    axes[0, 0].set(ylabel='Sum of gene counts (millions)', title='A  Deposited count totals')
    axes[0, 1].bar(x, qc.detected_genes / 1000, color=colors)
    axes[0, 1].set(ylabel='Genes with count > 0 (thousands)', title='B  Detected features')
    axes[1, 0].scatter(x - .07, qc.mor_size_factor, color=BLUE, marker='o', label='Median of ratios')
    axes[1, 0].scatter(x + .07, qc.total_count_size_factor, color=ORANGE, marker='s', label='Total count')
    axes[1, 0].axhline(1, color=GREY, lw=.7, ls=':')
    axes[1, 0].set(ylabel='Within-time size factor (geometric mean = 1)', title='C  Normalization factors')
    axes[1, 0].legend(loc='best')
    for ax in [axes[0, 0], axes[0, 1], axes[1, 0]]:
        ax.set_xticks(x, labels, rotation=45, ha='right')
    heat = axes[1, 1].imshow(correlations, cmap='cividis', vmin=float(correlations.min()), vmax=1)
    axes[1, 1].set_xticks(x, labels, rotation=45, ha='right')
    axes[1, 1].set_yticks(x, labels)
    axes[1, 1].set_title('D  Pearson profile correlation: log2(MOR + 1)')
    for i in range(8):
        for j in range(8):
            value = correlations[i, j]
            axes[1, 1].text(j, i, f'{value:.3f}', ha='center', va='center', fontsize=6.5,
                            color='white' if value < (1 + correlations.min()) / 2 else 'black')
    fig.colorbar(heat, ax=axes[1, 1], label='Pearson correlation', shrink=.8)
    fig.suptitle('S2 sample diagnostics: two deposited libraries per group\nC = control; D6 A = acute inflamed; D30 H = recovered-baseline history', fontsize=13)
    save(fig, folder, 'fig01_sample_qc')

    qualified = effects[effects.eligible_union]
    a, b = qualified.D6_log2_effect_mor.to_numpy(), qualified.D30_log2_effect_mor.to_numpy()
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), layout='constrained')
    hexbins = density(axes[0, 0], a, b, 'D6 acute/control log2 effect', 'D30 history/control log2 effect',
                       'A  Unselected qualified-gene effect profiles')
    fig.colorbar(hexbins, ax=axes[0, 0], label='Genes per hexagon (log scale)', shrink=.8)
    for values, color, label, style in [(a, ORANGE, 'D6 acute inflamed', '-'), (b, BLUE, 'D30 recovered-baseline history', '--')]:
        ordered = np.sort(np.abs(values))
        axes[0, 1].plot(ordered, np.arange(1, len(ordered) + 1) / len(ordered), color=color, label=label, ls=style)
    axes[0, 1].set(xlabel='Absolute descriptive log2 effect', ylabel='Fraction of qualified genes',
                   title='B  Continuous absolute-effect distributions', ylim=(0, 1.02))
    axes[0, 1].legend(loc='lower right')
    for ax, time in zip(axes[1], ['D6', 'D30']):
        h = density(ax, qualified[time + '_log2_effect_mor'].to_numpy(), qualified[time + '_log2_effect_total'].to_numpy(),
                    'Median-of-ratios log2 effect', 'Total-count-scaled log2 effect',
                    f'{"C" if time == "D6" else "D"}  {time} normalization sensitivity')
        fig.colorbar(h, ax=ax, label='Genes per hexagon (log scale)', shrink=.8)
    fig.suptitle(f'S2 continuous RNA effects: {len(qualified):,} genes qualified at either time\nFinite-library description; cross-time platform/layout differences remain', fontsize=13)
    save(fig, folder, 'fig02_effect_profiles')

    locations = {gene: i for i, gene in enumerate(effects.gene_id)}
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), layout='constrained')
    positions = np.array([-.08, .08, .92, 1.08, 1.92, 2.08, 2.92, 3.08])
    for ax, case in zip(axes.flat, cases.itertuples()):
        vals = mor[locations[case.gene_id]]
        transformed = np.empty(8)
        for start in [0, 4]:
            denominator = np.mean(vals[start:start + 2]) + 1
            transformed[start:start + 4] = np.log2((vals[start:start + 4] + 1) / denominator)
        ax.scatter(positions, transformed, c=colors, s=35, edgecolors='white', linewidths=.4, zorder=3)
        for group in range(4):
            time_start = 0 if group < 2 else 4
            mean = np.log2((np.mean(vals[2 * group:2 * group + 2]) + 1) / (np.mean(vals[time_start:time_start + 2]) + 1))
            ax.plot([group - .18, group + .18], [mean, mean], color='black', lw=1)
        ax.axhline(0, color=GREY, lw=.6, ls=':')
        ax.set_xticks(range(4), ['D6 C', 'D6 acute', 'D30 C', 'D30 history'])
        ax.set_ylabel('Control-relative log2 count')
        name = case.gene_name if case.gene_name != 'NA' else case.gene_id
        reason = '\n'.join(textwrap.wrap(case.selection_reason, 45))
        ax.set_title(f'{name} | {case.gene_id}\n{reason}\nD6 effect {case.D6_log2_effect_mor:.2f}; D30 effect {case.D30_log2_effect_mor:.2f}', fontsize=9)
    fig.suptitle('Selected examples: finite library values, not biological classes\nDots = libraries; bars = transformed count-scale group means; no longitudinal pairing', fontsize=13)
    save(fig, folder, 'fig03_library_examples')
