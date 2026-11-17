"""Independent stdlib checks of S3Q provenance, joins and metadata consistency."""
import argparse
import csv
import gzip
import json
import math
from pathlib import Path


def verify(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = {Path(x['path']).name: (root / x['path'], x) for x in contract['inputs']}
    manifest = json.loads(inputs['acquisition_manifest_v1.json'][0].read_text())
    source = {x['gsm']: x for x in manifest['files']}
    expected = ['GSM' + str(i) for i in range(2441001, 2441009)]
    checks = 0
    def equal(a, b, label):
        nonlocal checks
        checks += 1
        assert a == b, (label, a, b)
    with inputs['library_crosswalk.tsv'][0].open() as handle: cross = {x['gsm']: x for x in csv.DictReader(handle, delimiter='\t')}
    declared, current = {}, None
    with gzip.open(inputs['GSE92967_family.soft.gz'][0], 'rt') as handle:
        for line in handle:
            if line.startswith('^SAMPLE = '): current = line.strip().split(' = ')[1]
            if current in expected and line.startswith('!Sample_supplementary_file'): declared.setdefault(current, []).append(line.strip().split(' = ', 1)[1])
    with (output / 'source_identity.tsv').open() as handle: identities = list(csv.DictReader(handle, delimiter='\t'))
    equal([row['gsm'] for row in identities], expected, 'identity/order')
    for row in identities:
        gsm = row['gsm']; original = source[gsm]; path, binding = inputs[row['filename']]
        equal(row['sha256'], binding['sha256'], 'hash binding'); equal(row['sha256'], original['sha256'], 'acquisition hash')
        equal(int(row['bytes']), path.stat().st_size, 'bytes'); equal(row['url'], declared[gsm][0].replace('ftp://', 'https://', 1), 'GEO URL')
        for key, field in [('title', 'title'), ('day', 'day_label'), ('history', 'history_label'), ('replicate_label', 'replicate_label'), ('genome_metadata', 'processing_reference'), ('processing_metadata', 'processing_metadata'), ('exact_pool_to_library_map', 'exact_pool_to_library_map')]: equal(row[key], cross[gsm][field], 'crosswalk:' + key)
    header = json.loads((output / 'header_metadata.json').read_text()); tracks = header['tracks']
    equal([x['gsm'] for x in tracks], expected, 'header/order')
    reference = {line.split()[0]: int(line.split()[1]) for line in inputs['mm10.chrom.sizes'][0].read_text().splitlines()}
    with (output / 'chromosome_dictionary.tsv').open() as handle: chromosome_rows = list(csv.DictReader(handle, delimiter='\t'))
    dictionary = {(x['gsm'], x['chromosome']): x for x in chromosome_rows}
    equal(len(dictionary), len(chromosome_rows), 'unique chromosome rows')
    equal(len(dictionary), sum(len(t['chromosomes']) for t in tracks), 'all chromosome rows')
    q = json.loads((output / 'qualification.json').read_text())
    equal(q['all_tracks_share_dictionary'], all(t['chromosomes'] == tracks[0]['chromosomes'] for t in tracks), 'shared dictionary')
    equal(q['all_track_chromosomes_match_mm10'], all(reference.get(c) == length for t in tracks for c, length in t['chromosomes'].items()), 'mm10 compatibility')
    canonical = {'chr' + str(i) for i in range(1, 20)} | {'chrX'}
    equal(q['all_autosomes_and_X_present'], all(canonical <= set(t['chromosomes']) for t in tracks), 'canonical chromosomes')
    for t, comparison in zip(tracks, q['chromosome_comparisons']):
        equal(t['is_bigwig'], True, 'reader format')
        equal(t['stored_header']['chromCount'], len(t['chromosomes']), 'header chromosome count')
        equal(comparison['gsm'], t['gsm'], 'comparison identity')
        equal(comparison['absent_reference_chromosomes'], sorted(set(reference) - set(t['chromosomes'])), 'missing reference chromosomes')
        equal(comparison['missing_autosomes_or_X'], sorted(canonical - set(t['chromosomes'])), 'missing autosomes/X')
        equal(comparison['mismatches_or_extras'], {c: {'track': length, 'mm10': reference.get(c)} for c, length in t['chromosomes'].items() if reference.get(c) != length}, 'mismatch inventory')
        for c, length in t['chromosomes'].items():
            row = dictionary[(t['gsm'], c)]
            equal(int(row['track_length']), length, 'track chromosome length')
            equal(row['mm10_length'], str(reference.get(c, 'NA')), 'reference chromosome length')
            equal(row['same_length'], str(reference.get(c) == length), 'length match flag')
        query = t['bounded_query']; equal((query['chrom'], query['start'], query['end'], query['missing']), ('chr1', 10000000, 10000100, 'NaN'), 'prespecified query')
        if query['status'] == 'readable':
            equal(query['returned_bases'], 100, 'query length'); equal(query['finite_bases'] + query['missing_bases'], 100, 'query missingness')
        summary = t['stored_header']['summary']
        equal(all(math.isfinite(x) for x in summary.values()), True, 'finite stored summary')
        equal(summary['min'] <= summary['mean'] <= summary['max'], True, 'stored summary range')
        equal(0 <= summary['basesCovered'] <= sum(t['chromosomes'].values()), True, 'covered bases bound')
        equal(summary['std'] >= 0, True, 'nonnegative stored std')
    equal(q['tracks'], 8, 'track count'); equal(q['total_bytes'], 6679503736, 'byte total')
    for key in ['between_track_signal_comparison', 'population_inference', 'new_biological_analysis']: equal(q[key], False, key)
    equal(header['between_track_signal_comparison'], False, 'reader scope')
    result = {'status': 'passed', 'checks': checks, 'tracks': 8,
              'scope': 'independent stdlib provenance/crosswalk/chromosome/summary-consistency checks; runner verifies actual input hashes',
              'all_signal_blocks_independently_decoded': False, 'independent_biological_replication': False}
    (output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8'); print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--contract', type=Path, required=True); parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args(); verify(args.contract, args.run_dir)
