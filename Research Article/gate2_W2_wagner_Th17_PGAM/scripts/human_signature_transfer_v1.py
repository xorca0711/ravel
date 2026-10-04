#!/usr/bin/env python
"""Wp-R4: transfer the mouse PGAM-related signatures onto human CSF and blood T cells.

Donor-level descriptive analysis of GSE138266 (Schafflick et al. 2020): 12 donors,
6 multiple sclerosis and 6 idiopathic intracranial hypertension, CSF for all 12 and
blood for 10. The donor is the unit. Signature definitions are exposed (they come
from the mouse study), so this is signature transport, not independent validation.

Frozen design:
  1. Donor and tissue come from the deposited file names; disease class comes from
     the donor-code prefix (MS versus PST/PTC), which Wp-R0 recovered from the GEO
     sample titles. Nothing else about the donors is deposited.
  2. Per-sample QC: at least 200 detected genes, mitochondrial fraction at most
     10 per cent, log10 UMI within 3 median absolute deviations of the sample
     median. The floor is low because CSF libraries are shallow; the per-sample
     gene-count distribution is reported so the floor's effect is auditable.
  3. Cell identity is gated on counts with a declared rule, not clustered: a cell
     is a CD4-lineage (non-CD8) T cell if at least two of CD3D/CD3E/CD3G/TRAC/TRBC2
     are detected, CD8A and CD8B are both zero, and the summed log-normalised
     T-marker signal exceeds the summed signal of each competing lineage panel
     (B, myeloid, NK, erythroid/platelet). Lineage panels are compared rather than
     required to be zero: ambient RNA makes LYZ and HBB near-ubiquitous in blood
     libraries, so a hard-zero rule removes most genuine T cells. CD4 itself is
     not required: its dropout rate would make the gate depth-dependent. The label
     is therefore "CD4-lineage T cell", not "CD4+ T cell".
  3b. One deposited CSF sample (PST83775) is an unfiltered barcode matrix with
     737,280 barcodes and a median of zero detected genes, unlike the other 21.
     Any sample with more than 100,000 barcodes is treated as unfiltered and gets
     a 500-UMI cell-calling floor before the shared QC; this is recorded per
     sample in the output.
  4. A donor-tissue unit needs at least 20 gated cells; units below that are
     excluded and listed.
  5. Scores use the mouse study's method - per-gene z-scaling across all retained
     cells of all samples, multiplied by the gene sign, then averaged - with the
     z-scaling done once on the pooled set so that between-donor differences are
     preserved. Pooling is required: z-scaling within a sample would set every
     donor mean to zero by construction.
  6. Mouse-to-human mapping is exact symbol identity on upper case. Mapped and
     unmapped counts are reported per gene set; no ortholog database is used, so
     one-to-many and renamed orthologs are lost and this is a stated limit.
  6b. The paper's Figure S4 also claims the N1, P1 and P4 programmes are higher in
     MS blood, so the Table S5 programme marker sets are scored here as well.
  7. Activation and proliferation scores are fixed gene sets declared here, and
     the disease contrast is reported both unadjusted and with the activation
     score as a covariate, because CSF T cells are more activated than blood
     T cells and activation is the rival explanation for any score difference.
"""
from __future__ import annotations

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

T_MARKERS = ["CD3D", "CD3E", "CD3G", "TRAC", "TRBC2"]
CD8_MARKERS = ["CD8A", "CD8B"]
LINEAGE_PANELS = {"B": ["MS4A1", "CD79A", "CD79B"],
                  "myeloid": ["LYZ", "CD14", "FCN1", "AIF1"],
                  "NK": ["GNLY", "NKG7", "KLRD1"],
                  "ery_plt": ["HBB", "HBA1", "PPBP"]}
EXCLUDE = CD8_MARKERS + [g for p in LINEAGE_PANELS.values() for g in p]
RAW_BARCODE_LIMIT = 100_000
RAW_UMI_FLOOR = 500
ACTIVATION = ["CD69", "JUN", "JUNB", "FOS", "FOSB", "DUSP1", "NR4A1", "TNFAIP3", "ZFP36", "IER2"]
PROLIFERATION = ["MKI67", "TOP2A", "PCNA", "TYMS", "CCNB1", "CDK1", "UBE2C", "BIRC5", "STMN1", "RRM2"]
MIN_GENES = 200
MAX_MITO = 0.10
MAD_K = 3.0
MIN_CELLS = 20


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sample(tar: tarfile.TarFile, trio: dict, needed: set[str]):
    """One pass over a CellRanger v2 trio; returns QC vectors and a sparse cells x needed matrix."""
    with gzip.open(io.BytesIO(tar.extractfile(trio["genes"]).read()), "rt") as fh:
        genes = pd.read_csv(fh, sep="\t", header=None)
    symbols = genes[1].astype(str).str.upper().to_numpy()
    n_barcodes = sum(1 for _ in gzip.open(io.BytesIO(tar.extractfile(trio["barcodes"]).read()), "rt"))

    want = {}
    for i, s in enumerate(symbols):
        if s in needed and s not in want:
            want[s] = i
    mito = np.array([i for i, s in enumerate(symbols) if s.startswith("MT-")], dtype=np.int64)
    is_mito = np.zeros(len(symbols), dtype=bool)
    is_mito[mito] = True
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
                ri.append(ci_)
                ci.append(j)
                vv.append(val)
    counts = sp.csr_matrix((np.array(vv, dtype=np.float32), (np.array(ri), np.array(ci))),
                           shape=(n_cells, len(kept_symbols)))
    qc = pd.DataFrame({"total": total, "n_genes": ngene,
                       "mito_frac": np.divide(mtot, np.maximum(total, 1))})
    return counts, qc, kept_symbols, n_barcodes, (n_genes, n_cells, nnz)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--r3-run", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, out = Path(args.data_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    verified = {f: sha256(root / f) for f in
                ["GSE138266_RAW.tar", "GSE138266_samples.soft.txt", "acquisition_v1.json",
                 "acquisition_v3_matrices.json", "NIHMS2092659-supplement-2.xlsx",
                 "NIHMS2092659-supplement-3.xlsx", "NIHMS2092659-supplement-5.xlsx"]}
    verified["wp_bulk_contrasts_v1/signatures.csv"] = sha256(Path(args.r3_run) / "signatures.csv")

    # --- gene sets ----------------------------------------------------------
    s1 = pd.read_excel(root / "NIHMS2092659-supplement-2.xlsx", sheet_name="Table S1")
    s1.columns = [str(c).strip() for c in s1.columns]
    gene_col = [c for c in s1.columns if c.lower() in ("gene", "symbol", "gene_symbol")][0]
    mod_col = [c for c in s1.columns if "module" in c.lower() or "program" in c.lower()][0]
    hvg_col = [c for c in s1.columns if "hvg" in c.lower()][0]
    s1["symbol"] = s1[gene_col].astype(str).str.upper()
    s1["is_hvg"] = s1[hvg_col].astype(str).str.upper().isin(["TRUE", "YES", "1", "1.0"])
    modules = {}
    for mod, sub in s1.groupby(mod_col):
        key = "proinflammatory" if "inflam" in str(mod).lower() else "proregulatory"
        modules[key] = {"authors": sorted(set(sub.loc[sub.is_hvg, "symbol"])),
                        "all": sorted(set(sub["symbol"]))}

    s3 = pd.read_excel(root / "NIHMS2092659-supplement-3.xlsx", sheet_name="Table S3")
    s3.columns = [str(c).strip() for c in s3.columns]
    sym3 = [c for c in s3.columns if c.lower() in ("gene", "symbol", "gene_symbol")][0]
    grp3 = [c for c in s3.columns if "comparison" in c.lower() or "contrast" in c.lower()
            or "treatment" in c.lower()][0]
    lfc3 = [c for c in s3.columns if "logfc" in c.lower().replace(" ", "")][0]
    adj3 = [c for c in s3.columns if "adj" in c.lower()][0]
    s3["symbol"] = s3[sym3].astype(str).str.upper()
    sig_sets = {}
    for g, sub in s3.groupby(grp3):
        if "TH17N" not in str(g).upper() or "EGCG" not in str(g).upper():
            continue
        sel = sub[(sub[adj3] <= 0.05) & (sub[lfc3].abs() >= np.log2(1.5))]
        sig_sets["S3_Th17n_EGCG"] = dict(zip(sel["symbol"], np.sign(sel[lfc3])))
    r3 = pd.read_csv(Path(args.r3_run) / "signatures.csv")
    sub = r3[r3["signature"] == "Th17n.Div.1.EGCG"]
    sig_sets["R3_Th17n_Div1_EGCG"] = dict(zip(sub["symbol"].str.upper(), np.sign(sub["logFC"])))

    s5 = pd.read_excel(root / "NIHMS2092659-supplement-5.xlsx", sheet_name="Table S5")
    s5.columns = [str(c).strip() for c in s5.columns]
    prog_col = [c for c in s5.columns if "program" in c.lower()][0]
    mark_col = [c for c in s5.columns if "gene" in c.lower()][0]
    programmes = {str(p): sorted(set(sub[mark_col].astype(str).str.upper()))
                  for p, sub in s5.groupby(prog_col)}

    score_sets = {"proinflammatory_authors": {g: 1.0 for g in modules["proinflammatory"]["authors"]},
                  "proinflammatory_all": {g: 1.0 for g in modules["proinflammatory"]["all"]},
                  "proregulatory_authors": {g: 1.0 for g in modules["proregulatory"]["authors"]},
                  "proregulatory_all": {g: 1.0 for g in modules["proregulatory"]["all"]},
                  "activation": {g: 1.0 for g in ACTIVATION},
                  "proliferation": {g: 1.0 for g in PROLIFERATION}}
    for k, v in sig_sets.items():
        score_sets[k] = {g: float(s) for g, s in v.items()}
    for p, genes in programmes.items():
        score_sets[f"programme_{p}"] = {g: 1.0 for g in genes}

    needed = set(T_MARKERS) | set(EXCLUDE)
    for v in score_sets.values():
        needed |= set(v)

    # --- per-sample pass ----------------------------------------------------
    tar = tarfile.open(root / "GSE138266_RAW.tar")
    trios: dict[tuple[str, str, str], dict] = {}
    for m in tar.getnames():
        gsm, rest = m.split("_", 1)
        parts = rest.split("_")
        donor, tissue = parts[0], parts[1]
        kind = ("barcodes" if "barcodes" in m else "genes" if "genes" in m else "matrix")
        trios.setdefault((gsm, donor, tissue), {})[kind] = m

    blocks, metas, qcs = [], [], []
    common: list[str] | None = None
    for (gsm, donor, tissue), trio in sorted(trios.items(), key=lambda kv: kv[0][1:]):
        counts, qc, kept, n_bc, dims = read_sample(tar, trio, needed)
        if common is None:
            common = kept
        if kept != common:
            keep_idx = [kept.index(g) for g in common if g in kept]
            counts = counts[:, keep_idx]
            kept = [g for g in common if g in kept]
        unfiltered = n_bc > RAW_BARCODE_LIMIT
        called = (qc["total"].to_numpy() >= RAW_UMI_FLOOR) if unfiltered else np.ones(len(qc), dtype=bool)
        lt = np.log10(np.maximum(qc["total"].to_numpy(), 1))
        med = np.median(lt[called])
        mad = stats.median_abs_deviation(lt[called], scale="normal")
        keep = (called & (qc["n_genes"] >= MIN_GENES).to_numpy() & (qc["mito_frac"] <= MAX_MITO).to_numpy()
                & (np.abs(lt - med) <= MAD_K * max(mad, 1e-9)))
        gidx = {g: i for i, g in enumerate(kept)}

        # lineage comparison on log-normalised values, not hard-zero exclusion
        norm = sp.diags((1e4 / np.maximum(qc["total"].to_numpy(), 1)).astype(np.float32)) @ counts
        norm = norm.tocsr()
        norm.data = np.log1p(norm.data)

        def panel_sum(genes):
            cols = [gidx[g] for g in genes if g in gidx]
            return np.asarray(norm[:, cols].sum(axis=1)).ravel() if cols else np.zeros(norm.shape[0])

        t_cols = [gidx[g] for g in T_MARKERS if g in gidx]
        t_pos = np.asarray((counts[:, t_cols] > 0).sum(axis=1)).ravel() >= 2
        t_signal = panel_sum(T_MARKERS)
        cd8_zero = np.asarray(counts[:, [gidx[g] for g in CD8_MARKERS if g in gidx]].sum(axis=1)).ravel() == 0
        wins = np.ones(norm.shape[0], dtype=bool)
        for genes in LINEAGE_PANELS.values():
            wins &= t_signal > panel_sum(genes)
        gate = keep & t_pos & cd8_zero & wins
        qcs.append({"gsm": gsm, "donor": donor, "tissue": tissue,
                    "disease": "MS" if donor.startswith("MS") else "IIH",
                    "n_barcodes_file": n_bc, "n_cells_matrix": dims[1], "n_genes_matrix": dims[0],
                    "deposited_unfiltered": bool(unfiltered), "n_cells_called": int(called.sum()),
                    "median_genes": float(np.median(qc["n_genes"])),
                    "median_umi": float(np.median(qc["total"])),
                    "median_mito_frac": float(np.median(qc["mito_frac"])),
                    "n_pass_qc": int(keep.sum()), "n_t_positive": int((keep & t_pos).sum()),
                    "n_cd4_lineage": int(gate.sum())})
        if gate.sum() >= MIN_CELLS:
            blocks.append(counts[gate])
            metas.append(pd.DataFrame({"gsm": gsm, "donor": donor, "tissue": tissue,
                                       "disease": "MS" if donor.startswith("MS") else "IIH"},
                                      index=range(int(gate.sum()))))
    tar.close()
    qc_df = pd.DataFrame(qcs)
    qc_df.to_csv(out / "sample_qc.csv", index=False, lineterminator="\n")

    X = sp.vstack(blocks).tocsr()
    meta = pd.concat(metas, ignore_index=True)
    assert X.shape[0] == len(meta)
    gidx = {g: i for i, g in enumerate(common)}

    # CP10K + log1p on the needed columns only; the pooled z-scaling that follows
    # is linear, so scores are computed without densifying the matrix.
    scale = 1e4 / np.maximum(np.asarray(X.sum(axis=1)).ravel(), 1)
    X = sp.diags(scale.astype(np.float32)) @ X
    X.data = np.log1p(X.data)
    X = X.tocsr()

    n = X.shape[0]
    mu = np.asarray(X.sum(axis=0)).ravel() / n
    sq = np.asarray(X.multiply(X).sum(axis=0)).ravel() / n
    sd = np.sqrt(np.maximum(sq - mu ** 2, 0.0))

    mapping_rows, scores = [], {}
    for name, signed in score_sets.items():
        use = [(gidx[g], s) for g, s in signed.items() if g in gidx and sd[gidx[g]] > 0]
        mapping_rows.append({"score": name, "n_genes_defined": len(signed),
                             "n_genes_mapped": len(use),
                             "unmapped": ";".join(sorted(g for g in signed if g not in gidx))[:2000]})
        if not use:
            scores[name] = np.full(n, np.nan)
            continue
        w = np.zeros(X.shape[1], dtype=np.float64)
        for j, s in use:
            w[j] = s / (sd[j] * len(use))
        scores[name] = np.asarray(X @ w).ravel() - float((w * mu).sum())
    pd.DataFrame(mapping_rows).to_csv(out / "gene_mapping.csv", index=False, lineterminator="\n")

    cells = meta.copy()
    for k, v in scores.items():
        cells[k] = v
    cells["pathogenicity_authors"] = cells["proinflammatory_authors"] - cells["proregulatory_authors"]
    cells["pathogenicity_all"] = cells["proinflammatory_all"] - cells["proregulatory_all"]
    cells.to_csv(out / "cell_scores.csv.gz", index=False, compression="gzip", lineterminator="\n")

    score_cols = [c for c in cells.columns if c not in ("gsm", "donor", "tissue", "disease")]
    donor = cells.groupby(["donor", "tissue", "disease"])[score_cols].mean().reset_index()
    donor["n_cells"] = cells.groupby(["donor", "tissue", "disease"]).size().to_numpy()
    donor.to_csv(out / "donor_scores.csv", index=False, lineterminator="\n")

    # --- disease contrasts within tissue -----------------------------------
    rows = []
    for tissue, sub in donor.groupby("tissue"):
        ms = sub[sub.disease == "MS"]
        ii = sub[sub.disease == "IIH"]
        for c in score_cols:
            u = stats.mannwhitneyu(ms[c], ii[c], alternative="two-sided")
            A = np.column_stack([np.ones(len(sub)), (sub.disease == "MS").astype(float),
                                 sub["activation"].to_numpy()])
            coef, *_ = np.linalg.lstsq(A, sub[c].to_numpy(), rcond=None)
            resid = sub[c].to_numpy() - A @ coef
            dfr = len(sub) - A.shape[1]
            s2 = (resid ** 2).sum() / dfr
            se = np.sqrt(s2 * np.linalg.inv(A.T @ A)[1, 1])
            rows.append({"tissue": tissue, "score": c, "n_MS": len(ms), "n_IIH": len(ii),
                         "median_MS": float(ms[c].median()), "median_IIH": float(ii[c].median()),
                         "median_difference": float(ms[c].median() - ii[c].median()),
                         "mannwhitney_p": float(u.pvalue),
                         "disease_coef_adj_activation": float(coef[1]),
                         "disease_t_adj_activation": float(coef[1] / se) if se > 0 else np.nan,
                         "disease_p_adj_activation": float(2 * stats.t.sf(abs(coef[1] / se), dfr)) if se > 0 else np.nan,
                         "residual_df": int(dfr)})
    dc = pd.DataFrame(rows)
    dc["mannwhitney_bh"] = np.nan
    for tissue, sub in dc.groupby("tissue"):
        p = sub["mannwhitney_p"].to_numpy()
        order = np.argsort(p)
        q = np.empty_like(p)
        q[order] = np.minimum.accumulate((p[order] * len(p) / (np.arange(len(p)) + 1))[::-1])[::-1]
        dc.loc[sub.index, "mannwhitney_bh"] = np.minimum(q, 1.0)
    dc.to_csv(out / "disease_contrasts.csv", index=False, lineterminator="\n")

    # --- paired CSF minus blood within donor -------------------------------
    wide = donor.pivot_table(index=["donor", "disease"], columns="tissue", values=score_cols)
    paired_rows = []
    tissues = sorted(donor.tissue.unique())
    if len(tissues) == 2:
        t1, t2 = tissues
        for c in score_cols:
            d = (wide[(c, t1)] - wide[(c, t2)]).dropna()
            if len(d) < 3:
                continue
            w = stats.wilcoxon(d.to_numpy())
            dis = np.array([idx[1] for idx in d.index])
            u = stats.mannwhitneyu(d.to_numpy()[dis == "MS"], d.to_numpy()[dis == "IIH"],
                                   alternative="two-sided") if (dis == "MS").sum() >= 2 and (dis == "IIH").sum() >= 2 else None
            paired_rows.append({"score": c, "contrast": f"{t1}_minus_{t2}", "n_donors": int(len(d)),
                                "median_difference": float(np.median(d)),
                                "n_positive": int((d > 0).sum()),
                                "wilcoxon_p": float(w.pvalue),
                                "difference_median_MS": float(np.median(d.to_numpy()[dis == "MS"])),
                                "difference_median_IIH": float(np.median(d.to_numpy()[dis == "IIH"])),
                                "disease_difference_p": float(u.pvalue) if u is not None else np.nan})
    pd.DataFrame(paired_rows).to_csv(out / "paired_tissue.csv", index=False, lineterminator="\n")

    results = {
        "schema": "wp_r4_human_transfer/v1",
        "inputs_verified": verified,
        "unit": "donor (12; 6 MS and 6 IIH), with tissue nested within donor for the 10 paired donors",
        "n_cells_retained": int(n),
        "n_units": int(len(donor)),
        "units_excluded_below_min_cells": qc_df.loc[qc_df.n_cd4_lineage < MIN_CELLS,
                                                    ["donor", "tissue", "n_cd4_lineage"]].to_dict("records"),
        "qc": {"min_genes": MIN_GENES, "max_mito_frac": MAX_MITO, "mad_k": MAD_K, "min_cells": MIN_CELLS,
               "raw_barcode_limit": RAW_BARCODE_LIMIT, "raw_umi_floor": RAW_UMI_FLOOR},
        "gate": {"t_markers": T_MARKERS, "cd8_markers": CD8_MARKERS, "lineage_panels": LINEAGE_PANELS,
                 "label": "CD4-lineage (non-CD8) T cell; CD4 transcript not required"},
        "gene_mapping": {r["score"]: [r["n_genes_defined"], r["n_genes_mapped"]] for r in mapping_rows},
        "cells_per_unit": donor[["donor", "tissue", "disease", "n_cells"]].to_dict("records"),
        "interpretation_limit": ("Donor-level descriptive transport of exposed mouse-derived signatures into a human "
            "dataset collected for a different purpose. Six donors per group; disease groups differ in more than "
            "disease. Mouse-to-human mapping is symbol identity only. Supports a statement about whether the "
            "signature separates these donors, not about mechanism in human disease."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
