# Continuation validation — 4 October 2026

All ten required repository check groups passed against freshly fetched
`origin/main` at `a5d41834395cac0b82b488d48759ceb6fab8f2d5`.
This validates repository integrity and execution provenance; it does not certify
literature completeness, biological replication or scientific acceptance.

| Check | Actual result |
|---|---|
| Repository/link/artifact validator | 9,621 checks passed after the final prose update |
| Numeric claim contract | 18 bindings passed |
| Nb1 and Nb4 archived evidence | Both passed |
| A16, A23 and A22/A23 extension evidence | All three passed |
| Repository unit tests | 143 tests, OK; one existing optional-runtime skip |
| Python source compilation | Passed |
| Research gate against refreshed main | Passed, zero errors |
| New source-join tests (separate targeted run) | Five passed; duplicates, missing identity and label conflicts rejected |
| R0 preflight and receipt verification | Passed; execution frozen at `fee96e4` |
| Independent identity verification | All 290 author-SRX/GSM joins and 139/151 split checked against raw SOFT blocks |

The first whitespace check stopped on a Markdown hard-break trailing space;
it was corrected before the check suite. No gate or validator was weakened.
Source acquisition encountered publisher challenges and one appendix-host DNS
failure; Europe PMC supplied the appendix and PGAM workbooks. These were source
access failures, not failed biological runs. A later sandbox-only preservation
check encountered Git ownership restrictions; final user-context verification
confirmed the original checkout clean at `1527bea`, without changing global
safe-directory settings.

Exact-byte Git attributes cover only the new Wagner scripts/contracts and R0
outputs, preserving hash-bound files across Windows checkouts. Registry changes
add the one contract, one receipt and Wg current-evidence links. Existing question
records, candidate plans, question guides, contracts, receipts, infrastructure
allowlists, scientific archives and claim grades are preserved.

Logs: the continuation scratch directory's `validation/results.json` and one
log per check, located in the [handoff](HANDOFF_2026-10-04.md). The final
prose-only update passed the link/artifact and whitespace checks; the passed
numerical archive checks are reused. No biological pipeline is rerun for prose.

Delivery is local on `codex/wagner-continuation-20261004`; no push, PR or merge.
The original planning checkout remains the recovery source. Interpretation
boundaries are proposed revisions requiring explicit scientific review before
acceptance. CPLEX, historical runtime equivalence, source-unit gaps and actual
laboratory access remain unresolved; external protection settings are unchanged.

## Historical initial planning validation

### Documentation-stage validation

4 October 2026. All ten required local check groups passed on the staged package
against main `a5d41834395cac0b82b488d48759ceb6fab8f2d5`. A final fetch returned
the same revision. These checks validate repository structure and recorded
evidence, not biological reproduction or scientific acceptance.

Scope: paper-source review, direct GEO catalogue intake, six proposed local
branches, source-reproduction owner and current repository navigation.
The provided PDF hash and public source access are recorded in
[the manifest](SOURCE_MANIFEST.md). Figure 2 and the Figure 6 legend pages
were rendered and visually inspected; no new scientific figure was produced.

Remaining inputs: exact per-cell/preparation maps, original normalized matrix,
numerical supplements and assay-level data, historical Compass/Recon2 settings,
qualified CPLEX runtime/license and stage-specific frozen contracts.
Historical results, policy, validators, claims, canonical questions and frozen
artifacts must remain unchanged. Server protection and host access are not
re-audited or established by local validation.


## Checks completed

| Check | Result |
|---|---|
| Repository artifact/link validator | Passed 9,572 checks |
| Claim contract | Passed 18 numeric bindings |
| Nb1 output verification | Passed |
| Nb4 archived evidence | Passed |
| A16 archived Stage 1 evidence | Passed |
| A23 external evidence | Passed |
| A22/A23 extension evidence | Passed |
| Unit-test discovery | 143 tests, OK with one skip |
| Python source compilation | Passed; bytecode cache directed outside the worktree |
| Research gate with `--base origin/main` | Passed, no errors |

Commands match REPRODUCIBILITY.md and the two existing CI workflows. Full test
logs are retained in this chat's private scratch workspace. No new scientific
code was introduced and no biological pipeline was rerun. A skipped test and
passing infrastructure checks do not establish an installed Compass runtime.

The targeted integration audit also confirmed seven unique Wg owners with
resolving plan/evidence paths; all prior registry questions, candidates, guides,
contracts and receipts are unchanged. All other paper records and both reading
sequences are unchanged. The 23 changed paths consist of 21 Markdown documents
and two navigation/registry JSON files. Registry line endings were restored to
the existing LF convention before final staging; no schema or validator changed.

The initial Git fetch and worktree write needed sandbox permission; both
succeeded with scoped escalation. Browser source challenges were resolved for
GEO catalogue text only, as recorded in the manifest. There were no failing
repository checks. The final documentation-record update is followed by a local
link/artifact validation and whitespace check; the already-passing numerical
archive verifiers and test suite need no repeat for that prose-only update.

## Delivery state

Prepared on local branch `codex/wagner-th17-plan` in the isolated managed
`wagner-th17-plan` worktree. The primary checkout's previously reported edits
and private content remain present and untouched. No push, pull request, merge,
Notion edit or external setting change is part of this delivery.
