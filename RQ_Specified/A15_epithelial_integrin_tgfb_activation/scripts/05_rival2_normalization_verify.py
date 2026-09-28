"""Independently re-read A15 counts and verify correction v1 with NumPy/SciPy.

This module does not import either the original or corrected execution implementation.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu, rankdata

HERE = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def independent_test(values):
    ranks = rankdata(values, method="average")
    observed = float(ranks[:4].sum() - 10)
    distribution = np.array([ranks[list(pick)].sum() - 10
                             for pick in itertools.combinations(range(8), 4)])
    p = min(1.0, 2 * min(np.mean(distribution <= observed), np.mean(distribution >= observed)))
    return observed, float(p)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    destination = out / "independent_verification.json"
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite {destination}")
    run_path = out / "correction_run.json"
    run = load(run_path)
    spec = load(HERE / "config/a15_rival2_normalization_correction_v1.json")
    original = load(HERE / "tables/rival2/stage3_execute_run.json")
    checks = []

    def check(name, passed, detail=None):
        record = {"check": name, "passed": bool(passed)}
        if detail is not None:
            record["detail"] = detail
        checks.append(record)

    def close(name, observed, expected, tolerance=1e-10):
        check(name, np.allclose(observed, expected, atol=tolerance, rtol=1e-10),
              {"max_absolute_difference": float(np.max(np.abs(np.asarray(observed) - np.asarray(expected))))})

    for name, entry in run["inputs"].items():
        check(f"input hash: {name}", digest(entry["path"]) == entry["sha256"] == spec["sha256"][name])
    for name, expected in run["output_sha256"].items():
        check(f"output hash: {name}", digest(out / name) == expected)
    check("specification hash", digest(HERE / "config/a15_rival2_normalization_correction_v1.json") ==
          run["specification_sha256"])
    check("specification prose hash", digest(HERE / "reports/NORMALIZATION_CORRECTION_SPEC_V1.md") ==
          run["specification_markdown_sha256"])
    check("execution source hash", digest(HERE / "scripts/04_rival2_normalization_correction.py") ==
          run["execution_script_sha256"])
    check("original output and grades preserved", run["primary_files_replaced"] is False and
          run["claim_rows_added"] == 0 and run["register_grades_changed"] is False)
    columns = [s["column"] for arm in ("case", "reference") for s in original["arms"]["epithelium"][arm]]
    expected_samples = [{"arm": arm, "mouse": s["mouse"], "column": s["column"]}
                        for arm in ("case", "reference") for s in original["arms"]["epithelium"][arm]]
    check("original eight mice and column ordering", run["samples_case_then_reference"] == expected_samples)
    count_path = args.data_root / spec["data_paths_relative_to_data_root"]["counts"]
    symbol_path = args.data_root / spec["data_paths_relative_to_data_root"]["symbol_map"]
    check("independent data root count hash", digest(count_path) == spec["sha256"]["counts"])
    check("independent data root symbol hash", digest(symbol_path) == spec["sha256"]["symbol_map"])
    genes, data = [], []
    with gzip.open(count_path, "rt", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        id_field = reader.fieldnames[0]
        for row in reader:
            genes.append(row[id_field])
            data.append([int(row[c]) for c in columns])
    matrix = np.asarray(data, dtype=np.float64)
    gene_index = {g: i for i, g in enumerate(genes)}
    check("complete unique nonnegative matrix", len(genes) == len(gene_index) == spec["expected_count_rows"] and
          matrix.shape[1] == 8 and np.all(matrix >= 0))
    totals = matrix.sum(axis=0)
    close("all original library totals", totals, [original["library_totals"][c] for c in columns], 0)
    lookup = load(symbol_path)["records"]
    excluded = {lookup[s]["id"] for s in spec["reference_universe"]["excluded_symbols"]}
    mask = np.all(matrix > 0, axis=1) & np.array([g not in excluded for g in genes])
    reference_ids = sorted(g for g, keep in zip(genes, mask) if keep)
    with (out / "reference_genes.tsv").open(encoding="utf-8") as stream:
        recorded_ids = [r["ensembl_id"] for r in csv.DictReader(stream, delimiter="\t")]
    check("independent reference IDs", reference_ids == recorded_ids)
    check("broad reference minimum/count", int(mask.sum()) == run["reference_gene_count"] and
          mask.sum() >= spec["reference_universe"]["minimum_reference_genes"])
    positive = matrix[mask]
    geometric_means = np.exp(np.log(positive).mean(axis=1))
    factors = np.median(positive / geometric_means[:, None], axis=0)
    factors /= np.exp(np.log(factors).mean())
    close("all median-ratio factors", factors, [run["size_factors"][c] for c in columns])
    close("factor geometric mean", np.exp(np.log(factors).mean()), 1)
    with (out / "panel_scores.tsv").open(encoding="utf-8") as stream:
        score_rows = list(csv.DictReader(stream, delimiter="\t"))
    with (out / "size_factors.tsv").open(encoding="utf-8") as stream:
        factor_rows = list(csv.DictReader(stream, delimiter="\t"))
    close("factor table", [float(r["size_factor"]) for r in factor_rows], factors)
    observed_separation = {}
    for name, symbols in spec["panels"].items():
        selected = [s for s in symbols if np.median(matrix[gene_index[lookup[s]["id"]]]) >= 10]
        block = matrix[[gene_index[lookup[s]["id"]] for s in selected]]
        scores = np.log2(block / factors[None, :] + 1).mean(axis=0)
        result = run["corrected_sensitivity"][name]
        check(f"{name}: coverage", selected == result["coverage"]["symbols"])
        close(f"{name}: all scores", scores, result["case_values"] + result["reference_values"])
        panel_table = [r for r in score_rows if r["panel"] == name]
        check(f"{name}: score table mouse ordering", [r["mouse"] for r in panel_table] ==
              [r["mouse"] for r in expected_samples])
        close(f"{name}: score table", [float(r["score"]) for r in panel_table], scores)
        difference = scores[:4].mean() - scores[4:].mean()
        close(f"{name}: mean effect", difference, result["mean_difference"])
        u, p = independent_test(scores)
        close(f"{name}: exact midrank U and p", [u, p],
              [result["exact_test"]["u"], result["exact_test"]["p_two_sided"]])
        if len(np.unique(scores)) == 8:
            scipy_p = mannwhitneyu(scores[:4], scores[4:], alternative="two-sided", method="exact").pvalue
            close(f"{name}: SciPy exact rank-sum p", p, scipy_p)
        else:
            check(f"{name}: ties handled by exhaustive midrank permutations", True,
                  "SciPy tie-free exact comparison not applicable")
        shifts = (scores[:4, None] - scores[None, 4:]).ravel()
        close(f"{name}: all pairwise shifts", shifts, result["shift"]["pairwise_differences_case_major"])
        close(f"{name}: Hodges-Lehmann and full interval", [np.median(shifts), shifts.min(), shifts.max(), 68 / 70],
              [result["shift"][k] for k in ("estimate", "lower", "upper", "attained_coverage")])
        observed_separation[name] = bool(p <= 2 / 70 + 1e-12)
        check(f"{name}: corrected gate", observed_separation[name] == result["separates_at_declared_alpha"])
        # Reproduce the ACTUAL preserved primary from raw counts, not from a proxy score.
        log_cpm = np.log2(block / totals[None, :] * 1e6 + 1)
        standard_deviation = log_cpm.std(axis=1, ddof=1)
        z = np.divide(log_cpm - log_cpm.mean(axis=1)[:, None], standard_deviation[:, None],
                      out=np.zeros_like(log_cpm), where=standard_deviation[:, None] > 0)
        for variant, original_scores in (("standardised", z.mean(axis=0)),
                                          ("unstandardised", log_cpm.mean(axis=0))):
            saved = original["results"][f"primary1_{name}"][variant]
            close(f"{name}: preserved {variant} CPM scores", original_scores,
                  saved["case_values"] + saved["reference_values"], 5.1e-5)
            close(f"{name}: preserved {variant} CPM mean effect", original_scores[:4].mean() - original_scores[4:].mean(),
                  saved["mean_difference"], 5.1e-5)
            _, original_p = independent_test(original_scores)
            close(f"{name}: preserved {variant} CPM exact p", original_p, saved["exact_test"]["p_two_sided"], 5.1e-7)
            check(f"{name}: preserved {variant} CPM gate", (original_p <= 2 / 70 + 1e-12) ==
                  saved["separates_at_declared_alpha"])
    disagreement = {name: separated != original["results"][f"primary1_{name}"]["standardised"]["separates_at_declared_alpha"]
                    for name, separated in observed_separation.items()}
    reason = "the median-of-ratios verdict differs from the CPM verdict"
    reasons = [r for r in original["verdict"]["downgrade_reasons"] if r != reason]
    if any(disagreement.values()):
        reasons.append(reason)
    old = original["verdict"]
    positive = old["transitional_separates"] or old["identity_separates"] or old["omnibus_correlation_separates"]
    expected_verdict = ("inconclusive" if reasons else "epithelium_differs_but_does_not_discriminate" if positive
                        else "weak_bound_on_rival_2" if old["engagement_separates_in_declared_direction"]
                        else "engagement_not_established")
    check("normalization disagreement and all other gates preserved", disagreement ==
          run["decision"]["normalization_disagreement_by_panel"] and reasons == run["decision"]["downgrade_reasons"])
    check("corrected algorithmic verdict", expected_verdict == run["decision"]["corrected_algorithmic_verdict"])
    failures = [c for c in checks if not c["passed"]]
    record = {"schema": "a15-rival2-normalization-independent-verification/v1",
              "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "correction_run_sha256": digest(run_path), "verifier_script_sha256": digest(Path(__file__)),
              "numpy_version": np.__version__, "implementation_independent": True,
              "total_checks": len(checks), "failed_checks": len(failures), "checks": checks}
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"checks": len(checks), "failed": len(failures), "failures": failures}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
