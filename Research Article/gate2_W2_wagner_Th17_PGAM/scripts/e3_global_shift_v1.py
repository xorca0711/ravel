#!/usr/bin/env python
"""Wp-E3: which genes carry the non-selective Th17n EGCG shift?

Wp-R3 found that EGCG in Th17n raises the pro-inflammatory and pro-regulatory
gene groups by similar amounts on top of a transcriptome-wide upward shift
(centred medians +0.15 and +0.23, between-group Mann-Whitney p = 0.97). The
question this opens is what that global shift *is*: a coherent biological
programme, or a compositional consequence of TPM renormalisation.

The pre-RQ checkpoint excluded this analysis on the ground that a negative
result would be uninterpretable, because TPM renormalisation alone can produce a
whole-transcriptome shift and the deposit has neither counts nor spike-ins. That
exclusion was wrong, and this entrypoint is the corrected version: a
compositional shift is a function of a gene's expression level, so a null drawn
to match the gene set's own expression-decile composition absorbs it. A
programme that exceeds that null is not a renormalisation artefact, and a
programme that does not is genuinely uninformative rather than merely confounded.

Frozen design:
  1. Programme gene sets are declared below, before any score is computed. They
     are prefix-based where the family is defined by nomenclature (ribosomal
     proteins, OXPHOS subunits) and explicit lists otherwise.
  2. Each set's statistic is the median centred log2 fold change: its median
     minus the median of the genes in neither pathogenicity group, which is the
     global shift being explained.
  3. Two nulls per set, both 1,000 draws, seed 20261005:
       size-matched      random genes, same count
       expression-matched random genes, same count AND same AveExpr-decile
                         composition - the one that answers the confound
  4. The shift is additionally profiled against expression level directly: the
     median log2 fold change per AveExpr decile, with Spearman correlation
     between decile rank and median shift. A monotone relation is the signature
     of a compositional effect; a flat profile with programme-specific excursions
     is the signature of a biological one.
  5. Reported for all four division-1 arms, so Th17n EGCG - the condition the
     paper's thesis rests on - is read against the other three rather than alone.

Unit: library. GSE290297 declares no animal field, so nothing here is
animal-level inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261005
N_DRAWS = 1000
N_DECILES = 10

EXPLICIT_SETS: dict[str, list[str]] = {
    "integrated_stress_response": [
        "ATF4", "DDIT3", "TRIB3", "SESN2", "CHAC1", "ASNS", "ATF3", "PPP1R15A",
        "EIF4EBP1", "NUPR1", "CEBPB", "VEGFA", "SLC7A11", "MTHFD2", "SHMT2"],
    "unfolded_protein_response": [
        "XBP1", "HSPA5", "DNAJB9", "HERPUD1", "EDEM1", "SEC61A1", "PDIA4",
        "PDIA6", "CALR", "CANX", "HSP90B1", "ERN1", "ATF6"],
    "nrf2_oxidative_stress": [
        "NQO1", "HMOX1", "GCLC", "GCLM", "TXNRD1", "SRXN1", "GSR", "PRDX1",
        "GPX1", "CAT", "SOD1", "SOD2", "TXN1"],
    "hypoxia_hif": [
        "SLC2A1", "PDK1", "BNIP3", "ANKRD37", "EGLN3", "P4HA1", "ALDOC",
        "ADM", "NDRG1", "HIF1A"],
    "glycolysis": [
        "HK1", "HK2", "GPI1", "PFKL", "PFKP", "PFKM", "ALDOA", "TPI1", "GAPDH",
        "PGK1", "PGAM1", "ENO1", "PKM", "LDHA", "SLC16A3"],
    "cell_cycle": [
        "MKI67", "TOP2A", "PCNA", "TYMS", "CCNB1", "CDK1", "UBE2C", "BIRC5",
        "STMN1", "RRM2", "CCNA2", "CDC20", "PLK1", "AURKB", "MCM2", "MCM5"],
    "amino_acid_transport": [
        "SLC7A5", "SLC3A2", "SLC1A5", "SLC38A1", "SLC38A2", "SLC7A1", "SLC7A11",
        "SLC6A9", "SLC1A4"],
    "serine_one_carbon": [
        "PHGDH", "PSAT1", "PSPH", "SHMT1", "SHMT2", "MTHFD1", "MTHFD2",
        "MTHFD1L", "MTR", "MAT2A", "AHCY", "DNMT1", "DNMT3A", "ALDH1L2"],
    "cholesterol_srebp": [
        "HMGCR", "HMGCS1", "SQLE", "FDFT1", "IDI1", "LSS", "MVD", "MVK",
        "INSIG1", "SREBF2", "DHCR7", "CYP51"],
    "th17_effector": [
        "IL17A", "IL17F", "IL23R", "IL22", "CSF2", "RORC", "BATF", "IL1R1",
        "CCR6", "IL21"],
}
PREFIX_SETS: dict[str, tuple[str, ...]] = {
    "ribosomal_proteins": ("RPL", "RPS"),
    "oxphos_subunits": ("NDUF", "COX", "ATP5", "UQCR", "SDH"),
    "mitochondrial_encoded": ("MT-",),
    "histones": ("HIST", "H2A", "H2B", "H3C", "H4C"),
    "heat_shock": ("HSPA", "HSPB", "HSPH", "DNAJ"),
}
ARMS = ["Th17n.Div.1.EGCG", "Th17n.Div.1.DHEA", "Th17p.Div.1.EGCG", "Th17p.Div.1.DHEA"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_sets(symbols: pd.Index) -> dict[str, list[str]]:
    sets = {k: sorted(set(v) & set(symbols)) for k, v in EXPLICIT_SETS.items()}
    for name, prefixes in PREFIX_SETS.items():
        sets[name] = sorted(s for s in symbols if any(s.startswith(p) for p in prefixes))
    return sets


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    runs, out = Path(args.runs_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    src = {"bulk_contrasts": runs / "wp_bulk_contrasts_v1/bulk_contrasts.csv.gz",
           "bulk_partition": runs / "wp_bulk_contrasts_v1/partition_Div1.csv.gz",
           "group_distributions": runs / "wp_bulk_contrasts_v1/group_logfc_distributions.csv"}
    verified = {k: sha256(v) for k, v in src.items()}
    contrasts = pd.read_csv(src["bulk_contrasts"])
    partition = pd.read_csv(src["bulk_partition"]).set_index("symbol")["group"]

    rng = np.random.default_rng(SEED)
    set_rows, decile_rows, membership = [], [], []

    for arm in ARMS:
        d = contrasts[contrasts.contrast == arm].set_index("symbol")
        d = d[np.isfinite(d.logFC) & np.isfinite(d.AveExpr)]
        grp = partition.reindex(d.index)
        base = float(d.loc[grp == "not_significant", "logFC"].median())

        # expression deciles over the whole fitted universe
        dec = pd.qcut(d.AveExpr.rank(method="first"), N_DECILES,
                      labels=False, duplicates="drop").astype(int)
        by_dec = (d.assign(decile=dec).groupby("decile")
                  .agg(n_genes=("logFC", "size"), median_logFC=("logFC", "median"),
                       mean_AveExpr=("AveExpr", "mean")).reset_index())
        by_dec["centred_median_logFC"] = by_dec.median_logFC - base
        by_dec.insert(0, "contrast", arm)
        sp = stats.spearmanr(by_dec.decile, by_dec.median_logFC)
        decile_rows.append(by_dec)

        sets = build_sets(d.index)
        pool = d.index.to_numpy()
        dec_of = dict(zip(d.index, dec))
        by_decile_pool: dict[int, np.ndarray] = {
            k: np.array([g for g in pool if dec_of[g] == k]) for k in range(int(dec.max()) + 1)}

        for name, members in sets.items():
            members = [g for g in members if g in d.index]
            if len(members) < 5:
                continue
            obs = float(d.loc[members, "logFC"].median()) - base
            # size-matched null
            size_draws = np.array([float(np.median(d.loc[rng.choice(pool, len(members), replace=False), "logFC"])) - base
                                   for _ in range(N_DRAWS)])
            # expression-matched null: same decile composition
            counts = pd.Series([dec_of[g] for g in members]).value_counts().to_dict()
            expr_draws = np.empty(N_DRAWS)
            for b in range(N_DRAWS):
                picked = []
                for k, n in counts.items():
                    avail = by_decile_pool.get(k, np.array([]))
                    if len(avail) == 0:
                        continue
                    picked.extend(rng.choice(avail, min(n, len(avail)), replace=False))
                expr_draws[b] = float(np.median(d.loc[picked, "logFC"])) - base
            set_rows.append({
                "contrast": arm, "programme": name, "n_genes": len(members),
                "observed_centred_median": obs,
                "size_null_q025": float(np.quantile(size_draws, .025)),
                "size_null_q975": float(np.quantile(size_draws, .975)),
                "size_null_p": float((np.abs(size_draws - size_draws.mean()) >= abs(obs - size_draws.mean())).mean()),
                "expr_null_mean": float(expr_draws.mean()),
                "expr_null_q025": float(np.quantile(expr_draws, .025)),
                "expr_null_q975": float(np.quantile(expr_draws, .975)),
                "expr_null_p": float((np.abs(expr_draws - expr_draws.mean()) >= abs(obs - expr_draws.mean())).mean()),
                "median_AveExpr_of_set": float(d.loc[members, "AveExpr"].median()),
                "median_AveExpr_of_universe": float(d.AveExpr.median()),
                "n_in_pathogenicity_groups": int((partition.reindex(members) != "not_significant").sum()),
                "global_shift_base": base,
                "decile_spearman_rank_vs_median": float(sp.statistic),
                "decile_spearman_p": float(sp.pvalue),
            })
            if arm == ARMS[0]:
                membership.append(pd.DataFrame({"programme": name, "symbol": members}))

    sets_df = pd.DataFrame(set_rows)
    sets_df.to_csv(out / "programme_shift.csv", index=False, lineterminator="\n")
    pd.concat(decile_rows, ignore_index=True).to_csv(out / "expression_decile_profile.csv",
                                                     index=False, lineterminator="\n")
    pd.concat(membership, ignore_index=True).to_csv(out / "programme_membership.csv",
                                                    index=False, lineterminator="\n")

    focal = sets_df[sets_df.contrast == ARMS[0]].sort_values("observed_centred_median")
    exceed = focal[focal.expr_null_p <= 0.05]
    dprof = pd.concat(decile_rows, ignore_index=True)
    results = {
        "schema": "wp_e3_global_shift/v1",
        "inputs_verified": verified,
        "unit": "library; GSE290297 declares no animal field",
        "question": "What carries the transcriptome-wide upward shift under EGCG in Th17n division-1 libraries?",
        "global_shift_per_arm": {a: float(sets_df.loc[sets_df.contrast == a, "global_shift_base"].iloc[0])
                                 for a in ARMS if (sets_df.contrast == a).any()},
        "decile_trend_per_arm": {
            a: {"spearman_decile_vs_median": float(sets_df.loc[sets_df.contrast == a,
                                                               "decile_spearman_rank_vs_median"].iloc[0]),
                "centred_median_lowest_decile": float(dprof[(dprof.contrast == a) & (dprof.decile == dprof.decile.min())]
                                                      ["centred_median_logFC"].iloc[0]),
                "centred_median_highest_decile": float(dprof[(dprof.contrast == a) & (dprof.decile == dprof.decile.max())]
                                                       ["centred_median_logFC"].iloc[0])}
            for a in ARMS if (sets_df.contrast == a).any()},
        "focal_arm": ARMS[0],
        "focal_programmes_exceeding_expression_matched_null": exceed[
            ["programme", "n_genes", "observed_centred_median", "expr_null_q025",
             "expr_null_q975", "expr_null_p"]].to_dict("records"),
        "focal_all_programmes": focal[["programme", "n_genes", "observed_centred_median",
                                       "size_null_p", "expr_null_p"]].to_dict("records"),
        "thresholds": {"n_draws": N_DRAWS, "seed": SEED, "n_deciles": N_DECILES,
                       "min_genes_per_set": 5},
        "why_the_expression_matched_null": (
            "A compositional consequence of TPM renormalisation is a function of a gene's expression level, so a null "
            "drawn with the gene set's own AveExpr-decile composition absorbs it. A programme exceeding that null is "
            "not a renormalisation artefact; a programme inside it is uninformative rather than confounded. This is "
            "the correction to the pre-RQ checkpoint's reason for excluding this analysis."),
        "interpretation_limit": (
            "Library-level descriptive readout of a frozen contrast table on deposited TPM, with no animal field, so "
            "no animal-level or causal inference. Programme membership is a declared gene list, not a measured "
            "pathway activity, and a transcript-level shift is not flux or protein. The expression-matched null "
            "addresses the compositional confound but cannot exclude a genuine global biological response that "
            "happens to be expression-dependent."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
