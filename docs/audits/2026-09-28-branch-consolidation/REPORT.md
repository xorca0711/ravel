# Branch consolidation review, 28 September 2026

The owner requested reviewing all remaining branches, retaining appropriate
unique work, then deleting branches so only main remains. The review began
at main `4cba769` after fetching and pruning remote references.

| Branch at review | Tip | Work absent from main | Decision |
|---|---|---|---|
| codex/england-analysis-plan | `5474ede` | Three commits: `53f9699` A16 plan, `be3ffe3` Stage 1, `5474ede` control-count correction | Merge with dated interpretation corrections; retain original scientific evidence |
| codex/england-rq-reframing | `fe87448` | None; included by PR #104 | Remove merged branch reference |
| codex/computational-research-pipeline (local only after prune) | `0b7946e` | None; already an ancestor of main | Remove stale local branch reference |
| Claude/docs-residue-and-figure-gallery (local only after prune) | `53fb600` | None; already an ancestor of main | Remove stale local branch reference |

The new [A16 integration review](../../../RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md)
explains why the results are useful exploratory evidence and why the original
ambient/threshold exclusions and position-independent interpretation cannot be
adopted. The original contract, two scripts, tables and reports are retained.
The current README and shared register carry the corrected interpretation.
The two register conflicts are resolved by retaining main's source audit and
adding the new execution status, rather than restoring pre-audit premises.

The [A16 verifier](../../../RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py)
checks archived hashes and reconstructs key summaries from saved tables. It
does not rerun the raw-data analysis or validate a biological mechanism.
Repository-required checks and PR CI remain the integration gates.

The England source worktree contains staged, unstaged and untracked work beyond
the committed branch. It is not merged automatically, reset or deleted. Its
worktree and recoverable Git state are preserved when removing branch refs;
other completed worktrees can likewise remain detached. The unrelated
`docs/audits/2026-09-28-rq-adversarial-review/` in the primary checkout stays
outside this merge. This operation does not discard caches, drafts or stashes.

Local validation passed: compilation; 53 repository tests (one existing skip); 18 numeric claim bindings; Nb1 provenance; repository links/artefacts; and 1,867 A16 archived-evidence checks. The original A16 files, except its current README, are byte-identical to source commit `5474ede`.
