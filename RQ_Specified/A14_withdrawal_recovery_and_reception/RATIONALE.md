# A14 rationale: two hypotheses, two decisions, one shared outcome family

Written 28 September 2026; corrected 29 September 2026, with no eligible A14 dataset identified
in the reviewed evidence. A14 is a design, not a result. This
document does what the register card compresses into a paragraph: it gives each hypothesis its
own population, outcome, rival set and decision rule, and it explains when separate or joint
designs can answer them without confounding their contrasts.

## Why recovery is the question, and why RNA cannot answer it

An alveolar epithelial cell held in an IL-1-driven transitional state has four futures that a
transitional RNA score cannot distinguish: it matures, it reverts, it dies, or it is replaced by
a neighbour's progeny. All four reduce the transitional score. Only the first is repair. This is
why A14 is specified around measured mature output and viability rather than around the
disappearance of a state, and it is the boundary that most constrains what any future result may
claim.

The biological interest is the difference between reversible repair and persistent remodelling.
If a transitional state is recoverable after a short exposure but not a long one, exposure
duration is a control point on that transition. If fibroblast reception changes the outcome under
a fixed exposure, the stromal compartment is part of the control. Those are two different claims
about where the control sits, and they are separable by design.

## H1, duration: does how long the signal lasted change whether recovery happens?

**Hypothesis.** Longer IL-1beta exposure reduces mature epithelial recovery after verified
withdrawal, relative to transient exposure at the same intensity.

**Population.** Alveolar epithelial cells in a system where exposure can be started and stopped
and the same preparation followed afterwards: independent animals, or independent culture
preparations that are genuinely independent rather than repeat wells of one mixture.

**Contrast.** Transient against sustained exposure, at matched intensity, with verified
withdrawal and time-matched controls that were never exposed, all observed over comparable
post-withdrawal intervals.

**Outcome.** Mature-cell yield and viability per preparation, with traced descendants and a
function readout where available. Not a transitional RNA score, and not a cycling score.

**Rivals specific to H1.**

1. **Residual exposure.** The signal was not actually withdrawn, so "sustained" and "withdrawn"
   differ in current exposure rather than in history. Addressed by measuring target engagement
   after withdrawal, not by assuming the washout worked.
2. **Toxicity.** Longer exposure reduced yield by killing cells, independent of any effect on
   the transition. Addressed by viability measured alongside yield.
3. **Death and replacement.** Mature cells present at the end are the progeny of unexposed
   neighbours rather than recovered transitional cells. Addressed by lineage tracing; without it,
   yield alone cannot separate recovery from replacement.
4. **Time in culture or in vivo**, rather than time under exposure. Addressed by the time-matched
   unexposed controls.

**Decision.** Define the contrast as recovery after sustained exposure minus recovery after
transient exposure. Before inspecting outcomes, fix the minimum meaningful decrement and the
uncertainty rule. A decrease that meets both rules after verified withdrawal, in independent
preparations, supports H1. A reliably meaningful increase contradicts H1's direction. Otherwise,
a sufficiently precise estimate excluding a meaningful decrement weakens H1; an estimate that
cannot distinguish a meaningful decrement from its absence is inconclusive. Failed engagement
verification or missing post-withdrawal observation is also inconclusive, rather than negative.
Viability must distinguish reduced recovery from toxicity, and absent lineage evidence limits
the conclusion to mature yield rather than recovery of the originally transitional cells.

## H2, reception: does it matter which compartment receives the signal?

**Hypothesis.** Fibroblast IL-1 reception modifies epithelial recovery beyond direct epithelial
reception of the same signal.

**Population.** A system containing both compartments, in which IL1R1 can be removed from one
compartment at a time while exposure is held fixed: epithelial-only and stromal-containing
preparations, with compartment-specific perturbation.

**Contrast.** Epithelial-specific against fibroblast-specific IL1R1 perturbation under a fixed
exposure and a fixed withdrawal schedule, with direct epithelial reception controlled rather than
varied alongside.

**Outcome.** The same family as H1 — mature-cell yield, viability, traced descendants, function —
measured per preparation, alongside verified target engagement in the perturbed compartment.

**Rivals specific to H2.**

1. **An epithelial-only response.** Everything observed follows from epithelial reception, and
   the fibroblast arm changes nothing once epithelial reception is controlled. This is H2's
   primary rival and the reason the epithelial arm is not optional.
2. **Incomplete or off-target perturbation.** The compartment-specific knockout was partial, so a
   null is a failure of the instrument rather than of the hypothesis. Addressed by measuring
   engagement in the perturbed compartment.
3. **Compartment composition.** Removing reception from fibroblasts changed which cells are
   present rather than how they respond. Addressed by recording composition as well as outcome.
4. **A mediator that is not IL-1.** Fibroblasts alter epithelial recovery through a parallel
   route that the IL1R1 perturbation does not isolate. This bounds the interpretation and is
   disclosed rather than resolved by this design.

**Decision.** An outcome change under fibroblast-specific intervention, with direct epithelial
reception controlled, supports H2. A precise absence weakens it. Failed engagement is
inconclusive. H2 can hold while H1 fails and the reverse, which is why each carries its own rule.

## Why the decisions are separate, even in a joint design

A long-exposure, fibroblast-perturbed arm differs from a short-exposure,
epithelial-perturbed arm in two ways at once. That comparison alone cannot separate duration
from reception. The prohibition applies to this inseparable contrast, not to every joint or
factorial design. A design that varies the factors separately and adequately observes the
relevant combinations may identify each contrast and their interaction.

Eligibility is assessed for each hypothesis: H1 needs duration contrasts at fixed receiving
conditions and time-matched unexposed controls; H2 needs reception contrasts at fixed exposure
with direct epithelial reception controlled. Each must have documented biological units,
adequate replication and the relevant engagement, viability and lineage checks. A joint design
must state how interactions affect its contrasts and uncertainty; it cannot assume effects
are constant across conditions or count shared units as independent replication. A design
adequate for one hypothesis is not automatically adequate for the other. Either hypothesis
can advance alone, and its result does not decide the other.

## What the neighbouring IL-1 work does and does not contribute

A12's exploratory 12-patient pilot improved held-out prediction of an inflammatory RNA response
from recipient receptor and inhibitor RNA, with an unstable fibroblast increment
([A12](../A12_recipient_context/README.md)). A13's amended pilot found no aggregate held-out gain
from a fibroblast programme, RMSE moving from 0.2283 to 0.2373
([A13](../A13_fibroblast_beyond_macrophage_il1b/README.md)). A2 bounds what its screen's design
can support at all, since four wells split from a common mixture are not four preparations
([A2](../A2_areg_source_delivery/README.md)).

What they contribute is motivation for H2's compartment question and a warning about units. What
they cannot contribute is evidence about reception — receptor and inhibitor RNA is not measured
reception — or about recovery, since neither involved withdrawal, and both are human
cross-sections rather than followed preparations.

## What is genuinely open

Both hypotheses remain unanswered. No eligible dataset linking the required recovery outcomes,
verified withdrawal and hypothesis-specific contrasts has been identified in the reviewed
evidence. This does not establish absence from public archives or author-held data. Mature
endpoint measurements in neighbouring studies are not automatically eligible withdrawal
contrasts, but their existence must not be described as an absence of mature measurement.

The next sourcing step is a bounded review of existing or author-provided evidence against the
same contracts, recorded separately for H1 and H2. New data generation is a candidate if that
route remains unresolved. Endpoint definitions, contrasts, meaningful-effect criteria and
replication requirements are fixed before outcome inspection; sourcing does not relax them.

## Connections and boundaries

- **A12** owns recipient receptor and inhibitor context as RNA prediction; A14 owns reception as
  a perturbation. A12's endpoint is an inflammatory RNA response, A14's is mature output.
- **A13** owns whether a fibroblast programme adds information about an epithelial outcome in
  human cross-sections; A14 asks whether fibroblast reception changes recovery under a controlled
  exposure. A13's negative does not bear on A14's H2.
- **A8** shares the need to establish an eligible, linked mature epithelial endpoint and the
  [shared inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
  that separates measurement availability from design eligibility. A8 is observational and about
  a component definition; A14 is interventional and about exposure and reception.
- **A1** owns the regulatory distinction between transitional states and the endpoint sourcing
  both A8 and A14 draw on.
- **A4** owns the lineage-sequence question. A14 traces descendants as an outcome and makes no
  claim about the order of prior activity.
- Nothing here bears on malignant transformation, and neither hypothesis licenses a claim about
  it.

Measurement contracts: [MC1](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1) for biological units,
confounding and endpoints; [MC3-MC4](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc3) for state and
source identity and for ligand-receptor representation.
