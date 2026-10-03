# RQ specificity review and proposed repairs

3 October 2026. Requested after the owner rejected the one-line atlas summaries
as too broad to motivate useful hypotheses and assays. This is a review and a
set of proposed revisions, not approval of a new hypothesis or experimental
design. No question is selected, no result is rerun, and no canonical card,
frozen evidence or claim grade is changed.

Reviewed against integrated main `537eec83fe102a7eaa3e3f34a7f6b48cf852be15`,
the registered cards/packages, their later qualifications, and the private
24-question atlas. The review branch retains the preceding explanatory-session
checkpoint `767d32c`. The original diagrams remain historical drafts; they
should not be used as the current hypothesis specifications.

## Finding: the summaries changed the scientific question

The problem is substantive, not just that the titles were short.

1. **Biological specificity was removed.** A19's Fzd input, retained alveolar
   identity and predicted withdrawal benefit became a "specified input" and
   a "defined state." A22's NKX2-1-associated directional prediction became an
   unspecified identity change affecting an unspecified chemokine.
2. **Prerequisite work replaced the organizing hypothesis.** Establishing state
   correspondence, recovering a sample join, nominating an endpoint or improving
   prediction can be useful work. They do not, by themselves, supply the
   biological explanation the owner requested. A13's "can an output be nominated"
   is an evidence-development task, not a completed biological hypothesis.
3. **Assay names replaced discriminating measurements.** Listing imaging, RNA,
   protein and function does not say which measurement separates which outcomes.
   The atlas rarely made the predicted pattern, opposing pattern and unresolved
   pattern concrete enough to guide an experiment.
4. **Generic cartoons implied more specificity than the text supplied.** A cell,
   dashed arrow and later cell do not define a mechanism. Some diagrams combined
   measurement order, state transition and cell communication in the same visual
   grammar. The arrow's biological meaning must be explicit.
5. **Validity was emphasized without establishing scientific value.** More
   controls cannot make rediscovery of a published phenomenon a new contribution.
   Withdrawal-associated recovery is already a precedent for A14; its precise
   history or compartment comparison must supply the additional question.

The [owner's biological-hypothesis rule](../../RESEARCH_QUESTIONS.md), near the end of the register,
already requires a plausible biological process, directional or causal
prediction, competing explanations and a discriminating outcome. The
[governance](../RESEARCH_GOVERNANCE.md) also correctly permits descriptive and
prediction work. Both can be respected: keep the biological question, its
supporting analysis and its current evidence gap as separate layers.

## Repair the specification before redrawing it

Each RQ should open with a short biological title followed by a substantive
hypothesis paragraph. That paragraph must retain the population, named input or
contrast, proposed process, expected direction and biological outcome. A
hypothesis can be a bounded functional relationship without a fully identified
molecular mediator; do not invent one to complete a template.

Immediately below it, explain: (a) the exact result that motivates the idea,
(b) the inferential step still untested, (c) the strongest biological rival,
(d) one comparison capable of distinguishing them, and (e) what the possible
readout patterns would mean. Specify which parts are restoration of an existing
card and which are newly proposed narrowing choices.

An assay must have a defined job. For example, lineage-linked absolute cell
counts address yield; independent protein identity and morphology address cell
identity; actual signaling engagement addresses whether the intended contrast
occurred. None substitutes for the others. Function remains a separate claim
requiring a validated model-specific readout. Endpoint-only state abundance
cannot automatically identify entry, exit, survival or selection.

Missing access does not prevent proposing a biological comparison now. Missing
biology does prevent calling an unspecified process a finished hypothesis.
Record those two kinds of incompleteness separately. Exact assay calibration,
durations, effect margins and sample sizes remain implementation work.

## Worked repair 1: A4 — test Wnt gating of inflammatory transition

**Current scope:** same-lineage Wnt-associated maintenance followed by an
IL-1-responsive transition, versus selection. See [card](../../RESEARCH_QUESTIONS.md#a4)
and [package](packages_2026-10-03/A4.md). The atlas's "does one lineage change its
response" omitted the biological input and gave a weak account of the contribution.

**Plausible new narrowing, requiring review:** in adult AT2-derived preparations,
continued Fzd5-supported Wnt signaling restricts IL-1-beta-dependent acquisition
of a transitional epithelial state; ending that input permits state acquisition
within tracked starting lineages. The alternatives are selection of a
pre-existing responsive subset, a general withdrawal/stress effect, and an
effect on later progression rather than initial transition.

Fzd5 is an explicit proposed receptor choice grounded in the published AT2
agonist precedent, not an already accepted A4 parameter. This adds a causal
gating question to the existing sequence question and therefore requires an
amendment if adopted. Broad Wnt/IL-1 crosstalk is not itself a novelty claim.

**Comparison:** continued versus ended receptor input, evaluated with and
without IL-1-beta in a common primary AT2 lineage context. Starting IL1R1 status
and Wnt response need independent characterization; a history label is not a
current-activity measurement.

**Measurements and interpretation:** resolve acquisition of an independently
qualified transitional identity over time in starting lineages, alongside
division, survival and onward progression. KRT8/CLDN4 measurements can contribute
to identity qualification but cannot alone define a fate. An input effect on
transition acquisition that depends on IL-1 favors gating. An effect without
IL-1 weakens that specificity. Expansion of already responsive lineages favors
selection. Unchanged entry but altered later AT1 output points to a later step.
If only terminal marker fractions are feasible, call the endpoint occupancy;
do not claim to have tested entry. Retain the later t0/missing-lineage refinement.

**What becomes useful:** a comparison about where Wnt acts in the transition,
with a readout that separates entry from selection and progression. Whether that
exact contrast is already answered remains a targeted novelty-review question.

## Worked repair 2: A19 — separate expansion from productive maturation

The [original card](../../RESEARCH_QUESTIONS.md#a19),
[current interpretation](../../RQ_Specified/A19_fzd_response_reversibility/RESULTS.md)
and [plan](../../RQ_Specified/A19_fzd_response_reversibility/PLAN.md) already have
more biological content than the atlas. Restore it before adding new terms.

**Proposed narrow hypothesis:** in primary AT2-derived organoids retaining an
independently defined alveolar identity, ending Fzd5-selective stimulation after
expansion increases absolute lineage-derived AT1-identity output relative to
continued stimulation, while retaining AT2 descendants capable of renewed
expansion. Fzd5 is a provisional implementation choice from a published AT2
input, not a finding or a claim of reagent access.

**Primary comparison:** withdraw versus continue that same input after a common
expansion history, with a common outcome time and documented biological cessation.
This is the temporal contrast. Receptor-selective input and CHIR are not combined
as interchangeable exposures.

**Measurements and interpretation:** count lineage-linked AT1-identity descendants
per recorded starting AT2 input using independent protein identity and morphology;
measure viable AT2 reserve and its response capacity separately. More AT1-identity
cells with retained responsive reserve supports the joint proposal. More AT1
cells with depleted reserve fails the joint criterion. A larger AT1 fraction
caused only by AT2 death fails the yield interpretation. Mature functional repair
is an additional claim until a suitable function assay is validated.

**Separate state question:** after defining alveolar-retaining and airway-shifted
states before the withdrawal comparison, ask whether the withdrawal effect
differs between them. State association does not show that the state itself
causes competence. A state recorded after the schedule cannot be treated as an
untreated baseline. Keep existing H1/H2/H3 decisions separate.

**Why plausible but unresolved:** the repository's CHIR-context observations
motivate concern about loss of alveolar identity; they are not evidence of Fzd5
withdrawal, mature function or retained reserve. The contribution must exceed
the already known general association between Wnt input and cell identity.

## Worked repair 3: A20 — retain the actual receptor comparison

This RQ already has a relatively specific
[narrowed hypothesis](../../RQ_Specified/A20_fibroblast_fzd_context/NARROWED_HYPOTHESIS.md).
The repair is to foreground its full biology rather than rewrite it as generic
"fibroblast support."

**Hypothesis:** comparable Fzd2 loss in independently identified adult AF1-like
fibroblasts reduces the maintained AT2 pool and subsequent absolute
AT2-lineage-derived AT1 output more than comparable Fzd1 loss. Reduced pool
maintenance is the proposed route; reduced maturation capacity and generalized
fibroblast loss are competing explanations.

**Comparison:** Fzd2-loss, Fzd1-loss and matched reference fibroblasts supporting
the same starting AT2 population in a qualified primary coculture. Verify
fibroblast identity and the validity of both receptor contrasts.

**Measurements and interpretation:** measure early viable AT2 yield and later
lineage-derived AT1 identity/output, plus fibroblast survival. An early pool
deficit followed by lower later output is compatible with pool maintenance. A
preserved early pool with reduced later AT1 output favors a maturation-stage
effect. Fibroblast loss may explain the total effect but weakens a narrower
claim about support from surviving fibroblasts. Do not adjust away the early
AT2 deficit in the primary total-effect comparison. None of these patterns alone
proves mediation by the early pool.

**What becomes useful:** early-versus-late measurements answer a specific
biological alternative. Organoid area alone cannot answer it. AF1 identity,
functional maturation and independent replication still require qualification.

## Worked repair 4: A14 — restore direction and split the hypotheses

Restore H1 from the [card](../../RESEARCH_QUESTIONS.md#a14): **longer prior
IL-1-beta exposure reduces later AT1-lineage recovery after verified cessation,
at comparable recovery intervals and culture age.** The distinction is incomplete
recovery after exposure history, not simply whether any recovery occurs.

Measure exposure cessation, absolute traced AT1-identity output and viable
transition/AT2 descendants. A reduction persisting beyond residual input and
simple loss supports the bounded history effect. A response explained by
continuing exposure or death does not identify persistent epithelial state.

Keep H2 separate: **fibroblast IL1R1 reception contributes to the recovery effect
beyond direct epithelial reception.** Its compartment comparison uses the same
recovery endpoint. The direction of the fibroblast contribution needs its own
evidence-based nomination; do not invent a harmful stromal effect merely because
the duration hypothesis is directional. Generic withdrawal-associated recovery
and stromal inflammatory responses already have published precedents.

## Worked repair 5: A23 — distinguish a transport-linked route from injury

**Proposed specific hypothesis:** impaired SLC34A2-dependent transport promotes
acquisition of a transition-associated epithelial stress phenotype before broad
AT2 identity loss, through disrupted epithelial phosphate handling; secondary
extracellular mineral injury is the leading alternative. This is a causal
candidate to test, not a conclusion from the current RNA pattern.

**Comparison and measurements:** compare a qualified SLC34A2-impaired and
reference primary AT2 context with extracellular mineral conditions documented.
Measure transporter-dependent function, intracellular/extracellular phosphate
compartments, time-ordered identity and viable yield separately. A discriminating
follow-up would ask whether independently restored transport function attenuates
the state phenotype. Restoration is conditional on an interpretable, validated
approach and can have pleiotropic effects; it is not assumed available.

Loss of transporter-dependent activity followed by a within-lineage state
response, and attenuation under an interpretable restoration, would support the
route more strongly than temporal order alone. A phenotype confined to generalized
injury or extracellular mineral disturbance favors those alternatives. Recovery
of transport without state recovery does not rescue the proposed link. Do not
assume the direction of intracellular phosphate from transporter RNA: other
transport activity may compensate. Three RNA markers remain a screen signature,
not a sufficient fate definition. Preserve the external PAM non-reproduction.

## Portfolio review: disposition proposed for all 24 questions

These are recommendations about framing, not a new claim/status register. Every
ID remains available and retains its [registered dossier](README.md).

| RQ | Specific defect or retained strength | Plausible repair before another figure |
|---|---|---|
| A0 | State correspondence replaced the proposed conservation/reuse biology. | Keep correspondence as a prerequisite. Identify the biological process alleged to be shared before proposing a new test; preserve the failed fixed transfer and do not retune it. |
| A1 | "Early regulation" identifies neither a regulatory feature nor a biological route. | Nominate a source-supported regulatory difference in a specified epithelial state and its expected later consequence. Keep added prediction as a supporting test; no invented regulator. |
| A2 | Source/presentation, availability and consequence remain placeholders. | Name one epithelial source contrast and one fibroblast consequence. Separate a ligand-supply effect from any residual presentation effect; general AREG involvement is already a precedent. |
| A3 | History association lost the nominated biological programme and host consequence. | Fix the programme, comparable history/age/origin context and a plausible consequence before a functional hypothesis. RNA cannot nominate metabolic flux. |
| A4 | The headline became generic flexibility; sequence alone has a weak novelty account. | Preserve the lineage-versus-selection test; consider the explicit Wnt-gating amendment above only after targeted novelty/assay review. |
| A5 | Independent replication was presented as the full biological question. | Restore developmental-programme reuse as the biological idea. Keep exact frozen replication as current work; any functional element must be independently nominated. |
| A6 | "Same-state change" omits the programme and consequential output. | Nominate the macrophage state/programme and expected consequence from sources. Retain the sparse-control hold rather than present a generic IPF assay. |
| A7 | Broad identity loss and an extra baseline-state interaction became one generic effect. | Retain CEBPA and the broad identity prediction; explicitly define the baseline states for the additional interaction. Post-treatment labels cannot supply them. |
| A8 | The frozen RNA component became generic early information. | Name the exact component and its biological interpretation separately from its measurement definition. Keep linked later AT1 contribution as the predictive endpoint; mechanistic branches need named candidates and separate tests. |
| A9 | "Competence" does not identify a receptor axis, state contrast or consequence. | Nominate a measured recipient receptor/function contrast and a fibroblast consequence at comparable AREG input; expression coverage is only eligibility. |
| A10 | Earlier prediction was insufficiently distinguished from concurrent growth association. | Retain the exact programme, observation time and growth endpoint. Present forecasting as supporting work; a causal epithelial-growth claim needs its own bounded intervention. |
| A11 | A residual component was at risk of being treated as a biological process. | Preserve fixed residual/shared/stress comparison. State that measurement specificity is being evaluated; a lesion mechanism needs independently justified biology. |
| A12 | "IL-1 competence" obscured epithelial versus stromal reception and inhibitor context. | Name one recipient compartment and one receptor/inhibitory axis with a specified downstream consequence. Keep ligand/source attribution separate. |
| A13 | "Nominate an output" is a development task, not a finished hypothesis. | Mark the biological mechanism underdeveloped. Review actual fibroblast outputs and epithelial consequences before naming a mediator; retain the negative proxy result. |
| A14 | Exposure length and direction vanished; H1 and H2 were flattened together. | Restore directional history H1, retain compartment H2 separately, and distinguish both from published generic withdrawal recovery. |
| A15 | General latent TGF-beta activation is already known; source context and consequence remain vague. | Name the particular epithelial activation contrast and fibroblast endpoint, then show why that context is informative beyond the established pathway. |
| A16 | A marker, later response and mechanism were left interchangeable. | First establish epithelial CD177 protein attribution; then nominate one later response. Do not draw CD177 as a causal fate regulator without a separate hypothesis. |
| A17 | A latent founder class was visualized like a known cell type. | Keep stable-founder versus switching/observation models explicit. Finish technical qualification; nominate new measurements only if they distinguish otherwise equivalent models. |
| A18 | "Growth versus identity" omitted what would constitute a meaningful biological dissociation. | Specify the WT lineage/context and independent absolute expansion/identity/survival endpoints. Molecular channel attribution remains a later question. |
| A19 | Fzd input, alveolar identity and expected withdrawal benefit were abstracted away. | Restore them, separate schedule/state/input hypotheses, and retain the joint AT1-output/reserve criterion. |
| A20 | The full existing receptor comparison was stronger than the short title. | Reuse the narrowed Fzd2-versus-Fzd1 hypothesis and distinguish early pool maintenance from a later maturation effect. |
| A21 | "Accompany" reduced a proposed functional route to generic co-occurrence. | Retain the proposed Fzd4 integrity-to-lineage route as a hypothesis; distinguish endothelial survival, renewal and fate with separate evidence. Do not call coupling mediation. |
| A22 | NKX2-1, predicted direction and the failed broad-score generalization disappeared. | Restore the focal NKX2-1-associated chemokine-reduction question. Name the actual protein endpoint before calling it assay-ready; do not revive broad identity generality from the failed predictor. |
| A23 | Transport impairment became unspecified "altered handling" and temporal order stood in for mechanism. | Retain the transport-linked stress hypothesis, distinguish extracellular injury, and use direct handling/restoration evidence with the external negative result visible. |

## Repository implementation proposal

1. Use the current canonical cards and amended result reports as the starting
   point; restore lost specificity without restoring obsolete priorities or
   unsupported historical interpretations.
2. Revise each dossier's opening into biological hypothesis, rationale and
   opposing prediction. Place supporting analyses, metadata holds and access
   constraints below that explanation. Do not silently promote a proposed
   narrowing such as the A4/Fzd5 example to accepted scope.
3. Align the local RQ README with that full paragraph. The one-line title is
   navigation; the decision table is a design aid. Neither replaces the argument.
4. For each proposed assay, state the measured variable, which competing result
   patterns it can distinguish, and the interpretation it cannot supply. If both
   hypotheses predict the same readout, it is not the decisive assay.
5. Redraw only after the biological contrast is coherent. A valid A19 drawing
   should show the common expansion history, continued-versus-ended named input,
   and both output branches. A4 needs entry-versus-selection/progression, not
   simply differently colored cells connected by arrows.

No new universal pipeline or validator is needed to complete this review.
Existing gates should remain. A later proposed editorial check can flag missing
named contrasts, placeholder outcomes or a diagram whose arrows have no textual
claim; it cannot establish biological plausibility or novelty. Review the actual
argument rather than rewarding filled headings.

## Evidence and limits of this review

- Repository authority: [question register](../../RESEARCH_QUESTIONS.md),
  [registry](../../analysis/research/registry.json),
  [conditional packages](packages_2026-10-03/README.md),
  [later refinements](continuation_2026-10-03/PACKAGE_REVIEW.md), and the
  [bounded novelty review](followup_2026-10-03/NOVELTY.md). The portfolio audit
  reviews framing; it is not a fresh full-text novelty review of all 24 RQs.
- [Nabhan 2023](https://pubmed.ncbi.nlm.nih.gov/37321220/) supplies the published
  Fzd5/Fzd6 AT2-input precedent. This session retrieved the indexed primary
  abstract; the publisher full-text fetch failed. Existing methods review and
  source records were reused. A proposed Fzd5 narrowing is not claimed novel.
- [Choi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/), especially the
  inflammatory transition/recovery results and Discussion, constrains A4/A14:
  broad transition biology and withdrawal-associated recovery are precedents,
  not new contributions of this proposal.
- [Uehara 2023](https://www.nature.com/articles/s41467-023-36810-8) supplies
  phosphate-homeostasis and extracellular mineral-context precedent for A23.
  It does not establish the proposed early epithelial state route.
- [Nabhan 2026](https://doi.org/10.1073/pnas.2606113123) and its repository source
  package own the A22/A23 screen context. Fresh full-text access was blocked;
  no unseen result is asserted. The current repo's adverse follow-ups remain.

Confirmed: the atlas and newer summaries omitted material biological details
that remain in several original cards. Uncertain: novelty and feasibility of
new narrowing choices, exact endpoints for underdeveloped questions, actual
model access and precision. Proposed: repair the biological argument before
changing the figures. The owner's rejection concerns framing utility; it does
not reject every biological question or erase historical evidence.
