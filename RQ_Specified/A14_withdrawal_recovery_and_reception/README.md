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
apart deliberately: either can hold without the other. Separate experiments or
a joint design can qualify if each contrast is identifiable and independently
supported; changing both factors in an inseparable contrast cannot answer either.

**Read first:** [question card](../../RESEARCH_QUESTIONS.md#a14),
[rationale](RATIONALE.md), [plan](PLAN.md),
[design schematic](../../analysis/figures/rq/README.md#a14).

## Evidence and analysis history

**Status, 29 September 2026: registered; the design is unexecuted; nothing
computed for A14.** This folder was created on the owner's instruction to give A14
its own workspace rather than a card alone. It adds no new question identifier, no
claim row and no grade, and it does not change the register card.

A14 has never had a result. It is a mechanistic follow-up to the repair-versus-
persistence question, not an existing withdrawal-fate finding, and published
tracing informs its design without replacing the required withdrawal contrasts.
Its schematic is in the register's cross-question gallery
([A14 panels](../../analysis/figures/rq/README.md#a14)); its outcome panels
require eligible measured data, and no anticipated response curve is presented as a result.

## The two hypotheses in one sentence each

- **H1, duration.** Longer IL-1beta exposure reduces mature epithelial recovery
  after verified withdrawal, compared with transient exposure of the same
  intensity.
- **H2, reception.** Fibroblast IL-1 reception modifies epithelial recovery beyond
  direct epithelial reception of the same signal.

They share an outcome family but retain separate contrasts. H1 varies the exposure
and holds receiving conditions fixed; H2 holds the exposure fixed and varies which
compartment can receive it. A joint design must preserve those contrasts and assess
any interaction without pooling incompatible conditions. The [rationale](RATIONALE.md)
gives each its own population, outcome, rival and decision, and the [plan](PLAN.md)
gives each its own arm.

H1 requires a meaningful decrease in recovery after longer exposure. A reliable
reverse effect contradicts that direction; a precise absence of a meaningful
decrement weakens it; imprecision or failed observation/engagement checks is
inconclusive. The meaningful-effect and uncertainty rules must be fixed before
outcomes are inspected. Viability and lineage evidence still bound any recovery claim.

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

## Register readiness: eligible withdrawal evidence is the blocking input

The shared
[outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
records A14's requirement as row O28. **No eligible dataset has been identified in
the reviewed evidence** for either hypothesis: measured mature output must be
linked to verified withdrawal, the relevant contrast and independent biological
units, with viability and lineage evidence bounding interpretation. Mature and
genetically lineage-labelled endpoints already exist in O2/O3; those records do
not by themselves supply A14's required design. O29 concerns documented
EdU/BrdU/label-retention assays and must not be used to erase genetic lineage
evidence. The earlier
[gap-fill ledger](../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)
records the unresolved endpoint gate, not global absence of mature measurements.

A bounded search of existing sources or author-provided data may satisfy either
contract. No public-archive search under these eligibility conditions has yet been
completed. New data generation becomes a candidate only if compatible existing
evidence remains unidentified; all routes retain the same endpoint and unit requirements.

## Layout

| Path | Role |
|---|---|
| [RATIONALE.md](RATIONALE.md) | Each hypothesis with its own population, outcome, rival and decision; conditions for separate or joint designs |
| [PLAN.md](PLAN.md) | Stage 0 registration, the two frozen arms, feasibility conditions and what execution would require |
| [config/a14_question_contract.json](config/a14_question_contract.json) | Machine-readable scope, the two decision rules, prohibitions, and the declaration that nothing is scored |
| [A12 recipient context](../A12_recipient_context/README.md), [A13 fibroblast increment](../A13_fibroblast_beyond_macrophage_il1b/README.md) | The IL-1 RNA-context results that motivate H2 without answering it |
| [A1 outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md) | Shared endpoint sourcing; A14's requirement is row O28 |

## Six things a later session must not do

1. **Do not report loss of a transitional RNA score as recovery.** It cannot
   distinguish maturation, reversion, death or replacement. This is the register
   card's own boundary and the single most likely misreading of any future result.
2. **Do not infer separate effects from inseparable contrasts** that change
   exposure duration and receiving compartment together. A joint design is eligible
   only when each hypothesis has identifiable contrasts, controls and independent units.
3. **Do not treat A12's or A13's RNA-context results as evidence about reception.**
   Receptor or inhibitor RNA is not measured reception, and neither pilot involved
   withdrawal.
4. **Do not count repeat wells split from one cell mixture as independent
   preparations.** A2's recovered methods establish why that fails.
5. **Do not claim withdrawal without verifying it.** Residual exposure is a named
   rival, and target engagement must be measured alongside the outcome.
6. **Do not extend any recovery result to malignant transformation.** Neither
   hypothesis bears on it.
