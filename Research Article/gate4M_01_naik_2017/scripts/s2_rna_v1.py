"""S2 finite-library RNA description; execute only through the frozen runner."""
from __future__ import annotations
import argparse
import gzip
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import pandas as pd

SAMPLES = [f'GSM{x}' for x in range(2440985, 2440993)]
NUMERIC_TIE = 1e-10


def json_write(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode())


def tsv_write(path, frame):
    frame.to_csv(path, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')


def normalize(matrix):
    positive = np.all(matrix > 0, axis=1)
    if not positive.any():
        raise ValueError('No all-positive genes for the prespecified MOR reference')
    logs = np.log(matrix[positive])
    log_factors = np.median(logs - logs.mean(axis=1, keepdims=True), axis=0)
    mor_factors = np.exp(log_factors - log_factors.mean())
    totals = matrix.sum(axis=0)
    if np.any(totals <= 0):
        raise ValueError('Empty count library')
    total_factors = totals / np.exp(np.log(totals).mean())
    return matrix / mor_factors, matrix / total_factors, matrix / totals * 1e6, mor_factors, total_factors, int(positive.sum())


def contrast(matrix):
    control, exposed = matrix[:, :2], matrix[:, 2:]
    cm, em = control.mean(axis=1), exposed.mean(axis=1)
    log_control, log_exposed = np.log2(control + 1), np.log2(exposed + 1)
    pairs = log_exposed[:, :, None] - log_control[:, None, :]
    unregularized = np.full(len(matrix), np.nan)
    valid = (cm > 0) & (em > 0)
    unregularized[valid] = np.log2(em[valid] / cm[valid])
    return {'mean_control_mor': cm, 'mean_exposed_mor': em,
            'log2_effect_mor': np.log2((em + 1) / (cm + 1)),
            'log2_effect_unregularized': unregularized,
            'control_log_range': np.ptp(log_control, axis=1),
            'exposed_log_range': np.ptp(log_exposed, axis=1),
            'pair_min': pairs.min(axis=(1, 2)), 'pair_max': pairs.max(axis=(1, 2)),
            'regularization_sensitive': np.minimum(cm, em) < 1 - NUMERIC_TIE}


def correlation(a, b):
    if len(a) < 2 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def quantiles(values):
    return {str(q): float(np.quantile(values, q)) for q in [0, .25, .5, .75, .9, .95, 1]}


def summaries(effects, mask):
    frame = effects.loc[mask]
    if frame.empty:
        return {'genes': 0}
    a, b = frame.D6_log2_effect_mor.to_numpy(), frame.D30_log2_effect_mor.to_numpy()
    result = {'genes': len(frame), 'D6_effect_quantiles': quantiles(a), 'D30_effect_quantiles': quantiles(b),
              'D6_abs_effect_quantiles': quantiles(np.abs(a)), 'D30_abs_effect_quantiles': quantiles(np.abs(b)),
              'fraction_abs_D30_smaller': float(np.mean(np.abs(b) < np.abs(a) - NUMERIC_TIE)),
              'fraction_abs_effect_tied': float(np.mean(np.abs(np.abs(b) - np.abs(a)) <= NUMERIC_TIE)),
              'fraction_sign_agreement_nonzero': float(np.mean(((a > NUMERIC_TIE) & (b > NUMERIC_TIE)) | ((a < -NUMERIC_TIE) & (b < -NUMERIC_TIE)))),
              'pearson_effect_profiles': correlation(a, b),
              'spearman_effect_profiles': correlation(pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy())}
    for time in ['D6', 'D30']:
        delta = frame[f'{time}_normalization_delta'].to_numpy()
        low, high = frame[f'{time}_pair_min'].to_numpy(), frame[f'{time}_pair_max'].to_numpy()
        result[time] = {'abs_normalization_delta_quantiles': quantiles(np.abs(delta)),
                        'fraction_norm_sign_flip': float(frame[f'{time}_norm_sign_flip'].mean()),
                        'fraction_pair_range_crosses_zero': float(np.mean((low <= NUMERIC_TIE) & (high >= -NUMERIC_TIE))),
                        'pair_range_width_quantiles': quantiles(high - low),
                        'fraction_regularization_sensitive': float(frame[f'{time}_regularization_sensitive'].mean()),
                        'fraction_all_zero': float(frame[f'{time}_all_zero'].mean()),
                        'fraction_qualified_this_time': float(frame[f'{time}_qualified_cpm'].mean()),
                        'fraction_group_zero': float((frame[f'{time}_control_zero'] | frame[f'{time}_exposed_zero']).mean())}
    return result


def annotation(path, genes):
    wanted = set(genes)
    found = {}
    with gzip.open(path, 'rt') as handle:
        for line in handle:
            if line.startswith('#'):
                continue
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 9 or fields[2] != 'gene':
                continue
            attrs = dict(re.findall(r'(\w+) "([^"]*)"', fields[8]))
            gene = attrs.get('gene_id')
            if gene not in wanted:
                continue
            record = (attrs.get('gene_name', 'NA'), attrs.get('gene_type', 'NA'))
            if gene in found and found[gene] != record:
                raise ValueError(f'Conflicting exact-version annotation: {gene}')
            found[gene] = record
    return found


def select_cases(effects):
    eligible = effects[effects.eligible_union].copy()
    scores = [
        ('D6 maximum signed effect', eligible.D6_log2_effect_mor),
        ('D6 minimum signed effect', -eligible.D6_log2_effect_mor),
        ('D30 maximum signed effect', eligible.D30_log2_effect_mor),
        ('D30 minimum signed effect', -eligible.D30_log2_effect_mor),
        ('Largest normalization discrepancy', np.maximum(abs(eligible.D6_normalization_delta), abs(eligible.D30_normalization_delta))),
        ('Widest library effect range', np.maximum(eligible.D6_pair_max - eligible.D6_pair_min, eligible.D30_pair_max - eligible.D30_pair_min)),
    ]
    used, selected = set(), []
    for reason, score in scores:
        ranked = eligible.assign(selection_score=np.asarray(score)).sort_values(['selection_score', 'gene_id'], ascending=[False, True])
        row = ranked.loc[~ranked.gene_id.isin(used)].iloc[0]
        used.add(row.gene_id)
        selected.append({'selection_reason': reason, **row.to_dict()})
    return pd.DataFrame(selected)


def run(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    paths = {Path(x['path']).name: root / x['path'] for x in contract['inputs']}
    source = pd.read_csv(paths['library_crosswalk.tsv'], sep='\t', keep_default_na=False, dtype=str).set_index('gsm')
    columns, genes, qc = [], None, []
    for index, gsm in enumerate(SAMPLES):
        matched = [p for name, p in paths.items() if name.startswith(gsm + '_') and name.endswith('.tab.gz')]
        if len(matched) != 1:
            raise ValueError(f'Nonunique declared input for {gsm}')
        frame = pd.read_csv(matched[0], sep='\t', header=None, names=['gene_id', 'count'], dtype={'gene_id': str, 'count': np.int64})
        if frame.gene_id.duplicated().any() or len(frame) != 47729 or (frame['count'] < 0).any():
            raise ValueError(f'Invalid source structure for {gsm}')
        if genes is None:
            genes = frame.gene_id.to_numpy()
        elif not np.array_equal(genes, frame.gene_id.to_numpy()):
            raise ValueError('Exact versioned identifier/order mismatch')
        time = 'D6' if index < 4 else 'D30'
        role = 'control' if index % 4 < 2 else 'exposed'
        record = source.loc[gsm]
        if record.assay != 'RNA-seq' or record.day_label != time[1:] or record.wound_hour_label:
            raise ValueError(f'Unexpected S1M assay/time/wound identity for {gsm}')
        expected_history = 'control' if role == 'control' else 'prior_inflammation'
        if record.history_label != expected_history:
            raise ValueError(f'S1M condition mismatch for {gsm}')
        columns.append(frame['count'].to_numpy())
        qc.append({'gsm': gsm, 'time': time, 'role': role,
                   'condition': 'control' if role == 'control' else 'acute_inflamed' if time == 'D6' else 'recovered_baseline_history',
                   'short_label': f'{time}_{"C" if role == "control" else "A" if time == "D6" else "H"}{index % 2 + 1}',
                   'run': record.runs, 'biosample': record.biosamples,
                   'instrument': record.instrument_models, 'layout': record.library_layouts,
                   'source_file': matched[0].name})
    counts = np.column_stack(columns).astype(np.float64)
    mor, total, cpm = (np.empty_like(counts) for _ in range(3))
    effects = pd.DataFrame({'gene_id': genes})
    values = pd.DataFrame({'gene_id': genes})
    for time, offset in [('D6', 0), ('D30', 4)]:
        part = counts[:, offset:offset + 4]
        y, z, per_million, sf, tf, basis = normalize(part)
        mor[:, offset:offset + 4], total[:, offset:offset + 4], cpm[:, offset:offset + 4] = y, z, per_million
        stats = contrast(y)
        total_effect = np.log2((z[:, 2:].mean(axis=1) + 1) / (z[:, :2].mean(axis=1) + 1))
        for name, val in stats.items(): effects[f'{time}_{name}'] = val
        effects[f'{time}_log2_effect_total'] = total_effect
        effects[f'{time}_normalization_delta'] = stats['log2_effect_mor'] - total_effect
        primary_effect = stats['log2_effect_mor']
        effects[f'{time}_norm_sign_flip'] = ((primary_effect > NUMERIC_TIE) & (total_effect < -NUMERIC_TIE)) | ((primary_effect < -NUMERIC_TIE) & (total_effect > NUMERIC_TIE))
        effects[f'{time}_qualified_cpm'] = (per_million >= 1 - NUMERIC_TIE).sum(axis=1) >= 2
        effects[f'{time}_zero_libraries'] = (part == 0).sum(axis=1)
        effects[f'{time}_control_zero'] = (part[:, :2] == 0).all(axis=1)
        effects[f'{time}_exposed_zero'] = (part[:, 2:] == 0).all(axis=1)
        effects[f'{time}_all_zero'] = (part == 0).all(axis=1)
        effects[f'{time}_all_library_differences_same_sign'] = (stats['pair_min'] > NUMERIC_TIE) | (stats['pair_max'] < -NUMERIC_TIE)
        for local in range(4):
            j = offset + local
            qc[j].update({'gene_count_total': int(part[:, local].sum()),
                          'detected_genes': int((part[:, local] > 0).sum()),
                          'zero_genes': int((part[:, local] == 0).sum()),
                          'mor_size_factor': float(sf[local]), 'total_count_size_factor': float(tf[local]),
                          'mor_reference_genes': basis,
                          'top10_gene_count_fraction': float(np.sort(part[:, local])[-10:].sum() / part[:, local].sum())})
            values[f'{SAMPLES[j]}__mor'] = y[:, local]
            values[f'{SAMPLES[j]}__total'] = z[:, local]
            values[f'{SAMPLES[j]}__cpm'] = per_million[:, local]
    effects['eligible_union'] = effects.D6_qualified_cpm | effects.D30_qualified_cpm
    effects['eligible_both'] = effects.D6_qualified_cpm & effects.D30_qualified_cpm
    effects['descriptive_D30_minus_D6_effect'] = effects.D30_log2_effect_mor - effects.D6_log2_effect_mor
    annotated = annotation(paths['gencode.vM9.annotation.gtf.gz'], genes)
    effects.insert(1, 'gene_name', [annotated.get(gene, ('NA', 'NA'))[0] for gene in genes])
    effects.insert(2, 'gene_type', [annotated.get(gene, ('NA', 'NA'))[1] for gene in genes])
    sample_qc = pd.DataFrame(qc)
    cases = select_cases(effects)
    correlations = np.corrcoef(np.log2(mor[effects.eligible_union] + 1).T)
    tsv_write(output / 'gene_effects.tsv', effects)
    with (output / 'gene_values.tsv.gz').open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding='utf-8', newline='') as text:
                values.to_csv(text, sep='\t', index=False, float_format='%.17g', na_rep='NA', lineterminator='\n')
    tsv_write(output / 'sample_qc.tsv', sample_qc)
    tsv_write(output / 'sample_correlation.tsv', pd.DataFrame(correlations, columns=SAMPLES).assign(gsm=SAMPLES)[['gsm'] + SAMPLES])
    tsv_write(output / 'selected_cases.tsv', cases)
    summary = {'analysis_id': contract['analysis_id'], 'input_genes': len(genes), 'libraries': SAMPLES,
               'all_genes': summaries(effects, np.ones(len(effects), dtype=bool)),
               'qualified_union': summaries(effects, effects.eligible_union),
               'qualified_both': summaries(effects, effects.eligible_both),
               'D6_only_qualified': int((effects.D6_qualified_cpm & ~effects.D30_qualified_cpm).sum()),
               'D30_only_qualified': int((effects.D30_qualified_cpm & ~effects.D6_qualified_cpm).sum()),
               'no_population_inference': True, 'absolute_RNA_not_measured': True,
               'cross_time_platform_layout_qualified': True}
    json_write(output / 'summary.json', summary)
    json_write(output / 'annotation_coverage.json', {'source': 'GENCODE M9 reference-chromosome GTF',
               'exact_version_matches': len(annotated), 'unmatched': len(genes) - len(annotated),
               'unmatched_ids': [gene for gene in genes if gene not in annotated]})
    from s2_plot_v1 import plot_all
    plot_all(output, effects, mor, sample_qc, correlations, cases)
    import matplotlib
    json_write(output / 'runtime.json', {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
                                       'matplotlib': matplotlib.__version__, 'stochastic_steps': 'none'})
    subprocess.run([sys.executable, str(Path(__file__).with_name('s2_verify_v1.py')),
                    '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'analysis_id': contract['analysis_id'], 'genes': len(genes),
                      'qualified_union': int(effects.eligible_union.sum()), 'verification': 'passed'}))


def self_test():
    matrix = np.array([[1, 2, 4, 8], [2, 4, 8, 16], [0, 0, 0, 0]], dtype=float)
    y, z, cpm, sf, tf, basis = normalize(matrix)
    assert basis == 2 and np.allclose(y[:, :1], y) and np.allclose(z[:, :1], z)
    assert np.isclose(np.prod(sf), 1) and np.isclose(np.prod(tf), 1)
    assert np.allclose(cpm.sum(axis=0), 1e6)
    stats = contrast(y)
    assert np.allclose(stats['log2_effect_mor'], 0) and np.isnan(stats['log2_effect_unregularized'][-1])
    asymmetric = np.array([[0., 2., 4., 8.]])
    result = contrast(asymmetric)
    assert np.isclose(result['log2_effect_mor'][0], math.log2(7 / 2))
    assert np.isclose(result['pair_min'][0], math.log2(5 / 3))
    assert np.isclose(result['pair_max'][0], math.log2(9))
    print('Synthetic S2 normalization/contrast checks passed; research data not read.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test: self_test()
    elif args.contract and args.output and args.output.is_dir(): run(args.contract, args.output)
    else: parser.error('Use the research runner with a frozen --contract and --output directory')
