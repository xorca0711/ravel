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

Execution, export verification and final integration-check results will be
recorded after pre-freeze review and the governed render. No biological analysis
or inferential statistic is being recomputed.
