"""Corrected count-zero and adjustment-range labels; unchanged anchor values."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
MEASUREMENTS = [
    ('S2_D6', 'D6', 's2__D6_log2_effect_{norm}', 'S2 D6'),
    ('S2_D30', 'D30', 's2__D30_log2_effect_{norm}', 'S2 D30 (same B0 libraries)'),
    ('S4_B0_primary', 'D30', 's4__B0_log2_effect_{norm}', 'S4 B0 primary'),
    ('S4_W6_post', 'D30', 's4__W6_log2_effect_{norm}', 'S4 W6 unadjusted'),
    ('S4_W12_post', 'D30', 's4__W12_log2_effect_{norm}', 'S4 W12 unadjusted'),
    ('S4_W6_primary', 'D30', 's4__W6_adjusted_{norm}', 'S4 W6 adjusted primary'),
    ('S4_W12_primary', 'D30', 's4__W12_adjusted_{norm}', 'S4 W12 adjusted primary'),
    ('S4B_B0_c2_h2', 'D30', 's4b__B0_c2_h2_{norm}', 'S4B B0 C2/H2 reference'),
    ('S4B_W6_c2_h2', 'D30', 's4b__W6_c2_h2_{norm}', 'S4B W6 adjusted C2/H2'),
    ('S4B_W12_c2_h2', 'D30', 's4b__W12_c2_h2_{norm}', 'S4B W12 adjusted C2/H2'),
    ('S4B_B0_c1_h1', 'D30', 's4b__B0_c1_h1_{norm}', 'S4B B0 C1/H1 reference'),
    ('S4B_W6_c1_h1', 'D30', 's4b__W6_c1_h1_{norm}', 'S4B W6 adjusted C1/H1'),
    ('S4B_W12_c1_h1', 'D30', 's4b__W12_c1_h1_{norm}', 'S4B W12 adjusted C1/H1')]

def export(fig, output, name):
    fig.savefig(output / (name + '.png'), dpi=300, bbox_inches='tight')
    fig.savefig(output / (name + '.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def plot_anchors(output, manifest, anchors):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.titlesize': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})
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
                a = selected.loc[selected.flank.astype(str) == flank].iloc[0]; zero_counts.append(sum(a[g + '__zero_mean'] == 'True' for g in GSMS))
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
                  title=f'{name}; count-zero flag: {item["rna_any_count_zero_flag"]}; adjustment range includes zero: {item["rna_any_adjustment_range_includes_zero_flag"]}\nLow/regularization flag: {item["rna_any_low_or_regularization_flag"]}')
        right.tick_params(axis='x', rotation=55, labelsize=7)
        if i == 0: right.legend(frameon=False, fontsize=8)
    export(fig, output, 'fig02_published_anchors')
