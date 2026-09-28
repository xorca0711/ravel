# A8 rationale: why signature overlap is a measurement check, not a maturation mechanism

Written 28 September 2026, before any A8 endpoint has been computed. This document exists to
settle one confusion that the register card's brevity invites: the observation that motivates A8
is a fact about two gene lists, and it licenses a check on the measurement rather than a claim
about maturation biology.

## The proposition, stated so it can fail

A component of epithelial RNA specific to maturation carries information about how much mature
AT1 contribution a population actually produces, beyond what the shared transitional component
already carries. Stated to fail: freeze the two components, measure mature AT1 contribution
independently in the same animals, and the maturation-specific component adds nothing the shared
component did not already provide.

Note what the failure condition is not. It is not "the increment shrinks when shared genes are
removed", and it is not "the two gene lists overlap". Both of those are true of the present data
and neither is a result about maturation.

## What the founding observation actually is

Claim C168 records that the source-derived ADI and AT1 holdout lists **share 119 genes**, and
that the four-gene late-AT1 panel **changes direction across technical seeds 17 and 29** at
2,000 UMIs in several injured wells and in the one eligible external mouse
([module_overlap.csv](../../Research%20Article/epithelial_state_specificity/results/module_overlap.csv),
[A8 diagnostics](../../analysis/figures/rq/README.md#a8)). The claim's own wording is the
boundary: broad ADI and AT1 marker scores "are not independent evidence for transitional identity
and mature AT1 fate". It is owned by the
[epithelial state specificity package](../../Research%20Article/epithelial_state_specificity/README.md),
not by A8, and A8 adds nothing to it.

Three consequences follow, and only three.

1. **Any analysis that scores "transitional" and "mature AT1" from these lists scores some of the
   same genes twice.** An apparent increment from a "maturation" score over a "transition" score
   can therefore be partly definitional. This is a measurement problem with a measurement
   remedy: freeze a disjoint partition before opening an endpoint.
2. **The small late-AT1 panel is not a stable instrument at this depth.** A four-gene panel whose
   direction depends on the technical seed cannot carry a fate claim, whatever it shows.
3. **Neither consequence says anything about whether maturation is a distinct programme.** The
   overlap is consistent with a genuinely shared biology of transition and maturation, and
   equally consistent with two distinct programmes described by two poorly separated gene lists.

## Why the inference runs in neither direction

The structural difficulty is the same one A16 records for marker attribution, and it is worth
naming because it determines what A8 may conclude.

Suppose the partition is made disjoint and the increment falls. Two explanations survive. Either
the original increment was definitional, which is the measurement rival; or the shared genes
carried real maturation biology that disjointification removed, in which case the fall is an
artefact of the remedy. Nothing in the RNA distinguishes these, because the shared genes are
shared for both reasons at once.

Suppose instead the increment persists. That does not establish a maturation-specific mechanism
either, because the remaining genes can still be correlated with the shared component, with
timing, with mixture, or with measurement quality — the rivals the register card already names.

The asymmetry that makes A8 worth keeping is therefore narrow, and it is about the **outcome**
rather than the predictor. With an independently measured mature AT1 contribution, a frozen
partition can be tested for added information against something that is not itself an RNA score.
Without that outcome, no partition of the RNA can settle anything, and the question is not a
computation waiting for time — it is a question waiting for a measurement.

## Rivals

1. **Definitional dependence (the measurement rival).** The increment is an artefact of 119
   shared genes and a seed-sensitive panel. Addressed by freezing a disjoint partition before the
   endpoint is opened. This rival is currently the best supported, because it is the only one with
   evidence behind it.
2. **Shared transition alone.** The shared component carries all the information and there is no
   maturation-specific contribution. This is the register card's primary biological rival.
3. **Timing.** The predictor and the endpoint sample different points of the same process, so an
   increment reflects when cells were captured rather than what programme they ran.
4. **Mixture.** The population contains more than one state, and the increment tracks
   composition rather than a per-cell programme.
5. **Measurement quality.** Depth, detection and panel size differ between the components; a
   larger or better-measured component can appear more informative for that reason alone.
6. **Circularity through the outcome.** If the "mature" endpoint is itself defined from an RNA
   panel overlapping the predictor, any increment is guaranteed. This is the rival the register
   card's instruction is written against, and it is why the outcome must be protein, morphology
   or a traced descendant yield.

## What is genuinely open

Whether a maturation-specific component exists as a measurable, separable programme at all is
open. So is whether mature AT1 contribution is predictable from any early epithelial measurement.
A8's specific contribution is narrower than either: it asks whether a frozen maturation component
adds information about a measured mature endpoint, which is the one version of the question that
an existing dataset could in principle answer if the endpoint were measured.

What is not open is whether the current evidence supports a maturation mechanism. It does not,
and this document exists so that a later session does not read the overlap arithmetic as though
it did.

## Connections and boundaries

- **A1** owns the regulatory distinction between RNA-similar transitional states and, since 28
  September 2026, the [comparison matrix](../A1_transitional_epithelial_state_distinction/COMPARISON_MATRIX.md)
  and the [shared outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md).
  A8 uses that inventory as its sourcing and does not maintain a second copy. A8 is narrower than
  A1: one component partition, one endpoint, no chromatin or regulatory layer.
- **A10** owns the organoid growth endpoint. Its
  [endpoint statement](../A10_organoid_growth_outcome/reports/ENDPOINT_TIMING_UNITS_2026-09-28.md)
  disqualifies it as A8's later outcome: predictor and outcome are concurrent and in the same
  well, and the unit is the well.
- **A14** shares the absence of a measured mature outcome and nothing else. Its question is
  interventional and about IL-1 exposure and reception; A8's is observational and about the
  definition of a maturation component. They are separate workspaces for that reason.
- **A7** owns whether Cebpa loss attenuates AT2 identity across or within states, and the
  epithelial state specificity package that owns C168 serves that question too. A8 does not
  reinterpret its genotype contrasts.
- **A16** owns marker attribution in the England mutant compartment. A8 borrows only its
  structural lesson: when conditioning shrinks an estimate under both rivals, the informative
  step is a new measurement rather than another partition.

Measurement contracts: [MC1](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1) for biological units,
confounding and endpoints; [MC5](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc5) for programme
dependence and validation.