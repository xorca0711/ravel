# A23: does phosphate homeostasis constrain entry into an alveolar transition state?

<!-- current-rq-framing:start -->
## Current biological hypothesis and novelty boundary — 3 October 2026

SLC34A2 transport impairment may increase acquisition of a transition-associated epithelial stress state before broad AT2 identity loss, rather than merely prolong an existing intermediate state by impairing exit to AT1 maturation. This entry-versus-residence distinction narrows the original proposal. Phosphate-dependent repair failure and the Slc34a2-loss transitional RNA module already have published precedents; the mechanism cannot be claimed new from their combination.

**What is already known, and what remains:** Lv already links SLC34A2/intracellular phosphate to AT2 self-renewal and AT1 differentiation; Nabhan reports the transitional module, and Uehara establishes mineral-context biology. The inspected Lv endpoints do not resolve the proposed entry-versus-exit comparison; its novelty and biological value remain provisional. [Primary-source comparison](../../docs/research_dossiers/NOVELTY_SPECIFICITY_APPLICATION_2026-10-03.md#a23).

**What the measurements would decide:** Lineage-linked acquisition and subsequent exit measured separately can distinguish increased entry from prolonged residence; endpoint state abundance cannot. Measure transport function, compartment-specific phosphate, injury and viability independently. A qualified restoration contrast can test transport dependence, but rescue of counts alone cannot identify the affected transition step. Preserve the external negative marker result.

**Current disposition:** Narrowed entry-versus-exit question; novelty unresolved. This revision specifies proposed work; scientific acceptance, model access and assay qualification remain pending.

| Evidence and implementation | Current boundary |
|---|---|
| Biological unit and endpoint | Independent primary AT2 donor/animal preparations with documented mineral context. Link measured phosphate handling to absolute viable transition-defined cells per starting AT2 input; abundance and transport flux are distinct. |
| Current evidence and limit | The screen marker pattern did not reproduce coordinately in the external PAM case. Lower SLC20A1/2 RNA supplies no transcriptional compensation evidence but does not exclude functional compensation. |
| Next decision / hold | Scientific review and measurement qualification are deferred. Keep handling, timing and recovery unresolved; three markers are not fate, and a single human case is not replicated perturbation. |

**Read in this order:** [current evidence](reports/external_pilot_v2/RESULTS.md),
[development dossier](../../docs/research_dossiers/A23.md),
[conditional hypothesis package](../../docs/research_dossiers/packages_2026-10-03/A23.md).
[Deferred work](../../docs/research_dossiers/REMAINING_WORK.md) and
[execution requirements](../../docs/RESEARCH_GOVERNANCE.md) govern any later
analysis. Draft completion does not establish assay validity, resource access,
meaningful effects, precision or scientific acceptance. Existing numerical
results and original plans below retain their recorded scope.
<!-- current-rq-framing:end -->

## Transporter extension executed, 1 October 2026

[New results](reports/transporter_context_v1/RESULTS.md) |
[Contract](config/transporter_context_v1.json) | [Figure 5](FIGURES.md#figure-5-alternative-transporter-context).
SLC20A1 and SLC20A2 RNA are lower in the PAM case across five fixed AT2
selections. Within-case depth-conditional associations with KRT8/CLU are small
and mixed. Increased alternative-transporter RNA is unsupported as an
explanation for the absent coordinated transition pattern. Compensatory flux,
time and recovery remain unmeasured; the functional candidate remains conditional.


**Proposed 1 October 2026; P2 descriptive analysis and P3 source audit executed; causal
sequence open.** The [shared question card](../../RESEARCH_QUESTIONS.md#a23) owns the
hypothesis. The owner requested derivation after the Nb3 follow-up; retain/reject
and scientific acceptance remain open. No claim grade is added.

**Hypothesis.** Impaired SLC34A2-dependent phosphate homeostasis promotes an
alveolar transition-associated stress response before broad lineage collapse.
Restoring the relevant homeostatic defect should attenuate this response if the
link is causal. Transport, phosphate, temporal order and recovery were not
measured in Nb3.

The Slc34a2-targeted perturbation in Nb3 increases Krt8, Sprr1a and Clu; their mean contrast is
+0.524 and stays positive under all tested control/gene/well omissions.
AT2-marker attenuation is smaller than under NKX21, but is not absent:
the paired-depth estimate is −0.219 from seven paired-QC wells, versus eight
in the original mouse-QC contrast. Bulk averages cannot identify a within-cell
trajectory or establish a normal versus pathological fate.

| Read | Purpose |
|---|---|
| [External results](reports/external_pilot_v2/RESULTS.md) | Human case comparison, biochemical reproduction and strict hypothesis review |
| [Figure gallery](FIGURES.md) | Five current figures as PNG/PDF/SVG, with source units and limitations |
| [Reproduce](reports/external_pilot_v2/REPRODUCE.md) | Acquisition, environment, checks and immutable output records |
| [Rationale](RATIONALE.md) | Homeostasis/transition biology, evidence and competing explanations |
| [Analysis pipeline](PIPELINE.md) | P0-P6 stages, distinct predictions, source gates, outputs and figure plan |
| [Intake results](reports/intake_v1/INTAKE.md) | 51 checks; 19 inherited values/range endpoints and five source-role decisions; no new biological fit |
| [Source eligibility](SOURCES.md) | New PAM case-context lead, source reuse and remaining transport/time/recovery gates |
| [Plan](PLAN.md) | Time, state, transport and outcome requirements |
| [Strict candidate review](../../Research%20Article/gate2_N2_nabhan_2026/reports/RQ_INTEGRATION_REVIEW.md) | E4 remains A23; no separate duplicate state RQ or claim of absent identity loss |
| [Nb3 follow-up](../../Research%20Article/gate2_N2_nabhan_2026/reports/FOLLOWUP_RESULTS.md) | Executed sensitivities and limits |
| [Nb3 figures](../../Research%20Article/gate2_N2_nabhan_2026/FIGURES.md) | Figures 5 and 7, with full numerical provenance |

The article package owns the discovery fits. A23 now owns the external
case summaries and source-biochemistry reproduction. Neither is a replicated
phosphate-mediated epithelial-state test.

## Execution status and next step

P0/P1 intake, P2 coverage/marker analysis and P3 selected endpoint audit are
complete within their recorded scope. The PAM case does not reproduce a
coordinated KRT8/SPRR1A/CLU increase. Identity-marker differences depend on cell
selection, and lower target RNA is not a transport measurement.

The source biochemical data motivate a **conditional compensation branch** of
A23: compensatory phosphate handling may buffer epithelial-state response.
This is a testable explanation, not a demonstrated cause of the human pattern.
See the [strict review](reports/external_pilot_v2/RESULTS.md#strict-review-of-the-a23-hypothesis).

All 14,210 published cells were recovered in a post-pilot raw-matrix sensitivity;
the marker pattern persists. Independent annotation/ambient-RNA assessment remains
a limit on finer state interpretation. P4 and P5 need
linked replicated transport/state/time and restoration/function data. The source
workbook cannot connect those endpoints across its unlabelled animal rows.

The current archived-pilot verification command is
`python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/08_verify_external_current.py`.
It checks the unchanged numerical records and the
[original gallery snapshot](metadata/history/pre_transporter_extension/snapshot.json).
The original verifier remains preserved for its historical checkout.
