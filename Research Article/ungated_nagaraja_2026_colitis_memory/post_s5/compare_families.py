"""Whole-clone sampling within mouse lines, conditional cell randomization and omission."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy.special import ndtr
from scipy.stats import false_discovery_control

from family_sources import exclusive_matrix, inventory
from plot_families import render


def save(frame, out, name):
    frame.to_csv(out / (name + ".tsv"), sep="\t", index=False, na_rep="NA", float_format="%.12g")


def clone_variances(x, starts, sizes):
    summed = np.add.reduceat(x, starts, axis=0)
    squared = np.add.reduceat(x * x, starts, axis=0)
    return np.maximum(0, squared - summed * summed / sizes) / (sizes - 1)


def estimate(values, groups, clone_lines, selected, permutations, seed):
    selected = np.sort(selected)
    sizes = np.array([len(groups[g]) for g in selected])
    assert min(sizes) >= 2
    rows = np.concatenate([groups[g] for g in selected])
    assert len(np.unique(rows)) == len(rows)
    scores = np.ascontiguousarray(values[rows])
    starts = np.r_[0, np.cumsum(sizes)[:-1]]
    lines = np.repeat(clone_lines[selected], sizes)
    pools = [np.flatnonzero(lines == label) for label in np.unique(lines)]
    observed = np.median(clone_variances(scores, starts, sizes[:, None]), axis=0)
    rng = np.random.default_rng(seed)
    null = np.empty((permutations, scores.shape[1]))
    for i in range(permutations):
        order = np.concatenate([rng.permutation(pool) for pool in pools])
        # Groups and lines are in lexicographic order. This check protects cell exchangeability.
        if i == 0:
            assert np.array_equal(np.sort(order), np.arange(len(order))) and np.array_equal(lines, lines[order])
        variance = clone_variances(scores[order], starts, sizes[:, None])
        null[i] = np.median(np.sqrt(variance), axis=0) ** 2
    mean = null.mean(axis=0)
    sd = null.std(axis=0, ddof=1)
    aligned = mean - observed
    p = np.full_like(sd, np.nan)
    valid = sd > 0
    p[valid] = 2 * ndtr(-np.abs(aligned[valid] / sd[valid]))
    q = p.copy()
    if valid.any():
        q[valid] = false_discovery_control(p[valid])
    return pd.DataFrame(dict(observed=observed, null_mean=mean, null_sd=sd, null_mcse=sd/np.sqrt(permutations),
                             ref025=np.quantile(null,.025,axis=0), ref975=np.quantile(null,.975,axis=0),
                             aligned=aligned, lower_p=(1+(null<=observed).sum(axis=0))/(permutations+1),
                             normal_two_sided_p=p, matched_q=q, matched_tighter=(aligned>0)&(q<.05)))


def main(out):
    catalog, leaders, pairs = inventory()
    matched = set(pairs.organoid_feature)
    cells, scores = exclusive_matrix(matched)
    finite = np.isfinite(scores).sum()
    complete = sorted(finite.index[finite.eq(len(cells))])
    if not complete:
        raise ValueError("No common-cell matched reporters")
    leaders["matched_tissue"] = leaders.index.isin(matched)
    leaders["finite_exclusive_cells"] = finite
    leaders["resampling_status"] = np.select(
        [~leaders.matched_tissue, leaders.finite_exclusive_cells.lt(len(cells))],
        ["outside matched set", "incomplete scores on fixed cells"], default="eligible")
    pairs["resampling_status"] = pairs.organoid_feature.map(leaders.resampling_status)
    save(catalog, out, "table2_catalog")
    save(pairs, out, "reporter_links")
    groups = cells.groupby(["organoid_line","clone"], sort=True)
    keys = list(groups.indices)
    group_rows = [groups.indices[key] for key in keys]
    clone_lines = np.array([line for line, _ in keys])
    all_groups = np.arange(len(keys))
    lines = sorted(set(clone_lines))
    by_line = [all_groups[clone_lines == line] for line in lines]
    assert len(keys) == 121 and len(cells) == 3572 and len(lines) == 6
    counts = []
    estimates = []
    values = scores[complete].to_numpy()

    def run(design, draw, omitted, selected, nperm, seed):
        label = f"{design}/{draw}/{omitted}"
        result = estimate(values, group_rows, clone_lines, selected, nperm, seed)
        result.insert(0, "feature", complete)
        result.insert(0, "selection", label)
        estimates.append(result)
        for line, group_set in zip(lines, by_line):
            chosen = sorted(set(selected).intersection(group_set))
            counts.append(dict(selection=label, design=design, draw=draw, omitted=omitted, line=line,
                               eligible_clones=len(group_set), chosen_clones=len(chosen),
                               chosen_cells=sum(len(group_rows[g]) for g in chosen), n_perm=nperm,
                               clone_ids="|".join(keys[g][1] for g in chosen)))
        return result

    whole = run("full", 0, "none", all_groups, 1000, [20261120,0,0])
    whole = whole.set_index("feature")
    np.testing.assert_allclose(leaders.loc[complete,"clean_exclusive_observed"], whole.observed,
                               rtol=1e-9, atol=1e-9)
    for i, line in enumerate(lines):
        run("omit", 0, line, all_groups[clone_lines != line], 1000, [20261120,1,i])
    for percent in (50,75):
        for draw in range(1,65):
            rng = np.random.default_rng([20261120,2,percent,draw])
            selected = np.concatenate([rng.choice(gs, size=max(2,len(gs)*percent//100), replace=False)
                                       for gs in by_line])
            run(f"keep{percent}", draw, "none", selected, 96, [20261120,3,percent,draw])

    long = pd.concat(estimates, ignore_index=True)
    designs = pd.DataFrame(counts)
    summary = []
    for (design, feature), frame in long.merge(designs[["selection","design"]].drop_duplicates(),
                                               on="selection", validate="many_to_one").groupby(["design","feature"]):
        positive = frame.aligned.gt(0).mean()
        detect = frame.matched_tighter.mean()
        summary.append(dict(design=design, feature=feature, draws=len(frame), median=frame.aligned.median(),
                            minimum=frame.aligned.min(), p05=frame.aligned.quantile(.05),
                            p95=frame.aligned.quantile(.95), maximum=frame.aligned.max(),
                            positive_fraction=positive, threshold_fraction=detect,
                            positive_draws=int(frame.aligned.gt(0).sum()), threshold_draws=int(frame.matched_tighter.sum()),
                            direction_mcse=np.sqrt(positive*(1-positive)/len(frame)) if design.startswith("keep") else np.nan,
                            threshold_mcse=np.sqrt(detect*(1-detect)/len(frame)) if design.startswith("keep") else np.nan))
    leaders = leaders.join(whole.drop(columns="selection").add_prefix("within_line_"))
    save(leaders.reset_index(), out, "family_evidence")
    save(designs, out, "clone_selections")
    save(long, out, "conditional_draws")
    save(pd.DataFrame(summary), out, "stability")
    render(out, leaders, pd.DataFrame(summary))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
