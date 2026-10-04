# Pre-RQ checkpoint validation — 4 October 2026

Current source-aligned RNA run: [receipt](../../analysis/research/runs/wg_bulk_limma_v1/receipt.json),
frozen at `5a50fb8`. Remaining-stage source qualification and failure archival:
[receipt](../../analysis/research/runs/wg_closeout_qualification_v1/receipt.json),
frozen at `3de0860`. Neither successful receipt grants scientific acceptance.

- Independent weighted least-squares solves cover 113 predetermined genes per
  series across all contrasts. Coefficient/SE discrepancies are at most
  6.04e-14/1.15e-14. All-gene moderated t-tail, BH and interval arithmetic passes
  frozen tolerances. [Verification](../../analysis/research/runs/wg_bulk_limma_v1/verification.json).
- Both new article plates were visually inspected: readable axes, conditions,
  counts, group symbols and non-overlapping captions. PNG/PDF/SVG exports and
  combined PDF are saved. Older outputs were not overwritten.
- Nine historical code/metadata files match Git object and SHA256 identities;
  the metadata ZIP passes CRC. All 12 ATAC SOFT labels independently match R0.
  These checks do not execute the held Compass, ATAC or functional analyses.
- All twenty failed-run files match their archive copies, their still-present
  local originals and their bytes at commit `30bf90d`. The three copied receipts
  retain `execution_failed`. Earlier numerical failure and missing outputs are
  not concealed. [Mapping](../../analysis/research/runs/wg_closeout_qualification_v1/failure_preservation.json).
- Preservation follows the already-existing
  [Nb5 contract](../gate2_N4_nabhan_aging_atlas_2020/config/failed_run_preservation_v1.json).
  Duplicate original paths are ignored/untracked locally after archival; no
  original file is deleted. The successful preservation receipt replaces the
  three unsuccessful registry entries. Frozen source contracts remain registered.
  No schema, validator, historical baseline, infrastructure allowlist or failure
  status was changed. Earlier statements below that a governance change/review
  was the only integration route are superseded by this existing-workflow finding.

Final repository/integration checks: **passed** against refreshed `origin/main`
`a5d41834395cac0b82b488d48759ceb6fab8f2d5`.

| Check | Result |
|---|---|
| Research gate against main | Pass, zero errors; prior five integration errors resolved through the existing preservation pattern |
| Repository links/artifacts | 9,848 checks passed after final prose and gallery navigation updates |
| Evidence/provenance unit tests | 143 tests passed, one existing optional-runtime skip |
| Source compilation | Passed across analysis, article and RQ directories, excluding ignored runtimes |
| New staged output byte audit | All 55 receipt-bound outputs exactly match staged Git bytes, including PDF/SVG and archived failure files |
| Whitespace check | Passed with scoped exact-byte attributes for frozen generated files |
| Six unchanged claim/archive check groups | Earlier passes reused after an empty scoped diff from `30bf90d`; main unchanged. These are the 18 claim bindings plus Nb1, Nb4, A16, A23 and A22/A23 archived verifiers |

Original planning checkout is clean at `1527bea`; the primary checkout retains
exactly its two prior metadata-file modifications. Protected research rules and
legacy baselines are unchanged.

New RNA statistics and current registration were checked; unchanged historical
biological analyses were not rerun. No push, PR or merge is performed.

The following records are historical checkpoints, not current pending-job lists.

# Historical R3 and caption validation — 4 October 2026

The current R3 qualification, numerical v2 and layout-render v1 receipts all
verify. The refreshed integration base remains
`a5d41834395cac0b82b488d48759ceb6fab8f2d5`. Original and primary checkout
preservation checks confirm only the primary's two pre-existing metadata edits;
the original planning worktree remains clean.

- Four synthetic qualification tests and two current paired-arithmetic tests
  pass. They cover duplicate identities, incomplete technical pairs, metadata
  conflicts, invalid matrices, genotype aliasing, fractional count aggregation
  and animal pairing independent of row order. New-code compilation passes.
- All four gzip files match GEO's advertised sizes and pass CRC validation.
  All 128 matrix-column occurrences match source records; independent parsers
  agree on all values. Exact rational and SVD model ranks agree.
- Independent scalar calculations match current expression normalization and
  paired differences to at most 1.60e-14 (frozen tolerance 1e-10); PCA singular
  values agree with Gram eigenvalues. These are numerical checks, not biological
  replication or exact historical limma reproduction.
- Both RNA PNG plates were visually inspected. The current Figure 4 render
  separates its x-label and legend. Figure 5 is pixel-identical to the inspected
  original. PNG/PDF/SVG and combined PDF outputs are saved; original numerical
  and graphical evidence remains immutable.
- The added Figure 3 caption matches all 14 frozen d/q rows at its declared
  rounding. Existing R1 PNGs and numerical outputs are unchanged. Figure 5 now
  has a separate gallery table defining both axes, CPM, the offset, group labels,
  animal dots, means and unequal panel scales; Figure 4 defines PC scores and
  explained variance.
- The repository link/artifact validator passes. Seven unchanged check groups
  (claim bindings, five archived-evidence verifiers and repository unit tests)
  retain their documented R1 passes; their code/inputs and main base did not
  change. New source compilation and current run checks were performed. No
  biological analysis was rerun for caption or layout updates.

## Current integration hold

The research gate reports exactly **five** errors, all confined to preserved
failed attempts: unsuccessful receipt plus incomplete output list for R1 v1;
unsuccessful receipt for R1 v2; unsuccessful receipt plus incomplete output
list for R3 descriptive v1. The latter stopped at literal gene-name matching
before any biological contrast. Its explicit source-case correction is
[documented separately](BULK_AMENDMENT_v2.md); current R3 v2 passes.

No gate/schema/allowlist, failed status or scientific acceptance was changed.
Integration remains pending explicit review of failed-run retention handling.
The current successful receipts do not erase failed evidence. No push, PR or
merge was made. Logs are in this session's private scratch `validation_r3/`;
hash-bound execution checks and results are linked from [BULK_RESULTS.md](BULK_RESULTS.md).

# Historical R1 numerical and figure validation — 4 October 2026

The current numerical and figure receipts verify successfully. This establishes
execution provenance and the declared numerical calculations, not biological
replication, exact manuscript reproduction or scientific acceptance.

- R1 v3: 6,373 reaction, 1,722 group and 6,353 expanded-row checks pass.
  Rank-sum U agrees exactly; maximum p/q discrepancies are 6.66e-16/7.77e-16.
  Transformation residual is 3.55e-15; effect-size tolerance remains as frozen.
- The ten numerical result/environment files match v2 byte for byte.
  Five targeted calculation tests pass; the separate R0 tests remain valid.
- Figure v2 receipt passes. Four PDF pages were rendered; corrected plates
  1/2/S1 were inspected. Plate 3 is pixel-identical to the previously inspected
  render. Labels, scales, counts and legend spacing are readable. All four
  plates have vector PDF/SVG and 300-dpi PNG versions plus full captions.
- Eight unchanged repository check groups pass, including 143 unit tests with
  one existing skip, 18 claim bindings, all required archived-evidence verifiers,
  and source compilation. New figure code is compiled separately after its edit.
- Main was refreshed and remains `a5d41834395cac0b82b488d48759ceb6fab8f2d5`.
  Final link/artifact validation passed **9,684 checks**. Nine of ten required
  check groups pass; the integration gate reports exactly the three failures
  below. New figure-code compilation also passes.

## Final integration-gate result

1. `wg_source_scores_v1/receipt.json`: execution unsuccessful.
2. `wg_source_scores_v1/receipt.json`: expected output list incomplete after the failed join.
3. `wg_source_scores_v2/receipt.json`: execution unsuccessful after numerical verification failed.

There are no other reported gate errors. Numerical v3 and figure v2 are successful
and verify independently; the integration gate remains **failed**, not waived.

## Failed-run preservation and integration review

The runner correctly saved v1/v2 as failed. The current registry validator only
accepts successful receipts. Registering those preserved failed attempts therefore
causes an integration check failure even though the current numerical and figure
runs verify. The records remain honest; no gate, schema, allowlist or failed
status was changed to make this work pass. Integration is pending explicit
review of how failed attempts should be registered and hash-checked separately
from successful scientific executions. Deleting failed evidence is not a fix.

Frozen SVG output contains Matplotlib path whitespace, and the first generated
caption file has a terminal blank line. Scoped Git attributes preserve those
exact hashed bytes. This formatting treatment does not change scientific
validation. PDFs are explicitly staged despite the repository's global PDF
ignore rule so a checkout retains every receipt-bound figure.

Logs and rendered QA images are in this chat's private scratch workspace under
`validation_r1/` and `figure_qa_v2/`. Earlier checkpoint validation below remains
historical and must not be read as the current integration status.

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
