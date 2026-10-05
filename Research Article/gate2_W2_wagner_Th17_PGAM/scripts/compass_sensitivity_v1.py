#!/usr/bin/env python
"""Wp-R2: Compass reaction scores as a declared version-and-input sensitivity.

This is NOT a reproduction of Figure 1. The published run used scVI-imputed
expression whose model and matrix were never deposited, so the input here is
different by necessity. Four deviations are declared and carried into every
statement the run supports:

  1. Input. Micropooled CP10K counts from the deposited matrix (Wp-R1's QC'd
     Th17n cells), not scVI-imputed single cells. Pooling replaces imputation as
     the sparsity control; both are information sharing, but they are not the
     same operator, and `lambda 0` is kept as published.
  2. Reaction scope. Only the two subsystems the paper's claim rests on -
     glycolysis/gluconeogenesis and glycine/serine/alanine/threonine metabolism.
     The published run scored ~900 reactions, so the reaction *ranking* reported
     in Figure 1A cannot be reproduced; only the sign and size of the
     PGAM-versus-pathogenicity association within this subset.
  3. Version. Compass 1.0.0 from the authors' own wagnerlab-berkeley fork with
     the Gurobi optimiser, not the version used in 2025.
  4. Execution. A serial pool shim (scripts/compass_serial_runner_v1.py),
     because this host denies multiprocessing pipes. No algorithmic change.

Unit: micropool (nested in library, nested in animal). Two animals. The endpoint
is an across-pool correlation, which is a description of this deposit's cells and
is not animal-level inference.

Frozen design:
  - Pools: within each Th17n library, 20-component truncated SVD of log1p CP10K,
    k-means with k = round(n_cells / 50), seed 20261004; pools with at least 20
    cells are eligible.
  - A stratified subsample of POOL_TARGET eligible pools (equal share per library,
    seed 20261004) is scored, because each pool costs about a minute of solver time.
  - Endpoint: Spearman correlation across pools between each reaction's Compass
    score and the pool mean pathogenicity score, with PGM (3PG <-> 2PG, the PGAM
    reaction) and DPGM named in advance; the same against the Table S3 Th17n EGCG
    signature score; and PGM's rank among all scored reactions.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats
from scipy.cluster.vq import kmeans2
from scipy.sparse.linalg import svds

SEED = 20261004
POOL_CELLS = 50
MIN_POOL_CELLS = 20
POOL_TARGET = 60
SUBSYSTEMS = ["Glycolysis/gluconeogenesis", "Glycine, serine, alanine and threonine metabolism"]
NAMED_REACTIONS = ["PGM_pos", "PGM_neg", "DPGM_pos", "DPGM_neg", "PGK_pos", "PGK_neg",
                   "ENO_pos", "ENO_neg", "PGCD_pos", "PGCD_neg", "PSERT_pos", "PSERT_neg",
                   "PSP_L_pos", "PSP_L_neg", "GHMT2r_pos", "GHMT2r_neg"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--r1-run", required=True, help="Wp-R1 run directory holding cell_scores.csv.gz")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, out, r1 = Path(args.data_root), Path(args.output), Path(args.r1_run)
    out.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent

    verified = {f: sha256(root / f) for f in
                ["GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz",
                 "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz",
                 "GSE289733_filtered_feature_bc_matrix_features.tsv.gz",
                 "acquisition_v3_matrices.json"]}
    verified["wp_singlecell_reproduction_v1/cell_scores.csv.gz"] = sha256(r1 / "cell_scores.csv.gz")

    cells = pd.read_csv(r1 / "cell_scores.csv.gz")
    th17n = cells[cells.cell_type == "Th17n"].copy()
    bcs = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz", header=None)[0].to_numpy()
    feats = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_features.tsv.gz", sep="\t", header=None)
    symbols = feats[1].astype(str).to_numpy()

    wanted = {b: i for i, b in enumerate(th17n.barcode)}
    newcol = np.full(len(bcs), -1, dtype=np.int64)
    for j, b in enumerate(bcs):
        if b in wanted:
            newcol[j] = wanted[b]
    rows, cols, vals = [], [], []
    with gzip.open(root / "GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz", "rt") as fh:
        line = fh.readline()
        while line.startswith("%"):
            line = fh.readline()
        n_genes, _, _ = (int(v) for v in line.split())
        for raw in fh:
            g, c, v = raw.split()
            j = newcol[int(c) - 1]
            if j >= 0:
                rows.append(j)
                cols.append(int(g) - 1)
                vals.append(np.float32(v))
    X = sp.csr_matrix((np.array(vals, dtype=np.float32), (np.array(rows), np.array(cols))),
                      shape=(len(th17n), n_genes))
    X = sp.diags((1e4 / np.maximum(np.asarray(X.sum(axis=1)).ravel(), 1)).astype(np.float32)) @ X
    X = sp.csr_matrix(X)
    detected = np.asarray((X > 0).sum(axis=0)).ravel() >= 10
    first = {}
    keep_gene = np.zeros(X.shape[1], dtype=bool)
    for i, s in enumerate(symbols):
        if detected[i] and s not in first:
            first[s] = i
            keep_gene[i] = True
    X = X[:, keep_gene]
    gene_names = symbols[keep_gene]

    # --- micropools within library -----------------------------------------
    L = X.copy()
    L.data = np.log1p(L.data)
    pool_of = np.empty(X.shape[0], dtype=object)
    lib = th17n.library.to_numpy()
    for lb in np.unique(lib):
        m = np.where(lib == lb)[0]
        U, S, _ = svds(L[m], k=20)
        k = max(2, round(len(m) / POOL_CELLS))
        _, lab = kmeans2(U * S, k, minit="++", seed=SEED, missing="warn")
        pool_of[m] = [f"L{lb}_P{i:03d}" for i in lab]
    th17n["pool"] = pool_of
    sizes = th17n.pool.value_counts()
    eligible = sorted(sizes[sizes >= MIN_POOL_CELLS].index)

    rng = np.random.default_rng(SEED)
    by_lib: dict[str, list[str]] = {}
    for p in eligible:
        by_lib.setdefault(p.split("_")[0], []).append(p)
    per = max(1, POOL_TARGET // len(by_lib))
    chosen: list[str] = []
    for lb in sorted(by_lib):
        pool_list = sorted(by_lib[lb])
        chosen += list(rng.choice(pool_list, size=min(per, len(pool_list)), replace=False))
    chosen = sorted(chosen)

    mask = th17n.pool.isin(chosen).to_numpy()
    expr = {}
    for p in chosen:
        sel = (th17n.pool.to_numpy() == p)
        expr[p] = np.asarray(X[sel].mean(axis=0)).ravel()
    E = pd.DataFrame(expr, index=gene_names)
    E.to_csv(out / "pool_expression.tsv", sep="\t")

    score_cols = ["pathogenicity_authors", "proinflammatory_authors", "proregulatory_authors",
                  "Th17n_EGCG_S3_local", "Th17n_EGCG_S3_all", "proliferation"]
    score_cols = [c for c in score_cols if c in th17n.columns]
    pool_meta = (th17n[mask].groupby("pool")
                 .agg(n_cells=("pool", "size"), library=("library", "first"),
                      glucose=("glucose", "first"), animal=("animal", "first"),
                      **{c: (c, "mean") for c in score_cols}).reset_index())
    pool_meta.to_csv(out / "pool_scores.csv", index=False, lineterminator="\n")

    # --- Compass ------------------------------------------------------------
    sub_file = out / "subsystems.txt"
    sub_file.write_text("\n".join(SUBSYSTEMS) + "\n", encoding="utf-8", newline="\n")
    compass_dir = out / "compass"
    compass_dir.mkdir(exist_ok=True)
    cmd = [sys.executable, str(here / "compass_serial_runner_v1.py"), "--",
           "--data", str(out / "pool_expression.tsv"),
           "--model", "RECON2_mat", "--species", "mus_musculus", "--lambda", "0",
           "--select-subsystems", str(sub_file),
           "--num-processes", "1", "--num-threads", "4", "--optimizer", "gurobi",
           "--output-dir", str(compass_dir), "--temp-dir", str(out / "compass_temp")]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    (out / "compass_stdout.log").write_text(proc.stdout[-200000:], encoding="utf-8")
    (out / "compass_stderr.log").write_text(proc.stderr[-200000:], encoding="utf-8")
    if proc.returncode != 0 or not (compass_dir / "reactions.tsv").exists():
        (out / "results.json").write_text(json.dumps(
            {"schema": "wp_r2_compass_sensitivity/v1", "status": "compass_failed",
             "returncode": proc.returncode, "inputs_verified": verified,
             "n_pools_requested": len(chosen)}, indent=1) + "\n", encoding="utf-8")
        return 1

    R = pd.read_csv(compass_dir / "reactions.tsv", sep="\t", index_col=0)
    # Compass scores are -log penalties; higher means more consistent with the data
    R = R.loc[:, [c for c in pool_meta["pool"] if c in R.columns]]
    meta = pool_meta.set_index("pool").loc[R.columns]
    rows_out = []
    for rid, vals in R.iterrows():
        v = vals.to_numpy(dtype=float)
        if np.nanstd(v) == 0:
            continue
        row = {"reaction": rid, "n_pools": int(np.isfinite(v).sum()),
               "mean_score": float(np.nanmean(v)), "sd_score": float(np.nanstd(v))}
        for c in score_cols:
            sp_ = stats.spearmanr(v, meta[c].to_numpy(), nan_policy="omit")
            row[f"rho_{c}"] = float(sp_.statistic)
            row[f"p_{c}"] = float(sp_.pvalue)
        rows_out.append(row)
    corr = pd.DataFrame(rows_out)
    p = corr["p_pathogenicity_authors"].to_numpy()
    order = np.argsort(p)
    q = np.empty_like(p)
    q[order] = np.minimum.accumulate((p[order] * len(p) / (np.arange(len(p)) + 1))[::-1])[::-1]
    corr["bh_pathogenicity"] = np.minimum(q, 1.0)
    corr = corr.sort_values("rho_pathogenicity_authors")
    corr.to_csv(out / "reaction_correlations.csv", index=False, lineterminator="\n")

    named = corr[corr.reaction.isin(NAMED_REACTIONS)].copy()
    named["rank_of_rho"] = [int((corr.rho_pathogenicity_authors <= r).sum()) for r in named.rho_pathogenicity_authors]
    named.to_csv(out / "named_reactions.csv", index=False, lineterminator="\n")

    results = {
        "schema": "wp_r2_compass_sensitivity/v1",
        "status": "executed",
        "inputs_verified": verified,
        "unit": "micropool of Th17n cells, nested in library (4) and animal (2)",
        "deviations_from_published_run": [
            "input is micropooled CP10K counts, not the scVI-imputed matrix (never deposited)",
            f"reaction scope restricted to {len(SUBSYSTEMS)} subsystems, so Figure 1A's ranking is out of scope",
            "Compass 1.0.0 (wagnerlab-berkeley fork) with Gurobi, not the published version",
            "serial pool shim because this host denies multiprocessing pipes",
        ],
        "pooling": {"target_cells_per_pool": POOL_CELLS, "min_cells": MIN_POOL_CELLS,
                    "eligible_pools": len(eligible), "scored_pools": len(chosen), "seed": SEED},
        "n_reactions_scored": int(len(corr)),
        "n_cells_pooled": int(mask.sum()),
        "named_reaction_correlations": named.to_dict("records"),
        "most_negative": corr.head(10)[["reaction", "rho_pathogenicity_authors",
                                        "p_pathogenicity_authors", "bh_pathogenicity"]].to_dict("records"),
        "most_positive": corr.tail(10)[["reaction", "rho_pathogenicity_authors",
                                        "p_pathogenicity_authors", "bh_pathogenicity"]].to_dict("records"),
        "interpretation_limit": ("Version-and-input sensitivity, not a reproduction of Figure 1. Supports a statement "
            "about whether the PGAM reaction's association with the pathogenicity score has the published sign under a "
            "modern Compass, a restricted reaction set and pooled rather than imputed input; supports no claim about "
            "the published reaction ranking, and no animal-level or causal inference."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
