# A9 recipient receptor/context RNA screen v1

Completed 3 November 2026 under freeze `9123b7a`. [Receipt](../../../analysis/research/runs/A9_receptor_context_v1_20261103/receipt.json) and [all donor/gene contrasts](../../../analysis/research/runs/A9_receptor_context_v1_20261103/within_donor_recipient_pairs.tsv) preserve the complete measured evidence. Independent coordinator numerical review passed 28,649 arithmetic checks (maximum error 4.44e-16). Execution is not scientific acceptance.

The question is whether the original recipient labels differ in six specified receptor/context transcripts. This descriptive comparison retains the original 22 donors and 4,648 cells. Of 44 donor/recipient strata, 41 meet the original 10-cell subtype threshold; 19 donors support both labels. All 132 attempted gene pairs are retained: 114 estimated and 18 unestimated. Cells are nested in donors and reused source data are not replication.

The endpoint is the mean per-cell natural log1p(10,000 × raw count / full-feature library), with Myofibroblast minus Fibroblast within each donor. All six fixed targets are shown below; summaries weight the 19 eligible donors equally. Raw sums, detected counts, libraries and EGFR/ERBB2 co-detection with all recipient cells as denominator are saved in the run.

| Gene | Mean paired difference | Range across donors |
|---|---:|---:|
| EGFR | -0.497502 | -1.262078 to -0.040752 |
| ERBB2 | +0.011473 | -0.082623 to +0.148079 |
| ERBB3 | +0.004321 | -0.072827 to +0.056173 |
| ERBB4 | -0.090096 | -0.399751 to +0.048170 |
| ERRFI1 | -0.528130 | -1.196026 to -0.142124 |
| LRIG1 | +0.077050 | -0.185153 to +0.319636 |

EGFR and ERRFI1 are lower in Myofibroblast in every eligible donor pair; the other four targets have mixed directions. This establishes a measured RNA context difference within the deposited labels, not a receptor-competence ranking. RNA dropout, depth and annotation remain relevant alternatives. Sparse zeros do not establish absent protein or equal function.

The original encoded-complex result remains unfavorable: 7 of 22 donors meet complex coverage, below the required 11. No LIANA refit, ligand-rank rescue or relaxed gate was performed. EGFR/ERBB2 co-detection does not show a physical dimer or AREG dependence. ERBB3/ERBB4 are family context, not designated direct AREG receptors; ERRFI1/LRIG1 RNA does not measure effective inhibition. The missing discriminator is matched functional receptor/feedback measurement and AREG-dependent response within recipient contexts.

[Reviewed target roles](../../../docs/research_reviews/2026-11-03-full-priority-screening/A9_TARGET_SOURCE_REVIEW.md), [exact specification](../../../docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A9_RECIPIENT_SPEC_V1.md) and [contract](../../../analysis/research/contracts/A9.receptor_context_v1.json) separate published premises, analysis choices and repository evidence.
