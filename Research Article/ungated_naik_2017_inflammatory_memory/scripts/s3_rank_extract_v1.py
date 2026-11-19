"""Exact base-resolution window extraction in the pinned WSL reader environment."""
import argparse
import csv
import gzip
import io
import json
from pathlib import Path
import resource
import sys
import time
import importlib.metadata

import bbi
import numpy as np


def array_summary(values, expected_length):
    if len(values) != expected_length or not np.isfinite(values).all():
        raise ValueError('Unexpected missing/nonfinite value or length; no imputation/exclusion allowed')
    return float(np.mean(values, dtype=np.float64)), int(np.count_nonzero(values == 0))


def extract(windows_path, manifest_path, output, max_seconds):
    root = Path(__file__).resolve().parents[3]
    assert sys.version_info[:3] == (3, 13, 18) and importlib.metadata.version('pybbi') == '0.4.2' and np.__version__ == '2.5.5'
    with windows_path.open() as handle: windows = list(csv.DictReader(handle, delimiter='\t'))
    sources = json.loads(manifest_path.read_text())['files']
    started = time.monotonic(); completed = []; written = 0
    progress = {'status': 'running', 'rows_written': 0, 'completed_libraries': []}
    def checkpoint(gsm, count, status='running'):
        elapsed = time.monotonic() - started
        rss_mib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        progress.update(status=status, current_library=gsm, windows_completed_in_current_library=count,
                        rows_written=written, elapsed_seconds=elapsed, peak_rss_mib=rss_mib, completed_libraries=completed)
        (output / 'extraction_progress.json').write_text(json.dumps(progress, indent=2) + '\n')
        if elapsed > max_seconds or rss_mib > 2048:
            raise RuntimeError('Provisional runtime/memory budget exceeded; partial output preserved')
    try:
        with (output / 'window_signal.tsv.gz').open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as handle:
                    writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
                    writer.writerow(['window_id', 'gsm', 'mean_signal', 'encoded_zero_bases'])
                    for source in sources:
                        gsm = source['gsm']; checkpoint(gsm, 0)
                        path = root / 'raw_data/naik2017_s3_sources' / source['filename']
                        with bbi.open(str(path)) as track:
                            for index, window in enumerate(windows, 1):
                                start, end = int(window['start']), int(window['end'])
                                values = track.fetch(window['chrom'], start, end, missing=np.nan, exact=True)
                                mean, zeros = array_summary(values, end - start)
                                writer.writerow([window['window_id'], gsm, format(mean, '.17g'), zeros]); written += 1
                                if index % 128 == 0: checkpoint(gsm, index)
                        handle.flush()
                        completed.append(gsm); checkpoint(gsm, len(windows))
                        print(json.dumps({'event': 'library_complete', 'gsm': gsm, 'windows': len(windows),
                                          'elapsed_seconds': progress['elapsed_seconds'], 'peak_rss_mib': progress['peak_rss_mib']}), flush=True)
        checkpoint(sources[-1]['gsm'], len(windows), 'completed')
    except Exception as error:
        progress.update(status='failed_partial_preserved', error=str(error))
        (output / 'extraction_progress.json').write_text(json.dumps(progress, indent=2) + '\n')
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--windows', type=Path, required=True); parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True); parser.add_argument('--max-seconds', type=float, required=True)
    args = parser.parse_args(); extract(args.windows, args.manifest, args.output, args.max_seconds)
