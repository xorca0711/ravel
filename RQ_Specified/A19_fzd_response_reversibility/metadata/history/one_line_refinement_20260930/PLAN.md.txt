# A19 investigation plan

**Current execution route:** [extension pipeline](EXTENSION_PIPELINE.md) ·
[external evidence review](EXTERNAL_EVIDENCE.md) ·
[draft execution specification](config/extension_pipeline_draft.json).
The stages below retain the parent H1–H3 design; P1–P3 in the extension document
are priorities that prepare or conditionally execute those tests, not a new
numbering of the parent stages.

This proposed design derives from exposed results; it is not a frozen confirmatory
protocol. Numerical thresholds and assay details remain unselected. No new fit is
required to restate the Nb2 premise.

## Stage 0: eligibility before fitting

For each candidate record the independent animal/donor/preparation, initial
population, culture/injury context, input identity, actual engagement, withdrawal
verification, observation time, repeated-unit links and independent mature/viability
endpoints. Count units per **contrast**. Replicate suffixes and cell numbers do not
establish independence. Review accessible supplements, author-provided and public
data first; new data generation is conditional on finding no eligible evidence.

GSE208770 supplies exposed bulk RNA but no required Fzd schedule with linked later
outcome. GSE327565 is a Stk3/4-loss reference, not Fzd withdrawal. GSE262927 supplies
state context without randomized Fzd treatment; transitional coverage fails. None
is the H1–H3 validation set. Human basaloid FZD6 enrichment is a separate population
context, not evidence that an AT2 response transfers to airway-derived cells.

## Stage 1: primary temporal comparison

Specify the total effect of intermittent versus continuous receptor stimulation
at a common observation time and comparable starting population. Choose the
exposure convention prospectively: equal on-period intensity is a schedule effect
including different cumulative input. Equal cumulative input asks a different
question and belongs in a separate design contrast. A drug-free interval alone
does not establish a biological off-period.

Primary outcome: absolute mature lineage-descendant output per initial viable
labeled population. Retained AT2 capacity and later-bout response are separate
preservation criteria. Avoid fraction-only outcomes that rise when other cells
die. Do not select or match on achieved expansion after treatment; it may mediate
the schedule effect.

Record biological units, baseline variation, repeated measures and batch allocation.
Before new outcomes, freeze an endpoint-appropriate model, useful gain margin,
capacity-preservation margin, uncertainty rule, exclusions and independent
validation. A sample floor is not a power calculation. Meaningful mature-output
gain with retained capacity supports H1; precise failure of either nominated
criterion weakens the combined claim. Imprecise or missing outcomes are inconclusive.

## Stage 2: conditional state and input contrasts

H2 estimates a treatment-by-**initial-state** interaction with states defined before
exposure independently of the outcome. Post-treatment states can be mediators;
do not condition on them as if randomized. A difference in significance is not
an interaction test. Compare the interaction in an a priori receptor-abundance
range or model baseline receptor abundance separately, where reliable measurement
and overlap permit; do not infer beyond-abundance effects without that contrast.
Sparse states stop the comparison rather than being merged until a signal appears.

H3 uses a common engagement range established by independent calibration or a
designed response surface. Do not match on observed post-treatment Wnt/YAP score
or growth and call the remainder an unbiased route effect. CHIR has a different
point of action; unequal exposure/off-target activity remain rivals. Direct
activity and later fate must be linked to claim a connecting mechanism. YAP/TAZ
dynamics, canonical output and branch-specific signaling are separate measures;
the three-gene panel cannot identify them.

Freeze H2/H3 interaction/effect margins and multiplicity separately. A precise lack
of meaningful interaction weakens H2; inconsistent engagement is inconclusive.
H3 can support an input-specific total effect without identifying its mediator.
Mechanistic mediation requires its own causal design.

## Reporting and stop rules

Report H1–H3 separately, including unfavorable results, complete unit counts and
prespecified contrasts. RNA scores are supporting readouts; the mature outcome
cannot be the same predictor panel. Missing independent endpoints, failed
engagement, unresolved units or absent initial states stop the affected inference.
First deliverable: candidate-source eligibility and an amended prospective
contract, not another score sweep of Nb2.


## Execution addendum, 30 September 2026

The owner authorized A19 analysis and formal figures. The bounded
[source inventory](SOURCES.md) found no complete direct Fzd schedule/fate/reserve
experiment among the inspected sources. A separate [exploratory contract](config/exploratory_v1.json)
was frozen before new numeric outcomes, with prior narrative exposure recorded.
The run executed donor-paired qPCR and source-block bulk RNA from the 2022 human
organoid study; [results](RESULTS.md), [figures](FIGURES.md) and [methods](METHODS.md)
are deposited here. This is not another fit of the exposed Nb2 matrix.

The observations motivate a post-analysis refinement: release from a maintenance
input may permit alveolar maturation only while alveolar competence is retained;
otherwise alternative lineage states or selection may dominate. That proposition
is biological and falsifiable through traced mature output and reserve, rather
than through agreement between marker scores. Direct H1–H3 decisions remain
unresolved. The original stages, competing explanations and prospective
confirmatory gate above remain in force; no outcome-derived numerical margin
or accepted mechanism is inserted retrospectively.


## Integrated extension amendment, 30 September 2026

The owner requested that the three proposed priorities be integrated with the
results' hypothesis-refinement section, then added an external web evidence
review. [EXTENSION_PIPELINE.md](EXTENSION_PIPELINE.md) now specifies eligibility,
contrasts, units, competing explanations, decision/stop rules and planned
artifacts for cellular identity (P1), existing input-context effects (P2) and
linked functional evidence (P3). The draft JSON records pending numerical
choices; it is not a frozen single-cell or confirmatory contract.

The [eight-study evidence review](EXTERNAL_EVIDENCE.md) supports competing-fate
biology and adds the missing-maturation-cue and modifiable-state alternatives.
It distinguishes already used studies, reference datasets and potentially useful
functional results. No reviewed source is assumed to join every required
endpoint. S0 and S1 state questions remain separate, and the original H1 reserve
criterion is retained. Existing scientific outputs remain unchanged; the
[pre-amendment versions](reports/history/2026-09-30-before-extension/snapshot.json)
of the edited question documents are preserved.
