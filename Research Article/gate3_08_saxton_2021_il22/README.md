# Saxton 2021 IL-22: source reproduction and recipient-context analysis

**Reviewed recovery closeout, 31 October 2026:** the bounded metadata/source/documentation
review passed [originating review](REVIEW_2026-10-31.md) and is integrated locally.
The original biological sequence is not completed. The
[recovery scope](RECOVERY_SCOPE_2026-10-31.md) governs current work; the original
plan below remains historical, including its broader authorization language.

[Results](RESULTS.md) | [Complete hold ledger](COMPLETION_LEDGER.md) |
[Independent R1 review](R1_REVIEW.md) | [Source correction](SOURCE_CORRECTION_2026-10-31.md) |
[E1/E2 source feasibility](SOURCE_FEASIBILITY.md) | [Evidence index](FIGURES.md) |
[Validation and handoff](VALIDATION.md).

| Step | Current source-review / execution disposition |
|---|---|
| R0 | Main source/endpoint audit reviewed; supplementary/raw-source access and assessment limits documented |
| R1 | Original v2 executed; independent hashes, formats, dimensions, joins and QC arithmetic pass; animal identities remain unverified |
| R2 | Unexecuted; platform-policy execution hold, despite recovered count files |
| R3 | Unexecuted; platform-policy execution hold; no response scoring/modeling |
| R4 | Source audit complete with Figure 5 correction; numerical reconstruction held by policy scope and raw-value/replicate/identity limits |
| R5 | Endpoint/source audit complete; Figure 7 G/H caption conflict retained; numerical reconstruction held by policy scope and unit/nesting limits |
| E1 | Bounded existing-source assessment complete; numerical extension unexecuted; pooled-unit and endpoint-linkage limits recorded |
| E2 | Bounded literature/source assessment complete; no linked persistence/recovery analysis; uninspected sources remain not assessed |
| D1 | Results, evidence index, exact ledger, local integration and originating technical/source review complete; human scientific acceptance remains unassessed |

## Historical plan (retained verbatim below)

31 October 2026. Stable reading ID **8**, Gate **3A**; execution namespace
**Sx22** (checked absent from the current registry). The owner explicitly requested
a stepwise plan and a separate technical session to launch the analysis. The
review base is main `4df267d3f5035b249df2e587c70a8b9e9253b049`, including DY1
PR #153 and Yadav PR #154. No Saxton numerical analysis has run at plan creation.

[Published paper](https://doi.org/10.1016/j.immuni.2021.03.008) ·
[Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8054646/) ·
[GSE160217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160217) ·
[Figure-focused evidence review](../../docs/research_reviews/2026-10-31-saxton-il22/README.md)

The current authorization covers source qualification, eligible reproduction,
bounded exploratory extensions and their review. It does not depend on completing
the older Niethamer/S1 pilot or obtaining a favorable result. Niethamer/S1 itself
remains unrun and gated; all unit, exposure, source and contract requirements still
apply. The earlier reading-only review remains a historical checkpoint. Owner
reading is partial (abstract/introduction/discussion), not certified complete.

## Biological purpose

Determine what the deposited evidence supports about separating selected
inflammatory and protective responses to WT IL-22 and the published 22-B3 variant,
then identify whether recipient state is a measurable extension relevant to
epithelial recovery. Structural design is background for the published comparison;
this plan does not develop new ligands or optimize molecular interventions.

The primary reproduction estimand is the **22-B3 versus WT difference in acute
bulk colon gene expression**, with each versus PBS providing response context.
Biological unit: the original animal/preparation, to be qualified before inference.
Endpoint: measured gene expression, not secretion, phosphorylation, chromatin
memory, mature lineage output or repair. The main validity threats are mistaken
sample identity/independence, small biological replication, technical processing
differences and whole-tissue cell composition.

The paper and its outcomes have already been read. All reanalyses are exposed
reproduction or exploration; freezing a later contract does not make them
unexposed confirmation. Published gene panels are reproduction targets, not an
independently chosen validation set. Source reanalysis is not new biological
replication. Unfavorable and imprecise findings are retained.

## Stepwise execution ledger

The technical session owns status updates, contracts and immutable results. A
stage is complete only with linked evidence, or a specific hold after proportionate
source recovery. Source qualification can finish while its numerical subtask is
held. Lack of an interesting effect is never a hold or a reason to expand scope.

| Step | Work and comparison | Endpoint and unit | Eligibility / decision | Initial status |
|---|---|---|---|---|
| **R0 — evidence and source inventory** | Reconcile main paper, supplements, available figure source values and GSE160217; audit Figs. 3–7 | Source/panel/sample identities; no biological effect estimate | Record authoritative URLs, versions, hashes, assay units, time points, contrasts, source reuse and actual biological versus technical replication | Ready for source qualification |
| **R1 — RNA input qualification and QC** | Inspect counts/processed matrices, sample map, gene identifiers, library summaries and outliers without outcome-driven exclusions | Sample/animal-level inputs and technical diagnostics | Confirm group mapping, independent units, valid count scale, annotation and identifiable design; unknowns restrict inference rather than invite guesses | Depends on R0 |
| **R2 — Fig. 6 reproduction and direct contrast** | WT–PBS, 22-B3–PBS and direct 22-B3–WT under one specified count model where eligible | Gene-level expression effects and uncertainty, animal/preparation unit | Freeze normalization, filtering, design, multiplicity family and exclusions; use estimates/intervals alongside adjusted significance. If only aggregates qualify, report source-level descriptions separately | Conditional on R1 |
| **R3 — response pattern and robustness** | Compare published barrier/inflammatory panels; add bounded independently sourced response sets only after defining their provenance | Expression patterns, gene membership and sensitivity of effect direction/ranking | Separate paper-selected panels from exploration; no universal protective score, noisy-denominator retention ratio, or equivalence from a nonsignificant test. Tiny-n influence checks are descriptive | Conditional on R2 |
| **R4 — signaling and recipient context** | Audit existing WT/22-B3 signaling and receptor data across Fig. 3–5 assay/tissue contexts | Phospho-STAT dose-response or receptor measurements in their native assay units; cell preparation/animal | Estimate curve parameters only if dose coverage, replicate mapping and measurement scale identify them. Do not divide unlike antibody readouts or fit missing plateaus. Receptor RNA is not surface abundance | Source audit ready; numerical work conditional |
| **R5 — functional outcome reconstruction** | Reconstruct eligible Fig. 7 contrasts separately for intestinal, pancreatic and systemic outputs | Original survival/viability, crypt, serum injury and inflammatory endpoints; correct animal/organoid hierarchy | Preserve assay units, timing, SD/SEM conventions and nesting. No pooled repair score, chronic-safety claim or mature-alveolar interpretation. Missing source units produce a panel-specific hold | Source audit ready; numerical work conditional |
| **E1 — epithelial recipient-state extension** | Qualify one closest existing epithelial injury/recovery cohort before considering a new source; compare prespecified states/time groups within its design | Il22ra1/Il10rb and qualified response-transcript context at animal/donor level | Verify cell state, sample identity, independence and comparators before an exploratory contract. Cell fractions and within-state expression are separate endpoints. Stop at expression context without ligand perturbation evidence | Source qualification authorized; numerical work conditional |
| **E2 — persistence and recovery discriminator** | Compare the paper's acute evidence with the 2025 OSMR/withdrawal result, older priming evidence and current A14/A19 limits | Source/design qualification for verified cessation, later response and functional recovery | A memory or recovery-effect analysis needs actual linked longitudinal/withdrawal and functional measurements. Literature comparison can complete without that dataset; do not substitute an acute gene score | Bounded literature/source assessment ready; empirical analysis held pending qualifying data |
| **D1 — synthesis, figures and review handoff** | Reconcile every step with original claims and existing RQ evidence | Evidence/status ledger, results, figure gallery and interpretation boundaries | Separate executed, reviewed and accepted statuses; source-data and rendering checks plus independent review. Record exact reopening evidence for every hold | Follows available stage returns |

R0/R1 establish the RNA analysis before R2. R4/R5 source audits can continue if
RNA access is delayed. E1 must not turn into an unrestricted atlas search. Start
with the current registry and existing qualified cohorts; if none answers its
bounded comparison, record why and qualify at most the closest alternative before
changing scope. Never rerun older frozen analyses just to create a new figure.

## Meaning of possible results

- Retained barrier-associated RNA together with reduced inflammatory RNA would
  reproduce a transcriptional distinction in this source. It would not prove
  functional protection or general tissue selectivity.
- Broadly reduced responses would weaken a simple transcriptional-selectivity
  account at that exposure/time. It is informative even if the paper's functional
  endpoints remain favorable in other experiments.
- Imprecise direct contrasts remain imprecise. Different significance calls
  against PBS are not a treatment difference, and no equivalence margin is invented.
- Different receptor/response RNA across recipient states would motivate a
  context hypothesis. Composition, ongoing exposure and receptor protein remain
  alternatives; it would not predict 22-B3 efficacy or establish memory.
- Evidence that a receptor response falls after withdrawal argues against its
  autonomous persistence in that setting. Persisting RNA without a linked recovery
  endpoint does not establish altered regenerative competence.

## Literature premises and extension limits

Reuse the [31 October reading review](../../docs/research_reviews/2026-10-31-saxton-il22/README.md)
for the unchanged main-paper premises and completed search record. The full IL-22
paper and relevant methods were inspected; Figs. 5–7 were visually checked.
Supplementary sources still need R0 qualification. GSE access previously returned
a browser challenge; the indexed deposit identifies the intended groups and a
count supplement, but files and sample-to-animal identities remain unverified.
Use ordinary public GEO/NCBI/publisher download interfaces; an unavailable view
does not itself prove that the deposit cannot be recovered.

[Cineus, Luo et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12133592/),
Fig. 4 and the withdrawal passage, constrain a universal STAT3/protection label.
[Bachmann et al. 2013](https://pubmed.ncbi.nlm.nih.gov/23153456/) is an abstract-read
priming precedent, not a fully audited dataset. Before E1/E2 numerical work or
material RQ development, complete a targeted current/older/contrary primary-source
pass for that exact comparison under the [literature workflow](../../docs/LITERATURE_WORKFLOW.md).
Record actual dates, queries, versions, correction checks and read versus
uninspected leads. Do not claim novelty or completed searches in advance.

## Repository placement and existing questions

This folder owns reproduction, basic article-local questions, source reports and
the gallery. Use `config/`, `scripts/` and `tests/` as needed; actual immutable run
outputs belong under `analysis/research/runs/`, with registry-bound contracts and
receipts. Keep raw downloads in ignored caches with provenance and hashes.
Register the necessary article-local candidate(s), using the verified Sx22
namespace, before freezing numerical work. Do not create a new canonical A ID.

Direct work on an established RQ belongs under its existing folder, linked back
here. A conceptual resemblance alone justifies a context note, not a duplicate
analysis. Inspect current results/amendments and dossier before extending:

- [A19](../../RQ_Specified/A19_fzd_response_reversibility/RESULTS.md): receptor context
  and reversibility; Saxton does not supply receptor-specific Fzd withdrawal or
  mature AT1 recovery.
- [A14](../../RQ_Specified/A14_withdrawal_recovery_and_reception/README.md): ongoing
  input versus inflammatory history; no post-cessation memory claim from acute RNA.
- [A22](../../RQ_Specified/A22_epithelial_identity_niche_response/README.md) and
  [A2](../../RQ_Specified/A2_areg_source_delivery/README.md): recipient response,
  ligand delivery and extracellular output remain distinct measurements.
- A1/A8 supply regulatory-state and mature-output limits; DY1's discordance and
  STAT6/ARG1 questions remain separate from IL-22 signaling.
- The merged [Yadav final review](../../RQ_Specified/Yadav_followups_20261031/REVIEW_T1B_FINAL.md)
  already preserves source/flux/joint mature-repair holds. Its publications and
  source descriptions are context, not independent IL-22 validation or eligible
  substitute data. Do not reopen its closed work without new qualifying evidence.

## Execution and review contract

Follow AGENTS.md, current PROGRESS, research governance and the registry. Inspect
HEAD/main/dirty state and use a separate managed checkout before edits. Freeze and
commit hash-bound code/contracts before substantive numerical runs; use the
research runner and retain all failed/preflight outcomes. Synthetic tests should
target units, joins, contrasts and error handling. Scientific verification must
check source identities, arithmetic and endpoint meaning, beyond schema success.

For every hold record the missing field/file/design, attempted authoritative
recovery, affected inference, work that remains possible and exact reopening
evidence. Status cannot be merely “restricted” or “needs more data.” Amendments
must explain what changed and why before the next run; do not loosen governance
or preserve only favorable analyses.

For each eligible result, produce a readable source-linked figure and caption
stating contrast, units, biological n, uncertainty and limit. Reuse the neighboring
paper gallery style without modifying its frozen figures. End with `RESULTS.md`,
`FIGURES.md`, this updated ledger, source/literature context, targeted validation
and a concise review handoff listing commit, contracts, receipts and holds.
Independent review belongs to the originating review chat; technical completion
does not create human scientific acceptance. No external publication, author
contact or bench work is part of this launch.
