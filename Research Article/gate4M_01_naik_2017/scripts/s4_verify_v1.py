"""Independent S4 arithmetic, metadata and annotation verification; stdlib only."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path
import statistics

IDS = [f'GSM{x}' for x in range(2440989, 2441001)]
PHASES = ['B0', 'W6', 'W12']
MARKERS = ['Xist', 'Ddx3y', 'Eif2s3y', 'Kdm5d', 'Uty']
TIE = 1e-10


def table(path):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'rt', newline='', encoding='utf-8') as handle:
        yield from csv.DictReader(handle, delimiter='\t')


def flip(a, b):
    return (a > TIE and b < -TIE) or (a < -TIE and b > TIE)


def ratio(a, b, c=1):
    return math.log2((a + c) / (b + c)) if c or (a > 0 and b > 0) else None


def pearson(a, b):
    if len(a) < 2: return None
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    va = math.fsum((v - ma) ** 2 for v in a)
    vb = math.fsum((v - mb) ** 2 for v in b)
    if va == 0 or vb == 0: return None
    return math.fsum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb)


def ranks(values):
    ordered = sorted(range(len(values)), key=values.__getitem__)
    result = [0.] * len(values)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[ordered[end]] == values[ordered[start]]: end += 1
        for i in range(start, end): result[ordered[i]] = (start + 1 + end) / 2
        start = end
    return result


def estimate(columns):
    references = [r for r in zip(*columns) if all(v > 0 for v in r)]
    means = [statistics.fmean(math.log(v) for v in row) for row in references]
    logs = [statistics.median(math.log(row[j]) - mean for row, mean in zip(references, means)) for j in range(12)]
    center = statistics.fmean(logs)
    sizes = [math.exp(v - center) for v in logs]
    totals = [sum(column) for column in columns]
    total_center = math.exp(statistics.fmean(math.log(v) for v in totals))
    return sizes, [v / total_center for v in totals], totals, len(references)


def annotations(path):
    result = {}
    with gzip.open(path, 'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            fields = line.rstrip('\n').split('\t')
            if len(fields) != 9 or fields[2] != 'gene': continue
            attrs = {}
            for item in fields[8].split(';'):
                bits = item.strip().split(' ', 1)
                if len(bits) == 2: attrs[bits[0]] = bits[1].strip().strip('"')
            gene = attrs.get('gene_id')
            rec = (attrs.get('gene_name', 'NA'), attrs.get('gene_type', 'NA'), fields[0])
            assert gene not in result or result[gene] == rec
            result[gene] = rec
    return result


def values_for_gene(counts, sizes, total_factors, totals):
    primary = [v / sizes[j] for j, v in enumerate(counts)]
    secondary = [v / total_factors[j] for j, v in enumerate(counts)]
    cpm = [v / totals[j] * 1e6 for j, v in enumerate(counts)]
    expected, pairs = {}, {}
    for k, phase in enumerate(PHASES):
        raw = counts[4 * k:4 * k + 4]
        p, s = primary[4 * k:4 * k + 4], secondary[4 * k:4 * k + 4]
        cm, hm = statistics.fmean(p[:2]), statistics.fmean(p[2:])
        ct, ht = statistics.fmean(s[:2]), statistics.fmean(s[2:])
        logs = [math.log2(v + 1) for v in p]
        combinations = [logs[h] - logs[c] for h in [2, 3] for c in [0, 1]]
        pairs[phase] = combinations
        effect, alt = ratio(hm, cm), ratio(ht, ct)
        record = {'mean_control_mor': cm, 'mean_exposed_mor': hm, 'mean_control_total': ct, 'mean_exposed_total': ht,
                  'log2_effect_mor': effect, 'log2_effect_total': alt, 'log2_effect_unregularized': ratio(hm, cm, 0),
                  'control_log_range': abs(logs[1] - logs[0]), 'exposed_log_range': abs(logs[3] - logs[2]),
                  'pair_min': min(combinations), 'pair_max': max(combinations),
                  'regularization_sensitive': min(cm, hm) < 1 - TIE, 'normalization_delta': effect - alt,
                  'norm_sign_flip': flip(effect, alt), 'qualified_cpm': sum(v >= 1 - TIE for v in cpm[4 * k:4 * k + 4]) >= 2,
                  'zero_libraries': raw.count(0), 'control_zero': not any(raw[:2]), 'exposed_zero': not any(raw[2:]),
                  'all_zero': not any(raw), 'all_library_differences_same_sign': min(combinations) > TIE or max(combinations) < -TIE}
        expected.update({phase + '_' + key: value for key, value in record.items()})
    for k, phase in enumerate(PHASES[1:], 1):
        effect = expected[phase + '_log2_effect_mor'] - expected['B0_log2_effect_mor']
        alt = expected[phase + '_log2_effect_total'] - expected['B0_log2_effect_total']
        u, b = expected[phase + '_log2_effect_unregularized'], expected['B0_log2_effect_unregularized']
        combinations = [post - base for post in pairs[phase] for base in pairs['B0']]
        low, high = min(combinations), max(combinations)
        record = {'adjusted_mor': effect, 'adjusted_total': alt, 'adjusted_unregularized': u - b if u is not None and b is not None else None,
                  'adjustment_norm_delta': effect - alt, 'adjustment_norm_sign_flip': flip(effect, alt),
                  'adjustment_min': low, 'adjustment_max': high, 'adjustment_range_includes_zero': low <= TIE and high >= -TIE,
                  'adjustment_low_mean': expected[phase + '_regularization_sensitive'] or expected['B0_regularization_sensitive'],
                  'union_qualified': expected[phase + '_qualified_cpm'] or expected['B0_qualified_cpm'],
                  'both_qualified': expected[phase + '_qualified_cpm'] and expected['B0_qualified_cpm']}
        for offset, group in [(0, 'control'), (2, 'exposed')]:
            for suffix in ['mor', 'total']:
                record[group + '_wound_baseline_' + suffix] = ratio(expected[phase + '_mean_' + group + '_' + suffix], expected['B0_mean_' + group + '_' + suffix])
            record[group + '_wound_baseline_unregularized'] = ratio(expected[phase + '_mean_' + group + '_mor'], expected['B0_mean_' + group + '_mor'], 0)
            combos = [math.log2(primary[4 * k + offset + w] + 1) - math.log2(primary[offset + b] + 1) for w in [0, 1] for b in [0, 1]]
            record[group + '_wound_baseline_min'], record[group + '_wound_baseline_max'] = min(combos), max(combos)
        expected.update({phase + '_' + key: value for key, value in record.items()})
    expected['global_union_qualified'] = any(expected[p + '_qualified_cpm'] for p in PHASES)
    expected['all_three_qualified'] = all(expected[p + '_qualified_cpm'] for p in PHASES)
    return expected, primary, secondary, cpm


def verify(contract_path, folder):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = [root / item['path'] for item in contract['inputs']]
    columns, genes = [], None
    for gsm in IDS:
        paths = [p for p in inputs if p.name.startswith(gsm + '_') and p.name.endswith('.tab.gz')]
        assert len(paths) == 1
        with gzip.open(paths[0], 'rt') as handle: records = list(csv.reader(handle, delimiter='\t'))
        assert all(len(r) == 2 for r in records)
        ids = [r[0] for r in records]
        assert len(ids) == len(set(ids)) == 47729
        if genes is None: genes = ids
        else: assert genes == ids
        counts = [int(r[1]) for r in records]
        assert min(counts) >= 0
        columns.append(counts)
    sizes, total_factors, totals, basis = estimate(columns)
    comparison_count, max_error = 0, 0.

    def check(actual, expected, name):
        nonlocal comparison_count, max_error
        comparison_count += 1
        if expected is None:
            assert actual == 'NA', (name, actual, expected)
        elif isinstance(expected, bool):
            assert actual == str(expected), (name, actual, expected)
        else:
            value = float(actual)
            assert math.isfinite(value) and math.isclose(value, expected, rel_tol=TIE, abs_tol=TIE), (name, value, expected)
            max_error = max(max_error, abs(value - expected) / max(1., abs(expected)))

    source_rows = list(table(next(p for p in inputs if p.name == 'library_crosswalk.tsv')))
    assert len({r['gsm'] for r in source_rows}) == len(source_rows)
    sources = {r['gsm']: r for r in source_rows}
    qc = list(table(folder / 'sample_qc.tsv'))
    assert [r['gsm'] for r in qc] == IDS
    for j, r in enumerate(qc):
        source = sources[IDS[j]]
        phase, history = PHASES[j // 4], 'control' if j % 4 < 2 else 'prior_inflammation'
        assert (source['assay'], source['day_label'], source['wound_hour_label'], source['history_label']) == ('RNA-seq', '30', ['', '6', '12'][j // 4], history)
        assert not source['label_conflicts']
        assert r['run'] == source['runs'] and r['biosample'] == source['biosamples']
        assert r['phase'] == phase and r['role'] == ('control' if j % 4 < 2 else 'exposed')
        assert r['instrument'] == source['instrument_models'] == 'Illumina HiSeq 2500'
        assert r['layout'] == source['library_layouts'] == 'SINGLE'
        sex = [v.strip() for v in source['characteristics'].split('|') if v.partition(':')[0].strip().lower() in ('sex', 'gender')]
        assert r['recorded_sex'] == (' | '.join(sex) if sex else 'not reported in selected GEO characteristics')
        for field, expected in [('gene_count_total', totals[j]), ('mor_reference_genes', basis),
                                ('mor_size_factor', sizes[j]), ('total_count_size_factor', total_factors[j]),
                                ('detected_genes', sum(v > 0 for v in columns[j]))]: check(r[field], expected, field)
    ann = annotations(next(p for p in inputs if p.name == 'gencode.vM9.annotation.gtf.gz'))
    summary = json.loads((folder / 'summary.json').read_text())
    cases = list(table(folder / 'selected_cases.tsv'))
    chosen = {r['gene_id']: r for r in cases}
    assert len(chosen) == len(cases)
    candidates = [[] for _ in range(6)]
    qualification_counts = {key: 0 for key in ['global_union_qualified', 'all_three_qualified', 'W6_union_qualified', 'W6_both_qualified', 'W12_union_qualified', 'W12_both_qualified']}
    checksums = {(p, u): {'n': 0, 'larger': 0, 'ties': 0, 'norm_flip': 0, 'range_zero': 0, 'low': 0}
                 for p in ['W6', 'W12'] for u in ['all_genes', 'comparison_union', 'baseline_intersection']}
    profiles = {name: {key: [] for key in ['W6_adjusted_mor', 'W12_adjusted_mor', 'W6_log2_effect_mor', 'W12_log2_effect_mor']}
                for name in ['global_union', 'all_three_qualified']}
    values_iter = iter(table(folder / 'gene_values.tsv.gz'))
    n = 0
    for n, r in enumerate(table(folder / 'gene_effects.tsv.gz'), 1):
        i, gene = n - 1, genes[n - 1]
        assert r['gene_id'] == gene
        assert (r['gene_name'], r['gene_type'], r['chromosome']) == ann.get(gene, ('NA', 'NA', 'NA'))
        counts = [column[i] for column in columns]
        expected, primary, secondary, cpm = values_for_gene(counts, sizes, total_factors, totals)
        for key, value in expected.items(): check(r[key], value, key)
        v = next(values_iter)
        assert v['gene_id'] == gene
        for j, gsm in enumerate(IDS):
            for suffix, vector in [('raw', counts), ('mor', primary), ('total', secondary), ('cpm', cpm)]: check(v[gsm + '__' + suffix], vector[j], suffix)
        for key in qualification_counts: qualification_counts[key] += expected[key]
        for name, flag in [('global_union', 'global_union_qualified'), ('all_three_qualified', 'all_three_qualified')]:
            if expected[flag]:
                for key in profiles[name]: profiles[name][key].append(float(r[key]))
        for slot, phase, factor in [(0, 'W6', 1), (1, 'W6', -1), (2, 'W12', 1), (3, 'W12', -1)]:
            if expected[phase + '_union_qualified']: candidates[slot].append((factor * float(r[phase + '_adjusted_mor']), gene))
        if expected['all_three_qualified'] and flip(expected['W6_adjusted_mor'], expected['W12_adjusted_mor']):
            candidates[4].append((min(abs(float(r['W6_adjusted_mor'])), abs(float(r['W12_adjusted_mor']))), gene))
        widths = [float(r[p + '_adjustment_max']) - float(r[p + '_adjustment_min']) for p in ['W6', 'W12'] if expected[p + '_union_qualified']]
        if widths: candidates[5].append((max(widths), gene))
        if gene in chosen:
            for key, value in expected.items(): check(chosen[gene][key], value, 'selected ' + key)
        for phase in ['W6', 'W12']:
            for universe, eligible in [('all_genes', True), ('comparison_union', expected[phase + '_union_qualified']), ('baseline_intersection', expected[phase + '_both_qualified'])]:
                if not eligible: continue
                c = checksums[(phase, universe)]
                c['n'] += 1
                b, p = abs(expected['B0_log2_effect_mor']), abs(expected[phase + '_log2_effect_mor'])
                c['larger'] += p > b + TIE
                c['ties'] += abs(p - b) <= TIE
                c['norm_flip'] += expected[phase + '_adjustment_norm_sign_flip']
                c['range_zero'] += expected[phase + '_adjustment_range_includes_zero']
                c['low'] += expected[phase + '_adjustment_low_mean']
    assert n == len(genes) and next(values_iter, None) is None
    used = set()
    actual_slots = {int(r['plot_slot']): r for r in cases}
    missing_slots = {r['slot'] for r in summary['unfilled_case_slots']}
    for slot, ranked in enumerate(candidates, 1):
        remaining = sorted(((-score, gene) for score, gene in ranked if gene not in used))
        if not remaining:
            assert slot in missing_slots and slot not in actual_slots
        else:
            score, gene = remaining[0]
            assert actual_slots[slot]['gene_id'] == gene
            check(actual_slots[slot]['selection_score'], -score, 'case ranking')
            used.add(gene)
    for (phase, universe), c in checksums.items():
        out = summary['comparisons'][phase][universe]
        check(out['genes'], c['n'], 'summary universe')
        if c['n']:
            for field, key in [('fraction_abs_post_larger_than_baseline', 'larger'), ('fraction_abs_post_baseline_tied', 'ties'),
                               ('fraction_adjustment_norm_sign_flip', 'norm_flip'), ('fraction_adjustment_range_includes_zero', 'range_zero'),
                               ('fraction_adjustment_low_mean', 'low')]: check(out[field], c[key] / c['n'], field)
    check(summary['global_union_genes'], qualification_counts['global_union_qualified'], 'global union')
    check(summary['all_three_qualified_genes'], qualification_counts['all_three_qualified'], 'all-three intersection')
    for name, vectors in profiles.items():
        out = summary['cross_time'][name]
        for suffix, key6, key12 in [('adjusted', 'W6_adjusted_mor', 'W12_adjusted_mor'), ('unadjusted', 'W6_log2_effect_mor', 'W12_log2_effect_mor')]:
            a, b = vectors[key6], vectors[key12]
            for stat, expected in [('pearson', pearson(a, b)), ('spearman', pearson(ranks(a), ranks(b)))]:
                actual = out[stat + '_' + suffix]
                check('NA' if actual is None else actual, expected, stat + ' ' + suffix)
        a, b = vectors['W6_adjusted_mor'], vectors['W12_adjusted_mor']
        actual = out['fraction_opposite_nonzero']
        check('NA' if actual is None else actual, sum(flip(x, y) for x, y in zip(a, b)) / len(a) if a else None, 'opposite directions')
    coverage = json.loads((folder / 'annotation_coverage.json').read_text())
    check(coverage['exact_version_matches'], sum(g in ann for g in genes), 'annotation matches')
    assert coverage['unmatched_ids'] == [g for g in genes if g not in ann]
    marker_table = list(table(folder / 'marker_qc.tsv'))
    lookup = {g: i for i, g in enumerate(genes)}
    expected_marker_keys = []
    for name in MARKERS:
        hits = sorted(g for g, rec in ann.items() if rec[0] == name)
        status = 'missing_annotation' if not hits else ('unique_exact_annotation' if len(hits) == 1 else 'ambiguous_symbol')
        for gene in hits or ['NA']:
            for j, gsm in enumerate(IDS):
                expected_marker_keys.append((name, gene, gsm))
                rec = next(r for r in marker_table if (r['requested_name'], r['gene_id'], r['gsm']) == (name, gene, gsm))
                assert rec['annotation_status'] == status and rec['recorded_sex'] == qc[j]['recorded_sex']
                assert (rec['gene_type'], rec['chromosome']) == ((ann[gene][1], ann[gene][2]) if gene in ann else ('NA', 'NA'))
                present = gene in lookup
                check(rec['in_count_universe'], present, 'marker universe membership')
                count = columns[j][lookup[gene]] if present else None
                for suffix, value in [('raw', count), ('mor', count / sizes[j] if present else None),
                                      ('total', count / total_factors[j] if present else None), ('cpm', count / totals[j] * 1e6 if present else None)]: check(rec[suffix], value, 'marker ' + suffix)
    assert [(r['requested_name'], r['gene_id'], r['gsm']) for r in marker_table] == expected_marker_keys
    report = {'status': 'passed', 'implementation': 'Python standard library; no analysis-function imports',
              'input_libraries': 12, 'gene_rows': len(genes), 'numeric_and_flag_checks': comparison_count,
              'max_scaled_error': max_error, 'relative_tolerance': TIE, 'absolute_tolerance': TIE,
              'joint_mor_reference_genes': basis, 'qualified_counts': qualification_counts,
              'marker_rows_verified': len(marker_table), 'independent_biological_replication': False}
    (folder / 'verification.json').write_bytes((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    verify(args.contract, args.run_dir)
