"""Presentation correction only; consume frozen receptor summary without reanalysis."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
source = root / "analysis/research/runs/A12_erbb_sorted_reference_v1_20261103/receptor_summary.csv"
with source.open(newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 4
fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.8))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.18, top=0.77, wspace=0.28)
colors = ["#747f8c", "#287e8f"]
for j, (subset, label) in enumerate([("deposited", "Deposited"), ("operational_qc", "Operational QC")]):
    group = [r for r in rows if r["subset"] == subset]
    assert [r["gene"] for r in group] == ["ERBB4", "ERBB2"]
    x = [i + (j - 0.5) * 0.3 for i in range(2)]
    for ax, metric, ylabel in [(axes[0], "detection_percent", "Barcodes with at least 1 UMI (%)"),
                               (axes[1], "full_rna_cpm", "UMI per million full RNA UMIs")]:
        values = [float(r[metric]) if r[metric] else float("nan") for r in group]
        ax.bar(x, values, width=0.28, color=colors[j], label=f"{label}: {int(group[0]['n_barcodes']):,} barcodes")
        ax.set_xticks([0, 1], ["ERBB4", "ERBB2"])
        ax.set_ylabel(ylabel)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylim(bottom=0)
fig.suptitle("ERBB RNA in one fresh HTII-280-sorted preparation", y=0.96, fontsize=13)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.89), ncol=2, frameon=False, fontsize=10)
fig.text(0.5, 0.07, "GSM4522986; one library, unresolved donor identity and epithelial states", ha="center", fontsize=10)
fig.text(0.5, 0.025, "Measured RNA context does not establish receptor activity or protein co-expression", ha="center", fontsize=9)
fig.savefig(out / "erbb_sorted_rna_v2.png", dpi=180)
plt.close(fig)
print("Rendered frozen four-row summary; no count matrix reopened.")
