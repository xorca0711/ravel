# A22: does epithelial identity determine fibroblast chemokine competence?

<!-- current-rq-framing:start -->
## Current research framing — 3 October 2026

**Proposed development scope; scientific review remains deferred.** The
question card owns the registered question. The dossier/package develop its
next discriminator; the linked result owns what has actually been measured.

| Decision element | Current question-specific summary |
|---|---|
| Proposed discriminator | Does a defined epithelial identity change alter measured chemokine output within comparable fibroblast states beyond viable epithelial amount? |
| Strongest rival | Fibroblast selection, source depletion or an NKX21-specific effect explains the pattern. |
| Biological unit and endpoint | Mapped epithelial and fibroblast donor/preparation units with shared mixtures and split wells nested. Measure total extracellular output of a prospectively selected chemokine per starting recipient population; report viable-cell-normalized output separately. |
| Current evidence and limit | The 672-well analysis shows a small gain that reverses after NKX21 omission and in whole-plate prediction. It weakens the broad predictor; RNA scores do not establish secretion or recruitment. |
| Next decision / hold | Review is deferred. M05/M06 retain preparation and spatial animal/treatment holds; chemokine output, within-state identity and function need separate qualification before stronger claims. |

**Read in this order:** [current evidence](reports/identity_amount_v2/RESULTS.md),
[development dossier](../../docs/research_dossiers/A22.md),
[conditional hypothesis package](../../docs/research_dossiers/packages_2026-10-03/A22.md).
Source-mapping closeout: [M05/M06 and reopening conditions](../../docs/research_dossiers/source_mapping_closeout_2026-10-03/README.md).
[Deferred work](../../docs/research_dossiers/REMAINING_WORK.md) and
[execution requirements](../../docs/RESEARCH_GOVERNANCE.md) govern any later
analysis. Draft completion does not establish assay validity, resource access,
meaningful effects, precision or scientific acceptance. Existing numerical
results and original plans below retain their recorded scope.
<!-- current-rq-framing:end -->

**Nb4 follow-through, 3 October 2026:** [scoped sequential analyses](../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_SEQUENCE_RESULTS.md) and [pipelines](../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_PIPELINES.md). Article-local diagnostics preserve this question’s existing evidence and biological endpoint gates; no claim grade or acceptance decision changes.

## Executed extension, 1 October 2026

[Identity–amount results](reports/identity_amount_v2/RESULTS.md) |
[Figure gallery](FIGURES.md) | [Frozen v2 contract](config/identity_amount_v2.json).
The same-screen P2 extension now covers 672 wells and 201 targets. Identity
reduces equal-target held-out MSE by 0.64%, but worsens it by 0.97% after NKX21
omission and by 35.00% in whole-plate prediction. The broad operational
predictor is weakened; the focal mechanism, within-state response and
protein/function hypotheses remain open. No scientific acceptance or grade changes.


**Proposed 1 October 2026; P2 descriptive extension executed, mechanism open.**
The [shared question card](../../RESEARCH_QUESTIONS.md#a22) owns the hypothesis.
The owner requested derivation after Nb3 follow-up; retain/reject and scientific
acceptance remain open. No claim grade is added.

**Hypothesis.** NKX2-1-dependent alveolar epithelial identity sustains a
fibroblast chemokine response. Loss of that identity favours wound-associated
fibroblast activity beyond differences in epithelial amount alone. The proposed
functional consequence is changed immune-cell recruitment,
which the present RNA screen has not measured.

NKX21 has AT2 −2.072, fibroblast chemokines −3.357 and wound markers +1.468 in
Nb3's marker-score contrast units. All three directions persist through the
tested control/gene/well omissions; paired-depth sensitivity retains AT2 and
chemokine reductions. Across 195 targets, however, the paired association is
only rho 0.210, falling to 0.151 with depth covariates. Strong focal motivation
does not establish a general rule or a growth-independent causal effect.

| Read | Purpose |
|---|---|
| [Rationale](RATIONALE.md) | Biological context, evidence, rivals and relationship to existing questions |
| [Analysis pipeline](PIPELINE.md) | P0-P6 stages, estimands, source gates, output hierarchy and figure plan |
| [Intake results](reports/intake_v1/INTAKE.md) | 64 checks of inherited evidence; 18 extracted values and four source eligibility records; no new fit |
| [Source eligibility](SOURCES.md) | Same-screen reuse, conditional spatial work and unmet independent RNA/function requirements |
| [Plan](PLAN.md) | Functional outcomes, design requirements and decision boundaries |
| [Related branches after strict review](../../RESEARCH_QUESTIONS.md#a22-candidates-20261001) | E7 induction versus selection; E8 tissue specificity and immune/clinical links remain distinct unresolved hypotheses |
| [Nb3 follow-up](../../Research%20Article/gate2_N2_nabhan_2026/reports/FOLLOWUP_RESULTS.md) | Completed analysis, sensitivities and remaining source/design gaps |
| [Nb3 figures](../../Research%20Article/gate2_N2_nabhan_2026/FIGURES.md) | Figures 4, 7 and 8 plus source tables |

The paper package retains ownership of the motivating discovery fits; A22 owns
the new P2 diagnostic fits. Corrected human S5/code,
independent preparations, state/composition measurements and a secreted-protein/
recipient-function endpoint are still needed for the stronger answer.

## Execution status and next step

P0 ran as a provenance/evidence audit. P1 has a bounded source registry; no
independent RNA or functional source is admitted yet. P2 has completed the RNA–imaging join and frozen descriptive comparison of
amount-related proxies versus proxies plus epithelial identity. P3-P5 have separate source/design gates and need
not wait for a favorable P2 result. Details and the runnable intake commands are
in the [pipeline](PIPELINE.md#run-the-intake).

The pipeline draft remains historical. The executed extension uses a separate
exploratory contract and adds one current figure. No functional result or
claim-grade promotion is reported.
