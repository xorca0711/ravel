# A28 development plan

**Evidence update — 7 October 2026:** read the [Wp correction report](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md) before the historical derivation. Corrected scores remain descriptive; a null contrast is not equivalence, and marker protein changes alone do not establish functional competence.

Draft after outcome exposure; **no executable contract is frozen**. The
elements below are what a prospective contract must fix before any value is
computed, in the order the repository's execution rules require.

## Biological decision

In Th17 cells, does entry into the pathogenic transcriptional state proceed by loss of the regulatory programme, by gain of the effector programme, or by either route depending on the perturbation — and are the two routes distinguishable in the same cells at the protein level?

## Estimand

The within-mouse difference, between glucose conditions and between polarisation conditions, in the JOINT per-cell distribution of Foxp3/CTLA4 protein and IL-17A/IL-17F protein — not the two marginal means.

## Biological unit

Mouse. Wells from one preparation are technical replicates and do not add animals. Cells are observations within mouse.

## Eligible observations

Live single CD4 T cells passing the division-tracker gate, from Th17n cultures at 1 mM and 25 mM glucose and from Th17p cultures, all harvested at a fixed time point declared before staining.

## Primary comparison

Glucose 1 mM versus 25 mM in Th17n, on the paired per-mouse shift of the joint protein distribution. The Th17p cytokine comparison is the second declared comparison, not a post-hoc addition.

## Multiplicity family

Family = the two declared comparisons crossed with the two protein axes (four tests). Fixed before data collection; no further marker enters the family.

## Meaningful effect or prediction margin

None nominated. Two mice and no independent dataset give no honest basis for one; a margin must be set from pilot variance before confirmation, and until then the design is descriptive.

## Validation split

Not applicable — no model is fitted. If a classifier is later used to define states, train-only standardisation and held-out mice are required.

## Evidence qualification before computation

Division must be matched or modelled, because low glucose slows division and cycle phase was regressed out of the published latent space. Proliferation held constant is an eligibility rule, not a power guarantee.

## Strongest rival to defeat

One latent axis: the two modules are anti-correlated by construction, so a one-sided move may be a property of the gene lists rather than of the cells. Composition rather than within-cell state, proliferation differences, and (in the human leg) local activation are the further rivals.

## Stop and interpretation rules

If the required population, animal or endpoint support is absent, report a held
design, not a null and not a failed biological hypothesis. If outcomes are
imprecise, retain the uncertainty; no equivalence margin is supplied here. Do
not relax a failed stratum, add a condition or change a gene set after seeing
an effect. Freeze one justified primary comparison, source and code hashes,
biological units, scale, exclusions, multiplicity and prior outcome exposure
before substantive execution, and use a new registered contract with the
research runner described in [governance](../../docs/RESEARCH_GOVERNANCE.md).

Prior outcome exposure for this question is **full** on the motivating results;
a later freeze does not erase it, and any execution under this RQ is
exploratory unless it uses evidence that was unexposed when its contract was
written.

## Related questions and supporting branches

See the [overlap screen](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/OVERLAP_MATRIX.md) for the
comparison against A0 to A27 and against the other two Wp-derived questions.
The [derivation card](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/Q1_arm_asymmetry.md) holds the full
observation-to-question trace.

[Dossier](../../docs/research_dossiers/A28.md) · [Workspace](README.md) · [Canonical card](../../RESEARCH_QUESTIONS.md#a28)
