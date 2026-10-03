"""A5-specific library metadata join; submitter aliases never stand for mice."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from qualify_biosample_metadata_v1 import geo_links


def qualify(soft: Path, xml: Path) -> tuple[dict, list[dict]]:
    source = geo_links(soft)
    if source['series'] != 'GSE303646':
        raise ValueError('This source-specific reader only supports GSE303646')
    root = ET.parse(xml).getroot()
    if root.tag != 'BioSampleSet':
        raise ValueError('Expected BioSampleSet')
    records, aliases = {}, set()
    for sample in root.findall('BioSample'):
        accession = sample.get('accession', '')
        if not re.fullmatch(r'SAMN\d+', accession) or accession in records:
            raise ValueError('Missing or duplicate accession')
        names = [x.text for x in sample.findall('./Ids/Id') if x.get('db_label') == 'Sample name']
        if len(names) != 1 or not re.fullmatch(r'MUC\d+', names[0] or '') or names[0] in aliases:
            raise ValueError('Missing, duplicate or invalid submitter library alias')
        aliases.add(names[0])
        geo = [x.text for x in sample.findall('./Ids/Id') if x.get('db') == 'GEO']
        if len(geo) != len(set(geo)) or any(not re.fullmatch(r'GSM\d+', x or '') for x in geo):
            raise ValueError('Invalid reverse GEO identifiers')
        attrs = [(x.get('harmonized_name') or x.get('attribute_name'), x.text or '')
                 for x in sample.findall('./Attributes/Attribute')]
        if any(not k for k, v in attrs):
            raise ValueError('Unnamed attribute')
        records[accession] = {'alias': names[0], 'geo': geo, 'attributes': attrs,
                             'sra': sorted(x.text for x in sample.findall('./Ids/Id') if x.get('db') == 'SRA' and x.text)}
    if set(records) != set(source['links'].values()):
        raise ValueError('Requested and returned accession membership differ')
    rows, keys, reverse_count = [], Counter(), 0
    for gsm, samn in sorted(source['links'].items()):
        record = records[samn]
        match = re.match(r'^(MUC\d+)(?:_|$)', source['titles'][gsm])
        if not match or match.group(1) != record['alias']:
            raise ValueError('GEO title and BioSample submitter alias disagree')
        if record['geo'] and gsm not in record['geo']:
            raise ValueError('Contradictory reverse GEO identifier')
        reverse_count += bool(record['geo'])
        keys.update({k for k, v in record['attributes']})
        safe = [(k, v) for k, v in record['attributes'] if k in {'breed', 'ecotype', 'age', 'sex', 'tissue'}]
        rows.append({'series': source['series'], 'geo_sample': gsm, 'biosample': samn,
                     'submitter_library_alias': record['alias'], 'geo_title': source['titles'][gsm],
                     'sra_sample': '; '.join(record['sra']), 'reverse_geo_link_present': bool(record['geo']),
                     'identity_fields': json.dumps(safe, ensure_ascii=True)})
    return {'schema_version': 1, 'series': source['series'], 'geo_records': len(rows),
            'biosample_records': len(records), 'exact_library_alias_matches': len(rows),
            'reverse_geo_links': reverse_count, 'attribute_key_record_counts': dict(sorted(keys.items())),
            'biological_unit_count': None, 'unit_status': 'not_determined_by_parser', 'expression_read': False,
            'interpretation': 'GEO-declared accessions and matching submitter library aliases establish a metadata join, not independent mice or a barcode/state map.'}, rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--soft', required=True); p.add_argument('--biosample', required=True); p.add_argument('--output', required=True)
    a = p.parse_args(); out = Path(a.output)
    targets = [out/'inventory.json', out/'sample_links.tsv']
    if any(x.exists() for x in targets): raise ValueError('Refusing to overwrite output')
    inventory, rows = qualify(Path(a.soft), Path(a.biosample))
    out.mkdir(parents=True, exist_ok=True)
    targets[0].write_bytes((json.dumps(inventory, indent=2)+'\n').encode())
    with targets[1].open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(json.dumps({'library_alias_matches': len(rows), 'biological_units': 'not inferred', 'expression_read': False}))


if __name__ == '__main__': main()
