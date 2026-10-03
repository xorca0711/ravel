# Nb5 execution and validation ledger

3 October 2026. This supersedes planning-only status, not frozen outputs.
Base: fetched `origin/main` `76dc9b47f72e774e51502162b2f8ba9d0dc02f17`.
Work: `codex/nb5-aging-atlas-plan`, isolated managed worktree. No push, PR,
merge, scientific acceptance or external service setting change is implied.

## Frozen executions

| Contract | Outcome / correction | Evidence |
|---|---|---|
| [metadata_v1](config/metadata_v1.json) | Failed source many-to-one join because merged spreadsheet cells were not decoded | [Original failed receipt, preserved bytes](../../analysis/research/runs/nb5_failed_run_preservation_v1/failed_receipt.json) |
| [metadata_v2](config/metadata_v2.json) | Explicit merged ranges decoded; no biological filter changed | [Receipt](../../analysis/research/runs/nb5_metadata_v2/receipt.json) |
| [metadata_v3](config/metadata_v3.json) | Added author Figure 4 object prospectively | [Receipt](../../analysis/research/runs/nb5_metadata_v3/receipt.json) |
| [descriptive_v1](config/descriptive_v1.json) | Fixed exposed composition, RNA, state, repertoire and source-list descriptions | [Receipt](../../analysis/research/runs/nb5_descriptive_v1/receipt.json) |
| [repertoire_v2](config/repertoire_v2.json) | Corrected exact young-cell names from author code and partitioned clones within mice; only P06 superseded | [Receipt](../../analysis/research/runs/nb5_repertoire_v2/receipt.json) |
| [source_audit_v1](config/source_audit_v1.json) | Corrected bidirectional gene-list denominator and audited annotations; original RNA outputs unchanged | [Receipt](../../analysis/research/runs/nb5_source_audit_v1/receipt.json) |
| [figures_v1](config/figures_v1.json) | Six plates; no biological rerun | [Receipt](../../analysis/research/runs/nb5_figures_v1/receipt.json) |
| [failed-run preservation](config/failed_run_preservation_v1.json) | Exact archive only; original analysis remains failed | [Preservation receipt](../../analysis/research/runs/nb5_failed_run_preservation_v1/receipt.json) |

Contracts and their code were committed before each execution. All input and
output hashes remain bound. The complete failed run is archived byte-for-byte
in the preservation run, with [original paths and hashes](../../analysis/research/runs/nb5_failed_run_preservation_v1/preservation.json).
The original local files remain unchanged and are also recoverable from commit
`a0565ea`. Only their duplicate Git index entries are retired in favor of the
registered archive; no source file is deleted or moved. The original receipt
still says `execution_failed`. The existing validator only accepts successful
receipts, so archival success is explicitly separated from scientific execution.
Governance and validators were not changed.

## Numerical verification and visual inspection

- Every composition count agrees with a separate Counter calculation over
  source cells. Direct CSR traversal independently reproduces Cdkn2a detection
  and mean for every mouse in all five general objects.
- Across 17,777 RNA summaries, unconditional mean equals detected fraction
  times positive-cell mean (maximum residual 5.69e-14). Zero-positive rows
  retain a missing conditional mean. All normalized source rows sum to
  approximately 10,000; none is relabeled as raw counts.
- Every corrected repertoire animal/clone size agrees between Counter and
  grouped arithmetic. Source numerators match 55/479/348; denominator and
  unmatched-row discrepancies remain explicit.
- Source-list and label audit records 200 unique combined ageing genes and
  56 overlaps, not a forced match to the manuscript's 55.
- All six 300-dpi PNG plates were visually inspected: legible labels,
  nonoverlapping panels, visible unit counts and explicit scales. SVG and
  individual/combined PDF exports are present. Six-page PDF structure is checked.

These are computational checks using reused data, not biological replication
or independent scientific acceptance. The full check results are in the
[descriptive verification](../../analysis/research/runs/nb5_descriptive_v1/verification.json)
and [repertoire verification](../../analysis/research/runs/nb5_repertoire_v2/verification.json).

## Environment and replay

Python 3.12.14; NumPy 2.4.6; SciPy 1.18.0; pandas 2.3.3; h5py 3.16.0;
matplotlib 3.11.1; openpyxl 3.1.5. The bundled x64 interpreter used the existing
scientific dependency directory; no dependency installation was required.
Receipts store repository-relative commands. Reacquire exact inputs using
SOURCE_MANIFEST.md, verify their hashes, and use a new run ID. Never replay
over a frozen run directory. The failed run can be restored from the archive
mapping if its preservation command must be independently repeated.

## Repository verification

All ten required checks passed against freshly fetched, unchanged `origin/main`
`76dc9b47f72e774e51502162b2f8ba9d0dc02f17`:

| Required check | Result |
|---|---|
| Python compilation | Passed |
| Evidence/provenance unit tests | 123 tests; one existing skip; passed |
| Claim contract | 18 numeric bindings; passed |
| Nb1 frozen evidence | Passed |
| Nb4 archive | 20 run records and 164 output hashes; passed |
| A16 archived evidence | 1,867 checks; passed |
| A23 external analysis archive | Passed |
| A22/A23 extension evidence | Passed |
| Repository validation | 7,951 checks; local links, JSON and numeric bindings passed |
| Research gate against origin/main | Passed; no unregistered scientific assets |

`git diff --check` passed. Every figure PNG has approximately 300-dpi metadata;
the combined PDF contains six pages. Original failed-run files remain present
and byte-identical to the registered archive. The two pre-existing primary
checkout edits retain their original SHA-256 values; `.claude/` and ignored
source data were not modified. No historical biological analysis was rerun.
Local commits include the necessary prospective freezes and completed evidence;
no push, PR or merge was requested. External scientific review, lab access and
GitHub protection settings remain outside this execution's verified scope.

## Caption edition on 3 October 2026

[Figures v2](config/figures_v2.json) adds full captions inside every PNG, SVG
and PDF, including rationale, panel definitions, observed results and limits.
The [verified receipt](../../analysis/research/runs/nb5_figures_v2/receipt.json)
binds the unchanged numerical inputs and the new renderer/caption module.
Version 1 remains immutable. An AST comparison confirms that the main panel
calculations and selections are unchanged, excluding only export metadata.

Every caption passed mechanical checks for canvas bounds and separation from
plots, title and source attribution. All six PNGs were visually inspected.
The combined PDF has six pages, each containing extractable rationale and
results text. No new biological analysis or extension was executed. Current
repository verification for this edition passed all ten required checks,
including 123 tests (one existing skip), 7,963 repository checks and the
research gate. Version 2 is superseded for presentation by version 3 below.


## Compact caption edition on 3 October 2026

The owner found the v2 caption paragraphs too long. The committed
[v3 contract](config/figures_v3.json) therefore limits embedded captions to
short footnotes modeled on neighboring Nb2/Nb4 figures. Expanded explanations
remain in the gallery. The [verified receipt](../../analysis/research/runs/nb5_figures_v3/receipt.json)
binds the new renderer and caption module to unchanged input tables; v1 and v2
are preserved. The frozen renderer's panel-calculation AST matches v1 exactly,
excluding export metadata. No biological analysis or extension was rerun.

All six PNGs were visually inspected: captions occupy 2–3 lines at 9 points,
with 39–51 words. Mechanical bounds and panel-separation checks passed for all
plates. PNG metadata is 300 dpi, and all six compact captions are extractable
from the six-page PDF. The layout reuses the existing bottom margin and adds
only the space necessary; plot physical dimensions are preserved.

The preceding full check suite remains valid for unchanged tests and archived
analyses. Final checks for the new renderer, registered receipt and gallery
links are recorded below. Generated SVG path serialization contains trailing
spaces; immutable SVG output bytes are retained. Whitespace checking is scoped
to authored Markdown, Python and JSON.


Final integration check: `origin/main` advanced to
`bf7d7166887fb4207eb4582f41925a565a327dbf` (PR #132). Merge `6c247c0`
retains both branches' exact-byte rules, registry entries and progress records;
all incoming registry entries were mechanically checked for preservation.
All ten required checks then passed: compilation, 134 tests (one existing
skip), 18 numeric claim bindings, Nb1/Nb4/A16/A23/A22–A23 archive verification,
8,050 repository checks and the research gate against the updated base.
Authored-file whitespace checks passed. No scientific acceptance, new extension
execution, push or PR is implied by this presentation update.
