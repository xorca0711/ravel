# Nb2 bulk v1: source directions, direct contrasts and uncertainty

Executed 29 September 2026 from all 18 GSE208770 count files. This is an **adapted
assay reproduction**, followed by exploratory component analysis. It does not
reproduce an independent animal-level experiment: the paper's three biological
replicates per condition are described as animals **or** independent cultures,
and all 18 BioSample records leave preparation identities and pairing unresolved.
Model intervals and p-values below are conditional on independent libraries.

## What was recovered

The input has 52,636 Ensembl gene rows. Schema checks establish nonnegative integer
counts, identical gene order/width across libraries, and 18 matching accessions.
The frozen count filter retains **16,534 genes**. TMM–voom and unpaired limma fit
six conditions, ten contrasts, rank six and 12 residual degrees of freedom.
The source's internal annotation/normalization pipeline was not available; this
implementation is explicitly different. See [contract](contract.json),
[run record](run_complete.json), [schema audit](../../metadata/bulk_schema_audit.json)
and [sample metadata](../../metadata/samples.tsv).

Nineteen of twenty Figure 4D names map to Ensembl GRCm38 release 102. Cyr61 maps to
Ccn1, Ctgf to Ccn2, and Cenpc to Cenpc1. **Crim2 is printed in the supplied figure
but remains unresolved**; Crim1 was not substituted. The three-gene Hippo-associated
summary is an adaptation, not a complete reconstruction of the source panel.

## Source transcriptional directions

Per-library panel means support the source's broad direction: agonists increase
Wnt, proliferation and AT2-associated RNA relative to 48-hour withdrawal. The
mean AT1 panel decreases, more strongly for Fzd6 than Fzd5. These summaries do
not establish that individual cells maintain AT2 identity while gaining AT1 competence.

| Treatment minus 48-hour withdrawal | Wnt | Proliferation | AT2 | AT1 | Hippo-associated, 3 genes |
|---|---:|---:|---:|---:|---:|
| CHIR | +3.417 | +0.713 | +1.113 | −2.936 | −1.234 |
| Fzd5 agonist | +2.724 | +1.065 | +1.551 | −0.383 | +0.636 |
| Fzd6 agonist | +2.619 | +0.594 | +1.810 | −1.348 | +0.079 |

Values are differences of arithmetic means of library-level mean log2CPM across
the indicated genes, not fold changes in a measured biological function. All
library points and source gene dots are displayed [separately](figures/01_source_panels.png).
The Birc5-excluded Wnt sensitivity retains positive agonist–withdrawal differences
(Fzd5 +3.258; Fzd6 +3.259), so the panel direction is not supplied solely by this
proliferation-associated member. See [panel effects](tables/panel_effects.tsv) and
[specificity sensitivity](tables/wnt_specificity_sensitivity.tsv).

## The most useful direct comparison

The three resolved Hippo-associated genes give a Fzd5–CHIR panel difference of
**+1.870 mean log2CPM**. All nine cross-arm library differences are positive
(range +1.156 to +2.608). Fzd6–CHIR is +1.313, with mixed library differences
(−0.262 to +2.528). The nine pairwise differences are a descriptive range, **not
nine independent replicates**.

Gene-level Ccn1, Ccn2 and Amotl2 effects are positive in both contrasts, but none
has genome-wide BH FDR <0.05. Source-nominated Tgfb2 and Zbtb16 likewise do not pass
that threshold. The appropriate lead is a coherent, source-exposed transcriptional
component with uncertain population precision, not newly validated Hippo activity.
The [direct-effect plot](figures/03_direct_effects.png) includes gene-wise conditional
intervals; the [full gene table](tables/gene_effects.tsv.gz) retains both per-contrast
and pooled-ten-contrast BH values.

No genes meet per-contrast FDR <0.05 in Fzd6–Fzd5; this agrees with the source's
absence of detected differences under one analysis route. It **does not demonstrate
equivalence**. The interval for the Axin2 difference, for example, spans about
−2.76 to +1.06 log2FC. No useful-effect equivalence margin was justified in advance.

## A meaningful exploratory finding is sensitivity to gene correlation

CAMERA tests 3,640 expressed GO BP/Hallmark sets using an expressed, unique-symbol
background and a prespecified correlation of 0.01. Mitochondrial and ribosome-related
sets rank prominently in receptor–CHIR contrasts. However, the prespecified Hallmark
sensitivity estimates substantial residual correlation for oxidative phosphorylation
(about 0.282). Its per-contrast Hallmark FDR becomes **0.494** for Fzd5–CHIR,
**0.443** for Fzd6–CHIR and **0.708** for Fzd6–Fzd5. Thus the apparent metabolic
separation is **not robust to the correlation assumption**.

MYC targets V2 remains lower in both receptor–CHIR contrasts in the estimated-
correlation sensitivity (50-Hallmark-family FDR 0.016 and 0.026). This is a
conditional exploratory RNA association; it could reflect activation strength,
growth or library composition. It does not isolate a receptor-specific fate program.
The [sensitivity plot](figures/04_enrichment_sensitivity.png) recalculates the fixed-
correlation BH values over the same 50-set Hallmark family for a fair visual
comparison. The original [all-set output](tables/camera_all_sets.tsv.gz) is preserved.
This display-only multiplicity harmonization was added after inspecting the run;
it does not change the frozen statistical outputs.

## Why exact reproduction remains open

PCA identifies marked separation of GSM6369139 (24-hour withdrawal), and a second
direction involving GSM6369143 (CHIR) and GSM6369144 (Fzd6). No sample was removed.
The [PCA](figures/02_bulk_pca.png) is a flag for preparation/quality investigation,
not evidence that any library is technically invalid. The top two components
explain 49.96% and 17.32% of variation in the selected 2,000-gene QC matrix.

At FDR <0.05 and absolute log2FC >2, the adapted fit yields CHIR 30 up/81 down,
Fzd5 0/0 and Fzd6 2/1 against 48-hour withdrawal. The paper's stated DEG totals
are therefore **not numerically reproduced**. The [threshold reconciliation](tables/threshold_reconciliation.tsv)
also preserves >1 log2FC, raw p<0.001 and adjusted p<0.001 settings separately.
No setting or sample filter was chosen to force agreement. Recovering source
normalization, preparation identities and timing is the next decision-changing
step; adding a guessed batch or pairing term would not resolve these gaps.

## Implication for the owner's questions

Nb2-N2 has a concrete transcriptional premise for an independently replicated,
state/function-linked follow-up. Its rivals remain mechanical/culture stress,
activation amplitude and cell mixture. Nb2-N1 still cannot be tested as a dosing-
schedule hypothesis: these six deposited conditions are neither a repeated-pulse
experiment nor a later maturation readout. The RNA data also cannot resolve
compensation after verified Fzd5 deletion (Nb2-N4) or endogenous Fzd6 engagement
(Nb2-N8). No A-series question or claim grade is promoted.

## Reproduction notes

Preparation: `01_prepare_bulk.py`; freeze: `02_freeze_bulk.py`; fitting:
`03_bulk.R`; figures: `05_figures.py --section bulk`. Their implementation and
replay commands are in [the execution guide](../../EXECUTION.md). R 4.6.1,
limma 3.68.5, edgeR 4.10.5 and jsonlite 2.0.0 were used. The first launch stopped
before fitting because jsonlite was absent; it was installed into the ignored
run-local runtime and the unchanged frozen script resumed. No statistical
contract changed during that recovery.
