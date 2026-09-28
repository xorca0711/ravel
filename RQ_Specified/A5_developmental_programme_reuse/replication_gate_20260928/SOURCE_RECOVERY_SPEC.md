# A5 external replication source-recovery specification

Frozen for source recovery on 2026-09-28, before new sample/state coverage counts
or expression scoring. This is a metadata gate, not an amendment to A5.

## Bounded source recovery

Start from deposited/source-author metadata for GSE303646 and the previously
recorded GSE202325 candidate. GSE202325 is an infection cohort and is outside this
non-pathogen recovery pass: use accession, title and the existing broad-label
verdict only; do not pursue infection protocols or analyse its expression data.
If necessary, inspect one source-led sterile-injury alternative only when a primary
paper/repository explicitly offers the required states and recoverable units.
Use cached records first. Record the exact URL, retrieval time, response outcome,
file hash, and fields recovered. Do not contact authors or download broad matrices
before sufficient cell/mouse/state metadata exists.

## Immutable A5 instrument and decision rules

The existing PLAN.md, config/strunz_test_contract.json and
 tables/external_test_modules.json are authoritative. Preserve the 99/57/53
Guo-derived lists exactly, exact mouse symbols, no alias repair, and the original
500-UMI expected detection instrument. Primary contrast is author-defined
transitional Krt8-positive ADI-equivalent cells minus author-defined activated AT2
within the same independently identified mouse, day 2 through day 21 inclusive.
Broad AT2 is not the primary comparator. Do not infer activation from injury alone.

Require at least 70% gene-list assay coverage; raw nonnegative integer UMI counts
and exact barcode matching; at least 30 cells per arm after raw library depth >=
500 UMI; and at least three independent paired mice across the fixed time window
(not three at every day). No floor, window, reference, module or depth retuning.
Retain the two-sided one-sample paired-difference t test, 95% interval, alpha 0.05,
equal-mouse estimand, three-member Holm secondary family, and planned descriptive
controls/heterogeneity checks. No cross-study pooled test or new classifier.

## Sequential gates

1. Scope/independence: mouse adult sterile injury, fixed day window; document new
   versus reused animals/cells and any discovery exposure. A new accession, study
   title, sample name, GEM lane, well or sequencing sublibrary alone is not proof
   of an independent mouse.
2. Mouse identity: explicit author/deposit evidence links each cell barcode to a
   biological mouse and describes pooling/splitting. Technical splits collapse to
   mouse; undemultiplexed pools cannot be counted as mice. Preserve unresolved
   identity instead of manufacturing replicate labels.
3. Population identity: downloadable author barcode labels or an author-provided
   cluster crosswalk, independent of the tested Guo programme, establishes both
   transitional and activated AT2 states. Record source labels, author evidence
   for correspondence, labelling method and any overlap with programme selection.
   Do not relabel broad AT2, unknown cells, or clusters using the target gene set.
4. Count provenance: deposited matrix is deduplicated raw UMI counts; corrected,
   log-transformed, size-factor normalized or read-count-only data are not a
   substitute. Match unique barcodes and gene universe to labels exactly.
5. Coverage and eligibility: only after gates 1-4 are sufficiently documented,
   count metadata arms, then raw-depth-eligible cells, and exact fixed-module
   assay coverage. Report every exclusion and unknown separately from failure.
6. Execution: if feasibility passes, freeze a candidate-specific validation
   contract, source hashes, exact state crosswalk and script revision with the
   parent agent's checkpoint commit BEFORE expression scoring. Notify the parent
   at spec-ready and before any scientific expression scores. No scoring is
   authorized merely by writing this source-recovery specification.

## Output semantics

Per-candidate JSON uses pass/fail/unresolved/not_assessed gates and explicit missing
fields. A missing deposited state map is an access/identity blocker, not evidence
that the biological state is absent. Record rejected candidates and unsuccessful
source retrievals; distinguish confirmed evidence from author statements and
unresolved inference. If no candidate passes, deliver the source ledger, actual
recovered metadata and a precise enabling-data requirement, without new A5 scores.
