# Q4a accessibility description validation

1 November 2026. [Results](ACCESSIBILITY_RESULTS.md);
[receipt](../../analysis/research/runs/arz1_accessibility_description_v2/receipt.json).
Numerical execution, originating independent raw-source audit, and visual review
of the corrected primary and unchanged sensitivity figures passed. These checks
do not assign scientific acceptance or establish biological replication.

## Prospective source-semantic review

The [v1 hold](ACCESSIBILITY_V1_HOLD.md) remains immutable at checkpoint
`5e85c6f`. No accessibility endpoint was released in v1. Originating review
independently confirmed the three opposite-strand prefix pairs, then authorized
the two explicit count definitions in
[the v2 amendment](config/ACCESSIBILITY_AMENDMENT_V2.md) and
[frozen review](config/ACCESSIBILITY_REVIEW_FROZEN_V2.txt).

V2 freeze is `3f2b5872b9b1f7e4dcb2ea428b94357c9bd42a4c`.
Its [contract](config/accessibility_contract_v2.json) binds 32 inputs and nine code
dependencies, including reused v1 region/RNA helpers, and declares 18 outputs.
The originating reviewer inspected the new core, wrapper, plotting and targeted
tests before execution and reported no blocking implementation issue.

All 12 synthetic tests passed, including the known-answer opposite-strand pair
with primary=2 and grouped=1 in BOTH numerator and denominator, nonadjacent
opposite-strand records, excluded barcodes/contigs, and same-strand duplicate
rejection despite changed readSupport. Region conversion/merging/fallback,
truncation, malformed records, header/order failures, weighting, zero depth and
changed RNA population behavior are covered. The first sandbox attempt failed
to create temporary fixtures; the authorized normal-temp-access rerun passed.
Input preflight and exact staged code/specification hashes passed before execution.

The staged whitespace check flagged one extra blank line at EOF in the frozen
v2 test file. This formatting exception is retained transparently; it does not
change test behavior. No frozen byte or check was rewritten to conceal it.
The older three Saxton and two RNA-SVG whitespace exceptions remain untouched.

The final `git diff --check origin/main` reports exactly these six frozen files
(exit 2). Trailing-whitespace counts below are diagnostic locations; SVG line
spans do not imply that every intervening line is affected. No whitespace rule
or attribute was weakened, and the final report edits are whitespace-clean.

| Frozen repository path | Preserved whitespace diagnostics |
|---|---|
| `Research Article/gate3_08_saxton_2021_il22/reassessment_v1/config/description_contract_v1.json` | 143 trailing-whitespace locations, lines 1–143 |
| `analysis/research/runs/sx22_program_description_v1/tmm_stderr.log` | 7 trailing-whitespace locations, lines 1–7 |
| `analysis/research/runs/sx22_program_description_v1/tmm_stdout.log` | 37 trailing-whitespace locations, lines 1–37 |
| `analysis/research/runs/arz1_rna_description_v1/figure_01_primary.svg` | 232 trailing-whitespace locations, spanning lines 24–1200 |
| `analysis/research/runs/arz1_rna_description_v1/figure_02_sensitivity.svg` | 53 trailing-whitespace locations, spanning lines 24–1077 |
| `Research Article/ungated_arozamena_2026_inflammatory_memory/tests/test_accessibility_v2.py` | One extra blank line at EOF, line 78 |

## Post-run validation

The runner completed all three full fragment traversals and all 18 declared
outputs. All four loci and 128 paired cases qualified, with no local holds.
Receipt verification passed. All 152,186,923 records reached source EOF/CRC and
structural checks before any measurement endpoint was released. Each count
definition's denominator and locus differences reconcile with collision counts;
paired sets agree exactly. All 48 RNA reuse checks matched the frozen same-selection
RNA sums/denominators and transformed values.

An independent audit importing no production code reconstructed all four M33
region families directly from the GTF, then recomputed library and contrast
arithmetic from saved barcode counts using separate Python/math.fsum calculations.
It passed 39,962 depth rows, 19,981 unique paired barcodes, 159,848 locus rows,
144 library summaries, all 128 paired cases, 64 definition deltas, 12 population
rows and all three source-accounting records. It also reconciled all 3,181
library/barcode collision records with denominator differences and verified RNA
reuse and all positive-pair/QC flags between count definitions. Local audit script
and exact result are retained under `.tools/arz1_accessibility_validation/`.

Both actual PNGs were inspected. The sensitivity figure passed technical and
originating visual review, including its separate definition-delta color scale.
Originating review requested correction of the primary legend, which crowds/
touches the left panel title. The separately frozen
[render-only contract](config/primary_render_contract_v1.json), committed in
`c9fbf92`, binds only the existing contrast table, v2 receipt, correction brief
and two code files. It generated the corrected primary PNG/SVG under
[a separate receipt](../../analysis/research/runs/arz1_accessibility_primary_render_v1/receipt.json),
which passed verification. The corrected PNG passed both technical and originating
visual inspection.
An independent SVG/source-table check confirmed all 16 bar x geometries and all
16 value labels unchanged, with title/legend baselines now 42.241406 SVG points
apart. No measurement was rerun or value changed. Original v2 images and receipt
remain byte-identical. New SVG whitespace cleanup occurred during first generation,
before receipt hashing; no frozen artifact was normalized afterward.

On 1 November 2026, the originating reviewer reported that its independent full
raw-source audit **passed**: 60 hash bindings, all 152,186,923 fragment records
through gzip EOF/CRC, 39,962 barcode-depth rows, 159,848 barcode-locus rows, all
128 paired contrasts, all collision diagnostics and 64 count-definition deltas.
The reviewer independently reconstructed the GTF TSS windows and gene bodies,
recounted both fragment definitions, and recounted all four target RNA loci from
raw input, without importing production analysis code. It reused the hash-bound
RNA depths/QC that it had already independently verified; this does not claim a
second fresh reconstruction of every RNA depth/QC value during this audit.
The saved-count audit and raw-source recount are complementary technical checks,
not independent biological replication. This records the review received from
parent chat `01a18687-3e55-7b51-b514-52f5f55a210b`; parent owns the integrated
[originating review record](ORIGINATING_REVIEW.md).

## Repository and preservation checks

Freshly fetched `origin/main` is unchanged at
`51d3b930b3805c616e67e414390ecf060647d090`. Compile passed; all 158 shared tests
passed with two Windows skips. Required Nabhan, Travaglini/Nabhan, A16, A23 and
A22/A23 archive/evidence verifiers passed. Logs are retained locally under
`.tools/arz1_accessibility_validation/`. Before the render-only correction,
13,127 repository checks, the base-aware research gate and 18 claim bindings
passed. All 21 v2 run files matched staged bytes exactly; the three declared gzip
tables were explicitly staged despite the general gzip ignore rule. These new
outputs were whitespace-clean. The render code compiled and its input preflight
and exact staged bindings passed before execution. Both receipts are registered.
After the render/report additions, 13,134 repository checks and the base-aware
research gate passed. All five render run files match staged bytes exactly;
the new artifacts/report changes are whitespace-clean, and the original v2
outputs are unchanged from their preservation commit. Passed shared/archive
tests and claim bindings are reused because rendering does not invalidate them.
After the originating raw audit passed, the requested final repository check
(13,134 checks), refreshed-base research gate and claim check (18 bindings) also
passed. Both v2 and render receipts were confirmed registered exactly once;
no duplicate registry entry was added. This final handoff changes only the two
accessibility reports and does not rerun any biological analysis or render.
The last scope check contains only this article package, its new accessibility
runs and the research registry; parent-owned navigation/PROGRESS remain outside
this technical patch.

No governance/validator, claim grade, source freeze, earlier run or human scientific
decision is changed. Parent owns README, literature/RQ navigation, PROGRESS and PR
integration. No push or main merge is part of this technical phase.
