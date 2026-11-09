"""Frozen metadata recovery; no expression analysis or treatment estimates."""
import argparse
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import openpyxl

RAW = Path('raw_data/navarro_2026/source_v1')


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    wb = openpyxl.load_workbook(RAW / 'S1.xlsx', read_only=True, data_only=True)
    ws = wb['Mouse_Metadata']
    headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    metadata = []
    for row in ws.iter_rows(min_row=2):
        if row[0].value:
            metadata.append({'source_row': row[0].row, **dict(zip(headers, [c.value for c in row]))})
    dump(out / 's1_mouse_metadata.json', metadata)
    inventory = {}
    for name in ['S1.xlsx', 'S4.xlsx']:
        with zipfile.ZipFile(RAW / name) as z:
            assert z.testzip() is None
        book = openpyxl.load_workbook(RAW / name, read_only=True, data_only=True)
        inventory[name] = [{'sheet': s.title, 'rows_in_declared_range': s.max_row,
                            'columns_in_declared_range': s.max_column} for s in book]
    dump(out / 'workbook_inventory.json', inventory)

    biosamples = {}
    for e in ET.parse(RAW / 'biosample.xml').getroot().iter('BioSample'):
        biosamples[e.attrib['accession']] = {a.attrib['attribute_name']: a.text for a in e.iter('Attribute')}
    sra = {}
    for e in ET.parse(RAW / 'sra.xml').getroot().iter('EXPERIMENT'):
        sra[e.attrib['accession']] = {'instrument': e.findtext('./PLATFORM/ILLUMINA/INSTRUMENT_MODEL'),
                                    'library': e.findtext('./DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME')}
    with (RAW / 'ena.tsv').open(encoding='utf-8') as f:
        runs = list(csv.DictReader(f, delimiter='\t'))
    assert len({r['run_accession'] for r in runs}) == len(runs) == 20
    main_mapping = {
        'SVZ_IL10_young_control_GEX': (11, 'vehicle', None),
        'SVZ_IL10_old_control_GEX': (12, 'vehicle', None),
        'SVZ_IL10_WT_low_GEX': (13, 'WT', 0.02),
        'SVZ_IL10_Mut_low_GEX': (14, 'D25K', 0.02),
        'SVZ_IL10_WT_high_GEX': (15, 'WT', 0.1),
        'SVZ_IL10_Mut_high_GEX': (16, 'D25K', 0.1),
    }
    rows_by_id = {m['source_row']: m for m in metadata}
    crosswalk = []
    for run in runs:
        attrs = biosamples[run['sample_accession']]
        rec = {k: run[k] for k in ['run_accession', 'sample_accession', 'experiment_accession', 'library_name', 'library_strategy']}
        rec.update(collection_date=attrs.get('collection_date'), deposited_age=attrs.get('age'),
                   tissue=attrs.get('tissue'), sex=attrs.get('sex'),
                   source_locator='ENA run table; BioSample ' + run['sample_accession'],
                   code_alias='unresolved', true_mouse_key='not recovered',
                   biological_replication='pool is not a mouse replicate')
        if run['library_name'] in main_mapping:
            row, treatment, dose = main_mapping[run['library_name']]
            m = rows_by_id[row]
            rec.update(treatment=treatment, dose_mg_per_mL=dose, s1_row=row,
                       mice_per_library=m['Number of mice pooled'], age=m['Age'],
                       sex=m['Sex'], strain=m['Strain'], multiplexing=m['Multiplexing'],
                       chemistry=m['10x kit'], lane=m['10x lane'], vehicle='ACSF',
                       treatment_days=7, libraries_per_condition=1,
                       dose_mapping_basis='S1 A13:A16 numerical doses; ENA low/high ordering; no code-alias identity established',
                       platform=sra.get(run['experiment_accession'], {}).get('instrument', 'not inspected'),
                       source_locator=f'ENA {run["run_accession"]}; S1 Mouse_Metadata row {row}; paper STAR Methods')
        crosswalk.append(rec)
    assert sum(r['sample_accession'] == 'SAMN53298933' for r in crosswalk) == 6
    dump(out / 'source_crosswalk.json', crosswalk)
    with zipfile.ZipFile(RAW / 'code_v1.zip') as z:
        audit = []
        for suffix in ['IL10/1.Seurat.R', 'IL10/2.Microglia.R', 'IL10/3.Tcells.R']:
            data = z.read(next(n for n in z.namelist() if n.endswith(suffix)))
            lines = data.decode().splitlines()
            audit.append({'file': suffix, 'sha256': hashlib.sha256(data).hexdigest(),
                          'identity_or_exclusion_locators': [i for i, line in enumerate(lines, 1)
                            if any(t in line for t in ['Read10X(', 'readRDS(', 'saveRDS(svz', 'Remove', 'nCount_RNA >', 'WT50', 'Mut50'])]})
    dump(out / 'code_audit.json', audit)
    conflicts = [
        {'id': 'cognition_direct_tests', 'locators': ['S4 Figure 7 I14', 'S4 Figure 7 I19'],
         'finding': 'Direct rank-sum P values are reported separately from within-group chance tests; reproduce both, no WT arm.'},
        {'id': 'nesting_dose_pooling', 'locators': ['S4 Figure 7 D3', 'S4 Figure 7 D5', 'S4 Figure 7 I6'],
         'finding': 'Combined nesting pools 0.1 and 0.02 mg/mL; WT occurs only in 0.1 mg/mL cohort. Preserve aggregate reproduction and separate dose-specific description.'},
        {'id': 'neurogenesis_labels', 'locators': ['S4 Figure 6 A57', 'S4 Figure 6 A76', 'S4 Figure 6 E10:E16', 'paper Fig.6G/I/J and Methods P92'],
         'finding': 'Data-block titles say SVZ for both EdU outcomes; experiment descriptors and paper assign OB. Table panel letters differ from final paper; units also conflict. Analyze stored scale only; do not call values original counts/mm2.'},
        {'id': 'source_count_conflicts', 'locators': ['S1 Mouse_Metadata E8:E9', 'S4 Figure 2 D4', 'paper STAR Methods RIPR experiment 2', 'S1 Mouse_Metadata F18:F19', 'S4 Figure 3 D5'],
         'finding': 'RIPR second-cohort pool counts differ (S1 4, S4 5, paper 3); separate-WT control age differs (S1 27 months, S4 25 months). Optional cohorts remain unqualified for pooled comparisons.'},
        {'id': 'absent_individual_keys', 'locators': ['S1 Mouse_Metadata B11:B16/H11:H16', 'S4 Figure 6 and Figure 7 raw blocks'],
         'finding': 'Sample numbers/lane/index identify libraries, not demultiplexed mice. S4 gives group columns and some experiment blocks, no demonstrated stable mouse keys across assays.'},
        {'id': 'aliases', 'locators': ['IL10/1.Seurat.R:23-41,232,251-252', 'S1 Mouse_Metadata rows 11-16'],
         'finding': 'S1 samples/lanes are not code C1-C8 order. Six deposited RNA libraries versus eight code aliases remains unresolved. Saved object precedes later plot-only WT50/Mut50 filtering.'},
    ]
    dump(out / 'qualification.json', {'candidate': 'Nn26-P01', 'animal_stage': 'eligible for exposed panel-wise reproduction after frozen contract',
        'RNA_stage': 'object qualification pending runtime/resources; aliases unresolved',
        'independence': 'no new mouse independence established', 'conflicts': conflicts,
        'scientific_acceptance': 'not_assessed'})
    # Independent parser: raw OOXML values versus openpyxl for every S1 metadata cell.
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(RAW / 'S1.xlsx') as z:
        ss = ET.fromstring(z.read('xl/sharedStrings.xml'))
        strings = [''.join(n.itertext()) for n in ss]
        xml = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        compared = 0
        for cell in xml.findall('.//m:c', ns):
            value = cell.find('m:v', ns)
            if value is None: continue
            expected = strings[int(value.text)] if cell.get('t') == 's' else float(value.text)
            observed = ws[cell.get('r')].value
            assert expected == observed, (cell.get('r'), expected, observed)
            compared += 1
    dump(out / 'validation.json', {'raw_xml_cell_checks': compared, 'zip_integrity': 'passed',
        'unique_ENA_runs': len(runs), 'main_RNA_libraries': 6,
        'python': sys.version, 'openpyxl': openpyxl.__version__, 'status': 'passed'})


if __name__ == '__main__':
    main()
