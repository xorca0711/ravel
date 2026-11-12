"""Compare Wang's frozen descriptive Hallmark scores with Signal2Noise ranks."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from breadth_v1 import S2, enrichment, rank, read_sets
from describe_v1 import plt, write_tsv

RUNS = Path("analysis/research/runs")
MANIFEST = RUNS / "wang18_s1_qualification_v1/sample_manifest.tsv"
FACTORS = S2.with_name("library_coordinates.tsv")
S3 = RUNS / "wang18_s3_breadth_v1/hallmark_scores.tsv"
LABELS = {
    "TNFA_SIGNALING_VIA_NFKB": "TNF via NF-κB",
    "INFLAMMATORY_RESPONSE": "Inflammatory response",
    "INTERFERON_GAMMA_RESPONSE": "Interferon-γ response",
    "IL2_STAT5_SIGNALING": "IL-2 / STAT5",
    "E2F_TARGETS": "E2F targets",
    "G2M_CHECKPOINT": "G2/M checkpoint",
    "APOPTOSIS": "Apoptosis",
    "UNFOLDED_PROTEIN_RESPONSE": "Unfolded protein response",
}


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def signal2noise(normalized, deficient, control):
    """Use GSEA v3.0's mean-based metric with unbiased variance and the floor on."""
    if min(deficient.sum(), control.sum()) < 3:
        raise ValueError("Signal2Noise requires at least three libraries per group")
    if np.any(deficient & control):
        raise ValueError("Signal2Noise groups must be disjoint")
    ko, ref = normalized[:, deficient], normalized[:, control]
    ko_mean, ref_mean = ko.mean(axis=1), ref.mean(axis=1)
    means = np.stack((ko_mean, ref_mean))
    standard_deviations = np.stack((ko.std(axis=1, ddof=1), ref.std(axis=1, ddof=1)))
    floor = 0.20 * np.abs(means)
    denominator = np.maximum(standard_deviations, np.where(floor == 0, 0.20, floor)).sum(axis=0)
    scores = (ko_mean - ref_mean) / denominator
    if not np.isfinite(scores).all():
        raise ValueError("Nonfinite Signal2Noise statistic")
    return scores


def library_inputs():
    manifest, factors = read_tsv(MANIFEST), read_tsv(FACTORS)
    columns = [row["column"] for row in manifest]
    labels = [row["group"] for row in manifest]
    if ([(row["column"], row["group"]) for row in factors] != list(zip(columns, labels))
            or len(set(columns)) != len(columns)):
        raise ValueError("S1 manifest and S2 factors differ")
    size_factors = np.array([float(row["factor"]) for row in factors])
    if not (np.isfinite(size_factors).all() and (size_factors > 0).all()):
        raise ValueError("Invalid frozen size factors")
    labels = np.array(labels)
    deficient, wild_type = labels == "deficient", labels == "wild_type"
    if (deficient.sum(), wild_type.sum(), (labels == "flox_het").sum(), len(labels)) != (4, 4, 1, 9):
        raise ValueError("Unexpected deposited genotype groups")
    rows = [row for row in read_tsv(S2) if row["count_status"] == "eligible"
            and row["mapping"] == "unique"]
    ids = np.array([row["ensembl_id"] for row in rows])
    symbols = [row["symbol"] for row in rows]
    if len(set(ids)) != len(ids) or len(set(symbols)) != len(symbols) or "" in symbols:
        raise ValueError("Frozen ranked universe does not have unique identifiers")
    counts = np.array([[int(row[f"raw_{column}"]) for column in columns] for row in rows])
    if (counts < 0).any() or ((counts >= 10).sum(axis=1) < 4).any():
        raise ValueError("Frozen rank-eligible counts are inconsistent")
    return columns, deficient, wild_type, ids, symbols, counts / size_factors


def rankings(columns, deficient, wild_type, ids, normalized):
    configs = {}
    for key, control in (("pooled", ~deficient), ("strict_wt", wild_type)):
        configs[key] = (deficient, control)
        for j in np.flatnonzero(deficient | control):
            keep = np.arange(len(columns)) != j
            configs[f"{key}_omit_{columns[j]}"] = (deficient & keep, control & keep)
    universe = np.arange(len(ids))
    scores_and_order, diagnostics = {}, {}
    for key, (case, control) in configs.items():
        scores = signal2noise(normalized, case, control)
        scores_and_order[key] = scores, rank(scores, ids, universe)
        _, multiplicities = np.unique(scores, return_counts=True)
        diagnostics[key] = {
            "deficient_libraries": int(case.sum()),
            "control_libraries": int(control.sum()),
            "genes_in_exact_ties": int(multiplicities[multiplicities > 1].sum()),
            "largest_tie": int(multiplicities.max()),
        }
    return scores_and_order, diagnostics


def score_hallmarks(symbols, rankings_by_group):
    baseline = {row["hallmark"]: row for row in read_tsv(S3)}
    gene_sets = read_sets()
    if len(gene_sets) != 50 or gene_sets.keys() != baseline.keys():
        raise ValueError("S3 and F2 Hallmark inventories differ")
    index = {symbol: i for i, symbol in enumerate(symbols)}
    rows = []
    for name, members in gene_sets.items():
        old = baseline[name]
        covered = members.intersection(index)
        hits = [index[symbol] for symbol in sorted(covered)]
        if (int(old["ranked_universe"]), int(old["total_members"]), int(old["covered"]),
                old["missing_or_unranked"]) != (len(index), len(members), len(hits),
                                                ";".join(sorted(members - covered))):
            raise ValueError(f"Frozen S3 coverage differs for {name}")
        row = {key: old[key] for key in ("hallmark", "total_members", "covered",
                                         "ranked_universe", "missing_or_unranked")}
        eligible = 10 <= len(hits) < len(index)
        row["status"] = "scored" if eligible else "insufficient_coverage"
        for field in ("ES_primary", "ES_strict_wt", "omit_library_min", "omit_library_max"):
            row[f"s3_{field}"] = old[field]
        for key, (scores, ordered) in rankings_by_group.items():
            if eligible:
                score, leading, _ = enrichment(scores, ordered, hits)
                row[f"signal2noise_{key}"] = score
                if key in ("pooled", "strict_wt"):
                    row[f"leading_signal2noise_{key}"] = ";".join(symbols[i] for i in leading)
            else:
                row[f"signal2noise_{key}"] = ""
                if key in ("pooled", "strict_wt"):
                    row[f"leading_signal2noise_{key}"] = ""
        for key in ("pooled", "strict_wt"):
            omission = [row[f"signal2noise_{label}"] for label in rankings_by_group
                        if label.startswith(f"{key}_omit_")]
            row[f"signal2noise_{key}_omit_min"] = min(omission)
            row[f"signal2noise_{key}_omit_max"] = max(omission)
        rows.append(row)
    return rows


def draw_comparison(output, rows):
    by_set = {row["hallmark"]: row for row in rows}
    fig, axes = plt.subplots(ncols=2, figsize=(10.4, 5.2), sharex=True,
                             sharey=True, layout="constrained")
    panels = (
        ("S3 log₂ mean ratio", "s3_ES_primary", "s3_ES_strict_wt",
         "s3_omit_library_min", "s3_omit_library_max"),
        ("F2 Signal2Noise", "signal2noise_pooled", "signal2noise_strict_wt",
         "signal2noise_pooled_omit_min", "signal2noise_pooled_omit_max"),
    )
    for axis, (title, pooled, strict, low, high) in zip(axes, panels, strict=True):
        for i, name in enumerate(LABELS):
            row = by_set[name]
            if row["status"] != "scored":
                continue
            axis.hlines(i, float(row[low]), float(row[high]), color="#777777", linewidth=1.4)
            axis.scatter(float(row[pooled]), i, color="#215e76", s=34, zorder=3,
                         label="Pooled controls" if i == 0 else None)
            axis.scatter(float(row[strict]), i, facecolor="white", edgecolor="#a24134",
                         marker="D", s=30, zorder=4, label="+/+ controls" if i == 0 else None)
        axis.axvline(0, color="#777777", linewidth=0.8)
        axis.set(title=title, xlabel="Descriptive enrichment score", yticks=range(len(LABELS)),
                 yticklabels=list(LABELS.values()))
    axes[0].invert_yaxis()
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.26), ncol=2, frameon=False)
    fig.savefig(output / "signal2noise_overview.png", dpi=180)
    plt.close(fig)


def main(output):
    columns, deficient, wild_type, ids, symbols, normalized = library_inputs()
    scores, diagnostics = rankings(columns, deficient, wild_type, ids, normalized)
    rows = score_hallmarks(symbols, scores)
    write_tsv(output / "hallmark_signal2noise.tsv", rows)
    (output / "ranking_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8")
    draw_comparison(output, rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
