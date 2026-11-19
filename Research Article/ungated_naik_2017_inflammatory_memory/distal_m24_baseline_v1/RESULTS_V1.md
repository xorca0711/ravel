# The M24 accessibility gap after balancing four D6 control libraries

Balancing early control accessibility modestly attenuated the M24 post-IMQ versus naïve difference between distal Memory and Resolved regions. The gap change fell from **+0.12149 to +0.11608 fragment CPM**. Among regions with shared support, Memory averaged **0.08792 CPM higher** and Resolved **0.02816 CPM lower** in post-IMQ pools. The late separation therefore persisted after bringing the two classes much closer in their observed D6 control rankings. [Frozen method](METHOD_V1.md) · [Previous M24 result](../distal_m24_outcome_v1/RESULTS_V1.md) · [Exact class changes](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/history_changes.tsv)

## What changed when baseline rank was added?

Each class change subtracts the mean of the two naïve pools from the mean of the two post-IMQ pools. The gap is the Memory change minus the Resolved change. All entries are fragment CPM.

| Region population and weights | Memory change | Resolved change | Gap change |
|---|---:|---:|---:|
| Original D6 induction and width weights | +0.097605 | −0.023888 | +0.121493 |
| Original weights restricted to jointly supported regions | +0.098075 | −0.024080 | +0.122155 |
| New induction, width and baseline-rank weights on those regions | +0.087922 | −0.028160 | **+0.116082** |

Excluding 23 Memory and 27 Resolved regions and renormalizing the old weights increased the gap change by **0.000661 CPM**. Redistributing weight among the retained regions then decreased it by **0.006073 CPM**. The net change was **−0.005411 CPM**. Redistribution reduced the positive Memory change more than it deepened the negative Resolved change. [Exact decomposition for both classes and their gap](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/change_decomposition.json)

## How much did the four M24 pools vary?

| M24 pool | Weighted Memory | Weighted Resolved | Within-pool gap |
|---|---:|---:|---:|
| Naïve 1 · GSM9034861 | 0.25518 | 0.19918 | 0.05599 |
| Naïve 2 · GSM9034862 | 0.29944 | 0.25549 | 0.04395 |
| Post-IMQ 1 · GSM9034863 | 0.40829 | 0.21215 | 0.19614 |
| Post-IMQ 2 · GSM9034864 | 0.32217 | 0.18621 | 0.13596 |

The new cross-pool gap differences were **+0.14015, +0.15219, +0.07997 and +0.09201 CPM** (post 1 versus naïve 1 and 2, then post 2 versus naïve 1 and 2). Memory increased in all four comparisons. Resolved rose by 0.01297 CPM in the first comparison and fell in the other three. The four contrasts reuse the same pools. [Pool summaries](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/pool_summaries.tsv) · [Cross-pool contrasts for every weighting](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/cross_pool.tsv)

## How well did the controls agree, and what remained imbalanced?

All 6,300 D6 library–region reads passed. Across 4,327,880 library-bases, 920,435 had producer-encoded sparse zero depth and none had an explicitly stored zero. Entirely zero regions numbered 0, 6, 1 and 0 in Naik 1, Naik 2, Larsen 1 and Larsen 2. Naik 2's six zero regions shared a midrank. The four-library mean had 1,373 distinct ranks. [Coverage audit](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/coverage.json) · [Interval means](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/baseline_intervals.tsv)

| D6 control rank correlation (Spearman) | Naik 2 | Larsen 1 | Larsen 2 |
|---|---:|---:|---:|
| Naik 1 | 0.850 | 0.801 | 0.801 |
| Naik 2 | | 0.815 | 0.827 |
| Larsen 1 | | | 0.922 |

Both classes occurred in **55 of 64** joint strata, spanning all four baseline quartiles and all 16 original induction-by-width cells. The weighted target retained **768/791 Memory** and **757/784 Resolved** regions, carrying 98.20% and 98.53% of their previous weight, respectively. Regional effective sizes fell from 597.5 to 508.6 for Memory and from 588.5 to 526.7 for Resolved. [Rank diagnostics](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/rank_qc.json) · [Region weights](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/region_weights.tsv) · [Support and balance](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/support.json)

The standardized Memory minus Resolved difference in consensus baseline rank fell from **+0.568 to +0.051** (raw percentile-rank difference +0.15346 to +0.01384 on a 0–1 scale). Residual standardized differences for Naik 1, Naik 2, Larsen 1 and Larsen 2 were −0.004, −0.081, +0.198 and +0.079. Width balance was similar (+0.052 to +0.051), while residual imbalance in D6 induction **increased** (+0.093 to +0.142). Balancing the consensus reduced the class difference along that measured axis, while library-specific and within-stratum differences remained. [Balance by covariate and weighting](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/support.json)

## Interpretation and verification

Bringing the observed D6 control ranks into closer balance reduced the estimated late gap change by about 4.45% relative to the previous weighting. The inference applies to the supported distal intervals and four pooled M24 libraries in one experiment. The data leave absolute baseline accessibility, individual-mouse D6-to-M24 pairing, changes in sorted-cell composition and continuous maintenance in the same cells unresolved. Cowley Fig. 1 and the previous shared-source M24 estimates were known before the sensitivity was frozen. [Cowley et al., Fig. 1](https://doi.org/10.1126/science.adz6830) · [Exposure record and contract](../../../analysis/research/contracts/Nk17-P01.distal_m24_baseline_v1.json)

The governed runner completed once from `df25bb8` without a coverage or support hold. Receipt verification passed. A separate standard-library calculation rebuilt tied ranks from the saved D6 means, the two- and three-way strata and weights from region covariates, and the pool-level changes from the 6,300 saved M24 means. It reproduced the rank agreement, support, balance, four-pool contrasts and decomposition in 13,114 numerical comparisons with relative and absolute tolerances of 10⁻¹². [Verified receipt](../../../analysis/research/runs/naik2017_distal_m24_baseline_v1/receipt.json) · [Saved M24 means](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/intervals.tsv)
