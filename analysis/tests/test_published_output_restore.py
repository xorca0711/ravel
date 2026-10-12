"""Offline rejection and preservation tests for release-output restoration."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

MODULE = Path(__file__).resolve().parents[1] / 'scripts/restore_published_outputs.py'
spec = importlib.util.spec_from_file_location('published_outputs', MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ravel-restore-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.path = 'analysis/research/runs/example/result.txt'
        self.data = b'original evidence\n'
        self.member = {'path': self.path, 'bytes': len(self.data),
                       'sha256': hashlib.sha256(self.data).hexdigest()}

    def archive(self, entries=None, members=None):
        members = members or [self.member]
        manifest = json.dumps({'members': members}).encode()
        archive = self.base / 'fixture.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('publication-manifest.json', manifest)
                for name, value in entries if entries is not None else [(self.path, self.data)]:
                    z.writestr(name, value)
        lock = {'bytes': archive.stat().st_size, 'sha256': m.sha256(archive),
                'manifest_bytes': len(manifest), 'manifest_sha256': hashlib.sha256(manifest).hexdigest(),
                'members': members,
                'url': 'https://github.com/xorca0711/ravel/releases/download/test/fixture.zip'}
        return archive, lock

    def rejected(self, archive, lock, message):
        with self.assertRaisesRegex(m.RestoreError, message):
            m.restore(self.root, lock, archive)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_exact_restore_is_idempotent(self):
        archive, lock = self.archive()
        self.assertEqual(m.restore(self.root, lock, archive)['created'], 1)
        self.assertEqual((self.root/self.path).read_bytes(), self.data)
        self.assertEqual(m.restore(self.root, lock, archive)['created'], 0)

    def test_wrong_whole_hash_before_any_write(self):
        archive, lock = self.archive()
        lock['sha256'] = '0'*64
        self.rejected(archive, lock, 'Archive size/hash')

    def test_missing_extra_duplicate_members(self):
        for entries in ([], [(self.path,self.data), ('extra',b'x')],
                        [(self.path,self.data),(self.path,self.data)]):
            with self.subTest(entries=len(entries)):
                archive, lock = self.archive(entries)
                self.rejected(archive, lock, 'member set')

    def test_member_hash_checked_even_when_archive_hash_matches(self):
        archive, lock = self.archive([(self.path,b'x'*len(self.data))])
        self.rejected(archive, lock, 'Member hash')

    def test_manifest_hash_checked(self):
        archive, lock = self.archive()
        lock['manifest_sha256'] = '0'*64
        self.rejected(archive, lock, 'Manifest hash')

    def test_traversal_absolute_and_windows_paths(self):
        for bad in ('../escape', '/escape', 'C:/escape', 'a\\escape', 'a/../escape'):
            with self.subTest(path=bad):
                item = {**self.member, 'path': bad}
                archive, lock = self.archive([(bad,self.data)],[item])
                self.rejected(archive, lock, 'Unsafe')

    def test_casefold_collisions(self):
        item = {**self.member, 'path': self.path.upper()}
        archive, lock = self.archive(members=[self.member,item])
        self.rejected(archive, lock, 'Duplicate locked')

    def test_archive_symlink_refused(self):
        archive, lock = self.archive()
        manifest = json.dumps({'members': [self.member]}).encode()
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('publication-manifest.json', manifest)
            entry = zipfile.ZipInfo(self.path)
            entry.create_system = 3
            entry.external_attr = (0o120777 << 16)
            z.writestr(entry, self.data)
        lock['bytes'], lock['sha256'] = archive.stat().st_size, m.sha256(archive)
        self.rejected(archive, lock, 'Non-regular')

    def test_later_member_failure_does_not_install_earlier_member(self):
        second = {**self.member, 'path': 'analysis/later.txt', 'sha256': '0'*64}
        archive, lock = self.archive([(self.path,self.data), (second['path'],self.data)],
                                     [self.member,second])
        self.rejected(archive, lock, 'Member hash')

    def test_existing_conflict_preserved(self):
        archive, lock = self.archive()
        dest = self.root/self.path
        dest.parent.mkdir(parents=True)
        dest.write_bytes(b'local work')
        with self.assertRaisesRegex(m.RestoreError, 'refusing overwrite'):
            m.restore(self.root, lock, archive)
        self.assertEqual(dest.read_bytes(), b'local work')

    def test_destination_symlink_refused(self):
        archive, lock = self.archive()
        try:
            (self.root/'analysis').symlink_to(self.base, target_is_directory=True)
        except OSError:
            self.skipTest('Host lacks symlink privilege; exercised in Linux CI')
        with self.assertRaisesRegex(m.RestoreError, 'Symlink'):
            m.restore(self.root, lock, archive)

    def test_download_budget_and_host(self):
        archive, lock = self.archive()
        with patch.object(m, 'build_opener') as factory:
            factory.return_value.open.return_value = io.BytesIO(b'x'*12)
            with self.assertRaisesRegex(m.RestoreError, 'exceeds'):
                m.download({**lock, 'bytes': 5}, self.base/'download.zip')
        with self.assertRaisesRegex(m.RestoreError, 'Only locked Ravel'):
            m.download({**lock,'url':'https://example.com/other'}, self.base/'other.zip')

    def test_foreign_redirect_refused(self):
        with self.assertRaisesRegex(m.RestoreError, 'redirect host'):
            m.ReleaseRedirects().redirect_request(None,None,302,'',{},'https://example.com/private')


if __name__ == '__main__':
    unittest.main()
