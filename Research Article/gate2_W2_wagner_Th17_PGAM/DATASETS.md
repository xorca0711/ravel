# Input deposits, units and unresolved joins

**Current execution and interpretation — 7 October 2026:** see [corrections](CORRECTIONS_2026-10-07.md) and [the current README](README.md). Dated stage plans, intake states and derivation counts below remain historical. A28–A30 are now registered; the full portfolio is A0–A30.

Retrieved and verified on **4 October 2026 (Asia/Seoul)** from NCBI GEO. Every
count below was read from the deposited records and file headers by
[scripts/qualify_sources_v1.py](scripts/qualify_sources_v1.py) in a dry run
outside the governed runner; see [Validation](VALIDATION.md#dry-run-outside-the-runner).
File-level URLs, bytes and SHA-256 values are in the
[source manifest](SOURCE_MANIFEST.md).

| Deposit | Role in this package | Verified inventory |
|---|---|---|
| [GSE289733](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289733) | Fig. 3 and Fig. 2E single-cell source | 8 sample records; 2 animal labels (Mo1, Mo2) × Th17n/Th17p × 1 mM/25 mM; one series-level aggregated matrix of 19,203 barcodes (all unique) × 31,053 Gene Expression features; CellRanger 3.1.0, mm10, `cellranger aggr`; **0 per-sample matrices** |
| [GSE290297](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290297) | Fig. 2 bulk source | 79 sample records joining one-to-one to 79 matrix columns of `GSE290297_collected_inhibitors_tpm_4geo.csv.gz` (20,465 gene rows, TPM); design is cell type × {DMSO, EGCG, Methanol, DHEA} × {Div.1, Total}, five libraries per cell except Th17p/DMSO/Div.1 which has four; **no animal or culture field** |
| [GSE138266](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138266) | Fig. S4 human reuse (Schafflick et al. 2020) | 22 sample records; donor codes recovered from sample titles give 6 MS and 6 idiopathic-intracranial-hypertension donors, 10 of 12 with both CSF and PBMC; `GSE138266_RAW.tar` only |

## Single-cell aggregation order is the binding unknown

The deposit is the **pre-QC aggregated filtered matrix** (19,203 barcodes), not
the 5,192 cells the paper analysed after exclusions. Barcode suffixes `-1` to
`-8` give per-library membership (2,890 / 2,676 / 2,147 / 2,583 / 1,595 / 2,502 /
2,077 / 2,733 barcodes), but **no deposited field states which suffix is which
GSM**, and there are no per-sample matrices to resolve it. The GEO sample order
(Th17n_1mM_Mo1, Th17n_25mM_Mo1, Th17n_1mM_Mo2, Th17n_25mM_Mo2, Th17p_1mM_Mo1,
Th17p_25mM_Mo1, Th17p_1mM_Mo2, Th17p_25mM_Mo2) is a plausible `aggr` order but is
an assumption, not a declaration.

Wp-R1 therefore has to recover condition labels, and the only honest route is
marker-based assignment with the assumed order stated as the prior and tested
against it: Th17p versus Th17n by differentiation markers, glucose arm by
glucose-responsive transcripts such as TXNIP, and animal by genotype-independent
library structure. Any assignment is a **derived label with an error mode**, so
it must be reported as such, and the suffix-to-GSM table must record
`mapping_status` rather than silently adopting the order. If assignment is
ambiguous for any library, that library's cells are excluded from
condition-contrasting endpoints instead of being assigned by majority vote.

## Units, and what cannot be claimed with them

- **Single cell:** cells are nested in 8 libraries from 2 animals, and the
  design is **fully crossed** — both `Mo1` and `Mo2` contribute to all four
  cell-type-by-glucose conditions, two libraries per condition. Animal is
  therefore not confounded with condition, and a within-animal paired contrast
  across glucose or differentiation does exist; with n = 2 it cannot support
  population inference. A cell-wise p value here describes the libraries, not
  mice: the published p < 10⁻³³ for the glucose effect on the pathogenicity
  score is a cell-wise statistic of exactly this kind.
- **Bulk:** five libraries per group with no animal field. The paper states
  3–6 biological replicates per in-vitro group and 2–3 mice per RNA-seq group,
  so some of these five are plausibly separate mice and some plausibly split
  cultures — the deposit does not say which. Treat the library as the unit,
  report it as the unit, and do not convert five libraries into five mice.
- **Division gating:** `Div.1` and `Total` are different populations of the same
  culture, not replicates. Contrasts must stay within one gating arm; mixing them
  changes the population being compared.
- **Human:** the donor is a real unit, and 10 donors contribute paired CSF and
  blood. This is the only place in the paper where a donor-level paired contrast
  is available, which is why Wp-R4 is worth running even though the signature
  being transported is exposed.
- **Cell cycle:** phase composition differs between conditions and was regressed
  out of the latent space as a nuisance covariate. Proliferation is therefore a
  live alternative explanation for score differences across glucose conditions,
  and any re-derivation must report the phase composition it is conditioning on.

## Human reuse cohort

The discrepancy here is **internal to the reused deposit**, not something the
Wang text asserts: that paper only says it reanalysed a previously published
dataset of blood and CSF from MS patients and an idiopathic-intracranial-hypertension
control cohort. GSE138266's own `!Series_overall_design` field describes a
five-versus-five case-control design with two samples per donor, which would give
20 samples; its sample records resolve to 6 MS and 6 control donor codes with 22
samples, because one donor in each group contributes CSF only. Define the Wp-R4
population from the sample records, not from either summary sentence, and note
that neither tells us which donors passed the published CD4 filtering, which is
not deposited.

No donor characteristic field exists: donor identity is recovered from sample
titles (`MS19270_CSF`, `MS19270_PBMC`, …). Age, sex, treatment status and disease
duration are absent, so MS-versus-control differences cannot be adjusted for
them.

## Missing inputs

**Resolved 4 October 2026:** Supplementary Tables S1 and S3–S6 were recovered
from the NIH PMC Cloud open-data package `PMC12443480.1`; see the
[source manifest](SOURCE_MANIFEST.md). Table S1 carries 116 pro-inflammatory and
68 pro-regulatory genes with an `is_HVG` flag whose true counts are 63 and 30 —
exactly the numbers the paper states were scored — so the published score is
reproducible from the authors' own list rather than substituted. Wp-R1 and Wp-R3
are therefore exact reproductions of those definitions, not reconstructions.

| Missing | Consequence | Reopening condition |
|---|---|---|
| The 5,192-cell analysed set, its exclusions and the fitted scVI model | Exact single-cell reproduction impossible; re-derived embeddings and clusters differ by construction | Author-supplied processed object |
| Compass outputs for this paper | Fig. 1 cannot be reproduced without rerunning Compass on a re-derived imputed matrix | Author-supplied reaction scores, or a licensed solver plus a declared version sensitivity |
| Numeric values for flow cytometry, LC/MS 13C, Legendplex, EAE scores and histology | Figures 1C–1G, 3 (13C), 4 and S5 are not reproducible from data | Author-supplied source data; digitisation would be a separate approximate reconstruction with its own uncertainty, never raw data |

Raw inputs live in ignored `raw_data/wagner_pgam_w2_20261004/` with an
`acquisition_v1.json` manifest. They are available at execution and hash-matched
by the contract; they are not committed to the repository.
