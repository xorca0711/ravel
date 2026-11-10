"""Archive migration checks use synthetic contracts and Git history only."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

import test_research_governance as fixtures
from lib.path_migrations import MANIFEST, entries, migration_errors, resolve_historical
from lib.research_governance import ResearchError, check_registry, execute, receipt_errors, within


class PathMigrationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.GovernanceTests('test_valid_exposed_exploration')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.fixture.write('.gitattributes', '* -text\n')
        self.fixture.index['infrastructure_paths'].append('analysis/research/registry.json')
        self.records = []

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              capture_output=True).stdout.decode().strip()

    def save(self):
        self.fixture.write(MANIFEST, json.dumps({'schema_version': 1, 'files': self.records}))

    def move(self, old, new):
        source, target = self.root / old, self.root / new
        data = source.read_bytes()
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        self.records.append({'from': old, 'to': new,
                             'source_revision': self.base,
                             'sha256': hashlib.sha256(data).hexdigest()})
        self.save()

    def freeze(self):
        self.fixture.freeze()
        self.base = self.git('rev-parse', 'HEAD')
        self.fixture.index['infrastructure_paths'].append(MANIFEST)
        self.fixture.save_index()

    def test_receipt_and_base_gate_preserve_exact_moved_code(self):
        self.fixture.freeze()
        receipt = execute(self.root, 'contract.json', 'before_move')
        receipt_path = receipt.relative_to(self.root).as_posix()
        self.fixture.index['receipts'].append(receipt_path)
        self.freeze()
        saved_receipt = receipt.read_bytes()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        self.assertEqual(migration_errors(self.root, self.base), [])
        self.assertEqual(check_registry(self.root, base=self.base), [])
        self.assertEqual(receipt_errors(self.root, receipt_path), [])
        self.assertEqual(receipt.read_bytes(), saved_receipt)
        self.assertEqual(within(self.root, 'analysis/run.py'), self.root/'analysis/canonical/run.py')
        self.assertEqual(within(self.root, 'analysis/run.py', exists=False), self.root/'analysis/run.py')
        self.assertIsNone(resolve_historical(self.root, 'analysis/other.py'))

    def test_changed_missing_and_reappearing_files_fail(self):
        self.freeze()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        target = self.root/'analysis/canonical/run.py'
        original = target.read_bytes()
        for data in (b'tampered', original.replace(b'\n', b'\r\n')):
            target.write_bytes(data)
            with self.assertRaises(ResearchError):
                within(self.root, 'analysis/run.py')
            self.assertTrue(migration_errors(self.root, self.base))
        target.unlink()
        self.assertTrue(migration_errors(self.root, self.base))
        target.write_bytes(original)
        (self.root/'analysis/run.py').write_bytes(original)
        self.assertTrue(any('reappeared' in e for e in migration_errors(self.root, self.base)))

    def test_unsafe_ambiguous_and_chained_maps_fail(self):
        self.freeze()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        valid = copy.deepcopy(self.records)
        for path in ('../escape.py', '/absolute.py', 'C:/escape.py', 'dir\\file.py', './alias.py'):
            self.records = copy.deepcopy(valid)
            self.records[0]['to'] = path
            self.save()
            with self.assertRaises(ValueError):
                entries(self.root)
        for extra in (valid[0], dict(valid[0], **{'from':'another.py'}),
                      dict(valid[0], **{'from':valid[0]['to'], 'to':'third.py'})):
            self.records = copy.deepcopy(valid) + [extra]
            self.save()
            with self.assertRaises(ValueError):
                entries(self.root)

    def test_manifest_cannot_redefine_source_bytes_or_revision(self):
        self.freeze()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        target = self.root/'analysis/canonical/run.py'
        target.write_bytes(b'changed code')
        self.records[0]['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        self.save()
        self.assertTrue(any('source hash' in e for e in migration_errors(self.root, self.base)))
        self.records[0]['source_revision'] = '0'*40
        self.save()
        self.assertTrue(migration_errors(self.root, self.base))

    def test_previously_accepted_map_cannot_be_removed(self):
        self.freeze()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        self.git('add', '.')
        self.git('-c', 'user.name=Synthetic Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'synthetic relocation')
        accepted = self.git('rev-parse', 'HEAD')
        self.records = []
        self.save()
        self.assertTrue(any('immutable' in e for e in migration_errors(self.root, accepted)))

    def test_migrated_code_or_contract_cannot_execute(self):
        self.freeze()
        self.move('analysis/run.py', 'analysis/canonical/run.py')
        with self.assertRaisesRegex(ResearchError, 'cannot be replayed'):
            execute(self.root, 'contract.json', 'after_move')
        self.move('contract.json', 'canonical/contract.json')
        for contract in ('contract.json', 'canonical/contract.json'):
            with self.assertRaisesRegex(ResearchError, 'cannot be replayed'):
                execute(self.root, contract, 'after_move')
        self.assertFalse((self.root/'analysis/research/runs/after_move').exists())


if __name__ == '__main__':
    unittest.main()
