#!/usr/bin/env python
"""A30 (v2): does the CSF pro-inflammatory elevation survive activation adjustment?

Supersedes a30_activation_stratified_v1.py, whose executed run is preserved at
analysis/research/runs/wp_a30_activation_stratified_v1. Two defects were found
there before any value was reported: the Table S5 parse assigned instead of
accumulating, so each programme score used a single gene; and the runner's
interpreter lacked scanpy, so the declared de novo state decomposition did not
execute. The design, the activation panel, the strata, the floor, the primary
family and the stop rule are unchanged.

Wp-M3 found that in ten paired donors the pro-inflammatory module is higher in
CSF than in that donor's own blood (+0.061, 10/10 donors, empirical p 0.003
against a matched random-set null) while the pro-regulatory arm does not move
(p 0.394 on the authors' HVG set, 0.931 on all mapped genes). The declared
activation set moves in the same direction (+0.109, p 0.013), so that
unstratified contrast cannot separate a compartment-imposed effector state from
cells simply being more activated in an inflamed compartment.

This entrypoint runs the stratified re-test the A30 development plan fixed.

Frozen design, fixed before any stratified value was computed:

  1. ACTIVATION PANEL. 21 genes, verified disjoint from the union of both
     module gene lists, so stratifying on activation does not stratify on the
     endpoint. CD40LG was removed from the candidate panel as a module member;
     the panel Wp-R4 used is not reused because it contains ZFP36, which is a
     pro-regulatory module gene. Disjointness is asserted at run time, not
     assumed. Exclusion was deliberately NOT extended to the Table S3
     differential-expression universe: S3 is not this analysis's endpoint and
     covers 11,364 genes, so excluding it would leave no usable panel.
  2. STRATA. Three tertiles of the activation score, cut on GLOBAL quantiles
     across all cells, so a low-activation CSF cell is compared against a
     low-activation blood cell rather than against its own compartment's
     distribution.
  3. FLOOR. A unit contributes to a stratum only with at least 50 cells there,
     and a donor contributes to a stratum only when both of its units clear the
     floor. Units and donors lost at the floor are reported per stratum.
  4. ENDPOINT. Per stratum, the paired CSF-minus-blood difference of
     donor-level mean score, tested by Wilcoxon signed-rank and against 1,000
     matched-size random gene sets scored identically. Both module arms are
     reported in every stratum whichever way the primary falls, with the
     activation score itself as a positive control that the stratification
     worked and programme N3 because Wp-M3 found it moving.
  5. MULTIPLICITY. The declared family is 2 module arms x 3 strata = 6 tests,
     BH-adjusted within that family. Activation, programme N3 and the
     proliferation control are reported outside the family as context.
  6. DECOMPOSITION. The total paired difference is split by the symmetric
     Kitagawa identity into a composition term and a within-state term, twice:
     over activation strata, which asks how much of the elevation is simply
     more activated cells in CSF; and over cell states clustered de novo from
     genes outside both modules and outside the activation panel, which is the
     composition rival a CSF-enriched Th17-lineage subset would produce.

Stop rule, fixed here: report every stratum and both arms including null
results. Do not drop a stratum, change the floor, change the number of strata
or change the clustering resolution after seeing a value. A failure to separate
the hypotheses is reported as precision-limited, never as evidence of absence.

Unit: donor, paired. Ten donors contribute both compartments; cells are
observations within donor. Residency is not addressed by any output here.
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
N_DRAWS = 10000
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

    # v3 erratum: CP10K is taken over the all-gene library size carried from the
    # first pass. v1 and v2 divided by the row sum of the LOADED gene subset, so a
    # score depended on what else was scored in the same run; see the erratum note.
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

    # --- strata -------------------------------------------------------------
    edges = np.quantile(cells["activation_disjoint"], np.linspace(0, 1, N_STRATA + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    cells["stratum"] = pd.cut(cells["activation_disjoint"], bins=edges,
                              labels=[f"act{t+1}" for t in range(N_STRATA)],
                              include_lowest=True).astype(str)
    cells.to_csv(out / "cell_strata.csv.gz", index=False, compression="gzip",
                 lineterminator="\n")

    unit = (cells.groupby(["donor", "tissue", "stratum"]).size()
            .rename("n_cells").reset_index())
    unit["clears_floor"] = unit.n_cells >= STRATUM_FLOOR
    unit.to_csv(out / "stratum_support.csv", index=False, lineterminator="\n")

    # --- donor-level means and the paired contrast --------------------------
    rng = np.random.default_rng(SEED)
    pool = np.array([g for g in common if sd[cidx[g]] > 0])
    pool_cols = np.array([cidx[g] for g in pool])
    dm = (cells.groupby(["donor", "tissue", "stratum"])[REPORTED].mean().reset_index())
    dm = dm.merge(unit, on=["donor", "tissue", "stratum"])
    strata_all = sorted(cells["stratum"].unique())
    size_of = {m["score"]: int(m["n_mapped"]) for m in mapping}

    # Which donors a stratum supports, fixed by the declared floor before any
    # null is drawn, so the null is evaluated on exactly the observed design.
    support = {}
    for stratum in strata_all:
        sub = dm[(dm.stratum == stratum) & dm.clears_floor]
        wide = sub.pivot(index="donor", columns="tissue", values=REPORTED)
        have = [t for t in ("CSF", "PBMCs")]
        donors = [d for d in wide.index
                  if all((score, t) in wide.columns and not pd.isna(wide.loc[d, (score, t)])
                         for score in REPORTED for t in have)]
        support[stratum] = (sorted(donors), wide)

    # Null draws are shared across strata and across scores of equal mapped
    # size: the draw depends only on the gene-set size, not on which stratum it
    # is later aggregated over, so each size is drawn once.
    cell_donor = cells["donor"].to_numpy()
    cell_tissue = cells["tissue"].to_numpy()
    cell_stratum = cells["stratum"].to_numpy()
    index = {}
    for stratum in strata_all:
        smask = cell_stratum == stratum
        kept_donors, _ = support[stratum]
        index[stratum] = [(np.flatnonzero(smask & (cell_donor == d) & (cell_tissue == "CSF")),
                           np.flatnonzero(smask & (cell_donor == d) & (cell_tissue == "PBMCs")))
                          for d in kept_donors]
    # Each draw is aggregated to its per-stratum paired median immediately, so
    # only the aggregates are held rather than 1,000 cell-length vectors.
    null_diff: dict[int, dict[str, np.ndarray]] = {}
    for k in sorted({size_of[s] for s in REPORTED}):
        acc = {s: np.empty(N_DRAWS) for s in strata_all}
        for i in range(N_DRAWS):
            cols = rng.choice(pool_cols, size=k, replace=False)
            sub = np.asarray(X[:, cols].todense())
            v = ((sub - mu[cols]) / sd[cols]).mean(axis=1)
            for stratum in strata_all:
                acc[stratum][i] = np.median([v[ia].mean() - v[ib].mean()
                                             for ia, ib in index[stratum]])
        null_diff[k] = acc

    rows, per_donor = [], []
    for stratum in strata_all:
        kept_donors, wide = support[stratum]
        for score in REPORTED:
            a = wide.loc[kept_donors, (score, "CSF")].to_numpy()
            b = wide.loc[kept_donors, (score, "PBMCs")].to_numpy()
            diff = a - b
            obs = float(np.median(diff))
            w = (stats.wilcoxon(diff).pvalue if len(diff) >= 5 and np.any(diff != 0)
                 else float("nan"))
            k = size_of[score]
            draws = null_diff[k][stratum]
            emp = float((np.abs(draws - draws.mean()) >= abs(obs - draws.mean())).mean())
            rows.append({"stratum": stratum, "score": score, "n_genes_mapped": k,
                         "n_donors": len(kept_donors), "n_donors_positive": int((diff > 0).sum()),
                         "median_difference": obs, "wilcoxon_p": w,
                         "null_mean": float(draws.mean()),
                         "null_q025": float(np.quantile(draws, .025)),
                         "null_q975": float(np.quantile(draws, .975)),
                         "empirical_two_sided_p": emp,
                         "in_primary_family": score in PRIMARY_FAMILY})
            for d, v in zip(kept_donors, diff):
                per_donor.append({"stratum": stratum, "score": score, "donor": d,
                                  "csf_minus_blood": float(v)})
    null_rows = [{"size": k, "stratum": s, "null_mean": float(v.mean()),
                  "null_sd": float(v.std())}
                 for k, acc in null_diff.items() for s, v in acc.items()]
    contrasts = pd.DataFrame(rows)
    fam = contrasts.in_primary_family
    p = contrasts.loc[fam, "empirical_two_sided_p"].to_numpy()
    o = np.argsort(p); m_ = len(p)
    bh = np.empty(m_); run = 1.0
    for rank in range(m_ - 1, -1, -1):
        run = min(run, p[o[rank]] * m_ / (rank + 1)); bh[o[rank]] = run
    contrasts.loc[fam, "bh_within_family"] = bh
    contrasts.to_csv(out / "stratified_contrasts.csv", index=False, lineterminator="\n")
    pd.DataFrame(per_donor).to_csv(out / "per_donor_differences.csv", index=False,
                                   lineterminator="\n")
    pd.DataFrame(null_rows).to_csv(out / "null_draw_sample.csv", index=False,
                                   lineterminator="\n")

    # --- decomposition over activation strata --------------------------------
    paired = sorted(set(cells[cells.tissue == "CSF"].donor) & set(cells[cells.tissue == "PBMCs"].donor))
    strata = sorted(cells["stratum"].unique())
    dec_rows = []
    for score in PRIMARY_FAMILY + ["proinflammatory_all", "proregulatory_all"]:
        for d in paired:
            sl = cells[cells.donor == d]
            wa = np.array([ (sl[(sl.tissue=="CSF") & (sl.stratum==s)].shape[0]) for s in strata], float)
            wb = np.array([ (sl[(sl.tissue=="PBMCs") & (sl.stratum==s)].shape[0]) for s in strata], float)
            if wa.sum() == 0 or wb.sum() == 0:
                continue
            ma = np.array([sl[(sl.tissue=="CSF") & (sl.stratum==s)][score].mean() for s in strata])
            mb = np.array([sl[(sl.tissue=="PBMCs") & (sl.stratum==s)][score].mean() for s in strata])
            ok = ~(np.isnan(ma) | np.isnan(mb))
            wa, wb = wa / wa.sum(), wb / wb.sum()
            ma = np.where(np.isnan(ma), 0.0, ma); mb = np.where(np.isnan(mb), 0.0, mb)
            comp, within = kitagawa(wa, ma, wb, mb)
            total = float(np.sum(wa * ma) - np.sum(wb * mb))
            dec_rows.append({"basis": "activation_stratum", "score": score, "donor": d,
                             "total": total, "composition": comp, "within": within,
                             "n_states_used": int(ok.sum()),
                             "identity_residual": float(total - comp - within)})

    # --- decomposition over de novo cell states ------------------------------
    cluster_note = ""
    try:
        import scanpy as sc_  # noqa
        import anndata as ad
        keep_genes = [g for g in common
                      if g not in module_union and g not in set(ACTIVATION_PANEL)]
        kcols = [cidx[g] for g in keep_genes]
        A = ad.AnnData(X[:, kcols].copy())
        A.var_names = keep_genes
        A.obs = cells[["donor", "tissue", "stratum"]].reset_index(drop=True)
        sc_.pp.highly_variable_genes(A, n_top_genes=N_HVG)
        A = A[:, A.var.highly_variable].copy()
        sc_.pp.scale(A, max_value=10)
        sc_.tl.pca(A, n_comps=N_PCS, svd_solver="arpack", random_state=SEED)
        sc_.pp.neighbors(A, n_neighbors=15, random_state=SEED)
        sc_.tl.leiden(A, resolution=LEIDEN_RES, random_state=SEED, key_added="state",
                      flavor="igraph", n_iterations=2, directed=False)
        cells["state"] = A.obs["state"].to_numpy()
        cluster_note = (f"de novo Leiden on {A.shape[1]} HVGs selected from "
                        f"{len(keep_genes)} genes outside both modules and the activation "
                        f"panel; resolution {LEIDEN_RES}, seed {SEED}")
    except Exception as exc:  # recorded, never silently skipped
        cells["state"] = "unavailable"
        cluster_note = f"de novo clustering unavailable: {type(exc).__name__}: {exc}"

    if cells["state"].nunique() > 1:
        states = sorted(cells["state"].unique())
        for score in PRIMARY_FAMILY:
            for d in paired:
                sl = cells[cells.donor == d]
                wa = np.array([sl[(sl.tissue=="CSF") & (sl.state==s)].shape[0] for s in states], float)
                wb = np.array([sl[(sl.tissue=="PBMCs") & (sl.state==s)].shape[0] for s in states], float)
                if wa.sum() == 0 or wb.sum() == 0:
                    continue
                ma = np.array([sl[(sl.tissue=="CSF") & (sl.state==s)][score].mean() for s in states])
                mb = np.array([sl[(sl.tissue=="PBMCs") & (sl.state==s)][score].mean() for s in states])
                pooled = np.array([sl[sl.state==s][score].mean() for s in states])
                ma = np.where(np.isnan(ma), pooled, ma); mb = np.where(np.isnan(mb), pooled, mb)
                ma = np.where(np.isnan(ma), 0.0, ma); mb = np.where(np.isnan(mb), 0.0, mb)
                wa, wb = wa / wa.sum(), wb / wb.sum()
                comp, within = kitagawa(wa, ma, wb, mb)
                total = float(np.sum(wa * ma) - np.sum(wb * mb))
                dec_rows.append({"basis": "de_novo_state", "score": score, "donor": d,
                                 "total": total, "composition": comp, "within": within,
                                 "n_states_used": len(states),
                                 "identity_residual": float(total - comp - within)})
        (cells.groupby(["state", "tissue"]).size().rename("n_cells").reset_index()
         .to_csv(out / "state_composition.csv", index=False, lineterminator="\n"))
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

    primary = contrasts[contrasts.in_primary_family]
    results = {
        "schema": "wp_a30_activation_stratified/v3",
        "inputs_verified": verified,
        "unit": "donor, paired; cells are observations within donor",
        "question": ("Does the paired CSF-minus-blood elevation of the pro-inflammatory module "
                     "survive stratification on an activation score built from genes disjoint "
                     "from both modules?"),
        "cp10k_denominator": "all_gene_library_size_from_first_pass",
        "supersedes": "wp_a30_activation_stratified_v2 (loaded-gene-subset denominator, 1,000 draws)",
        "activation_panel": ACTIVATION_PANEL,
        "activation_panel_disjoint_from_modules": True,
        "module_union_size": len(module_union),
        "cell_recovery_vs_wp_R4_v2": recovery,
        "strata": {"n": N_STRATA, "basis": "global tertiles of the disjoint activation score",
                   "floor_cells_per_unit": STRATUM_FLOOR},
        "primary_family": PRIMARY_FAMILY,
        "primary_results": primary[["stratum", "score", "n_donors", "n_donors_positive",
                                    "median_difference", "wilcoxon_p",
                                    "empirical_two_sided_p", "bh_within_family"]].to_dict("records"),
        "context_results": contrasts[~contrasts.in_primary_family][
            ["stratum", "score", "n_donors", "median_difference",
             "empirical_two_sided_p"]].to_dict("records"),
        "decomposition_summary": summ.to_dict("records"),
        "clustering": cluster_note,
        "thresholds": {"n_draws": N_DRAWS, "seed": SEED, "n_hvg": N_HVG, "n_pcs": N_PCS,
                       "leiden_resolution": LEIDEN_RES},
        "interpretation_limit": (
            "Ten paired donors with no age, sex, treatment or disease-duration field, so no "
            "covariate adjustment is possible and a null is precision-limited rather than "
            "evidence of absence. Module scores are RNA, not protein, secretion or regulatory "
            "function. Stratifying on activation addresses the activation rival only; residency "
            "and recirculation are not addressed by any output here, because that needs "
            "shared-clone comparison across compartments which this deposit cannot supply. "
            "Reanalysis of this deposit shares one evidence lineage with the source paper and "
            "with Schafflick et al. 2020 and is never independent replication."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n",
                                      encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
