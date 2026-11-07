"""Fixed-candidate descriptive profiles from the selected Peeters rlog release."""
import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / 'raw_data/dupage_candidate_followup_20261107'
CANDIDATES = ['Tigit', 'Prdm1', 'Ccr2', 'Igfbp4']
ANCHORS = ['Areg', 'Il2ra', 'Igf1r']
GENES = CANDIDATES + ANCHORS
GROUPS = ['WT_N', 'Y641F_N', 'WT_D4', 'Y641F_D4']
SAMPLES = [f'{g}_r{i}' for g in GROUPS for i in range(1, 4)]
CONTRASTS = ['gain_N', 'gain_D4', 'activation_WT', 'activation_Y641F', 'interaction']
BLUE, ORANGE = '#0072B2', '#D55E00'


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


def sign(value):
    return int(value > 0) - int(value < 0)


def contrast(values, omit=None):
    m = {g: float(np.mean([values[s] for s in SAMPLES if s.startswith(g + '_r') and s != omit])) for g in GROUPS}
    result = {'gain_N': m['Y641F_N'] - m['WT_N'],
              'gain_D4': m['Y641F_D4'] - m['WT_D4'],
              'activation_WT': m['WT_D4'] - m['WT_N'],
              'activation_Y641F': m['Y641F_D4'] - m['Y641F_N']}
    result['interaction'] = result['gain_D4'] - result['gain_N']
    return m, result


def metadata():
    records, current = [], None
    with gzip.open(RAW / 'GSE262130_family.soft.gz', 'rt', encoding='utf-8') as stream:
        for line in stream:
            if line.startswith('^SAMPLE = '):
                current = {'gsm': line.strip().split(' = ', 1)[1]}
                records.append(current)
            elif current is not None and line.startswith('!Sample_title = '):
                current['title'] = line.strip().split(' = ', 1)[1]
            elif current is not None and line.startswith('!Sample_characteristics_ch1 = '):
                key, value = line.strip().split(' = ', 1)[1].split(': ', 1)
                current[key] = value
    for row in records:
        genotype = {'WT': 'WT', 'Ezh2-Y641F': 'Y641F'}[row['genotype']]
        state = {'naïve': 'N', 'activated (in vitro)': 'D4'}[row['treatment']]
        replicate = re.search(r'rep([123])$', row['title']).group(1)
        row['matrix_sample'] = f'{genotype}_{state}_r{replicate}'
        row['animal_or_pool'] = 'unknown'
    assert len(records) == 12 and {r['matrix_sample'] for r in records} == set(SAMPLES)
    return records


def save(fig, out, name):
    for suffix in ['png', 'pdf', 'svg']:
        fig.savefig(out / f'{name}.{suffix}', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    samples = metadata()
    write_tsv(out / 'sample_metadata.tsv', samples,
              ['gsm', 'title', 'tissue', 'cell type', 'genotype', 'treatment', 'matrix_sample', 'animal_or_pool'])
    selected = {g: [] for g in GENES}
    with gzip.open(RAW / 'GSE262130_rld_sig_up.txt.gz', 'rt', encoding='utf-8') as stream:
        reader = csv.DictReader(stream, delimiter='\t')
        assert len(reader.fieldnames) == 14 and set(reader.fieldnames) == {'Genes', 'Gene_names'} | set(SAMPLES)
        total_rows = 0
        for row in reader:
            total_rows += 1
            assert None not in row and all(v is not None for v in row.values()), 'Malformed source row'
            if row['Gene_names'] in selected:
                selected[row['Gene_names']].append(row)
    availability, observations, sensitivity, summaries, values_by_gene = [], [], [], [], {}
    for gene in GENES:
        rows = selected[gene]
        status = 'unique' if len(rows) == 1 else ('absent_from_selected_release' if not rows else 'ambiguous_symbol')
        availability.append({'gene': gene, 'role': 'candidate' if gene in CANDIDATES else 'context_anchor',
                             'status': status, 'source_rows': len(rows), 'ensembl_ids': ';'.join(r['Genes'] for r in rows)})
        if status != 'unique':
            continue
        values = {s: float(rows[0][s]) for s in SAMPLES}
        assert all(math.isfinite(v) for v in values.values()), gene
        values_by_gene[gene] = values
        for sample, value in values.items():
            observations.append({'gene': gene, 'ensembl_id': rows[0]['Genes'], 'sample': sample,
                                 'group': sample.rsplit('_r', 1)[0], 'rlog': value})
        primary_means, primary = contrast(values)
        configs = []
        for omitted in [None] + SAMPLES:
            _, contrasts = contrast(values, omitted)
            configs.append(contrasts)
            for name in CONTRASTS:
                sensitivity.append({'gene': gene, 'configuration': 'primary' if omitted is None else f'omit_{omitted}',
                                    'contrast': name, 'value': contrasts[name]})
        for name in CONTRASTS:
            result = [x[name] for x in configs]
            summaries.append({'gene': gene, 'contrast': name, 'primary': primary[name],
                              'sensitivity_min': min(result), 'sensitivity_max': max(result),
                              'sign_stable_13': all(sign(x) == sign(primary[name]) for x in result),
                              **{g + '_mean': primary_means[g] for g in GROUPS}})
    write_tsv(out / 'availability.tsv', availability, ['gene', 'role', 'status', 'source_rows', 'ensembl_ids'])
    write_tsv(out / 'observations.tsv', observations, ['gene', 'ensembl_id', 'sample', 'group', 'rlog'])
    write_tsv(out / 'sensitivity.tsv', sensitivity, ['gene', 'configuration', 'contrast', 'value'])
    write_tsv(out / 'contrasts.tsv', summaries,
              ['gene', 'contrast', 'primary', 'sensitivity_min', 'sensitivity_max', 'sign_stable_13'] + [g + '_mean' for g in GROUPS])
    with (ROOT / 'analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv').open(encoding='utf-8', newline='') as stream:
        old = {r['gene_id']: r for r in csv.DictReader(stream, delimiter='\t') if r['gene_id'] in GENES}
    lookup = {(r['gene'], r['contrast']): r for r in summaries}
    comparison = []
    for gene in GENES:
        for external, original in [('gain_N', 'delta_high'), ('gain_D4', 'delta_low'), ('interaction', 'interaction')]:
            current = lookup.get((gene, external))
            du = float(old[gene][original]) if gene in old else None
            pe = current['primary'] if current else None
            label = 'unavailable'
            if du is not None and pe is not None:
                label = 'opposite' if sign(du) * sign(pe) < 0 else ('same' if sign(du) * sign(pe) > 0 else 'zero')
            comparison.append({'gene': gene, 'dupage_contrast': original, 'dupage_mean_log_fpkm1': du,
                               'peeters_contrast': external, 'peeters_mean_rlog_difference': pe,
                               'peeters_sign_stable_13': current['sign_stable_13'] if current else '',
                               'direction_relation_only': label})
    write_tsv(out / 'direction_comparison.tsv', comparison, list(comparison[0]))
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'legend.frameon': False})
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.subplots_adjust(left=.09, right=.98, bottom=.14, top=.88, hspace=.55, wspace=.3)
    for ax, gene in zip(axes.flat, CANDIDATES):
        ax.set_title(gene, loc='left', weight='bold')
        if gene not in values_by_gene:
            ax.text(.5, .5, 'Unavailable in selected release\nNot a null expression result', ha='center', transform=ax.transAxes)
        else:
            for x, group in enumerate(GROUPS):
                vals = [values_by_gene[gene][f'{group}_r{i}'] for i in range(1, 4)]
                color = BLUE if group.startswith('WT') else ORANGE
                ax.scatter(np.array([-.12, 0, .12]) + x, vals, color=color, s=36)
                ax.plot([x-.23, x+.23], [np.mean(vals)]*2, color='black', linewidth=1.4)
        ax.set_xticks(range(4), ['WT\nfresh', 'Y641F\nfresh', 'WT\nday 4', 'Y641F\nday 4'])
        ax.set_ylabel('Published rlog expression')
    fig.suptitle('EZH2 gain-context profiles of the four candidate genes', weight='bold', y=.97)
    fig.text(.5, .925, 'Peeters 2024 / GSE262130 | fixed candidates; authors’ selected-gene matrix', ha='center', fontsize=10)
    fig.text(.025, .025, 'Dots: recorded libraries (3/group), not verified independent mice. Black bars: means.\nFresh sorting versus four-day culture; no paired trajectories or population inference.', fontsize=9)
    save(fig, out, 'fig05_candidate_profiles')
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.subplots_adjust(left=.1, right=.98, bottom=.24, top=.79, wspace=.45)
    for ax in axes:
        ax.axvline(0, color='#777777', linestyle='--', linewidth=.8)
        ax.set_yticks(range(4), CANDIDATES)
        ax.invert_yaxis()
    for i, gene in enumerate(CANDIDATES):
        for offset, original, ext, color in [(-.13, 'delta_high', 'gain_N', BLUE), (.13, 'delta_low', 'gain_D4', ORANGE)]:
            axes[0].scatter(float(old[gene][original]), i+offset, color=color, s=40)
            if (gene, ext) in lookup:
                row = lookup[(gene, ext)]
                axes[1].plot([row['sensitivity_min'], row['sensitivity_max']], [i+offset]*2, color=color, linewidth=2)
                axes[1].scatter(row['primary'], i+offset, color=color, s=40)
    axes[0].set_title('A  DuPage: Ezh2 loss (KO − HET)', loc='left', weight='bold')
    axes[0].set_xlabel('Difference in mean log2(FPKM + 1)')
    axes[1].set_title('B  Peeters: Ezh2 gain (Y641F − WT)', loc='left', weight='bold')
    axes[1].set_xlabel('Difference in mean published rlog expression')
    for ax, labels in zip(axes, [('CD62L high', 'CD62L low'), ('Freshly sorted', 'Four-day culture')]):
        for color, label in zip([BLUE, ORANGE], labels): ax.scatter([], [], color=color, label=label)
        ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.03), ncol=2, fontsize=9)
    fig.suptitle('Cross-study direction check — different interventions and scales', y=.98, weight='bold')
    fig.text(.025, .035, 'Points: primary contrasts. Panel B lines: primary + 12 library-omission range, not confidence intervals.\nCompare signs only; states, genotype controls and normalization differ. Opposite direction is not causal validation.', fontsize=9)
    save(fig, out, 'fig06_candidate_direction_context')
    manifest = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.iterdir()) if f.suffix in {'.png', '.pdf', '.svg'}}
    (out / 'figure_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    summary = {'analysis_id': 'Dp1.candidate_followup_v1', 'source_rows_selected_by_authors': total_rows,
               'candidates': CANDIDATES, 'context_anchors': ANCHORS, 'availability': availability,
               'library_count': 12, 'independent_animal_count': None, 'sensitivity_configurations': 13,
               'new_inferential_tests': False, 'validation_scope': 'none',
               'limit': 'Selected published rlog matrix; descriptive context comparison, not independent validation or function.',
               'runtime': {'numpy': np.__version__, 'matplotlib': matplotlib.__version__}}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'available': [x['gene'] for x in availability if x['status'] == 'unique'], 'figures': 2}))


if __name__ == '__main__':
    main()
