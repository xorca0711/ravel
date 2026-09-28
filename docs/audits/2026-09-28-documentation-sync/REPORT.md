# Project documentation synchronization, 28 September 2026

Base: remote main `71321fa275259225681f57403871cc5f4f48bef2`, after merged
gap-fill PR [#107](https://github.com/xorca0711/scRNA_seq/pull/107).
Branch: `codex/research-doc-sync`.

The owner requested a project-level README without a front claims table,
updated dataset information and a current research-article roadmap, plus fixes
to related documentation that had drifted. This pass uses tracked repository
evidence; it does not claim a new public-data or bibliographic search.

## Changes and evidence

| Area | Synchronization | Evidence authority |
|---|---|---|
| Main navigation | Replace selected claim rows and paper-specific start links with questions, studies, datasets, figures, evidence and reproduction routes | [README](../../../README.md); owner instruction; unchanged [claim register](../../../CLAIMS.md) |
| Dataset inventory | Retain all 17 former README dataset rows; add later expression, regulatory, imaging and clone inputs, and distinguish failed cohort gates from analysed data | [Inventory](../../DATASETS.md) links each row to its run report, unit definitions and eligibility record |
| Paper roadmap | Reconcile Cardoso corrections, England A16/A17, Yu-derived pilots and A2/A10 use of paper 14's deposit; preserve reading decisions and publication identifiers | [Paper index](../../../Research%20Article/README.md), [machine roadmap](../../../Research%20Article/ROADMAP.json) and their linked reports |
| Execution state | Identify the current gap-fill ledger, mark completed A5/A12 audits and blocked scoring, repair the C7 dependency and retire the obsolete next-task pointer | [Merged execution ledger](../../roadmap_runs/2026-09-28-gap-fill/RESULTS.md); [legacy queue](../../research_pipeline/queue.json) |
| England summaries | Replace pending corrected-C1/source-accounting steps with completed bounded checks and their remaining inference limits | [A16 corrected C1](../../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md); [A17 accounting](../../roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md) |
| Supporting guides | Generalize the docs index, clarify original-atlas scope and bibliography coverage, link A10's later design evidence, and synchronize handoffs | [Structure](../../REPOSITORY_STRUCTURE.md), [reproducibility](../../../REPRODUCIBILITY.md), [historical dataset gate](../../NEXT_DATASET_GATE.md), [progress](../../../PROGRESS.md) |

## Preservation and limits

This is a documentation-only revision. No source analysis, figure, result
table, frozen contract, registered claim or original dated execution report
changes. No new matrix is scored. The paper reading order, note statuses,
DOIs and PMIDs remain as recorded at the base commit. Dataset counts are
qualified by the selected design; they do not reclassify technical libraries
as animals or reuse as replication.

A5 still lacks the required barcode/state/mouse map. None of the three A12
cohorts inspected in the recovery passes the unchanged external test. A16's
corrected matching leaves substantial imbalance; A17 accounting does not
complete its stochastic refit. Those gaps remain visible in the current
roadmap. Historical plans and handoffs retain their dated context.

## Verification

Validation results are recorded in [VALIDATION.json](VALIDATION.json): 3,740
repository checks and 40 targeted documentation checks passed. Checks cover
local links and JSON, dataset-accession preservation, roadmap
reading/identifier invariance, queue dependency resolution and the changed-file
scope. Scientific tests are not rerun for this prose and status synchronization.
