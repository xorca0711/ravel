# TN0 intake: completed with explicit source and coverage limits

**2 October 2026.** The owner completed the paper and requested this N3 folder.
Repository/roadmap and neighboring-workspace review, private context-note
reading, original PDF inspection, web supplement retrieval and bounded source
tabulation are complete. No expression reanalysis was performed.

## Evidence delivered

- [Source manifest](../config/source_manifest.json): 32 hash-verified files,
  including the original annotated PDF, private note snapshots, public source
  workbooks, author code and metadata. Payloads stay in ignored storage.
- [Workbook schema](../runs/intake_v1/supplement_schema.json): 12 workbooks
  covering all nine supplementary tables and three figure-source tables.
- [Human coverage](../runs/intake_v1/human_celltype_coverage.tsv): 348 rows,
  58 populations x three donors x two assays, retaining missing-source markers.
- [Library design](../runs/intake_v1/library_design.tsv): source sampling
  entries, including entries that must be excluded or resolved before atlas use.
- [Coverage gates](../runs/intake_v1/source_coverage_gates.tsv): declared
  10/20/30/50-cell thresholds, assay-specific donor counts, and explicit limits.
- [Run record](../runs/intake_v1/run_record.json): environment, input count,
  code/config hashes and output hashes. Original executed code is preserved.

## Source arithmetic is unresolved

| Quantity | Deposited/published | Independently summed from 58 population rows |
|---|---:|---:|
| Total cells | Table 2 final total / paper: 75,066 | 75,071 |
| SS2 cells | Paper: 9,404 | 9,409 |
| 10x cells | Paper: 65,662 | 65,662 |
| Patient 1 SS2 | Table 2 final donor row: 4,352 | 3,987 |

Each of the 58 population row totals agrees with its numeric donor/assay
entries. However, the six donor/assay values printed in the table's final
row sum to **75,436**, which agrees with neither its printed total nor the
58-population sum. Blank/dash entries remain nonnumeric source absences; they
are not recoded as observed zeros. These are source arithmetic findings, not
proof of which cells are erroneous or of an error in the underlying matrices.
[Reconciliation JSON](../runs/intake_v1/table2_reconciliation.json) and
[row checks](../runs/intake_v1/table2_row_checks.tsv) preserve the evidence.

Do not force source metadata to 75,066 by dropping five cells or repair the
Patient 1 value silently. Reconcile exact release, labels and cell membership
first. Synapse documents corrected FACS metadata/count objects, but that note
alone does not establish the cause of these Table 2 discrepancies.

## Coverage changes the analysis order

At the proposed 20-cell-per-arm floor, AT2-s versus AT2 has **one eligible 10x
donor (P3)** and **two SS2 donors (P1, P3)** in Table 2. Neither meets the
three-donor floor. At 30/50 cells, the SS2 contrast retains only P1. Combining
assays does not increase independent donors. This is enough to hold a broad
AT2-s population comparison while preserving donor-specific source displays.

Alveolar versus adventitial fibroblasts has three 10x donors at 20 cells and
two SS2 donors. The 10x result is only a count-floor pass; region, sorting,
raw-count and label checks remain pending. At 50 cells even its 10x count gate
falls to two donors. These floors do not establish statistical power.

## Reader and source-version cautions

All 34 Table 7 worksheets advertise dimensions of 1 x 1. Resetting dimensions
reveals their data; the recorded actual shapes prevent a false empty-table
conclusion. Table 4 includes `Cluster 15 (SS)` and Table 9's sheet is `Table_S8`:
infer neither assay nor table number solely from a sheet suffix.

Table 5 supplies a `significant_means` sheet, not full permutation p-values.
Publisher caption inequalities for Tables 5/7 conflict with ordinary significance
wording; original code and unfiltered outputs must settle executable thresholds.
The pinned notebooks and current Synapse correction notice remain distinct
versions of evidence.

## Next decision

Recover versioned cell metadata from Synapse, identify the corrected FACS
release, build an audited donor/assay/region crosswalk and run TN1. Select an
expression object only after that audit. First source-reproduction targets are
the bounded AT2/stromal panels and MYRF/TBX5 specificity, subject to coverage.
The pipeline does not claim human AT2-s stemness, functional signaling,
lineage conversion or repair.
