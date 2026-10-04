# Wagner R1: source-score reconstruction and pathway heterogeneity

4 October 2026. **Numerical estimates generated; independent verification in progress.**
Owner **Wg-R01**, with supporting evidence for **Wg-P02**. This is an exposed,
descriptive analysis of the pinned author example, not independent biological
replication or complete reproduction of the manuscript.

## Question, decision and strongest rival

Do the source-provided Compass penalties recover condition-associated reaction
patterns, and which patterns are lost when reactions are summarized by pathway?
The decision concerns the required resolution of a metabolic readout. The
strongest rival is that score orientation, correlated reaction duplication,
annotation choices or unknown biological nesting produce apparent specificity.

The observations are **139 Th17p and 151 Th17n cells**, qualified by the R0 exact
identity join. Independent animals/preparations remain unknown. The endpoint is
the standardized difference in transformed predicted-activity scores, with
source-cell Mann–Whitney/BH values used to reconstruct the source convention.
Neither a score nor a source-cell q value establishes metabolic flux, fate,
pathway activation or a population-level condition effect.

## Main observations

| Quantity | Reconstructed value | Interpretation |
|---|---:|---|
| Deposited reaction profiles | 10,211 | Same pinned author matrix, not new cells |
| Exactly constant raw profiles | 3,647 | Excluded from undefined Spearman grouping; identities retained |
| Individual reactions passing transformed-range filter | 6,373 | Individual-reaction test family |
| Formed / range-retained metareactions | 1,912 / 1,722 | Grouped test family uses the 1,722 retained groups |
| Core reaction members / distinct groups with a core member | 1,838 / 784 | Multiple reaction members are not independent hits |
| Display pathways / pathways with both source-significant directions | 53 / 20 | Unique groups counted within each pathway; groups may overlap across pathways |

Glycolysis/gluconeogenesis contains **29 distinct groups**, with median d **0.319**;
19 groups meet source q < 0.1 in the Th17p-higher direction and none in the
opposite direction. Thus this run does not show a within-glycolysis opposing
association. A later PGAM result from different data cannot be substituted for
this source observation.

Fatty-acid oxidation has **107 groups**, median d **−0.020**, with **7 Th17p-higher
and 23 Th17n-higher** groups at source q < 0.1. A near-zero pathway median conceals
large, oppositely signed group associations. Arginine/proline metabolism likewise
has **12 groups**, median d **0.197**, with **6 positive and 1 negative** group;
its arginine-decarboxylase/agmatinase group is negative. The mitochondrial TCA
subset has **13 groups**, median d **0.128**, and 3 positive/0 negative groups
meeting the source threshold. These are descriptive representation differences.

| Prespecified reaction | Metareaction d: Th17p minus Th17n | Source-cell BH q |
|---|---:|---:|
| PGM_neg: phosphoglycerate mutase | 0.508 | 2.87e−5 |
| LDH_L_neg: lactate dehydrogenase | 0.383 | 0.00149 |
| PDHm_pos: pyruvate dehydrogenase | 0.436 | 0.00175 |
| ICDHyrm_pos: isocitrate dehydrogenase | 0.049 | 0.871 |
| C160CPT1_pos: carnitine palmitoyltransferase | −0.255 | 0.0357 |
| ARGN_pos: arginase | −0.406 | 0.000862 |
| ARGDCm_pos / AGMTm_pos: one shared group | −0.395 | 0.00109 |
| SPMDOX_pos: spermidine dehydrogenase | −0.147 | 0.00378 |
| r0281_neg: putrescine diamine oxidase | −1.204 | 2.01e−46 |

All 14 prespecified reactions, including weak effects, are retained in the
[complete table](../../analysis/research/runs/wg_source_scores_v3/selected_reactions.tsv).
The display table above is a readable subset, not a newly selected test family.

## Reconstruction limits and retained discrepancies

The declared implementation forms **1,912 groups**, compared with **1,911**
reported in the paper. Its **784 core groups** match the reported core count.
The total mismatch remains unresolved; neither filtering nor clustering was
tuned to obtain a match. No exact manuscript numerical reference table was
recovered. Count agreement and qualitative concordance are insufficient for
claiming exact historical reproduction.

The helper uses `-log(penalty + 1)`; this implementation explicitly freezes
`-log1p(penalty)`. They are mathematically equivalent, but finite-precision ties
can differ. The source helper also lacks an explicit guard for exactly constant
raw profiles, and historical clustering/software equivalence is unqualified.
The supported label is **declared-algorithm reconstruction of author processed
outputs**, with source-rule and numerical implementation differences disclosed.

The first two runs are retained: v1 stopped on a Windows integer join; v2 stopped
when independent verification exposed float64 tie differences. The
[v3 amendment](NUMERICAL_AMENDMENT_v3.md) records the correction and prior outcome
exposure. Version 3 preserves exact tested scores and separates transformation
verification from rank-test arithmetic. No statistical threshold was relaxed.

Deposited single-cell batch labels 7 and 8 contain both conditions; batch 9
contains 17 Th17n cells only. These are not verified biological replicate labels.
No batch-adjusted animal model, independent-unit uncertainty or confirmatory
claim is supplied. Small source-cell q values cannot resolve that missing unit.

## Evidence and next decision

- [Frozen design](SOURCE_ANALYSIS_DESIGN_v1.md), [current contract](config/source_scores_v3.json)
  and [amendment](NUMERICAL_AMENDMENT_v3.md).
- [Current receipt](../../analysis/research/runs/wg_source_scores_v3/receipt.json),
  [summary](../../analysis/research/runs/wg_source_scores_v3/summary.json),
  [all pathway results](../../analysis/research/runs/wg_source_scores_v3/pathway_summary.tsv).
- [Exact tested arrays](../../analysis/research/runs/wg_source_scores_v3/tested_scores.npz)
  and [reaction/group crosswalk](../../analysis/research/runs/wg_source_scores_v3/metareaction_membership.tsv).
- Primary methods source: [Wagner et al., Cell (2021)](https://doi.org/10.1016/j.cell.2021.05.045),
  STAR Methods and author helper/notebook pinned in the R0 manifest. Primary-source
  precedent interpretation is separate from these newly computed local results.

Wg-P02 now has a bounded source-data result supporting reaction-level reporting
for the mixed pathways. It does not establish a new metabolic mechanism or
generalize a glycolytic exception. R2 full Compass, R3 RNA, R4 ATAC, R5 functional
assays and the other branches retain their separately stated source/design gates.
Human acceptance, claim promotion and global RQ registration remain unassigned.
