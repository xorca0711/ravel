"""Annotation-fixed finite-track relative ranks; no original-domain reproduction."""
import argparse
import gzip
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd

TIE = 1e-10
GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
CANONICAL = ['chr' + str(i) for i in range(1, 20)] + ['chrX']
QUANTILES = [0, .25, .5, .75, .9, .95, 1]


def save(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
def tsv(path, frame):
    if path.name.endswith('.gz'):
        with path.open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as handle:
                    frame.to_csv(handle, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')
    else: frame.to_csv(path, sep='\t', index=False, na_rep='NA', float_format='%.17g', lineterminator='\n')


def annotation_windows(gtf, chrom_sizes):
    annotations, mappings, windows = {}, [], {}
    with gzip.open(gtf, 'rt') as handle:
        for line in handle:
            if line.startswith('#'): continue
            f = line.rstrip().split('\t')
            if len(f) != 9 or f[2] != 'gene': continue
            a = dict(re.findall(r'(\w+) "([^"]*)";', f[8])); gene = a['gene_id']
            assert gene not in annotations
            a.update(chrom=f[0], strand=f[6], tss=int(f[3]) - 1 if f[6] == '+' else int(f[4]) - 1)
            annotations[gene] = a
            if a['gene_type'] != 'protein_coding' or f[0] not in CANONICAL: continue
            assert f[6] in ['+', '-'] and 0 <= a['tss'] < chrom_sizes[f[0]]
            for flank in [1000, 2000]:
                start, end = max(0, a['tss'] - flank), min(chrom_sizes[f[0]], a['tss'] + flank)
                key = f'{flank}:{f[0]}:{start}-{end}'; anchor = f"{f[0]}:{a['tss']}"
                row = {'window_id': key, 'anchor_id': anchor, 'flank': flank, 'chrom': f[0], 'start': start, 'end': end,
                       'clipped': start != a['tss'] - flank or end != a['tss'] + flank}
                if key in windows: assert windows[key]['anchor_id'] == anchor, 'unexpected clipped anchor collision; review required'
                windows[key] = row
                mappings.append({'gene_id': gene, 'gene_name': a['gene_name'], 'gene_type': a['gene_type'], 'strand': f[6],
                                 'tss': a['tss'], 'window_id': key, 'anchor_id': anchor, 'flank': flank})
    order = lambda r: (r['flank'], CANONICAL.index(r['chrom']), r['start'], r['end'])
    return pd.DataFrame(sorted(windows.values(), key=order)), pd.DataFrame(mappings), annotations


def percentile_points(values):
    values = np.asarray(values, dtype=float)
    if len(values) < 2 or not np.isfinite(values).all(): raise ValueError('Ranks require at least two finite window means')
    order = np.argsort(values, kind='stable'); sorted_values = values[order]
    starts = np.r_[0, np.flatnonzero(sorted_values[1:] != sorted_values[:-1]) + 1]
    ends = np.r_[starts[1:], len(values)]
    ranks = 100 * ((starts + ends - 1) / 2) / (len(values) - 1)
    out = np.empty(len(values)); out[order] = np.repeat(ranks, ends - starts)
    assert abs(float(out.mean()) - 50) <= TIE
    return out


def flip(a, b): return ((a > TIE) & (b < -TIE)) | ((a < -TIE) & (b > TIE))
def quantiles(x): return {str(q): float(np.quantile(x, q)) for q in QUANTILES}


def analyze(windows, signal):
    assert not signal.duplicated(['window_id', 'gsm']).any()
    assert set(signal.gsm) == set(GSMS) and len(signal) == len(windows) * 8
    frame = windows.copy(); diagnostics = []
    for gsm in GSMS:
        part = signal.loc[signal.gsm == gsm].set_index('window_id').loc[frame.window_id]
        frame[gsm + '__mean'] = part.mean_signal.to_numpy(dtype=float)
        frame[gsm + '__zero_bases'] = part.encoded_zero_bases.to_numpy(dtype=int)
        frame[gsm + '__percentile'] = np.nan
        for flank in [1000, 2000]:
            mask = frame.flank == flank; v = frame.loc[mask, gsm + '__mean'].to_numpy()
            ranks = percentile_points(v); frame.loc[mask, gsm + '__percentile'] = ranks
            counts = np.unique(v, return_counts=True)[1]
            diagnostics.append({'gsm': gsm, 'flank': flank, 'windows': len(v), 'mean_percentile': float(ranks.mean()),
                                'zero_mean_windows': int((v == 0).sum()), 'unique_means': len(counts),
                                'tied_windows': int(counts[counts > 1].sum()), 'largest_tie_group': int(counts.max())})
    for phase, group in [('D6', GSMS[:4]), ('D30', GSMS[4:])]:
        c = frame[[g + '__percentile' for g in group[:2]]].to_numpy(); h = frame[[g + '__percentile' for g in group[2:]]].to_numpy()
        frame[phase + '_delta'] = h.mean(axis=1) - c.mean(axis=1)
        combinations = np.stack([h[:, i] - c[:, j] for i in range(2) for j in range(2)], axis=1)
        for k, name in enumerate(['h1_c1', 'h1_c2', 'h2_c1', 'h2_c2']): frame[phase + '_' + name] = combinations[:, k]
        frame[phase + '_range_min'] = combinations.min(axis=1); frame[phase + '_range_max'] = combinations.max(axis=1)
        frame[phase + '_range_width'] = np.ptp(combinations, axis=1)
        frame[phase + '_range_touches_zero'] = (combinations.min(axis=1) <= TIE) & (combinations.max(axis=1) >= -TIE)
    summary = {'by_flank': {}, 'width_sensitivity': {}, 'units': 'percentile points of within-library ordering', 'population_inference': False,
               'global_mean_rank_is_constrained': True, 'original_memory_domain_classification': False}
    for flank in [1000, 2000]:
        f = frame.loc[frame.flank == flank]; block = {'windows': len(f)}
        for phase in ['D6', 'D30']:
            d = f[phase + '_delta'].to_numpy()
            block[phase + '_delta_quantiles'] = quantiles(d); block[phase + '_absolute_delta_quantiles'] = quantiles(np.abs(d))
            block[phase + '_range_width_quantiles'] = quantiles(f[phase + '_range_width'].to_numpy())
            block[phase + '_fraction_range_touches_zero'] = float(f[phase + '_range_touches_zero'].mean())
            block[phase + '_fraction_computational_zero'] = float((np.abs(d) <= TIE).mean())
            block[phase + '_mean_delta_constrained_zero'] = float(d.mean())
        block['fraction_absolute_D30_smaller_than_D6'] = float((np.abs(f.D30_delta) < np.abs(f.D6_delta) - TIE).mean())
        block['fraction_opposite_D6_D30_signs'] = float(flip(f.D6_delta.to_numpy(), f.D30_delta.to_numpy()).mean())
        summary['by_flank'][str(flank)] = block
    primary = frame.loc[frame.flank == 1000].set_index('anchor_id'); sensitivity = frame.loc[frame.flank == 2000].set_index('anchor_id').loc[primary.index]
    for phase in ['D6', 'D30']:
        a, b = primary[phase + '_delta'].to_numpy(), sensitivity[phase + '_delta'].to_numpy(); shift = b - a
        summary['width_sensitivity'][phase] = {'shift_quantiles': quantiles(shift), 'absolute_shift_quantiles': quantiles(np.abs(shift)),
            'fraction_sign_flip': float(flip(a, b).mean()), 'fraction_computational_zero_status_change': float(((np.abs(a) <= TIE) != (np.abs(b) <= TIE)).mean())}
    return frame, pd.DataFrame(diagnostics), summary


def prepare_examples(selected_path, annotations, mappings):
    selected = pd.read_csv(selected_path, sep='\t', dtype=str, keep_default_na=False)
    examples = [{'gene_id': 'ENSMUSG00000037860.15', 'gene_name': 'Aim2', 'selection_reason': 'published anchor; not newly selected'}]
    examples += selected[['gene_id', 'gene_name', 'selection_reason']].to_dict('records')
    eligible = set(mappings.gene_id)
    for slot, e in enumerate(examples, 1):
        e['plot_slot'] = slot; e['eligible'] = e['gene_id'] in eligible
        a = annotations.get(e['gene_id']); e['annotation_gene_type'] = a['gene_type'] if a else 'NA'
        e['status'] = 'assayed_TSS_proxy' if e['eligible'] else ('unassayed_non_protein_coding' if a and a['gene_type'] != 'protein_coding' else 'unassayed_annotation_or_chromosome')
    return examples


def run(contract_path, output):
    started = time.monotonic(); root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig')); inputs = {Path(i['path']).name: root / i['path'] for i in contract['inputs']}
    sizes = {line.split()[0]: int(line.split()[1]) for line in inputs['mm10.chrom.sizes'].read_text().splitlines()}
    windows, mappings, annotations = annotation_windows(inputs['gencode.vM9.annotation.gtf.gz'], sizes)
    assert mappings.gene_id.nunique() == 21775 and len(windows) == 43520 and not windows.clipped.any()
    assert all(int((windows.flank == f).sum()) == 21760 for f in [1000, 2000])
    tsv(output / 'windows.tsv', windows); tsv(output / 'gene_window_map.tsv.gz', mappings)
    examples = prepare_examples(inputs['selected_cases.tsv'], annotations, mappings); save(output / 'example_manifest.json', examples)
    chosen = []
    for flank in [1000, 2000]:
        f = windows.loc[windows.flank == flank].reset_index(drop=True)
        spaced = {int(i * (len(f) - 1) // 31) for i in range(32)}
        anchor_ids = set(mappings.loc[(mappings.flank == flank) & mappings.gene_id.isin([e['gene_id'] for e in examples if e['eligible']]), 'window_id'])
        for i, row in f.iterrows():
            reasons = (['annotation_order_spaced'] if i in spaced else []) + (['fixed_example'] if row.window_id in anchor_ids else [])
            if reasons: chosen.append({'window_id': row.window_id, 'flank': flank, 'selection_reason': '|'.join(reasons)})
    tsv(output / 'verification_windows.tsv', pd.DataFrame(chosen))
    wsl_root = subprocess.run(['wsl.exe', '--exec', 'wslpath', '-a', str(root)], capture_output=True, text=True, check=True).stdout.strip()
    def linux(path): return wsl_root + '/' + path.resolve().relative_to(root).as_posix()
    python = wsl_root + '/raw_data/naik2017_s3_runtime_v1/venv/bin/python'
    def remaining():
        seconds = 7200 - (time.monotonic() - started)
        if seconds <= 0: raise RuntimeError('Analysis wall budget exceeded; outputs preserved')
        return seconds
    subprocess.run(['wsl.exe', '--exec', python, linux(Path(__file__).with_name('s3_rank_extract_v1.py')), '--windows', linux(output / 'windows.tsv'),
                    '--manifest', linux(inputs['acquisition_manifest_v1.json']), '--output', linux(output), '--max-seconds', str(remaining())], check=True)
    subprocess.run(['wsl.exe', '--exec', python, linux(Path(__file__).with_name('s3_rank_mean_verify_v1.py')), '--output', linux(output),
                    '--manifest', linux(inputs['acquisition_manifest_v1.json']), '--max-seconds', str(remaining())], check=True)
    signal = pd.read_csv(output / 'window_signal.tsv.gz', sep='\t', float_precision='round_trip')
    frame, diagnostics, summary = analyze(windows, signal); summary['analysis_id'] = contract['analysis_id']
    tsv(output / 'window_effects.tsv.gz', frame); tsv(output / 'library_diagnostics.tsv', diagnostics); save(output / 'summary.json', summary)
    rows = []
    for e in examples:
        for flank in [1000, 2000]:
            row = dict(e, flank=flank)
            if e['eligible']:
                key = mappings.loc[(mappings.gene_id == e['gene_id']) & (mappings.flank == flank), 'window_id'].item()
                row.update(frame.loc[frame.window_id == key].iloc[0].to_dict())
            rows.append(row)
    cases = pd.DataFrame(rows); tsv(output / 'selected_cases.tsv', cases)
    from s3_rank_plot_v1 import plot
    plot(output, frame, cases)
    import matplotlib
    save(output / 'runtime.json', {'host_python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__, 'matplotlib': matplotlib.__version__,
                                   'elapsed_seconds_before_final_verification': time.monotonic() - started, 'analysis_wall_budget_seconds': 7200,
                                   'reader': {'python': '3.13.18', 'pybbi': '0.4.2', 'numpy': '2.5.5', 'peak_rss_limit_mib': 2048}, 'stochastic_steps': 'none'})
    subprocess.run([sys.executable, str(Path(__file__).with_name('s3_rank_verify_v1.py')), '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True, timeout=remaining())
    remaining()
    total_bytes = sum(p.stat().st_size for p in output.iterdir() if p.is_file())
    assert total_bytes < 50 * 1024 * 1024, 'Derived artifact budget exceeded; preserve output for review'
    print(json.dumps({'analysis_id': contract['analysis_id'], 'windows_per_width': 21760, 'genes': 21775, 'derived_bytes_before_receipt': total_bytes,
                      'analysis_elapsed_seconds': time.monotonic() - started, 'status': 'completed_descriptive_rank_endpoint'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--contract', type=Path, required=True); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); run(args.contract, args.output)
