# Wagner RQ framing against the recent merged standards

4 October 2026. Owner-requested review of the six cards at `359fd63`.
Live GitHub merged-PR metadata and a fresh fetch confirm that the latest merged
main is `a5d41834395cac0b82b488d48759ceb6fab8f2d5` (PR #136). The applicable
standards below are identical in this worktree and main. This is an authoring-
agent audit, not independent scientific review or a human adoption decision.

**Finding: partial alignment, with different roles across the six cards.**
P03/P06 contain provisional biological hypotheses. P04 is a source-replication
and model-discrimination companion whose directional hypothesis remains
incomplete. P05 is a directional prediction proposal for possible association
with A1, not an established regulatory mechanism or adopted A1 specification.
P01/P02 are explicitly supporting measurement questions. The earlier summary
of four biological cards was too coarse to communicate these distinctions.

## Which merged standards were checked

| Merged PR / current authority | Requirement used in this audit |
|---|---|
| [#130: grounded research packages](https://github.com/xorca0711/scRNA_seq/pull/130), [governance](../../../docs/RESEARCH_GOVERNANCE.md) | Separate drafting, scientific review and execution. Record unit, endpoint, rival, exposure and unknown feasibility; descriptive/predictive work is legitimate within its stated purpose |
| [#133: local entrypoints](https://github.com/xorca0711/scRNA_seq/pull/133), [alignment record](../../../docs/research_dossiers/RQ_ENTRYPOINT_ALIGNMENT_2026-10-03.md) | Readers opening a workspace should see its current comparison, rival, unit/endpoint, evidence and next decision; a historical plan cannot silently own current scope |
| [#134: biological specificity](https://github.com/xorca0711/scRNA_seq/pull/134), [applied revision](../../../docs/research_dossiers/NOVELTY_SPECIFICITY_APPLICATION_2026-10-03.md) and [owner rule](../../../RESEARCH_QUESTIONS.md#execution-and-interpretation-rules) | Preserve named population, input, biological process, directional/causal prediction and discriminating outcome. Measurement eligibility and prediction gain cannot substitute for the organizing biological explanation |
| [#135: Nb5 application](https://github.com/xorca0711/scRNA_seq/pull/135) | Supporting branches can remain supporting; distinct biology is not merged merely because it shares an analysis. Registration and numbering are not acceptance |
| [#136: literature and illustrations](https://github.com/xorca0711/scRNA_seq/pull/136), [workflow](../../../docs/LITERATURE_WORKFLOW.md) and [context template](../../../docs/templates/LITERATURE_CONTEXT.md) | Connect exact primary precedents and local observations to the proposed increment, strongest rival and informative outcomes. Preserve search/access limits and versioned qualitative guides |

The earlier [specificity critique](../../../docs/research_dossiers/RQ_SPECIFICITY_REVIEW_2026-10-03.md)
is useful rationale, but its proposed repairs are not all adopted standards:
the applied revision explicitly declines the proposed A4/Fzd5 entry gate.
PR titles or a merged example do not override the current qualified text.

## Card-by-card result

| Card | Alignment at the reviewed revision | Remaining framing issue / permitted role |
|---|---|---|
| [P01](P01.md) | Named Th17p/n contrast, score/RNA comparator, mapping/smoothing rival and assay-selection decision are present | Valid measurement support. It cannot count as a completed organizing biological hypothesis; preparation-level validation remains held |
| [P02](P02.md) | Reaction/compartment contrast, artifact rival and readout-resolution decision are present; published heterogeneity is acknowledged | Valid measurement support. Opposing score directions do not identify a causal enzyme or a new mechanism |
| [P03](P03.md) | Named DFMO/Th17n differentiation, persistence after verified recovery, suppressive function, selection/transient rivals and outcome patterns are present | Meets provisional biological-framing content. Effect definition, recovery/function qualification and closest-precedent completeness remain open; this is not accepted conversion or novelty |
| [P04](P04.md) | Named WT/conditional-deficient Th17n, DFMO, Foxp3 RNA/protein, IL-10, linked units and kinetic rival are present | Partial: “modifies ... differently” does not specify the expected endpoint pattern. Keep as source replication/model discrimination until the direction and precise RNA-versus-protein claim are grounded |
| [P05](P05.md) | Named IL-1β withdrawal, early epithelial glucose-to-lactate change, predicted lower AT1 output with slower relaxation, baseline and niche rivals are present | Meets a bounded predictive proposal. It does not establish that metabolic relaxation is a causal regulatory feature, or automatically fill A1's missing regulatory specification. Routing remains proposed |
| [P06](P06.md) | Named human neutrophil–lung fibroblast system, ARG1/substrate balance, conditional compensation direction, supply-dominant rival and collagen outcome are present | Meets provisional biological-framing content. Exact precedent, source specificity and whether the real exposure range allows compensation remain unresolved |

These assessments concern specification, not an ordering of research merit or
a human retain/reject decision. All six branches remain available.

## Findings that affect the next decision

### 1. P04 still needs a directional endpoint specification

The card's working hypothesis states that genotype modifies protein/secretory
responses differently from RNA at aligned times. That is an identifiable
model-comparison problem, but it leaves the expected biological pattern open.
The [source-grounding record](SOURCES_AND_GROUNDING.md) and qualified Wagner
paper, Results “The chromatin regulator JMJD3 maintains Treg-like state…” and
Fig. 6G–H, motivate a more specific possibility: reduced Foxp3 protein/IL-10
responses to DFMO with JMJD3 deficiency, despite a retained aggregate Treg RNA
response. This is a source premise, not a new conclusion of the local analysis.

**Required distinction before adoption:** an aggregate Treg program is not the
same endpoint as Foxp3 RNA. The current card nominates the Foxp3 RNA/protein pair.
The [local model](../MODEL_RESULTS.md) does not establish absence or equivalence
of the Foxp3 RNA interaction; its uncertainty and multiplicity remain binding.
Specify and justify which RNA endpoint carries the prediction, then state the
aligned-time pattern that would favor endpoint dependence over delay. Do not
invent a post-transcriptional mechanism merely to fill the biological-process
field. This audit records the gap; it does not adopt a new directional hypothesis.

### 2. P05 is a predictive companion; A1 scope is not silently repaired

P05 already predicts less later AT1 output with slower biochemical relaxation.
Its proposed increment is early information beyond starting RNA and current
input; general glycolysis/withdrawal biology is a published premise. The
[A1 working hypothesis](../../../docs/research_dossiers/A1.md#working-hypothesis)
still requests a regulatory feature. A biochemical rate may mark competence
without demonstrating the proposed regulatory explanation. Adoption would need
to state whether this is a supporting predictor or an explicitly broadened A1
scope, and reconcile the canonical hypothesis and guide if their meaning changes.
The current evidence links are navigation, not that adoption decision.

### 3. The entrypoint should expose hypotheses and supporting roles

The initial index primarily listed questions and grouped P03–P06 as biological
cards. Full cards supplied much of the missing detail, but the overview concealed
P04's directional gap and P05's predictive status. This review corrects the
entrypoint labels and adds substantive proposition summaries. It preserves the
original questions, unfavorable results and canonical A1/A8/A14 hypotheses.

### 4. Article-local illustration status must be explicit

The existing Mermaid figure is a dependency map, not six hypothesis/readout
schematics. The eight numerical plates are results, not substitutes for those
schematics. However, the merged context template explicitly says:

> An article-local candidate may retain an explicit pending-figure note.

Such a note is now present in the derivation index. No registered qualitative
SVG is claimed for these six proposals. If a candidate is promoted to a canonical
question or a canonical hypothesis changes, its context, local entrypoint,
versioned illustration and `question_guides` bindings must be reconciled under
the existing workflow. No new documentation category or gate exemption is needed.

## Evidence and limits of this check

The same-day [search/reading ledger](SOURCES_AND_GROUNDING.md),
[precedent audit](../PRECEDENT_REVIEW.md) and
[pre-derivation update](../pre_rq_review/LITERATURE_UPDATE.md) are reused for
unchanged biology. They separate exact published experiments, local exposed
results, version/shared-source issues and access gaps. This audit checks their
framing and traceability; it does not claim a fresh exhaustive literature search.
PGAM orientation, relevant restricted full texts and R2/R4/R5 holds remain.

No effect margin, assay readiness, independent sample count or human authority
is invented. No numerical analysis, canonical hypothesis, registry, registered
figure, contract, claim grade or governance/validator is changed. A passing gate
checks integrity and registered canonical-guide coverage; it does not certify
that each article-local proposal satisfies the biological-hypothesis rule.
Validation is recorded in [the package log](../VALIDATION.md).
