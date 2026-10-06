# Wp question derivation, 5 October 2026

Derived after the reproduction ladder (Wp-R0 to Wp-R4), the eligible branch
cards (Wp-P01, Wp-P03), the metadata phenotypes (Wp-M1 to Wp-M3) and the two
extension analyses (Wp-E3, Wp-E5) had all executed under the governed runner
with verified receipts. The executed evidence is listed in
[REPRODUCTION_SCOPE.md](../REPRODUCTION_SCOPE.md#extension-work-5-october-2026);
the pre-registration checkpoint is [PRE_RQ_EVIDENCE.md](../PRE_RQ_EVIDENCE.md).

**What this folder is.** Three candidate questions proposed for registration in
the central index, each with its biological process, directional prediction,
competing biological explanations and discriminating outcome. Candidate
identifiers are article-local (`Wp-Q1` to `Wp-Q3`) until registration assigns a
central ID.

**What it is not.** It records no human retain/reject decision, no claim grade,
no scientific acceptance and no novelty finding. Every candidate is
outcome-exposed: each was proposed after its motivating result was read, which
is stated on each card and cannot be undone by a later freeze.

| Candidate | Question | Motivating evidence | Status |
|---|---|---|---|
| [Wp-Q1](Q1_arm_asymmetry.md) | Does the pathogenic shift proceed by losing regulatory competence rather than by gaining effector competence? | [Wp-R1](../R1_RESULTS.md), [Wp-P01](../P01_RESULTS.md), [Wp-P03](../P03_RESULTS.md), [Wp-M3](../METADATA_PHENOTYPES_RESULTS.md) | proposed |
| [Wp-Q2](Q2_biosynthetic_demand.md) | Does PGAM restriction raise effector output through phosphoenolpyruvate, through relieved biosynthetic demand, or through stress? | [Wp-E3](../E3_RESULTS.md), [Wp-R3](../R3_RESULTS.md), [Wp-P02](../branches/P02_serine_one_carbon_direction.md) | proposed |
| [Wp-Q3](Q3_csf_compartment.md) | Is the elevated pro-inflammatory module in human CSF T cells compartment-specific or a correlate of local activation? | [Wp-M3](../METADATA_PHENOTYPES_RESULTS.md), [Wp-R4](../R4_RESULTS.md) | proposed |

## Why these three and not the others

The package holds nine listed extension candidates and six branch cards. Most
are not question material, and the reasons differ:

- **Wp-P02** remains the highest-information *branch* in the package, but its
  conflict (this paper's Compass serine direction against Godfrey's opposite
  Treg mechanism) is a model-discrimination question whose decisive measurement
  is already specified on the card and whose RNA arm is closed as
  uninformative-for-discrimination. Registering it as a central question would
  add an identifier, not information. Wp-Q2 takes the one part of the stress
  arm that the executed evidence newly constrains.
- **Wp-P04** is permanently blocked (the EAE endpoint-class dependence needs
  per-animal data that is not deposited and that the owner has ruled out
  obtaining). **Wp-P05** resolved negative. **Wp-P06** is conditional on an
  epithelial transfer condition this package does not hold.
- **E1, E2 and E4** are validation or technical-artefact work, excluded by the
  owner's instruction. **E6** is the wet experiment, not a reanalysis question.
  **E7 to E9** were named in the checkpoint so they would be refused rather
  than revisited.
- **Wp-M1 and Wp-M2** are descriptive phenotypes of the drug and gate metadata.
  They constrain how the deposit may be read; neither proposes a biological
  process whose alternatives a feasible measurement could separate, so neither
  becomes a question on its own. Wp-M1 feeds Wp-Q2's proliferation rival and
  Wp-M2 feeds Wp-Q1's perturbation-class contrast.
- **Wp-E5** found no admissible independent nutrient dataset, so no candidate
  here may claim external support. Each card states what its two-mouse or
  ten-donor basis can and cannot carry.

## Files

- [Q1_arm_asymmetry.md](Q1_arm_asymmetry.md), [Q2_biosynthetic_demand.md](Q2_biosynthetic_demand.md), [Q3_csf_compartment.md](Q3_csf_compartment.md) — the candidate cards.
- [OVERLAP_MATRIX.md](OVERLAP_MATRIX.md) — each candidate against all 28 registered questions.
- [SOURCES_AND_GROUNDING.md](SOURCES_AND_GROUNDING.md) — published finding to repository output to proposed question, with receipt-level locators and exposure labels.
- [LITERATURE_UPDATE.md](LITERATURE_UPDATE.md) — the searches actually run, with dates, queries, access record and what each source changes.
- [JOINT_EXPERIMENT.md](JOINT_EXPERIMENT.md) — whether A28, A29 and Wp-P02 can share one preparation. A29 and P02 share a perturbation axis and should be one factorial; A28's primary is a glucose titration and shares only the mice, harvest, division gate and stain. Decision open.
