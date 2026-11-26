# Pestal et al. (2025) — KLF family members control expression of genes required for tissue macrophage identities

**gate3_2R_B2** · Brief owner read reported 26 November 2026. Analysis planned.

## Published findings

```text
Macrophage precursors enter the peritoneal cavity
    → KLF2 supports acquisition of large cavity macrophage identity
    → native cavity macrophages show KLF2 binding at Gata6 and retinoid receptor loci
Lung alveolar macrophages
    → KLF4 deficiency changes population abundance and the phenotype of remaining cells
```

The day-0 and day-7 transfer experiment asks when KLF2-dependent expression emerges (Fig. 3). Native-cell binding and ectopic-expression experiments ask which loci might explain that dependence (Figs. 4–5). The lung experiments use a different KLF, macrophage population and set of comparisons (Figs. 6–7, Fig. S5 and Table S5). [Primary paper](https://doi.org/10.1084/jem.20240379)

## Ravel analyses and results

The prior reading singled out the lung KLF4 phenotype. Begin by reconstructing cavity populations and shared-host competition, then test acquisition after transfer and regulation at individual loci. The lung has its own comparison of cell representation and phenotype among remaining cells. No Pestal-specific run was registered at `0d32085`.

## Data and methods

GSE288281 includes RNA from donor bone-marrow-derived macrophages before and after cavity transfer, an overexpression series, and sorted alveolar macrophages. GSE288282 contains native large cavity macrophage CUT&RUN, with anti-GFP and IgG paired within three mice. [RNA](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE288281) · [CUT&RUN](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE288282)

## Interpretation and open questions

Failure to recover a canonical cavity macrophage could reflect impaired niche sensing, poor survival or entry into a different maturation route. Day-zero precursors and the contrasting KLF2 and GATA6 perturbations constrain different explanations. In lung, both abundance and the phenotype of surviving cells can change.

## Figures and supporting documentation

[Retinoid competence, maturation routes and lung identity](LITERATURE_CONTEXT.md) · [RNA, binding and alveolar comparison handoff](ANALYSIS_PLAN.md) · [Roberts on the clearance phenotype](../gate3_2R_B1_roberts_2017/README.md) · [Wang’s example of qualifying a sorted-cell RNA comparison](../gate3_10_wang_2018_ezh2/README.md)
