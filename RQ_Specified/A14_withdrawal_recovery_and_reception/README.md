# A14: do exposure duration and fibroblast IL-1 reception separately determine recovery?

<a id="biological-question"></a>

## Organizing biological question

> Do exposure duration and fibroblast IL-1 reception separately determine
> recovery after withdrawal?

If alveolar epithelial cells are held in an IL-1-driven transitional state and the
signal is then withdrawn, do they recover mature identity and function — and does
that depend on how long they were exposed, and on whether neighbouring fibroblasts
received the signal too? The question matters because shared RNA cannot
distinguish reversible repair from persistent dysfunction, which is the difference
between successful regeneration and remodelling.

**This workspace carries two hypotheses with separate decisions.** They are kept
apart deliberately: either can hold without the other, and a single combined
experiment that confounds them would answer neither.

**Read first:** [question card](../../RESEARCH_QUESTIONS.md#a14),
[rationale](RATIONALE.md), [plan](PLAN.md),
[design schematic](../../analysis/figures/rq/README.md#a14).

## Evidence and analysis history

**Status, 28 September 2026: registered; the design is unexecuted; nothing
computed for A14.** This folder was created on the owner's instruction to give A14
its own workspace rather than a card alone. It adds no new question identifier, no
claim row and no grade, and it does not change the register card.

A14 has never had a result. It is a mechanistic follow-up to the repair-versus-
persistence question, not an existing withdrawal-fate finding, and published
tracing informs its design without replacing the experiment. The only tracked
asset is the experimental schematic in the register's cross-question gallery
([A14 panels](../../analysis/figures/rq/README.md#a14)); its outcome panels
require new data, and no anticipated response curve is presented as a result.

## The two hypotheses in one sentence each

- **H1, duration.** Longer IL-1beta exposure reduces mature epithelial recovery
  after verified withdrawal, compared with transient exposure of the same
  intensity.
- **H2, reception.** Fibroblast IL-1 reception modifies epithelial recovery beyond
  direct epithelial reception of the same signal.

They share an outcome family and nothing else. H1 varies the exposure and holds
the receiving compartments fixed; H2 holds the exposure fixed and varies which
compartment can receive it. The [rationale](RATIONALE.md) gives each its own
population, outcome, rival and decision, and the [plan](PLAN.md) gives each its
own arm.

## What it stands on, and what that is worth

It stands on the IL-1 work in neighbouring questions, none of which is a recovery
result. A12's exploratory 12-patient pilot found that recipient receptor and
inhibitor RNA improved held-out prediction of an inflammatory RNA response while
its fibroblast increment was unstable
([A12](../A12_recipient_context/README.md)); A13's amended pilot found no
aggregate held-out gain from a fibroblast programme, with RMSE moving from 0.2283
to 0.2373 ([A13](../A13_fibroblast_beyond_macrophage_il1b/README.md)). Both are
RNA-context results in human cross-sections. Neither measures reception, neither
involves withdrawal, and neither bears on recovery. They motivate H2's compartment
question and they cannot answer it.

## Register readiness: the experiment is the blocking input

The shared
[outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
records A14's requirement as row O28 and finds it **not available**: mature-cell
yield, viability, traced descendants and function after verified IL-1beta
withdrawal are not measured in any surveyed deposit. Row O29 records that no EdU,
BrdU or label-retention assay is named anywhere in that evidence, so a
label-retention readout cannot be assumed available either. A14 therefore shares
A1's missing-outcome gate, as the
[gap-fill ledger](../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md) records.

Unlike A8, A14's gap is not a dataset that might exist somewhere. Its contrasts
require a perturbation and a withdrawal that have to be performed.

## Layout

| Path | Role |
|---|---|
| [RATIONALE.md](RATIONALE.md) | Each hypothesis with its own population, outcome, rival and decision; why they are not one experiment |
| [PLAN.md](PLAN.md) | Stage 0 registration, the two frozen arms, feasibility conditions and what execution would require |
| [config/a14_question_contract.json](config/a14_question_contract.json) | Machine-readable scope, the two decision rules, prohibitions, and the declaration that nothing is scored |
| [A12 recipient context](../A12_recipient_context/README.md), [A13 fibroblast increment](../A13_fibroblast_beyond_macrophage_il1b/README.md) | The IL-1 RNA-context results that motivate H2 without answering it |
| [A1 outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md) | Shared endpoint sourcing; A14's requirement is row O28 |

## Six things a later session must not do

1. **Do not report loss of a transitional RNA score as recovery.** It cannot
   distinguish maturation, reversion, death or replacement. This is the register
   card's own boundary and the single most likely misreading of any future result.
2. **Do not combine the two hypotheses into one experiment** whose arms vary
   exposure duration and receiving compartment together. The result would be
   uninterpretable for both.
3. **Do not treat A12's or A13's RNA-context results as evidence about reception.**
   Receptor or inhibitor RNA is not measured reception, and neither pilot involved
   withdrawal.
4. **Do not count repeat wells split from one cell mixture as independent
   preparations.** A2's recovered methods establish why that fails.
5. **Do not claim withdrawal without verifying it.** Residual exposure is a named
   rival, and target engagement must be measured alongside the outcome.
6. **Do not extend any recovery result to malignant transformation.** Neither
   hypothesis bears on it.