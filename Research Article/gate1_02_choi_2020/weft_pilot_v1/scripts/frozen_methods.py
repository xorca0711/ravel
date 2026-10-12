"""Frozen, inert extracts from pinned legacy sources. No historical modules imported.
Generated from exact AST source segments; see config/source-bindings.json.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import scipy.sparse as sp
import anndata as ad
import scanpy as sc

PAPER_FILTER = {"min_genes_exclusive": 500, "max_genes_exclusive": 7000, "min_counts_exclusive": 2000}

FLOOR_FILTER = {"min_counts": 500, "min_genes": 200}

PAPER_SCRUBLET = {"sim_doublet_ratio": 2, "n_neighbors": 30, "expected_doublet_rate": 0.1,
                  "score_cut": 0.7, "cluster_mean_cut": 0.6}

STATE_SETS = {
    "hAT2_canonical": ["Sftpc", "Sftpa1", "Lyz2"],
    "AT2_identity": ["Etv5", "Abca3", "Cebpa"],                 # DOWN in primed AT2
    "AT2_lipid": ["Acly", "Hmgcr", "Hmgcs1"],                   # DOWN in primed AT2
    "pAT2_inflammatory": ["Ptges", "Orm1", "Tmem173", "Ifitm2", "Ifitm3"],
    "cAT2": ["Cdk1", "Mki67", "Cenpa"],
    "DATP": ["Cldn4", "Krt8", "Ndrg1", "Sprr1a", "AW112010"],
    "AT1_canonical": ["Pdpn", "Hopx", "Cav1"],                  # LOW in DATP
    "AT1_early": ["Lmo7", "Pdpn", "Hopx"],
    "AT1_late": ["Aqp5", "Vegfa", "Cav1", "Spock2"],
    "DATP_figure7": ["Cldn4", "AW112010", "Lhfp"],
    "p53": ["Trp53", "Mdm2", "Ccnd1", "Gdf15"],
    "arrest": ["Cdkn1a", "Cdkn2a"],
    "hypoxia": ["Hif1a", "Ndrg1"],
    "hypoxia_without_Ndrg1": ["Hif1a"],
    "ifng_response": ["Ifngr1", "Ly6a", "Irf7", "Cxcl16"],
    "glycolysis": ["Pgk1", "Pkm", "Slc16a3"],
    "responder": ["Il1r1"],
}

CONTAMINANT_SETS = {
    "ciliated": ["Foxj1", "Wnt7b", "Cd24a"],
    "mesenchyme": ["Vcam1", "Acta2", "Des", "Pdgfra", "Col1a1", "Col1a2"],
    "immune": ["Ptprc", "Tyrobp", "Il2rg", "Lck"],
    "endothelium": ["Pecam1", "Cdh5", "Cldn5"],
    "club_or_airway": ["Scgb1a1", "Scgb3a2", "Cyp2f2"],
}

STATE_ORDER = ["hAT2", "cAT2", "pAT2", "DATP", "AT1"]

ANNOTATION_THRESHOLDS = {
    "contaminant_min": 0.5, "sftpc_low": 0.5, "cAT2_min": 0.35, "AT1_min": 0.5,
    "DATP_min": 0.4, "DATP_negative_ratio": 0.5, "sftpc_high": 0.7,
    "pAT2_identity_ratio": 0.7, "pAT2_inflammatory_ratio": 1.5,
    "dispersed_present_fraction": 0.02, "dispersed_markers": 3,
}

RESOLUTIONS = [0.3, 0.5, 1.0]

def detection(adata, genes, mask=None):
    """Fraction of cells detecting each gene, from the counts layer."""
    X = adata.layers["counts"] if "counts" in adata.layers else adata.X
    present = [g for g in genes if g in adata.var_names]
    if mask is not None:
        X = X[mask]
    if not present:
        return pd.Series(dtype=float)
    sub = X[:, [adata.var_names.get_loc(g) for g in present]]
    return pd.Series(np.asarray((sub > 0).mean(axis=0)).ravel(), index=present)

def cluster_detection_table(adata, cluster_key):
    """Per-cluster mean detection of every set in STATE_SETS and CONTAMINANT_SETS."""
    rows = []
    for cl in sorted(adata.obs[cluster_key].astype(str).unique(), key=lambda s: int(s) if s.isdigit() else s):
        mask = (adata.obs[cluster_key].astype(str) == cl).to_numpy()
        row = {"cluster": cl, "n_cells": int(mask.sum())}
        sftpc = detection(adata, ["Sftpc"], mask)
        row["Sftpc"] = float(sftpc.get("Sftpc", np.nan))
        for name, genes in {**STATE_SETS, **CONTAMINANT_SETS}.items():
            d = detection(adata, genes, mask)
            row[name] = float(d.mean()) if len(d) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def annotate_clusters(table: pd.DataFrame) -> pd.DataFrame:
    """Apply the frozen rule to a cluster detection table. Returns the table
    with 'state' and 'rule' columns; nothing is fitted."""
    T = ANNOTATION_THRESHOLDS
    table = table.copy()
    state, rule = {}, {}
    for _, r in table.iterrows():
        cl = r["cluster"]
        cont = {k: r[k] for k in CONTAMINANT_SETS if r[k] >= T["contaminant_min"]}
        if cont and r["Sftpc"] < T["sftpc_low"]:
            state[cl], rule[cl] = "contaminant_" + max(cont, key=cont.get), "1"
        elif r["cAT2"] >= T["cAT2_min"]:
            state[cl], rule[cl] = "cAT2", "2"
        elif r["AT1_canonical"] >= T["AT1_min"] and r["Sftpc"] < T["sftpc_low"]:
            state[cl], rule[cl] = "AT1", "3"
    at1 = [cl for cl, s in state.items() if s == "AT1"]
    at1_ref = float(table.set_index("cluster").loc[at1, "AT1_canonical"].mean()) if at1 else np.nan
    for _, r in table.iterrows():
        cl = r["cluster"]
        if cl in state:
            continue
        neg = (r["AT1_canonical"] < T["DATP_negative_ratio"] * at1_ref) if at1 else (r["AT1_canonical"] < T["AT1_min"])
        if r["DATP"] >= T["DATP_min"] and neg:
            state[cl], rule[cl] = "DATP", "4"
    sftpc_high = [r for _, r in table.iterrows() if r["cluster"] not in state and r["Sftpc"] >= T["sftpc_high"]]
    if sftpc_high:
        ref = max(sftpc_high, key=lambda r: r["AT2_identity"])
        ref_id, ref_inf = ref["AT2_identity"], ref["pAT2_inflammatory"]
        state[ref["cluster"]], rule[ref["cluster"]] = "hAT2", "5 (reference)"
        for r in sftpc_high:
            cl = r["cluster"]
            if cl in state:
                continue
            if r["AT2_identity"] <= T["pAT2_identity_ratio"] * ref_id and \
               r["pAT2_inflammatory"] >= T["pAT2_inflammatory_ratio"] * max(ref_inf, 1e-9):
                state[cl], rule[cl] = "pAT2", "6"
            else:
                state[cl], rule[cl] = "hAT2", "7"
    for _, r in table.iterrows():
        state.setdefault(r["cluster"], "unassigned")
        rule.setdefault(r["cluster"], "8")
    table["state"] = table["cluster"].map(state)
    table["rule"] = table["cluster"].map(rule)
    table["AT1_reference_detection"] = at1_ref
    return table

def annotate_clusters_b(table: pd.DataFrame) -> pd.DataFrame:
    """The corrected pass (trial D2b), thresholds unchanged.

    D2's first pass showed that in a lineage-sorted library every cluster
    detects Sftpc (ambient surfactant transcript plus the sort), so the
    rule's "Sftpc below 0.5" clauses for AT1 and for contaminants never fire
    and an AT1 cluster is called hAT2 while ciliated and immune clusters stay
    in. This pass keeps every threshold and adds one condition on the
    condition: the Sftpc clauses are applied only where Sftpc separates
    clusters, meaning at least one cluster falls below the low bound. Where
    no cluster does, Sftpc is uninformative and the clauses are dropped. The
    first pass's outcome stays in the record beside this one.
    """
    T = ANNOTATION_THRESHOLDS
    informative = bool((table["Sftpc"] < T["sftpc_low"]).any())
    if informative:
        out = annotate_clusters(table)
        out["sftpc_informative"] = True
        return out
    # Sftpc is uninformative here: the clauses are dropped by evaluating the
    # same rules on the same table with the Sftpc conditions removed.
    t2 = table.copy()
    state, rule = {}, {}
    for _, r in t2.iterrows():
        cl = r["cluster"]
        cont = {k: r[k] for k in CONTAMINANT_SETS if r[k] >= T["contaminant_min"]}
        if cont:
            state[cl], rule[cl] = "contaminant_" + max(cont, key=cont.get), "1b"
        elif r["cAT2"] >= T["cAT2_min"]:
            state[cl], rule[cl] = "cAT2", "2"
        elif r["AT1_canonical"] >= T["AT1_min"]:
            state[cl], rule[cl] = "AT1", "3b"
    at1 = [cl for cl, s in state.items() if s == "AT1"]
    at1_ref = float(t2.set_index("cluster").loc[at1, "AT1_canonical"].mean()) if at1 else np.nan
    for _, r in t2.iterrows():
        cl = r["cluster"]
        if cl in state:
            continue
        neg = (r["AT1_canonical"] < T["DATP_negative_ratio"] * at1_ref) if at1 else (r["AT1_canonical"] < T["AT1_min"])
        if r["DATP"] >= T["DATP_min"] and neg:
            state[cl], rule[cl] = "DATP", "4"
    rest = [r for _, r in t2.iterrows() if r["cluster"] not in state]
    if rest:
        ref = max(rest, key=lambda r: r["AT2_identity"])
        ref_id, ref_inf = ref["AT2_identity"], ref["pAT2_inflammatory"]
        state[ref["cluster"]], rule[ref["cluster"]] = "hAT2", "5 (reference)"
        for r in rest:
            cl = r["cluster"]
            if cl in state:
                continue
            if r["AT2_identity"] <= T["pAT2_identity_ratio"] * ref_id and \
               r["pAT2_inflammatory"] >= T["pAT2_inflammatory_ratio"] * max(ref_inf, 1e-9):
                state[cl], rule[cl] = "pAT2", "6"
            else:
                state[cl], rule[cl] = "hAT2", "7"
    out = table.copy()
    out["state"] = out["cluster"].map(state).fillna("unassigned")
    out["rule"] = out["cluster"].map(rule).fillna("8")
    out["AT1_reference_detection"] = at1_ref
    out["sftpc_informative"] = False
    return out

def dispersed_presence(adata, genes, min_markers=3, mask=None):
    """Fraction of (masked) cells carrying at least min_markers of the set."""
    X = adata.layers["counts"] if "counts" in adata.layers else adata.X
    present = [g for g in genes if g in adata.var_names]
    if mask is not None:
        X = X[mask]
    sub = X[:, [adata.var_names.get_loc(g) for g in present]]
    k = np.asarray((sub > 0).sum(axis=1)).ravel()
    return float((k >= min_markers).mean()), int((k >= min_markers).sum())

def mad_bounds(x: np.ndarray, nmads: float) -> tuple[float, float]:
    """Median absolute deviation bounds, the repository's QC rule (mirrors
    analysis/scripts/pipeline_utils.mad_bounds without importing across folders)."""
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med))) * 1.4826
    return med - nmads * mad, med + nmads * mad

def same_library_enrichment(adata, key="library", n_neighbors=30):
    """Mean over cells of (same-library neighbours / expected under mixing)."""
    conn = adata.obsp["connectivities"].tocsr()
    lib = adata.obs[key].astype(str).to_numpy()
    frac = pd.Series(lib).value_counts(normalize=True)
    vals = []
    for i in range(conn.shape[0]):
        nb = conn.indices[conn.indptr[i]:conn.indptr[i + 1]]
        if len(nb) == 0:
            continue
        same = float((lib[nb] == lib[i]).mean())
        vals.append(same / frac[lib[i]])
    return float(np.mean(vals))

RULES = {
    "question": "How many cells does each library carry under the paper's own filter, what is their quality, and which are doublets",
    "calling": PAPER_FILTER,
    "calling_note": "the paper's post-Cell-Ranger filter applied to every raw barcode; Cell Ranger 2.0.2's caller is not reproduced",
    "sensitivity_floor": FLOOR_FILTER,
    "qc": {"nmads_counts_genes": 5, "nmads_mt": 3, "mt_cap_percent": 20,
           "note": "per library; a bound that removes nothing is reported as not binding"},
    "doublets": {"method": "scanpy scrublet per capture, seed 0",
                 "expected_rate": "0.008 per 1,000 called cells (10x table)",
                 "threshold": "automatic; fallback to the top expected-rate fraction if undefined, logged",
                 "paper_settings_recorded_not_used": PAPER_SCRUBLET},
    "unit": "the library; each in vivo library pools two mice (STAR Methods)",
    "paper_reported_counts": {
        "tomato_positive_captured_before_contaminant_removal": 12514,
        "tomato_positive_in_figure_1B": 12086,
        "contaminants_removed_by_paper": {"ciliated": 214, "mesenchyme": 16, "immune": 25},
        "non_lineage_labelled_captured": 14017,
        "non_lineage_labelled_doublet_cluster_removed": 1125,
        "organoid_epithelial_control": 1286,
        "organoid_epithelial_il1b": 2584,
    },
}

def call_and_qc(X: sp.csr_matrix, var: pd.DataFrame, barcodes: np.ndarray, meta: dict,
                rec: RunRecord) -> tuple[ad.AnnData, dict]:
    counts = np.asarray(X.sum(axis=1)).ravel()
    genes = X.getnnz(axis=1)
    paper = (genes > PAPER_FILTER["min_genes_exclusive"]) & (genes < PAPER_FILTER["max_genes_exclusive"]) \
        & (counts > PAPER_FILTER["min_counts_exclusive"])
    floor = (counts >= FLOOR_FILTER["min_counts"]) & (genes >= FLOOR_FILTER["min_genes"])
    row = {**meta, "n_barcodes": int(X.shape[0]),
           "paper_rule_cells": int(paper.sum()), "floor_rule_cells": int(floor.sum()),
           "floor_only_barcodes": int((floor & ~paper).sum()), "paper_only_barcodes": int((paper & ~floor).sum())}

    Xc = X[paper]
    obs = qc_metrics(Xc, var, "mouse")
    obs.index = pd.Index(barcodes[paper], name="barcode")
    keep = np.ones(len(obs), dtype=bool)
    bounds = {}
    for col in ("total_counts", "n_genes"):
        lo, hi = mad_bounds(np.log1p(obs[col].to_numpy()), RULES["qc"]["nmads_counts_genes"])
        m = (np.log1p(obs[col]) >= lo) & (np.log1p(obs[col]) <= hi)
        bounds[col] = {"low": float(np.expm1(lo)), "high": float(np.expm1(hi)),
                       "removed_low": int((np.log1p(obs[col]) < lo).sum()),
                       "removed_high": int((np.log1p(obs[col]) > hi).sum())}
        keep &= m.to_numpy()
    mt = obs["pct_mt"].to_numpy()
    _, hi_mt = mad_bounds(mt, RULES["qc"]["nmads_mt"])
    hi_mt = min(hi_mt, RULES["qc"]["mt_cap_percent"])
    bounds["pct_mt"] = {"high": float(hi_mt), "removed_high": int((mt > hi_mt).sum())}
    keep &= mt <= hi_mt
    row["mad_removed"] = int((~keep).sum())
    row["binding_bounds"] = ";".join(k + ":" + ",".join(s for s, v in b.items() if s.startswith("removed") and v > 0)
                                     for k, b in bounds.items() if any(s.startswith("removed") and v > 0 for s, v in b.items())) or "none"
    Xq = Xc[keep]
    obs = obs[keep].copy()
    adata = ad.AnnData(X=Xq.astype(np.float32), obs=obs,
                       var=var.set_index(var["gene_symbol"].where(~var["gene_symbol"].duplicated(), var["gene_id"])))
    adata.var_names_make_unique()
    adata.var.index.name = "feature"   # the index is the symbol, or the ID where a symbol is duplicated
    adata.layers["counts"] = adata.X.copy()
    for k, v in meta.items():
        adata.obs[k] = v

    n = adata.n_obs
    expected = 0.008 * n / 1000
    sc.pp.scrublet(adata, random_state=0, verbose=False, expected_doublet_rate=expected)
    thr = float(adata.uns.get("scrublet", {}).get("threshold", np.nan))
    method = "scrublet automatic threshold"
    if not np.isfinite(thr):
        cut = np.quantile(adata.obs["doublet_score"], 1 - expected)
        adata.obs["predicted_doublet"] = adata.obs["doublet_score"] >= cut
        thr = float(cut)
        method = f"fallback: top {100 * expected:.2f}% of scores"
    adata.obs["predicted_doublet"] = adata.obs["predicted_doublet"].astype(bool)
    row.update({"cells_after_qc": int(n), "scrublet_expected_rate": float(expected),
                "scrublet_threshold": thr, "scrublet_method": method,
                "doublets_flagged": int(adata.obs["predicted_doublet"].sum()),
                "cells_final": int((~adata.obs["predicted_doublet"]).sum()),
                "median_counts": float(np.median(adata.obs["total_counts"])),
                "median_genes": float(np.median(adata.obs["n_genes"])),
                "median_pct_mt": float(np.median(adata.obs["pct_mt"])),
                "paper_scrublet_score_gt_0.7": int((adata.obs["doublet_score"] > 0.7).sum())})
    rec.set(f"bounds_{meta['library']}", bounds)
    return adata, row

def embed(adata: ad.AnnData) -> None:
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, flavor="seurat_v3", n_top_genes=2000, layer="counts")
    emb = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.scale(emb, max_value=10)
    sc.tl.pca(emb, n_comps=30, random_state=0)
    adata.obsm["X_pca"] = emb.obsm["X_pca"]
    sc.pp.neighbors(adata, n_neighbors=30, n_pcs=30, use_rep="X_pca", random_state=0)
    for r in RESOLUTIONS:
        sc.tl.leiden(adata, resolution=r, key_added=f"leiden_{r}", flavor="igraph", n_iterations=2, random_state=0)
    sc.tl.umap(adata, random_state=0)

def qc_metrics(X: sp.csr_matrix, var: pd.DataFrame, species: str) -> pd.DataFrame:
    """Per-cell QC metrics. No cell is filtered here; Gate 0 only measures."""
    symbols = var["gene_symbol"].astype(str)
    if species == "mouse":
        mt = symbols.str.startswith("mt-")
        ribo = symbols.str.startswith(("Rps", "Rpl")) & ~symbols.str.contains("-ps", case=False)
        hb = symbols.str.startswith(("Hba", "Hbb"))
    else:
        mt = symbols.str.startswith("MT-")
        ribo = symbols.str.startswith(("RPS", "RPL")) & ~symbols.str.contains("-ps", case=False)
        hb = symbols.str.startswith(("HBA", "HBB"))

    total = np.asarray(X.sum(axis=1)).ravel()
    with np.errstate(invalid="ignore", divide="ignore"):
        out = pd.DataFrame({
            "total_counts": total,
            "n_genes": X.getnnz(axis=1),
            "pct_mt": 100 * np.asarray(X[:, mt.to_numpy()].sum(axis=1)).ravel() / np.maximum(total, 1),
            "pct_ribo": 100 * np.asarray(X[:, ribo.to_numpy()].sum(axis=1)).ravel() / np.maximum(total, 1),
            "pct_hb": 100 * np.asarray(X[:, hb.to_numpy()].sum(axis=1)).ravel() / np.maximum(total, 1),
        })
    return out
