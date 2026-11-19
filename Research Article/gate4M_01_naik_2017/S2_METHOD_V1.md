# S2 v1: finite-library acute and recovered-baseline RNA description

18 November 2026. Prospective specification, before S2 effect calculation.
The coordinator reviewed [S1M](S1M_RESULTS_V2.md), its parser and selected source
fields without requesting a revision. That review supports this scoped next
comparison; it is not human scientific acceptance. The owner authorized S2 and
local commits. Earlier service restrictions and all failed/refused attempts remain
preserved. This stage does not retry held source-method extraction.

## Purpose, comparison and units

The published premise motivates asking how acute inflammation-associated RNA
differences compare with recovered-baseline history differences. S1M established
common gene identifiers and within-time platform/layout matching, while exposing
cross-time platform/layout differences and incomplete exact pool/pairing records.
S2 will measure continuous RNA-count differences and their technical sensitivity;
it does not establish chromatin memory, isolated recovery effects or repair.

| Time and contrast direction | Exposed libraries | Controls |
|---|---|---|
| D6 acute inflamed minus control | GSM2440987, GSM2440988 | GSM2440985, GSM2440986 |
| D30 recovered-baseline prior inflammation minus control | GSM2440991, GSM2440992 | GSM2440989, GSM2440990 |

All 47,729 exact versioned gene IDs remain in the tables. D6 is **acute inflamed**,
even where original filenames use a post-inflammation label. Each group has two
deposited libraries. The reported duplicate pooled preparations remain positive
design evidence; this descriptive route neither denies that evidence nor rules
out a separately justified inferential reproduction. No animals, times or assays
are paired, and no gene is a biological replicate. No population p-values,
confidence intervals, equivalence tests or resolved/persistent classes are used.

## Normalization and contrasts

Normalize each four-library timepoint separately. Use every gene with a positive
count in all four libraries to define a geometric-mean reference. For library j,
take the exponential of the median log count/reference ratio, then divide the
four factors by their geometric mean. This explicitly fixes the factor scale
to geometric mean one. Divide counts by those factors (MOR normalized counts).
Genes excluded from factor estimation still receive normalized values.

This implements the ratio/log-median calculation documented in the
[official DESeq2 source, `estimateSizeFactorsForMatrix`](https://raw.githubusercontent.com/thelovelab/DESeq2/devel/R/core.R)
(reviewed 18 November 2026, function lines 523–565), with an explicit geometric
centering convention. It is not a DESeq2 model fit. The
[official vignette, control features section](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#control-features-for-estimating-size-factors)
explains the central-distribution assumption; broad/asymmetric expression changes
can challenge it. No invariant control genes or spike-ins are assumed here.

The sole normalization sensitivity uses total-count factors: each library's
gene-count total divided by the geometric mean of the four totals. This is CPM
rescaled to the timepoint's geometric-reference library total. Output ordinary
CPM as well. Using this reference-count scale keeps the sensitivity pseudocount
comparable to MOR units; an identical numeric pseudocount applied directly to
CPM would represent a different scale.

For each gene and timepoint, compute the arithmetic mean of the two normalized
values in each history group. The reported effect is
`log2((exposed_mean + 1)/(control_mean + 1))` under each normalization. The added
one is technical regularization in reference-count units, not an expression
measurement or biological effect margin. Also output the unregularized log ratio
where both means are positive; otherwise use explicit `NA`. Flag group-zero,
all-zero, individual-zero and group-mean-below-one cases.

Output each library value, each group's log-count range, and the minimum/maximum
of all four exposed-versus-control library log ratios. These four combinations
are a finite spread diagnostic, not matched pairs, independent replicate effects
or a confidence interval. Sign consistency across all four and normalization
sign changes are algebraic diagnostics, not biological classes.

Use `1e-10` as a computational tie tolerance for sign, equal-absolute-effect and
expression/pseudocount-boundary flags; continuous values remain unchanged. This
is the arithmetic-verification tolerance, not a biological effect margin.

## Expression qualification, summaries and displays

A timepoint is expression-qualified for a gene when CPM is at least one in at
least two of its four libraries. This is a technical expression filter that
does not use effect direction or an acute-effect rank. The primary display
universe is the **union** of genes qualified at either D6 or D30, so acute-only
and D30-only expression are retained. Report the intersection qualified at both
times as a bounded abundance-qualification sensitivity, and keep all remaining
genes and flags in the complete tables. Do not discard an unfavorable library.

Summaries for each universe include continuous effect quantiles, absolute-effect
distributions, D6/D30 profile correlation, the fraction with a smaller observed
absolute D30 effect, library spread, and normalization differences/sign changes.
Fractions summarize this feature set only, with no gene-based inference. The
zero-pseudocount context and expression-selection limitations remain visible.
No acute-ranked subset is used to estimate an overall attenuation fraction.

Three measured figures (PNG at 300 dpi and PDF) are prespecified:

1. Sample QC: count totals, detected genes, normalization factors, and Pearson
   correlation of `log2(MOR + 1)` profiles over the union-qualified genes. This
   is a diagnostic; no PCA, fixed learner axes or 500-gene subset is used.
2. Continuous effects and normalization sensitivity over the unselected
   union-qualified universe, including absolute-effect ECDFs. D6 and D30
   remain cross-sectional profiles, potentially platform/layout dependent.
3. Six illustrative finite-library displays: the maximum and minimum signed
   D6 effects, maximum and minimum signed D30 effects, greatest normalization
   discrepancy, and greatest cross-library effect range. Select a unique gene
   per slot by descending score, breaking ties by exact gene ID, taking the next
   gene if already selected. Show control-relative per-library log values within
   each timepoint; no lines imply trajectories across times. These selected
   extremes invite regression to the mean and are illustrations only, not the
   basis for attenuation proportions or functional claims.

Annotation labels use the public [GENCODE mouse M9 release](https://www.gencodegenes.org/mouse/release_M9.html)
reference-chromosome GTF. Match exact versioned gene IDs only; retain unmatched
IDs and report coverage. Parse gene names/biotypes, not sequences or operational
experimental content. Annotation does not select the analysis universe or imply
function. Source URL, acquisition time, byte count and SHA-256 are retained in
the ignored acquisition record and bound as inputs.

## Exposure, validation and decision boundary

All work is exposed description: published results/selected loci and D6 profiles
were previously viewed; S1M inspected metadata and count structure. No S2 effects
have been calculated at this specification. The new freeze does not erase prior
exposure. No new mechanistic literature claim or novelty claim is planned.

Freeze and commit the contract, numerical code, plotting code and a separately
implemented standard-library verifier before execution. The verifier rereads
the eight inputs without importing the analysis functions, independently
recomputes log-median and total-count factors, all normalized values, means,
contrasts, flags and finite-library ranges, and checks source joins. Tolerances
are computational (`1e-10` relative and absolute), not biological margins.
Stop on input/code/identifier mismatches, empty positive-reference genes or failed
verification; retain any failed receipt and use a new version for amendments.

Pre-freeze synthetic test record: the first end-to-end fixture exposed a
floating-point zero boundary (`D30_norm_sign_flip`: NumPy `True`, independent
standard-library `False`). Both implementations now apply the prespecified
computational tie rule above and retain continuous values. No research input
was read and no research run/receipt existed for that synthetic test. Its
temporary artificial fixtures were removed by the test's bounded cleanup;
the reproducible fixture generator is retained in `scripts/test_s2_pipeline_v1.py`.
The corrected synthetic pipeline passed 3,006,967 numeric/flag checks; its largest
scaled discrepancy was about `1.8e-15`. These are software-fixture results only.
The coordinator also reviewed the prospective normalization/contrast/display
logic and emphasized visible union-versus-both-time qualification and zero flags;
that review requested no additional method family and is not human acceptance.

Median-of-ratios and total-count scaling measure relative RNA, not absolute RNA
abundance. Platform/layout, cell composition and sparse preparations remain
consequential alternatives. Smaller D30 effects alone do not establish return to
baseline, equivalence or a within-cell recovery trajectory. Mixed, unfavorable
and normalization-sensitive patterns must remain in the result.

After receipt verification/registration and figure inspection, update the current
interpretation and propose the next bounded S3 or S4 decision. Stop for parent
review after S2; the overall plan remains unfinished. No external publication,
contact, protection change or human scientific acceptance is authorized here.
