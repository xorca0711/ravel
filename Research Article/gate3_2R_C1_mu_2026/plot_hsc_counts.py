"""Plot frozen library-level HSC counts without recomputing the analysis."""
import argparse
import csv
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/ravel-mu-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
source = Path("analysis/research/runs/mu2026_s4_rna_v1/hsc_counts.tsv")
with source.open() as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
fig, axes = plt.subplots(2, 2, figsize=(7, 5), layout="constrained")
labels = ("Cre 1", "Cre 2", "T3 2", "T3 3")
samples = ("Mx1Cre_1", "Mx1Cre_2", "Mx1T3_2", "Mx1T3_3")
for ax, row in zip(axes.flat, rows, strict=True):
    for index, sample in enumerate(samples):
        ax.scatter(index, float(row[f"{sample}_normalized"]),
                   color="#315c82" if index < 2 else "#912e20")
    ax.set(title=row["released_gene_label"], ylabel="Normalized count", ylim=(0, None))
    ax.set_xticks(range(4), labels)
fig.suptitle("Aged HSC RNA · one point per released library")
fig.savefig(args.output / "hsc_library_counts.pdf")
