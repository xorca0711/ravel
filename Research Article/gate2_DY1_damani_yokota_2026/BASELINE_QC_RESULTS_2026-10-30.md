# Baseline source-file and sample-profile diagnostics

30 October 2026. DY1-P01. Full context remains N. brasiliensis-associated immune
history and later IAV challenge in the Damani-Yokota study. These independently
scoped jobs inspect baseline host files and a fixed technical transformation;
they do not estimate a history effect, model infection response or prioritize an
intervention. The [job/input assessment](METHODS_AND_INPUT_ASSESSMENT_2026-10-30.md)
separates their permitted scope from missing data and interpretation limits.

## Six exon files and eight called-peak files

The metadata audit executed from freeze `fb29cd3`, after reviewer clearance and
four synthetic tests. All 14 copied inputs matched the original source-v1 SHA-256
records. The original cache remains intact. An independent dataframe calculation
verified 205 structural/arithmetic checks against the streaming parser.

All six exon files contain the same 406,850 non-summary feature IDs in the same
order, plus five count-summary rows. No malformed field count, non-integer or
negative count, or duplicate ID was found. Exactly 143,437 features are zero across
all six files; 263,413 remain for the separately specified profile diagnostic.

| Source library | Sum of non-summary exon-bin hits | Zero exon-bin rows |
|---|---:|---:|
| GSM9964554 |31,295,678|194,817|
| GSM9964555 |64,399,149|181,466|
| GSM9964556 |21,706,241|216,956|
| GSM9964557 |38,107,948|195,225|
| GSM9964558 |35,089,078|187,481|
| GSM9964559 |53,657,342|203,113|

These are **exon-bin hit sums**, not certified unique gene/fragment totals. The
five source count-summary categories remain separately reported and do not enter
the feature denominator. No history-group statistic is computed from this table.

All eight peak files pass the listed basic field, finite/nonnegative numeric,
interval-ordering, summit-offset and strand checks. Each retains all its rows;
none has a duplicate interval or a missing signal/p/q field under the declared
sentinel rules. Per-file interval counts and widths remain technical summaries:

| Source library | Called intervals | Median width, bases |
|---|---:|---:|
| GSM8591248 |94,475|338|
| GSM8591249 |106,940|341|
| GSM8591250 |66,471|317|
| GSM8591251 |95,518|323|
| GSM8591252 |110,803|343|
| GSM8591253 |106,579|341|
| GSM8591254 |113,282|341|
| GSM8591255 |120,195|342|

“Basic format” does not mean chromosome-size/build concordance, full BED
conformance, score integer 0..1000 conformance, read depth, complexity or FRiP.
Signal fields are not consensus-region read counts. These checks resolve none
of the source/article processing disagreement, omitted common-region count
matrix or unidentified author-excluded library. No library was excluded and no
selected regulatory locus was inspected.

[Receipt](../../analysis/research/runs/DY1_baseline_file_qc_v1/receipt.json) ·
[Exon audit](../../analysis/research/runs/DY1_baseline_file_qc_v1/exon_files.tsv) ·
[Count-summary categories](../../analysis/research/runs/DY1_baseline_file_qc_v1/exon_summary_categories.tsv) ·
[Peak audit](../../analysis/research/runs/DY1_baseline_file_qc_v1/peak_files.tsv) ·
[Independent verification](../../analysis/research/runs/DY1_baseline_file_qc_v1/verification.json).

## Fixed six-library exon-hit profile

After count-format eligibility passed, the separate descriptive contract froze
at `d7f0f82`. It retains all six source libraries and all non-summary features
except the fixed 143,437 all-zero rows. Each retained bin uses
`log2(1 + 1e6 × bin count / all non-summary exon-bin hits)`; features are centered
across all six libraries before a full deterministic SVD. No variable-gene,
condition-based or low-count filter was introduced. No source library was removed.

The first five components account for 31.256%, 24.491%, 20.357%, 12.986% and 10.909%
of variance in this fixed transformed matrix; the sixth is at numerical zero.
These fractions describe the chosen transformation. The source labels shown in
the figure are metadata, not independently verified animal/pool groups, and the
geometry does not establish a biological history effect or an outlier decision.

![Fixed exon-bin profile diagnostic](../../analysis/research/runs/DY1_baseline_exon_profile_v1/sample_profile.png)

The author's Methods describe low-overall-count filtering whose exact rule was
not recovered, DESeq2 v1.48.2 variance-stabilizing transformation and `plotPCA`.
This exon-hit logCPM/full-SVD diagnostic is an explicitly different adaptation;
it is not the author's gene-level PCA reproduction. STAR/mm10 and HTSeq v0.6.0
method labels do not resolve the exact exon-count feature/mode or establish
unique-fragment counting. No named-gene loading, target rank or group test is
exported. The plot was visually checked for legibility.

Three synthetic tests cover all-zero-only filtering/full denominators,
library-scaling behavior and invalid/constant-profile stops. The actual run
independently checks covariance eigenvalues, full-coordinate Gram reconstruction,
feature centering and source/feature/denominator agreement. Those are numerical
checks on the same files, not biological replication or acceptance.

[Receipt](../../analysis/research/runs/DY1_baseline_exon_profile_v1/receipt.json) ·
[All sample coordinates](../../analysis/research/runs/DY1_baseline_exon_profile_v1/sample_coordinates.tsv) ·
[Full variance table](../../analysis/research/runs/DY1_baseline_exon_profile_v1/variance.tsv) ·
[Verification](../../analysis/research/runs/DY1_baseline_exon_profile_v1/verification.json).

## Baseline sparse integrity and CMO signal inventory

The separate baseline-only audit executed from freeze `edc5e60`. It read all
67,983,499 stored entries once, covering the two baseline triplets only. Both
matrices match their feature/barcode dimensions, have unique library-local
barcodes and feature keys, contain positive supported integer values within
coordinate bounds, and match the declared stored-entry totals. Each has 32,285
Gene Expression rows and six Antibody Capture rows.

| Matrix | Barcodes | Stored entries | Gene Expression count sum | Antibody Capture count sum |
|---|---:|---:|---:|---:|
| GSM9964560 / count1 |22,282|44,168,578|119,080,679|30,139,070|
| GSM9964561 / count2 |19,629|23,814,921|49,482,766|36,794,898|

The CMO inventory retains all six exact source feature IDs per matrix. Every
row has some nonzero signal; none is an all-zero unused feature. No duplicate
stored tag coordinates were found. Raw totals sum stored entries, positive
barcode counts use unique coordinates, and maxima refer to stored entries,
not thresholded assignments or a maximum aggregated per-cell signal. Repeated
Gene Expression coordinates were not audited. These limits are recorded rather
than silently treating all stored entries as unique matrix positions.

Nonzero or large tag signals do not prove meaningful assigned conditions,
mixed-condition libraries, independent pools or an animal identity. The observed
inventory adds technical evidence beyond feature presence, but does not resolve
the source-v2 condition/library uncertainty. No assignment threshold, ranking,
cell-to-condition crosswalk or biological subset was generated. The later IAV
challenge matrices were not processed by this job.

Five synthetic tests cover type accounting, coordinate/value guards, declared
entry mismatch, barcode duplication and duplicate-tag semantics. The actual run
passed 152 aggregate checks: numpy masks/integer sums versus pandas groupby,
and tag-barcode Boolean occupancy versus sets. These share one parser and the
same input files; they are independent arithmetic checks, not independent
biological replication or a second source.

[Receipt](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/receipt.json) ·
[Library integrity](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/libraries.tsv) ·
[Feature-type accounting](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/feature_type_accounting.tsv) ·
[Complete CMO inventory](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/cmo_signal_inventory.tsv) ·
[Verification and its limits](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/verification.json).

## Consequence for later jobs

The completed checks qualify a file format and a technical profile, not the
original biological estimands. Distinct independently collected pools can be
valid units without individual mouse names; the unresolved item is the exact
library/tag→pool map and independence/overlap assurance. Reused CMO labels and
observed counts do not manufacture that relationship. The source-specific unit,
gene-count semantics, author-model, ATAC count/pipeline and cross-assay-linkage
holds remain distinct. A successful QC run does not authorize another task or
supply missing causal, activity, enzyme-output or recipient evidence.

## Validation and preservation

All 12 targeted synthetic tests passed (four structural, five sparse, three
profile), as did 161 repository tests with one skip. Compilation, the claim
contract, Nb1/Nb4/A16/A23 and A22–A23 evidence verifiers, 11,535 repository
validation checks, and the research gate passed against freshly fetched main
`78320a186b6f52426e7c7c5349a2f26492b718b7`. These checks verify the recorded
artifacts and repository requirements, not scientific acceptance.

An initial test invocation encountered a sandbox temporary-directory permission
failure; the approved execution passed. No analysis run failed in these three
jobs. All original inputs, earlier frozen code/contracts/outputs, and historical
failure records remain preserved. No governance, validator, root ignore rule or
canonical RQ changed. No biological analysis was rerun for this final report.

The exact next step is review-branch integration of this stable execution
handoff. No additional numerical job is queued. Reopening an effect job requires
its stated source/design evidence and a prospective versioned contract. Author
code access remains unverified after the recorded 29 October access failure;
no external settings or services were changed.
