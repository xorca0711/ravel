# Reconciliation of the context notes with source evidence

The supplied Notion Result(Body) text was read on 2 October 2026. Its wording
is treated as the owner's reading context, not as verified gene nomenclature
or a numerical specification. Private snapshots remain in ignored storage;
the Notion page itself was not changed. Source locators below refer to the
[paper](https://doi.org/10.1038/s41586-020-2922-4) and downloaded workbooks.

| Note topic | Source check | Consequence |
|---|---|---|
| Differentiating basal cells: reduced HES1/KRT7/SCGB3A2 | Main text, New lung cell types: reduced **KRT5**, increased **HES1, KRT7, SCGB3A2** | Correct the sign before making a panel |
| AT2 signaling: CTNNBIP | Main text uses CTNNBIP; pinned SS2 notebook and Table 4 Cluster 15 (SS) use **CTNNBIP1** | Preserve original text and map to the measured symbol explicitly |
| Alveolar fibroblast SPIMT2 | Main text and Table 4 Cluster 30 use **SPINT2** | Correct transcription; retain FGFR4/GPC3 context |
| Complement CF1; glutamate receptor GRIA | Main text uses **CFI** and **GRIA1**; Table 4 supports GRIA1 | Avoid silent misspelled-gene dropouts |
| CX3CR1 ligand CD3CL1 | ED6 chemokine context uses **CX3CL1** | Record symbol correction before any future compatibility analysis |
| AT2-s is about tenfold rarer | Fig. 1d image source: 20 of 203 scored SFTPC-positive cells; sequencing Table 2 has 870 AT2-s and 4,574 AT2 | Distinct denominators; do not force a 10% sequencing target or natural prevalence estimate |
| Human AT2-s as a mouse stem-cell homolog | Paper explicitly calls homology provisional | Keep as a candidate correspondence, not a stemness annotation |
| MYRF and TBX5 as master regulators | Selective RNA and localization evidence; functional regulatory roles are proposed | Stage a donor-aware specificity question before causal interpretation |
| Fibroblast excitability and immune recruitment | Inferred from expressed machinery | Functional hypotheses, not measurements of excitation or recruitment |
| Residency signature | Tissue-associated patterns compared with a prior signature | Tissue association alone cannot prove stable residence or exclude transient recruitment |
| Disease-gene expression reveals origin | Expression localizes candidates; disease initiation is not tested by this atlas | Do not infer causality from localization |

## Source inconsistencies to retain

- Supplementary Table 2's last-row, per-donor, and 58-population totals are not
  mutually consistent. Keep both deposited and recomputed totals; do not repair
  source cells silently or infer which individual cells account for the mismatch.
- Table 7 worksheets declare a one-cell used range despite containing many
  rows/columns. The intake reader resets dimensions and counts actual rows.
- Publisher descriptions for Tables 5 and 7 use greater-than p-value notation
  where the surrounding text describes significance. Table 5's actual sheet is
  `significant_means`, not a full p-value table. These captions are not an
  executable threshold contract; reconcile source code and complete outputs
  before reproducing significance filtering.
- One SS2 marker sheet is named `Cluster 15 (SS)` rather than `(SS2)`.
  The manifest/schema preserves that label. A parser must not silently omit it.
