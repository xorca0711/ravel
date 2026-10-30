# DY1 gallery: rendering and independent review

Review performed 30 October 2026, Asia/Seoul; integrated 31 October after the
owner approved the integration retry. Owner-requested presentation work, with the existing
technical chat implementing the renderer and the coordinating chat reviewing it.
This is technical review, not a human scientific acceptance or a new biological
analysis.

## Scope and inventory

The [gallery](FIGURES.md) retains all ten original PNGs and presents thirteen
current plates: nine unchanged originals, one readable F1 replacement and three
new summaries. The original F1 remains linked as a historical presentation.
The numerical F1/F2/F4 results and original run outputs remain unchanged.

Four new plates are bound to
[the presentation contract](config/presentation_figures_v1.json), freeze
`06be8fda7bf5cff615c85bbd2df5928bbae065b4`, and the
[executed receipt](../../analysis/research/runs/DY1_presentation_figures_v1/receipt.json).
Each has 300-dpi PNG (3540 × 2400), vector SVG and PDF; the
[four-page bundle](../../analysis/research/runs/DY1_presentation_figures_v1/DY1_presentation_plates_v1.pdf)
contains the same plates. Original PNGs are not relabelled as vector exports.

## Review evidence

Before freeze, the coordinating reviewer inspected the contract, parameters,
renderer and tests. All eleven input/code SHA256 bindings matched. Only saved
F1/F2/F4 values are read; arithmetic is limited to display conversion and
formatting. Six human scopes, two within-IPF scopes and all eight F4 correlations
are fixed. No source analysis, bootstrap, omission calculation or correlation
was rerun.

After execution:

- All ten original PNGs matched their executed receipts. Seven earlier originals
  were visually inspected in this gallery pass; the prior F1/F2/F4 figure review
  was reused. F1's crowded labels prompted the new presentation.
- All four new PNGs were independently inspected: axes, labels, small values,
  source scopes, donor counts and footnotes are readable without clipping.
- The parent independently passed **461 checks** across current input/code/output
  hashes, source-row selection, 126 displayed numeric records and formatting,
  and 56 plotted coordinate records. CSV reads were separate from the renderer's
  pandas selection. This checks display fidelity, not new biological validity.
- All four bundle pages were independently rasterized and visually inspected.
  All 4,205 extracted characters were within page bounds; no embedded raster
  image was present in the PDF bundle.
- The renderer's saved [verification](../../analysis/research/runs/DY1_presentation_figures_v1/data_label_verification.json)
  records 378 scalar checks, 62 label records and coordinate bindings. Its
  [render record](../../analysis/research/runs/DY1_presentation_figures_v1/render_record.json)
  records no text overlap or clipping and 9-point, three-line footnotes of
  45–49 words. Export checks retain SVG text, vector PDF, PNG DPI and page counts.

These checks reuse the previously reviewed biological results; they are not an
independent cohort replication or proof of the original paper's mechanism.

## Interpretation and presentation decisions

| Decision | Reason |
|---|---|
| Replace the display role of F1 only | Long original labels were crowded; new horizontal labels and explicit percentage-point shifts are readable. Numerical evidence remains frozen. |
| Show all six F2 contrast scopes | Annotation, cell floor and site change the comparison; selecting one could hide the FABP4-panel variation. |
| Separate original intervals from omission ranges | The external within-IPF interval spans zero despite negative omission ranges; influence checks do not override sampling uncertainty. |
| Use the full −1 to +1 F4 scale | Small GRIP1/NCOA2 mapped-row associations should not appear large through axis truncation. No p-value or CI from dependent rows is invented. |
| Keep source and mechanistic holds explicit | No figure supplies original NAM biological identities, within-state ATAC, linked ARG1 mediation or repair endpoints. |

The executor corrected two synthetic-layout overlap failures before freeze,
clarified F1's axis to describe both weighting schemes, and split the human
contrast x-axis label across two lines. These were draft presentation changes;
no failed biological analysis or frozen output was overwritten. The
[executor note](PRESENTATION_RENDER_NOTE_2026-10-30.md) records its checks.

Temporary approval-service capacity/deadline failures delayed read-only Git
checks and the clearance message. Authorized retries later succeeded; the
approval gate was not bypassed. No additional permission or unresolved external
setting is required for these figure files.

The repository's PDF ignore rule initially excluded the five PDFs from staging.
The executor explicitly added those five outputs and verified all sixteen declared
outputs in stable handoff `5aa6e08cb89e4df9a866d757c8f6afe6ad1023be`.
The final packaged handoff passed 11,751 repository checks and the research gate.
Native Matplotlib SVG path data produces 319 whitespace notices in a broad Git
whitespace check; source/document files have none. Frozen vector bytes were
preserved rather than edited after rendering.

## Integration validation — 31 October 2026

The integrated gallery and navigation passed 11,873 repository checks and the
base-aware research gate against freshly fetched main `28fb610`. The seven new
or updated documentation files have a clean whitespace diff. No renderer,
numerical output, frozen contract or biological analysis was changed during
integration; the prior visual and data checks remain applicable.
