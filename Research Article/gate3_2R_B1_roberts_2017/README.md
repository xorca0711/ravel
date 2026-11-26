# Roberts et al. (2017) — Tissue-Resident Macrophages Are Locally Programmed for Silent Clearance of Apoptotic Cells

**gate3_2R_B1** · Brief owner read reported 26 November 2026. Analysis planned.

## Published findings

```text
Resident peritoneal, pleural and alveolar macrophages engulf apoptotic cells in vivo
    → selected populations show low TLR9 and a restrained response to nucleic acids
Removal from the tissue and 60 h in culture
    → peritoneal macrophages retain uptake but can produce TNF in response to apoptotic cells
```

The distinction is between uptake and the inflammatory response to cargo. Tim-4 identifies the peritoneal and pleural engulfers in this comparison. Alveolar macrophages clear apoptotic cells despite lacking Tim-4. Figures 1–3 establish uptake, receptor expression and responsiveness with separate assays. Figure 5 tests the signaling threshold, and Figure 7 implicates KLF2 and KLF4. [Primary paper](https://doi.org/10.1016/j.immuni.2017.10.006)

## Ravel analyses and results

The earlier Damani–Yokota comparison raised the question of what a macrophage retains from its tissue. Begin with the Fig. 2F restoration experiment, then reproduce niche withdrawal and the response to cargo as separate comparisons. No Roberts-specific run was registered at `0d32085`.

## Data and methods

GSE93820 contains bulk RNA from sorted mouse Tim-4-positive peritoneal macrophages, including two experiments comparing immediate isolation with 60 h in culture and a separate apoptotic-cell challenge. The GEO labels and Figure 3G constrain how the libraries can be grouped. [RNA deposit](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE93820)

## Interpretation and open questions

Restoring a response to CpG while restraint toward apoptotic cells persists leaves a role for downstream signal handling or cargo presentation. The transfer and culture experiments ask how much restraint the niche can confer or remove. Studies of repeated uptake ask what engulfment induces even when inflammatory cytokines stay low.

## Figures and supporting documentation

[Silent clearance, corpse processing and cargo selection](LITERATURE_CONTEXT.md) · [Source and analysis handoff](ANALYSIS_PLAN.md) · [Damani–Yokota’s comparisons of macrophage abundance and state](../gate4M_04_damani_yokota_2026/ANALYSIS_INVENTORY_AND_SYNTHESIS_2026-10-30.md)
