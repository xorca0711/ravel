"""Render existing qualified Song source rows and descriptive estimates."""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUNS = Path("analysis/research/runs")
COLORS = {"WT": "#176582", "KO": "#a34135"}


def read(stage, name):
    with (RUNS / f"song24_c2_{stage}_v2" / f"{name}.csv").open() as handle:
        return list(csv.DictReader(handle))


def draw_rows(ax, x, entries, genotype):
    values = [float(row["value"]) for row in entries if row["value"]]
    offsets = [(i - (len(values) - 1) / 2) * min(0.08, 0.42 / len(values)) for i in range(len(values))]
    ax.scatter([x + offset for offset in offsets], values, color=COLORS[genotype], alpha=.82, s=28)
    return len(values)


def mcu(output):
    observations = read("S2", "observations")
    contrasts = read("S2", "contrasts")
    fig, axes = plt.subplots(2, 2, figsize=(9, 7), layout="constrained")
    units = ["Rhod-2 (normalized AU)", "TMRM (normalized AU)",
             "Recovered HSC number (source units)", "Colony count"]
    for ax, letter, unit in zip(axes.flat, "ABCD", units):
        panel = "ED 7" + letter
        rows = [row for row in observations if row["panel"] == panel]
        for i, condition in enumerate(("Ctrl", "MCUKD")):
            effect = next(row for row in contrasts if row["panel"] == panel and
                          row["contrast"] == f"KO_{condition} - WT_{condition}")
            counts = []
            for offset, genotype, key in [(-.15, "WT", "control"), (.15, "KO", "case")]:
                x = i + offset
                count = draw_rows(ax, x, [row for row in rows if row["group"] == f"{genotype}_{condition}"], genotype)
                assert count == int(effect[f"n_{key}"])
                counts.append(count)
                ax.hlines(float(effect[f"mean_{key}"]), x-.10, x+.10, color="black", linewidth=1.6)
            label = "Control shRNA" if i == 0 else "MCU shRNA"
            ax.set_xticks([0, 1])
            ax.text(i, -.16, f"{label}\nWT {counts[0]} · KO {counts[1]}", ha="center",
                    transform=ax.get_xaxis_transform(), fontsize=9)
        ax.set_xticklabels([])
        ax.set(xlim=(-.47, 1.47), ylabel=unit, title=f"Extended Data Fig. 7{letter.lower()}")
        ax.grid(axis="y", alpha=.2)
    fig.suptitle("Young HSCs after 48 h of cytokines and shRNA\nBlue: WT    Red: Cd38 KO    Bars: source-row means")
    fig.savefig(output / "mcu_four_group.png", dpi=180)
    plt.close(fig)


def transplant(output):
    observations = read("S4", "observations")
    contrasts = read("S4", "contrasts")
    panels = ["Fig 1F", "Fig 3G", "ED 6B", "ED 10D"]
    labels = ["Cd38 · 3 months", "Cd38 · 24 months", "MCU · 7 months", "MCU · 24 months"]
    fig, (ax, effect_ax) = plt.subplots(1, 2, figsize=(12, 5.2), layout="constrained")
    for i, (panel, label) in enumerate(zip(panels, labels)):
        rows = [row for row in observations if row["panel"] == panel and row["endpoint"] == "16 wks"]
        effect = next(row for row in contrasts if row["panel"] == panel and row["endpoint"] == "16 wks")
        counts = []
        for offset, genotype, key in [(-.18, "WT", "control"), (.18, "KO", "case")]:
            x = i + offset
            count = draw_rows(ax, x, [row for row in rows if row["group"] == genotype], genotype)
            assert count == int(effect[f"n_{key}"])
            counts.append(count)
            ax.hlines(float(effect[f"mean_{key}"]), x-.12, x+.12, color="black", linewidth=1.6)
        ax.text(i, -.17, f"WT {counts[0]} · KO {counts[1]}", ha="center",
                transform=ax.get_xaxis_transform(), fontsize=8)
        delta = float(effect["difference"])
        effect_ax.hlines(i, float(effect["loo_min"]), float(effect["loo_max"]), color="#484f55", linewidth=2)
        effect_ax.scatter(delta, i, color="#20282d", zorder=3)
        effect_ax.annotate(f"{delta:+.2f}", (delta, i), xytext=(0, 9), textcoords="offset points",
                           ha="center", fontsize=9)
    ax.set_xticks(range(4), labels, rotation=10, fontsize=8)
    ax.set(ylabel="Peripheral-blood donor contribution (%)", title="Recipient rows and means")
    ax.grid(axis="y", alpha=.2)
    effect_ax.axvline(0, color="#999999", linestyle="--", linewidth=1)
    effect_ax.set_yticks(range(4), labels)
    effect_ax.set(xlabel="KO − WT (percentage points)", title="Within-cohort contrasts\nLines show leave-one-row ranges",
                  ylim=(3.5, -.5), xlim=(-42, 20))
    fig.suptitle("Week-16 competitive transplant output\nBlue: WT donor    Red: KO donor")
    fig.savefig(output / "week16_transplant.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    output = Path(sys.argv[1])
    mcu(output)
    transplant(output)
