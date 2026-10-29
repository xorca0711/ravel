# Corrected source metadata: v2

29 October 2026. **The two documented v1 metadata interpretations are corrected.**
The new [receipt](../../analysis/research/runs/DY1_source_v2/receipt.json) records
successful execution at frozen commit `015b339808b004210c9983ae8b9e35cd5bb6d2ed`.
The [amendment](SOURCE_V2_AMENDMENT.md) and [contract](config/source_v2.json)
record scope, exposure and the `amendment_of` link. V1 remains byte-for-byte intact.

## Findings and supersession

The naive reference's `multiplexed_sample ` header contains a trailing space.
Trimming headers and field values recovers `Naive`; no new label is invented.
The exact reference labels, retaining internal spelling and punctuation, are:

| Reference accession | Label in reference CSV | Tag identifiers |
|---|---|---|
| GSM9964564 | `Naive` | CMO301–303 |
| GSM9964565 | `Day 35 post nb infection` | CMO304–306 |
| GSM9964566 | `Day 35 post nb infection + IAV, 3dpi` | CMO301–304, CMO309–310 |
| GSM9964567 | `Naive + IAV,3dpi` | CMO301–304, CMO309–310 |

Each feature table contains 32,285 Gene Expression rows and six Antibody Capture
rows. The tag presence inventory is:

| Feature table | CMO identifiers present |
|---|---|
| GSM9964560_count1_features.tsv.gz | CMO301–306 |
| GSM9964561_count2_features.tsv.gz | CMO301–306 |
| GSM9964562_count6_features.tsv.gz | CMO301–304, CMO309–310 |
| GSM9964563_count5_features.tsv.gz | CMO301–304, CMO309–310 |

Evidence: [reference labels](../../analysis/research/runs/DY1_source_v2/reference_labels.tsv),
[feature tags](../../analysis/research/runs/DY1_source_v2/feature_tags.tsv),
[all membership checks](../../analysis/research/runs/DY1_source_v2/reference_presence.tsv)
and [structured result with input hashes](../../analysis/research/runs/DY1_source_v2/source_qualification.json).

This supersedes only the blank GSM9964564 label and categorical
`scRNA_condition_batch` statement in
[v1's qualification output](../../analysis/research/runs/DY1_source_v1/source_qualification.json).
Condition/library confounding remains **unresolved**. Feature presence proves
neither that cells of each condition occur in each library nor that conditions
are confounded with libraries. Tag identifiers are local to a source record;
their reuse does not identify animals or pools. No reference-to-library biological
pairing is inferred from the table above or the exhaustive membership file.

## Verification and preservation

The unchanged research gate executed the committed frozen contract once and
verified its receipt. A separate positional CSV reader checked the compressed
source references against the production parser's uncompressed-reference output.
A separate feature line/set census checked inventory and membership joins.
[Verification](../../analysis/research/runs/DY1_source_v2/verification.json)
passed for all 18 reference rows, 24 feature-tag rows, 72 membership rows and
eight accession/title records. This checks the same public sources; it is not
independent biological replication. The reviewer found no blocking scope or
correctness issue before freeze and verified the saved results afterward;
the exact bounded review is recorded in the validation record. That technical
review is not scientific acceptance.

Nine synthetic tests passed for whitespace, quoted commas, missing/blank/extra
fields, duplicate reference IDs, normalized-header collisions and feature-field
handling. All 20 copied metadata inputs (1,199,598 bytes) matched the v1 contract
hashes before freeze and at execution. No metadata run failed; stderr is empty.
The runner's original `verification: pending` field remains untouched;
subsequent receipt verification is recorded here, not edited into the receipt.

All nine v1 files (script, contract, receipt, four outputs and two logs) were
checked byte-for-byte against the preserved execution checkout. Fifteen missing
historical Choi validation outputs were restored from local copies only after
checking their published-lock hashes; no analysis was rerun to restore them.
Repository validation and final preservation checks are recorded in
[the validation record](SOURCE_V2_VALIDATION.md).

## Remaining status

Stage 0 remains partial: animal/pool identity, actual cell conditions and
condition-by-library support remain unknown. Numerical components of stages 1–7
and results-based stage 8 remain unfinished after the earlier platform
restriction. Prior source reading and design audits remain completed review work.
This task did not retry the restricted analyses and establishes no new biological
effect, mechanism, RQ result, claim grade or scientific acceptance.

The [README ledger](README.md#completion-ledger-documentation-close-out) owns the
current stage status. The current bounded task has no further analysis queued.
The owner's broader analysis request remains authorized but unfulfilled. The
platform restriction and this session's metadata-only scope prevent resumption
here; no repeat authorization is being requested. No external-service write or
settings change occurred; earlier access limitations were not retested.

## Primary source locators

These are the deposited source records represented by the cached, hash-bound
inputs, not new web retrievals:
[GSE343897](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE343897),
[GSM9964564](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9964564),
[GSM9964565](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9964565),
[GSM9964566](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9964566),
[GSM9964567](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9964567).
Exact repository evidence and input SHA-256 values are linked separately above.
