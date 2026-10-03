# Planning package verification

Verified 3 October 2026 on `codex/nb5-aging-atlas-plan` in the isolated managed
worktree. Final fetched `origin/main` remains
`76dc9b47f72e774e51502162b2f8ba9d0dc02f17` (PR #131). No remote base change
was found during delivery. At the planning checkpoint, changes were local and uncommitted. Later execution
freezes are recorded separately; no PR or merge is implied by this checkpoint. Runtime: Python 3.12.14 on Windows.

## Required checks

| Check | Result |
|---|---|
| Compile repository Python sources, excluding ignored `.tools` | Passed |
| Unit and contract tests | Passed, 123 tests, one existing skip |
| Generated claim manifest and summary | Passed |
| Nb1 archived evidence | Passed |
| Nb4 archived evidence | Passed |
| A16 archived Stage 1 evidence | Passed |
| A23 current external evidence | Passed |
| A22 and A23 extension evidence | Passed |
| Repository artifact and Markdown validation | Passed, 7849 checks after branch expansion |
| Research governance and changed-assets check against `origin/main` | Passed after branch expansion |

Commands match `REPRODUCIBILITY.md` and the two GitHub workflow definitions.
Archived evidence verifiers inspect existing outputs; no biological pipeline
was rerun. Code and archived evidence did not change after their checks.
Documentation and governance validation were refreshed after the additional
branch cards and registry changes.

## Targeted preservation review

- Eight distinct Nb5 candidate IDs resolve to eight distinct plan files whose
  headings match the registry; each states unit, endpoint, rival and limits.
- All existing registry questions, candidates, contracts, receipts and baseline
  values were preserved. The change adds article-local candidates only.
- Stable roadmap paper entries, original reading order and the N3 companion
  entry were preserved. N4 is a companion entry with the requested folder label.
- Prior `PROGRESS.md` content was verified byte-for-byte after removing only
  this task's inserted checkpoint. Existing history is not rewritten.
- SHA-256 checks confirmed the two unrelated primary-checkout modified files
  retained their observed bytes. Other worktrees and ignored data were untouched.
- Source reproduction and additional hypotheses have separate documents;
  branch registration is not scientific acceptance. No new A-number or claim
  grade, executable analysis contract, run receipt or numerical result exists.

One read-only preservation audit initially hit the sandbox identity's Git
ownership check; it passed under the repository owner's identity. No global
Git trust configuration was changed. No check was weakened to obtain a pass.

## Scientific and external limits

Source-table contents, matrix layers, biological joins, animal coverage,
precision and actual laboratory access remain unqualified. Primary-source
pointers and the owner's note were used for planning; exact source-code and
supplement versions still need reconciliation. GitHub protection settings were
not changed or re-audited. Owner scientific decisions and future execution
remain separate from this documentation verification.
