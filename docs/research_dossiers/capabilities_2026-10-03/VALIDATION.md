# Capability-stage validation

3 October 2026. Documentation/registry-link revision on the repair branch, checked against refreshed `origin/main` at `0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`. The pre-revision PR HEAD was `6b9ce9ee94dc043411df5dd18c666fd474d59f7f`. GitHub checks must also succeed at the final pushed revision.

## Required local checks

Commands follow the repository workflows; no biological pipeline was replayed.

| Check | Result | Log SHA-256 |
|---|---|---|
| compile | Passed | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | Passed | `0cdfeb98da484305d0d8f4797dfd14978abf1410bcfc82b1edc302746db0734b` |
| claim_contract | Passed | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | Passed | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | Passed | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | Passed | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | Passed | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | Passed | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | Passed | `5ad70711fc6892fa23128e408384377b76465b4c5933a92124a136dd8dad264c` |
| research_gate | Passed | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

Unit-test output reports 123 tests and 1 skips. Logs are retained privately; hashes identify the exact output. No new test was added for these documentation-only changes.

## Documentation, source and preservation checks

- 280 local Markdown reference paths resolve across the new stage, dossier entries and current navigation.
- All 32 corpus IDs are represented once; original PDF SHA-256 values were rechecked unchanged. The inventory totals 677 pages.
- Registry retains 24 RQs, nine Nb4 candidates, nine contracts and eight successful receipts; the separately archived failed A5 attempt is retained.
- Tracked edits are documentation and registry links only; no frozen scientific code, outputs, contracts or receipts changed.
- Public stage documents contain no local private-planning paths or Notion page references. Full PDFs, extraction caches, funding snapshots and the private lab comparison remain outside Git.
- The main agent reviewed the eight-lab comparison, including its model attribution, access caveats and source limitations. A targeted check corroborated the DuPage publication acknowledgement/material-transfer limitation and the Saxton PDF page correction.
- Repository validation and the research gate check current references and historical integrity; passing them does not certify scientific novelty or assay validity.

## Current-state limits

PR130 remained open/not merged at the refreshed pre-edit check; main was unchanged. The normal checkout and older worktrees were not modified in this revision. Their prior preservation record remains in [CHECKOUT.md](../followup_2026-10-03/CHECKOUT.md); the normal checkout may lag the new PR tip and must be inspected before later consolidation. The owner retains review/merge. Full hypothesis packages and actual lab access remain pending as recorded in [NEXT_STEPS.md](NEXT_STEPS.md).
