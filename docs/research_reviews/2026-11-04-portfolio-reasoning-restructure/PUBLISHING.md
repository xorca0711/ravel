# Reviewed RQ restructuring: integration and publication

4 November 2026. The owner authorized committing and pushing the reviewed
restructuring/fixes and opening a pull request. This supersedes the earlier
documentation-only delivery restriction; it does not authorize a new analysis
or merging the resulting PR.

## Integration scope

The publication worktree is
`X:/GitHub/ravel/.worktrees/rq-reasoning-pr-20261104`, on
`codex/rq-reasoning-restructure-20261104`. The original C: review worktree,
including its unrelated and ignored work, is preserved.

Main was refreshed at `acefbced7fd073f4f29ea265468aca640e1ded4c`. PR #163 had
merged into its former side branch, not main. The current narratives depend on
that reviewed screening history and on four subsequently reviewed descriptive
analyses (A3, A5, A27, A31), including A5's separate display-only revision.
Publishing documentation alone would leave missing evidence and provenance.

- `1b7049c` merges current main into the preserved research history. The sole
  PROGRESS conflict retained both dated records; the current synthesis then
  supersedes their old execution status. Governance files match main.
- `57f6dea` commits the reviewed evidence dependencies separately: reports,
  public-source preparation records, five receipts and their frozen outputs,
  source-navigation updates and registry evidence links. No computation reran.
- `0bb57ef` covers all 33 README/context/dossier narratives,
  collection navigation, rationale review, validated A3/A9 corrections and
  current-versus-historical work routing. Registered hypotheses, artwork,
  adverse results and scientific acceptance states remain unchanged.

## Validation

Before export, 253 selected pending files were copied byte for byte into the
isolated worktree. The two pending guidance files already equalled merged main
and were not reintroduced as policy changes. A separate commit audit verified
76 receipt-bound Git blobs with zero mismatches, including all 33 declared new
outputs; two source inputs remain external and are not represented as committed
raw data. Existing source-level scientific reviews are reused.

The original review records 16,449 repository checks, the provenance gate,
224 preserved sections and all 33 hypothesis/image pairs. Fresh isolated-tree
validation on `0bb57ef` passed:

- **16,450 repository checks**.
- **170 unit tests**, with the Windows-specific symlink test skipped; Python
  compilation, claim-manifest verification and every required archived-evidence
  verifier also passed.
- Research provenance and changed-asset gate against `acefbced`: zero errors
  after the checkout-byte repair described below.
- All 33 registered guides and image hashes agree with the reviewed source.
  All 255 pending source-file contents remained unchanged during export.

The first fresh-checkout gate reported 23 hash errors from **14 historical files**.
Each discrepancy was proven to be line-ending-only. The original Git blobs
matched the frozen receipt hashes and were restored locally byte for byte; the
gate then passed. There is no Git content change to these files and no altered
contract, expected hash or validator. Git's Windows conversion setting can still
display these local byte restorations as modified; they are intentionally not
restaged. The initial locked-output download also encountered sandbox DNS/temp
restrictions; the authorized retry verified all 16 published members and restored
15 absent files, without an analysis rerun.

Logs and export/hash manifests are retained under
`C:/Users/dream/AppData/Local/Temp/ravel-pr-publish-0q8uhfyd`. Final publication
metadata changes only documentation and receives scoped link/whitespace checks;
already-passed scientific checks are not repeated for those metadata edits.
The PR description records these results and the exact dependency scope. No
successful technical check confers scientific acceptance or resolves a missing
biological measurement, and the PR remains subject to review rather than an
automatic merge.
