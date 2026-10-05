#!/usr/bin/env python
"""Wp-R3: reproduce the Wang 2025 bulk EGCG and DHEA contrasts from deposited TPM.

Descriptive estimation. The deposit (GSE290297) supplies TPM only, with no animal
or culture field, so the LIBRARY is the unit and nothing here supports population
inference. Division gates Div.1 and Total are different gated populations of the
same cultures and are never pooled.

Endpoints, all frozen before execution:
  1. Per-gene moderated contrasts within each cell type and division gate:
     EGCG vs DMSO and DHEA vs Methanol (each inhibitor against its own solvent).
  2. The three-group gene partition from the paper: DMSO Th17p vs Th17n with
     BH <= 0.05 and |log2 FC| >= 1.5 defines Th17p-associated, Th17n-associated
     and non-significant genes.
  3. The logFC distribution of each group under each treatment, which is the
     published Figure 2C/2D claim in testable form.
  4. Signature derivation at the published thresholds (|log2 FC| >= log2(1.5),
     BH <= 0.05) and gene-level agreement against the authors' Table S3.

Method: log2(TPM + 1), limma-style moderated t with a shared empirical-Bayes
variance prior implemented locally (scipy/statsmodels only), because TPM is a
continuous normalised value and a count model would misstate its mean-variance
relationship. The implementation is checked against the authors' own Table S3
rather than asserted: the concordance table is a reported endpoint, not a filter.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import digamma, polygamma
from statsmodels.nonparametric.smoothers_lowess import lowess


SOLVENT = {"EGCG": "DMSO", "DHEA": "Methanol"}
PARTITION_ALPHA = 0.05
PARTITION_LFC = 1.5           # paper states log2 fold change >= 1.5 in absolute value
SIGNATURE_LFC = math.log2(1.5)  # paper states abs(logFC) >= log2(1.5)
SIGNATURE_ALPHA = 0.05


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def bh(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values, NaN-safe."""
    p = np.asarray(p, dtype=float)
    out = np.full(p.shape, np.nan)
    ok = ~np.isnan(p)
    q = p[ok]
    n = q.size
    if n == 0:
        return out
    order = np.argsort(q)
    ranked = q[order] * n / (np.arange(n) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    adj = np.empty(n)
    adj[order] = np.clip(ranked, 0, 1)
    out[ok] = adj
    return out


def squeeze_var(var: np.ndarray, df: int, covariate: np.ndarray | None = None) -> tuple[np.ndarray, float, float]:
    """Empirical-Bayes variance shrinkage, following limma's moderated t.

    Fits a scaled inverse-chi-square prior to the observed residual variances by
    matching the mean and variance of log(s^2) (Smyth 2004), then shrinks each
    gene's variance toward the prior. With ``covariate`` (average log expression)
    the prior location follows a lowess trend, as in limma-trend.
    """
    good = var > 0
    z = np.log(var[good])
    e = z - digamma(df / 2) + math.log(df / 2)
    trend = None
    if covariate is not None:
        fit = lowess(e, covariate[good], frac=0.3, it=3, return_sorted=False)
        trend = np.full(var.shape, np.nan)
        trend[good] = fit
        order = np.argsort(covariate[good])
        trend[~good] = np.interp(covariate[~good], covariate[good][order], fit[order])
        e = e - fit
    mean_e = e.mean()
    var_e = e.var(ddof=1)
    target = var_e - polygamma(1, df / 2)
    if target <= 0:
        df_prior = np.inf
        var_prior = math.exp(mean_e)
    else:
        # Solve polygamma(1, df_prior/2) = target by bisection on log scale.
        lo, hi = 1e-6, 1e6
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if polygamma(1, mid / 2) > target:
                lo = mid
            else:
                hi = mid
        df_prior = math.sqrt(lo * hi)
        var_prior = math.exp(mean_e + digamma(df_prior / 2) - math.log(df_prior / 2))
    if trend is not None:
        # Prior location per gene follows the trend; var_prior reports its median.
        scale = math.exp(mean_e + digamma(df_prior / 2) - math.log(df_prior / 2)) if np.isfinite(df_prior) \
            else math.exp(mean_e)
        prior_gene = np.exp(trend) * scale
        var_prior = float(np.median(prior_gene))
    else:
        prior_gene = np.full(var.shape, var_prior)
    if np.isinf(df_prior):
        post = prior_gene.copy()
    else:
        post = (df_prior * prior_gene + df * var) / (df_prior + df)
    post = np.where(good, post, prior_gene)
    return post, float(df_prior), float(var_prior)


def moderated_contrast(a: np.ndarray, b: np.ndarray, trend: bool = True) -> pd.DataFrame:
    """Two-group moderated t test on log2 TPM; a is treatment, b is comparator."""
    na, nb = a.shape[1], b.shape[1]
    df = na + nb - 2
    mean_a, mean_b = a.mean(axis=1), b.mean(axis=1)
    ss = ((a - mean_a[:, None]) ** 2).sum(axis=1) + ((b - mean_b[:, None]) ** 2).sum(axis=1)
    var = ss / df
    ave = np.concatenate([a, b], axis=1).mean(axis=1)
    post, df_prior, var_prior = squeeze_var(var, df, covariate=ave if trend else None)
    se = np.sqrt(post * (1 / na + 1 / nb))
    logfc = mean_a - mean_b
    total_df = df + (df_prior if np.isfinite(df_prior) else 1e6)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, logfc / se, np.nan)
    p = 2 * stats.t.sf(np.abs(t), total_df)
    frame = pd.DataFrame({"logFC": logfc, "AveExpr": ave,
                          "t": t, "P.Value": p, "adj.P.Val": bh(p)})
    frame.attrs["df_prior"] = df_prior
    frame.attrs["var_prior"] = var_prior
    frame.attrs["df_residual"] = df
    frame.attrs["n_treatment"] = na
    frame.attrs["n_comparator"] = nb
    return frame


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.data_root)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    man = json.loads((root / "acquisition_v1.json").read_text(encoding="utf-8"))
    man2 = json.loads((root / "acquisition_v2_supplements.json").read_text(encoding="utf-8"))
    verified = []
    for record in man["files"] + man2["files"]:
        path = root / record["file"]
        if not path.exists():
            continue
        verified.append({"file": record["file"], "recorded_sha256": record["sha256"],
                         "observed_sha256": sha256(path),
                         "match": sha256(path) == record["sha256"]})
    need = {"GSE290297_collected_inhibitors_tpm_4geo.csv.gz", "GSE290297_samples.soft.txt",
            "NIHMS2092659-supplement-3.xlsx"}
    present = {v["file"] for v in verified if v["match"]}
    if not need <= present:
        raise SystemExit(f"Missing or unverified required inputs: {sorted(need - present)}")

    # --- sample table from the GEO records (the only source of condition labels)
    text = (root / "GSE290297_samples.soft.txt").read_text(encoding="utf-8", errors="replace")
    samples, current = [], None
    for line in text.splitlines():
        if line.startswith("^SAMPLE"):
            current = {"gsm": line.split("=", 1)[1].strip()}
            samples.append(current)
        elif current is not None and line.startswith("!Sample_"):
            key, _, value = line[len("!Sample_"):].partition(" = ")
            current.setdefault(key.strip(), []).append(value.strip())
    rows = []
    for s in samples:
        fields = {}
        for item in s.get("characteristics_ch1", []):
            k, _, v = item.partition(": ")
            fields[k.strip().lower()] = v.strip()
        title = s["title"][0]
        rows.append({"gsm": s["gsm"], "title": title, "column": title.split("_")[0],
                     "cell_type": fields.get("cell type", ""), "treatment": fields.get("treatment", ""),
                     "divisions": fields.get("divisions", "")})
    design = pd.DataFrame(rows).set_index("column")

    with gzip.open(root / "GSE290297_collected_inhibitors_tpm_4geo.csv.gz", "rt") as handle:
        tpm = pd.read_csv(handle)
    tpm = tpm.rename(columns={tpm.columns[0]: "symbol"}).set_index("symbol")
    if sorted(tpm.columns) != sorted(design.index):
        raise SystemExit("TPM columns and sample records do not correspond one to one")
    design = design.loc[tpm.columns]
    expr_all = np.log2(tpm.to_numpy(dtype=float) + 1.0)
    genes_all = tpm.index.to_numpy()

    # Authors' Table S3 fixes the analysed gene universe per experiment. DMSO is
    # the EGCG experiment's solvent, so the Th17p-vs-Th17n partition (fitted on
    # DMSO libraries) uses the EGCG universe.
    s3 = pd.read_excel(root / "NIHMS2092659-supplement-3.xlsx", sheet_name="Table S3")
    s3 = s3.rename(columns={s3.columns[0]: "comparison"})
    universe = {drug: set(s3.loc[s3["comparison"].str.endswith("." + drug), "symbol"]) for drug in SOLVENT}

    # Frozen analysis variants. PRIMARY is declared first and is the only one that
    # feeds partitions, distributions and signatures; the others are reported
    # sensitivities. The unfiltered/no-trend variant is the specification seen in
    # the pre-freeze dry run and is retained rather than discarded.
    VARIANTS = {
        "primary_S3universe_trend": {"filter": "S3", "trend": True},
        "sens_S3universe_notrend": {"filter": "S3", "trend": False},
        "sens_unfiltered_notrend": {"filter": None, "trend": False},
    }

    def mask_for(cell_type, gate, treatment):
        return ((design["cell_type"] == cell_type) & (design["divisions"] == gate)
                & (design["treatment"] == treatment)).to_numpy()

    def fit(cell_type, gate, treatment, comparator, drug_universe, trend):
        if drug_universe is None:
            keep = np.ones(len(genes_all), dtype=bool)
        else:
            keep = np.isin(genes_all, list(universe[drug_universe]))
        a = expr_all[keep][:, mask_for(cell_type, gate, treatment)]
        b = expr_all[keep][:, mask_for(cell_type if comparator[0] is None else comparator[0], gate, comparator[1])]
        if a.shape[1] < 2 or b.shape[1] < 2:
            return None, {"status": "skipped_too_few_libraries", "n_treatment": int(a.shape[1]),
                          "n_comparator": int(b.shape[1])}
        res = moderated_contrast(a, b, trend=trend)
        res.insert(0, "symbol", genes_all[keep])
        info = {"status": "fitted", "n_genes": int(keep.sum()), "n_treatment": int(a.shape[1]),
                "n_comparator": int(b.shape[1]), "df_residual": res.attrs["df_residual"],
                "df_prior": res.attrs["df_prior"], "var_prior": res.attrs["var_prior"],
                "n_bh_0.05": int((res["adj.P.Val"] <= 0.05).sum())}
        return res, info

    variant_contrasts, meta = {}, []
    for vname, spec in VARIANTS.items():
        frames = []
        for cell_type in ("Th17n", "Th17p"):
            for gate in ("Div.1", "Total"):
                for drug, solvent in SOLVENT.items():
                    res, info = fit(cell_type, gate, drug, (None, solvent),
                                    drug if spec["filter"] == "S3" else None, spec["trend"])
                    info.update({"variant": vname, "contrast": f"{cell_type}.{gate}.{drug}"})
                    meta.append(info)
                    if res is not None:
                        res.insert(0, "contrast", f"{cell_type}.{gate}.{drug}")
                        frames.append(res)
        variant_contrasts[vname] = pd.concat(frames, ignore_index=True)
    primary = variant_contrasts["primary_S3universe_trend"]
    primary.to_csv(out / "bulk_contrasts.csv.gz", index=False, compression="gzip", lineterminator="\n")
    pd.DataFrame(meta).to_csv(out / "bulk_contrast_summary.csv", index=False, lineterminator="\n")

    # --- partition: DMSO Th17p vs Th17n, per gate, primary specification ------
    partitions, part_meta = {}, []
    for gate in ("Div.1", "Total"):
        keep = np.isin(genes_all, list(universe["EGCG"]))
        a = expr_all[keep][:, mask_for("Th17p", gate, "DMSO")]
        b = expr_all[keep][:, mask_for("Th17n", gate, "DMSO")]
        res = moderated_contrast(a, b, trend=True)
        res.insert(0, "symbol", genes_all[keep])
        sig = res["adj.P.Val"] <= PARTITION_ALPHA
        res["group"] = np.where(sig & (res["logFC"] >= PARTITION_LFC), "Th17p_associated",
                       np.where(sig & (res["logFC"] <= -PARTITION_LFC), "Th17n_associated", "not_significant"))
        res.to_csv(out / f"partition_{gate.replace('.', '')}.csv.gz", index=False, compression="gzip",
                   lineterminator="\n")
        partitions[gate] = pd.Series(res["group"].to_numpy(), index=res["symbol"].to_numpy())
        part_meta.append({"gate": gate, "n_th17p_libraries": int(a.shape[1]), "n_th17n_libraries": int(b.shape[1]),
                          "df_prior": res.attrs["df_prior"], "n_bh_0.05": int(sig.sum()),
                          **{k: int(v) for k, v in res["group"].value_counts().items()}})

    # --- logFC distribution per group per treatment (Figure 2C/2D form) -------
    dist_rows = []
    for name, sub in primary.groupby("contrast", sort=True):
        gate = "Div.1" if ".Div.1." in name else "Total"
        grp = partitions[gate].reindex(sub["symbol"]).to_numpy()
        for label in ("Th17p_associated", "Th17n_associated", "not_significant"):
            vals = sub["logFC"].to_numpy()[grp == label]
            if vals.size == 0:
                continue
            w = stats.wilcoxon(vals, zero_method="zsplit") if vals.size > 10 else None
            dist_rows.append({"contrast": name, "gene_group": label, "n_genes": int(vals.size),
                              "median_logFC": float(np.median(vals)), "mean_logFC": float(vals.mean()),
                              "q25": float(np.percentile(vals, 25)), "q75": float(np.percentile(vals, 75)),
                              "frac_up": float((vals > 0).mean()),
                              "wilcoxon_p_vs_zero": float(w.pvalue) if w is not None else float("nan")})
    dist = pd.DataFrame(dist_rows)
    dist["wilcoxon_bh"] = bh(dist["wilcoxon_p_vs_zero"].to_numpy())
    dist.to_csv(out / "group_logfc_distributions.csv", index=False, lineterminator="\n")

    # --- signatures at the published thresholds, primary specification -------
    sig_rows, sig_tables = [], []
    for name, sub in primary.groupby("contrast", sort=True):
        keep = (sub["adj.P.Val"] <= SIGNATURE_ALPHA) & (sub["logFC"].abs() >= SIGNATURE_LFC)
        sel = sub[keep]
        sig_rows.append({"signature": name, "n_genes": int(keep.sum()),
                         "n_up": int((sel["logFC"] > 0).sum()), "n_down": int((sel["logFC"] < 0).sum())})
        sig_tables.append(pd.DataFrame({"signature": name, "symbol": sel["symbol"],
                                        "sign": np.sign(sel["logFC"]).astype(int),
                                        "logFC": sel["logFC"], "adj.P.Val": sel["adj.P.Val"]}))
    pd.concat(sig_tables, ignore_index=True).to_csv(out / "signatures.csv", index=False, lineterminator="\n")
    pd.DataFrame(sig_rows).to_csv(out / "signature_summary.csv", index=False, lineterminator="\n")

    # --- agreement with the authors' Table S3, every variant, both gates ------
    conc_rows = []
    for vname, frame in variant_contrasts.items():
        for comparison, sub in s3.groupby("comparison", sort=True):
            cell_type, drug = comparison.split(".")
            for gate in ("Div.1", "Total"):
                ours = frame[frame["contrast"] == f"{cell_type}.{gate}.{drug}"]
                merged = sub.merge(ours, on="symbol", suffixes=("_source", "_ours"))
                if merged.empty:
                    continue
                src_sig = (merged["adj.P.Val_source"] <= SIGNATURE_ALPHA) & (merged["logFC_source"].abs() >= SIGNATURE_LFC)
                our_sig = (merged["adj.P.Val_ours"] <= SIGNATURE_ALPHA) & (merged["logFC_ours"].abs() >= SIGNATURE_LFC)
                both = src_sig & our_sig
                conc_rows.append({
                    "variant": vname, "source_comparison": comparison, "our_contrast": f"{cell_type}.{gate}.{drug}",
                    "n_source_genes": int(len(sub)), "n_shared_genes": int(len(merged)),
                    "pearson_logFC": float(merged["logFC_source"].corr(merged["logFC_ours"])),
                    "spearman_logFC": float(merged["logFC_source"].corr(merged["logFC_ours"], method="spearman")),
                    "pearson_t": float(merged["t_source"].corr(merged["t_ours"])),
                    "sign_agreement": float((np.sign(merged["logFC_source"]) == np.sign(merged["logFC_ours"])).mean()),
                    "n_source_signature": int(src_sig.sum()), "n_our_signature": int(our_sig.sum()),
                    "n_signature_overlap": int(both.sum()),
                    "jaccard_signature": float(both.sum() / max(1, (src_sig | our_sig).sum())),
                    "recall_of_source_signature": float(both.sum() / max(1, src_sig.sum())),
                    "sign_agreement_in_overlap": float((np.sign(merged.loc[both, "logFC_source"]) ==
                                                        np.sign(merged.loc[both, "logFC_ours"])).mean())
                    if both.any() else float("nan"),
                })
    concordance = pd.DataFrame(conc_rows)
    concordance.to_csv(out / "source_concordance.csv", index=False, lineterminator="\n")

    design_counts = design.groupby(["cell_type", "treatment", "divisions"]).size()
    results = {
        "schema": "wp_r3_bulk_contrasts/v1",
        "inputs_verified": verified,
        "unit": "library; the deposit declares no animal or culture field",
        "value_scale": "log2(TPM + 1); the deposit supplies TPM only",
        "n_libraries": int(expr_all.shape[1]), "n_genes_deposited": int(expr_all.shape[0]),
        "gene_universe": {drug: len(u) for drug, u in universe.items()},
        "design_counts": {"|".join(k): int(v) for k, v in design_counts.items()},
        "variants": VARIANTS, "primary_variant": "primary_S3universe_trend",
        "contrast_summary": meta, "partition_summary": part_meta,
        "group_logfc": dist.to_dict(orient="records"),
        "signature_summary": sig_rows, "source_concordance": conc_rows,
        "thresholds": {"partition_alpha": PARTITION_ALPHA, "partition_abs_log2fc": PARTITION_LFC,
                       "signature_alpha": SIGNATURE_ALPHA, "signature_abs_log2fc": SIGNATURE_LFC},
        "interpretation_limit": (
            "Library-level descriptive contrasts on deposited TPM. No animal or culture field exists, so these "
            "are not animal-level estimates and support no population inference. Division gates are different "
            "gated populations, never pooled. Agreement with Table S3 is reproduction of the source's own "
            "analysis, not independent replication."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True, default=str) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
