# Technical verification and preservation

8 November 2026. No human scientific acceptance or claim promotion.

| Frozen stage | Commit | Execution |
|---|---|---|
| Source qualification v1 | `e30618c` | Failed row-order annotation assertion, before treatment contrasts; bytes retained |
| Source qualification v2 | `ea6267a` | Executed with explicit unique-ID alignment and unchanged annotation equality |
| RNA description v1 | `1334d29` | Executed; all 14 expected artifacts present |
| Failure preservation v1 | `1334d29` | Exact archive only; original failed status retained |

All successful receipts verify their recorded contract, code and output hashes.
Raw inputs were SHA-256 bound before execution. Source rows and every published
target remain; the current result does not replace the original papers or claim
independent biological replication. The metadata correction changes only a row
join after identifying identical keyed annotations; no biological exclusion or
threshold changed. Original source files were never modified.

The [known-answer tests](scripts/test_description_v1.py) passed before freeze:
proportional-library normalization, known group contrasts, and rejection of an
empty positive reference. The [independent scalar verifier](scripts/verify_v1.py)
imports no production code and passed at 1e-10 tolerance: all 58,735 primary rows,
raw stable-ID joins, 64 normalization factors, 552 target/library/scale values,
621 target/case rows, 54 amplitude fits, 162 panel summaries/member counts and
483 range rows. These are numerical checks of the same source, not replication.

All three actual PNGs were inspected. The 23 source labels and IL2 asterisk are
readable; every library and five contrasts appear; scatter references are labeled
with noisy-axis/shared-PBS limits; the eight Figure5B targets display all scales
and omission ranges, including CCL1 crossing zero. No clipping or post-run edits
were needed. Vector PDFs are explicitly retained despite the global PDF ignore.

The existing R runtime did not resolve edgeR during a pre-freeze probe. The
description prospectively selected and specified median-ratio CPM; no TMM values
were computed or selected after results. The isolated probe did not install or
modify software. Python, NumPy and Matplotlib supplied the qualified local CPU
execution. S9 access failures and version/notice coverage are recorded in the
[source context](LITERATURE_CONTEXT.md), not mistaken for missing source-wide data.

The success-only receipt validator initially rejected the failed v1 receipt.
Following existing Nb5/DY1 practice, a separate hash-bound metadata run archived
all four original files, without changing their bytes or execution_failed status.
Original files remain locally and in `ea6267a`; only duplicate index entries are
retired in favor of the registered archive. A private directory-local ignore keeps
the unchanged original failed files local; the root `.gitignore` is itself bound
by an older run and was restored exactly after the gate detected the attempted
ignore-rule addition. Validators, governance and frozen
historical evidence remain unchanged.

Additional independent metadata joins/QC, all-row residual identities and 69
input/code/output hash bindings passed, including exact contracts at their freeze
commits. All 36 global owners, 38 prior local candidates and existing guides/
infrastructure are preserved. A scratch verification stopped on an optional
missing evidence key; correcting that checker confirmed preservation without
changing scientific code or output. The broad test suite initially encountered
sandbox temporary-directory permissions; using a scoped temporary directory
passed all 167 tests (two expected Windows skips). The repository validator passed
17,647 checks after the handoff link was completed.

Final repository/integration checks and remaining review state are recorded in
[the combined handoff](../../docs/research_reviews/2026-11-08-saxton-reading/EXECUTION_HANDOFF.md).
