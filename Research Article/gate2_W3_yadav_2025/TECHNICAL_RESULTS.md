# Yadav functional and RNA technical checkpoint

30 October 2026. Article-local owner **Yd1-P01**; existing Wg-P06 is unchanged.
F1-F5, complete count integrity, conservative annotation and the fixed R1 RNA
descriptions have executed under committed contracts. This is exposed reuse of
published evidence, not independent biological replication or scientific acceptance.

Steps 5-6 are now complete to their source-feasibility boundary; read the
[current spatial/context and synthesis checkpoint](CONTEXT_AND_SYNTHESIS.md) for
the full completion/hold ledger.

Read this result before the [prospective designs](EXECUTION_DESIGN.md),
[annotation strategy](ANNOTATION_STRATEGY.md) and [RNA endpoint design](RNA_ENDPOINT_DESIGN.md).
The [first checkpoint](SOURCE_QUALIFICATION.md) retains exact source/assay locators,
sample-identity limits and discrepancies. [All figures](FIGURES.md) include PNG and PDF.

## Current job ledger

| Job | Executed scope and evidence | Boundary / next dependency |
| --- | --- | --- |
| Q1 / source qualification | Seven source inputs, 34 workbook sheets, six GEO libraries; first checkpoint retained. | Source units are qualified only to the recorded limits. |
| F1 / human PCLS | 3B, 3D, 5A source slice values and differences. | No patient map, inferred triples, patient effects or patient precision. |
| F2 / human coculture | 5D-F and separate 6G, each donor combination shown with all supplied conditions. | 5D D2 stays blank; no well matching or pooled-donor inference. Shared endpoints are dependent; 6G donor overlap is unknown. |
| F3 / mouse lung | 3B and 3E unpaired means and conditional Welch intervals. | Source-animal independence assumed; allocation/batch and pooled control genotypes limit interpretation. |
| F4 / culture specificity and rescue | All S3C-D and 3J arms and fixed contrasts retained. | Source-culture descriptions; alpha-SMA is separate from collagen. Preparation independence is unknown. |
| F5 / metabolites | Both 3K relative abundances. | No tracer, flux, synthesis-rate or absolute concentration inference. |
| Count integrity | Every deposited matrix entry parsed in all six libraries; barcode/feature joins and QC saved. | Technical validity does not establish biological independence. |
| Annotation | Two fixed QC masks; core marker classes plus mixed, other, unassigned and excluded states. | Adapted markers, not author SingleR/DoubletFinder reproduction, validated lineage or pure populations. |
| R1 / coculture RNA | Macrophage-like Arg1 and fibroblast-like Il6, three fixed comparisons, two QC masks. | Library descriptions only; no cell-based population tests, suffix pairing, Compass or CellChat. |
| S1 / spatial | **Completed** source/definition audit and all 18 published marginal values; [current result](CONTEXT_AND_SYNTHESIS.md). | Raw reconstruction remains held on spatial inputs, definitions, patient/field/result joins and exact execution details. |
| C1 / reused contexts | **Completed** seven-context provenance/portability matrix; no new expression scans were needed. | Any stronger numerical comparison requires exact files, capture/units/reuse qualification and a selected prospective design. |
| Wg-P06 / thesis synthesis | **Completed** article-local synthesis; current hypothesis, rival and scientific decisions unchanged. | Joint substrate/routing/functional measurements and the epithelial-regeneration bridge remain unmeasured. |

## Functional source reconstruction

Primary source: [Yadav et al., JCI188734](https://www.jci.org/articles/view/188734),
[official supporting values](https://www.jci.org/articles/view/188734/sd/4) and
[supplement](https://www.jci.org/articles/view/188734/sd/1). Repository estimates
below derive from the frozen source-cell mapping, not an independent cohort.
All 230 source slots are retained: 229 values and the single blank 5D D2.
There are 53 group summaries and 35 prespecified contrasts. Real zeros remain zeros.

The human slice comparisons are lower under blockade in the supplied values, but
missing patient assignments prevent a patient-level estimate. In each documented
human donor combination, 5D-F coculture values exceed fibroblast-alone means and
tocilizumab lowers them. The separate 6G endpoint retains neutrophil-only values
as well as the P2RX4-inhibitor contrast. These endpoint patterns share source
material and do not multiply the number of independent donors.

Mouse lung ornithine differs by -82.05 micromolar (95% Welch interval -115.72 to
-48.38). Hydroxyproline differs by -0.09773 mg/mL (interval -0.23196 to +0.03649);
the interval spans zero. Keep this imprecision visible. The latter estimates a
mean difference with a Welch interval, whereas the paper reports a Mann-Whitney
comparison; this is not a reproduction of its test or evidence of equivalence.
Control animals combine reported Arg1 fl/fl or fl/+ genotypes; allocation, batch
and individual control genotype are unavailable.

The S3C source panel/workbook support coculture rescue, with the conflicting
monoculture wording in the legend retained in the first checkpoint. Ornithine
partly restores the COL1A1 mean after CB-1158 in the supplied cultures. S3D
ornithine-minus-coculture alpha-SMA is +33.33 MFI, which does not establish
equivalence or a universal myofibroblast effect. OAT and genetic arms remain
visible regardless of direction. Fig. 3K records relative proline and
hydroxyproline abundance, not labeled substrate incorporation.

### Every fixed functional contrast

Values are target minus reference means, in the displayed source units. All
non-F3 rows are descriptive differences without population intervals. "Donor"
means the source donor combination, not paired wells.

| Job / panel | Donor combination | Target minus reference | Difference | Unit |
| --- | --- | --- | ---: | --- |
| F1 / 3B_PCLS | source | CB-1158 minus Untreated | -0.893082 | Relative to untreated |
| F1 / 3D | source | CB-1158 minus Untreated | -0.605425 | Relative to untreated |
| F1 / 5A | source | Tocilizumab minus Untreated | -516.834 | ARG1 (pg/mL) |
| F2 / 5D | Donor 1 | Coculture minus Fib alone | +14178 | COL1A1 MFI |
| F2 / 5D | Donor 1 | Tocilizumab minus Coculture | -13881 | COL1A1 MFI |
| F2 / 5D | Donor 2 | Coculture minus Fib alone | +12833.3 | COL1A1 MFI |
| F2 / 5D | Donor 2 | Tocilizumab minus Coculture | -16347 | COL1A1 MFI |
| F2 / 5E | Donor 1 | Coculture minus Fib alone | +344.263 | ARG1 (pg/mL) |
| F2 / 5E | Donor 1 | Tocilizumab minus Coculture | -352.131 | ARG1 (pg/mL) |
| F2 / 5E | Donor 2 | Coculture minus Fib alone | +1275.85 | ARG1 (pg/mL) |
| F2 / 5E | Donor 2 | Tocilizumab minus Coculture | -676.256 | ARG1 (pg/mL) |
| F2 / 5F | Donor 1 | Coculture minus Fib alone | +36.3283 | Ornithine (micromolar) |
| F2 / 5F | Donor 1 | Tocilizumab minus Coculture | -34.8103 | Ornithine (micromolar) |
| F2 / 5F | Donor 2 | Coculture minus Fib alone | +28.4467 | Ornithine (micromolar) |
| F2 / 5F | Donor 2 | Tocilizumab minus Coculture | -27.3731 | Ornithine (micromolar) |
| F2 / 6G | Donor 1 | Coculture minus Fib alone | +573.409 | IL-6 (pg/mL) |
| F2 / 6G | Donor 1 | Coculture minus Neutrophils alone | +809.731 | IL-6 (pg/mL) |
| F2 / 6G | Donor 1 | P2RX4 inhibitor minus Coculture | -379.581 | IL-6 (pg/mL) |
| F2 / 6G | Donor 2 | Coculture minus Fib alone | +658.447 | IL-6 (pg/mL) |
| F2 / 6G | Donor 2 | Coculture minus Neutrophils alone | +921.003 | IL-6 (pg/mL) |
| F2 / 6G | Donor 2 | P2RX4 inhibitor minus Coculture | -415.528 | IL-6 (pg/mL) |
| F3 / 3B_mouse | source | CB-1158 minus Untreated | -82.0464 | Ornithine (micromolar) |
| F3 / 3E | source | Lysm-Cre Arg1 floxed minus Arg1 floxed controls | -0.0977334 | Hydroxyproline (mg/mL) |
| F4 / S3C | source | Co minus Mono | +33234.7 | COL1A1 MFI |
| F4 / S3C | source | Co + CB minus Co | -26267.3 | COL1A1 MFI |
| F4 / S3C | source | Co + CB + ornithine minus Co + CB | +15834 | COL1A1 MFI |
| F4 / S3C | source | Co + OAT inhibitor minus Co | -29600 | COL1A1 MFI |
| F4 / S3D | source | Co minus Mono | +19033.3 | Alpha-SMA MFI |
| F4 / S3D | source | Co + ornithine minus Co | +33.3333 | Alpha-SMA MFI |
| F4 / S3D | source | Co + OAT inhibitor minus Co | -4866.67 | Alpha-SMA MFI |
| F4 / 3J | source | WT Mac coculture minus Fib alone | +13396.3 | COL1A1 MFI |
| F4 / 3J | source | Arg1 KO Mac coculture minus WT Mac coculture | -10133.3 | COL1A1 MFI |
| F4 / 3J | source | KO co + CB-1158 minus Arg1 KO Mac coculture | -466.667 | COL1A1 MFI |
| F5 / 3K_proline | source | CB-1158 minus Untreated | -0.458892 | Relative abundance |
| F5 / 3K_hydroxyproline | source | CB-1158 minus Untreated | -0.765541 | Relative abundance |

Exact observations, group summaries and contrasts are linked by run below.

## Full count integrity and conservative annotation

All six GSE242510 libraries contain 32,285 feature rows and jointly 12,519
deposited barcodes. Full gzip decompression, declared-versus-actual entry counts,
integer/nonnegative values, index bounds, zero/duplicate-coordinate checks,
unique identifiers and joins passed. No stored zero entries or duplicate
coordinates were found. The feature type is protein_coding, not the 10x literal
Gene Expression. Annotation never used Arg1 or Il6.

The primary mask requires 200-10,000 detected genes inclusive and at most 5%
mitochondrial counts. The prespecified broad sensitivity keeps at least 200 genes,
at most 10% mitochondrial counts and no upper gene limit. Both are retained.
Core class rules and held-out marker sets are in the frozen annotation specification;
all 24 library/mask/class combinations met the coverage rule of at least 20 cells
and at least 50% with a held-out marker at two or more counts. This rule provides
technical coverage and broad compatibility, not purity or statistical power.

### Primary-QC composition (all deposited barcodes as denominator)

| GSM suffix / library | Deposited | Fibroblast-like | Macrophage-like | Mixed Fib/Mac | Other/mixed | Unassigned | QC excluded |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 752 / Fib alone 1 | 2081 | 1346 | 82 | 6 | 75 | 570 | 2 |
| 753 / Fib + Mac 1 | 1674 | 825 | 87 | 518 | 88 | 22 | 134 |
| 754 / P2rx4KO Fib + Mac 1 | 2333 | 1004 | 632 | 219 | 267 | 141 | 70 |
| 755 / Fib alone 2 | 1856 | 1446 | 64 | 11 | 117 | 212 | 6 |
| 756 / Fib + Mac 2 | 1984 | 1127 | 410 | 93 | 65 | 280 | 9 |
| 757 / P2rx4KO Fib + Mac 2 | 2591 | 1210 | 556 | 31 | 218 | 549 | 27 |

The fibroblast-only libraries contain 82 and 64 macrophage-compatible cells.
WT coculture 1 has 518 mixed cells and only 87 macrophage-like core cells.
Ambient transcripts, mixed cells, incomplete lineage specificity and culture
selection therefore remain concrete threats. No labels were retuned after
target extraction. Cell-level flags and both composition denominators are saved,
so discarded or ambiguous states remain inspectable.

## R1: library-level transcript descriptions

Primary metric: the library/class average of log1p(counts per 10,000 total cell
counts), including zero target counts. These are normalized RNA summaries, not
protein secretion, enzyme activity or flux. Conditions have two libraries each;
preparation, animal, pooling and suffix-pairing identities remain unknown.

### Primary-QC library summaries

| GSM suffix | Condition | Core class / gene | Cells | Mean log1p per 10,000 | Nonzero fraction |
| --- | --- | --- | ---: | ---: | ---: |
| 752 | Fib_alone | macrophage_Arg1 | 82 | 0.0248 | 0.0488 |
| 752 | Fib_alone | fibroblast_Il6 | 1346 | 0.3711 | 0.5409 |
| 753 | WT_coculture | macrophage_Arg1 | 87 | 0.9999 | 0.5632 |
| 753 | WT_coculture | fibroblast_Il6 | 825 | 0.9404 | 0.9042 |
| 754 | KO_coculture | macrophage_Arg1 | 632 | 0.1799 | 0.1472 |
| 754 | KO_coculture | fibroblast_Il6 | 1004 | 0.7940 | 0.8018 |
| 755 | Fib_alone | macrophage_Arg1 | 64 | 0.1315 | 0.1250 |
| 755 | Fib_alone | fibroblast_Il6 | 1446 | 0.4032 | 0.6355 |
| 756 | WT_coculture | macrophage_Arg1 | 410 | 1.0866 | 0.5268 |
| 756 | WT_coculture | fibroblast_Il6 | 1127 | 0.7099 | 0.6894 |
| 757 | KO_coculture | macrophage_Arg1 | 556 | 0.2500 | 0.1421 |
| 757 | KO_coculture | fibroblast_Il6 | 1210 | 0.7551 | 0.7116 |

The two fibroblast-only macrophage-like summaries are retained as diagnostics;
they were not added as a new condition contrast. Condition means give equal
weight to libraries. Each range below is the minimum and maximum of all four
crossed library differences, never a confidence interval or a paired effect.

| Comparison | QC | Equal-library mean difference | Crossed-library range |
| --- | --- | ---: | --- |
| Arg1_KO_vs_WT | primary | -0.82834 | -0.90670 to -0.74997 |
| Il6_KO_vs_WT | primary | -0.05056 | -0.18521 to +0.08410 |
| Il6_WT_co_vs_alone | primary | +0.43795 | +0.30666 to +0.56924 |
| Arg1_KO_vs_WT | broad | -0.82916 | -0.90617 to -0.75215 |
| Il6_KO_vs_WT | broad | -0.04222 | -0.17224 to +0.08779 |
| Il6_WT_co_vs_alone | broad | +0.43055 | +0.30593 to +0.55516 |

Both KO coculture libraries have lower macrophage-like Arg1 than either WT
coculture library under both masks. Fibroblast-like Il6 is higher in both WT
coculture libraries than either fibroblast-only library. The KO-minus-WT Il6
comparison is heterogeneous: its average is slightly negative but crossed
differences have both signs under both masks. Detection fraction, mean normalized
counts and pseudobulk CPM preserve those respective directional patterns. All
companion estimates and crossed differences are retained in the R1 CSVs.

This describes consistency with selected published transcript comparisons.
Unknown preparation/batch, large composition differences and class selection
prevent an identifiable population genotype effect or a claim that the complete
published signaling circuit has been reproduced.

![R1 fixed RNA descriptions](../../analysis/research/runs/Yd1_rna_endpoints_v1/rna.png)

## Contracts, frozen revisions and receipts

Contracts froze before their dependent numerical execution. Exposure was recorded
honestly: published outcomes and functional values were known before their freeze;
technical QC preceded annotation; annotation/composition preceded local target
extraction. Later freezing does not erase prior exposure.

| Job | Contract | Freeze / execution revision | Immutable output directory and receipt |
| --- | --- | --- | --- |
| F1 | [Contract](config/functional_f1_contract_v1.json) | 920765c7fdca | [Outputs](../../analysis/research/runs/Yd1_functional_f1_v1/) / [receipt](../../analysis/research/runs/Yd1_functional_f1_v1/receipt.json) |
| F2 | [Contract](config/functional_f2_contract_v1.json) | 920765c7fdca | [Outputs](../../analysis/research/runs/Yd1_functional_f2_v1/) / [receipt](../../analysis/research/runs/Yd1_functional_f2_v1/receipt.json) |
| F3 | [Contract](config/functional_f3_contract_v1.json) | 920765c7fdca | [Outputs](../../analysis/research/runs/Yd1_functional_f3_v1/) / [receipt](../../analysis/research/runs/Yd1_functional_f3_v1/receipt.json) |
| F4 | [Contract](config/functional_f4_contract_v1.json) | 920765c7fdca | [Outputs](../../analysis/research/runs/Yd1_functional_f4_v1/) / [receipt](../../analysis/research/runs/Yd1_functional_f4_v1/receipt.json) |
| F5 | [Contract](config/functional_f5_contract_v1.json) | 920765c7fdca | [Outputs](../../analysis/research/runs/Yd1_functional_f5_v1/) / [receipt](../../analysis/research/runs/Yd1_functional_f5_v1/receipt.json) |
| Count integrity | [Contract](config/count_integrity_v1.json) | 8748bf9c34ee | [Outputs](../../analysis/research/runs/Yd1_count_integrity_v1/) / [receipt](../../analysis/research/runs/Yd1_count_integrity_v1/receipt.json) |
| Annotation | [Contract](config/annotation_contract_v1.json) | 4d5b68f60158 | [Outputs](../../analysis/research/runs/Yd1_annotation_v1/) / [receipt](../../analysis/research/runs/Yd1_annotation_v1/receipt.json) |
| R1 RNA | [Contract](config/rna_endpoints_contract_v1.json) | 088e6b2faa34 | [Outputs](../../analysis/research/runs/Yd1_rna_endpoints_v1/) / [receipt](../../analysis/research/runs/Yd1_rna_endpoints_v1/receipt.json) |
| Display v2 | [Contract](config/figure_display_v2.json) | f2e75aafa932 | [Outputs](../../analysis/research/runs/Yd1_figure_display_v2/) / [receipt](../../analysis/research/runs/Yd1_figure_display_v2/receipt.json) |

The display-only v2 run supersedes current links to functional and QC images.
It wraps crowded labels, shows real zero dots fully, removes crowded minor log
tick labels and states a 10% QC color saturation. Original v1 figures, source
tables, contracts and receipts remain unchanged.

## Verification and remaining limits

Independent openpyxl 3.1.5 reads of the original XLSX matched all 230 source
slots, 53 summaries and 35 contrasts. The check recalculated means, sample SD,
extrema, mean differences, F3 standard errors/degrees of freedom and interval
arithmetic. Both F3 t critical values were separately checked against the
incomplete-beta two-tail identity (0.05). Missing D2 and the absence of unsupported
intervals were explicitly checked. This is numerical verification on reused data.

For RNA, a second chunked MatrixMarket reader independently matched all per-cell
totals, detected-gene counts and Arg1/Il6 count vectors in all six libraries.
Scalar Python arithmetic independently matched all 24 library/class/mask summaries.
The [saved verification record](../../analysis/research/runs/Yd1_rna_endpoints_v1/independent_verification.json)
is part of the frozen R1 receipt. A separate table-only check also verified all
24 condition/metric/mask contrasts and 96 crossed differences against the saved
library summaries. Annotation accounting retains all 12,519 barcodes in each mask.

Every current PNG was visually inspected; PNG/PDF pairs share the same rendered
figure. Repository/receipt validation and current integration-base status are
recorded in [PROGRESS](../../PROGRESS.md). Passing these checks establishes
execution/provenance consistency, not biological truth or human acceptance.

No governance, validator, canonical RQ, claim grade or human decision was changed.
The original checkout and review worktree are preserved; no push, PR, merge,
Notion write or external account setting changed. Keep the execution worktree and
ignored raw source cache for review. The selected spatial/context and synthesis work is now recorded in
[the article closeout](CONTEXT_AND_SYNTHESIS.md); stronger jobs reopen only with
the specified evidence or newly selected scope.
