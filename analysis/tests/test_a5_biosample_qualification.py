"""The alternate identity scheme must never ignore a contradictory source ID."""
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import qualify_a5_biosample_metadata_v3 as q

SOFT = '''^SERIES = GSE303646
!Series_sample_id = GSM1
^SAMPLE = GSM1
!Sample_title = MUC1_young_control_d0
!Sample_series_id = GSE303646
!Sample_relation = BioSample: SAMN1
'''
XML = '''<BioSampleSet><BioSample accession="SAMN1"><Ids><Id db_label="Sample name">MUC1</Id></Ids>
<Attributes><Attribute attribute_name="sex">male</Attribute><Attribute attribute_name="treatment">DO NOT EXPORT</Attribute></Attributes>
</BioSample></BioSampleSet>'''


class A5BioSampleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.soft = Path(self.tmp.name)/'input.soft'; self.xml = Path(self.tmp.name)/'input.xml'
        self.soft.write_text(SOFT); self.xml.write_text(XML)

    def run_case(self): return q.qualify(self.soft, self.xml)

    def test_missing_reverse_link_is_reported_not_imputed(self):
        inventory, rows = self.run_case()
        self.assertEqual(inventory['reverse_geo_links'], 0)
        self.assertIsNone(inventory['biological_unit_count'])
        self.assertFalse(rows[0]['reverse_geo_link_present'])
        self.assertNotIn('DO NOT EXPORT', str((inventory, rows)))

    def test_alias_disagreement_stops(self):
        self.xml.write_text(XML.replace('MUC1', 'MUC2'))
        with self.assertRaisesRegex(ValueError, 'disagree'): self.run_case()

    def test_contradictory_reverse_link_stops(self):
        self.xml.write_text(XML.replace('</Ids>', '<Id db="GEO">GSM2</Id></Ids>'))
        with self.assertRaisesRegex(ValueError, 'Contradictory'): self.run_case()

    def test_wrong_accession_stops(self):
        self.xml.write_text(XML.replace('SAMN1', 'SAMN2'))
        with self.assertRaisesRegex(ValueError, 'membership'): self.run_case()

    def test_duplicate_alias_stops(self):
        self.xml.write_text(XML.replace('</Ids>', '<Id db_label="Sample name">MUC1</Id></Ids>'))
        with self.assertRaisesRegex(ValueError, 'alias'): self.run_case()

    def test_other_study_rejected(self):
        self.soft.write_text(SOFT.replace('GSE303646', 'GSE1'))
        with self.assertRaisesRegex(ValueError, 'only supports'): self.run_case()


if __name__ == '__main__': unittest.main()
