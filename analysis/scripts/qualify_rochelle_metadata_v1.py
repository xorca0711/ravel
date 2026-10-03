"""Read only source labels; no expression scores or inferred animal identities."""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

EXPECTED = ('GSE306194', 'GSE306714')

def parse_soft(text: str, expected_series: str) -> list[dict]:
    series, rows, sample, seen = None, [], None, set()
    for line in text.splitlines():
        if line.startswith('^'):
            if line.startswith('^SERIES = '):
                if series is not None:
                    raise ValueError('Multiple series records')
                series = line.split(' = ', 1)[1]
            sample = None
            if line.startswith('^SAMPLE = '):
                gsm = line.split(' = ', 1)[1]
                if gsm in seen:
                    raise ValueError('Duplicate sample: ' + gsm)
                seen.add(gsm)
                sample = {'study': expected_series, 'gsm': gsm, 'title': '', 'source_name': [], 'characteristics': {}, 'supplementary_files': []}
                rows.append(sample)
        elif sample is not None and ' = ' in line:
            key, value = line.split(' = ', 1)
            if key == '!Sample_title':
                if sample['title']:
                    raise ValueError('Repeated sample title')
                sample['title'] = value
            elif key == '!Sample_source_name_ch1':
                sample['source_name'].append(value)
            elif key == '!Sample_characteristics_ch1':
                field, sep, item = value.partition(': ')
                if not sep:
                    field, item = 'unstructured', value
                sample['characteristics'].setdefault(field, []).append(item)
            elif key.startswith('!Sample_supplementary_file'):
                sample['supplementary_files'].append(value)
    if series != expected_series or not rows or any(not row['title'] for row in rows):
        raise ValueError('Wrong series, empty source or missing title')
    return rows

def summarize(rows: list[dict]) -> dict:
    labels = sorted({label for row in rows for label in row['characteristics'].get('individual', [])})
    return {'sample_records': len(rows), 'explicit_individual_labels': labels,
            'sample_records_without_explicit_individual': sum(not row['characteristics'].get('individual') for row in rows),
            'interpretation': 'Sample records and reported individual labels only; not an inferred independent-preparation count. Embedded title codes are retained verbatim, not mapped across sources.'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sources', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if any((args.output / name).exists() for name in ('samples.json', 'samples.csv', 'summary.json')):
        raise FileExistsError('Refusing output overwrite')
    rows, summary = [], {}
    for acc in EXPECTED:
        src = args.sources / (acc + '_family.soft.gz')
        data = src.read_bytes()
        parsed = parse_soft(gzip.decompress(data).decode('utf-8'), acc)
        rows.extend(parsed)
        summary[acc] = {**summarize(parsed), 'input_sha256': hashlib.sha256(data).hexdigest()}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'samples.json').write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'samples.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['study', 'gsm', 'title', 'individual_labels', 'group_labels', 'characteristics_json'])
        writer.writeheader()
        for row in rows:
            writer.writerow({'study': row['study'], 'gsm': row['gsm'], 'title': row['title'],
                'individual_labels': '|'.join(row['characteristics'].get('individual', [])),
                'group_labels': '|'.join(row['characteristics'].get('group', [])),
                'characteristics_json': json.dumps(row['characteristics'], sort_keys=True)})
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))

if __name__ == '__main__':
    main()
