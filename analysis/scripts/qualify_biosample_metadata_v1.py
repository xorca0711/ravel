"""Join public BioSample metadata to frozen GEO identities, never to animals.

Local files only. No expression data, protocol fields, contacts or network access.
An accession match is a record identity check, not biological independence.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from qualify_geo_metadata_v1 import read_family


def geo_links(path: Path) -> dict:
    series, samples = read_family(path)
    links = {}
    current = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('^'):
            current = line.split(' = ', 1)[1] if line.startswith('^SAMPLE = ') else None
        elif current and line.startswith('!Sample_relation = BioSample:'):
            found = re.findall(r'\bSAMN\d+\b', line)
            if len(found) != 1 or current in links:
                raise ValueError('Missing, ambiguous or repeated BioSample relation')
            links[current] = found[0]
    if set(links) != {s['accession'] for s in samples}:
        raise ValueError('Every GEO sample needs one explicit BioSample relation')
    return {'series': series['accession'], 'links': links,
            'titles': {s['accession']: s['fields']['Sample_title'][0] for s in samples}}


def biosamples(paths: list[Path]) -> dict:
    records = {}
    for path in paths:
        root = ET.parse(path).getroot()
        if root.tag != 'BioSampleSet':
            raise ValueError('Expected BioSampleSet, not an error response')
        for sample in root.findall('BioSample'):
            accession = sample.get('accession', '')
            if not re.fullmatch(r'SAMN\d+', accession) or accession in records:
                raise ValueError('Missing or duplicate BioSample accession')
            geo = [x.text for x in sample.findall('./Ids/Id') if x.get('db') == 'GEO']
            if not geo or len(geo) != len(set(geo)) or any(not re.fullmatch(r'GSM\d+', x or '') for x in geo):
                raise ValueError('Missing, invalid or duplicate GEO identity in BioSample')
            attrs = []
            for attr in sample.findall('./Attributes/Attribute'):
                key = attr.get('harmonized_name') or attr.get('attribute_name')
                if not key:
                    raise ValueError('Attribute without a name')
                attrs.append((key, attr.text or ''))
            records[accession] = {'geo': set(geo), 'title': sample.findtext('./Description/Title', ''),
                'sra': sorted(x.text for x in sample.findall('./Ids/Id') if x.get('db') == 'SRA' and x.text),
                'attributes': attrs}
    if not records:
        raise ValueError('Empty BioSample response')
    return records


def qualify(soft_paths: list[Path], xml_paths: list[Path]) -> tuple[dict, list[dict]]:
    sources = [geo_links(p) for p in soft_paths]
    if len({x['series'] for x in sources}) != len(sources):
        raise ValueError('Duplicate GEO series')
    requested = {samn for x in sources for samn in x['links'].values()}
    records = biosamples(xml_paths)
    if set(records) != requested:
        raise ValueError('Requested and returned BioSample membership differ')
    rows, summaries = [], []
    # Export a small metadata allowlist; retain all attribute NAMES for review.
    safe_fields = {'source_name', 'cell_type', 'strain', 'sex', 'age', 'genotype', 'batch',
                   'tissue', 'organism', 'mouse_id', 'animal_id', 'donor_id', 'pool_id',
                   'preparation_id', 'biological_replicate', 'sample_id', 'isolate'}
    for source in sources:
        counts, title_matches = Counter(), 0
        for gsm, samn in sorted(source['links'].items()):
            record = records[samn]
            if gsm not in record['geo']:
                raise ValueError('GEO/BioSample identity disagreement')
            counts.update({k for k, _ in record['attributes']})
            title_matches += source['titles'][gsm] == record['title']
            selected = [(k, v) for k, v in record['attributes'] if k.lower().replace(' ', '_') in safe_fields]
            rows.append({'series': source['series'], 'geo_sample': gsm, 'biosample': samn,
                         'sra_sample': '; '.join(record['sra']), 'title': record['title'],
                         'attribute_names': json.dumps(sorted({k for k, _ in record['attributes']})),
                         'identity_fields': json.dumps(selected, ensure_ascii=True)})
        summaries.append({'series': source['series'], 'geo_records': len(source['links']),
                          'biosample_records': len(set(source['links'].values())),
                          'exact_title_matches': title_matches,
                          'attribute_key_record_counts': dict(sorted(counts.items())),
                          'biological_unit_count': None, 'unit_status': 'not_determined_by_parser'})
    return {'schema_version': 1, 'studies': summaries, 'expression_read': False,
            'interpretation': 'Matched database identities do not establish animals, pools, preparations, fate or independent replication.'}, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--soft', nargs='+', required=True)
    parser.add_argument('--biosample', nargs='+', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    paths = [output / 'inventory.json', output / 'sample_links.tsv']
    if any(p.exists() for p in paths):
        raise ValueError('Refusing to overwrite metadata outputs')
    inventory, rows = qualify([Path(x) for x in args.soft], [Path(x) for x in args.biosample])
    output.mkdir(parents=True, exist_ok=True)
    paths[0].write_bytes((json.dumps(inventory, indent=2) + '\n').encode())
    with paths[1].open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({'matched_geo_records': len(rows), 'biological_units': 'not inferred', 'expression_read': False}))


if __name__ == '__main__':
    main()
