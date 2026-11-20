# Cowley et al. (2026) — Sequence determinants of epidermal chromatin memory

## Published findings

```text
An acute skin flare opens regulatory DNA in epidermal stem cells
  ├─ Establishment: inflammatory transcription factors, including AP-1, open domains.
  │  Most subsequently lose accessibility. Roughly one in ten retains long-term memory.
  ├─ Persistence: sequence features distinguish long-lived from resolving domains.
  │    CpG-rich regions remain hypomethylated, bind methylation-sensitive factors,
  │    and accumulate the histone variant H2A.Z. The combination favors open chromatin.
  └─ Recall: genes associated with long-lived domains, including Aim2 and Il18,
     retain heightened responsiveness to a later stimulus even two years after the flare.
     The late recall assay measures transcription; wound repair was assessed separately.

Implication: the features that establish an inflammatory memory can differ from the
             sequence and chromatin features that sustain it through cell divisions.
```

The authors followed regions that opened during skin inflammation for up to two years. Comparing regions of different lifetimes linked CpG-rich sequences to sustained DNA hypomethylation and H2A.Z occupancy. [Primary article](https://doi.org/10.1126/science.adz6830) · [Accessibility, sequence and epigenetic measurements](https://pmc.ncbi.nlm.nih.gov/articles/PMC13295011/)

## Ravel analyses and results

The Naik package contains a shared-source comparison of Cowley’s distal Memory and Resolved regions at 24 months. The accessibility gap between the two classes widened in each of the four possible comparisons of previously inflamed and control pools. The four comparisons reuse two pools per condition. [Results and sampling units](../gate4M_01_naik_2017/distal_m24_outcome_v1/RESULTS_V1.md)

## Data and methods

The authors compared epidermal stem-cell ATAC profiles over recovery with nucleotide-level predictions of domain persistence, DNA methylation and histone-variant measurements. The genomic region is the unit for the sequence comparisons.

## Interpretation and open questions

Sequence features help explain why some regions outlast others. The persistence of a region alone does not identify the target gene or quantify its contribution to wound repair.

## Figures and supporting documentation

| Study materials | Location |
|---|---|
| Data and design | [Epidermal ATAC-seq, GSE299177](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299177) |
| Computational methods | [Authors’ archived analysis code](https://doi.org/10.5281/zenodo.18057635) |
| Results and figures | [Primary article and supplementary material](https://doi.org/10.1126/science.adz6830) · [Ravel 24-month comparison and figure](../gate4M_01_naik_2017/distal_m24_outcome_v1/RESULTS_V1.md) |
| Related studies | [Gate 4M paper sequence](../README.md#gate-4-topic-centered-reading) |
