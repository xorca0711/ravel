"""All declared associations and fixed published anchors, with distinct units."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from s5m_integrate_v1 import MEASUREMENTS, GSMS


def export(fig, output, name):
    fig.savefig(output / (name + '.png'), dpi=300, bbox_inches='tight')
    fig.savefig(output / (name + '.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def plot(output, associations, manifest, anchors, summary):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.titlesize': 10,
                         'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(15, 13), layout='constrained')
    fig.suptitle('S5M: all finite gene-feature associations\nDependent genomic features and shared source libraries; no population tests or causal coupling', fontsize=13)
    columns = [(flank, stat) for flank in [1000, 2000] for stat in ['pearson', 'spearman', 'inverse_anchor_pearson']]
    labels = ['±1k r', '±1k ρ', '±1k r(w)', '±2k r', '±2k ρ', '±2k r(w)']
    for row_index, norm in enumerate(['mor', 'total']):
        for col_index, universe in enumerate(['primary', 'all_mapped']):
            ax = axes[row_index, col_index]; block = associations.loc[(associations.universe == universe) & (associations.normalization == norm)]
            matrix = np.full((len(MEASUREMENTS), len(columns)), np.nan)
            for i, (name, phase, template, label) in enumerate(MEASUREMENTS):
                for j, (flank, stat) in enumerate(columns):
                    value = block.loc[(block.measurement == name) & (block.flank == flank) & (block.statistic == stat), 'coefficient'].item()
                    matrix[i, j] = float(value) if value is not None else np.nan
            cmap = plt.get_cmap('RdBu_r').copy(); cmap.set_bad('#dddddd')
            im = ax.imshow(matrix, vmin=-1, vmax=1, cmap=cmap, aspect='auto')
            for i in range(len(MEASUREMENTS)):
                for j in range(len(columns)):
                    value = matrix[i, j]
                    ax.text(j, i, 'NA' if not np.isfinite(value) else f'{value:.2f}', ha='center', va='center',
                            color='white' if np.isfinite(value) and abs(value) > .65 else 'black', fontsize=8)
            u = summary['universes'][universe]
            ax.set(xticks=range(len(columns)), xticklabels=labels, yticks=range(len(MEASUREMENTS)),
                   yticklabels=[x[3] for x in MEASUREMENTS], title=f'{universe}; {norm.upper()}\n{u["genes"]:,} genes / {u["unique_anchors"]:,} anchors')
            for boundary in [1.5, 6.5, 9.5]: ax.axhline(boundary, color='#777777', linewidth=.7)
    fig.colorbar(im, ax=axes, shrink=.75, label='Descriptive coefficient (r, ρ, or inverse-multiplicity weighted r)')
    export(fig, output, 'fig01_associations')

    fig, axes = plt.subplots(5, 2, figsize=(15, 17), layout='constrained')
    fig.suptitle('Five paper-selected anchors: distinct ATAC rank and RNA endpoints\nAll widths, normalization contexts and references retained; bars are library ranges, not confidence intervals', fontsize=13)
    short = ['S2 D6', 'S2 D30', 'B0 P', 'W6 post', 'W12 post', 'W6 adj P', 'W12 adj P', 'B0 2/2', 'W6 adj 2/2', 'W12 adj 2/2', 'B0 1/1', 'W6 adj 1/1', 'W12 adj 1/1']
    for i, item in enumerate(manifest):
        left, right = axes[i]; name = item['gene_name']; selected = anchors.loc[anchors.gene_id == item['gene_id']] if not anchors.empty else anchors
        if selected.empty:
            for ax in [left, right]: ax.text(.5, .5, name + '\nNo joined source record; not zero', ha='center', va='center', transform=ax.transAxes); ax.set_axis_off()
            continue
        row = selected.iloc[0]
        if item['atac_status'] == 'assayed_TSS_proxy':
            labels_atac = []; zero_counts = []
            for j, (phase, flank) in enumerate([(p, f) for p in ['D6', 'D30'] for f in ['1000', '2000']]):
                a = selected.loc[selected.flank.astype(str) == flank].iloc[0]
                delta, lo, hi = [float(a['atac__' + phase + suffix]) for suffix in ['_delta', '_range_min', '_range_max']]
                left.vlines(j, lo, hi, color='#7a9bb0', linewidth=1.1)
                left.scatter(j, delta, marker='o' if flank == '1000' else 'D', s=28, facecolors='#2676a5' if flank == '1000' else 'none', edgecolors='#2676a5', zorder=3)
                labels_atac.append(phase + (' ±1k' if flank == '1000' else ' ±2k'))
            for flank in ['1000', '2000']:
                a = selected.loc[selected.flank.astype(str) == flank].iloc[0]; zero_counts.append(sum(bool(a[g + '__zero_mean']) for g in GSMS))
            left.axhline(0, color='#999999', linewidth=.6)
            left.set(xticks=range(4), xticklabels=labels_atac, ylabel='ATAC rank contrast (percentile points)',
                     title=f'{name}; primary-qualified: {item["universe_primary"]}\nZero-mean libraries: ±1k {zero_counts[0]}/8; ±2k {zero_counts[1]}/8')
        else:
            left.text(.5, .5, name + '\n' + item['atac_status'] + '\nNo zero value assigned', ha='center', va='center', transform=left.transAxes); left.set_axis_off()
        for norm, offset, marker, face in [('mor', -.09, 'o', '#b65a22'), ('total', .09, 'D', 'none')]:
            values = []
            for unused, phase, template, label in MEASUREMENTS:
                value = row[template.format(norm=norm)]
                values.append(float(value) if str(value) not in ['NA', 'nan', ''] else np.nan)
            right.scatter(np.arange(len(values)) + offset, values, marker=marker, s=20, facecolors=face, edgecolors='#b65a22', linewidths=.7, label=norm.upper())
        right.axhline(0, color='#999999', linewidth=.6)
        right.set(xticks=range(len(short)), xticklabels=short, ylabel='RNA log2 contrast',
                  title=f'{name}; source zero flag: {item["rna_any_zero_flag"]}; low/regularization flag: {item["rna_any_low_or_regularization_flag"]}')
        right.tick_params(axis='x', rotation=55, labelsize=7)
        if i == 0: right.legend(frameon=False, fontsize=8)
    export(fig, output, 'fig02_published_anchors')
