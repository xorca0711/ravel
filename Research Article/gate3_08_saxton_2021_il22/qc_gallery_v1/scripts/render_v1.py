"""Render reviewed technical tables only; never load expression or rerun QC."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[4]
R1 = ROOT/'analysis/research/runs/sx22_r1_v2'
X1 = ROOT/'analysis/research/runs/sx22_x1_annotation_v1'
ORDER = ('PBS_1', 'PBS_2', 'LH5_1', 'LH5_2', 'LH30_1', 'LH30_2')
DIMENSIONS = (
    ('multiple_stable_ids', 'stable_id_count', 'Multiple stable IDs'),
    ('multiple_chromosomes', 'chromosome_count', 'Multiple chromosomes'),
    ('multiple_strands', 'strand_count', 'Multiple strands'),
    ('multiple_loci', 'locus_count', 'Multiple coordinate tuples'),
    ('multiple_biotypes', 'biotype_count', 'Multiple biotypes'),
    ('multiple_descriptions', 'description_count', 'Multiple descriptions'),
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def source_bindings(directory, names):
    receipt = json.loads((directory/'receipt.json').read_text())
    for name in names:
        path = directory/name
        declared = [r for r in receipt['outputs'] if r['path'] == path.relative_to(ROOT).as_posix()]
        require(len(declared) == 1, 'Missing/ambiguous source receipt output')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == declared[0]['sha256'], 'Source receipt mismatch')


def r1_values(qc, samples):
    require(tuple(r['column'] for r in qc) == ORDER, 'Changed QC source order or coverage')
    require(tuple(r['column'] for r in samples) == ORDER, 'Changed sample source order or coverage')
    output = []
    for i, row in enumerate(qc):
        total, nonzero = int(row['total_counts']), int(row['genes_nonzero'])
        fraction = Decimal(row['top10_count_fraction'])
        require(total > 0 and 0 < nonzero <= 35275, 'Invalid copied count denominator')
        require(fraction.is_finite() and 0 <= fraction <= 1, 'Invalid largest-ten fraction')
        percent = fraction * 100
        output.append(dict(source_order=i+1, library=row['column'], total_counts=total,
                           nonzero_gene_rows=nonzero, largest_ten_fraction=row['top10_count_fraction'],
                           largest_ten_percent=str(percent), total_counts_display=f'{total:,}',
                           nonzero_gene_rows_display=f'{nonzero:,}', largest_ten_percent_display=f'{percent:.4f}%'))
    return output


def x1_values(summary, repeated):
    denominator = int(summary['repeated_symbol_labels'])
    require(len(repeated) == denominator and denominator > 0, 'Repeated-label denominator mismatch')
    require(len({r['symbol'] for r in repeated}) == denominator, 'Duplicate repeated-symbol record')
    multiplicity = Counter(int(r['row_count']) for r in repeated)
    require(min(multiplicity) >= 2, 'Non-repeated symbol in source table')
    require(sum(k*v for k,v in multiplicity.items()) == summary['rows_with_repeated_nonempty_symbols'], 'Repeated-row total mismatch')
    require(dict(multiplicity) == {int(k): int(v) for k,v in summary['repeated_symbol_multiplicity'].items()}, 'Multiplicity summary mismatch')
    rows = []
    for k, count in sorted(multiplicity.items()):
        rows.append(dict(panel='multiplicity', category=f'{k} records per label', count=count,
                         denominator=denominator, unit='repeated symbol labels',
                         source_key=f'repeated_symbol_multiplicity.{k}', display=f'{count} / {denominator}'))
    for suffix, field, label in DIMENSIONS:
        values = [int(r[field]) for r in repeated]
        require(all(1 <= value <= int(row['row_count']) for value, row in zip(values, repeated)), 'Invalid annotation cardinality')
        count = sum(value > 1 for value in values)
        key = 'repeated_symbols_' + suffix
        require(count == summary[key], 'Overlapping dimension summary mismatch')
        rows.append(dict(panel='overlapping_dimensions', category=label, count=count,
                         denominator=denominator, unit='repeated symbol labels', source_key=key,
                         display=f'{count} / {denominator}'))
    return rows


def clean_svg(text):
    cleaned = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
    ET.fromstring(cleaned)
    return cleaned


def save_figure(fig, output, stem):
    png, svg = output/(stem+'.png'), output/(stem+'.svg')
    require(not png.exists() and not svg.exists(), 'Figure output already exists')
    with png.open('xb') as stream:
        fig.savefig(stream, format='png', dpi=180)
    buffer = io.StringIO()
    fig.savefig(buffer, format='svg', metadata={'Date': None})
    with svg.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(clean_svg(buffer.getvalue()))
    plt.close(fig)


def style():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'sx22-qc-gallery-v1'})


def bars(ax, labels, values, displays, color, maximum=None):
    y = list(range(len(labels)))
    ax.barh(y, values, height=.62, color=color)
    ax.set_yticks(y, labels); ax.invert_yaxis()
    bound = maximum if maximum is not None else max(values)
    require(bound > 0, 'Invalid chart range')
    ax.set_xlim(0, bound*1.37)
    for i, (value, display) in enumerate(zip(values, displays)):
        ax.text(value + bound*.025, i, display, va='center', fontsize=10)
    ax.grid(axis='x', color='#e1e5e8', linewidth=.6); ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0)
    for spine in ax.spines.values(): spine.set_visible(False)


def render_r1(rows, output):
    style()
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    fig.subplots_adjust(left=.085, right=.98, bottom=.27, top=.73, wspace=.34)
    panels = [('A  Total counts', 'total_counts', 'total_counts_display', 1e6, 'Millions of deposited counts'),
              ('B  Nonzero gene rows', 'nonzero_gene_rows', 'nonzero_gene_rows_display', 1, 'Gene rows with count > 0'),
              ('C  Largest-ten count fraction', 'largest_ten_percent', 'largest_ten_percent_display', 1, 'Share of total counts (%)')]
    for ax, (title, key, display, scale, xlabel) in zip(axes, panels):
        bars(ax, [r['library'] for r in rows], [float(r[key])/scale for r in rows],
             [r[display] for r in rows], '#376a89')
        ax.set_title(title, loc='left', fontsize=12, pad=18); ax.set_xlabel(xlabel, labelpad=11)
        if key == 'nonzero_gene_rows': ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
    fig.text(.035, .94, 'R1 | Technical library QC', fontsize=21, weight='bold')
    fig.text(.035, .865, 'Six deposited library records, in original source order. Values copied from the reviewed frozen table.', fontsize=11)
    fig.text(.035, .17, 'Largest-ten fraction = sum of the ten largest gene-row counts / total counts in that library. No gene names are ranked here.', fontsize=10)
    fig.text(.035, .105, 'Libraries are technical records; animal identities and independence remain unverified.', fontsize=11)
    fig.text(.035, .04, 'These QC panels do not estimate treatment effects or support functional inference. Original biological execution holds remain unchanged.', fontsize=10)
    save_figure(fig, output, 'r1_library_qc')


def render_x1(rows, output):
    style()
    fig, axes = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={'width_ratios': [1, 1.15]})
    fig.subplots_adjust(left=.15, right=.98, bottom=.28, top=.72, wspace=.68)
    for ax, panel, title in zip(axes, ('multiplicity', 'overlapping_dimensions'),
                               ('A  Records sharing a symbol label', 'B  Overlapping annotation dimensions')):
        selected = [r for r in rows if r['panel'] == panel]
        denominator = selected[0]['denominator']
        bars(ax, [r['category'] for r in selected], [r['count'] for r in selected],
             [r['display'] for r in selected], '#68588b', maximum=denominator)
        ax.set_xticks([0, 13, 26, 39, 52]); ax.set_xlabel('Repeated symbol labels (denominator = 52)', labelpad=10)
        ax.set_title(title, loc='left', fontsize=12, pad=18)
    fig.text(.035, .94, 'X1 | Annotation ambiguity among repeated symbol labels', fontsize=20, weight='bold')
    fig.text(.035, .865, '52 repeated labels span 122 deposited annotation rows. The exact annotation release remains unknown.', fontsize=11)
    fig.text(.035, .19, 'Panel A bins form a partition of the 52 labels. Panel B dimensions overlap: do not add them as mutually exclusive categories.', fontsize=10)
    fig.text(.035, .125, 'A coordinate tuple is (chromosome, strand, start, end). Counts describe deposited annotation records, without remapping or collapsing rows.', fontsize=10)
    fig.text(.035, .06, 'This is technical metadata QC, not expression analysis, named-target ranking or a functional result. Values reuse the frozen X1 summary.', fontsize=10)
    save_figure(fig, output, 'x1_annotation_qc')


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    output = Path(parser.parse_args().output).resolve()
    require(output.parent == ROOT/'analysis/research/runs' and output.is_dir(), 'Fresh runner directory required')
    require(all(p.name in {'receipt.json','stdout.log','stderr.log'} for p in output.iterdir()), 'Existing output artifacts')
    source_bindings(R1, ['library_qc.csv','samples.csv'])
    source_bindings(X1, ['summary.json','repeated_symbols.csv'])
    r1 = r1_values(read_csv(R1/'library_qc.csv'), read_csv(R1/'samples.csv'))
    summary = json.loads((X1/'summary.json').read_text())
    require(summary['repeated_symbol_labels'] == 52 and summary['rows_with_repeated_nonempty_symbols'] == 122, 'Changed fixed annotation scope')
    x1 = x1_values(summary, read_csv(X1/'repeated_symbols.csv'))
    write_csv(output/'r1_plot_values.csv', r1); write_csv(output/'x1_plot_values.csv', x1)
    render_r1(r1, output); render_x1(x1, output)
    with (output/'render_summary.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(scope='Render-only technical QC from reviewed immutable tables',
                       r1_library_order=list(ORDER), r1_metric_values=18, x1_category_values=len(x1),
                       x1_repeated_labels=52, x1_annotation_rows=122,
                       x1_dimensions_overlap=True, animal_identity='unknown',
                       svg_whitespace='Normalized in memory before first write; XML parsed before output hashing',
                       matplotlib=matplotlib.__version__, scientific_acceptance='not_assessed'), stream, indent=2)
        stream.write('\n')
    print('Rendered two technical QC figures and exact plot-value tables; no source analysis rerun.')


if __name__ == '__main__':
    main()
