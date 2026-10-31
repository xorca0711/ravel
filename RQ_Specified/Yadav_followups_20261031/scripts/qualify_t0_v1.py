"""Frozen T0 source/metadata qualification. Never computes biological effects."""
import argparse
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'raw_data/Yadav_followups_T0_20261031'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def dump(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def table(path, rows):
    if not rows:
        raise ValueError('Empty metadata table: ' + str(path))
    with path.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def source_access(job):
    prefixes = ('hamanaka', 'lee', 'GSE273882') if job == 'br' else ('atg5',)
    attempts = []
    for log in sorted(CACHE.glob('retrievals_v*.json')):
        for row in json.loads(log.read_text(encoding='utf-8')):
            if not row['file'].startswith(prefixes):
                continue
            item = dict(row, acquisition_receipt=log.relative_to(ROOT).as_posix())
            path = CACHE / row['file']
            item['content_verified'] = False
            if path.exists():
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != row.get('sha256'):
                    raise ValueError('Acquisition hash mismatch: ' + row['file'])
                valid = True
                if path.suffix == '.pdf':
                    valid = data.startswith(b'%PDF')
                elif path.suffix in ('.zip', '.xlsx'):
                    valid = zipfile.is_zipfile(path)
                elif path.suffix == '.xml':
                    ET.fromstring(data)
                elif path.suffix == '.json':
                    json.loads(data)
                elif path.suffix == '.jpg':
                    valid = data.startswith(b'\xff\xd8')
                item['content_verified'] = valid
                if not valid:
                    item['interpretation'] = 'Access response is not the requested content; never use as PDF evidence.'
            attempts.append(item)
    members = []
    if job == 'br':
        for archive in ['hamanaka_supplementary.zip', 'lee_supplementary.zip']:
            with zipfile.ZipFile(CACHE / archive) as z:
                for info in z.infolist():
                    members.append({'archive': archive, 'member': info.filename,
                                    'bytes': info.file_size,
                                    'sha256': hashlib.sha256(z.read(info)).hexdigest()})
    return {'requests': attempts, 'archive_members': members,
            'limit': 'Acquired primary sources and metadata only; access is not scientific validation.'}


def geo_map():
    text = (CACHE / 'GSE273882_sample_metadata.txt').read_text(encoding='utf-8')
    if '!sample_table_begin' in text.lower() or '^PLATFORM' in text:
        raise ValueError('Metadata-only boundary failed')
    rows = []
    for block in text.split('^SAMPLE = ')[1:]:
        lines = block.splitlines()
        fields = {}
        for line in lines[1:]:
            if ' = ' in line:
                key, value = line.split(' = ', 1)
                fields.setdefault(key, []).append(value)
        if fields.get('!Sample_data_row_count') != ['0']:
            raise ValueError('Nonempty GEO data rows')
        title = fields['!Sample_title'][0]
        traits = fields.get('!Sample_characteristics_ch1', [])
        rows.append({'gsm': lines[0], 'title': title, 'attributes': '; '.join(traits),
                     'growth_protocol': ' '.join(fields.get('!Sample_growth_protocol_ch1', [])),
                     'treatment_protocol': ' '.join(fields.get('!Sample_treatment_protocol_ch1', [])),
                     'relations': '; '.join(fields.get('!Sample_relation', [])),
                     'listed_file': '; '.join(fields.get('!Sample_supplementary_file_1', [])),
                     'title_prefix': title.rsplit('_', 2)[0],
                     'biological_independence': 'unknown',
                     'cross_assay_pairing': 'unknown; title suffix or clone token does not identify a shared preparation'})
    return rows


def workbook_metadata():
    result, samples = [], []
    with zipfile.ZipFile(CACHE / 'hamanaka_metabolomics_v1.xlsx') as z:
        strings = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        relations = {e.get('Id'): e.get('Target') for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        book = ET.fromstring(z.read('xl/workbook.xml'))
        for sheet in book.findall('s:sheets/s:sheet', NS):
            rid = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = relations[rid]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            tree = ET.fromstring(z.read(target))
            cells = {}
            for c in tree.findall('.//s:c', NS):
                value = c.find('s:v', NS)
                if c.get('t') == 's' and value is not None:
                    cells[c.get('r')] = strings[int(value.text)]
                elif c.get('t') == 'inlineStr':
                    cells[c.get('r')] = ''.join(c.find('s:is', NS).itertext())
            result.append({'sheet': sheet.get('name'), 'dimension': tree.find('s:dimension', NS).get('ref'),
                           'text_cells': cells,
                           'boundary': 'Only text labels retained; no numeric measurement or formula evaluated.'})
            for coord, value in cells.items():
                if re.fullmatch(r'A\d+', coord) and re.search(r'_(?:0[1-4])$', value):
                    row = re.search(r'\d+', coord).group()
                    samples.append({'sheet': sheet.get('name'), 'source_cell': coord, 'sample_label': value,
                                    'column_B_text': cells.get('B' + row, ''),
                                    'column_C_text': cells.get('C' + row, ''),
                                    'unit_status': 'unknown; repeated metabolite rows and suffixes are not independent donors'})
    return result, samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', choices=['br', 'e'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads((HERE / f'config/t0_{args.job}_spec_v1.json').read_text(encoding='utf-8'))
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    dump(out / 'source_access.json', source_access(args.job))
    dump(out / 't1_disposition.json', spec['decisions'])
    if args.job == 'br':
        table(out / 'assay_unit_map.csv', spec['assays'])
        table(out / 'tracer_map.csv', spec['tracers'])
        table(out / 'source_issues.csv', spec['issues'])
        table(out / 'geo_sample_map.csv', geo_map())
        layout, samples = workbook_metadata()
        dump(out / 'workbook_layout.json', layout)
        table(out / 'workbook_sample_map.csv', samples)
        lines = (CACHE / 'GSE273882_filelist.txt').read_text(encoding='utf-8').splitlines()
        files = []
        for line in lines:
            if line.startswith(('Archive\t', 'File\t')):
                kind, name, time, size, filetype = line.split('\t')
                files.append({'source': 'GSE273882', 'kind': kind, 'name': name,
                              'source_timestamp': time, 'bytes': int(size), 'type': filetype,
                              'acquired': 'no; listing only'})
        article = json.loads((CACHE / 'hamanaka_figshare_listing.json').read_text(encoding='utf-8'))
        for f in article['files']:
            files.append({'source': article['doi'], 'kind': 'processed metabolomics', 'name': f['name'],
                          'source_timestamp': article['published_date'], 'bytes': f['size'],
                          'type': f['mimetype'], 'acquired': 'yes; text labels inventoried, no effects computed'})
        table(out / 'file_inventory.csv', files)
    else:
        table(out / 'endpoint_unit_map.csv', spec['endpoints'])
    print(json.dumps({'job': args.job, 'owner': spec['owner'], 'work_type': 'metadata',
                      'outputs': sorted(p.name for p in out.iterdir() if p.is_file())}))


if __name__ == '__main__':
    main()
