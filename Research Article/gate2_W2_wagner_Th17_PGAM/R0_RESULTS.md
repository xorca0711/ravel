# Wp-R0 result: what the three deposits actually contain

Executed 4 October 2026 under the governed runner. Contract
[config/source_qualification_v1.json](config/source_qualification_v1.json),
receipt [analysis/research/runs/wp_source_qualification_v1/receipt.json](../../analysis/research/runs/wp_source_qualification_v1/receipt.json),
outputs in the same run directory. `verify` returned no errors; a successful
receipt records execution, not scientific validity.

This is **metadata recovery**. No expression value was read, nothing is compared
to a published figure, and nothing here supports population inference.

## Single cell, GSE289733

| Quantity | Value |
|---|---|
| Sample records | 8 |
| Animal labels | `Mo1`, `Mo2` |
| Condition combinations | Th17n and Th17p × 1 mM and 25 mM glucose |
| Per-sample supplementary matrices | 0 |
| Barcodes in the deposited aggregated matrix | 19,203, all unique |
| Aggregation suffixes | 8 (`-1` … `-8`), with 2,890 / 2,676 / 2,147 / 2,583 / 1,595 / 2,502 / 2,077 / 2,733 barcodes |
| Features | 31,053, all `Gene Expression` |
| Suffix-to-GSM mapping | **not stated in the deposit** |

The suffix count matches the declared library count, which is the necessary
condition for Wp-R1 to open — but the deposit never says which suffix is which
library, and there are no per-sample matrices to settle it. Condition labels must
therefore be re-derived, and the GEO sample order is a prior to be tested, not a
fact to be applied. The matrix is also the pre-QC aggregate: 19,203 barcodes
against the 5,192 cells the paper analysed, so the analysed set and its
exclusions are not recoverable from this file.

## Bulk, GSE290297

| Quantity | Value |
|---|---|
| Sample records | 79 |
| Matrix columns | 79, joining one-to-one with **0** unmatched in either direction |
| Gene rows | 20,465 |
| Value scale | TPM as deposited; no estimated or raw counts |
| Animal or culture field | **absent** |
| Design | 16 cells of cell type × {DMSO, EGCG, Methanol, DHEA} × {Div.1, Total}, five libraries each, except Th17p/DMSO/Div.1 with four |

The join is clean, so Wp-R3 can open descriptively. Two constraints come with
it: the library is the only verifiable unit, because no animal field exists; and
the values are TPM, so the analysis method must be valid for continuous
normalised data rather than counts.

## Human reuse, GSE138266

| Quantity | Value |
|---|---|
| Sample records | 22 |
| Donor codes recovered from sample titles | 12 — 6 multiple sclerosis, 6 idiopathic intracranial hypertension |
| Donors with both CSF and blood | 10 |
| Donor characteristic field | **absent**; identity comes from titles |

This is the only donor-level unit available anywhere in the paper, which is why
Wp-R4 is worth running despite transporting an exposed signature. It also
contradicts the published description of a five-versus-five design; the
discrepancy is recorded in [Datasets](DATASETS.md#human-reuse-cohort) and the
population is defined from the deposit.

## Stage eligibility decided by this run

| Stage | Status | Binding reason |
|---|---|---|
| Wp-R1 single cell | eligible, descriptive only | suffix-to-GSM order undeclared; labels must be derived; 2 animals, one per condition cell |
| Wp-R2 Compass | blocked, external | no solver licence; the published run's imputed input and fitted model are not deposited |
| Wp-R3 bulk | eligible, descriptive only | clean join, but TPM-only and no animal field |
| Wp-R4 human | eligible, descriptive only | donor unit exists; CD4 identity, pseudobulk rule and covariates must be re-derived or stay unknown |
| Wp-R5 assays | blocked, no deposit | no numerical values for flow cytometry, 13C tracing, Legendplex, EAE or histology |

## Independent verification

Every endpoint above was recomputed in the session by a second route — pandas
readers for the barcode, feature and TPM headers, and a regex pass over the SOFT
blocks for the design and donor counts — and compared to the run's
`results.json`. Twelve comparisons were made (barcode total, unique barcodes,
feature count, the eight per-suffix counts as a set, bulk sample records, TPM
column count, the column-to-title set equality, the 16-cell design table, gene
rows, human sample records, donor codes and paired donors) and **all agreed**.
This is numerical verification of the inventory, not biological replication.

## What this run does not establish

It does not reproduce any published panel, does not establish independent
biological replication, and does not show that any eligible stage will agree with
the paper. An `eligible_descriptive` status means a stage may open at descriptive
level; it is not a statement that its result would license population inference.
The missing supplementary tables mean every later signature is a reconstruction
with declared substitutions, as set out in
[Reproduction scope](REPRODUCTION_SCOPE.md#wp-r1-single-cell-reconstruction).
