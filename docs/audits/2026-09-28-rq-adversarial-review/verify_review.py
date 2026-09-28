"""Small read-only evidence probes for the 2026-09-28 review; no scientific refits."""
import ast
import csv
import hashlib
import json
import math
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


tracked = [name for name in git("ls-files", "-z").split("\0") if name]
syntax = []
for name in tracked:
    if name.endswith(".py"):
        try:
            ast.parse((ROOT / name).read_text(encoding="utf-8-sig"), filename=name)
        except (SyntaxError, UnicodeError) as error:
            syntax.append({"path": name, "error": str(error)})

pilot_checks = {}
base = "docs/roadmap_runs/2026-09-27-followthrough/"
for question in ("A12", "A13"):
    data = rows(base + question + "_heldout_predictions.csv")
    selected = [r for r in data if float(r["uncertainty"]) == .2
                and int(r["cell_floor"]) == 50 and float(r["alpha"]) == 1
                and (question == "A13" or r["recipient"] == "AT2")]
    grouped = {}
    for row in selected:
        grouped.setdefault(row["model"], []).append(row)
    mse = {name: sum((float(r["observed"]) - float(r["predicted"])) ** 2
                    for r in group) / len(group) for name, group in grouped.items()}
    pilot_checks[question] = {
        "n_per_model": {k: len(v) for k, v in grouped.items()},
        "rmse": {k: math.sqrt(v) for k, v in mse.items()},
        "joint_mse_improvement_over_alternative": mse["alternative"] - mse["joint"],
        "joint_Q2_vs_training_mean": 1 - mse["joint"] / mse["mean"],
        "input_sha256": hashlib.sha256((ROOT / (base + question + "_heldout_predictions.csv")).read_bytes()).hexdigest(),
    }

# Exact proportional libraries: median-of-ratios already removes their depth ratio.
# Multiplying the factor by library size normalizes depth twice.
counts_a, counts_b = [100, 200, 300], [200, 400, 600]
sf_a, sf_b = 1 / math.sqrt(2), math.sqrt(2)
proper_a = counts_a[0] / sf_a
proper_b = counts_b[0] / sf_b
current_a = counts_a[0] / (sf_a * sum(counts_a) / 1e6)
current_b = counts_b[0] / (sf_b * sum(counts_b) / 1e6)
assert math.isclose(proper_a, proper_b)
assert math.isclose(current_b / current_a, .5)

result = {
    "snapshot": {"head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"),
                 "locally_recorded_origin_main": git("rev-parse", "origin/main"),
                 "ahead_behind_local_origin": git("rev-list", "--left-right", "--count", "HEAD...origin/main"),
                 "live_remote_queried": False},
    "tracked_files": len(tracked),
    "tracked_python_sources": sum(n.endswith(".py") for n in tracked),
    "syntax_failures": syntax,
    "rq_workspace_counts": dict(sorted(Counter(n.split("/")[1] for n in tracked if n.startswith("RQ_Specified/") and n.count("/") > 1).items())),
    "pilot_metric_reaggregation": pilot_checks,
    "A15_scaling_counterexample": {"proper_normalized_ratio_B_over_A": proper_b / proper_a,
                                  "implemented_double_normalized_ratio_B_over_A": current_b / current_a,
                                  "implemented_log_score_difference": math.log2(current_b + 1) - math.log2(current_a + 1),
                                  "scope": "Deterministic method counterexample, not a re-estimated biological effect"},
    "A11_exact_two_sided_p_floor": {str(n): 2 / 2 ** n for n in (3, 4, 8)},
}
(OUT / "evidence.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"tracked_files": len(tracked), "python_sources": result["tracked_python_sources"],
                  "syntax_failures": len(syntax), "pilot_checks": pilot_checks,
                  "A15_counterexample_confirmed": True}, indent=2))
