# Documentation Index

**Latest portfolio checkpoint:** [integrated results](portfolio_extensions/2026-10-07/SYNTHESIS.md), [selected evidence statuses](portfolio_extensions/2026-10-07/EVIDENCE_CHECKPOINT.md), and [return checklist](portfolio_extensions/2026-10-07/RETURN_CHECKLIST.md).

**Preceding repository audit:** [findings and corrections](audits/2026-10-07-repository-readiness/REPORT.md) and [all-question review](audits/2026-10-07-repository-readiness/QUESTION_REVIEW.md).

Start current research development with the [dossier index](research_dossiers/README.md), [governance](RESEARCH_GOVERNANCE.md) and [reconciliation report](audits/2026-10-03-repository-repair/REPORT.md).

Start with the [research questions](../RESEARCH_QUESTIONS.md),
[paper roadmap](../Research%20Article/README.md) and [dataset inventory](DATASETS.md).
The [current project state](../PROGRESS.md), [conditional packages](research_dossiers/packages_2026-10-03/README.md)
and [remaining-work ledger](research_dossiers/REMAINING_WORK.md) distinguish
completed drafting from remaining inputs, scientific review and eligibility.
The [September roadmap](RESEARCH_ROADMAP.md) and
[28 September gap-fill ledger](roadmap_runs/2026-09-28-gap-fill/RESULTS.md) retain
historical planning and execution context.

The [combined RQ development proposal](audits/2026-09-28-rq-development-proposal/PROPOSAL.md)
sets out proposed rationale, scope and next-evidence work for each question;
it does not replace the current register or executed-result ledger.

Evidence summaries: [claim register](../CLAIMS.md), [claim summary](CLAIM_SUMMARY.md)
and [negative-results index](NEGATIVE_RESULTS.md). The summaries are generated
from the register; corrections belong in their source records.

Repository guides: [structure and label scope](REPOSITORY_STRUCTURE.md),
[research architecture](RESEARCH_ARCHITECTURE.md),
[reproducibility](../REPRODUCIBILITY.md) and [portfolio summary](PORTFOLIO_SUMMARY.md).
The [next-dataset gate](NEXT_DATASET_GATE.md) is a historical design with links
to the resulting analyses. Dated reviews, including the
[England source review](audits/2026-09-28-england-paper-rqs/REPORT.md), retain their
original scope; they are not the repository-wide navigation hierarchy.

> **Tool reference pages are not execution records.** The five tool pages below
> describe tools and the reference study's design. They do **not** imply that
> every tool described here was used in the original atlas analysis, most were
> not. For what was actually executed, with real parameters and cell counts,
> see **[`PIPELINE_AS_RUN.md`](PIPELINE_AS_RUN.md)**, which is generated from
> the pipeline's own outputs and states tool-by-tool which were used.
>
> In that original pipeline, of the five tools documented here, only **Scrublet** was used.
> SoupX, scds, Slingshot and tradeSeq were **not**. `PIPELINE_AS_RUN.md` also
> records where the executed analysis departs from the two source publications.

One schematic per tool. Each file states what the tool consumes and returns,
gives a `flowchart` of its internal decisions, lists its parameters and their
sources, and records the failure modes that are silent rather than loud.

- [`SOUPX.md`](SOUPX.md): ambient RNA estimation from empty droplets, automated
  and marker-based contamination fractions, and why correction must precede
  doublet calling in lung tissue.
- [`SCRUBLET.md`](SCRUBLET.md): simulated-doublet neighbourhood scoring,
  threshold selection on the simulated-score histogram, the two free
  consistency checks, and the limits of neotypic detection.
- [`SCDS.md`](SCDS.md): co-expression (`cxds`) and classifier (`bcds`) scoring,
  their `hybrid` combination, benchmark position against other callers, and the
  fact that scds deliberately returns no threshold.
- [`SLINGSHOT.md`](SLINGSHOT.md): minimum spanning tree topology, simultaneous
  principal curves, the two unreported knobs that decide the answer, and what
  supervision does to the interpretation of a trajectory.
- [`TRADESEQ.md`](TRADESEQ.md): the negative binomial GAM, knot selection by
  AIC, the mapping from biological question to statistical test, and the
  pseudotime-comparability caveat that applies directly to the reference study.

Rationale and background (written after the analysis ran):

- [`ANALYSIS_RATIONALE.md`](ANALYSIS_RATIONALE.md): every major decision in two
  passes, what was decided from the data alone, and what changed after reading
  the two source papers, including where the first pass was wrong.
- [`BACKGROUND_FOR_BIOLOGISTS.md`](BACKGROUND_FOR_BIOLOGISTS.md): batch effects
  and Harmony from first principles, for a reader without a computational
  background, including when correction destroys the experiment.
- [`DOUBLETS_AND_SCRUBLET.md`](DOUBLETS_AND_SCRUBLET.md): what a doublet is, how
  Scrublet works, and the two-round audit of whether it removed this project's
  populations of interest, a crude gate said yes, a stricter gate overturned
  it (AT0 flagged at 3.9% vs a 6.3% baseline).
- [`UMAP_AND_FIGURES.md`](UMAP_AND_FIGURES.md): how the UMAP is built from
  counts, what it does and does not mean, how to read dot plots and feature
  plots, and why cluster-marker p-values are a ranking device, not a test.

Supporting documents:

- [`PIPELINE_AS_RUN.md`](PIPELINE_AS_RUN.md): **what was actually executed**,
  per-dataset parameters, cell counts, batch decisions, which of the tools
  above were used, and how the analysis diverges from the source papers.
  Generated from the pipeline's artefacts; regenerate with
  `analysis/scripts/05_write_pipeline_as_run.py`.
- [`Research Article/gate1_01_niethamer_2025/GSE262927/README.md`](../Research%20Article/gate1_01_niethamer_2025/GSE262927/README.md): the full analysis report
  for the primary (mouse) dataset, including QC tables and output locations.
- [`WORKFLOW_Niethamer2025.md`](WORKFLOW_Niethamer2025.md): the end-to-end sequence, ordering
  constraints, subset-and-recluster loop, lineage-trace calling, and quality
  control acceptance order.
- [`scRNAseq_workflow_Niethamer2025.md`](scRNAseq_workflow_Niethamer2025.md):
  the annotated pipeline reference, study design, stage-by-stage parameters,
  marker-gene annotation tables, and the twelve parameters the reference study
  leaves unspecified.
- [`../Research Article/README.md`](../Research%20Article/README.md): the paper-by-paper roadmap
  (the owner's reading order), with per-paper study notes, extracted decision criteria and
  analysis trials; the HLCA note is at
  [`../Research Article/gate1_04_sikkema_2023_hlca/README.md`](../Research%20Article/gate1_04_sikkema_2023_hlca/README.md).
- [`../REFERENCES.md`](../REFERENCES.md): every source study, roadmap paper and
  method paper with DOIs, PMC links and data accessions.

Alignment (STARsolo) and the Seurat stages have no separate schematic. Their
steps are linear and fully covered in [`WORKFLOW_Niethamer2025.md`](WORKFLOW_Niethamer2025.md); a
per-tool diagram would only restate it.

No PDFs are stored in this repository. Three of the five method papers are
CC BY 4.0 and three are not, so every paper is linked to its open-access
version in [`../REFERENCES.md`](../REFERENCES.md) instead.
