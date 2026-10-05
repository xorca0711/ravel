#!/usr/bin/env python
"""Wp-P03: is the low-glucose pathogenicity shift composition or within-state change?

Kitagawa decomposition of the glucose score difference on the Wp-R1 per-cell
output, per animal and per cell type. No new expression is read.

Estimator, frozen before any term was computed:
    D     = sum_k p_k(low) m_k(low) - sum_k p_k(high) m_k(high)
    within      = sum_k pbar_k [ m_k(low) - m_k(high) ]
    composition = sum_k [ p_k(low) - p_k(high) ] mbar_k
    interaction = D - within - composition
with pbar_k and mbar_k the pooled-condition proportion and mean of programme k,
as the card specifies ("proportions held at the pooled-condition values for the
within term"). Programmes with fewer than MIN_CELLS cells in either condition for
a given animal are pooled into an `other` category rather than dropped, so the
proportions still sum to one and D is reproduced exactly.

Reported for the pathogenicity score and for each arm separately, under:
  - both Wp-R1 programme labellings (all markers, and markers excluding genes
    shared with the score) as the labelling sensitivity;
  - proliferation terciles computed within library as a stratum, with the
    decomposition run inside each stratum and averaged with stratum weights, as
    the card's substitute for regressing cell-cycle phase out.

Unit: cells within 8 libraries from 2 animals, crossed over all four conditions.
Two animals cap this at descriptive; every term is reported per animal and the
run declares the result inconclusive if the two animals disagree in sign.

Declared substitutions against the card's text, both forced by the deposit:
  1. The card asks for a coarser and a finer Leiden resolution. The analysed
     5,192-cell object and its clustering are not deposited, so Wp-R1 assigned
     programmes by Table S5 marker score. The two available labellings are the
     only labelling sensitivity possible here, and they are not a resolution
     sweep.
  2. The card asks for cell-cycle phase as a stratum. Phase is not deposited;
     the Wp-R1 proliferation score is used as a continuous proxy, cut into
     within-library terciles.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

MIN_CELLS = 20
SCORES = {"pathogenicity": "pathogenicity_authors",
          "proinflammatory_arm": "proinflammatory_authors",
          "proregulatory_arm": "proregulatory_authors"}
LABELLINGS = ["programme", "programme_excl_overlap"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def decompose(df: pd.DataFrame, label_col: str, score_col: str) -> dict:
    """Kitagawa decomposition of the 1 mM minus 25 mM difference in mean score."""
    low, high = df[df.glucose == "1mM"], df[df.glucose == "25mM"]
    if len(low) == 0 or len(high) == 0:
        return {}
    labels = df[label_col].astype(str)
    counts_low = low[label_col].astype(str).value_counts()
    counts_high = high[label_col].astype(str).value_counts()
    small = {p for p in labels.unique()
             if counts_low.get(p, 0) < MIN_CELLS or counts_high.get(p, 0) < MIN_CELLS}
    key = labels.where(~labels.isin(small), "other")
    work = df.assign(_k=key.to_numpy())
    lo, hi = work[work.glucose == "1mM"], work[work.glucose == "25mM"]

    ks = sorted(work["_k"].unique())
    p_lo = np.array([ (lo["_k"] == k).mean() for k in ks])
    p_hi = np.array([ (hi["_k"] == k).mean() for k in ks])
    m_lo = np.array([ lo.loc[lo["_k"] == k, score_col].mean() if (lo["_k"] == k).any() else 0.0 for k in ks])
    m_hi = np.array([ hi.loc[hi["_k"] == k, score_col].mean() if (hi["_k"] == k).any() else 0.0 for k in ks])
    p_bar, m_bar = (p_lo + p_hi) / 2, (m_lo + m_hi) / 2

    total = float(lo[score_col].mean() - hi[score_col].mean())
    within = float((p_bar * (m_lo - m_hi)).sum())
    comp = float(((p_lo - p_hi) * m_bar).sum())
    return {"total_difference": total, "within_term": within, "composition_term": comp,
            "interaction_term": total - within - comp,
            "within_share": within / total if total != 0 else np.nan,
            "composition_share": comp / total if total != 0 else np.nan,
            "n_programmes": len(ks), "n_pooled_into_other": len(small),
            "n_cells_low": int(len(lo)), "n_cells_high": int(len(hi))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--r1-run", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    r1, out = Path(args.r1_run), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    verified = {"wp_singlecell_reproduction_v1/cell_scores.csv.gz": sha256(r1 / "cell_scores.csv.gz"),
                "wp_singlecell_reproduction_v1/programme_composition.csv":
                    sha256(r1 / "programme_composition.csv")}
    cells = pd.read_csv(r1 / "cell_scores.csv.gz")

    # proliferation terciles within library, the declared cell-cycle stratum
    cells["prolif_stratum"] = (cells.groupby("library")["proliferation"]
                               .transform(lambda s: pd.qcut(s, 3, labels=["low", "mid", "high"],
                                                            duplicates="drop").astype(str)))

    rows, strat_rows = [], []
    for cell_type, byct in cells.groupby("cell_type"):
        for animal, sub in byct.groupby("animal"):
            for label_col in LABELLINGS:
                for score_name, score_col in SCORES.items():
                    d = decompose(sub, label_col, score_col)
                    if d:
                        rows.append({"cell_type": cell_type, "animal": animal, "labelling": label_col,
                                     "score": score_name, **d})
                    # stratified version: decompose inside each proliferation tercile
                    parts, weights = [], []
                    for stratum, ssub in sub.groupby("prolif_stratum"):
                        ds = decompose(ssub, label_col, score_col)
                        if ds:
                            parts.append(ds)
                            weights.append(len(ssub))
                    if parts:
                        w = np.array(weights, dtype=float)
                        w /= w.sum()
                        strat_rows.append({"cell_type": cell_type, "animal": animal,
                                           "labelling": label_col, "score": score_name,
                                           "n_strata": len(parts),
                                           **{k: float(np.sum(w * np.array([p[k] for p in parts])))
                                              for k in ("total_difference", "within_term",
                                                        "composition_term", "interaction_term")}})
    dec = pd.DataFrame(rows)
    dec.to_csv(out / "decomposition.csv", index=False, lineterminator="\n")
    strat = pd.DataFrame(strat_rows)
    strat["within_share"] = strat.within_term / strat.total_difference
    strat["composition_share"] = strat.composition_term / strat.total_difference
    strat.to_csv(out / "decomposition_proliferation_strata.csv", index=False, lineterminator="\n")

    # per-programme detail, so a reader can see which programme carries each term
    detail = []
    for cell_type, byct in cells.groupby("cell_type"):
        for animal, sub in byct.groupby("animal"):
            for label_col in LABELLINGS:
                for p, psub in sub.groupby(label_col):
                    lo = psub[psub.glucose == "1mM"]
                    hi = psub[psub.glucose == "25mM"]
                    tot_lo = (sub.glucose == "1mM").sum()
                    tot_hi = (sub.glucose == "25mM").sum()
                    detail.append({"cell_type": cell_type, "animal": animal, "labelling": label_col,
                                   "programme": p, "n_low": int(len(lo)), "n_high": int(len(hi)),
                                   "proportion_low": len(lo) / tot_lo if tot_lo else np.nan,
                                   "proportion_high": len(hi) / tot_hi if tot_hi else np.nan,
                                   "pathogenicity_low": float(lo.pathogenicity_authors.mean()) if len(lo) else np.nan,
                                   "pathogenicity_high": float(hi.pathogenicity_authors.mean()) if len(hi) else np.nan})
    pd.DataFrame(detail).to_csv(out / "programme_detail.csv", index=False, lineterminator="\n")

    def summarise(frame: pd.DataFrame) -> list[dict]:
        keep = frame[(frame.labelling == "programme") & (frame.score == "pathogenicity")]
        return keep[["cell_type", "animal", "total_difference", "within_term",
                     "composition_term", "interaction_term", "within_share",
                     "composition_share"]].to_dict("records")

    th17n = dec[(dec.cell_type == "Th17n") & (dec.score == "pathogenicity")]
    signs_agree = {}
    for label_col in LABELLINGS:
        sub = th17n[th17n.labelling == label_col]
        signs_agree[label_col] = {
            "within_sign_agrees_across_animals": bool(len(set(np.sign(sub.within_term))) == 1),
            "composition_sign_agrees_across_animals": bool(len(set(np.sign(sub.composition_term))) == 1)}

    results = {
        "schema": "wp_p03_glucose_decomposition/v1",
        "inputs_verified": verified,
        "unit": "cells within 8 libraries from 2 animals, crossed over all four conditions",
        "estimator": "Kitagawa: within uses pooled proportions, composition uses pooled within-programme means",
        "min_cells_per_programme_per_condition": MIN_CELLS,
        "declared_substitutions": [
            "programme labels are Wp-R1 Table S5 marker assignments, not the authors' Leiden clusters; the two "
            "available labellings replace the card's coarser/finer resolution sweep",
            "cell-cycle phase is not deposited; within-library proliferation-score terciles are the stratum",
        ],
        "primary_decomposition": summarise(dec),
        "stratified_decomposition": summarise(strat),
        "sign_consistency_across_animals": signs_agree,
        "exposure_note": ("Before freezing, library-level programme proportions and within-programme medians from the "
            "Wp-R1 outputs were recombined by hand, which recovered roughly +0.126 and +0.111 of the +0.133 and "
            "+0.109 observed differences and suggested composition would dominate. That arithmetic is recorded as "
            "exposure; no estimator, threshold or stratum was chosen in response to it."),
        "interpretation_limit": ("A decomposition on derived programme labels cannot establish that a cell changed "
            "state or that a programme was lost; both need lineage or time-resolved measurement, which this deposit "
            "does not contain. Programmes are defined from the same expression as the score, so a composition term "
            "is partly guaranteed by construction - this is the card's own clustering-artefact rival, and the "
            "informative content is how the term moves between labellings and strata, not its bare size. Two animals "
            "cap the result at descriptive."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
