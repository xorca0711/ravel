from pathlib import Path
import sys
import unittest
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reference_source_v1 import parse_soft, source_rows, audit_counts, condition


class SourceTests(unittest.TestCase):
    def test_soft_join_retains_timing_conflict(self):
        text = '^SAMPLE = GSM1\n!Sample_title = Wild type, vehicle, 24h, rep4\n!Sample_characteristics_ch1 = genotype: C57BL/6, LysM-Cre+/+ ; GRIP1wt/wt\n!Sample_characteristics_ch1 = treatment: Vehicle, 25 hours\n!Sample_relation = BioSample: https://www.ncbi.nlm.nih.gov/biosample/SAMN1\n'
        _, samples = parse_soft(text); row = source_rows('GSE248042', samples)[0]
        self.assertEqual(row['matrix_column'], 'WT_C_Rep4'); self.assertTrue(row['timing_conflict'])
        self.assertEqual(row['source_treatment'], 'Vehicle, 25 hours')
        self.assertEqual(row['within_assay_condition_pairing'], 'unknown')

    def test_conditions_are_source_explicit(self):
        self.assertEqual(condition('IL,4 24 hours'), 'IL4')
        self.assertEqual(condition('Corticosterone, 24 hours'), 'CORT')
        with self.assertRaises(ValueError): condition('unidentified')

    def test_exact_count_accounting(self):
        rows, zeros = audit_counts(pd.DataFrame({'x': [0, 1, 3], 'y': [0, 2, 0]}), ['x', 'y'], 'RNA')
        self.assertEqual(zeros, 1); self.assertEqual([r['count_sum'] for r in rows], [4, 2])

    def test_bad_counts_fail(self):
        for value in [-1, .5, float('nan')]:
            with self.assertRaises(ValueError): audit_counts(pd.DataFrame({'x': [value]}), ['x'], 'RNA')


if __name__ == '__main__': unittest.main()
