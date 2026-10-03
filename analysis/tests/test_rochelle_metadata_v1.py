import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / 'scripts/qualify_rochelle_metadata_v1.py'
spec = importlib.util.spec_from_file_location('rochelle_v1', P)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SourceIdentityTests(unittest.TestCase):
    def test_repeated_donor_and_multiplex_title_are_not_new_units(self):
        source = '^SERIES = GSE306194\n'
        for i in range(2):
            source += f'^SAMPLE = GSM{i}\n!Sample_title = passage {i}\n!Sample_characteristics_ch1 = individual: Donor1\n'
        source += '^SAMPLE = GSM9\n!Sample_title = D7V caudal; R0G proximal\n'
        result = module.summarize(module.parse_soft(source, 'GSE306194'))
        self.assertEqual(result['explicit_individual_labels'], ['Donor1'])
        self.assertEqual(result['sample_records_without_explicit_individual'], 1)

    def test_duplicate_or_mismatched_source_rejected(self):
        source = '^SERIES = GSE306194\n^SAMPLE = GSM1\n!Sample_title = x\n'
        with self.assertRaises(ValueError):
            module.parse_soft(source + '^SAMPLE = GSM1\n!Sample_title = y\n', 'GSE306194')
        with self.assertRaises(ValueError):
            module.parse_soft(source, 'GSE306714')

    def test_conflicting_characteristics_remain_explicit(self):
        source = '^SERIES = GSE306194\n^SAMPLE = GSM1\n!Sample_title = x\n!Sample_characteristics_ch1 = individual: A\n!Sample_characteristics_ch1 = individual: B\n'
        self.assertEqual(module.parse_soft(source, 'GSE306194')[0]['characteristics']['individual'], ['A', 'B'])

if __name__ == '__main__':
    unittest.main()
