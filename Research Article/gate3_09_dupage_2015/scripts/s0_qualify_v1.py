"""Dp1-S0 metadata/feature qualification only; no biological contrast or test."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import tarfile

RAW = Path('raw_data/dupage_20261107')
KEY = ('gene_id', 'gene_short_name', 'locus')
EXCLUDED = 'GSM1423627'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(path, rows, fields=None):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)


def table(handle):
    return list(csv.DictReader(handle, delimiter='\t'))


def feature_key(row):
    return tuple(row[k] for k in KEY)


def reference_label(row):
    name = row['gene_short_name']
    return (name not in {'', '-'} and name == row['gene_id']
            and not name.startswith(('XLOC_', 'CUFF.'))
            and not any(c in name for c in ',;|')
            and re.fullmatch(r'chr[^:]+:\d+-\d+', row['locus']) is not None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    metadata = {}
    current = None
    for line in (RAW/'GSE58998_family.soft').read_text().splitlines():
        if line.startswith('^SAMPLE = '):
            current = line.split(' = ', 1)[1]
            metadata[current] = defaultdict(list)
        elif current and line.startswith('!Sample_') and ' = ' in line:
            k, v = line.split(' = ', 1)
            metadata[current][k.removeprefix('!Sample_')].append(v)
    assert len(metadata) == 12
    with (RAW/'ena_runs.tsv').open() as f:
        ena = table(f)
    assert len({r['run_accession'] for r in ena}) == len(ena)
    ena_by_exp = defaultdict(list)
    for row in ena:
        ena_by_exp[row['experiment_accession']].append(row)
    files = {}
    file_hashes = []
    with tarfile.open(RAW/'GSE58998_RAW.tar') as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            gsm = re.match(r'(GSM\d+)_', member.name).group(1)
            assert gsm not in files
            payload = archive.extractfile(member).read()
            files[gsm] = table(io.StringIO(gzip.decompress(payload).decode()))
            file_hashes.append({'gsm': gsm, 'member': member.name,
                                'compressed_sha256': hashlib.sha256(payload).hexdigest()})
    assert set(files) == set(metadata)
    manifests = []
    for gsm, meta in sorted(metadata.items()):
        title = meta['title'][0]
        match = re.fullmatch(r'Ezh2-(HET|KO)-CD62L(hi|lo) rep(\d+)', title)
        assert match, title
        relations = ' '.join(meta['relation'])
        srx = re.search(r'SRX\d+', relations).group()
        biosample = re.search(r'SAMN\d+', relations).group()
        runs = ena_by_exp[srx]
        assert runs and all(r['sample_accession'] == biosample for r in runs)
        characteristics = dict(x.split(': ', 1) for x in meta['characteristics_ch1'])
        manifests.append({
            'gsm': gsm, 'title': title, 'genotype': match[1], 'state': match[2],
            'source_replicate_label': match[3], 'retained': gsm != EXCLUDED,
            'exclusion': 'source low read count exclusion' if gsm == EXCLUDED else '',
            'srx': srx, 'biosample': biosample,
            'srr': ';'.join(r['run_accession'] for r in runs), 'runs': len(runs),
            'ena_read_count': sum(int(r['read_count']) for r in runs),
            'ena_base_count': sum(int(r['base_count']) for r in runs),
            'ena_fastq_bytes': sum(sum(int(x) for x in r['fastq_bytes'].split(';')) for r in runs),
            'layout': ';'.join(sorted({r['library_layout'] for r in runs})),
            'sex': characteristics['gender'], 'strain': characteristics['strain'],
            'tissue': characteristics['tissue'], 'cell_type': characteristics['cell type'],
            'mouse_id': 'unknown', 'pool_id': 'unknown', 'pairing': 'unknown',
            'age': 'unknown', 'batch': 'unknown', 'independent_animals': 'unknown',
            'assembly': 'mm10', 'annotation_release': 'unknown',
        })
    assert {m['srx'] for m in manifests} == set(ena_by_exp)
    retained = [g for g in sorted(files) if g != EXCLUDED]
    qc = []
    qualified = {}
    for gsm, rows in sorted(files.items()):
        key_count = Counter(feature_key(r) for r in rows)
        gene_count = Counter(r['gene_id'] for r in rows)
        track_count = Counter(r['tracking_id'] for r in rows)
        good = {}
        invalid = 0
        for row in rows:
            value = float(row['FPKM'])
            invalid += not math.isfinite(value) or value < 0
            if (reference_label(row) and key_count[feature_key(row)] == 1
                    and gene_count[row['gene_id']] == 1):
                good[feature_key(row)] = row
        qualified[gsm] = good
        qc.append({'gsm': gsm, 'rows': len(rows), 'unique_tracking': len(track_count),
                   'duplicate_tracking_keys': sum(v > 1 for v in track_count.values()),
                   'unique_feature_keys': len(key_count),
                   'duplicate_feature_keys': sum(v > 1 for v in key_count.values()),
                   'duplicated_gene_ids': sum(v > 1 for v in gene_count.values()),
                   'reference_label_rows': sum(reference_label(r) for r in rows),
                   'unique_reference_locus_rows': len(good),
                   'status_counts': json.dumps(dict(Counter(r['FPKM_status'] for r in rows)), sort_keys=True),
                   'invalid_or_negative_fpkm': invalid,
                   'zero_fpkm': sum(float(r['FPKM']) == 0 for r in rows),
                   'header': '|'.join(rows[0])})
    assert not any(q['invalid_or_negative_fpkm'] for q in qc)
    common = set.intersection(*(set(qualified[g]) for g in retained))
    all_common = set.intersection(*(set(x) for x in qualified.values()))
    union = set.union(*(set(qualified[g]) for g in retained))
    assert common
    identity = []
    for key in sorted(union):
        present = [g for g in retained if key in qualified[g]]
        identity.append(dict(zip(KEY, key)) | {
            'retained_files_present': len(present), 'common_11': key in common,
            'common_12': key in all_common,
            'all_retained_status_ok': key in common and all(qualified[g][key]['FPKM_status'] == 'OK' for g in retained),
            'present_gsms': ';'.join(present)})
    matrix = []
    for key in sorted(common):
        row = dict(zip(KEY, key))
        for gsm in sorted(files):
            source = qualified[gsm].get(key)
            row[gsm+'_FPKM'] = source['FPKM'] if source else ''
            row[gsm+'_status'] = source['FPKM_status'] if source else 'feature_not_qualified'
        matrix.append(row)
    with gzip.open(RAW/'GSE58998_FPKM_all_samples_merged.txt.gz', 'rt') as f:
        merged = table(f)
    merged_counts = Counter((r['gene_short_name'], r['locus']) for r in merged)
    crosswalk = []
    for row in merged:
        k = (row['gene_short_name'], row['gene_short_name'], row['locus'])
        if k in common and merged_counts[(k[1], k[2])] == 1:
            crosswalk.append({'gene_id': k[0], 'gene_short_name': k[1], 'locus': k[2],
                              'merged_tracking_id': row['tracking_id']})
    summary = {
        'scope': 'metadata and feature qualification; no expression contrast or population inference',
        'libraries': len(files), 'retained_libraries': len(retained), 'sra_runs': len(ena),
        'retained_groups': dict(Counter(m['genotype']+'_'+m['state'] for m in manifests if m['retained'])),
        'excluded_gsm': EXCLUDED,
        'unique_reference_locus_union_retained': len(union), 'common_reference_loci_11': len(common),
        'common_reference_loci_12': len(all_common),
        'common_reference_loci_11_all_status_ok': sum(r['all_retained_status_ok'] for r in identity),
        'merged_rows': len(merged), 'merged_unique_tracking': len({r['tracking_id'] for r in merged}),
        'merged_exact_symbol_locus_crosswalk': len(crosswalk),
        'merged_status_counts': {g: dict(Counter(r[g+'_status'] for r in merged)) for g in ('Het_hi','Het_lo','KO_hi','KO_lo')},
        'ena_total_fastq_bytes': sum(m['ena_fastq_bytes'] for m in manifests),
        'route': 'Descriptive FPKM on unique gene-labelled genomic spans shared across retained libraries; merged estimates separately labelled',
        'feature_limit': 'Exact gene label and mm10 span compatibility; transcript/exon equivalence and annotation release are not established. No symbol-only merging or transcript FPKM summation.',
        'unit_limit': 'Source calls preparations biological samples; individual mice/pools, cross-state pairing and batch remain unknown. GSM, BioSample and SRR are not independent animals.',
        'count_model': 'held: no count matrix, per-transcript abundance import semantics or independently verified biological units',
        'source_hashes': {name: sha(RAW/name) for name in ['GSE58998_RAW.tar','GSE58998_family.soft','GSE58998_FPKM_all_samples_merged.txt.gz','ena_runs.tsv']},
    }
    write_tsv(out/'sample_manifest.tsv', manifests)
    write_tsv(out/'file_qc.tsv', qc)
    write_tsv(out/'archive_member_hashes.tsv', file_hashes)
    write_tsv(out/'feature_identity.tsv', identity)
    write_tsv(out/'common_fpkm.tsv', matrix)
    write_tsv(out/'merged_crosswalk.tsv', crosswalk, ['gene_id','gene_short_name','locus','merged_tracking_id'])
    (out/'qualification.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in {'source_hashes','merged_status_counts'}}))


if __name__ == '__main__':
    main()
