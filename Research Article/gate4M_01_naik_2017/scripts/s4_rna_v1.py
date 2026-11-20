"""Prospective S4 baseline-adjusted finite-library RNA description."""
from __future__ import annotations
import argparse
import gzip
import io
import json
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from s2_rna_v1 import normalize, contrast, json_write, tsv_write, quantiles, correlation

SAMPLES = [f'GSM{x}' for x in range(2440989, 2441001)]
PHASES = ['B0', 'W6', 'W12']
MARKERS = ['Xist', 'Ddx3y', 'Eif2s3y', 'Kdm5d', 'Uty']
TIE = 1e-10


def compressed_tsv(path, frame):
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding='utf-8', newline='') as text:
                frame.to_csv(text, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')


def annotate(path, genes):
    wanted, found = set(genes), {}
    markers = {name: {} for name in MARKERS}
    with gzip.open(path, 'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 9 or fields[2] != 'gene': continue
            attrs = dict(re.findall(r'(\w+) "([^"]*)"', fields[8]))
            gene, name = attrs.get('gene_id'), attrs.get('gene_name', 'NA')
            record = (name, attrs.get('gene_type', 'NA'), fields[0])
            if gene in wanted:
                if gene in found and found[gene] != record: raise ValueError(f'Ambiguous annotation: {gene}')
                found[gene] = record
            if name in markers:
                if gene in markers[name] and markers[name][gene] != record: raise ValueError(f'Ambiguous marker: {gene}')
                markers[name][gene] = record
    identity = []
    for name in MARKERS:
        hits = markers[name]
        status = 'missing_annotation' if not hits else ('unique_exact_annotation' if len(hits) == 1 else 'ambiguous_symbol')
        identity.append({'requested_name': name, 'status': status,
                         'records': [{'gene_id': gene, 'gene_name': rec[0], 'gene_type': rec[1], 'chromosome': rec[2],
                                      'in_count_universe': gene in wanted} for gene, rec in sorted(hits.items())]})
    return found, identity


def sex_metadata(text):
    parts = [part.strip() for part in text.split('|') if part.split(':', 1)[0].strip().lower() in ['sex', 'gender']]
    return ' | '.join(parts) if parts else 'not reported in selected GEO characteristics'


def sign_flip(a, b):
    return ((a > TIE) & (b < -TIE)) | ((a < -TIE) & (b > TIE))


def logratio(a, b, pseudo=1):
    if pseudo: return np.log2((a + pseudo) / (b + pseudo))
    result = np.full(len(a), np.nan)
    valid = (a > 0) & (b > 0)
    result[valid] = np.log2(a[valid] / b[valid])
    return result


def calculate(raw, mor, total, cpm):
    fields = {}
    for k, phase in enumerate(PHASES):
        sl = slice(4 * k, 4 * k + 4)
        stats, alt = contrast(mor[:, sl]), contrast(total[:, sl])
        for key, values in stats.items(): fields[f'{phase}_{key}'] = values
        fields[f'{phase}_mean_control_total'] = alt['mean_control_mor']
        fields[f'{phase}_mean_exposed_total'] = alt['mean_exposed_mor']
        fields[f'{phase}_log2_effect_total'] = alt['log2_effect_mor']
        fields[f'{phase}_normalization_delta'] = stats['log2_effect_mor'] - alt['log2_effect_mor']
        fields[f'{phase}_norm_sign_flip'] = sign_flip(stats['log2_effect_mor'], alt['log2_effect_mor'])
        fields[f'{phase}_qualified_cpm'] = (cpm[:, sl] >= 1 - TIE).sum(axis=1) >= 2
        fields[f'{phase}_zero_libraries'] = (raw[:, sl] == 0).sum(axis=1)
        fields[f'{phase}_control_zero'] = np.all(raw[:, 4 * k:4 * k + 2] == 0, axis=1)
        fields[f'{phase}_exposed_zero'] = np.all(raw[:, 4 * k + 2:4 * k + 4] == 0, axis=1)
        fields[f'{phase}_all_zero'] = np.all(raw[:, sl] == 0, axis=1)
        fields[f'{phase}_all_library_differences_same_sign'] = (stats['pair_min'] > TIE) | (stats['pair_max'] < -TIE)
    for k, phase in enumerate(PHASES[1:], 1):
        adjusted = fields[f'{phase}_log2_effect_mor'] - fields['B0_log2_effect_mor']
        alternative = fields[f'{phase}_log2_effect_total'] - fields['B0_log2_effect_total']
        fields[f'{phase}_adjusted_mor'] = adjusted
        fields[f'{phase}_adjusted_total'] = alternative
        fields[f'{phase}_adjusted_unregularized'] = fields[f'{phase}_log2_effect_unregularized'] - fields['B0_log2_effect_unregularized']
        fields[f'{phase}_adjustment_norm_delta'] = adjusted - alternative
        fields[f'{phase}_adjustment_norm_sign_flip'] = sign_flip(adjusted, alternative)
        low = fields[f'{phase}_pair_min'] - fields['B0_pair_max']
        high = fields[f'{phase}_pair_max'] - fields['B0_pair_min']
        fields[f'{phase}_adjustment_min'] = low
        fields[f'{phase}_adjustment_max'] = high
        fields[f'{phase}_adjustment_range_includes_zero'] = (low <= TIE) & (high >= -TIE)
        fields[f'{phase}_adjustment_low_mean'] = fields[f'{phase}_regularization_sensitive'] | fields['B0_regularization_sensitive']
        fields[f'{phase}_union_qualified'] = fields[f'{phase}_qualified_cpm'] | fields['B0_qualified_cpm']
        fields[f'{phase}_both_qualified'] = fields[f'{phase}_qualified_cpm'] & fields['B0_qualified_cpm']
        for offset, group in [(0, 'control'), (2, 'exposed')]:
            for suffix in ['mor', 'total']:
                fields[f'{phase}_{group}_wound_baseline_{suffix}'] = logratio(fields[f'{phase}_mean_{group}_{suffix}'], fields[f'B0_mean_{group}_{suffix}'])
            fields[f'{phase}_{group}_wound_baseline_unregularized'] = logratio(fields[f'{phase}_mean_{group}_mor'], fields[f'B0_mean_{group}_mor'], 0)
            combinations = np.log2(mor[:, 4 * k + offset:4 * k + offset + 2] + 1)[:, :, None] - np.log2(mor[:, offset:offset + 2] + 1)[:, None, :]
            fields[f'{phase}_{group}_wound_baseline_min'] = combinations.min(axis=(1, 2))
            fields[f'{phase}_{group}_wound_baseline_max'] = combinations.max(axis=(1, 2))
        if not np.allclose(fields[f'{phase}_exposed_wound_baseline_mor'] - fields[f'{phase}_control_wound_baseline_mor'], adjusted, atol=TIE, rtol=TIE):
            raise ValueError('Adjusted/group-response algebra mismatch')
    qualifications = np.column_stack([fields[f'{phase}_qualified_cpm'] for phase in PHASES])
    fields['global_union_qualified'] = qualifications.any(axis=1)
    fields['all_three_qualified'] = qualifications.all(axis=1)
    return fields


def summarize(frame, phase, mask):
    f = frame.loc[mask]
    n = len(f)
    if not n: return {'genes': 0}
    out = {'genes': n}
    for key in ['B0_log2_effect_mor', f'{phase}_log2_effect_mor', f'{phase}_adjusted_mor',
                f'{phase}_control_wound_baseline_mor', f'{phase}_exposed_wound_baseline_mor']:
        values = f[key].to_numpy()
        out[key + '_quantiles'] = quantiles(values)
        out[key + '_absolute_quantiles'] = quantiles(np.abs(values))
    base, post, adj = (f[key].to_numpy() for key in ['B0_log2_effect_mor', f'{phase}_log2_effect_mor', f'{phase}_adjusted_mor'])
    out['fraction_abs_post_larger_than_baseline'] = float(np.mean(np.abs(post) > np.abs(base) + TIE))
    out['fraction_abs_post_baseline_tied'] = float(np.mean(np.abs(np.abs(post) - np.abs(base)) <= TIE))
    out['fraction_post_adjusted_opposite_nonzero'] = float(np.mean(sign_flip(post, adj)))
    for suffix in ['adjustment_norm_sign_flip', 'adjustment_range_includes_zero', 'adjustment_low_mean']:
        out['fraction_' + suffix] = float(f[f'{phase}_{suffix}'].mean())
    for time in ['B0', phase]:
        out[time + '_fraction_all_zero'] = float(f[f'{time}_all_zero'].mean())
        out[time + '_fraction_group_zero'] = float((f[f'{time}_control_zero'] | f[f'{time}_exposed_zero']).mean())
        out[time + '_fraction_qualified'] = float(f[f'{time}_qualified_cpm'].mean())
    out['fraction_all_eight_zero'] = float((f.B0_all_zero & f[f'{phase}_all_zero']).mean())
    out['adjustment_range_width_quantiles'] = quantiles((f[f'{phase}_adjustment_max'] - f[f'{phase}_adjustment_min']).to_numpy())
    out['abs_adjustment_normalization_delta_quantiles'] = quantiles(np.abs(f[f'{phase}_adjustment_norm_delta'].to_numpy()))
    return out


def select_cases(frame):
    rules = []
    for phase in ['W6', 'W12']:
        for direction, factor in [('maximum', 1), ('minimum', -1)]:
            rules.append((f'{phase} {direction} signed adjusted effect', frame[f'{phase}_union_qualified'], factor * frame[f'{phase}_adjusted_mor']))
    opposite = sign_flip(frame.W6_adjusted_mor, frame.W12_adjusted_mor) & frame.all_three_qualified
    rules.append(('Strongest opposite W6/W12 adjusted directions', opposite, np.minimum(abs(frame.W6_adjusted_mor), abs(frame.W12_adjusted_mor))))
    width6 = (frame.W6_adjustment_max - frame.W6_adjustment_min).where(frame.W6_union_qualified, -np.inf)
    width12 = (frame.W12_adjustment_max - frame.W12_adjustment_min).where(frame.W12_union_qualified, -np.inf)
    rules.append(('Widest adjusted library-combination range', frame.global_union_qualified, np.maximum(width6, width12)))
    selected, missing, used = [], [], set()
    for slot, (reason, mask, score) in enumerate(rules, 1):
        eligible = frame.loc[mask & ~frame.gene_id.isin(used)].copy()
        if eligible.empty:
            missing.append({'slot': slot, 'selection_reason': reason, 'status': 'no eligible unused gene'})
            continue
        eligible['selection_score'] = np.asarray(score)[eligible.index]
        row = eligible.sort_values(['selection_score', 'gene_id'], ascending=[False, True]).iloc[0]
        selected.append({'plot_slot': slot, 'selection_reason': reason, **row.to_dict()})
        used.add(row.gene_id)
    return pd.DataFrame(selected), missing


def run(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    paths = {Path(x['path']).name: root / x['path'] for x in contract['inputs']}
    source = pd.read_csv(paths['library_crosswalk.tsv'], sep='\t', dtype=str, keep_default_na=False)
    if source.gsm.duplicated().any(): raise ValueError('Nonunique source join')
    source = source.set_index('gsm')
    genes, columns, qc = None, [], []
    for j, gsm in enumerate(SAMPLES):
        matches = [p for name, p in paths.items() if name.startswith(gsm + '_') and name.endswith('.tab.gz')]
        if len(matches) != 1: raise ValueError(f'Nonunique input for {gsm}')
        data = pd.read_csv(matches[0], sep='\t', header=None, names=['gene_id', 'count'], dtype={'gene_id': str, 'count': np.int64})
        if len(data) != 47729 or data.gene_id.duplicated().any() or (data['count'] < 0).any(): raise ValueError(f'Invalid count structure: {gsm}')
        if genes is None: genes = data.gene_id.to_numpy()
        elif not np.array_equal(genes, data.gene_id.to_numpy()): raise ValueError('Gene universe/order mismatch')
        record = source.loc[gsm]
        phase, hour = PHASES[j // 4], ['', '6', '12'][j // 4]
        role = 'control' if j % 4 < 2 else 'exposed'
        history = 'control' if role == 'control' else 'prior_inflammation'
        if (record.assay, record.day_label, record.wound_hour_label, record.history_label,
            record.instrument_models, record.library_layouts) != ('RNA-seq', '30', hour, history, 'Illumina HiSeq 2500', 'SINGLE'):
            raise ValueError(f'S1M identity mismatch: {gsm}')
        if record.label_conflicts: raise ValueError(f'Source label conflict: {gsm}')
        qc.append({'gsm': gsm, 'phase': phase, 'role': role,
                   'short_label': f'{phase}_{"C" if role == "control" else "H"}{j % 2 + 1}',
                   'run': record.runs, 'biosample': record.biosamples, 'instrument': record.instrument_models,
                   'layout': record.library_layouts, 'recorded_sex': sex_metadata(record.characteristics),
                   'source_compartment': record.source_compartment, 'source_file': matches[0].name})
        columns.append(data['count'].to_numpy())
    raw = np.column_stack(columns)
    mor, total, cpm, sf, tf, basis = normalize(raw)
    if not np.isfinite(mor).all() or not np.isfinite(total).all(): raise ValueError('Nonfinite normalization')
    annotations, marker_identity = annotate(paths['gencode.vM9.annotation.gtf.gz'], genes)
    fields = {'gene_id': genes, 'gene_name': [annotations.get(g, ('NA', 'NA', 'NA'))[0] for g in genes],
              'gene_type': [annotations.get(g, ('NA', 'NA', 'NA'))[1] for g in genes],
              'chromosome': [annotations.get(g, ('NA', 'NA', 'NA'))[2] for g in genes], **calculate(raw, mor, total, cpm)}
    effects = pd.DataFrame(fields)
    compressed_tsv(output / 'gene_effects.tsv.gz', effects)
    values = {'gene_id': genes}
    for j, gsm in enumerate(SAMPLES):
        for name, matrix in [('raw', raw), ('mor', mor), ('total', total), ('cpm', cpm)]: values[gsm + '__' + name] = matrix[:, j]
        qc[j].update({'gene_count_total': int(raw[:, j].sum()), 'detected_genes': int((raw[:, j] > 0).sum()),
                      'mor_size_factor': sf[j], 'total_count_size_factor': tf[j], 'mor_reference_genes': basis})
    compressed_tsv(output / 'gene_values.tsv.gz', pd.DataFrame(values))
    qc = pd.DataFrame(qc)
    tsv_write(output / 'sample_qc.tsv', qc)
    correlations = np.corrcoef(np.log2(mor[effects.global_union_qualified] + 1).T)
    tsv_write(output / 'sample_correlation.tsv', pd.DataFrame({'gsm': SAMPLES, **{gsm: correlations[:, j] for j, gsm in enumerate(SAMPLES)}}))
    index = {gene: i for i, gene in enumerate(genes)}
    marker_rows = []
    for item in marker_identity:
        for rec in item['records'] or [{'gene_id': 'NA', 'chromosome': 'NA', 'gene_type': 'NA', 'in_count_universe': False}]:
            for j, gsm in enumerate(SAMPLES):
                row = {'requested_name': item['requested_name'], 'annotation_status': item['status'],
                       'gene_id': rec['gene_id'], 'gene_type': rec['gene_type'], 'chromosome': rec['chromosome'],
                       'in_count_universe': rec['in_count_universe'], 'gsm': gsm, 'phase': qc.iloc[j].phase,
                       'role': qc.iloc[j].role, 'recorded_sex': qc.iloc[j].recorded_sex}
                i = index.get(rec['gene_id'])
                for name, matrix in [('raw', raw), ('mor', mor), ('total', total), ('cpm', cpm)]: row[name] = matrix[i, j] if i is not None else np.nan
                marker_rows.append(row)
    markers = pd.DataFrame(marker_rows)
    tsv_write(output / 'marker_qc.tsv', markers)
    cases, missing_cases = select_cases(effects)
    tsv_write(output / 'selected_cases.tsv', cases)
    summary = {'analysis_id': contract['analysis_id'], 'input_genes': len(genes), 'libraries': SAMPLES,
               'joint_mor_reference_genes': basis, 'global_union_genes': int(effects.global_union_qualified.sum()),
               'all_three_qualified_genes': int(effects.all_three_qualified.sum()), 'comparisons': {},
               'cross_time': {}, 'unfilled_case_slots': missing_cases,
               'recorded_sex_labels': qc.recorded_sex.value_counts().to_dict(),
               'no_sex_assignment_exclusion_or_pairing': True, 'no_population_inference': True,
               'absolute_RNA_or_repair_not_measured': True}
    for phase in ['W6', 'W12']:
        summary['comparisons'][phase] = {name: summarize(effects, phase, mask) for name, mask in
             [('all_genes', np.ones(len(genes), dtype=bool)), ('comparison_union', effects[f'{phase}_union_qualified']),
              ('baseline_intersection', effects[f'{phase}_both_qualified'])]}
    for name, mask in [('global_union', effects.global_union_qualified), ('all_three_qualified', effects.all_three_qualified)]:
        a, b = effects.loc[mask, 'W6_adjusted_mor'], effects.loc[mask, 'W12_adjusted_mor']
        raw6, raw12 = effects.loc[mask, 'W6_log2_effect_mor'], effects.loc[mask, 'W12_log2_effect_mor']
        summary['cross_time'][name] = {'genes': int(mask.sum()), 'pearson_adjusted': correlation(a, b),
             'spearman_adjusted': correlation(a.rank(), b.rank()), 'pearson_unadjusted': correlation(raw6, raw12),
             'spearman_unadjusted': correlation(raw6.rank(), raw12.rank()),
             'fraction_opposite_nonzero': float(sign_flip(a, b).mean()) if len(a) else None,
             'shared_baseline_can_induce_correlation': True}
    json_write(output / 'summary.json', summary)
    json_write(output / 'annotation_coverage.json', {'source': 'GENCODE M9 reference-chromosome GTF',
               'exact_version_matches': len(annotations), 'unmatched': len(genes) - len(annotations),
               'unmatched_ids': [g for g in genes if g not in annotations], 'markers': marker_identity})
    from s4_plot_v1 import plot_all
    plot_all(output, effects, mor, qc, correlations, markers, cases, summary)
    import matplotlib
    json_write(output / 'runtime.json', {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
               'matplotlib': matplotlib.__version__, 'stochastic_steps': 'none', 'shared_helper': 'unchanged frozen s2_rna_v1.py'})
    subprocess.run([sys.executable, str(Path(__file__).with_name('s4_verify_v1.py')), '--contract', str(contract_path.resolve()),
                    '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'analysis_id': contract['analysis_id'], 'genes': len(genes), 'verification': 'passed'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.contract, args.output)
