"""Correct penalty orientation using a hash-bound recovered v1 cache.

No solver rerun. Refuse correction unless ALL stored v2 reaction statistics
are reproduced from this cache and the stored v2 pool metadata.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def correlations(matrix, meta, columns):
    rows = []
    for rid, values in matrix.iterrows():
        v = values.to_numpy(float)
        if np.std(v) == 0:
            continue
        row = dict(reaction=rid, n_pools=len(v), mean_score=float(v.mean()), sd_score=float(v.std()))
        for col in columns:
            rho, p = stats.spearmanr(v, meta[col])
            row.update({f"rho_{col}": float(rho), f"p_{col}": float(p)})
        rows.append(row)
    result = pd.DataFrame(rows).set_index("reaction").sort_index()
    p = result.p_pathogenicity_authors.to_numpy()
    order = np.argsort(p)
    q = np.empty_like(p)
    q[order] = np.minimum.accumulate((p[order] * len(p) / np.arange(1, len(p) + 1))[::-1])[::-1]
    result["bh_pathogenicity"] = np.minimum(q, 1)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--penalties", required=True)
    ap.add_argument("--previous", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    previous, out = Path(args.previous), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    pools = pd.read_csv(previous / "pool_scores.csv").set_index("pool")
    raw = pd.read_csv(args.penalties, sep="\t", index_col=0)
    assert raw.columns.is_unique and raw.index.is_unique and pools.index.is_unique
    assert set(raw.columns) == set(pools.index)
    raw = raw.loc[:, pools.index]
    assert np.isfinite(raw.to_numpy()).all() and (raw.to_numpy() >= 0).all()
    old = pd.read_csv(previous / "reaction_correlations.csv").set_index("reaction").sort_index()
    columns = [c.removeprefix("rho_") for c in old.columns if c.startswith("rho_")]
    reproduced = correlations(raw, pools, columns)
    assert reproduced.index.equals(old.index), "Recovered cache has a different reaction universe"
    checks = []
    for col in old.columns:
        np.testing.assert_allclose(reproduced[col], old[col], rtol=1e-9, atol=1e-12, err_msg=col)
        checks.append(dict(column=col, n_reactions=len(old), max_absolute_error=float(np.max(np.abs(reproduced[col] - old[col])))))
    corrected = correlations(-np.log1p(raw), pools, columns)
    for col in columns:
        np.testing.assert_allclose(corrected[f"rho_{col}"], -old[f"rho_{col}"], atol=1e-12)
        np.testing.assert_allclose(corrected[f"p_{col}"], old[f"p_{col}"], atol=1e-12)
    corrected["mean_raw_penalty"] = reproduced.mean_score
    corrected["sd_raw_penalty"] = reproduced.sd_score
    corrected["rank_of_rho_ascending"] = corrected.rho_pathogenicity_authors.rank(method="max").astype(int)
    corrected.to_csv(out / "reaction_correlations.csv", lineterminator="\n")
    named_ids = pd.read_csv(previous / "named_reactions.csv").reaction
    named = corrected.loc[named_ids].copy()
    named.to_csv(out / "named_reactions.csv", lineterminator="\n")
    pools.to_csv(out / "pool_scores.csv", lineterminator="\n")
    pd.DataFrame(checks).to_csv(out / "cache_verification.csv", index=False, lineterminator="\n")
    result = dict(schema="wp_compass_orientation/v3", status="executed",
        recovered_source="v1 cache, reproducing all stored v2 numeric reaction summaries; original v2 solver file not recovered",
        transform="consistency = -log1p(raw penalty); higher means greater expression consistency, not flux",
        reactions_total=len(raw), reactions_nonconstant=len(corrected), pools=len(pools),
        libraries=int(pools.library.nunique()), animals=int(pools.animal.nunique()),
        verified_cells=len(old) * len(old.columns), named_reactions=named.reset_index().to_dict("records"),
        interpretation_limit="Exposed descriptive sensitivity. Micropools are nested, not independent animals. PGAM's corrected positive association does not reproduce the paper's negative sign under these substituted inputs. It does not refute the paper's intervention results; no flux, causal or population inference.")
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
