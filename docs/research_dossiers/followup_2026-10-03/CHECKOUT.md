# Normal checkout consolidation

The normal checkout now uses `codex/workspace-ready`, a separate review branch
containing PR #130. The local `main` reference was left at its original revision
until owner integration. The repair worktree remains `codex/research-governance`.
Neither main nor the PR was merged by the agent.

## Preservation and verification

- Original primary HEAD: `33b27cf1f03da706ee987f3fd00b7127eaaff79e`.
- All 686 original changed/untracked files were verified against the exact private archive before checkout.
- 685 non-private paths were committed to local-only `codex/preserved-primary-20261003` at `220063ede1d998ae8852cd6be51934d9c82004c4`. This branch is not pushed or merged into the repair branch.
- The remaining private settings file was verified unchanged. The nested checkout's HEAD remained unchanged.
- 62,350 ignored files (77,914,694,712 bytes) were preserved in place. Every inventoried file retained its size, modification time and file identity after checkout. This is preservation verification, not a new content-hash backup of raw data.
- No target tracked path collided with the inventoried ignored paths. Checkout used the no-overwrite-ignore protection. No reset, clean, stash or forced checkout was used.
- The primary tracked tree was clean after switching. The original archive and Git bundle remain private recovery evidence.

The sandbox and full user Git environment differ only in whether the private
settings file appears as untracked: the latter can read its global ignore rule.
The consolidation compared all other status entries and verified the file's
bytes independently, rather than treating that ignore difference as new work.

## Retained worktrees

All nine older non-primary worktree HEADs and status entries still match the
preservation checkpoint (ignoring only that private-file visibility difference).
They are retained. Existing per-file reconciliation in the [repair report](../../audits/2026-10-03-repository-repair/REPORT.md)
continues to govern unique work and superseded interpretations. A clean tracked
tree is not proof that ignored inputs can be deleted.

| Worktree | HEAD | Tracked changed files | Disposition |
|---|---|---|---|
| a22-ci-reconcile | `7024e1a007e1` | 0 | Retained; preserved state unchanged |
| england-analysis-plan | `5474ede1868f` | 49 | Retained; preserved state unchanged |
| england-rq-reframing | `d47bb8b198d0` | 0 | Retained; preserved state unchanged |
| nabhan-2023-plan | `0a1c1d1fe421` | 0 | Retained; preserved state unchanged |
| nb3-rq-review | `7030706af513` | 0 | Retained; preserved state unchanged |
| nb4-lung-atlas | `f1967e6bdd1e` | 0 | Retained; preserved state unchanged |
| rq-gap-fill | `a29e8fd8a0e0` | 0 | Retained; preserved state unchanged |
| rq-rationale-audit | `0b7946eba7f7` | 0 | Retained; preserved state unchanged |
| sharp-margulis-5e858e | `fee907165d9f` | 0 | Retained; preserved state unchanged |

The `england-analysis-plan` and `england-rq-reframing` working files retain their
prior private snapshots and reconciliation decisions. Clean older tips may
still carry ignored datasets or useful history. Retirement is deferred until
the needed inputs have a verified destination and the owner has integrated the
reviewed state; this stage does not describe them as redundant storage.

## Continuing after review

Use the normal checkout for future work after verifying its branch/HEAD and local
changes. Metadata inputs needed by the new receipts are retained under ignored
raw_data; successful verification does not require publishing raw inputs.
After the owner merges the PR, fetch main and reconcile the review branch by a
safe fast-forward where possible. Preserve new article files or other local work
before any branch change. Do not revive the recovery snapshot as current main.

Final local/remote checks and the review-branch handoff are recorded in
[VALIDATION.md](VALIDATION.md). Raw-data backup and old-worktree retirement remain
separate storage decisions, not hidden deletions in this repository repair.
