# Validation record — 7 October 2026

Integration base: freshly fetched `origin/main` at
`cc5ce7e09bc03df49a982569236d572407ecb195`; PR #145 confirmed merged at
06:12:10 UTC. Tests ran on the scoped audit branch with the current staged
implementation. GitHub CI will independently check the submitted commit.

| Check | Result |
|---|---|
| Whole tracked-file inventory | 5,967 files, 783 Markdown, 1,190 parsed JSON, 2,612 scanned code/document/config text files; no missing tracked files, conflict markers or malformed JSON |
| Registry coverage | 31 questions, 31 article candidates, 69 contracts, 64 registered receipts |
| Research gate against current main | Passed, no errors; receipt hashes, frozen code, historical artifacts and guide declarations checked |
| Repository validator | 10,757 checks passed before adding the generated inventory itself |
| Unit tests | 148 passed, no skips; task-local TEMP/TMP used |
| Python source compilation | Passed for analysis, article and RQ trees; `.tools` excluded as in CI |
| Claim bindings and generated summaries | Passed |
| Nb1, Nb4, A16 Stage 1, A23 external, A22/A23 extension verifiers | All passed |
| Independent correction arithmetic | 91 checks / 4,999 values passed; all 22 original QC selections preserved |
| Compass raw-cache agreement | All 1,328 stored v2 numeric summary values reproduced before correction |
| Raw human QC | Two libraries reconstructed independently, one per tissue; not a replay of all 22 |
| Bulk controls for M3 input correction | M1/M2 tables unchanged |
| Visual QA | Corrected figure v4 and A28/A29 v2 schematics rendered and inspected |
| Diff whitespace | Authored changes passed; original Matplotlib path whitespace in frozen SVG outputs retained to preserve receipt hashes |

The inventory is generated after staging the audit and excludes its own then-new
JSON path from the 5,967-file enumeration. It records **100 of 214 unique contract
input paths present in this audit worktree**. Absent historical raw inputs restrict
reruns in this worktree, not tracked-output verification or the existence of those
inputs elsewhere. New correction inputs passed hash checks before execution.

Five frozen predecessor contracts have no registered receipt: A5 metadata v2
(superseded by v3), Nb5 metadata v1 (v2), Wg source scores v1/v2 (v3), and Wg paired
bulk v1 (v2). They remain specifications, not claimed executions; none is an
unexplained gap in a current executed stage.

## Corrections and failed checks retained

- The first raw-data junction failed the gate's within-root requirement. It was
  replaced with local hard links, with raw contents preserved; the gate was not changed.
- The initial A28/A29 SVG declaration used a byte hash instead of the gate's
  newline-normalized text hash. Declarations were corrected before delivery;
  original v1 illustrations remain unchanged.
- Correction figure v3 failed visual layout QA because its footer overlapped the
  axis label. A frozen v4 layout amendment passed visual inspection; v3 is retained.
- Automatic approval review rejected an inventory-placeholder staging command
  because it could discard audit evidence. Nothing in that command executed.
  The final inventory was generated directly from the real scan instead.

See [numerical verification](correction_verification.json),
[inventory](inventory.json), [audit scope](REPORT.md), and
[return checklist](RETURN_CHECKLIST.md). Passing checks does not establish
biological truth, novelty, regulatory equivalence or human scientific acceptance.
