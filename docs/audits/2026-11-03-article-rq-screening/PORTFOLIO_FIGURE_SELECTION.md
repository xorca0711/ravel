# Root README portfolio figure selection

Reviewed 3 November 2026. Documentation curation of existing numerical outputs;
no new analysis, rendering of scientific data, claim promotion or asset copy.

The owner requested a visually strong methods panel and removal of the pilot
intake description. The Ravel project media on the supplied LinkedIn profile
were inspected as a style reference. The owner subsequently clarified that
these month-old choices need not be matched individually. Selection therefore
uses current repository captions, correction history and the visual diversity
of available figures. No LinkedIn content or account setting was changed.

## Confirmed panel

Six previews in three paired rows, immediately after the start-here links.
Each image opens its existing full-resolution file; the adjacent caption links
the owning methods and source values. Small preview text is not a substitute
for opening the scientific figure. Complete study/RQ galleries stay local.

| View | Why it belongs in a research portfolio | Current evidence and interpretation boundary |
|---|---|---|
| Nb4 stromal UMAP | Colourful, interpretable cell neighborhoods; donor, anatomy and expression on fixed coordinates demonstrate analysis/QC judgment. | [Figure 7 and source links](../../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/FIGURES.md#figure-7-new-stromal-umap-with-technical-context). 5,033 cells, three donors; no trajectory or donor-effect removal is claimed. |
| A11 patient-paired expression | PCA, paired observations, contrasts and a heatmap show the statistical unit and heterogeneity rather than only an attractive embedding. | [Generated A11 caption](../../../analysis/figures/rq/README.md#a11). 70 patient–histology units include 23 normal/LUAD pairs; cross-sectional RNA programmes do not establish malignant identity or progression. |
| A1 CUT&Tag locus tracks | A distinct epigenomic measurement, native-coordinate handling and H3 controls complement expression plots. | [Direct histone profiles](../../../RQ_Specified/A1_transitional_epithelial_state_distinction/figures/README.md#direct-histone-profiles-and-controls). Corrected `second_batch_verified` asset; one iPSC line, two preparations per state, independently scaled CPM tracks. Alternate-TSS sensitivity remains linked; no gene-wide activation or absolute occupancy claim. |
| Nb3 Hallmark enrichment | The dot heatmaps communicate multicomparison analysis; the sensitivity panel visibly tests whether a result depends on a modelling assumption. | [Figure 8](../../../Research%20Article/gate2_N2_nabhan_2026/FIGURES.md#figure-8-hallmark-context-and-correlation-sensitivity). Rank-based cameraPR and multiplicity adjustment, with all 50 sets retained. Exploratory RNA context with source nesting; enrichment is not measured pathway activity. |
| Yu spatial RNA | Whole-section geometry adds a visibly different assay and demonstrates spatial coordinate/QC handling. | [Spatial report](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/REPORT.md). The illustration is two sections from one patient; spots are mixtures. No pathology-defined region, cell contact or independent replication is inferred. |
| Arozamena paired RNA/accessibility | A current corrected multiome example shows barcode pairing, coordinate reconciliation and modality-specific normalization. | [Accessibility results](../../../Research%20Article/ungated_arozamena_2026_inflammatory_memory/ACCESSIBILITY_RESULTS.md). Use `arz1_accessibility_primary_render_v1`, which already supersedes the earlier display. Finite libraries share CTRL; fragment-record overlap is not peak/cut-site counting, promoter activity or regulatory memory. |

## Exclusions and preservation

- The old A1 RNA–ATAC composite has a legacy “closed or silenced” title whose
  interpretation was withdrawn. Its visual appeal does not justify prominent
  reuse in the root README. The newer corrected paired example carries the
  RNA/accessibility method instead.
- The A1 promoter heatmap remains useful in its gallery, but a second CUT&Tag
  example would duplicate the same assay at the expense of spatial and
  patient-level analysis. The selected tracks retain all plotted controls.
- Recent Yadav plots were considered through their current gallery. A seventh
  source-reconstruction panel would expand the root page without adding a
  missing method category to this bounded selection.
- Proposed schematics, synthetic diagnostics and photographs were not mixed
  into this measured-data panel. Selecting a figure does not rank or retain
  its biological RQ or certify that its hypothesis succeeded.
- Source images, numerical outputs, frozen scripts and owning galleries are
  unchanged. Only Markdown presentation/navigation is modified.

## Validation

All six source images were visually inspected at readable resolution against
their current captions. The README uses ordinary GitHub-flavoured Markdown
tables and repository-relative paths, with full-resolution image and methods
links. A local GitHub-style browser preview showed the full two-column layout
and all six loaded images at their expected native dimensions. This verifies
the local layout, not GitHub's exact rendering. Repository validation passed
15,106 checks; the research gate and whitespace checks passed against unchanged
`origin/main` (`115f3c5`). Numerical tests were reused because no analysis code
or data changed. See [the project state](../../../PROGRESS.md).
