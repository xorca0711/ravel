"""Fig. 2h-i reconstruction using released cell/clone memberships and distinct mouse lines."""
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import norm, ttest_ind

from plot_clones import draw

CACHE = Path("raw_data/nagaraja_s0")
KEYS = Path("analysis/research/runs/ng26_s0_keys_v1")
VARIANTS = ("released", "line_qualified", "clean_exclusive")
REPORTERS = ("Fos", "Etv2", "Ctcf", "Hnf4g")
N_PERM = 1000


def write(table, path):
    table.to_csv(path, index=False, sep="\t", na_rep="NA", lineterminator="\n",
                 float_format="%.15g")


def load_inputs():
    long = pd.read_csv(CACHE / "moesm4.txt", sep="\t", dtype={"score": "float64"})
    members = long[["atac_cell", "clone", "sample"]].drop_duplicates()
    keys = pd.read_csv(KEYS / "cell_clone_line_mouse.tsv", sep="\t")
    keys = keys.loc[keys.in_score_table].rename(columns={"clone_id": "clone", "history": "sample"})
    members = members.merge(keys, on=["atac_cell", "clone", "sample"], how="outer",
                            validate="one_to_one", indicator=True, sort=False)
    assert members._merge.eq("both").all() and len(members) == 4815
    assert members.atac_cell.nunique() == 4193 and members.mouse_donor.nunique() == 6
    assert members.groupby("organoid_line").mouse_donor.nunique().eq(1).all()
    index = ["atac_cell", "clone", "sample"]
    assert not long.duplicated(["feature", *index]).any()
    features = long.feature.drop_duplicates().tolist()
    assert len(features) == 299 and long.groupby("feature").size().eq(len(members)).all()
    matrix = long.pivot(index=index, columns="feature", values="score").reindex(
        index=pd.MultiIndex.from_frame(members[index]), columns=features)
    with ZipFile(CACHE / "moesm5.zip") as archive:
        name, = [n for n in archive.namelist() if "Table4_" in n]
        ref = pd.read_excel(io.BytesIO(archive.read(name))).rename(columns={"bag_leader": "feature"})
    assert set(ref.feature) == set(features) and not ref.feature.duplicated().any()
    return members, matrix.to_numpy().T.copy(), features, ref


def group_layout(members, variant):
    keep = members.clean_memberships_of_cell.eq(1) if variant == "clean_exclusive" else np.ones(len(members), bool)
    keys = ["clone"] if variant == "released" else ["organoid_line", "clone"]
    subset = members.loc[keep].sort_values(keys, kind="stable")
    sizes = subset.groupby(keys, sort=False).size()
    eligible = subset.groupby(keys, sort=False)["atac_cell"].transform("size").ge(2)
    layout = subset.index[eligible].to_numpy()
    counts = sizes[sizes.ge(2)].to_numpy()
    assert counts.sum() == len(layout)
    return layout, counts, dict(variant=variant, input_memberships=len(subset),
                                input_cells=subset.atac_cell.nunique(), all_units=len(sizes),
                                singleton_units=int(sum(sizes == 1)), dispersion_units=len(counts),
                                dispersion_memberships=len(layout),
                                dispersion_cells=members.loc[layout, "atac_cell"].nunique())


def stats_for_feature(values, counts, feature_number, variant_number):
    # A uniform permutation of membership scores into fixed clone slots has the
    # same joint assignment law as shuffling clone labels on fixed score rows.
    starts = np.r_[0, np.cumsum(counts)[:-1]]
    rng = np.random.default_rng(np.random.SeedSequence([123, variant_number, feature_number]))
    finite = np.isfinite(values)
    infinity = np.isinf(values)
    numeric = np.where(finite, values, 0)
    square = numeric ** 2
    all_finite = finite.all()

    def variances(idx):
        sums = np.add.reduceat(numeric[idx], starts, axis=-1)
        squares = np.add.reduceat(square[idx], starts, axis=-1)
        n = counts if all_finite else np.add.reduceat(finite[idx].astype(int), starts, axis=-1)
        with np.errstate(invalid="ignore", divide="ignore"):
            var = np.where(n >= 2, np.maximum(squares - sums**2 / n, 0) / (n - 1), np.nan)
        # R sd(..., na.rm=TRUE) removes NA/NaN but +/-Inf produces undefined SD.
        if infinity.any():
            var = np.where(np.logical_or.reduceat(infinity[idx], starts, axis=-1), np.nan, var)
        return var

    order = np.arange(len(values))
    observed_groups = variances(order)
    observed = np.median(observed_groups)
    null = np.full(N_PERM, np.nan)
    if np.isfinite(observed_groups).any():
        for begin in range(0, N_PERM, 32):
            count = min(32, N_PERM - begin)
            idx = rng.permuted(np.broadcast_to(order, (count, len(values))), axis=1)
            null[begin:begin+count] = np.median(np.sqrt(variances(idx)), axis=1) ** 2
    mean = np.mean(null)
    sd = np.std(null, ddof=1)
    z = (observed - mean) / sd if sd > 0 else np.nan
    row = dict(observed=observed, null_mean=mean, null_sd=sd, delta=observed-mean,
               z=z, p=2*norm.sf(abs(z)), finite_group_sd=np.isfinite(observed_groups).sum(),
               finite_null=np.isfinite(null).sum(), input_nan=np.isnan(values).sum(),
               input_inf=infinity.sum())
    return row, null


def adjust(pvalues):
    # R p.adjust defaults to the number of nonmissing tests in the BH calculation.
    good = pvalues.dropna().sort_values()
    q = good.to_numpy() * len(good) / np.arange(1, len(good) + 1)
    return pd.Series(np.minimum(1, np.minimum.accumulate(q[::-1])[::-1]), index=good.index)


def dispersion(out, members, matrix, features, ref):
    rows, coverage, nulls = [], [], {}
    for v, variant in enumerate(VARIANTS):
        idx, counts, eligibility = group_layout(members, variant)
        coverage.append(eligibility)

        def evaluate(i):
            return stats_for_feature(matrix[i, idx], counts, i, v)

        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(evaluate, range(len(features))))
        table = pd.DataFrame([answer[0] for answer in results])
        table.insert(0, "feature", features)
        table.insert(0, "variant", variant)
        table["fdr"] = adjust(table.p)
        rows.append(table)
        nulls[variant] = np.stack([answer[1] for answer in results])
    np.savez_compressed(out / "null_draws.npz", features=np.array(features), **nulls)
    full = pd.concat(rows, ignore_index=True)
    reference = ref.rename(columns={k: "t4_"+k for k in ref.columns if k != "feature"})
    full = full.merge(reference, on="feature", validate="many_to_one", sort=False)
    full["t4_delta"] = full.t4_clone_median_var - full.t4_shuf_median_var
    full["observed_minus_t4"] = full.observed - full.t4_clone_median_var
    full["null_minus_t4"] = full.null_mean - full.t4_shuf_median_var
    full["null_difference_joint_mcse"] = full.null_minus_t4 / np.sqrt(
        (full.null_sd**2 + full.t4_shuf_sd_var**2)/N_PERM)
    write(full, out / "dispersion.tsv")
    write(pd.DataFrame(coverage), out / "membership_coverage.tsv")
    return full


def history_distributions(out, members, fos):
    assert np.isfinite(fos).all()
    data = members.assign(score=fos)
    all_clones, summaries, line_rows, contrasts = [], [], [], []
    for variant in (*VARIANTS, "scored_exclusive"):
        d = data
        if variant == "clean_exclusive":
            d = d.loc[d.clean_memberships_of_cell.eq(1)]
        elif variant == "scored_exclusive":
            d = d.loc[d.scored_memberships_of_cell.eq(1)]
        group = ["sample", "clone"] if variant == "released" else ["sample", "organoid_line", "mouse_donor", "clone"]
        clones = d.groupby(group, as_index=False).agg(n=("score", "size"), fos_median=("score", "median"))
        clones.insert(0, "variant", variant)
        all_clones.append(clones)
        for minimum in (1, 5):
            selected = clones.loc[clones.n.ge(minimum)]
            by_history = {k: g.fos_median for k,g in selected.groupby("sample")}
            welch = ttest_ind(by_history["Colitis"], by_history["Control"], equal_var=False)
            student = ttest_ind(by_history["Colitis"], by_history["Control"], equal_var=True)
            for k, scores in by_history.items():
                summaries.append(dict(variant=variant, min_memberships=minimum, history=k,
                                      clones=len(scores), median=scores.median(), mean=scores.mean(),
                                      above_1p25=scores.gt(1.25).sum(),
                                      pct_above=100*scores.gt(1.25).mean(),
                                      clone_welch_p=welch.pvalue, clone_pooled_p=student.pvalue))
        if variant == "released":
            continue
        lines = clones.groupby(["sample","organoid_line","mouse_donor"], as_index=False).agg(
            n_clones=("clone","size"), memberships=("n","sum"), mean_clone_median=("fos_median","mean"),
            median_clone_median=("fos_median","median"), high_clones=("fos_median", lambda x: sum(x>1.25)))
        lines["scored_cells"] = lines.organoid_line.map(d.groupby("organoid_line").atac_cell.nunique())
        lines["variant"] = variant
        line_rows.append(lines)
        for omit in ["none", *lines.organoid_line]:
            subset = lines.loc[lines.organoid_line.ne(omit)]
            for endpoint in ("mean_clone_median", "median_clone_median"):
                c = subset.loc[subset["sample"].eq("Control"), endpoint].to_numpy()
                h = subset.loc[subset["sample"].eq("Colitis"), endpoint].to_numpy()
                diffs = h[:,None]-c
                contrasts.append(dict(variant=variant, omitted_line=omit, endpoint=endpoint,
                                      control_lines=len(c), colitis_lines=len(h),
                                      colitis_minus_control=h.mean()-c.mean(),
                                      positive_cross_pairs=int((diffs>0).sum()), cross_pairs=diffs.size))
    combined = pd.concat(all_clones, ignore_index=True)
    lines = pd.concat(line_rows, ignore_index=True)
    write(combined, out / "fos_clones.tsv")
    write(pd.DataFrame(summaries), out / "fos_by_history.tsv")
    write(lines, out / "fos_by_line.tsv")
    write(pd.DataFrame(contrasts), out / "line_contrasts.tsv")
    return combined, lines


if __name__ == "__main__":
    destination = Path(sys.argv[1])
    members, matrix, features, reference = load_inputs()
    dispersion_rows = dispersion(destination, members, matrix, features, reference)
    clone_rows, lines = history_distributions(destination, members, matrix[features.index("Fos")])
    draw(destination, dispersion_rows, clone_rows, lines)
