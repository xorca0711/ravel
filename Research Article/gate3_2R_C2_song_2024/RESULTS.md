# Song C2 revised analysis

The 18-hour young activation assay favored a cycling contribution to lower recovered HSC numbers after Cd38 loss. MCU knockdown nearly removed the Rhod-2 genotype contrast, with mixed downstream responses. Competitive donor output reversed direction between the published young and old cohorts. The aged NAD+ and stress readouts support a different metabolic context, while the HSC-specific mediator remains unresolved.

## S0 · Sources, units and eligibility

| Context | Assay and biological unit | Eligibility |
|---|---|---|
| Fresh young, 3 months | ED 1b–e uses marrow LSK (Lin− c-Kit+ Sca-1+) and highly enriched LSK CD150+ CD48− counts plus flow cycling and viability. ED 4 uses enriched HSCs and fluorescent readouts. Mouse or independent preparation is the relevant unit. | Workbook rows support descriptive contrasts. Preparation IDs and linkage across assays remain unresolved. |
| Stimulated young, 3 months | Fig. 1a–c measures recovered enriched HSCs after cytokines, with an 18 h BrdU pulse. Fig. 2d–l measures metabolites, ATP and flow signals. ED 7 uses cytokines and 48 h of control or MCU shRNA. Assay preparations or independent pools are the relevant units. | Descriptive contrasts and four-arm difference of differences. No preparation crosswalk or covariance estimate. |
| RNA | Twelve GEO libraries, two per genotype within fresh young, 24 h stimulated young and fresh old. 35,976 shared gene symbols. Library manifest includes compressed file SHA-256, detected genes and totals. GEO says 2 months for young mice and 24 months for old mice. Fig. 2 says 3 months for young mice. | Library description. No individual or pool independence, fresh/stimulated pairing, exact young age match or sample-specific sex established. Old-stimulated comparisons held. |
| Competitive transplants | C57BL/6 Cd38 WT/KO donor cohorts at 3 and 24 months. General protocol uses 250 sorted CD45.2 donor HSCs and 500,000 CD45.1 competitor marrow cells in B6.SJL recipients. Outcome is peripheral-blood donor percentage by flow at week 16. Marrow engraftment, lineage and young whole-marrow homing at 16 h have separate denominators. | Recipient-row summaries within each age. Donor pooling, batch, sample-specific sex, exact event denominator and shared donor material remain unresolved. Formal age interaction held. |
| Aged genetics and inhibitor | 24-month-old Cd38 WT/KO animals and a distinct 24-month-old WT vehicle/78c cohort treated systemically for eight weeks. Enriched-HSC relative NAD+ and dye assays, blood counts, marrow gating and whole-marrow colony assays sample different outcomes. | Descriptive within-experiment contrasts. No aged inhibitor-to-donor output linkage or NAD+ mediation. |

The paper primarily characterized females. Assay and donor identities cannot be inferred from matching row numbers. Source cells include labeled observations and separate computed averages/SEMs. Normalized values share control denominators. Source versions, plan blobs and routes are recorded in [source provenance](SOURCE_PROVENANCE.md).

## S1 · Young activation

Cd38 KO minus WT after cytokines was **−3.29** in source-reported recovered HSC count units (7.76 vs 11.05), **−5.09 percentage points** BrdU+ (8.32% vs 13.42%) and **+0.30 points** 7-AAD+ (4.74% vs 4.44%). The 7-AAD leave-one-row range was −0.11 to +0.87 points. The Fig. 1b workbook calculated-summary label says “BrdU MFI,” while the observation header and plotted axis designate percentage BrdU+. Fresh highly enriched HSC number differed by +0.03 source units. Quiet baseline assays and the single viability time point leave small effects and other survival intervals open.

On the control-normalized scale, stimulated Fluo-4, Rhod-2, TMRM and ROS were lower by 0.208, 0.157, 0.173 and 0.196 AU. Total succinate and fumarate were lower by 0.189 and 0.235 AU, [U-¹³C]glucose-derived labeled malate and fumarate by 0.210 and 0.442 AU, and ATP by 0.142 AU. Relative LC–MS abundance and fluorescent signals constrain the activation model at measured endpoints. These measurements do not yield respiratory flux or calcium concentration. [Activation figure](../../analysis/research/runs/song24_c2_S1_v2/activation.png)

## S2 · Which genotype differences change under MCU knockdown?

| ED 7 endpoint | KO − WT, control | KO − WT, MCU shRNA | Difference of contrasts | Leave-one-row range for difference |
|---|---:|---:|---:|---:|
| Rhod-2, normalized AU | −0.261 | +0.002 | +0.263 | +0.202 to +0.328 |
| TMRM, normalized AU | −0.183 | +0.116 | +0.299 | +0.252 to +0.348 |
| Recovered HSC number, source units | −1.865 | −0.589 | +1.277 | +0.756 to +1.652 |
| Colonies | −14.667 | −7.000 | +7.667 | +3.500 to +15.500 |

These ranges measure row influence. Each arm has three observations except KO/control TMRM, which has two and a blank despite the legend's n=3. Pairing and preparation allocation remain unresolved, so an interaction confidence interval was held. Rhod-2 converged as WT signal fell under shRNA. TMRM reversed because WT fell and KO changed little. Cell recovery retained a smaller deficit. Colony output retained a negative KO estimate and its within-shRNA leave-one-row range crosses zero. With smaller signals in the WT knockdown arm and few observations, dynamic range and a possible floor remain alternative explanations. Genetic MCU loss in separate 3-month stimulated cells shifted BrdU by −3.93 points and 7-AAD by +1.24 points, with lower Rhod-2, TMRM and ROS. The 7-month MCU resting experiment had different donor ages and supports only its own resting comparison.

## S3 · RNA and functional agreement

The 12 libraries passed exact feature-symbol matching and duplicate checks. 11,610 symbols passed the filter of at least 10 counts in at least two libraries. Log₂(CPM + 0.5) yielded direction matches to published Supplementary Table 1 among genes with absolute published log₂ fold change of at least 0.5 (481/481 young stimulated, 2,921/2,926 young fresh and 2,074/2,076 old fresh, excluding zero reconstructed contrasts). The RNA table includes every library and all five descriptive contrasts. Count-model inference and new BH-adjusted claims are held pending donor/pool independence.

Mouse MSigDB Hallmark v2025.1 is a named adaptation of the published GSEA. E2F and G2M median gene contrasts were −0.125 and −0.120 log₂ in stimulated young cells and remained negative after each single-library omission. Their stimulated minus fresh medians were −0.095 and −0.122, with omission ranges crossing zero. This supports qualitative agreement with BrdU while leaving an activation-specific RNA interaction uncertain. Oxidative phosphorylation was close to zero (+0.009, median rank percentile 0.473) and its omission range crossed zero, despite lower directly measured calcium-related, potential and metabolic readouts. The earlier mitochondrial-encoded symbol adaptation had zero tested coverage and remains recorded. Hallmark membership and missing genes are explicit in the output. [Mouse MSigDB release](https://www.gsea-msigdb.org/gsea/msigdb/mouse/collections.jsp)

Old fresh cells showed positive E2F (+0.380) and G2M (+0.377) medians and negative cytosolic ribosomal-symbol median (−0.319). Oxidative phosphorylation (+0.131) was omission-sensitive. The ED 9h Ki-67 contrast was +3.39 percentage points, with the paper reporting a weak comparison (one-sided P=0.1974). The old-cell RNA could reflect representation of cycling progenitors in the enriched gate. The ribosomal result is expression evidence and leaves protein synthesis rates unresolved.

## S4 · Week-16 donor contribution

| Experiment | WT mean | KO mean | KO − WT | Leave-one-recipient-row range |
|---|---:|---:|---:|---:|
| Cd38, 3-month donors, Fig. 1f (11 WT, 12 KO) | 46.78% | 16.01% | **−30.77 points** | −37.04 to −27.94 |
| Cd38, 24-month donors, Fig. 3g (13 WT, 15 KO) | 7.48% | 18.91% | **+11.43 points** | +8.56 to +13.14 |
| MCU, 7-month donors, ED 6b | 44.55% | 22.54% | −22.01 points | −24.87 to −19.19 |
| MCU, 24-month donors, ED 10d | 14.69% | 28.00% | +13.31 points | +11.15 to +14.95 |

The Cd38 point contrasts differ by **42.20 percentage points** across cohorts. Fig. 3g's legend says 12 WT and 14 KO, but cells Q107 and R107 average 13 WT and 15 KO at week 16. WT13 and KO15 have missing earlier time points. Excluding those two rows as a sensitivity check gives +11.02 points. Unlinked donor and recipient allocations prevent a formal age interaction. The matching MCU directions support a similar context boundary within those experiments, with 7-month donors in the younger MCU transplant rather than the 3-month Cd38 cohort.

KO marrow engraftment shifted −36.67 points young and +25.24 points old. KO donor lymphoid share differed by −5.99 points young and +15.64 points old, separate from total donor output. Young homing shifted −0.22 points under the tested 16 h assay (published one-sided P=0.2659). Old homing remains unmeasured in these comparisons.

## S5 · Aged NAD+, stress and systemic 78c

Fig. 3a measured +0.167 AU relative NAD+ in old Cd38 KO enriched HSCs. ED 9c–g showed lower TMRM, ROS, Hsp60 expression, 7-AAD and activated caspase-1 readouts. In the distinct 78c-versus-vehicle cohort, Fig. 4b gave +0.230 AU relative NAD+. PB lymphoid share increased 10.95 points, marrow lineage-balanced HSC share increased 27.35 points and whole-marrow colonies increased by 27.48. TMRM and ROS were lower by 0.410 and 0.361 AU. The workbook's “TMEM” label for ED 9c and “colonies” summary headers for Fig. 4n–o were interpreted using the matching figure legends and primary observation headers.

These parallel effects support responsiveness to systemic inhibition and are consistent with lower stress-sensitive signals in old genetic loss. A blood composition shift, a marrow phenotype gate and a colony assay each measure different things. The inhibitor experiment does not provide a matched long-term competitive-transplant outcome or isolate CD38 inhibition within HSCs.

## S6 · Where the mechanism remains open

Camacho-Pereira et al. Fig. 5B–F separated liver mitochondrial NAD+ from SIRT3-dependent mitochondrial function using CD38/SIRT3 genetics. That experiment gives a precedent for testing whether the elevated NAD+ and lower stress seen in old Song HSCs require SIRT3 to improve donor output. The missing bridge to Mu’s HSC training and myeloid transfer findings is an HSC-specific CD38–SIRT3 comparison linked to downstream cell function. Song’s donor and systemic treatment assays do not supply it. [Camacho-Pereira et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4911708/)

Dellorusso et al. Figs. 3–5 and 6–7 connected inflammatory signaling, autophagy-stratified old HSCs, glycolytic measures and regeneration. Song’s fresh aged RNA showed a cycle/ribosomal pattern and an unstable oxidative phosphorylation signal. That pattern did not establish a coherent old metabolic stress or compensation program to match to the Dellorusso autophagy contrast, so the external count comparison closed at contextual reading. Totani et al. Fig. 1 and the subsequent metabolic comparisons show that high mitochondrial mass can coexist with regenerative capacity in a defined old HSC subset. That boundary reinforces the distinction between lower TMRM or ROS signal in Song and restoration of self-renewal. [Dellorusso et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11350610/) · [Totani et al.](https://doi.org/10.1038/s43587-025-00828-y)

## Run records and verification

| Stage | Verified receipt | Values and other outputs |
|---|---|---|
| S0 | [Receipt](../../analysis/research/runs/song24_c2_S0_v2/receipt.json) | [GSM manifest](../../analysis/research/runs/song24_c2_S0_v2/libraries.csv) |
| S1 | [Receipt](../../analysis/research/runs/song24_c2_S1_v2/receipt.json) | [Cells](../../analysis/research/runs/song24_c2_S1_v2/observations.csv) · [Contrasts](../../analysis/research/runs/song24_c2_S1_v2/contrasts.csv) |
| S2 | [Receipt](../../analysis/research/runs/song24_c2_S2_v2/receipt.json) | [Cells](../../analysis/research/runs/song24_c2_S2_v2/observations.csv) · [Contrasts](../../analysis/research/runs/song24_c2_S2_v2/contrasts.csv) |
| S3 | [Receipt](../../analysis/research/runs/song24_c2_S3_v2/receipt.json) · [Hallmark receipt](../../analysis/research/runs/song24_c2_S3_hallmark_v1/receipt.json) | [Library contrasts](../../analysis/research/runs/song24_c2_S3_v2/expression.csv) · [Sign checks](../../analysis/research/runs/song24_c2_S3_v2/rna_summary.json) · [Hallmark membership and sensitivity](../../analysis/research/runs/song24_c2_S3_hallmark_v1/hallmark.json) |
| S4 | [Receipt](../../analysis/research/runs/song24_c2_S4_v2/receipt.json) | [Cells](../../analysis/research/runs/song24_c2_S4_v2/observations.csv) · [Contrasts](../../analysis/research/runs/song24_c2_S4_v2/contrasts.csv) |
| S5 | [Receipt](../../analysis/research/runs/song24_c2_S5_v2/receipt.json) | [Cells](../../analysis/research/runs/song24_c2_S5_v2/observations.csv) · [Contrasts](../../analysis/research/runs/song24_c2_S5_v2/contrasts.csv) |

Independent same-source checks matched Fig. 1a–c against workbook means in E:F rows 4, 20 and 36, all four ED 7 interactions against J:M rows 4 and 20 and E:H rows 36 and 52, Fig. 1f/3g against Q:R rows 93/107, and Fig. 3a/4b against H:I row 4. The Hallmark run independently recalculated expression contrast columns from library values for the covered symbols. These checks establish numerical agreement. The initial syntax failure occurred before data processing and is retained in the [v1 logs](FAILED_RUNS_V1.md) with the superseded contracts.

Repository research-gate and validation, claim bindings, and 208 unit tests passed. The repository-wide compile check still reports the original syntax error in the immutable v1 script. Both executed entrypoints parse successfully. The archived failure blocks a green full compile check on this branch.
