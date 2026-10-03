"""Extract bounded GEO identity metadata; never infer biological replication.

Reads local SOFT family inputs only. It does not access expression tables, network
resources or protocol fields. Statistical and biological eligibility are reviewed
separately from this inventory.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re


def read_family(path: Path) -> tuple[dict, list[dict]]:
    series = None
    samples = []
    current = None
    kind = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('^'):
            match = re.fullmatch(r'\^(\w+) = (.+)', line)
            if not match:
                raise ValueError('Malformed SOFT entity header')
            kind, accession = match.groups()
            current = {'accession': accession, 'fields': {}}
            if kind == 'SERIES':
                if series is not None:
                    raise ValueError('Expected exactly one SERIES entity')
                series = current
            elif kind == 'SAMPLE':
                samples.append(current)
        elif line.startswith('!') and ' = ' in line and current is not None:
            key, value = line[1:].split(' = ', 1)
            # Do not retain contacts, protocol text, expression tables or raw reads.
            allowed = {'Series_title', 'Series_last_update_date', 'Series_sample_id',
                       'Series_supplementary_file', 'Series_relation', 'Series_type',
                       'Sample_title', 'Sample_organism_ch1', 'Sample_molecule_ch1',
                       'Sample_library_strategy', 'Sample_series_id',
                       'Sample_characteristics_ch1'}
            if key in allowed:
                current['fields'].setdefault(key, []).append(value)
    if series is None or not re.fullmatch(r'GSE\d+', series['accession']):
        raise ValueError('Missing valid GEO series')
    ids = [s['accession'] for s in samples]
    declared = series['fields'].get('Series_sample_id', [])
    if not ids or len(ids) != len(set(ids)) or len(declared) != len(set(declared)):
        raise ValueError('Missing or duplicate sample IDs')
    if set(ids) != set(declared):
        raise ValueError('Series/sample membership mismatch')
    if any(not re.fullmatch(r'GSM\d+', x) for x in ids):
        raise ValueError('Invalid GEO sample identifier')
    for s in samples:
        fields = s['fields']
        if len(fields.get('Sample_title', [])) != 1:
            raise ValueError('Each sample requires exactly one title')
        if series['accession'] not in fields.get('Sample_series_id', []):
            raise ValueError('Sample omits enclosing series membership')
    return series, samples


def summarize(series: dict, samples: list[dict]) -> dict:
    keys = Counter()
    memberships = Counter()
    assays = Counter()
    organisms = Counter()
    for s in samples:
        f = s['fields']
        keys.update({v.split(':', 1)[0].strip().lower()
                     for v in f.get('Sample_characteristics_ch1', []) if ':' in v})
        memberships.update(set(f.get('Sample_series_id', [])))
        assays.update(set(f.get('Sample_library_strategy', [])))
        organisms.update(set(f.get('Sample_organism_ch1', [])))
    return {'series': series['accession'], 'series_fields': series['fields'],
            'sample_record_count': len(samples), 'membership_record_counts': dict(sorted(memberships.items())),
            'library_strategy_counts': dict(sorted(assays.items())),
            'organism_record_counts': dict(sorted(organisms.items())),
            'characteristic_key_record_counts': dict(sorted(keys.items())),
            'biological_unit_count': None,
            'biological_unit_status': 'not_determined_by_parser',
            'expression_values_read': False,
            'interpretation': 'Counts refer to deposited sample records, not animals, donors, preparations or independent wells.'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', nargs='+', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    paths = [output/'inventory.json', output/'samples.tsv']
    if any(p.exists() for p in paths):
        raise ValueError('Refusing to overwrite metadata outputs')
    inventories = []
    rows = []
    seen = set()
    for name in args.input:
        path = Path(name)
        series, samples = read_family(path)
        if series['accession'] in seen:
            raise ValueError('Duplicate series input')
        seen.add(series['accession'])
        summary = summarize(series, samples)
        summary['input_path'] = path.as_posix()
        summary['input_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        inventories.append(summary)
        for sample in samples:
            f = sample['fields']
            # Export only identity fields. Treatment protocols remain in the original input.
            identity = [x for x in f.get('Sample_characteristics_ch1', [])
                        if x.split(':', 1)[0].strip().lower() != 'treatment']
            rows.append({'series': series['accession'], 'sample': sample['accession'],
                         'title': f['Sample_title'][0],
                         'organism': '; '.join(f.get('Sample_organism_ch1', [])),
                         'library_strategy': '; '.join(f.get('Sample_library_strategy', [])),
                         'series_memberships': '; '.join(f.get('Sample_series_id', [])),
                         'identity_fields': json.dumps(identity, ensure_ascii=True)})
    paths[0].write_bytes((json.dumps({'schema_version': 1, 'studies': inventories}, indent=2)+'\n').encode())
    with paths[1].open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({'series_count': len(inventories), 'sample_records': len(rows),
                      'biological_units': 'not inferred', 'expression_read': False}))


if __name__ == '__main__':
    main()
