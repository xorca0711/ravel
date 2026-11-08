# Peng source qualification results — 8 November 2026

**Pg1-P01 completed the bounded source ledger, metadata joins and accessible
annotation inventory. Region-level reproduction and the A12 extension remain
unestimated.** The successful [v3 receipt](../../analysis/research/runs/Pg1_metadata_v3_20261108/receipt.json)
binds the [contract](contracts/metadata_v3.json), code, inputs and immutable outputs.
The specification was committed at `84d156e` before execution. Execution and source
qualification do not constitute human scientific acceptance.

The question was whether author sample/annotation definitions support faithful
spatial reproduction. Audited units were deposited metadata records; patients
are the intended biological units. We compared explicit GEO library aliases and
patient/demographic fields across platforms and against C3 inventories. The main
threat was a plausible false specimen match. All inputs and earlier outcomes were
exposed. No expression matrix, biological model or author plotting script ran.

## Confirmed metadata and its limits

| Deposited platform | Records | Author patient labels | Interpretation |
|---|---:|---:|---|
| GSE307534 Visium | 56 | 25 | 11 AAH, 14 AIS, 4 MIA, 26 LUAD, one Normal-labelled section |
| GSE308103 snRNA-seq | 75 | 23 | 24 Normal, 9 AAH, 14 AIS, 4 MIA, 24 LUAD libraries |
| GSE307529 WES | 54 | 25 | 10 AAH, 14 AIS, 4 MIA, 26 LUAD deposited labels; one VCF identity hold |

The [185-row sample table](../../analysis/research/runs/Pg1_metadata_v3_20261108/samples.csv)
preserves titles, explicit aliases, parsed fields, suffixes and unknown IDs
separately. `histology_deposited` is current GEO tissue metadata, not spot pathology
or a recovered original diagnosis. No Xenium record was invented.

| Platform pair | Shared exact author aliases | First-only / second-only | Patient-label overlap |
|---|---:|---:|---:|
| Visium / snRNA | 52 | 4 / 23 | 23 |
| Visium / WES | 54 | 2 / 0 | 25 |
| snRNA / WES | 50 | 25 / 4 | 23 |

These are **alias correspondences**, not confirmed lesion or serial-section
matches. The WES pairs include the explicitly flagged P6 file-identity hold.
[Crosswalk including unmatched aliases](../../analysis/research/runs/Pg1_metadata_v3_20261108/crosswalk.csv)
and [patient memberships](../../analysis/research/runs/Pg1_metadata_v3_20261108/patients.csv)
retain the distinct levels. All 25 deposited patient labels have internally
consistent age/sex/smoking/ethnicity across their available platforms; this is
neither genotype verification nor independent replication. The 23 RNA patients
are P3–P25; P1/P2 explain the four Visium-only aliases. Relative to Visium, WES
lacks `P4_AAH` and `P4_Normal` while retaining `P4_AAH-1`.

The audit compared 651 existing C3 inventory rows on applicable fields, with no
disagreement. [Exact comparison rows](../../analysis/research/runs/Pg1_metadata_v3_20261108/prior_inventory_comparison.csv).
This reuses existing evidence; it is not another cohort or biological replication.

## Discrepancies that remain visible

- **WES GSM9226083:** author title/description identify `P6_AAH`; the linked file
  is `GSM9226083_P6_AIS.WES.PASS.recode.vcf.gz`. Both strings remain. The VCF's
  histology and file-level specimen identity are held, and the two affected
  cross-platform correspondences carry that hold. The correct assignment is unknown.
- Five snRNA filenames omit a hyphen present in the explicit author alias:
  GSM9237905 (`P4_Normal-1`), GSM9237907 (`P4_AAH-1`), GSM9237917 (`P7_LUAD-1`),
  GSM9237960 (`P21_AIS-1`) and GSM9237968 (`P23_AIS-1`). The URL belongs to its
  GSM, but filename strings are not silently normalized or used as join keys.
- **P7:** both deposited lesion aliases already say LUAD. The paper describes a
  precursor-to-LUAD revision at case level; it does not identify the original
  diagnosis and revised-library mapping in the recovered sources. Those fields
  remain unknown. This is unresolved historical provenance, not an observed
  current-GEO contradiction.
- **WES denominator:** the paper's STAR Methods reports 79 sequenced samples,
  versus 54 deposited GSM/VCF records. The deposit has no Normal-labelled WES
  records. A difference of 25 does not identify the missing files or establish
  that every omitted record is a matched normal. Table S1/author clarification is needed.

[Issue ledger](../../analysis/research/runs/Pg1_metadata_v3_20261108/join_issues.csv).
Primary locators: [GEO GSM9226083](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9226083),
and [Peng author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC12980502/),
opening Results cohort description, Histopathological processing of tissues and
Whole-exome sequencing. Repository calculations above are distinct evidence.

## Source/annotation availability and stage decisions

The source ledger hash-checks retrieved files against their saved acquisition
receipts. A materially different publisher-page route was attempted using the
[PubMed-confirmed PII](https://pubmed.ncbi.nlm.nih.gov/41202811/); after an initial sandbox DNS failure, the network-enabled
request returned HTTP 403. Prior PMC/EuropePMC failures were reused. Restricted
Zenodo access was not bypassed. [URLs, timestamps, hashes and failures](../../analysis/research/runs/Pg1_metadata_v3_20261108/source_manifest.json).

The existing archive inventory covers 728 Visium members, including two coordinate
and two PNG references per section. Its candidate-pathology table remains empty.
This bounded inventory is not proof that authors lack annotations. Prior C3
barcode/coordinate QC is reused; no image alignment or polygon QC was performed
without the actual exports. [Annotation availability/QC](../../analysis/research/runs/Pg1_metadata_v3_20261108/annotation_availability.csv).

The public [Figure 5 code](https://api.github.com/repos/FuduanPeng/LungPCA_Code/git/blobs/fc1fb907dddd5a84969b490982b470542d6e17a1)
was retrieved through the GitHub connector at blob
`fc1fb907dddd5a84969b490982b470542d6e17a1`. Figure 1/5 code references eleven missing
processed objects; Figs. 5F/I/L rely on Xenium Explorer. These scripts plot inputs,
not a recovered upstream annotation pipeline. [Object names and exact lines](../../analysis/research/runs/Pg1_metadata_v3_20261108/author_required_objects.csv).

| PLAN stage | Outcome | Exact next input or decision |
|---|---|---|
| 0 source ledger | Complete for inspected sources | New source/version only if it resolves a named gap |
| 1 sample joins | Complete at metadata/alias levels | Table S1 and block/lesion/section manifest; P6/P7 clarifications |
| 2 pathology/ROI recovery | Published rules and accessible inventory complete; exports unrecovered | Author barcode labels, ROI geometry, panels and approved processed objects |
| 3 alignment/QC | Held | Same-section IDs, images, coordinate frame/units, transforms and polygon/barcode exports |
| 4 source reproduction | Held | Qualified author labels and full neighborhood inputs, then its own prospective contract |
| 5 A12 within-state context | Unestimated | Qualified state/pathology/source labels, independently specified measured endpoint and gene coverage, patient nesting, then an exposed A12 contract |
| 6 TMA transport | Held | Cohort/core→lesion→patient map and measured panel; qualify the actual endpoint before any validation contract |
| 7 functional bridge | Not executed | Linked longitudinal mature output/withdrawal measurements and feasible model; existing A1/A8/A14 ownership remains |

The [annotation/join schema](QUALIFICATION_SCHEMA.md) and
[precise missing-file request](MISSING_FILE_REQUEST.md) are ready for review.
The request has **not been sent**. There is no warranted additional whole-section
score or imputed-panel calculation that would resolve these missing inputs.
Multimodal integration is deferred because no qualified cross-platform spatial
objects are available. No paid compute or NGS workflow was needed.

## Failure preservation and verification

V1 failed an assumed filename/alias equality; [v2 amendment](AMENDMENT_V2.md)
made the five snRNA differences explicit. V2 then exposed the WES histology
conflict; [v3 amendment](AMENDMENT_V3.md) requires the narrow file hold. Neither
failed attempt is relabelled successful. V3 contains byte-identical
[v1](../../analysis/research/runs/Pg1_metadata_v3_20261108/failure_preservation.json)
and [v2](../../analysis/research/runs/Pg1_metadata_v3_20261108/failure_v2_preservation.json)
archives, including failed receipts, partial outputs and logs. Original local
directories remain unmodified and are ignored only after archive verification.

Five focused parser tests passed. A separately implemented verifier used raw
SOFT block extraction, CSV/set arithmetic and file hashes without importing the
production parser: **3,961 checks passed**, covering counts, explicit aliases,
suffixes, demographic fields, all join/missing-counterpart cardinalities, C3
coverage, unknown identities, six discrepancies, the P6 hold and both archives.
[Verification record](../../analysis/research/runs/Pg1_metadata_v3_20261108/verification.json).
The runner receipt's generic `verification: pending` field is not rewritten;
the separate hash-bound verification output records the completed checks.

Repository checks and refreshed-base delivery validation are recorded in
[VALIDATION.md](VALIDATION.md). Existing A11/A12/A13 unfavorable results, global
question identities, claims and frozen evidence remain unchanged.
