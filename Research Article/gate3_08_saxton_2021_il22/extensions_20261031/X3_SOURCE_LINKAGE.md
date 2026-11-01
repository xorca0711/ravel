# X3: companion withdrawal-panel source qualification

31 October 2026 (Asia/Seoul). Sx22-P01 documentary work. Purpose: qualify what the
advertised source material identifies for Supplementary Fig. 5e and whether it
provides a link to later function. Unit of inspection: panel, source document and
source-reported experiment/preparation key. Endpoint: label and linkage availability,
not the magnitude of a biological response. Main validity threat: borrowing units
or endpoints from other panels because they share a figure number or paper.

## Source and access

[Cineus, Luo et al., Nature Immunology 2025](https://doi.org/10.1038/s41590-025-02149-z),
DOI 10.1038/s41590-025-02149-z, has a public
[supplementary PDF](https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-025-02149-z/MediaObjects/41590_2025_2149_MOESM1_ESM.pdf).
The retrieved 28-page file has SHA-256
`96dc5adaf01a669ac89b1e3ed5fbb8fe293bdb5ddda7099f79547f90ec4e8bc8`.
Europe PMC's article XML independently advertises the same MOESM1 filename.
The publisher reporting summary (MOESM2) and supplementary tables (MOESM4) were
also retrieved and hashed. All requests and limits are in [SOURCE_MANIFEST](SOURCE_MANIFEST.md).

The PMC file request returned HTTP 200 HTML, not a PDF. The `springer-cdn.com`
hostname failed to resolve locally; the ordinary `static-content.springer.com`
publisher mirror succeeded. These are access outcomes, not platform biological
restrictions. No login, access-control bypass or author request was used.

## Exact panel reading

Poppler renders of **PDF p. 23 (Figure S5)** and **p. 24 (caption; printed p. 18)**
were visually inspected; extracted text was checked against those images.
The panel is **S5e**, although the overall figure title concerns other immune-cell
experiments. The main-text removal passage immediately preceding Figure 4 cites
this panel. The following records labels only, with no digitization or effect fit.

| Item | What the inspected source supplies | What it does not establish |
|---|---|---|
| System / endpoint | Colon epithelial organoids; Osmr qPCR transcript expression | Receptor protein, signaling activity, lineage output or functional recovery |
| Vertical axis | Relative expression normalized to untreated; logarithmic axis labeling | Raw Ct values, raw individual observations or an independently measured reference distribution |
| Horizontal axis | Time after IL-22 withdrawal in days; displayed observation labels 0, 1, 4, 6 and 8 | Sample-specific timestamps, biological sample identity or a repeated-measure unit map |
| Cessation / handling labels | Nominal withdrawal at the transition to no IL-22; a splitting/passaging marker appears at day 1 | Measurement of residual ligand or confirmed signal cessation; handling and elapsed time are not independently resolved by the picture |
| Source replication | Caption says representative of two independent experiments | Number of biological preparations or technical replicates per time point; identity of observations; meaning of the plotted error bars for this panel |
| Neighboring panels | S5c/d report a separate genotype/colitis mouse comparison and histology | Their six-mice-per-genotype count and histology cannot be assigned to organoid panel S5e |
| Link to function | No unit key or cross-panel endpoint join is shown for S5e in the inspected materials | A transcript time series does not establish a within-unit link to later viable mature output or other functional recovery |

The labels document nominal exposure history. They do not turn an intervention
description into verified biological cessation or distinguish persistence from
handling, selection or continued input. Those are interpretation limits, not a
new experiment design. The original curve was not reconstructed, compared or scored.

## Reporting and workbook coverage

The five-page reporting summary was text-inspected at p. 2 (sample size,
replication/randomization/blinding) and p. 4 (primary organoid/animal context).
It defers experimental replication to figure legends and describes study-wide
identification practices, but does not publish an S5e observation-to-mouse or
preparation key. A statement that animals received identifiers is not the key itself.
General reporting does not resolve this panel's per-time replication or error bars.

The MOESM4 workbook was opened read-only as an OOXML source document. Sheet names
and leading rows were inspected; no values were recalculated or biological tables
reanalyzed. Its index identifies the following material:

| Table / exact index-sheet locator | Advertised content |
|---|---|
| `Suppl. Table 1`, A1 | Single-cell epithelial/stromal/immune analysis |
| `Suppl. Table 2`, A1 | Bulk-RNA experimental-group comparisons for Figure 2 |
| `Suppl Table 3`, A1 | Epithelial characterization during colitis |
| `Suppl Table 4`, A1 | Pathway-analysis tables for Figures 2 and 6 |
| `Suppl Table 5`, row 1 | Human sample/cohort metadata |
| `Suppl Table 6`, A1 | Cell-line transcript-response tables |
| `Suppl Table 7`, A1 | Reagent inventory |
| `Suppl Table 8`, row 1 | Patient/cohort metadata |

This inventory did not identify an S5e raw-qPCR or organoid-to-function crosswalk.
It is **not a complete cell-by-cell workbook audit** or proof that no other export
exists. Leading rows include published results and reagent/sample information;
none was used to estimate effects, select targets or design an intervention.

## Remaining item-specific limits

MOESM3 (peer review file) was advertised but not inspected. MOESM5 and MOESM6 are
advertised as raw blots for Figure 4a/d and Extended Data Figure 7b–d; their files
were not opened and are not represented as S5e sources. Supplementary PDF pages
outside the target figure/caption and reporting-summary pages outside the stated
scope were not exhaustively reviewed. GEO matrices and other sequencing deposits
for this companion were not downloaded or mapped to S5e.

**Disposition:** X3 documentary inspection is complete at this coverage. Nominal
withdrawal/time and transcript endpoint labels are qualified. Biological-unit
identity, per-time replication, measured cessation and linkage to later function
remain unqualified. Reopening a source-linkage question would require an explicit
panel/observation/preparation key and the actual endpoint relationship; it would
not itself lift the original platform-policy execution holds. No human scientific
acceptance or new numerical eligibility is asserted.
