# IL-22 priming extension: source screen completed

8 November 2026. Sx22-P01. [Prospective plan](PLAN.md) ·
[technical overview](../../../docs/research_reviews/2026-11-08-saxton-reading/EXTENSION_EXECUTION.md).

The bounded public-source screen is complete. **No inspected source qualifies
for a B3-versus-WT × IFNα-priming interaction in a defined epithelial population.**
Numerical interaction estimation and laboratory execution remain held; this is
not evidence that such data cannot exist elsewhere or that the question is novel.

The [frozen v2 screen](../../../analysis/research/runs/sx22_priming_qualification_v2/screen.json)
retains all 16 distinct returned GSE records (15 broad-query records and one
exact-B3 record), including related SuperSeries/subseries. These are not 16
independent experiments. Full candidate identities, sample titles and dispositions
are in [source_candidates.csv](../../../analysis/research/runs/sx22_priming_qualification_v2/source_candidates.csv).
The [receipt](../../../analysis/research/runs/sx22_priming_qualification_v2/receipt.json)
records execution at `4fb14dd` after the byte-preservation correction.

| Closest source | Actual inspected design | Missing comparison |
|---|---|---|
| [GSE160217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160217) | Existing Saxton acute bulk-colon PBS/WT/B3 source | IFN priming and a defined epithelial preparation |
| [GSE307526](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307526) and related records | Full SOFT: Ccd18-Co colon fibroblasts, separate cytokine exposures | Epithelial B3 and crossed priming arms; fibroblasts are not epithelium |
| [GSE89610](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE89610) | Full SOFT: Huh7.5 cytokine/time microarrays with separate IFNα/IL-22 labels; generic protocol text conflicts with some labels | B3 and verified sequential/crossed priming design |
| [GSE214633](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214633) | Full SOFT: cytokine-injected mouse PBMC atlas with pooled/hashtag libraries | Epithelial cells, B3 and the proposed interaction; joined cytokine library names do not establish co-treatment |

Other retained hits concern infection, lupus T-cell/AHR/JUN studies, influenza
memory T cells, chicken lungs or psoriasis. The searched records do not contain
the required tuple. Actual translated queries, counts and warnings are saved in
the screen; no date filter or unreported truncation was used.

**IFN priming of IL-22 responses was already specified by Bachmann et al.
(2013; online 2012)** ([primary abstract](https://pubmed.ncbi.nlm.nih.gov/23153456/)).
This is a published premise. Full methods remain inaccessible in this pass,
so priming dose and schedule are not copied from an abstract or invented.
Saxton's engineered B3-versus-WT boundary is the proposed extension, not generic
priming. **Cineus/Luo et al. (2025)** already specifies the epithelial
IL-22/STAT3–OSMR inflammatory connection ([primary paper](https://doi.org/10.1038/s41590-025-02149-z));
it does not establish that connection under B3.

The [completed acute Osmr result](../osmr_v1/RESULTS.md) remains unfavorable for
retained B3 induction. It is not rescued by a broader keyword screen or an
unmeasured chronic-memory claim. The next informative work is the plan's matched
unprimed/primed × PBS/WT/B3 comparison, with separate calibrated pSTAT1/pSTAT3
measurements and a specified downstream protein response. Barrier protection
requires a separately qualified functional assay. Source/model availability,
ligand compatibility, exact schedule and precision remain open before bench work.
