# Source v2: bounded metadata amendment

29 October 2026. Owner-authorized correction of the two interpretations documented
in [the v1 correction note](SOURCE_QUALIFICATION_CORRECTION.md), based on handoff
`d62612ba0975e60f6b9d03e00ef22c3924af898b`. This is source metadata recovery under
article-local candidate DY1-P01, not a biological hypothesis test or resumption
of the restricted analyses. Current global RQs and scientific acceptance remain
unchanged. The previous chat transcript was not loaded.

## Question, endpoint and decision

Which condition labels and tag identifiers actually occur in the deposited
reference files and feature tables after trimming header/value whitespace?
The endpoint is a source-label and identifier census. Its unit is a reference
record or feature table. The decision is whether the two v1 interpretations are
correctly superseded; animal/pool identities remain unknown.

The principal validity threats are blank labels caused by whitespace and false
joins across reused tag names. Labels retain their original case, spelling and
internal punctuation. All reference-file/tag-ID by feature-file membership checks
are reported, including negative matches. These are string-membership checks,
not expression-library pairings, cell assignments or biological replication.

## Exposure and amendment

Before freeze, this session read the v1 output, review corrections and four
reference CSVs; earlier reviewers had inspected feature-table CMO rows. These
observations are explicitly exposed. A new freeze does not erase that exposure.
No biological outcome comparison is specified.

The [new contract](config/source_v2.json) has `amendment_of` pointing to
[source_v1](config/source_v1.json). V1 code, contract, outputs and receipt remain
byte-for-byte preserved. V2 supersedes only the naive reference-label parse and
the categorical `scRNA_condition_batch` interpretation; it does not reproduce or
replace the remaining v1 inventory.

## Inputs, implementation and verification

The contract binds 20 existing public-source files (1,199,598 bytes): four small
reference CSVs, their compressed originals, four feature tables and eight GSM
metadata records. Source and destination SHA-256 values were checked against the
unchanged v1 contract. Inputs are copied to repository-relative ignored paths.
No count matrix, barcode table, sequencing read, bulk count or peak file is used.

[Parser](scripts/qualify_sources_v2.py) trims headers and values, rejects missing
required fields and ambiguous headers, and inventories each feature table.
[Synthetic tests](tests/test_sources_v2.py) cover whitespace, quoted commas,
missing/blank/extra fields, duplicate identifiers and normalized header collisions.
[Separate verification code](scripts/verify_sources_v2.py) reads compressed
references positionally and independently computes feature identifier sets,
all membership rows, accession/title fields and output summaries. This is
computational verification of the same sources, not independent biological
replication or scientific acceptance. Errors stop execution and remain recorded;
no failed run is deleted or overwritten.

## Interpretation boundary and stopping rule

Feature presence establishes neither condition/library confounding nor its
absence. Actual cell conditions, meaningful tag counts, ambient/background
signal and animal/pool assignments remain unassessed. No cells are assigned,
animals inferred, expression differences estimated, motifs scanned or mechanisms
derived. Stage 0 remains partial; this correction cannot complete stages 1–8.
No output is created under `RQ_Specified`.

Execution requires passing input preflight, a committed frozen contract and
hash-bound code, followed by the unchanged repository `research_gate` runner.
Current results and verification will be recorded separately after execution.
