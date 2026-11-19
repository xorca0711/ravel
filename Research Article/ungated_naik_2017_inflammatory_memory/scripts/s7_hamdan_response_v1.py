"""Bounded per-donor RNA interaction. Real execution requires a frozen contract."""
import argparse
import csv
import gzip
import io
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import pandas as pd

KEYS = ['NI0_1', 'NI0_2', 'NIT_1', 'NIT_2', 'I0_1', 'I0_2', 'IT_1', 'IT_2']
GROUPS = ['NI0', 'NIT', 'I0', 'IT']
ENDPOINTS = ['B', 'P', 'R_NI', 'R_I', 'A']
TOL = 1e-10


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def save_table(path, frame):
    if path.suffix == '.gz':
        with path.open('wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding='utf-8', newline='') as text:
                frame.to_csv(text, sep='\t', index=False, float_format='%.17g', lineterminator='\n')
    else:
        frame.to_csv(path, sep='\t', index=False, float_format='%.17g', lineterminator='\n')


def source_metadata(path, manifest):
    with gzip.open(path, 'rt', encoding='utf-8') as handle:
        text = handle.read()
    samples = {}
    for block in text.split('^SAMPLE = ')[1:]:
        gsm = block.splitlines()[0]
        if gsm in samples: raise ValueError('Duplicate SOFT sample')
        fields = {}
        for line in block.splitlines():
            if line.startswith('!Sample_') and ' = ' in line:
                key, value = line.split(' = ', 1)
                fields.setdefault(key, []).append(value)
        samples[gsm] = fields
    rows = manifest['samples']
    if len(rows) != 16 or len({r['gsm'] for r in rows}) != 16 or len({r['column'] for r in rows}) != 16:
        raise ValueError('Expected sixteen distinct source libraries')
    for patient in ['4', '83']:
        donor = [r for r in rows if r['patient'] == patient]
        if [r['key'] for r in donor] != KEYS: raise ValueError('Changed donor/condition order')
    for row in rows:
        m = samples.get(row['gsm'], {})
        expected = {'!Sample_description': row['column'], '!Sample_title': row['title'],
                    '!Sample_platform_id': row['platform']}
        if any(m.get(k) != [v] for k, v in expected.items()):
            raise ValueError('Ambiguous or changed exact GEO identity: '+row['gsm'])
    return pd.DataFrame(rows)


def read_counts(path, manifest):
    with gzip.open(path, 'rt', encoding='utf-8') as handle:
        source_reader = csv.reader(handle, delimiter='\t')
        header = next(source_reader)
        if any(len(row) != len(header) for row in source_reader):
            raise ValueError('Malformed source row width')
    expected = manifest['annotation_columns'] + manifest['source_columns']
    if header != expected or len(set(header)) != len(header):
        raise ValueError('Changed or duplicate source count header')
    selected = [r['column'] for r in manifest['samples']]
    frame = pd.read_csv(path, sep='\t', dtype=str, keep_default_na=False,
                        usecols=manifest['annotation_columns']+selected)
    if frame.empty or frame.GeneId.eq('').any() or frame.GeneId.duplicated().any():
        raise ValueError('Empty or duplicate source GeneId')
    counts = {}
    for patient in ['4', '83']:
        columns = [r['column'] for r in manifest['samples'] if r['patient'] == patient]
        part = frame[columns]
        if not all(part[c].str.fullmatch(r'[0-9]+').all() for c in columns):
            raise ValueError('Counts must be nonnegative integers without missing values')
        values = part.to_numpy(dtype=np.float64)
        if not np.isfinite(values).all() or (values >= 2**53).any() or (values.sum(axis=0) >= 2**53).any():
            raise ValueError('Counts/totals exceed exact float integer range')
        counts[patient] = values
    return frame[manifest['annotation_columns']].copy(), counts


def factors(counts):
    if counts.ndim != 2 or counts.shape[1] != 8 or not np.isfinite(counts).all() or (counts < 0).any():
        raise ValueError('Expected finite nonnegative gene-by-eight counts')
    totals = counts.sum(axis=0)
    positive = (counts > 0).all(axis=1)
    if (totals <= 0).any() or not positive.any():
        raise ValueError('Nonpositive total or empty all-eight-positive MOR reference')
    reference = counts[positive]
    gm = np.exp(np.log(reference).mean(axis=1))
    medians = np.median(reference / gm[:, None], axis=0)
    mor = medians / np.exp(np.log(medians).mean())
    total = totals / np.exp(np.log(totals).mean())
    if not all(np.isfinite(x).all() and (x > 0).all() for x in (mor, total)):
        raise ValueError('Invalid normalization factors')
    return {'MOR': mor, 'total': total}, totals, int(positive.sum())


def signs(values):
    return np.where(values > TOL, 1, np.where(values < -TOL, -1, 0))


def response(counts, size_factors):
    normalized = counts / size_factors
    means = normalized.reshape(-1, 4, 2).mean(axis=2)
    e = np.log2(means + 1)
    data = {**{'raw_'+k: counts[:, i].astype(np.int64) for i, k in enumerate(KEYS)},
            **{'norm_'+k: normalized[:, i] for i, k in enumerate(KEYS)},
            **{'mean_'+k: means[:, i] for i, k in enumerate(GROUPS)},
            **{'e_'+k: e[:, i] for i, k in enumerate(GROUPS)}}
    data.update(B=e[:, 2]-e[:, 0], P=e[:, 3]-e[:, 1],
                R_NI=e[:, 1]-e[:, 0], R_I=e[:, 3]-e[:, 2])
    data['A'] = data['P']-data['B']
    library_e = np.log2(normalized+1).reshape(-1, 4, 2)
    low, high = library_e.min(axis=2), library_e.max(axis=2)
    data['A_min'] = low[:, 3]-high[:, 2]-high[:, 1]+low[:, 0]
    data['A_max'] = high[:, 3]-low[:, 2]-low[:, 1]+high[:, 0]
    data['A_range_zero'] = (data['A_min'] <= TOL) & (data['A_max'] >= -TOL)
    data['eligible'] = (counts > 0).any(axis=1)
    data['all_raw_zero'] = ~data['eligible']
    data['any_raw_zero'] = (counts == 0).any(axis=1)
    for i, group in enumerate(GROUPS): data['both_zero_'+group] = (counts[:, i*2:i*2+2] == 0).all(axis=1)
    for endpoint in ENDPOINTS:
        data['sign_'+endpoint] = signs(data[endpoint])
    return pd.DataFrame(data)


def summarize(frame):
    f = frame.loc[frame.eligible]
    n = len(f)
    quantiles = {}
    for endpoint in ENDPOINTS+['abs_A']:
        a = f.A.abs() if endpoint == 'abs_A' else f[endpoint]
        quantiles[endpoint] = dict(zip(['q025', 'q25', 'q50', 'q75', 'q975'],
                                      np.quantile(a, [.025, .25, .5, .75, .975]).tolist())) if n else None
    tables = {}
    for x, y in [('P', 'A'), ('R_NI', 'R_I')]:
        tables[x+'_vs_'+y] = {str(a)+','+str(b): int(((f['sign_'+x] == a) & (f['sign_'+y] == b)).sum())
                               for a in [-1, 0, 1] for b in [-1, 0, 1]}
    strata = {}
    for name, subset in [('any_raw_zero', f.loc[f.any_raw_zero]), ('no_raw_zero', f.loc[~f.any_raw_zero])]:
        counts = {x+'_vs_'+y: {str(a)+','+str(b): int(((subset['sign_'+x] == a) & (subset['sign_'+y] == b)).sum())
                  for a in [-1, 0, 1] for b in [-1, 0, 1]} for x, y in [('P', 'A'), ('R_NI', 'R_I')]}
        strata[name] = dict(denominator=len(subset), sign_tables=counts,
            sign_fractions={k: {cell: count/len(subset) if len(subset) else None for cell, count in table.items()}
                            for k, table in counts.items()})
    post_positive = f.loc[f.sign_P == 1]
    conditional = {'denominator': len(post_positive)}
    for sign in [-1, 0, 1]:
        count = int((post_positive.sign_A == sign).sum())
        conditional[str(sign)] = {'count': count, 'fraction': count/len(post_positive) if len(post_positive) else None}
    apos = f.loc[f.sign_A == 1]
    return dict(source_gene_count=len(frame), eligible_count=n,
                structural_all_zero_count=int(frame.all_raw_zero.sum()),
                zero_flags={k: int(f[k].sum()) for k in ['any_raw_zero']+['both_zero_'+g for g in GROUPS]+['A_range_zero']},
                computational_zeros={k: int((f['sign_'+k] == 0).sum()) for k in ENDPOINTS},
                sign_tables=tables, raw_zero_strata=strata, post_positive_A=conditional,
                A_positive_responses={'denominator': len(apos),
                    'I_induced': int((apos.sign_R_I == 1).sum()),
                    'both_repressed': int(((apos.sign_R_I == -1) & (apos.sign_R_NI == -1)).sum())},
                quantiles=quantiles)


def sensitivity(primary, secondary):
    out = pd.DataFrame({'eligible': primary.eligible, 'A_MOR': primary.A, 'A_total': secondary.A,
                        'A_total_minus_MOR': secondary.A-primary.A,
                        'opposite_A_signs': primary.sign_A*secondary.sign_A == -1,
                        'A_zero_status_change': (primary.sign_A == 0) != (secondary.sign_A == 0)})
    f = out.loc[out.eligible]
    stats = {'eligible_count': len(f)}
    for field in ['opposite_A_signs', 'A_zero_status_change']:
        count = int(f[field].sum())
        stats[field] = {'count': count, 'fraction': count/len(f) if len(f) else None}
    stats['median_abs_A_shift'] = float(f.A_total_minus_MOR.abs().median()) if len(f) else None
    return out, stats


def calculate(count_path, metadata_path, manifest, output):
    sample_table = source_metadata(metadata_path, manifest)
    annotation, counts = read_counts(count_path, manifest)
    save_table(output/'source_samples.tsv', sample_table)
    norm_rows, responses, sensitivities, result_frames = [], [], [], {}
    summary = {'by_patient_method': {}, 'normalization_sensitivity': {}}
    for patient in ['4', '83']:
        sizes, totals, reference_n = factors(counts[patient])
        sample_rows = [s for s in manifest['samples'] if s['patient'] == patient]
        result_frames[patient] = {}
        for method, sf in sizes.items():
            frame = response(counts[patient], sf)
            result_frames[patient][method] = frame
            summary['by_patient_method'][patient+'_'+method] = summarize(frame)
            values = pd.concat([annotation, frame], axis=1)
            values.insert(0, 'method', method); values.insert(0, 'patient', patient)
            responses.append(values)
            for i, row in enumerate(sample_rows):
                norm_rows.append(dict(patient=patient, method=method, gsm=row['gsm'], column=row['column'],
                    key=row['key'], total=int(totals[i]), size_factor=float(sf[i]),
                    source_gene_count=len(annotation), positive_all_eight_reference_count=reference_n))
        sens, summary['normalization_sensitivity'][patient] = sensitivity(result_frames[patient]['MOR'], result_frames[patient]['total'])
        sens = pd.concat([annotation, sens], axis=1); sens.insert(0, 'patient', patient); sensitivities.append(sens)
    save_table(output/'normalization.tsv', pd.DataFrame(norm_rows))
    save_table(output/'gene_responses.tsv.gz', pd.concat(responses, ignore_index=True))
    save_table(output/'normalization_sensitivity.tsv.gz', pd.concat(sensitivities, ignore_index=True))
    save_json(output/'summary.json', summary)
    save_json(output/'source_structure.json', dict(source_gene_count=len(annotation),
        annotation_columns=manifest['annotation_columns'], source_columns=manifest['source_columns'],
        excluded_columns=manifest['excluded_columns'], patients=['4', '83'], selected_library_count=16,
        all_gene_rows_exported=True, culture_pairing='unknown', platform_discrepancy='GEO HiSeq4000; paper NextSeq2000'))
    return result_frames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', required=True); parser.add_argument('--output', required=True)
    args = parser.parse_args(); started = time.perf_counter()
    root, output = Path.cwd(), Path(args.output)
    contract = json.loads((root/args.contract).read_text(encoding='utf-8'))
    if contract['status'] != 'frozen': raise ValueError('S7 draft is not authorized for source execution')
    if contract['analysis_id'] != 'Nk17-P01.s7_hamdan_response_v1': raise ValueError('Wrong analysis ID')
    if any((output/name).exists() for name in contract['expected_outputs']): raise ValueError('Refuse output overwrite')
    output.mkdir(parents=True, exist_ok=True)
    inputs = {Path(x['path']).name: root/x['path'] for x in contract['inputs']}
    manifest = json.loads(inputs['S7_HAMDAN_SOURCE_MAP_V1.json'].read_text(encoding='utf-8'))
    frames = calculate(inputs['GSE282444_gene_counts.txt.gz'], inputs['GSE282444_family.soft.gz'], manifest, output)
    from s7_hamdan_plot_v1 import plot
    plot(frames, output)
    from s7_resources_v1 import peak_memory_bytes
    peak_memory_bytes()
    subprocess.run([sys.executable, str(Path(__file__).with_name('s7_hamdan_verify_v1.py')),
                    '--counts', str(inputs['GSE282444_gene_counts.txt.gz']), '--soft', str(inputs['GSE282444_family.soft.gz']),
                    '--map', str(inputs['S7_HAMDAN_SOURCE_MAP_V1.json']), '--output', str(output)], check=True,
                    timeout=max(1, 1800-(time.perf_counter()-started)))
    elapsed = time.perf_counter()-started
    total_bytes = sum(p.stat().st_size for p in output.iterdir() if p.is_file())
    save_json(output/'runtime.json', dict(elapsed_seconds_before_runtime=elapsed, output_bytes_before_runtime=total_bytes,
        python=sys.version, numpy=np.__version__, pandas=pd.__version__, execution_platform=sys.platform,
        memory_limit_bytes=2*1024**3, duration_limit_seconds=1800, output_limit_bytes=500*1024**2,
        peak_process_memory_bytes=peak_memory_bytes(),
        resource_check_scope='Observed process peak and post-stage elapsed/output checks; no OS memory sandbox'))
    if elapsed > 1800 or total_bytes > 500*1024**2: raise ValueError('Declared run resource ceiling exceeded')
    print('S7 all-source rows and independent verification completed; see full outputs for interpretation.')


if __name__ == '__main__': main()
