# Source-checkpoint validation

1 November 2026. Scope: **Arz1-P01 metadata Q0-Q2 only**. Interpretation and
eligibility are in [SOURCE_QUALIFICATION.md](SOURCE_QUALIFICATION.md).
No biological analysis, population inference or human acceptance was performed.

## Frozen executions and parser coverage

| Execution | Freeze | Outcome |
|---|---|---|
| [V1 receipt](../../analysis/research/runs/arz1_source_qualification_v1/receipt.json) | `8673abad74022d8d8a90d43857f68698806ecb66` | Executed; four HDF5 libraries qualified, three MatrixMarket components held on empty feature records; six GEO series, 44 sample/BioSample pairs and five dense tables inventoried |
| [V2 receipt](../../analysis/research/runs/arz1_source_qualification_v2/receipt.json) | `4028767b6d4b05e2eba6fa657480c9dd33465f3d` | Executed; four original HDF5 rows reused unchanged, three MatrixMarket files qualified by the prospective counted-empty-record adapter |

Eight v1 synthetic tests and five new v2 tests passed before their respective
execution. They cover source fields, duplicate IDs/barcodes, unsigned CSC column
resets, coordinate/value integrity, dimensions, dense fractional estimates,
empty-record handling, malformed nonempty records and no-overwrite/LF output
behavior. These unchanged tests were not redundantly rerun for report editing.
Both freezes passed input preflight; staged specification bytes were checked
against worktree bytes. V1 bindings were verified unchanged before v2 execution.
Receipt verification passed after each execution; receipt contents are preserved,
including the runner's historical `verification: pending` field. Later validation
does not mutate a receipt to rewrite its recorded status.

V2 preserves all source bytes. Empty feature-record counts are 159,944 / 146,464 /
110,123 for CTRL/KRT20/LGR5; each nonempty record has six fields including its
explicit modality. Barcode/MatrixMarket files have no empty records. All seven
matrices have verified unique sparse coordinates and finite nonnegative integer
values. All their deposited columns carry positive RNA and peak counts on one
shared column axis. These are technical checks, not cell-state or donor evidence.

## Independent verification and its limits

A scratch verifier at `.tools/arz1_source_validation/verify_metadata.py` imports
no production qualification code. It independently reconstructed source joins and
read identifiers/headers, passing the following checks:

- Exact six-series SOFT sample set and 44 one-to-one GEO/BioSample source joins.
- All seven raw matrix header/feature/barcode dimensions, ordered fingerprints,
  feature types, unique identifiers and declared sparse-entry counts.
- Four reused HDF5 inventory records exactly equal their v1 rows; three amended
  feature-file blank counts and six-field nonempty records agree with v2.
- All 49 ordered barcode pairs and 98 modality-specific feature pairs agree with
  direct set intersections/order checks. All common feature IDs agree exactly:
  **31,950 RNA IDs and zero peaks across seven libraries**.
- Five dense-table source headers, row counts and identifier fingerprints match;
  all three immune barcode lists match their matrix columns in order.

The originating reviewer independently reported a separate audit of all **127
unique contract/input/code/output hash-bound paths** across v1/v2, all seven raw
header/feature/barcode dimensions and fingerprints, and every saved overlap.
That audit and this verifier did **not** independently rescan every sparse numeric
triplet. Numeric-body integrity relies on the reviewed frozen streaming/chunked
parsers and synthetic coverage. Neither audit constitutes biological replication.
The report does not claim independent validation of author donor identities.

PDF source reading additionally included rendered visual inspection of transparent
peer-review p30 and Reporting Summary p3. The first qualifies donor deconvolution
as supportive consistency evidence without independent genotype validation; the
second's generic replication wording does not resolve the pooled assay units.
Source workbook inspection was limited to text labels and cell locations.

## Integration checks and preservation

Integration base freshly fetched on 1 November 2026:
`origin/main = 51d3b930b3805c616e67e414390ecf060647d090`.
Parent-approved scope base: `565d8a95339593ca1f6da3385b08eb1f62e4c03d`.
Required checks passed on that base:

- `python analysis/scripts/validate_repository.py`: 13,021 checks passed,
  including local Markdown links, JSON, numeric bindings and claim consistency.
- `python analysis/scripts/research_gate.py check --base origin/main`: passed.
- `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified`:
  passed; shared `analysis/tests` suite: **158 tests run, successful with 2 Windows skips**.
- `python analysis/scripts/claim_contract.py --check`: 18 numeric bindings passed.
- Existing Nabhan, Travaglini/Nabhan, A16, A23 and A22/A23 archive/evidence
  verifiers all passed; no biological analyses were rerun for documentation.

Concise command results and full local logs are retained under
`.tools/arz1_source_validation/`. Staged and complete Arozamena-scope whitespace
checks passed with no exemptions. The preserved broader-PR historical exceptions
below remain separate from this new work.

Own changes are limited to the Arozamena package, two immutable run directories,
and registry additions for two contracts/two receipts. The parent owns README,
literature context, navigation and PROGRESS updates. All prior Saxton files,
root attributes, governance, validators, claim grades and acceptance decisions
remain outside this change. The three known older Saxton whitespace exceptions
in the broader PR are preserved historical bytes; no new exception is introduced
for Arozamena. No push, PR mutation or main merge is part of this checkpoint.

The current limitation is scientific input/specification review, not an external
service setting: the parent must review the narrower RNA estimand and freeze its
numerical brief before any endpoint execution. Original state-resolved Q3,
cross-condition Q4 and linked-function Q6 retain the exact prerequisites listed
in the source report. Raw fragments/reads and merged bulk bigWigs remain deferred.
