# IL-10 RNA: completed source description and robustness

8 November 2026. **Sx10-P01; exposed shared-source reanalysis.** The deposited
activated human CD8 libraries support broadly weaker 10-DE responses and mixed
super-10 responses relative to WT. Super-10 is higher for IFNG/IL18RAP but lower
for GZMB/IL22/SOCS3 in every specified scale/omission case. It does not uniformly
amplify the WT transcriptional pattern. CCL1's almost-zero direct super-10-WT
contrast is sensitive to library omission and cannot be assigned a stable direction.

[Figures](FIGURES.md) · [Exact methods](METHODS_V1.md) ·
[Source qualification](SOURCE_QUALIFICATION.md) · [Validation](VALIDATION.md) ·
[Completed/held ledger](COMPLETION_LEDGER.md).

## Comparison, coverage and primary findings

GSE160332 contains eight libraries from human CD8 cells activated for three days,
then treated with PBS or 10 nM WT IL-10, 10-DE or super-10 for 24 hours. Two
biological RNA replicates are author-reported; donor/preparation identities and
pairing remain unknown. All library and stable-ID rows are retained. This is a
finite-library description, not independent replication or population inference.

The fixed CPM>=1 in at least two libraries rule admits 12,677/58,735 rows. All
23 Figure5A symbols map uniquely; IL2 falls below the rule and remains shown but
excluded from panel medians. All eight Figure5B symbols qualify and are already
within Figure5A; the panels are not independent evidence. There are 12,655 eligible
background rows after excluding every target. No favorable gene replacement,
sample exclusion, extra signature or effect-margin selection occurred.

Primary values below are differences of group means of **log2(CPM+1)**. They
are neither fitted population log-fold changes nor the authors' exact plotting
procedure. The fixed Figure5B targets appear in plan order; the final two columns
answer the direct requested comparisons. Full precision is in
[target_sensitivity.csv](../../analysis/research/runs/sx10_description_v1/target_sensitivity.csv).

| Target | WT-PBS | 10-DE-PBS | super-10-PBS | 10-DE-WT | super-10-WT |
|---|---:|---:|---:|---:|---:|
| IFNG | -0.146 | -0.027 | +1.294 | +0.119 | +1.440 |
| IL18RAP | +0.152 | +0.038 | +0.898 | -0.115 | +0.746 |
| IL9 | +2.238 | +1.078 | +2.100 | -1.161 | -0.138 |
| GZMB | +1.522 | +0.348 | +0.906 | -1.174 | -0.617 |
| CCL1 | -2.092 | -0.879 | -2.094 | +1.213 | -0.001 |
| CCL17 | -2.408 | -0.505 | -1.743 | +1.903 | +0.666 |
| CCL22 | -2.451 | -0.908 | -2.045 | +1.543 | +0.406 |
| SESN3 | -1.021 | -0.220 | -0.939 | +0.800 | +0.082 |

Positive direct changes in suppressed chemokines mean **weaker suppression**,
not uniform stimulation. IFNG is an instructive qualification: WT-PBS is slightly
negative here; its positive 10-DE-WT value is movement toward PBS, not enhanced
WT-like induction. Published source-group names do not dictate each measured sign.

Among the 11 eligible source-up targets, all 11 are closer to PBS under 10-DE in
primary CPM; nine keep the WT direction and two reverse. All 11 eligible source-down
targets are closer to PBS and retain their WT direction. Up/down direct medians
are -1.075/+1.030 respectively. Under super-10, 7/11 up and 10/11 down members
are closer to PBS, with direct medians -0.223/+0.406. These separate direction
groups are descriptions of a published selection, not opposing functional scores.

## Amplitude reference and bounded sensitivity

The fixed background through-origin coefficient compares variant-PBS with WT-PBS.
Shared PBS, noisy WT values, measurement error and unknown donor/preparation effects
limit this reference; beta is not a causal response fraction or variance explained.

| Scale | 10-DE beta: full [omission range] | super-10 beta: full [omission range] |
|---|---:|---:|
| CPM | 0.376 [0.305, 0.516] | 0.645 [0.539, 0.751] |
| Median-ratio CPM | 0.373 [0.300, 0.516] | 0.644 [0.535, 0.755] |
| Deposited FPKM | 0.373 [0.302, 0.518] | 0.653 [0.548, 0.769] |

Both variants lie below the equal-response reference globally, while super-10
has specific targets above WT. Overall attenuation and gene-response differences
coexist. Primary up/down median amplitude residuals are -0.173/+0.067 for 10-DE
and +0.203/-0.190 for super-10. A residual above a reference does not establish
preserved function or causal selectivity. All panel/case values and member
disagreements are retained in [panel_summaries.csv](../../analysis/research/runs/sx10_description_v1/panel_summaries.csv).

All three scales × nine views retain positive super-10-WT for IFNG and IL18RAP,
and negative values for GZMB, IL22 and SOCS3. Primary direct values and eight-omission
ranges are +1.440 [+1.390,+1.490], +0.746 [+0.660,+0.833],
-0.617 [-0.642,-0.591], -0.893 [-0.994,-0.792] and
-0.532 [-0.589,-0.474], respectively. These are observed ranges, **not CIs**.
For CCL1 the primary direct value is -0.001 with range [-0.246,+0.243]; all
three scales cross zero under omission. No stable CCL1 enhancement/suppression
claim is made. Under 10-DE, 10-11/11 eligible up members and 11/11 down members
are closer to PBS across all 27 cases; the exact full-data result remains primary.

[Every target range](../../analysis/research/runs/sx10_description_v1/target_ranges.csv),
[all library values](../../analysis/research/runs/sx10_description_v1/target_library_values.csv),
[all-row primary output](../../analysis/research/runs/sx10_description_v1/all_gene_primary.csv)
and [normalization factors](../../analysis/research/runs/sx10_description_v1/normalization_factors.csv)
retain the full results. No normalization, exclusion or target was chosen after viewing outcomes.

## Interpretation and next decision

This source description reproduces the paper's mixed super-10 and weaker 10-DE
transcriptional patterns within the qualified scope. The modest IFNG WT-PBS sign,
low IL2 capture and CCL1 omission sensitivity limit broad source-group statements.
The contribution is measurement verification and robustness, not a new mechanism.

Published phospho-flow and myeloid/ELISA findings are separate premises in the
[assay map](SOURCE_EVIDENCE.md). The RNA library units are not joined to their
donors/experiments. D25K is not an RNA arm, and Figure4E survival tests WT/10-DE.
No RNA value demonstrates myeloid suppression, secretion, cytotoxicity, STAT1
mediation, receptor thresholds, protection, kinetics or persistence. The results
do not warrant an affinity-only model or a claim that super-10 must amplify every
gene. No exact replay is claimed: S9 and exact author transformation/filtering/
aggregation remain unrecovered. No human acceptance or claim grade is inferred.

The bounded authorized computation is complete. To estimate population effects,
obtain actual donor/preparation and allocation/pairing keys and qualify an
identifiable model/precision plan. To connect RNA heterogeneity to signaling or
secretion, obtain assay-matched raw dose/time measurements and biological-unit
joins; additional scores cannot supply that link. A new model, atlas or raw-read
pipeline is not required by these results.
