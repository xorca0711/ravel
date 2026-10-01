# Retrospective RQ review: Niethamer 2025

Reviewed 2026-10-01 against the saved analysis sequence and the RQ register on
`origin/main` at `f61343cc16c83e979b071393adccdcf8084ea294`. This is an evidence
review, not a rerun or a claim-grade decision. Later computation on the same
animals is a sensitivity analysis, not independent replication.

## Analysis sequence and its consequences

| Date / order | Saved evidence | Consequence for framing |
|---|---|---|
| August 2026, Stage 0 | [Atlas and coverage](GSE262927/README.md); [stage-by-stage record](ANALYSIS_TRIAL_PLAN.md#stage-0-initial-run-can-the-published-biology-be-recovered-from-raw-counts) | Blind annotation and injury-associated composition provide context. RNA ordering does not measure fate, and persistent state fractions do not establish persistence of individual cells. |
| 2026-09-10, N1–N4 | [Phase](GSE262927/phase_timecourse/README.md), [myeloid composition](GSE262927/myeloid_focus/README.md), [trace-window origin](GSE262927/myeloid_focus/amac_origin/README.md), [batch sensitivity](GSE262927/myeloid_focus/batch_sensitivity/README.md) | The trace peak agrees for four of five lineages; myeloid composition turns over; the early trace window contributes strongly to the late aMAC pool. Marrow-reference and within-aMAC-origin tests fail coverage gates. Reporter history and present cycling RNA remain separate measurements. |
| 2026-09-21, G0 → G1/G1b and G2 | [Feasibility](trials/g0_gsea_feasibility/g0_summary.md), [G1](trials/g1_gsea_by_phase/g1_summary.md), [post hoc gate correction G1b](trials/g1b_corrected_positive_control/g1b_summary.md), [G2](trials/g2_gsea_ipf/g2_summary.md) | Historical DNA-replication and cross-cohort enrichment readings must be interpreted through the later correction below. The changed G1 positive control was not an independent validation. |
| 2026-09-22, W1 | [Summary](trials/w1_amac_pseudobulk_de/w1_summary.md), [animal units](trials/w1_amac_pseudobulk_de/w1_units.csv), [set results](trials/w1_amac_pseudobulk_de/w1_sets.csv) | Four late-active, eight resolution and three long-term eligible animals yield descriptive gene differences, but no registered set clears. Age and processing compete with injury history; the seven-gene ornithine set is ineligible. W1 reuses G1 animals. |
| 2026-09-22, statistical correction | [Current interpretation](../../analysis/corrections/statistics/README.md), [run record](../../analysis/corrections/statistics/run_record.json), [G2 comparison table](../../analysis/corrections/statistics/tables/g2_corrected_replication.csv), [validation subtype coverage](../../analysis/corrections/statistics/tables/GSE135893_subtype_eligibility.csv) | Covariate-adjusted G1 DNA-replication sets do not pass. G2 has zero replicated sets under estimated correlation and 30 under fixed 0.01; this is method sensitivity, not validated mechanism or evidence of absence. W1 remains without significant sets. Subtype coverage prevents a replicated within-state explanation. |
| 2026-09-29, later main-only presentation revision | [Immutable revision note](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/Research%20Article/gate1_01_niethamer_2025/GSE262927/figure_revision_20260929/README.md) | Categorical spacing, cross-sectional animals and shared-RNA annotation comparisons are clarified. Saved values were replayed; this adds no biological evidence. |

## Strict contribution decisions

| Existing RQ | Candidate contribution | Decision and discriminator |
|---|---|---|
| **A3, injury history versus aging** | A late injury-associated macrophage programme might persist beyond normal aging. | **Already incorporated; no duplicate branch.** The current card explicitly requires age-matched uninjured animals and separates state fractions, within-state programmes and tracing. The correction narrows the premise: no established persistent DNA-replication or arginine/ornithine mechanism. Aging, replacement and processing remain rivals; a matched animal-level injury-history contrast is the discriminator. |
| **A6, within-state IPF change versus mixture** | IPF might alter macrophage programmes beyond abundance changes. | **Already incorporated; no duplicate branch.** Harmonized state definitions and adequate donors are required before composition-standardized pseudobulk comparisons. The fixed-correlation result cannot replace the failed primary result; nonsignificance cannot establish a mixture-only mechanism. |
| **A4, sequential Wnt/IL-1 responsiveness** | The shared epithelial/mesenchymal proliferation window might identify an interaction window. | **Context only.** Concurrent peaks do not establish communication or the direction of a Wnt-to-IL-1 sequence. The later [Nb1 review](../gate1_03_nabhan_2018/RQ_RETROSPECTIVE_REVIEW.md) handles ligand-source evidence; do not count the same GSE262927 animals as a second confirmation. |

No new canonical biological branch is justified by these already-incorporated
results. The useful retrospective change is to preserve the narrowed premises
and prevent historical GSEA conclusions from being revived as mechanism.
