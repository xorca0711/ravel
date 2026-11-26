"""Plot marker expression from the deposited Kallisto estimated fragment counts."""
import argparse
from pathlib import Path

import h5py
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyze import MARKERS, RAW, annotation


def read_counts(libraries, genes, transcript_genes):
    columns = {}
    metadata = []
    for row in libraries.itertuples():
        sample = row.sample
        with h5py.File(RAW / f"{row.accession}_{sample}.h5", "r") as h:
            ids = h["aux/ids"].asstr()[:]
            counts = h["est_counts"][:]
        if len(ids) != len(counts) or not np.isfinite(counts).all() or (counts < 0).any():
            raise ValueError(f"Invalid estimated counts in {row.accession}")
        symbols = [transcript_genes.get(t.split(".")[0]) for t in ids]
        by_gene = pd.Series(counts).groupby(pd.Series(symbols), dropna=True).sum().reindex(genes)
        if by_gene.isna().any() or counts.sum() <= 0:
            raise ValueError(f"Missing marker or library denominator in {row.accession}")
        columns[row.accession] = by_gene
        genotype = "WT" if "WT" in sample else "KO"
        if "day0" in sample:
            group = f"Input {genotype}"
        elif "day7" in sample:
            group = f"Day 7 {genotype}"
        else:
            group = genotype
        metadata.append((row.accession, sample, group, counts.sum()))
    md = pd.DataFrame(metadata, columns=["accession", "sample", "group", "total_estimated_fragments"])
    return pd.DataFrame(columns).rename_axis("gene"), md.set_index("accession")


def plot(expression, metadata, groups, title, subtitle, output):
    nrows = (len(expression) + 2) // 3
    fig, axes = plt.subplots(nrows, 3, figsize=(10.5, 1.9 * nrows + 1.2), sharey=True)
    colors = {"WT": "#176379", "KO": "#b25128"}
    for ax, (gene, values) in zip(axes.flat, expression.iterrows(), strict=True):
        for i, group in enumerate(groups):
            points = values.loc[metadata.index[metadata.group == group]]
            offsets = np.linspace(-0.09, 0.09, len(points))
            ax.scatter(i + offsets, points, color=colors[group.split()[-1]], s=27,
                       alpha=0.85, edgecolor="white", linewidth=0.35, zorder=3)
        ax.set_title(gene, loc="left", fontstyle="italic", fontsize=12)
        ax.set_xticks(range(len(groups)), groups, fontsize=8)
        ax.set_xlim(-0.45, len(groups) - 0.55)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.18)
    fig.suptitle(title, x=0.075, y=0.985, ha="left", fontsize=16, fontweight="bold")
    fig.text(0.075, 0.936, subtitle, ha="left", fontsize=9)
    fig.supylabel("log₂(counts per million + 1)", x=0.012, fontsize=10)
    fig.subplots_adjust(top=0.84, bottom=0.065, left=0.075, right=0.985,
                        hspace=0.65, wspace=0.23)
    fig.savefig(output, dpi=165)
    plt.close(fig)


def main(output):
    genes = set(MARKERS["transfer"] + MARKERS["lung"])
    mapping = {}
    for _, attrs in annotation("GRCm38", "transcript"):
        symbol = attrs.get("gene_name")
        if symbol in genes:
            tx = attrs["transcript_id"].split(".")[0]
            if mapping.setdefault(tx, symbol) != symbol:
                raise ValueError(f"Ambiguous marker assignment for {tx}")
    source = Path("analysis/research/runs")
    metadata = []
    plot_values = []
    settings = [
        ("transfer", "cavity", ["Input WT", "Input KO", "Day 7 WT", "Day 7 KO"],
         [2, 2, 3, 2], "Cavity marker acquisition after transfer",
         "Nine RNA libraries from input or recovered macrophages  ·  WT and Klf2-deficient donors"),
        ("lung", "lung", ["WT", "KO"], [2, 2], "Marker expression in recovered alveolar macrophages",
         "Four sorted-cell RNA libraries  ·  WT and Klf4-deficient macrophages"),
    ]
    for stage, name, groups, sizes, title, subtitle in settings:
        libraries = pd.read_csv(source / f"pestal_{stage}_v1/libraries.tsv", sep="\t")
        counts, samples = read_counts(libraries, MARKERS[stage], mapping)
        if samples.group.value_counts().reindex(groups).tolist() != sizes:
            raise ValueError(f"Unexpected library groups in {stage}")
        normalized = counts.div(samples.total_estimated_fragments, axis="columns") * 1_000_000
        values = np.log2(normalized + 1)
        counts.to_csv(output / f"{name}_estimated_counts.tsv", sep="\t")
        plot_values.append(values.rename_axis(columns="accession").stack().rename(
            "log2_cpm_plus1").reset_index().assign(experiment=name))
        metadata.append(samples.assign(experiment=name))
        plot(values, samples, groups, title, subtitle, output / f"{name}_markers.png")
    pd.concat(metadata).to_csv(output / "libraries.tsv", sep="\t")
    pd.concat(plot_values).to_csv(output / "plot_values.tsv", sep="\t", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
