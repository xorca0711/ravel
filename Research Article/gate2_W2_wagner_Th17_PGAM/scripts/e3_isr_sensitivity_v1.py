#!/usr/bin/env python
"""Wp-E3 sensitivity: does the ISR shift survive removing its serine-pathway genes?

Wp-E3 reported that under EGCG in Th17n division-1 libraries the integrated
stress response is the most downward-shifted of fifteen declared programmes
(centred median -0.491, outside its expression-matched null at p = 0.000) while
serine/one-carbon also falls (-0.299, p = 0.001). Those two statements are not
independent: the declared ISR list and the declared serine/one-carbon list share
members, because canonical ATF4 target genes include serine-pathway enzymes.

Before the ISR observation can be used as a premise anywhere - in particular in
the Wp-P02 branch card, where it bears on the paper's stress-driven mechanism -
the shift has to be shown to survive removal of the shared genes. Otherwise
"the stress response falls" and "serine synthesis falls" may be the same few
genes counted twice.

This entrypoint recomputes both programmes with the intersection removed, under
the identical construction Wp-E3 used (same frozen input tables, same global
shift definition, same seed, same number of draws, same expression-decile
null), and additionally emits every member gene's centred log2 fold change so
the medians can be checked by hand.

Frozen design, fixed before any reduced-set value was computed:
  1. The shared genes are not hardcoded. They are computed as the intersection
     of the two sets as Wp-E3 actually scored them, read from that run's own
     committed membership table.
  2. Four variants per arm: ISR full, ISR minus shared, serine full, serine
     minus shared. The full variants are recomputations and must reproduce the
     Wp-E3 values exactly; the run asserts this and fails if they do not.
  3. The statistic, the null and the global-shift base are Wp-E3's, unchanged.
  4. All four division-1 arms are reported, not only the focal one.

Stop rule, fixed here before the reduced sets were computed: if the Th17n EGCG
ISR shift does not remain outside its expression-matched null after the shared
genes are removed, the ISR observation cannot enter the Wp-P02 card as evidence
about cellular stress, and the card must record that instead. The result is
reported in either direction.

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

SEED = 20261005
N_DRAWS = 1000
N_DECILES = 10
ARMS = ["Th17n.Div.1.EGCG", "Th17n.Div.1.DHEA", "Th17p.Div.1.EGCG", "Th17p.Div.1.DHEA"]
PAIR = ("integrated_stress_response", "serine_one_carbon")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def expression_matched_null(d, pool_by_decile, dec_of, members, base, rng):
    """Wp-E3's null, unchanged: random genes with the set's own decile counts."""
    counts = pd.Series([dec_of[g] for g in members]).value_counts().to_dict()
    draws = np.empty(N_DRAWS)
    for b in range(N_DRAWS):
        picked = []
        for k, n in counts.items():
            avail = pool_by_decile.get(k, np.array([]))
            if len(avail) == 0:
                continue
            picked.extend(rng.choice(avail, min(n, len(avail)), replace=False))
        draws[b] = float(np.median(d.loc[picked, "logFC"])) - base
    return draws


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    runs, out = Path(args.runs_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    src = {"bulk_contrasts": runs / "wp_bulk_contrasts_v1/bulk_contrasts.csv.gz",
           "bulk_partition": runs / "wp_bulk_contrasts_v1/partition_Div1.csv.gz",
           "e3_membership": runs / "wp_e3_global_shift_v1/programme_membership.csv",
           "e3_shift": runs / "wp_e3_global_shift_v1/programme_shift.csv"}
    verified = {k: sha256(v) for k, v in src.items()}
    contrasts = pd.read_csv(src["bulk_contrasts"])
    partition = pd.read_csv(src["bulk_partition"]).set_index("symbol")["group"]
    membership = pd.read_csv(src["e3_membership"])
    e3_shift = pd.read_csv(src["e3_shift"])

    sets = {name: sorted(membership.loc[membership.programme == name, "symbol"])
            for name in PAIR}
    shared = sorted(set(sets[PAIR[0]]) & set(sets[PAIR[1]]))
    variants = {
        f"{PAIR[0]}__full": sets[PAIR[0]],
        f"{PAIR[0]}__minus_shared": [g for g in sets[PAIR[0]] if g not in shared],
        f"{PAIR[1]}__full": sets[PAIR[1]],
        f"{PAIR[1]}__minus_shared": [g for g in sets[PAIR[1]] if g not in shared],
        "shared_genes_only": shared,
    }

    rng = np.random.default_rng(SEED)
    rows, gene_rows = [], []
    for arm in ARMS:
        d = contrasts[contrasts.contrast == arm].set_index("symbol")
        d = d[np.isfinite(d.logFC) & np.isfinite(d.AveExpr)]
        grp = partition.reindex(d.index)
        base = float(d.loc[grp == "not_significant", "logFC"].median())
        dec = pd.qcut(d.AveExpr.rank(method="first"), N_DECILES,
                      labels=False, duplicates="drop").astype(int)
        dec_of = dict(zip(d.index, dec))
        pool_by_decile = {k: np.array([g for g in d.index if dec_of[g] == k])
                          for k in range(int(dec.max()) + 1)}

        for variant, members in variants.items():
            members = [g for g in members if g in d.index]
            obs = float(d.loc[members, "logFC"].median()) - base
            draws = expression_matched_null(d, pool_by_decile, dec_of, members, base, rng)
            rows.append({
                "contrast": arm, "variant": variant, "n_genes": len(members),
                "removed_genes": ";".join(shared) if variant.endswith("minus_shared") else "",
                "observed_centred_median": obs,
                "expr_null_mean": float(draws.mean()),
                "expr_null_q025": float(np.quantile(draws, .025)),
                "expr_null_q975": float(np.quantile(draws, .975)),
                "expr_null_p": float((np.abs(draws - draws.mean())
                                      >= abs(obs - draws.mean())).mean()),
                "median_AveExpr_of_set": float(d.loc[members, "AveExpr"].median()),
                "global_shift_base": base,
            })
        for name in PAIR:
            for g in sets[name]:
                if g not in d.index:
                    continue
                gene_rows.append({"contrast": arm, "programme": name, "symbol": g,
                                  "is_shared": g in shared,
                                  "logFC": float(d.loc[g, "logFC"]),
                                  "centred_logFC": float(d.loc[g, "logFC"]) - base,
                                  "AveExpr": float(d.loc[g, "AveExpr"]),
                                  "adj_P_Val": float(d.loc[g, "adj.P.Val"])
                                  if "adj.P.Val" in d.columns else float("nan")})

    sens = pd.DataFrame(rows)
    sens.to_csv(out / "isr_serine_sensitivity.csv", index=False, lineterminator="\n")
    pd.DataFrame(gene_rows).to_csv(out / "member_gene_logfc.csv", index=False,
                                   lineterminator="\n")

    # the full variants must reproduce Wp-E3 exactly, or the recomputation is wrong
    recomputation_check = {}
    for name in PAIR:
        for arm in ARMS:
            ours = float(sens.loc[(sens.contrast == arm) & (sens.variant == f"{name}__full"),
                                  "observed_centred_median"].iloc[0])
            theirs = float(e3_shift.loc[(e3_shift.contrast == arm) & (e3_shift.programme == name),
                                        "observed_centred_median"].iloc[0])
            recomputation_check[f"{arm}|{name}"] = {"ours": ours, "wp_e3": theirs,
                                                    "abs_diff": abs(ours - theirs)}
    worst = max(v["abs_diff"] for v in recomputation_check.values())
    if worst > 1e-12:
        raise SystemExit(f"recomputation of the full sets does not match Wp-E3 (worst {worst})")

    focal = ARMS[0]
    def row(variant):
        r = sens.loc[(sens.contrast == focal) & (sens.variant == variant)].iloc[0]
        return {"n_genes": int(r.n_genes), "centred_median": float(r.observed_centred_median),
                "expr_null_q025": float(r.expr_null_q025),
                "expr_null_q975": float(r.expr_null_q975),
                "expr_null_p": float(r.expr_null_p)}
    isr_reduced = row(f"{PAIR[0]}__minus_shared")
    survives = bool(isr_reduced["expr_null_p"] <= 0.05 and isr_reduced["centred_median"] < 0)

    results = {
        "schema": "wp_e3_isr_sensitivity/v1",
        "inputs_verified": verified,
        "unit": "library; GSE290297 declares no animal field",
        "question": ("Does the Wp-E3 integrated-stress-response shift survive removing the genes "
                     "it shares with the serine/one-carbon set, and vice versa?"),
        "shared_genes": shared,
        "n_shared": len(shared),
        "focal_arm": focal,
        "focal": {v: row(v) for v in variants},
        "isr_shift_survives_removal_in_focal_arm": survives,
        "stop_rule_outcome": (
            "ISR shift remains outside its expression-matched null after removing the shared "
            "genes; the observation may be used as evidence about cellular stress, within the "
            "transcript-level limits below." if survives else
            "ISR shift does not remain outside its expression-matched null after removing the "
            "shared genes; the observation cannot be used as evidence about cellular stress and "
            "Wp-P02 must record that it is carried by the serine-pathway members."),
        "recomputation_check": recomputation_check,
        "all_arms": sens.to_dict("records"),
        "thresholds": {"n_draws": N_DRAWS, "seed": SEED, "n_deciles": N_DECILES},
        "interpretation_limit": (
            "Library-level descriptive readout of frozen contrast tables on deposited TPM, with "
            "no animal field, so no animal-level or causal inference. Removing shared members "
            "makes the two gene sets disjoint; it does not make the programmes biologically "
            "independent, because ATF4 output and serine synthesis are coupled in the biology "
            "as well as in the lists. Transcript abundance of ISR target genes is a downstream "
            "proxy for a response set by eIF2-alpha phosphorylation and ATF4 translation, so no "
            "value here measures stress-response activity."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
