"""Separate interval-weighted exact means for the prespecified readback subset."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path
import resource
import time

import bbi


def interval_mean(track, chrom, start, end):
    cursor, zeros, count, weighted = start, 0, 0, []
    for name, left, right, value in track.fetch_intervals(chrom, start, end, iterator=True):
        left, right = max(start, left), min(end, right)
        if right <= left: continue
        assert name == chrom and left == cursor and math.isfinite(value), 'gap/overlap/nonfinite interval'
        width = right - left; weighted.append(width * value); zeros += width if value == 0 else 0
        cursor = right; count += 1
    assert cursor == end, 'incomplete interval coverage'
    return math.fsum(weighted) / (end - start), zeros, count


def verify_subset(output, manifest_path, max_seconds):
    root = Path(__file__).resolve().parents[3]; started = time.monotonic()
    with (output / 'verification_windows.tsv').open() as f: chosen = {r['window_id'] for r in csv.DictReader(f, delimiter='\t')}
    with (output / 'windows.tsv').open() as f: windows = {r['window_id']: r for r in csv.DictReader(f, delimiter='\t') if r['window_id'] in chosen}
    primary = {}
    with gzip.open(output / 'window_signal.tsv.gz', 'rt') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['window_id'] in chosen: primary[(r['gsm'], r['window_id'])] = (float(r['mean_signal']), int(r['encoded_zero_bases']))
    sources = json.loads(manifest_path.read_text())['files']; maximum = 0.0; checked = 0
    with (output / 'mean_readback.tsv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(['gsm', 'window_id', 'base_array_mean', 'interval_weighted_mean', 'encoded_zero_bases', 'intervals', 'scaled_error'])
        for source in sources:
            with bbi.open(str(root / 'raw_data/naik2017_s3_sources' / source['filename'])) as track:
                for key, window in windows.items():
                    value, zeros, count = interval_mean(track, window['chrom'], int(window['start']), int(window['end']))
                    expected, expected_zeros = primary[(source['gsm'], key)]
                    error = abs(value - expected) / max(1, abs(expected)); maximum = max(maximum, error)
                    assert error <= 1e-10 and zeros == expected_zeros, 'independent exact-mean mismatch'
                    writer.writerow([source['gsm'], key, format(expected, '.17g'), format(value, '.17g'), zeros, count, format(error, '.17g')]); checked += 1
                    if time.monotonic() - started > max_seconds or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 2 * 1024 * 1024:
                        raise RuntimeError('Exact-readback resource budget exceeded; partial output preserved')
    print(json.dumps({'readback_checks': checked, 'maximum_scaled_error': maximum}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True); parser.add_argument('--manifest', type=Path, required=True); parser.add_argument('--max-seconds', type=float, required=True)
    args = parser.parse_args(); verify_subset(args.output, args.manifest, args.max_seconds)
