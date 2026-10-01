"""Failure-path tests for the A23 evidence intake, using synthetic temporary files."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/00_intake.py'
SPEC = importlib.util.spec_from_file_location('a23_intake', PATH)
INTAKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INTAKE)


class A23IntakeProtectionTests(unittest.TestCase):
    def test_changed_source_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'source.tsv'
            path.write_bytes(b'original source')
            entries = [dict(path=path.name, sha256=INTAKE.digest(path))]
            path.write_bytes(b'changed source')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                INTAKE.verify_inputs(root, entries)

    def test_manifest_cannot_escape_its_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            root.mkdir()
            outside = root.parent / 'outside.txt'
            outside.write_bytes(b'outside')
            with self.assertRaisesRegex(ValueError, 'outside repository'):
                INTAKE.verify_inputs(root, [dict(path='../outside.txt', sha256=INTAKE.digest(outside))])

    def test_unknown_units_cannot_pass_eligibility(self):
        for value in (None, False, 'true', 1):
            self.assertFalse(INTAKE.eligible(dict(units=value, endpoint=True), ['units', 'endpoint']))
        self.assertTrue(INTAKE.eligible(dict(units=True, endpoint=True), ['units', 'endpoint']))

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            existing = root / 'tables'
            existing.mkdir()
            sentinel = existing / 'saved.tsv'
            sentinel.write_bytes(b'preserve me')
            with self.assertRaises(FileExistsError):
                INTAKE.guard_outputs([root / 'metadata', existing, root / 'reports'])
            self.assertEqual(sentinel.read_bytes(), b'preserve me')
            self.assertFalse((root / 'metadata').exists())


if __name__ == '__main__':
    unittest.main()
