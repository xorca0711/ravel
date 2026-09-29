# Figure audit completion, 29 September 2026

This completes the presentation audit begun in [PR #118](https://github.com/xorca0711/scRNA_seq/pull/118), following the distribution-focused A16 additions in [merged PR #117](https://github.com/xorca0711/scRNA_seq/pull/117). The intended standard is to make the observations and biological units behind a result visible, choose a display appropriate to the analysis, and keep every title within the evidence. It does not require one plot style everywhere or imply that a summary statistic is inherently invalid.

The [consolidated inventory](FIGURE_AUDIT_CONSOLIDATED.csv) now exists. It contains **367 figure families and 480 assets: 367 PNGs, 86 SVGs and 27 PDF companions**. A family is one extensionless repository path; historical versions and saved render copies have distinct paths. Every tracked image and every figure PDF has a disposition. The archived portfolio PDF is a document, not a figure asset, and is excluded. At the start of this continuation, PR #118 contained 346 families / 447 assets under this definition.

## What PR #118 had and what needed correction

The branch had revised several claim-bearing labels and rendered some figures, but seven figures explicitly identified by its own audit remained stale. Its claimed 118-row CSV was absent, and its 112/118 figure totals were inconsistent. Those totals and the purported universal claim verification are withdrawn. Saved tables, plus an existing A1 display cache, allowed all seven cited stale presentations to be regenerated without new scientific fits.

Several proposed corrections also needed correction:

- **A2:** donor ranks are deposited. The current figure now shows the 22 actual donor ranks per resource and their medians.
- **A6:** the transcript-share denominator is all macrophage transcripts in each gene set, not within-state transcript activity.
- **England EN_C02:** the replacement claim that AT2-assigned clusters always contain AT1 cells was still false. Four Experiment-2 clusters have AT2 cells and no detected AT1 cells. The figure now reports the observed top-AT2 gate counts, 8/8 and 5/7.
- **A12 F03:** the predicted ranges are wider than observed; descriptive prediction-on-observation slopes alone do not establish failure at the extremes. Both the figure and its rationale now state the measured quantities.
- **A16:** having the most control genes is not a power calculation. Singular wording such as “the most” did not itself imply that only one entry met the display floor. The real problem was the power and specificity interpretation.
- **A12 F01:** aggregate RMSE is a legitimate summary. The missing information was the paired patient-level errors, now displayed underneath it; no interval treats overlapping LOPO training sets as independent.

## Completed changes

**41 current figure families** have corrected presentations within PR #118, including retained corrections from its initial commits. The inventory separates these from their preserved predecessors.

| Scope | Current families corrected | Main changes |
| --- | ---: | --- |
| A12 | 3 | Paired errors for all 12 patients; 70 patient-histology observations from 23 people; correct 50% reference placement; corrected range/slope interpretation |
| A16 | 5 | Three tested k values; control counts without power claims; histograms without a power-based interpretability claim; matched-control means labeled as averages; residual imbalance retained in interpretation |
| Shared A1/A2/A6-A9 and iCAP, plus three local A1 revisions | 10 | Actual donor ranks; correct denominators; nuclei/wells and technical uncertainty limits; reporter-detected denominator; verified 22-mouse HPCS and eight-mouse CD44 identities with remaining confounding explicit |
| England | 9 | Saved-table rendering; corrected gate counts; separate rank-biserial and SMD axes; association rather than attribution, depth exclusion or equivalence; correct library/cell/time units |
| Cardoso, Choi and Niethamer | 13 | Eight Cardoso claim revisions; Choi column scaling and cell counts; four Niethamer categorical-time and same-RNA annotation revisions |
| A5/A11 | 1 | Explicit 24/26 mice versus eight patient pairs; original estimates and interval methods retained |

A12's paired plots reveal why the aggregate matters: joint error improves for 7/12 AT2 patients, 5/12 fibroblast patients and 8/12 A13 patients. A13 nevertheless has worse aggregate error because improvements and losses differ in magnitude. The primary-setting statement that no A13 model beats the training mean is now kept separate from the alpha=10 alternative, which does beat it.

Further untouched-figure corrections remove Cardoso's causal depth, universal mixture/resolution, isolated species-effect and definitive state-identity claims. Choi's heatmap scales programme columns, despite its old row-scaling label. Niethamer's equally spaced harvests are categories, and comparisons with labels derived from the same RNA are internal concordance, not independent biological validation. A1's verified identity closure does not remove chase/library confounding or resolve TIGIT pool independence.

Current galleries and rationales point to dated revisions where the originals are historical records. Frozen execution sources, original archived figures and scientific numerical tables are preserved. Live producer wording is synchronized so the corrected errors do not recur in a future render.

## Coverage and remaining limits

| Disposition | Families | Meaning |
| --- | ---: | --- |
| Corrected current | 41 | Saved-evidence corrections rendered; corrected images visually inspected |
| Retained, numerical checks | 12 | A0/A10 saved values and displayed labels checked; no further modification identified |
| Retained, source/family screen | 280 | Producers, units, labels and representative displays screened; this is **not** independent validation of every raw measurement |
| Preserved, superseded | 26 | Earlier figure versions kept for provenance; use the linked current presentation |
| Historical reference | 5 | Archived or reference evidence, not promoted to current claims |
| Reproduction copy | 1 | Saved render copy, not another scientific result |
| Retained, reproduction input gap | 2 | England EN_F03 and FU_F01 retained; exact missing processed inputs are listed per row |

The 280 screened families include descriptive embeddings, feature maps, annotation/QC panels and unit summaries. Their retention means no concrete additional presentation defect was identified at the recorded review depth. It does not turn descriptive RNA, pooled cells, one cell line, or technical seeds into biological replication or functional evidence.

EN_F03 requires the per-library processed RNA cell tables; FU_F01 requires the processed round-2 embeddings and continuation cell table. Neither has a demonstrated numerical error that can be repaired from the available aggregate tables. Restore those inputs only if exact reproduction is needed. Historical versions remain unchanged even when their wording is superseded.

## Verification

[Deciding checks](figure_audit_2026-09-29/deciding_checks.json) retain the numerical and provenance checks from the scoped reviews. Each corrected presentation has local input/output provenance. These records describe the renderer's actual input bytes; unpinned text line endings can differ between Windows and Linux checkouts. The consolidated inventory therefore normalizes SVG line endings for its portable hash check, while PNG/PDF hashes are exact bytes.

Run `python docs/figure_audit_2026-09-29/verify_inventory.py` to check complete tracked coverage, unique families, format counts and all 480 asset hashes. This verifies this dated inventory; it does not rerun science. Repository-required compilation, evidence tests, claim-contract checks, Nb1 verification, archived A16 verification and documentation validation are recorded with the final PR checks.

Local validation passed: 69 evidence tests, 18 numeric claim bindings, 17 Nb1 output hashes, 1,867 archived A16 checks and 4,594 repository checks. The inventory check verifies all 480 image/PDF assets. No scientific fits or source tables were rerun or edited.
