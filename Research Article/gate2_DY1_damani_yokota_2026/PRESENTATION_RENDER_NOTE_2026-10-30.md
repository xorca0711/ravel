# DY1 presentation derivatives: rendering record

30 October 2026, Asia/Seoul. Rendering only, from the successful reviewed F1/F2/F4
tables. The [results](rq_discordance/FOLLOWUP_RESULTS_2026-10-30.md) and
[independent scientific-boundary review](rq_discordance/FOLLOWUP_REVIEW_2026-10-30.md)
remain the result authorities. These plates change presentation, not estimates,
intervals, donor eligibility, source annotations or scientific acceptance.

## Scope and preserved evidence

The biological units remain human donors for F2 and source mouse/preparation
groups for the non-infectious F1/F4 reference. Mapped genes and regions are
dependent measurements. All outcomes were exposed before this rendering task.
The relevant presentation risks are crowded labels, changing denominators or
source definitions, and confusing omission ranges with sampling uncertainty.

The versioned [contract](config/presentation_figures_v1.json) and
[parameters](config/presentation_parameters_v1.json) fix four plates:

| Stem | Purpose and source | Presentation limit |
|---|---|---|
| `01_representation_weighting_v1` | All four F1 pair/equal-gene summaries, explicit percentage-point shifts and mixed-direction gene counts | Presentation replacement for the crowded original F1 PNG only; related mappings are not independent validation |
| `02_human_contrasts_v1` | Two fixed panels, all six F2 IPF-Control cohort/annotation/site scopes; original intervals and donor n copied | Different source annotations, cell floors and sites remain explicit; no pooled cohort effect or new bootstrap |
| `03_human_coupling_v1` | Primary Macrophage20 and external union50 within-IPF correlation; original interval and separate component/donor omission ranges | Only original intervals describe sampling uncertainty; the external interval still spans zero |
| `04_cofactor_correlations_v1` | All eight F4 GRIP1/NCOA2 mapped-row correlations, separate source-labelled IL4/CTRL comparisons | Full Spearman scale; no new interval, p-value, interaction or causal-mechanism claim |

The original ten PNGs, earlier scripts, contracts, receipts and data tables remain
unchanged. The complete inventory/gallery and README navigation are maintained
by the coordinating reviewer. This note owns only the four-plate render package.

## Rendering and checks

Style follows the neighboring Nb5 figures-v3 workflow: white backgrounds,
restrained colors, readable horizontal labels, A/B/C panel letters where useful,
and compact purpose/result/limit footnotes. Every plate exports a 300-dpi PNG and
genuine vector SVG/PDF, with a four-page PDF bundle. Fixed 11.8-by-8-inch canvases
preserve generous caption margins; no tight-bounding-box crop masks overflow.

The renderer records source input/code hashes, selected row keys, raw and
display-scaled values, formatted labels and plotted coordinates. An independent
CSV/scalar pass verifies source selection and formatting without pandas. Export
checks require vector SVG/PDF, exact SVG label presence, 300-dpi PNG dimensions,
four bundle pages and text/caption bounds with no text overlap. Human visual
inspection of all four PNGs and rendered PDF pages follows execution.

Five synthetic tests cover all four layouts, nonfinite/ambiguous source rows,
coordinate disagreement, and separate original-interval/range semantics. Two
initial draft fixture checks caught title/legend collisions; positions were
corrected before source rendering. Subsequent preview inspection shortened the
F1 axis wording to cover both weighting rules and split the human-contrast axis
labels over two lines. These are pre-freeze layout changes, not failed biological
or governed source-data runs.

## Execution and export review

Pre-freeze independent review cleared the exact 11 input/code hash bindings.
The package froze at `06be8fda7bf5cff615c85bbd2df5928bbae065b4`, then completed
its sole governed render successfully. The
[receipt](../../analysis/research/runs/DY1_presentation_figures_v1/receipt.json)
verifies. No source-data render failed and no frozen output was overwritten.

- [Four-page vector PDF bundle](../../analysis/research/runs/DY1_presentation_figures_v1/DY1_presentation_plates_v1.pdf)
- [Export inventory and hashes](../../analysis/research/runs/DY1_presentation_figures_v1/render_inventory.tsv)
- [Render record and caption/layout checks](../../analysis/research/runs/DY1_presentation_figures_v1/render_record.json)
- [Source-value, label and coordinate verification](../../analysis/research/runs/DY1_presentation_figures_v1/data_label_verification.json)

All 378 scalar checks passed for 126 source-value records. All four canvases
passed visible-text bounds, overlap and caption-clearance checks. SVG exports
retain vector text with every recorded label; PNGs are 3540-by-2400 pixels at
300 dpi. Independent PDF inspection with pypdf/pdfplumber confirmed four
single-page PDFs plus the four-page bundle, no embedded raster images, all
character bounds within pages, and all 62 recorded labels in the bundle text.

The executor visually inspected all four final PNGs and all four bundle pages
rendered with Poppler at 120 dpi. Labels, intervals, values and captions are
readable without clipping or collisions. In particular, the six human scopes
retain distinct n/site/annotation labels and the external original correlation
interval visibly crosses zero. The coordinating reviewer independently confirmed
saved-value parity and readable, in-bounds rendering of all four PDF pages.

The new script compiles, repository validation passed 11,751 checks, and the
research gate passed against freshly fetched `origin/main`
`28fb61015f9b921f591e41ff26010a960c305947`. The integration branch remained at
`4af89c8df3b234b2f4e005cf4d12d014343ab7d4`; no remote change required reconciliation.
Canonical 32-question records, guides and protected infrastructure are unchanged.

The broad Git whitespace check reports 319 native Matplotlib SVG path-data
trailing-whitespace notices and no non-SVG warnings. These are retained as exact
frozen export bytes; SVG parsing, vector/text parity, visual checks and receipt
hashes pass. No validator, policy or frozen file was changed to suppress them.

The repository's general PDF ignore rule initially excluded the five new PDFs
from directory staging. A packaging audit caught this before handoff; those
exact requested exports were explicitly added without changing the ignore rule
or any artifact bytes. All 16 declared outputs are tracked. Repository and
base-aware gate checks were repeated for the complete packaged set.

No biological analysis or inferential statistic was recomputed. Valid earlier
biological tests and source verifiers are reused because their code, inputs and
evidence are unchanged; the new renderer has its own targeted tests and export
verification. Gallery, README and literature navigation are outside this package.
