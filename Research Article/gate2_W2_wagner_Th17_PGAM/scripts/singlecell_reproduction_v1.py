#!/usr/bin/env python
"""Wp-R1: reproduce the Wang 2025 single-cell results from the GSE289733 deposit.

Descriptive estimation. Cells are nested in 8 libraries from 2 animals; the two
animals are crossed with all four cell-type x glucose conditions (one library
each). Library-level summaries are primary; cell-level distributions are shown
but no cell-wise p value is treated as population inference.

Frozen design:
  1. Condition labels per aggregation suffix are DERIVED from pseudobulk markers
     (cell type from a Th17p-minus-Th17n marker contrast; glucose from Txnip,
     the canonical glucose-induced transcript) and compared with the GEO sample
     order, which is a prior and is never applied unchecked. Animal labels are
     taken from the GEO order only where the derived cell type and glucose agree
     with it, and are marked prior-only.
  2. Signatures use the paper's method: z-scale log expression per gene across
     cells, multiply by sign, average. Module genes and HVG flags come from the
     authors' Table S1; programme markers from Table S5; EGCG and DHEA signatures
     from Table S3 (primary) and from the Wp-R3 run (secondary).
  3. Programmes N1-N3 / P1-P4 are assigned per cell by maximum Table S5 marker
     score within its derived cell type. Marker genes shared with the score being
     compared across programmes are removed in a declared sensitivity, because
     otherwise "N1 has the lowest pathogenicity" could follow from gene overlap.
  4. The glucose x cell-type interaction is fitted on library pseudobulk with
     animal as a covariate (8 libraries, 3 residual df), not on cells.
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

SIGNATURE_LFC = float(np.log2(1.5))
SIGNATURE_ALPHA = 0.05
TH17P_MARKERS = ["IL23R", "TBX21", "CSF2", "GZMB", "IL22", "IFNG"]
TH17N_MARKERS = ["IL10", "MAF", "IKZF3", "CD5L", "FOXP3", "CTLA4"]
GLUCOSE_MARKER = "TXNIP"
PROLIFERATION = ["MKI67", "TOP2A", "CDK1", "CCNB1", "CCNB2", "BIRC5", "CENPF", "TPX2", "PCNA",
                 "MCM2", "MCM3", "MCM5", "MCM6", "TYMS", "RRM2", "UBE2C", "CDC20", "HMGB2"]
PRIOR_ORDER = {  # GEO sample order, used only as a testable prior
    "1": ("Th17n", "1mM", "Mo1"), "2": ("Th17n", "25mM", "Mo1"), "3": ("Th17n", "1mM", "Mo2"),
    "4": ("Th17n", "25mM", "Mo2"), "5": ("Th17p", "1mM", "Mo1"), "6": ("Th17p", "25mM", "Mo1"),
    "7": ("Th17p", "1mM", "Mo2"), "8": ("Th17p", "25mM", "Mo2")}
PAPER_FIG3D = {"Th17p": {"up_with_glucose": ["TBX21", "CCL5", "IL23R", "IL22"],
                         "down_with_glucose": ["CSF2", "GZMB"]},
               "Th17n": {"glucose_sensitive": ["FOXP3", "CTLA4", "IL2RA", "TSC22D3"]}}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def bh(p):
    p = np.asarray(p, float)
    out = np.full(p.shape, np.nan)
    ok = ~np.isnan(p)
    q = p[ok]
    if q.size == 0:
        return out
    o = np.argsort(q)
    r = q[o] * q.size / (np.arange(q.size) + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]
    a = np.empty(q.size)
    a[o] = np.clip(r, 0, 1)
    out[ok] = a
    return out


def read_mtx_cells_by_genes(path: Path, n_genes: int, n_cells: int, nnz: int) -> sp.csr_matrix:
    """Stream a CellRanger MatrixMarket file (genes x cells) into cells x genes CSR."""
    rows = np.empty(nnz, dtype=np.int32)
    cols = np.empty(nnz, dtype=np.int32)
    vals = np.empty(nnz, dtype=np.float32)
    k = 0
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if not line.startswith("%"):
                break  # dimension line
        for chunk in pd.read_csv(fh, sep=" ", header=None, names=["g", "c", "v"],
                                 dtype={"g": np.int32, "c": np.int32, "v": np.float32}, chunksize=5_000_000):
            n = len(chunk)
            rows[k:k + n] = chunk["g"].to_numpy() - 1
            cols[k:k + n] = chunk["c"].to_numpy() - 1
            vals[k:k + n] = chunk["v"].to_numpy()
            k += n
    if k != nnz:
        raise SystemExit(f"MatrixMarket nnz mismatch: header {nnz}, read {k}")
    m = sp.csr_matrix((vals, (cols, rows)), shape=(n_cells, n_genes), dtype=np.float32)
    del rows, cols, vals
    m.sum_duplicates()
    return m


def zscore_cols(x: np.ndarray) -> np.ndarray:
    mu = x.mean(axis=0)
    sd = x.std(axis=0)
    sd[sd == 0] = np.nan
    return (x - mu) / sd


def signature(logx: sp.csr_matrix, gene_index: dict, genes_signed: dict) -> tuple[np.ndarray, int]:
    """Paper's score: mean over genes of sign * z-scaled log expression across cells."""
    use = [(gene_index[g], s) for g, s in genes_signed.items() if g in gene_index]
    if not use:
        return np.full(logx.shape[0], np.nan), 0
    cols = [c for c, _ in use]
    signs = np.array([s for _, s in use], dtype=np.float32)
    dense = logx[:, cols].toarray()
    z = zscore_cols(dense)
    keep = ~np.all(np.isnan(z), axis=0)
    z, signs = z[:, keep], signs[keep]
    return np.nanmean(z * signs, axis=1), int(keep.sum())


def seurat_hvg(logx: sp.csr_matrix, batches: np.ndarray, min_mean=0.0125, max_mean=3.0, min_disp=0.5):
    """Seurat-flavour HVG with batches (scanpy defaults), reimplemented to avoid AnnData copies."""
    votes = np.zeros(logx.shape[1], dtype=int)
    for b in np.unique(batches):
        sub = logx[batches == b]
        expm = sub.copy()
        expm.data = np.expm1(expm.data)
        mean = np.asarray(expm.mean(axis=0)).ravel()
        sq = expm.copy()
        sq.data **= 2
        var = np.asarray(sq.mean(axis=0)).ravel() - mean ** 2
        var *= sub.shape[0] / max(1, sub.shape[0] - 1)
        mean[mean == 0] = 1e-12
        disp = var / mean
        disp[disp == 0] = np.nan
        logdisp = np.log(disp)
        logmean = np.log1p(mean)
        bins = pd.cut(logmean, bins=20)
        grp = pd.Series(logdisp).groupby(bins, observed=False)
        avg, sd = grp.transform("mean").to_numpy(), grp.transform("std").to_numpy()
        norm = (logdisp - avg) / sd
        votes += ((logmean > min_mean) & (logmean < max_mean) & (norm > min_disp)).astype(int)
    return votes >= 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--r3-run", required=True, help="Wp-R3 run directory holding signatures.csv")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, out = Path(args.data_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    manifests = ["acquisition_v1.json", "acquisition_v2_supplements.json", "acquisition_v3_matrices.json"]
    verified = []
    for m in manifests:
        for rec in json.loads((root / m).read_text(encoding="utf-8"))["files"]:
            p = root / rec["file"]
            if p.exists():
                verified.append({"file": rec["file"], "match": sha256(p) == rec["sha256"]})
    need = {"GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz", "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz",
            "GSE289733_filtered_feature_bc_matrix_features.tsv.gz", "NIHMS2092659-supplement-2.xlsx",
            "NIHMS2092659-supplement-3.xlsx", "NIHMS2092659-supplement-4.xlsx", "NIHMS2092659-supplement-5.xlsx"}
    ok = {v["file"] for v in verified if v["match"]}
    if not need <= ok:
        raise SystemExit(f"Missing or unverified inputs: {sorted(need - ok)}")

    # --- load ---------------------------------------------------------------
    barcodes = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_barcodes.tsv.gz", header=None)[0].to_numpy()
    feats = pd.read_csv(root / "GSE289733_filtered_feature_bc_matrix_features.tsv.gz", sep="\t", header=None)
    with gzip.open(root / "GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz", "rt") as fh:
        for line in fh:
            if not line.startswith("%"):
                ng, nc, nnz = map(int, line.split())
                break
    X = read_mtx_cells_by_genes(root / "GSE289733_filtered_feature_bc_matrix_matrix.mtx.gz", ng, nc, nnz)
    symbols = feats[1].astype(str).str.upper().to_numpy()
    library = np.array([b.rsplit("-", 1)[1] for b in barcodes])

    # --- QC (declared substitution: the authors' thresholds are not stated) ---
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
        keep = (n_genes[m] >= 500) & (mito_frac[m] <= 0.10) & (lt >= med - 3 * mad) & (lt <= med + 3 * mad)
        qc[np.where(m)[0]] = keep
        qc_rows.append({"library": lib, "n_barcodes": int(m.sum()), "n_pass_qc": int(keep.sum()),
                        "median_genes": float(np.median(n_genes[m])), "median_umi": float(np.median(total[m])),
                        "median_mito_frac": float(np.median(mito_frac[m]))})
    X = X[qc]
    library, barcodes = library[qc], barcodes[qc]
    total = total[qc]
    # drop genes never detected after QC, then collapse duplicate upper-case symbols by keeping the first
    detected = np.asarray((X > 0).sum(axis=0)).ravel() > 0
    _, first = np.unique(symbols, return_index=True)
    keepg = np.zeros(len(symbols), dtype=bool)
    keepg[first] = True
    keepg &= detected
    X = X[:, keepg]
    symbols = symbols[keepg]
    gidx = {g: i for i, g in enumerate(symbols)}

    # library pseudobulk (CPM) for label derivation and the interaction model
    libs = sorted(np.unique(library), key=int)
    pb = np.vstack([np.asarray(X[library == l].sum(axis=0)).ravel() for l in libs])
    cpm = pb / pb.sum(axis=1, keepdims=True) * 1e6
    lcpm = np.log2(cpm + 1)

    # normalise cells: CP10K + log1p, in place
    X = sp.csr_matrix(X, dtype=np.float32)
    scale = 1e4 / np.maximum(np.asarray(X.sum(axis=1)).ravel(), 1)
    X = sp.diags(scale.astype(np.float32)) @ X
    X.data = np.log1p(X.data)
    X = X.tocsr()

    # --- 1. derive condition labels per library ------------------------------
    def gmean(genes):
        cols = [gidx[g] for g in genes if g in gidx]
        return lcpm[:, cols].mean(axis=1), [g for g in genes if g in gidx]

    p_score, p_used = gmean(TH17P_MARKERS)
    n_score, n_used = gmean(TH17N_MARKERS)
    type_score = p_score - n_score
    order = np.argsort(type_score)
    derived_type = np.empty(len(libs), dtype=object)
    derived_type[order[:4]] = "Th17n"
    derived_type[order[4:]] = "Th17p"
    sorted_ts = np.sort(type_score)
    type_gap = float(sorted_ts[4] - sorted_ts[3])
    type_within = float(max(np.diff(sorted_ts[:4]).max(), np.diff(sorted_ts[4:]).max()))
    txnip = lcpm[:, gidx[GLUCOSE_MARKER]]
    derived_glu = np.empty(len(libs), dtype=object)
    glu_gaps = {}
    for t in ("Th17n", "Th17p"):
        ii = np.where(derived_type == t)[0]
        o = ii[np.argsort(txnip[ii])]
        derived_glu[o[:2]] = "1mM"
        derived_glu[o[2:]] = "25mM"
        v = np.sort(txnip[ii])
        glu_gaps[t] = {"between": float(v[2] - v[1]), "within_max": float(max(v[1] - v[0], v[3] - v[2]))}
    lab_rows = []
    for i, l in enumerate(libs):
        pt, pg, pa = PRIOR_ORDER[l]
        agree = (derived_type[i] == pt) and (derived_glu[i] == pg)
        lab_rows.append({"library": l, "prior_cell_type": pt, "prior_glucose": pg, "prior_animal": pa,
                         "th17p_minus_th17n_marker_score": float(type_score[i]), "txnip_log2cpm": float(txnip[i]),
                         "derived_cell_type": derived_type[i], "derived_glucose": derived_glu[i],
                         "agrees_with_prior": bool(agree),
                         "animal_label": pa if agree else "unknown",
                         "animal_status": "prior_only_untested" if agree else "unassigned"})
    labels = pd.DataFrame(lab_rows)
    qcdf = pd.DataFrame(qc_rows).merge(labels, on="library")
    qcdf.to_csv(out / "library_labels.csv", index=False, lineterminator="\n")
    lab = labels.set_index("library")
    cell_type = lab.loc[library, "derived_cell_type"].to_numpy()
    glucose = lab.loc[library, "derived_glucose"].to_numpy()
    animal = lab.loc[library, "animal_label"].to_numpy()

    # --- 2. gene sets ---------------------------------------------------------
    s1 = pd.read_excel(root / "NIHMS2092659-supplement-2.xlsx", sheet_name="Table S1")
    s1["symbol"] = s1["symbol"].astype(str).str.upper()
    s1["is_HVG"] = s1["is_HVG"].astype(str).str.lower().eq("true")
    s3 = pd.read_excel(root / "NIHMS2092659-supplement-3.xlsx", sheet_name="Table S3")
    s3 = s3.rename(columns={s3.columns[0]: "comparison"})
    s3["symbol"] = s3["symbol"].astype(str).str.upper()
    s4 = pd.read_excel(root / "NIHMS2092659-supplement-4.xlsx", sheet_name="Table S4")
    s4 = s4.rename(columns={s4.columns[0]: "symbol", s4.columns[1]: "rho_source", s4.columns[2]: "partial_rho_source"})
    s4["symbol"] = s4["symbol"].astype(str).str.upper()
    s5 = pd.read_excel(root / "NIHMS2092659-supplement-5.xlsx", sheet_name="Table S5")
    s5["marker genes"] = s5["marker genes"].astype(str).str.upper()
    r3sig = pd.read_csv(Path(args.r3_run) / "signatures.csv")
    r3sig["symbol"] = r3sig["symbol"].astype(str).str.upper()

    hvg = seurat_hvg(X, animal)
    hvg_set = set(symbols[hvg])

    def mod(module, hvg_mode):
        sub = s1[s1["module"] == module]
        if hvg_mode == "authors":
            sub = sub[sub["is_HVG"]]
        elif hvg_mode == "local":
            sub = sub[sub["symbol"].isin(hvg_set)]
        return {g: 1 for g in sub["symbol"]}

    def s3sig(comparison, hvg_mode):
        sub = s3[(s3["comparison"] == comparison) & (s3["adj.P.Val"] <= SIGNATURE_ALPHA)
                 & (s3["logFC"].abs() >= SIGNATURE_LFC)]
        if hvg_mode == "local":
            sub = sub[sub["symbol"].isin(hvg_set)]
        return {g: int(np.sign(v)) for g, v in zip(sub["symbol"], sub["logFC"])}

    def r3s(name, hvg_mode):
        sub = r3sig[r3sig["signature"] == name]
        if hvg_mode == "local":
            sub = sub[sub["symbol"].isin(hvg_set)]
        return {g: int(s) for g, s in zip(sub["symbol"], sub["sign"])}

    scores, ngenes = {}, {}
    for mode in ("authors", "local", "all"):
        pi, n1 = signature(X, gidx, mod("pro-inflammatory", mode))
        pr, n2 = signature(X, gidx, mod("pro-regulatory", mode))
        scores[f"proinflammatory_{mode}"], scores[f"proregulatory_{mode}"] = pi, pr
        scores[f"pathogenicity_{mode}"] = pi - pr
        ngenes[f"proinflammatory_{mode}"], ngenes[f"proregulatory_{mode}"] = n1, n2
    for mode in ("local", "all"):
        for comp in ("Th17n.EGCG", "Th17n.DHEA"):
            v, n = signature(X, gidx, s3sig(comp, mode))
            scores[f"{comp.replace('.', '_')}_S3_{mode}"], ngenes[f"{comp.replace('.', '_')}_S3_{mode}"] = v, n
        for name in ("Th17n.Div.1.EGCG", "Th17n.Div.1.DHEA"):
            v, n = signature(X, gidx, r3s(name, mode))
            key = f"{name.replace('.', '_')}_R3_{mode}"
            scores[key], ngenes[key] = v, n
    prol, nprol = signature(X, gidx, {g: 1 for g in PROLIFERATION})
    scores["proliferation"], ngenes["proliferation"] = prol, nprol

    # --- 3. programme assignment from Table S5 markers --------------------------
    prog_sets = {p: set(g["marker genes"]) for p, g in s5.groupby("program")}
    s1_genes = set(s1["symbol"])
    egcg_genes = set(s3sig("Th17n.EGCG", "all"))
    overlap = {p: {"n_markers": len(gs), "n_in_S1_modules": len(gs & s1_genes),
                   "n_in_EGCG_signature": len(gs & egcg_genes)} for p, gs in prog_sets.items()}
    progs_for = {"Th17n": ["N1", "N2", "N3"], "Th17p": ["P1", "P2", "P3", "P4"]}
    prog_score = {}
    for variant, exclude in (("all_markers", set()), ("excl_S1_and_EGCG", s1_genes | egcg_genes)):
        for p, gs in prog_sets.items():
            prog_score[(variant, p)] = signature(X, gidx, {g: 1 for g in gs - exclude})[0]
    programme = {}
    for variant in ("all_markers", "excl_S1_and_EGCG"):
        lab_v = np.empty(X.shape[0], dtype=object)
        for t, plist in progs_for.items():
            m = cell_type == t
            mat = np.vstack([prog_score[(variant, p)][m] for p in plist]).T
            lab_v[m] = np.array(plist)[np.nanargmax(mat, axis=1)]
        programme[variant] = lab_v

    cells = pd.DataFrame({"barcode": barcodes, "library": library, "cell_type": cell_type, "glucose": glucose,
                          "animal": animal, "total_umi": total, **scores,
                          "programme": programme["all_markers"],
                          "programme_excl_overlap": programme["excl_S1_and_EGCG"]})
    cells.to_csv(out / "cell_scores.csv.gz", index=False, compression="gzip", lineterminator="\n")

    # --- 4. endpoints ------------------------------------------------------------
    arms = ["proinflammatory", "proregulatory", "pathogenicity"]
    # Fig 3C: per library means, and within-animal low-minus-high glucose differences
    libsum = cells.groupby(["library", "cell_type", "glucose", "animal"])[
        [f"{a}_{m}" for a in arms for m in ("authors", "local", "all")] + ["proliferation"]].mean().reset_index()
    libsum["n_cells"] = cells.groupby(["library"]).size().reindex(libsum["library"]).to_numpy()
    libsum.to_csv(out / "library_score_means.csv", index=False, lineterminator="\n")
    paired = []
    for t in ("Th17n", "Th17p"):
        for an in sorted(set(libsum["animal"]) - {"unknown"}):
            lo = libsum[(libsum.cell_type == t) & (libsum.glucose == "1mM") & (libsum.animal == an)]
            hi = libsum[(libsum.cell_type == t) & (libsum.glucose == "25mM") & (libsum.animal == an)]
            if len(lo) == 1 and len(hi) == 1:
                row = {"cell_type": t, "animal": an}
                for a in arms:
                    for m in ("authors", "local", "all"):
                        row[f"{a}_{m}_low_minus_high"] = float(lo[f"{a}_{m}"].iloc[0] - hi[f"{a}_{m}"].iloc[0])
                row["proliferation_low_minus_high"] = float(lo["proliferation"].iloc[0] - hi["proliferation"].iloc[0])
                # cell-level effect size within this animal (descriptive only)
                cl = cells[(cells.cell_type == t) & (cells.animal == an)]
                for a in arms:
                    x = cl.loc[cl.glucose == "1mM", f"{a}_authors"]
                    y = cl.loc[cl.glucose == "25mM", f"{a}_authors"]
                    row[f"{a}_authors_cell_smd"] = float((x.mean() - y.mean()) /
                                                         np.sqrt((x.var() + y.var()) / 2))
                paired.append(row)
    pd.DataFrame(paired).to_csv(out / "glucose_paired_differences.csv", index=False, lineterminator="\n")

    # Fig 3E/3G/3H: composition and scores by programme
    comp = (cells.groupby(["library", "cell_type", "glucose", "animal", "programme"]).size()
            .rename("n").reset_index())
    comp["fraction"] = comp["n"] / comp.groupby("library")["n"].transform("sum")
    comp.to_csv(out / "programme_composition.csv", index=False, lineterminator="\n")
    comp2 = (cells.groupby(["library", "cell_type", "glucose", "animal", "programme_excl_overlap"]).size()
             .rename("n").reset_index())
    comp2["fraction"] = comp2["n"] / comp2.groupby("library")["n"].transform("sum")
    comp2.to_csv(out / "programme_composition_excl_overlap.csv", index=False, lineterminator="\n")
    agree_prog = float((cells["programme"] == cells["programme_excl_overlap"]).mean())

    prog_rows = []
    for variant, col in (("all_markers", "programme"), ("excl_S1_and_EGCG", "programme_excl_overlap")):
        for (l, t, gl, an, p), sub in cells.groupby(["library", "cell_type", "glucose", "animal", col]):
            prog_rows.append({"variant": variant, "library": l, "cell_type": t, "glucose": gl, "animal": an,
                              "programme": p, "n_cells": len(sub),
                              "pathogenicity_authors_median": float(sub["pathogenicity_authors"].median()),
                              "Th17n_EGCG_S3_local_median": float(sub["Th17n_EGCG_S3_local"].median()),
                              "Th17n_EGCG_S3_all_median": float(sub["Th17n_EGCG_S3_all"].median()),
                              "Th17n_DHEA_S3_local_median": float(sub["Th17n_DHEA_S3_local"].median())})
    prog = pd.DataFrame(prog_rows)
    prog.to_csv(out / "programme_scores_by_library.csv", index=False, lineterminator="\n")

    # within each Th17n library: is N1 the lowest on pathogenicity and EGCG signature?
    n1_checks = []
    for variant in ("all_markers", "excl_S1_and_EGCG"):
        sub = prog[(prog.variant == variant) & (prog.cell_type == "Th17n")]
        for l, g in sub.groupby("library"):
            g = g[g.n_cells >= 20]
            if "N1" not in set(g.programme) or len(g) < 2:
                continue
            for metric in ("pathogenicity_authors_median", "Th17n_EGCG_S3_local_median", "Th17n_EGCG_S3_all_median"):
                n1v = float(g.loc[g.programme == "N1", metric].iloc[0])
                others = g.loc[g.programme != "N1", metric]
                n1_checks.append({"variant": variant, "library": l, "metric": metric, "N1": n1v,
                                  "min_other": float(others.min()), "N1_is_lowest": bool(n1v < others.min()),
                                  "n_programmes_with_20_cells": int(len(g))})
    pd.DataFrame(n1_checks).to_csv(out / "n1_lowest_checks.csv", index=False, lineterminator="\n")

    # Fig 2E: per-cell correlation of signatures with pathogenicity in Th17n 25 mM cells
    corr_rows = []
    sigcols = ["Th17n_EGCG_S3_local", "Th17n_DHEA_S3_local", "Th17n_EGCG_S3_all", "Th17n_DHEA_S3_all",
               "Th17n_Div_1_EGCG_R3_local", "Th17n_Div_1_DHEA_R3_local"]
    for scope, m in (("Th17n_25mM_pooled", (cells.cell_type == "Th17n") & (cells.glucose == "25mM")),
                     ("Th17n_all_glucose_pooled", cells.cell_type == "Th17n")):
        for sc in sigcols:
            x, y = cells.loc[m, sc], cells.loc[m, "pathogenicity_authors"]
            corr_rows.append({"scope": scope, "library": "pooled", "signature": sc, "n_cells": int(m.sum()),
                              "pearson": float(x.corr(y)), "spearman": float(x.corr(y, method="spearman"))})
        for l in sorted(set(cells.loc[m, "library"]), key=int):
            mm = m & (cells.library == l)
            for sc in sigcols:
                x, y = cells.loc[mm, sc], cells.loc[mm, "pathogenicity_authors"]
                corr_rows.append({"scope": scope, "library": l, "signature": sc, "n_cells": int(mm.sum()),
                                  "pearson": float(x.corr(y)), "spearman": float(x.corr(y, method="spearman"))})
    # circularity check: signature genes overlapping the S1 modules removed
    egcg_noov = {g: s for g, s in s3sig("Th17n.EGCG", "local").items() if g not in s1_genes}
    dhea_noov = {g: s for g, s in s3sig("Th17n.DHEA", "local").items() if g not in s1_genes}
    m = (cells.cell_type == "Th17n") & (cells.glucose == "25mM")
    for name, gs in (("Th17n_EGCG_S3_local_noS1overlap", egcg_noov), ("Th17n_DHEA_S3_local_noS1overlap", dhea_noov)):
        v, n = signature(X, gidx, gs)
        x, y = pd.Series(v[m.to_numpy()]), pd.Series(cells.loc[m, "pathogenicity_authors"].to_numpy())
        corr_rows.append({"scope": "Th17n_25mM_pooled", "library": "pooled", "signature": name, "n_cells": int(m.sum()),
                          "pearson": float(x.corr(y)), "spearman": float(x.corr(y, method="spearman")),
                          "n_signature_genes": n})
    pd.DataFrame(corr_rows).to_csv(out / "signature_pathogenicity_correlations.csv", index=False, lineterminator="\n")
    s1_overlap = {"EGCG_signature_local": len(set(s3sig("Th17n.EGCG", "local")) & s1_genes),
                  "EGCG_signature_local_total": len(s3sig("Th17n.EGCG", "local")),
                  "DHEA_signature_local": len(set(s3sig("Th17n.DHEA", "local")) & s1_genes),
                  "DHEA_signature_local_total": len(s3sig("Th17n.DHEA", "local"))}

    # Table S4: per-gene Spearman with the EGCG signature in Th17n cells vs the authors' values
    th17n = (cells.cell_type == "Th17n").to_numpy()
    egcg_v = cells.loc[th17n, "Th17n_EGCG_S3_local"].to_numpy()
    dhea_v = cells.loc[th17n, "Th17n_DHEA_S3_local"].to_numpy()
    s4g = [g for g in s4["symbol"] if g in gidx]
    dense = X[th17n][:, [gidx[g] for g in s4g]].toarray()
    re = stats.rankdata(egcg_v)
    rd = stats.rankdata(dhea_v)
    rows4 = []
    for j, g in enumerate(s4g):
        rg = stats.rankdata(dense[:, j])
        r_ge = np.corrcoef(rg, re)[0, 1]
        r_gd, r_ed = np.corrcoef(rg, rd)[0, 1], np.corrcoef(re, rd)[0, 1]
        partial = (r_ge - r_gd * r_ed) / np.sqrt((1 - r_gd ** 2) * (1 - r_ed ** 2))
        rows4.append({"symbol": g, "rho_ours": r_ge, "partial_rho_ours": partial})
    s4m = s4.merge(pd.DataFrame(rows4), on="symbol")
    s4m.to_csv(out / "tableS4_concordance.csv", index=False, lineterminator="\n")
    s4_summary = {"n_genes": int(len(s4m)),
                  "pearson_rho": float(s4m["rho_source"].corr(s4m["rho_ours"])),
                  "pearson_partial_rho": float(s4m["partial_rho_source"].corr(s4m["partial_rho_ours"])),
                  "sign_agreement_rho": float((np.sign(s4m["rho_source"]) == np.sign(s4m["rho_ours"])).mean())}

    # Fig 3D: glucose x cell-type interaction on library pseudobulk with animal covariate
    lab_ok = labels[labels.animal_label != "unknown"].set_index("library")
    inter_rows = []
    if len(lab_ok) == 8:
        li = [libs.index(l) for l in lab_ok.index]
        Y = lcpm[li]
        # Keep a gene if it reaches 1 CPM in at least half the libraries. A
        # higher floor silently drops cell-type-restricted transcripts such as
        # FOXP3 and TBX21, which are exactly the genes Figure 3D names.
        expressed = (cpm[li] >= 1).mean(axis=0) >= 0.5
        cpm_named = {g: round(float(np.median(cpm[li, gidx[g]])), 3)
                     for groups in PAPER_FIG3D.values() for genes in groups.values()
                     for g in genes if g in gidx}
        D = pd.DataFrame({"type": (lab_ok["derived_cell_type"] == "Th17p").astype(float).to_numpy(),
                          "glu": (lab_ok["derived_glucose"] == "25mM").astype(float).to_numpy(),
                          "animal": (lab_ok["animal_label"] == "Mo2").astype(float).to_numpy()})
        D["inter"] = D["type"] * D["glu"]
        A = np.column_stack([np.ones(8), D[["animal", "type", "glu", "inter"]].to_numpy()])
        coef, *_ = np.linalg.lstsq(A, Y[:, expressed], rcond=None)
        resid = Y[:, expressed] - A @ coef
        dfr = 8 - A.shape[1]
        s2 = (resid ** 2).sum(axis=0) / dfr
        XtXi = np.linalg.inv(A.T @ A)
        t_inter = coef[4] / np.sqrt(s2 * XtXi[4, 4])
        p_inter = 2 * stats.t.sf(np.abs(t_inter), dfr)
        eg = symbols[expressed]
        glu_eff_n = coef[3]                 # 25mM minus 1mM in Th17n
        glu_eff_p = coef[3] + coef[4]       # 25mM minus 1mM in Th17p
        inter = pd.DataFrame({"symbol": eg, "glucose_effect_Th17n": glu_eff_n, "glucose_effect_Th17p": glu_eff_p,
                              "interaction": coef[4], "t_interaction": t_inter, "p_interaction": p_inter,
                              "bh_interaction": bh(p_inter)})
        inter.to_csv(out / "glucose_interaction_pseudobulk.csv.gz", index=False, compression="gzip",
                     lineterminator="\n")
        for t, groups in PAPER_FIG3D.items():
            col = f"glucose_effect_{t}"
            for direction, genes in groups.items():
                for g in genes:
                    row = inter[inter.symbol == g]
                    inter_rows.append({"cell_type": t, "paper_claim": direction, "symbol": g,
                                       "glucose_effect_25mM_minus_1mM": float(row[col].iloc[0]) if len(row) else None,
                                       "p_interaction": float(row["p_interaction"].iloc[0]) if len(row) else None,
                                       "median_library_cpm": cpm_named.get(g),
                                       "expressed": bool(len(row))})
        pd.DataFrame(inter_rows).to_csv(out / "fig3d_named_genes.csv", index=False, lineterminator="\n")
        inter_summary = {"n_expressed_genes": int(expressed.sum()), "residual_df": int(dfr),
                         "n_p_lt_0.001": int((p_inter < 0.001).sum()), "n_bh_0.05": int((bh(p_inter) <= 0.05).sum()),
                         "expression_floor_cpm": 1.0, "min_fraction_libraries": 0.5}
    else:
        inter_summary = {"status": "not_fitted_animal_labels_unresolved"}

    results = {
        "schema": "wp_r1_singlecell/v1", "inputs_verified": verified,
        "unit": "library (8) nested in animal (2); animals crossed with all four conditions",
        "qc": qc_rows, "n_cells_after_qc": int(X.shape[0]), "n_genes_after_qc": int(X.shape[1]),
        "label_derivation": {"th17p_markers_used": p_used, "th17n_markers_used": n_used,
                             "type_gap_between_groups": type_gap, "type_max_gap_within_groups": type_within,
                             "glucose_gaps": glu_gaps, "all_libraries_agree_with_prior":
                                 bool(labels["agrees_with_prior"].all()), "labels": lab_rows},
        "cells_by_condition": cells.groupby(["cell_type", "glucose"]).size().rename("n").reset_index()
        .to_dict(orient="records"),
        "n_local_hvg": int(hvg.sum()), "genes_scored": ngenes,
        "s1_authors_hvg_flags_recovered_as_local_hvg": {
            m: int(s1[(s1.module == m) & s1.is_HVG & s1.symbol.isin(hvg_set)].shape[0]) for m in
            ("pro-inflammatory", "pro-regulatory")},
        "programme_marker_overlap": overlap, "programme_assignment_agreement_after_overlap_removal": agree_prog,
        "signature_S1_overlap": s1_overlap, "tableS4_concordance": s4_summary,
        "glucose_interaction": inter_summary,
        "interpretation_limit": ("Reproduction of the source's own single-cell analysis on its deposit. Labels are "
                                 "derived; animal identity is a prior; the analysed 5,192-cell set and scVI model are "
                                 "not deposited, so cell membership differs. Two animals cannot support population "
                                 "inference and agreement is not independent replication."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True, default=str) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
