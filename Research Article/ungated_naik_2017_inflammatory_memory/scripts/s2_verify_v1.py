"""Independent S2 arithmetic/source verifier: standard library only."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path
import statistics

IDS = [f'GSM{x}' for x in range(2440985, 2440993)]
TIE = 1e-10


def estimate(columns):
    rows = list(zip(*columns))
    reference = [row for row in rows if all(x > 0 for x in row)]
    means = [statistics.fmean(math.log(x) for x in row) for row in reference]
    logs = [statistics.median(math.log(row[j]) - mean for row, mean in zip(reference, means)) for j in range(4)]
    center = statistics.fmean(logs)
    size = [math.exp(x - center) for x in logs]
    totals = [sum(column) for column in columns]
    total_center = math.exp(statistics.fmean(math.log(x) for x in totals))
    return size, [x / total_center for x in totals], totals, len(reference)


def verify(contract_path, folder):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = [root / item['path'] for item in contract['inputs']]
    columns, genes = [], None
    for gsm in IDS:
        source = [path for path in inputs if path.name.startswith(gsm + '_') and path.name.endswith('.tab.gz')]
        assert len(source) == 1, gsm
        with gzip.open(source[0], 'rt', newline='') as handle:
            records = list(csv.reader(handle, delimiter='\t'))
        assert all(len(row) == 2 for row in records)
        identifiers = [row[0] for row in records]
        assert len(identifiers) == len(set(identifiers)) == 47729
        if genes is None: genes = identifiers
        else: assert identifiers == genes
        columns.append([int(row[1]) for row in records])
    size, total_factors, totals, basis = [], [], [], []
    for start in [0, 4]:
        sf, tf, total, n = estimate(columns[start:start + 4])
        size.extend(sf); total_factors.extend(tf); totals.extend(total); basis.extend([n] * 4)
    comparisons = 0
    maximum_scaled_error = 0.

    def check(actual, expected, name):
        nonlocal comparisons, maximum_scaled_error
        comparisons += 1
        if expected is None:
            assert actual == 'NA', (name, actual, expected)
        elif isinstance(expected, bool):
            assert actual == str(expected), (name, actual, expected)
        else:
            actual = float(actual)
            assert math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-10), (name, actual, expected)
            maximum_scaled_error = max(maximum_scaled_error, abs(actual - expected) / max(1., abs(expected)))

    crosswalk_path = next(path for path in inputs if path.name == 'library_crosswalk.tsv')
    with crosswalk_path.open(newline='') as handle:
        source_map = {row['gsm']: row for row in csv.DictReader(handle, delimiter='\t')}
    with (folder / 'sample_qc.tsv').open(newline='') as handle:
        qc = list(csv.DictReader(handle, delimiter='\t'))
    assert [row['gsm'] for row in qc] == IDS
    for j, row in enumerate(qc):
        assert row['run'] == source_map[IDS[j]]['runs']
        assert row['biosample'] == source_map[IDS[j]]['biosamples']
        assert row['role'] == ('control' if j % 4 < 2 else 'exposed')
        assert row['time'] == ('D6' if j < 4 else 'D30')
        for key, expected in [('mor_size_factor', size[j]), ('total_count_size_factor', total_factors[j]),
                              ('gene_count_total', totals[j]), ('mor_reference_genes', basis[j]),
                              ('detected_genes', sum(x > 0 for x in columns[j]))]:
            check(row[key], expected, key)
    with gzip.open(folder / 'gene_values.tsv.gz', 'rt', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        n = 0
        for n, row in enumerate(reader, 1):
            i = n - 1
            assert row['gene_id'] == genes[i]
            for j, gsm in enumerate(IDS):
                count = columns[j][i]
                check(row[gsm + '__mor'], count / size[j], 'MOR value')
                check(row[gsm + '__total'], count / total_factors[j], 'total-count value')
                check(row[gsm + '__cpm'], count / totals[j] * 1e6, 'CPM value')
        assert n == len(genes)
    union = both = 0
    with (folder / 'gene_effects.tsv').open(newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        n = 0
        for n, row in enumerate(reader, 1):
            i = n - 1
            assert row['gene_id'] == genes[i]
            qualified, effects = [], []
            for time, start in [('D6', 0), ('D30', 4)]:
                raw = [columns[j][i] for j in range(start, start + 4)]
                primary = [columns[j][i] / size[j] for j in range(start, start + 4)]
                secondary = [columns[j][i] / total_factors[j] for j in range(start, start + 4)]
                cm, em = statistics.fmean(primary[:2]), statistics.fmean(primary[2:])
                logs = [math.log2(x + 1) for x in primary]
                pairs = [logs[h] - logs[c] for h in [2, 3] for c in [0, 1]]
                effect = math.log2((em + 1) / (cm + 1))
                total_effect = math.log2((statistics.fmean(secondary[2:]) + 1) / (statistics.fmean(secondary[:2]) + 1))
                eligible = sum(columns[j][i] / totals[j] * 1e6 >= 1 - TIE for j in range(start, start + 4)) >= 2
                qualified.append(eligible); effects.append(effect)
                expected = {'mean_control_mor': cm, 'mean_exposed_mor': em, 'log2_effect_mor': effect,
                            'log2_effect_total': total_effect,
                            'log2_effect_unregularized': math.log2(em / cm) if em > 0 and cm > 0 else None,
                            'control_log_range': max(logs[:2]) - min(logs[:2]),
                            'exposed_log_range': max(logs[2:]) - min(logs[2:]),
                            'pair_min': min(pairs), 'pair_max': max(pairs),
                            'normalization_delta': effect - total_effect,
                            'norm_sign_flip': (effect > TIE and total_effect < -TIE) or (effect < -TIE and total_effect > TIE),
                            'qualified_cpm': eligible, 'zero_libraries': sum(x == 0 for x in raw),
                            'control_zero': all(x == 0 for x in raw[:2]),
                            'exposed_zero': all(x == 0 for x in raw[2:]), 'all_zero': all(x == 0 for x in raw),
                            'regularization_sensitive': min(cm, em) < 1 - TIE,
                            'all_library_differences_same_sign': min(pairs) > TIE or max(pairs) < -TIE}
                for key, value in expected.items(): check(row[time + '_' + key], value, time + '_' + key)
            check(row['eligible_union'], any(qualified), 'union qualification')
            check(row['eligible_both'], all(qualified), 'both qualification')
            check(row['descriptive_D30_minus_D6_effect'], effects[1] - effects[0], 'contrast difference')
            union += any(qualified); both += all(qualified)
        assert n == len(genes)
    summary = json.loads((folder / 'summary.json').read_text())
    assert summary['qualified_union']['genes'] == union and summary['qualified_both']['genes'] == both
    report = {'status': 'passed', 'implementation': 'Python standard library; no analysis-function imports',
              'input_libraries': len(IDS), 'gene_rows': len(genes), 'numeric_and_flag_checks': comparisons,
              'max_scaled_error': maximum_scaled_error, 'relative_tolerance': 1e-10, 'absolute_tolerance': 1e-10,
              'qualified_union': union, 'qualified_both': both, 'independent_biological_replication': False}
    (folder / 'verification.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    verify(args.contract, args.run_dir)
