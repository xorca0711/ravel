#!/usr/bin/env python
"""A30 successor (v2): the de novo cell-state decomposition on the full feature space.

The frozen A30 design asked for the paired CSF-minus-blood difference to be
split into composition and within-state terms on two bases. Run
wp_a30_activation_stratified_v2 delivered the activation-stratum basis and
recorded that the second basis, de novo cell states, did not execute: the
parallel k-nearest-neighbour backend raises PermissionError WinError 5 in this
sandbox, which is an environment restriction, not a property of the data. That
deviation is declared in that run's results.json and is discharged here rather
than left open.

Nothing about the question, the modules, the paired contrast or the stop rule
changes. This entrypoint re-reads the deposit under the identical Wp-R4 v2
gate, asserts the recovered cell set is the one already analysed, clusters the
cells from genes outside both modules and outside the activation panel, and
reports the decomposition. The k-nearest-neighbour graph is built with the
exact scikit-learn backend and all thread pools pinned to one worker, so the
result does not depend on a parallel scheduler.

Why the composition basis matters: a CSF-enriched Th17-lineage subset would
raise an effector module through mixture alone, with no cell changing state.
That is the rival a stratified contrast cannot address, and the one a described
CCR5-high Th17.1 population makes concrete.

Unit: donor, paired. Cells are observations within donor.
"""
from __future__ import annotations

import os

# Pinned before scanpy imports, because the restriction is in the thread-pool
# creation path rather than in any computation.
for _v in ("NUMBA_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
           "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["JOBLIB_MULTIPROCESSING"] = "0"

import argparse
import gzip
import hashlib
import io
import json
import re
import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats

# --- frozen constants, identical to Wp-R4 v2 where the pipeline is shared ----
T_MARKERS = ["CD3D", "CD3E", "CD3G", "TRAC", "TRBC2"]
CD8_MARKERS = ["CD8A", "CD8B"]
LINEAGE_PANELS = {"B": ["MS4A1", "CD79A", "CD79B"],
                  "myeloid": ["LYZ", "CD14", "FCN1", "AIF1"],
                  "NK": ["GNLY", "NKG7", "KLRD1"],
                  "ery_plt": ["HBB", "HBA1", "PPBP"]}
RAW_BARCODE_LIMIT = 100_000
RAW_UMI_FLOOR = 500
MIN_GENES = 200
MAX_MITO = 0.10
MAD_K = 3.0
MIN_CELLS = 20

# --- frozen for this analysis ------------------------------------------------
ACTIVATION_PANEL = ["CD69", "JUN", "JUNB", "FOS", "FOSB", "DUSP1", "NR4A1", "NR4A2",
                    "IER2", "EGR1", "KLF6", "NFKBIA", "CD38", "HLA-DRA", "HLA-DRB1",
                    "IL2RA", "ICOS", "TNFRSF9", "TNFRSF4", "CD27", "TNFAIP3"]
PROLIFERATION = ["MKI67", "TOP2A", "PCNA", "TYMS", "CCNB1", "CDK1", "UBE2C", "BIRC5",
                 "STMN1", "RRM2"]
N_STRATA = 3
STRATUM_FLOOR = 50
N_DRAWS = 1000
SEED = 20261005
N_HVG = 2000
N_PCS = 30
LEIDEN_RES = 1.0
PRIMARY_FAMILY = ["proinflammatory_authors", "proregulatory_authors"]
REPORTED = PRIMARY_FAMILY + ["proinflammatory_all", "proregulatory_all",
                             "activation_disjoint", "programme_N3", "proliferation"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sample(tar, trio, needed):
    """One pass over a CellRanger v2 trio; QC vectors plus cells x needed counts."""
    with gzip.open(io.BytesIO(tar.extractfile(trio["genes"]).read()), "rt") as fh:
        genes = pd.read_csv(fh, sep="\t", header=None)
    symbols = genes[1].astype(str).str.upper().to_numpy()
    n_barcodes = sum(1 for _ in gzip.open(io.BytesIO(tar.extractfile(trio["barcodes"]).read()), "rt"))

    want = {}
    for i, s in enumerate(symbols):
        if s in needed and s not in want:
            want[s] = i
    is_mito = np.array([s.startswith("MT-") for s in symbols])
    col_of = np.full(len(symbols), -1, dtype=np.int64)
    for j, (s, i) in enumerate(sorted(want.items())):
        col_of[i] = j
    kept_symbols = [s for s, _ in sorted(want.items())]

    with gzip.open(io.BytesIO(tar.extractfile(trio["matrix"]).read()), "rt") as fh:
        line = fh.readline()
        while line.startswith("%"):
            line = fh.readline()
        n_genes, n_cells, nnz = (int(v) for v in line.split())
        total = np.zeros(n_cells, dtype=np.float64)
        ngene = np.zeros(n_cells, dtype=np.int32)
        mtot = np.zeros(n_cells, dtype=np.float64)
        ri, ci, vv = [], [], []
        for raw in fh:
            g, c, v = raw.split()
            gi, ci_, val = int(g) - 1, int(c) - 1, float(v)
            total[ci_] += val
            ngene[ci_] += 1
            if is_mito[gi]:
                mtot[ci_] += val
            j = col_of[gi]
            if j >= 0:
                ri.append(ci_); ci.append(j); vv.append(val)
    counts = sp.csr_matrix((np.array(vv, dtype=np.float32), (np.array(ri), np.array(ci))),
                           shape=(n_cells, len(kept_symbols)))
    qc = pd.DataFrame({"total": total, "n_genes": ngene,
                       "mito_frac": np.divide(mtot, np.maximum(total, 1))})
    return counts, qc, kept_symbols, n_barcodes, (n_genes, n_cells, nnz)


def read_gated_full(tar, trio, gate, keep_symbols):
    """Second pass over the same trio keeping gated cells across keep_symbols."""
    with gzip.open(io.BytesIO(tar.extractfile(trio["genes"]).read()), "rt") as fh:
        genes = pd.read_csv(fh, sep="\t", header=None)
    symbols = genes[1].astype(str).str.upper().to_numpy()
    col_of = np.full(len(symbols), -1, dtype=np.int64)
    pos = {s: j for j, s in enumerate(keep_symbols)}
    seen = set()
    for i, s in enumerate(symbols):
        if s in pos and s not in seen:
            col_of[i] = pos[s]; seen.add(s)
    row_of = np.full(len(gate), -1, dtype=np.int64)
    row_of[np.flatnonzero(gate)] = np.arange(int(gate.sum()))
    with gzip.open(io.BytesIO(tar.extractfile(trio["matrix"]).read()), "rt") as fh:
        line = fh.readline()
        while line.startswith("%"):
            line = fh.readline()
        ri, ci, vv = [], [], []
        for raw in fh:
            g, c, v = raw.split()
            j = col_of[int(g) - 1]
            if j < 0:
                continue
            r = row_of[int(c) - 1]
            if r < 0:
                continue
            ri.append(r); ci.append(j); vv.append(float(v))
    return sp.csr_matrix((np.array(vv, dtype=np.float32), (np.array(ri), np.array(ci))),
                         shape=(int(gate.sum()), len(keep_symbols)))


def pooled_z_scores(X, gidx, sd, mu, signed):
    """Mean signed z-score over mapped genes; the Wp-R4 v2 convention, unchanged."""
    use = [(gidx[g], s) for g, s in signed.items() if g in gidx and sd[gidx[g]] > 0]
    if not use:
        return np.full(X.shape[0], np.nan), 0
    cols = [c for c, _ in use]
    sgn = np.array([s for _, s in use], dtype=np.float32)
    sub = np.asarray(X[:, cols].todense())
    z = (sub - mu[cols]) / sd[cols]
    return (z * sgn).mean(axis=1), len(use)


def kitagawa(w_a, m_a, w_b, m_b):
    """Symmetric decomposition; composition + within equals the total exactly."""
    comp = float(np.sum((w_a - w_b) * (m_a + m_b) / 2.0))
    within = float(np.sum((w_a + w_b) / 2.0 * (m_a - m_b)))
    return comp, within


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--r4-run", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, out = Path(args.data_root), Path(args.output)
    r4 = Path(args.r4_run)
    out.mkdir(parents=True, exist_ok=True)

    verified = {f: sha256(root / f) for f in
                ["GSE138266_RAW.tar", "GSE138266_samples.soft.txt", "acquisition_v1.json",
                 "acquisition_v3_matrices.json", "NIHMS2092659-supplement-2.xlsx",
                 "NIHMS2092659-supplement-5.xlsx"]}
    for f in ["cell_scores.csv.gz", "sample_qc.csv"]:
        verified[f"wp_human_signature_transfer_v2/{f}"] = sha256(r4 / f)

    # --- gene sets ----------------------------------------------------------
    s1 = pd.read_excel(root / "NIHMS2092659-supplement-2.xlsx", sheet_name="Table S1")
    s1.columns = [str(c).strip() for c in s1.columns]
    gene_col = [c for c in s1.columns if c.lower() in ("gene", "symbol", "gene_symbol")][0]
    mod_col = [c for c in s1.columns if "module" in c.lower() or "program" in c.lower()][0]
    hvg_col = [c for c in s1.columns if "hvg" in c.lower()][0]
    s1["symbol"] = s1[gene_col].astype(str).str.upper().str.strip()
    s1["is_hvg"] = s1[hvg_col].astype(str).str.upper().isin(["TRUE", "YES", "1", "1.0"])
    modules = {}
    for mod, sub in s1.groupby(mod_col):
        key = "proinflammatory" if "inflam" in str(mod).lower() else "proregulatory"
        modules[key] = {"authors": sorted(set(sub.loc[sub.is_hvg, "symbol"])),
                        "all": sorted(set(sub["symbol"]))}
    module_union = set(modules["proinflammatory"]["all"]) | set(modules["proregulatory"]["all"])

    # the disjointness the design rests on, asserted rather than assumed
    overlap = sorted(set(ACTIVATION_PANEL) & module_union)
    if overlap:
        raise SystemExit(f"activation panel overlaps the modules: {overlap}")

    s5 = pd.read_excel(root / "NIHMS2092659-supplement-5.xlsx", sheet_name="Table S5")
    s5.columns = [str(c).strip() for c in s5.columns]
    prog_col = [c for c in s5.columns if "program" in c.lower()][0]
    mark_col = [c for c in s5.columns if "gene" in c.lower()][0]
    # Table S5 is long-format, one marker gene per row with the programme name
    # repeated, so rows must be accumulated rather than assigned. v1 of this
    # entrypoint assigned, which left each programme holding its last single
    # gene; see the supersession note in the contract.
    programmes = {}
    for _, r in s5.iterrows():
        name = str(r[prog_col]).strip()
        genes = [g.strip().upper() for g in re.split(r"[,;\s]+", str(r[mark_col])) if g.strip()]
        programmes.setdefault(f"programme_{name}", []).extend(genes)
    programmes = {k: sorted(set(v)) for k, v in programmes.items()}

    score_sets = {
        "proinflammatory_authors": {g: 1 for g in modules["proinflammatory"]["authors"]},
        "proinflammatory_all": {g: 1 for g in modules["proinflammatory"]["all"]},
        "proregulatory_authors": {g: 1 for g in modules["proregulatory"]["authors"]},
        "proregulatory_all": {g: 1 for g in modules["proregulatory"]["all"]},
        "activation_disjoint": {g: 1 for g in ACTIVATION_PANEL},
        "proliferation": {g: 1 for g in PROLIFERATION},
    }
    for name, genes in programmes.items():
        score_sets[name] = {g: 1 for g in genes}

    # --- samples ------------------------------------------------------------
    soft = (root / "GSE138266_samples.soft.txt").read_text(encoding="utf-8", errors="replace")
    gsm, title = None, {}
    for line in soft.splitlines():
        if line.startswith("^SAMPLE"):
            gsm = line.split("=")[1].strip()
        elif line.startswith("!Sample_title") and gsm:
            title[gsm] = line.split("=", 1)[1].strip()

    tar = tarfile.open(root / "GSE138266_RAW.tar")
    trios = {}
    for m in tar.getmembers():
        g = re.match(r"(GSM\d+)", Path(m.name).name)
        if not g:
            continue
        kind = ("barcodes" if "barcode" in m.name else
                "genes" if ("genes" in m.name or "features" in m.name) else
                "matrix" if "matrix" in m.name else None)
        if kind:
            trios.setdefault(g.group(1), {})[kind] = m

    needed = set(T_MARKERS) | set(CD8_MARKERS) | {g for p in LINEAGE_PANELS.values() for g in p}
    needed |= set(ACTIVATION_PANEL) | module_union | set(PROLIFERATION)
    for genes in programmes.values():
        needed |= set(genes)

    qcs, blocks, metas, gates, order = [], [], [], {}, []
    all_gene_totals = []
    for g, trio in sorted(trios.items()):
        if len(trio) < 3 or g not in title:
            continue
        t = title[g]
        tissue = "CSF" if "CSF" in t.upper() else "PBMCs"
        donor = t.replace("_CSF", "").replace("_PBMCs", "").replace("_PBMC", "").strip()
        counts, qc, kept, n_bc, dims = read_sample(tar, trio, needed)
        unfiltered = n_bc > RAW_BARCODE_LIMIT
        called = (qc["total"].to_numpy() >= RAW_UMI_FLOOR) if unfiltered else np.ones(len(qc), bool)
        lt = np.log1p(qc["total"].to_numpy())
        med = np.median(lt[called])
        mad = stats.median_abs_deviation(lt[called], scale="normal")
        keep = (called & (qc["n_genes"] >= MIN_GENES).to_numpy()
                & (qc["mito_frac"] <= MAX_MITO).to_numpy()
                & (np.abs(lt - med) <= MAD_K * max(mad, 1e-9)))
        gidx_s = {s: i for i, s in enumerate(kept)}
        norm = sp.diags((1e4 / np.maximum(qc["total"].to_numpy(), 1)).astype(np.float32)) @ counts
        norm = norm.tocsr()
        norm.data = np.log1p(norm.data)

        def panel_sum(genes):
            cols = [gidx_s[x] for x in genes if x in gidx_s]
            return np.asarray(norm[:, cols].sum(axis=1)).ravel() if cols else np.zeros(norm.shape[0])

        t_cols = [gidx_s[x] for x in T_MARKERS if x in gidx_s]
        t_pos = np.asarray((counts[:, t_cols] > 0).sum(axis=1)).ravel() >= 2
        t_signal = panel_sum(T_MARKERS)
        cd8_zero = np.asarray(counts[:, [gidx_s[x] for x in CD8_MARKERS
                                         if x in gidx_s]].sum(axis=1)).ravel() == 0
        wins = np.ones(norm.shape[0], dtype=bool)
        for genes in LINEAGE_PANELS.values():
            wins &= t_signal > panel_sum(genes)
        gate = keep & t_pos & cd8_zero & wins
        qcs.append({"gsm": g, "donor": donor, "tissue": tissue,
                    "disease": "MS" if donor.startswith("MS") else "IIH",
                    "n_cd4_lineage": int(gate.sum())})
        if gate.sum() >= MIN_CELLS:
            blocks.append((g, counts[gate], kept))
            all_gene_totals.append(qc["total"].to_numpy()[gate])
            metas.append(pd.DataFrame({"gsm": g, "donor": donor, "tissue": tissue,
                                       "disease": "MS" if donor.startswith("MS") else "IIH"},
                                      index=range(int(gate.sum()))))
            gates[g] = (trio, gate)
            order.append(g)
    pd.DataFrame(qcs).to_csv(out / "sample_qc.csv", index=False, lineterminator="\n")

    common = sorted(set.intersection(*[set(k) for _, _, k in blocks]))
    cidx = {s: i for i, s in enumerate(common)}
    X = sp.vstack([b[:, [{s: i for i, s in enumerate(kept)}[s] for s in common]]
                   for _, b, kept in blocks]).tocsr()
    meta = pd.concat(metas, ignore_index=True)
    assert X.shape[0] == len(meta)

    # v3 erratum: CP10K over the all-gene library size, matching the clustering
    # matrix F below, which already normalised correctly. v2 scored on the loaded
    # gene subset's row sums, so the Kitagawa state means inherited that defect.
    library_size = np.concatenate(all_gene_totals)
    assert library_size.shape[0] == X.shape[0]
    scale = 1e4 / np.maximum(library_size, 1)
    X = (sp.diags(scale.astype(np.float32)) @ X).tocsr()
    X.data = np.log1p(X.data)
    n = X.shape[0]
    mu = np.asarray(X.sum(axis=0)).ravel() / n
    sd = np.sqrt(np.maximum(np.asarray(X.multiply(X).sum(axis=0)).ravel() / n - mu ** 2, 0.0))

    cells = meta.copy()
    mapping = []
    for name, signed in score_sets.items():
        v, k = pooled_z_scores(X, cidx, sd, mu, signed)
        cells[name] = v
        mapping.append({"score": name, "n_defined": len(signed), "n_mapped": k})
    pd.DataFrame(mapping).to_csv(out / "gene_mapping.csv", index=False, lineterminator="\n")

    # the cell set must match Wp-R4 v2 exactly, or the stratification is not
    # attaching to the analysed cells
    prior = pd.read_csv(r4 / "cell_scores.csv.gz", usecols=["gsm", "donor", "tissue"])
    recovery = {"prior_cells": int(len(prior)), "this_run_cells": int(len(cells)),
                "per_unit_identical": bool(
                    prior.groupby(["gsm", "tissue"]).size().sort_index().equals(
                        cells.groupby(["gsm", "tissue"]).size().sort_index()))}
    if not recovery["per_unit_identical"]:
        raise SystemExit(f"cell recovery differs from Wp-R4 v2: {recovery}")

    # --- activation strata, reproduced only as the decomposition basis label ---
    edges = np.quantile(cells["activation_disjoint"], np.linspace(0, 1, N_STRATA + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    cells["stratum"] = pd.cut(cells["activation_disjoint"], bins=edges,
                              labels=[f"act{t+1}" for t in range(N_STRATA)],
                              include_lowest=True).astype(str)

    # --- de novo cell states -------------------------------------------------
    import scanpy as sc_
    import anndata as ad
    sc_.settings.n_jobs = 1

    # Second pass over the deposit for the FULL feature space. v1 of this
    # entrypoint clustered on the scored-gene subset the first pass loads,
    # which is only a few hundred genes and is dominated by programme markers,
    # so its "de novo" states were not independent of the biology and could not
    # see a subset defined by genes nobody had scored. The states must be able
    # to resolve a population such as a CCR5-high Th17-lineage cluster, so the
    # clustering matrix is rebuilt from every gene shared across samples.
    tar2 = tarfile.open(root / "GSE138266_RAW.tar")
    full_blocks, full_syms = [], None
    for g in order:
        trio, gate = gates[g]
        with gzip.open(io.BytesIO(tar2.extractfile(trio["genes"]).read()), "rt") as fh:
            syms = pd.read_csv(fh, sep="\t", header=None)[1].astype(str).str.upper().tolist()
        full_syms = sorted(set(syms)) if full_syms is None else sorted(set(full_syms) & set(syms))
    for g in order:
        trio, gate = gates[g]
        full_blocks.append(read_gated_full(tar2, trio, gate, full_syms))
    tar2.close()
    F = sp.vstack(full_blocks).tocsr()
    assert F.shape[0] == len(cells), (F.shape, len(cells))
    fscale = 1e4 / np.maximum(np.asarray(F.sum(axis=1)).ravel(), 1)
    F = (sp.diags(fscale.astype(np.float32)) @ F).tocsr()
    F.data = np.log1p(F.data)
    drop = module_union | set(ACTIVATION_PANEL)
    keep_genes = [g for g in full_syms if g not in drop]
    kcols = [full_syms.index(g) for g in keep_genes] if len(keep_genes) < 2000 else \
            [i for i, g in enumerate(full_syms) if g not in drop]
    A = ad.AnnData(F[:, kcols].copy())
    A.var_names = keep_genes
    A.obs = cells[["donor", "tissue", "stratum"]].reset_index(drop=True)
    sc_.pp.highly_variable_genes(A, n_top_genes=N_HVG)
    A = A[:, A.var.highly_variable].copy()
    sc_.pp.scale(A, max_value=10)
    sc_.tl.pca(A, n_comps=N_PCS, svd_solver="arpack", random_state=SEED)
    sc_.pp.neighbors(A, n_neighbors=15, random_state=SEED, transformer="sklearn")
    sc_.tl.leiden(A, resolution=LEIDEN_RES, random_state=SEED, key_added="state",
                  flavor="igraph", n_iterations=2, directed=False)
    cells["state"] = A.obs["state"].to_numpy()
    states = sorted(cells["state"].unique(), key=lambda s: int(s))
    cells[["donor", "tissue", "stratum", "state"] + REPORTED].to_csv(
        out / "cell_states.csv.gz", index=False, compression="gzip", lineterminator="\n")

    comp_tbl = (cells.groupby(["state", "tissue"]).size().rename("n_cells").reset_index())
    tot = cells.groupby("tissue").size()
    comp_tbl["fraction_of_tissue"] = [r.n_cells / tot[r.tissue] for r in comp_tbl.itertuples()]
    comp_tbl.to_csv(out / "state_composition.csv", index=False, lineterminator="\n")

    paired = sorted(set(cells[cells.tissue == "CSF"].donor)
                    & set(cells[cells.tissue == "PBMCs"].donor))
    dec_rows = []
    for score in PRIMARY_FAMILY:
        for d in paired:
            sl = cells[cells.donor == d]
            wa = np.array([sl[(sl.tissue == "CSF") & (sl.state == s)].shape[0] for s in states], float)
            wb = np.array([sl[(sl.tissue == "PBMCs") & (sl.state == s)].shape[0] for s in states], float)
            if wa.sum() == 0 or wb.sum() == 0:
                continue
            pooled = np.array([sl[sl.state == s][score].mean() for s in states])
            ma = np.array([sl[(sl.tissue == "CSF") & (sl.state == s)][score].mean() for s in states])
            mb = np.array([sl[(sl.tissue == "PBMCs") & (sl.state == s)][score].mean() for s in states])
            # a state absent from one compartment of a donor contributes no
            # within term there; its pooled mean keeps the composition term defined
            ma = np.where(np.isnan(ma), pooled, ma)
            mb = np.where(np.isnan(mb), pooled, mb)
            ma = np.where(np.isnan(ma), 0.0, ma)
            mb = np.where(np.isnan(mb), 0.0, mb)
            wa, wb = wa / wa.sum(), wb / wb.sum()
            comp, within = kitagawa(wa, ma, wb, mb)
            total = float(np.sum(wa * ma) - np.sum(wb * mb))
            dec_rows.append({"basis": "de_novo_state", "score": score, "donor": d,
                             "total": total, "composition": comp, "within": within,
                             "n_states_used": len(states),
                             "identity_residual": float(total - comp - within)})
    dec = pd.DataFrame(dec_rows)
    dec.to_csv(out / "decomposition.csv", index=False, lineterminator="\n")

    summ = (dec.groupby(["basis", "score"])
            .agg(n_donors=("donor", "size"), total=("total", "median"),
                 composition=("composition", "median"), within=("within", "median"),
                 comp_sign_agree=("composition", lambda v: int(np.sum(np.sign(v) == np.sign(np.median(v))))),
                 within_sign_agree=("within", lambda v: int(np.sum(np.sign(v) == np.sign(np.median(v))))),
                 max_residual=("identity_residual", lambda v: float(np.max(np.abs(v)))))
            .reset_index())
    summ.to_csv(out / "decomposition_summary.csv", index=False, lineterminator="\n")

    results = {
        "schema": "wp_a30_state_decomposition/v3",
        "inputs_verified": verified,
        "unit": "donor, paired; cells are observations within donor",
        "question": ("Does the paired CSF-minus-blood difference in the pro-inflammatory module "
                     "arise from a shift in the mixture of cell states, or from a change within "
                     "states?"),
        "discharges": ("the de novo state basis declared by "
                       "wp_a30_activation_stratified_v2 and recorded there as not executed"),
        "cell_recovery_vs_wp_R4_v2": recovery,
        "n_states": len(states),
        "clustering": (f"Leiden resolution {LEIDEN_RES} on {A.shape[1]} highly variable genes "
                       f"selected from {len(keep_genes)} genes, the full shared feature space minus both modules and "
                       f"the activation panel; {N_PCS} PCs, exact scikit-learn neighbours, "
                       f"seed {SEED}, all thread pools pinned to one worker"),
        "decomposition_summary": summ.to_dict("records"),
        "thresholds": {"seed": SEED, "n_hvg": N_HVG, "n_pcs": N_PCS,
                       "leiden_resolution": LEIDEN_RES},
        "interpretation_limit": (
            "Clusters are a partition of this deposit's cells, not independently validated cell "
            "types, and the decomposition is descriptive: a composition term says the mixture "
            "differs, not why. Ten paired donors with no covariate fields. A state absent from "
            "one compartment of a donor is carried at its pooled mean so the identity stays "
            "exact, which attributes that state's whole contribution to the composition term. "
            "Residency is not addressed here."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
