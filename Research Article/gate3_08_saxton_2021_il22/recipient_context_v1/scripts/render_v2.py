"""Rendering correction only: preserve small positive measurements in display."""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
from describe_v1 import ROOT, GENES, LIBRARIES, LABELS, AGGREGATES, require

SOURCE = ROOT / 'analysis/research/runs/sx22_e1a_recipient_description_v1/strata.csv'


def display_value(value):
    if value is None or np.isnan(value):
        return 'NA'
    require(np.isfinite(value) and value >= 0, 'Invalid display value')
    if value == 0:
        return '0'
    return '<0.1' if value < .1 else f'{value:.1f}'


def render(rows, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'sx22-e1a-v1'})
    labels = LABELS + AGGREGATES
    lookup = {(r['library'], r['pipeline_label_or_aggregate'], r['gene']): r for r in rows}
    denominators = np.array([[lookup[(lib, label, GENES[0])]['n_cells'] for lib in LIBRARIES]
                            for label in labels])
    detection = np.full((len(labels), 6), np.nan)
    abundance = detection.copy()
    for i, label in enumerate(labels):
        for k, lib in enumerate(LIBRARIES):
            for j, gene in enumerate(GENES):
                r = lookup[(lib, label, gene)]
                if r['n_cells']:
                    detection[i, 2*k+j] = r['detection_fraction'] * 100
                    abundance[i, 2*k+j] = r['counts_per_million_stratum_counts']
    fig, axes = plt.subplots(1, 3, figsize=(19, 9), gridspec_kw={'width_ratios': [2, 4.2, 4.2]})
    fig.subplots_adjust(left=.23, right=.98, top=.78, bottom=.27, wspace=.13)
    panel_specs = [(denominators, denominators, 'Greys', Normalize(0, max(1, denominators.max())),
                    'A  Retained cells (n)', ['PBS', 'day 14', 'day 28']),
                   (detection, detection, 'Blues', Normalize(0, 100),
                    'B  Cells with positive count (%)', [f'{lib}\n{gene}' for lib in ('PBS', 'day 14', 'day 28') for gene in GENES]),
                   (abundance, np.log10(1 + abundance), 'YlGnBu',
                    Normalize(0, max(1, np.nanmax(np.log10(1 + abundance)))),
                    'C  Counts per million stratum counts', [f'{lib}\n{gene}' for lib in ('PBS', 'day 14', 'day 28') for gene in GENES])]
    for panel, (ax, spec) in enumerate(zip(axes, panel_specs)):
        raw, color, cmap_name, norm, title, xticks = spec
        cmap = plt.get_cmap(cmap_name).with_extremes(bad='#eeeeee')
        image = ax.imshow(color, aspect='auto', cmap=cmap, norm=norm)
        ax.set_title(title, fontsize=11, pad=13, loc='left')
        ax.set_xticks(range(raw.shape[1]), xticks, fontsize=8)
        ax.xaxis.tick_top(); ax.tick_params(axis='both', length=0)
        ax.set_yticks(range(len(labels)), labels if panel == 0 else [''] * len(labels), fontsize=8.5)
        for i in range(raw.shape[0]):
            for j in range(raw.shape[1]):
                value = raw[i, j]
                text = f'{int(value):,}' if panel == 0 else display_value(value)
                ink = 'white' if np.isfinite(color[i, j]) and norm(color[i, j]) > .64 else '#17212b'
                ax.text(j, i, text, ha='center', va='center', fontsize=8, color=ink)
        ax.axhline(len(LABELS)-.5, color='#17212b', linewidth=1.4)
        if panel:
            ax.axvline(1.5, color='white', linewidth=2)
            ax.axvline(3.5, color='white', linewidth=2)
            box = ax.get_position()
            color_axis = fig.add_axes([box.x0, .22, box.width, .02])
            bar = fig.colorbar(image, cax=color_axis, orientation='horizontal')
            bar.set_label('Positive-count cells (%)' if panel == 1 else 'Color = log10(1 + counts per million)', fontsize=8)
            bar.ax.tick_params(labelsize=8)
        for spine in ax.spines.values(): spine.set_visible(False)
    reference = (axes[0].get_position().y0, axes[0].get_position().height)
    require(all(np.allclose((ax.get_position().y0, ax.get_position().height), reference)
                for ax in axes), 'Figure rows are not vertically aligned')
    fig.text(.02, .95, 'Two prespecified transcripts in the saved Choi benchmark', fontsize=19, weight='bold')
    fig.text(.02, .905, 'Observed cells within each library and literal pipeline label. No condition contrasts or population inference.', fontsize=11)
    fig.text(.02, .865, 'PBS: GSM4304609 / PBS_AT2_Tomato     day 14: GSM4304611 / Day14_AT2_Tomato     day 28: GSM4304613 / Day28_AT2_Tomato', fontsize=9)
    fig.text(.02, .145, 'Each library pools two mice; one library per condition. Library, time and processing cannot be separated.', fontsize=10)
    fig.text(.02, .105, 'NA = no cells; 0 = exact zero; <0.1 = positive below 0.1. Non-detection is not biological absence. Literal labels are not validated identities.', fontsize=9)
    fig.text(.02, .065, 'Abundance = 1,000,000 x summed gene counts / summed counts across all saved features in the same stratum. Aggregates overlap the label rows.', fontsize=9)
    fig.text(.02, .025, 'Counts do not measure receptor protein, signaling, responsiveness, memory, lineage or repair. Non-contaminant uses the original label-prefix rule.', fontsize=9)
    for suffix in ('png', 'svg'):
        path = output / f'recipient_transcripts_v2.{suffix}'
        require(not path.exists(), 'Figure already exists')
        fig.savefig(path, dpi=180, metadata={'Date': None} if suffix == 'svg' else {})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output).resolve()
    require(output.parent == ROOT / 'analysis/research/runs' and output.is_dir(), 'Runner output required')
    require(all(p.name in {'receipt.json', 'stdout.log', 'stderr.log'} for p in output.iterdir()), 'Existing output artifacts')
    with SOURCE.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 78, 'Unexpected stratum table')
    displayed = []
    for row in rows:
        row['n_cells'] = int(row['n_cells'])
        for key in ('detection_fraction', 'counts_per_million_stratum_counts'):
            row[key] = float(row[key]) if row[key] else None
        require((row['n_cells'] == 0) == (row['status'] == 'empty_stratum'), 'Missingness mismatch')
        displayed.append(dict(library=row['library'], label=row['pipeline_label_or_aggregate'], gene=row['gene'],
                              n_cells=row['n_cells'],
                              detection_percent_display=display_value(row['detection_fraction'] * 100 if row['n_cells'] else None),
                              abundance_display=display_value(row['counts_per_million_stratum_counts'])))
    render(rows, output)
    with (output/'display_values.csv').open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(displayed[0])); writer.writeheader(); writer.writerows(displayed)
    with (output/'render_summary.json').open('x', encoding='utf-8') as stream:
        json.dump({'kind': 'Rendering correction only; numerical source table unchanged',
                   'source': SOURCE.relative_to(ROOT).as_posix(),
                   'supersedes_figure': 'analysis/research/runs/sx22_e1a_recipient_description_v1/recipient_transcripts.png',
                   'display_rule': 'NA for unavailable; 0 for exact zero; <0.1 for strictly positive values below 0.1; otherwise one decimal',
                   'small_positive_display_cells': sum(r[k]=='<0.1' for r in displayed for k in ('detection_percent_display','abundance_display'))}, stream, indent=2)
        stream.write('\n')
    print('Rendering correction complete; original numerical source and figures preserved.')


if __name__ == '__main__':
    main()
