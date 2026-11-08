# Previous documentation index

> Archived on 8 November 2026. This is a historical navigation snapshot.
> Use the [current documentation index](../../README.md) and [source register](../../DATASETS.md).

# Documentation Index

**Current navigation — 7 November 2026:** [biological topic map](../../guides/RESEARCH_TOPICS.md)
connects all 33 RQs and 19 paper packages. [Current question arguments](../../../RQ_Specified/README.md),
[reviewed rationale](../../research_reviews/2026-11-04-portfolio-reasoning-restructure/RATIONALE_ASSESSMENT.md)
and [project state](../../../PROGRESS.md) own current findings and work status.
[Latest source/structure reconciliation](../../audits/2026-11-07-public-data-inventory/RECONCILIATION_V2.md).

## Current entry points

| Need | Current owner |
|---|---|
| Questions, evidence and next comparisons | [Question homes](../../../RQ_Specified/README.md), [dossiers](../../research_dossiers/README.md), [registry](../../../analysis/research/registry.json) |
| Papers, reading permissions and analyses | [Article index](../../../Research%20Article/README.md) and [roadmap data](../../../Research%20Article/ROADMAP.json) |
| Public sources and local cache inventory | [Dataset inventory](../../DATASETS.md), [source-use update](../source-inventories/DATASET_UPDATES_2026-11-07.md) |
| Directory ownership and evidence rules | [Structure](../../guides/REPOSITORY_STRUCTURE.md), [architecture](../../RESEARCH_ARCHITECTURE.md), [governance](../../RESEARCH_GOVERNANCE.md) |
| Verification and handoff | [Reproducibility](../../../REPRODUCIBILITY.md), [project state](../../../PROGRESS.md) |

## Dated reviews and planning history

The checkpoints below preserve their original scope. Their next steps and
completion statements do not override current owning reports. The
[4 November architecture audit](../../audits/2026-11-04-topic-navigation/README.md)
records the preceding navigation review.

**3 November primary-target literature review:** [recent sources and biological implications](../../research_reviews/2026-11-03-primary-candidate-literature/README.md)
and [literature-informed screening plan](../../research_reviews/2026-11-03-primary-candidate-literature/ANALYSIS_PLAN_V1.md).
New technical execution is tracked separately from the completed reading and
earlier cut-or-fill results; existing hypotheses and functional limits remain.

**3 November article/RQ screening and structure review:** [all 20 article directories, unfinished work and hygiene](../../audits/2026-11-03-article-rq-screening/README.md)
and [source/metadata starting-point assessment](../../audits/2026-11-03-article-rq-screening/STARTING_POINT_ASSESSMENT.md).

**3 November RQ trajectory review:** [all 33 starting questions, current evidence and framing drift](../../audits/2026-11-03-rq-evidence-trajectory/README.md).
Separates measured narrowing from negative diagnostics and unexecuted biological
comparisons; preserves all question identities and scientific acceptance states.
[Follow-through plan](../../audits/2026-11-03-rq-evidence-trajectory/CUT_OR_FILL_PLAN.md)
cuts unsupported interpretations and specifies bounded fills and reopening gates.

Current schematic review: [all 33 reviewed cellular figures and biological-detail audit](../../audits/2026-11-02-rq-schematic-review/README.md).

**2 November navigation hygiene and RQ registration:** [audit and checks](../../audits/2026-11-02-navigation-hygiene/REPORT.md) · [six-candidate scope assessment](../../audits/2026-11-02-navigation-hygiene/RQ_ASSESSMENT.md). Root navigation stays collection-level; paper galleries stay article-owned. The illustrated guide includes proposed A32 and a separate article-local crosswalk.

**Portfolio presentation and history:** [portfolio summary](../../portfolio/PORTFOLIO_SUMMARY.md)
and [25 October summary synchronization](../../audits/2026-10-25-summary-synchronization/REPORT.md).
The [12 October Weft intake](../../../weft_intake/README.md) is a reviewed trial handoff;
it does not supersede the existing question portfolio.

**Historical integrated checkpoint — 7 October 2026:** [integrated results](../../portfolio_extensions/2026-10-07/SYNTHESIS.md), [selected evidence statuses](../../portfolio_extensions/2026-10-07/EVIDENCE_CHECKPOINT.md), and [return checklist](../../portfolio_extensions/2026-10-07/RETURN_CHECKLIST.md).

**Preceding repository audit:** [findings and corrections](../../audits/2026-10-07-repository-readiness/REPORT.md) and [all-question review](../../audits/2026-10-07-repository-readiness/QUESTION_REVIEW.md).

Start current research development with the [dossier index](../../research_dossiers/README.md)
and [governance](../../RESEARCH_GOVERNANCE.md). The [3 October reconciliation](../../audits/2026-10-03-repository-repair/REPORT.md)
is a historical preservation record, not the latest checkout state.

Start with the [research questions](../../../RESEARCH_QUESTIONS.md),
[paper roadmap](../../../Research%20Article/README.md) and [dataset inventory](../../DATASETS.md).
The [current project state](../../../PROGRESS.md) and [conditional packages](../../research_dossiers/packages_2026-10-03/README.md)
describe current handoff and historical package conditions, respectively. The
[historical remaining-work ledger](../planning/REMAINING_WORK.md) retains
its dated scope; current owner reports supply later results and unresolved inputs.
The [September roadmap](../planning/RESEARCH_ROADMAP.md) and
[28 September gap-fill ledger](../../roadmap_runs/2026-09-28-gap-fill/RESULTS.md) retain
historical planning and execution context.

The [combined RQ development proposal](../../audits/2026-09-28-rq-development-proposal/PROPOSAL.md)
sets out proposed rationale, scope and next-evidence work for each question;
it does not replace the current register or executed-result ledger.

Evidence summaries: [claim register](../../../CLAIMS.md), [claim summary](../../CLAIM_SUMMARY.md)
and [negative-results index](../../NEGATIVE_RESULTS.md). The summaries are generated
from the register; corrections belong in their source records.

Repository guides: [structure and label scope](../../guides/REPOSITORY_STRUCTURE.md),
[research architecture](../../RESEARCH_ARCHITECTURE.md),
[reproducibility](../../../REPRODUCIBILITY.md) and [portfolio summary](../../portfolio/PORTFOLIO_SUMMARY.md).
The [next-dataset gate](../planning/NEXT_DATASET_GATE.md) is a historical design with links
to the resulting analyses. Dated reviews, including the
[England source review](../../audits/2026-09-28-england-paper-rqs/REPORT.md), retain their
original scope; they are not the repository-wide navigation hierarchy.

## Methods and original pipeline references

> **Tool reference pages are not execution records.** The five tool pages below
> describe tools and the reference study's design. They do **not** imply that
> every tool described here was used in the original atlas analysis, most were
> not. For what was actually executed, with real parameters and cell counts,
> see **[`PIPELINE_AS_RUN.md`](../../PIPELINE_AS_RUN.md)**, which is generated from
> the pipeline's own outputs and states tool-by-tool which were used.
>
> In that original pipeline, of the five tools documented here, only **Scrublet** was used.
> SoupX, scds, Slingshot and tradeSeq were **not**. `PIPELINE_AS_RUN.md` also
> records where the executed analysis departs from the two source publications.

One schematic per tool. Each file states what the tool consumes and returns,
gives a `flowchart` of its internal decisions, lists its parameters and their
sources, and records the failure modes that are silent rather than loud.

- [`SOUPX.md`](../../methods/tools/SOUPX.md): ambient RNA estimation from empty droplets, automated
  and marker-based contamination fractions, and why correction must precede
  doublet calling in lung tissue.
- [`SCRUBLET.md`](../../methods/tools/SCRUBLET.md): simulated-doublet neighbourhood scoring,
  threshold selection on the simulated-score histogram, the two free
  consistency checks, and the limits of neotypic detection.
- [`SCDS.md`](../../methods/tools/SCDS.md): co-expression (`cxds`) and classifier (`bcds`) scoring,
  their `hybrid` combination, benchmark position against other callers, and the
  fact that scds deliberately returns no threshold.
- [`SLINGSHOT.md`](../../methods/tools/SLINGSHOT.md): minimum spanning tree topology, simultaneous
  principal curves, the two unreported knobs that decide the answer, and what
  supervision does to the interpretation of a trajectory.
- [`TRADESEQ.md`](../../methods/tools/TRADESEQ.md): the negative binomial GAM, knot selection by
  AIC, the mapping from biological question to statistical test, and the
  pseudotime-comparability caveat that applies directly to the reference study.

Rationale and background (written after the analysis ran):

- [`ANALYSIS_RATIONALE.md`](../../ANALYSIS_RATIONALE.md): every major decision in two
  passes, what was decided from the data alone, and what changed after reading
  the two source papers, including where the first pass was wrong.
- [`BACKGROUND_FOR_BIOLOGISTS.md`](../../methods/background/BACKGROUND_FOR_BIOLOGISTS.md): batch effects
  and Harmony from first principles, for a reader without a computational
  background, including when correction destroys the experiment.
- [`DOUBLETS_AND_SCRUBLET.md`](../../methods/background/DOUBLETS_AND_SCRUBLET.md): what a doublet is, how
  Scrublet works, and the two-round audit of whether it removed this project's
  populations of interest, a crude gate said yes, a stricter gate overturned
  it (AT0 flagged at 3.9% vs a 6.3% baseline).
- [`UMAP_AND_FIGURES.md`](../../methods/background/UMAP_AND_FIGURES.md): how the UMAP is built from
  counts, what it does and does not mean, how to read dot plots and feature
  plots, and why cluster-marker p-values are a ranking device, not a test.

Supporting documents:

- [`PIPELINE_AS_RUN.md`](../../PIPELINE_AS_RUN.md): **what was actually executed**,
  per-dataset parameters, cell counts, batch decisions, which of the tools
  above were used, and how the analysis diverges from the source papers.
  Generated from the pipeline's artefacts; regenerate with
  `analysis/scripts/05_write_pipeline_as_run.py`.
- [`Research Article/gate1_01_niethamer_2025/GSE262927/README.md`](../../../Research%20Article/gate1_01_niethamer_2025/GSE262927/README.md): the full analysis report
  for the primary (mouse) dataset, including QC tables and output locations.
- [`WORKFLOW_Niethamer2025.md`](../../methods/workflows/WORKFLOW_Niethamer2025.md): the end-to-end sequence, ordering
  constraints, subset-and-recluster loop, lineage-trace calling, and quality
  control acceptance order.
- [`scRNAseq_workflow_Niethamer2025.md`](../../methods/workflows/scRNAseq_workflow_Niethamer2025.md):
  the annotated pipeline reference, study design, stage-by-stage parameters,
  marker-gene annotation tables, and the twelve parameters the reference study
  leaves unspecified.
- [`../Research Article/README.md`](../../../Research%20Article/README.md): the paper-by-paper roadmap
  (the owner's reading order), with per-paper study notes, extracted decision criteria and
  analysis trials; the HLCA note is at
  [`../Research Article/gate1_04_sikkema_2023_hlca/README.md`](../../../Research%20Article/gate1_04_sikkema_2023_hlca/README.md).
- [`../REFERENCES.md`](../../../REFERENCES.md): bibliographic index of source studies, roadmap papers and
  methods, with DOIs, PMC links and data accessions; current article reports
  retain later source-specific citations.

Alignment (STARsolo) and the Seurat stages have no separate schematic. Their
steps are linear and fully covered in [`WORKFLOW_Niethamer2025.md`](../../methods/workflows/WORKFLOW_Niethamer2025.md); a
per-tool diagram would only restate it.

Downloaded full-text papers and publisher supplements remain outside Git.
Generated research-figure PDFs may be tracked with their provenance.
[`../REFERENCES.md`](../../../REFERENCES.md) links the source publications; source
access and reuse terms remain publication-specific.
