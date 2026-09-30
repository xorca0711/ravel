# A19 methods and execution

**Run: exploratory_v1, 30 September 2026.** This is an exploratory secondary
analysis of human organoid RNA responses, selected to challenge narrower
predictions of A19. It is not a preregistered confirmatory test of H1–H3.
[Results](RESULTS.md) · [Figures](FIGURES.md) · [Source inventory](SOURCES.md).

## Contract, exposure and units

The owner authorized A19 analysis and paper-style figures under `RQ_Specified`.
The [original question contract](reports/question_contract_pre_execution.json)
is preserved byte-for-byte. The [exploratory contract](config/exploratory_v1.json)
was frozen at **2026-09-30 00:31:57 UTC**, after exposure to Nb2 results,
source narratives/captions, workbook string labels and GEO metadata, but before
new numerical outcomes were inspected. The [frozen record](reports/exploratory_v1_contract.json)
contains its SHA256 and the subsequently acquired input hashes. This is an
in-repository run record, not an external preregistration or independent
attestation. Original effect margins, endpoint choices and validation cohort
remain unset because no eligible direct H1 experiment was identified in this
bounded inventory.

qPCR units are exact source donor codes within a sheet, gene and condition.
Source Fig. 6a describes independent pooled organoid cultures; its codes do
not establish lineage tracking of single cells. Shared donor labels across
figures are not additional independent replication. Bulk RNA uses two source
blocks; each contains the four background-by-medium combinations. The paper's
two donor cultures are not explicitly linked to GEO batch labels. Different
knockdown hairpins are confounded with block. Eight libraries are not eight
donors, and no cell count enters an inferential sample size.

## qPCR extraction and estimation

1. Read cached numeric values from the five nominated Supplementary Data 3
   sheets with openpyxl. Carry the source gene/condition headings down to each
   explicit donor row. Preserve workbook row, original assay label, DeltaCt,
   reported DeltaDeltaCt/fold values and non-detection status. Normalize only
   three labels: GSK3β to GSK3B, P63 to TP63 and TGFb1 to TGFB1.
2. Plot **−DeltaCt**. For comparison C and reference R, the paired change is
   `DeltaCt(R) − DeltaCt(C)`. This is a log2 normalized-expression ratio only
   under the usual equal-efficiency/reference assumptions; it is not an
   absolute transcript count. Values of different genes are not directly
   comparable as absolute expression. Published fold-change columns are
   retained for audit but not used to estimate effects.
3. Match exact donor codes for each frozen contrast. Do not align by row
   position, replace undetected Ct values, infer missing donors or pool sheets.
   Retain every selected marker and contrast. The audit has 72 complete,
   12 missing-arm and one matched-but-nonquantified comparison; there are
   three undetected rows in the raw extraction.
4. Report paired effects, mean, median and range. For at least two quantified
   pairs, give `mean ± t(0.975,n−1) × SD/sqrt(n)`. These are conditional,
   descriptive 95% intervals assuming independent approximately normal
   donor effects. Tiny samples cannot verify those assumptions. They are
   not simultaneous intervals; no discovery p-values, equivalence decisions
   or retrospective power claims are produced.

The source-labelled **TCF4** assay is not reassigned to TCF7L2. Assay identity
must be resolved before interpreting it as a specific canonical Wnt effector.
The Fig. 4e assays are displayed separately, not combined into an activity score.

## Bulk normalization and supporting RNA panels

The intake script selects only eight sample titles matching
`(ctrl|GSK3kd)_(ctrl|CHIR)_[12]`. It reads gene IDs and the count column from
source featureCounts files; all 60,662 rows align across the eight libraries.
Keep genes with at least 10 counts in at least two libraries: **14,581 retained**.
Create an edgeR DGEList from the filtered matrix, recalculate library sizes,
and apply TMM normalization. The primary expression scale is
`log2(count / (filtered_library_size × TMM_factor) × 1e6 + 1)`.
The sensitivity scale uses the same filtered library sizes without TMM factors.
No differential-expression model or population-level interaction test is fitted.

The frozen contract nominates six panels and three sentinels. Official Ensembl
human symbol lookups provide stable IDs; remove version suffixes only for
matching. A panel needs at least 60% of its nominated genes and two genes.
All mappings and failures are retained in
[bulk_panel_membership.tsv](tables/exploratory_v1/bulk_panel_membership.tsv).
AT2 identity and AT1-associated panels each retain 6/6, airway 2/3, Wnt targets
4/4, proliferation 5/5; basal identity fails at 1/4. Do not substitute a zero
for the failed panel or broaden it after seeing results.

A score is the unweighted mean of eligible genes' log2(CPM+1), with no fitted
weights, within-gene z scaling, reference-cell subtraction or cross-cohort
harmonization. For each background and block, compute CHIR-absent minus
CHIR-present expression/score. The knockdown-minus-control response difference
is also retained per block. Those contrasts describe the eight libraries;
blocks/hairpins cannot supply a clean population interaction estimate.
Gene-level values and effects retain all eligible nominated markers and
sentinels (GSK3B, EGF, FOXM1), including results not highlighted in the figures.

Programs are supporting RNA phenotypes. They do not measure cell fractions,
Wnt activity, Hippo kinase activation, lineage transition, mature function or
retained AT2 capacity. CHIR absence is not called a verified Fzd withdrawal;
its timing and engagement are not interchangeable with the parent hypothesis.

## Pipeline and files

| Step | Script | Deposited outputs |
|---|---|---|
| Public-source acquisition | [00_fetch_sources.py](scripts/00_fetch_sources.py) | URLs/hashes and exact sample/annotation metadata; full payloads in ignored cache |
| Source extraction | [01_prepare.py](scripts/01_prepare.py) | Selected qPCR source rows, source sample map and library QC |
| Normalization | [02_normalize.R](scripts/02_normalize.R) | TMM factors/effective library sizes and R session; full matrices ignored |
| Contrasts | [03_analyze.py](scripts/03_analyze.py) | Paired effects, missingness audit, summaries, coverage, gene/program responses |
| Figures | [04_figures.py](scripts/04_figures.py) | Four PNG/SVG/PDF sets and source/output hashes |
| Independent checks | [05_verify.py](scripts/05_verify.py) | [verification.json](reports/verification.json) |
| Visual review | [06_render_review.py](scripts/06_render_review.py) | PDF-page PNGs in ignored cache; [review record](reports/visual_review.json) |

The verifier does not import the extraction/analysis functions. It checks exact
workbook cell coordinates and donor headings, source count columns, frozen
hashes, Ct arithmetic/intervals, filter membership, normalization denominator
arithmetic across full matrices, panel coverage, effects/interactions and export
hashes. It verifies implementation and provenance, not biological independence
or the statistical assumptions of the source experiment.

## Reproduction

From the repository root, use Python with numpy, pandas, scipy, openpyxl,
matplotlib and pymupdf, and R with edgeR. Run the commands in order; acquisition
requires public network access. Full inputs stay under the ignored question
cache. The first render belongs to `exploratory_v1`; preserve finalized artifacts
and use a separately recorded output directory for later scientific amendments.

```powershell
python RQ_Specified/A19_fzd_response_reversibility/scripts/00_fetch_sources.py
python RQ_Specified/A19_fzd_response_reversibility/scripts/01_prepare.py
Rscript RQ_Specified/A19_fzd_response_reversibility/scripts/02_normalize.R RQ_Specified/A19_fzd_response_reversibility
python RQ_Specified/A19_fzd_response_reversibility/scripts/03_analyze.py
python RQ_Specified/A19_fzd_response_reversibility/scripts/04_figures.py
python RQ_Specified/A19_fzd_response_reversibility/scripts/05_verify.py
python RQ_Specified/A19_fzd_response_reversibility/scripts/06_render_review.py
```

This run used the bundled Codex Python and repository scientific site-packages
via `analysis/scripts/run_with_environment.py --site-packages
X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages <script>`. R 4.6.1 used edgeR 4.10.5
and limma 3.68.5; [R_session.txt](reports/R_session.txt) and verification metadata
record runtime versions. Exact PDF/SVG bytes can vary across regeneration due
to export metadata and library versions; numeric tables and the source hashes
are the scientific comparison targets. The recorded hashes identify this run.

## Corrections and limitations

The first extractor failed on an empty openpyxl cell lacking a row attribute;
using the iterator row index fixed source-coordinate recording without changing
selection. [intake_correction.json](reports/intake_correction.json) and the
[failed source](reports/execution_sources/01_prepare_before_cell_fix.py) retain
that event. Figure-script newline escaping was corrected before successful
rendering. Visual review then moved labels away from axes/data and clarified
the airway-derived origin of the passage experiment. No numerical outcome or
contract was changed by those fixes. The frozen figure shorthand mentioning a
receptor-input comparator is not treated as evidence of a receptor experiment;
the final captions correctly identify the GSK3 context and leave H3 unresolved.

The R locale fallback and deprecated calcNormFactors alias emitted warnings;
normalization completed and arithmetic checks passed. A first PDF-review call
without the scientific site-packages failed to import fitz; the repository
runtime and pymupdf resolved it. Source acquisition failures remain in the
intake log. Neither inaccessible individual observations nor undetected
expression was imputed. Existing Nb2/A0–A18 analyses were not modified.
