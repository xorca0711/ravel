"""Supported-reader metadata and one prespecified bounded readability query."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

import bbi
import numpy as np


def read_headers(manifest_path, output):
    root = Path(__file__).resolve().parents[3]
    manifest = json.loads(manifest_path.read_text())
    assert platform.machine() == 'aarch64' and sys.version_info[:3] == (3, 13, 18)
    assert importlib.metadata.version('pybbi') == '0.4.2' and np.__version__ == '2.5.5'
    tracks = []
    for source in manifest['files']:
        path = root / 'raw_data/naik2017_s3_sources' / source['filename']
        assert bbi.is_bigwig(str(path)), source['gsm']
        chroms = bbi.chromsizes(str(path))
        info = bbi.info(str(path))
        zooms = bbi.zooms(str(path))
        query = {'chrom': 'chr1', 'start': 10000000, 'end': 10000100, 'coordinate_system': 'zero-based half-open', 'missing': 'NaN'}
        if chroms.get('chr1', 0) >= query['end']:
            values = bbi.fetch(str(path), 'chr1', query['start'], query['end'], missing=np.nan, exact=True)
            assert len(values) == 100 and not np.isinf(values).any()
            query.update({'status': 'readable', 'returned_bases': len(values), 'finite_bases': int(np.isfinite(values).sum()), 'missing_bases': int(np.isnan(values).sum())})
        else:
            query['status'] = 'not_queryable_chromosome_dictionary'
        tracks.append({'gsm': source['gsm'], 'filename': source['filename'], 'is_bigwig': True, 'chromosomes': chroms,
                       'stored_header': info, 'zoom_levels': zooms, 'bounded_query': query})
    output.write_text(json.dumps({'reader': {'python': sys.version, 'machine': platform.machine(), 'pybbi': importlib.metadata.version('pybbi'), 'numpy': np.__version__},
                                'tracks': tracks, 'between_track_signal_comparison': False}, indent=2, allow_nan=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--manifest', type=Path, required=True); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); read_headers(args.manifest, args.output)
