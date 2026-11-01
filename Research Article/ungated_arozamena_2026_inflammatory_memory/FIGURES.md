# Arozamena figure gallery

1 November 2026. Four figure plates are reviewed: two RNA and two paired
RNA/accessibility plates. PNG and SVG are alternate formats of the same plate,
not separate analyses. [RNA results](RNA_RESULTS.md),
[accessibility results](ACCESSIBILITY_RESULTS.md),
[originating review](ORIGINATING_REVIEW.md) and [job ledger](README.md) give the
scope and remaining holds. Held-v1 placeholders and archived render versions
are not additional substantive figures.

## Figure 1: separate deposited RNA contrasts

![Four accession-specific selected-target RNA contrasts](../../analysis/research/runs/arz1_rna_description_v1/figure_01_primary.png)

Eight paper-selected targets, each post-injury library minus its own control,
in log2(CPM+1) units using all-source RNA denominators. Three panels have mostly
positive changes; GSE329778 LGR5 has seven negative targets. These whole-library
descriptions do not isolate ISC/state-specific expression. The two GSE329778
contrasts reuse CTRL. [SVG](../../analysis/research/runs/arz1_rna_description_v1/figure_01_primary.svg) ·
[Exact plotting values](../../analysis/research/runs/arz1_rna_description_v1/selected_target_contrasts.csv).

## Figure 2: weighting and RNA-only QC sensitivity

![Fixed barcode-weighting and RNA-QC sensitivity](../../analysis/research/runs/arz1_rna_description_v1/figure_02_sensitivity.png)

The same targets and contrasts under four fixed cases. Equal-barcode CPM is
averaged before transformation. RNA QC applies the source's RNA thresholds and
an explicit mt- naming convention; it omits ATAC QC. GSE329778 LGR5's panel median
changes from -0.506 to +0.556 under pooled RNA QC, retaining 635/6,921 barcodes.
Selection sensitivity does not identify the true biological direction. These
cases are not independent replicates or uncertainty intervals.
[SVG](../../analysis/research/runs/arz1_rna_description_v1/figure_02_sensitivity.svg) ·
[Panel summaries](../../analysis/research/runs/arz1_rna_description_v1/selected_target_summary.csv).

## Figure 3: paired RNA and fixed-region fragment contrasts

![Four source-selected loci in two paired RNA and fragment contrasts](../../analysis/research/runs/arz1_accessibility_primary_render_v1/figure_01_paired_primary_corrected.png)

Cd74, Tiam1, Cd83 and Ciita were named in the paper's Figure 5d/e before these
outcomes. This adaptation uses the third deposit's GRCm39 reference, matched
positive-depth barcodes and fixed M33 TSS-window unions. It is a direct
paper-linked measurement comparison, not a general cytokine schematic.
Both contrasts reuse CTRL. Fragment overlap and RNA have separate total-depth
denominators; neither measures promoter activity, TF occupancy or memory.
[SVG](../../analysis/research/runs/arz1_accessibility_primary_render_v1/figure_01_paired_primary_corrected.svg) ·
[Exact values](../../analysis/research/runs/arz1_accessibility_description_v2/paired_contrasts.csv).

The primary image uses a [render-only spacing correction](../../analysis/research/runs/arz1_accessibility_primary_render_v1/receipt.json).
All 16 bar values are unchanged. The original v2 primary PNG/SVG and receipt
remain preserved; the correction supersedes presentation only.

## Figure 4: region, selection, weighting and count-definition sensitivity

![All paired measurement sensitivities and separate count-definition deltas](../../analysis/research/runs/arz1_accessibility_description_v2/figure_02_paired_sensitivity.png)

LGR5 Tiam1 has negative TSS-window and positive gene-body contrasts across all
fixed QC/weight cases. RNA selection changes some gene-level signs. The bottom
row uses its own explicit scale to show the coordinate-grouped minus
strand-record contrast: its largest absolute difference is 0.00270523, with no
fragment-contrast sign changes among 64 comparisons. This measures robustness
to two record definitions, not biological equivalence. Sparse Ciita counts need
the [full count context](ACCESSIBILITY_RESULTS.md#primary-descriptive-results).
RNA appears once because changing regions/count definitions reuses its values.
[SVG](../../analysis/research/runs/arz1_accessibility_description_v2/figure_02_paired_sensitivity.svg) ·
[Definition deltas](../../analysis/research/runs/arz1_accessibility_description_v2/count_definition_deltas.csv).
