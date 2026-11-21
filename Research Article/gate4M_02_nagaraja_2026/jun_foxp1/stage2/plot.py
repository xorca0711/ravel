"""One descriptive figure in native assay units, with no cross-modality pairing."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


COLORS = {"AP1 only": "#23658a", "AP1 + Fox": "#aa5422"}


def spread(n, halfwidth=.13):
    return np.linspace(-halfwidth, halfwidth, n) if n > 1 else np.zeros(n)


def scatter_groups(ax, groups, classes):
    for x, values in enumerate(groups):
        for offset, (label, color) in zip([-.14, .14], COLORS.items()):
            sub = values[classes.reindex(values.index).eq(label)].dropna()
            ax.scatter(x + offset + spread(len(sub), .11), sub, s=13, color=color, alpha=.7,
                       linewidths=0, zorder=2)
            if len(sub):
                ax.plot(x + offset + np.array([-.1, .1]), [sub.median()] * 2, lw=1.5, color="black")
    ax.axhline(0, color="#8c8c8c", lw=.7, zorder=0)
    ax.set_xlim(-.5, len(groups) - .5)


def draw(binding, atac, meth, specimens, out):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "text.color": "black", "axes.labelcolor": "black",
                         "xtick.color": "black", "ytick.color": "black"})
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.9))
    fig.subplots_adjust(top=.88, bottom=.14, left=.094, right=.98, hspace=.60, wspace=.31)
    classes = binding.set_index("locus").motif_class
    a, b, c, d = axes.flat
    for idx, (label, color) in enumerate(COLORS.items()):
        group = binding[binding.motif_class.eq(label)]
        x = np.array([0, .74]) + 1.85 * idx
        for jitter, row in zip(spread(len(group), .06), group.itertuples()):
            y = [row.JUN_raw, row.JUNFOXP1_raw]
            a.plot(x + jitter, y, color=color, alpha=.28, lw=.75)
            a.scatter(x + jitter, y, s=10, color=color, alpha=.65, linewidths=0)
    a.set_xticks([0, .74, 1.85, 2.59], ["JUN", "JUN+FOXP1", "JUN", "JUN+FOXP1"])
    a.set_xlim(-.25, 2.85)
    a.set_ylabel("Raw footprint score")
    a.set_title("A   Paired biochemical footprints", loc="left", fontweight="bold")
    scatter_groups(b, [atac[atac.time.eq(day)].set_index("locus").delta_CPM for day in ("50", "102")], classes)
    b.set_xticks([0, 1], ["Day 50\n2 recovered, 2 control", "Day 102\n4 recovered, 2 control"])
    b.set_ylabel("Recovered − control (fragment CPM)")
    b.set_title("B   Epithelial accessibility", loc="left", fontweight="bold")
    windows = ["amplicon", "left_flank", "right_flank"]
    models = ["P4 organoid", "whole colon"]
    scatter_groups(c, [meth[meth.model.eq(m) & meth.window.eq(w)].set_index("locus").delta_pp
                       for m in models for w in windows], classes)
    c.set_xticks(range(6), ["Full", "Left", "Right"] * 2)
    for x, label in ((1, "P4 organoid"), (4, "Tissue vehicle")):
        c.text(x, -.18, label, ha="center", va="top", transform=c.get_xaxis_transform())
    c.set_ylabel("Recovered − control (percentage points)")
    c.set_title("C   Regional methylation", loc="left", fontweight="bold")
    motif = specimens[specimens.window.eq("scored_motif") & specimens.mean_fraction.notna()]
    assert motif.locus.nunique() == 1 and len(motif) == 12
    motif_color = COLORS[classes[motif.locus.iloc[0]]]
    for i, (m, arm) in enumerate((m, arm) for m in models for arm in ("control", "recovered")):
        values = motif[motif.model.eq(m) & motif.arm.eq(arm)].mean_fraction * 100
        x = [0, .85, 2.2, 3.05][i]
        d.scatter(x + spread(len(values)), values, s=30, color=motif_color, edgecolor="black", linewidth=.45)
        d.plot(x + np.array([-.17, .17]), [values.mean()] * 2, color="black", lw=1.4)
    d.set_xticks([0, .85, 2.2, 3.05], ["Control", "Recovered"] * 2)
    for x, label in ((.425, "P4 organoid"), (2.625, "Tissue vehicle")):
        d.text(x, -.18, label, ha="center", va="top", transform=d.get_xaxis_transform())
    d.set_xlim(-.47, 3.54)
    d.set_ylim(-3, 103)
    d.set_ylabel("Methylation at one CpG (%)")
    d.set_title("D   Sole scored-motif CpG", loc="left", fontweight="bold")
    handles = [Line2D([], [], linestyle="", marker="o", color=color,
                      label=f"{label} ({int(classes.eq(label).sum())} loci)") for label, color in COLORS.items()]
    fig.legend(handles=handles, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(.5,.986))
    fig.text(.094, .025, "B–C: one point per measurable locus per group; bars show class medians.  "
             "D: one point per mouse or line; bars show arm means.", fontsize=10)
    for ext in ["pdf", "png"]:
        fig.savefig(out / f"locus_measurements.{ext}", dpi=240, facecolor="white")
    plt.close(fig)
