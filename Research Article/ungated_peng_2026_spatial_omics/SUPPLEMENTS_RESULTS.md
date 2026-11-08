# Supplied Tables S1–S6: source qualification — 8 November 2026

**Current result:** six owner-supplied workbooks are qualified as published source
metadata and assay definitions. The successful [supplement v2 receipt](../../analysis/research/runs/Pg1_supplements_v2_20261108/receipt.json)
binds the [contract](contracts/supplements_v2.json), committed at `a46a835` before
execution. **42,530 independently implemented checks passed.** The previous
[GEO metadata result](RESULTS.md), its v3 receipt, all frozen outputs and earlier
unfavorable A11/A12/A13 evidence are unchanged.

Purpose: determine which source holds the newly supplied tables lift or narrow.
Immediate audited units are cells, published lists and reported sample groups;
patients remain biological units. We compare Table S1 against verified GEO
metadata and compare published lists against fixed A12 definitions. Source
identity, merged-cell propagation and false equivalence of lists/panels are the
principal validity threats. All source contents and previous outcomes were
exposed; this is not confirmation, expression analysis or scientific acceptance.

## Source access and auditable extraction

The files `NIHMS2118436-supplement-2.xlsx` through `-7.xlsx` are Tables S1–S6.
Each original and ignored local copy matches the owner-supplied SHA-256. Original
workbooks were opened without saving; formulas were not executed. The ledger
retains saved formulas, cached values, cell types, number formats and source
addresses. The prior download failures remain historical; receipt of local files
resolves table-content access without changing restricted Zenodo access.

| Artifact | What it preserves |
|---|---|
| [Source manifest](../../analysis/research/runs/Pg1_supplements_v2_20261108/source_manifest.json) | Supplied-source provenance, file hashes, URLs and intake timestamps |
| [9,585 source cells](../../analysis/research/runs/Pg1_supplements_v2_20261108/source_cells.csv) | Exact workbook/sheet/cell, raw saved values, formula and format metadata |
| [11-sheet manifest](../../analysis/research/runs/Pg1_supplements_v2_20261108/sheet_manifest.csv) | Dimensions, merged ranges, formula counts and date systems |

Source locators below refer to these supplied files, not a claim of a successful
new public download. Numbered tables and repository calculations are distinct
evidence. The full source-cell ledger also retains notes and blank distinctions
needed to interpret the extracted tables.

## S1: participation, clinical fields and remaining identities

Table S1 Tab 2 A31 defines the asterisk as two samples/tissue blocks. It never
creates a second independent patient. Reconstructed checkmark counts agree with
all published histology totals and the four saved total formulas.

| Platform | S1 reported total | GEO v3 records | What changed |
|---|---:|---:|---|
| Visium | 56 | 56 | Patient/histology participation reconciles |
| snRNA-seq | 75 | 75 | Patient/histology participation reconciles |
| WES | 79 | 54 | Gap localized to 24 Normal plus one AAH sample/block |
| Discovery Xenium 5K | 12 | No recovered GEO series | Participation recovered; no fabricated libraries or sections |

[All 500 participation cells](../../analysis/research/runs/Pg1_supplements_v2_20261108/platform_participation.csv)
retain blank/not-marked versus checked and doubled cells. [Aggregate arithmetic](../../analysis/research/runs/Pg1_supplements_v2_20261108/participation_totals.csv)
binds each result to the source range and reported total.

**WES:** Tab 2 AA17:AA22 reports Normal 24, AAH 11, AIS 14, MIA 4, LUAD 26,
total 79. GEO has 0, 10, 14, 4 and 26 respectively. The AAH gap is localized to
**P4**: E18 marks two blocks, while GEO has one WES record for that group. This
rules out the unsupported explanation that all 25 missing deposited records were
normal samples. It does not establish why files are absent, which unnamed block
is missing or how matched-normal controls were deposited.

**P6 and P7 holds remain.** S1 G18 marks P6 AAH, consistent with the GEO title and
explicit alias, but it has no VCF identifier to settle the `P6_AIS` filename
conflict for GSM9226083. H21 marks two P7 LUAD blocks; it does not recover the
original precursor diagnosis or specify which alias was reclassified.

**Discovery Xenium:** Tab 2 E25/L25/Y25 marks AAH participation for P4/P11/P24;
R26/T26/V26 marks AIS for P17/P19/P21, with their LUADs in row 28. These are six
patients and twelve reported tissues. The [participation-to-candidate table](../../analysis/research/runs/Pg1_supplements_v2_20261108/xenium_participation.csv)
retains both Visium AAH candidates for P4 and both AIS candidates for P21. Even a
single alias candidate does not prove the exact Xenium block or serial section.

**Clinical fields:** S1 Tab 1 A4:L28 provides 25 patient records, including stage,
tumor diameter and reported driver mutations. Blank driver fields remain blank,
not mutation-negative. Of 740 age/sex/smoking/ethnicity comparisons with the 185
GEO records, 726 agree under the declared sex/smoking label mapping. The 14 text
differences concern only P24/P25 ethnicity: `White or Caucasian` versus
`White/Caucasian`. They remain visible rather than harmonized. This is a wording
difference, not evidence of a biological mismatch or genotype-verified identity.
[Clinical extraction](../../analysis/research/runs/Pg1_supplements_v2_20261108/discovery_clinical.csv)
and [every comparison](../../analysis/research/runs/Pg1_supplements_v2_20261108/clinical_GEO_comparison.csv).

## S1: TMA structure is partly qualified

Tab 3 A5:S26 yields 22 aggregate group rows, **19 distinct `TMA P#` patient labels,
eight TMAs and four slides**. Expanding only the worksheet's actual merged ranges
preserves leading-zero slide IDs, Top/Bottom positions, shared patient rows and
unmerged blank mutation fields. Sums of group core counts and unique TMA totals
both equal **188**, agreeing with E27. F27 reports 19 patients. G27 reports 36
lesions, but that number is **not independently reconstructed** by interpreting
parenthetical numbers in lesion text.

`AAH (12)` and `MIA (35), AAH (14,16)` remain raw text. The table is not an
individual core-ID→lesion-ID→barcode map. TMA patient numbering remains distinct
from discovery; the paper's reported separate-cohort provenance is not a new
independence check. [Merged-source group table](../../analysis/research/runs/Pg1_supplements_v2_20261108/TMA_groups.csv)
and [core-count reconciliation](../../analysis/research/runs/Pg1_supplements_v2_20261108/TMA_totals.csv).

## S2–S4: measured-list definitions, not interchangeable endpoints

[All 36 namespaced lists](../../analysis/research/runs/Pg1_supplements_v2_20261108/gene_list_inventory.csv)
and [gene/Ensembl memberships with source cells](../../analysis/research/runs/Pg1_supplements_v2_20261108/gene_lists.csv)
retain exact symbols, trimming only surrounding whitespace. No synonym, ortholog
or missing-gene inference was used.

- **S2:** nine pan-lineage snRNA MPs, nine epithelial snRNA MPs and eleven Visium
  MPs. Pan-lineage MP6 and Visium MP1 each contain 49 nonempty entries; the other
  lists contain 50. No entry was invented. `MP6` has different meanings across
  these namespaces and is not automatically A11's frozen feature.
- **S3 human:** KAC 102 genes, NF-kB 21 and Interferon 136. **S3 mouse:** KAC 98
  and Inflammatory 199. A mouse inflammatory list is not a human endpoint;
  the human NF-kB list is not the existing A12 TNF/NFkB hallmark response.
- **S4 Tab 1:** two 100-gene custom add-ons, each with Ensembl IDs, for whole-tissue
  5K Prime and TMA lung assays. These are not verified complete base-plus-add-on
  panels or measured matrices. Tab 2 retains 150 published alveolar DEG rows.

**A12 component membership:** among its ten fixed targets, the whole-tissue
custom add-on lists **NFKBIA** (S4 Tab 1 A89); the TMA custom add-on lists
**IL1R1** (C29) and **NFKBIA** (C69). Every absent target is labelled
`not_listed_in_custom_addon`, never “unmeasured.” Coverage of the full assay
remains unknown. [All twenty component/add-on checks](../../analysis/research/runs/Pg1_supplements_v2_20261108/A12_addon_membership.csv).

Exact overlap with A12's already frozen response also matters for later state
qualification. Epithelial MP6, MP7 and MP9 share 2, 25 and 21 response genes;
human KAC, NF-kB and Interferon share 7, 4 and 10. The human NF-kB list includes
the A12 components IL1R1, MYD88, NFKBIA and TNFAIP3; its four response overlaps
are NFKB1, NFKBIA, RELA and TNFAIP3. [Complete human-list overlap inventory](../../analysis/research/runs/Pg1_supplements_v2_20261108/A12_published_list_overlaps.csv)
retains all lists and exact genes. This identifies potential feature sharing;
it does not prove which genes produced the unavailable author state labels or
establish circularity in a completed spatial analysis. No new score was computed.

## S5–S6: published summaries and one unresolved gene cell

[Published DEG extraction](../../analysis/research/runs/Pg1_supplements_v2_20261108/published_DEG_summaries.csv)
retains 1,327 S5 mouse DEG rows plus the 150 S4 human rows, with source values and
cell labels. These are published summaries, not raw cell or animal treatment
outcomes. **S5 Sheet1 A333** is numeric serial `45903` with `d-mmm` formatting,
displayed by the independent reader as 3 September 2025. Its gene symbol is left
blank and flagged unresolved; no gene name is guessed from that date. The cDC1
label and remaining published values are retained.

[S6 extraction](../../analysis/research/runs/Pg1_supplements_v2_20261108/seqIF_COMET_metadata.csv)
retains 20 antibody/run metadata rows, expanding actual merged cycle cells only.
It supplies seq-IF/COMET assay definitions, not measured longitudinal outcomes or
evidence that a protein-defined state predicts fate.

## Holds after source intake

| Hold at metadata v3 | Current disposition | Exact remaining input |
|---|---|---|
| Tables S1–S6 inaccessible | **Lifted** for these supplied files | None; originals and copies are hash-matched |
| WES 79 versus 54 unexplained | **Narrowed** to 24 Normal + one P4 AAH block | Deposit/exclusion/normal-control manifest and exact block/file mappings |
| Clinical and platform participation unavailable | **Lifted at reported patient/group level** | Lesion/block/section IDs and alias-specific selection still absent |
| Discovery Xenium participation unknown | **Narrowed** to named patients/histologies | P4/P21 selected blocks, exact section/slide/library IDs and cell objects |
| TMA structure unavailable | **Narrowed** to aggregate TMA/patient/core counts | Individual core/lesion IDs, barcode mapping, exclusions and qualified assay data |
| Program/signature/custom-add-on definitions unavailable | **Lifted for published lists** | Complete versioned base panels and actual measured gene axes; independent state qualification |
| P6 VCF/P7 original review unresolved | **Remain** | Specific source corrections/mapping, not another aggregate count |
| Barcode pathology/state, ROI polygons, registration and full cell inputs missing | **Remain** | Actual exports and image/coordinate frames for stage 3 |
| S5 gene at A333 | **New narrow source-quality hold** | Original gene symbol from the source; no date-to-symbol guess |

Thus stages 0–2 advance and stage 6 gains aggregate cohort qualification. Stage 3
alignment cannot run without actual annotations/geometry; stage 4 reproduction
and stage 5 A12 remain unestimated. Stage 6 endpoint transport still needs core
identities, measured panel coverage and its own contract. S5/S6 do not supply the
linked mature-output/withdrawal measurements for stage 7. No new global RQ,
functional experiment package or external validation claim is created.

The [revised missing-file request](MISSING_FILE_REQUEST.md) removes requests for
the now supplied tables and names the remaining files. It is **not sent**.

## Verification, preservation and delivery

The [v2 amendment](SUPPLEMENTS_AMENDMENT_V2.md) records the date-cell discrepancy
found by independent openpyxl parsing after v1's OOXML extraction. The
[failed-v1 archive](../../analysis/research/runs/Pg1_supplements_v2_20261108/failure_preservation.json)
retains every byte and the failed status. The original failed directory remains
local, unmodified. The [verification record](../../analysis/research/runs/Pg1_supplements_v2_20261108/verification.json)
checks raw cells, merges, formulas, participation arithmetic, clinical comparisons,
gene lists, A12 membership/overlaps, unresolved identifiers and archived bytes.
The independently implemented checks use the same supplied sources; this is not
independent biological replication. [Delivery checks](SUPPLEMENTS_VALIDATION.md).
