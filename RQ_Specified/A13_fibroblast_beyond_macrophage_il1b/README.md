# A13: fibroblast programmes beyond macrophage interleukin-1 beta

<!-- current-rq-framing:start -->
## Current research framing — 3 October 2026

**Proposed development scope; scientific review remains deferred.** The
question card owns the registered question. The dossier/package develop its
next discriminator; the linked result owns what has actually been measured.

| Decision element | Current question-specific summary |
|---|---|
| Proposed discriminator | Can a measured fibroblast output and a linked epithelial recovery endpoint be nominated for a test beyond comparable inflammatory input? |
| Strongest rival | Source amount, survival or shared inflammation explains the association rather than activity per fibroblast. |
| Biological unit and endpoint | Donor/preparation-resolved fibroblast–epithelial systems. The immediate endpoint is a nomination record with a measured output, independent recovery measurement, units and temporal linkage; no mediator is selected merely to fill the package. |
| Current evidence and limit | The twelve-triad TGF-hallmark/HPCS-proxy pilot worsened RMSE and models performed poorly against baseline. It establishes neither feedback nor that all fibroblast programmes are uninformative. |
| Next decision / hold | Review is deferred. Keep the causal branch held until a qualified output/endpoint pair exists; another hallmark score does not rescue the negative proxy result. |

**Read in this order:** [current evidence](../../docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md),
[development dossier](../../docs/research_dossiers/A13.md),
[conditional hypothesis package](../../docs/research_dossiers/packages_2026-10-03/A13.md).
[Deferred work](../../docs/research_dossiers/REMAINING_WORK.md) and
[execution requirements](../../docs/RESEARCH_GOVERNANCE.md) govern any later
analysis. Draft completion does not establish assay validity, resource access,
meaningful effects, precision or scientific acceptance. Existing numerical
results and original plans below retain their recorded scope.
<!-- current-rq-framing:end -->

**Nb4 follow-through, 3 October 2026:** [scoped sequential analyses](../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_SEQUENCE_RESULTS.md) and [pipelines](../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_PIPELINES.md). Article-local diagnostics preserve this question’s existing evidence and biological endpoint gates; no claim grade or acceptance decision changes.

**Related branch reviewed 1 October 2026:** [Nb3 epithelial-to-fibroblast
induction versus selection](../../RESEARCH_QUESTIONS.md#a13-candidates-20261001)
is a reverse-direction rival, not evidence of feedback or a rescue of the
later 12-triad pilot's worse held-out performance. The no-fit statements below
belong to the historical IPF/Kim coverage gate; the separately frozen pilot
is described in the follow-through linked next.

## Organizing biological question

> Do fibroblast programmes add information about epithelial plasticity beyond macrophage IL1B?

The working hypothesis is that fibroblast inflammatory, matrix and trophic
programmes contribute information about the epithelial response beyond that
contained in macrophage IL1B RNA. Shared inflammation and cell composition are
competing explanations for an apparent association.

This folder establishes whether matched macrophage–fibroblast–epithelial
measurements support a joint test, and links to the later amended pilot that
tests added predictive information. A12 asks about recipient signalling context;
A13 asks about the fibroblast programme's additional information for an epithelial
endpoint. Neither comparison alone establishes mediation or reciprocal feedback.

**Read first:** [question card](../../RESEARCH_QUESTIONS.md#a13),
[original coverage report](reports/COVERAGE_RESULTS.md),
[amended pilot and coverage decisions](../../docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md).

## Evidence and analysis history

**Rationale and plan written, 28 September 2026.** The [rationale](RATIONALE.md)
traces the broad niche proposition to the single TGF-beta-RNA/HPCS-proxy pair that
was actually tested, and states what the null does not cover -- notably that at
the primary setting no model beats the training mean, which weakens the instrument
rather than the biology. The [plan](PLAN.md) records the cycle as closed, both external
candidates as resolved on design, and the five conditions a different pair would
have to meet before any new computation. Documentation only; nothing was rescored.

**Latest follow-through:** [A13 results and candidate decisions](../../docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md). Historical specifications and numerical results below are preserved; read the dated follow-through for the current execution state.

**Scope clarification, 27 September 2026:** the [rationale audit](../../docs/audits/2026-09-27-rq-rationale/REPORT.md)
retains the zero/three-pair coverage result and no-fit decision. The recorded
fibroblast bottleneck applies to the inspected cohorts; it does not prove that
a larger or differently sampled cohort cannot supply complete triads. Comparable
states, protocol, depth and actual per-patient counts govern a new eligibility audit.

**Current scope:** the later amended 12-patient pilot is complete and shows no
aggregate held-out predictive gain. Its specification and outputs live in the
linked follow-through package. The coverage artifacts stored here retain their
earlier failed gates; they were not used to fit that later model.

**Historical coverage result, 27 September 2026: gate not met; no fit on these
inputs.** The original coverage step produced no association estimate or claim
row. The sections below describe that step and its preserved decisions.

Read the [coverage results](reports/COVERAGE_RESULTS.md). The frozen decisions are in
[`config/a13_triad_coverage_spec.json`](config/a13_triad_coverage_spec.json), committed before
any count existed.

## What the gate asked, and the answer

A joint model needs at least ten patients holding a complete macrophage, fibroblast and
epithelial triad. The card recorded six and three such donors in the two IPF cohorts and
warned that 23 human cohort patients does not mean 23 complete paired triads.

The only cohort on disk that had never been counted is the Kim lung adenocarcinoma deposit.
It gives **zero** complete paired triads at the 50-cell floor under the epithelial definition
the two IPF cohorts used, and **three** under a wider one. Both are far below ten.

**The zero is definitional.** Every one of the eleven tumour samples holds exactly zero cells
labelled type 2, because the deposit annotates tumour-sample epithelium as tumour states
instead. A paired tumour-versus-normal contrast and a type 2 epithelial compartment are
therefore incompatible in this deposit at any cohort size.

**Under the wider definition, fibroblast capture binds**, with the largest fibroblast label
reaching 50 cells in ten of twenty-two samples and a median of 32.5. That constraint is a
property of the assay rather than of the cohort, so a larger deposit does not open the gate by
itself.

## Two things a later session should know

1. **The earlier triad rule was label-level, and it was not written down.** A compartment met
   the floor when one single cell label reached it, not when its labels summed to it. The first
   run here assumed pooling, reproduced 230 of 240 prior flags, and refused at its own check.
   The rule was recovered from the disagreement pattern and now reproduces all 240. Any future
   count must use it, or its numbers will not be comparable with the six and three the card
   quotes.
2. **Do not fit anything on this coverage.** Three patients cannot support a joint model, and
   the card already warns that a met floor would not be a power guarantee either.

## Layout

| Path | Contents |
|---|---|
| `config/a13_triad_coverage_spec.json` | floors, compartment labels per cohort, the reproduction requirement, the declared reading |
| `scripts/01_count_triads.py` | standard library only, hash-verified inputs, refuses to overwrite, and refuses to report new counts if the reproduction check fails |
| `tables/` | per-unit counts, the reproduction check, the run record, and the refused first attempt |
| `reports/` | [coverage results](reports/COVERAGE_RESULTS.md) |
