"""Render the frozen Nb3 results as a paper-style figure package; no model fits.

Default output is immutable. Use --output tmp/... for a fresh review draft.
Input tables, plotted values, code, palette and all exports are hashed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
CACHE = ROOT / "raw_data/GSE307112/Nb3_v1"
TARGETS = ["NKX21", "BECN1", "KEAP1", "TRP53", "CDKN2B", "CTNNB1", "CSNK2A1", "ELOVL1", "ATP6V0E", "SLC34A2", "FZD5", "PORCN", "ERBB2", "ERBB3", "EGFR", "ERBB4"]
MOUSE = ["AT2_figure3", "transition_figure3", "IFN_figure3", "hypoxia_figure3", "gastric_maintext", "Wnt_maintext", "AT1_maintext"]
HUMAN = ["ID_figure4", "OXPHOS_figure4", "Hippo_figure4", "wound_figure4", "chemokines_figure4", "PLIN2_sentinel"]
LABEL = dict(zip(MOUSE + HUMAN, ["AT2", "Transition", "Interferon", "Hypoxia", "Gastric", "Wnt", "AT1", "ID genes", "Mitochondrial ND", "Hippo markers", "Wound markers", "Chemokines", "PLIN2"]))
ENDPOINTS = ["organoids_count", "organoids_area_mean", "organoids_area_prop"]
ENDLABEL = ["Organoid count", "Mean segmented size", "Bounding-box coverage"]
INPUTS, OUTPUTS, CHECKS = {}, [], []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remember(path):
    INPUTS[path.relative_to(ROOT).as_posix()] = sha(path)
    return path


def read(relative):
    return pd.read_csv(remember(HERE / relative), sep="\t")


def source(out, name, frame):
    assert not frame.empty, name
    frame.to_csv(out / "source_data" / f"{name}.tsv", sep="\t", index=False, float_format="%.12g", lineterminator="\n")


def title(ax, letter, text):
    ax.set_title(f"{letter}   {text}", loc="left", fontsize=9, fontweight="bold", pad=9)


def zero(ax):
    ax.axvline(0, color=P["muted"], lw=.7, zorder=0)


def forest(ax, frame, labels, color, xlabel=True):
    assert np.isfinite(frame[["effect", "ci_low", "ci_high"]]).all().all()
    assert (frame.ci_low <= frame.effect).all() and (frame.effect <= frame.ci_high).all()
    y = np.arange(len(frame))
    ax.errorbar(frame.effect, y, xerr=np.vstack([frame.effect-frame.ci_low, frame.ci_high-frame.effect]), fmt="o", ms=3.3, lw=.9, capsize=1.8, color=color)
    ax.set_yticks(y, labels)
    ax.set_ylim(len(frame)-.45, -.55)
    zero(ax)
    if xlabel:
        ax.set_xlabel("Marker-panel contrast\n(mean log$_2$[TMM CPM + 0.5])")


def heat(ax, matrix, limit, decimals=1, labels=None):
    assert np.isfinite(matrix.to_numpy()).all()
    im = ax.imshow(matrix, cmap=DIV, vmin=-limit, vmax=limit, aspect="auto", interpolation="none")
    ax.set_xticks(range(len(matrix.columns)), labels if labels is not None else matrix.columns)
    ax.set_yticks(range(len(matrix)), matrix.index)
    ax.tick_params(length=0, pad=4)
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(len(matrix)):
        for j in range(len(matrix.columns)):
            value = matrix.iloc[i, j]
            ax.text(j, i, f"{value:.{decimals}f}", ha="center", va="center", fontsize=6.5,
                    color=P["surface"] if abs(value) > .72*limit else P["ink"])
    return im


def save(out, fig, name):
    for ext in ("png", "pdf", "svg"):
        path = out / f"{name}.{ext}"
        kw = {"metadata": {"Creator": "Nb3 publication figure renderer", "CreationDate": None, "ModDate": None}} if ext == "pdf" else {}
        fig.savefig(path, dpi=300, **kw)
        OUTPUTS.append(path)
    plt.close(fig)


def main():
    global P, C, DIV
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "figures/publication_v1")
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite figure package: {out}")
    (out / "source_data").mkdir(parents=True)
    palette = remember(ROOT / "analysis/config/palette.json")
    P = json.loads(palette.read_text())
    C = list(P["categorical"].values())
    DIV = LinearSegmentedColormap.from_list("repo_signed", [C[0], P["surface"], C[1]])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9,
        "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "figure.facecolor": P["surface"], "axes.facecolor": P["surface"], "savefig.facecolor": P["surface"],
        "text.color": P["ink"], "axes.labelcolor": P["ink"], "xtick.color": P["ink_2"], "ytick.color": P["ink_2"],
        "axes.edgecolor": P["axis"], "axes.linewidth": .6, "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "svg.hashsalt": "Nb3-publication-v1",
        "figure.constrained_layout.use": True, "figure.constrained_layout.w_pad": .065,
        "figure.constrained_layout.h_pad": .085})
    imaging = read("runs/R1_v1/imaging_effects.tsv")
    panels = read("runs/R4_v1/fixed_panel_effects.tsv")
    associations = read("runs/extensions_v1/target_associations.tsv")
    imaging14 = imaging[(imaging.variant == "all_wells_scaling") & (imaging.day == "day14")]

    # Figure 1: unchanged focal targets, including positive and null contrasts.
    f1 = imaging14[imaging14.target.isin(TARGETS)].copy()
    source(out, "F01_imaging", f1)
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 5.8), sharey=True)
    for j, (ax, end, label) in enumerate(zip(axes, ENDPOINTS, ENDLABEL)):
        d = f1[f1.endpoint == end].set_index("target").loc[TARGETS]
        forest(ax, d, TARGETS, C[0], False)
        title(ax, "ABC"[j], label)
        ax.set_xlabel("Effect versus TIGIT\n(within-plate SD)")
    fig.supxlabel("Day 14 · points: technical-well OLS effects; bars: 95% technical intervals", fontsize=7)
    save(out, fig, "Nb3_F01_imaging")

    # Figure 2: exact stable-ID joins; every source-selected common gene shown.
    concordance = read("runs/R2_v1/source_concordance.tsv")
    consistency = read("runs/concordance_audit_v1/source_internal_consistency.tsv")
    source(out, "F02_target_concordance", concordance)
    source(out, "F02_source_consistency", consistency)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.5))
    for j, species in enumerate(["mouse", "human"]):
        with np.load(remember(CACHE / f"source_DE_{species}.npz")) as a:
            index = list(a["targets"]).index("NKX21")
            d = pd.DataFrame({"ID": a["gene"], "source_logFC": a["logfc"][:, index]})
        fitted = pd.read_csv(remember(CACHE / f"DE/{species}/NKX21.tsv.gz"), sep="\t")
        d = d.merge(fitted[["ID", "symbol", "logFC"]], on="ID", validate="one_to_one").rename(columns={"logFC": "Nb3_logFC"})
        source(out, f"F02_{species}_NKX21_genes", d)
        r = float(np.corrcoef(d.source_logFC, d.Nb3_logFC)[0, 1])
        expected = concordance[(concordance.species == species) & (concordance.target == "NKX21")].iloc[0]
        assert np.isclose(r, expected.pearson_logFC, atol=1e-10)
        CHECKS.append(f"{species} NKX21 gene-scatter Pearson matches frozen concordance")
        ax = axes[0, j]
        ax.scatter(d.source_logFC, d.Nb3_logFC, s=2.5, alpha=.22, c=C[j], linewidth=0, rasterized=True)
        lim = np.ceil(max(abs(d.source_logFC).max(), abs(d.Nb3_logFC).max()))
        ax.plot([-lim, lim], [-lim, lim], color=P["muted"], ls="--", lw=.7)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel(f"Source {'S4' if j == 0 else 'S5'} log$_2$ fold change")
        ax.set_ylabel("Nb3 log$_2$ fold change")
        title(ax, "AB"[j], f"NKX21 · {species}")
        ax.text(.03, .97, f"{len(d):,} genes\nr = {r:.3f}", transform=ax.transAxes, va="top", fontsize=7,
                bbox={"facecolor": P["surface"], "edgecolor": "none", "alpha": .88, "pad": 2})
    ax = axes[1, 0]
    for j, species in enumerate(["mouse", "human"]):
        d = concordance[concordance.species == species].sort_values("target")
        jitter = np.random.default_rng(21+j).uniform(-.14, .14, len(d))
        ax.scatter(d.pearson_logFC, j+jitter, s=6, color=C[j], alpha=.5, linewidth=0)
        ax.plot([d.pearson_logFC.median()]*2, [j-.25, j+.25], color=P["ink"], lw=1.4)
        ax.text(.02, .90-j*.12, f"{species}: n = {len(d)}, median = {d.pearson_logFC.median():.4f}", transform=ax.transAxes, fontsize=7)
    ax.set_yticks([0, 1], ["Mouse S4", "Human S5"]); ax.set_ylim(1.5, -.65)
    ax.set_xlim(-.1, 1.05); ax.set_xlabel("Pearson r across source-selected genes")
    title(ax, "C", "Concordance across targets")
    ax = axes[1, 1]
    for j, species in enumerate(["mouse", "human"]):
        row = consistency[consistency.species == species].iloc[0]
        pct = 100 * row.direction_matches / row.listed_direction_pairs
        ax.barh(j, pct, color=P["deemph"], height=.45)
        ax.barh(j, 100-pct, left=pct, color=C[1], height=.45)
        ax.text(1, j-.32, f"{row.direction_conflicts:,}/{row.listed_direction_pairs:,} conflicts", fontsize=7)
    ax.set_yticks([0, 1], ["Mouse S4", "Human S5"]); ax.set_ylim(1.5, -.65)
    ax.set_xlim(0, 100); ax.set_xlabel("Listed gene–target direction pairs (%)")
    ax.legend(handles=[Line2D([0], [0], color=P["deemph"], lw=5, label="Sign agrees"), Line2D([0], [0], color=C[1], lw=5, label="Sign conflicts")], loc="lower center", frameon=False)
    title(ax, "D", "Internal source-table check")
    fig.supxlabel("Human numeric S5 reproduction remains unresolved; source labels are retained.", fontsize=7)
    save(out, fig, "Nb3_F02_source_concordance")

    # Figure 3: one common diverging scale for all selected marker-panel contrasts.
    f3 = panels[panels.target.isin(TARGETS) & panels.program.isin(MOUSE+HUMAN)].copy()
    source(out, "F03_fixed_panels", f3)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 6.6), gridspec_kw={"width_ratios": [7, 6]})
    limit = float(np.ceil(f3.effect.abs().max()))
    for j, (species, programs, ax) in enumerate(zip(["mouse", "human"], [MOUSE, HUMAN], axes)):
        mat = f3[f3.species == species].pivot(index="target", columns="program", values="effect").loc[TARGETS, programs]
        im = heat(ax, mat, limit, labels=[LABEL[x] for x in programs])
        ax.tick_params(axis="x", labelrotation=55)
        for label in ax.get_xticklabels(): label.set_ha("right")
        if j: ax.set_yticklabels([])
        title(ax, "AB"[j], "Mouse epithelium" if j == 0 else "Human fibroblasts")
    fig.colorbar(im, ax=axes, location="bottom", shrink=.75, pad=.03, aspect=40,
                 label="Marker-panel contrast: mean log$_2$(TMM CPM + 0.5)")
    fig.supxlabel("Target versus same-plate TIGIT + tdTomato · common scale; numbers are effect estimates", fontsize=7)
    save(out, fig, "Nb3_F03_fixed_panels")

    # Figure 4: focal compartment contrasts and target-level associations.
    nkx = panels[(panels.target == "NKX21") & panels.program.isin(MOUSE+HUMAN)]
    source(out, "F04_NKX21_panels", nkx)
    wide = panels.assign(key=panels.species+"__"+panels.program).pivot(index="target", columns="key", values="effect")
    growth = imaging14[imaging14.endpoint == "organoids_area_prop"].set_index("target").effect
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.7))
    for j, (species, programs) in enumerate(zip(["mouse", "human"], [MOUSE, HUMAN])):
        d = nkx[nkx.species == species].set_index("program").loc[programs]
        forest(axes[0, j], d, [LABEL[x] for x in programs], C[j])
        axes[0, j].set_xlim(-4.5, 8.5)
        title(axes[0, j], "AB"[j], f"NKX21 · {species}")
    for j, (left, x) in enumerate([("mouse__AT2_figure3", wide["mouse__AT2_figure3"]), ("growth_coverage", growth)]):
        d = pd.concat([x.rename("x"), wide["human__chemokines_figure4"].rename("y")], axis=1).dropna()
        row = associations[(associations.left == left) & (associations.right == "human__chemokines_figure4")].iloc[0]
        assert len(d) == row.eligible_targets
        assert np.isclose(d.x.corr(d.y, method="spearman"), row.spearman)
        CHECKS.append(f"{left} scatter n and Spearman match frozen association")
        source(out, f"F04_association_{j+1}", d.reset_index())
        ax = axes[1, j]
        ax.scatter(d.x, d.y, s=10, color=P["muted"], alpha=.55, linewidth=0)
        for target in ["NKX21", "TRP53", "BECN1", "KEAP1"]:
            r = d.loc[target]
            ax.scatter([r.x], [r.y], s=16, color=C[1], linewidth=.4, edgecolor=P["ink"])
        # Only the focal perturbation is labelled; every point retains its target in source data.
        r = d.loc["NKX21"]
        ax.annotate("NKX21", (r.x, r.y), xytext=(5, 8) if j == 0 else (-5, 8), textcoords="offset points", ha="left" if j == 0 else "right", fontsize=7)
        ax.axhline(0, color=P["axis"], lw=.6, zorder=0); zero(ax)
        ax.set_xlabel("AT2 marker-panel contrast" if j == 0 else "Coverage contrast (within-plate SD)")
        ax.set_ylabel("Fibroblast chemokine-panel contrast")
        ax.text(.03, .97, f"n = {len(d)} targets\nSpearman ρ = {row.spearman:.3f}", transform=ax.transAxes, va="top", fontsize=7)
        title(ax, "CD"[j], "AT2 markers and chemokines" if j == 0 else "Growth and chemokines")
    fig.supxlabel("RNA axes: mean log$_2$(TMM CPM + 0.5) contrasts · 95% intervals in A–B are technical", fontsize=7)
    save(out, fig, "Nb3_F04_paired_niche")

    # Figure 5: pre-existing focal patterns, preserving broad and null intervals.
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.8))
    selections = [
        [(t, g) for t in ["NKX21", "BECN1", "CSNK2A1"] for g in ["transition_figure3", "IFN_figure3", "hypoxia_figure3"]],
        [(t, g) for t in ["CTNNB1", "PORCN", "FZD5", "ELOVL1", "ATP6V0E"] for g in ["Wnt_maintext", "AT1_maintext"]],
        [("SLC34A2", g) for g in ["AT2_figure3", "transition_figure3", "AT1_maintext", "IFN_figure3", "hypoxia_figure3", "Wnt_maintext"]]]
    lookup = panels[panels.species == "mouse"].set_index(["target", "program"])
    for j, (ax, selection) in enumerate(zip(axes.ravel(), selections)):
        d = lookup.loc[selection].reset_index()
        source(out, f"F05_panel_{'ABC'[j]}", d)
        labels = [f"{r.target} · {LABEL[r.program]}" for r in d.itertuples()] if j < 2 else [LABEL[r.program] for r in d.itertuples()]
        forest(ax, d, labels, C[0])
        title(ax, "ABC"[j], ["Transition and stress markers", "Wnt and AT1 markers", "SLC34A2 marker profile"][j])
    ica = read("runs/R3_v1/source_ICA_activities.tsv")
    targets = ["NKX21", "BECN1", "CSNK2A1", "CTNNB1", "ELOVL1", "ATP6V0E", "SLC34A2"]
    mat = ica.set_index("target").loc[targets, ["ICA_05", "ICA_13", "ICA_17"]]
    source(out, "F05_source_ICA", mat.reset_index())
    im = heat(axes[1, 1], mat, np.ceil(abs(mat).to_numpy().max()), decimals=2, labels=["ICA 5", "ICA 13", "ICA 17"])
    title(axes[1, 1], "D", "Deposited component activities")
    fig.colorbar(im, ax=axes[1, 1], location="bottom", pad=.04, aspect=30, label="Source S6 activity (signed)")
    fig.supxlabel("A–C: 95% technical intervals · D: deposited S6 values; component signs are arbitrary", fontsize=7)
    save(out, fig, "Nb3_F05_candidate_patterns")

    # Figure 6: quantiles describe controls, not confidence or cross-species abundance.
    receptors = read("runs/extensions_v1/receptor_expression.tsv")
    source(out, "F06_receptor_expression", receptors)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.8))
    genes = ["EGFR", "ERBB2", "ERBB3", "ERBB4"]
    for j, species in enumerate(["mouse", "human"]):
        d = receptors[receptors.species == species].assign(key=lambda x: x.gene.str.upper()).set_index("key").loc[genes]
        ax = axes[0, j]
        ax.errorbar(d.median_TMM_CPM, np.arange(4), xerr=np.vstack([d.median_TMM_CPM-d.q25_TMM_CPM, d.q75_TMM_CPM-d.median_TMM_CPM]), fmt="o", ms=4, color=C[j], capsize=2, lw=1)
        ax.set_yticks(range(4), d.gene); ax.set_ylim(3.6, -.6); ax.set_xlim(left=-2)
        ax.set_xlabel("TMM CPM (median and interquartile range)")
        title(ax, "AB"[j], f"{species.capitalize()} controls · n = {d.control_libraries.iloc[0]}")
        axes[1, 0].scatter(100*d.fraction_positive, np.arange(4)+(j-.5)*.16, label=species.capitalize(), color=C[j], marker="os"[j], s=23)
    ax = axes[1, 0]
    ax.set_yticks(range(4), genes); ax.set_ylim(3.6, -.6); ax.set_xlim(-3, 104)
    ax.set_xlabel("Control libraries with nonzero expression (%)")
    ax.legend(frameon=False, loc="lower left"); title(ax, "C", "Detection within each compartment")
    ax = axes[1, 1]
    for j, day in enumerate(["day07", "day14"]):
        d = imaging[(imaging.variant == "all_wells_scaling") & (imaging.day == day) & (imaging.endpoint == "organoids_area_prop")].set_index("target").loc[genes]
        source(out, f"F06_receptor_growth_{day}", d.reset_index())
        ax.errorbar(d.effect, np.arange(4)+(j-.5)*.18, xerr=np.vstack([d.effect-d.ci_low, d.ci_high-d.effect]), fmt="os"[j], color=C[j], ms=3.5, capsize=1.5, lw=.8, label=f"Day {7 if j == 0 else 14}")
    ax.set_yticks(range(4), genes); ax.set_ylim(3.6, -.6); zero(ax)
    ax.set_xlabel("Coverage contrast (within-plate SD)"); ax.legend(frameon=False, loc="lower left")
    title(ax, "D", "Epithelial receptor perturbations")
    fig.supxlabel("Species were normalized separately · D: 95% technical intervals; day 7 is secondary", fontsize=7)
    save(out, fig, "Nb3_F06_receptor_context")

    # Supplement 1: library QC and already-run imaging scaling sensitivity.
    qc = read("runs/R2_v1/library_qc.tsv")
    xenome = read("runs/R2_v1/xenome_QC.tsv")
    counts = qc.pivot(index="library", columns="species", values="detected_genes")
    passed = qc.pivot(index="library", columns="species", values="source_qc_pass")
    retention = pd.DataFrame({"population": ["Input wells", "Mouse pass", "Human pass", "Paired pass"], "libraries": [len(counts), int(passed.mouse.sum()), int(passed.human.sum()), int((passed.mouse & passed.human).sum())]})
    source(out, "S01_retention", retention); source(out, "S01_gene_detection", counts.reset_index())
    source(out, "S01_xenome", xenome)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.1))
    ax = axes[0, 0]
    ax.barh(np.arange(4), retention.libraries, color=[P["deemph"], C[0], C[1], P["muted"]], height=.55)
    ax.set_yticks(range(4), retention.population); ax.invert_yaxis(); ax.set_xlim(0, 1010); ax.set_xlabel("Libraries / wells")
    for i, n in enumerate(retention.libraries): ax.text(n+12, i, str(n), va="center", fontsize=8)
    title(ax, "A", "Species-specific QC retention")
    ax = axes[0, 1]
    ax.scatter(counts.mouse, counts.human, color=P["muted"], s=5, alpha=.5, linewidth=0)
    ax.axvline(7500, color=C[0], ls="--", lw=.9); ax.axhline(10000, color=C[1], ls="--", lw=.9)
    ax.set_xlabel("Detected mouse genes"); ax.set_ylabel("Detected human genes")
    ax.ticklabel_format(axis="both", style="sci", scilimits=(0, 0)); title(ax, "B", "Gene detection · 886 wells")
    ax = axes[1, 0]
    x = np.sort(xenome.fraction_unambiguous)
    ax.step(x, np.arange(1, len(x)+1)/len(x), where="post", color=C[0], lw=1.2)
    ax.axvline(np.median(x), ls="--", lw=.8, color=P["muted"])
    ax.text(.04, .93, f"Median = {np.median(x):.3f}", transform=ax.transAxes, va="top", fontsize=8)
    ax.set_xlabel("Xenome unambiguous read fraction"); ax.set_ylabel("Cumulative fraction of wells")
    title(ax, "C", "Species-assignment diagnostic")
    ax = axes[1, 1]
    joined = imaging[(imaging.day == "day14")].pivot(index=["target", "endpoint"], columns="variant", values="effect").reset_index()
    source(out, "S01_imaging_scaling", joined)
    lo = joined[["all_wells_scaling", "exclude_tdTomato_scaling"]].min().min()-.3
    hi = joined[["all_wells_scaling", "exclude_tdTomato_scaling"]].max().max()+.3
    ax.plot([lo, hi], [lo, hi], color=P["muted"], ls="--", lw=.7)
    for j, end in enumerate(ENDPOINTS):
        d = joined[joined.endpoint == end]
        ax.scatter(d.all_wells_scaling, d.exclude_tdTomato_scaling, s=8, color=C[j], marker=["o", "s", "^"][j], alpha=.55, linewidth=0, label=["Count", "Size", "Coverage"][j])
    ax.set_xlabel("Primary scaling effect (SD)"); ax.set_ylabel("Exclude tdTomato scaling effect (SD)")
    ax.legend(frameon=False, loc="upper left", markerscale=1.5); title(ax, "D", "Day-14 scaling sensitivity")
    fig.supxlabel("Paired wells are a subset of species QC passes; wells are not independent preparations.", fontsize=7)
    save(out, fig, "Nb3_S01_QC_and_scaling")

    # Supplement 2: source coefficients retain their original signs and comparators.
    projections = read("runs/R3_v1/source_ICA_panel_projections.tsv")
    programs = ["AT2_figure3", "transition_figure3", "IFN_figure3", "hypoxia_figure3", "Wnt_maintext", "AT1_maintext"]
    genes_order = []
    for program in programs:
        genes_order.extend(projections[projections.program == program].symbol.drop_duplicates().tolist())
    mat = projections.pivot(index="symbol", columns="component", values="projection_z").loc[genes_order, ["ICA_05", "ICA_13", "ICA_17"]]
    source(out, "S02_ICA_projections", projections[projections.component.isin(mat.columns)])
    budding = read("runs/R3_v1/source_budding_markers.tsv")
    genes = ["Sox9", "Axin2", "Ctnnd2", "Tgfb3", "Tcf7", "Rtkn2", "Spock2", "Cav1", "Hopx", "Aqp5"]
    source(out, "S02_budding_source", budding[budding.symbol.isin(genes)])
    fig = plt.figure(figsize=(7.2, 7.2))
    grid = fig.add_gridspec(2, 2, width_ratios=[1.1, 1])
    ax = fig.add_subplot(grid[:, 0])
    im = heat(ax, mat, np.ceil(abs(mat).to_numpy().max()), decimals=1, labels=["ICA 5", "ICA 13", "ICA 17"])
    title(ax, "A", "Source S7 gene projections")
    fig.colorbar(im, ax=ax, location="bottom", pad=.025, aspect=30, label="Signed projection z")
    for j, comparison in enumerate(["buddingmorpho_vs_TigitTdTom", "buddingmorpho_vs_othersWithIm"]):
        ax = fig.add_subplot(grid[j, 1])
        d = budding[budding.comparison == comparison].set_index("symbol").loc[genes]
        ax.scatter(d.logFC, np.arange(len(d)), s=18, color=C[0], marker="o")
        ax.set_yticks(range(len(d)), genes); ax.set_ylim(len(d)-.4, -.6); zero(ax)
        ax.set_xlabel("Source S3 log$_2$ fold change")
        title(ax, "BC"[j], "Budding versus controls" if j == 0 else "Budding versus other imaged")
    fig.supxlabel("Source-table views only · ICA Wnt coverage: 2/5 markers · S3 comparator scales differ", fontsize=7)
    save(out, fig, "Nb3_S02_source_components_and_budding")

    # Supplement 3: already-computed depth and influence diagnostics; no causal adjustment.
    depth = read("runs/extensions_v1/paired_depth_diagnostics.tsv")
    loo = read("runs/extensions_v1/leave_target_out.tsv")
    depth = depth[(depth.subset == "controls_only") & depth.program.isin(MOUSE+HUMAN)].copy()
    depth["key"] = depth.species+"__"+depth.program
    order = ["mouse__"+x for x in MOUSE]+["human__"+x for x in HUMAN]
    parts = []
    for depth_species in ["mouse", "human"]:
        d = depth[depth.depth_species == depth_species].set_index("key")
        parts.append(d[["spearman", "plate_residual_spearman"]].rename(columns={"spearman": depth_species+" raw", "plate_residual_spearman": depth_species+" residual"}))
    mat = pd.concat(parts, axis=1).loc[order]
    mat.index = ["M · "+LABEL[x] for x in MOUSE]+["H · "+LABEL[x] for x in HUMAN]
    source(out, "S03_depth_diagnostics", depth)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})
    im = heat(axes[0], mat, 1, decimals=2, labels=["Mouse\nraw", "Mouse\nresidual", "Human\nraw", "Human\nresidual"])
    title(axes[0], "A", "Control RNA score–depth association")
    axes[0].set_xlabel("Read-depth compartment and adjustment")
    fig.colorbar(im, ax=axes[0], location="bottom", pad=.04, aspect=30, label="Spearman ρ · 99 paired control wells")
    ax = axes[1]
    influence = []
    for j, left in enumerate(["mouse__AT2_figure3", "growth_coverage"]):
        a = associations[(associations.left == left) & (associations.right == "human__chemokines_figure4")].iloc[0]
        d = loo[(loo.left == left) & (loo.right == "human__chemokines_figure4")]
        base = 3*j
        ax.scatter([a.spearman], [base], color=C[0], s=24, marker="o")
        if pd.notna(a.growth_residual_spearman):
            ax.scatter([a.growth_residual_spearman], [base+.6], color=C[1], s=24, marker="s")
        ax.scatter(d.spearman, np.full(len(d), base+1.2), s=16, marker="|", color=P["muted"])
        drop = d[d.omitted == "NKX21"].iloc[0]
        ax.scatter([drop.spearman], [base+1.2], s=30, facecolor="none", edgecolor=P["ink"], zorder=4)
        influence.append(d)
    source(out, "S03_leave_target_out", pd.concat(influence))
    source(out, "S03_associations", associations[associations.left.isin(["mouse__AT2_figure3", "growth_coverage"]) & (associations.right == "human__chemokines_figure4")])
    ax.set_yticks([0, .6, 1.2, 3, 4.2], ["AT2 · raw", "AT2 · growth residual", "AT2 · omit one", "Coverage · raw", "Coverage · omit one"])
    ax.set_ylim(5.4, -.7); ax.set_xlim(0, .28); ax.set_xlabel("Spearman ρ with chemokine contrast")
    ax.legend(handles=[Line2D([0], [0], marker="|", linestyle="none", color=P["muted"], label="16 focal omissions"), Line2D([0], [0], marker="o", linestyle="none", markerfacecolor="none", color=P["ink"], label="Omit NKX21")], frameon=False, loc="lower left")
    title(ax, "B", "Influence and growth residuals")
    fig.supxlabel("M: mouse marker panel; H: human marker panel · residual correlations do not identify causality", fontsize=7)
    save(out, fig, "Nb3_S03_depth_and_influence")

    writer = PdfWriter()
    pdfs = [p for p in OUTPUTS if p.suffix == ".pdf"]
    for path in pdfs:
        reader = PdfReader(path)
        assert len(reader.pages) == 1
        writer.add_page(reader.pages[0])
    writer.add_metadata({"/Title": "Nb3: publication-style figure atlas, v1", "/Author": "Nb3 analysis"})
    atlas = out / "Nb3_figure_atlas.pdf"
    with atlas.open("wb") as handle: writer.write(handle)
    OUTPUTS.append(atlas)
    CHECKS.extend(["All forest estimates finite and inside their recorded intervals", "All heatmap cells finite", "Nine single-page figure PDFs assembled into atlas"])
    source_paths = sorted((out / "source_data").glob("*.tsv"))
    record = {"schema": "Nb3-publication-figures/v1", "analysis_id": "Nb3", "purpose": "Post-analysis visualization of frozen results; no new fits or scientific endpoint selection",
        "hierarchy": "Article-local versioned figure directory; scripts, gallery and source data remain with owning study; shared RQ directories unchanged",
        "style": {"width_inches": 7.2, "raster_dpi": 300, "formats": ["PDF", "SVG", "PNG"], "palette": "analysis/config/palette.json", "font": "DejaVu Sans", "base_font_pt": 8},
        "scientific_limits": ["Technical wells do not establish independent preparations", "Human numeric S5 reproduction remains failed/unresolved", "Fixed marker panels are not complete pathways or cell proportions", "ICA and budding panels are deposited coefficients, not refits"],
        "script_sha256": sha(Path(__file__)), "inputs": INPUTS,
        "outputs": {p.relative_to(out).as_posix(): sha(p) for p in OUTPUTS+source_paths},
        "checks": CHECKS, "visual_QA": "Recorded separately after inspection of PNG and PDF renders",
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__}}
    (out / "render_record.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"figures": len(pdfs), "source_tables": len(source_paths), "checks": len(CHECKS), "output": str(out)}))


if __name__ == "__main__":
    main()
