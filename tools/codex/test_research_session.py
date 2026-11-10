"""Lifecycle behavior tests use disposable repositories, never scientific runs."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("research_session", HERE / "research_session.py")
hook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hook)


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ravel hook test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces"
        self.root.mkdir()
        self.cache = Path(self.temp.name) / "cache"
        self.write(hook.SKILL, "---\nname: fixture\n---\nFixture reasoning procedure.")
        self.write(hook.REGISTRY, json.dumps({
            "questions": [{"id": "Q1", "dossier": "docs/research_dossiers/Q1.md",
                           "evidence": ["RQ_Specified/Q1/reports/RESULTS.md"]}],
            "question_guides": [{"question": "Q1", "entrypoint": "RQ_Specified/Q1/README.md",
                                 "context": "RQ_Specified/Q1/LITERATURE_CONTEXT.md"}],
            "article_candidates": [{"id": "P1", "plan": "Research Article/P1/PLAN.md",
                                    "evidence": ["Research Article/P1/RESULTS.md"]}],
        }))
        self.result = "RQ_Specified/Q1/reports/RESULTS.md"
        self.write(self.result, "# Original result\n")
        self.write("docs/research_dossiers/Q1.md", "# Dossier\n")
        self.run_git("init", "-q")
        self.run_git("config", "core.autocrlf", "false")
        self.run_git("add", ".")
        self.commit()

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def run_git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, timeout=10)

    def commit(self):
        self.run_git("-c", "user.name=Hook Test", "-c", "user.email=hook-test@example.invalid",
                     "commit", "-qm", "fixture", "--no-verify")

    def event(self, kind="SessionStart", **extra):
        return {"hook_event_name": kind, "source": "startup", "cwd": str(self.root),
                "session_id": "fixture-session", **extra}

    def call(self, kind="SessionStart", **extra):
        return hook.process(self.event(kind, **extra), self.cache)

    def test_startup_resume_compact_clear_fork_from_subdirectory(self):
        for source in sorted(hook.SOURCES):
            with self.subTest(source=source):
                result = self.call(source=source, cwd=str(self.root / "RQ_Specified/Q1"))
                self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "SessionStart")
                self.assertIn(str(self.root).replace("\\", "\\\\"), result["hookSpecificOutput"]["additionalContext"])

    def test_preexisting_dirty_and_untracked_work_are_not_attributed(self):
        self.write(self.result, "# Preexisting work")
        self.write("Research Article/P1/notes.md", "# Preexisting untracked work")
        self.call()
        self.assertEqual(self.call("Stop"), {})
        self.write(self.result, "# Further revision")
        self.assertEqual(self.call("Stop")["decision"], "block")

    def test_changed_evidence_routes_to_current_owner(self):
        self.call()
        self.write(self.result, "# A changed result")
        result = self.call("Stop")
        self.assertEqual(result["decision"], "block")
        locators = hook.owners(self.root, [self.result])
        self.assertEqual([x["id"] for x in locators], ["Q1"])
        self.assertEqual(locators[0]["current_documents"]["context"],
                         "RQ_Specified/Q1/LITERATURE_CONTEXT.md")

    def test_shared_dossier_directory_does_not_match_other_owner(self):
        self.assertEqual(hook.owners(self.root, ["docs/research_dossiers/Q2.md"]), [])

    def test_new_article_report_routes_by_plan_directory(self):
        self.assertEqual([x["id"] for x in hook.owners(self.root, ["Research Article/P1/NEW.md"])], ["P1"])

    def test_one_continuation_then_new_turn_can_be_reviewed(self):
        self.call()
        self.write(self.result, "# First change")
        self.assertEqual(self.call("Stop")["decision"], "block")
        self.write(self.result, "# Reviewed synthesis")
        self.assertEqual(self.call("Stop", stop_hook_active=True), {})
        self.assertEqual(self.call("Stop"), {})
        self.write(self.result, "# Later turn's new evidence")
        self.assertEqual(self.call("Stop")["decision"], "block")

    def test_committing_during_session_does_not_hide_changes(self):
        self.call()
        self.write(self.result, "# Committed result")
        self.run_git("add", self.result)
        self.commit()
        self.assertEqual(self.call("Stop")["decision"], "block")

    def test_compaction_preserves_outstanding_change(self):
        self.call()
        self.write(self.result, "# Outstanding change")
        self.call(source="compact")
        self.assertEqual(self.call("Stop")["decision"], "block")

    def test_nonresearch_work_does_not_trigger_review(self):
        self.call()
        self.write("tools/utility.py", "print('ok')")
        self.write("docs/guides/EDITOR.md", "# Editor setup")
        self.assertEqual(self.call("Stop"), {})

    def test_line_endings_do_not_trigger_review(self):
        self.call()
        (self.root / self.result).write_bytes(b"# Original result\r\n")
        self.assertEqual(self.call("Stop"), {})

    def test_missing_baseline_does_not_review_previous_work(self):
        self.write(self.result, "# Earlier work")
        result = self.call("Stop")
        self.assertNotIn("decision", result)
        self.assertIn("systemMessage", result)

    def test_deleted_result_is_detected(self):
        self.call()
        (self.root / self.result).unlink()
        self.assertEqual(self.call("Stop")["decision"], "block")

    def test_cache_is_scoped_by_checkout_and_session(self):
        other = Path(self.temp.name) / "other"
        self.assertNotEqual(hook.state_file(self.root, "one", self.cache),
                            hook.state_file(self.root, "two", self.cache))
        self.assertNotEqual(hook.state_file(self.root, "one", self.cache),
                            hook.state_file(other, "one", self.cache))
        self.assertEqual(hook.state_file(self.root, "../escape", self.cache).parent, self.cache)

    def test_outside_checkout_reference_rejected(self):
        with self.assertRaises(ValueError):
            hook.inside(self.root, "../../outside")

    def test_actual_config_command_runs_with_spaces_and_nested_cwd(self):
        self.write("tools/codex/research_session.py", (HERE / "research_session.py").read_text(encoding="utf-8"))
        config = json.loads((HERE.parents[1] / ".codex/hooks.json").read_text(encoding="utf-8"))
        handler = config["hooks"]["SessionStart"][0]["hooks"][0]
        command = handler["command_windows"] if sys.platform == "win32" else handler["command"]
        event = self.event(cwd=str(self.root / "RQ_Specified/Q1"), session_id=self.temp.name)
        result = subprocess.run(command, shell=True, input=json.dumps(event), text=True,
                                cwd=event["cwd"], capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["hookEventName"], "SessionStart")

    def test_other_checkout_without_implementation_is_a_noop(self):
        config = json.loads((HERE.parents[1] / ".codex/hooks.json").read_text(encoding="utf-8"))
        handler = config["hooks"]["SessionStart"][0]["hooks"][0]
        command = handler["command_windows"] if sys.platform == "win32" else handler["command"]
        result = subprocess.run(command, shell=True, input=json.dumps(self.event()), text=True,
                                cwd=self.root, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse((self.root / "tools").exists())

    def test_malformed_event_reports_unavailability_without_verdict(self):
        result = subprocess.run([sys.executable, str(HERE / "research_session.py")],
                                input="[]", capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("systemMessage", json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
