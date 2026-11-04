# Research skills and plugin usage review

Reviewed 4 November 2026. This is a capability and applicability audit, not a
new numerical analysis, method freeze, installation request or scientific result.
The current [biological screening amendment](BIOLOGICAL_SCREENING_AMENDMENT_V1.md)
and [repository decision workflow](../../AGENT_DECISION_WORKFLOW.md) govern use.

## What is actually available

- **212 SciAgent skill files** are present under
  `C:/Users/dream/.codex/plugins/cache/sciagent-skills/sciagent-skills/1.0.0/skills`.
  These include 73 genomics/bioinformatics, 11 systems-biology/multiomics,
  24 scientific-writing, eight visualization and four biostatistics skills.
  The remaining categories cover computing, cells, molecules, proteins,
  structural biology, imaging and laboratory automation. This counts files on
  disk; it does not assert that every skill is loaded in this chat.
- **95 local skill files have 4 November modification timestamps**, under
  `C:/Users/dream/.codex/skills`. This bundle is predominantly AI/ML training,
  inference, optimization and agent orchestration. Modification times indicate
  recent local files, not verified installation dates.
- Existing NCBI Entrez, CELLxGENE, BioStudies, literature/citation, Scanpy and NGS
  journey skills remain useful. New overlapping guides do not create an
  independent source or require replacing a working method.
- Live callable tools are exposed for **NGS Analysis Workbench/Compute,
  BioRender, Context7, Hugging Face, Biological Sequence Viewer, Notion,
  GitHub and Google Drive**. Tool exposure establishes an interface, not
  successful authentication, account identity or execution readiness.
  BioNeMo domain skills are present; a ready NIM service was not established.

The audit inventoried names/categories, screened relevant descriptions, and
read selected workflow and limitation sections. It did not perform a complete
line-by-line or executable review of all 307 files. Plugin Management was used
to check discoverability; searches are non-exhaustive. Scite appeared as **not
installed**, so it is not counted as a current capability. Nothing was installed
or reconfigured.

## Where they can improve the current research

| Capability and local skill names | Biological use in this repository | Appropriate next use and limit |
|---|---|---|
| NCBI Gene, QuickGO, UniProt, Reactome (`gene-database`, `quickgo-database`, `reactome-database`) | A5: distinguish junction/polarity, matrix, transport and signaling-context members; A31: clarify receptor-partner annotations | Reuse A5's completed source-backed annotation. Consult selectively when a newly nominated member needs identity/function clarification. Curated function does not establish activity in the measured cells. |
| `cellchat-cell-communication` | Cardoso-style sender → input → recipient candidate links; A9/A12 recipient configurations | A future bounded screen could compare a named ligand/receptor/cofactor configuration within defined samples and cell groups. Preserve donor support and separate population abundance from within-group expression. Inferred communication is not measured secretion, receptor engagement or a causal edge. It does not automatically represent extracellular proteolysis, active-ligand release or an ARG1 substrate circuit. |
| `jaspar-database`, `homer-motif-analysis`, `bedtools-genomic-intervals`, `deeptools-ngs-analysis` | A3/DY1: separate candidate regulatory persistence from RNA effector context | First specify the unresolved regulatory comparison, compatible peak coordinates/genome, background and source units. Then inspect a bounded candidate motif/locus set if it can change interpretation. Motif occurrence/enrichment is not occupancy or TF activity; related TF motifs may be indistinguishable. A normalized bigWig is not an integer peak-count matrix. |
| `multimodal-omics-integration`, `mofaplus-multi-omics`, `muon-multiomics-singlecell` | A3 RNA–ATAC discrepancy; eligible Arozamena single-cell multiome questions | Use only when modality units and the intended contrast fit. MultiVI supports paired and unpaired **single-cell** data; it does not turn the paper's bulk ATAC and scRNA measurements into matched cells. Imputation is a model output, not an observed missing modality. No automatic integration rerun. |
| `cellxgene-census`, `cell-type-annotation`, `celltypist-cell-annotation` | A31: an external fibroblast context; A12: epithelial recipient state; A27: eventual label qualification | Select source, release, donor, tissue and assay before extracting cells. Reference/marker comparison can test label compatibility, but transferred labels cannot establish that historical labels were independent of receptor information. Preserve nominal A27 codes in the cleared run. Reused atlas samples are not replication. |
| `gseapy-gene-enrichment`, `deseq2-differential-expression`, `statistical-analysis` | A future comparison yielding a justified gene set, ranking or replicated count model | Fix the gene universe, identifier mapping, ranking/contrast, biological unit and dependence before testing. Do not test a preselected module against an inappropriate whole-genome universe. A3's qualified Salmon-derived descriptive display does not become an inferential DE analysis just because DESeq2 is available. |
| `brenda-database`, `kegg-pathway-analysis`, `cobrapy-metabolic-modeling` | A32/Wg-P06: distinguish ARG1 substrate supply, recipient routing and separate matrix/epithelial outcomes | Enzyme/reaction annotation can organize alternatives. Flux modeling requires a justified compartment model, exchange constraints and objective. RNA alone cannot supply measured substrate exposure, reaction flux or collagen output. A default growth objective would not answer this RQ. |
| `general-figure-guide`, `omics-plotting`, `matplotlib-scientific-plotting`, `multipanel`; BioRender | Clear measured figures and explicit biological hypotheses | Apply label/scale/support/NA checks to new outputs. Use deterministic plots for measured values and BioRender for qualitative biological entities. Preserve frozen outputs; a correction uses a new version. A3/A27 reviews can benefit without recalculating their endpoints. |

These are candidate uses, not approvals for all the analyses in the table.
Current evidence still decides whether a method adds information.

## Which guidance needs adaptation

1. **Generic autonomous research is not the repository controller.**
   `0-autoresearch-skill` requests a continuity loop, its own root-level state
   architecture, autonomous pivots and indefinite continuation. It also contains
   useful protocol-locking and negative-result recording advice. The repository
   already owns these functions through question cards, contracts, receipts and
   review. Do not create competing state files, scheduled loops or a new
   research direction merely because the skill says to do so. `a-evolve` targets
   AI-agent optimization, not biological evidence adjudication.
2. **Hypothesis prompts are optional reasoning aids.**
   The new `hypothesis-generation` guide calls for an always-mechanistic
   explanation and three to five alternatives. That is too rigid for legitimate
   descriptive, replication or prediction work here. Retain the distinction
   between observation, explanation and prediction; use consequential alternatives
   when relevant. Do not invent mediators or extra groups to fill a template.
   `brainstorming-research-ideas` itself excludes already-defined execution tasks.
3. **Versioned source documentation outranks example snippets.**
   The CellChat guide centers v2; the official repository now distinguishes v2
   from spatial v3. The JASPAR guide references 2024 collections. Pin the actual
   selected package/database versions rather than assuming a newly installed
   skill contains the newest compatible recipe. Context7 can help with API
   usage; primary papers remain necessary for scientific assumptions.
4. **The AI/ML bundle has limited immediate value for these screens.**
   Its brainstorming, writing and quantitative plotting advice can help selectively.
   Most model-training/quantization/agent/cloud skills do not address the current
   RQs. `academic-plotting` includes a Gemini diagram route; that is a separate
   provider dependency, not evidence that Gemini access exists. Existing plotting
   and BioRender tools already fit the present figure tasks.

## Read-only readiness checks

The existing `X:/GitHub/ravel/.venv-x64/Scripts/python.exe` reports distribution
metadata for Scanpy 1.12.3, AnnData 0.13.2, NumPy 2.4.6, pandas 2.3.3,
SciPy 1.18.0, matplotlib 3.11.1, seaborn 0.13.2, GSEApy 1.3.1,
scvi-tools 1.5.0.post1, MuData 0.4.1 and PyDESeq2 0.5.4. Metadata was absent
for `cellxgene-census` and `cobra` in that environment. This was **not** an import,
compatibility or workflow smoke test. `Rscript` was not found on the checked
shell PATH; other R installations/environments were not exhaustively searched.

Workbench lists one target, `local`. Its server-authored runtime snapshot reports
Windows/amd64, no discovered Nextflow/Snakemake controller, missing Java/Docker
on that service's PATH, and no reachable Docker daemon. Thus Workbench execution
readiness is **not established**. This does not invalidate or block the existing
repository-run Python analyses, and says nothing about an unregistered remote
host or another environment. No installation or workflow was launched.

BioRender currently exposes custom illustration creation and asynchronous preview
retrieval in addition to search. That is useful for a future schematic task;
this audit did not create a paid job or verify the intended external account.
The Sequence Viewer could inspect a specific sequence question, but it is not
needed to replace A27's fixed operational receptor-key counting. Hugging Face
is more relevant if a specific reference model/dataset is justified; generic
model availability does not improve the present statistical estimand.

## Application sequence

1. Finish reviewing the **already frozen A3** result and the **approved A27**
   implementation. Apply figure/interpretation checks without changing their
   endpoints. A5/A31 reviewed results remain complete.
2. For each subsequent biological decision, name one useful capability from the
   table and the result that could change a candidate, interpretation or next
   measurement. Prefer existing evidence and simple deterministic analysis when
   they answer it.
3. Read that skill's applicable sections; verify current primary documentation,
   source identity/units and actual runtime. Record only material unresolved
   constraints. Do not restart a portfolio-wide qualification exercise.
4. If a new numerical comparison is justified, amend and freeze it prospectively
   under existing governance, then run and independently review it. Keep negative
   results, source overlap and exposure explicit. No new claim grade follows from
   a new tool or a completed run.

The existing technical chat received these usage boundaries. This review changes
tool selection advice, not the cleared A3/A27 designs or their scientific status.

## Primary documentation checked

- [CellChat official repository](https://github.com/jinworks/CellChat): inference
  scope and v2/v3 distinction; accessed 4 November 2026.
- [MultiVI model documentation](https://docs.scvi-tools.org/en/stable/user_guide/models/multivi.html):
  single-cell inputs, paired/unpaired integration and missing-modality modeling;
  accessed 4 November 2026.
- [CELLxGENE duplicate-cell documentation](https://chanzuckerberg.github.io/cellxgene-census/notebooks/api_demo/census_duplicated_cells.html):
  repeated cells across datasets and `is_primary_data`; accessed 4 November 2026.
  Deduplicating cells alone does not establish independent donor cohorts.
