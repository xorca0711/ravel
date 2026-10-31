"""Public record cross-references only; no read/sequence download or expression."""
import argparse
from collections import defaultdict
import csv
import gzip
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

CACHE = Path('raw_data/Sx22/extensions_20261031')
UNIT_KEY = re.compile(r'animal|mouse.?id|donor|individual|pool|batch|prepar|isolation|replicate|aliquot|well|plate|lane|flow.?cell', re.I)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def only(values, label):
    require(len(values) == 1, 'Expected one ' + label)
    return values[0]


def soft_samples(text):
    records = []
    current = None
    for line in text.splitlines():
        if line.startswith('^SAMPLE = '):
            current = {'gsm': line.split(' = ', 1)[1], 'fields': defaultdict(list)}
            records.append(current)
        elif line.startswith('^'):
            current = None
        elif current is not None and line.startswith('!Sample_'):
            key, value = line.split(' = ', 1)
            current['fields'][key].append(value)
    output = []
    for record in records:
        f = record['fields']
        attributes = defaultdict(list)
        for value in f['!Sample_characteristics_ch1']:
            key, val = value.split(': ', 1)
            attributes[key].append(val)
        attributes['source_name'] = f['!Sample_source_name_ch1']
        relations = f['!Sample_relation']
        output.append(dict(gsm=record['gsm'], title=only(f['!Sample_title'], 'title'),
                           biosample=only([r.rsplit('/', 1)[1] for r in relations if r.startswith('BioSample: ')], 'BioSample'),
                           experiment=only([r.split('term=', 1)[1] for r in relations if r.startswith('SRA: ')], 'experiment'),
                           attributes=dict(attributes)))
    require(len({x['gsm'] for x in output}) == len(output), 'Duplicate GEO sample')
    return output


def attributes(nodes, key, value):
    result = defaultdict(list)
    for node in nodes:
        result[key(node)].append(value(node))
    return dict(result)


def external(node, namespace):
    return only([x.text for x in node.findall('./IDENTIFIERS/EXTERNAL_ID')
                 if x.get('namespace') == namespace], namespace + ' external link')


def join_records(geo, biosample_root, sra_root):
    bs_nodes = biosample_root.findall('./BioSample')
    packages = sra_root.findall('./EXPERIMENT_PACKAGE')
    bs = {x.get('accession'): x for x in bs_nodes}
    sra = {x.find('EXPERIMENT').get('accession'): x for x in packages}
    require(len(bs) == len(bs_nodes) and len(sra) == len(packages), 'Duplicate source accession')
    require(set(bs) == {x['biosample'] for x in geo}, 'BioSample coverage mismatch')
    require(set(sra) == {x['experiment'] for x in geo}, 'SRA experiment coverage mismatch')
    rows, detailed, field_rows = [], [], []
    for g in geo:
        b, p = bs[g['biosample']], sra[g['experiment']]
        sample, experiment = p.find('SAMPLE'), p.find('EXPERIMENT')
        require(b.findtext('./Description/Title') == g['title'], 'BioSample title mismatch')
        require(only([x.text for x in b.findall('./Ids/Id') if x.get('db') == 'GEO'], 'GEO reverse link') == g['gsm'], 'GEO reverse mismatch')
        require(only([x.text for x in b.findall('./Ids/Id') if x.get('db') == 'SRA'], 'SRA sample link') == sample.get('accession'), 'SRA sample mismatch')
        require(external(sample, 'BioSample') == g['biosample'], 'BioSample reverse mismatch')
        require(external(sample, 'GEO') == g['gsm'], 'SRA GEO reverse mismatch')
        require(sample.findtext('TITLE') == g['title'], 'SRA title mismatch')
        require(experiment.get('alias') == g['gsm'], 'Experiment alias mismatch')
        descriptor = experiment.find('./DESIGN/SAMPLE_DESCRIPTOR')
        require(descriptor.get('accession') == sample.get('accession'), 'Experiment sample descriptor mismatch')
        require(external(descriptor, 'GEO') == g['gsm'], 'Descriptor GEO mismatch')
        ba = attributes(b.findall('./Attributes/Attribute'), lambda x: x.get('attribute_name'), lambda x: x.text or '')
        sa = attributes(sample.findall('./SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE'), lambda x: x.findtext('TAG'), lambda x: x.findtext('VALUE') or '')
        for key in ['source_name', 'tissue', 'strain', 'treatment']:
            require(g['attributes'].get(key) == ba.get(key) == sa.get(key), 'Source attribute mismatch: ' + key)
        scopes = {'GEO': g['attributes'], 'BioSample': ba, 'SRA_sample': sa}
        run_records = []
        for run in p.findall('./RUN_SET/RUN'):
            require(run.find('EXPERIMENT_REF').get('accession') == g['experiment'], 'Run experiment mismatch')
            members = []
            for member in run.findall('./Pool/Member'):
                require(member.get('accession') == sample.get('accession'), 'Pool member sample mismatch')
                require(external(member, 'BioSample') == g['biosample'] and external(member, 'GEO') == g['gsm'], 'Pool member cross-reference mismatch')
                members.append({k: member.get(k, '') for k in ['accession', 'sample_name', 'sample_title', 'member_name']})
            ra = attributes(run.findall('./RUN_ATTRIBUTES/RUN_ATTRIBUTE'), lambda x: x.findtext('TAG'), lambda x: x.findtext('VALUE') or '')
            scopes['SRA_run_' + run.get('accession')] = ra
            run_records.append(dict(accession=run.get('accession'), alias=run.get('alias', ''),
                                    public=run.get('is_public', ''), sample_members=members,
                                    attributes=ra))
        require(run_records, 'No run record returned')
        layout = experiment.find('./DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT')
        layout_name = only([child.tag for child in layout], 'library layout')
        candidate_keys = []
        for scope, values in scopes.items():
            for key, entries in sorted(values.items()):
                field_rows.append(dict(gsm=g['gsm'], record_scope=scope, key=key,
                                       values=json.dumps(entries, ensure_ascii=False)))
                if UNIT_KEY.search(key):
                    candidate_keys.append(dict(scope=scope, key=key, values=entries))
        rows.append(dict(gsm=g['gsm'], column=g['title'], treatment=only(ba['treatment'], 'treatment'),
                         biosample=g['biosample'], sra_sample=sample.get('accession'),
                         experiment=g['experiment'], run_accessions=';'.join(x['accession'] for x in run_records),
                         run_count=len(run_records), library_layout=layout_name,
                         source_unit_attribute_candidates=len(candidate_keys),
                         animal_pairing='not established', biological_independence='unknown'))
        detailed.append(dict(gsm=g['gsm'], source_attributes=scopes, unit_attribute_candidates=candidate_keys,
                             runs=run_records, instrument=experiment.findtext('./PLATFORM/ILLUMINA/INSTRUMENT_MODEL'),
                             submission={k: p.find('SUBMISSION').get(k, '') for k in ['accession', 'alias', 'center_name', 'lab_name']},
                             library_layout=layout_name))
    runs = [r['accession'] for x in detailed for r in x['runs']]
    require(len(runs) == len(set(runs)), 'Run accession reused across samples')
    return rows, detailed, field_rows


def write_csv(path, rows):
    with path.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def main(output):
    with gzip.open('raw_data/Sx22/GSE160217_family.soft.gz', 'rt') as stream:
        geo = soft_samples(stream.read())
    require({x['gsm'] for x in geo} == {f'GSM{i}' for i in range(4869228, 4869234)}, 'Unexpected GEO inventory')
    rows, detailed, fields = join_records(geo, ET.parse(CACHE / 'biosamples.xml').getroot(),
                                          ET.parse(CACHE / 'sra_packages.xml').getroot())
    summary = dict(sample_records=len(rows), run_records=sum(r['run_count'] for r in rows),
                   exact_cross_references='all GEO, BioSample, SRA sample/experiment/run links agree',
                   source_unit_attribute_candidates=sum(r['source_unit_attribute_candidates'] for r in rows),
                   independence='unknown beyond source report', animal_pairing='not established',
                   caveat='PAIRED is sequencing layout; Pool/Member contains database sample membership, not animal pooling evidence',
                   protocol_review='Human review of named records is required beyond attribute-name screening',
                   sequence_downloads=False)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'sample_provenance.csv', rows)
    write_csv(output / 'field_inventory.csv', fields)
    write_json(output / 'record_metadata.json', detailed)
    access = json.loads((CACHE / 'acquisition_v1.json').read_text())
    write_json(output / 'source_access.json', [x for x in access if x['path'].endswith(('biosamples.xml', 'sra_packages.xml'))])
    write_json(output / 'summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args().output)
