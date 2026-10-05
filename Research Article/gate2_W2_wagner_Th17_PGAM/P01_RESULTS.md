# Wp-P01 result: the ranking is stable, the glucose effect is not

Executed 5 October 2026 under the governed runner. Contract
[config/score_construction_v1.json](config/score_construction_v1.json),
entrypoint [scripts/score_construction_v1.py](scripts/score_construction_v1.py),
receipt
[analysis/research/runs/wp_score_construction_v1/receipt.json](../../analysis/research/runs/wp_score_construction_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

No new expression was read: every variant the card pre-specified is a column of
the Wp-R1 per-cell output or an algebraic function of two of them. Unit: cell,
nested in 8 libraries and 2 animals. This card makes no population claim.

## 1. Cell ordering: stable to gene selection, not reducible to one arm

Th17n cells (n = 8,711), each variant against the reference score:

| Variant | Spearman vs reference | Per-library range | Cells changing tercile |
|---|---|---|---|
| Arms z-scaled before subtraction | 0.999 | 0.999–1.000 | 2.1 % |
| Locally recomputed HVGs | 0.960 | 0.948–0.969 | 14.8 % |
| Full module lists, no HVG filter | 0.924 | 0.913–0.945 | 20.8 % |
| Pro-regulatory arm alone (negated) | 0.839 | 0.817–0.862 | 29.5 % |
| Pro-inflammatory arm alone | 0.817 | 0.803–0.855 | 31.2 % |
| STAR Methods subtraction order | −1.000 | −1.000 | 66.7 % |

**The ranking is a property of the cells, within a sensitivity envelope.** Gene
selection — the choice that worried the card most, since only 63 of 116 and 30 of
68 published module genes survived an HVG filter computed on this dataset —
costs 0.08 of rank correlation and moves a fifth of cells across a tercile
boundary. That is a real envelope but not a re-ordering: reaction- and
programme-level statements can carry over if they are not sensitive at the
tercile level. Weighting barely matters (0.999).

**Neither arm substitutes for the score.** Each arm alone agrees with the
reference at only ~0.82–0.84 and moves ~30 % of cells across a tercile, so the
difference is carrying information neither arm has. The two arms are *negatively*
correlated across cells (Spearman −0.39 to −0.50 per library, −0.41 pooled) with
comparable spread (SD 0.29 vs 0.32), which is what makes the difference a
meaningful contrast at single-cell level.

That cell-level anti-correlation is worth holding against
[Wp-R3](R3_RESULTS.md), where the two arms moved *together* under EGCG in bulk
Th17n libraries. The arms oppose each other across cells within a condition and
move together under the drug — which is exactly why a single difference score
reports the EGCG effect poorly.

The STAR Methods row is not a sensitivity: a rank correlation of exactly −1
confirms the documented sign conflict inverts every cell. The figures follow the
Results text, so the Methods sentence is an error, and this run puts a number on
what accepting it would do.

## 2. Downstream statement A: N1 stays the lowest programme

Under every sign-preserving variant, N1 has the lowest median score in all four
Th17n libraries — 4/4 for each of six variants, under both the all-marker and
the overlap-excluded programme labelling, 48 checks in total. Only the inverted
Methods sign flips it (0/4, as it must). **This conclusion of the paper does not
depend on how the score was built.**

## 3. Downstream statement B: the glucose effect does depend on it

Animal-paired 1 mM − 25 mM difference in mean Th17n score, by variant:

| Variant | Mo1 | Mo2 | Pairs positive |
|---|---|---|---|
| Reference | +0.133 | +0.109 | 2/2 |
| Arms z-scaled | +0.394 | +0.346 | 2/2 |
| Pro-regulatory arm alone (negated) | +0.187 | +0.089 | 2/2 |
| Locally recomputed HVGs | +0.095 | +0.074 | 2/2 |
| **Full module lists, no HVG filter** | **+0.013** | **+0.011** | 2/2 |
| **Pro-inflammatory arm alone** | **−0.053** | **+0.020** | **1/2** |

**The direction survives; the magnitude does not.** Dropping the HVG filter
shrinks the effect roughly tenfold — from +0.13 to +0.013 — while keeping its
sign. The HVG filter was computed on this dataset, so the genes that entered the
published score are those most variable in exactly the comparison being made;
that is not circular (variability was not selected on glucose), but it does mean
the effect size is a property of the filtered gene set rather than of the
published modules.

The pro-inflammatory arm alone is inconsistent in sign across the two animals.
This is the paper's own attribution — Figure 3C assigns the glucose effect to
the regulatory arm — now confirmed from the opposite direction: the inflammatory
arm carries no reliable glucose signal at all.

## 4. What this run cannot do

The card's central worry is that the *reaction ranking* inherits any instability
of the score. That cannot be re-evaluated here: per-cell Compass scores do not
exist. [Wp-R2](R2_RESULTS.md) scored 60 micropools, did not save pool
membership, and its pooling is not bit-reproducible, so no variant score can be
projected onto those reactions. The two downstream statements above are the ones
this deposit can condition. Testing the reaction consequence would need a
re-run of Compass with pool membership saved — about an hour of solver time, and
worth doing only if a reaction-level claim is about to be carried elsewhere.

## 5. Independent check

The pooled Th17n `all_genes` Spearman correlation was recomputed outside the
pipeline directly from the Wp-R1 cell table: 0.923651 against the run's
0.923651, difference 0.0.

## 6. Limits

- Every variant uses the same expression matrix and the same cells, so agreement
  between them shows the absence of a gene-selection artefact, not independent
  evidence.
- A stable ranking does not show the score measures pathogenicity. That is a
  functional claim requiring the paper's transfer experiments.
- Two animals; the glucose rows are two numbers each, reported without a test.
- The locally recomputed HVG variant depends on our QC and cell set, which
  differ from the paper's undeposited 5,192-cell object.
