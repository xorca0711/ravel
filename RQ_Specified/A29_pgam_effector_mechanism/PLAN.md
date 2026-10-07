# A29 development plan

**Evidence update — 7 October 2026:** read the [Wp correction report](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md) before the historical derivation. Corrected scores remain descriptive; a null contrast is not equivalence, and marker protein changes alone do not establish functional competence.

Draft after outcome exposure; **no executable contract is frozen**. The
elements below are what a prospective contract must fix before any value is
computed, in the order the repository's execution rules require.

## Biological decision

Does restriction of glycolysis at PGAM raise Th17 effector output by lowering phosphoenolpyruvate and relieving PEP-mediated inhibition of the JunB/BATF/IRF4 complex, by relieving biosynthetic and proliferative demand, or by inducing a stress response?

## Estimand

The within-mouse effect of PGAM restriction on (a) the absolute intracellular PEP pool and (b) IL-17A protein per cell, and the extent to which PEP supplementation abolishes (b).

## Biological unit

Mouse. Culture wells from one preparation are technical replicates.

## Eligible observations

Th17n cultures at a fixed time point, live cells passing the division gate; metabolomics from matched parallel wells of the same preparation.

## Primary comparison

PGAM-restricted versus vehicle, on the PEP pool. Second declared comparison: PEP supplementation versus vehicle on the PGAM-restricted arm, on IL-17A protein. Third: matched growth slowing versus PGAM restriction on IL-17A protein.

## Multiplicity family

Family = the three declared comparisons. Metabolite panel members other than PEP, 2PG and 3PG are reported as context and are not in the family.

## Meaningful effect or prediction margin

None nominated. The direction of the PEP pool change is the primary outcome and is qualitative; a magnitude margin requires pilot variance.

## Validation split

Not applicable. Genetic Pgam1 reduction must be titrated and its knockdown efficiency reported per preparation, because complete deletion attenuates T-cell responses.

## Evidence qualification before computation

Absolute pools, not label ratios: the published ¹³C result cannot distinguish a steady pool from a falling one, and the whole question turns on which it is. Per-cell RNA or ribosome content must be measured so the compositional rival is addressed by data.

## Strongest rival to defeat

Absolute PEP might remain stable, which would challenge the proposed bulk-pool route; the reported isotope-label ratio does not establish that stability. Further rivals: ISR-independent stress through sustained cytoplasmic calcium that no transcript module sees; a per-cell-RNA-content compositional effect; division-rate dilution; and off-target action of EGCG.

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
The [derivation card](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/Q2_biosynthetic_demand.md) holds the full
observation-to-question trace.

[Dossier](../../docs/research_dossiers/A29.md) · [Workspace](README.md) · [Canonical card](../../RESEARCH_QUESTIONS.md#a29)
