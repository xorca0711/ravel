"""Reconstruct the day-four contrast at the deposited library level."""

import argparse
import gzip
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qualify_v1 import RAW, read_counts, read_manifest, write_tsv

GTF = RAW / "Mus_musculus.GRCm38.78.gtf.gz"
ANCHORS = ("Il10", "Tgfb1", "Il2", "Tnf", "Ifng", "Prf1", "Gzmb", "Foxp3", "Ezh2")
COLORS = {"deficient": "#a24134", "wild_type": "#215e76", "flox_het": "#727d2c"}
LABELS = {"deficient": "fl/fl", "wild_type": "+/+", "flox_het": "fl/+"}


def read_symbols(genes):
    names = {}
    with gzip.open(GTF, "rt", encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if fields[2] != "gene":
                continue
            attrs = dict(re.findall(r'(\w+) "([^"]+)"', fields[8]))
            gene = attrs["gene_id"]
            if gene in genes and "gene_name" in attrs:
                if gene in names:
                    raise ValueError(f"Duplicate gene record in GTF: {gene}")
                names[gene] = attrs["gene_name"]
    return names


def median_ratio(counts):
    reference = counts[np.all(counts > 0, axis=1)]
    if not len(reference):
        raise ValueError("No positive-all-libraries normalization reference")
    ratios = reference / np.exp(np.log(reference).mean(axis=1, keepdims=True))
    factors = np.median(ratios, axis=0)
    return factors / np.exp(np.log(factors).mean()), len(reference)


def mean_ratio(values, deficient, control):
    return np.log2((values[:, deficient].mean(axis=1) + 0.5)
                   / (values[:, control].mean(axis=1) + 0.5))


def read_inputs():
    columns, raw_counts = read_counts()
    manifest = read_manifest(columns)
    genes = list(raw_counts)
    counts = np.array(list(raw_counts.values()), dtype=np.int64)
    labels = np.array([sample["group"] for sample in manifest])
    deficient = labels == "deficient"
    control = ~deficient
    wild_type = labels == "wild_type"
    if (deficient.sum(), control.sum(), wild_type.sum()) != (4, 5, 4):
        raise ValueError("Unexpected size of the deposited comparison")
    symbols = read_symbols(raw_counts)
    frequencies = Counter(symbols.values())
    unique = {symbol: i for i, gene in enumerate(genes)
              if (symbol := symbols.get(gene)) and frequencies[symbol] == 1}
    return columns, genes, counts, labels, deficient, control, wild_type, symbols, frequencies, unique


def main(output):
    (columns, genes, counts, labels, deficient, control, wild_type,
     symbols, frequencies, unique) = read_inputs()
    factors, reference_count = median_ratio(counts)
    normalized = counts / factors
    eligible = (counts >= 10).sum(axis=1) >= 4
    pooled = mean_ratio(normalized, deficient, control)
    strict = mean_ratio(normalized, deficient, wild_type)
    rows = []
    for i, gene in enumerate(genes):
        symbol = symbols.get(gene, "")
        mapping = "missing" if not symbol else (
            "unique" if frequencies[symbol] == 1 else "ambiguous")
        status = "eligible" if eligible[i] else (
            "all_zero" if not counts[i].any() else "low_count")
        rows.append(dict(
            ensembl_id=gene, symbol=symbol, mapping=mapping, count_status=status,
            pooled_control_log2_mean_ratio=pooled[i] if status != "all_zero" else "",
            strict_wt_log2_mean_ratio=strict[i] if status != "all_zero" else "",
            **{f"raw_{name}": counts[i, j] for j, name in enumerate(columns)},
        ))
    write_tsv(output / "complete_contrast.tsv", rows)
    anchors = []
    for name in ANCHORS:
        if name not in unique:
            raise ValueError(f"Published anchor cannot be uniquely mapped: {name}")
        i = unique[name]
        anchors.append(rows[i] | {
            f"normalized_{column}": normalized[i, j] for j, column in enumerate(columns)
        })
    write_tsv(output / "anchor_values.tsv", anchors)

    matrix = np.log2(normalized[eligible].T + 1)
    left, singular, _ = np.linalg.svd(matrix - matrix.mean(axis=0), full_matrices=False)
    for j in range(2):
        pivot = np.abs(left[:, j]).argmax()
        left[:, j] *= np.sign(left[pivot, j])
    scores = left[:, :2] * singular[:2]
    variance = singular**2 / (singular**2).sum()
    write_tsv(output / "library_coordinates.tsv", [
        dict(column=name, group=labels[i], factor=factors[i],
             library_total=counts[:, i].sum(), PC1=scores[i, 0], PC2=scores[i, 1])
        for i, name in enumerate(columns)
    ])
    summary = dict(rows=len(genes), count_status=dict(Counter(r["count_status"] for r in rows)),
                   mapping=dict(Counter(r["mapping"] for r in rows)),
                   reference_genes=reference_count, variance_PC1_PC2=variance[:2].tolist())
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for group, color in COLORS.items():
        keep = labels == group
        axes[0].scatter(*scores[keep].T, color=color, label=LABELS[group], zorder=3)
    for i, name in enumerate(columns):
        axes[0].annotate(name[3:], scores[i], xytext=(4, 3), textcoords="offset points", fontsize=8)
    axes[0].margins(0.18)
    axes[0].set(xlabel=f"PC1 ({variance[0]:.1%})", ylabel=f"PC2 ({variance[1]:.1%})",
                title="Deposited libraries")
    axes[0].legend(frameon=False)
    axes[1].scatter(np.log10(normalized[eligible].mean(axis=1) + 0.5), pooled[eligible],
                    s=6, alpha=0.24, color="#215e76", edgecolors="none")
    axes[1].axhline(0, color="#474747", linewidth=0.8)
    axes[1].set(xlabel="log10 mean normalized reads + 0.5",
                ylabel="log2 deficient / pooled control", title="Rank-eligible gene contrasts")
    fig.savefig(output / "library_overview.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(3, 3, figsize=(9.5, 8), layout="constrained", sharex=True)
    order = ("wild_type", "flox_het", "deficient")
    for axis, name in zip(axes.flat, ANCHORS, strict=True):
        i = unique[name]
        for j, group in enumerate(order):
            y = normalized[i, labels == group]
            x = j + (np.linspace(-0.12, 0.12, len(y)) if len(y) > 1 else np.zeros(1))
            axis.scatter(x, y, color=COLORS[group], s=27, zorder=3)
            axis.hlines(y.mean(), j - 0.18, j + 0.18, color=COLORS[group], alpha=0.6)
        axis.set(title=name, xticks=range(3), xticklabels=[LABELS[g] for g in order])
    fig.supylabel("Median-ratio normalized reads")
    fig.savefig(output / "anchor_libraries.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
