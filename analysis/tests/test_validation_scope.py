"""Validation must stay inside the active checkout, including arbitrary nested worktrees."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_repository import source_files


class ValidationScopeTests(unittest.TestCase):
    def test_nested_checkouts_and_worktree_container_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            (root / "current.md").write_text("# Current")
            for name, marker in [("sibling", "file"), ("clone", "directory"), (".worktrees", None)]:
                nested = root / name
                nested.mkdir()
                (nested / "not_current.md").write_text("# Different checkout")
                if marker == "file":
                    (nested / ".git").write_text("gitdir: elsewhere")
                elif marker == "directory":
                    (nested / ".git").mkdir()
            self.assertEqual(source_files(root, ".md"), [root / "current.md"])

    def test_active_scientific_subfolders_are_still_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "RQ_Specified" / "A15" / "reports"
            target.mkdir(parents=True)
            (target / "report.md").write_text("# Current evidence")
            self.assertEqual(source_files(root, ".md"), [target / "report.md"])
