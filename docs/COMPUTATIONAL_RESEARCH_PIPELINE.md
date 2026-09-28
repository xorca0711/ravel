# Computational pipeline for remaining research gaps

**Synchronized 28 September 2026.** A11 C0–C5 and its diagnostics are complete;
the [current A11 report](../RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md)
governs interpretation after identity adjudication. A5 recovery (C6-audit-followups)
and the three-candidate A12 audit (C9) are now complete with data gates. C7/C8
and C10 remain blocked; no independent validation score has run. C11 status
synchronization is complete. The [queue](research_pipeline/queue.json) records
these states and the [global gap-fill ledger](roadmap_runs/2026-09-28-gap-fill/RESULTS.md)
covers the additional A15–A18 work. No scientific job is running.

The [handoff](handoffs/2026-09-27-computational-research.md) holds exact paths, sources and prior decisions. The [queue](research_pipeline/queue.json) records execution state. The purpose is to distinguish reused injury programmes from lesion-associated expression, identify reproducible source/recipient associations, and expose which fate or mechanism claims still need additional measurements. Each task produces a reviewable checkpoint; completion of retrieval is never completion of analysis.

## Task contracts and decision gates

The table retains the original task definitions. Current execution status is
in the queue and summary above; completed intake/analysis tasks are not a new launch order.

| Task | Bounded work and biological purpose | Saved deliverable | Exit condition |
|---|---|---|---|
| C0 | Retrieve the annotated GSE198864 object for an independent injury challenge | URL, size and SHA-256 | Complete; 2,115,735,865 bytes cached |
| C1 | Inspect object structure, gene identifiers, RNA count semantics, author cell labels, donors, treatment, medium and time; separate scRNA from bulk/autopsy | Object inventory; sample-to-GSM/donor map; counts by author label; unresolved-field table | Unique supported joins and an explicit feasible-contrast list, or a documented data gap. No programme scores |
| C2 | Define one A11 acute-injury contrast and its limits before outcome access | New JSON contract, prose rationale, source hashes, Git commit | Freeze population, donor unit, paired controls, primary pathogen, normalization, modules, coverage/cell/unit floors, inference, missingness and multiplicity. Report contract commit before scoring |
| C3 | Apply C2 to names/labels/count structure; construct donor-arm pseudobulks only for eligible units | Coverage, exclusion reasons, unit table, pseudobulk hashes | Raw nonnegative count semantics verified; all primary gates pass. No threshold reduction to rescue a failed gate |
| C4 | Execute frozen A11 RNA contrast | Scores, donor paired differences, intervals, primary and secondary results, diagnostics, run record | Quantify acute induction or uncertainty. No cancer-specificity proof from a null result; no repair/function or causal signalling claim |
| C5 | Independently verify joins, group sums, module membership and numerical inference | Verification JSON and concise biological report | Independent recomputation matches within a stated tolerance, or discrepancy is resolved and recorded |
| C6-audit-followups | Audit A5 external sample/state correspondence, first GSE202325, then GSE303646 if needed | Mouse identity map and programme-independent annotation-validation plan | Author state labels verified, or a separately named transport protocol frozen. Stop if animal identity or annotation validity remains missing |
| C7 | Execute A5 validation of a new annotation method before any target-module comparison | Mouse-held-out confusion/abstention results, excluded-feature set and domain-shift diagnostics | Prespecified annotation acceptance criteria pass; no use of tested developmental modules to select labels or thresholds. Failed classifier is a result, not a reason to relabel cells |
| C8 | Run eligible independent A5 contrast using the frozen instrument, or its explicitly justified amendment | Per-mouse scores, paired effect and uncertainty | Full UMI provenance, >=500 UMIs/cell, >=30 cells/arm, >=3 mice across days 2–21, >=70% module coverage for the unchanged test; report amendment limits |
| C9 | Identify an independent A12 cohort with comparable fixed recipient states and source compartments | Bounded candidate ledger, donor/state coverage and transfer contract | Sufficient independent eligible units for a justified fixed-model evaluation; no re-selection of predictors on validation outcomes |
| C10 | Execute and verify A12 transfer if C9 passes | Held-out predictions, absolute error/calibration, baseline comparison, uncertainty | Train-only transformations and donor independence; distinguish frozen-model transfer from a new cohort-specific refit |
| C11 | Update current RQ status and next data requirements | Dated report, current queue, PROGRESS, AI_CONTEXT | Every task marked completed, interrupted, pending or blocked with evidence; no claim that all public data have been exhausted |

The original C1–C5-first sequence is complete. C6-audit-followups and C9 have
also produced bounded recovery reports; they are not still ready-to-run tasks.
Reopen their dependent analyses only when new evidence satisfies the recorded
gate. C7 now depends on the actual C6-audit-followups ID rather than a nonexistent C6 entry.

## Contract requirements

Use one contract and a fresh output directory per new test. Separate primary estimand, technical sensitivity and biological controls. Preserve original gene maps, normalization scope and inference when claiming the same instrument. Any change is a named amendment with its own interpretation. State author-annotation dependence and possible selection of surviving cells after infection. Hash source files; record assay identity and donor evidence, not merely accession strings.

A11's executed instrument and subsequent identity restrictions are recorded
in its frozen contract, saved computations and current report. The intake
contract is not an instruction to restart C1. Integrated/scaled expression is
not raw input, and exact small-sample intervals may be unattainable; these
measurement limits remain explicit in the saved analysis.

A5 annotation transport is a different task from clustering. Establish correspondence to transitional and activated-AT2 states without including the tested module genes, select thresholds before new-cohort outcomes, evaluate on held-out biological units and allow abstention. Failure of an external author label to exist does not authorize inventing it. GSE202325 has age/time/chemistry strata; specify the target population and aggregation before scores.

A12's discovery result does not license new causal claims. External validation must preserve population and outcome definitions, distinguish changes in cell composition from within-state response and avoid reusing exposed discovery patients as independent evidence. Do not reopen A13's failed proxy through an unregistered search over alternative programmes.

## Gaps that this pipeline cannot close without new compatible evidence

- A1/A8: early regulatory measurement linked to later independent lineage/function outcome. Unpaired RNA/ATAC or simultaneous scores do not supply the missing link.
- A2/A10: independent preparations, crossed guides/positions and calibrated imaging; four wells split from one preparation do not create four biological replicates.
- A3/A4: time-matched controls or an appropriate recorder/lineage design for persistence/history.
- A9/A14/A15: selective engagement/activation or post-entry intervention with viability and lineage outcomes for mechanism claims.
- A12-S1: independent unknown-cell identity/ambient/doublet adjudication; RNA assignment does not measure secreted mature IL1B protein.

Existing compatible data may sometimes satisfy these requirements. Record the missing evidence rather than declaring every gap requires a newly performed wet experiment. Preserve A0 stop decisions and the owner-rejected A6 direction unless a new, explicitly justified scope is established.
