# Existing RQs, unfinished article work and metadata screening

3 November 2026. Requested after review of the five cut-or-fill packages.
Reviewed results were committed as `fe0316c`, following the three prospective
freeze commits. Integration base was refreshed to unchanged `115f3c5`.
This follow-up is a source/status and architecture assessment, not another
biological analysis, portfolio ranking or scientific acceptance decision.

## What can usefully proceed

The strongest immediate opportunities concern **recovering identities and
qualifying observations**, rather than adding signatures or fitting more models.
The [starting-point assessment](STARTING_POINT_ASSESSMENT.md) states each
question, actual material, missing fields, useful outcome and stop condition.

1. **A30 provenance reconstruction qualification.** The original state export
   does not retain barcode/library identifiers. All six raw inputs named in its
   receipt exist in the main checkout's ignored cache, although absent from this
   worktree. Qualify their hashes and the original runtime, then determine
   whether an isolated replay can reproduce the saved memberships while carrying
   identifiers through the original processing. This is a concrete recovery
   route to investigate, not permission to join rows by position. No replay ran.
2. **A26/A27 receptor-recovery audit.** Existing all-cell metadata and the pinned
   author clone notebook offer a route to distinguish all captured T cells from
   receptor-reconstructed cells. The metadata headers do not themselves contain
   productive-chain/recovery fields. Recover those records before interpreting
   state-specific or cross-organ repertoire differences. This is shared-source
   measurement qualification, not independent age replication.
3. **A6 / Nb4-P03/P05 donor-state eligibility.** Consolidate existing source
   identities, disease labels and author macrophage states across the already
   used IPF sources; identify a fixed shared state with actual control support.
   Do not repeat a sparse proliferating-state comparison or select a new state
   because its expression effect looks favorable.
4. **Nb1 / A4/A19 external source qualification.** GSE129605 remains an acquired,
   unfinished eligibility candidate. Its primary series record was refreshed;
   it still does not provide the required sample-to-animal and state joins.
   Its day-11 design could support a bounded expression comparison if qualified,
   not the acute lineage-history or receptor-specific functional questions.
5. **Wagner R4 and Niethamer D1 access/design checks.** The former needs its
   actual peak/count/annotation source, the latter Treg and independent-unit
   metadata. A bounded public-record refresh encountered access failures for
   GSE165088, GSE292440 and GSE300399. These are access limits, not proof that
   the datasets or required populations are absent.

These are execution-order suggestions based on recoverability and existing
inputs. They do not rank or retire the biological questions. A new numerical
screen still needs its own scoped contract, exposure record, freeze and runner.
The older cut-or-fill stop rules remain in force.

## What the article scan found

The [article inventory](ARTICLE_INVENTORY.md) covers **all 20 immediate
directories: 18 study packages, one cross-study module and one source archive**.
It uses current reports and later corrections ahead of old plans. The registry
retains 37 article-local candidates; they are not 37 additional canonical RQs.

- Genuine open work includes Niethamer S1/D1/V1, Nb1 external qualification,
  exact/functional Nb2 reproduction, parts of the broader Nb4 proposals, Nb5
  receptor/state qualifications, Wagner R2/R4/R5, and the original DY1,
  Saxton and Arozamena source/design-dependent analyses.
- Yadav's original feasible reconstruction, X0-X2/X6 and subsequent bounded
  follow-ups are already complete. X3-X5 have specific empirical holds.
  The old article-index assertion that numerical analysis had not run was wrong.
- Nb5's previously unrun P02 model-comparison task has now been addressed by
  the bounded A25 male-cortex comparison. Its mixed result does not complete
  every possible region/sex/generalization question, but it is no longer an
  omitted computation waiting to start.
- Wang/Wp R5 is deliberately closed without execution under the owner's
  previous decision. Old Choi proposals and completed sensitivity branches are
  not automatically reopened because a checklist still contains them.

No new cohort passed a full RQ eligibility gate in this scan. The two newly
read age/TCR candidates illustrate why assay availability is insufficient:
[GSE275967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE275967)
is aged-only WT versus mutant spleen, while
[GSE155005](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155005)
is a pooled-donor transfer into an aged recipient. Neither directly supplies
the existing independent age or paired spleen/marrow comparison.
Exact metadata coverage and access records are in the assessment.

## Current folder structure

```text
RQ_Specified/
  README.md                         all 33 question homes
  SCHEMATIC_GALLERY.md / .html       qualitative hypotheses
  FIGURES.md                        measured-result navigation
  A<id>_<topic>/                     exactly one home per A0-A32
    README.md                       Biological Q, then literature/visual context
    LITERATURE_CONTEXT.md
    PLAN.md                         development plan; not automatically frozen
    schematics/                     current illustration plus preserved history
    reports/, figures/, ...         only where local work exists
  A5_A11_shared_component_contract/  shared definitions, not an extra RQ
  Yadav_followups_20261031/          retained source/follow-up workspace

docs/research_dossiers/A<id>.md      full scientific argument
analysis/research/registry.json     identities and evidence/provenance navigation
analysis/research/runs/<run-id>/    immutable governed outputs and receipts
Research Article/<paper>/          paper-owned reproduction/branch evidence
```

All 33 registered homes exist, have a local context and registered schematic,
and retain the requested first two README sections. The two shared directories
are intentional. A figure outside its RQ folder is acceptable when the owning
README links the immutable run; copying it into a second folder would create
competing versions.

The article side has historical `trials/`, newer `runs/` and shared governed
run deposits. That heterogeneity reflects retained provenance, not automatically
misplaced work. The useful common interface is **paper purpose → current
result/hold ledger → source/units → gallery → RQ connections**. Paper READMEs do
not need the RQ-specific heading template, and old raw/frozen paths should not
be renamed simply to make their trees look alike. DY1 remains **ungated**;
its historical directory name is a documented exception.

## Hygiene changes made

- Corrected Yadav's stale status in both article-index views, and added missing
  Yadav, Nb4 and Nb5 gallery navigation to the executed-study table.
- Added current A25 result links ahead of Nb5's historical unrun statements;
  retained the original completion report and older G3 ledger as dated records.
- Added current P09/A31 and Wg-P06/Yadav cross-links so older proposal pages do
  not masquerade as the latest execution state.
- Updated the RQ index after the five-package execution and added A17/A25
  measured-run navigation to the RQ figure index. These are separate from the
  33 qualitative schematics; no duplicate image copies were made.
- Linked this audit from the article, RQ and documentation indexes. Question
  identities, hypotheses, images, claims and frozen outputs are unchanged.
- On the owner's subsequent explicit request, removed the Weft pilot row,
  description and diagram from the root README, preserving the intake itself.
  Added a six-view portfolio panel: Nb4 UMAP, A11 patient-paired expression,
  A1 CUT&Tag, Nb3 Hallmark enrichment, Yu spatial RNA and Arozamena paired
  RNA/accessibility. The owner's LinkedIn media served as a style reference,
  not a fixed list; current captions and corrections determined eligibility.
  All six selected images were visually inspected; no image was edited or
  copied. [Selection and provenance](PORTFOLIO_FIGURE_SELECTION.md) explain
  the choices. The structure document records this bounded root showcase
  separately from the owning article/question galleries.

Remaining useful maintenance is event-driven: update an owning index when its
current result changes, and retain supersession links on old plans. No broad
folder migration, data deletion, new placeholder directory or governance change is
justified by this inspection.

## Coverage and validation

The deterministic inventory used tracked paths plus the registry; all 20 article
entrypoints and their linked current result/hold records were assessed. The
recent all-33 trajectory audit was reused, with targeted current plan/result
reads rather than a second full biological audit. This was not a fresh read of
every paper, an exhaustive literature search, or a rerun of every table.
Direct primary metadata was read for the three successful accessions; other
accessions retain the precise failures described in the assessment.

Pre-commit repository validation and research-gate checks passed for the
reviewed result commit. The two immutable Matplotlib SVG whitespace exceptions
are recorded in its technical ledger. Before the final portfolio curation,
this audit passed **15,077 repository checks** and the research gate against
`origin/main`; final documentation checks are recorded in the project state.
Existing numerical validation is reused. No external
account writes, messages, push, PR or merge were performed.
