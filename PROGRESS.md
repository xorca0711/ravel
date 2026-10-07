# Current project state

**Update this before stopping work, every session.**

## Readiness checkpoint — 7 October 2026

PR #145 is merged into main at `cc5ce7e09bc03df49a982569236d572407ecb195`.
PR #140 is closed as superseded. This subsequent audit is on
`codex/repo-readiness-audit-20261007`, in
`X:\GitHub\scRNA_seq\.worktrees\ravel-rename-20261007`.
The primary checkout has been safely fast-forwarded to that main revision;
the audit is in [PR #146](https://github.com/xorca0711/ravel/pull/146),
ready for review and conflict-free when opened. Merge route:
`codex/repo-readiness-audit-20261007` → `main`. No merge was performed.
Use the PR’s current checks for remote CI status.

- [Full audit and limitations](docs/audits/2026-10-07-repository-readiness/REPORT.md)
- [Return checklist for approximately 21 October](docs/audits/2026-10-07-repository-readiness/RETURN_CHECKLIST.md)
- [All 31 question baselines](docs/audits/2026-10-07-repository-readiness/QUESTION_REVIEW.md)
- [Current Wang/Wagner 2025 corrections](Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md)
- [Validation record](docs/audits/2026-10-07-repository-readiness/VALIDATION.md)

## Completed

Whole-repository text/structure/provenance scan and current-index reconciliation;
all-question rationale review; new governed Compass orientation v3, human
full-library normalization v3 and dependent M3 v2 corrections. Independent checks
cover 4,999 values. Original outputs remain preserved. Current figure v4 and
A28/A29 schematic v2 interpretations replace affected earlier panels/labels.
R4 cell gates are unchanged (35,928 cells); A30 v3 was already full-gene normalized
and was not rerun. No new claim grade or human scientific acceptance was created.

Validation: 148 unit tests, all required archive verifiers, claim bindings,
compilation and the research gate passed. The final repository validator
passed 10,762 checks. See the validation record for scope and final CI status.

## Next analysis and remaining qualifications

Select the paper/RQ from the owner's next question; no portfolio ranking is
implied. Read its current results, amendment and literature context before its
plan. Qualify biological units, endpoint, comparisons and available inputs;
then commit a new exposed/frozen contract before a numerical run.

For continued Wp work, the correction report owns current signs and values.
A30 still needs justified null/QC/common-state qualification for stronger claims;
A28 needs functional evidence beyond marker proteins; A29 needs a metabolite and
functional discriminator. Other RQs retain the source, unit, precision and
technical holds listed in the review ledger, including A17 implementation.
These are explicit requirements for future work, not positive results in waiting.

The X-drive ARM64 Python environment works; the x64 launcher remains unavailable.
Raw data are not all present in every worktree: use contract input preflight.
The Wp cache is exposed by hard links in the audit worktree; never modify raw
inputs in place. An old empty Git lock was preserved and removed from the active
lock name; no user data or worktree was deleted. Remote protection settings and
human scientific/bench approvals were not changed or certified.

## Historical checkpoints

The previous long PROGRESS file is preserved at the exact
[pre-audit revision](https://github.com/xorca0711/ravel/blob/cc5ce7e09bc03df49a982569236d572407ecb195/PROGRESS.md).
Its draft/ready/open PR statements describe their dated checkpoints and are not
current instructions. Earlier dated audits and frozen evidence remain in place.
