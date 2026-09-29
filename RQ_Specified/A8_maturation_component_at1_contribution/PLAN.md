# A8 analysis plan: freeze the partition and qualify a linked mature endpoint

Written 28 September 2026, before any A8 endpoint has been computed. A8 is a registered question
whose blocking input is an eligible linked dataset, so this plan is short by design: it fixes what must be
written down before an endpoint is opened, and it states the gate that a candidate dataset would
have to clear. No endpoint analysis is ready to run on the examined repository evidence.

**Corrected 29 September 2026:** retain separate association and prospective-prediction
routes, consistent with the register. The earlier blanket exclusion of concurrent
measurements was too narrow.

## Structure

```mermaid
flowchart TB
    S0[Stage 0: registration, this folder] --> S1[Stage 1: freeze the component partition, no endpoint opened]
    S1 --> S2[Stage 2: external eligibility gate for a measured mature AT1 endpoint]
    S2 -->|no candidate identified in examined evidence| BLOCK[Remain blocked, bounded search or data request]
    S2 -->|a deposit clears it| S3[Stage 3: execution, needs authorization]
    S3 --> S4[Stage 4: report and register readiness row]
    BLOCK --> W[Eligible existing data or a feasible new measurement]
```

## Stage 0: registration, which is what this folder contains

The question, its [rationale](RATIONALE.md), this plan and the
[contract](config/a8_question_contract.json). A8 is already in the canonical register, so this
folder adds no identifier; it replaces a card-only presence with a workspace. No endpoint scored,
no dataset opened for A8, no claim row.

## Stage 1: freeze the component partition, before any endpoint is opened

This is the step the founding observation actually licenses. It is specification, not computation.

**What must be written down.** A disjoint partition of the source-derived lists into a
shared-transition component and a maturation-specific component, with the 119 overlapping genes
assigned explicitly and by a stated rule rather than case by case; the exclusion of the
seed-unstable four-gene late-AT1 panel from any primary role, with its instability recorded; a
minimum component size below which a component is declared unusable rather than scored; and the
normalization and depth conventions, fixed in advance.

**Why it is frozen before the endpoint.** Under the measurement rival, the partition itself
determines the answer. A partition chosen after an increment is visible cannot distinguish a
maturation component from a favourable assignment of shared genes.

**What Stage 1 may not conclude.** Nothing biological. A frozen partition is an instrument. Its
existence is not evidence that the components measure different processes, and the overlap
arithmetic that motivated it stays a property of two gene lists.

## Stage 2: common eligibility conditions and two timing routes

A deposit or experiment is eligible only if it satisfies all five common conditions
**simultaneously**, then meets the timing contract of the nominated route.

1. **Mature AT1 contribution measured independently of RNA** — protein, morphology, or a traced
   descendant yield. An RNA score of AT1 identity is not the endpoint, whatever its gene list.
2. **An epithelial RNA measurement in the same biological units** as the endpoint, so the
   frozen components can be computed where the outcome was measured.
3. **Documented predictor and endpoint timing**, with the interpretation route specified before
   analysis. Timing requirements differ between association and prospective prediction below.
4. **Biological replication at the animal, donor or preparation level**, at least three
   independent units per arm, with unit identities deposited. Repeat wells split from one
   mixture are not independent preparations.
5. **The endpoint's definition independent of the predictor's genes**, so that an increment
   cannot be produced by shared membership.

| Route | Timing and estimand | Interpretation boundary |
|---|---|---|
| Incremental association | Concurrent RNA and independently measured mature contribution are eligible; document timing and test the maturation component's added association conditional on shared transition | Does not establish future prediction or a mechanism |
| Prospective prediction | RNA precedes the endpoint in the same biological units, with feasible linkage documented; test added information about the later endpoint conditional on shared transition | A concurrent endpoint cannot qualify, and predictive information alone does not establish a mechanism |

**Stop rules.** Missing endpoint independence, biological-unit linkage or documented timing
blocks either route. A concurrent dataset may qualify for association but cannot be relabelled
as prospective prediction. A candidate satisfying every condition except the replication floor
may be described as explicitly non-inferential and may not change the readiness row. A search
that identifies no eligible candidate is recorded as a sourcing result, not a biological negative
result. No condition is relaxed to obtain a testable dataset.

**State on 29 September 2026.** No eligible linked candidate has been identified in the examined
evidence, and **no public-data search has been performed under these contracts**. The
[shared outcome inventory](../A1_transitional_epithelial_state_distinction/reports/A1_A8_A14_OUTCOME_INVENTORY.md)
records A8's linkage requirement as row O27. O2/O3 already include non-RNA mature endpoints and
genetic lineage-labelled outcomes; their compatibility with A8's RNA predictors and biological
units is not established. O29's lack of documented EdU, BrdU or label-retention assays is a
separate assay-coverage observation, not evidence that genetic tracing endpoints are absent.
That survey covered the A1 documents, not the public archives, so the absence of a candidate here
is a statement about what has been examined and not a claim that no such deposit exists.

## Stage 3: execution, not authorized

Stage 3 needs an eligible dataset and a separate owner authorization. Nothing to execute exists
at present, so no authorization is sought.

## Stage 4: report and register

One report per executed stage with a run record carrying input hashes, the script hash and the
seed. The register effect is bounded in advance: an executed stage may change the A8 readiness row
in [RESEARCH_QUESTIONS.md](../../RESEARCH_QUESTIONS.md#a8) and may add a negative result, and may
not add a graded claim row without the owner's decision.

## The discriminating evidence, for completeness

Use RNA components and an independently measured mature AT1 contribution linked within verified
biological units. Concurrent measurements can test incremental association. A feasible linkage
from earlier RNA to a later endpoint can test prospective prediction. Either existing data or
new measurements may satisfy the selected contract. The frozen maturation component is tested
for added information over the frozen shared component. The
decision rule is the register card's: added information that transports supports the nominated
component; a precise absence of a meaningful increment weakens it; missing endpoints or
imprecision is inconclusive.

## What this plan refuses to do

- To score both the predictor and the mature outcome from RNA, in any form, including two
  different panels drawn from overlapping source lists.
- To use the four-gene late-AT1 panel as a primary instrument while its direction depends on the
  technical seed.
- To treat A10's organoid size, a cycling score or a transitional score as the mature outcome.
- To report concurrent association as prospective prediction.
- To pool preparations, relax the three-unit floor, or reassign the 119 shared genes after an
  increment has been seen.
- To interpret a shrinking increment after disjointification as evidence against a maturation
  component, or a persisting one as evidence for a mechanism.

## Order of work

1. Write the partition freeze of Stage 1. It requires no data and it is the prerequisite for
   everything else.
2. Perform a bounded Stage 2 search under the two contracts, recording the examined sources,
   linkage and timing checks, and a dated sourcing result if nothing clears.
3. If a deposit clears, seek authorization for Stage 3; otherwise the next action is not an
   analysis but a data request or assessment of a feasible new measurement.
