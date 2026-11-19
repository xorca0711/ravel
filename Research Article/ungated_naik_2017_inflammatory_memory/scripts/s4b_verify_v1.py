"""Independent stdlib verification of S4B against immutable S4 output values."""
import argparse
import csv
import gzip
import itertools
import json
import math
from pathlib import Path

TIE = 1e-10
BASE = ['GSM2440989', 'GSM2440990', 'GSM2440991', 'GSM2440992']
REFERENCES = {'c2_h2': (1, 3), 'c1_h1': (0, 2)}
FLAGS = ['W6_union_qualified', 'W6_both_qualified', 'W12_union_qualified', 'W12_both_qualified', 'global_union_qualified', 'all_three_qualified']


def read_rows(path):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8', newline='') as handle:
        yield from csv.DictReader(handle, delimiter='\t')


def numeric(value):
    return math.nan if value == 'NA' else float(value)


def ratio(h, c, pseudocount):
    if pseudocount == 0 and (h <= 0 or c <= 0): return math.nan
    return math.log2((h + pseudocount) / (c + pseudocount))


def flip(a, b):
    return (a > TIE and b < -TIE) or (a < -TIE and b > TIE)


def quantile(values, q):
    position = q * (len(values) - 1)
    lo, hi = math.floor(position), math.ceil(position)
    return values[lo] + (values[hi] - values[lo]) * (position - lo)


def verify(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    paths = {Path(item['path']).name: root / item['path'] for item in contract['inputs']}
    upstream_summary = json.loads(paths['summary.json'].read_text())
    summary = json.loads((output / 'summary.json').read_text())
    checks, max_error = 0, 0.0

    def equal(actual, expected, label):
        nonlocal checks, max_error
        checks += 1
        if isinstance(expected, bool):
            assert actual == str(expected) or (isinstance(actual, bool) and actual is expected), (label, actual, expected)
        elif isinstance(expected, (int, float)):
            got = numeric(actual) if isinstance(actual, str) else actual
            if math.isnan(expected):
                assert math.isnan(got), (label, actual, 'NA')
            else:
                assert math.isfinite(got), (label, actual, expected)
                error = abs(got - expected) / max(1, abs(expected))
                max_error = max(max_error, error)
                assert error <= TIE, (label, actual, expected, error)
        else:
            assert actual == expected, (label, actual, expected)

    selected_source = list(read_rows(paths['selected_cases.tsv']))
    selected_ids = [row['gene_id'] for row in selected_source]
    assert len(selected_ids) == len(set(selected_ids)) == 6
    selected_expected = {}
    pools = {(phase, universe, ref): {'primary': [], 'alternative': [], 'shift': [], 'flip': 0, 'norm_flip': 0, 'zero': 0, 'low': 0}
             for phase in ['W6', 'W12'] for universe in ['all_genes', 'comparison_union', 'baseline_intersection'] for ref in REFERENCES}
    seen = set()
    rows = itertools.zip_longest(read_rows(paths['gene_effects.tsv.gz']), read_rows(paths['gene_values.tsv.gz']), read_rows(output / 'reference_effects.tsv.gz'))
    for upstream, values, actual in rows:
        assert upstream is not None and values is not None and actual is not None, 'row-count mismatch'
        gene = upstream['gene_id']
        assert gene not in seen
        seen.add(gene)
        equal(values['gene_id'], gene, 'value order')
        expected = {'gene_id': gene, 'gene_name': upstream['gene_name']}
        for flag in FLAGS:
            assert upstream[flag] in ('True', 'False')
            expected[flag] = upstream[flag] == 'True'
        mor = [float(values[gsm + '__mor']) for gsm in BASE]
        total = [float(values[gsm + '__total']) for gsm in BASE]
        raw = [int(values[gsm + '__raw']) for gsm in BASE]
        assert all(math.isfinite(x) and x >= 0 for x in mor + total + raw)
        for norm in ['mor', 'total', 'unregularized']:
            v = total if norm == 'total' else mor
            pseudocount = 0 if norm == 'unregularized' else 1
            baseline = ratio((v[2] + v[3]) / 2, (v[0] + v[1]) / 2, pseudocount)
            equal(upstream['B0_log2_effect_' + norm], baseline, gene + ': frozen primary baseline')
            expected['B0_primary_' + norm] = baseline
            for phase in ['W6', 'W12']:
                post = numeric(upstream[phase + '_log2_effect_' + norm])
                expected[phase + '_post_' + norm] = post
                expected[phase + '_primary_' + norm] = post - baseline
                equal(upstream[phase + '_adjusted_' + norm], post - baseline, gene + ': frozen adjustment')
            for ref, (c, h) in REFERENCES.items():
                alternative = ratio(v[h], v[c], pseudocount)
                expected['B0_' + ref + '_' + norm] = alternative
                shift = baseline - alternative
                expected[ref + '_adjusted_shift_' + norm] = shift
                for phase in ['W6', 'W12']:
                    adjusted = expected[phase + '_post_' + norm] - alternative
                    expected[phase + '_' + ref + '_' + norm] = adjusted
                    if math.isfinite(adjusted) and math.isfinite(expected[phase + '_primary_' + norm]):
                        equal(adjusted - expected[phase + '_primary_' + norm], shift, gene + ': fixed-time shift')
        expected['primary_reference_low_mor'] = min((mor[0] + mor[1]) / 2, (mor[2] + mor[3]) / 2) < 1 - TIE
        expected['primary_reference_any_zero'] = (raw[0] + raw[1] == 0) or (raw[2] + raw[3] == 0)
        equal(upstream['B0_regularization_sensitive'], expected['primary_reference_low_mor'], gene + ': frozen low flag')
        equal(upstream['B0_control_zero'] == 'True' or upstream['B0_exposed_zero'] == 'True', expected['primary_reference_any_zero'], gene + ': frozen zero flag')
        for ref, (c, h) in REFERENCES.items():
            expected[ref + '_reference_any_zero'] = raw[c] == 0 or raw[h] == 0
            expected[ref + '_reference_low_mor'] = min(mor[c], mor[h]) < 1 - TIE
            for phase in ['W6', 'W12']:
                alternative = expected[phase + '_' + ref + '_mor']
                primary = expected[phase + '_primary_mor']
                sign_flip = flip(alternative, primary)
                norm_flip = flip(alternative, expected[phase + '_' + ref + '_total'])
                expected[phase + '_' + ref + '_primary_sign_flip'] = sign_flip
                expected[phase + '_' + ref + '_normalization_sign_flip'] = norm_flip
                for universe, flag in [('all_genes', None), ('comparison_union', phase + '_union_qualified'), ('baseline_intersection', phase + '_both_qualified')]:
                    if flag is not None and not expected[flag]: continue
                    pool = pools[(phase, universe, ref)]
                    pool['primary'].append(primary); pool['alternative'].append(alternative)
                    pool['shift'].append(expected[ref + '_adjusted_shift_mor'])
                    for key, value in [('flip', sign_flip), ('norm_flip', norm_flip), ('zero', expected[ref + '_reference_any_zero']), ('low', expected[ref + '_reference_low_mor'])]:
                        pool[key] += value
        assert set(actual) == set(expected), 'unexpected output fields'
        for key, value in expected.items(): equal(actual[key], value, gene + ':' + key)
        if gene in selected_ids: selected_expected[gene] = actual

    equal(len(seen), upstream_summary['input_genes'], 'upstream row count')
    equal(summary['input_genes'], len(seen), 'summary row count')
    equal(summary['analysis_id'], contract['analysis_id'], 'analysis ID')
    for key, value in [('same_adjusted_shift_at_both_times_by_construction', True), ('size_factors_refit', False), ('qualification_recomputed', False), ('sex_assignment_pairing_or_exclusion', False), ('population_inference', False), ('new_example_selection', False)]:
        equal(summary[key], value, key)
    for (phase, universe, ref), pool in pools.items():
        block = summary['comparisons'][phase][universe][ref]
        n = len(pool['primary'])
        equal(block['genes'], n, 'summary n')
        if not n: continue
        for field, name in [('primary', phase + '_primary_mor'), ('alternative', phase + '_' + ref + '_mor'), ('shift', ref + '_adjusted_shift_mor')]:
            for absolute in [False, True]:
                ordered = sorted(abs(x) if absolute else x for x in pool[field])
                key = name + ('_absolute_quantiles' if absolute else '_quantiles')
                for q in [0, .25, .5, .75, .9, .95, 1]: equal(block[key][str(q)], quantile(ordered, q), key)
        for count, key in [('flip', phase + '_' + ref + '_primary_sign_flip'), ('norm_flip', phase + '_' + ref + '_normalization_sign_flip'), ('zero', ref + '_reference_any_zero'), ('low', ref + '_reference_low_mor')]:
            equal(block['fraction_' + key], pool[count] / n, key)
    selected_actual = list(read_rows(output / 'selected_cases.tsv'))
    equal([row['gene_id'] for row in selected_actual], selected_ids, 'selected order')
    for source, actual in zip(selected_source, selected_actual):
        for key in ['plot_slot', 'selection_reason']: equal(actual[key], source[key], 'selection unchanged')
        for key, value in selected_expected[source['gene_id']].items(): equal(actual[key], value, 'selected row')
    manifest = json.loads((output / 'reference_manifest.json').read_text())
    equal(manifest['primary']['control'], BASE[:2], 'primary control identity')
    equal(manifest['primary']['history'], BASE[2:], 'primary history identity')
    for ref, (c, h) in REFERENCES.items():
        equal(manifest['alternatives'][ref]['control'], BASE[c], 'alternative control identity')
        equal(manifest['alternatives'][ref]['history'], BASE[h], 'alternative history identity')
        equal(manifest['alternatives'][ref]['libraries_per_history'], 1, 'single-library reference')
    result = {'status': 'passed', 'checks': checks, 'genes': len(seen), 'selected_cases': len(selected_actual),
              'maximum_scaled_error': max_error, 'computational_tolerance': TIE,
              'implementation': 'independent stdlib arithmetic from frozen S4 values; no analysis helper imported',
              'scope': 'all copied fields, baseline and adjusted arithmetic, NA/zero/low flags, shift identity, quantiles, fractions, fixed selection and reference identities',
              'independent_biological_replication': False}
    (output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    verify(args.contract, args.run_dir)
