"""Compile repository Python sources and verify the recorded Song v1 parse failure."""
import compileall
import hashlib
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SONG = Path("Research Article/gate3_2R_C2_song_2024")
FAILED_SCRIPT = SONG / "scripts/analyze_v1.py"
FAILURE_RECORD = SONG / "FAILED_RUNS_V1.md"
# Digests from the original Song study head, 2a312302.
SCRIPT_SHA256 = "5971601f7216c32daf20d4164e2380890740c42d1095748b26488dd24c0de7d8"
RECORD_SHA256 = "4a2b197c270a5a16d922dd4dda9e1e724afb9108fa827a5d8baa6de06c2f2031"


def verify_failed_source(root):
    source = (root / FAILED_SCRIPT).read_bytes()
    if hashlib.sha256(source).hexdigest() != SCRIPT_SHA256:
        raise ValueError(f"Archived source changed: {FAILED_SCRIPT}")
    if hashlib.sha256((root / FAILURE_RECORD).read_bytes()).hexdigest() != RECORD_SHA256:
        raise ValueError(f"Archived failure record changed: {FAILURE_RECORD}")

    try:
        compile(source, str(FAILED_SCRIPT), "exec", dont_inherit=True)
    except SyntaxError as exc:
        if (exc.lineno, exc.msg) != (192, "'{' was never closed"):
            raise
    else:
        raise ValueError(f"Expected the recorded SyntaxError in {FAILED_SCRIPT}")


def check(root):
    verify_failed_source(root)
    # The exact archived path was compiled above. All other .py files retain the
    # original compileall check, including other scripts named analyze_v1.py.
    skip = re.compile(r"[/\\]\.tools[/\\]|^" + re.escape(str(root / FAILED_SCRIPT)) + r"\Z")
    results = []
    for name in ("analysis", "Research Article", "RQ_Specified"):
        folder = root / name
        if not folder.is_dir():
            raise FileNotFoundError(folder)
        results.append(compileall.compile_dir(str(folder), quiet=1, force=True, rx=skip))
    return all(results)


if __name__ == "__main__":
    try:
        passed = check(ROOT)
    except (OSError, SyntaxError, ValueError) as error:
        sys.exit(str(error))
    if not passed:
        sys.exit(1)
    print("Python sources compiled and the archived Song v1 parse failure matched its record.")
