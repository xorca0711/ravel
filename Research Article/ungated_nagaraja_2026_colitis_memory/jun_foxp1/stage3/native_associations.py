"""Secondary genomic-locus comparison of history differences in distinct cohorts."""
from pathlib import Path
import sys

import pandas as pd

from rank_models import CLASSES, estimate, load_endpoints, omission_summary, save
from figures import native_figure


def main(out):
    panel, sources = load_endpoints()
    records, omissions, pairs = [], [], []
    for day in ("d102", "d50"):
        a = sources[day]
        for m in (e for e in sources.values() if e.model != "epithelial ATAC"):
            key = dict(time=day, methylation=m.key)
            meta = dict(**key, model=m.model, window=m.window, atac_controls=a.control.shape[1],
                        atac_recovered=a.recovered.shape[1], methylation_controls=m.control.shape[1],
                        methylation_recovered=m.recovered.shape[1])
            cov = [m.cov[0], ("amplicon_width", a.geometry.width_bp), m.cov[2]]

            def fit(check, y, adj, mask=None, group="all", details=False):
                result, data = estimate(m.delta, y, adj, mask, details)
                records.append(dict(**meta, check=check, subgroup=group,
                                    covariates=",".join(n for n, _ in adj) or "intercept", **result))
                return result, data

            full, detail = fit("geometry_adjusted", a.delta, cov, details=True)
            fit("unadjusted", a.delta, [])
            for label in CLASSES:
                fit("within_class", a.delta, [], panel.motif_class.eq(label), label)
            fit("per_kb", 1000 * a.delta / a.geometry.width_bp, cov)
            fit("coupled_baselines", a.delta, cov + [("atac_control", a.baseline), ("methyl_control", m.baseline)])
            fit("common_CpG_adjustment", a.delta, cov + [("common_CpGs", m.geometry.common_CpGs)])
            if m.window != "amplicon":
                fit("flank_width_adjustment", a.delta, cov + [("window_width", m.geometry.width_bp)])
            for j, i in enumerate(detail["index"]):
                pairs.append(dict(**key, locus=panel.index[i], motif_class=panel.motif_class.iloc[i],
                                  methyl_control_fraction=m.baseline.iloc[i], methyl_recovered_fraction=m.target.iloc[i],
                                  atac_control_CPM=a.baseline.iloc[i], atac_recovered_CPM=a.target.iloc[i],
                                  **{k: v[j] for k, v in detail.items() if k != "index"}))
            for locus in panel.index[a.delta.notna() & m.delta.notna()]:
                row, _ = estimate(m.delta, a.delta, cov, panel.index != locus)
                omissions.append(dict(**meta, omission="locus", unit=locus, arm="none", full_rho=full["rho"], **row))
            for side, e in [("atac_mouse", a), ("methylation_mouse_or_line", m)]:
                for arm, unit, delta in e.omissions():
                    x, y = (m.delta, delta) if side == "atac_mouse" else (delta, a.delta)
                    row, _ = estimate(x, y, cov)
                    omissions.append(dict(**meta, omission=side, unit=unit, arm=arm, full_rho=full["rho"], **row))
    result, omit, points = map(pd.DataFrame, (records, omissions, pairs))
    ranges = omission_summary(omit, ["time", "methylation"])
    for df, name in [(result, "native_associations.tsv"), (omit, "native_omissions.tsv.gz"),
                     (ranges, "native_omission_ranges.tsv"), (points, "native_pairs.tsv.gz")]:
        save(df, out, name)
    native_figure(result, ranges, out)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
