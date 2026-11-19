"""Independent stdlib interval/mapping/rank/contrast/summary verification."""
import argparse
import csv
import gzip
import itertools
import json
import math
from pathlib import Path

TIE = 1e-10
GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
CHROMS = ['chr' + str(i) for i in range(1, 20)] + ['chrX']


def rows(path):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8', newline='') as f: yield from csv.DictReader(f, delimiter='\t')


def rank_points(values):
    ordered = sorted(enumerate(values), key=lambda x: x[1]); result = [None] * len(values); offset = 0
    for value, group in itertools.groupby(ordered, key=lambda x: x[1]):
        members = list(group); average_zero_rank = offset + (len(members) - 1) / 2
        for index, unused in members: result[index] = average_zero_rank / (len(values) - 1) * 100
        offset += len(members)
    return result


def quantile(values, q):
    ordered = sorted(values); x = (len(ordered) - 1) * q; lo, hi = math.floor(x), math.ceil(x)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (x - lo)


def opposite(a, b): return (a > TIE and b < -TIE) or (a < -TIE and b > TIE)


def verify(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig')); inputs = {Path(x['path']).name: root / x['path'] for x in contract['inputs']}
    checks, maximum = 0, 0.0
    def equal(a, b, label):
        nonlocal checks, maximum
        checks += 1
        if isinstance(b, bool): assert a == str(b) or (isinstance(a, bool) and a is b), (label, a, b)
        elif isinstance(b, (float, int)):
            value = float(a); assert math.isfinite(value) and math.isfinite(b), (label, a, b)
            error = abs(value - b) / max(1, abs(b)); maximum = max(maximum, error)
            assert error <= TIE, (label, a, b, error)
        else: assert a == b, (label, a, b)
    sizes = {line.split()[0]: int(line.split()[1]) for line in inputs['mm10.chrom.sizes'].read_text().splitlines()}
    genes, expected_windows, expected_maps = {}, {}, {}
    with gzip.open(inputs['gencode.vM9.annotation.gtf.gz'], 'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            fields = line.rstrip().split('\t')
            if len(fields) != 9 or fields[2] != 'gene': continue
            attributes = {}
            for entry in fields[8].split(';'):
                if entry.strip():
                    key, value = entry.strip().split(' ', 1); attributes[key] = value.strip('"')
            gene = attributes['gene_id']; assert gene not in genes
            attributes.update(chrom=fields[0], strand=fields[6], tss=int(fields[3 if fields[6] == '+' else 4]) - 1)
            genes[gene] = attributes
            if attributes['gene_type'] != 'protein_coding' or fields[0] not in CHROMS: continue
            for flank in [1000, 2000]:
                tss = attributes['tss']; start = max(0, tss - flank); end = min(sizes[fields[0]], tss + flank)
                key = str(flank) + ':' + fields[0] + ':' + str(start) + '-' + str(end)
                expected_windows[key] = {'window_id': key, 'anchor_id': fields[0] + ':' + str(tss), 'flank': flank,
                    'chrom': fields[0], 'start': start, 'end': end, 'clipped': start != tss-flank or end != tss+flank}
                expected_maps[(gene, flank)] = dict(gene_id=gene, gene_name=attributes['gene_name'], gene_type=attributes['gene_type'],
                    strand=fields[6], tss=tss, window_id=key, anchor_id=fields[0] + ':' + str(tss), flank=flank)
    windows = list(rows(output / 'windows.tsv')); ids = [w['window_id'] for w in windows]
    equal(set(ids), set(expected_windows), 'all windows retained'); equal(len(ids), len(set(ids)), 'unique windows')
    order = sorted(expected_windows, key=lambda k: (expected_windows[k]['flank'], CHROMS.index(expected_windows[k]['chrom']), expected_windows[k]['start'], expected_windows[k]['end']))
    equal(ids, order, 'annotation order')
    for row in windows:
        for key, value in expected_windows[row['window_id']].items(): equal(row[key], value, 'interval:' + key)
    mappings = list(rows(output / 'gene_window_map.tsv.gz'))
    equal(len(mappings), len(expected_maps), 'mapping count')
    seen = set()
    for row in mappings:
        key = (row['gene_id'], int(row['flank'])); assert key not in seen; seen.add(key)
        for field, value in expected_maps[key].items(): equal(row[field], value, 'mapping:' + field)
    equal(seen, set(expected_maps), 'many-gene mappings retained')
    source_examples = [{'gene_id': 'ENSMUSG00000037860.15', 'gene_name': 'Aim2', 'selection_reason': 'published anchor; not newly selected'}]
    source_examples += [{k: r[k] for k in ['gene_id', 'gene_name', 'selection_reason']} for r in rows(inputs['selected_cases.tsv'])]
    examples = json.loads((output / 'example_manifest.json').read_text()); equal(len(examples), 7, 'fixed example count')
    for slot, (e, source) in enumerate(zip(examples, source_examples), 1):
        for key, value in source.items(): equal(e[key], value, 'example selection')
        equal(e['plot_slot'], slot, 'example order'); eligible = (e['gene_id'], 1000) in expected_maps
        equal(e['eligible'], eligible, 'example eligibility')
        annotation = genes.get(e['gene_id']); equal(e['annotation_gene_type'], annotation['gene_type'] if annotation else 'NA', 'example annotation')
        status = 'assayed_TSS_proxy' if eligible else ('unassayed_non_protein_coding' if annotation and annotation['gene_type'] != 'protein_coding' else 'unassayed_annotation_or_chromosome')
        equal(e['status'], status, 'unassayed is not zero')
    chosen = {}
    for flank in [1000, 2000]:
        subset = [k for k in order if expected_windows[k]['flank'] == flank]
        spaced = {i * (len(subset) - 1) // 31 for i in range(32)}
        anchors = {expected_maps[(e['gene_id'], flank)]['window_id'] for e in examples if e['eligible']}
        for i, key in enumerate(subset):
            why = (['annotation_order_spaced'] if i in spaced else []) + (['fixed_example'] if key in anchors else [])
            if why: chosen[key] = '|'.join(why)
    actual_chosen = list(rows(output / 'verification_windows.tsv'))
    equal({r['window_id']: r['selection_reason'] for r in actual_chosen}, chosen, 'prespecified exact-readback subset')
    signals = {}
    for row in rows(output / 'window_signal.tsv.gz'):
        key = (row['window_id'], row['gsm']); assert key not in signals and key[0] in expected_windows and key[1] in GSMS
        value, zeros = float(row['mean_signal']), int(row['encoded_zero_bases']); assert math.isfinite(value)
        window = expected_windows[key[0]]; assert 0 <= zeros <= window['end'] - window['start']
        signals[key] = (value, zeros)
    equal(len(signals), len(order) * 8, 'complete signal matrix')
    ranks, diagnostics = {}, {}
    for flank in [1000, 2000]:
        subset = [k for k in order if expected_windows[k]['flank'] == flank]
        for gsm in GSMS:
            means = [signals[(key, gsm)][0] for key in subset]; points = rank_points(means)
            for key, value in zip(subset, points): ranks[(key, gsm)] = value
            equal(math.fsum(points) / len(points), 50, 'fixed mean rank')
            sizes_of_ties = [len(list(g)) for unused, g in itertools.groupby(sorted(means))]
            diagnostics[(gsm, flank)] = {'windows': len(means), 'mean_percentile': math.fsum(points)/len(points),
                'zero_mean_windows': sum(x == 0 for x in means), 'unique_means': len(sizes_of_ties),
                'tied_windows': sum(x for x in sizes_of_ties if x > 1), 'largest_tie_group': max(sizes_of_ties)}
    diagnostic_rows = list(rows(output / 'library_diagnostics.tsv'))
    equal(len(diagnostic_rows), len(diagnostics), 'diagnostic row count')
    equal({(r['gsm'], int(r['flank'])) for r in diagnostic_rows}, set(diagnostics), 'diagnostic coverage')
    for row in diagnostic_rows:
        for key, value in diagnostics[(row['gsm'], int(row['flank']))].items(): equal(row[key], value, 'diagnostic:' + key)
    effects, expected_effects = {}, {}
    for row in rows(output / 'window_effects.tsv.gz'):
        key = row['window_id']; assert key not in effects; effects[key] = row; expected = {}
        for field, value in expected_windows[key].items(): equal(row[field], value, 'effect coordinates')
        for gsm in GSMS:
            for suffix, value in [('mean', signals[(key, gsm)][0]), ('zero_bases', signals[(key, gsm)][1]), ('percentile', ranks[(key, gsm)])]:
                equal(row[gsm + '__' + suffix], value, 'effect library field')
        for phase, libraries in [('D6', GSMS[:4]), ('D30', GSMS[4:])]:
            p = [ranks[(key, gsm)] for gsm in libraries]
            combinations = [p[i] - p[j] for i in [2, 3] for j in [0, 1]]
            expected[phase + '_delta'] = (p[2] + p[3] - p[0] - p[1]) / 2
            for name, value in zip(['h1_c1', 'h1_c2', 'h2_c1', 'h2_c2'], combinations): expected[phase + '_' + name] = value
            expected.update({phase + '_range_min': min(combinations), phase + '_range_max': max(combinations), phase + '_range_width': max(combinations)-min(combinations),
                             phase + '_range_touches_zero': min(combinations) <= TIE and max(combinations) >= -TIE})
        for field, value in expected.items(): equal(row[field], value, field)
        expected_effects[key] = expected
    equal(set(effects), set(order), 'all effects retained')
    summary = json.loads((output / 'summary.json').read_text())
    equal(summary['analysis_id'], contract['analysis_id'], 'analysis ID')
    equal(summary['units'], 'percentile points of within-library ordering', 'rank units')
    equal(summary['population_inference'], False, 'no population inference')
    equal(summary['global_mean_rank_is_constrained'], True, 'rank mean constraint')
    equal(summary['original_memory_domain_classification'], False, 'no original domain classification')
    for flank in [1000, 2000]:
        subset = [k for k in order if expected_windows[k]['flank'] == flank]; n = len(subset); block = summary['by_flank'][str(flank)]
        equal(block['windows'], n, 'summary n')
        ds = {phase: [expected_effects[k][phase + '_delta'] for k in subset] for phase in ['D6', 'D30']}
        for phase in ['D6', 'D30']:
            vectors = {phase + '_delta_quantiles': ds[phase], phase + '_absolute_delta_quantiles': [abs(x) for x in ds[phase]],
                       phase + '_range_width_quantiles': [expected_effects[k][phase + '_range_width'] for k in subset]}
            for name, values in vectors.items():
                for q in [0, .25, .5, .75, .9, .95, 1]: equal(block[name][str(q)], quantile(values, q), name)
            equal(block[phase + '_fraction_range_touches_zero'], sum(expected_effects[k][phase + '_range_touches_zero'] for k in subset)/n, 'range fraction')
            equal(block[phase + '_fraction_computational_zero'], sum(abs(x) <= TIE for x in ds[phase])/n, 'zero fraction')
            equal(block[phase + '_mean_delta_constrained_zero'], math.fsum(ds[phase])/n, 'mean contrast'); equal(math.fsum(ds[phase])/n, 0, 'rank constraint')
        equal(block['fraction_absolute_D30_smaller_than_D6'], sum(abs(b) < abs(a)-TIE for a,b in zip(ds['D6'], ds['D30']))/n, 'absolute displacement fraction')
        equal(block['fraction_opposite_D6_D30_signs'], sum(opposite(a,b) for a,b in zip(ds['D6'],ds['D30']))/n, 'opposite direction fraction')
    by_anchor = {(w['anchor_id'], w['flank']): key for key,w in expected_windows.items()}
    anchors = sorted({anchor for anchor,flank in by_anchor}); n = len(anchors)
    for phase in ['D6', 'D30']:
        a = [expected_effects[by_anchor[(anchor,1000)]][phase+'_delta'] for anchor in anchors]
        b = [expected_effects[by_anchor[(anchor,2000)]][phase+'_delta'] for anchor in anchors]; shifts = [y-x for x,y in zip(a,b)]
        block = summary['width_sensitivity'][phase]
        for name, values in [('shift_quantiles',shifts),('absolute_shift_quantiles',[abs(x) for x in shifts])]:
            for q in [0,.25,.5,.75,.9,.95,1]: equal(block[name][str(q)],quantile(values,q),name)
        equal(block['fraction_sign_flip'],sum(opposite(x,y) for x,y in zip(a,b))/n,'width sign fraction')
        equal(block['fraction_computational_zero_status_change'],sum((abs(x)<=TIE)!=(abs(y)<=TIE) for x,y in zip(a,b))/n,'width zero fraction')
    readback = list(rows(output / 'mean_readback.tsv'))
    equal({(r['window_id'],r['gsm']) for r in readback}, {(key,gsm) for key in chosen for gsm in GSMS}, 'readback coverage')
    equal(len(readback),len(chosen)*8,'unique readback rows')
    for row in readback:
        key=(row['window_id'],row['gsm']); value,zeros=signals[key]
        equal(row['base_array_mean'],value,'readback primary'); equal(row['interval_weighted_mean'],value,'independent interval mean')
        equal(row['encoded_zero_bases'],zeros,'independent zero count')
        equal(row['scaled_error'],abs(float(row['interval_weighted_mean'])-value)/max(1,abs(value)),'readback error')
    cases = list(rows(output / 'selected_cases.tsv')); equal(len(cases),14,'all example/width rows')
    for row,(e,flank) in zip(cases,[(e,f) for e in examples for f in [1000,2000]]):
        for field,value in e.items(): equal(row[field],value,'case identity')
        equal(row['flank'],flank,'case width')
        if e['eligible']:
            key=expected_maps[(e['gene_id'],flank)]['window_id']
            for field,value in effects[key].items(): equal(row[field],value,'case effect copied')
        else:
            equal(row['D6_delta'],'NA','unassayed not zero'); equal(row['D30_delta'],'NA','unassayed not zero')
    result={'status':'passed','checks':checks,'genes':len({g for g,f in expected_maps}),'windows_per_width':len(anchors),
            'exact_readback_checks':len(readback),'maximum_scaled_error':maximum,'computational_tolerance':TIE,
            'scope':'independent GTF parsing, all mappings/ranks/contrasts/summaries and fixed examples; separately reread interval-weighted means on predetermined subset',
            'independent_binary_decoder':False,'independent_biological_replication':False}
    (output/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); print(json.dumps(result))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--contract',type=Path,required=True); parser.add_argument('--run-dir',type=Path,required=True)
    args=parser.parse_args(); verify(args.contract,args.run_dir)
