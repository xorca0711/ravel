# Integration validation — 3 November 2026

Validated on `codex/full-priority-screening-20261103`, stacked on `f54ad29c092fcc9f6c38048d902a7b79bc066686`. Refreshed `origin/main` is `445a0ca934f2f67060fbf7faec7746612526fb92`; PR #162 remains open at the unchanged stack base. GitHub identity was verified as `xorca0711`; Git author remains `Xorca`.

- Repository validator: **15,650 checks passed**.
- Research registry/base check: passed against `origin/codex/a32-resolution-screen-20261103`.
- All seven new receipts verify; all 67 staged run files match their working-copy bytes exactly (6,779,496 bytes total). Raw source matrices and cached primary-source PDFs are not included.
- Python compilation passed. The default runtime suite passed 167 tests with two skips: unavailable scientific runtime and Windows symlink privilege. The skipped scientific module then passed all four tests in the existing x64 analysis runtime. Together this covers 170 distinct tests, with only the host symlink test skipped; Linux CI exercises that path.
- Claim contract passed all 18 numeric bindings. Required Nb1, Nb4, A16, A23 and A22/A23 extension archive checks passed.
- Hash-locked published-output restoration verified all 16 members and created zero files; no biological analysis was rerun.
- All **1,609 local links** in the 85 changed Markdown files resolved before this validation note was added. The validation note's new navigation links were checked separately.
- Documentation, code and JSON whitespace checks passed. Generic whitespace checking flags 574 TSV lines with terminal empty fields. Those fields encode missing or unsupported measurements; the frozen bytes and tabular columns are intentionally preserved. No attribute or validator was changed to suppress the findings.
- All 21 canonical files updated by the technical chat preserve their preexisting body bytes; each adds only a two-line current-result note. Other owner updates preserve prior evidence and hypotheses.

The first sandbox test/restore attempts failed on temporary-directory permissions/network access. The same commands succeeded in the authorized local runtime; no tests, outputs, contracts or governance rules were modified to obtain a pass.

These checks establish integration/provenance consistency. Independent numerical and biological review is recorded in [the coordinator review](COORDINATOR_REVIEW.md); scientific limits and reopening conditions remain in [the coverage report](README.md) and [technical ledger](TECHNICAL_LEDGER.md). Execution completion does not constitute human scientific acceptance.

## Cross-platform publication correction

The first remote Repository checks workflow passed, but [Research governance run 41632601028](https://github.com/xorca0711/ravel/actions/runs/41632601028) failed on nine configuration hashes. The Windows execution bytes were CRLF; their unchanged Git text blobs were LF, and Linux materialized LF without an explicit checkout rule. Local validation therefore passed while the clean Linux checkout correctly rejected the mismatched bytes.

Two directory-local `.gitattributes` files now specify `text eol=crlf` for exactly those nine filenames. They leave the root attributes file, contracts, receipts, scripts, recorded hashes, Git configuration blobs and scientific outputs unchanged. An independent check verified every affected input's original raw hash, exact equivalence to its LF Git blob after newline normalization, and all existing code/input bindings. A fresh `core.autocrlf=false` checkout reproduced all nine recorded execution files byte for byte. This is a packaging correction, not a reanalysis, retrospective hash change or validator exception.

The technical chat independently reviewed the exact-byte correction before publication, including the original A12 pilot result/validation hashes and unchanged historical Git blob. No conflicting older raw binding was found. The rules are slash-anchored to direct-child filenames. They make Git checkouts at the corrected revision portable; they do not alter historical commits or raw Git/archive bytes. The succeeding remote workflow on the corrected head remains the authority for the clean Linux result.
