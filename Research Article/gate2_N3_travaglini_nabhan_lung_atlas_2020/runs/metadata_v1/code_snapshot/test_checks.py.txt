"""Scientific input gates: prevent pseudoreplication, silent omission and bad joins."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from common import PACKAGE, read_json, new_run


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


metadata = load_script('01_metadata_gate')
intake = load_script('00_source_intake')
CONFIG = read_json(PACKAGE / 'config/pipeline_v1.json')


def cell(donor='P1', cell_id='1', **changes):
    row = {'cell_id': cell_id, 'donor_id': donor, 'assay': '10x', 'sample_id': donor + '_sample', 'tissue': 'lung', 'condition': 'histologically_normal', 'anatomical_region': 'distal', 'author_cell_type': 'Alveolar Epithelial Type 2', 'raw_library_id': donor + '_library', 'counts_unit': 'UMI'}
    row.update(changes)
    return row


class InputGates(unittest.TestCase):
    def test_source_absence_is_not_numeric_zero(self):
        self.assertIsNone(intake.source_number('-'))
        self.assertEqual(intake.source_number(0), 0)
        with self.assertRaises(ValueError):
            intake.source_number(1.5)

    def test_duplicate_composite_key_fails(self):
        errors, _, _, _ = metadata.audit_rows([cell(), cell()], CONFIG)
        self.assertTrue(any('duplicate' in x for x in errors))

    def test_barcode_can_repeat_across_libraries(self):
        errors, _, counts, _ = metadata.audit_rows([cell(), cell(raw_library_id='another')], CONFIG)
        self.assertEqual(errors, [])
        self.assertEqual(sum(counts.values()), 2)

    def test_missing_donor_and_wrong_assay_units_fail(self):
        errors, _, _, _ = metadata.audit_rows([cell(donor='unknown'), cell(cell_id='2', assay='SS2')], CONFIG)
        self.assertEqual(len(errors), 3)  # two rejected rows and no valid cells

    def test_library_identity_conflict_fails(self):
        errors, _, _, _ = metadata.audit_rows([cell(), cell('P2', cell_id='2', raw_library_id='P1_library')], CONFIG)
        self.assertTrue(any('conflicting' in x for x in errors))

    def test_tumor_and_blood_are_excluded(self):
        errors, excluded, counts, _ = metadata.audit_rows([cell(condition='tumor'), cell(cell_id='2', raw_library_id='blood_library', tissue='blood')], CONFIG)
        self.assertEqual(errors, [])
        self.assertEqual(sum(excluded.values()), 2)
        self.assertEqual(sum(counts.values()), 0)

    def test_cells_and_regions_do_not_create_donors(self):
        rows = [cell(cell_id=f'{side}_{i}', author_cell_type=label) for side, label in enumerate(('Alveolar Epithelial Type 2', 'Signaling Alveolar Epithelial Type 2')) for i in range(40)]
        errors, _, _, gates = metadata.audit_rows(rows, CONFIG)
        self.assertFalse(errors)
        self.assertTrue(all(g['metadata_count_gate'] == 'HOLD' for g in gates))

    def test_three_matched_donors_can_pass_metadata_only(self):
        rows = [cell(donor=f'P{d}', cell_id=f'{side}_{i}', author_cell_type=label) for d in (1, 2, 3) for side, label in enumerate(('Alveolar Epithelial Type 2', 'Signaling Alveolar Epithelial Type 2')) for i in range(20)]
        errors, _, _, gates = metadata.audit_rows(rows, CONFIG)
        self.assertFalse(errors)
        self.assertEqual([g['n_eligible_donors'] for g in gates if g['contrast'] == 'AT2_state'], [3])
        for row in rows:
            if row['author_cell_type'].startswith('Signaling'):
                row['anatomical_region'] = 'proximal'
                row['raw_library_id'] += '_proximal'
                row['sample_id'] += '_proximal'
        errors, _, _, gates = metadata.audit_rows(rows, CONFIG)
        self.assertFalse(errors)
        self.assertTrue(all(g['metadata_count_gate'] == 'HOLD' for g in gates))

    def test_existing_run_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaises(ValueError):
                new_run(path)


if __name__ == '__main__':
    unittest.main()
