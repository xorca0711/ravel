"""Exposed panel-wise reproduction. Source cells are not cross-assay mouse IDs."""
import argparse
import csv
import json
import math
import platform
import statistics
import warnings
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import scipy
from scipy import special, stats

CONFIG = Path('Research Article/ungated_navarro_negredo_2026_aged_brain_il10/config/animal_panels_v1.json')


def csv_out(path, rows):
    if not rows:
        raise ValueError('Empty output: ' + str(path))
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def raw_cells(path):
    """Independent raw OOXML extraction; no openpyxl implementation reuse."""
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    rel_ns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    result = {}
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        links = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r.get('Target') for r in links}
        for sheet in wb.find('m:sheets', ns):
            target = targets[sheet.get(rel_ns)]
            name = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            root = ET.fromstring(z.read(name))
            values = {}
            for c in root.findall('.//m:c', ns):
                v = c.find('m:v', ns)
                if v is not None and c.get('t') not in {'s', 'str', 'b', 'e'}:
                    values[c.get('r')] = float(v.text)
            result[sheet.get('name')] = values
    return result


def independent_u(a, b):
    return sum((x > y) + 0.5 * (x == y) for x in a for y in b)


def independent_exact_p(n, m, u):
    # Distribution of rank sums by selecting n ranks among n+m; integer DP.
    counts = [{0: 1}] + [{} for _ in range(n)]
    for rank in range(1, n + m + 1):
        for k in range(min(rank, n), 0, -1):
            for total, count in list(counts[k - 1].items()):
                counts[k][total + rank] = counts[k].get(total + rank, 0) + count
    low = min(u, n * m - u) + n * (n + 1) // 2
    return min(1.0, 2 * sum(v for s, v in counts[n].items() if s <= low) / math.comb(n + m, n))


def independent_asymptotic_p(a, b, u, continuity):
    n, m = len(a), len(b)
    values = a + b
    sizes = [values.count(v) for v in set(values)]
    total = n + m
    variance = n * m / 12 * ((total + 1) - sum(t**3 - t for t in sizes) / (total * (total - 1)))
    if variance == 0:
        return 1.0
    z = (abs(u - n * m / 2) - (0.5 if continuity else 0)) / math.sqrt(variance)
    return min(1.0, math.erfc(z / math.sqrt(2)))


def plot_group(out, name, endpoints, values, contrasts, seed):
    cols = 2 if len(endpoints) == 4 else 3
    rows = math.ceil(len(endpoints) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4.3 * cols, 4.0 * rows), squeeze=False,
                             layout='constrained')
    rng = np.random.default_rng(seed)
    colors = {'Young': '#56B4E9', 'Control': '#777777', 'WT': '#D55E00', 'D25K': '#009E73', 'RIPR': '#CC79A7'}
    for ax, e in zip(axes.flat, endpoints):
        groups = list(e['groups'])
        for i, group in enumerate(groups):
            selected = [r for r in values if r['endpoint'] == e['id'] and r['group'] == group]
            blocks = list(e['blocks'])
            for block in blocks:
                ys = [r['value'] for r in selected if r['block'] == block]
                marker = ['o', '^', 's'][blocks.index(block) % 3]
                ax.scatter(i + rng.uniform(-.11, .11, len(ys)), ys, marker=marker,
                           color=colors[group], edgecolor='white', linewidth=.4, s=30, zorder=3)
            mean = statistics.mean(r['value'] for r in selected)
            ax.hlines(mean, i-.22, i+.22, color='black', linewidth=1.2, zorder=4)
        ax.set_xticks(range(len(groups)), [f'{g}\nn={sum(r["endpoint"] == e["id"] and r["group"] == g for r in values)}' for g in groups])
        ax.set_ylabel(e['unit'])
        ax.set_title(e['title'], fontsize=11, fontweight='bold', pad=26)
        key = 'D25K-Control' if 'D25K' in groups else 'RIPR-Control'
        c = next(r for r in contrasts if r['endpoint'] == e['id'] and r['comparison'] == key and r['scope'] == 'all')
        label = f'Direct {key}: calculated p={c["p_primary"]:.4g}'
        if c['p_reported'] != '':
            label += f'; S4 {c["p_reported"]:g}'
        ax.text(.5, 1.025, label, ha='center', va='bottom', transform=ax.transAxes, fontsize=8)
        if e['chance']:
            ax.axhline(e['chance']['null'], color='#333333', linestyle=':', linewidth=.9)
        if e['id'].startswith('nesting'):
            ax.set_ylim(.65, 4.5)
            ax.set_yticks([1, 2, 3, 4])
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.13)
    for ax in list(axes.flat)[len(endpoints):]:
        ax.set_visible(False)
    fig.suptitle('Navarro Negredo 2026 — deposited mouse-level values\n'
                 'Dots: source observations; horizontal bars: means; triangles: second block. Unadjusted reproduction.', fontsize=11)
    fig.savefig(out / (name + '.png'), dpi=220, facecolor='white')
    fig.savefig(out / (name + '.svg'), facecolor='white')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    config = json.loads(CONFIG.read_text())
    book = openpyxl.load_workbook(config['source'], read_only=True, data_only=True)
    xml = raw_cells(config['source'])
    long, summaries, reconciliation, contrasts, chance = [], [], [], [], []
    independent_checks = 0
    for e in config['endpoints']:
        sheet = book[e['sheet']]
        for group, cells in e['groups'].items():
            for cell in cells:
                value = sheet[cell].value
                if value is None:
                    continue
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
                    raise ValueError((e['id'], cell, value))
                assert abs(xml[e['sheet']][cell] - value) < 1e-12
                independent_checks += 1
                row = int(''.join(c for c in cell if c.isdigit()))
                block = [b for b, rs in e['blocks'].items() if row in rs]
                assert len(block) == 1
                long.append(dict(endpoint=e['id'], sheet=e['sheet'], cell=cell,
                                 source_row_id=e['sheet'] + '!' + cell, group=group,
                                 block=block[0], dose=e['dose_mg_mL'], value=value,
                                 unit=e['unit'], identity='source coordinate, not stable cross-assay mouse ID'))
            vals = [r['value'] for r in long if r['endpoint'] == e['id'] and r['group'] == group]
            assert len(vals) >= 2
            mean, sd = float(np.mean(vals)), float(np.std(vals, ddof=1))
            assert math.isclose(mean, statistics.mean(vals), rel_tol=1e-12, abs_tol=1e-12)
            assert math.isclose(sd, statistics.stdev(vals), rel_tol=1e-12, abs_tol=1e-12)
            independent_checks += 2
            summaries.append(dict(endpoint=e['id'], group=group, n=len(vals), mean=mean, sd=sd,
                                  median=float(np.median(vals)), min=min(vals), max=max(vals), unit=e['unit']))
            ref = e['source_mean_cells'][group]
            reported_mean = sheet[ref].value
            reconciliation.append(dict(endpoint=e['id'], item='cached_mean_' + group,
                locator=e['sheet'] + '!' + ref, reported=reported_mean, calculated=mean,
                difference=mean-reported_mean, agrees_abs_1e_6=abs(mean-reported_mean) < 1e-6))
        scopes = ['all'] + (list(e['blocks']) if len(e['blocks']) > 1 else [])
        for scope in scopes:
            data = {g: [r['value'] for r in long if r['endpoint'] == e['id'] and r['group'] == g
                        and (scope == 'all' or r['block'] == scope)] for g in e['groups']}
            for comparison in config['methods']['comparisons']:
                a, b = comparison.split('-')
                if a not in data or b not in data or min(len(data[a]), len(data[b])) < 2:
                    continue
                x, y = data[a], data[b]
                tied = len(set(x+y)) < len(x+y)
                method = 'asymptotic' if tied else 'exact'
                test = stats.mannwhitneyu(x, y, alternative='two-sided', method=method, use_continuity=True)
                u = independent_u(x, y)
                assert abs(u-test.statistic) < 1e-10
                independent_p = independent_asymptotic_p(x, y, u, True) if tied else independent_exact_p(len(x), len(y), u)
                assert math.isclose(independent_p, test.pvalue, rel_tol=1e-10, abs_tol=1e-12)
                independent_checks += 2
                reported = e['reported'].get(comparison, '') if scope == 'all' else ''
                rec = dict(endpoint=e['id'], scope=scope, comparison=comparison, n_a=len(x), n_b=len(y),
                    mean_difference=statistics.mean(x)-statistics.mean(y),
                    rank_biserial=2*u/(len(x)*len(y))-1, U=u, ties=tied,
                    p_primary=float(test.pvalue), primary_method=method + ('_tie_corrected_continuity' if tied else '_no_ties'),
                    p_asymptotic_continuity=float(stats.mannwhitneyu(x,y,method='asymptotic',use_continuity=True).pvalue),
                    p_asymptotic_no_continuity=float(stats.mannwhitneyu(x,y,method='asymptotic',use_continuity=False).pvalue),
                    p_reported=reported, reported_locator=e['sheet'] + '!' + e['source_statistics'],
                    interpretation='unadjusted reproduction' if reported != '' else 'predeclared descriptive/option diagnostic; no new discovery claim')
                contrasts.append(rec)
        if e['chance']:
            for group in e['groups']:
                vals = [r['value'] for r in long if r['endpoint'] == e['id'] and r['group'] == group]
                null = e['chance']['null']
                test = stats.ttest_1samp(vals, null, alternative='two-sided')
                t = (statistics.mean(vals)-null)/(statistics.stdev(vals)/math.sqrt(len(vals)))
                df = len(vals)-1
                beta_p = float(special.betainc(df/2, .5, df/(df+t*t)))
                assert math.isclose(t, test.statistic, rel_tol=1e-10)
                assert math.isclose(beta_p, test.pvalue, rel_tol=1e-10)
                independent_checks += 2
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    signed = stats.wilcoxon(np.array(vals)-null, alternative='two-sided', zero_method='wilcox', method='approx')
                chance.append(dict(endpoint=e['id'], group=group, n=len(vals), null=null,
                    t=float(test.statistic), df=df, p_t_two_sided=float(test.pvalue),
                    p_signed_rank_asymptotic_diagnostic=float(signed.pvalue),
                    p_reported=e['chance']['reported'][group], interpretation='within-group comparison with chance; not treatment effect'))
    csv_out(out/'observations.csv', long)
    csv_out(out/'summaries.csv', summaries)
    csv_out(out/'contrasts.csv', contrasts)
    csv_out(out/'chance_tests.csv', chance)
    csv_out(out/'source_mean_reconciliation.csv', reconciliation)
    for name, ids in [('cognition', ['ymaze','nor','open_field','dg_cd68']),
                      ('neurogenesis', ['svz_dcx','ob_dcx_edu','ob_neun_edu']),
                      ('nesting', ['nesting_high','nesting_low','nesting_combined','nesting_ripr']),
                      ('immune_protein', ['cd86','bst2','mhci','svz_cd68','ifitm3'])]:
        plot_group(out, name, [e for e in config['endpoints'] if e['id'] in ids], long, contrasts, config['plot_seed'])
    result = {'candidate':'Nn26-P01', 'analysis_type':'exposed reproduction',
        'endpoints':len(config['endpoints']), 'traceable_observation_records':len(long),
        'observation_count_is_not_unique_mice':True,
        'independent_numeric_checks':independent_checks,
        'source_mean_mismatches':[r for r in reconciliation if not r['agrees_abs_1e_6']],
        'primary_p_differences_over_0_001':[r for r in contrasts if r['p_reported'] != '' and abs(r['p_primary']-r['p_reported']) > .001],
        'limits':[e['id']+': '+e['limit'] for e in config['endpoints'] if e['limit']],
        'new_intervals':'not estimated; no invented animal pairing, scale or margin',
        'scientific_acceptance':'not_assessed',
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
                       'scipy':scipy.__version__,'openpyxl':openpyxl.__version__,'matplotlib':matplotlib.__version__}}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (out/'validation.json').write_text(json.dumps({'status':'passed','independent_checks':independent_checks,
        'methods':'OOXML source cells; standard-library moments; pairwise U; rank-sum dynamic programming or erfc tie correction; beta-function t probability'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'endpoints':len(config['endpoints']),'checks':independent_checks,'source_mean_mismatches':len(result['source_mean_mismatches'])}))


if __name__ == '__main__':
    main()
