# Saved metadata/QC evidence index

31 October 2026. This index covers the existing **R1 technical evidence**, not a
biological reproduction gallery. No new measured plot, densitometry, digitization,
response program or functional figure was generated. Tables are directly readable
and avoid implying biological comparisons that were never executed.

| Evidence item | Frozen source | What can be read / caption limit |
|---|---|---|
| Sample identity map | [samples.csv](../../analysis/research/runs/sx22_r1_v2/samples.csv) | Six library records joined to GEO/BioSample and source treatment; biological n is source-reported. `paired=no` means no pairing established/used, not verified unpaired animals |
| Library QC | [library_qc.csv](../../analysis/research/runs/sx22_r1_v2/library_qc.csv) | Total counts, detected gene rows and largest-ten fraction per library; these are technical summaries with no group effect or interval. Exact values and independent review appear in [R1_REVIEW](R1_REVIEW.md) |
| Identifier / zero-row QC | [gene_qc.csv](../../analysis/research/runs/sx22_r1_v2/gene_qc.csv) | Every deposited gene retained, with symbol multiplicity and all-library zero flag; no collapse or exclusion |
| Frozen diagnostic summary | [summary.json](../../analysis/research/runs/sx22_r1_v2/summary.json) | 35,275 rows; six libraries; 52 repeated nonempty symbol labels, not 52 gene rows; 12,935 all-zero rows |
| Execution provenance | [receipt.json](../../analysis/research/runs/sx22_r1_v2/receipt.json), [environment](../../analysis/research/runs/sx22_r1_v2/environment.txt), [stdout](../../analysis/research/runs/sx22_r1_v2/stdout.log), [stderr](../../analysis/research/runs/sx22_r1_v2/stderr.log) | Original immutable execution facts; later verification is in the separate review, not rewritten receipt fields |

The [source-panel correction](SOURCE_CORRECTION_2026-10-31.md) provides exact
PDF/figure locators and render provenance for the literature audit. Temporary
page images are review aids from the supplied hash-verified PDF, not new repository
figures or reconstructed data. R2/R3 and numerical R4/R5/E1/E2 have no result figures
to index; their dispositions are in the [completion ledger](COMPLETION_LEDGER.md).
A future measured rendering would need frozen source tables and the repository's
rendering provenance; none is asserted for this documentation-only index.
