#!/usr/bin/env python
"""Wp-E: phenotypes carried by deposited metadata fields that the package has not used.

The three deposits declare exactly these biological fields:
  GSE290297 (bulk)        cell type, treatment, divisions
  GSE289733 (single cell)  cell type, glucose, animal
  GSE138266 (human)        donor, tissue, disease

Wp-R1 to Wp-P03 used cell type, treatment, glucose, animal and disease. Two
fields were never used as biological variables: `divisions`, which entered only
as a gate sensitivity, and `tissue`, whose compartment effect was reported but
never tested for specificity. This entrypoint asks what phenotype each carries.

Three analyses, each a biological question rather than a validation check:

  E-B1  Is the inhibitor response division-coupled?
        `divisions` as a biological variable. Compare each drug's effect in
        first-division cells against its effect in the total population, and ask
        whether the solvent-only difference between those populations - what
        distinguishes a just-divided cell from the bulk - predicts where the
        drugs act. A drug acting through division history should show its effect
        concentrated in the gate, and its effect vector aligned with the gate's
        own signature.

  E-B2  Do PGAM and G6PD inhibition converge on one Th17 phenotype?
        `treatment` as a drug-class variable. EGCG (PGAM) and DHEA (G6PD) block
        two branches leaving the same hexose-phosphate pool. If they converge,
        a shared metabolic constraint drives the Th17 state; if they diverge,
        the branch identity matters. Measured as the correlation of their gene
        effect vectors within cell type and gate, the size of the concordant and
        discordant gene sets, and how each drug moves the deposit's own
        pathogenicity gene groups.

  E-B3  Is the CSF-versus-blood T-cell phenotype module-specific?
        `tissue` as a within-donor biological variable. Wp-R4 found the
        pro-inflammatory module, the pathogenicity score and both EGCG
        signatures higher in CSF than in the same donor's blood in 9-10 of 10
        paired donors, and reported that this had not been tested against the
        matched random-set null that defeated the disease contrast. This runs
        that test on the paired contrast.

Units are inherited: library for E-B1 and E-B2 (GSE290297 declares no animal
field), donor for E-B3. Nothing here is animal-level inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261005
N_DRAWS = 1000
SIG_ALPHA, SIG_LFC = 0.05, np.log2(1.5)
PATHWAY_GENES = ["PGAM1", "PHGDH", "PSAT1", "SHMT1", "SHMT2", "MTHFD2", "G6PDX", "TXNIP"]
EFFECTOR_GENES = ["IL17A", "IL17F", "IL23R", "IL22", "CSF2", "GZMB", "IFNG",
                  "FOXP3", "IL10", "CTLA4", "MAF", "IKZF3"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_soft(text: str) -> dict[str, tuple[str, str, str]]:
    import re
    out = {}
    for gsm, body in re.findall(r"\^SAMPLE = (\S+)(.*?)(?=\^SAMPLE|\Z)", text, flags=re.S):
        title = re.search(r"!Sample_title = (.*)", body).group(1).strip()
        d = dict(c.strip().split(": ", 1) for c in
                 re.findall(r"!Sample_characteristics_ch1 = (.*)", body))
        out[title.split("_")[0]] = (d["cell type"], d["treatment"], d["divisions"])
    return out


# ------------------------------------------------------------------ E-B1
def division_phenotype(contrasts: pd.DataFrame, expr: pd.DataFrame,
                       ann: dict, partition: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Does the inhibitor response depend on division history?

    Every quantity compared here is built from DISJOINT library sets. A gate
    signature is Div.1 minus Total within one treatment arm; comparing the
    solvent arm's gate signature with the drug arm's gate signature uses four
    non-overlapping library groups, so the correlation is not inflated by a
    shared term. The interaction (drug gate signature minus solvent gate
    signature) is reported as a distribution and is deliberately NOT correlated
    against either signature, because it contains both by construction.
    """
    cols = list(expr.columns)
    L = np.log2(expr + 1.0)

    def arm_gate_signature(ct: str, treatment: str) -> pd.Series | None:
        a = [c for c in cols if ann[c] == (ct, treatment, "Div.1")]
        b = [c for c in cols if ann[c] == (ct, treatment, "Total")]
        if not a or not b:
            return None
        return L[a].mean(axis=1) - L[b].mean(axis=1)

    sig_rows, summary = [], []
    for ct in ["Th17n", "Th17p"]:
        for drug, solvent in [("EGCG", "DMSO"), ("DHEA", "Methanol")]:
            sv = arm_gate_signature(ct, solvent)
            dv = arm_gate_signature(ct, drug)
            if sv is None or dv is None:
                continue
            shared = sv.index.intersection(dv.index)
            sig_rows.append(pd.DataFrame({
                "cell_type": ct, "drug": drug, "solvent": solvent, "symbol": shared,
                "gate_signature_solvent": sv.reindex(shared).to_numpy(),
                "gate_signature_drug": dv.reindex(shared).to_numpy()}))

            d1 = contrasts[contrasts.contrast == f"{ct}.Div.1.{drug}"].set_index("symbol")
            tt = contrasts[contrasts.contrast == f"{ct}.Total.{drug}"].set_index("symbol")
            g = d1.index.intersection(tt.index).intersection(shared)
            inter = (d1.loc[g, "logFC"] - tt.loc[g, "logFC"]).to_numpy()
            summary.append({
                "cell_type": ct, "drug": drug, "n_genes": int(len(g)),
                # clean: the two gate signatures use four disjoint library groups
                "pearson_gate_signature_solvent_vs_drug":
                    float(np.corrcoef(sv.reindex(g), dv.reindex(g))[0, 1]),
                "spearman_gate_signature_solvent_vs_drug":
                    float(stats.spearmanr(sv.reindex(g), dv.reindex(g)).statistic),
                "sd_gate_signature_solvent": float(np.std(sv.reindex(g))),
                "sd_gate_signature_drug": float(np.std(dv.reindex(g))),
                # clean: the two drug effects use disjoint library groups
                "pearson_drug_effect_div1_vs_total":
                    float(np.corrcoef(d1.loc[g, "logFC"], tt.loc[g, "logFC"])[0, 1]),
                "median_abs_drug_effect_div1": float(d1.loc[g, "logFC"].abs().median()),
                "median_abs_drug_effect_total": float(tt.loc[g, "logFC"].abs().median()),
                "n_significant_div1_only": int(((d1.loc[g, "adj.P.Val"] <= SIG_ALPHA) &
                                                (tt.loc[g, "adj.P.Val"] > SIG_ALPHA)).sum()),
                "n_significant_total_only": int(((tt.loc[g, "adj.P.Val"] <= SIG_ALPHA) &
                                                 (d1.loc[g, "adj.P.Val"] > SIG_ALPHA)).sum()),
                "n_significant_both": int(((d1.loc[g, "adj.P.Val"] <= SIG_ALPHA) &
                                           (tt.loc[g, "adj.P.Val"] <= SIG_ALPHA)).sum()),
                "interaction_sd": float(np.std(inter)),
                "interaction_median_abs": float(np.median(np.abs(inter))),
            })
    # Is a gate signature measurable at all? The two vehicle arms are independent
    # library sets measuring the same thing, so their agreement is the ceiling
    # against which any drug-versus-vehicle disagreement must be read.
    arms = ["DMSO", "Methanol", "EGCG", "DHEA"]
    pair_rows = []
    for ct in ["Th17n", "Th17p"]:
        sigs = {a: arm_gate_signature(ct, a) for a in arms}
        for i, a in enumerate(arms):
            for b in arms[i + 1:]:
                if sigs[a] is None or sigs[b] is None:
                    continue
                g = sigs[a].index.intersection(sigs[b].index)
                kind = ("vehicle_vs_vehicle" if {a, b} == {"DMSO", "Methanol"}
                        else "drug_vs_drug" if {a, b} == {"EGCG", "DHEA"}
                        else "drug_vs_vehicle")
                pair_rows.append({"cell_type": ct, "arm_a": a, "arm_b": b, "comparison": kind,
                                  "n_genes": int(len(g)),
                                  "pearson": float(np.corrcoef(sigs[a].reindex(g), sigs[b].reindex(g))[0, 1]),
                                  "spearman": float(stats.spearmanr(sigs[a].reindex(g), sigs[b].reindex(g)).statistic)})
    gate_pairs = pd.DataFrame(pair_rows)

    gate_sig = pd.concat(sig_rows, ignore_index=True)
    gate_sig["interaction"] = gate_sig.gate_signature_drug - gate_sig.gate_signature_solvent
    gate_sig["group"] = partition.reindex(gate_sig.symbol).to_numpy()
    named = gate_sig[gate_sig.symbol.isin(PATHWAY_GENES + EFFECTOR_GENES)].copy()
    meta = {"summary": summary,
            "arm_pair_agreement": gate_pairs.to_dict("records"),
            "gate_signature_genes": int(gate_sig.symbol.nunique()),
            "shared_term_rule": ("Only quantities built from disjoint library groups are correlated. The solvent and "
                                 "drug gate signatures use four non-overlapping groups; the two gate-specific drug "
                                 "effects likewise. The interaction contains both gate signatures by construction and "
                                 "is therefore reported as a distribution only, never correlated against them."),
            "note": ("Div.1 and Total are different sorted populations of the same cultures and the deposit declares "
                     "no pairing field, so a gate signature is a descriptive mean difference with no test. Total "
                     "plausibly contains the Div.1 cells, which attenuates every gate quantity here.")}
    return gate_sig, named, meta, gate_pairs


# ------------------------------------------------------------------ E-B2
def drug_convergence(contrasts: pd.DataFrame, partition: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame, list]:
    rows, summary = [], []
    for ct in ["Th17n", "Th17p"]:
        for gate in ["Div.1", "Total"]:
            e = contrasts[contrasts.contrast == f"{ct}.{gate}.EGCG"].set_index("symbol")
            h = contrasts[contrasts.contrast == f"{ct}.{gate}.DHEA"].set_index("symbol")
            shared = e.index.intersection(h.index)
            frame = pd.DataFrame({"cell_type": ct, "gate": gate, "symbol": shared,
                                  "logFC_EGCG": e.loc[shared, "logFC"].to_numpy(),
                                  "logFC_DHEA": h.loc[shared, "logFC"].to_numpy(),
                                  "adj_EGCG": e.loc[shared, "adj.P.Val"].to_numpy(),
                                  "adj_DHEA": h.loc[shared, "adj.P.Val"].to_numpy()})
            frame["group"] = partition.reindex(frame.symbol).to_numpy()
            both = ((frame.adj_EGCG <= SIG_ALPHA) & (frame.adj_DHEA <= SIG_ALPHA)
                    & (frame.logFC_EGCG.abs() >= SIG_LFC) & (frame.logFC_DHEA.abs() >= SIG_LFC))
            same = both & (np.sign(frame.logFC_EGCG) == np.sign(frame.logFC_DHEA))
            frame["joint_call"] = np.where(~both, "not_both",
                                           np.where(same, "concordant", "discordant"))
            rows.append(frame)
            grp_meds = {}
            base = float(frame.loc[frame.group == "not_significant", "logFC_EGCG"].median())
            base_h = float(frame.loc[frame.group == "not_significant", "logFC_DHEA"].median())
            for gkey, short in [("Th17p_associated", "Th17p"), ("Th17n_associated", "Th17n")]:
                sel = frame.group == gkey
                grp_meds[f"EGCG_centred_median_{short}_assoc"] = float(frame.loc[sel, "logFC_EGCG"].median() - base)
                grp_meds[f"DHEA_centred_median_{short}_assoc"] = float(frame.loc[sel, "logFC_DHEA"].median() - base_h)
            summary.append({"cell_type": ct, "gate": gate, "n_shared_genes": int(len(frame)),
                            "pearson_EGCG_vs_DHEA": float(np.corrcoef(frame.logFC_EGCG, frame.logFC_DHEA)[0, 1]),
                            "spearman_EGCG_vs_DHEA": float(stats.spearmanr(frame.logFC_EGCG, frame.logFC_DHEA).statistic),
                            "n_concordant": int(same.sum()),
                            "n_discordant": int((both & ~same).sum()),
                            "sign_agreement_all_genes": float((np.sign(frame.logFC_EGCG) == np.sign(frame.logFC_DHEA)).mean()),
                            **grp_meds})
    per_gene = pd.concat(rows, ignore_index=True)
    named = per_gene[per_gene.symbol.isin(PATHWAY_GENES + EFFECTOR_GENES)].copy()
    return per_gene, named, summary


# ------------------------------------------------------------------ E-B3
def tissue_specificity(zmat: pd.DataFrame, donor_scores: pd.DataFrame,
                       gene_sets: dict[str, list[str]]) -> tuple[pd.DataFrame, list]:
    idx = pd.DataFrame([i.split("|") for i in zmat.index], columns=["donor", "tissue"], index=zmat.index)
    paired = sorted(set(idx.loc[idx.tissue == "CSF", "donor"]) & set(idx.loc[idx.tissue == "PBMCs", "donor"]))
    csf = zmat.loc[[f"{d}|CSF" for d in paired]].to_numpy()
    blood = zmat.loc[[f"{d}|PBMCs" for d in paired]].to_numpy()
    delta = csf - blood                                   # donors x genes, CSF minus blood
    genes = list(zmat.columns)
    pos = {g: i for i, g in enumerate(genes)}
    usable = np.where(np.isfinite(delta).all(axis=0))[0]
    rng = np.random.default_rng(SEED)
    rows = []
    for name, members in gene_sets.items():
        cols = [pos[g] for g in members if g in pos and pos[g] in set(usable.tolist())]
        if len(cols) < 5:
            continue
        obs_per_donor = delta[:, cols].mean(axis=1)
        obs = float(np.median(obs_per_donor))
        draws = np.empty(N_DRAWS)
        for b in range(N_DRAWS):
            c = rng.choice(usable, size=len(cols), replace=False)
            draws[b] = float(np.median(delta[:, c].mean(axis=1)))
        w = stats.wilcoxon(obs_per_donor)
        rows.append({"score": name, "n_genes_mapped": len(cols), "n_donors": len(paired),
                     "observed_median_csf_minus_blood": obs,
                     "n_donors_positive": int((obs_per_donor > 0).sum()),
                     "wilcoxon_p": float(w.pvalue),
                     "null_mean": float(draws.mean()), "null_sd": float(draws.std(ddof=1)),
                     "null_q025": float(np.quantile(draws, .025)),
                     "null_q975": float(np.quantile(draws, .975)),
                     "empirical_two_sided_p": float((np.abs(draws - draws.mean()) >= abs(obs - draws.mean())).mean()),
                     "n_draws": N_DRAWS})
    out = pd.DataFrame(rows)
    return out, out.to_dict("records")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--runs-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root, runs, out = Path(args.data_root), Path(args.runs_root), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    src = {
        "tpm": root / "GSE290297_collected_inhibitors_tpm_4geo.csv.gz",
        "bulk_soft": root / "GSE290297_samples.soft.txt",
        "acquisition": root / "acquisition_v1.json",
        "bulk_contrasts": runs / "wp_bulk_contrasts_v1/bulk_contrasts.csv.gz",
        "bulk_partition": runs / "wp_bulk_contrasts_v1/partition_Div1.csv.gz",
        "human_z": runs / "wp_human_signature_transfer_v3/donor_gene_mean_z.csv.gz",
        "human_donor_scores": runs / "wp_human_signature_transfer_v3/donor_scores.csv",
        "human_mapping": runs / "wp_human_signature_transfer_v3/gene_mapping.csv",
        "s1": root / "NIHMS2092659-supplement-2.xlsx",
        "s3": root / "NIHMS2092659-supplement-3.xlsx",
        "s5": root / "NIHMS2092659-supplement-5.xlsx",
    }
    verified = {k: sha256(v) for k, v in src.items()}

    expr = pd.read_csv(src["tpm"], index_col=0)
    ann = parse_soft(open(src["bulk_soft"], encoding="utf-8", errors="replace").read())
    assert set(ann) == set(expr.columns), "library annotation does not match the matrix columns"
    contrasts = pd.read_csv(src["bulk_contrasts"])
    partition = pd.read_csv(src["bulk_partition"]).set_index("symbol")["group"]

    per_gene_div, gate_named, div_meta, gate_pairs = division_phenotype(contrasts, expr, ann, partition)
    gate_pairs.to_csv(out / "division_gate_arm_agreement.csv", index=False, lineterminator="\n")
    per_gene_div.to_csv(out / "division_gate_signatures.csv.gz", index=False,
                        compression="gzip", lineterminator="\n")
    gate_named.to_csv(out / "division_gate_named_genes.csv", index=False, lineterminator="\n")
    pd.DataFrame(div_meta["summary"]).to_csv(out / "division_summary.csv", index=False, lineterminator="\n")

    per_gene_drug, drug_named, drug_summary = drug_convergence(contrasts, partition)
    per_gene_drug.to_csv(out / "drug_convergence_genes.csv.gz", index=False,
                         compression="gzip", lineterminator="\n")
    drug_named.to_csv(out / "drug_named_genes.csv", index=False, lineterminator="\n")
    pd.DataFrame(drug_summary).to_csv(out / "drug_convergence_summary.csv", index=False, lineterminator="\n")

    # gene sets for E-B3, rebuilt exactly as Wp-R4 built them
    s1 = pd.read_excel(src["s1"], sheet_name="Table S1")
    s1.columns = [str(c).strip() for c in s1.columns]
    gcol = [c for c in s1.columns if c.lower() in ("gene", "symbol", "gene_symbol")][0]
    mcol = [c for c in s1.columns if "module" in c.lower() or "program" in c.lower()][0]
    hcol = [c for c in s1.columns if "hvg" in c.lower()][0]
    s1["symbol"] = s1[gcol].astype(str).str.upper()
    s1["is_hvg"] = s1[hcol].astype(str).str.upper().isin(["TRUE", "YES", "1", "1.0"])
    gene_sets: dict[str, list[str]] = {}
    for mod, sub in s1.groupby(mcol):
        key = "proinflammatory" if "inflam" in str(mod).lower() else "proregulatory"
        gene_sets[f"{key}_authors"] = sorted(set(sub.loc[sub.is_hvg, "symbol"]))
        gene_sets[f"{key}_all"] = sorted(set(sub["symbol"]))
    s3 = pd.read_excel(src["s3"], sheet_name="Table S3")
    s3.columns = [str(c).strip() for c in s3.columns]
    sym3 = [c for c in s3.columns if c.lower() in ("gene", "symbol", "gene_symbol")][0]
    grp3 = [c for c in s3.columns if "comparison" in c.lower() or "contrast" in c.lower()
            or "treatment" in c.lower()][0]
    lfc3 = [c for c in s3.columns if "logfc" in c.lower().replace(" ", "")][0]
    adj3 = [c for c in s3.columns if "adj" in c.lower()][0]
    s3["symbol"] = s3[sym3].astype(str).str.upper()
    for g, sub in s3.groupby(grp3):
        if "TH17N" in str(g).upper() and "EGCG" in str(g).upper():
            sel = sub[(sub[adj3] <= 0.05) & (sub[lfc3].abs() >= SIG_LFC)]
            gene_sets["S3_Th17n_EGCG"] = sorted(set(sel["symbol"]))
    s5 = pd.read_excel(src["s5"], sheet_name="Table S5")
    s5.columns = [str(c).strip() for c in s5.columns]
    pcol = [c for c in s5.columns if "program" in c.lower()][0]
    kcol = [c for c in s5.columns if "gene" in c.lower()][0]
    for p, sub in s5.groupby(pcol):
        gene_sets[f"programme_{p}"] = sorted(set(sub[kcol].astype(str).str.upper()))
    gene_sets["activation"] = ["CD69", "JUN", "JUNB", "FOS", "FOSB", "DUSP1", "NR4A1",
                               "TNFAIP3", "ZFP36", "IER2"]
    gene_sets["proliferation"] = ["MKI67", "TOP2A", "PCNA", "TYMS", "CCNB1", "CDK1",
                                  "UBE2C", "BIRC5", "STMN1", "RRM2"]

    zmat = pd.read_csv(src["human_z"], index_col=0)
    donor_scores = pd.read_csv(src["human_donor_scores"])
    tissue, tissue_rows = tissue_specificity(zmat, donor_scores, gene_sets)
    tissue.to_csv(out / "tissue_specificity_null.csv", index=False, lineterminator="\n")

    results = {
        "schema": "wp_e_metadata_phenotypes/v2",
        "inputs_verified": verified,
        "metadata_fields_used": {
            "E-B1": "GSE290297 `divisions` (Div.1 vs Total), as a biological variable",
            "E-B2": "GSE290297 `treatment` (EGCG vs DHEA), as a drug-class variable",
            "E-B3": "GSE138266 `tissue` (CSF vs blood), within donor",
        },
        "unit": {"E-B1": "library; GSE290297 declares no animal field",
                 "E-B2": "library; GSE290297 declares no animal field",
                 "E-B3": "donor, paired across tissue"},
        "division_phenotype": div_meta,
        "drug_convergence": drug_summary,
        "tissue_specificity": tissue_rows,
        "thresholds": {"alpha": SIG_ALPHA, "abs_log2fc": float(SIG_LFC), "n_draws": N_DRAWS, "seed": SEED},
        "interpretation_limit": (
            "E-B1 and E-B2 are library-level descriptive contrasts on deposited TPM with no animal field, so neither "
            "supports animal-level or causal inference. Div.1 and Total are overlapping sorted populations of the "
            "same cultures with no pairing field declared, so the division phenotype is an association between two "
            "gated populations, not a measurement of what a dividing cell does. E-B2 compares two drugs whose "
            "solvents differ, so a shared solvent effect cannot be excluded. E-B3 is donor-level and paired, which "
            "is the strongest unit in the package, but the signatures transported are the mouse study's own and the "
            "cohort was collected for another purpose; a compartment difference is not evidence about disease."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
