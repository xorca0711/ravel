# Recovery scope after the technical chat stopped

31 October 2026. The owner requested a replacement technical chat, continued
coordination, review of saved results and a disposition for every planned step.
This record narrows the replacement to data integrity, source/endpoint review and
documentation. It does not authorize replaying blocked biological execution.

## Observed failure and preserved evidence

The original technical chat `01a19140-3fcb-7012-9c02-b8744eab73c7` reports
`systemError`. Both its initial execution turn and the subsequent “proceed” turn
ended with an explicit biological-content safety restriction. The service did
not identify the triggering item. This was not a filesystem approval timeout,
missing dataset or model-fit failure. Do not label it as any of those conditions,
retry the same execution in another chat, remove scientific context to disguise
the request, or claim that the restriction has been lifted.

The original checkout and ignored caches remain intact at
`C:/Users/dream/.codex/worktrees/saxton-il22-execution-20261031/ravel`.
Committed handoff `ff09fab3fb37fd4bf915845e5cd59effaa386210` contains source
qualification, the frozen R1 metadata contract, code and synthetic tests.
The R1 v2 run had completed successfully but its output directory was untracked
when the chat stopped. The review branch merged the committed work, copied all
three declared inputs and eight run files byte-for-byte, registered the receipt,
and verified its hashes successfully. No biological contrast was rerun.

The saved [receipt](../../analysis/research/runs/sx22_r1_v2/receipt.json) identifies
the original execution commit, inputs, code and output hashes. Its acceptance and
verification fields remain the original execution record; later review belongs
in a separate report. The [summary](../../analysis/research/runs/sx22_r1_v2/summary.json)
reports six columns, 35,275 gene rows, no duplicated Ensembl IDs, 52 duplicated
nonempty symbol entries and 12,935 all-zero rows. These are input/QC facts, not
treatment results. There are no saved R2/R3 treatment estimates to review.

## Permitted replacement work

1. Independently verify the saved R1 receipt, file integrity, table dimensions,
   identifier diagnostics and metadata joins. Use source-reported replication
   honestly; separate BioSamples do not independently certify separate mice.
   Technical format/count checks are allowed; do not calculate biological effects.
2. Review the source audit against the actual PDF figures and legends. Preserve
   discrepancies and correct documentary mistakes with an explicit supersession
   note. Raw curve/animal values, missing keys and unavailable supplements remain
   specific source limitations, not an invitation to infer hidden values.
3. Complete the source-only parts of E1/E2 using existing repository qualification
   records and the already documented literature. Establish what fields/endpoints
   a candidate source actually supplies. No receptor-response scoring, new
   treatment models, dose-response fitting, variant ranking, functional-effect
   estimation, target prioritization or molecular design is part of this recovery.
4. Produce a results/hold ledger and gallery index of the existing metadata/QC
   evidence. A clearly labeled metadata/QC visualization from frozen summaries is
   permissible with the repository's rendering provenance; it must not imply
   treatment effects or biological validation. Do not manufacture biological
   figures to complete the gallery.
5. Update the article README and PROGRESS, retain all original plans/contracts,
   run targeted mechanical checks, and return a local committed handoff for the
   originating chat's independent review. Do not publish or contact authors.

The replacement should stop and report if it encounters the same content
restriction; do not create a chain of replacement chats. This limited scope is a
substantive change of work, not a rephrasing of the blocked execution.

## Reviewer observation requiring reconciliation

The source audit repeats a labeling mismatch from the published Figure 5 legend.
In the supplied final PDF p. 8, the receptor qPCR bars are **panel H**, while **F
and G** show HepG2 immunoblots. Panel I is the receptor-expression comparison.
The legend calls the qPCR panel F and refers to HT-29 where the figure labels
HepG2. Do not silently treat H as a blot or F as qPCR. This is a source-location
correction, not a new signaling result. The Fig. 7 G/H organ-label discrepancy
reported in the original audit also needs source-location review.

## Required status distinctions

| Status | Meaning |
|---|---|
| Completed execution | An actual immutable run or source-review artifact exists |
| Reviewed | A separate review identifies what was checked and any surviving limitations |
| Data/design hold | The exact absent measurement, identifier, source file or design feature prevents the stated inference |
| Platform-policy execution hold | The blocked biological execution has not been resumed; the error does not identify a more specific cause |
| Not assessed | The work has not been done; it must not be disguised as a confirmed data limitation |

R2/R3 currently have a platform-policy execution hold, not a missing-count-file
hold: the count and metadata files were recovered. Source-reported n=2/group,
absent separate mouse/batch identifiers and annotation uncertainty remain
scientific limitations independently of platform status. R4/R5 additionally need
qualified raw measurements/replicate keys for stronger numerical reconstruction.
E1/E2 source assessment may finish while their numerical or mechanistic extensions
remain unexecuted. The final README must keep those two levels separate.

Completion of this recovery means every permitted source/documentation task is
reviewed and every original step has an accurate disposition. It does not mean
the original biological sequence executed or the paper was fully reproduced.
