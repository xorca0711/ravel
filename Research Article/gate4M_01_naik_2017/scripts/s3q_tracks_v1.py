"""S3Q metadata qualification; no biological accessibility comparison."""
import argparse
import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys


GSMS = ['GSM' + str(i) for i in range(2441001, 2441009)]
CANONICAL = ['chr' + str(i) for i in range(1, 20)] + ['chrX']


def save(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
def write_tsv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def run(contract_path, output):
    root = Path(__file__).resolve().parents[3]
    contract = json.loads(contract_path.read_text(encoding='utf-8-sig'))
    inputs = {Path(item['path']).name: root / item['path'] for item in contract['inputs']}
    manifest = json.loads(inputs['acquisition_manifest_v1.json'].read_text())
    assert [item['gsm'] for item in manifest['files']] == GSMS
    assert sum(item['bytes'] for item in manifest['files']) == 6679503736
    with inputs['library_crosswalk.tsv'].open() as handle: crosswalk = {r['gsm']: r for r in csv.DictReader(handle, delimiter='\t')}
    urls, current = {}, None
    with gzip.open(inputs['GSE92967_family.soft.gz'], 'rt') as handle:
        for line in handle:
            if line.startswith('^SAMPLE = '): current = line.strip().split(' = ')[1]
            if current in GSMS and line.startswith('!Sample_supplementary_file'):
                urls.setdefault(current, []).append(line.strip().split(' = ', 1)[1])
    identities = []
    for item in manifest['files']:
        gsm = item['gsm']; row = crosswalk[gsm]
        assert urls[gsm] == [item['declared_url']] and item['url'] == item['declared_url'].replace('ftp://', 'https://', 1)
        assert item['filename'] in inputs and inputs[item['filename']].stat().st_size == item['bytes']
        assert row['title'] == item['title'] and row['assay'] == 'ATAC-seq' and row['processing_reference'] == 'mm10'
        identities.append({'gsm': gsm, 'title': row['title'], 'day': row['day_label'], 'history': row['history_label'],
                           'replicate_label': row['replicate_label'], 'filename': item['filename'], 'url': item['url'],
                           'bytes': item['bytes'], 'sha256': item['sha256'], 'genome_metadata': row['processing_reference'],
                           'processing_metadata': row['processing_metadata'], 'exact_pool_to_library_map': row['exact_pool_to_library_map']})
    write_tsv(output / 'source_identity.tsv', identities)
    wsl_root = subprocess.run(['wsl.exe', '--exec', 'wslpath', '-a', str(root)], capture_output=True, text=True, check=True).stdout.strip()
    def linux(path): return wsl_root + '/' + path.resolve().relative_to(root).as_posix()
    reader = Path(__file__).with_name('s3q_reader_v1.py')
    python = wsl_root + '/raw_data/naik2017_s3_runtime_v1/venv/bin/python'
    subprocess.run(['wsl.exe', '--exec', python, linux(reader), '--manifest', linux(inputs['acquisition_manifest_v1.json']), '--output', linux(output / 'header_metadata.json')], check=True)
    headers = json.loads((output / 'header_metadata.json').read_text())
    reference = dict(line.split() for line in inputs['mm10.chrom.sizes'].read_text().splitlines())
    reference = {k: int(v) for k, v in reference.items()}
    chromosome_rows, comparisons = [], []
    for track in headers['tracks']:
        chroms = track['chromosomes']
        mismatches = {c: {'track': length, 'mm10': reference.get(c)} for c, length in chroms.items() if reference.get(c) != length}
        comparisons.append({'gsm': track['gsm'], 'chromosome_count': len(chroms), 'mismatches_or_extras': mismatches,
                            'absent_reference_chromosomes': sorted(set(reference) - set(chroms)),
                            'missing_autosomes_or_X': sorted(set(CANONICAL) - set(chroms)),
                            'chrM_present': 'chrM' in chroms, 'chrY_present': 'chrY' in chroms})
        for chrom, length in chroms.items():
            chromosome_rows.append({'gsm': track['gsm'], 'chromosome': chrom, 'track_length': length,
                                    'mm10_length': reference.get(chrom, 'NA'), 'same_length': reference.get(chrom) == length})
    write_tsv(output / 'chromosome_dictionary.tsv', chromosome_rows)
    qualification = {'analysis_id': contract['analysis_id'], 'tracks': 8, 'total_bytes': manifest['total_bytes'],
                     'all_tracks_share_dictionary': all(t['chromosomes'] == headers['tracks'][0]['chromosomes'] for t in headers['tracks']),
                     'all_track_chromosomes_match_mm10': all(not c['mismatches_or_extras'] for c in comparisons),
                     'all_autosomes_and_X_present': all(not c['missing_autosomes_or_X'] for c in comparisons),
                     'chromosome_comparisons': comparisons, 'scale_status': 'unresolved; GEO mm10/.bw metadata and stored header do not establish normalization',
                     'coordinate_universe_status': 'not recovered; coordinator source review reused, no new workbook scan',
                     'between_track_signal_comparison': False, 'population_inference': False, 'new_biological_analysis': False}
    save(output / 'qualification.json', qualification)
    save(output / 'runtime.json', {'host_python': sys.version, 'reader': headers['reader'], 'reader_environment_relative_path': 'raw_data/naik2017_s3_runtime_v1/venv'})
    subprocess.run([sys.executable, str(Path(__file__).with_name('s3q_verify_v1.py')), '--contract', str(contract_path.resolve()), '--run-dir', str(output.resolve())], check=True)
    print(json.dumps({'status': 'completed_metadata_only', 'tracks': len(identities), 'between_track_scale': 'unresolved'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--contract', type=Path, required=True); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); run(args.contract, args.output)
