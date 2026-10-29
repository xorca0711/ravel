import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('hc',Path(__file__).resolve().parents[1]/'scripts/qualify_human_clinical_v2.py')
hc=importlib.util.module_from_spec(spec);spec.loader.exec_module(hc)
class ClinicalTests(unittest.TestCase):
    text='^SAMPLE = GSM1\n!Sample_title = 001C scRNAseq\n!Sample_characteristics_ch1 = disease: Control\n!Sample_characteristics_ch1 = age: 32\n!Sample_characteristics_ch1 = Sex: F\n'
    def test_preserves_subject_zero_prefix(self):self.assertEqual(hc.parse_samples(self.text).donor.iloc[0],'001C')
    def test_duplicate_subject_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):hc.parse_samples(self.text+self.text.replace('GSM1','GSM2'))
    def test_missing_age_retained(self):self.assertTrue(hc.parse_samples(self.text.replace('!Sample_characteristics_ch1 = age: 32\n','')).age.isna().all())
    def test_loose_title_not_guessed(self):
        with self.assertRaisesRegex(ValueError,'title-to-subject'):hc.parse_samples(self.text.replace('001C scRNAseq','sample from001C'))
if __name__=='__main__':unittest.main()
