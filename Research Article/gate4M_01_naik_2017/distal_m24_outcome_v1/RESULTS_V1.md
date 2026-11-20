# M24 accessibility at distal epidermal Memory and Resolved regions

At 24 months, the post-IMQ pools had higher mean accessibility across the 791 distal Memory regions and lower mean accessibility across the 784 distal Resolved regions than the naïve pools. Together these differences widened the Memory–Resolved gap by **0.11697 fragment CPM**. The gap widened in each of the four possible post-IMQ versus naïve pool comparisons. [Figure (PNG)](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/m24_distal.png) · [Figure (PDF)](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/m24_distal.pdf)

<a id="how-much-did-each-class-contribute"></a>

## Contributions of the two region classes

Each entry below is the mean of the two post-IMQ pool summaries minus the mean of the two naïve pool summaries, in fragment CPM. The gap is the Memory change minus the Resolved change. The primary summary gives equal weight to each region's full-width mean signal. The median uses the median of those region means within each class and pool. [Frozen method](METHOD_V1.md) · [Exact changes](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/history_changes.tsv)

| Within-pool summary | Memory change | Resolved change | Change in gap |
|---|---:|---:|---:|
| Mean, full distal set | +0.08974 | −0.02723 | **+0.11697** |
| Mean, D6- and width-weighted | +0.09761 | −0.02389 | **+0.12149** |
| Median, full distal set | +0.05312 | −0.02004 | **+0.07315** |

| M24 pool | Memory mean | Resolved mean | Gap |
|---|---:|---:|---:|
| Naïve 1 (GSM9034861) | 0.24062 | 0.21211 | 0.02851 |
| Naïve 2 (GSM9034862) | 0.30098 | 0.26298 | 0.03800 |
| Post-IMQ 1 (GSM9034863) | 0.40638 | 0.22132 | 0.18506 |
| Post-IMQ 2 (GSM9034864) | 0.31471 | 0.19931 | 0.11540 |

| Post-IMQ minus naïve | Memory change | Resolved change | Change in gap | Weighted change in gap |
|---|---:|---:|---:|---:|
| Post 1 − naïve 1 | +0.16575 | +0.00920 | +0.15655 | +0.16988 |
| Post 1 − naïve 2 | +0.10540 | −0.04166 | +0.14706 | +0.15630 |
| Post 2 − naïve 1 | +0.07409 | −0.01280 | +0.08689 | +0.08669 |
| Post 2 − naïve 2 | +0.01373 | −0.06367 | +0.07740 | +0.07311 |

The four comparisons reuse the same pools. In the first comparison both class means rose. In the last, the Memory mean rose slightly while its median fell by 0.01269 CPM. The positive aggregate median gap change therefore coexists with variation across pool comparisons and summary measures. [All pool summaries](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/pool_summaries.tsv) · [All cross-pool contrasts](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/cross_pool.tsv)

<a id="what-does-the-weighting-resolve"></a>

## Interpretation of the weighted comparison

Both classes occurred in all 16 D6 induction-by-width strata. Weighting retained all regions, with regional effective sample sizes of 597.47 for Memory and 588.55 for Resolved. The standardized class difference fell from 0.888 to 0.093 for D6 log2 fold change and from 0.424 to 0.052 for width. The late gap change persisted at this improved balance. Residual within-stratum differences and D6 control accessibility remain unresolved. The deposited baseMean combines conditions and times. [Stratum support and balance](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/support.json) · [Regional weights](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/region_weights.tsv)

Cowley et al. already showed late accessibility trajectories. This shared-source analysis quantifies the distal subset, the contribution of the Resolved comparator and the spread across the available pools. Class selection used earlier D6/D30 measurements, and the tested region universe incorporated M12. M24 did not select the classes, but the published aggregate trajectory was known before the analysis. Each M24 library pools two or three mice, with two pools per history from one experiment. Individual membership, cross-group pairing and sorted-cell composition remain unresolved. These data describe late accessibility. Continuous maintenance in the same cells, a repair mechanism and mouse-level variability remain unmeasured. [Cowley et al., Fig. 1 and Methods](https://doi.org/10.1126/science.adz6830) · [Source qualification](../distal_m24_qualification_20261119/METADATA_REGISTRATION_V1.md)

## Execution and readback

The frozen contract ran once. All 6,300 region–pool observations passed full-width coverage checks, including 485,283 explicitly stored zero-valued bases across 4,327,880 assayed library-bases. A separate calculation from the saved interval means and registered region covariates reproduced pool summaries, class changes, cross-pool contrasts, regional weights and balance in 1,683 numerical comparisons using relative and absolute tolerances of 10⁻¹². Receipt verification passed. Visual inspection of the actual PNG and rendered one-page PDF confirmed legible class and pool labels, legends and points in all four panels. [Contract](../../../analysis/research/contracts/Nk17-P01.distal_m24_outcome_v1.json) · [Interval values](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/intervals.tsv) · [Coverage](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/coverage.json) · [Receipt](../../../analysis/research/runs/naik2017_distal_m24_outcome_v1/receipt.json)
