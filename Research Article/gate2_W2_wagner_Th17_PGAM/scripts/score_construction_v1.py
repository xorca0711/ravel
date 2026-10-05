#!/usr/bin/env python
"""Wp-P01: is the pathogenicity ranking a property of the cells or of the score?

Measurement validation on the Wp-R1 per-cell output. No new expression is read:
every score variant the card pre-specified is already a column of
`cell_scores.csv.gz`, or an algebraic function of two of them.

Frozen variant list (fixed before execution, from the card):
  reference        pro-inflammatory minus pro-regulatory, authors' Table S1 HVG flags
  all_genes        the same, using the full published module lists (no HVG filter)
  local_hvg        the same, using HVGs recomputed on this deposit
  arm_standardised the two arms z-scaled across the scored cells before subtraction
  proinflammatory  the pro-inflammatory arm alone
  proregulatory_neg the pro-regulatory arm alone, negated so that "more pathogenic"
                   stays the high end and the rank correlation is comparable
  methods_sign     the STAR Methods subtraction order (pro-regulatory minus
                   pro-inflammatory); its rank correlation with the reference is
                   exactly -1 by construction and is reported to make the
                   documented sign conflict explicit rather than silent

Endpoints: Spearman correlation of each variant against the reference, pooled and
per library; the fraction of cells changing score tercile; and two downstream
statements re-evaluated under every variant - whether N1 remains the lowest-median
programme in each Th17n library, and whether the pathogenicity score still rises
at 1 mM glucose in each animal-paired comparison.

Unit: cells, nested in 8 libraries and 2 animals. This card makes no population
claim: it asks whether a measurement is internally stable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REFERENCE = "reference"
MIN_PROGRAMME_CELLS = 20


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def zscore(x: np.ndarray) -> np.ndarray:
    sd = np.nanstd(x)
    return (x - np.nanmean(x)) / sd if sd > 0 else np.zeros_like(x)


def tercile(x: np.ndarray) -> np.ndarray:
    q1, q2 = np.nanquantile(x, [1 / 3, 2 / 3])
    return np.digitize(x, [q1, q2])


def build_variants(df: pd.DataFrame) -> dict[str, np.ndarray]:
    pi = df["proinflammatory_authors"].to_numpy()
    pr = df["proregulatory_authors"].to_numpy()
    return {
        REFERENCE: df["pathogenicity_authors"].to_numpy(),
        "all_genes": df["pathogenicity_all"].to_numpy(),
        "local_hvg": df["pathogenicity_local"].to_numpy(),
        "arm_standardised": zscore(pi) - zscore(pr),
        "proinflammatory": pi,
        "proregulatory_neg": -pr,
        "methods_sign": -df["pathogenicity_authors"].to_numpy(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--r1-run", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    r1, out = Path(args.r1_run), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    verified = {"wp_singlecell_reproduction_v1/cell_scores.csv.gz": sha256(r1 / "cell_scores.csv.gz")}
    cells = pd.read_csv(r1 / "cell_scores.csv.gz")

    scopes = {"Th17n": cells[cells.cell_type == "Th17n"].reset_index(drop=True),
              "Th17p": cells[cells.cell_type == "Th17p"].reset_index(drop=True),
              "all_cells": cells.reset_index(drop=True)}

    # --- 1. rank agreement and tercile movement ----------------------------
    rows = []
    for scope, df in scopes.items():
        variants = build_variants(df)
        ref = variants[REFERENCE]
        ref_t = tercile(ref)
        for name, v in variants.items():
            if name == REFERENCE:
                continue
            rows.append({"scope": scope, "library": "pooled", "variant": name, "n_cells": len(df),
                         "spearman_vs_reference": float(stats.spearmanr(ref, v).statistic),
                         "pearson_vs_reference": float(np.corrcoef(ref, v)[0, 1]),
                         "fraction_changing_tercile": float((tercile(v) != ref_t).mean())})
        for lib, sub in df.groupby("library"):
            sv = build_variants(sub.reset_index(drop=True))
            sref = sv[REFERENCE]
            sref_t = tercile(sref)
            for name, v in sv.items():
                if name == REFERENCE:
                    continue
                rows.append({"scope": scope, "library": str(lib), "variant": name, "n_cells": len(sub),
                             "spearman_vs_reference": float(stats.spearmanr(sref, v).statistic),
                             "pearson_vs_reference": float(np.corrcoef(sref, v)[0, 1]),
                             "fraction_changing_tercile": float((tercile(v) != sref_t).mean())})
    agreement = pd.DataFrame(rows)
    agreement.to_csv(out / "variant_agreement.csv", index=False, lineterminator="\n")

    # --- 2. arm independence -----------------------------------------------
    arm_rows = []
    for scope, df in scopes.items():
        for lib, sub in list(df.groupby("library")) + [("pooled", df)]:
            pi = sub["proinflammatory_authors"].to_numpy()
            pr = sub["proregulatory_authors"].to_numpy()
            arm_rows.append({"scope": scope, "library": str(lib), "n_cells": len(sub),
                             "spearman_arms": float(stats.spearmanr(pi, pr).statistic),
                             "sd_proinflammatory": float(np.std(pi)),
                             "sd_proregulatory": float(np.std(pr)),
                             "sd_ratio_prorg_over_proinf": float(np.std(pr) / np.std(pi)) if np.std(pi) > 0 else np.nan})
    pd.DataFrame(arm_rows).to_csv(out / "arm_independence.csv", index=False, lineterminator="\n")

    # --- 3. downstream statement A: is N1 still the lowest programme? -------
    n1_rows = []
    th17n = scopes["Th17n"]
    for label_col in ["programme", "programme_excl_overlap"]:
        for lib, sub in th17n.groupby("library"):
            variants = build_variants(sub.reset_index(drop=True))
            labels = sub[label_col].to_numpy()
            keep = [p for p in np.unique(labels) if (labels == p).sum() >= MIN_PROGRAMME_CELLS]
            for name, v in variants.items():
                med = {p: float(np.median(v[labels == p])) for p in keep}
                if "N1" not in med or len(med) < 2:
                    continue
                others = [m for p, m in med.items() if p != "N1"]
                n1_rows.append({"labelling": label_col, "library": str(lib), "variant": name,
                                "n_programmes": len(med), "N1_median": med["N1"],
                                "min_other_median": min(others),
                                "N1_is_lowest": bool(med["N1"] < min(others))})
    n1 = pd.DataFrame(n1_rows)
    n1.to_csv(out / "n1_lowest_by_variant.csv", index=False, lineterminator="\n")

    # --- 4. downstream statement B: glucose direction under each variant ----
    glu_rows = []
    for scope in ["Th17n", "Th17p"]:
        df = scopes[scope]
        variants = build_variants(df)
        for name, v in variants.items():
            work = df.assign(_v=v)
            for animal, sub in work.groupby("animal"):
                lo = sub.loc[sub.glucose == "1mM", "_v"]
                hi = sub.loc[sub.glucose == "25mM", "_v"]
                if len(lo) == 0 or len(hi) == 0:
                    continue
                glu_rows.append({"scope": scope, "variant": name, "animal": str(animal),
                                 "mean_1mM": float(lo.mean()), "mean_25mM": float(hi.mean()),
                                 "low_minus_high": float(lo.mean() - hi.mean()),
                                 "n_low": int(len(lo)), "n_high": int(len(hi))})
    glu = pd.DataFrame(glu_rows)
    glu.to_csv(out / "glucose_direction_by_variant.csv", index=False, lineterminator="\n")

    pos = (glu[glu.scope == "Th17n"].groupby("variant")["low_minus_high"]
           .agg(n_pairs="size", n_positive=lambda s: int((s > 0).sum()),
                min_difference="min", max_difference="max").reset_index())

    pooled = agreement[(agreement.library == "pooled") & (agreement.scope == "Th17n")]
    results = {
        "schema": "wp_p01_score_construction/v1",
        "inputs_verified": verified,
        "unit": "cell, nested in 8 libraries and 2 animals; no population claim",
        "n_cells": {k: int(len(v)) for k, v in scopes.items()},
        "variants": list(build_variants(scopes["Th17n"]).keys()),
        "pooled_Th17n_agreement": pooled[["variant", "spearman_vs_reference",
                                          "fraction_changing_tercile"]].to_dict("records"),
        "per_library_spearman_range": {
            v: [float(s.min()), float(s.max())] for v, s in
            agreement[(agreement.scope == "Th17n") & (agreement.library != "pooled")]
            .groupby("variant")["spearman_vs_reference"]},
        "n1_lowest_counts": (n1.groupby(["labelling", "variant"])["N1_is_lowest"]
                             .agg(n_checks="size", n_lowest="sum").reset_index().to_dict("records")),
        "glucose_direction_Th17n": pos.to_dict("records"),
        "downstream_not_testable": ("Per-cell Compass reaction scores do not exist: Wp-R2 scored micropools and did "
            "not save pool membership, and the pooling is not bit-reproducible. The card's reaction-ranking "
            "consequence therefore cannot be re-evaluated under these variants; the two downstream statements above "
            "are the ones this deposit can condition."),
        "interpretation_limit": ("Internal stability of a measurement computed on one deposit's cells. A stable "
            "ranking does not show that the score measures pathogenicity, which is a functional claim. Variants "
            "differ only in gene selection, weighting and sign; they share the same expression matrix, so agreement "
            "between them is not independent evidence."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
