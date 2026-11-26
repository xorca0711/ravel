"""Render the frozen locus table and place published flow beside residual AM RNA."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("output", type=Path)
out = parser.parse_args().output
runs = Path("analysis/research/runs")
raw = Path("raw_data/pestal")
loci = pd.read_csv(runs / "pestal_regulatory_v1/markers.tsv", sep="\t", index_col="gene")
fig, (ax, peak_ax) = plt.subplots(
    1, 2, figsize=(10, 7), gridspec_kw={"width_ratios": [3, 1]}, layout="constrained"
)
columns = ["S2_author_lfc", "S3_author_lfc", "S4_author_lfc"]
values = loci[columns].to_numpy()
cm = plt.get_cmap("RdBu_r").copy()
cm.set_bad("#dddddd")
image = ax.imshow(values, cmap=cm, vmin=-17, vmax=17, aspect="auto")
ax.set_xticks(range(3), ["Transfer d7\nWT − KO", "KLF2 OE\n− empty", "GATA6 OE\n− empty"])
ax.set_yticks(range(len(loci)), loci.index)
for (i, j), value in np.ndenumerate(values):
    label = "NA" if np.isnan(value) else f"{value:+.2f}"
    ax.text(j, i, label, ha="center", va="center", color="white" if abs(value) > 10 else "black")
fig.colorbar(image, ax=ax, label="Author log2 fold change")
peak_ax.barh(range(len(loci)), loci.overlap, color="#28586a")
peak_ax.set_ylim(ax.get_ylim())
peak_ax.set_yticks([])
peak_ax.set_xlabel("Combined BED overlaps")
fig.suptitle("Transfer dependence, native KLF2 occupancy and induction")
fig.savefig(out / "loci.png", dpi=170)
plt.close(fig)

def panels(sources, labels, name):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")
    for axis, source, label in zip(axes, sources, labels):
        axis.imshow(plt.imread(source))
        axis.set_title(label)
        axis.set_axis_off()
    fig.text(0.01, 0.01, "Published panels from Pestal et al. (2025), doi:10.1084/jem.20240379, CC BY 4.0.")
    fig.savefig(out / name, dpi=180)
    plt.close(fig)

panels([raw / "jem_20240379_fig1.jpg", raw / "jem_20240379_fig2.jpg"],
       ["A. Residual cavity populations (published Fig. 1)", "B. Shared-host competition (published Fig. 2)"],
       "cavity_population.png")
panels([raw / "jem_20240379_fig7.jpg", runs / "pestal_lung_v1/markers.png"],
       ["A. Shared-host AM competition (published Fig. 7)", "B. RNA in recovered AMs (all four libraries)"],
       "lung_population_and_state.png")
