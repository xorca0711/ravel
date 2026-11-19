"""Pinned pybbi reader: qualify every header before any research-window fetch."""
import argparse
import csv
import gzip
import importlib.metadata
import io
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np


def save(path, value): path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def rows(path):
    opener = gzip.open if path.name.endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8', newline='') as f: return list(csv.DictReader(f, delimiter='\t'))


def array_summary(values, length):
    if len(values) != length or not np.isfinite(values).all():
        raise ValueError('Missing/nonfinite base or wrong length; no imputation or exclusion')
    return float(np.mean(values, dtype=np.float64)), int(np.count_nonzero(values == 0))


def qualify_headers(sources, sizes, required, root, backend, old_headers):
    tracks, decisions, failures = [], [], []
    old_dictionary = old_headers['tracks'][0]['chromosomes']
    assert all(t['chromosomes'] == old_dictionary for t in old_headers['tracks'])
    for source in sources:
        gsm = source['gsm']; path = str(root/source['path'])
        try:
            if not backend.is_bigwig(path): raise ValueError('Source is not a recognized BigWig')
            chroms = backend.chromsizes(path)
            tracks.append(dict(gsm=gsm, path=source['path'], is_bigwig=True, chromosomes=chroms,
                stored_header=backend.info(path), zoom_levels=backend.zooms(path)))
            needed = {c:dict(track=chroms.get(c), mm10=sizes[c], matches=chroms.get(c) == sizes[c]) for c in sorted(required)}
            unused = {c:dict(track=chroms[c], mm10=sizes.get(c), matches=chroms[c] == sizes.get(c)) for c in sorted(set(chroms)-set(required))}
            comparison = {c:dict(D180=chroms.get(c), S3=old_dictionary.get(c)) for c in sorted(set(chroms)|set(old_dictionary)) if chroms.get(c) != old_dictionary.get(c)}
            ok = all(x['matches'] for x in needed.values())
            decisions.append(dict(gsm=gsm, required_chromosomes=needed, unused_track_chromosomes=unused,
                mm10_chromosomes_not_in_track=sorted(set(sizes)-set(chroms)), differences_from_S3_dictionary=comparison,
                qualified_for_window_extraction=ok))
            if not ok: failures.append(dict(gsm=gsm, error='Required chromosome absent or length differs from frozen mm10'))
        except Exception as error:
            failures.append(dict(gsm=gsm, error=str(error)))
    qualification = dict(status='qualified_headers' if not failures else 'failed_before_extraction',
        all_four_headers_qualified=not failures and len(tracks) == 4, required_chromosomes=sorted(required),
        tracks=decisions, failures=failures, full_window_signal_qualified=False,
        signal_units='unresolved', original_retained_domains='not supplied by this proxy analysis',
        between_track_raw_signal_comparison=False, population_inference=False)
    return dict(tracks=tracks, research_window_values_read=False), qualification


def extract(output, sources, windows, root, backend, budget):
    written, completed = 0, []; progress = dict(status='running')
    def checkpoint(gsm, count, status='running'):
        progress.update(status=status, current_library=gsm, windows_completed_in_current_library=count,
            rows_written=written, completed_libraries=list(completed), **budget())
        save(output/'extraction_progress.json', progress)
    try:
        with (output/'window_signal.tsv.gz').open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8', newline='') as handle:
                    writer=csv.writer(handle,delimiter='\t',lineterminator='\n')
                    writer.writerow(['window_id','gsm','mean_signal','encoded_zero_bases'])
                    for source in sources:
                        gsm=source['gsm'];checkpoint(gsm,0)
                        with backend.open(str(root/source['path'])) as track:
                            for i, window in enumerate(windows,1):
                                start,end=int(window['start']),int(window['end'])
                                values=track.fetch(window['chrom'],start,end,missing=np.nan,exact=True)
                                mean,zeros=array_summary(values,end-start)
                                writer.writerow([window['window_id'],gsm,format(mean,'.17g'),zeros]);written+=1
                                if i % 128 == 0: checkpoint(gsm,i)
                        handle.flush();completed.append(gsm);checkpoint(gsm,len(windows))
                        print(json.dumps(dict(event='D180_library_complete',gsm=gsm,windows=len(windows),**budget())),flush=True)
        checkpoint(sources[-1]['gsm'],len(windows),'completed')
    except Exception as error:
        progress.update(status='failed_partial_preserved',error=str(error),rows_written=written)
        save(output/'extraction_progress.json',progress);raise


def readback(output,sources,windows,root,backend,budget):
    # Immutable S3 interval-iterator implementation; separate from base-array reduction.
    from s3_rank_mean_verify_v1 import interval_mean
    chosen={r['window_id'] for r in rows(output/'verification_windows.tsv')}
    subset=[w for w in windows if w['window_id'] in chosen]
    primary={(r['gsm'],r['window_id']):(float(r['mean_signal']),int(r['encoded_zero_bases']))
        for r in rows(output/'window_signal.tsv.gz') if r['window_id'] in chosen}
    checked,maximum=0,0.;progress=dict(status='running',checks=0)
    try:
        with (output/'mean_readback.tsv').open('w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f,delimiter='\t',lineterminator='\n')
            writer.writerow(['gsm','window_id','base_array_mean','interval_weighted_mean','encoded_zero_bases','intervals','scaled_error'])
            for source in sources:
                with backend.open(str(root/source['path'])) as track:
                    for w in subset:
                        value,zeros,count=interval_mean(track,w['chrom'],int(w['start']),int(w['end']))
                        expected,expected_zeros=primary[source['gsm'],w['window_id']]
                        error=abs(value-expected)/max(1,abs(expected));maximum=max(maximum,error)
                        assert math.isfinite(error) and error <= 1e-10 and zeros == expected_zeros
                        writer.writerow([source['gsm'],w['window_id'],format(expected,'.17g'),format(value,'.17g'),zeros,count,format(error,'.17g')])
                        checked+=1;progress.update(checks=checked,maximum_scaled_error=maximum,**budget())
                f.flush();save(output/'readback_progress.json',progress)
        progress.update(status='completed',same_binary_decoder=True,arithmetic='interval overlap lengths and math.fsum',**budget())
        save(output/'readback_progress.json',progress)
        print(json.dumps(dict(event='D180_interval_readback_complete',checks=checked,maximum_scaled_error=maximum,**budget())),flush=True)
    except Exception as error:
        progress.update(status='failed_partial_preserved',error=str(error),checks=checked)
        save(output/'readback_progress.json',progress);raise


def qualify_then_extract(output,sources,windows,sizes,root,backend,old_headers,budget,perform_readback=True):
    headers,qualification=qualify_headers(sources,sizes,{w['chrom'] for w in windows},root,backend,old_headers)
    save(output/'header_metadata.json',headers);save(output/'qualification.json',qualification)
    assert qualification['all_four_headers_qualified'], 'D180 qualification failed; no research-window extraction'
    extract(output,sources,windows,root,backend,budget)
    if perform_readback: readback(output,sources,windows,root,backend,budget)


def run(output,sizes_path,old_headers_path,max_seconds):
    import bbi
    import resource
    assert platform.machine() == 'aarch64' and sys.version_info[:3] == (3,13,18)
    assert importlib.metadata.version('pybbi') == '0.4.2' and np.__version__ == '2.5.5'
    started=time.monotonic();root=Path(__file__).resolve().parents[3]
    sources=json.loads((output/'source_manifest.json').read_text())['files'];windows=rows(output/'windows.tsv')
    sizes={line.split()[0]:int(line.split()[1]) for line in sizes_path.read_text().splitlines()}
    def budget():
        elapsed=time.monotonic()-started;rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
        if elapsed > max_seconds or rss > 2048: raise RuntimeError('Reader resource budget exceeded; preserve partial outputs')
        return dict(elapsed_seconds=elapsed,peak_rss_mib=rss)
    qualify_then_extract(output,sources,windows,sizes,root,bbi,json.loads(old_headers_path.read_text()),budget)


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--sizes',type=Path,required=True)
    parser.add_argument('--s3-headers',type=Path,required=True);parser.add_argument('--max-seconds',type=float,required=True)
    a=parser.parse_args();run(a.output,a.sizes,a.s3_headers,a.max_seconds)
