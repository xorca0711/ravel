# RQ delivery corrections

**Date:** 29 September 2026

**Status:** Applied; no new scientific analysis

**Baseline:** 5d4619da3a3d7ebe8bfc38de71241b44a588751b

**Review:** [Seven findings](REPORT.md)

## Applied changes

| Finding | Resolution |
|---|---|
| R1 — A1 primary-test mismatch | [Comparison matrix](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/COMPARISON_MATRIX.md) and README now mark the regulatory primary test as unspecified and non-executable. IRE1 RNA/AGER remains a supporting sourcing candidate. The gate requires a named regulatory measurement **and** an early RNA comparator linked to a later mature endpoint, with verified units and feasible timing. |
| R2 — A16 attribution | [Rationale](../../../RQ_Specified/A16_cd177_state_attribution/RATIONALE.md) separates observed attenuation from unresolved biological attribution. Figure labels describe control count without claiming power. The Stage 0 text, frozen contract, source tables and original figures/scripts remain preserved. Revised presentation outputs and hashes are in [revision_20260929](../../../RQ_Specified/A16_cd177_state_attribution/figures/revision_20260929/figure_run.json). |
| R3 — Shared inventory | [All 29 records](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md) now distinguish measurement coverage from units, timing, linkage and eligibility. O12 records the 22 verified mice while retaining design limitations; O26 links A10's completed statement; O27/O28 describe missing eligible evidence rather than universal endpoint absence. O2/O3 genetic-lineage endpoints are distinguished from O29's assay-coverage gap. |
| R4 — A8 timing scope | [Plan](../../../RQ_Specified/A8_maturation_component_at1_contribution/PLAN.md), README, rationale and JSON preserve separate incremental-association and prospective-prediction routes. Concurrent independent endpoints can qualify for association; prospective prediction requires earlier RNA. |
| R5 — A14 H1 direction | [Plan](../../../RQ_Specified/A14_withdrawal_recovery_and_reception/PLAN.md), rationale and JSON distinguish a meaningful decrease, a reliable reverse effect, a precise absence and imprecision. The meaningful-decrement threshold and uncertainty rule remain to be specified before scoring. |
| R6 — A14 joint designs | Prose and JSON permit joint designs only when the separate contrasts are identifiable, required controls are retained and biological units/replication are adequate. The blanket prohibition is removed. |
| R7 — A14 sourcing | Prose and JSON allow bounded sourcing of existing or available author-provided data under the same requirements. New data generation is not assumed necessary from absence in the reviewed record. |

The A1 register card, AI context, progress and development notes are synchronized.
A10's accepted endpoint statement and analysis are unchanged. Two scoped agents
updated A8 and A14; the parent reviewed the contracts and integrated shared wording.

## A1 execution decision

The owner authorized the regulatory primary test **if executable**. It is not
executable with the current repository evidence:

1. A specific regulatory predictor and assay/scoring definition are not nominated.
2. No verified cohort links that regulatory measurement, early RNA and later mature
   output in the same animals, clones or preparations.
3. Feasible temporal linkage, the RNA comparator, estimand and meaningful-increment
   decision rule still need a qualifying design.

The IRE1 day-7 RNA and published day-14 AGER endpoint come from different
experimental units. Their existence does not clear these requirements, and linking
RNA alone would answer a different question. No primary fit or RNA-only substitute
was run. No new source search was claimed.

## Verification

Validation results are recorded in [VALIDATION.json](VALIDATION.json).
Checks cover repository links/JSON/selected numeric bindings, the A16 frozen
evidence verifier, old and revised figure provenance, unchanged plot coordinates,
the inventory's structure and the changed contracts. Both revised PNGs were
visually inspected. These checks validate the correction package, not the
biological hypotheses or future design feasibility.

The first presentation render stopped at a renamed control-count variable; that
reference was repaired and the complete render succeeded. No scientific table
or model output changed.

## Remaining work

A1 needs a qualifying regulatory/RNA/outcome design before execution. A8 still
needs a frozen component partition and an eligible linked endpoint dataset.
A14 still needs eligible recovery data and finalized decision specifications.
These are evidence and specification gaps, not unperformed corrections.
