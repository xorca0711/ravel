# Grounding: published finding to repository output to proposed question

Compiled 5 October 2026. Every value quoted on a candidate card traces to a
committed table of a governed run with a verified receipt. Reanalysis of the
source's own deposits and citation of the source paper are **one evidence
lineage**, not independent replication; no candidate may describe any value
below as external support.

## The source

Wang, Wagner, Fessler et al. 2025, *Cell Reports* 44:115799,
[doi:10.1016/j.celrep.2025.115799](https://doi.org/10.1016/j.celrep.2025.115799)
(PMID 40482033, PMC12443480, author manuscript NIHMS2092659). Deposits:
GSE289733 (single cell, 19,203 barcodes × 31,053 genes, 8 libraries, 2 animals),
GSE290297 (bulk, 79 TPM libraries, 20,465 genes, no animal field),
GSE138266 (reused human, 22 samples, 12 donors; Schafflick et al. 2020).
Qualification of all three: [DATASETS.md](../DATASETS.md),
[R0_RESULTS.md](../R0_RESULTS.md), receipt `wp_source_qualification_v1`.

## Wp-Q1 — arm asymmetry

| Element | Content |
|---|---|
| Published finding | Low glucose raises the Th17 pathogenicity score; PGAM restrains pathogenicity (main text and Fig. 3). |
| Repository output | Score rises at 1 mM in 4/4 animal-paired comparisons **through the pro-regulatory arm**: `wp_singlecell_reproduction_v1/glucose_paired_differences.csv` and `library_score_means.csv`. Arms anti-correlated across 15,830 cells, Spearman −0.389 to −0.503: `wp_score_construction_v1/arm_independence.csv`. Pro-inflammatory arm alone sign-inconsistent: `glucose_direction_by_variant.csv`. Composition carries the effect, within-state term sign-inconsistent: `wp_glucose_decomposition_v1/decomposition.csv`. Human paired contrast moves the opposite arm: `wp_metadata_phenotypes_v1/tissue_specificity_null.csv`. |
| Unresolved contrast | Two one-sided arm moves in opposite arms, under a nutrient perturbation in mouse culture and a compartment contrast in human disease. The deposited RNA cannot distinguish separately regulated competences from one latent axis, because both arms are computed from the same transcriptome. |
| Exposure | **Fully exposed.** Every value above was read and reported before the question was written. Wp-P01 and Wp-P03 were themselves outcome-exposed branch cards; Wp-P03's stop rule fired. |
| Reports | [R1](../R1_RESULTS.md), [P01](../P01_RESULTS.md), [P03](../P03_RESULTS.md), [METADATA_PHENOTYPES](../METADATA_PHENOTYPES_RESULTS.md) |

## Wp-Q2 — biosynthetic demand against stress

| Element | Content |
|---|---|
| Published finding | The Discussion proposes that PGAM inhibition raises pathogenicity via cellular stress, citing a 2-DG study and a PGAM1 cancer study for the stress-TGF-β link. |
| Repository output | Under EGCG in Th17n, against an expression-decile-matched null: Th17 effector +0.544 (p 0.000), ISR −0.491 (0.000), histones −0.465, serine/one-carbon −0.299, cell cycle −0.260, ribosomal proteins −0.205; UPR +0.063 (0.121), NRF2 −0.069 (0.419), heat shock +0.025 (0.372) — `wp_e3_global_shift_v1/programme_shift.csv`. Overlap discharged: `wp_e3_isr_sensitivity_v1/isr_serine_sensitivity.csv` and `member_gene_logfc.csv`. Every serine and one-carbon transcript falls under both drugs: `wp_bulk_contrasts_v1/bulk_contrasts.csv.gz`. PGAM reaction rho −0.291, rank 11/83, fails BH: `wp_compass_sensitivity_v1_rerun/reaction_correlations.csv`. Division gate restructured rather than removed: `wp_metadata_phenotypes_v1/division_gate_arm_agreement.csv`. |
| Published premises checked | Brucklacher-Waldert et al. 2017, *Cell Reports* 19:2357, [doi:10.1016/j.celrep.2017.05.052](https://doi.org/10.1016/j.celrep.2017.05.052) (PMID 28614720) — **full text read**; reports that cellular stress substitutes for TGF-β, with sustained cytoplasmic calcium and partial XBP1, and that 2-DG and 3-bromopyruvate enhance Th17 polarisation. Huang et al. 2019, *Cell Metabolism* 30:1107, [doi:10.1016/j.cmet.2019.09.014](https://doi.org/10.1016/j.cmet.2019.09.014) (PMID 31607564) — **paywalled, abstract only**; HKB99 acts through PGAM1-ACTA2 with JNK/c-Jun, AKT and ERK changes in lung cancer, and TGF-β does not appear in the abstract. This remains a flag, not a refutation. |
| Unresolved contrast | The effector gain co-occurs with falling biosynthetic and proliferative programmes and with reduced ATF4 output, in the one arm where effector rises. Co-occurrence in five libraries per arm is not a mechanism, and no transcript measures stress-response activity. |
| Exposure | **Fully exposed** for the Wp-E3 values. The sensitivity run's reduced-set values were **unexposed** when its contract and stop rule were frozen, which the contract records; the full-set values it recomputes were exposed. |
| Added 5 October 2026 after the literature search | Ishikawa and colleagues 2023, *Cell Reports* 42:112205, [doi:10.1016/j.celrep.2023.112205](https://doi.org/10.1016/j.celrep.2023.112205) (PMID 36857180) — **full text read**; PEP inhibits the Th17 programme by binding JunB and blocking JunB/BATF/IRF4 DNA binding, without changing glycolysis or proliferation. PGAM sits two steps upstream of PEP, so this predicts the source's phenotype directly. The source's own Fig. 1E ¹³C tracing reports PEP unchanged under EGCG, which constrains it; a 15-minute label ratio is not a pool size. The source cites this paper as reference 7, in the Introduction's opening citation bundle only; its Discussion does not return to it. Wp-Q2 was reframed from two-way to three-way, with the prior framing preserved. |
| Reports | [E3](../E3_RESULTS.md), [R3](../R3_RESULTS.md), [R2](../R2_RESULTS.md), [P02 branch card](../branches/P02_serine_one_carbon_direction.md), [LITERATURE_UPDATE.md](LITERATURE_UPDATE.md) |

## Wp-Q3 — CSF compartment against activation

| Element | Content |
|---|---|
| Published finding | Transported Th17 modules are reported higher in MS in the reused human cohort (Fig. 4 and S5 of the source). |
| Repository output | The disease contrast does not reproduce: nothing in CSF reaches BH ≤ 0.05, smallest is programme N3 at BH 0.147 — `wp_human_signature_transfer_v2/disease_contrasts.csv`. In blood the modules separate the cohorts but matched random sets separate them as well (p 0.29) and the activation set separates them in the opposite direction — `random_set_null.csv`. The surviving contrast is paired within donor: pro-inflammatory +0.061, 10/10 donors, empirical p 0.003; pro-regulatory +0.007, p 0.394, and +0.022, p 0.931 on all mapped genes; activation +0.109, p 0.013 — `wp_metadata_phenotypes_v1/tissue_specificity_null.csv` and `wp_human_signature_transfer_v2/paired_tissue.csv`. |
| Deposit limits carried into the question | One CSF library deposited unfiltered at 737,280 barcodes, handled with a 500-UMI floor; a hard-zero lineage gate left 1 to 124 cells in four blood libraries; no age, sex, treatment or disease-duration field exists — `wp_human_signature_transfer_v2/sample_qc.csv`, [R0](../R0_RESULTS.md), [R4](../R4_RESULTS.md). |
| Unresolved contrast | A paired donor-level contrast on ten donors cannot separate a compartment-specific effector programme from activation, and the activation set is a measured competitor rather than a hypothetical one. |
| Exposure | **Fully exposed.** The paired contrast was proposed in Wp-R4 as untested and then executed in Wp-M3; the question was written after both. |
| Reports | [METADATA_PHENOTYPES](../METADATA_PHENOTYPES_RESULTS.md), [R4](../R4_RESULTS.md), [R0](../R0_RESULTS.md) |

## Contribution descriptions

Per [the literature workflow](../../../docs/LITERATURE_WORKFLOW.md), stated as
descriptions and not as a ranking:

- **Wp-Q1** — model discrimination between a one-axis and a two-competence
  reading of an established score.
- **Wp-Q2** — model discrimination among three published or published-adjacent
  mechanisms (stress substituting for TGF-β, PEP release from JunB inhibition,
  demand competition), none of them proposed here as new.
- **Wp-Q3** — measurement validation and a boundary extension of a published
  transfer that did not reproduce as published.

None of the three is described as novel, and no absence of a search hit is
treated as novelty. Published Th17 plasticity, glycolytic control of Th17
differentiation and CSF T-cell compartmentalisation remain **premises**.

## What is not available

No independent Th17 nutrient dataset qualified: [Wp-E5](../E5_RESULTS.md)
screened 114 series, failed 64 on record-level rules and deferred 50 to record
inspection with none admissible, so the Wp-R1 glucose basis remains two mice.
Author-held per-animal EAE data is unobtainable (the owner ruled out author
contact), which keeps Wp-P04 blocked. The published scVI-imputed Compass input
was never deposited, which is why Wp-R2 is a declared version-and-input
sensitivity rather than a reproduction.
