# E1a: observed transcript measurements

31 October 2026 (Asia/Seoul). **C0–C3 completed at the defined descriptive scope.**
Owner Sx22-P01; no canonical RQ or scientific acceptance is created.
[Gallery](FIGURES.md) · [C0 qualification](C0_QUALIFICATION.md) ·
[Validation](VALIDATION.md) · [Prospective question and source context](README.md).

## What was measured

This shared-source reanalysis describes the two fixed transcripts `Il22ra1` and
`Il10rb` in the 11,683 retained Choi benchmark cells. It uses the saved count layer,
library identifiers and literal pipeline labels without preprocessing or
relabeling. Each library pools two mice and there is one library per condition;
the measurement unit is the retained cell, not an independent animal replicate.
The [source scientific review](../../gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md)
qualifies selection, pooling and incomplete annotation. Published Choi Figure 1
and Saxton receptor-context findings are premises documented in the plan, not
newly reproduced biological findings here.

For a gene and a library/label stratum, detection is the number of cells with a
positive saved count divided by the number of retained cells in that stratum.
Count-derived abundance is:

`1,000,000 × sum(gene counts in stratum) / sum(all 27,998 saved feature counts in the same stratum)`.

This is a ratio of count sums, not a mean of individually normalized cells.
Cells with more captured counts contribute more to its denominator. It is not
TPM, protein abundance or a response score. No condition contrast, test, effect
estimate, confidence interval or target ranking was calculated.

## Observed aggregate measurements

Positive-cell numerators below use the explicit cell denominator in the same row.
The original non-contaminant rule excludes only labels beginning `contaminant_`;
unassigned cells would remain included. Aggregates overlap the label rows and
must not be added together or treated as independent evidence.

| Library / denominator | Cells | Il22ra1 positive cells | Il22ra1 counts per million | Il10rb positive cells | Il10rb counts per million |
|---|---:|---:|---:|---:|---:|
| PBS / all retained | 4,319 | 0 | 0 | 1,098 | 60.539617 |
| PBS / non-contaminant | 4,236 | 0 | 0 | 1,066 | 60.008210 |
| day 14 / all retained | 3,790 | 2 | 0.057935 | 1,327 | 57.239504 |
| day 14 / non-contaminant | 3,592 | 1 | 0.030580 | 1,247 | 56.052668 |
| day 28 / all retained | 3,574 | 0 | 0 | 1,197 | 55.506064 |
| day 28 / non-contaminant | 2,571 | 0 | 0 | 814 | 54.837359 |

The [complete stratum table](../../../analysis/research/runs/sx22_e1a_recipient_description_v1/strata.csv)
contains exact cell/count denominators, detection fractions, gene-count sums and
0/1/at-least-2 count bins for every label/library/gene. The
[cell audit table](../../../analysis/research/runs/sx22_e1a_recipient_description_v1/cell_counts.csv)
retains both selected counts and total counts for every original cell ID.

## Coverage and interpretation

Il22ra1 has two observed single-count detections in the entire retained matrix:
one in a day-14 `DATP`-labelled cell and one in a day-14
`contaminant_ciliated`-labelled cell. The respective stratum denominators are 672
and 71. These are literal pipeline labels and sparse captured counts, not
identified responsive cell types, true biological localization or proof against
ambient signal. The non-contaminant aggregate consequently contains one observed
single count. No additional gene, threshold, cohort or analysis was selected to
obtain a more positive pattern.

Il10rb detection is reported separately for the same retained cells. It is not a
substitute for Il22ra1 measurement, receptor assembly, signaling or cytokine
response. No joint receptor/response score was constructed. Populated label
strata range from 3 to 4,166 cells; all remain reported, including the small
contaminant-labelled groups. Their apparent percentages do not carry animal-level
precision. Cell selection, sparse capture and annotation error remain unresolved.

The 78 table rows comprise 11 declared labels and two overlapping aggregates,
in three libraries, for two genes. Eighteen rows are empty: `pAT2`, `unassigned`
and `contaminant_endothelium` in every library, for both genes. Their cell count
is zero and their measurement fields are unavailable, not biological zeros.
The absent pAT2 label is not recovered or replaced. In a populated stratum,
zero detection is an observed count result, not proof of biological absence.

The dataset supports transparent transcript measurement description but supplies
very little observed Il22ra1 capture. It does not resolve receptor protein or
functional recipient state, and cannot support animal-level time/treatment
effects. Library/time confounding, pooled animals, exclusion bias and imperfect
labels remain as reviewed. No repair, memory, lineage or later-function claim
follows from this result.

## Execution and presentation

The numerical contract/code were committed at `5fbe78f` before the
[immutable descriptive run](../../../analysis/research/runs/sx22_e1a_recipient_description_v1/receipt.json).
The original one-decimal figure obscured four small-positive annotations.
A [separate exposed rendering amendment](RENDER_AMENDMENT_V2.md), frozen at
`56da56e`, produced the [current v2 figure](FIGURES.md) and
[render receipt](../../../analysis/research/runs/sx22_e1a_render_v2/receipt.json).
V2 changes display strings only; the original numerical table and all original
code, contracts, receipts and figures remain unchanged.

Independent checks reconciled all 23,366 selected cell counts, every cell total,
all 78 summary rows and all 18 empty rows. The originating reviewer independently
reported the same agreement. The display audit verifies all 156 measurement
annotations and distinguishes small positives, exact zeros and unavailable data.
See validation for exact methods and repository checks. Numerical verification
is not biological replication or human scientific acceptance.

All original Saxton WT/variant analyses, R2/R3 service holds and unqualified
persistence/function joins remain unchanged. Next is originating review and
authorized local integration; no additional biological extension is queued here.
