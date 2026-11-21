# S4 · Adenoma size, burden and spatial P20 after colitis

**Recovered mice had a larger fraction of gross adenomas over 1 mm and greater microscopic tissue involvement.** The mean gross lesion count was similar between groups. Each contrast below weights mice equally. The gross and microscopic series used separate induction regimens and harvests. [Original Fig. 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC13083248/#Fig4) · [Mouse-level figures and source values](../FIGURES.md#s4--adenoma-burden-and-spatial-p20)

| Endpoint | Control mean | Recovered mean | Recovered − control | Range omitting one mouse |
|---|---:|---:|---:|---:|
| Gross adenomas per mouse (4 / 5 mice) | 25.0 | 24.4 | −0.6 | −3.25 to +3.73 |
| Gross adenomas >1 mm, within-mouse fraction | 31.69% | 59.07% | +27.38 points | +18.82 to +31.49 |
| Microscopic lesions counted per mouse (7 / 10 mice) | 11.57 | 24.10 | +12.53 | +9.87 to +14.43 |
| Microscopic tumour area / assessed tissue area | 0.183% | 0.486% | +0.303 points | +0.258 to +0.357 |

The nine exact Fig. 4c/ED9d mouse-label joins imply 34 large lesions among 100 control lesions and 70 among 122 recovered lesions. Independent counting of ED9a diameter rows gives those same totals from the same animals. For ED9h, the worksheet supplies raw microscopic counts and the tumour area fraction. Recreating **lesions per unit tissue area** requires each mouse’s assessed tissue area. Pooling the lesion areas cannot recover those denominators without a lesion-to-mouse key. [Joined gross mouse rows](../../../analysis/research/runs/ng26_s4_v1/gross_mice.tsv) · [Microscopic mouse rows](../../../analysis/research/runs/ng26_s4_v1/microscopic_mice.tsv) · [Mouse contrasts](../../../analysis/research/runs/ng26_s4_v1/mouse_contrasts.tsv)

| Lesion areas | Control | Recovered |
|---|---|---|
| **Fig. 4e** | Median **2,847 µm²**, 81 rows (legend 88) | Median **5,111 µm²**, 241 rows (legend 256) |
| **Fig. 4l, vehicle** | Median 1,613 µm², 42 rows (legend 48) | Median 4,988 µm², 88 rows (legend 95) |
| **Fig. 4l, T-5224** | Median 2,543 µm², 38 rows (legend 43) | Median 3,012 µm², 156 rows (legend 163) |

The released Fig. 4e areas reproduce both printed medians. Their counts also equal the sums in the mouse worksheet. Which areas belong to individual mice remains unknown. The Fig. 4l legend gives 6/5 control and 7/7 recovered vehicle/drug mice. The four released area distributions have history and treatment labels only. A mouse-level interaction needs each animal’s lesion assignments or an arm-labelled per-mouse outcome. The area table’s strict 20,000 µm² exceedances concern the plot’s display ceiling; the original Fig. 4e high-tail annotation uses a lower dashed line. [All lesion measurements](../../../analysis/research/runs/ng26_s4_v1/lesion_measurements.tsv) · [Counts, quartiles and tails](../../../analysis/research/runs/ng26_s4_v1/lesion_distributions.tsv) · [Original source workbook](https://pmc-oa-opendata.s3.amazonaws.com/PMC13083248.1/41586_2026_10258_MOESM9_ESM.xlsx)

**Fig. 4j measures a separate RNA endpoint.** The vector plot has 117 control and 137 recovered lesion symbols. Median P20 scores read from the axis were approximately −0.34 and +1.00. Scores exceeded 3 in **2/117 (1.7%)** and **12/137 (8.8%)**, exactly recovering the printed fractions to rounding. No point was within .05 of the threshold. The published P = 1.01×10⁻⁹ compares lesions. GSE316618 lists counts, barcodes, features, positions and images for one control section (GSM9456973, 13-B/A1) and one recovered section (GSM9456974, 7-B/D1). Its supplementary inventory lacks the original bin-to-lesion calls and per-lesion P20 table. Plot coordinates identify neither the lesion nor its contributing bins. The two sections cannot distinguish specimen from history. [Plot-derived values](../../../analysis/research/runs/ng26_s4_v1/p20_plotted_points.tsv) · [Spatial source inventory](../../../analysis/research/runs/ng26_s4_v1/spatial_file_inventory.tsv) · [GSE316618](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316618) · [Authors’ lesion-calling code](https://github.com/snagaraja13/colitis_memory/blob/v1.0.1/5_Spatial_RNA/03_spatial.call_tumors.R)

S4 supports larger lesions and greater area burden **at collection**. A single harvest does not identify initiation frequency, incidence over time or individual growth rates. The organoid clone, methylation, spatial RNA and lesion-size records lack the serial lineage and matched measurements needed to test chromatin-to-growth mediation. S4 stops for review. [Frozen comparison](../../../analysis/research/contracts/Ng26-P01.s4_v1.json) · [Execution receipt](../../../analysis/research/runs/ng26_s4_v1/receipt.json)
