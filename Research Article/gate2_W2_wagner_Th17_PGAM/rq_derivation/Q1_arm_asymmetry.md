# Wp-Q1 — Does the pathogenic shift proceed by losing regulatory competence rather than by gaining effector competence?

**Historical derivation:** the [7 October correction report](../CORRECTIONS_2026-10-07.md) and current A28–A30 dossiers supersede affected Compass/human values and inference wording below. Retain this record of what was known when the questions were proposed.

**Wp-Q1 · Proposed biological question · Outcome-exposed.**
[Derivation index](README.md) · [Overlap](OVERLAP_MATRIX.md) ·
[Grounding](SOURCES_AND_GROUNDING.md).

## Observation → gap → question

The published pathogenicity score is a difference: the mean of a
pro-inflammatory gene module minus the mean of a pro-regulatory one. A rise in
that difference is reported as increased pathogenicity, and the paper's central
glucose result is such a rise.

Three executed results together say that the rise is one-sided, and that which
side moves depends on the perturbation.

1. [Wp-R1](../R1_RESULTS.md): at 1 mM versus 25 mM glucose the score rises in
   4 of 4 animal-paired comparisons (+0.133 and +0.109 in Th17n, +0.044 and
   +0.059 in Th17p) and it rises **because the pro-regulatory arm falls**. The
   pro-inflammatory arm does not rise.
2. [Wp-P01](../P01_RESULTS.md): across 15,830 single cells the two arms are
   **anti-correlated** (Spearman −0.389 to −0.503, pooled −0.410). Scoring the
   pro-inflammatory arm alone makes the glucose effect sign-inconsistent across
   the two animals (−0.053 and +0.020); the regulatory arm carries it.
3. [Wp-M3](../METADATA_PHENOTYPES_RESULTS.md): in ten paired human donors, CSF
   minus blood moves the **pro-inflammatory** arm specifically (+0.061, 10/10
   donors, empirical p = 0.003 against a matched random-set null) while the
   pro-regulatory arm does not move on either definition (p = 0.394 for the
   authors' HVG set, 0.931 for all 58 mapped genes).

So the two best-supported arm asymmetries in this package point in **opposite
arms**, under a nutrient perturbation in mouse culture and a compartment
contrast in human disease. The deposited data cannot say whether that is two
routes into one state or two different states that score alike.

**Question.** In Th17 cells, does entry into the pathogenic transcriptional
state proceed by loss of the regulatory programme, by gain of the effector
programme, or by either route depending on the perturbation — and are the two
routes distinguishable in the same cells at the protein level?

The decision this informs is what a pathogenicity score means when it moves: a
one-sided move is not interchangeable with the other side's move if the
resulting cells differ functionally.

## Hypothesis and biology

Regulatory and effector competence are **separately regulated** in the same
Th17 cell, not two ends of one axis. Nutrient restriction removes the
regulatory programme (Foxp3, CTLA4, IKZF2-type output) without adding effector
output; an inflammatory compartment adds effector output (IL-17, IL-23R, CSF2)
without removing the regulatory programme. The prediction is directional and
falsifiable: under glucose restriction, per-cell Foxp3 and CTLA4 protein should
fall with IL-17 protein unchanged; under an IL-1β/IL-23 pathogenic cytokine
condition, IL-17 should rise with Foxp3 and CTLA4 unchanged. A single latent
axis predicts that both perturbations move both proteins reciprocally.

The biology this would bear on is not specific to Th17 cells. Whether a
transitional or regulatory state is exited by losing its own programme or by
being overwritten by the next one is the same question that arises for
progenitor populations in regenerating tissue, and the answer determines
whether a perturbation that produces the same score produces the same cell.

## Strongest rivals

1. **One latent axis.** The two modules are anti-correlated by construction —
   genes that go up in one Th17 polarisation go down in the other — so a
   one-sided move may be a property of the gene lists rather than of the cells.
   This is the rival the design must defeat first, and the RNA data cannot do
   it, because both arms are computed from the same transcriptome.
2. **Composition, not state.** [Wp-P03](../P03_RESULTS.md) decomposed the
   glucose effect and found the **composition** term positive in both animals
   under all four labelling and stratification combinations (share 0.68 to
   3.45), while the within-state term disagreed in sign across animals
   (+0.034 and −0.037) and the card's stop rule fired as inconclusive. The
   regulatory arm may fall because the mixture of programmes changes, not
   because any cell loses regulatory competence.
3. **Proliferation.** Low glucose slows division and the published latent space
   regressed phase out. Wp-R1 found proliferation higher at 25 mM in 4 of 4
   pairs, so the arms may track growth state. Wp-P03 found the proliferation
   stratification moves the decomposition terms by less than 0.006 in score
   units, which weakens but does not remove this rival.
4. **Activation, in the human leg.** The declared activation set also exceeds
   its null in CSF versus blood (+0.109, p = 0.013), and in blood it correlates
   with every module at Spearman −0.61 to −0.87. A compartment that is simply
   more activated will move an effector module.

## Unit, contrast and endpoint

Mouse for any new experiment, donor for any human leg; cells within library are
descriptive only. GSE290297 has no animal field at all, so the bulk libraries
cannot carry this question.

The discriminating measurement is a **per-cell joint protein readout**: Th17n
differentiation under 1 mM against 25 mM glucose, and under the Th17p cytokine
cocktail, with intracellular Foxp3, CTLA4, IL-17A and IL-17F co-stained in the
same cells, a division tracker to hold proliferation, and the mouse as the
unit. The endpoint is the **joint distribution**, not two marginal means: the
question is whether cells that lose Foxp3 are the same cells that gain IL-17.
Single-cell RNA cannot substitute, because the anti-correlation rival lives in
the transcript lists themselves.

A cheaper intermediate exists and is not decisive: score the arms separately in
an independent Th17 nutrient dataset. [Wp-E5](../E5_RESULTS.md) screened for
one and found 50 candidates deferred to record inspection with none admissible,
so this route is open but currently unavailable.

## Informative outcomes

| Outcome | Interpretation and action |
|---|---|
| Foxp3/CTLA4 fall with IL-17 flat under glucose restriction, and IL-17 rises with Foxp3/CTLA4 flat under Th17p cytokines | Supports separately regulated competences; a one-sided score move is then a real biological statement and the two routes must be reported separately |
| Both proteins move reciprocally under both perturbations | One latent axis; the arm asymmetry is a property of the gene lists and the score should be reported as a single axis |
| Cells losing Foxp3 are disjoint from cells gaining IL-17 | Composition, not within-cell transition; the glucose result is a mixture shift and Wp-P03's inconclusive within term is explained |
| Effects vanish when division is held constant | Proliferation confound; both the mouse and human legs need a growth-matched comparison before any arm claim |
| Mouse-level variation swamps the contrast | Report inconclusive with the achieved precision; do not add conditions to recover a sign |

## Contribution and readiness

Contribution description: **model discrimination**, between a one-axis and a
two-competence reading of an established score. Neither module is novel; both
are the published Gaublomme 2015 lists, and Th17 plasticity including
Foxp3/IL-17 co-expression is long established — those are premises, not
findings claimed here. What is unresolved is whether the score's two arms move
independently under different perturbation classes, which is what the executed
evidence newly raises and cannot settle.

Readiness: the design is specified but **not executable in this package**. It
needs culture work with protein readouts and animal-level replication. No
effect margin is nominated, because the package holds two mice and no
independent dataset from which one could honestly be derived.
