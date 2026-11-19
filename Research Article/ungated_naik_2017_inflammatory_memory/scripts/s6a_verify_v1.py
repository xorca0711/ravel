"""Independent source/Decimal verification, including missing baseline semantics."""
import argparse
from collections import defaultdict
from decimal import Decimal, InvalidOperation, getcontext
import json
from pathlib import Path

from s5f_verify_v1 import xml_cells, csv_rows

getcontext().prec = 50


def verify(mapping, paths, run_dir, analysis_id=None):
    cache = xml_cells(mapping, paths)
    checks, maximum = 0, Decimal(0)
    def equal(actual, expected, label):
        nonlocal checks, maximum
        checks += 1
        if expected is None:
            assert actual == 'NA', (label, actual, expected)
        elif isinstance(expected, Decimal):
            try:
                a = Decimal(actual)
            except InvalidOperation as error:
                raise AssertionError((label, 'Expected numeric output', actual)) from error
            assert a.is_finite() and expected.is_finite(), label
            error = abs(a-expected)/max(Decimal(1), abs(expected))
            maximum = max(maximum, error)
            assert error <= Decimal('1e-10'), (label, a, expected)
        else:
            assert actual == str(expected), (label, actual, expected)
    def row_equal(actual, expected, label):
        assert set(actual) == set(expected), (label, 'field mismatch')
        for k, v in expected.items(): equal(actual[k], v, label + ':' + k)
    def moments(values):
        n = len(values)
        if not n: return (None,)*5
        avg = sum(values)/n
        ordered = sorted(values)
        med = ordered[n//2] if n % 2 else (ordered[n//2-1]+ordered[n//2])/2
        sd = (sum((v-avg)**2 for v in values)/(n-1)).sqrt() if n > 1 else None
        return avg, med, min(values), max(values), sd
    def missing_reason(a, b):
        pieces = []
        if a: pieces.append('current=' + ','.join(sorted(a)))
        if b: pieces.append('baseline=' + ','.join(sorted(b)))
        return ';'.join(pieces) if pieces else 'available'

    panels = {p['id']: p for p in mapping['panels']}
    if mapping.get('rate_groups_source'):
        root = Path(__file__).resolve().parents[3]
        rate_rows = {(r['endpoint'], r['group']): r for r in csv_rows(root/mapping['rate_groups_source'])}
        for p in mapping['panels']:
            for gid in p['group_order']:
                r = rate_rows[p['rate_endpoint'], p['rate_group_ids'][gid]]
                assert int(r['source_n']) == p['main_rate_ns'][gid]
                assert int(r['caption_n']) == p['main_caption_n']
                assert r['caption_n_relation'] == p['main_caption_relation']
                checks += 3
    # Check the prospective contrast meanings independently of the main reducer.
    for p in mapping['panels']:
        gs = p['group_order']
        if p['comparison_type'] == 'oe_only':
            assert len(gs) == 2
            expected_coeffs = [{gs[0]: -1, gs[1]: 1}]
        else:
            assert len(gs) == 4
            if p['comparison_type'] == 'oe_blockade':
                first, second = {gs[0]: -1, gs[2]: 1}, {gs[1]: -1, gs[3]: 1}
            else:
                assert p['comparison_type'] in ['history_background', 'history_inhibition']
                first, second = {gs[0]: -1, gs[1]: 1}, {gs[2]: -1, gs[3]: 1}
            expected_coeffs = [first, second, {**{g: -v for g, v in first.items()}, **second}]
        assert [c['coefficients'] for c in p['contrasts']] == expected_coeffs, 'Wrong contrast meaning'

    roles = defaultdict(set)
    def read(e, address, role):
        key = e['workbook'], e['sheet'], address
        roles[key].add(role)
        return cache[key]
    expected_groups, observations, vectors = [], [], {}
    for e in mapping['endpoints']:
        p = panels[e['panel']]
        assert e['day'] in p['days']
        for guard in e['header_guards']:
            assert read(e, guard['cell'], 'header') == guard['value'], 'Changed header/day'
        for g in e['groups']:
            assert read(e, g['label_cell'], 'group_label') == g['source_label'], 'Changed label'
            values, absent = [], []
            for address in g['cells']:
                v = read(e, address, 'observation')
                if v is None: absent.append(address)
                else:
                    assert isinstance(v, Decimal) and v.is_finite(), 'Invalid numeric source'
                    values.append(v)
                observations.append(dict(endpoint=e['id'], panel=e['panel'], day=e['day'], group=g['id'],
                    workbook=e['workbook'], sheet=e['sheet'], cell=address, value=v,
                    missing=v is None, measured_zero=v is not None and v == 0))
            n = len(values)
            assert n == g['expected_n'] and absent == g['expected_missing_cells'], 'Changed source occupancy'
            avg, med, lo, hi, sd = moments(values)
            record = dict(endpoint=e['id'], panel=e['panel'], day=e['day'], group=g['id'], label=g['label'],
                source_label=g['source_label'], unit='mm^2', source_slots=len(g['cells']), source_n=n,
                missing_n=len(absent), mean=avg, median=med, source_min=lo, source_max=hi, sample_sd=sd,
                all_measured_records_zero=bool(values) and all(v == 0 for v in values),
                dispersion_scope='finite_source_values' if n > 1 else ('singleton_no_sd' if n == 1 else 'all_blank_group_day'),
                source_cells=';'.join(g['cells']), missing_cells=';'.join(absent), extended_caption_n=p['extended_caption_n'],
                main_caption_n=p['main_caption_n'], main_caption_relation=p['main_caption_relation'],
                main_rate_n=p['main_rate_ns'][g['id']], extended_count_equal=n == p['extended_caption_n'],
                main_caption_count_compatible=n >= p['main_caption_n'] if p['main_caption_relation'] == 'at_least' else n == p['main_caption_n'],
                rate_count_equal=n == p['main_rate_ns'][g['id']],
                count_comparison_scope='daily_record_counts_do_not_establish_animal_or_fit_membership')
            expected_groups.append(record)
            key = e['panel'], e['day'], g['id']
            assert key not in vectors
            vectors[key] = record
    def verify_rows(name, expected):
        actual = csv_rows(run_dir/(name+'.tsv'))
        assert len(actual) == len(expected), name
        for i, (a, b) in enumerate(zip(actual, expected)): row_equal(a, b, name+':'+str(i))
    verify_rows('observations', observations)
    verify_rows('groups', expected_groups)
    source = []
    for key in sorted(roles):
        v = cache[key]
        source.append(dict(workbook=key[0], sheet=key[1], cell=key[2], value=v,
            kind='blank' if v is None else ('number' if isinstance(v, Decimal) else 'text'),
            roles='|'.join(sorted(roles[key]))))
    verify_rows('source_cells', source)

    components = []
    for g in expected_groups:
        b = vectors[g['panel'], 0, g['group']]
        a_missing, b_missing = ([g['group']] if not g['source_n'] else []), ([g['group']] if not b['source_n'] else [])
        ok = not (a_missing or b_missing)
        components.append(dict(endpoint=g['endpoint'], panel=g['panel'], day=g['day'], group=g['group'], unit='mm^2',
            source_n=g['source_n'], baseline_n=b['source_n'], current_mean=g['mean'], baseline_mean=b['mean'],
            mean_change=g['mean']-b['mean'] if ok else None, current_median=g['median'], baseline_median=b['median'],
            median_change=g['median']-b['median'] if ok else None, missing_reason=missing_reason(a_missing, b_missing),
            structural_day0_zero=g['day'] == 0 and ok))
    verify_rows('group_baseline_components', components)
    contrasts = []
    for p in mapping['panels']:
        for day in p['days']:
            for c in p['contrasts']:
                coef = c['coefficients']
                a_missing = sorted(g for g in coef if not vectors[p['id'], day, g]['source_n'])
                b_missing = sorted(g for g in coef if not vectors[p['id'], 0, g]['source_n'])
                def linear(d, stat, missing):
                    if missing: return None
                    return sum(Decimal(weight)*vectors[p['id'], d, g][stat] for g, weight in coef.items())
                a, am = linear(day, 'mean', a_missing), linear(day, 'median', a_missing)
                b, bm = linear(0, 'mean', b_missing), linear(0, 'median', b_missing)
                ok = not (a_missing or b_missing)
                at_floor = all(vectors[p['id'], day, g]['all_measured_records_zero'] for g in coef)
                contrasts.append(dict(contrast=p['id']+'__'+c['id'], panel=p['id'], day=day, label=c['label'], unit='mm^2',
                    coefficients=json.dumps(coef, sort_keys=True, separators=(',', ':')),
                    source_ns=json.dumps({g: vectors[p['id'], day, g]['source_n'] for g in coef}, sort_keys=True, separators=(',', ':')),
                    baseline_ns=json.dumps({g: vectors[p['id'], 0, g]['source_n'] for g in coef}, sort_keys=True, separators=(',', ':')),
                    raw_mean=a, raw_median=am, baseline_mean=b, baseline_median=bm,
                    adjusted_mean=a-b if ok else None, adjusted_median=am-bm if ok else None,
                    missing_current_groups=';'.join(a_missing), missing_baseline_groups=';'.join(b_missing),
                    raw_missing_reason=missing_reason(a_missing, []), baseline_missing_reason=missing_reason([], b_missing),
                    adjusted_missing_reason=missing_reason(a_missing, b_missing), structural_day0_zero=day == 0 and ok,
                    all_contributing_current_records_zero=at_floor, adjusted_at_area_floor=at_floor and ok))
    verify_rows('contrasts', contrasts)
    meta = json.loads((run_dir/'metadata.json').read_text(encoding='utf-8'))
    expected_meta = dict(endpoint_count=len(mapping['endpoints']), group_count=len(expected_groups), contrast_count=len(contrasts),
        source_cell_count=len(source), observation_slots=len(observations), nonmissing_source_records=sum(x['value'] is not None for x in observations),
        missing_source_slots=sum(x['value'] is None for x in observations), measured_zero_records=sum(x['measured_zero'] for x in observations),
        all_blank_group_days=[dict(panel=x['panel'], day=x['day'], group=x['group']) for x in expected_groups if not x['source_n']],
        raw_missing_contrasts=sum(x['raw_mean'] is None for x in contrasts), adjusted_missing_contrasts=sum(x['adjusted_mean'] is None for x in contrasts),
        structural_day0_contrasts=sum(x['structural_day0_zero'] for x in contrasts),
        all_zero_area_contrasts=[dict(contrast=x['contrast'], day=x['day']) for x in contrasts if x['all_contributing_current_records_zero']],
        adjusted_at_area_floor_contrasts=sum(x['adjusted_at_area_floor'] for x in contrasts),
        independent_biological_replication=False, population_inference=False, source_fits_rerun=False, anonymous_columns_promoted_to_animals=False)
    for k, v in expected_meta.items():
        checks += 1
        assert meta[k] == v, ('metadata', k)
    if analysis_id is not None:
        assert meta['analysis_id'] == analysis_id and meta['source_files'] == mapping['source_files']
    pdf_checked = 0
    if mapping.get('pdf_caption_guards'):
        root = Path(__file__).resolve().parents[3]
        lines = (root/mapping['caption_source']['path']).read_text(encoding='utf-8').splitlines()
        for guard in mapping['pdf_caption_guards']:
            assert lines[guard['line']-1] == guard['value']
            pdf_checked += 1
    return dict(status='passed', checks=checks, maximum_scaled_error=float(maximum), source_reader='stdlib ZIP/XML',
        arithmetic='50-digit Decimal', endpoints=len(mapping['endpoints']), groups=len(expected_groups), contrasts=len(contrasts),
        source_cells=len(source), pdf_caption_guards_checked=pdf_checked, independent_biological_replication=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    c = json.loads(args.contract.read_text(encoding='utf-8-sig'))
    m = json.loads(next(root/x['path'] for x in c['inputs'] if x['path'].endswith('/S6A_SOURCE_MAP_V1.json')).read_text(encoding='utf-8'))
    result = verify(m, {k: root/v['path'] for k, v in m['source_files'].items()}, args.run_dir, c['analysis_id'])
    result['analysis_id'] = c['analysis_id']
    (args.run_dir/'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
