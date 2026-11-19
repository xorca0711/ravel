"""Artificial cases only: baseline offsets, changing coverage, zero/NA and group meaning."""
import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

from s6a_reconstruct_v1 import reconstruct, read_workbooks, write_outputs
from s6a_verify_v1 import verify


def fixture(folder, missing_baseline=False):
    wb = Workbook()
    wb.remove(wb.active)
    m = dict(panels=[], endpoints=[], pdf_caption_guards=[])
    raw = {
        'EDF6f': [
            [[10, 12], [12, 14], [6, 8], [7, 9]],
            [[7, 9], [8, 10], [4, 6], [5, 7]],
            [[None, None], [None, None], [0, 0], [0, None]]],
        'EDF6g': [
            [[10, 10], [10, 10], [10, 10], [10, 10]],
            [[8, 8], [10, 10], [6, 6], [8, 8]]]}
    if missing_baseline: raw['EDF6f'][0][0] = [None, None]
    for name, days in raw.items():
        ids = ['Ctrl', 'PI', 'KOCtrl', 'KOPI'] if name == 'EDF6f' else ['CtrlIg', 'CtrlAnti', 'OEIg', 'OEAnti']
        ws = wb.create_sheet(name)
        ws['A1'], ws['A2'] = 'Wound Area (mm^2)', 'Day'
        if name == 'EDF6f': first, second = {ids[0]: -1, ids[1]: 1}, {ids[2]: -1, ids[3]: 1}
        else: first, second = {ids[0]: -1, ids[2]: 1}, {ids[1]: -1, ids[3]: 1}
        cs = [dict(id=i, label=i, coefficients=c) for i, c in zip(['effect_reference', 'effect_altered', 'difference_of_effects'],
            [first, second, {**{g: -v for g, v in first.items()}, **second}])]
        p = dict(id=name, label=name, group_order=ids, days=list(range(len(days))),
            comparison_type='history_background' if name == 'EDF6f' else 'oe_blockade',
            extended_caption_n=2, main_caption_n=2, main_caption_relation='equal', main_rate_ns={g: 2 for g in ids}, contrasts=cs)
        m['panels'].append(p)
        for d, values in enumerate(days):
            row = d+3
            ws.cell(row, 1, d)
            e = dict(id=f'{name}_D{d}', panel=name, workbook='1', sheet=name, day=d, kind='records', unit='mm^2',
                header_guards=[dict(cell='A1', value='Wound Area (mm^2)'), dict(cell='A2', value='Day'), dict(cell=f'A{row}', value=d)], groups=[])
            for i, (gid, vs) in enumerate(zip(ids, values)):
                start = 2+i*2
                label_cell = f'{get_column_letter(start)}2'
                ws[label_cell] = gid
                cells = []
                for j, v in enumerate(vs):
                    address = f'{get_column_letter(start+j)}{row}'
                    ws[address] = v
                    cells.append(address)
                e['groups'].append(dict(id=gid, label=gid, source_label=gid, label_cell=label_cell, cells=cells,
                    expected_n=sum(v is not None for v in vs), expected_missing_cells=[c for c, v in zip(cells, vs) if v is None]))
            m['endpoints'].append(e)
    path = folder/'fixture.xlsx'
    wb.save(path)
    wb.close()
    return m, {'1': path}


class DailyAreaTests(unittest.TestCase):
    def test_offsets_coverage_and_zero_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder)
            data = reconstruct(m, read_workbooks(m, paths))
            cs = {(r['panel'], r['day'], r['contrast'].split('__')[1]): r for r in data['contrasts']}
            r = cs['EDF6f', 1, 'effect_reference']
            self.assertEqual((r['raw_mean'], r['baseline_mean'], r['adjusted_mean']), (1, 2, -1))
            r = cs['EDF6f', 1, 'difference_of_effects']
            self.assertEqual((r['raw_mean'], r['baseline_mean'], r['adjusted_mean']), (0, -1, 1))
            self.assertIsNone(cs['EDF6f', 2, 'effect_reference']['raw_mean'])
            self.assertEqual(cs['EDF6f', 2, 'effect_reference']['raw_missing_reason'], 'current=Ctrl,PI')
            self.assertIsNone(cs['EDF6f', 2, 'difference_of_effects']['adjusted_mean'])
            self.assertEqual(cs['EDF6f', 2, 'effect_altered']['raw_mean'], 0)
            self.assertFalse(cs['EDF6f', 2, 'effect_altered']['structural_day0_zero'])
            self.assertTrue(cs['EDF6f', 2, 'effect_altered']['all_contributing_current_records_zero'])
            self.assertTrue(cs['EDF6f', 2, 'effect_altered']['adjusted_at_area_floor'])
            self.assertEqual(cs['EDF6f', 2, 'effect_altered']['adjusted_mean'], -1)
            self.assertFalse(cs['EDF6f', 2, 'effect_reference']['all_contributing_current_records_zero'])
            self.assertFalse(cs['EDF6f', 1, 'difference_of_effects']['all_contributing_current_records_zero'])
            self.assertFalse(cs['EDF6g', 1, 'difference_of_effects']['all_contributing_current_records_zero'])
            self.assertEqual(data['metadata']['all_zero_area_contrasts'], [dict(contrast='EDF6f__effect_altered', day=2)])
            gs = {(r['panel'], r['day'], r['group']): r for r in data['groups']}
            self.assertEqual(gs['EDF6f', 2, 'KOCtrl']['sample_sd'], 0)
            self.assertIsNone(gs['EDF6f', 2, 'KOPI']['sample_sd'])
            self.assertEqual(gs['EDF6f', 2, 'KOPI']['source_n'], 1)
            self.assertNotIn(('EDF6g', 2, 'CtrlIg'), gs)
            self.assertEqual(gs['EDF6g', 1, 'OEAnti']['mean'], gs['EDF6g', 1, 'CtrlIg']['mean'])
            self.assertEqual(cs['EDF6g', 1, 'effect_altered']['raw_mean'], -2)
            self.assertEqual(data['metadata']['measured_zero_records'], 3)
            write_outputs(folder, data)
            result = verify(m, paths, folder)
            self.assertEqual(result['status'], 'passed')
            print('ARTIFICIAL_VERIFICATION', json.dumps(result))

    def test_missing_baseline_keeps_current_raw_contrast(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder, missing_baseline=True)
            data = reconstruct(m, read_workbooks(m, paths))
            r = next(r for r in data['contrasts'] if r['panel'] == 'EDF6f' and r['day'] == 1 and r['contrast'].endswith('effect_reference'))
            self.assertEqual(r['raw_mean'], 1)
            self.assertIsNone(r['baseline_mean'])
            self.assertIsNone(r['adjusted_mean'])
            self.assertEqual(r['adjusted_missing_reason'], 'baseline=Ctrl')
            write_outputs(folder, data)
            self.assertEqual(verify(m, paths, folder)['status'], 'passed')

    def test_floor_requires_exact_zeros_and_available_baseline_for_adjustment(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder)
            wb = load_workbook(paths['1'])
            wb['EDF6f']['F5'] = 1e-12
            wb.save(paths['1'])
            wb.close()
            data = reconstruct(m, read_workbooks(m, paths))
            r = next(r for r in data['contrasts'] if r['panel'] == 'EDF6f' and r['day'] == 2 and r['contrast'].endswith('effect_altered'))
            self.assertFalse(r['all_contributing_current_records_zero'])
            write_outputs(folder, data)
            self.assertEqual(verify(m, paths, folder)['status'], 'passed')
            wb = load_workbook(paths['1'])
            wb['EDF6f']['F5'] = 0
            wb['EDF6f']['F3'] = wb['EDF6f']['G3'] = None
            wb.save(paths['1'])
            wb.close()
            g = m['endpoints'][0]['groups'][2]
            g['expected_n'], g['expected_missing_cells'] = 0, ['F3', 'G3']
            data = reconstruct(m, read_workbooks(m, paths))
            r = next(r for r in data['contrasts'] if r['panel'] == 'EDF6f' and r['day'] == 2 and r['contrast'].endswith('effect_altered'))
            self.assertTrue(r['all_contributing_current_records_zero'])
            self.assertFalse(r['adjusted_at_area_floor'])
            self.assertIsNone(r['adjusted_mean'])
            self.assertEqual(r['adjusted_missing_reason'], 'baseline=KOCtrl')
            write_outputs(folder, data)
            self.assertEqual(verify(m, paths, folder)['status'], 'passed')

    def test_wrong_day_header_count_and_blank_pattern_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder)
            cache = read_workbooks(m, paths)
            for address, value in [('A1', 'Wrong unit'), ('A3', 99), ('B2', 'Wrong group'), ('B3', float('nan')), ('B3', True), ('B5', 0)]:
                changed = dict(cache)
                changed['1', 'EDF6f', address] = value
                with self.assertRaises(ValueError): reconstruct(m, changed)
            changed = copy.deepcopy(m)
            changed['endpoints'][0]['groups'][0]['expected_n'] = 9
            with self.assertRaises(ValueError): reconstruct(changed, cache)

    def test_formula_rejected_by_both_readers(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder)
            wb = load_workbook(paths['1'])
            wb['EDF6f']['B3'] = '=1+2'
            wb.save(paths['1'])
            wb.close()
            with self.assertRaises(ValueError): read_workbooks(m, paths)
            with self.assertRaises(AssertionError): verify(m, paths, folder)

    def test_output_and_contrast_meaning_tamper_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            m, paths = fixture(folder)
            data = reconstruct(m, read_workbooks(m, paths))
            write_outputs(folder, data)
            for filename, field, value in [('contrasts', 'raw_mean', '99'), ('contrasts', 'baseline_mean', '99'),
                    ('contrasts', 'adjusted_mean', '99'), ('contrasts', 'missing_current_groups', 'fake'),
                    ('contrasts', 'all_contributing_current_records_zero', 'True'), ('contrasts', 'adjusted_at_area_floor', 'True'),
                    ('groups', 'sample_sd', 'NA'), ('group_baseline_components', 'missing_reason', 'fake'),
                    ('observations', 'missing', 'True'), ('source_cells', 'kind', 'fake')]:
                path = folder/(filename+'.tsv')
                original = path.read_bytes()
                with path.open(encoding='utf-8', newline='') as handle: rows = list(csv.DictReader(handle, delimiter='\t'))
                rows[0][field] = value
                with path.open('w', encoding='utf-8', newline='') as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaises(AssertionError): verify(m, paths, folder)
                path.write_bytes(original)
            bad = copy.deepcopy(m)
            bad['panels'][1]['contrasts'][1]['coefficients'] = {'OEAnti': 1, 'CtrlIg': -1}
            with self.assertRaises(AssertionError): verify(bad, paths, folder)


if __name__ == '__main__': unittest.main()
