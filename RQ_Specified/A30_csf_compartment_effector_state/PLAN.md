# A30 development plan

> **Current interpretation, 7 October 2026:** read the [PR140 audit](../../docs/audits/2026-10-07-pr140/REPORT.md) and [revised extension baseline](EXTENSION_BASELINE_V2.md). The historical text below is retained; activation exclusion, regulatory equivalence and TCR-based residency claims are not supported.

Draft after outcome exposure; **no executable contract is frozen**. The
elements below are what a prospective contract must fix before any value is
computed, in the order the repository's execution rules require.

## Biological decision

In human CNS autoimmunity, is the elevated pro-inflammatory programme in CSF T cells a compartment-specific state, or a correlate of local activation that any activation-adjacent gene set would show?

## Estimand

The paired within-donor CSF-minus-blood difference in the pro-inflammatory module score, estimated within activation strata defined independently of the modules; and separately, the decomposition of that paired difference into composition and within-state terms.

## Biological unit

Donor, paired. Ten donors contribute both compartments. Cells are observations within donor.

## Eligible observations

CD4-lineage T cells passing the Wp-R4 gate and per-unit floors already recorded, from the ten donors with both compartments. The unfiltered CSF library keeps its 500-UMI floor; the four blood libraries with 1 to 124 gated cells are excluded from the paired set and the exclusion is reported.

## Primary comparison

Paired CSF-minus-blood on the pro-inflammatory arm within activation strata, against a matched-size random-set null of 1,000 draws. The pro-regulatory arm is reported alongside on the same null, always, whichever way the primary falls.

## Multiplicity family

Family = the two arms crossed with the declared strata. The other twelve gene sets scored in Wp-M3 are reported in full as context, as the metadata contract already requires.

## Meaningful effect or prediction margin

None nominated on ten donors. A null result is reported as precision-limited, never as evidence of absence.

## Validation split

Not applicable — no predictive model. Activation strata must be defined from genes disjoint from both modules, and that gene list is frozen in the contract before any stratified value is computed.

## Evidence qualification before computation

The stratification, the arms, the null and the decomposition are fixed before any stratified value is inspected. This leg cannot defeat residency; that limit is declared in advance rather than discovered afterwards.

## Strongest rival to defeat

Local activation, which exceeds its own matched null in the same direction (+0.109, p 0.013) and is therefore a measured competitor rather than a hypothetical one. Tissue residency or recirculation, and composition — now with a named candidate in the CSF-enriched CCR5-high Th17.1 cluster.

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
The [derivation card](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/Q3_csf_compartment.md) holds the full
observation-to-question trace.

[Dossier](../../docs/research_dossiers/A30.md) · [Workspace](README.md) · [Canonical card](../../RESEARCH_QUESTIONS.md#a30)
