"""Wp-R1 expression-floor sensitivity on the GSE289733 library pseudobulk.

Wp-R1 keeps a gene when it reaches 1 CPM in at least half of the eight
libraries. That floor was lowered from 10 CPM during a dry run after the higher
floor silently removed FOXP3, TBX21, CCL5 and IL23R, which are four of the ten
genes Figure 3D names. The floor was therefore chosen with knowledge of which
genes it admits, and this entrypoint exists to record what the choice costs and
buys across the whole range rather than to leave that dependence undocumented.

What it does: for each candidate floor, refit the declared glucose x cell-type
interaction model on the libraries that pass, and report (a) which of the ten
named genes remain in the tested universe, (b) their effect, raw p and BH q, and
(c) the size of the tested universe, which is the multiplicity correction for
every row of the table. At floor 0 it additionally dumps every gene reaching
BH <= 0.05 together with its library CPM, because an unfiltered universe is the
case where the floor's absence is most likely to manufacture a finding.

Library condition labels are taken from the frozen Wp-R1 run and are NOT a
parameter here; only the floor varies. The per-gene model is unchanged, so any
movement in a per-gene effect or raw p would be a defect and is asserted
against.

Unit: library (8) nested in animal (2), animals crossed with all four
conditions, exactly as in Wp-R1. No new biological claim is made.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats

PAPER_FIG3D = {"Th17p": {"up_with_glucose": ["TBX21", "CCL5", "IL23R", "IL22"],
                         "down_with_glucose": ["CSF2", "GZMB"]},
               "Th17n": {"glucose_sensitive": ["FOXP3", "CTLA4", "IL2RA", "TSC22D3"]}}
FLOORS = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
FROZEN_FLOOR = 1.0
MIN_GENES = 500
MAX_MITO = 0.10
MAD_K = 3.0
MIN_FRACTION_LIBRARIES = 0.5


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bh(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    m = len(p)
    order = np.argsort(p)
    q = np.empty(m)
    run = 1.0
    for rank in range(m - 1, -1, -1):
        run = min(run, p[order[rank]] * m / (rank + 1))
        q[order[rank]] = run
    return q


def read_mtx_cells_by_genes(path: Path, ng: int, nc: int, nnz: int) -> sp.csr_matrix:
    rows = np.empty(nnz, np.int32)
    cols = np.empty(nnz, np.int32)
    vals = np.empty(nnz, np.float32)
    i = 0
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("%"):
                continue
            break
        for line in fh:
            g, c, v = line.split()
            rows[i] = int(c) - 1
            cols[i] = int(g) - 1
            vals[i] = float(v)
            i += 1
    if i != nnz:
        raise SystemExit(f"matrix declares {nnz} entries, read {i}")
    return sp.csr_matrix((vals, (rows, cols)), shape=(nc, ng))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--r1-run", required=True, help="Wp-R1 run directory holding library_labels.csv")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, out, r1 = Path(args.data_root), Path(args.output), Path(args.r1_run)
    out.mkdir(parents=True, exist_ok=True)

    verified = {f: sha256(root / f) for f in
                ["GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz",
                 "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz",
                 "GSE289733_filtered_feature_bc_matrix_features.tsv.gz"]}
    verified["wp_singlecell_reproduction_v1/library_labels.csv"] = sha256(r1 / "library_labels.csv")
    verified["wp_singlecell_reproduction_v1/fig3d_named_genes.csv"] = sha256(r1 / "fig3d_named_genes.csv")

    barcodes = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz",
                           header=None)[0].to_numpy()
    feats = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_features.tsv.gz",
                        sep="\t", header=None)
    with gzip.open(root / "GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz", "rt") as fh:
        for line in fh:
            if not line.startswith("%"):
                ng, nc, nnz = (int(v) for v in line.split())
                break
    X = read_mtx_cells_by_genes(root / "GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz",
                                ng, nc, nnz)
    symbols = feats[1].astype(str).str.upper().to_numpy()
    library = np.array([b.rsplit("-", 1)[1] for b in barcodes])

    # QC and pseudobulk, identical to the frozen Wp-R1 entrypoint
    n_genes = np.diff(X.indptr)
    total = np.asarray(X.sum(axis=1)).ravel()
    mito = np.array([s.startswith("MT-") for s in symbols])
    mito_frac = np.asarray(X[:, mito].sum(axis=1)).ravel() / np.maximum(total, 1)
    qc = np.ones(X.shape[0], dtype=bool)
    qc_rows = []
    for lib in sorted(np.unique(library), key=int):
        m = library == lib
        lt = np.log10(np.maximum(total[m], 1))
        med, mad = np.median(lt), stats.median_abs_deviation(lt, scale="normal")
        keep = ((n_genes[m] >= MIN_GENES) & (mito_frac[m] <= MAX_MITO)
                & (lt >= med - MAD_K * mad) & (lt <= med + MAD_K * mad))
        qc[np.where(m)[0]] = keep
        qc_rows.append({"library": lib, "n_barcodes": int(m.sum()), "n_pass_qc": int(keep.sum())})
    X = X[qc]
    library = library[qc]
    detected = np.asarray((X > 0).sum(axis=0)).ravel() > 0
    _, first = np.unique(symbols, return_index=True)
    keepg = np.zeros(len(symbols), dtype=bool)
    keepg[first] = True
    keepg &= detected
    X = X[:, keepg]
    symbols = symbols[keepg]
    gidx = {g: i for i, g in enumerate(symbols)}

    libs = sorted(np.unique(library), key=int)
    pb = np.vstack([np.asarray(X[library == l].sum(axis=0)).ravel() for l in libs])
    cpm = pb / pb.sum(axis=1, keepdims=True) * 1e6
    lcpm = np.log2(cpm + 1)

    lab = pd.read_csv(r1 / "library_labels.csv")
    lab["library"] = lab["library"].astype(str)
    lab = lab[lab.animal_label != "unknown"].set_index("library")
    if len(lab) != 8:
        raise SystemExit(f"expected 8 labelled libraries, found {len(lab)}")
    li = [libs.index(l) for l in lab.index]
    Y, C = lcpm[li], cpm[li]
    D = pd.DataFrame({"type": (lab["derived_cell_type"] == "Th17p").astype(float).to_numpy(),
                      "glu": (lab["derived_glucose"] == "25mM").astype(float).to_numpy(),
                      "animal": (lab["animal_label"] == "Mo2").astype(float).to_numpy()})
    D["inter"] = D["type"] * D["glu"]
    A = np.column_stack([np.ones(len(li)), D[["animal", "type", "glu", "inter"]].to_numpy()])
    dfr = len(li) - A.shape[1]
    XtXi = np.linalg.inv(A.T @ A)

    named = [(t, claim, g) for t, groups in PAPER_FIG3D.items()
             for claim, genes in groups.items() for g in genes]
    rows, universe = [], []
    for floor in FLOORS:
        expressed = (C >= floor).mean(axis=0) >= MIN_FRACTION_LIBRARIES
        coef, *_ = np.linalg.lstsq(A, Y[:, expressed], rcond=None)
        resid = Y[:, expressed] - A @ coef
        s2 = (resid ** 2).sum(axis=0) / dfr
        t_inter = coef[4] / np.sqrt(s2 * XtXi[4, 4])
        p_inter = 2 * stats.t.sf(np.abs(t_inter), dfr)
        q_inter = bh(p_inter)
        eg = symbols[expressed]
        pos = {g: i for i, g in enumerate(eg)}
        universe.append({"floor_cpm": floor, "n_universe": int(expressed.sum()),
                         "n_p_lt_0.001": int((p_inter < 0.001).sum()),
                         "n_bh_0.05": int((q_inter <= 0.05).sum())})
        if floor == 0.0:
            hit = pd.DataFrame({"symbol": eg, "p_interaction": p_inter, "bh_interaction": q_inter,
                                "median_library_cpm": np.median(C[:, expressed], axis=0),
                                "max_library_cpm": C[:, expressed].max(axis=0),
                                "n_libraries_at_1cpm": (C[:, expressed] >= 1).sum(axis=0)})
            (hit[hit.bh_interaction <= 0.05].sort_values("bh_interaction")
             .to_csv(out / "unfiltered_bh_hits.csv", index=False, lineterminator="\n"))
        for t, claim, g in named:
            present = g in pos
            i = pos.get(g)
            eff = (coef[3][i] if t == "Th17n" else coef[3][i] + coef[4][i]) if present else None
            rows.append({"floor_cpm": floor, "cell_type": t, "paper_claim": claim, "symbol": g,
                         "median_library_cpm": round(float(np.median(C[:, gidx[g]])), 3),
                         "in_tested_universe": present,
                         "glucose_effect_25mM_minus_1mM": float(eff) if present else None,
                         "p_interaction": float(p_inter[i]) if present else None,
                         "bh_interaction": float(q_inter[i]) if present else None})
    named_df = pd.DataFrame(rows)
    named_df.to_csv(out / "floor_sweep_named_genes.csv", index=False, lineterminator="\n")
    uni_df = pd.DataFrame(universe)
    uni_df.to_csv(out / "floor_sweep_universe.csv", index=False, lineterminator="\n")

    # the per-gene model does not depend on the floor; drift here would be a defect
    inv = named_df.dropna(subset=["p_interaction"]).groupby("symbol").agg(
        effect_spread=("glucose_effect_25mM_minus_1mM", lambda v: float(v.max() - v.min())),
        p_spread=("p_interaction", lambda v: float(v.max() - v.min())),
        bh_min=("bh_interaction", "min"), bh_max=("bh_interaction", "max"),
        n_floors_present=("floor_cpm", "size")).reset_index()
    inv.to_csv(out / "per_gene_floor_invariance.csv", index=False, lineterminator="\n")
    worst = float(max(inv.effect_spread.max(), inv.p_spread.max()))
    if worst > 1e-9:
        raise SystemExit(f"per-gene estimates moved with the floor by {worst}; model is not "
                         "floor-independent and the sweep cannot be interpreted")

    # agreement with the frozen Wp-R1 table at the frozen floor
    frozen = pd.read_csv(r1 / "fig3d_named_genes.csv")
    mine = named_df[named_df.floor_cpm == FROZEN_FLOOR]
    m = frozen.merge(mine, on=["cell_type", "paper_claim", "symbol"],
                     suffixes=("_frozen", "_rescan"))
    agreement = {c: float(np.nanmax(np.abs(m[c + "_frozen"].to_numpy(float)
                                           - m[c + "_rescan"].to_numpy(float))))
                 for c in ["glucose_effect_25mM_minus_1mM", "p_interaction", "median_library_cpm"]}
    agreement["n_rows_compared"] = int(len(m))

    lost = {f"{f:g}": sorted(named_df[(named_df.floor_cpm == f)
                                      & ~named_df.in_tested_universe].symbol)
            for f in FLOORS}
    unf = pd.read_csv(out / "unfiltered_bh_hits.csv")
    results = {
        "schema": "wp_r1_floor_sensitivity/v1",
        "inputs_verified": verified,
        "unit": "library (8) nested in animal (2); animals crossed with all four conditions",
        "question": ("What does the Wp-R1 expression floor cost and buy? Which of the ten "
                     "genes Figure 3D names leave the tested universe at each floor, and how "
                     "does the floor change the multiplicity correction for the whole table?"),
        "qc": qc_rows,
        "floors": FLOORS,
        "frozen_floor_cpm": FROZEN_FLOOR,
        "min_fraction_libraries": MIN_FRACTION_LIBRARIES,
        "universe_by_floor": uni_df.to_dict("records"),
        "named_genes_lost_by_floor": lost,
        "per_gene_estimates_floor_invariant": True,
        "max_per_gene_drift": worst,
        "agreement_with_frozen_wp_R1": agreement,
        "unfiltered_hits": {
            "n_bh_0.05": int(len(unf)),
            "n_never_detected_at_1cpm": int((unf.n_libraries_at_1cpm == 0).sum()),
            "n_median_library_cpm_below_1": int((unf.median_library_cpm < 1).sum()),
            "genes": unf.symbol.tolist()},
        "interpretation_limit": (
            "This is a parameter sensitivity record, not a new biological result. The floor "
            "changes which genes are tested and therefore the BH correction; it does not "
            "change any per-gene estimate, which is asserted above. The eight libraries are "
            "two animals crossed with four conditions, so a per-gene interaction rests on "
            "four residual degrees of freedom and an unfiltered universe admits genes whose "
            "residual variance is numerically zero. No floor is endorsed here beyond the one "
            "the Wp-R1 contract already declares."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
