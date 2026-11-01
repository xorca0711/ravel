# Arozamena source qualification and eligibility checkpoint

1 November 2026. **Arz1-P01, metadata only; scientific acceptance not assessed.**
All seven deposited multiome matrices are structurally qualified after the
documented v2 empty-record adapter. They share **31,950 RNA feature IDs and no
exact peak ID across all seven**. A narrower, accession-specific RNA description
is feasible for review. The original within-state/composition question, comparable
cross-condition accessibility, validated mouse-level inference and early-to-later
function linkage remain held for the specific evidence below.

This checkpoint measures source records, matrix structure and identifier coverage.
It computes no expression/accessibility contrast, state assignment, donor inference
or functional association. The principal validity threat is a mistaken biological
unit, processing-stage or feature join. Published outcomes and metadata are exposed;
the later endpoint specification must retain that exposure.

## Exact evidence and source coverage

- [V1 methods](METADATA_METHODS.md), [v1 contract](config/metadata_contract_v1.json)
  and [v1 receipt](../../analysis/research/runs/arz1_source_qualification_v1/receipt.json):
  frozen at `8673abad74022d8d8a90d43857f68698806ecb66`, completed with three
  component holds. All original code, inputs and outputs remain unchanged.
- [V2 amendment](config/METADATA_AMENDMENT_V2.md),
  [v2 contract](config/metadata_contract_v2.json) and
  [v2 receipt](../../analysis/research/runs/arz1_source_qualification_v2/receipt.json):
  frozen at `4028767b6d4b05e2eba6fa657480c9dd33465f3d`. V2 supersedes only the
  three MatrixMarket parser holds, reuses the four qualified HDF5 records and
  establishes seven-library identifier coverage. [Validation](VALIDATION.md).
- [Intake manifest](sources/intake_v1.json) binds **95 exact local files**, including
  request/extraction records and **21 processed inputs**. It gives every byte size
  and SHA256. Source bytes are preserved in ignored `raw_data/Arz1/`; they are not
  bundled into Git. Reproduction elsewhere requires these exact versions.
- [Series](../../analysis/research/runs/arz1_source_qualification_v1/series_records.csv),
  [44 sample records](../../analysis/research/runs/arz1_source_qualification_v1/sample_records.csv),
  [44 BioSample joins](../../analysis/research/runs/arz1_source_qualification_v1/biosample_crosswalk.csv),
  [deposited links](../../analysis/research/runs/arz1_source_qualification_v1/deposited_file_links.csv)
  and [article index](../../analysis/research/runs/arz1_source_qualification_v1/article_source_index.json)
  are repository metadata evidence, separate from the primary-source statements.

The primary source is [Arozamena et al.](https://doi.org/10.1038/s41467-026-79014-6),
*Inflammatory memory primes the intestine for enhanced regenerative potential*,
Nature Communications, version of record **27 October 2026**, PMID 42946733,
PMCID PMC13714302. Crossref, Europe PMC and full-text identifiers agree.
Acquisition date: **1 November 2026**. Read coverage was targeted source/design
qualification, not a new systematic literature or novelty assessment.

The [Europe PMC full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13714302/fullTextXML)
is 207,174 bytes, SHA256
`e5719b710fb47107d578e1824e30f3e482ac90c43ff919aa671fc6a973978395`.
Its [public supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13714302/supplementaryFiles)
is 13,490,763 bytes, SHA256
`8fcb91bd772ba0ec966e4a8ef631d08e61478a3efdda18ffe9b6718392340652`.
Four exact XML-linked members were extracted with provenance: Supplementary
Information (MOESM1, 21 pages), Reporting Summary (MOESM2, 4 pages), transparent
peer review (MOESM3, 41 pages), and source data workbook (MOESM4). All member hashes
are in the manifest. Reporting Summary p3 and peer-review p30 were also rendered
and visually inspected; source workbook extraction covers text cells only.

Six public GEO SOFT records and supplementary-directory listings were read through
the [NCBI GEO FTP service](https://ftp.ncbi.nlm.nih.gov/geo/series/). The SOFT URL
pattern is `/geo/series/{GSE-prefix}nnn/{GSE}/soft/{GSE}_family.soft.gz`.
All 44 linked BioSamples were retrieved through public NCBI EFetch. Their exact
GEO relations match, but these accessions identify submissions, not animals.

Access failures were resolved for source reading: the direct Nature web open
redirected to identity authorization; its ordinary PDF request returned HTML
(3,038 bytes, preserved as the misleadingly named `article.pdf`); the publisher
supplement CDN had a DNS resolution failure; the PMC OA-package manifest returned
404. Europe PMC public XML/archive requests succeeded. No content-policy refusal,
credential challenge bypass or private-data access occurred. These failed routes
do not establish missing source data.

## Biological units and unresolved source contradictions

The article's **Methods Sec22** reports 9 control, 6 Lgr5-condition and 6
Krt20-condition intestines. **Sec26** reports three mice pooled per condition/run,
three runs, and downstream integrated pooled cellular profiles.
It explicitly distinguishes them from independent mouse-level replicates. This
supports a reported pooled design, but the inspected deposits do not establish a
mouse-to-preparation-to-library crosswalk or certify that pools use distinct mice.
An independent preparation could be a valid unit if that provenance is recovered;
unknown mouse identities alone do not make a fixed-library description impossible.

Sec26 describes inferred 21-donor assignments and a donor-annotated Seurat object.
Results **Sec5** uses donor-like groupings and consistency language. Supplementary
Information **p11, Fig. 6 caption** describes donor-resolved comparisons; this is
an author statement, not external identity validation. In transparent peer review
**p30**, the authors report no remaining material for independent SNP/genotype
validation and qualify Souporcell-based agreement as supportive consistency/QC.
Reporting Summary **p3** gives a generic biological-replication statement that
does not resolve the assay-specific pooling. Thus neither inferred donors,
BioSample IDs nor recurring barcode strings certify independent animals.

Two source disagreements must remain visible:

1. Sec26 calls Multiome 1 Control/Krt20 and Multiome 2 Control/Lgr5. GEO labels
   **GSE302685 multiome1/Lgr5** and **GSE302687 multiome2/Krt20**. Use accession
   and deposited condition; do not silently reconcile article run numbering.
2. Sec22 describes tdTomato-negative controls and positive post-injury lineage
   cells; GSE302685 describes positive sorting in both conditions, while Sec26
   describes pooled positive cells generically. GSE329778 additionally labels
   CTRL as wild type and the lineage groups with reporter genotypes. History,
   lineage selection, sorting and genotype therefore remain entangled. A later
   matching state label would not remove these design differences.

Inspection covered all six SOFT/listing sets, linked BioSamples, seven processed
matrix schemas, article external links/data availability, four supplements and
266 extracted workbook text cells. **No deposited barcode-to-author-state map,
donor assignment/confidence table, validated mouse/pool crosswalk or downstream
integrated Seurat object was located in that coverage.** The inspected HDF5
datasets contain counts, sparse indices, features and barcodes only. MatrixMarket
triples provide the corresponding axes. Article external repository links point
to nf-core pipelines, not a study-specific annotation object. This is a bounded
search result, not a claim that no such object exists anywhere or with the authors.

## Qualified matrices and separate cohorts

[V2 inventory](../../analysis/research/runs/arz1_source_qualification_v2/matrix_inventory.csv)
and [feature types](../../analysis/research/runs/arz1_source_qualification_v2/feature_types.csv)
are authoritative. Counts below are deposited barcodes/features, not cells passing
the paper's complete joint QC or validated biological replicates.

| Accession / deposited condition | Source lineage context | Barcodes | RNA features | Peak features |
|---|---|---:|---:|---:|
| GSE302685 control | Lgr5-associated cohort | 6,942 | 32,285 | 141,432 |
| GSE302685 irradiated | Lgr5-associated, reported 21-day history | 8,405 | 32,285 | 125,314 |
| GSE302687 control | Krt20-associated cohort | 9,897 | 32,285 | 96,085 |
| GSE302687 irradiated | Krt20-associated, reported 21-day history | 10,362 | 32,285 | 124,136 |
| GSE329778 CTRL | Separate three-condition deposit | 5,164 | 33,696 | 126,248 |
| GSE329778 KRT20 | Separate three-condition deposit | 7,896 | 33,696 | 112,768 |
| GSE329778 LGR5 | Separate three-condition deposit | 6,921 | 33,696 | 76,427 |

All stored entries passed finite, nonnegative integer checks. Coordinates are
unique under verified strict sparse order. Every deposited barcode has positive
RNA and peak entries in the same matrix column; this is count-level modality
pairing. Cross-library barcode overlap is whitelist reuse, not a cell/animal join.
The three GSE329778 feature files each contain one empty line per valid six-field
record. V1 held those empty records; v2 explicitly counts/skips them while retaining
all nonempty records and original source bytes. No modality label was guessed.

The four HDF5 RNA ID sets agree; the three MatrixMarket RNA ID sets agree; their
intersection is [31,950 stable IDs](../../analysis/research/runs/arz1_source_qualification_v2/common_feature_ids.csv).
All seven peak sets differ. Exact peak intersections are **73** for the GSE302685
pair, **47** for GSE302687, **37** for GSE329778 CTRL/KRT20 and **21** for its
CTRL/LGR5 pair; the seven-way peak intersection is empty. IDs use the same
`chr:start-end` syntax in inspected examples, so a separator change does not
explain this result. [All pairwise overlaps](../../analysis/research/runs/arz1_source_qualification_v2/feature_overlap.csv).

Sec26 reports a later unified consensus peak set and compatible mm10/GRCm38
assembly nomenclature. The deposited processed matrices are not that demonstrated
common-count matrix. Distinct processing stages could explain this; metadata alone
does not establish an error in the paper. Neither zero-filling absent peaks nor
merging overlapping intervals reconstructs fragment counts on a common basis.
The tiny exact intersections do not represent general accessibility concordance.

| Other accession | Verified deposited coverage | Interpretation limit |
|---|---|---|
| GSE302684 bulk ATAC | 9 sample records, three title-level replicates per CTRL/IRR/TREAT; three condition-merged bigWigs linked | No sample-level peak/count matrix located; merged tracks cannot recover biological variation or epithelial states |
| GSE329965 immune scRNA | CD45 immune libraries CTRL/7DPI/21DPI; 17,299 x 1,531, 18,170 x 1,371 and 17,239 x 1,186 gene-by-barcode tables; barcode lists match in order | Separate immune cohort, not the epithelial multiome state map; integer nonnegative counts do not establish animal units |
| GSE329696 bulk RNA | Counts and TPM each 45,706 genes x 18 libraries, three titles each for baseline, 7DPI, 21DPI, 3 months, control-organoid P3 and irradiated-organoid P3 | Salmon counts contain fractional estimates; retain them. Group/replicate labels do not establish longitudinal matching or independent preparations |

The [dense inventory](../../analysis/research/runs/arz1_source_qualification_v1/dense_table_inventory.json)
retains exact column names and ID fingerprints. The source workbook has Figure
1/2/4/6/7 and Extended Data Figure 1/6 sheets. For example, Figure 2 A1/A27/A34
identify panels and B3/L3 label first/second irradiation; they do not identify a
GEO library, animal or preparation. No such functional join was located in the
text-cell extraction. Numeric workbook values were not analyzed.

## Eligibility and concrete next comparison for review

| Job | Current disposition | Exact prerequisite for broader work |
|---|---|---|
| Q0 source | Completed within documented public coverage | A new object/location can extend coverage; direct publisher route failures are not active blockers |
| Q1 units/assays | Accession/condition and same-column modalities qualified; pooled design is author-reported | Verified mouse/preparation/pool IDs, distinctness and accession/run/sorting reconciliation for stronger unit/design claims |
| Q2 metadata | Seven matrices and five dense tables structurally checked; v1 holds retained and narrowly superseded | Exact author replay needs author QC-retained barcodes, annotations and downstream object/version |
| Q3 within-state/composition | Original estimand held; narrower whole-library RNA description is feasible | Source barcode-state map with provenance, or a separately reviewed operational annotation design; marker scores cannot be relabelled as cell identity |
| Q4 cross-condition RNA/accessibility | Held despite within-library modality pairing | A common re-counted peak matrix or sufficient fragments plus a reviewed common-feature counting design; qualified state map for within-state claims and explicit peak-gene mapping for gene-linked comparisons |
| Q5 sensitivity | Eligible only around the narrower RNA description after a reviewed freeze | Fixed contrasts, denominator, zero-depth handling, RNA-only QC definitions and bounded sensitivity family; no outcome-driven filters or cell-based population inference |
| Q6 early-to-later function | Held | Actual animal/preparation join connecting early molecular assay to a named later measured endpoint, timing and cohort correspondence; shared group names/replicate numbers are insufficient |

**Recommended adapted RNA estimand, not an execution authorization:** use the
31,950 shared gene IDs and retain four separate deposited contrasts:
GSE302685 irradiated minus its control (Lgr5-associated), GSE302687 irradiated
minus its control (Krt20-associated), and GSE329778 LGR5 minus CTRL and KRT20 minus
CTRL. The latter two reuse one control. Do not average unmatched controls or treat
the four contrasts as independent replication. The observational unit is each
deposited library; barcode summaries describe its finite sampled material.

For gene g, library l and shared universe G, a concrete candidate endpoint is
the UMI-weighted share `P(l,g) = sum_c x(l,g,c) / sum_c sum_h_in_G x(l,h,c)`.
Report accession-specific differences in `1e6 * P`, alongside an equal-barcode
summary `E(l,g) = mean_c [x(l,g,c) / sum_h_in_G x(l,h,c)]` for positive-depth
barcodes. The parent brief must freeze denominators, zero-depth handling, eligible
barcodes and whether all shared genes or an exactly sourced program is reported.
Undefined ratios should remain undefined, not receive an unreviewed pseudocount.

P versus E tests sensitivity to barcode depth weighting, not composition versus
within-state causation. A bounded RNA-only QC sensitivity could use the source
Sec26 RNA thresholds, after fixing gene detection/count definitions and a verified
mitochondrial annotation. It must be labelled an adaptation because the author's
full QC also requires ATAC/fragment metrics. No filtering has been applied here.
Report cohort-specific concordant, discordant and null patterns without selecting
favorable genes or claiming population significance. Selection, composition,
genotype/history and processing remain plausible explanations even for agreement.

**Q4 reopening is constrained by actual deposits.** GSE329778 links CTRL/KRT20/LGR5
fragments (402,473,208 / 512,718,078 / 793,731,383 compressed bytes). These were
not downloaded or validated. The GSE302685/302687 inspected supplements expose
only their HDF5 matrices, not fragments. No common re-counted peak matrix was
located. A third-deposit-only common-feature analysis would be a separately
reviewed adaptation; it would not reconstruct all three runs or the author's
state-resolved analysis. No raw-read reprocessing or coordinate remapping is
proposed just to force eligibility.

## Resources, preservation and handoff

The four HDF5 files total about 219 MB; the three compressed MatrixMarket matrices
about 195 MB, plus small feature/barcode files. Existing Python 3.12.10, NumPy
2.5.1 and h5py 3.16.0 from `.tools/sx22_e1a_runtime` sufficed. No package install,
dense multiome materialization or raw-read download was needed. Source-time memory
was 16,758,542,336 bytes total / 1,172,365,312 available; C free space decreased
from 5,479,817,216 to 5,056,577,536 bytes after acquisition. These are snapshots,
not a guarantee that later integration will fit.

Deferred GSE329778 RAW tar is 1,911,848,960 bytes. Bulk ATAC listing sizes are
approximately 1.2G/1.0G/862M; exact bigWig bytes were not retrieved. Those large
objects are not needed to decide current metadata eligibility. No external
account setting blocks this checkpoint.

Next: originating source/numerical review, then a source-supported RNA brief and
separate committed contract if accepted. No biological endpoint may run on this
metadata authorization. The originating reviewer owns README, literature context,
navigation, PROGRESS and PR #157 integration; this technical branch owns the new
source evidence, reports, contracts, scripts and runs. Prior Saxton evidence,
governance, root attributes and scientific acceptance/claim grades are preserved.
