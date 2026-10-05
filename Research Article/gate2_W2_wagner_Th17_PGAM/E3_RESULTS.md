# Wp-E3 result: the global shift is not a stress response — it is effector gain against biosynthetic loss

Executed 5 October 2026 under the governed runner. Contract
[config/e3_global_shift_v1.json](config/e3_global_shift_v1.json), entrypoint
[scripts/e3_global_shift_v1.py](scripts/e3_global_shift_v1.py), receipt
[analysis/research/runs/wp_e3_global_shift_v1/receipt.json](../../analysis/research/runs/wp_e3_global_shift_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

**This candidate was wrongly excluded.** The [pre-RQ checkpoint](PRE_RQ_EVIDENCE.md)
dropped E3 on the ground that a negative result would be uninterpretable,
because TPM renormalisation alone can produce a transcriptome-wide shift and the
deposit has neither counts nor spike-ins. That reason does not hold: a
compositional effect is a **function of a gene's expression level**, so a null
drawn with the gene set's own expression-decile composition absorbs it. The
analysis below is the corrected version.

Unit: library. GSE290297 declares no animal field, so nothing here is
animal-level inference.

## The confound is real, and it is bounded

Median log₂ fold change by expression decile, Th17n EGCG, centred on the
non-significant genes:

| Decile (mean AveExpr) | 0 (0.4) | 2 (1.9) | 4 (3.4) | 6 (4.7) | 8 (6.5) | 9 (8.4) |
|---|---|---|---|---|---|---|
| Centred median | −0.03 | **+0.06** | +0.05 | +0.01 | −0.03 | **−0.07** |

The shift *is* expression-dependent: Spearman between decile rank and median is
−0.58 for both EGCG arms and −0.81 to −0.92 for the DHEA arms. Highly expressed
genes move down relative to the middle of the distribution, which is the
signature of renormalisation against a fixed total. But the whole excursion
spans about 0.13 log₂ units, so the confound sets the scale a programme must
beat — not a reason to abandon the question.

## What exceeds the expression-matched null

Th17n EGCG, division-1 gate. Centred median log₂ fold change per programme,
with the 95 % interval of 1,000 random sets matched on size **and** expression
decile:

| Programme | Genes | Centred median | Expr-matched 95 % | p |
|---|---|---|---|---|
| **Th17 effector** | 9 | **+0.54** | −0.18 to +0.18 | **0.000** |
| Cholesterol / SREBP | 12 | +0.11 | −0.14 to +0.12 | 0.062 |
| Hypoxia / HIF | 9 | +0.13 | −0.15 to +0.16 | 0.103 |
| Unfolded protein response | 13 | +0.06 | −0.16 to +0.09 | 0.121 |
| OXPHOS subunits | 97 | −0.03 | −0.10 to −0.02 | 0.218 |
| Heat shock | 56 | +0.03 | −0.07 to +0.06 | 0.372 |
| Amino-acid transport | 9 | −0.08 | −0.18 to +0.18 | 0.358 |
| NRF2 / oxidative stress | 13 | −0.07 | −0.15 to +0.14 | 0.419 |
| Glycolysis | 15 | −0.05 | −0.15 to +0.08 | 0.903 |
| **Ribosomal proteins** | 93 | **−0.21** | −0.11 to −0.02 | **0.000** |
| **Cell cycle** | 16 | **−0.26** | −0.17 to +0.03 | **0.000** |
| **Serine / one-carbon** | 13 | **−0.30** | −0.17 to +0.09 | **0.001** |
| **Histones** | 61 | **−0.47** | −0.05 to +0.08 | **0.000** |
| **Integrated stress response** | 13 | **−0.49** | −0.15 to +0.14 | **0.000** |

**The global shift is not a stress programme.** The integrated stress response
is the single most *downregulated* programme (−0.49), and the unfolded protein
response, NRF2 and heat-shock sets do not move at all. The one programme moving
up beyond its null is the Th17 effector set itself (+0.54), against a
coordinated fall in biosynthetic and proliferative capacity — histones,
ribosomal proteins, cell cycle, serine/one-carbon.

That is a recognisable cellular state: effector output rising while growth
machinery contracts. It also explains the Wp-R3 non-selectivity from the other
side. Both pathogenicity gene groups rose under EGCG in Th17n because the
pro-regulatory group is not what is falling — what falls is the biosynthetic
apparatus, which sits in neither group.

## Bearing on the Wp-P02 stress arm

The paper's Discussion proposes that glycolysis blockade promotes Th17 effector
function by activating cellular-stress TGF-β signalling networks. Two lines
already weigh against the premise: the cited stress paper reports stress
*substituting* for TGF-β rather than activating it (recorded on
[the branch card](branches/P02_serine_one_carbon_direction.md)), and now the
authors' own bulk libraries show the integrated stress response moving **down**,
not up, under EGCG — in both cultures (−0.49 in Th17n, −0.60 in Th17p, both
beyond their nulls).

A transcript module is not signalling activity, and a fall in ISR transcripts is
compatible with a transient earlier activation that has resolved by the
sequencing timepoint. But the stress arm now has no supporting evidence in this
deposit and one line against it, which is a stronger position than the
"unverified premise" it previously held.

## Where the serine arm sits

Serine and one-carbon genes fall beyond their expression-matched null (−0.30,
p = 0.001) — and are also one of the two highest-expressed sets tested (median
AveExpr 7.2 against 3.7 for the universe), which is why the matched null
matters here more than anywhere else. The size-matched null would have called
this at p = 0.000; the expression-matched null still calls it, so the
[Wp-R3 serine observation](R3_RESULTS.md) survives the confound that could most
plausibly have produced it.

## Cross-arm comparison

| Programme | Th17n EGCG | Th17n DHEA | Th17p EGCG | Th17p DHEA |
|---|---|---|---|---|
| Th17 effector | **+0.54*** | **−1.18*** | **−0.73*** | **−1.12*** |
| Integrated stress response | **−0.49*** | **+0.34*** | **−0.60*** | −0.15 |
| Histones | **−0.47*** | **−0.26*** | **−0.60*** | −0.05 |
| Serine / one-carbon | **−0.30*** | −0.15 | **−0.50*** | −0.15 |
| Ribosomal proteins | **−0.21*** | +0.01* | **−0.35*** | +0.07* |
| Glycolysis | −0.05 | +0.14* | **−0.32*** | +0.18* |

(`*` = exceeds its expression-matched null.) Th17n EGCG is the only arm of the
four in which the effector programme rises; in the other three it falls, by
0.73 to 1.18. And the stress response moves in **opposite** directions under the
two drugs in Th17n: down under EGCG, up under DHEA. Whatever EGCG does in
non-pathogenic Th17 cells, it is not the same cellular response that G6PD
inhibition produces in the same cells.

## Independent arithmetic check

The integrated-stress-response centred median was recomputed outside the
pipeline directly from the frozen Wp-R3 contrast table, with the gene list read
back from the run's own membership file and the centring base recomputed from
the partition table: −0.49091606 against the run's −0.49091606, difference
exactly 0, over 13 mapped genes with base +0.091796.

## Limits

- Library-level on deposited TPM with no animal field; no animal-level or causal
  inference.
- Programme membership is a declared gene list, not measured pathway activity,
  and the sets overlap by design (MTHFD2 and SHMT2 sit in both the stress and
  serine sets); the overlap is reported, not resolved.
- A transcript shift is not flux or protein. The ISR result constrains the
  stress arm's premise; it does not measure signalling.
- The expression-matched null absorbs a compositional effect but cannot exclude
  a genuine global response that is itself expression-dependent.
- Five libraries per arm; empirical p values describe the gene-set draw, not
  sampling of mice.
