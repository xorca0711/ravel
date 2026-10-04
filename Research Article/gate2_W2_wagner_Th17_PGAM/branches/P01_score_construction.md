# Wp-P01 — Is the pathogenicity ranking a property of the cells or of the score?

**Status:** proposed, outcome-exposed. Measurement validation, not a biological
hypothesis.

## Proposition, stated so it can fail

The ordering of Th17n cells by the published pathogenicity score, which every
reaction correlation in Figure 1 is computed against, is stable to the choices
made in building that score. If it is not — if dropping the highly-variable-gene
restriction, scoring the two arms separately, or replacing the module lists with
their published supersets re-orders cells substantially — then the reaction
ranking inherits that instability, and reaction-level claims must be reported
with it.

## What the source did

The score is the difference between a pro-inflammatory and a pro-regulatory
module score from Gaublomme et al. 2015. Only genes that were highly variable in
*this* dataset entered: 63 of 116 pro-inflammatory and 30 of 68 pro-regulatory
genes. Gene scores are z-scaled log expression averaged within the module. The
Results text and STAR Methods state opposite subtraction orders; the figures
follow the Results text.

So the score depends on (i) which published module genes survived an HVG filter
computed on the new data, (ii) equal weighting within each arm, (iii) the
difference of two arms that need not move together, and (iv) a sign convention
that the paper itself documents inconsistently.

## Strongest rival

The ranking is robust and these are implementation details. That outcome is
informative and would strengthen the paper's Figure 1: it would mean the
reaction ranking is not an artefact of gene selection.

## Decision this would inform

Whether reaction-level and program-level statements from this paper can be
carried into other analyses as-is, or must travel with a sensitivity envelope.
It also decides whether the arm decomposition used by
[Wp-P03](P03_glucose_composition_vs_state.md) is legitimate.

## Unit, endpoint and measurement

Unit: cells, nested in 8 libraries and 2 animals — this card makes no population
claim and needs none, because it is about a measurement's internal stability.
Endpoint: rank correlation between the reference score and each variant score,
reported as a distribution over cells, plus the proportion of cells changing
score tercile. Variants fixed before execution: full published module lists
without the HVG filter; each arm alone; equal weights replaced by arm-wise
standardisation; the two published sign conventions.

## Informative outcomes

- Spearman correlation near 1 across variants: the ranking is a property of the
  cells; reaction claims carry over.
- A variant that re-orders a substantial share of cells: name it, and report
  every downstream reaction or program statement conditioned on it.
- The two arms moving independently: the single score is a lossy summary and the
  arms should be reported separately, which is also what the paper's own Figure 3C
  does when it attributes the glucose effect to the regulatory arm alone.

## Stop condition and boundary

Stop when the pre-specified variant list is exhausted; do not search for a
variant that produces a preferred result. This card cannot establish that the
score measures pathogenicity — that is a functional claim requiring the transfer
experiments the paper reports, not a better gene list. It also cannot be run
before the module lists are recovered: if Table S1 stays unavailable, the
reference score is itself a substitution, and that must be stated in the result.

**Nearest existing work:** [Wg-P01](../../gate2_W1_wagner_th17_autoimmunity/branches/P01_score_specificity.md)
asks whether network-derived structure adds information beyond simpler RNA
summaries; this card is the narrower question of whether the *outcome* variable
those scores are correlated against is stable.
