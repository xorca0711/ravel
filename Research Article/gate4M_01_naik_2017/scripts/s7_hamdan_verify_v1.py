"""Independent stdlib/Decimal reconstruction; imports no S7 analysis functions."""
import argparse
import csv
from decimal import Decimal as D, localcontext
import gzip
import itertools
import json
from pathlib import Path
import re
import time

KEYS = ['NI0_1', 'NI0_2', 'NIT_1', 'NIT_2', 'I0_1', 'I0_2', 'IT_1', 'IT_2']
GROUPS = ['NI0', 'NIT', 'I0', 'IT']
EPS = D('1e-10')
EXPECTED_GSMS = {'4': [8643398, 8643399, 8643396, 8643397, 8643407, 8643408, 8643405, 8643406],
                 '83': [8643414, 8643415, 8643409, 8643410, 8643421, 8643422, 8643416, 8643417]}


class Audit:
    def __init__(self): self.checks, self.maximum_scaled_error = 0, D(0)

    def equal(self, actual, expected, where):
        self.checks += 1
        if isinstance(expected, dict):
            if not isinstance(actual, dict) or set(actual) != set(expected): raise AssertionError(where+': keys')
            for key in expected: self.equal(actual[key], expected[key], where+'/'+key)
        elif isinstance(expected, list):
            if not isinstance(actual, list) or len(actual) != len(expected): raise AssertionError(where+': length')
            for i, value in enumerate(expected): self.equal(actual[i], value, where+'/'+str(i))
        elif isinstance(expected, bool):
            if not (actual is expected or actual == str(expected)): raise AssertionError(where+': bool')
        elif isinstance(expected, (int, D)):
            observed = D(str(actual)); target = D(expected)
            if not observed.is_finite(): raise AssertionError(where+': nonfinite')
            error = abs(observed-target)/max(D(1), abs(target))
            self.maximum_scaled_error = max(self.maximum_scaled_error, error)
            if isinstance(expected, int) and observed != target: raise AssertionError(where+': integer')
            if error > EPS: raise AssertionError(where+': numeric mismatch '+str(error))
        elif actual != expected:
            raise AssertionError(where+': exact value')


def rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8', newline='') as handle:
        yield from csv.DictReader(handle, delimiter='\t')


def median(values):
    values = sorted(values); n = len(values)
    return values[n//2] if n % 2 else (values[n//2-1]+values[n//2])/2


def geometric(values): return (sum(v.ln() for v in values)/len(values)).exp()


def sign(value): return 1 if value > EPS else -1 if value < -EPS else 0


def quantile(values, numerator, denominator):
    ordered = sorted(values); position = D(len(values)-1)*numerator/denominator
    low = int(position); high = min(low+1, len(values)-1)
    return ordered[low]+(position-low)*(ordered[high]-ordered[low])


def expected_row(counts, sf, log2):
    n = [D(c)/f for c, f in zip(counts, sf)]
    means = [(n[i]+n[i+1])/2 for i in range(0, 8, 2)]
    e = [(m+1).ln()/log2 for m in means]
    result = {'raw_'+key: c for key, c in zip(KEYS, counts)}
    result.update({'norm_'+key: v for key, v in zip(KEYS, n)})
    result.update({'mean_'+key: v for key, v in zip(GROUPS, means)})
    result.update({'e_'+key: v for key, v in zip(GROUPS, e)})
    b, p, rni, ri = e[2]-e[0], e[3]-e[1], e[1]-e[0], e[3]-e[2]
    # Deliberately use the alternative algebraic decomposition to check main P-B.
    result.update(B=b, P=p, R_NI=rni, R_I=ri, A=ri-rni)
    individual = [(v+1).ln()/log2 for v in n]
    combinations = [individual[it]-individual[i0]-individual[nt]+individual[n0]
                    for n0, nt, i0, it in itertools.product([0, 1], [2, 3], [4, 5], [6, 7])]
    low, high = min(combinations), max(combinations)
    result.update(A_min=low, A_max=high, A_range_zero=low <= EPS and high >= -EPS,
                  eligible=any(counts), all_raw_zero=not any(counts), any_raw_zero=0 in counts)
    for i, group in enumerate(GROUPS): result['both_zero_'+group] = not any(counts[2*i:2*i+2])
    for key in ['B', 'P', 'R_NI', 'R_I', 'A']: result['sign_'+key] = sign(result[key])
    return result


def accumulator(n):
    return dict(source_gene_count=n, eligible_count=0, structural_all_zero_count=0,
                zero_flags={k: 0 for k in ['any_raw_zero']+['both_zero_'+g for g in GROUPS]+['A_range_zero']},
                computational_zeros={k: 0 for k in ['B', 'P', 'R_NI', 'R_I', 'A']},
                sign_tables={k: {str(a)+','+str(b): 0 for a in [-1, 0, 1] for b in [-1, 0, 1]}
                             for k in ['P_vs_A', 'R_NI_vs_R_I']},
                raw_zero_strata={name: dict(denominator=0,
                    sign_tables={k: {str(a)+','+str(b): 0 for a in [-1, 0, 1] for b in [-1, 0, 1]}
                                 for k in ['P_vs_A', 'R_NI_vs_R_I']}, sign_fractions={})
                    for name in ['any_raw_zero', 'no_raw_zero']},
                post_positive_A={'denominator': 0, **{str(s): {'count': 0, 'fraction': None} for s in [-1, 0, 1]}},
                A_positive_responses={'denominator': 0, 'I_induced': 0, 'both_repressed': 0},
                quantiles={k: [] for k in ['B', 'P', 'R_NI', 'R_I', 'A', 'abs_A']})


def accumulate(acc, r):
    if not r['eligible']:
        acc['structural_all_zero_count'] += 1
        return
    acc['eligible_count'] += 1
    for k in acc['zero_flags']: acc['zero_flags'][k] += int(r[k])
    for k in acc['computational_zeros']: acc['computational_zeros'][k] += int(r['sign_'+k] == 0)
    for name, (x, y) in {'P_vs_A': ('P', 'A'), 'R_NI_vs_R_I': ('R_NI', 'R_I')}.items():
        acc['sign_tables'][name][str(r['sign_'+x])+','+str(r['sign_'+y])] += 1
    stratum = acc['raw_zero_strata']['any_raw_zero' if r['any_raw_zero'] else 'no_raw_zero']
    stratum['denominator'] += 1
    for name, (x, y) in {'P_vs_A': ('P', 'A'), 'R_NI_vs_R_I': ('R_NI', 'R_I')}.items():
        stratum['sign_tables'][name][str(r['sign_'+x])+','+str(r['sign_'+y])] += 1
    if r['sign_P'] == 1:
        acc['post_positive_A']['denominator'] += 1
        acc['post_positive_A'][str(r['sign_A'])]['count'] += 1
    if r['sign_A'] == 1:
        a = acc['A_positive_responses']; a['denominator'] += 1
        a['I_induced'] += int(r['sign_R_I'] == 1)
        a['both_repressed'] += int(r['sign_R_I'] == r['sign_R_NI'] == -1)
    for k in acc['quantiles']: acc['quantiles'][k].append(abs(r['A']) if k == 'abs_A' else r[k])


def finish(acc):
    for stratum in acc['raw_zero_strata'].values():
        n = stratum['denominator']
        stratum['sign_fractions'] = {k: {cell: D(count)/n if n else None for cell, count in table.items()}
                                   for k, table in stratum['sign_tables'].items()}
    for key, values in acc['quantiles'].items():
        acc['quantiles'][key] = {name: quantile(values, num, den) for name, num, den in
            [('q025', 1, 40), ('q25', 1, 4), ('q50', 1, 2), ('q75', 3, 4), ('q975', 39, 40)]} if values else None
    d = acc['post_positive_A']['denominator']
    for key in ['-1', '0', '1']:
        entry = acc['post_positive_A'][key]; entry['fraction'] = D(entry['count'])/d if d else None
    return acc


def verify(count_path, soft_path, manifest_path, output):
    start = time.perf_counter(); audit = Audit()
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    with gzip.open(soft_path, 'rt', encoding='utf-8') as handle: soft = handle.read()
    records = {}
    for block in re.split(r'^\^SAMPLE = ', soft, flags=re.M)[1:]:
        identity, _, remainder = block.partition('\n')
        if identity in records: raise AssertionError('Duplicate SOFT identity')
        records[identity] = remainder
    for patient in ['4', '83']:
        selected = [s for s in manifest['samples'] if s['patient'] == patient]
        audit.equal([s['gsm'] for s in selected], ['GSM'+str(i) for i in EXPECTED_GSMS[patient]], 'fixed GSMs')
        audit.equal([s['key'] for s in selected], KEYS, 'fixed condition ordering')
    for s in manifest['samples']:
        for key, expected in [('title', s['title']), ('description', s['column']), ('platform_id', 'GPL20301')]:
            found = re.findall(r'^!Sample_'+key+r' = (.*)$', records[s['gsm']], flags=re.M)
            audit.equal(found, [expected], s['gsm']+'/'+key)
    exported_samples = list(rows(output/'source_samples.tsv'))
    audit.equal(exported_samples, manifest['samples'], 'all sixteen exported sample rows')
    annotation, count_rows = [], {'4': [], '83': []}
    with gzip.open(count_path, 'rt', encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle, delimiter='\t')
        audit.equal(reader.fieldnames, manifest['annotation_columns']+manifest['source_columns'], 'exact header')
        if len(reader.fieldnames) != len(set(reader.fieldnames)): raise AssertionError('Duplicate columns')
        seen = set()
        for row in reader:
            if None in row or any(v is None for v in row.values()): raise AssertionError('Malformed source width')
            identity = row['GeneId']
            if not identity or identity in seen: raise AssertionError('Empty/duplicate GeneId')
            seen.add(identity); annotation.append({k: row[k] for k in manifest['annotation_columns']})
            for patient in ['4', '83']:
                selected = [row[s['column']] for s in manifest['samples'] if s['patient'] == patient]
                if not all(re.fullmatch(r'[0-9]+', v) for v in selected): raise AssertionError('Invalid integer count')
                values = [int(v) for v in selected]
                if max(values) >= 2**53: raise AssertionError('Integer exceeds exact float range')
                count_rows[patient].append(values)
    if not annotation: raise AssertionError('Empty source')
    sf_by_patient, norm_expected = {}, []
    with localcontext() as ctx:
        ctx.prec = 50; log2 = D(2).ln()
        for patient in ['4', '83']:
            source = count_rows[patient]
            totals = [sum(row[i] for row in source) for i in range(8)]
            if min(totals) <= 0 or max(totals) >= 2**53: raise AssertionError('Invalid total')
            reference = [[D(x) for x in row] for row in source if all(x > 0 for x in row)]
            if not reference: raise AssertionError('Empty MOR reference')
            ratio_columns = [[] for _ in range(8)]
            for row in reference:
                g = geometric(row)
                for i, value in enumerate(row): ratio_columns[i].append(value/g)
            medians = [median(values) for values in ratio_columns]; center = geometric(medians)
            total_center = geometric([D(t) for t in totals])
            sizes = {'MOR': [x/center for x in medians], 'total': [D(t)/total_center for t in totals]}
            sf_by_patient[patient] = sizes
            samples = [s for s in manifest['samples'] if s['patient'] == patient]
            for method, factors in sizes.items():
                for i, s in enumerate(samples):
                    norm_expected.append(dict(patient=patient, method=method, gsm=s['gsm'], column=s['column'], key=s['key'],
                        total=totals[i], size_factor=factors[i], source_gene_count=len(annotation),
                        positive_all_eight_reference_count=len(reference)))
        audit.equal(list(rows(output/'normalization.tsv')), norm_expected, 'normalization')
        gene_reader = iter(rows(output/'gene_responses.tsv.gz'))
        summary = {'by_patient_method': {}, 'normalization_sensitivity': {}}
        interactions = {}
        for patient in ['4', '83']:
            interactions[patient] = {}
            for method in ['MOR', 'total']:
                acc = accumulator(len(annotation)); values = []
                for i, counts in enumerate(count_rows[patient]):
                    expected = expected_row(counts, sf_by_patient[patient][method], log2)
                    observed = next(gene_reader, None)
                    audit.equal(observed, {'patient': patient, 'method': method, **annotation[i], **expected},
                                patient+'/'+method+'/'+annotation[i]['GeneId'])
                    accumulate(acc, expected); values.append(expected['A'])
                interactions[patient][method] = values
                summary['by_patient_method'][patient+'_'+method] = finish(acc)
        if next(gene_reader, None) is not None: raise AssertionError('Unexpected extra gene response rows')
        sensitivity_reader = iter(rows(output/'normalization_sensitivity.tsv.gz'))
        for patient in ['4', '83']:
            n = 0; flips = 0; zero_changes = 0; shifts = []
            for i, (primary, secondary) in enumerate(zip(interactions[patient]['MOR'], interactions[patient]['total'])):
                eligible = any(count_rows[patient][i]); opposite = sign(primary)*sign(secondary) == -1
                zero_change = (sign(primary) == 0) != (sign(secondary) == 0)
                expected = dict(patient=patient, **annotation[i], eligible=eligible, A_MOR=primary, A_total=secondary,
                    A_total_minus_MOR=secondary-primary, opposite_A_signs=opposite, A_zero_status_change=zero_change)
                audit.equal(next(sensitivity_reader, None), expected, 'normalization sensitivity/'+patient+'/'+str(i))
                if eligible:
                    n += 1; flips += int(opposite); zero_changes += int(zero_change); shifts.append(abs(secondary-primary))
            summary['normalization_sensitivity'][patient] = dict(eligible_count=n,
                opposite_A_signs={'count': flips, 'fraction': D(flips)/n if n else None},
                A_zero_status_change={'count': zero_changes, 'fraction': D(zero_changes)/n if n else None},
                median_abs_A_shift=median(shifts) if n else None)
        if next(sensitivity_reader, None) is not None: raise AssertionError('Extra sensitivity rows')
        audit.equal(json.loads((output/'summary.json').read_text()), summary, 'full summary')
        audit.equal(json.loads((output/'source_structure.json').read_text()), dict(source_gene_count=len(annotation),
            annotation_columns=manifest['annotation_columns'], source_columns=manifest['source_columns'],
            excluded_columns=manifest['excluded_columns'], patients=['4', '83'], selected_library_count=16,
            all_gene_rows_exported=True, culture_pairing='unknown', platform_discrepancy='GEO HiSeq4000; paper NextSeq2000'), 'source structure')
    result = dict(status='passed', checks=audit.checks, maximum_scaled_error=float(audit.maximum_scaled_error),
        source_genes=len(annotation), response_rows=4*len(annotation), sensitivity_rows=2*len(annotation),
        library_combinations_per_response=16, decimal_precision=50,
        elapsed_seconds=time.perf_counter()-start, method='Independent stdlib CSV/SOFT and Decimal; no main analysis imports')
    from s7_resources_v1 import peak_memory_bytes
    result['peak_process_memory_bytes'] = peak_memory_bytes()
    (output/'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ['counts', 'soft', 'map', 'output']: p.add_argument('--'+name, required=True)
    a = p.parse_args()
    print(json.dumps(verify(Path(a.counts), Path(a.soft), Path(a.map), Path(a.output))))
