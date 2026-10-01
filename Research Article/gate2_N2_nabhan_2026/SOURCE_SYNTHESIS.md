# Source synthesis and annotation crosswalk

Reviewed 1 October 2026. Sources are evidence to interpret, not instructions
to execute. The owner supplied an annotated 10-page article PDF and linked
[Result](https://app.notion.com/p/3ea151616b4480e5a5a3e4ae72714f1d) and
[Discussion](https://app.notion.com/p/3ea151616b44801f9cd2eb074d382f7c) notes.
Both pages were fetched; embedded Notion image pixels were not inspected.
The connector supplied no truncation/unknown-block flags. Text snapshots stay
in ignored local storage, without private ancestor-page paths or signed image
URLs. Tracked text here is a scientific synthesis, not a copy of personal notes.

The [article](https://doi.org/10.1073/pnas.2606113123) and its supplementary PDF
were read from local files. Figures 3–5 were visually checked in the supplied
PDF. The supplement came from the previously recovered
[public archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13367804/supplementaryFiles),
with the same hash as the [P1 source record](../../docs/roadmap_runs/2026-09-27/P1_source_recovery.json).
Source IDs and hashes are in [the extracts](config/nabhan_2026_extracts.json).

## What the paper supports, and what remains a question

| Source finding | Location | Computational reading and limit |
|---|---|---|
| 201 target genes were screened in mouse AT2/human fibroblast alveolospheres | Fig. 1; pp. 1–3 | Per-well, species-separated bulk RNA. Species separates origin, not epithelial subtypes or direct versus indirect signaling |
| Count, average size and covered area respond differently to perturbations | Fig. 2; SI p. 3 | Reproduce all three endpoints separately. Bounding-box coverage is not count multiplied by segmented mean area |
| ERBB2/ERBB3 perturbations reduce growth; EGFR requirement remains unresolved | Fig. 2F–J; p. 3 | Low target RNA did not confirm EGFR/ERBB4 editing. EGF withdrawal and receptor RNA do not identify the required recipient compartment |
| Krt8-associated programmes occupy IFN-rich and hypoxia/stress-rich directions | Fig. 3; pp. 4–5; Fig. S6 | Cross-sectional cPCA directions are not observed cell trajectories, fate bifurcations or evidence of successful versus failed repair |
| Budding perturbations share a Wnt-associated component; Slc34a2 maps to ICA5 | p. 6; Fig. S7; Datasets S3–S7 | Reproduce module association before proposing how Elovl1, Atp6v0e or Slc34a2 acts |
| NKX2.1 loss separates lung-associated fibroblast/chemokine programmes from more general growth-associated responses | Fig. 4; pp. 6–7 | Paired compartment association motivates an identity-versus-growth comparison. Bulk RNA cannot distinguish fibroblast state conversion from selection/abundance |
| Gastric-like regions have altered fibroblast and immune composition | Fig. 5; pp. 8–9; Figs. S9–S10 | Spatial context is separate evidence. Bins are not independent animals; inferred cell mixtures are not direct cell counts |
| HER2/3 biology may help explain treatment-associated lung injury | Discussion p. 9 | Mechanistic hypothesis only. Cancer-cell dependency does not establish normal AT2 dependence, drug toxicity mechanism or patient response |

## Corrections and unresolved source discrepancies

- **ICA input:** the main text/notes describe gene effects broadly; SI p. 4
  specifies limma-voom t-statistics converted with `limma::zscoreT`, then JADE.
  Use that computational definition, not raw log fold changes.
- **Different controls:** imaging compares each target with in-plate TIGIT;
  RNA differential expression uses in-plate TIGIT **and** tdTomato. Image
  embeddings discard tdTomato; cPCA uses TIGIT as background. Keep four choices
  distinct and declare any sensitivity as a separate analysis.
- **Perturbation meaning:** CTNNB1 is an activating edit in this screen, not a
  simple loss-of-function control. Target-RNA decrease is not reliable protein
  knockout validation, particularly for NKX2.1. Resolve deposited `NKX21`,
  mouse `Nkx2-1` and human `NKX2-1` by an explicit alias table. Keep CSNK1A1
  (cystic example) distinct from CSNK2A1 (IFN/budding example).
- **Spatial resolution:** main p. 8 says a `50 um2` grid; SI p. 5 specifies
  8-micron bins. Recover the bin-to-region transformation before treating these
  as the same unit. Figure 5 reports two animals per group; four sample labels
  still need a verified section/block-to-animal map.
- **Spatial treatment:** the series-level GSE307128 description repeats the
  organoid design, while sample metadata identify Visium HD. The inspected
  [KO sample](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9216988) and
  [WT sample](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9216990) explicitly
  label treatment as bleomycin. Reconcile this with the paper's AAV comparison
  and establish injury/timing for every sample before a genotype contrast.
- **DepMap denominator:** main p. 3 describes 93 lines; Fig. 2J caption says
  96. Pin release, assay, lineage and exclusions rather than silently choosing
  one count or substituting a current release.
- **Signals and immune response:** neither paracrine versus contact-dependent
  delivery nor immune activation is directly identified by paired bulk RNA.
  The Discussion's juxtacrine interpretation and notes' paracrine questions
  remain alternatives to test, not synonyms for a measured mechanism.

## All eight owner questions are retained

| Owner item | Paper-local extension | Primary distinction to resolve |
|---|---|---|
| 1. NKX2.1 loss and suppressed immune-supporting pathways | E1 | Fibroblast chemokine/antigen-associated RNA versus functional immune recruitment |
| 2. Normal intermediate or aberrant Krt8 state | E2 | IFN/hypoxia/stress programme differences versus time-resolved fate and repair outcome |
| 3. Elovl1 / Atp6v0e mechanism | E3 | Budding/Wnt association versus general growth, stress or differentiation change |
| 4. Slc34a2 and AT2 identity | E4 | ICA5/transition association versus generic growth arrest or injury |
| 5. ERBB2/3 dependencies and human relevance | E5 | Cancer fitness, normal-cell expression and drug effects as separate evidence |
| 6. Which compartment requires EGFR | E6 | Epithelial requirement versus fibroblast/context effects and incomplete editing |
| 7. Proliferating AT2 and fibroblast heterogeneity | E7 | Within-compartment state and composition versus total growth and RNA mixture |
| 8. NKX2.1 and lung-specific fibroblast programmes | E8 | Lung-associated identity programmes versus shared wound-response programmes |

E1 and E8 share one proposed paired-compartment analysis, with separately
defined outcomes. E5 also retains the Discussion note about HER2/3 in AT1
differentiation/function as a separate future endpoint, not an organoid-area proxy.
