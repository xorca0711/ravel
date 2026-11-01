# Q4a accessibility description validation

1 November 2026. [Results](ACCESSIBILITY_RESULTS.md);
[receipt](../../analysis/research/runs/arz1_accessibility_description_v2/receipt.json).
Numerical execution and the render-only correction are complete; originating
raw-source review is still in progress and is not represented as passed.

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
which passed verification. The corrected PNG passed technical visual inspection.
An independent SVG/source-table check confirmed all 16 bar x geometries and all
16 value labels unchanged, with title/legend baselines now 42.241406 SVG points
apart. No measurement was rerun or value changed. Original v2 images and receipt
remain byte-identical. New SVG whitespace cleanup occurred during first generation,
before receipt hashing; no frozen artifact was normalized afterward.

Originating review is independently recounting the complete raw fragments under
both definitions, independently building M33 windows and recovering four-target
RNA counts before checking all 128 cases. That audit is pending here. The saved-
count audit and raw-source recount are different checks, not independent
biological replication. Current originating review authority remains
[ORIGINATING_REVIEW.md](ORIGINATING_REVIEW.md).

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
The last scope check contains only this article package, its new accessibility
runs and the research registry; parent-owned navigation/PROGRESS remain outside
this technical patch.

No governance/validator, claim grade, source freeze, earlier run or human scientific
decision is changed. Parent owns README, literature/RQ navigation, PROGRESS and PR
integration. No push or main merge is part of this technical phase.
