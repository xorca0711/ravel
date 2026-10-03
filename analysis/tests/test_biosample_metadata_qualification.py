"""Adversarial accession-join and interpretation checks on synthetic metadata."""
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import qualify_biosample_metadata_v1 as q

SOFT = '''^SERIES = GSE1
!Series_sample_id = GSM1
^SAMPLE = GSM1
!Sample_title = well 1
!Sample_series_id = GSE1
!Sample_relation = BioSample: https://example.test/SAMN1
'''
XML = '''<BioSampleSet><BioSample accession="SAMN1"><Ids><Id db="GEO">GSM1</Id>
<Id db="SRA">SRS1</Id></Ids><Description><Title>well 1</Title></Description>
<Attributes><Attribute attribute_name="batch">one</Attribute>
<Attribute attribute_name="treatment">DO NOT EXPORT</Attribute></Attributes>
<Owner><Contacts>DO NOT EXPORT</Contacts></Owner></BioSample></BioSampleSet>'''


class BioSampleQualificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.soft = Path(self.tmp.name) / 'input.soft'
        self.xml = Path(self.tmp.name) / 'input.xml'
        self.soft.write_text(SOFT)
        self.xml.write_text(XML)

    def run_case(self):
        return q.qualify([self.soft], [self.xml])

    def test_identity_is_not_replication_and_private_fields_not_exported(self):
        inventory, rows = self.run_case()
        self.assertIsNone(inventory['studies'][0]['biological_unit_count'])
        self.assertEqual(rows[0]['biosample'], 'SAMN1')
        self.assertNotIn('DO NOT EXPORT', str((inventory, rows)))

    def test_missing_geo_relation_stops(self):
        self.soft.write_text(SOFT.split('!Sample_relation')[0])
        with self.assertRaisesRegex(ValueError, 'Every GEO'): self.run_case()

    def test_duplicate_relation_stops(self):
        self.soft.write_text(SOFT + '!Sample_relation = BioSample: SAMN1\n')
        with self.assertRaisesRegex(ValueError, 'repeated'): self.run_case()

    def test_wrong_membership_stops(self):
        self.xml.write_text(XML.replace('SAMN1', 'SAMN2'))
        with self.assertRaisesRegex(ValueError, 'membership'): self.run_case()

    def test_wrong_reverse_geo_link_stops(self):
        self.xml.write_text(XML.replace('GSM1', 'GSM2'))
        with self.assertRaisesRegex(ValueError, 'disagreement'): self.run_case()

    def test_duplicate_returned_record_stops(self):
        with self.assertRaisesRegex(ValueError, 'duplicate BioSample'):
            q.qualify([self.soft], [self.xml, self.xml])

    def test_error_payload_stops(self):
        self.xml.write_text('<ERROR>temporary upstream error</ERROR>')
        with self.assertRaisesRegex(ValueError, 'error response'): self.run_case()


if __name__ == '__main__':
    unittest.main()
