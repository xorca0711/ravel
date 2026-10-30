# Methods and input assessment: independently decidable DY1 jobs

30 October 2026, Asia/Seoul. Article-local DY1-P01. This assessment starts from
reviewed integration `22125b2333e93ea666123299e86536b06f632c5e`; freshly fetched
main remains `78320a186b6f52426e7c7c5349a2f26492b718b7`. The scoped worktree was
clean before its fast-forward. Its branch has no configured upstream.

## Full context and present purpose

The Damani-Yokota 2026 study concerns type-2 immune history in lung macrophages,
including N. brasiliensis history and later influenza A virus (IAV) challenge:
separate baseline host bulk RNA and ATAC measurements, baseline and later
infectious-challenge scRNA measurements, proposed STAT6–EGR2–PPARγ/RXRA
associations, ARG1 contribution, and human disease context. The baseline samples
are part of this history-dependent study; calling their file audit neutral does
not remove that context. The [original stages](../../docs/research_reviews/2026-10-29-nam-memory/README.md)
remain the source of the broader questions, not a record that they all executed.

This pass identifies available measurements, missing identities and the limits
of each proposed inference. It performs source reading, filesystem inventory and
small header checks only. It fits no biological contrast, assigns no cell to an
animal, models no infection response, and ranks no mechanistic intervention.
A previous broad execution restriction is evidence of that execution's status;
it does not establish that every independently defined mouse-file QC task is
prohibited. Conversely, a data repair would not by itself clear a different
infection-response or intervention task.

The biological unit remains unknown for the original mouse data. A library or
tag is an observed data identifier; an independently collected pool can be a unit
only when its identity and overlap are established. Pool constituents, cells,
exon bins and peaks do not create independent replicates. The present structural
assessment has files/rows as technical units and no population-effect estimand.
Missing individual mouse names alone does not rule out pool-level inference:
distinct, independently collected pools can be valid units. The present unresolved
issue is the source-specific library/tag→pool identity and assurance of independent
collection/overlap, not a universal requirement to name every constituent mouse.
The reviewer rechecked the supplied paper's RNA Methods: material from12–15control
or trained mice was pooled for RNA-seq, and libraries were subsequently pooled for
sequencing; Fig4reports n=3–4/group. Extended Data8c describes each biological
replicate as a pool of3–6animals. These are published pooling premises, not a
crosswalk proving that each deposited library/tag is a distinct nonoverlapping
independently collected pool. No animal count is converted into an effective n.

## Evidence actually available

Current authority is the [source-v2 correction](SOURCE_V2_RESULTS.md), read before
the [v1 qualification](../../analysis/research/runs/DY1_source_v1/source_qualification.json).
V2 corrects the naive-label parsing issue and replaces v1's categorical
condition/library-confounding statement with **unresolved**. Its
[18 reference rows](../../analysis/research/runs/DY1_source_v2/reference_labels.tsv),
[feature inventory](../../analysis/research/runs/DY1_source_v2/feature_tags.tsv)
and [membership checks](../../analysis/research/runs/DY1_source_v2/reference_presence.tsv)
show record-local labels and feature presence, not assigned cells or animal IDs.

| Material | Available evidence | What it measures or does not establish |
|---|---|---|
| Six bulk RNA files, GSM9964554–559 | Deposited `ExonCounts.txt.gz` files; three source-labeled trained and three untrained libraries. V1 records 406,850 Ensembl exon-bin rows plus five count-summary rows per file, 47,911 gene prefixes. | Exon-bin counts. The first identifier has form `ENSMUSG…:001`; summing bins is not yet justified as unique gene-level fragment counting. |
| Eight ATAC files, GSM8591248–255 | Eight compressed narrowPeak files, four source-labeled naive and four trained libraries; cached source records describe replaced July2026 files. | Called intervals and score/signal fields. No deposited common-region read-count matrix was identified in the inspected supplementary records. Peak presence/signal is not read depth or a differential-accessibility count model. |
| Two baseline scRNA triplets | GSM9964560/count1 and GSM9964561/count2 matrix/feature/barcode files in the preserved execution cache. | Header spot checks match V1:32,291features×22,282barcodes/44,168,578entries and32,291×19,629/23,814,921, respectively. These are dimensions, not verified biological units or cell-state labels. |
| Two later-challenge triplets | Listed in the preserved cache and previously inventoried by V1; not reread numerically in this pass. | Availability does not authorize a response model; no new challenge count processing is proposed here. |
| CMO references and feature tables | Four references; both baseline feature tables contain the six CMO301–306 features. Each table has32,285Gene Expression and six Antibody Capture rows. | A tag reference is not a tag→animal/pool crosswalk. Tag presence cannot prove meaningful assigned cells in a library. |
| Source metadata |22GSM records in the [sample map](../../analysis/research/runs/DY1_source_v1/sample_map.tsv), cached GEO records, two BioSample records and an SRA record. | Source-record labels are known. The inspected bulk/baseline BioSample attribute names contain no animal/pool identifier. This is bounded negative evidence, not proof that no author crosswalk exists anywhere. |
| Annotation/preparation | Cached mm10 RefGene and literature records, original retrieval/access manifests. | File presence is not validated annotation compatibility, a qualified regulatory target set or successful author-code access. |
| Human analyses | Completed [78-donor primary run](HUMAN_RESULTS.md) and [21-donor external description](HUMAN_EXTERNAL_RESULTS.md), receipts and independent checks. | Exposed donor-level RNA/composition context; no exact author NAM reclustering, functional enzyme endpoint or causal recipient effect. |

The unused mouse inputs are preserved under
`C:/Users/dream/.codex/worktrees/nam-memory-execution-20261029/ravel/raw_data/nam_memory_2026/`.
The current worktree initially holds only the20source-v2 metadata inputs in its
corresponding folder, not those mouse count/peak matrices. Human inputs have their
separate existing caches. No original input was moved, deleted or overwritten.
The [retrieval manifest](../../analysis/research/runs/DY1_source_v1/retrieval_manifest.json)
records original URLs, sizes, dates and hashes; this assessment did not repeat
downloads or claim a new public-access check.

Header inspection confirmed two fields in one exon-count file, ten fields in one
narrowPeak record and integer-coordinate MatrixMarket headers in the two baseline
matrices. These small checks are not a full new integrity audit. V1's dimensions
and feature counts remain cited historical measurements, not recomputed results.

## Job-by-job disposition

“Data” denotes absent/ambiguous source evidence; “inference” denotes a claim the
available measurements/design cannot identify; “runtime/scope” denotes current
execution availability or the explicit task boundary. These causes can coexist.
No missing field is filled by assuming a more favorable design.

| Original stage and independent job | Present input / completed evidence | Exact remaining requirement or limit | Current disposition |
|---|---|---|---|
|0a. Accession/version/file provenance |22sample records, V1 retrieval hashes, V2 label correction | Current cached-byte agreement can be checked; replaced ATAC files need their own provenance, not inferred equivalence to the article pipeline | Neutral provenance QC supported; historical source reading complete |
|0b. Biological-unit and overlap map | Library titles, CMO references, limited BioSample/SRA metadata | Explicit tag/library→animal or independently collected pool map and overlap assurance; constituent lists only if needed to assess sharing, plus processing/batch/age information. Main/extended Methods pooling statements need source-specific reconciliation | Data hold for independent-unit inference; absence of individual names alone is not disqualifying |
|0c. CMO feature/label recovery | V2 already verifies labels and feature membership | Cell assignment and biological-unit identity are different missing objects | Completed label audit; do not repeat it or invent identities |
|1a. Exon-file structural/count-format audit | Six existing two-column exon-count files | Full row-universe, duplicate-ID, integer/nonnegative, zero-feature and summary-category checks | Cleared neutral metadata job; new frozen version required before execution |
|1b. RNA quantification semantics | Cached metadata says STAR/HT-seq/mm10; opaque exon-bin IDs available | Exact counting feature definition/mode, strandedness/pair treatment, annotation provenance and whether a fragment can contribute to multiple bins; article model's actual gene-count input | Data/measurement hold for exact gene-level reproduction; a format pass cannot resolve it |
|1c. Baseline RNA effect/PCA/model | Source-labeled three-versus-three libraries; no mouse biological run | Fit-specific count interpretation, valid units, confounder support and explicit scope assessment; a numeric design matrix can have rank without biological independence | Not executed or included in present metadata contract; not labeled categorically impossible because it is mouse data |
|1d. Peak-file structural QC | Eight ten-field called-peak files | Coordinate/field/duplicate integrity and per-file descriptive width/signal-field summaries | Cleared neutral metadata job; no group comparison or selected locus |
|1e. ATAC read-level QC and differential reproduction | Called peaks; source/article pipeline disagreement | Read/fragment or appropriate common-region count evidence, depth/complexity and enrichment information, actual replacement-file pipeline, excluded naive-library identity and documented rationale | Data hold for count-model/read-level reproduction. No peak-score substitution or data-driven outlier guessing |
|2a. Cross-assay identifier/annotation compatibility | Exon IDs, interval coordinates, declared mm10, cached annotation | Exact compatible gene/feature definitions and annotation versions; RNA/ATAC sample pairing is not established | Neutral schema/annotation assessment possible; not a paired biological correlation |
|2b. Direction/magnitude or discordance estimates | No qualified new mouse effect tables | Eligible assay-specific effects/uncertainty and a declared peak→gene association rule; unmatched bulk samples remain unmatched | Dependent data/inference hold; nonsignificant RNA would not establish unchanged RNA or regulatory poising |
|3a. Baseline sparse-file integrity | Two available baseline triplets, previously recorded dimensions | Full dimension/barcode/feature/index checks and technical count accounting, separately from condition assignment | Feasible neutral candidate after current QC; not executed in this assessment |
|3b. Tag assignment and NAM/state definition | CMO count features exist; author labels/crosswalk absent | Assignment evidence, tag→biological-unit crosswalk, population definition independent of tested outcomes, condition/library support | Count processing alone cannot resolve the identity hold; no demultiplexing or state fitting now |
|3c. Composition/within-state RNA separation | No qualified unit-level state table | Verified units, valid labels, denominator and common-state coverage; post-history conditioning changes interpretation | Data/inference hold; scRNA cannot supply within-state ATAC for separate bulk samples |
|4a. Literature/measurement-boundary review | Completed [primary literature context](LITERATURE_CONTEXT.md) and source Methods comparison | Newly used external binding/target resources would need exact source/context qualification | Existing qualitative review reusable; no target-set calculation needed for structural QC |
|4b. Observational regulatory association | Baseline effect inputs/annotation not qualified; late RNA/ATAC are separate measurements | RNA is not TF activity or binding; external occupancy does not establish occupancy here; no temporal relay is observed by a late snapshot | Data/inference-gated observational job, not categorically equated with intervention prioritization |
|4c. Mechanistic intervention prioritization | No qualified causal regulatory chain | Distinct scope and functional-evidence requirements | Outside this execution; no target/intervention ranking generated |
|5a. Later-condition design identifiability | Four nominal source conditions, V2 local labels | Actual condition-by-library cell support plus biological units/batches; a single later endpoint does not identify response kinetics | Qualitative identifiability review only; labels do not prove confounding or identify its absence |
|5b. History-by-infectious-challenge response modeling/prediction | Challenge triplets exist, but identities remain unresolved | Both data/design qualification and a separate safety/scope decision would be required | Not executed or queued; not reconstructed through another job or chat |
|6a. Captured-human ARG1 description | Completed primary/external human runs | Sparse RNA and absent neutrophil annotation limit source attribution; no enzyme/metabolite measurement | Completed within stated limits; no rerun needed |
|6b. Mouse Arg1 state/accessibility attribution | Original mouse count/peak data, no qualified state/effect result | Same unit/count/annotation dependencies as stages1–3; no deposited perturbation-omics panel identified | Not executed; no selected Arg1 analysis in neutral QC |
|6c. Functional-effect/mediation interpretation | Published comparison reviewed; omics and functional cohorts unlinked | Trained genotype contrast and training-specific interaction are different estimands; missing comparator limits the latter. Unlinked cohorts cannot identify mediation | Qualitative limitation review complete; no intervention design/priority or mediation fit |
|7a. Human donor, annotation and RNA context | Primary78donors and external12IPF/9Control, exact primary clinical joins, declared sensitivities | Same-source exposure, annotation sensitivity and incomplete clinical measurement remain | Completed supported work; no new cohort search or repeated fit warranted by this assessment |
|7b. Exact NAM/model/full marker/recipient claims | Public labels and bounded nine-gene external result | Author reclustering/model unavailable; external SELENOP exact mapping unresolved; specified within-group donor minima not met for some comparisons | Specific data/inference holds retained; no threshold relaxation or alias assumption |
|8a. Integrate completed evidence and limits | Source qualification, human results, negative/sparse findings and six RQ context notes | Preserve unresolved earlier jobs and existing endpoint authorities | Supported documentation; no scientific acceptance or new RQ implied |
|8b. Select a mechanistic intervention or assert readiness | No completed original mechanistic chain or new functional endpoint | Distinct scope/safety review and fit-for-purpose biological evidence; runtime completion would not supply these | Not executed or prioritized in this task |

## Why CMO counts cannot repair source identity by themselves

Observed tag counts could support a barcode-to-tag assignment under an explicit
method. They cannot tell whether the tagged material came from one animal, a pool,
overlapping pools or a technical split. Reused tag names are record-local, not
cross-library animal keys. Even perfect assignments would not resolve the
main/extended Methods pooling discrepancy or establish RNA–ATAC/functional-cohort
pairing. Counts may eventually inform condition/library support, but that is not
the missing biological identity crosswalk. No assignment thresholds, inferred
animal labels or infection-response outputs are generated here.

## Cleared neutral QC and its stopping boundary

The proposed next versioned metadata run covers only six exon-count files and
eight narrowPeak files. Its endpoints are file/row integrity, count-format
consistency and per-file technical summaries. It will recover exact cached
inputs by immutable copies or read-only use, bind their hashes, retain every
file, and independently check aggregate arithmetic. Exon-bin totals remain
exon-bin totals; peak signal fields remain signal fields. Missing raw reads,
counting semantics, biological units and author exclusions will stay unresolved
even if all structural checks pass.
For narrowPeak, “basic format” means only the listed field, interval-ordering,
summit/strand and finite/nonnegative numeric checks. Chromosome-size/build
concordance, full BED conformance, score integer0..1000 convention, read depth and
FRiP are not checked or inferred.

There will be no disease/history group test, effect-size estimate, clustering,
selected Stat6/Arg1 locus, enrichment, susceptibility/tolerance prediction,
pathogen parameter or intervention ranking. Structural verification reports
whether deposited files are parsable and internally consistent; it does not
identify a host target for pathogen manipulation or immune evasion and does not
reconstruct the held biological comparisons. The full study context above stays
with the contract and result. Any later job requires its own stated purpose,
inputs, unit/endpoint and applicable scope assessment rather than inheriting
permission from a successful file audit.

Python/numpy/pandas/scipy are available in the existing environment; anndata and
scanpy are absent there, and Rscript was not found on the inspected PATH. The
reviewer identified an existing portable executable at
`X:/GitHub/ravel/analysis/corrections/statistics/.tools/R-portable/app/bin/Rscript.exe`.
The neutral text-file audit does not need R or the missing Python packages.
Executable presence does not establish the required R package versions or repair
scientific limitations. No runtime installation, source download, external-service
write or governance change occurred in this pass.
