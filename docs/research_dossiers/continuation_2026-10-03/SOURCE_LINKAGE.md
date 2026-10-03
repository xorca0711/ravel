# New source qualification: Rochelle deposits

3 October 2026. Owner A8; A19 shares the feasibility question. Decision: whether
new source identities and acquisition/endpoint joins qualify a fixed early RNA
component → independent later mature outcome, or receptor withdrawal plus
retained reserve. Strongest rival: donor labels combine different preparations
or assays. Biological units remain donor/preparation, not GSM records.

The [source article](https://www.jci.org/articles/view/188701) names these two
accessions. Browser-tool access to GEO failed, but the official SOFT archives
were retrievable. The [frozen metadata contract](../../../analysis/research/contracts/A8.rochelle_metadata_v1.json)
was committed at `78845fc` before execution. Previously read article/workbook
labels and SOFT-header exposure are explicitly recorded.

| Source | Retrieved source SHA-256 | Directly recovered |
|---|---|---|
| [GSE306194 family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE306nnn/GSE306194/soft/GSE306194_family.soft.gz) | `e9a609c407d2940d11f03e701eab6cdc82365e27dcd66f5cdd98e9311ba4de83` | Nine GSM records; Donor1/Donor2/Donor3 each have UC, P0 and P2 labels |
| [GSE306714 family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE306nnn/GSE306714/soft/GSE306714_family.soft.gz) | `721f6bdb2f5d5b278e90e38b6869db69ff921e2bc9748a7a048faa4cef057c32` | Three GSM records; titles combine D7V/R0G codes with multiple scaffold/region labels; no explicit `individual` characteristic |

See the [verbatim sample table](../../../analysis/research/runs/a8_rochelle_metadata_v1/samples.csv),
[multi-valued characteristics](../../../analysis/research/runs/a8_rochelle_metadata_v1/samples.json)
and [verified receipt](../../../analysis/research/runs/a8_rochelle_metadata_v1/receipt.json).
A separately written regex parser reproduced all 12 accession/title/individual/group
rows directly from the two saved sources. Repeated donors were not counted as
independent preparations and title tokens were not converted into new samples.

## What this qualifies and what it does not

GSE306194 now has a direct accession → reported donor label → culture-stage
map. This resolves more than accession identity alone. It does not identify the
same cells across destructive samples or join those preparations to an independent
mature/function assay. UC/P0/P2 are source group labels, not invented elapsed times.

GSE306714 has useful scaffold/region/donor-code content in titles. Preserve the
literal `L1041` and `L1043` forms where suffixes differ; do not silently repair
them into guessed aliquot IDs. Do not equate three GSM records with three donors,
or connect Donor1/2/3 to D7V/R0G without an explicit alias map.

Read-only SOFT inspection lists one combined filtered feature/barcode H5 per
series and `NONE` for sample-level supplementary files. Matrix contents and raw
reads were not inspected. This is a limit of inspected metadata, not a claim
that no other source could supply a barcode or aliquot mapping.

The existing [support-workbook review](../packages_2026-10-03/SOURCES.md#rochelle-supporting-data-inspection)
already identified donor-labelled later measurements. The required bridge is
still explicit: barcode/library → donor alias → cell bank/preparation/scaffold
→ assay and acquisition time → independently measured endpoint, with pooling,
splits and reused donors retained. For A19, specified receptor input/cessation,
pre-withdrawal state and responsive reserve also remain absent from this join.

**Disposition:** retain both as informative candidate sources; do not run an
A8 prediction or A19 receptor/reserve test from donor-name matching. No expression
matrix, effect size or biological model was fitted. A separate descriptive
culture-stage question would need a distinct purpose and contract; it would not
close these outcome-linkage questions.

The older MesSTIM, A5, CEBPA/AP-1 and Nb3 source-map holds are unchanged.
No exhausted public-identity search or author outreach was repeated.
