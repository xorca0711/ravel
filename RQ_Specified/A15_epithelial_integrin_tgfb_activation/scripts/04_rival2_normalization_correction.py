"""Versioned A15 MOR repair; preserves frozen v3 results. Standard library only."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import itertools
import json
import math
import statistics as st
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
SPEC = HERE / "config/a15_rival2_normalization_correction_v1.json"
SPEC_MD = HERE / "reports/NORMALIZATION_CORRECTION_SPEC_V1.md"
ORIGINAL = HERE / "tables/rival2/stage3_execute_run.json"
JOIN = HERE / "tables/rival2/stage1_join.tsv"
MOR_REASON = "the median-of-ratios verdict differs from the CPM verdict"


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def refuse_existing_output(path):
    if Path(path).exists():
        raise FileExistsError(f"refusing existing output directory: {path}")


def verify_checkpoint(commit):
    resolved = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{commit}^{{commit}}"], cwd=ROOT, text=True
    ).strip()
    for path in (SPEC, SPEC_MD):
        committed = subprocess.check_output(
            ["git", "show", f"{resolved}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT)
        require(committed == path.read_bytes(), f"specification differs from checkpoint: {path}")
    return resolved


def median_ratio_factors(matrix, excluded_ids=(), minimum_reference_genes=1):
    """All-positive broad reference; arithmetic ratio medians, geometric centering."""
    excluded = set(excluded_ids)
    reference = sorted(g for g, values in matrix.items()
                       if g not in excluded and all(v > 0 for v in values))
    require(len(reference) >= minimum_reference_genes, "insufficient independent reference genes")
    n = len(matrix[reference[0]])
    require(all(len(v) == n for v in matrix.values()), "inconsistent library dimension")
    log_means = {g: st.fmean(math.log(v) for v in matrix[g]) for g in reference}
    raw = [st.median(math.exp(math.log(matrix[g][j]) - log_means[g]) for g in reference)
           for j in range(n)]
    center = math.exp(st.fmean(math.log(v) for v in raw))
    return [v / center for v in raw], reference


def panel_scores(matrix, members, factors):
    return [st.fmean(math.log2(matrix[g][j] / factor + 1) for g in members)
            for j, factor in enumerate(factors)]


def u_statistic(a, b):
    return sum((x > y) + 0.5 * (x == y) for x in a for y in b)


def contrast(scores, alpha=2 / 70):
    require(len(scores) == 8, "correction contrast requires exactly eight scores")
    case, reference = scores[:4], scores[4:]
    observed = u_statistic(case, reference)
    permuted = []
    for chosen in itertools.combinations(range(8), 4):
        chosen_set = set(chosen)
        permuted.append(u_statistic([scores[i] for i in chosen],
                                    [scores[i] for i in range(8) if i not in chosen_set]))
    low = sum(v <= observed for v in permuted) / len(permuted)
    high = sum(v >= observed for v in permuted) / len(permuted)
    p = min(1.0, 2 * min(low, high))
    shifts = [a - b for a in case for b in reference]
    return {
        "case_values": case, "reference_values": reference,
        "mean_difference": st.fmean(case) - st.fmean(reference),
        "exact_test": {"u": observed, "assignments": len(permuted),
                       "p_one_sided_lower": low, "p_one_sided_upper": high, "p_two_sided": p},
        "shift": {"estimate": st.median(shifts), "lower": min(shifts), "upper": max(shifts),
                  "attained_coverage": 68 / 70, "pairwise_differences_case_major": shifts},
        "separates_at_declared_alpha": p <= alpha + 1e-12,
    }


def updated_decision(original, corrected):
    panels = ("transitional", "identity")
    primary = {name: original["results"][f"primary1_{name}"]["standardised"] for name in panels}
    disagreement = {name: corrected[name]["separates_at_declared_alpha"] !=
                    primary[name]["separates_at_declared_alpha"] for name in panels}
    reasons = [r for r in original["verdict"]["downgrade_reasons"] if r != MOR_REASON]
    if any(disagreement.values()):
        reasons.append(MOR_REASON)
    old = original["verdict"]
    if reasons:
        value = "inconclusive"
    elif old["transitional_separates"] or old["identity_separates"] or old["omnibus_correlation_separates"]:
        value = "epithelium_differs_but_does_not_discriminate"
    elif old["engagement_separates_in_declared_direction"]:
        value = "weak_bound_on_rival_2"
    else:
        value = "engagement_not_established"
    return {"original_algorithmic_verdict": old["value"], "corrected_algorithmic_verdict": value,
            "changed": value != old["value"], "normalization_disagreement_by_panel": disagreement,
            "downgrade_reasons": reasons,
            "interpretation": "historical algorithmic label only; epithelial mediation unresolved; parent test blocked"}


def write_tsv(path, fields, rows):
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--freeze-commit", required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    refuse_existing_output(out)
    checkpoint = verify_checkpoint(args.freeze_commit)
    spec = read_json(SPEC)
    original = read_json(ORIGINAL)
    source_paths = {key: args.data_root.resolve() / rel
                    for key, rel in spec["data_paths_relative_to_data_root"].items()}
    source_paths.update(original_freeze=HERE / "config/a15_rival2_freeze_v3.json",
                        original_run=ORIGINAL, original_join=JOIN,
                        original_script=HERE / "scripts/02_rival2_execute.py")
    input_hashes = {key: sha256(path) for key, path in source_paths.items()}
    for key, value in input_hashes.items():
        require(value == spec["sha256"][key], f"input hash mismatch: {key}")
    freeze = read_json(source_paths["original_freeze"])
    original_panels = freeze["endpoints"]["primary_1_epithelial_identity_and_state"]["composites"]
    require({k: v["genes"] for k, v in original_panels.items()} == spec["panels"], "panel changed")
    join = list(csv.DictReader(JOIN.read_text(encoding="utf-8-sig").splitlines(), delimiter="\t"))
    arms = original["arms"]["epithelium"]
    sample_rows = []
    for arm in ("case", "reference"):
        declared = spec[f"{arm}_mice"]
        require([r["mouse"] for r in arms[arm]] == declared, f"original {arm} mouse IDs changed")
        for mouse in declared:
            candidates = [r for r in join if r["mouse"] == mouse and r["compartment"] == spec["compartment"]]
            require(len(candidates) == 1, f"mouse does not have exactly one epithelial row: {mouse}")
            row = candidates[0]
            for key in ("exposure", "batch"):
                require(row[key] == spec[key], f"{mouse}: {key} changed")
            require(row["treatment"] == spec[f"{arm}_treatment"], f"{mouse}: treatment changed")
            saved = next(r for r in arms[arm] if r["mouse"] == mouse)
            require(row["counts_column"] == saved["column"] and row["gsm"] == saved["gsm"], "join changed")
            sample_rows.append({"arm": arm, "mouse": mouse, "column": row["counts_column"]})
    columns = [r["column"] for r in sample_rows]
    require(len(set(columns)) == 8, "nonunique count columns")
    lookup = read_json(source_paths["symbol_map"])["records"]
    excluded_symbols = spec["reference_universe"]["excluded_symbols"]
    require(all(isinstance(lookup.get(s), dict) and lookup[s].get("id") for s in excluded_symbols),
            "unmapped required symbol")
    ids = {symbol: lookup[symbol]["id"] for symbol in excluded_symbols}
    require(len(set(ids.values())) == len(ids), "required symbols do not map one-to-one")
    matrix = {}
    totals = [0] * 8
    with gzip.open(source_paths["counts"], "rt", encoding="utf-8") as stream:
        reader = csv.reader(stream)
        header = next(reader)
        require(all(header.count(c) == 1 for c in columns), "missing or duplicate selected column")
        positions = [header.index(c) for c in columns]
        for row in reader:
            if not row:
                continue
            gene = row[0]
            require(gene not in matrix, f"duplicate count gene: {gene}")
            values = [int(row[i]) for i in positions]
            require(all(v >= 0 for v in values), f"negative count: {gene}")
            matrix[gene] = values
            totals = [a + b for a, b in zip(totals, values)]
    require(len(matrix) == spec["expected_count_rows"], "count row number changed")
    require(all(g in matrix for g in ids.values()), "required gene missing in counts")
    require(all(totals[j] == original["library_totals"][c] for j, c in enumerate(columns)),
            "library total differs from original")
    factors, reference = median_ratio_factors(
        matrix, ids.values(), spec["reference_universe"]["minimum_reference_genes"])
    results, score_rows, gene_rows = {}, [], []
    for name, symbols in spec["panels"].items():
        keep = [s for s in symbols if st.median(matrix[ids[s]]) >= spec["minimum_median_raw_count"]]
        expected = original["results"][f"primary1_{name}"]["standardised"]["coverage"]
        require(keep == expected["measurable_symbols"], f"{name}: original coverage changed")
        require(len(keep) >= spec["minimum_panel_fraction"] * len(symbols), f"{name}: coverage refused")
        scores = panel_scores(matrix, [ids[s] for s in keep], factors)
        results[name] = contrast(scores, spec["alpha_numerator"] / spec["alpha_denominator"])
        results[name]["coverage"] = {"declared": len(symbols), "measurable": len(keep), "symbols": keep}
        for j, sample in enumerate(sample_rows):
            score_rows.append({"panel": name, **sample, "score": scores[j]})
            for symbol in keep:
                raw = matrix[ids[symbol]][j]
                gene_rows.append({"panel": name, "symbol": symbol, "ensembl_id": ids[symbol],
                                  **sample, "raw_count": raw, "normalized_count": raw / factors[j],
                                  "log2_normalized_count_plus_1": math.log2(raw / factors[j] + 1)})
    record = {
        "schema": "a15-rival2-normalization-correction/v1", "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "freeze_commit": checkpoint, "specification_sha256": sha256(SPEC),
        "specification_markdown_sha256": sha256(SPEC_MD), "execution_script_sha256": sha256(Path(__file__)),
        "inputs": {key: {"path": str(path), "sha256": input_hashes[key]} for key, path in source_paths.items()},
        "samples_case_then_reference": sample_rows, "count_rows": len(matrix),
        "reference_gene_count": len(reference), "excluded_symbol_ids": ids,
        "library_totals": dict(zip(columns, totals)), "size_factors": dict(zip(columns, factors)),
        "score_unit": spec["score_unit"], "declared_alpha": 2 / 70, "corrected_sensitivity": results,
        "saved_original_comparison": {name: {
            "primary_standardized_CPM": original["results"][f"primary1_{name}"]["standardised"],
            "unstandardized_CPM": original["results"][f"primary1_{name}"]["unstandardised"],
            "withdrawn_defective_sensitivity": original["results"]["sensitivity_median_of_ratios"][name]}
            for name in spec["panels"]},
        "decision": updated_decision(original, results), "primary_files_replaced": False,
        "new_exploratory_panels": False, "claim_rows_added": 0, "register_grades_changed": False,
        "parent_test_remains_blocked": True,
    }
    out.mkdir(parents=True, exist_ok=False)
    write_tsv(out / "reference_genes.tsv", ["ensembl_id"], ({"ensembl_id": g} for g in reference))
    write_tsv(out / "size_factors.tsv", ["arm", "mouse", "column", "library_total", "size_factor"],
              ({**s, "library_total": totals[j], "size_factor": factors[j]} for j, s in enumerate(sample_rows)))
    write_tsv(out / "panel_scores.tsv", ["panel", "arm", "mouse", "column", "score"], score_rows)
    write_tsv(out / "per_gene_scores.tsv", list(gene_rows[0]), gene_rows)
    record["output_sha256"] = {p.name: sha256(p) for p in sorted(out.glob("*.tsv"))}
    with (out / "correction_run.json").open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"reference_genes": len(reference), "panels": {
        name: {"mean_difference": r["mean_difference"], "p": r["exact_test"]["p_two_sided"],
               "shift": {k: r["shift"][k] for k in ("estimate", "lower", "upper")}}
        for name, r in results.items()}, "decision": record["decision"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
