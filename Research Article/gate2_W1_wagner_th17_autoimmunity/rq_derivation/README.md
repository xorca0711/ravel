# Wagner: provisional RQ derivation

4 October 2026. Derived from the evidence and review at `1c099f0`; refreshed
main is `a5d41834395cac0b82b488d48759ceb6fab8f2d5`. The owner requested the
start of RQ derivation after the [pre-derivation review](../pre_rq_review/README.md).
These are exposed, agent-proposed questions for scientific review. They are not
human acceptance, novelty clearance, frozen experiments or new canonical A IDs.

**The first derivation pass is drafted for all six branches; framing is partially
aligned with the recent merged standards.** The [framing audit](FRAMING_AUDIT_2026-10-04.md)
identifies P03/P06 as provisional biological hypotheses, P04 as a source-replication
and model-discrimination companion with an incomplete directional specification,
P05 as a predictive companion proposed for A1, and P01/P02 as measurement support.
P05's relation to A1's regulatory-feature scope awaits adoption review; A8/A14
remain companions. All six proposals remain article-local and all prior RQs and
branch evidence remain available without ranking.

## Propositions visible at the entrypoint

- **P03 — persistent DFMO-associated suppressive function:** during naive mouse
  CD4 Th17n polarization, a subset of the DFMO-associated regulatory response is
  hypothesized to persist after verified drug/metabolic recovery and accompany
  later suppressive function. Transient inhibition and selected founder recovery
  are the strongest rivals. Linked function, viable yield and founder evidence
  discriminate them; RNA resemblance alone cannot.
- **P04 — JMJD3 dependence versus delay:** in WT and conditional-deficient Th17n
  preparations, DFMO responses may differ between Foxp3 RNA/protein and IL-10
  despite aligned times. The current proposal does not yet specify the expected
  endpoint directions. A shifted response time is the leading rival; this remains
  a comparison to develop, not a complete directional biological hypothesis.
- **P05 — early metabolic prediction:** after common IL-1β exposure and verified
  withdrawal, slower epithelial glucose-to-lactate relaxation is hypothesized to
  predict less later lineage-derived mature AT1 output beyond starting RNA state.
  Survival, residual input and stromal metabolism are rivals. Added predictive
  information would support a marker, not a causal regulatory mechanism.
- **P06 — ARG1 consumption/delivery balance:** reducing neutrophil ARG1 may lower
  ornithine supply to human lung fibroblasts while preserving arginine; under
  recipient arginine limitation, the latter is hypothesized to partly offset the
  collagen decrease. The rival is an ornithine-supply effect without compensation
  across the actual exposure range. Joint substrates, routing and collagen
  measurements distinguish these possibilities.

P01/P02 qualify score specificity and reaction resolution for assay selection;
they do not supply additional organizing biological hypotheses.

## Derived questions and proposed routing

| Card | Explicit question | Proposed role / remaining distinction |
|---|---|---|
| [P01](P01.md) | Which Th17 reaction-score associations retain information beyond matched enzyme RNA, technical variation and source smoothing? | Measurement qualification, not a new metabolic mechanism. No independent preparation split is currently qualified |
| [P02](P02.md) | Which pathway summaries conceal directionally different, correctly mapped reaction responses? | Reaction/compartment measurement prerequisite. An enzyme's RNA or reaction-score q value is not target efficacy |
| [P03](P03.md) | Does the DFMO-associated regulatory RNA response during Th17 polarization persist as drug-independent suppressive function, or resolve into a transient response or selected population? | Context and persistence question. Beyond an already published proliferation-independent phenotype or generic polyamine–Treg effect |
| [P04](P04.md) | Is the apparent JMJD3 dependence of DFMO responses endpoint-specific, or explained by delayed response kinetics? | Source-replication/model-discrimination companion to P03; directional endpoint specification remains incomplete. Compare linked assays at common times |
| [P05](P05.md) | Does early epithelial glycolytic relaxation after IL-1β withdrawal predict later lineage-derived mature AT1 output beyond starting RNA state, survival and residual input? | Predictive companion proposed for A1, with A8's fixed RNA comparator and A14's history/reception alternatives. A1 regulatory scope is not automatically resolved; A19 is a separate transport setting |
| [P06](P06.md) | Does recipient arginine sufficiency change the net collagen response to myeloid ARG1 activity, by balancing arginine consumption against ornithine delivery? | Human neutrophil–lung fibroblast context/model comparison. Source supply and recipient use are already published; the proposed increment is their joint, independently manipulated balance |

No table row is a retain/reject decision. The P05/P06 choices are **new proposed
specifications**, not features or mechanisms discovered in the local T-cell data.
P06's compensation prediction is an inference joining published premises, not
an established finding. Its detailed card explicitly allows no compensation.

## How the proposals follow from evidence

The numerical [R1](../SOURCE_SCORE_RESULTS.md) and [R3](../MODEL_RESULTS.md)
results are unchanged. R1 exposes representation differences; R3 establishes
relative bulk RNA responses with substantial program-definition sensitivity.
Neither measures tracked conversion, drug-free suppressive function, linked
RNA/protein kinetics, epithelial repair or intercellular substrate transfer.

The [source and grounding ledger](SOURCES_AND_GROUNDING.md) records the exact
comparison searches, targeted primary readings, additional Carriche and Lee
precedents, access limits and why more RNA fitting would not answer the proposed
functional questions. E1/E2/E3 from the prior review remain optional, separately
contracted analytical groundwork; they are not presented as new biological RQs.

```mermaid
flowchart TD
    E[Observed reaction scores and paired bulk RNA] --> M[P01/P02: qualify representations]
    E --> T[P03: persistence and suppressive function]
    T -. proposed companion .-> J[P04: endpoint dependence versus timing]
    L[Primary lung literature and existing A1/A8/A14] --> C[P05: early glycolytic relaxation and later AT1 output]
    S[Yadav and Hamanaka: distinct source and recipient premises] --> O[P06: arginine consumption versus ornithine delivery]
    T --> R[Prospective linked-unit evidence required]
    J --> R
    C --> R
    O --> R
```

This is a qualitative derivation map, not a measured figure or causal result.
Arrows show reasoning dependencies; no branch inherits evidence from another
tissue simply because it shares a metabolite or gene.

**Hypothesis illustrations: pending for these article-local candidates.** This
dependency map and the numerical gallery do not replace candidate-specific
hypothesis/rival/readout schematics. The merged context template permits this
explicit pending status. Canonical promotion would require the applicable
versioned guide and registry reconciliation; no such promotion is claimed here.

## What is complete and what remains

- Drafted: six derivation cards with question, biological unit, endpoint,
  strongest rival, informative favorable/unfavorable outcomes, precedent and
  explicit contribution; a concrete P05 feature and P06 source/recipient model;
  proposed overlap routing and a source-grounded review packet. The later framing
  audit records P04's directional gap and P05's predictive/A1-scope distinction.
- Required before canonical registration or adoption: scientific review of the
  exact proposed scope and contribution, including whether P03/P04 should be a
  question plus companion rather than separate global questions. No authority
  or human decision has been fabricated. See [review decisions](REVIEW.md).
- Required before execution: specimen/model access, assay qualification,
  independent-unit identities, endpoint timing, variance and a justified useful
  effect or precision target; then a new hash-bound exposed contract and freeze.
  The available RNA data cannot supply these missing functional measurements.
- Still unresolved: source R2/R4/R5 holds, PGAM signature orientation and relevant
  newly discovered restricted full texts. Exact novelty remains provisional.

This derivation does not rerun biology, alter canonical hypotheses or their
registered schematic hashes, or change a claim grade. The existing eight
article-style plates remain in the [gallery](../FIGURES.md). No additional
measured figure is generated from unobserved proposed outcomes.
