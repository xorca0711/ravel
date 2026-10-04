# Wp-R3 result: deposited bulk contrasts, and how far they reproduce Table S3

Executed 4 October 2026 under the governed runner. Contract
[config/bulk_contrasts_v1.json](config/bulk_contrasts_v1.json), script
[scripts/bulk_contrasts_v1.py](scripts/bulk_contrasts_v1.py), receipt
[analysis/research/runs/wp_bulk_contrasts_v1/receipt.json](../../analysis/research/runs/wp_bulk_contrasts_v1/receipt.json),
outputs in the same run directory. `verify` returned `{"ok": true, "errors": []}`.
A successful receipt records execution, not scientific validity.

**Unit and scale.** GSE290297 deposits TPM only and carries no animal or culture
field (Wp-R0). The library is therefore the only verifiable unit, every estimate
below is library-level and descriptive, and none of it supports population
inference about mice. `Div.1` and `Total` are different gated populations and are
never pooled. Agreement with Table S3 is reproduction of the authors' own
analysis on their own deposit — not independent replication.

**Pre-registered choices** (frozen before the governed run, after dry runs that
are recorded as exposure in `REPRODUCTION_SCOPE.md`): expression on
`log2(TPM + 1)`; gene universe restricted to the per-drug universe implied by
Table S3 (EGCG 11,197 genes, DHEA 10,980); local limma-style moderated *t* with
a lowess variance trend as the primary variant; contrasts within
cell type × division gate (EGCG vs DMSO, DHEA vs Methanol); `Div.1` as the
primary gate; pathogenicity partition from DMSO Th17p vs Th17n at BH ≤ 0.05 and
|log2FC| ≥ 1.5; signatures at BH ≤ 0.05 and |log2FC| ≥ log2 1.5.

## Design recovered from the deposit

Sixteen cells of cell type × {DMSO, EGCG, Methanol, DHEA} × {Div.1, Total}, five
libraries each except Th17p/DMSO/Div.1 with four. Residual df is 8 for every
contrast except Th17p Div.1 EGCG, which has 7.

## 1. Reproduction of Table S3

Per-gene agreement with the authors' deposited statistics, primary variant:

| Our contrast | Table S3 | Pearson *r* (log2FC) | Spearman ρ | Pearson *r* (t) | Sign agreement | Our signature | Theirs | Recall of theirs | Jaccard |
|---|---|---|---|---|---|---|---|---|---|
| Th17n Div.1 DHEA | Th17n.DHEA | 0.924 | 0.976 | 0.964 | 0.937 | 718 | 958 | 0.689 | 0.650 |
| Th17p Div.1 DHEA | Th17p.DHEA | 0.920 | 0.972 | 0.976 | 0.967 | 744 | 1113 | 0.639 | 0.620 |
| Th17p Div.1 EGCG | Th17p.EGCG | 0.906 | 0.954 | 0.940 | 0.842 | 1406 | 1646 | 0.672 | 0.568 |
| **Th17n Div.1 EGCG** | Th17n.EGCG | **0.834** | 0.883 | 0.845 | 0.795 | 463 | **926** | **0.405** | 0.370 |
| Th17n Total DHEA | Th17n.DHEA | 0.675 | 0.700 | 0.805 | 0.776 | 1180 | 958 | 0.591 | 0.360 |
| Th17p Total DHEA | Th17p.DHEA | 0.654 | 0.663 | 0.754 | 0.755 | 1167 | 1113 | 0.520 | 0.340 |
| Th17p Total EGCG | Th17p.EGCG | 0.717 | 0.719 | 0.823 | 0.767 | 1185 | 1646 | 0.487 | 0.395 |
| Th17n Total EGCG | Th17n.EGCG | 0.520 | 0.466 | 0.550 | 0.650 | 656 | 926 | 0.347 | 0.255 |

Two readings follow.

**The published bulk analysis used the first-division gate.** Every `Div.1`
contrast agrees with Table S3 far better than the matched `Total` contrast
(log2FC *r* 0.83–0.92 against 0.52–0.72), and in the overlap of called genes the
sign agrees in 100 % of cases for three of the four `Div.1` comparisons. The
deposit does not state the gate used for Table S3; this is the inference the
data support, and it is consistent with the paper's emphasis on first-division
cells. `Total` remains reported as the pre-registered secondary gate.

**One of the four reproductions is materially weaker: Th17n EGCG.** We recover
463 signature genes against the authors' 926 and reach only 0.405 recall, with
the lowest log2FC correlation in the `Div.1` set. The direction is not in
dispute — sign agreement inside the called overlap is 1.00 — so this is a
sensitivity difference, not a contradiction: our moderated variance for that
contrast is the least shrunken of the eight (prior df 2.77 against 3.3–4.5),
which suppresses borderline calls. The authors' exact variance model and any
further filtering for that contrast are not recoverable from the deposit. This
is recorded as an unresolved reproduction gap, not as a failure of the paper's
claim.

## 2. Pathogenicity partition from the deposit's own DMSO arms

Th17p vs Th17n in DMSO, `Div.1` gate, EGCG universe: **99 Th17n-associated** and
**79 Th17p-associated** genes at BH ≤ 0.05 and |log2FC| ≥ 1.5 (2,284 genes pass
BH alone; 11,003 are non-significant). The `Total` gate gives 166 / 129.
This partition is internal to GSE290297 and is deliberately independent of the
Gaublomme modules used elsewhere in the package, so the module-level readouts in
section 3 are not circular with respect to Table S1.

## 3. What the inhibitors do to the two gene groups

Distribution of log2FC within each gene group, `Div.1` gate (medians; the
non-significant group is the centring control, because both drugs shift the whole
transcriptome):

| Contrast | Th17p-assoc (n=79) | Th17n-assoc (n=99) | Non-sig | Centred P | Centred N |
|---|---|---|---|---|---|
| Th17n EGCG | +0.24 | +0.32 | +0.09 | +0.15 | +0.23 |
| Th17n DHEA | +0.45 | +0.16 | +0.05 | +0.40 | +0.11 |
| Th17p EGCG | +0.80 | +0.06 | +0.12 | +0.68 | −0.06 |
| Th17p DHEA | +0.09 | +0.22 | +0.00 | +0.08 | +0.22 |

Post-hoc readout of the governed table (not a frozen endpoint): a two-sided
Mann-Whitney between the two gene groups gives *p* = 0.97 for Th17n EGCG,
4.0 × 10⁻⁴ for Th17n DHEA, 2.5 × 10⁻⁵ for Th17p EGCG and 0.22 for Th17p DHEA.

**This qualifies the paper's bulk argument in one specific place.** PGAM
inhibition in the *non-pathogenic* culture — the condition the paper's thesis
rests on — raises both gene groups by a similar amount on top of a global
upward shift, so in this deposit the Th17n EGCG effect is not selective for the
pro-inflammatory group at the module level. Selectivity is clear in two other
places: DHEA (G6PD inhibition) in Th17n, and EGCG in the already-pathogenic
culture. Individual genes behave as the paper describes in Th17n — IL17A
+1.96, IL17F +1.19, CTLA4 +1.81 and TXNIP +0.67, all BH ≤ 0.05; FOXP3 falls
−0.72 but does not pass BH ≤ 0.05 — so
the discrepancy is between single-gene and module-level readouts of the same
libraries, which is exactly the kind of disagreement the module score in
Wp-R1 has to be checked against.

Named genes, `Div.1` log2FC (`*` = BH ≤ 0.05; post-hoc readout):

| Gene | Th17n EGCG | Th17n DHEA | Th17p EGCG | Th17p DHEA |
|---|---|---|---|---|
| IL17A | +1.96* | −2.49* | −1.44* | −1.11* |
| IL17F | +1.19* | −1.34* | −2.49* | −2.57* |
| IL23R | −0.17 | −1.42* | −1.88* | −2.82* |
| IL22 | +0.64 | −1.13 | −1.82* | −2.61* |
| GZMB | −0.65 | +0.25 | −0.32 | +3.35* |
| TBX21 | −0.28 | −0.25 | −0.10 | −1.47* |
| FOXP3 | −0.72 | −0.13 | −0.17 | +0.26 |
| IL10 | +0.93 | −0.29 | +0.03 | +0.13 |
| MAF | +0.97 | +0.03 | −0.54* | −0.50* |
| CTLA4 | +1.81* | +0.03 | +0.94* | +1.39* |
| TXNIP | +0.67* | +0.17 | +1.10* | +0.30* |
| PGAM1 | +0.04 | −0.07 | −0.30* | +0.08 |
| PHGDH | −0.46* | −0.04 | −0.65* | −0.15 |
| PSAT1 | −0.29 | −0.20* | −0.45* | −0.24* |
| SHMT1 | −0.17 | −0.27* | −0.26* | −0.18* |
| SHMT2 | −0.51* | −0.35* | −0.73* | −0.36* |
| MTHFD2 | −0.26 | −0.05 | −0.39* | −0.34* |
| G6PDX | −0.09 | −0.11 | −0.30* | −0.16* |

Note the EGCG effect on IL17A reverses sign between cultures: up in Th17n,
down in Th17p. The paper's thesis is about the non-pathogenic condition, so this
is not a contradiction of it, but it does mean "PGAM inhibition increases Th17
effector output" is not a condition-independent statement in this deposit.

## 4. Direct bearing on Wp-P02 (serine / one-carbon direction)

Every measured serine-synthesis and one-carbon transcript moves **down** under
EGCG in both cultures (PHGDH −0.46*/−0.65*, PSAT1, SHMT1, SHMT2 −0.51*/−0.73*,
MTHFD2), and down under DHEA as well. Transcript abundance is not flux, and
PGAM inhibition is expected to *raise* 3-phosphoglycerate, so a coordinated
transcriptional decrease is compatible with either a feedback response to
substrate excess or a genuinely reduced pathway. It does not by itself resolve
the direction conflict with Godfrey et al. 2025 (eLife 14:RP104423), which
reports PGAM inhibition suppressing Treg via 3PG-derived serine and one-carbon
metabolism. It does sharpen the discriminating measurement named on the branch
card: labelled serine/formate flux, not expression.

## 5. Independent arithmetic check

The contrast log2FC was recomputed outside the pipeline for Th17n Div.1 EGCG vs
DMSO as the plain difference of group means of `log2(TPM + 1)`, with the library
annotation re-parsed from the GEO SOFT records rather than from the pipeline's
own parse. Maximum absolute difference across all 11,181 genes:
4.4 × 10⁻¹⁶. The BH ≤ 0.05 count recomputed from the output table (1,861)
matches the receipt's `contrast_summary`. Named spot checks: IL17A +1.956902,
TXNIP +0.672702, FOXP3 −0.723239 in both.

## 6. Limits and open items

- Library-level only; no animal field exists, so nothing here is an
  animal-level estimate.
- TPM only; no count-based model is possible on this deposit.
- The `Div.1` gate is inferred as the published gate from concordance, not
  declared by the deposit.
- Th17n EGCG reproduces least well (recall 0.405). Unresolved; attributable to
  variance modelling that the deposit does not specify.
- Sensitivity variants `sens_S3universe_notrend` and `sens_unfiltered_notrend`
  are in the run directory. The unfiltered variant gives a degenerate partition
  (one gene) and is retained only as a record of the pre-freeze exposure.
- Section 3 and the named-gene table are post-hoc readouts of the governed
  output, flagged as such; they are hypothesis-shaping, not frozen endpoints.
