"""Portfolio figures from frozen screen tables; qualitative proposals are labelled."""
import argparse
import csv
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
import numpy as np

ROOT = Path('analysis/research/runs')
BLUE, ORANGE, GREEN, GREY = '#0072B2', '#D55E00', '#009E73', '#747B82'
FOCUS = ['Tigit', 'Prdm1', 'Areg', 'Ccr2', 'Il2ra', 'Igfbp4', 'Pde3b', 'Adcy6', 'Il1r2', 'Bcl2']


def read(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def save(fig, out, name):
    for extension in ['png', 'pdf', 'svg']:
        fig.savefig(out / (name + '.' + extension), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def footer(fig, text):
    fig.text(.02, .015, text, fontsize=8, color='#555555', va='bottom')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 11,
                         'axes.titleweight': 'bold', 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'legend.frameon': False})
    s1 = json.loads((ROOT / 'dupage_target_screen_v1/summary.json').read_text())
    s2 = json.loads((ROOT / 'dupage_target_screen_v2/summary.json').read_text())
    rows = read(ROOT / 'dupage_target_screen_v2/all_annotated.tsv')
    lookup = {r['gene_id']: r for r in rows}
    frontier = read(ROOT / 'dupage_target_screen_v2/protein_frontier.tsv')
    genes = sorted({r['gene_id'] for r in frontier})

    fig, axes = plt.subplots(1, 3, figsize=(12.3, 4.8), gridspec_kw={'width_ratios': [1.35, 1, 1.25]})
    fig.subplots_adjust(left=.13, right=.98, bottom=.23, top=.79, wspace=.72)
    labels = ['Protein coding', 'Other exact types', 'Unmatched symbol', 'Chromosome mismatch']
    values = [s2['protein_eligible'], s2['annotation_status']['exact_unique'] - s2['protein_eligible'],
              s2['annotation_status']['unmatched'], s2['annotation_status']['chromosome_discordant']]
    axes[0].barh(labels, values, color=[BLUE, GREY, ORANGE, '#CC79A7'])
    axes[0].invert_yaxis(); axes[0].set_xlim(0, 11614); axes[0].set_xlabel('Loci (fixed universe: 11,614)')
    for y, value in enumerate(values): axes[0].text(value + 140, y, f'{value:,}', va='center', fontsize=9)
    axes[0].set_title('A  Exact annotation audit', loc='left', pad=16)
    coding = s2['v1_frontier_protein_unique']; other = s1['frontier_unique_genes'] - coding
    axes[1].bar([0], [coding], color=BLUE, width=.5)
    axes[1].bar([0], [other], bottom=[coding], color=GREY, width=.5)
    axes[1].text(0, coding / 2, str(coding), ha='center', va='center', color='white', weight='bold')
    axes[1].text(0, coding + other / 2, str(other), ha='center', va='center', color='white', weight='bold')
    axes[1].set_xticks([0], ['Unrestricted\nreading frontier']); axes[1].set_ylim(0, 28)
    axes[1].set_ylabel('Unique loci'); axes[1].set_title('B  Assay qualification', loc='left', pad=16)
    axes[1].text(.5, -.25, 'Blue: protein coding\nGrey: other / unresolved', transform=axes[1].transAxes, ha='center', fontsize=8)
    names = ['Low: increase', 'Low: decrease', 'State: increase', 'State: decrease']
    counts = [s2['track_counts'][k] for k in ['low_positive', 'low_negative', 'state_positive', 'state_negative']]
    axes[2].barh(names, counts, color=[ORANGE, BLUE, ORANGE, BLUE]); axes[2].invert_yaxis()
    axes[2].set_xlim(0, 4700); axes[2].set_xlabel('Coding loci passing sign rules')
    for y, value in enumerate(counts): axes[2].text(value + 80, y, f'{value:,}', va='center', fontsize=9)
    axes[2].set_title('C  Two overlapping tracks', loc='left', pad=16)
    fig.suptitle('DuPage-first screen | Measurement qualification precedes target choice', x=.02, ha='left', fontsize=15, weight='bold')
    footer(fig, 'Poly-A RNA-seq is not a mature-small-RNA assay. Coding-only selection yields 32 displayed genes.\nTracks overlap; top 10 per signed track is a reading budget, not a significance or effect threshold.')
    save(fig, out, 'fig01_screen_qualification')

    matrix = np.array([[float(lookup[g][k]) for k in ['delta_high', 'delta_low', 'interaction']] for g in genes])
    cmap = LinearSegmentedColormap.from_list('blue_white_orange', [BLUE, '#FFFFFF', ORANGE])
    fig = plt.figure(figsize=(7.8, 11.4)); ax = fig.add_axes([.18, .12, .57, .76])
    limit = float(np.abs(matrix).max())
    im = ax.imshow(matrix, cmap=cmap, vmin=-limit, vmax=limit, aspect='auto')
    ax.set_yticks(range(len(genes)), genes, fontstyle='italic', fontsize=9)
    ax.set_xticks(range(3), ['KO−HET\nCD62L-high', 'KO−HET\nCD62L-low', 'State\ninteraction'])
    ax.xaxis.tick_top(); ax.tick_params(length=0, pad=7)
    for (y, x), value in np.ndenumerate(matrix):
        ax.text(x, y, f'{value:+.2f}', ha='center', va='center', fontsize=8,
                color='white' if abs(value) > limit * .65 else '#222222')
    ax.set_xticks(np.arange(-.5, 3, 1), minor=True); ax.set_yticks(np.arange(-.5, len(genes), 1), minor=True)
    ax.grid(which='minor', color='#E9EDF0', linewidth=.6); ax.tick_params(which='minor', length=0)
    cax = fig.add_axes([.82, .39, .03, .25]); cb = fig.colorbar(im, cax=cax)
    cb.set_label('Difference in mean log₂(FPKM + 1)', fontsize=9)
    fig.text(.03, .965, '32 protein-coding candidates', fontsize=17, weight='bold')
    fig.text(.03, .935, 'Complete union of four reading lists · alphabetical order', fontsize=11)
    footer(fig, 'Shared-source exploration, 11 preparations; biological independence is unresolved.\nInteraction = low-state contrast − high-state contrast. Values are not ordinary log₂ fold changes.\nColours show measured RNA differences, not significance, pathway activation or target validity.')
    save(fig, out, 'fig02_complete_protein_frontier')

    fig, axes = plt.subplots(1, 2, figsize=(11.3, 7.4), sharey=True)
    fig.subplots_adjust(left=.12, right=.98, bottom=.18, top=.81, wspace=.18)
    for ax, key, title, prefix in zip(axes, ['delta_low', 'interaction'], ['A  Activated-state RNA contrast', 'B  Difference between observed states'], ['low', 'interaction']):
        for y, gene in enumerate(FOCUS):
            row = lookup[gene]; point = float(row[key]); lo = float(row[prefix + '_sensitivity_min']); hi = float(row[prefix + '_sensitivity_max'])
            color = ORANGE if point > 0 else BLUE
            ax.plot([lo, hi], [y, y], color=color, lw=2, zorder=2)
            ax.scatter([point], [y], color=color, s=36, edgecolors='white', linewidth=.6, zorder=3)
        ax.axvline(0, color='#777777', lw=.8, ls='--'); ax.grid(axis='x', color='#EEEEEE')
        ax.set_title(title, loc='left', pad=14); ax.set_xlabel('Difference in mean log₂(FPKM + 1)')
    axes[0].set_yticks(range(len(FOCUS)), FOCUS, fontstyle='italic'); axes[0].invert_yaxis()
    fig.suptitle('Specific candidates, competing explanations', x=.02, ha='left', fontsize=16, weight='bold')
    fig.text(.02, .89, 'Post-outcome literature-focused display; not an unbiased ranking', fontsize=10, color='#555555')
    footer(fig, 'Dots: primary estimates. Lines: extrema across 11 separate library omissions, pseudocounts 0.5/2, and primary.\nSensitivity ranges are not confidence intervals. Areg/Il2ra are informative non-robust references; Pde3b is a prior-paper anchor.')
    save(fig, out, 'fig03_candidate_sensitivity')

    # A qualitative comparison matrix, not a measured pathway diagram.
    fig, ax = plt.subplots(figsize=(14.2, 8)); ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    headers = ['Observed RNA', 'Working question', 'Decisive first comparison', 'Alternative / informative failure']
    content = [
        ['Tigit and Prdm1 decrease.\nAreg interaction is fragile.',
         'Does Ezh2 loss impair inducible TIGIT–Blimp-1 output in viable activated Tregs?',
         'Matched HET/KO activation, with versus without TIGIT engagement: surface TIGIT, Blimp-1 and secreted AREG per viable cell.',
         'Equal output despite RNA changes weakens this route. A general activation or survival defect can mimic it. Repair needs its own functional assay.'],
        ['Ccr2 decreases, together with several other chemokine receptors.',
         'Does reduced CCR2 contribute to altered localization, cell fitness, or simply mark a changed Treg state?',
         'Measure CCR2 protein, direct chemotaxis, CD25/IL-2 response and viable recovery as separate endpoints.',
         'Abundance is not migration. Migration preserved with altered fitness favors a different explanation; shared-state shifts can explain both.'],
        ['Igfbp4 increases. External H3K27me3 context is compatible but unmatched.',
         'Is IGFBP4 a functional growth-factor buffer, a compensatory response, or a population marker?',
         'First confirm Treg-source protein. Then perturb IGFBP4 under defined IGF exposure and measure signaling, survival and suppression separately.',
         'Absent protein or unchanged function weakens the mediator model. Opposite effects support compensation; IGF effects depend on cell state.'],
    ]
    xs = [.01, .24, .49, .75]; widths = [.21, .23, .24, .24]; top = .79; height = .225
    for j, head in enumerate(headers): ax.text(xs[j] + .012, .85, head, fontsize=11, weight='bold', va='top')
    for i, cells in enumerate(content):
        y = top - i * height
        for j, value in enumerate(cells):
            ax.add_patch(Rectangle((xs[j], y - height + .012), widths[j], height - .02,
                                   facecolor=['#EDF5FA', '#F4F6F8', '#EFF7F3', '#FBF3EB'][j], edgecolor='none'))
            wrapped = '\n'.join(textwrap.fill(line, width=31 if j == 0 else 35) for line in value.split('\n'))
            ax.text(xs[j] + .012, y - .015, wrapped, fontsize=9.4, va='top', linespacing=1.45)
    ax.text(.01, .97, 'From candidate to a discriminating experiment', fontsize=18, weight='bold', va='top')
    ax.text(.01, .91, 'PROPOSED comparisons · no pathway mediation, secretion or repair function established by this screen', fontsize=10, color='#555555', va='top')
    ax.text(.01, .035, 'Premises: TIGIT study (2025), CCR2 study (2018) and IGF study (2020); exact locators in TARGET_SCREEN_RESULT.md.\nUnit: independently obtained mouse/preparation; wells are technical. Effect margin, sample size and laboratory feasibility remain unspecified.', fontsize=8.5, va='bottom', color='#555555')
    save(fig, out, 'fig04_proposed_comparisons')

    fields = ['gene_id', 'delta_high', 'delta_low', 'interaction', 'low_sensitivity_min', 'low_sensitivity_max',
              'interaction_sensitivity_min', 'interaction_sensitivity_max', 'chromatin_class', 'coding_low_rank', 'coding_state_rank']
    with (out / 'figure_source_values.tsv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=['display'] + fields, delimiter='\t'); writer.writeheader()
        for display, selected in [('complete_frontier', genes), ('focused_candidates', FOCUS)]:
            writer.writerows({'display': display, **{k: lookup[g][k] for k in fields}} for g in selected)
    (out / 'figure_manifest.json').write_text(json.dumps({'figures': 4, 'formats': ['png', 'pdf', 'svg'],
        'full_frontier_genes': genes, 'focused_post_outcome_genes': FOCUS,
        'numerical_source': 'dupage_target_screen_v2', 'qualitative_panel': 'fig04_proposed_comparisons',
        'interpretation': 'Exploratory RNA and proposed comparisons, no scientific acceptance.'}, indent=2) + '\n')
    print('Generated 4 figures in PNG/PDF/SVG, source-value table and manifest.')


if __name__ == '__main__':
    main()
