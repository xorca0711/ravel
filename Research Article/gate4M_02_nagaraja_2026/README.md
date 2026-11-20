# Nagaraja et al. (2026) — Colitis-associated chromatin memory and early tumour outgrowth

## Published findings

```text
Repeated colitis → epithelial recovery → tumour initiation through Apc loss
  ├─ Recovery: much of the acute RNA response subsides. Colonic stem-cell clones
  │  differ in persistent accessibility at AP-1 motifs, including in clonal organoids.
  ├─ Sequence context: FOX and AP-1 factors can bind cooperatively at selected sites.
  │  Biochemical binding assays test this interaction separately from clonal inheritance.
  └─ After Apc loss: early microscopic lesions are larger in colitis-recovered colons.
       Median lesion area: 5,111 μm² after colitis versus 2,847 μm² in controls.
       Macroscopic tumour counts do not rise in parallel. AP-1 inhibition at initiation
       reduces early outgrowth; inhibition alone was insufficient to erase the memory.

Implication: prior colitis leaves heterogeneous chromatin states in stem-cell clones
             and favors early growth of transformed epithelium after an initiating event.
```

Lineage tracing and single-cell chromatin profiles localized persistent AP-1 accessibility to particular stem-cell clones after recovery. Following tumour initiation, lesion size and lesion count distinguished early expansion from initiation frequency. [Primary article](https://doi.org/10.1038/s41586-026-10258-4)

## Ravel analyses and results

The [staged mouse-colon analysis](../ungated_nagaraja_2026_colitis_memory/README.md) follows the source and donor records. [S1](../ungated_nagaraja_2026_colitis_memory/s1/RESULTS.md) recovered a +16.42 percentage-point early-recovery FOS staining difference. [S2](../ungated_nagaraja_2026_colitis_memory/s2/RESULTS.md) recovered the observed clonal motif variances and showed where AP-1 resemblance depends on membership. [S3](../ungated_nagaraja_2026_colitis_memory/s3/RESULTS.md) compares acute EdU and washout size, reconstructs defined-protein binding scores and measures methylation at the published tissue and organoid loci. [S4](../ungated_nagaraja_2026_colitis_memory/s4/RESULTS.md) separates mouse-level tumour count and burden from the lesion sizes and the two-section P20 comparison. [S5](../ungated_nagaraja_2026_colitis_memory/s5/RESULTS.md) shows that much of the Fos-family variance deficit attenuates when cells are exchanged within the same mouse line. The [figure gallery](../ungated_nagaraja_2026_colitis_memory/FIGURES.md) links the source values and receipts.

## Data and methods

The authors compared colitis-recovered and control mouse colons, tracked stem-cell lineages and assayed accessible chromatin and transcription. Clonal organoids and biochemical binding assays addressed inheritance and AP-1 cooperation with FOX factors.

## Interpretation and open questions

A regional accessibility signal can mark an expanded clone. Matching the prior chromatin history of one clone to the later growth of its own lesion remains a different measurement.

The [post-S5 family comparison](../ungated_nagaraja_2026_colitis_memory/post_s5/RESULTS.md) reproduces the published Fos/AP-1 overlap and finds a smaller variance deficit when organoid cells are compared within mouse line. The [maintenance assessment](../ungated_nagaraja_2026_colitis_memory/post_s5/MAINTENANCE.md) maps the whole-colon methylation, binding and separate adenoma evidence to the missing lineage measurements.

## Figures and supporting documentation

| Study materials | Location |
|---|---|
| Data and design | [Bulk and spatial assays, GSE316619](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316619) |
| Computational methods | [Authors’ archived analysis code](https://doi.org/10.5281/zenodo.18487777) |
| Results and figures | [Chromatin and clones, Figs. 1–2; binding and tumour growth, Figs. 3–4](https://doi.org/10.1038/s41586-026-10258-4) |
| Related studies | [Gate 4M paper sequence](../README.md#gate-4-topic-centered-reading) |
