# A30: literature context and hypothesis schematic

Reviewed 5 October 2026. This note connects published findings to the current
proposed question. It is a bounded synthesis, not novelty clearance and not
scientific acceptance. The searches actually executed, their hit counts and
their coverage limits are recorded in the
[package literature update](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/LITERATURE_UPDATE.md).

## Published starting point

CSF compartmentalisation in multiple sclerosis is established, and a CSF-enriched Th17-lineage subset has since been described. Both are premises; the first is also the deposit this question would reanalyse.

| Primary source | Inspected locator and access record |
|---|---|
| [Schafflick et al. 2020, *Nat Commun* 11:247](https://doi.org/10.1038/s41467-019-14118-w) (PMID 31937773) | Abstract inspected 5 October 2026; the GSE138266 deposit reused by the source and by Wp-R4/Wp-M3. Location-associated CSF leukocyte composition and transcriptome; MS increases CSF cell-type diversity including cytotoxic T helper cells. **Same evidence lineage, not independent support.** |
| [EBioMedicine 2026, 106324](https://doi.org/10.1016/j.ebiom.2026.106324) (PMID 42250325) | Abstract inspected 5 October 2026; a CCR5-high Th17.1 cluster enriched in CSF versus paired blood, pre-cytotoxic, reduced after natalizumab. Supplies a named candidate population for the composition rival. |

## Repository observation

The source's published disease comparison does not reproduce: nothing separates the disease groups in CSF at BH ≤ 0.05, and in blood matched-size random gene sets separate the cohorts as well as the modules do (p 0.29). The surviving contrast is paired within donor: pro-inflammatory +0.061 in 10/10 donors (p 0.003), pro-regulatory +0.007 (p 0.394) and +0.022 (p 0.931), activation +0.109 (p 0.013). No donor covariate fields exist in the deposit.

Exact current result locators:

- [A30 workspace](README.md) and [development plan](PLAN.md)
- [Derivation card](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/Q3_csf_compartment.md)
- [Overlap screen against A0 to A27](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/OVERLAP_MATRIX.md)
- [Grounding and exposure record](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/SOURCES_AND_GROUNDING.md)
- [Reproduction scope and claim-by-claim outcome](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/REPRODUCTION_SCOPE.md)

## What this question could add

Test whether a transported module's one-sided elevation in CSF is distinguishable from local activation — which the source never tested, because it reported a disease contrast that does not reproduce. The reanalysis leg is executable in this package and its limits are known in advance, so a negative is as informative as a positive.

## Current hypothesis and rival

The cerebrospinal fluid compartment imposes an effector state on CD4-lineage T cells that is not reducible to local activation, with regulatory competence unchanged rather than suppressed. The prediction is that within matched activation strata the paired CSF-minus-blood elevation of the pro-inflammatory module persists while the pro-regulatory arm still does not move; an activation-only explanation predicts the elevation collapses. Compartment association is not evidence that the compartment caused the state.

**Strongest rival:** Local activation, which exceeds its own matched null in the same direction (+0.109, p 0.013) and is therefore a measured competitor rather than a hypothetical one. Tissue residency or recirculation, and composition — now with a named candidate in the CSF-enriched CCR5-high Th17.1 cluster.

## What the comparison would teach

Repeating the paired within-donor contrast inside activation strata defined from genes disjoint from both modules, with both arms reported against the same matched random-set null and the paired difference decomposed into composition and within-state terms. Persistence within strata with the pro-regulatory arm still flat supports a compartment-specific state; collapse supports activation; a dominant composition term indicates a mixture shift. Shared-clone comparison across compartments would be needed to address residency, and that requires samples this project does not hold.

## Hypothesis schematic

![A30: proposed comparison and strongest rival](schematics/hypothesis_v1.svg)

[Editable hypothesis schematic](schematics/hypothesis_v1.svg). Original
explanatory artwork. Dashed arrows denote the labelled proposal or rival;
shapes, colours and any counts are qualitative, not observations. The readout
cards explain which uncertainty a measurement could resolve. Missing features
and endpoints remain marked. This figure depicts a proposed question, not a
completed analysis.

## Next literature check

Planned, not reported as newly executed: forward citations of the closest
inspected primary sources above, and the queries recorded as pending in the
[package literature update](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/LITERATURE_UPDATE.md).
Expand to synonyms and contrary findings using the
[literature workflow](../../docs/LITERATURE_WORKFLOW.md). Recheck the exact
population, comparison, timing, unit and endpoint before making any stronger
contribution claim.

**Current unresolved specification:** Repeat the paired contrast within independently defined activation strata, reporting both arms against the same matched null and decomposing the paired difference into composition and within-state terms, with the stratification fixed before any value is inspected. This leg is executable in the package; the residency question needs paired samples with protein and TCR readouts that this project does not hold.

**Interpretation limit:** Module scores are RNA, not protein, secretion or
function. Reanalysis of the source deposits shares one evidence lineage with
the source paper and never becomes independent replication. No search
certifies novelty and no absence of a hit is evidence of a first.

[Current dossier](../../docs/research_dossiers/A30.md) · [Canonical card](../../RESEARCH_QUESTIONS.md#a30)
