"""Include the corrected C1 invariants in the repository's standard CI suite."""
import importlib.util
from pathlib import Path
import sys


SCRIPT_DIR = (Path(__file__).resolve().parents[2] / "RQ_Specified" /
              "A16_cd177_state_attribution/correction_20260928/scripts")


def load_tests(loader, tests, pattern):
    spec = importlib.util.spec_from_file_location(
        "a16_corrected_c1_invariant_tests", SCRIPT_DIR / "test_invariants.py")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(SCRIPT_DIR))
    return loader.loadTestsFromTestCase(module.InvariantTests)
