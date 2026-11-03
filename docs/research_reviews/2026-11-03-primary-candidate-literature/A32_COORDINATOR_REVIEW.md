# A32 public resolution screen: coordinator review

3 November 2026, Asia/Seoul. Continuation authorized by the owner's
"proceed with that" after [hold-resolution options](HOLD_RESOLUTION_OPTIONS.md).
This record distinguishes design review from completed numerical review.

## Scope and integration

The existing technical chat `01a1a00c-8680-7fd2-a7ea-4bf804005da8` owns the
GSE234197 source inspection, versioned contract/code, execution, A32 reports and
owning-page updates. The coordinator owns independent review and final integration.
The owner merged PR #161; this follow-up starts from main `445a0ca` on
`codex/a32-resolution-screen-20261103`. Existing dirty notes were preserved.

The original A32 question still asks about source ARG1 and joint matrix/mature
epithelial outcomes. This authorized branch is a descriptive RNA context screen,
not execution of that functional comparison. Speth's original access hold remains.
The Lin and Hamanaka requests are private, unsent drafts. No controlled access
application, outreach, laboratory operation or new scientific acceptance occurs.

## Independent primary-paper read and design points

[Truchi et al., Nature Communications, 6 August 2025](https://doi.org/10.1038/s41467-025-62431-4),
current PMC12328796, Results Fig. 1-2/S2 and Methods HTO demultiplexing,
sample integration and differential expression were inspected on 3 November.
The paper reports 36 source mice, 45,311 retained cells and labels spanning
macrophages, fibroblasts and alveolar epithelium. Those are published counts,
not yet an independent verification of the deposited object in this record.

Its reported similarity of macrophage-subset abundance dynamics across ages
(S2E/F) is relevant contrary context. Within-state expression and composition
must be distinguished. Original broad injury DE omits D60 injury samples and
pools PBS times; the proposed resolution screen retains D60 and time-matched
controls. Six age-by-day captures confound raw age/time comparisons with run.
Within-run injury/control contrasts reduce, but cannot exclude, run-by-condition
effects. Cross-sectional mice are not repeated longitudinal measurements.

These points were sent to the technical chat before its numerical freeze.
Use raw RNA counts for measured expression, retain source annotations and
record current-object selection. Do not silently impose the Methods' unusual
mitochondrial-percentage wording without checking source code/units. Source
histology or hydroxyproline cannot be joined to sequenced mice without explicit
identity evidence. No score is deposited collagen or mature epithelial function.

## Prospective specification and extraction review

The coordinator read the technical specification and `recover_metadata_v1.R`
plus its native-R fixture script before the metadata freeze. Fourteen named
genes are proposed, reported individually, with separate source-cell proportions.
The extractor streams XDR and discards large numeric payloads for metadata-only
deserialization; original sparse count files remain the expression source.
The technical chat reports passing native-R v2/v3 byte-preserving passthrough,
metadata/factor/S4/reference/ALTREP/nested-gzip checks and failure cases.
The coordinator reviewed the code rather than repeating those same fixtures.

The metadata run can proceed; real-source joins remain to be reviewed.
Before the expression freeze, the technical chat was asked to bind exact
gene-group source locators, state labels, support rule and uncertainty method.
Mouse values remain primary; PBS and BLM mice are unpaired, and reused HTO
suffixes across captures do not denote repeated observations of one mouse.
Unsupported populations remain in the support table. These are study-specific
review points, not changes to repository governance or scientific acceptance.

## Numerical review

Metadata recovery executed under freeze `7132cc0`. The coordinator independently
read its TSV using Python's standard-library CSV parser and counters: 45,311
unique cell IDs, 41 source labels and 36 capture-plus-HTO mouse IDs, with exactly
three PBS and three Bleo mice per capture. Every tag/condition assignment matched
the public workbook. This confirms recovered metadata consistency; expression
joins against original sparse matrices remain a later check.

The proposed joint three-compartment screen is not supported by the retained
cells. AT1 has 0-5 cells per mouse. AT2 has 0-25, with no injured group supplying
three mice at the proposed ten-cell support floor. Only young D14 fibroblasts
have all six mice above that floor. This is source support, not a gene-effect
result or evidence that epithelial recovery is absent.

The coordinator approved narrowing to eligible myeloid source-state contrasts
and young D14 fibroblasts, with unsupported rows retained. The ten-cell rule is
a pragmatic measurement-support rule chosen from exposed metadata, not a power
calculation. A separately labelled all-AM summary is allowable as secondary,
composition-sensitive context; it cannot restore within-state or epithelial
inference. This amendment and its reason were reported to the owner before
expression. No search for a more favorable cohort or threshold relaxation was
authorized as a response to sparse epithelial support.

The completed expression deposit contains 306 planned contrasts: 88 estimated
and 218 explicitly unestimated. There are no supported epithelial condition
contrasts. The coordinator independently recomputed support denominators,
eligibility, CPM/log transformations, means and interval arithmetic using CSV,
standard-library statistics and the t quantile: 4,308 checks passed, with maximum
absolute numerical difference `3.67e-15`.

Before the expression freeze, code review identified a degenerate-variance
problem: zero observed variance in both groups would produce a zero-width
confidence interval. The prospective design now retains the observed difference
but marks interval bounds/df unavailable in that case. Ordinary intervals are
explicitly pointwise Welch-t descriptions on mouse log2(CPM+1), with fragile
n=3 distributional assumptions and no simultaneous or confirmatory coverage
claim. Focused display panels were fixed before gene outcomes; the complete
fixed panel remains visible in the full tables/heatmap. The amended prospective
design was cleared for the authorized run.

## Completed source verification and figure review

The governed run completed successfully and its receipt verified. The coordinator
reviewed the separate native-R verifier and its PASS record: original YoungD14
counts reproduce all 306 gene/state/mouse rows, and every retained YoungD14
cell's RNA total matches. Its 88 uncertainty-policy checks include 76 intervals
and 12 zero-variance cases with NA bounds; the frozen log's shorthand
"88 intervals" should be read with that distinction. All 306 eligibility rows
were checked. The Python source pass also matched every retained barcode, RNA
total and detected-feature count across all six captures.

The coordinator reused the native-R original-matrix audit after code/output
review instead of duplicating that expensive raw pass. Its repeated triplet
subsetting was slow but progressed without error; the frozen run was retained.
This verification is numerical agreement within one source, not replication.

All three measured PNGs were visually inspected: cell support, complete RNA
contrasts and individual mouse values. Labels are readable; unsupported gray
cells, units, AM_all's secondary/composition-sensitive scope and the warning
about plotted incomplete groups are visible. No figure redraw was needed.

## Biological interpretation accepted for integration

The useful population nomination is the source-labelled AM2/AM3 context in
young D14 injured mice. Their respective Arg1 UMI totals are 244/157/245 and
626/341/322, compared with 15/2/6 in AM1; the report also provides cell counts
and CPM. PBS AM2/AM3 support is insufficient, so these measurements cannot
estimate within-state induction. The larger AM_all contrast is composition
sensitive. These labels are study-specific, not automatic equivalents of
other papers' macrophage-state names or polarization classes.

Young D14 fibroblast Col1a1/Col3a1/Fn1 differences are positive at the RNA
endpoint. They do not establish deposited collagen or an ARG1-mediated route.
The late young AM1 Arg1 observation is only 3/5/2 UMIs in injured mice versus
0/0/0 controls. Offset dependence, background and sparse detection prevent a
maintained-programme or functional-persistence conclusion despite a pointwise
interval excluding zero. No post-outcome cell/gene threshold was changed.

Accept the deposit for integration at this descriptive scope. The source cannot
answer joint myeloid/matrix/epithelial resolution, and it does not remove A32's
functional hold or Speth's access hold. No claim grade or human scientific
acceptance is promoted. The [results report](../../../RQ_Specified/A32_myeloid_arg1_matrix_epithelial_recovery/reports/RESOLUTION_CONTEXT_RESULTS_V1.md)
and [execution ledger](../../../RQ_Specified/A32_myeloid_arg1_matrix_epithelial_recovery/reports/RESOLUTION_EXECUTION_LEDGER_V1.md)
own the complete outputs and required-check results.

## Integration checks

Required technical checks passed: 15,249 repository checks, research gate
against refreshed main `445a0ca`, 170 unit tests (one skipped), compilation,
claims and archived-evidence checks, and both receipt verifications. The
coordinator separately checked the Git index: all 22 frozen output, code and
contract hashes match their receipts. No published output is missing from Git.

The full staged comparison exposed eight trailing-space lines in immutable
native-R warning logs: lines 2-5 of `stderr.log` in both
`A32_resolution_metadata_v1_20261103` and `A32_resolution_context_v1_20261103`.
These are the retained locale warnings, not numerical failures. Preserve the
logs rather than rewrite execution history for cosmetic whitespace. The
handoff's earlier patch check did not cover the complete staged deposit; this
record supplies that exact exception. No attributes or validators were changed.
