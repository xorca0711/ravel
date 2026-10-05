# A29: literature context and hypothesis schematic

Reviewed 5 October 2026. This note connects published findings to the current
proposed question. It is a bounded synthesis, not novelty clearance and not
scientific acceptance. The searches actually executed, their hit counts and
their coverage limits are recorded in the
[package literature update](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/LITERATURE_UPDATE.md).

## Published starting point

Three published mechanisms could produce the source's phenotype, and a fourth result points the opposite way in a different cell context. None is proposed here as new.

| Primary source | Inspected locator and access record |
|---|---|
| [Ishikawa and colleagues 2023, *Cell Rep* 42:112205](https://doi.org/10.1016/j.celrep.2023.112205) (PMID 36857180) | **Full text retrieved and read 5 October 2026** (open access). PEP binds JunB and blocks JunB/BATF/IRF4 DNA binding, suppressing IL-17A without significant change to glycolysis, proliferation or survival. PGAM sits two steps upstream of PEP. |
| [Brucklacher-Waldert et al. 2017, *Cell Rep* 19:2357](https://doi.org/10.1016/j.celrep.2017.05.052) (PMID 28614720) | **Full text read 5 October 2026** (earlier pass). Cellular stress supports Th17 differentiation in the ABSENCE of TGF-β; 2-DG enhances polarisation; mechanism is sustained cytoplasmic calcium with partial XBP1. |
| [Toriyama et al. 2020, *Commun Biol* 3:394](https://doi.org/10.1038/s42003-020-01122-w) (PMID 32709928) | Abstract inspected; complete T-cell *Pgam1* deletion attenuates CD4 and CD8 responses, so dose matters. |
| [iScience 2025, 114051](https://doi.org/10.1016/j.isci.2025.114051) (PMID 41399496) | Abstract inspected; 2-DG REDUCES IL-17A in lung Th17 tissue-resident memory cells — the opposite direction, in a different cell context. |
| [Huang et al. 2019, *Cell Metab* 30:1107](https://doi.org/10.1016/j.cmet.2019.09.014) (PMID 31607564) | **Paywalled; abstract only.** No TGF-β in the abstract. Remains a flag, not a refutation. |

## Repository observation

Against an expression-decile-matched null, EGCG in Th17n raises the Th17 effector programme (+0.544, p 0.000) while histones, serine/one-carbon, cell cycle and ribosomal proteins fall and the integrated stress response is the most downward-shifted set (−0.491, p 0.000); UPR, NRF2 and heat shock do not move. A frozen sensitivity shows the ISR result is not carried by the two genes shared with the serine set. ATF4 output falls while ATF4 itself does not move and SESN2 rises.

Exact current result locators:

- [A29 workspace](README.md) and [development plan](PLAN.md)
- [Derivation card](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/Q2_biosynthetic_demand.md)
- [Overlap screen against A0 to A27](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/OVERLAP_MATRIX.md)
- [Grounding and exposure record](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/SOURCES_AND_GROUNDING.md)
- [Reproduction scope and claim-by-claim outcome](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/REPRODUCTION_SCOPE.md)

## What this question could add

Determine which published mechanism produces this paper's phenotype. The source's Discussion names stress, its own libraries move the stress programme downward, and the PEP mechanism attached to the very pathway segment its Compass analysis singles out is cited only as Introduction background (reference 7) and never evaluated against its result. Distinguishing them is model discrimination among existing mechanisms, not a claim of a new one.

## Current hypothesis and rival

PGAM restriction raises Th17 effector output by lowering the phosphoenolpyruvate pool and relieving PEP-mediated inhibition of the JunB/BATF/IRF4 complex, rather than by inducing a stress response; relief of biosynthetic and proliferative demand is a third, separable possibility. The PEP route predicts that the PEP pool falls under PGAM inhibition and that PEP supplementation abolishes the effector gain; the demand route predicts that matched growth slowing without PGAM inhibition reproduces it. No mechanism here is proposed as new, and a transcript-level observation cannot establish any of them.

**Strongest rival:** PEP is genuinely unchanged, as the source's own ¹³C labelling would imply, which eliminates the primary route. Further rivals: ISR-independent stress through sustained cytoplasmic calcium that no transcript module sees; a per-cell-RNA-content compositional effect; division-rate dilution; and off-target action of EGCG.

## What the comparison would teach

Absolute PEP, 2PG and 3PG pools under PGAM inhibition, with a PEP-supplementation rescue arm, a matched growth-slowing arm that does not touch PGAM, and phospho-eIF2α/ATF4 protein. A falling pool with supplementation abolishing the IL-17 increase supports the metabolite route; an unchanged pool eliminates it; matched growth slowing reproducing the gain supports demand relief; rising phospho-eIF2α despite falling target transcripts would show transcript modules mis-read the response. The pool measurement is decisive precisely because the published 15-minute label ratio cannot distinguish a steady pool from a falling one.

## Hypothesis schematic

![A29: proposed comparison and strongest rival](schematics/hypothesis_v1.svg)

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

**Current unresolved specification:** Measure absolute PEP, 2PG and 3PG pools — not label ratios — under PGAM inhibition, with a PEP-supplementation rescue arm, a matched growth-slowing arm, and phospho-eIF2α/ATF4 protein. The pool measurement is the one quantity that separates the candidate mechanisms and the published labelling ratio cannot supply it.

**Interpretation limit:** Module scores are RNA, not protein, secretion or
function. Reanalysis of the source deposits shares one evidence lineage with
the source paper and never becomes independent replication. No search
certifies novelty and no absence of a hit is evidence of a first.

[Current dossier](../../docs/research_dossiers/A29.md) · [Canonical card](../../RESEARCH_QUESTIONS.md#a29)
