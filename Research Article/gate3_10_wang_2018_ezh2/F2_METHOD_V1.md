# F2 Signal2Noise ranking sensitivity

12 November 2026, Asia/Seoul. This exposed descriptive adaptation asks whether
the day-four inflammatory RNA set pattern persists when the nine deposited
Treg libraries are ranked using the metric named in Wang's S3B. The outcome
is a weighted Hallmark running-sum score for deficient-minus-control relative
transcript abundance in the released libraries. Unknown mouse/pool and block
identities and the control discrepancy still bound the comparison. Culture
recovery, state mixture and genotype-linked processing remain explanations.

## F1 review checkpoint

The supervising agent reviewed [F1](F1_SOURCE_AUDIT_20261112.md) at `9d9d241`
and independently inspected all nine SRA sample-attribute and original FASTQ
filename records. The rendered publisher S3B showed Signal2Noise, phenotype
orientation and zero crossing 5609. The source review passed its documentary
scope and supported opening F2. Scientific acceptance remains unassessed.
[Prior execution review](REVIEW_20261112.md).

## Pinned method definition

On 12 November 2026 the primary GSEA User Guide and the official tagged
GSEA Desktop v3.0 Java code at `60835bf6ff0869f2072b30e0551c170dc9b319e2`
were checked. `Metrics.Signal2Noise` requires at least three observations
per group and orients the numerator toward the class of interest.
`XMath.s2n` supplies the mean branch and delegates to `Vector.stddev`.
`Vector._var` subtracts one from the denominator for unbiased variance.
The low-variance fix floors each SD at 0.20 times the absolute group mean, using 0.20
when that floor would be zero. The zero-mean adjustment affects the floor
only. The mean in the numerator remains zero. The mean, unbiased-variance
and low-variance-fix options are specified explicitly for this adaptation.
[User Guide](https://docs.gsea-msigdb.org/GSEA/GSEA_User_Guide/) ·
[v3.0 metric](https://github.com/GSEA-MSigDB/gsea-desktop/blob/60835bf6ff0869f2072b30e0551c170dc9b319e2/src/edu/mit/broad/genome/alg/Metrics.java#L335-L382) ·
[v3.0 numerator and denominator](https://github.com/GSEA-MSigDB/gsea-desktop/blob/60835bf6ff0869f2072b30e0551c170dc9b319e2/src/edu/mit/broad/genome/math/XMath.java#L622-L639) ·
[v3.0 variance and floor](https://github.com/GSEA-MSigDB/gsea-desktop/blob/60835bf6ff0869f2072b30e0551c170dc9b319e2/src/edu/mit/broad/genome/math/Vector.java#L388-L447).

For each gene and group, compute the arithmetic mean and sample SD on the
median-ratio-normalized read counts. Let `adjusted_sd = max(sample_sd, floor)`.
The ranking score is the deficient-minus-control mean difference divided
by the sum of the two adjusted SDs. Use full-precision scores and descending
signed order. The official v3.0 comparator returns equality for equal scores
and has no gene-ID secondary key. F2 keeps the S3 deterministic secondary
key of ascending Ensembl stable ID for exact numeric ties. The historical
paper does not state its Java build, original expression scale or tie order.
[v3.0 score comparator](https://github.com/GSEA-MSigDB/gsea-desktop/blob/60835bf6ff0869f2072b30e0551c170dc9b319e2/src/edu/mit/broad/genome/math/DoubleElement.java#L105-L137).

## Frozen comparison and decision

- Reuse the nine S1 library identities, raw count columns and unique-symbol
  and eligibility flags from S2, the exact S2 median-ratio factors, and the
  50 mouse Hallmarks in MSigDB 2025.1.Mm. Read the original S3 pooled and
  +/+ scores, pooled omission ranges and exact coverage from its frozen output.
- Recompute Signal2Noise for four fl/fl against five pooled controls or
  four +/+ controls. Within each comparison omit each included library once
  and recompute the means, sample SDs, floor and ranking with size factors and
  the gene universe fixed. The smallest subset group has three libraries.
  These ranges describe influence of deposited libraries.
- Apply the existing S3 weighted running sum and 10-match coverage floor.
  Absolute rank statistics serve as hit weights, so changing the metric
  can change order and weights together. Preserve all sets, memberships,
  signed scores and omission scores. Keep the displayed themes fixed to S3.
  Use the same count scale throughout with no additional transform, tests,
  permutations or normalized enrichment scores.

Agreement would support robustness to this ranking choice within the same
libraries. A reversal or omission-sensitive result would narrow the evidence
for that theme. Neither outcome distinguishes recovery and composition from
within-state regulation. Exact author replay still requires the records listed
in F1. F2 stops at review before any subsequent stage.
