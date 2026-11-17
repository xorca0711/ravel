# S5M v1: finite gene-feature RNA–TSS-proxy associations

18 November 2026. Owner `Nk17-P01`. The coordinator reviewed S3 and the
[S5 proposal](S5_PROPOSAL_V1.md), then authorized this molecular stage after S3
preservation at `8ada940`. S5F remains separate and awaits S5M result review.
All source findings and S2/S3/S4/S4B outputs are exposed; no joint association
has been calculated at this specification. A later freeze cannot erase exposure.

## Purpose, units and interpretation

The published premise links inflammatory history, chromatin, recall and repair.
S2/S4/S4B describe heterogeneous RNA effects and baseline-reference sensitivity;
S3 describes smaller aggregate D30 rank displacements with mixed directions,
library spread and width dependence. The current question is whether those
finite gene-feature descriptions align, and whether baseline subtraction or
analysis representation changes that alignment. Stable association supports a
shared-source description only; weak or sensitive association narrows that link.

The biological measurements remain separate deposited RNA/ATAC libraries with
source-reported pooling/replication and unresolved exact animals, overlap,
composition and cross-assay matching. Genes and overlapping/shared TSS proxies
are dependent features, not independent animals, cells or experiments. Unknown
processing, mixture, shared baseline and zero-tie mass are material alternatives.
Naik Figure 5c reports increased IL-1beta protein without increased Il1b transcript
(coordinator bounded primary-source read); weak RNA alignment alone cannot refute
that distinct protein/functional premise. No causal mediation or new mechanism
is estimated. Original retained domains, distal regulation and noncoding ATAC
remain outside S3's endpoint.

## Frozen joins and universes

Read only immutable S2 `gene_effects.tsv`, S4 `gene_effects.tsv.gz`, S4B
`reference_effects.tsv.gz`, and S3 `gene_window_map.tsv.gz`/`window_effects.tsv.gz`,
with M9 annotation. Join by exact versioned M9 gene IDs; never strip versions,
substitute symbols or assign nearest enhancers. Use the union of source RNA and
S3-mapped IDs for the complete gene table. Preserve every source column under its
stage prefix, all source-presence flags, annotation status and both window IDs.
The gene-by-width ATAC table keeps all original means, encoded-zero base counts,
ranks, contrasts, four-library ranges and unassayed rows. Keep all many-gene
mappings; an unassayed value is NA, never zero. Fail duplicate/inconsistent joins.

The **all-mapped sensitivity universe** requires an assayed proxy at both widths,
all three RNA source tables, and finite values for the 26 RNA measurement/scale
fields below. The **primary universe** additionally requires frozen S2
`eligible_both` and S4 `all_three_qualified`; verify their component qualifications.
Do not change existing expression thresholds or select on ATAC outcomes/zeros.
Within either universe the exact genes remain fixed across widths, normalizations,
references and association statistics. Retain noneligible genes and reasons.

RNA zero/low/regularization flags are copied unchanged. Retain each ATAC
zero-mean indicator and encoded-zero count, plus per-time any/all-zero-mean flags.
Even all-zero local means can have a nonzero rank contrast because the remaining
universe/zero-tie mass differs. These flags accompany integration; no zero-based
exclusion, correction or biological inactivity claim is introduced.

## Measurements, statistics and coupling

For each universe and ±1/±2 kb width, calculate the following 13 associations
separately under each stage's frozen MOR and total-count RNA scales:

1. S2 D6 RNA versus S3 D6 rank contrast.
2. S2 D30 RNA versus S3 D30 rank contrast.
3. S4 B0, unadjusted W6 and W12, and primary adjusted W6 and W12 versus S3 D30.
4. For each S4B reference (`c2_h2`, `c1_h1`), its B0 and adjusted W6/W12 versus S3 D30.

S2 D30 and S4 B0 reuse GSM2440989–992 under different normalization contexts.
Display both with their stage labels; never subtract across those contexts or
count them as replication. Preserve the observed source/marker discrepancy,
one-library reference limitations and absence of matching or sex assignment.

Calculate ordinary Pearson and exact-average-tie Spearman over gene features.
Shared proxies repeat an ATAC value; report gene/unique-anchor counts. The sole
weighting sensitivity is Pearson with `w_g=1/k_a`, where k_a is the number of
eligible genes sharing anchor a **within that universe**. Each anchor then has
total weight one. Weights do not remove dependence among overlapping windows.
This yields 312 declared coefficients (13 measurements × 2 widths × 2 universes
× 2 normalizations × 3 statistics), with no p-values, intervals or best setting.

For weights w (ordinary w=1 or inverse multiplicity), use
`cov_w(X,Y)=sum(w*(X-mean_w X)*(Y-mean_w Y))/sum(w)` and its variance-normalized
correlation. Spearman applies ordinary Pearson to independently average-ranked
vectors. A constant input or fewer than two features gives NA with a reason;
do not coerce it to zero or loosen eligibility. Check exact constancy before
floating-point centering. Missing/nonfinite eligible values are a failure.

For each width/universe/normalization/reference/post-wound time and each of the
two raw-value weightings, retain baseline, post-wound and adjusted covariances
and verify `cov_w(X,A_t)=cov_w(X,L_t)-cov_w(X,L0)` (96 rows). Use the frozen RNA
adjustments; do not refit them. This is an algebraic identity, not an independent
validation of the biological baseline. Correlations themselves are not subtracted.
The two adjusted times share L0 and cannot provide independent corroboration.

## Fixed displays and verification

Figure 1 shows all 312 coefficients: four panels for universe/normalization,
13 labelled measurements by six width/statistic columns, a shared −1 to +1 colour
scale and explicit gene/anchor counts. Baseline, post and adjusted rows remain
visible together; the covariance table supplies their exact algebraic components.
Figure 2 has five fixed published anchors, with separate ATAC percentile-point
and RNA log2-effect axes, all widths/normalizations/references, eligibility and
zero/low flags. No line implies matched cells, animals or time trajectories.

Anchor IDs were resolved by annotation-only M9 inspection before joint analysis:
Aim2 `ENSMUSG00000037860.15`; Casp1 `ENSMUSG00000025888.5`;
Il1b `ENSMUSG00000027398.13`; Il1r1 `ENSMUSG00000026072.12`;
Il18 `ENSMUSG00000039217.12`. Retain every anchor, including any unassayed or
unqualified status; no replacements. They are paper-selected exposed examples.

Artificial tests cover exact-ID outer joins, absent/noncoding features, duplicated
anchors, frozen qualifications, zero-mean ranks, constant inputs, ties, weighted
versus ordinary association and the shared-baseline identity. Tampered joins or
coefficients must fail independent verification. Real-run verification uses a
separate stdlib implementation to reconstruct all joins, flags, weights,
coefficients, covariance components and anchor selection from frozen sources.
Require scaled numerical agreement within `1e-10`, only a computational tolerance.
Inspect both actual figures. Preserve failures and use new versions for corrections;
do not modify frozen S2/S3/S4/S4B artifacts or rerun those biological analyses.

Return the completed S5M report for coordinator review before S5F execution.
No question/claim promotion, scientific acceptance or publication follows from
passing the runner or these arithmetic checks.

## Pre-freeze implementation check

The final artificial fixture retained 13 exact-ID gene records, including absent
RNA, an explicit missing required value, noncoding/unknown/sex-chromosome cases,
a shared anchor and a zero-mean window with a rank shift. The fixed universes
had 6 primary and 8 all-mapped genes. All 312 coefficients and 96 covariance
identities passed 8,903 independent checks (maximum scaled error `1.2213e-15`).
Tampered source-copy and coefficient fields were rejected. No real biological
input was read by these tests; the five M9 anchor IDs were checked separately
using annotation metadata only.
