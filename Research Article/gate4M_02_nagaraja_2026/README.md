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

Lineage tracing and single-cell chromatin profiles localized persistent AP-1 accessibility to particular stem-cell clones after recovery. After tumour initiation, the authors observed larger early lesions with similar gross lesion counts. [Primary article](https://doi.org/10.1038/s41586-026-10258-4)

## Ravel analyses and results

**FOS marks a recovering epithelial population.** At day 21, FOS staining in CD44-positive crypt cells averaged 16.42% in three recovered mice and 0.00% in three controls. The published accessibility model also estimated a higher mean Fos-family motif score in recovered stem/progenitors. The staining and motif scores measure different endpoints. [Tissue recovery and source coverage](s1/RESULTS.md)

| Comparison | What Ravel found |
|---|---|
| Clonal organoids | The released score rows reproduced all 295 defined median clone variances. Among 50 motif reporters matched across tissue and organoid analyses, Fos alone met both published thresholds. For cells assigned to one clone, the Fos variance deficit fell from 10.36% under the global shuffle to 4.29% when cells could exchange only within their mouse line. None passed the full within-line multiple-testing threshold. [Clone replay](s2/RESULTS.md) · [Mouse-line sensitivity](s5/RESULTS.md) · [Family comparison](post_s5/RESULTS.md) |
| AP-1 inhibition and methylation | Whole-colon methylation at *Dcaf5* retained much of the colitis-associated difference during the five-day treatment window. At *Rbm27* the inhibitor-treated recovered mean moved closer to the control-vehicle mean. [Tissue and organoid results](s3/RESULTS.md) |
| Early adenomas | The average fraction of gross lesions over 1 mm was 59.07% after colitis and 31.69% in controls. Gross counts averaged 24.4 and 25.0 per mouse. An independent microscopic cohort also had greater tumour-area burden after colitis. [Mouse and lesion records](s4/RESULTS.md) |
| JUN and FOXP1 at 63 selected loci | Adding FOXP1 increased the JUN footprint at all 63 sequences in vitro without FOS. The size of that gain barely tracked the day-102 difference in epithelial accessibility (adjusted rank ρ = −0.015, four recovered and two control mice). At day 50 the association was inverse (−0.370) and weakened using fold change (−0.121). [Locus measurements](jun_foxp1/stage2/MEASUREMENTS.md) · [Association and sensitivity estimates](jun_foxp1/stage3/RESULTS.md) |
| Eight flanking CpGs in independent colon cohorts | Only **cg31603876_BC21** on chr13 had a shared methylation loss that survived every one-mouse omission. DSS-history minus control was −3.50 percentage points in day-14 isolated epithelium and −10.00 in day-23 whole colon. The smallest retained epithelial loss was 0.36 points. Five shared gains reversed on an epithelial mouse omission. Two sites had opposite directions. [All eight sites and individual mice](jun_foxp1/saline_markers/NUMERICAL_RESULTS.md) |

## Data and methods

| Evidence | Comparison and biological unit |
|---|---|
| Published SHARE-seq and SHARE-TRACE analyses | Ravel used deposited motif scores, clonal memberships, mouse counts and reported model fits. Six mouse-derived organoid lines contributed to the clonal comparison. Individual cells and clones share their line’s history. The exact per-mouse high-accessibility fractions and independent state labels remain unresolved. [Source and panel eligibility](s0/PANEL_ELIGIBILITY.md) · [Clone sampling](post_s5/RESULTS.md) |
| Biochemical footprints, native ATAC and methylation | Paired sequence scores compare one deposited library per protein condition. Native ATAC contrasts use same-cohort controls at days 50 and 102. Locus-level comparisons join genomic positions across separately sampled assays. Only one scored motif contains a CpG, and none of the 34 composite cores contains one. [Coverage by mouse, motif and flank](jun_foxp1/stage1/ELIGIBILITY.md) |
| Independent methylation array, GSE283386 | Three saline-treated DSS mice and three saline-treated water controls contributed to day-14 epithelial array estimates after one DSS exposure. The Nagaraja comparison used three recovered and three control vehicle mice, with whole-colon EM-seq after three DSS cycles. Within each study, differences use the same interrogated cytosine, equal mouse weights and a common DSS-minus-control direction. [Prespecified comparison and prior exposure](jun_foxp1/saline_markers/DESIGN.md) · [Specimens and strands](jun_foxp1/saline_markers/CHECKPOINT.md) |

## Interpretation and open questions

The tissue and clone results support Fos/AP-1 as a reporter of inflammatory history. The mouse-line sensitivity shows how much the clonal inference depends on which cells form the comparison group. The lesion data establish a size difference at harvest. Connecting an earlier chromatin state to the growth of its own lesion would require a lineage or specimen link. [Paper reproduction synthesis](SYNTHESIS.md) · [Maintenance evidence](post_s5/MAINTENANCE.md)

The chr13 site is a candidate **regional marker**. It lies 209 bp downstream of the sole scored-motif CpG. The two cohorts differ in recovery time, injury regimen, tissue preparation and assay. Whether JUN and FOXP1 occupy this region after FOS declines, and whether methylation loss precedes or follows occupancy, remain open. The Yin selection libraries can address each isolated factor’s preference for a shortened sequence. The native 12-base motif appeared only 0–2 times per library. [External dataset assessment](jun_foxp1/external/QUALIFICATION.md) · [Marker-screen interpretation](jun_foxp1/saline_markers/NUMERICAL_RESULTS.md#technical-closeout)

## Figures and supporting documentation

[Figure gallery · 14 figures, PDFs and source values](FIGURES.md) · [Analysis plan and stage records](ANALYSIS_PLAN.md) · [Literature and deposits](LITERATURE_CONTEXT.md) · [Authors’ analysis code](https://doi.org/10.5281/zenodo.18487777) · [Gate 4M reading sequence](../README.md#gate-4-topic-centered-reading)
