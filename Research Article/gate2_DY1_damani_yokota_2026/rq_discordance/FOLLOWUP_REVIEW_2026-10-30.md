# Independent technical review of DY1 follow-ups

30 October 2026, Asia/Seoul. The owner authorized execution through the existing
technical chat after the [feasibility assessment](FOLLOWUP_FEASIBILITY_2026-10-30.md).
The coordinating reviewer inspected each numerical package before execution and
checked the saved results independently afterward. Technical review is complete;
human scientific acceptance and canonical RQ promotion remain unassessed.

## Integration and disposition

Reviewed handoff `cee8466dc82bbf4ce3a12e840cd575b55864c7f8` was integrated from
`codex/dy1-followup-execution-20261030`. It descends from feasibility handoff
`8faecedbea928b6c8d7f7eeea27d95f398a1a00d` and merged main
`28fb61015f9b921f591e41ff26010a960c305947`. The source worktree retains its ignored
input caches; no frozen source, output or script was replayed or overwritten.

| Follow-up | Disposition | Evidence |
|---|---|---|
| F1 representation | Executed and reviewed | [Frozen receipt](../../../analysis/research/runs/DY1_P02_representation_audit_v1/receipt.json), freeze `757d03f` |
| F4 cofactor reference | Executed and reviewed | [Frozen receipt](../../../analysis/research/runs/DY1_P02_genotype_reference_v1/receipt.json), freeze `2f74c6c` |
| F2 human robustness, including external component reaggregation | Executed and reviewed | [Frozen receipt](../../../analysis/research/runs/DY1_human_panel_robustness_v1/receipt.json), freeze `446b023` |
| F3 paired source | Bounded public-source assessment complete; numerical work held | [Source/model note](FOLLOWUP_SOURCE_MODELS_2026-10-30.md#f3-bounded-public-qualification): controlled FASTQs; analysis-site timeout; files, rights, paired barcodes, preparation identities and common-state support unqualified |

The [results report](FOLLOWUP_RESULTS_2026-10-30.md) owns all findings and limits.
The original E1–E6 dispositions and original NAM measurement/mediation holds are
unchanged. Existing A1/A2/A8/A14/A19/A22 context notes link here without creating
new canonical numerical outputs or changing their hypotheses or decisions.

## Pre-execution decisions and corrections

- **F1:** reviewed the contract, code and four synthetic tests. Equal-gene
  weighting averages all mapped within-gene fractions, retaining zero directions
  and mixed ATAC signs. Both mappings resolve to the same RNA identifier namespace.
  Common-region joins, independent scalar counts and old E2 parity are required.
  Cleared without a code change.
- **F4:** reviewed the contract, exact sample parameters, source/model note, code
  and four tests. Separate within-condition cKO-minus-WT contrasts use actual n
  and unequal-n Welch intervals under explicitly conditional assumptions. A common
  four-group feature universe retains condition-specific all-zero rows. Cleared
  without changing the numerical design; no interaction or paired design invented.
- **F2:** reviewed the contract, external cache/direct-raw-audit lineage, original
  donor/site/floor selections, full-result parity and every omission. Required two
  corrections before freeze: reject nonfinite components instead of pandas'
  implicit missing-value averaging; mark comparisons to an undefined full
  reference unavailable instead of reporting zero sign reversals. Six tests,
  including both failure modes, passed before execution. No output-driven panel
  or donor choice was made.
- **F3:** corrected the source note to distinguish the SUMseq preprocessing
  project from `sum-seq_analysis`, the explicit analysis/files repository. The
  exact latter URL timed out in the bounded check. Failure to access it does not
  establish that public processed matrices are absent.

F4 had two draft parameter-file hash preflight failures before its final LF-byte
correction. No governed run had been created. The repository test suite initially
hit Windows sandbox temporary-Git creation/cleanup failures; its authorized retry
passed. These are recorded in the results history, separate from biological
failures. All three governed runs completed successfully. No gate was weakened.

## Independent post-run verification

These are verification calculations on reused data, not biological replication.
The parent did not import the new analysis scripts to produce the checks below.

| Job | Independent parent verification | Provenance checks |
|---|---|---:|
| F1 | 22 arithmetic/partition checks: reconstruct all four weighting summaries and both common-support comparisons directly from frozen E2 effects/membership, with scalar dictionaries | 18 input/code/output/contract/freeze checks |
| F4 | 447 checks: original sample selections; complete feature-universe and condition-zero flags; 17 fixed source-order features per assay/condition using scalar logarithms, means, SDs, SEs and intervals; all mapped sign/rank summaries | 24 input/code/output/contract/freeze checks |
| F2 | 2,897 checks: reconstruct all 1,195 rows and their n/status; all omission summary counts/ranges; unavailable-reference handling; all eight external components for 42 donor/population rows from the prior direct raw-count audit | 27 input/code/output/contract/freeze checks |

All checks passed. The 69 provenance checks include repeated input entries and
compare current code to each freeze commit; they are not 69 independent sources.
The implementation's separate verification records contain 429,215 F1, 1,458 F4
and 2,493 F2 checks. Those totals are not statistical sample sizes.

All three figures were inspected. F4 and F2 are readable. F1's long x-axis labels
are crowded; its exact table is the primary presentation and its frozen plot is
supplemental, not presentation-ready. No cosmetic overwrite of frozen evidence.

## Interpretation review

F1's +0.196 to +0.396 percentage-point shift bounds only unequal region weighting
under the saved mappings. It does not resolve normalization, cell mixture or
regulatory assignment. The two mappings largely coincide on common support;
agreement between their summaries is not independent annotation validation.

F4's weak mapped-row correlations describe this exposed feature universe. They
do not disprove specific regulation, establish an absence of genotype effects,
validate the NAM axis or test a 50% null. Baseline context is not an interaction;
conditional intervals retain their independence/normality and source limitations.

F2's stable matrix-associated direction under single omissions supports robustness
of that RNA summary only. The primary FABP4 estimate already had an interval
spanning zero; omitting its FABP4 component changes its sign. External IPF panel
correlation remains imprecise despite negative omission estimates. Deterministic
omission stability does not narrow original sampling intervals or establish
transport, secretion, repair, receptor response or ARG1 mediation.

The closest source comparisons and October 2026 literature access limits remain
in [LITERATURE_CONTEXT](LITERATURE_CONTEXT.md). No new mechanism, experiment
package, literature-exhaustion claim or human retain/reject decision was created.

## Validation and preservation

The technical handoff passed 14 targeted tests, 161 repository tests with one
skip, compileall, required existing evidence verifiers, 11,702 repository checks
and the research gate against freshly fetched main `28fb610`. The two initial
preflight failures and environmental test retry remain documented. Reviewer
README/context changes add no biological rerun; integrated documentation checks
are recorded in PROGRESS.

All numerical artifacts remain article-local/centrally registered under DY1-P01
or DY1-P02. Canonical question records, guides, protected governance/validators
and previous frozen evidence remain unchanged. Only the existing six RQ context
notes receive dated pointers; no numerical results are duplicated into them.
Source caches in the technical worktree must be preserved before any retirement.

**Next:** no eligible numerical job remains queued in F1–F4. F3 requires qualified
access/files/identities; original NAM effects, within-state ATAC, temporal memory,
ARG1 mediation and recipient function retain their distinct evidence requirements.
