# Originating review of E1a

31 October 2026. **Pass for the defined observed-cell description and corrected
v2 figure.** Technical handoff `b3c6e72d553bb333e5a85e1341b8f91d9bc78375` is
integrated locally on `codex/saxton-recipient-context-20261031`.
This is agent technical/source review, not human scientific acceptance.

## What was independently verified

- The numerical receipt and contract, with all 12 bound input/code/output hash
  entries, match the files inspected. Raw CSR buffers in the original H5AD
  independently reproduce all 23,366 selected cell counts and all 11,683 cell
  totals. The verification did not import or run the analysis entrypoint.
- All 78 stratum/gene rows independently reproduce their cell denominators,
  positive-cell counts, count sums, zero/one/at-least-two bins, detection fractions
  and ratio-of-sums abundance. All 18 empty rows correctly have unavailable
  measurement fields. The original ordered cell IDs and labels are retained.
- The v2 contract and its nine bound hash entries pass. All 78 display rows
  reproduce the 156 measurement labels from the unchanged numerical table,
  including exactly four small-positive `<0.1` annotations. SVG XML is valid.
- The corrected PNG was visually inspected: aligned rows, readable library/gene
  labels, explicit denominators, distinct empty/zero/small-positive cells, stated
  abundance/color scales and interpretation limits. No biological response,
  trajectory or protective effect is implied by the figure.
- Code review confirms two fixed transcripts, all declared labels and the original
  non-contaminant rule. No condition contrast, scoring, clustering, target ranking
  or source-pipeline replay was added. The final 30-path technical diff is limited
  to E1a, its runs, article navigation, PROGRESS and Sx22 registry bindings.

The numerical contract/code were frozen at `5fbe78f`. The rendering amendment
was frozen separately at `56da56e`; it does not recalculate measurements. Original
outputs, including the superseded v1 figure, remain unchanged. Historical Choi,
R1 and X1–X3 evidence, canonical RQs, root attributes and governance are preserved.

## Scientific disposition

Only two retained cells contain a single Il22ra1 count; one remains under the
original non-contaminant rule. This is inadequate evidence for a state-specific
receptor pattern, and it cannot establish biological absence or responsiveness.
Il10rb measurements are a separate descriptive endpoint. Different capture depth,
pooled animals, library/time confounding, selection and uncertain labels prevent
animal-level response or repair conclusions. The unfavorable measurement
coverage is retained without adding targets or cohorts to obtain a positive result.

C0–C3 are complete. The historical E1 animal-level response question, original
Saxton WT/variant treatment analyses and persistence/function comparisons remain
unexecuted with their documented service or measurement/linkage limitations.
This new descriptive question does not lift the original restriction or identify
its unspecified triggering item. No new restriction occurred during E1a.

## Validation and integration limits

The technical handoff passed 12,752 repository checks, the base-aware research
gate, 12 targeted tests, 158 shared tests (two Windows skips), compilation and
required receipt/claim/archive checks. [VALIDATION](VALIDATION.md) records commands,
runtime preparation and failures. These unchanged checks are reused. Final
integration passed 12,765 repository checks and the base-aware research gate
with zero errors, recorded in [PROGRESS](../../../PROGRESS.md).

The two frozen Matplotlib SVGs each contain 54 path-formatting lines with trailing
spaces. Preserving those exact bytes is an explicitly reviewed formatting
exception. Both XML/hash checks pass; authored-file whitespace is checked
separately. No attribute file, validator or frozen output was weakened or edited.
The isolated HDF5 dependency remains in the preserved technical worktree;
reviewing the published tables/figure does not require rerunning the analysis.

The handoff is local and unpublished. PR #155 remains the separate recovery PR.
No main merge, external setting change, author contact, Notion write, new claim
grade or human scientific acceptance occurred.
