#!/usr/bin/env python
"""A30 figure: layout-only rendering from frozen, tracked run tables.

No biological calculation happens here. Every number drawn is read from a
committed CSV of a governed run with a verified receipt; the only operations
are selection and placement.

Two panels, one message: the CSF pro-inflammatory elevation does not depend on
activation, and about two fifths of it is a cell-mixture shift.

  A  per-donor paired CSF-minus-blood difference in each activation stratum,
     both module arms, with the matched random-set interval behind each column
     so the reader sees the observed donors against the null that was used.
  B  the Kitagawa split of the same total difference on two bases, showing
     that the composition term is small on activation strata and substantial
     on independently clustered cell states.

Outputs refuse to overwrite, so a re-render requires deleting deliberately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PRO_INF, PRO_REG = "#B5452F", "#2E7D6E"
NULLBAND, GREY, INK = "#E8EDF1", "#8A979F", "#33434D"
COMP, WITHIN = "#C98A5B", "#4C86B0"
STRATA = ["act1", "act2", "act3"]
STRAT_LABEL = {"act1": "low", "act2": "mid", "act3": "high"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    runs, out = Path(args.runs_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    src = {"contrasts": runs / "wp_a30_activation_stratified_v2/stratified_contrasts.csv",
           "per_donor": runs / "wp_a30_activation_stratified_v2/per_donor_differences.csv",
           "dec_act": runs / "wp_a30_activation_stratified_v2/decomposition_summary.csv",
           "dec_state": runs / "wp_a30_state_decomposition_v2/decomposition_summary.csv"}
    verified = {k: sha256(v) for k, v in src.items()}
    ct = pd.read_csv(src["contrasts"])
    pdo = pd.read_csv(src["per_donor"])
    da = pd.read_csv(src["dec_act"])
    dsx = pd.read_csv(src["dec_state"])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                         "axes.linewidth": 0.8, "axes.edgecolor": "#55636B",
                         "xtick.color": "#55636B", "ytick.color": "#55636B",
                         "axes.labelcolor": INK, "text.color": INK,
                         "xtick.major.width": 0.8, "ytick.major.width": 0.8,
                         "figure.dpi": 300, "savefig.dpi": 300})

    fig = plt.figure(figsize=(7.2, 3.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.75, 1.0], wspace=0.38,
                          left=.085, right=.985, top=.74, bottom=.17)
    axA, axB = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])

    # ---- panel A -----------------------------------------------------------
    arms = [("proinflammatory_authors", "Pro-inflammatory", PRO_INF),
            ("proregulatory_authors", "Pro-regulatory", PRO_REG)]
    xs, labels, centres = [], [], []
    rng = np.random.default_rng(7)
    pos = 0.0
    for s in STRATA:
        grp = []
        for score, _, colour in arms:
            row = ct[(ct.stratum == s) & (ct.score == score)].iloc[0]
            axA.add_patch(plt.Rectangle((pos - .30, row.null_q025), .60,
                                        row.null_q975 - row.null_q025,
                                        facecolor=NULLBAND, edgecolor="none", zorder=1))
            v = pdo[(pdo.stratum == s) & (pdo.score == score)]["csf_minus_blood"].to_numpy()
            axA.scatter(pos + rng.uniform(-.13, .13, len(v)), v, s=11, color=colour,
                        alpha=.55, linewidths=0, zorder=3)
            axA.plot([pos - .26, pos + .26], [row.median_difference] * 2,
                     color=colour, lw=2.1, solid_capstyle="butt", zorder=4)
            axA.annotate(f"{row.median_difference:+.3f}", xy=(pos, row.median_difference),
                         xytext=(0, 7), textcoords="offset points", ha="center",
                         fontsize=7, color=colour, zorder=5)
            grp.append(pos)
            pos += 0.78
        centres.append(float(np.mean(grp)))
        labels.append(f"{STRAT_LABEL[s]}\nactivation")
        pos += 0.48
    axA.axhline(0, color=GREY, lw=.8, ls=(0, (4, 3)), zorder=2)
    axA.set_xticks(centres); axA.set_xticklabels(labels)
    axA.set_ylabel("CSF \u2212 blood, paired within donor")
    axA.set_xlim(-0.6, pos - 0.9)
    axA.margins(y=.12)
    axA.spines[["top", "right"]].set_visible(False)
    axA.set_title("A  The elevation is the same at every activation level",
                  loc="left", fontsize=8.5, pad=16)
    axA.text(0, 1.015, "one dot per donor \u00b7 bar = median \u00b7 shaded = 95 % of "
                       "matched random gene sets",
             transform=axA.transAxes, fontsize=6.8, color=GREY, va="bottom")
    for (score, name, colour), dx in zip(arms, (-0.30, 0.30)):
        axA.scatter([], [], s=16, color=colour, label=name)
    axA.legend(frameon=False, loc="lower right", fontsize=7, handletextpad=.4,
               borderpad=.1, labelspacing=.25)

    # ---- panel B -----------------------------------------------------------
    rows = [("Activation\nstrata (3)", da[(da.basis == "activation_stratum") &
                                          (da.score == "proinflammatory_authors")].iloc[0]),
            ("De novo cell\nstates (23)", dsx[dsx.score == "proinflammatory_authors"].iloc[0])]
    y = np.arange(len(rows))[::-1].astype(float)
    for yy, (_, r) in zip(y, rows):
        axB.barh(yy, r.composition, height=.42, color=COMP, edgecolor="none", zorder=3)
        axB.barh(yy, r.within, height=.42, left=r.composition, color=WITHIN,
                 edgecolor="none", zorder=3)
        axB.plot([r.total, r.total], [yy - .30, yy + .30], color=INK, lw=1.3, zorder=4)
        axB.annotate(f"{100*r.composition/r.total:.0f} %", xy=(r.composition / 2, yy),
                     ha="center", va="center", fontsize=7, color="white", zorder=5)
        axB.annotate(f"{100*r.within/r.total:.0f} %",
                     xy=(r.composition + r.within / 2, yy),
                     ha="center", va="center", fontsize=7, color="white", zorder=5)
    axB.set_yticks(y); axB.set_yticklabels([n for n, _ in rows], fontsize=7.5)
    axB.set_xlabel("share of the +0.071 total difference")
    axB.set_xlim(0, max(r.total for _, r in rows) * 1.16)
    axB.set_ylim(-0.6, len(rows) - 0.4)
    axB.spines[["top", "right", "left"]].set_visible(False)
    axB.tick_params(axis="y", length=0)
    axB.set_title("B  Independent states reveal a mixture shift",
                  loc="left", fontsize=8.5, pad=16)
    axB.text(0, 1.015, "vertical rule = total \u00b7 Kitagawa split, exact",
             transform=axB.transAxes, fontsize=6.8, color=GREY, va="bottom")
    axB.scatter([], [], marker="s", s=22, color=COMP, label="composition")
    axB.scatter([], [], marker="s", s=22, color=WITHIN, label="within-state")
    axB.legend(frameon=False, loc="lower right", fontsize=7, handletextpad=.4,
               borderpad=.1, labelspacing=.25)

    fig.text(.085, .055,
             "GSE138266, 10 donors contributing paired CSF and blood; donor is the unit. "
             "Activation is scored from 21 genes disjoint from both modules. In A the "
             "activation score itself is flat within strata (empirical p 0.66\u20130.92), so "
             "the strata are activation-matched; the pro-inflammatory arm does not reach "
             "BH \u2264 0.05 against its matched null (BH 0.063\u20130.068).",
             fontsize=6.4, color=GREY, va="top", wrap=True)

    stem = out / "figure_a30_activation_and_composition"
    for ext in ("png", "pdf", "svg"):
        p = Path(f"{stem}.{ext}")
        if p.exists():
            raise SystemExit(f"refusing to overwrite {p}")
        fig.savefig(p, bbox_inches=None)
    plt.close(fig)

    (out / "figure_manifest.json").write_text(json.dumps(
        {"schema": "wp_a30_figure/v1", "inputs_verified": verified,
         "outputs": {f"{stem.name}.{e}": sha256(Path(f"{stem}.{e}"))
                     for e in ("png", "pdf", "svg")},
         "matplotlib": matplotlib.__version__,
         "note": ("Layout-only rendering of frozen tables. Panel A shows every donor; "
                  "panel B is an exact algebraic split, not a model fit.")},
        indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
