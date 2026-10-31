# X3–X5 source qualification and prospective design return

31 October 2026, Asia/Seoul. **No new external expression matrix was read.**
[Checkpoint A results](CHECKPOINT_A_RESULTS.md) · [Plan and authority](README.md) ·
[Fresh literature context](LITERATURE_CONTEXT.md).
The X0 [contract](config/x0_contract_v1.json),
[input hashes](../../../analysis/research/runs/Yd1_extension_x0_v1/input_inventory.json)
and [receipt](../../../analysis/research/runs/Yd1_extension_x0_v1/receipt.json)
own the metadata recovery below.

Existing October-31 literature searches are reused. This pass followed identified
primary sources to sample records, directory/file lists and author code. Additional
queries were `site:nature.com/articles/s41590-026-02671-8 "data availability"`,
`"GSE210341" "metadata" fibroblast`,
`site:nature.com/articles/s41590-026-02671-8 "available" "data"` and
`site:nature.com/articles/s41586-024-07660-1 "Code availability"`.
These searches did not resolve the missing source tables/state export; unrelated
search hits were not used as evidence. The publisher browser route failed and
direct HTTPS returned a 3,038-byte client challenge, not article content.
No author was contacted.

New cache: `raw_data/Yd1_extension_20261031`. The prior review-chat planning cache
was copied byte-for-byte and remains preserved. Retrieval receipts v1–v4 retain
URLs, UTC times, byte lengths, hashes, failures and final URLs. The first sandbox
DNS attempts failed; bounded permitted retrievals succeeded. GitHub connector
exports have their own provenance file and are hash-bound in X0. Public record
availability does not by itself establish permission for every possible reuse.

## X3 — Tsukui sample/time joins qualify; author state/QC export remains missing

Primary [GSE210341](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE210341),
[GSM6428697](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM6428697) and the
[official file list](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE210nnn/GSE210341/suppl/filelist.txt)
describe mesenchymal enrichment and twelve reported samples pooled into four
10x lanes. A lane or the sole GSM is not a biological replicate.
The previous CMO readme identifies three tags per time: 301–303 day 0, 304–306
day 7, 307–309 day 14, 310–312 day 21. It does not explicitly connect each CMO
number to a numbered CSV sample suffix.

X0 recovered **50,785 unique barcodes**, matched one-to-one and in order between
the small barcode and metadata files. Metadata columns are barcode, orig.ident,
nCount_RNA, nFeature_RNA, sample, Day and treatment. Twelve sample labels have
three per day; no author state label or demultiplex confidence field is present.
Each nominated gene (Il6, P2rx4, Col1a1, Acta2) has one entry in the 32,286-row
feature file. This verifies feature identity, not measured expression or detection.

[Full sample coverage](../../../analysis/research/runs/Yd1_extension_x0_v1/x3_sample_coverage.csv):
day 0 has 4,063/4,215/3,441 pre-filter barcodes;
day 7 has 2,329/3,852/4,685;
day 14 has 4,403/4,247/4,995;
day 21 has 4,976/4,915/4,664.
These counts are metadata occupancy, not eligible author-state counts or evidence
of independent mice. [Machine-readable qualification](../../../analysis/research/runs/Yd1_extension_x0_v1/x3_qualification.json)
retains the unresolved joins.

| Identified file | Exact listed compressed bytes | Current action |
| --- | ---: | --- |
| GSM6428697_metadata.csv.gz | 639,155 | Retrieved; metadata only |
| GSM6428697_barcodes.tsv.gz | 232,337 | Retrieved; join verified |
| GSM6428697_genes.tsv.gz | 210,326 | Retrieved; four feature identities verified |
| GSM6428697_matrix.mtx.gz | 541,249,302 | Not retrieved/read |
| GSM6428697_seurat_v4_obj.rds.gz | 1,553,376,346 | Not retrieved/read; source record describes filtered/merged/clustered Seurat v4 object |
| GSE210341_RAW.tar | 2,095,718,400 | Not retrieved; unnecessary bundle for a bounded subset |

The GSM processing record reports filtering below 200 or above 7,500 detected
genes and above 15% mitochondrial fraction, demultiplexing/multiplet removal,
DoubletFinder and merged embedding. The existing CSV is explicitly pre-filter.
Reimplementing only those numeric cutoffs would not recover the authors' exact
retained cells, doublets or states. An author barcode-to-retained/state export, or
a reviewed way to inspect the identified object, is required.

### One bounded conditional design for review, not execution

- **Question/purpose:** within author-defined alveolar, inflammatory and fibrotic
  fibroblast states, does the sample-level Il6 RNA description differ across
  observed injury times, separately from the captured proportions of those
  states? This is a shared-source description of a published transition setting.
- **Unit and support:** the twelve reported sample labels, three per time. Animal
  identity/independence remains unknown; retain sample descriptions and prohibit
  population tests. Do not pair suffixes across days or count lanes as units.
  Author state names and barcode mappings must match the proposed three states
  exactly before a numerical contract; unresolved names hold the design.
- **Population/exclusions:** author-retained singlets in the three nominated
  states; exclude other author states from this specified denominator and report
  their counts separately. Do not infer states from Il6/P2rx4, recluster, integrate,
  transfer labels or tune QC. Preserve a ledger of author exclusions, missing
  state labels, ambiguous demultiplexing and unmatched barcodes. Unresolved
  retained-cell joins prevent execution.
- **Endpoints:** Il6 primary; P2rx4, Col1a1 and Acta2 separate companions.
  Within sample/state, detection is nonzero raw counts divided by all retained
  cells in that sample/state. Abundance is mean log1p(raw target/all-gene cell
  total × 10,000), with target counts and total counts retained. Keep target-zero
  cells. Gene absence in the assay is unavailable, not zero expression.
- **Composition:** each state's count divided by all retained cells in the three
  nominated states for that sample; state absent means zero composition.
  Expression for a zero-cell state is undefined, not zero. This denominator
  concerns the selected captured mesenchymal states, not the whole lung.
- **Contrasts:** day 7 minus day 0 is primary; day 14 minus day 0 and day 21 minus
  day 0 are fixed companions, separately for each nominated state/gene/metric.
  Equal sample weights and all nine crossed sample differences per eligible
  contrast; no p-values or confidence intervals. Require a nonempty state in all
  three reported samples of both days for a complete group expression contrast.
  Otherwise show every existing sample summary and mark that contrast unavailable;
  never remove an empty sample to manufacture support. This support condition is
  not a power or minimum-cell precision claim.
- **State dependence:** show the same four-gene endpoints for the union of the
  three nominated states alongside the separated states and composition.
  The union is a dependent reporting sensitivity, not independent validation.
  It cannot recover a causal within-state effect if state membership itself
  changes with injury.
- **Exposure/limits:** Yadav/Tsukui published Il6 state/time patterns and new
  metadata counts are exposed; no local target expression has been extracted.
  Capture, enrichment, state selection, injury time and unknown preparations
  remain alternatives. RNA is not secretion, flux, lineage transition or repair.

**Current disposition:** source metadata qualification complete; numerical design
and acquisition remain held for review plus author state/QC mapping. The smallest
next acquisition is the barcode/state/retention export, not a whole-atlas bundle.
If unavailable, the reviewer must decide whether the identified 1.55 GB object
is justified solely to export metadata before considering the 541 MB matrix.
The previous Strunz whole-lung alternative was not downloaded or substituted.

## X4 — culture/native and disease-stage numerical work held

Primary preprint:
[Vanegas-Avendano et al., 10.64898/2026.04.08.717092](https://doi.org/10.64898/2026.04.08.717092),
cached PMC13081991 XML. New read scope: Results sections S9–S13, Fig. 6 and
associated culture captions, Methods S20–S23, especially S21 tissue FFPE and S22
fixed-cell profiling. **Both native and cultured assays are described as fixed-RNA
profiling**; this pass does not support calling the culture assay bulk RNA.
That narrows the planning uncertainty but does not establish assay equivalence
across FFPE tissue and fixed cultured cells.

[GSE331144](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE331144),
all nine GSM records and its
[official file list](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE331nnn/GSE331144/suppl/filelist.txt)
were inspected. They list one healthy parenchyma title, seven IPF upper-lobe titles
and one IPF lower-lobe title, with raw/normalized count text files. The
[exact accession/file map](../../../analysis/research/runs/Yd1_extension_x0_v1/x4_sample_map.csv)
preserves every record. Titles such as U197/L197 suggest a potential lobe link but
do not prove a donor join. Nine accessions do not establish nine independent donors.
A001 and U001 must likewise not be equated by numeric suffix.

The bundle is **88,135,680 bytes**; listed raw files range from 409,334 to
13,291,439 bytes. No count files were acquired. None of the listed titles/files
identifies P1/P6 culture or an isolation protocol. The sample processing prose
describes matrix/feature/barcode files while actual supplementary links are raw
and normalized text tables: their orientation, raw measurement semantics,
complete cell/state support and probe coverage remain unvalidated. Source assay
mentions Chromium Human Transcriptome Probe Set v1.0.1; nominated gene/probe
availability is not inferred from a transcriptome label.

**Hold for a culture/native or P1/P6 comparison:** obtain exact culture count and
barcode/state files, donor–lobe–protocol–passage–library joins, the native/culture
probe/reference/normalization correspondence, and all target-zero cells. The
paper's same-cohort language and culture-state findings cannot supply those joins.
Do not substitute a native-only IPF/control contrast for the requested culture
question. Effect margins, population precision and an eligible matched cohort
remain unspecified because the needed identities are absent.

Second preprint:
[Justet et al., 10.64898/2026.05.27.727792](https://doi.org/10.64898/2026.05.27.727792),
cached PMC13317612, version 1. Results describe 24 Florence cryobiopsies integrated
with five control and four end-stage IPF Leuven explants; the latter are linked
to GSE286182. Methods state that the associated cryobiopsy transcriptomes are
being deposited. GSE286182 is therefore not established as the entire early-IPF
study. Read scope includes tissue acquisition, Results/Fig. 1, Methods S12–S15
and the depositing statement. The earlier prose Fig. 4 versus stromal Fig. 5
caption discrepancy is preserved as a source-version issue.

**Stage-comparison hold:** need the early-cohort accession/file map, donor and
specimen identifiers, harmonized raw assays and author cell labels, plus a design
that explicitly handles site and cryobiopsy-versus-explant confounding. These are
cross-sectional specimens, not longitudinal stages from the same donors. No
progression or causal disease-stage comparison is currently qualified. Both
records remain preprints; this pass does not claim a peer-reviewed successor.

## X5 — human source/capture qualification and overlap hold

Primary [SCAHN article](https://doi.org/10.1038/s41590-026-02671-8) and
[author code](https://github.com/Khatri-Lab/SCAHN/tree/a767278972b09ce991d86fde53bb1332bb194c35).
Commit `a767278972b09ce991d86fde53bb1332bb194c35` was verified through the public
commit endpoint (28 October 2026); the metadata snapshot and selected file blobs
are hash-bound in X0. This pass inspected the complete returned repository path
listing, README, `01_load_data.R`, `make_tableS1.R`, and targeted capture/source
sections of `02_atlas.R`. It did not run the code or read expression objects.

The [dependency audit](../../../analysis/research/runs/Yd1_extension_x0_v1/x5_code_qualification.json)
shows the actual data dependencies absent from that public code tree:

- `data/samplemeta.csv`, `results/annotation/SCAHN.cellmeta.csv`,
  `SCAHN.subsetproportion.rds` and `data/cellnumber.rds`;
- the generated source table `results/tables/SCAHN.tableS1.csv`;
- the selected-gene integrated expression object used by figure scripts.

Code evidence:
[01_load_data.R](https://github.com/Khatri-Lab/SCAHN/blob/a767278972b09ce991d86fde53bb1332bb194c35/scripts/figures_post_acceptance/01_load_data.R)
joins cells by `sampleid.pid`, retains samples with at least 30 cells (lines
47–49), groups states and strips a/b/c/d publication-ID suffixes (line 55).
Neither a sample key nor a publication identifier establishes a donor.
[make_tableS1.R](https://github.com/Khatri-Lab/SCAHN/blob/a767278972b09ce991d86fde53bb1332bb194c35/scripts/analysis/make_tableS1.R)
summarizes that already-filtered table; it does not include the input data.
[02_atlas.R](https://github.com/Khatri-Lab/SCAHN/blob/a767278972b09ce991d86fde53bb1332bb194c35/scripts/figures_post_acceptance/02_atlas.R)
lines 890–1000 distinguish fresh whole blood, fresh/frozen PBMC and techniques.
These source/capture differences cannot be treated as biological ARG1/IL6R effects.
Integrated selected-gene values are not a substitute for original raw counts.

| Parent source | Existing repository relation | SCAHN overlap status |
| --- | --- | --- |
| Salcher NSCLC atlas, version 2022.10.20 | Reused in Yadav's human RNA comparison; exact Yadav-selected donors/filtering unjoined | Not resolved from available code; need source table and original IDs |
| Adams GSE136831 | Existing Ravel human IPF/control source; also contributes control material to Salcher | Potential reuse must be joined, not presumed independent or absent |
| Habermann GSE135893 | Existing Ravel human IPF/control source; also contributes control material to Salcher | Same unresolved overlap boundary |
| Newly selected healthy/noninfectious blood or lung cohort | No cohort selected for numerical extraction yet | Donor, assay, state and all-zero coverage unqualified |

The established Salcher→Adams/Habermann parent overlap comes from the prior
[context audit](../CONTEXT_AND_SYNTHESIS.md), backed by its primary sources.
This does **not** assert that SCAHN contains each parent. No accessible, complete
SCAHN source table or donor crosswalk was obtained; absence from the code tree
is not proof that these data are unavailable elsewhere. Publisher content access
was blocked, so the complete supplement was not claimed as read.

**Precise numerical hold:** obtain the original source table, sample/donor and
capture annotations, a bounded healthy/noninfectious cohort's raw counts with
complete cell metadata, ARG1/IL6R measurement coverage, and all target-zero cells.
Resolve source/donor overlap before selecting a cohort or contrast. Preserve
pre-normalized publication IDs and separately document the author >=30-cell
sample filter; do not silently adopt it or expression-positive selection.

The single intended return, once those prerequisites exist, is a **within-one-source
healthy fresh-whole-blood neutrophil description**: sample/donor detection fractions
and raw-count-normalized abundance for ARG1 and IL6R, stratified by author state,
with all qualifying target-zero cells in the denominator. Cohort identity, donor
support and capture protocol are currently unknown, so no executable numerical
design or sample size is asserted. A protocol comparison needs an appropriate
within-source design; pooled cross-study correlations will not answer it.
Human neutrophil RNA cannot establish a common lineage with the small mouse
LY6G/CD64/CD11C population, suppressive function, receptor activity or IPF repair.

## Decision returned

X3 offers the most concrete next metadata step and a bounded conditional numerical
proposal; it still requires state/QC qualification and review. X4 and X5 have
specific source/design holds. None was expanded to obtain a positive result.
X6 awaits checkpoint-A review and eligible evidence; Wg-P06's substrate-balance
alternatives and the separate epithelial-output bridge remain unchanged.
