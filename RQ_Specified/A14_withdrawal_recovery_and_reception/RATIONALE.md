# A14 rationale: two hypotheses, two decisions, one shared outcome family

Written 28 September 2026, before any A14 endpoint exists. A14 is a design, not a result. This
document does what the register card compresses into a paragraph: it gives each hypothesis its
own population, outcome, rival set and decision rule, and it explains why they must not be run as
one experiment.

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

**Decision.** A recovery difference after verified withdrawal, in independent preparations,
supports H1. A precise absence of a difference weakens it. Failed engagement verification, or no
post-withdrawal observation, is inconclusive rather than negative.

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

## Why these are not one experiment

A single factorial that varied exposure duration and receiving compartment together would confound
the two claims in the arms that matter most: a long-exposure, fibroblast-perturbed arm differs
from a short-exposure, epithelial-perturbed arm in two ways at once. Worse, the two hypotheses
have different control requirements — H1 needs time-matched unexposed preparations, H2 needs a
controlled epithelial-reception arm — and an experiment sized for one is not automatically valid
for the other. The register card's phrasing, "either can hold without the other", is a design
constraint and not a hedge.

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

Everything A14 asks. There is no recovery measurement, no withdrawal observation, and no
compartment-specific reception experiment in the surveyed evidence. The honest statement of A14's
status is that it is a well-specified design whose value is in being specified before it is run,
so that its endpoints, contrasts and replication are fixed rather than chosen afterwards.

## Connections and boundaries

- **A12** owns recipient receptor and inhibitor context as RNA prediction; A14 owns reception as
  a perturbation. A12's endpoint is an inflammatory RNA response, A14's is mature output.
- **A13** owns whether a fibroblast programme adds information about an epithelial outcome in
  human cross-sections; A14 asks whether fibroblast reception changes recovery under a controlled
  exposure. A13's negative does not bear on A14's H2.
- **A8** shares the absence of a measured mature epithelial outcome and the
  [shared inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
  that records it, and nothing else. A8 is observational and about a component definition; A14 is
  interventional and about exposure and reception.
- **A1** owns the regulatory distinction between transitional states and the endpoint sourcing
  both A8 and A14 draw on.
- **A4** owns the lineage-sequence question. A14 traces descendants as an outcome and makes no
  claim about the order of prior activity.
- Nothing here bears on malignant transformation, and neither hypothesis licenses a claim about
  it.

Measurement contracts: [MC1](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1) for biological units,
confounding and endpoints; [MC3-MC4](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc3) for state and
source identity and for ligand-receptor representation.