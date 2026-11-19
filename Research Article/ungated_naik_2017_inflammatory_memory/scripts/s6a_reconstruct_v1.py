"""Approved finite daily-area reconstruction; never infer animal trajectories."""
import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
import time

import openpyxl
from s5f_reconstruct_v1 import read_workbooks, number, save, table


def reason(current, baseline=()):
    return ';'.join(x for x in [
        'current=' + ','.join(sorted(current)) if current else '',
        'baseline=' + ','.join(sorted(baseline)) if baseline else ''] if x) or 'available'


def reconstruct(mapping, cache):
    roles = defaultdict(set)
    observations, groups = [], []
    by_group = {}
    panels = {p['id']: p for p in mapping['panels']}
    assert len(panels) == len(mapping['panels'])
    assert len({e['id'] for e in mapping['endpoints']}) == len(mapping['endpoints'])

    def cell(e, address, role):
        key = e['workbook'], e['sheet'], address
        roles[key].add(role)
        return cache[key]

    for e in mapping['endpoints']:
        p = panels[e['panel']]
        assert e['day'] in p['days'] and e['unit'] == 'mm^2'
        assert [g['id'] for g in e['groups']] == p['group_order']
        for guard in e['header_guards']:
            if cell(e, guard['cell'], 'header') != guard['value']:
                raise ValueError('Changed header/day: ' + e['id'] + ':' + guard['cell'])
        for g in e['groups']:
            if cell(e, g['label_cell'], 'group_label') != g['source_label']:
                raise ValueError('Changed group label')
            values, missing_cells = [], []
            for address in g['cells']:
                v = cell(e, address, 'observation')
                missing = v is None
                if missing:
                    missing_cells.append(address)
                else:
                    v = number(v)
                    values.append(v)
                observations.append(dict(endpoint=e['id'], panel=e['panel'], day=e['day'],
                    group=g['id'], workbook=e['workbook'], sheet=e['sheet'], cell=address,
                    value=v, missing=missing, measured_zero=not missing and v == 0))
            if len(values) != g['expected_n'] or missing_cells != g['expected_missing_cells']:
                raise ValueError('Changed occupancy: ' + e['id'] + ':' + g['id'])
            n = len(values)
            row = dict(endpoint=e['id'], panel=e['panel'], day=e['day'], group=g['id'],
                label=g['label'], source_label=g['source_label'], unit='mm^2',
                source_slots=len(g['cells']), source_n=n, missing_n=len(missing_cells),
                mean=statistics.mean(values) if n else None,
                median=statistics.median(values) if n else None,
                source_min=min(values) if n else None, source_max=max(values) if n else None,
                all_measured_records_zero=n > 0 and min(values) == max(values) == 0,
                sample_sd=statistics.stdev(values) if n > 1 else None,
                dispersion_scope='finite_source_values' if n > 1 else ('singleton_no_sd' if n else 'all_blank_group_day'),
                source_cells=';'.join(g['cells']), missing_cells=';'.join(missing_cells),
                extended_caption_n=p['extended_caption_n'], main_caption_n=p['main_caption_n'],
                main_caption_relation=p['main_caption_relation'], main_rate_n=p['main_rate_ns'][g['id']],
                extended_count_equal=n == p['extended_caption_n'],
                main_caption_count_compatible=n >= p['main_caption_n'] if p['main_caption_relation'] == 'at_least' else n == p['main_caption_n'],
                rate_count_equal=n == p['main_rate_ns'][g['id']],
                count_comparison_scope='daily_record_counts_do_not_establish_animal_or_fit_membership')
            key = e['panel'], e['day'], g['id']
            assert key not in by_group
            by_group[key] = row
            groups.append(row)

    components = []
    for g in groups:
        b = by_group[g['panel'], 0, g['group']]
        missing_current = [g['group']] if g['source_n'] == 0 else []
        missing_baseline = [g['group']] if b['source_n'] == 0 else []
        available = not (missing_current or missing_baseline)
        components.append(dict(endpoint=g['endpoint'], panel=g['panel'], day=g['day'], group=g['group'],
            unit='mm^2', source_n=g['source_n'], baseline_n=b['source_n'],
            current_mean=g['mean'], baseline_mean=b['mean'],
            mean_change=g['mean'] - b['mean'] if available else None,
            current_median=g['median'], baseline_median=b['median'],
            median_change=g['median'] - b['median'] if available else None,
            missing_reason=reason(missing_current, missing_baseline),
            structural_day0_zero=g['day'] == 0 and available))

    contrasts = []
    for p in mapping['panels']:
        for day in p['days']:
            for c in p['contrasts']:
                coeff = c['coefficients']
                assert set(coeff) <= set(p['group_order']) and sum(coeff.values()) == 0
                assert all(v in [-1, 1] for v in coeff.values())
                current = {g: by_group[p['id'], day, g] for g in coeff}
                base = {g: by_group[p['id'], 0, g] for g in coeff}
                miss = sorted(g for g in coeff if current[g]['source_n'] == 0)
                bmiss = sorted(g for g in coeff if base[g]['source_n'] == 0)
                def effect(rows, missing, stat):
                    return None if missing else math.fsum(coeff[g] * rows[g][stat] for g in coeff)
                raw, med = effect(current, miss, 'mean'), effect(current, miss, 'median')
                braw, bmed = effect(base, bmiss, 'mean'), effect(base, bmiss, 'median')
                at_floor = all(current[g]['source_n'] > 0 and
                    current[g]['source_min'] == current[g]['source_max'] == 0 for g in coeff)
                contrasts.append(dict(contrast=p['id'] + '__' + c['id'], panel=p['id'], day=day,
                    label=c['label'], unit='mm^2', coefficients=json.dumps(coeff, sort_keys=True, separators=(',', ':')),
                    source_ns=json.dumps({g: current[g]['source_n'] for g in coeff}, sort_keys=True, separators=(',', ':')),
                    baseline_ns=json.dumps({g: base[g]['source_n'] for g in coeff}, sort_keys=True, separators=(',', ':')),
                    raw_mean=raw, raw_median=med, baseline_mean=braw, baseline_median=bmed,
                    adjusted_mean=raw-braw if not (miss or bmiss) else None,
                    adjusted_median=med-bmed if not (miss or bmiss) else None,
                    missing_current_groups=';'.join(miss), missing_baseline_groups=';'.join(bmiss),
                    raw_missing_reason=reason(miss), baseline_missing_reason=reason([], bmiss),
                    adjusted_missing_reason=reason(miss, bmiss),
                    structural_day0_zero=day == 0 and not (miss or bmiss),
                    all_contributing_current_records_zero=at_floor,
                    adjusted_at_area_floor=at_floor and not (miss or bmiss)))
    source = []
    for key in sorted(roles):
        v = cache[key]
        source.append(dict(workbook=key[0], sheet=key[1], cell=key[2],
            kind='blank' if v is None else ('text' if isinstance(v, str) else 'number'),
            value=v, roles='|'.join(sorted(roles[key]))))
    metadata = dict(endpoint_count=len(mapping['endpoints']), group_count=len(groups), contrast_count=len(contrasts),
        source_cell_count=len(source), observation_slots=len(observations),
        nonmissing_source_records=sum(not x['missing'] for x in observations),
        missing_source_slots=sum(x['missing'] for x in observations),
        measured_zero_records=sum(x['measured_zero'] for x in observations),
        all_blank_group_days=[dict(panel=x['panel'], day=x['day'], group=x['group']) for x in groups if x['source_n'] == 0],
        raw_missing_contrasts=sum(x['raw_mean'] is None for x in contrasts),
        adjusted_missing_contrasts=sum(x['adjusted_mean'] is None for x in contrasts),
        structural_day0_contrasts=sum(x['structural_day0_zero'] for x in contrasts),
        all_zero_area_contrasts=[dict(contrast=x['contrast'], day=x['day']) for x in contrasts if x['all_contributing_current_records_zero']],
        adjusted_at_area_floor_contrasts=sum(x['adjusted_at_area_floor'] for x in contrasts),
        independent_biological_replication=False, population_inference=False,
        source_fits_rerun=False, anonymous_columns_promoted_to_animals=False)
    return dict(source_cells=source, observations=observations, groups=groups,
        group_baseline_components=components, contrasts=contrasts, metadata=metadata)


def write_outputs(output, data):
    for name in ['source_cells', 'observations', 'groups', 'group_baseline_components', 'contrasts']:
        table(output/(name+'.tsv'), data[name])
    save(output/'metadata.json', data['metadata'])


def run(contract_path, output):
    started = time.monotonic()
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    map_path = next(root/x['path'] for x in contract['inputs'] if x['path'].endswith('/S6A_SOURCE_MAP_V1.json'))
    mapping = json.loads(map_path.read_text(encoding='utf-8'))
    lines = (root/mapping['caption_source']['path']).read_text(encoding='utf-8').splitlines()
    for guard in mapping['pdf_caption_guards']:
        assert lines[guard['line']-1] == guard['value'], 'Changed caption source'
    paths = {k: root/v['path'] for k, v in mapping['source_files'].items()}
    for k, path in paths.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == mapping['source_files'][k]['sha256']
    data = reconstruct(mapping, read_workbooks(mapping, paths))
    assert [data['metadata'][k] for k in ['endpoint_count', 'group_count', 'contrast_count']] == [62, 228, 166]
    data['metadata']['analysis_id'] = contract['analysis_id']
    data['metadata']['source_files'] = mapping['source_files']
    write_outputs(output, data)
    from s6a_plot_v1 import plot
    plot(output, mapping, data)
    import matplotlib
    save(output/'runtime.json', dict(python=sys.version, openpyxl=openpyxl.__version__, matplotlib=matplotlib.__version__,
        elapsed_seconds_before_verification=time.monotonic()-started, stochastic_steps='none', upstream_analyses_rerun=False))
    subprocess.run([sys.executable, str(Path(__file__).with_name('s6a_verify_v1.py')), '--contract', str(contract_path.resolve()),
        '--run-dir', str(output.resolve())], check=True)
    print(json.dumps(dict(analysis_id=contract['analysis_id'], status='completed_finite_daily_area_description',
        elapsed_seconds=time.monotonic()-started)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.contract, args.output)
