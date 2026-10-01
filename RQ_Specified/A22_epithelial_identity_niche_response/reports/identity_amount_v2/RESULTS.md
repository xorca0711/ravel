# A22 extension: identity versus amount-related proxies

**1 October 2026.** Same-screen exploratory P2 analysis executed. The owner
requested structuring and execution; scientific retain/reject remains pending.
[Contract](../../config/identity_amount_v2.json) | [Receipt](../../metadata/identity_amount_v2/run_record.json) | [Figure](../../FIGURES.md).

## Finding and hypothesis consequence

The inherited AT2 identity score adds little to prediction of fibroblast
chemokine RNA in this screen and fails the whole-plate diagnostic. The focal
NKX2-1 result remains motivating, but these data do not support extending it
into a general identity-to-chemokine rule beyond the nominated amount/depth proxies.
This is a limitation of an operational linear predictor, not evidence that
identity has no biological role or that epithelial abundance causes the response.

## Population and design

The exact library joins recover 771 paired-species QC wells from 886 imaging
rows. Removing 99 TIGIT/TDTOMATO control wells leaves **672 wells and 201 targets**;
one excluded control also has invalid imaging. All noncontrol paired wells pass
the complete-imaging gate. Target and plate labels agree across all joined tables.
Controls are excluded from fitting and evaluation, and no shared-control
contrast or test-outcome centering is used. SFTPD is the sole targeted gene
that overlaps the four-gene identity panel; its exclusion is reported below.

Baseline features are day-7/day-14 deposited mean-area and area-proportion
statistics, log1p organoid counts, and log2 mouse/human read totals. Identity is
the inherited mouse AT2 panel; the primary response is the inherited human
seven-chemokine panel. Training gives each target total weight one. OLS
standardization uses training data only. Target holdouts include plate indicators;
whole-plate holdouts omit them and purge any test target also on a training plate.
All 36 folds across the four variants pass target-coverage and model-rank gates.

Day-14 RNA and imaging are concurrent; day-7 imaging is also post-perturbation.
Imaging is not a viable-cell measurement, and adjusted variables can themselves
be consequences of treatment. Inherited whole-screen TMM normalization was not
recomputed inside folds: held-out count distributions have already contributed
to upstream processing. These are retrospective diagnostics conditional on that
processing, not clean external or prospective validation. Wells/targets do not
supply independent preparation-level replication.

## Held-out results

Positive values below mean lower equal-target mean squared error after adding
identity. Negative values mean worse prediction. No biological p-values,
confidence intervals or effect-size threshold are attached.

| Population | Target holdout | Whole-plate shift |
|---|---:|---:|
| All eligible targets | +0.64% | -35.00% |
| Without NKX21 | -0.97% | -35.46% |
| Without SFTPD | +0.62% | -34.86% |
| Without NKX21 and SFTPD | -0.95% | -35.30% |

Primary equal-target RMSE changes from **0.7715 to 0.7690** for target holdouts
and **0.9515 to 1.1056** for plate shifts, in mean-log2(TMM CPM + 0.5) panel-score
units. Only two of five primary target folds improve. All four primary plates
worsen: error reductions are −12.94%, −34.15%, −6.86% and −63.95% for plates
1–4. Excluding NKX21 does not restore plate generalization.

The secondary wound-marker panel also worsens: −0.39% in target holdouts and
−25.56% in plate shifts. It does not rescue the primary chemokine result or
measure fibrosis. Full variant/fold/target errors are retained in the
[metrics](../../tables/identity_amount_v2/metrics.tsv),
[predictions](../../tables/identity_amount_v2/predictions.tsv) and
[target-error table](../../tables/identity_amount_v2/target_errors.tsv).

## Strict review and next discriminator

| Prediction | Decision after this extension |
|---|---|
| NKX2-1 perturbation changes fibroblast chemokine RNA locally | Original Nb3 evidence retained; this extension is not an independent perturbation replication |
| AT2 panel adds broadly useful information beyond these proxies | Weakened by negligible target-holdout gain, loss after NKX21 omission and worse error on every primary held-out plate |
| Identity instructs a response within a fibroblast state | Not tested by bulk mixed-culture RNA |
| Altered secretion changes a defined recipient function | Not tested; RNA cannot supply protein or recruitment |

**Conditional candidate, related to A22 H2/E7:** a specific NKX2-1-associated
epithelial signal may affect chemokine output within a defined fibroblast state.
Its mediator and identity specificity remain unknown. Prioritize independently
measured epithelial/fibroblast amounts and state abundance, followed by
attributed secreted output. A within-state response must be separated from
state selection; linked temporal or lineage information is required to distinguish
those processes. P3 requires reconciled spatial design; P4/P5 still need eligible
independent perturbation and protein/function sources. More broad pathway
screening cannot resolve these missing measurements.

## Preserved amendment and reproduction

Version 1 regrouped targets into five folds after each target exclusion. That
made exclusion comparisons depend on fold changes as well as omission. The
[v2 amendment](../../config/identity_amount_v2.json), committed before the new
fits, freezes the complete primary target assignment across all variants.
Primary results are unchanged; the v1 contract, script, tables and receipt remain
archived. The current figure uses v2 only. Initial figure renders are also retained;
the layout-v2 render moves legends away from data, with no numerical change.

Run `scripts/02_identity_amount_v2.py` from this workspace only in a fresh copy
without its output directories; it refuses overwrites and needs NumPy plus the
tracked inputs. Verify an existing checkout with
`python analysis/scripts/verify_a22_a23_extensions.py` from the repository root.
`--with-raw` additionally reconstructs one model fold independently and verifies
A23 raw counts using the scientific environment. The earlier v1 is reproducible
with `scripts/01_identity_amount.py`. Figure builders are under `analysis/scripts/`.
