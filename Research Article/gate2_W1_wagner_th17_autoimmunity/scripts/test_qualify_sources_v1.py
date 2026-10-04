"""Adversarial identity-join checks for the source qualification stage."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('wg_qualify', Path(__file__).with_name('qualify_sources_v1.py'))
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.cells = [dict(cell_id='SRR1', MD_SRX='SRX1', cell_type='Th17p')]
        self.samples = [dict(series='GSE75109', gsm='GSM1', sra_relation='SRA: https://example.test/?term=SRX1', source_label='batch 1', animal_id='')]

    def test_join_does_not_invent_animal(self):
        result = q.join_cells(self.cells, self.samples)[0]
        self.assertEqual(result['animal_id'], '')
        self.assertEqual(result['biological_unit_status'], 'unresolved')

    def test_duplicate_srx_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate GEO SRX'):
            q.join_cells(self.cells, self.samples + copy.deepcopy(self.samples))

    def test_membership_mismatch_rejected(self):
        self.cells[0]['MD_SRX'] = 'SRX2'
        with self.assertRaisesRegex(ValueError, 'membership mismatch'):
            q.join_cells(self.cells, self.samples)

    def test_condition_conflict_rejected(self):
        self.cells[0]['cell_type'] = 'Th17n'
        with self.assertRaisesRegex(ValueError, 'condition mismatch'):
            q.join_cells(self.cells, self.samples)

    def test_duplicate_author_identity_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate or empty author cell ID'):
            q.join_cells(self.cells * 2, self.samples)


if __name__ == '__main__':
    unittest.main()
