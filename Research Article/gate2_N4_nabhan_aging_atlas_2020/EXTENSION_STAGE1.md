# Nb5 biological extension stage 1

3 October 2026. The owner authorized execution after reviewing the biological
focus. This stage compares explanations for age-associated tissue RNA and
T-cell repertoire structure. All previous outcomes are exposed; this is
exploratory description, with mouse as the biological unit. No global RQ is
selected and no functional or causal claim is tested.

## P01 Within-type change and population composition

**Question and decision:** In lung FACS and bladder droplet, does the
3-to-24-month RNA contrast arise within comparable annotated types, from their
captured proportions, or both? Decide whether follow-up needs measurements
within a population, absolute population abundance, or both. Real population
redistribution is a biological alternative. Differential capture and finer
subtype mixtures remain separate observational rivals.

Use the previously fixed complete marker family, with both mean normalized RNA
and detection proportion. Four display genes are fixed before this extension:
Cdkn2a, Cdkn1a, Lmnb1 and Il1b, preserving the earlier marker questions; these
are individual RNA endpoints, not senescence or secretion scores. Keep all
other genes in the result tables. No outcome-based gene ranking or testing.

The cell universe is the set of types present in every retained 3/24-month
mouse of an assay. Retain this same universe for the male-only sensitivity.
Compare observed and standardized summaries on that common denominator;
report excluded cells and minimum cells per type separately. A single captured
cell permits a descriptive value, not precision. Each mouse has equal weight.
Use the average 3-month mouse composition as the reference, separately within
the two sex scopes. Ages are separate groups, not longitudinal observations.

For age-specific mean type weights p and type RNA values e, retain the exact
four-term accounting of the difference in equal-mouse totals:

- Composition: sum of (p_old − p_young) × e_young.
- Within-type: sum of p_young × (e_old − e_young).
- Interaction: sum of (p_old − p_young) × (e_old − e_young).
- Animal covariance: old minus young mean within-age covariation of type
  weight and type RNA. This term is required because the mean of each mouse's
  weighted expression is not generally the product of two group means.

These additive quantities are accounting terms, not causal contributions or
percentages of ageing explained. Opposing terms and small totals remain visible.
Show individual-mouse fixed-reference values and within-type estimates. Delete
each mouse once with the type universe fixed; recompute group means/reference
weights and retain every result. This assesses influence, not replication.

Kidney coverage is recorded, but whole-kidney accounting is held: the common
3/24-month set contains only B cells, T cells, lymphocytes and macrophages.
Renal epithelial remodelling cannot be answered by this restricted set. Lung
droplet lacks 24-month observations. Neither is replaced by another age after
inspecting effects. Interpretation remains within captured annotations; even
a within-type signal need not be cell intrinsic.

## P06 Local repertoire concentration and compartment representation

**Question and decision:** Do older reconstructed T-cell repertoires show more
local clone repetition within immune compartments, or does changing tissue
representation account for the pooled difference? Distinguish local repertoire
structure from compartment mixture, while retaining assembly selection and
T-cell subtype composition as rivals.

Use the verified v2 cell–mouse–tissue–source-clone table. Recompute clone sizes
within each mouse and tissue; a clone seen once in each of two tissues is
shared but not locally repeated. Missing source clone labels remain separate
singletons under the inherited definition. Retain the 11 unmatched source rows.
The table has no T-cell subtype field; tissue restriction is not subset matching.

Primary displays use thymus, spleen and marrow, chosen from anatomical context
and coverage before examining new clone outcomes: all have at least three
mouse labels per age and minimum captured counts 93, 29 and 8 respectively.
These minima are sampling depths, not power criteria. Retain all tissues in
descriptive tables and every missing stratum in coverage. Clone IDs are nested
within mouse; shared tissues never create independent replication.

Endpoints per mouse/tissue are local nonsingleton-cell fraction, fraction in a
clone observed across tissues, and four disjoint categories: animal singleton;
shared clone sampled once locally; local repetition confined to one tissue;
local repetition of a shared clone. Common-depth expectation uses the exact
hypergeometric formula at each tissue's minimum depth across all three ages.
Compute this only where every age has at least two observed mice and depth is
at least two; these are mathematical descriptive eligibility rules.

For mice with all three focal tissues, restrict the universe to those tissues.
Compare observed local-clone burden, fixed young-reference tissue composition
and equal-tissue summaries on the same mice and denominator. Apply the same
four-term accounting to 3 versus 18 and 3 versus 24 months, including every
leave-one-mouse-out value. This endpoint is local repetition in the selected
compartments, not the earlier whole-atlas pooled clonality statistic.
No p-values or effect-size acceptance threshold; no proliferation, migration,
antigen specificity or immune-function inference from these measurements.

## P02 Readiness and remaining branches

The existing layer audit and author notebook still do not establish the
all-age unintegrated expression scale of the brain figure object. The general
brain object supplies 3/24-month normalized RNA but lacks the 18-month stratum.
The notebook reads the figure object without documenting its construction.
Thus the requested distinct-state-versus-mixture comparison stays held, rather
than being replaced by another UMAP or signature-overlap audit. Exact published
cluster mapping is needed for reproduction; a separately defined biological
state analysis would still need qualified scale, animals and processing.

No new source download or biological P02 fit is part of this stage. P03/P04
transport and P07/P08 design-dependent analyses retain their existing holds.
All branches remain available. Read the prior [results](RESULTS.md),
[branch register](BRANCH_REGISTER.md) and [extension assessment](EXTENSION_ASSESSMENT.md).

## Execution and validation

Commit both hash-bound contracts and code before running the repository runner.
Check exact decomposition identities, independent count-based reconstruction,
clone partitions and a rarefaction toy by exhaustive enumeration. Preserve all
unfavorable outcomes, then render new article-style figures with short embedded
captions under a separate versioned contract. Do not overwrite previous figures.
The report will separate new biological observations, remaining rivals and the
specific independent discriminator; execution alone does not derive an RQ.
