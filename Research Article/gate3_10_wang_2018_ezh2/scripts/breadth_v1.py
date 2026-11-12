"""Describe Hallmark rank patterns and leverage of the deposited libraries."""

import argparse
import csv
from pathlib import Path

import numpy as np

from describe_v1 import (ANCHORS, RAW, mean_ratio, median_ratio, plt, read_inputs,
                         write_tsv)

GMT = RAW / "mh.all.v2025.1.Mm.symbols.gmt"
S2 = Path("analysis/research/runs/wang18_s2_library_description_v1/complete_contrast.tsv")
HIGHLIGHTS = (
    "TNFA_SIGNALING_VIA_NFKB", "INFLAMMATORY_RESPONSE", "INTERFERON_GAMMA_RESPONSE",
    "IL2_STAT5_SIGNALING", "E2F_TARGETS", "G2M_CHECKPOINT", "APOPTOSIS",
    "UNFOLDED_PROTEIN_RESPONSE",
)


def rank(values, stable_ids, indices):
    return indices[np.lexsort((stable_ids[indices], -values[indices]))]


def enrichment(values, ordered, indices):
    hits = np.isin(ordered, indices)
    weights = np.abs(values[ordered[hits]])
    if weights.sum() == 0:
        weights = np.ones(len(weights))
    steps = np.full(len(ordered), -1 / (~hits).sum())
    steps[hits] = weights / weights.sum()
    walk = np.cumsum(steps)
    pivot = np.abs(walk).argmax()
    leading = np.arange(len(ordered)) <= pivot
    if walk[pivot] < 0:
        leading = ~leading
    return walk[pivot], ordered[hits & leading], walk


def read_sets():
    sets = {}
    with GMT.open(encoding="utf-8") as source:
        for line in source:
            name, _, *members = line.rstrip("\n").split("\t")
            short = name.removeprefix("HALLMARK_")
            if short in sets or len(members) != len(set(members)):
                raise ValueError(f"Duplicate gene-set name or member: {name}")
            sets[short] = set(members)
    if not set(HIGHLIGHTS) <= sets.keys():
        raise ValueError("Expected Hallmarks are missing")
    return sets


def main(output):
    (columns, genes, counts, _, deficient, control, wild_type,
     symbols, _, unique) = read_inputs()
    eligible = (counts >= 10).sum(axis=1) >= 4
    factors, _ = median_ratio(counts)
    normalized = counts / factors
    pooled = mean_ratio(normalized, deficient, control)
    strict = mean_ratio(normalized, deficient, wild_type)
    with S2.open(encoding="utf-8", newline="") as stream:
        s2 = list(csv.DictReader(stream, delimiter="\t"))
    if ([row["ensembl_id"] for row in s2] != genes
            or [row["count_status"] == "eligible" for row in s2] != eligible.tolist()
            or not np.array_equal(
                [float(row["pooled_control_log2_mean_ratio"])
                 for row in s2 if row["count_status"] == "eligible"], pooled[eligible])):
        raise ValueError("S2 contrast or eligible universe does not match")

    log_reads = np.log2(normalized + 1)
    log_mean_delta = log_reads[:, deficient].mean(axis=1) - log_reads[:, control].mean(axis=1)
    totals = counts.sum(axis=0)
    depth_scaled = counts / totals * np.exp(np.log(totals).mean())
    depth_ratio = mean_ratio(depth_scaled, deficient, control)
    without = np.arange(len(columns))[:, None] != np.arange(len(columns))
    dropped = [mean_ratio(normalized, deficient & keep, control & keep) for keep in without]
    ranks = dict(primary=pooled, log_mean_delta=log_mean_delta, strict_wt=strict,
                 depth_scaled=depth_ratio)
    stable = np.array(genes)
    indices = np.array(sorted(i for i in unique.values() if eligible[i]))
    order = {key: rank(values, stable, indices) for key, values in ranks.items()}
    drop_orders = [rank(values, stable, indices) for values in dropped]

    leverage = []
    anchors = {unique[name] for name in ANCHORS}
    for i in np.flatnonzero(eligible | np.isin(np.arange(len(genes)), list(anchors))):
        deletions = [values[i] for values in dropped]
        leverage.append(dict(
            ensembl_id=genes[i], symbol=symbols.get(genes[i], ""),
            eligible=int(eligible[i]), primary=pooled[i], strict_wt=strict[i],
            depth_scaled=depth_ratio[i], log_mean_delta=log_mean_delta[i],
            omit_library_min=min(deletions), omit_library_max=max(deletions),
            **{f"omit_{name}": deletions[j] for j, name in enumerate(columns)},
        ))
    write_tsv(output / "gene_sensitivity.tsv", leverage)

    rows, walks = [], {}
    for name, members in read_sets().items():
        covered = {gene for gene in members if gene in unique and eligible[unique[gene]]}
        hits = [unique[gene] for gene in sorted(covered)]
        row = dict(hallmark=name, total_members=len(members), covered=len(hits),
                   ranked_universe=len(indices), missing_or_unranked=";".join(sorted(members - covered)))
        if 10 <= len(hits) < len(indices):
            for key, values in ranks.items():
                score, leading, walk = enrichment(values, order[key], hits)
                row[f"ES_{key}"] = score
                row[f"leading_{key}"] = ";".join(symbols[genes[i]] for i in leading)
                if key == "primary":
                    walks[name] = walk
            deletions = [enrichment(values, ranked, hits)[0]
                         for values, ranked in zip(dropped, drop_orders, strict=True)]
            row.update(omit_library_min=min(deletions), omit_library_max=max(deletions))
        rows.append(row)
    all_columns = dict.fromkeys(key for row in rows for key in row)
    rows = [{key: row.get(key, "") for key in all_columns} for row in rows]
    write_tsv(output / "hallmark_scores.tsv", rows)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout="constrained",
                            gridspec_kw={"width_ratios": (1, 1.25)})
    for name, color in zip(HIGHLIGHTS[:2], ("#a24134", "#215e76"), strict=True):
        if name in walks:
            label = {"TNFA_SIGNALING_VIA_NFKB": "TNF via NF-κB",
                     "INFLAMMATORY_RESPONSE": "Inflammatory response"}[name]
            axes[0].plot(np.linspace(0, 100, len(indices)), walks[name], label=label, color=color)
    axes[0].axhline(0, color="#474747", linewidth=0.8)
    axes[0].set(xlabel="Rank percentile (highest deficient / control first)",
                ylabel="Weighted running sum", title="Published S3B themes")
    axes[0].legend(frameon=False)

    highlights = [next(row for row in rows if row["hallmark"] == name) for name in HIGHLIGHTS]
    names = [row["hallmark"].replace("_", " ").capitalize() for row in highlights]
    for i, row in enumerate(highlights):
        if row["ES_primary"] != "":
            axes[1].hlines(i, row["omit_library_min"], row["omit_library_max"], color="#767676")
            axes[1].scatter(row["ES_primary"], i, color="#215e76", zorder=3,
                            label="Pooled control" if i == 0 else None)
            axes[1].scatter(row["ES_strict_wt"], i, color="#a24134", marker="D", zorder=3,
                            label="+/+ only" if i == 0 else None)
    axes[1].axvline(0, color="#474747", linewidth=0.8)
    axes[1].set(yticks=range(len(names)), yticklabels=names, xlabel="Descriptive enrichment score",
                title="Selected sets and one-library omission range")
    axes[1].invert_yaxis()
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.21), ncol=2, frameon=False)
    fig.savefig(output / "hallmark_patterns.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
