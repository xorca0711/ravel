# A12: recipient context beyond ligand RNA

<!-- current-rq-framing:start -->
## Current biological hypothesis and novelty boundary — 3 October 2026

IL-1 receptor and inhibitory context in recipient epithelial cells or fibroblasts may explain an IL-1-dependent response beyond ligand RNA abundance. Those are separate recipient questions; the current portfolio has not fixed one compartment, receptor/inhibitory contrast and biological consequence for a mechanistic experiment. General NF-kB or inflammation scores cannot establish IL-1 specificity.

**What is already known, and what remains:** IL-1-dependent epithelial and stromal effects are published, including recipient-history effects. Exact-compartment novelty is unresolved until the contrast and consequence are specified. [Primary-source comparison](../../docs/research_dossiers/NOVELTY_SPECIFICITY_APPLICATION_2026-10-03.md#a12).

**What the measurements would decide:** A recipient-context effect under a qualified IL-1-dependent contrast supports specific reception. The same response without IL-1 dependence favors a general inflammatory marker. Source-attribution uncertainty and a generic pathway score cannot identify which cells delivered the active input.

**Current disposition:** Recipient compartment/axis/endpoint required. This revision specifies proposed work; scientific acceptance, model access and assay qualification remain pending.

| Evidence and implementation | Current boundary |
|---|---|
| Biological unit and endpoint | Identified donor/preparation units, with epithelial and fibroblast recipients analyzed separately. A future contrast needs a validated IL-1-dependent consequence per starting viable recipient input; the current measured endpoint is inflammatory RNA. |
| Current evidence and limit | The recipient index improves epithelial prediction in twelve patients while fibroblast results are unstable. Unassigned sources account for roughly 52–72% of IL1B, limiting macrophage-specific attribution. |
| Next decision / hold | Scientific review and assay qualification are deferred. Retain A12-S1 source uncertainty; protein/input and receptor evidence are required before IL-1/source-specific causal interpretation. |

**Read in this order:** [current evidence](../../docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md),
[development dossier](../../docs/research_dossiers/A12.md),
[conditional hypothesis package](../../docs/research_dossiers/packages_2026-10-03/A12.md).
[Deferred work](../../docs/research_dossiers/REMAINING_WORK.md) and
[execution requirements](../../docs/RESEARCH_GOVERNANCE.md) govern any later
analysis. Draft completion does not establish assay validity, resource access,
meaningful effects, precision or scientific acceptance. Existing numerical
results and original plans below retain their recorded scope.
<!-- current-rq-framing:end -->

<!-- literature-visual-context:start -->
## Literature context and visual hypothesis

[What previous findings contribute, what remains, and what the readouts would decide](LITERATURE_CONTEXT.md).

![A12: proposed hypothesis and rival explanation](schematics/hypothesis_v2.svg)

*Explanatory proposal, not measured results. Read the linked context and caption; arrows do not certify a mechanism or novelty.*
<!-- literature-visual-context:end -->


## Organizing biological question

> Does recipient receptor and inhibitor context explain responses beyond IL-1 ligand RNA?

The working hypothesis is that epithelial and fibroblast responses depend partly
on the recipient's capacity to receive or restrain a signal. Source IL1A/IL1B RNA
and cell mixture may therefore leave relevant variation unexplained.

This folder compares source-based models with recipient-context extensions in
fixed epithelial and fibroblast states, using patients held out from fitting.
It also audits independent-cohort eligibility. The measured endpoint is an
inflammatory RNA response; pathway activation and IL-1 selectivity remain
separate questions. A12-S1 concerns unresolved cell identities contributing to
the source RNA.

**Read first:** [question card](../../RESEARCH_QUESTIONS.md#a12),
[rationale](RATIONALE.md), [plan](PLAN.md),
[A12-S1 source-identity map](reports/A12_S1_SOURCE_IDENTITY_MAP.md),
[source-identity question](../../RESEARCH_QUESTIONS.md#a12-s1),
[pilot specification](../../docs/roadmap_runs/2026-09-27-followthrough/A12_pilot_specification.json),
[pilot report](../../docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md).

## Evidence and analysis history

**Rationale and plan written, 28 September 2026.** The [rationale](RATIONALE.md)
states what the recipient index and endpoint are, why the parent IL-1 question
connects to a general inflammatory readout, and what the three failed cohort
gates do not establish; the [plan](PLAN.md) records the pilot as closed and fixes
the choice a validation must make between fixed-procedure replication and
transport of a serialized fit. A [figure](figures/A12_F01_heldout_model_ladder.png)
plots both pilots' held-out ladders against their training-mean baselines. The
[A12-S1 map](reports/A12_S1_SOURCE_IDENTITY_MAP.md) quantifies how conditional the
macrophage source term is. Documentation only; nothing was rescored.

**Latest recovery, 28 September 2026:** the [external-cohort audit](external_validation_20260928/reports/RECOVERY_REPORT.md)
finds that none of its three candidates passes the unchanged comparison.
No external score or fit was produced; the exploratory pilot below is preserved.

**Exploratory pilot executed, 27 September 2026.** The [question](../../RESEARCH_QUESTIONS.md#a12) asks whether receptor/inhibitor context adds information beyond source RNA and mixture. RNA context is not pathway activation.

The [pre-fit specification](../../docs/roadmap_runs/2026-09-27-followthrough/A12_pilot_specification.json) and [complete report](../../docs/roadmap_runs/2026-09-27-followthrough/A12_PILOT.md) define a patient-held-out, gene-disjoint inflammatory RNA response in fixed AT2 and alveolar-fibroblast candidate states. Twelve matched patients pass primary coverage. The epithelial model improves relative to a source/TNF comparator; the fibroblast increment is unstable. Prior data exposure is recorded and no confirmation or IL-1-specific causal claim is made.

The [follow-through scripts and outputs](../../docs/roadmap_runs/2026-09-27-followthrough/README.md) share cohort provenance with the A13 extension. No module, label or normalization was tuned after inspecting the new predictions. Source identity remains conditional on assigned macrophages; A12-S1 is open. Independent epithelial validation is the next biological decision, while activation and selectivity require separate measurements.
