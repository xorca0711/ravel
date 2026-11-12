# Wang 2018 execution amendment v1

12 November 2026, after S1 and before viewing new count contrasts. The owner
authorized the technical run. S1 supports nine deposited libraries and a
mixed-allele control, with unknown mouse/pool and block relationships.

- S2 uses an adapted finite-library contrast. Primary is four deficient
  libraries minus all five deposited controls. Repeat with four verified +/+
  controls. Report all stable IDs, counts, mapping status and low-count rows.
  Rank only genes with counts of at least 10 in four or more libraries, with
  Ensembl 78 mapping when a gene symbol is needed. Median-ratio factors use
  genes positive in every library. The primary contrast is the log2 ratio of
  group arithmetic means after adding 0.5 normalized reads to both means.
  Capture per-library values for all seven published S3C targets plus
  Foxp3 and Ezh2. Allele-restricted comparison keeps the primary factors and
  eligible universe fixed. PCA uses log2(normalized reads + 1) across the
  rank-eligible genes, with no exclusion based on separation.
- S3 uses all mouse Hallmarks in MSigDB 2025.1.Mm, which supplies a versioned
  mouse-native mapping for the adapted analysis. It evaluates the TNF and
  inflammatory claims and profiles the full collection, including cell-cycle,
  apoptosis and stress patterns relevant to culture selection. Use unique
  exact gene-symbol matches from the deposited count universe and report set
  coverage and missing members. The primary ranking is the S2 log2 mean
  ratio; the sensitivity is the difference of group means on the
  log2(normalized reads + 1) scale. Use a weighted running-sum score with
  stable ID tie-breaks, coverage floor of 10 matched genes and leading-edge
  membership. No permutation probabilities or population intervals.
- Sensitivities keep the primary universe fixed. Use counts-per-million
  rescaled to the geometric mean library total as a normalization comparison.
  Drop one deposited library at a time with size factors fixed and report
  the effect and set score ranges as leverage diagnostics. This does not
  treat each dropped library as a verified independent biological unit.
- S4 and S5 remain conditional on the measured S2–S3 results. The separately
  published human tissue contrasts and tumor functional assays require
  different source material and biological units.

Exact S3B–C replay and independent-unit DE inference are held. The released
comparison can quantify deposited RNA patterns and their leverage. Changes in
transcript abundance cannot distinguish surviving state mixture from within-cell
regulation or supply a tumor, cytokine-protein, lineage or functional effect.
