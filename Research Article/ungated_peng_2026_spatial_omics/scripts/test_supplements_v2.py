import unittest
import tempfile
import zipfile
from pathlib import Path
from supplements_v2 import merged_anchors, cell, marks, rc, col, read_xlsx


class SourceTests(unittest.TestCase):
    def test_merge_expansion_is_bounded(self):
        s={'anchors':merged_anchors(['B5:B9','F11:F12']),
           'cells':{'B5':{'value':'0027472'},'F11':{'value':'TMA P#7'}}}
        self.assertEqual(cell(s,'B9',True),('0027472','B5'))
        self.assertEqual(cell(s,'B10',True),('','B10'))
        self.assertEqual(cell(s,'F12',True),('TMA P#7','F11'))
        self.assertEqual(cell(s,'F13',True),('','F13'))

    def test_punctuation_does_not_make_independent_patients(self):
        self.assertEqual([marks(x) for x in ['', '✓', '✓*', '✓ *']],[0,1,2,2])
        with self.assertRaises(ValueError):marks('maybe')

    def test_overlapping_merges_fail(self):
        with self.assertRaises(ValueError):merged_anchors(['A1:A3','A3:A4'])

    def test_addresses_beyond_Z(self):
        self.assertEqual(rc('AA31'),(31,27));self.assertEqual(col(31),'AE')

    def test_saved_strings_zero_formula_cache_and_merge(self):
        prefix='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'source.xlsx'
            with zipfile.ZipFile(path,'w') as z:
                z.writestr('xl/workbook.xml',f'<workbook xmlns="{prefix}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Tab 3" sheetId="1" r:id="rId1"/></sheets></workbook>')
                z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
                z.writestr('xl/sharedStrings.xml',f'<sst xmlns="{prefix}"><si><t>0027472</t></si></sst>')
                z.writestr('xl/styles.xml',f'<styleSheet xmlns="{prefix}"><cellXfs><xf numFmtId="0"/><xf numFmtId="16"/></cellXfs></styleSheet>')
                z.writestr('xl/worksheets/sheet1.xml',f'<worksheet xmlns="{prefix}"><dimension ref="A1:D2"/><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><v>0</v></c><c r="C1"><f>SUM(B1:B2)</f><v>0</v></c><c r="D1" s="1"><v>45903</v></c></row></sheetData><mergeCells><mergeCell ref="A1:A2"/></mergeCells></worksheet>')
            s=read_xlsx(path,'S1')['Tab 3']
            self.assertEqual(cell(s,'A2',True),('0027472','A1'))
            self.assertEqual(cell(s,'B1'),('0','B1'))
            self.assertEqual(cell(s,'B2'),('','B2'))
            self.assertEqual(s['cells']['C1']['formula'],'=SUM(B1:B2)')
            self.assertEqual(s['cells']['C1']['value'],'0')
            self.assertEqual(s['cells']['D1']['value'],'45903')
            self.assertEqual(s['cells']['D1']['number_format_code'],'d-mmm')


if __name__=='__main__':unittest.main()
