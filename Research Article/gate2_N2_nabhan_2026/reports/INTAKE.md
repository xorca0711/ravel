# Intake outcome, 1 October 2026

The paper package is structured and the lightweight inventory **passes**.
[Machine-readable record](intake_2026-10-01.json). No new biological model or
paper figure reproduction has run.

## Completed

- Reviewed the supplied article, both Notion pages, prior reproduction/extension
  conventions, A10/A2 outputs and the later P1 design recovery.
- Matched the newly supplied supplementary PDF to the cached source by SHA-256.
  Read its computational methods and inspected the article's Figures 3–5.
- Reused the existing supplement archive and extracted all seven datasets to
  ignored local storage. [Schema record](supplement_schema.json) identifies
  S6 as 200 target rows by 20 components and S7 as 20 gene-projection sheets.
  No additional upload is needed for S1–S7.
- Created source-method extracts, a dependency graph and eight question cards.
  E1/E8 share one proposed analysis; E2 is the other first priority.
- Verified 18 locally present manifest files against their recorded hashes.
  The two absent inputs are the full count workbook and Xenome QC at the
  historical A10 cache paths.
- Checked the existing crosswalk: 886 libraries, 203 target labels, four plate
  layouts, 15 RNA repeat groups and 885 paired imaging wells. No animal IDs are
  resolved in that crosswalk. These are metadata counts, not biological n.

## What remains before numerical reproduction

1. Recover the full count workbook and Xenome QC at verified hashes. The seven
   supplemental datasets do not replace raw counts. S4/S5 are selected DE
   summaries, and A10's selected-gene cache cannot implement whole-gene QC.
2. Finish source schema/alias and statistical-setting recovery. Freeze R1/R2
   before fitting. Record the different imaging versus RNA controls and the
   true read-count semantics.
3. Reconcile spatial treatment, block-to-animal identity and the reported
   50-um2 grid versus 8-micron bins before a genotype/region analysis.
4. Recover exact signature definitions, cPCA settings, ICA scaling/rank and
   source DE-table filters before claiming figure-level numerical reproduction.
5. Keep DepMap's 93-versus-96 denominator and the human IFN cohort identity
   explicit until source recovery resolves them.

Structural success does not clear these scientific gates. Existing A10/A2
results and old frozen configurations were preserved. The owner's now-complete
reading permits this new synthesis; it does not retrospectively make prior
screen analyses source-faithful reproductions or independent validation.

## Repository verification

Compilation, the 53-test suite (one skip), claim contracts, archived Nb1 and
A16 verifiers passed. All 417 link checks across the 12 changed/new Markdown
files passed. The full repository validator reported 17 link failures, all
confined to the pre-existing untracked adversarial-audit document. That folder
was not edited. [Verification record](verification.json).
