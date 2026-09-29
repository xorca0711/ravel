#!/usr/bin/env python
"""Render four presentation revisions from saved unit/cell tables, without fits."""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "figure_revision_20260929"
LINEAGES = ["Endothelium", "Mesenchyme", "Epithelium", "Myeloid", "Lymphoid"]
COLORS = ["#3b82ad", "#df5257", "#f08b2a", "#9370b6", "#4da25d"]
DAYS = [0, 6, 11, 19, 25, 42, 90, 366]


def strip(ax, data, value, days, color, key="day", hollow=False, median=True):
    for i, day in enumerate(days):
        part = data[data[key].eq(day)].sort_values("sample_id")
        offsets = np.linspace(-.10, .10, len(part)) if len(part) > 1 else np.zeros(len(part))
        ax.scatter(i + offsets, part[value], s=22, edgecolors=color,
                   facecolors="none" if hollow else color, alpha=.8)
    if median:
        med = data.groupby(key)[value].median().reindex(days)
        ax.plot(range(len(days)), med, color=color, alpha=.65, lw=1.3)
    ax.set_xticks(range(len(days)), [str(d) for d in days], fontsize=8)
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(bottom=0)


def save(fig, name):
    fig.savefig(OUT / (name + ".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    phase = HERE / "phase_timecourse/tables"
    inputs = [phase / "lineage_composition_per_animal.csv",
              phase / "traced_fraction_per_animal.csv", phase / "cycling_fraction_per_animal.csv",
              HERE / "regeneration_focus/tables/alveolar_cell_metadata.csv"]
    composition, trace, cycle, metadata = [pd.read_csv(p) for p in inputs]
    for table, keys in [(composition, ["sample_id", "lineage"]),
                        (trace, ["sample_id", "lineage"]), (cycle, ["sample_id", "lineage"])]:
        assert not table.duplicated(keys).any()
    fig, axes = plt.subplots(2, 5, figsize=(16, 6.8), constrained_layout=True)
    for j, (lineage, color) in enumerate(zip(LINEAGES, COLORS)):
        part = composition[composition.lineage.eq(lineage)]
        for i, column in enumerate(["pct_of_all_cells", "pct_within_compartment"]):
            strip(axes[i, j], part, column, DAYS, color)
        axes[0, j].set_title(lineage + "\n% of all cells (sort-engineered)", fontsize=9)
        compartment = "CD45-negative" if j < 3 else "CD45-positive"
        axes[1, j].set_title("% of " + compartment + " cells", fontsize=9)
        axes[1, j].set_xlabel("Days post infection\n(categorical spacing)", fontsize=8)
    axes[0, 0].set_ylabel("% per animal")
    axes[1, 0].set_ylabel("% per animal")
    fig.suptitle("Lineage composition | one dot per animal; lines connect group medians\nDifferent animals contribute at different days. The top-row composition is set by MACS recombination.", fontsize=11)
    save(fig, "lineage_composition_by_dpi")

    fig, axes = plt.subplots(2, 5, figsize=(16, 6.8), constrained_layout=True)
    for j, (lineage, color) in enumerate(zip(LINEAGES, COLORS)):
        part = trace[trace.lineage.eq(lineage) & trace.series.isin(["immediate_window", "baseline"])]
        strip(axes[0, j], part, "pct_traced", DAYS[:5], color)
        strip(axes[1, j], cycle[cycle.lineage.eq(lineage)], "pct_cycling", DAYS, color)
        axes[0, j].set_title(lineage + "\nKi67-traced, immediate window", fontsize=9)
        axes[0, j].set_xlabel("Harvest day, categorical spacing\n(tamoxifen 4 d earlier; 0 = uninjured)", fontsize=7)
        axes[1, j].set_title("Cells assigned S or G2M", fontsize=9)
        axes[1, j].set_xlabel("Days post infection\n(categorical spacing)", fontsize=8)
    axes[0, 0].set_ylabel("% traced of reporter-scored cells")
    axes[1, 0].set_ylabel("% cycling per animal")
    fig.suptitle("Proliferation by lineage | one dot per animal; lines connect group medians\nThese are cross-sectional groups, not repeated measurements of the same animals.", fontsize=11)
    save(fig, "proliferation_by_lineage")

    fig, axes = plt.subplots(1, 5, figsize=(16, 3.8), constrained_layout=True)
    for ax, lineage, color in zip(axes, LINEAGES, COLORS):
        part = trace[trace.lineage.eq(lineage)]
        strip(ax, part[part.day.eq(42)], "pct_traced", [2, 7, 14, 21], color, key="tam")
        strip(ax, part[part.day.eq(90)], "pct_traced", [2, 7, 14, 21], color, key="tam", hollow=True, median=False)
        ax.set_title(lineage, fontsize=10)
        ax.set_xlabel("Tamoxifen window start (dpi)\n(categorical spacing)", fontsize=8)
    axes[0].set_ylabel("% traced of reporter-scored cells")
    fig.suptitle("Trace at a common harvest | one dot per animal\nFilled: 42 dpi; open: 90 dpi. Lines connect 42-dpi group medians, not individual trajectories.", fontsize=11)
    save(fig, "traced_fraction_at_common_harvest_by_window")

    # Original Scanpy DPT coordinates were float32. Preserve that precision and
    # its tie ordering when replaying the existing rolling-mean display.
    pt = metadata.dpt_pseudotime.to_numpy(dtype=np.float32)
    ok = np.isfinite(pt)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)
    order = np.argsort(pt[ok])
    for column, color, label in [("AT2_score", "#4C72B0", "AT2"),
                                  ("transitional_score", "#C44E52", "Transitional (Krt8+)"),
                                  ("AT1_score", "#55A868", "AT1")]:
        score = metadata[column].to_numpy()[ok][order]
        smooth = pd.Series(score).rolling(max(25, len(score)//40), center=True, min_periods=1).mean()
        axes[0].plot(pt[ok][order], smooth, color=color, label=label)
    axes[0].set(xlabel="Diffusion pseudotime (rank order; no elapsed-time units)", ylabel="Module score (rolling mean)", title="Program scores along saved pseudotime")
    axes[0].legend(fontsize=8)
    names = [n for n in ["AT2", "Alveolar_transitional", "AT1_AT2", "AT1"] if (metadata.author_celltype.eq(n) & ok).any()]
    values = [pt[ok & metadata.author_celltype.eq(n)] for n in names]
    parts = axes[1].violinplot(values, showextrema=False, widths=.85)
    for body in parts["bodies"]:
        body.set_facecolor("#4C72B0"); body.set_alpha(.75)
    axes[1].scatter(range(1, len(values)+1), [np.median(v) for v in values], color="white", s=15, zorder=3)
    axes[1].set_xticks(range(1, len(names)+1), names, rotation=20, ha="right", fontsize=8)
    axes[1].set(ylabel="Diffusion pseudotime", title="Annotation comparison\nLabels were not used in pseudotime fitting")
    fig.suptitle("Saved RNA ordering and deposited annotations share cells and measurements\nViolins show cell distributions, not uncertainty across animals or independent fate validation.", fontsize=10)
    save(fig, "trajectory_alveolar_programmes")

    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    record = {"scope": "Presentation only from tracked tables; no trajectories, scores or model fits recomputed.",
              "inputs_sha256": {p.relative_to(HERE).as_posix(): digest(p) for p in inputs},
              "script_sha256": digest(Path(__file__)),
              "outputs_sha256": {p.name: digest(p) for p in sorted(OUT.glob("*.png"))}}
    (OUT / "figure_run.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print("Rendered four Niethamer presentation revisions from tracked tables.")


if __name__ == "__main__":
    main()
