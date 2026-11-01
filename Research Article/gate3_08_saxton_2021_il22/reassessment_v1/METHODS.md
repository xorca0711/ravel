# Frozen descriptive methods, version 1

1 November 2026. Owner: **Sx22-P01**. This specification implements Q1-Q4 of
the [reviewed amendment](README.md), using its [literature context](LITERATURE_CONTEXT.md)
and [technical eligibility assessment](TECHNICAL_ELIGIBILITY.md). It is exposed
shared-source reanalysis of the published WT IL-22 and engineered 22-B3 conditions
in mouse colon, six hours after administration. It does not design a ligand,
optimize an intervention or establish causal STAT activity.

## Question, unit and outcome exposure

Does the reported distinction between interferon-associated and selected
barrier-associated transcription survive an explicit overall-amplitude reference,
external IFN membership and bounded library/scale sensitivities? The competing
description is broadly weaker response with panel selection or individual-library
sensitivity. Cell composition, batches and noisy measurements remain alternatives.

The measured unit is a deposited RNA library: PBS_1/PBS_2, LH5_1/LH5_2 (WT),
LH30_1/LH30_2 (B3), displayed in that order. Original table order is preserved for
gene rows; the six named columns are explicitly reordered for display. The source
reports independent biological RNA replicates, but individual mouse/preparation,
allocation and batch keys remain unverified. Genes and overlapping sets reuse the
same libraries and are not independent biological replicates. Published outcomes,
panel memberships and previous source QC were exposed. Before this new freeze,
only metadata joins and synthetic test values were examined for the new code.
The later freeze cannot make this confirmatory or independent replication.

## Primary measurement

Preserve all 35,275 stable-ID rows and nine annotation fields in an inventory.
Validate that count and FPKM annotations agree exactly. With count C[g,j], the
denominator L[j] is the sum over **all** count rows in library j. Define
CPM[g,j] = 1,000,000 C[g,j]/L[j] and E[g,j] = log2(CPM[g,j]+1).
No gene-symbol collapse or count-row removal precedes normalization.

The fixed eligible universe is CPM >= 1 in at least two of all six libraries.
Retain all rows and values in the primary output, with an eligibility flag.
This universe is unchanged for every omission and scale sensitivity.
For each gene, x = mean(E_WT)-mean(E_PBS), y = mean(E_B3)-mean(E_PBS),
and d = mean(E_B3)-mean(E_WT). These are differences of mean log-expression,
not fitted animal-level log-fold changes or logs of arithmetic mean counts.
No p-values, FDR, confidence intervals, gene bootstrap or equivalence margin.

## Fixed memberships and coverage

[Membership manifest](sources/memberships_v1.json) fixes eight author selections:
the three literal Figure 6B groups, three 6D groups including separate Il1rn,
and the 6C/6E qPCR target lists. RNA values for qPCR targets do not reproduce qPCR.
The final supplied PDF page 9 was visually checked, with image SHA-256 recorded
in the manifest. The first-appearance order across these lists fixes the
31-unique-symbol figure; no outcome ranking is used. Category labels are source
labels, not a certification of tissue protection or inflammatory function.

Only HALLMARK_INTERFERON_ALPHA_RESPONSE and HALLMARK_INTERFERON_GAMMA_RESPONSE
from mouse MSigDB 2026.1.Mm are analyzed externally. The complete source GMT is
archived with its verified public-file hash; its other sets are not analyzed.
The source URL, version, retrieval date and exact-match metadata counts are in
the eligibility assessment. These memberships supply alternative gene selection,
not an independent biological study or a STAT-specific activity assay.

Every requested symbol gets a mapping row. Exact symbol match to one stable ID
is required; duplicate symbols are ambiguous and excluded from set summaries,
without choosing, summing or guessing aliases. Unmapped is unavailable, not zero.
Uniquely mapped but low-count members remain in mapping and gene tables and are
excluded only from medians. Each set summary is the median of its eligible,
uniquely mapped gene contrasts; report source, mapped, ambiguous, missing and
eligible counts. Empty membership gives unavailable endpoints. Report pairwise
overlap as source symbols, unique mapped IDs and eligible IDs; no independence
claim follows from different set names.

## Overall-amplitude reference

The background is the fixed eligible universe minus the union of **all** rows
matching any tested author/external membership. Even an ambiguous match is
excluded from background. This background remains fixed across views and scales.
Fit only the descriptive through-origin coefficient beta = sum(x*y)/sum(x*x).
Do not clamp beta, constrain signs, optimize filters or select a reference subset.
An empty background or zero denominator holds this component only. Record the
denominator, numerator, background count and status. The residual for a gene is
y-beta*x; each set uses the median of eligible member residuals.

Both axes share PBS and contain noise. The fit is a reference for the observed
vectors, not an errors-in-variables model, causal decomposition or statistical
test of selectivity. A positive/negative residual is only above/below that
reference in these measurements. No residual threshold certifies mechanism.

## Bounded sensitivities and figures

Run the full data and each of six single-library omissions (seven views). Every
omission retains at least one library in each group. Full data remain primary;
no library is removed from the main analysis. Report all predefined views.

Alongside raw CPM, use edgeR 4.10.5 TMM effective library sizes from all count rows
in each view: automatic refColumn=NULL, logratioTrim=0.3, sumTrim=0.05,
doWeighting=TRUE, Acutoff=-1e10. Re-estimate factors per view, with geometric mean
one, then log2(1,000,000 C/effective_size+1). Record all factors, denominators and
R/edgeR versions. Python invokes the qualified portable R in a child process;
LC_ALL=C applies to that child only. No inference/model-fitting function is used.
If that runtime cannot be qualified, record exact errors and hold TMM only.

Separately use the deposited log2(FPKM+1) values. This scale sensitivity is not a
reconstruction of unknown author preprocessing. Refit the same amplitude formula
in each scale/view, using the fixed primary background. Do not pool scales.
For every set and metric, record full-data value and observed minimum/maximum
over six omissions. Those ranges are not confidence intervals and need not
contain the full-data point. No extra sets, filters or pseudocount searches.

Three figures show (1) per-library expression and three contrasts for all unique
published targets, (2) background vectors and fixed-set residual medians, and
(3) direct-contrast and residual sensitivities. Heatmaps include below-filter
published members with an asterisk; unavailable values stay blank. Axes state
the transformed measurement. SVG trailing whitespace is normalized in memory
before the first exclusive write. All filenames are immutable run artifacts.

## Validation and stop conditions

Synthetic checks cover denominators/filter boundary, mean-log contrasts, single
omission, missing/ambiguous mapping, unclamped beta, empty summaries and local
holds, TMM identical-composition scaling, XML/whitespace and no-overwrite behavior.
Inspect synthetic figures before committing the hash-bound contract/code/tests.
Run once through the repository runner in a fresh directory. An independent
read-only calculation must verify source IDs, mapping, denominators, primary
values, all predefined contrasts/medians and omission/scale cases; inspect actual
figures before interpretation. Numerical rechecking is not biological replication.

Stop on input/hash/schema disagreement, changed membership family, nonfinite or
noninteger counts, invalid library sums or an occupied output directory. Preserve
failed receipts. Any real service restriction is recorded verbatim and stops the
affected dependent job; no context masking or replacement session. Q5 population
inference, Q6 exact author replay, Q7 signaling/function and Q8 animal-resolved
recipient/cessation/function joins retain their documented holds. Execution does
not authorize human retain/reject decisions or change scientific acceptance.
