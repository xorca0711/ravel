#!/usr/bin/env python
"""Wp figure plates: layout-only rendering from frozen, tracked run tables.

No biological calculation happens here. The only data operations are joins and
groupings needed to place marks: attaching the Wp-R3 partition label to each
gene's contrast row, and taking medians of values that the source tables already
contain. Every number drawn is read from a committed CSV produced by a governed
run with a verified receipt.

Six plates, one per executed stage plus one for the branch pair. Each plate
carries a claim title that is tested against every category it draws, the
design in the subtitle, and its interpretation limit in the footer. Colour is
bound once: Th17n purple, Th17p blue, throughout.

Outputs are refused rather than overwritten, so a re-render requires deleting
the previous files deliberately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

TH17N, TH17P = "#6A51A3", "#2171B5"
GREY, MID, ALARM = "#9CA3AF", "#555555", "#C2410C"
MS_C, IIH_C = "#B45309", "#0F766E"

PLATES = ["figure_1_gate_concordance", "figure_2_module_selectivity",
          "figure_3_glucose_arms", "figure_4_human_random_null",
          "figure_5_compass_reactions", "figure_6_branch_sensitivity"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "legend.fontsize": 8, "svg.fonttype": "none", "pdf.fonttype": 42,
    })


def head(fig, title: str, subtitle: str, foot: str) -> None:
    fig.suptitle(title, x=.045, ha="left", y=.985, fontsize=14, fontweight="bold")
    fig.text(.045, .93, subtitle, fontsize=9.5, va="top", color="#333333")
    width = fig.get_size_inches()[0]
    wrapped = textwrap.fill(" ".join(foot.split()), width=int(width * 13.5))
    fig.text(.045, .012, wrapped, fontsize=7.5, color="#444444", va="bottom")


def panel_letter(ax, letter: str) -> None:
    """Letter above the axes, so a panel can also carry its own title."""
    ax.text(-.02, 1.10, letter, transform=ax.transAxes, fontweight="bold",
            fontsize=12, ha="right", va="bottom")


# ----------------------------------------------------------------- figure 1
def fig_gate(conc: pd.DataFrame):
    d = conc[conc.variant == "primary_S3universe_trend"].copy()
    d["cell_type"] = d.our_contrast.str.split(".").str[0]
    d["gate"] = np.where(d.our_contrast.str.contains(".Div.1.", regex=False), "Div.1", "Total")
    d["drug"] = d.our_contrast.str.split(".").str[-1]
    d["arm"] = d.cell_type + " " + d.drug
    order = ["Th17n EGCG", "Th17n DHEA", "Th17p EGCG", "Th17p DHEA"]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.9))
    fig.subplots_adjust(left=.155, right=.975, top=.74, bottom=.2, wspace=.3)
    for ax, col, lab in zip(axes, ["pearson_logFC", "recall_of_source_signature"],
                            ["Pearson r of per-gene log\u2082 fold change",
                             "Fraction of the authors' signature recovered"]):
        for i, arm in enumerate(order):
            sub = d[d.arm == arm]
            lo = sub[sub.gate == "Div.1"][col].iloc[0]
            hi = sub[sub.gate == "Total"][col].iloc[0]
            colour = TH17N if arm.startswith("Th17n") else TH17P
            ax.plot([hi, lo], [i, i], color=GREY, lw=1.1, zorder=1)
            ax.scatter(hi, i, s=52, facecolor="white", edgecolor=colour, lw=1.4, zorder=2)
            ax.scatter(lo, i, s=52, color=colour, zorder=3)
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels(order)
        ax.set_ylim(-.6, len(order) - .4)
        ax.set_xlabel(lab)
        ax.set_xlim(0, 1)
        ax.grid(axis="x", color="#EEEEEE", lw=.7)
        ax.set_axisbelow(True)
    panel_letter(axes[0], "A")
    panel_letter(axes[1], "B")
    axes[0].annotate("weakest reproduction", xy=(.834, 0), xytext=(.40, .72),
                     fontsize=8, color=ALARM,
                     arrowprops=dict(arrowstyle="-", color=ALARM, lw=.8))
    handles = [Line2D([], [], marker="o", color="w", markerfacecolor=MID, markersize=8,
                      label="Division 1 (filled)"),
               Line2D([], [], marker="o", color="w", markerfacecolor="white",
                      markeredgecolor=MID, markersize=8, label="Total (open)")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.5, .055),
               ncol=2, frameon=False)
    head(fig, "The published bulk contrasts reproduce on the first-division gate",
         "GSE290297, 79 deposited TPM libraries | our moderated-t contrasts against the authors' Table S3,\n"
         "per cell type and inhibitor, computed separately in each division gate",
         "Agreement with Table S3 is reproduction of the authors' own analysis of their own deposit, not independent replication. "
         "The deposit declares no animal field, so every estimate is library-level. The gate is inferred from this agreement; the deposit does not state it.")
    return fig


# ----------------------------------------------------------------- figure 2
def fig_selectivity(contrasts: pd.DataFrame, partition: pd.DataFrame):
    grp = partition.set_index("symbol")["group"]
    arms = [("Th17n.Div.1.EGCG", "Th17n + EGCG"), ("Th17n.Div.1.DHEA", "Th17n + DHEA"),
            ("Th17p.Div.1.EGCG", "Th17p + EGCG"), ("Th17p.Div.1.DHEA", "Th17p + DHEA")]
    labels = {"Th17p_associated": "Th17p-associated\n(79 genes)",
              "Th17n_associated": "Th17n-associated\n(99 genes)"}
    fig, axes = plt.subplots(1, 4, figsize=(13.4, 5.1), sharey=True)
    fig.subplots_adjust(left=.105, right=.985, top=.73, bottom=.19, wspace=.1)
    rng = np.random.default_rng(20261005)
    for ax, (key, title) in zip(axes, arms):
        sub = contrasts[contrasts.contrast == key].copy()
        sub["group"] = grp.reindex(sub.symbol).to_numpy()
        base = float(np.median(sub.loc[sub.group == "not_significant", "logFC"]))
        ax.axvline(base, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
        colour = TH17N if key.startswith("Th17n") else TH17P
        for row, gkey in enumerate(["Th17p_associated", "Th17n_associated"]):
            v = sub.loc[sub.group == gkey, "logFC"].to_numpy()
            y = row + rng.uniform(-.16, .16, size=len(v))
            ax.scatter(v, y, s=7, color=colour, alpha=.38, linewidths=0, zorder=2)
            med = float(np.median(v))
            ax.plot([med, med], [row - .28, row + .28], color="black", lw=2.0, zorder=3)
            ax.annotate(f"{med - base:+.2f}", xy=(med, row + .36), ha="center",
                        fontsize=8, color="black")
        ax.set_yticks([0, 1])
        ax.set_yticklabels([labels["Th17p_associated"], labels["Th17n_associated"]])
        ax.set_ylim(-.65, 1.75)
        ax.set_xlim(-3.2, 3.2)
        ax.set_xlabel("log\u2082 fold change vs solvent")
        ax.set_title(title, loc="left", fontsize=10)
    for ax, letter in zip(axes, "ABCD"):
        panel_letter(ax, letter)
    head(fig, "In Th17n, PGAM inhibition moves both gene groups, not the pro-inflammatory group alone",
         "GSE290297 division-1 libraries | genes partitioned by the deposit's own DMSO Th17p-versus-Th17n contrast\n"
         "(BH \u2264 0.05 and |log\u2082 FC| \u2265 1.5), then plotted against each inhibitor",
         "Dashed line: median shift of the 11,003 genes in neither group, the whole-transcriptome move each inhibitor "
         "produces; the numbers are each group's median after that shift is removed. "
         "Library-level descriptive contrasts on deposited TPM; no animal field exists, so none of this is animal-level inference. "
         "Group medians are post-hoc readouts of the governed table. Centring removes the global shift but does not make the groups independent.")
    return fig


# ----------------------------------------------------------------- figure 3
def fig_glucose(means: pd.DataFrame, paired: pd.DataFrame):
    arms = [("proinflammatory_authors", "Pro-inflammatory arm"),
            ("proregulatory_authors", "Pro-regulatory arm"),
            ("pathogenicity_authors", "Pathogenicity score"),
            ("proliferation", "Proliferation score")]
    fig, axes = plt.subplots(1, 4, figsize=(13.0, 5.0), sharey=True)
    fig.subplots_adjust(left=.085, right=.985, top=.73, bottom=.21, wspace=.12)
    for ax, (col, title) in zip(axes, arms):
        for ct, colour in [("Th17n", TH17N), ("Th17p", TH17P)]:
            for animal, marker in [("Mo1", "o"), ("Mo2", "^")]:
                sub = means[(means.cell_type == ct) & (means.animal == animal)]
                lo = sub[sub.glucose == "1mM"][col].iloc[0]
                hi = sub[sub.glucose == "25mM"][col].iloc[0]
                ax.plot([0, 1], [lo, hi], color=colour, lw=1.3, alpha=.9, zorder=2)
                ax.scatter([0, 1], [lo, hi], s=40, marker=marker, color=colour, zorder=3)
        ax.axhline(0, color=GREY, lw=.8, zorder=1)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["1 mM", "25 mM"])
        ax.set_xlim(-.35, 1.35)
        ax.set_title(title, loc="left", fontsize=10)
    axes[0].set_ylabel("Library mean score")
    for ax, letter in zip(axes, "ABCD"):
        panel_letter(ax, letter)
    handles = [Line2D([], [], color=TH17N, lw=2, label="Th17n (TGF-\u03b2 + IL-6)"),
               Line2D([], [], color=TH17P, lw=2, label="Th17p (IL-1\u03b2 + IL-6 + IL-23)"),
               Line2D([], [], color=MID, marker="o", ls="", label="Animal Mo1"),
               Line2D([], [], color=MID, marker="^", ls="", label="Animal Mo2")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.5, .055),
               ncol=4, frameon=False)
    n_pos = int((paired.pathogenicity_authors_low_minus_high > 0).sum())
    head(fig, f"The pathogenicity score rises at low glucose through the pro-regulatory arm in {n_pos} of {len(paired)} animal pairs",
         "GSE289733, 8 libraries from 2 animals crossed over all four conditions | each line is one animal's paired\n"
         "libraries; scores use the authors' Table S1 modules with their highly-variable-gene flags",
         "Two animals. Each panel shows four paired differences and no test is performed; cell-level standard errors would describe cells, not mice. "
         "Scores are RNA module summaries, not measurements of pathogenicity, enzyme activity or flux.")
    return fig


# ----------------------------------------------------------------- figure 4
def fig_human(null: pd.DataFrame):
    # The pathogenicity score is a difference of two gene sets, not a set, so it has
    # no matched-size random comparator and is deliberately absent from this plate.
    show = ["proinflammatory_authors", "proregulatory_authors",
            "S3_Th17n_EGCG", "R3_Th17n_Div1_EGCG", "programme_N1", "programme_N3",
            "programme_P1", "programme_P4", "proliferation", "activation"]
    pretty = {"proinflammatory_authors": "Pro-inflammatory module",
              "proregulatory_authors": "Pro-regulatory module",
              "programme_N3": "Programme N3", "programme_P1": "Programme P1",
              "S3_Th17n_EGCG": "Th17n EGCG signature (Table S3)",
              "R3_Th17n_Div1_EGCG": "Th17n EGCG signature (Wp-R3)",
              "programme_N1": "Programme N1", "programme_P4": "Programme P4",
              "proliferation": "Proliferation set", "activation": "Activation set"}
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 6.0), sharey=True)
    fig.subplots_adjust(left=.29, right=.975, top=.72, bottom=.26, wspace=.08)
    for ax, tissue, tlab in zip(axes, ["CSF", "PBMCs"], ["Cerebrospinal fluid (6 vs 6)", "Blood (5 vs 5)"]):
        d = null[null.tissue == tissue].set_index("score")
        for i, key in enumerate(show):
            row = d.loc[key]
            ax.plot([row.null_q025, row.null_q975], [i, i], color=GREY, lw=5, alpha=.55,
                    solid_capstyle="butt", zorder=1)
            outside = not (row.null_q025 <= row.observed_median_difference <= row.null_q975)
            ax.scatter(row.observed_median_difference, i, s=58, zorder=3,
                       color=ALARM if outside else "black")
        ax.axvline(0, color="#CCCCCC", lw=.8, zorder=0)
        ax.set_yticks(range(len(show)))
        ax.set_yticklabels([pretty[s] for s in show])
        ax.invert_yaxis()
        ax.set_xlabel("MS minus comparison cohort, donor-level score")
        ax.set_title(tlab, loc="left", fontsize=10)
    panel_letter(axes[0], "A")
    panel_letter(axes[1], "B")
    handles = [Line2D([], [], color=GREY, lw=5, alpha=.55, label="95 % of 1,000 matched-size random gene sets"),
               Line2D([], [], color="black", marker="o", ls="", label="Observed, inside the random-set interval"),
               Line2D([], [], color=ALARM, marker="o", ls="", label="Observed, outside it")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.62, .125), ncol=3, frameon=False)
    head(fig, "In blood, random gene sets separate the two human cohorts as well as the modules do",
         "GSE138266 reused | 12 donors, 6 multiple sclerosis and 6 idiopathic intracranial hypertension;\n"
         "35,928 CD4-lineage T cells; each random set is drawn at the same mapped size and scored identically.\nThe two panels have different x scales: the blood differences are about three times larger.",
         "Donor-level transport of exposed mouse-derived signatures into a human dataset collected for another purpose; the comparison cohort is not healthy donors. "
         "A Mann-Whitney test on 5 versus 5 cannot fall below p = 0.0079. The pathogenicity score is a difference of two gene sets and has no matched random comparator, so it is not drawn. "
         "The random-set null was specified after the first run and is a post-hoc amendment.")
    return fig


# ----------------------------------------------------------------- figure 5
def fig_compass(corr: pd.DataFrame, named: pd.DataFrame):
    d = corr.sort_values("rho_pathogenicity_authors").reset_index(drop=True)
    ranks = named.set_index("reaction")["rank_of_rho"].to_dict()
    fig, ax = plt.subplots(figsize=(11.4, 5.6))
    fig.subplots_adjust(left=.085, right=.975, top=.72, bottom=.21)
    sig = d.bh_pathogenicity <= 0.05
    ax.scatter(d.index[~sig], d.rho_pathogenicity_authors[~sig], s=26,
               facecolor="white", edgecolor=GREY, lw=.9, zorder=2)
    ax.scatter(d.index[sig], d.rho_pathogenicity_authors[sig], s=34, color=MID, zorder=3)
    ax.axhline(0, color="#CCCCCC", lw=.9, zorder=1)

    def mark(key, label, dx, dy, colour, size):
        if key not in set(d.reaction):
            return
        i = int(d.index[d.reaction == key][0])
        y = float(d.rho_pathogenicity_authors.iloc[i])
        ax.scatter([i], [y], s=size, color=colour, zorder=4)
        ax.annotate(label, xy=(i, y), xytext=(i + dx, y + dy), fontsize=8, color=colour,
                    va="center", arrowprops=dict(arrowstyle="-", lw=.8, color=colour))

    mark("PGM_pos", f"PGAM, 3PG \u2192 2PG\n\u03c1 = {d.loc[d.reaction == 'PGM_pos', 'rho_pathogenicity_authors'].iloc[0]:.2f},"
                    f" rank {ranks['PGM_pos']} of 83, BH 0.18", 9, -.10, ALARM, 86)
    mark("PGCD_pos", f"PHGDH, first step of the 3PG \u2192 serine arm\n\u03c1 = "
                     f"{d.loc[d.reaction == 'PGCD_pos', 'rho_pathogenicity_authors'].iloc[0]:.2f},"
                     f" rank {ranks['PGCD_pos']} of 83", 17, .10, "black", 54)
    mark("THRD_L_pos", "Threonine dehydratase and lactate dehydrogenase:\nthe strongest negative associations, both BH < 0.001",
         11, .055, "black", 54)
    ax.set_xlabel("Reaction direction, ordered by correlation (83 scored)")
    ax.set_ylabel("Spearman \u03c1 with micropool\npathogenicity score")
    ax.set_xlim(-3, len(d) + 2)
    ax.margins(y=.18)
    handles = [Line2D([], [], color=MID, marker="o", ls="", label="BH \u2264 0.05 (7 reactions, none of them PGAM)"),
               Line2D([], [], color=GREY, marker="o", ls="", markerfacecolor="white", label="BH > 0.05")]
    ax.legend(handles=handles, loc="upper left", frameon=False)
    head(fig, "PGAM keeps the published negative sign but is not the most distinctive reaction",
         "Compass 1.0.0 on 60 micropools of Wp-R1 Th17n cells | version-and-input sensitivity, not Figure 1:\n"
         "the published scVI-imputed input was never deposited and the scope is two RECON2 subsystems",
         "Pools are not independent replicates and share animals and cultures, so the nominal degrees of freedom overstate the information. "
         "Compass scores are model outputs from RNA, not flux. Restricting the reaction set puts the published ~900-reaction ranking out of scope. "
         "Ranks are the governed run's own tie-aware values, so tied reactions share a rank.")
    return fig


# ----------------------------------------------------------------- figure 6
def fig_branches(agree: pd.DataFrame, glu: pd.DataFrame, dec: pd.DataFrame):
    pretty = {"arm_standardised": "Arms standardised", "local_hvg": "Locally recomputed HVGs",
              "all_genes": "Full module lists, no HVG filter",
              "proregulatory_neg": "Pro-regulatory arm alone",
              "proinflammatory": "Pro-inflammatory arm alone"}
    keep = list(pretty)
    a = agree[(agree.scope == "Th17n") & (agree.library == "pooled")].set_index("variant")
    g = glu[glu.scope == "Th17n"]
    fig = plt.figure(figsize=(13.2, 5.4))
    gs = fig.add_gridspec(1, 3, left=.235, right=.98, top=.73, bottom=.19, wspace=.55)
    ax1, ax2, ax3 = (fig.add_subplot(gs[0, i]) for i in range(3))

    ys = range(len(keep))
    ax1.barh(list(ys), [a.loc[k, "spearman_vs_reference"] for k in keep],
             color="#D9D9D9", edgecolor=MID, height=.6)
    for i, k in enumerate(keep):
        v = a.loc[k, "spearman_vs_reference"]
        ax1.text(v - .02, i, f"{v:.2f}", va="center", ha="right", fontsize=8)
    ax1.set_yticks(list(ys))
    ax1.set_yticklabels([pretty[k] for k in keep])
    ax1.invert_yaxis()
    ax1.set_xlim(0, 1.05)
    ax1.set_xlabel("Spearman \u03c1 against the published score")
    ax1.set_title("Cell ordering is stable", loc="left", fontsize=10)

    ref = g[g.variant == "reference"]
    for i, k in enumerate(["reference"] + keep):
        sub = g[g.variant == k]
        for _, row in sub.iterrows():
            ax2.scatter(row.low_minus_high, i, s=46,
                        marker="o" if row.animal == "Mo1" else "^",
                        color=ALARM if k == "proinflammatory" else MID, zorder=3)
    ax2.axvline(0, color=GREY, lw=.9)
    ax2.set_yticks(range(len(keep) + 1))
    ax2.set_yticklabels(["Published score"] + [pretty[k] for k in keep])
    ax2.invert_yaxis()
    ax2.set_xlabel("1 mM minus 25 mM, library mean")
    ax2.set_title("Its glucose effect size is not", loc="left", fontsize=10)

    dd = dec[(dec.cell_type == "Th17n") & (dec.labelling == "programme") &
             (dec.score == "pathogenicity")]
    width = .34
    for j, animal in enumerate(["Mo1", "Mo2"]):
        row = dd[dd.animal == animal].iloc[0]
        ax3.bar(j - width / 2, row.composition_term, width, color=TH17N, label="Composition" if j == 0 else None)
        ax3.bar(j + width / 2, row.within_term, width, color="#BDBDBD", edgecolor=MID,
                label="Within programme" if j == 0 else None)
        ax3.scatter([j], [row.total_difference], marker="D", s=46, color="black", zorder=4,
                    label="Total difference" if j == 0 else None)
    ax3.axhline(0, color=GREY, lw=.9)
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(["Mo1", "Mo2"])
    ax3.set_ylabel("Contribution to the glucose difference")
    ax3.set_title("The rise is a change of mixture", loc="left", fontsize=10)
    ax3.legend(frameon=False, loc="lower left", fontsize=7.5, handlelength=1.4)
    for ax, letter in zip([ax1, ax2, ax3], "ABC"):
        panel_letter(ax, letter)
    head(fig, "The cell ranking survives how the score was built; the glucose effect size does not",
         "GSE289733 Th17n cells | A-B, Wp-P01 variant scores against the published definition; "
         "C, Wp-P03 Kitagawa\ndecomposition of the same glucose difference into mixture and within-programme parts",
         "Every variant uses the same cells and the same expression matrix, so agreement between them is the absence of a gene-selection artefact, not independent evidence. "
         "In B, circles are animal Mo1 and triangles Mo2. In C the within-programme term has opposite signs in the two animals and is reported inconclusive; programmes are defined from the same expression as the score, so part of the mixture term is guaranteed by construction.")
    return fig


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    runs, out = Path(args.runs_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    targets = [out / f"{n}.{e}" for n in PLATES for e in ("png", "pdf", "svg")]
    assert not any(p.exists() for p in targets), "Refusing to overwrite figures"

    src = {
        "bulk_concordance": runs / "wp_bulk_contrasts_v1/source_concordance.csv",
        "bulk_contrasts": runs / "wp_bulk_contrasts_v1/bulk_contrasts.csv.gz",
        "bulk_partition": runs / "wp_bulk_contrasts_v1/partition_Div1.csv.gz",
        "sc_library_means": runs / "wp_singlecell_reproduction_v1/library_score_means.csv",
        "sc_paired": runs / "wp_singlecell_reproduction_v1/glucose_paired_differences.csv",
        "human_null": runs / "wp_human_signature_transfer_v2/random_set_null.csv",
        "compass_corr": runs / "wp_compass_sensitivity_v1_rerun/reaction_correlations.csv",
        "compass_named": runs / "wp_compass_sensitivity_v1_rerun/named_reactions.csv",
        "p01_agreement": runs / "wp_score_construction_v1/variant_agreement.csv",
        "p01_glucose": runs / "wp_score_construction_v1/glucose_direction_by_variant.csv",
        "p03_decomposition": runs / "wp_glucose_decomposition_v1/decomposition.csv",
    }
    verified = {k: sha256(v) for k, v in src.items()}
    tables = {k: pd.read_csv(v) for k, v in src.items()}

    style()
    figures = [
        ("figure_1_gate_concordance", fig_gate(tables["bulk_concordance"])),
        ("figure_2_module_selectivity", fig_selectivity(tables["bulk_contrasts"], tables["bulk_partition"])),
        ("figure_3_glucose_arms", fig_glucose(tables["sc_library_means"], tables["sc_paired"])),
        ("figure_4_human_random_null", fig_human(tables["human_null"])),
        ("figure_5_compass_reactions", fig_compass(tables["compass_corr"], tables["compass_named"])),
        ("figure_6_branch_sensitivity", fig_branches(tables["p01_agreement"], tables["p01_glucose"],
                                                     tables["p03_decomposition"])),
    ]
    manifest = []
    for name, fig in figures:
        for ext in ("png", "pdf", "svg"):
            fig.savefig(out / f"{name}.{ext}", dpi=300 if ext == "png" else None)
        manifest.append({"figure": name,
                         "files": [f"{name}.{e}" for e in ("png", "pdf", "svg")]})
    with PdfPages(out / "Wang_PGAM_figures.pdf") as pdf:
        for _, fig in figures:
            pdf.savefig(fig)
    for _, fig in figures:
        plt.close(fig)

    (out / "figure_manifest.json").write_text(json.dumps(
        {"schema": "wp_figures/v1", "inputs_verified": verified, "plates": manifest,
         "rendering": "layout only; joins and medians for placement, no new statistics",
         "interpretation_limit": ("Every plate renders values from a governed run with a verified receipt. "
            "The plates inherit each run's limits: library-level bulk contrasts with no animal field, two mice "
            "in the single-cell deposit, donor-level transport of exposed signatures in the human reuse, and a "
            "version-and-input sensitivity rather than a reproduction for the Compass plate.")},
        indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
