# Wp-Q3 — Is the elevated pro-inflammatory module in human CSF T cells compartment-specific or a correlate of local activation?

**Historical derivation:** the [7 October correction report](../CORRECTIONS_2026-10-07.md) and current A28–A30 dossiers supersede affected Compass/human values and inference wording below. Retain this record of what was known when the questions were proposed.

**Wp-Q3 · Proposed biological question · Outcome-exposed.**
[Derivation index](README.md) · [Overlap](OVERLAP_MATRIX.md) ·
[Grounding](SOURCES_AND_GROUNDING.md).

## Observation → gap → question

The source transported its mouse Th17 modules onto a reused human deposit
(GSE138266, Schafflick et al. 2020) and reported both modules higher in MS. That
disease comparison does **not** reproduce. [Wp-R4](../R4_RESULTS.md) found
nothing separating the disease groups in CSF at BH ≤ 0.05 — the smallest
adjusted value anywhere in CSF is programme N3 at BH 0.147 — and in blood the
modules do separate the cohorts but **so do matched-size random gene sets**
(observed +0.055 against a null spanning +0.004 to +0.070, p = 0.29), while the
declared activation set separates them in the *opposite* direction (−0.177) and
correlates with every module at Spearman −0.61 to −0.87.

The one contrast that survives a matched null is a different one.
[Wp-M3](../METADATA_PHENOTYPES_RESULTS.md) used the deposit's `tissue` field as
a paired within-donor variable, which the package had reported but never
tested, and compared CSF against the same donor's blood in ten paired donors
against 1,000 matched random sets:

| Gene set | Genes | CSF − blood | Donors up | Empirical p |
|---|---|---|---|---|
| Pro-inflammatory (S1 HVG) | 58 | +0.061 | 10/10 | **0.003** |
| Programme N3 | 25 | +0.081 | 10/10 | **0.007** |
| Activation set | 10 | +0.109 | 8/10 | **0.013** |
| Pro-regulatory (S1 HVG) | 25 | +0.007 | 6/10 | 0.394 |
| Pro-regulatory (all genes) | 58 | +0.022 | 7/10 | 0.931 |
| Th17n EGCG signature (Table S3) | 805 | +0.021 | 8/10 | 0.297 |

The arm asymmetry is specific and one-sided, and it is the **opposite arm** from
the mouse glucose experiment. But the activation set moves too, in the same
direction, and a paired donor-level contrast on ten donors cannot separate "the
pro-inflammatory programme is specifically elevated" from "these cells are
activated and the module overlaps activation".

**Question.** In human CNS autoimmunity, is the elevated pro-inflammatory
programme in CSF T cells a compartment-specific state, or a correlate of local
activation that any activation-adjacent gene set would show?

## Hypothesis and biology

The CSF compartment imposes a state on T cells that is **not reducible to
activation**: a locally sustained effector programme, with regulatory
competence unchanged rather than suppressed. The directional prediction is that
when CSF and blood T cells are compared **within a matched activation state**,
the pro-inflammatory elevation persists and the pro-regulatory arm still does
not move. An activation-only explanation predicts the elevation collapses once
activation is held.

The biological interest is the arm asymmetry, not the elevation. The same score
construction moves through its regulatory arm under nutrient restriction in
mouse culture and through its effector arm in a human inflamed compartment. If
both hold, a single "pathogenicity" readout is reporting two different cell
states, and the compartment is doing something the nutrient perturbation does
not.

## Strongest rivals

1. **Activation.** CSF T cells being more activated than blood T cells is the
   expected finding. The activation set exceeds its own null here, so this is
   not a hypothetical rival but a measured competitor.
2. **Tissue residency and recirculation.** CSF samples a migratory population;
   cells recovered there may differ in origin rather than in acquired state.
   Nothing in a paired contrast establishes that the same cell would have
   scored lower in blood.
3. **Composition.** The CSF CD4-lineage pool differs in subset mixture from
   blood. The elevation may be a mixture shift, exactly as
   [Wp-P03](../P03_RESULTS.md) found for the mouse glucose effect, where the
   composition term carried it and the within-state term was inconclusive.
4. **Deposit-level limits.** [Wp-R0](../R0_RESULTS.md) and Wp-R4 record two
   fixes this leg required: one CSF library was deposited unfiltered
   (737,280 barcodes, needing a 500-UMI floor) and a hard-zero lineage gate
   left 1 to 124 cells in four blood libraries. The deposit carries no age,
   sex, treatment or disease-duration field, so none of this can be adjusted
   for donor characteristics.

## Unit, contrast and endpoint

Donor, paired within donor. Ten donors contribute both compartments; cells are
descriptive. This is the only donor-level unit anywhere in the source.

Two legs, in increasing cost:

- **Reanalysis leg, available now.** Repeat the paired contrast *within*
  activation strata defined independently of the modules, and report the
  pro-inflammatory and pro-regulatory arms separately with the same matched
  null. Also decompose the paired difference into composition and within-state
  terms, as Wp-P03 did for the mouse arm. This cannot defeat residency, and
  with ten donors it is a precision-limited test; it is specified so the
  package knows what it would and would not settle.
- **Measurement leg, not available here.** Paired CSF and blood CD4 T cells
  from the same donors, sorted on activation markers, with intracellular
  IL-17A and Foxp3 protein, and TCR sequencing to identify cells of shared
  clonal origin across compartments. Shared clones compared across compartments
  is the only readout that addresses residency with the donor as unit.

## Informative outcomes

| Outcome | Interpretation and action |
|---|---|
| Elevation persists within matched activation strata, pro-regulatory still flat | Supports a compartment-specific effector state; the arm asymmetry becomes a reportable contrast against the mouse result |
| Elevation collapses once activation is held | Activation explains it; Wp-M3's result is downgraded to an activation correlate and the arm asymmetry claim is withdrawn |
| Composition term carries the paired difference | A mixture shift, not a within-cell state; the same reading as the mouse glucose result and the two become one phenomenon |
| Shared clones score alike across compartments | Residency or recirculation, not an acquired compartment state |
| Ten donors cannot separate the strata | Report inconclusive with achieved precision; do not relax the stratification to recover significance |

## Contribution and readiness

Contribution description: **measurement validation and boundary extension** of a
published transfer that did not reproduce as published. CSF T-cell
compartmentalisation in MS is established and is a premise; the specific
unresolved point is whether this module's one-sided elevation is distinguishable
from activation, which the source never tested because it reported a disease
contrast instead.

Readiness: the reanalysis leg is **executable in this package** under a new
contract, and is the only one of the three candidates for which that is true.
Its limits are known in advance and stated above. The measurement leg needs
clinical samples this project does not hold, and nothing here nominates an
effect margin on ten donors.
