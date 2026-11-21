"""Execute the prespecified biochemical–native comparisons."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from rank_models import CLASSES, estimate, load_endpoints, omission_summary, save
from figures import binding_figure


def main(out):
    panel, endpoints = load_endpoints()
    records, omissions, pairs = [], [], []
    for e in endpoints.values():
        meta = dict(endpoint=e.key, model=e.model, window=e.window, control_n=e.control.shape[1],
                    recovered_n=e.recovered.shape[1], nominal_loci=len(panel))
        for predictor in ["increment", "fold_ratio", "JUN_raw", "JUNFOXP1_raw"]:
            x = panel[predictor]
            def fit(check, y, cov, mask=None, subgroup="all", held="none", details=False):
                result, data = estimate(x, y, cov, mask, details=details)
                records.append(dict(**meta, predictor=predictor, check=check, subgroup=subgroup,
                                    held_control=held, control_n_in_difference=(meta["control_n"]-1
                                    if check == "independent_control_split" else meta["control_n"]
                                    if check not in ("control_only", "recovered_only") else np.nan),
                                    covariates=",".join(name for name, _ in cov) or "intercept", **result))
                return result, data

            main_fit, points = fit("geometry_adjusted", e.delta, e.cov, details=True)
            fit("unadjusted", e.delta, [])
            for i, offset in enumerate(points["index"]):
                pairs.append(dict(endpoint=e.key, predictor=predictor, locus=panel.index[offset],
                                  motif_class=panel.motif_class.iloc[offset], width_bp=e.geometry.width_bp.iloc[offset],
                                  reference_CpGs=e.geometry.reference_CpGs.iloc[offset],
                                  control_mean=e.baseline.iloc[offset], recovered_mean=e.target.iloc[offset],
                                  **{k: v[i] for k, v in points.items() if k != "index"}))
            if predictor not in ("increment", "fold_ratio"):
                continue
            for label in CLASSES:
                fit("within_class", e.delta, [], panel.motif_class.eq(label), subgroup=label)
            fit("control_only", e.baseline, e.cov)
            fit("recovered_only", e.target, e.cov)
            fit("coupled_control_adjustment", e.delta, e.cov + [("mean_control", e.baseline)])
            for specimen, delta, held in e.splits():
                fit("independent_control_split", delta, e.cov + [("held_control", held)], held=specimen)
            if e.model == "epithelial ATAC":
                fit("per_kb", 1000 * e.delta / e.geometry.width_bp, e.cov)
            else:
                fit("common_CpG_adjustment", e.delta, e.cov + [("common_CpGs", e.geometry.common_CpGs)])
            attrs = dict(**meta, predictor=predictor, full_rho=main_fit["rho"])
            valid = x.notna() & e.delta.notna()
            for locus in panel.index[valid]:
                result, _ = estimate(x, e.delta, e.cov, panel.index != locus)
                omissions.append(dict(**attrs, omission="locus", unit=locus, arm="none",
                                      remaining_controls=meta["control_n"], remaining_recovered=meta["recovered_n"], **result))
            for arm, specimen, delta in e.omissions():
                result, _ = estimate(x, delta, e.cov)
                omissions.append(dict(**attrs, omission="mouse_or_line", unit=specimen, arm=arm,
                                      remaining_controls=meta["control_n"] - int(arm == "control"),
                                      remaining_recovered=meta["recovered_n"] - int(arm == "recovered"), **result))
    results, omit, point = map(pd.DataFrame, (records, omissions, pairs))
    ranges = omission_summary(omit, ["endpoint", "predictor"])
    for df, name in [(results, "associations.tsv"), (omit, "omissions.tsv.gz"), (ranges, "omission_ranges.tsv"),
                     (point, "locus_pairs.tsv.gz")]:
        save(df, out, name)
    binding_figure(results, point, ranges, out)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
