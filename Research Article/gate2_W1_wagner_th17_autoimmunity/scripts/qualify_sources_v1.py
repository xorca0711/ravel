"""Qualify pinned Wagner source identities; no expression values or inference."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'analysis/scripts'))
from qualify_geo_metadata_v1 import read_family, summarize

SERIES = ('GSE75109', 'GSE75111', 'GSE162300', 'GSE162382', 'GSE165088')
PIN = '31141a8d82872fb09803a0bf66ffc793d1410be8'


def extra_fields(path):
    records = {}
    current = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('^'):
            current = None
            if line.startswith('^SAMPLE = '):
                current = line.split(' = ', 1)[1]
                if current in records:
                    raise ValueError('Duplicate SAMPLE accession')
                records[current] = {}
        elif current and line.startswith(('!Sample_relation = ', '!Sample_source_name_ch1 = ')):
            key, value = line[1:].split(' = ', 1)
            records[current].setdefault(key, []).append(value)
    return records


def unique(values, label):
    if len(values) != len(set(values)) or any(not x for x in values):
        raise ValueError(f'Duplicate or empty {label}')


def join_cells(cells, samples):
    unique([c['cell_id'] for c in cells], 'author cell ID')
    unique([c['MD_SRX'] for c in cells], 'author SRX')
    index = {}
    for sample in samples:
        if sample['series'] not in SERIES[:2]:
            continue
        ids = re.findall(r'\bSRX\d+\b', sample['sra_relation'])
        if len(ids) != 1 or ids[0] in index:
            raise ValueError('Missing, ambiguous or duplicate GEO SRX')
        index[ids[0]] = sample
    if set(index) != {c['MD_SRX'] for c in cells}:
        raise ValueError('Author/GEO SRX membership mismatch')
    joined = []
    for cell in cells:
        sample = index[cell['MD_SRX']]
        expected = {'GSE75109': 'Th17p', 'GSE75111': 'Th17n'}[sample['series']]
        if cell['cell_type'] != expected:
            raise ValueError('Author/GEO condition mismatch')
        joined.append(dict(cell_id=cell['cell_id'], srx=cell['MD_SRX'],
                           condition=expected, series=sample['series'], gsm=sample['gsm'],
                           source_label=sample['source_label'], animal_id=sample['animal_id'],
                           biological_unit_status='unresolved'))
    return joined


def write_tsv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def qualify(source, output):
    for name in ['qualification.json', 'source_manifest.json', 'samples.tsv', 'cell_join.tsv']:
        if (output / name).exists():
            raise FileExistsError(name)
    files = []
    tree = json.loads((source / 'author_tree.json').read_text())
    if tree['sha'] != PIN or tree.get('truncated'):
        raise ValueError('Author tree pin mismatch or truncated tree')
    blobs = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    for manifest in ['acquisition_v1.json', 'author_acquisition_v1.json']:
        acquisition = json.loads((source / manifest).read_text())
        if acquisition['author_pin'] != PIN:
            raise ValueError('Acquisition pin mismatch')
        for record in acquisition['files']:
            data = (source / record['path']).read_bytes()
            if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('Acquisition hash mismatch')
            if 'upstream_path' in record:
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if blobs[record['upstream_path']]['sha'] != blob:
                    raise ValueError('Author Git blob mismatch')
            files.append(record)
    samples, inventories = [], []
    for accession in SERIES:
        path = source / (accession + '_family.soft')
        series, entities = read_family(path)
        if series['accession'] != accession:
            raise ValueError('Unexpected GEO accession')
        extras = extra_fields(path)
        inventories.append(summarize(series, entities))
        for entity in entities:
            f = entity['fields']
            chars = {}
            for value in f.get('Sample_characteristics_ch1', []):
                key, sep, val = value.partition(':')
                if sep:
                    key = key.strip().lower()
                    if key in chars and chars[key] != val.strip():
                        raise ValueError('Conflicting sample characteristic')
                    chars[key] = val.strip()
            e = extras[entity['accession']]
            samples.append(dict(series=accession, gsm=entity['accession'], title=f['Sample_title'][0],
                                animal_id=chars.get('animal_id', ''),
                                cell_type=chars.get('cell type', chars.get('differentiation', '')),
                                treatment=chars.get('treatment', ''), genotype=chars.get('genotype', ''),
                                run_id=chars.get('run_id', ''),
                                source_label='; '.join(e.get('Sample_source_name_ch1', [])),
                                sra_relation='; '.join(v for v in e.get('Sample_relation', []) if v.startswith('SRA:'))))
    with (source / 'cell_metadata.csv').open(newline='') as handle:
        cells = list(csv.DictReader(handle))
    joined = join_cells(cells, samples)
    matrix_headers = {}
    for name in ['reactions.tsv', 'linear_gene_expression_matrix.tsv']:
        with (source / name).open(newline='') as handle:
            ids = next(csv.reader(handle, delimiter='\t'))[1:]
        unique(ids, name + ' columns')
        if set(ids) != {x['cell_id'] for x in cells}:
            raise ValueError('Matrix/metadata membership mismatch: ' + name)
        matrix_headers[name] = {'cell_count': len(ids), 'exact_order_match': ids == [x['cell_id'] for x in cells]}
    qualification = {
        'author_pin': PIN, 'sample_record_count': len(samples),
        'cell_join_count': len(joined), 'condition_cell_counts': dict(Counter(c['condition'] for c in joined)),
        'matrix_headers': matrix_headers, 'series': inventories,
        'explicit_animal_labels_within_series': {
            a: sorted({x['animal_id'] for x in samples if x['series'] == a and x['animal_id']}) for a in SERIES},
        'expression_values_read': False,
        'r1_source_score_descriptive_eligibility': 'eligible_for_separate_frozen_contract',
        'r1_population_inference': 'hold: sorted-cell animal/preparation identity and allocation unresolved',
        'r2_full_compass': 'hold: historical model/runtime/normalization equivalence and solver not qualified',
        'r3_r4': 'design labels recovered; assay matrix joins, technical-run handling and design rank require separate qualification',
        'cross_assay_pairing': 'not established by repeated WT labels',
        'interpretation_limit': 'SRX links author-labelled SRR cells to GSM. Independent SRA run-to-experiment verification is not performed. Library identity is not biological replication.'}
    output.mkdir(parents=True, exist_ok=True)
    (output / 'qualification.json').write_text(json.dumps(qualification, indent=2) + '\n')
    (output / 'source_manifest.json').write_text(json.dumps({'files': files}, indent=2) + '\n')
    write_tsv(output / 'samples.tsv', samples)
    write_tsv(output / 'cell_join.tsv', joined)
    print(json.dumps({k: qualification[k] for k in ['sample_record_count', 'cell_join_count', 'condition_cell_counts']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    qualify(args.source, args.output)
