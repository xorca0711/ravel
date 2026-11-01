# Combined gallery review

1 November 2026 (Asia/Seoul). Owner: Sx22-P01. The owner reported that the root
README did not expose the gallery and the extension page showed only one figure.
The root and paper-index navigation omitted Saxton; the E1a page correctly held
one three-panel figure. PNG/SVG alternatives and the preserved v1 rendering
were never additional results.

## Change and scope

The [combined gallery](FIGURES.md) now collects three current figures: R1 library
QC, X1 identifier QC and the unchanged E1a transcript description. Root/paper
README links and links from both extension packages lead to this gallery. X2
and X3 retain tables/source notes; held analyses have no fabricated figure slots.

The two new QC figures copy reviewed frozen quantities. The separate technical
chat committed [the render contract](qc_gallery_v1/config/render_contract_v1.json)
and bound code/tests at `05fa2ffa5af8bb28bbbe8db9bd3336c106dfa99c` before execution.
Its [receipt](../../analysis/research/runs/sx22_qc_gallery_render_v1/receipt.json)
records the new immutable run. This is outcome-exposed rendering, not a new
biological comparison, independent replication or a reopening of R2/R3.

## Independent originating-chat review

- A separate standard-library calculation matched all 18 copied library
  quantities and the percentage conversion/display against the six original
  `library_qc.csv` rows in order.
- A separate count from `repeated_symbols.csv` confirmed 52 labels, 122 rows,
  multiplicities of 48/3/1 labels at 2/3/17 records, and all six overlapping
  annotation dimensions. All nine plot-category values and denominators matched.
- All 16 contract/input/code/output hash bindings matched. Both SVG files parsed
  as XML and contained no trailing whitespace; no frozen file was reformatted.
- Both PNGs were inspected: library order, exact numbers, axes, units,
  zero-category label, denominator and overlapping-category warning are visible.
  No clipped labels or misleading error bars were found.
- Renderer/source review confirmed the absence of raw expression reanalysis,
  treatment tests, target ranking or animal-level inference. The existing E1a
  presentation and its original [review](recipient_context_v1/REVIEW.md) are reused.

The figures are accepted for this bounded display purpose. This review does not
create human scientific acceptance or change any canonical RQ or claim grade.

## Integration validation

The reviewed technical handoff `ba47620e056043662375feb3ebc2f81c473b6c63` was
integrated from main `41dc127`, which merged PR #155. A fresh fetch after
validation confirmed that the base remained unchanged.

- Combined-tree repository validation passed **12,833 checks**.
- The base-aware research gate passed with zero errors against `origin/main`.
- A focused navigation check resolved 260 local link/image targets and confirmed
  exactly three distinct embedded images in the combined gallery.
- The new diff passed whitespace checks without SVG exceptions. Scope inspection
  confirmed only the new QC package/run, its registry contract/receipt entries
  and navigation/review/status documentation; earlier frozen outputs and
  governance files were unchanged.
- The technical handoff's eight targeted tests, 158 shared tests (two skipped),
  compilation and archive checks passed. These valid checks were reused because
  originating integration changed only documentation, not the renderer or inputs.

No biological analysis was rerun for these presentation changes. The follow-up
branch is `codex/saxton-gallery-navigation-20261101`; publication and merge status
belong to its GitHub PR, separate from scientific acceptance.
