"""Adversarial metadata join tests; synthetic records contain no biological data."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('geo_metadata', Path(__file__).resolve().parents[1]/'scripts/qualify_geo_metadata_v1.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE = '''^DATABASE = GeoMiame
^SERIES = GSE1
!Series_sample_id = GSM1
!Series_sample_id = GSM2
^SAMPLE = GSM1
!Sample_title = same pool, GEX
!Sample_series_id = GSE1
!Sample_library_strategy = RNA-Seq
!Sample_characteristics_ch1 = Sex: pooled male and female
!Sample_extract_protocol_ch1 = Do not export protocol text
^SAMPLE = GSM2
!Sample_title = same pool, ATAC
!Sample_series_id = GSE1
!Sample_library_strategy = ATAC-seq
'''


class MetadataTests(unittest.TestCase):
    def parse(self, text):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'metadata.soft'; p.write_text(text, encoding='utf-8')
            return module.read_family(p)
    def test_paired_assays_do_not_become_two_animals(self):
        series, samples=self.parse(BASE)
        result=module.summarize(series,samples)
        self.assertEqual(result['sample_record_count'],2)
        self.assertIsNone(result['biological_unit_count'])
        self.assertNotIn('Sample_extract_protocol_ch1',samples[0]['fields'])
    def test_missing_declared_sample_rejected(self):
        with self.assertRaisesRegex(ValueError,'membership mismatch'):
            self.parse(BASE.split('^SAMPLE = GSM2')[0])
    def test_duplicate_sample_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):
            self.parse(BASE.replace('^SAMPLE = GSM2','^SAMPLE = GSM1'))
    def test_wrong_parent_series_rejected(self):
        with self.assertRaisesRegex(ValueError,'enclosing series'):
            self.parse(BASE.replace('!Sample_series_id = GSE1','!Sample_series_id = GSE9',1))
    def test_superseries_memberships_are_not_extra_samples(self):
        series,samples=self.parse(BASE.replace('!Sample_series_id = GSE1','!Sample_series_id = GSE1\n!Sample_series_id = GSE2'))
        result=module.summarize(series,samples)
        self.assertEqual(result['sample_record_count'],2)
        self.assertEqual(result['membership_record_counts'],{'GSE1':2,'GSE2':2})


if __name__=='__main__':
    unittest.main()
