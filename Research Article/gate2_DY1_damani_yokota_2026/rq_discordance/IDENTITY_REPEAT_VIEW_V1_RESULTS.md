# A3/DY1-P02: fixed-target repeat-stimulation source view

3 November 2026. Executed after reviewed freeze `b29961b`. [Receipt](../../../analysis/research/runs/A3_identity_repeat_source_view_v1_20261103/receipt.json), [all values and primitives](../../../analysis/research/runs/A3_identity_repeat_source_view_v1_20261103/target_source_average_view.tsv), [verification](../../../analysis/research/runs/A3_identity_repeat_source_view_v1_20261103/verification.json). Receipt verification passed; 48 scalar checks against the four original WT group averages agree with the frozen full-table contrasts (maximum absolute error 1.57e-15). This is numerical verification of the same source, not replication or scientific acceptance.

The six targets do not show uniform enhancement on repeat stimulation. Egr2 and Irf4 retain positive within-stage RNA ratios but smaller second-stage ratios; Pparg has the opposite stage-difference direction. Stat6/Rxra ratios are negative in both stages. ARG1 remains a separate effector: its second-minus-first result is nearly zero at offset 1 but more negative at offset 0.5, accompanied by a changed baseline. These are log ratios of author-supplied group averages, not individual trajectories or maintenance measurements.

| Gene | Offset | First stage | Second stage | Second minus first | Baseline shift |
|---|---:|---:|---:|---:|---:|
| Stat6 | 1.0 | -0.3395 | -0.4815 | -0.1420 | +0.0128 |
| Stat6 | 0.5 | -0.3401 | -0.4823 | -0.1423 | +0.0129 |
| Egr2 | 1.0 | +4.0489 | +2.8507 | -1.1982 | +0.8434 |
| Egr2 | 0.5 | +4.1086 | +2.8809 | -1.2277 | +0.8719 |
| Pparg | 1.0 | +0.0968 | +0.6863 | +0.5895 | -0.1423 |
| Pparg | 0.5 | +0.0988 | +0.6991 | +0.6002 | -0.1455 |
| Rxra | 1.0 | -0.4947 | -0.5294 | -0.0347 | +0.4364 |
| Rxra | 0.5 | -0.4968 | -0.5311 | -0.0343 | +0.4378 |
| Irf4 | 1.0 | +3.0328 | +2.4315 | -0.6013 | +0.5876 |
| Irf4 | 0.5 | +3.0667 | +2.4523 | -0.6144 | +0.6006 |
| Arg1 | 1.0 | +6.2595 | +6.2559 | -0.0036 | +0.8862 |
| Arg1 | 0.5 | +6.8755 | +6.5557 | -0.3198 | +1.2055 |

All four WT source averages and both controls are retained in the table; no KO values, biological n, uncertainty interval, target ranking or pooled cross-source estimate were produced. Source normalization remains author-labelled averaged CPM/Cufflinks. Different stage baselines, stimulation context, population composition and offsets limit interpretation. This view can guide a subsequent explicitly measured persistence/rechallenge comparison; it does not establish NAM/infection memory, protein activity or an injury-repair mechanism. The separate [completed six-target induction screen](IDENTITY_TARGETS_V1_RESULTS.md) remains unchanged. Every target and both offsets are reported; no expanded positive set was sought.

Independent coordinator review passed the 48 raw-value and 48 contrast checks.
