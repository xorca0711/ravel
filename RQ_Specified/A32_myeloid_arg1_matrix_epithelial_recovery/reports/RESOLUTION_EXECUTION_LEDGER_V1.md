# A32 resolution screen: execution ledger

3 November 2026. Base main `445a0ca`; branch `codex/a32-resolution-screen-20261103`. Coordinator owns PROGRESS and final integration.

## Completed work

- Metadata contract/code frozen at `7132cc0`; [recovery receipt](../../../analysis/research/runs/A32_resolution_metadata_v1_20261103/receipt.json) executed and verified. Bounded native-R recovery preserved 45,311 unique cells, 41 source labels and 36 capture+HTO mice. Original RDS retained; stripped assay payloads never used as expression.
- Expression contract/code frozen at `f63050d`; [screen receipt](../../../analysis/research/runs/A32_resolution_context_v1_20261103/receipt.json) executed and verified. Fourteen predeclared genes, ten source myeloid labels, fibroblasts, AT1/AT2 and composition-sensitive AM_all context. Cell floor ten and complete 3-versus-3 comparisons were fixed from metadata before gene outcomes.
- Every retained cell in all six raw captures matched barcode, original RNA UMI total and detected-feature count exactly. Native R independently read original YoungD14 MatrixMarket data and matched all 306 state/gene/mouse summaries; it also checked all 306 contrast statuses.
- The native verifier's “88 intervals” line means 88 estimated-contrast uncertainty policies: 76 nondegenerate pointwise Welch intervals and 12 zero-variance cases with NA bounds/df. Frozen output wording is preserved. Coordinating chat independently passed 4,308 support/endpoint/arithmetic checks (reported maximum difference 3.67e-15).
- All three measured PNGs inspected by technical and coordinating chats; labels, unsupported gray rows, secondary context and individual-mouse warning retained. [Full report](RESOLUTION_CONTEXT_RESULTS_V1.md), A32 README, literature context and dossier updated; registry binds both receipts and current evidence.

## Findings and retained limits

There are 88 estimated and 218 unestimated planned contrasts. Epithelial effects
are unestimated: only 22 AT1 and 130 AT2 cells overall. Fibroblast complete
support occurs only in young D14. Early BLM AM2/AM3 carry much of the observed
Arg1 RNA, including normalized RNA, but sparse PBS cells prevent within-state
induction estimates. Young-D14 Col1a1/Col3a1/Fn1 RNA changes coexist with myeloid
observations; this is not deposited collagen or ARG1 mediation. The late young
AM1 Arg1 signal has only 2–5 UMIs per BLM mouse, not a maintained programme.
The joint resolution question remains unanswered. Canonical A32 functional and
Speth access holds, hypotheses, illustrations and claim grades are unchanged.

## Verification and runtime

Passed focused R recovery fixtures and Python arithmetic/support fixtures;
required Python compilation; 170 repository unit tests (one skipped); claim
manifest and Nb1/Nb4/A16/A23/A22–A23 evidence checks; both receipt verifications;
research gate `check --base origin/main`; repository validation (15,249 checks);
tracked handoff patch whitespace check. Fresh fetch confirmed main remains `445a0ca`.
No biological run failed or was restarted; unfavorable/unsupported outcomes
remain. The independent R check was slow because it repeatedly subsets triplet
sparse data; its original frozen run was retained, not edited or duplicated.

Actual runtime: Python 3.12.13 AMD64, NumPy 2.4.6, pandas 2.3.3, SciPy 1.18.0,
Matplotlib 3.11.1; R 4.6.1 (2026-06-24 ucrt), Matrix 1.7.5. R locale startup
warnings were retained in logs; exact counts/IDs/arithmetic passed. Versions
were read in the same authorized runtime context used for execution.

The coordinator's full Git-index review subsequently found eight immutable
trailing-space warning lines: `stderr.log` lines 2-5 in each metadata/expression
run. They are preserved as execution history, with no validator/attribute
change. All 22 staged output/code/contract hashes match the frozen receipts;
see the [integration review](../../../docs/research_reviews/2026-11-03-primary-candidate-literature/A32_COORDINATOR_REVIEW.md#integration-checks).

## Handoff and exact next step

Return registry/A32 paths to the coordinator for final integration. Only the
two prospective freezes were committed here; no result-deposit commit, push
or PR was performed. All eleven expression receipt outputs exist and none is
ignored; the result run directory is currently untracked and must be included
with its receipt and logs in the coordinator's final commit. Final result
pages/ledger/registry edits remain reviewable in the working tree alongside
untouched coordinator-owned changes. Metadata outputs are already in `f63050d`.

No new external settings, controlled-access application, contact, paid compute,
user-app closure or system-memory change occurred. The initial coordination
message review rejection was resolved by the user's explicit destination-specific
authorization; subsequent coordination succeeded. No scientific acceptance or
human retain/reject decision was created.
