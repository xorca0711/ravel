# Prospective RNA description, version 1

8 November 2026. Sx10-P01. Fixed Figure 5A/B source description and bounded
response-pattern analysis under the [staged plan](../../docs/research_reviews/2026-11-08-saxton-reading/IL10_ANALYSIS_PLAN.md)
and [literature context](LITERATURE_CONTEXT.md). Published outcomes, source QC,
annotation and target eligibility are exposed. No matrix treatment contrasts
were inspected before this specification. This is not confirmation.

## Inputs, units and selection

GSE160332 count/FPKM files are aligned by exact unique stable ID; the metadata
v1 failed row-order assertion is preserved, and v2 proved identical keyed
annotations. All 58,735 rows and eight libraries remain. Human donor/preparation
IDs and pairing are unknown despite the paper's two-biological-replicate statement.
The descriptive unit is a deposited library; genes are features, not replicates.
Order: Unt_1/2=PBS, BS30_1/2=WT, BS65_1/2=10-DE, BS45_1/2=super-10.

Normalize primary CPM by sums over all raw count rows. Eligibility is full-data
CPM >=1 in at least two libraries, fixed for all cases: 12,677 rows. This reuses
the prior Saxton description's technical filter, not a biological effect margin,
power calculation or target-specific tuning. Source Figure 5A has 23 unique
exactly mapped symbols; IL2 alone fails eligibility and remains visible but
excluded from panel medians. Figure 5B's eight targets are all eligible and wholly
contained in 5A. Preserve the two 5A source direction groups separately.

## Measurements and bounded sensitivity

Primary E[g,j]=log2(CPM[g,j]+1). Five contrasts are differences of group means:
WT-PBS, DE-PBS, SUPER-PBS, DE-WT and SUPER-WT. These are not fitted population
log-fold changes. Display all 23 targets and all eight per-library values; retain
all-row primary values and contrasts for independent arithmetic checks.

Three scales, each with full data and every single-library omission (27 cases):
primary CPM; median-ratio count-normalized CPM (**MR_CPM**); deposited FPKM.
Each scale uses log2(value+1), hence distinct abundance/pseudocount meanings.
For MR_CPM, use only rows positive in every retained library to define per-gene
geometric means. Take each library's median count/geometric-mean ratio; rescale
these factors to geometric mean 1. Its effective denominator is that factor
times the geometric mean of retained raw library sums. MR_CPM=count/denominator
×1e6. Re-estimate factors/reference for each omission; do not change eligibility.
Record the factors, denominators and positive reference counts. This uses the
median-ratio normalization principle ([primary methods](https://doi.org/10.1186/gb-2010-11-10-r106));
it does not execute DESeq2, fit dispersion or import DESeq2 inferential claims.
Broad asymmetric RNA changes can violate relative normalization assumptions.

The existing portable R library was probed before freeze, but this session's R
runtime did not resolve edgeR despite its directory being present. No numerical
TMM analysis was attempted. MR_CPM is the chosen pre-outcome count-normalization
sensitivity; no package install or post-result method selection is required.

Define background as the fixed eligible rows excluding every Figure 5 target
match (12,655 rows). For each variant separately, x=WT-PBS, y=variant-PBS,
beta=sum(x*y)/sum(x*x), through the origin, without clipping or selecting genes
on x. Gene residual=y-beta*x. Report beta, denominator and RMS residual. This
is a noisy-axis amplitude reference with a shared PBS control, not a causal
parameter, explained fraction, likelihood model or independent validation.

For each fixed panel report median x, y, direct variant-WT and residual, plus
member counts: abs(y)<abs(x) (closer to PBS), x*y>0 (same direction), their
intersection (weaker same direction), and x*y<0 (opposite). Exact zero is neither
same nor opposite; no numerical effect margin is invented. Opposing source
directions are not combined into a functional score. Figure5B is shown as a
selected mixed panel; its aggregate does not represent inflammation or function.
Retain every gene/case and omission minimum/maximum. No p-values, CIs, FDR,
bootstraps, donor pairing, sample exclusion or additional gene-set search.

## Figures, verification and decision

Three figures: all source-target library values with five full-data contrasts;
two variant-versus-WT response scatterplots; fixed Figure5B direct contrasts and
all eight omission ranges across three scales. Source order is fixed, not ranked
by result. Range lines are not CIs. Test proportional-library normalization and
known contrasts before freeze. Independent scalar verification reconstructs
raw joins, normalization, all target/case endpoints and plotted ranges without
importing production code; visual inspection checks labels and bounds.

Broadly weaker 10-DE responses support finite-library attenuation; mixed super-10
effects oppose uniform amplification. Panel/library dependence limits fidelity.
No outcome substitutes for raw signaling/function or verifies donor independence.
Population inference remains held. Exact author replay also needs S9 and precise
display processing. Fail on input/code hash mismatch, invalid matrices or changed
mapping; preserve every failed run and negative result. Missing source evidence
holds only its dependent inference, not completed valid library descriptions.
