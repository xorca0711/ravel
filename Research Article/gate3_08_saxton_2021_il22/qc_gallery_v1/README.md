# Technical QC gallery v1

1 November 2026 (Asia/Seoul). Owner **Sx22-P01**. This package makes two already
reviewed technical summaries visible as figures. It does not add biological
findings or repeat the original analyses.

## Prospective render-only plan

Question: how can the existing library and annotation QC quantities be displayed
with their technical units, source order and denominator limits intact? Purpose:
provide two useful, auditable views of the saved evidence. The principal threat
is mistaking technical libraries for independent animals, or overlapping
annotation dimensions for mutually exclusive groups.

| Figure | Fixed source and display | Unit and boundary |
|---|---|---|
| R1 library QC | Three aligned horizontal-bar panels: total counts, nonzero gene rows and largest-ten count fraction. All six libraries in the frozen table's original order; one color, no treatment grouping or contrast | Technical library records. Animal identity/independence remains unknown. Values are copied, not recomputed from expression data |
| X1 annotation QC | Multiplicity distribution of repeated symbol labels; separate bars for six overlapping annotation dimensions in fixed metadata order | 52 repeated symbol labels covering 122 deposited rows. No named symbols, gene ranking, remapping, functional inference or category pie chart |

R1 authority: [review](../R1_REVIEW.md) and its immutable
[library table](../../../analysis/research/runs/sx22_r1_v2/library_qc.csv).
X1 authority: [reviewed results](../extensions_20261031/RESULTS.md), frozen
[summary](../../../analysis/research/runs/sx22_x1_annotation_v1/summary.json) and
[repeated-symbol metadata](../../../analysis/research/runs/sx22_x1_annotation_v1/repeated_symbols.csv).
Source receipts and sample order are hash-bound. No raw counts, H5AD, treatment
model, source pipeline or literature refresh is required for this rendering task.

All source values were exposed in prior reviews and in this task's input reading.
The new contract/code/tests must be committed before rendering the real tables.
Rendering uses the repository runner and a fresh immutable directory. Auditable
plot-value tables retain exact source quantities, explicit denominators and
display labels. Missing or inconsistent source fields stop rendering; no silent
replacement, small-group exclusion or post-result selection is permitted.

The largest-ten fraction is displayed as a percentage, with four decimal places;
integer labels remain exact. X1 multiplicity bins are numerically ordered, and
the six ambiguity dimensions retain source metadata order. Each dimension uses
the same denominator of 52 labels; the dimensions overlap and cannot be summed
as a partition. Zero categories remain visible and labelled. No error bars,
significance tests or population precision is implied.

SVG text is normalized for trailing whitespace in memory before its first write,
then parsed as XML before the runner hashes it. Frozen outputs are never edited.
PNG readability and independent source-to-plot values will be checked before
handoff. Scope is this package, its new run and runner-required registry entries.
The parent owns root/paper navigation, the article/E1a galleries and PROGRESS.

Original R2/R3 and all biological execution holds remain unchanged. No new
canonical RQ, scientific acceptance, push, PR creation or publication is included.

## Execution status

Prospective at plan creation. Results, figure links and validation will be added
after the committed rendering contract executes.
