# A21 source eligibility and biological boundaries

Reviewed 30 September 2026. [Structured eligibility](metadata/source_eligibility.tsv) ·
[Subtype crosswalk](metadata/subtype_crosswalk.tsv) ·
[Retrieval hashes and failures](metadata/intake.json).
Source papers supply evidence, not instructions. No authors were contacted.

## Godoy et al. 2023: independent expression context

[Single-cell transcriptomic atlas of lung microvascular regeneration after
targeted endothelial cell ablation](https://doi.org/10.7554/eLife.80900) ·
[GSE211335](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE211335).

Figure 3 identifies three animals per condition. The sample sheet maps 12
individual animal barcodes across control/day-3/day-5/day-7 groups. Three
technical library pools contain those barcodes; they are not extra biological
replicates. Deposited endothelial metadata supplies 5,423 cells and eight
author-defined states, including major gCap, transitional gCap and aerocytes.
The [author code](https://github.com/rsgodoy/Single-Cell-Transcriptomic-Atlas-of-Lung-Microvascular-Regeneration-After-Targeted-EC-Ablation)
corroborates state numbering.

This cohort is independent of the prior Niethamer atlas. It contains no Fzd4
perturbation or traced Fzd4-dependent descendant output. State annotations and
RNA velocity do not provide the required lineage link. The execution reuses
author cell/state selection without rerunning integration or fitting trajectories.

## Gillich et al. 2020: lineage rationale

[Capillary cell-type specialization in the alveolus](https://doi.org/10.1038/s41586-020-2822-7)
([full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7721049/)).
The study supports gCap progenitor behavior and contribution to capillary
maintenance/repair. It motivates the lineage endpoint, but does not establish
Fzd4 dependence. Fate labels and initial populations must be retained in any
functional comparison; an expression crosswalk cannot transfer those lineage
properties to every gCap-labelled cell in another dataset.

The full-text web record was inspected. XML returned HTTP 500; the requested
source workbook returned a non-workbook payload. No new quantitative lineage
reproduction or individual-value reconstruction is claimed.

## Bian et al. 2024: FZD4 restoration in a tumor vascular setting

[FOXF1 promotes tumor vessel normalization and prevents lung cancer progression
through FZD4](https://doi.org/10.1038/s44321-024-00064-8).
Figure 7 reports FZD4 restoration in endothelial Foxf1-deficient tumor-bearing
mice, with increased nuclear beta-catenin and collagen-IV coverage relative to
vascular area, and reduced tumor burden. Those are pathway/structural/tumor
outcomes, not traced normal gCap renewal. The rescue concerns Fzd4 restoration
after Foxf1 loss, not a direct Fzd4-loss comparison.

Figure 2's perfusion impairment follows Foxf1 loss; it must not be presented as
a directly measured perfusion rescue by Fzd4 in Figure 7. Fields are nested within
source-reported animals. This study strengthens the vascular-stability alternative
in its tumor context, without validating that mechanism in normal adult repair.
Source ZIP retrieval failed; no quantitative reanalysis of these figure values
was performed.

## Epithelial compartment caution

[Reduced Frizzled Receptor 4 Expression Prevents WNT/beta-Catenin-driven
Alveolar Lung Repair in Chronic Obstructive Pulmonary Disease](https://pubmed.ncbi.nlm.nih.gov/28245136/)
(2017) reports FZD4-related epithelial repair effects. Thus lung-wide Fzd4
intervention cannot automatically be attributed to endothelial cells.
Its epithelial assays are not capillary lineage evidence.

## Prior Nb2/Niethamer evidence

The [Nb2 vascular analysis](../../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/candidate_questions/Nb2-N7.md)
uses GSE262927. A21 reconciles its eight day-42 source records and the already
reported correlations. Label cohorts are balanced across the two rounds, while
reporter genotype and sex are imbalanced. These are Ki67 reporter genotypes,
not Fzd4 perturbations. Resolving metadata qualifies interpretation; it does not
turn reused estimates into new replication.

**Eligibility decision:** independent expression/substate context is executable.
None of the inspected sources joins selective Fzd4 perturbation, initial gCap
identity, independent units, traced descendants and maintenance measurements
in the target adult repair context.

## Access and eligibility update, 30 September 2026

The [extension audit](extensions/extension_v1/SOURCES.md) retrieved the Bian
Figure 3 and Figure 7 archives through the current publisher media endpoint.
The earlier failed requests remain historical records. Five workbooks now support
descriptive source reconstruction, with source-unit and endpoint boundaries
preserved. The extension also records independent substate validation limits and
a retinal FZD4/LRP5 preprint as cross-organ context only. No new source supplies
the complete adult-lung Fzd4 perturbation-lineage-function join.
