# Candidate numerical follow-up v1: EZH2 gain-context profiles

Prospective specification, 7 November 2026. Dp1-P01, exploratory/descriptive.
The owner clarified that proceeding with the candidates means actual numerical
follow-up, beyond literature review and experiment drafting. This plan follows
[source qualification](candidates/SOURCE_QUALIFICATION.md); the seven original
DuPage runs remain unchanged.

## Question, decision and exposure

Do the fixed TIGIT–PRDM1, CCR2 and IGFBP4 candidates show reciprocal directional
patterns in the published Ezh2 gain-context matrix, and are those observations
consistent across omission of each recorded library? Distinguish baseline gain
effects from differences after activation rather than reporting a single fold
change. This informs which protein/context qualifications to emphasize; it does
not choose a winner, retire a route or test functional mediation.

Candidate symbols are **Tigit, Prdm1, Ccr2, Igfbp4**. Fixed output/context anchors
are **Areg, Il2ra, Igf1r**; these are not extra screened candidates. No replacement
gene or threshold is chosen after seeing the source outcomes. All seven get an
availability record, including missing/ambiguous entries.

The DuPage outcomes and literature, including Peeters' published TIGIT direction
and CD25 exception, were exposed. Source headers, SOFT metadata and filtering
rules were inspected before this freeze; candidate rlog values were not. This is
an exposed exploratory follow-up, not confirmatory validation.

## Comparison and measurement

- Source: GSE262130, sorted CD62L-positive murine Tregs, Ezh2 Y641F versus WT,
  freshly sorted (N) or four-day in-vitro CD3/CD28 activation (D4) with IL-2.
- Biological unit: source preparation. Three libraries/group are declared;
  animals, pooling, pairing and batch are unknown. Cells/wells are not substituted
  for animals. All 12 declared libraries are retained.
- Measured endpoint: authors' rlog-transformed expression in the published union
  selected by adjusted p < 0.05 across six comparisons, with `blind=FALSE`.
  This selected transformed matrix is neither raw counts nor an unbiased gene set.
- Compute mean rlog differences: gain_N = Y641F_N − WT_N; gain_D4 = Y641F_D4 − WT_D4;
  activation_WT = WT_D4 − WT_N; activation_Y641F = Y641F_D4 − Y641F_N;
  interaction = gain_D4 − gain_N. Means are unpaired descriptive summaries.
- Sensitivity: primary plus each of 12 single-library omissions. Report minima,
  maxima and whether all 13 signs agree, separately for each contrast. These are
  observed perturbation ranges, not confidence intervals. Do not change the rlog
  transform, impute missing values or use its values as count-model input.
- Compare directions only with the preserved DuPage high/low KO−HET contrasts
  and interaction. Label opposite/same/zero signs mechanically; do not pool or
  compare effect magnitudes across mean-log-FPKM and rlog units.

## Hypothesis and consequential rivals

A simple reciprocal-direction hypothesis predicts gain effects opposite to
DuPage loss effects at corresponding descriptive states. It is only a screening
model: Y641F changes EZH2 biochemistry and chromatin distribution, not merely the
opposite dose of a knockout. Culture duration, IL-2, genetic controls, baseline
state and survivor composition differ. A sign match cannot exclude those rivals;
a mismatch does not falsify the original knockout effect or the candidate's role.

Informative outcomes: a stable opposite gain_D4 sign supports context-consistent
direction; baseline-only or state-dependent signs narrow the proposal; omission
instability weakens robustness; missing entries restrict assessability; discordance
is retained rather than triggering a new search for favorable data. None of these
is a human retain/reject decision.

## Outputs, stop rules and validation

Save the 12-library metadata map, all seven availability records, candidate-level
sample values, primary/sensitivity contrasts, directional comparison to DuPage,
machine-readable summary and figure source values. Figures: four candidate
sample-profile panels and two clearly separated loss/gain contrast panels, with
PNG/PDF/SVG exports. The output anchors remain in source tables; every displayed
value is recoverable from those tables. No statistical stars, p-values or error
bars implying population uncertainty.

Use exact case-sensitive gene names and retain source Ensembl IDs. A missing or
duplicate symbol produces an explicit unavailable record, not arbitrary selection.
Stop on mismatched hashes, wrong sample header, duplicate sample labels, malformed
rows or nonfinite values for an otherwise eligible candidate. Preserve any failed
receipt and amend prospectively if necessary; never overwrite a run directory.

The research runner must execute a committed hash-bound contract. Validate the
results with an independent standard-library recomputation of selected means and
all omission ranges, verify source identity/coverage, and inspect figures. No
sample-size estimate, inferential model or laboratory-ready claim is added.
