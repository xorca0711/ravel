"""Root-checkout installation tests; no trust-store writes or model calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("install_session_hooks", HERE / "install_session_hooks.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ravel hook install ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.target = self.root / "branch", self.root / "main"
        (self.source / ".codex").mkdir(parents=True)
        self.target.mkdir()
        for name in ("config.toml", "hooks.json"):
            self.source.joinpath(".codex", name).write_bytes(HERE.parents[1].joinpath(".codex", name).read_bytes())

    def test_preflight_has_no_writes(self):
        self.assertEqual(installer.plan(self.source, self.target)["status"], "ready")
        self.assertFalse((self.target / ".codex").exists())

    def test_install_preserves_source_and_is_idempotent(self):
        original = (self.source / ".codex/config.toml").read_bytes()
        original_sidecar = (self.source / ".codex/hooks.json").read_bytes()
        self.assertEqual(installer.install(self.source, self.target)["status"], "installed-pending-trust")
        installed = self.target / ".codex/hooks.json"
        self.assertEqual(json.loads(installed.read_text()), json.loads(original_sidecar))
        before = installed.read_bytes()
        self.assertEqual(installer.install(self.source, self.target)["status"], "already-installed")
        self.assertEqual(installed.read_bytes(), before)
        self.assertEqual((self.source / ".codex/config.toml").read_bytes(), original)
        self.assertEqual((self.source / ".codex/hooks.json").read_bytes(), original_sidecar)
        self.assertEqual({p.name for p in installed.parent.iterdir()}, {"config.toml", "hooks.json"})

    def test_existing_unrelated_config_is_preserved(self):
        (self.target / ".codex").mkdir()
        config = self.target / ".codex/config.toml"
        original = b'# Preserve this\nmodel = "example"\n'
        config.write_bytes(original)
        installer.install(self.source, self.target)
        self.assertEqual(config.read_bytes(), original)

    def test_different_sidecar_is_never_replaced(self):
        (self.target / ".codex").mkdir()
        p = self.target / ".codex/hooks.json"
        p.write_text('{"hooks": {}}')
        with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
            installer.install(self.source, self.target)
        self.assertEqual(p.read_text(), '{"hooks": {}}')

    def test_existing_inline_hooks_or_disabled_setting_are_preserved(self):
        (self.target / ".codex").mkdir()
        p = self.target / ".codex/config.toml"
        for content in ('[hooks]\nStop = []\n', '[features]\nhooks = false\n'):
            with self.subTest(content=content):
                p.write_text(content)
                with self.assertRaises(ValueError):
                    installer.install(self.source, self.target)
                self.assertEqual(p.read_text(), content)
                self.assertFalse((self.target / ".codex/hooks.json").exists())

    def test_main_checkout_uses_sidecar_without_duplicate(self):
        before = {p.name: p.read_bytes() for p in (self.source / ".codex").iterdir()}
        self.assertEqual(installer.install(self.source, self.source)["status"], "already-installed")
        self.assertEqual({p.name: p.read_bytes() for p in (self.source / ".codex").iterdir()}, before)

    def test_duplicate_source_inline_hooks_are_rejected(self):
        config = self.source / ".codex/config.toml"
        config.write_text(config.read_text() + "\n[hooks]\nStop = []\n")
        with self.assertRaisesRegex(ValueError, "only in hooks.json"):
            installer.install(self.source, self.target)
        self.assertFalse((self.target / ".codex").exists())

    def test_unexpected_source_event_is_rejected(self):
        sidecar = self.source / ".codex/hooks.json"
        payload = json.loads(sidecar.read_text())
        payload["hooks"]["PreToolUse"] = []
        sidecar.write_text(json.dumps(payload))
        with self.assertRaisesRegex(ValueError, "Unexpected source hook events"):
            installer.install(self.source, self.target)
        self.assertFalse((self.target / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
