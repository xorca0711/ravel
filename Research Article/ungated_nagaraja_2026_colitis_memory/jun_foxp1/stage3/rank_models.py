"""Common Stage 3 rank estimator and Stage 2 specimen-level sources."""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata


SOURCE = Path("analysis/research/runs/ng26_jf_measurements_v1")
CLASSES = ["AP1 only", "AP1 + Fox"]
WINDOWS = ["amplicon", "left_flank", "right_flank"]
MODELS = ["P4 organoid", "whole colon"]


def read(name):
    return pd.read_csv(SOURCE / name, sep="\t")


def save(df, out, name):
    df.to_csv(out / name, sep="\t", index=False, float_format="%.15g", na_rep="NA",
              compression={"method": "gzip", "mtime": 0} if name.endswith(".gz") else None)


def ranked(x):
    return rankdata(np.round(np.asarray(x, dtype=float), 12), method="average")


def estimate(x, y, covariates, mask=None, details=False):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    keep = np.isfinite(x) & np.isfinite(y)
    if mask is not None:
        keep &= mask
    for _, col in covariates:
        keep &= np.isfinite(col)
    n = int(keep.sum())
    k = 1 + len(covariates)
    row = dict(n=n, design_columns=k, design_rank=0, rho=np.nan, status="too few loci")
    data = {}
    if n >= 2:
        matrix = np.column_stack([np.ones(n)] + [ranked(np.asarray(v)[keep]) for _, v in covariates])
        values = np.column_stack([ranked(x[keep]), ranked(y[keep])])
        coef, _, rank, _ = np.linalg.lstsq(matrix, values, rcond=None)
        residual = values - matrix @ coef
        row["design_rank"] = int(rank)
        if rank < k:
            row["status"] = "rank deficient"
        elif n <= k + 1 or np.ptp(residual, axis=0).min() < 1e-10:
            row["status"] = "insufficient residual variation"
        else:
            row.update(rho=float(np.corrcoef(residual.T)[0, 1]), status="estimated")
        if details:
            data = dict(index=np.flatnonzero(keep), x=x[keep], y=y[keep], x_rank=values[:, 0],
                        y_rank=values[:, 1], residual_x=residual[:, 0], residual_y=residual[:, 1])
    return row, data


class Endpoint:
    def __init__(self, key, model, window, measurements, control, recovered, baseline, target, scale):
        self.key, self.model, self.window, self.scale = key, model, window, scale
        self.geometry = measurements
        self.control, self.recovered = control, recovered
        self.baseline, self.target = baseline, target
        self.delta = scale * (target - baseline)
        for table, ref in [(control, baseline), (recovered, target)]:
            assert np.allclose(table.mean(axis=1), ref, atol=1e-11, rtol=1e-12, equal_nan=True)
            assert table.isna().all(axis=1).equals(table.isna().any(axis=1))
        self.cov = [("class", measurements.motif_class.eq(CLASSES[1]).astype(float)),
                    ("width", measurements.width_bp), ("density", measurements.CpGs_per_100bp)]

    def omissions(self):
        for arm, table in [("control", self.control), ("recovered", self.recovered)]:
            for specimen in table:
                other = table.drop(columns=specimen).mean(axis=1)
                diff = self.target - other if arm == "control" else other - self.baseline
                yield arm, specimen, self.scale * diff

    def splits(self):
        for specimen in self.control:
            other = self.control.drop(columns=specimen).mean(axis=1)
            yield specimen, self.scale * (self.target - other), self.control[specimen]


def load_endpoints():
    b = read("locus_measurements.tsv").set_index("locus")
    assert len(b) == b.index.nunique() == 63
    a = read("atac_specimens.tsv")
    ah = read("atac_history.tsv")
    m = read("methylation_specimens.tsv.gz")
    mh = read("methylation_history.tsv")
    endpoints = {}
    for day in (102, 50):
        sample = a[a.time.eq(day)]
        ref = ah[ah.time.eq(day)].set_index("locus").reindex(b.index)
        arms = [sample[sample.condition.eq(arm)].pivot(index="locus", columns="specimen", values="CPM").reindex(b.index)
                for arm in ["control", "colitis"]]
        g = b[["motif_class", "width_bp", "reference_CpGs", "CpGs_per_100bp"]].copy()
        e = Endpoint(f"d{day}", "epithelial ATAC", "amplicon", g, *arms, ref.control_mean_CPM,
                     ref.recovered_mean_CPM, 1)
        e.delta = ref.delta_CPM
        endpoints[e.key] = e
    for model in MODELS:
        for window in WINDOWS:
            ref = mh[mh.model.eq(model) & mh.window.eq(window)].set_index("locus").reindex(b.index)
            sample = m[m.model.eq(model) & m.window.eq(window)]
            arms = [sample[sample.arm.eq(arm)].pivot(index="locus", columns="gsm", values="mean_fraction").reindex(b.index)
                    for arm in ["control", "recovered"]]
            g = ref[["width_bp", "reference_CpGs", "common_CpGs", "CpGs_per_100bp"]].join(b.motif_class)
            key = ("P4" if model == MODELS[0] else "vehicle") + "_" + window
            e = Endpoint(key, model, window, g, *arms, ref.control_mean_fraction, ref.recovered_mean_fraction, 100)
            e.delta = ref.delta_pp
            endpoints[key] = e
    return b, endpoints


def omission_summary(rows, group):
    records = []
    for key, block in rows.groupby(group + ["omission"], sort=False):
        finite = block[block.rho.notna()]
        row = dict(zip(group + ["omission"], key))
        row.update(planned=len(block), estimated=len(finite))
        if not finite.empty:
            low = finite.loc[finite.rho.idxmin()]
            high = finite.loc[finite.rho.idxmax()]
            peak = finite.loc[(finite.rho - finite.full_rho).abs().idxmax()]
            row.update(full_rho=peak.full_rho, min_rho=low.rho, min_id=low.unit, max_rho=high.rho,
                       max_id=high.unit, max_change_id=peak.unit, max_abs_change=abs(peak.rho-peak.full_rho),
                       sign_reversals=int((finite.rho * finite.full_rho < 0).sum()))
        records.append(row)
    return pd.DataFrame(records)
