# A30 erratum: the CP10K denominator, and a null too coarse to decide 0.05

> **Interpretation review, 7 October 2026:** the saved v3 values verify, but the Monte Carlo/BH argument, regulatory-equivalence wording and composition percentage require the qualifications in the [PR140 audit](../../docs/audits/2026-10-07-pr140/REPORT.md). Counts match; barcode identity was not verified. This historical erratum is retained and does not override the [current A30 baseline](../../RQ_Specified/A30_csf_compartment_effector_state/EXTENSION_BASELINE_V2.md).

This supersedes the **reported values** of `wp_a30_activation_stratified_v2` and
`wp_a30_state_decomposition_v2`. It does not withdraw them, change A30's
registered design, or propose a grade. Both predecessor runs and their receipts
are preserved and remain readable.

## 1. What was wrong

**The denominator.** Both v1 and v2 formed CP10K by dividing each cell by the
row sum of the **loaded gene subset** rather than by its all-gene library size.
A score therefore depended on which *other* gene sets happened to be loaded in
the same run. The all-gene library size was already computed in the first pass
over each matrix and simply was not used. The defect was declared in §5 of
`RQ_Specified/A30_csf_compartment_effector_state/RESULTS.md` at the time, with
the note that it should be fixed before any future run; it is fixed here.

In `a30_state_decomposition_v2` the inconsistency was internal to one run: the
clustering matrix `F` was correctly divided by the all-gene library size, while
the scoring matrix `X` was not. States and the scores they carried were
normalised on two different conventions.

**The null was too coarse to decide the threshold.** With 1,000 matched random
sets, the Monte-Carlo standard error near the observed empirical p is about
0.006. The v2 BH values were 0.063 to 0.068, i.e. 0.013 to 0.018 from 0.05 —
inside two standard errors. Re-running v2's exact configuration with only the
draw seed changed moved its BH values from 0.063 to 0.088. **v2 could not place
the result on either side of 0.05, and the "short of threshold by precision"
reading it was given was not supportable.** v3 uses 10,000 draws, for a
standard error near 0.001.

## 2. What changed, and what did not

| | v2 | v3 |
|---|---|---|
| CP10K denominator | loaded gene subset | all-gene library size |
| matched random sets | 1,000 | 10,000 |
| cells analysed | 35,928 | 35,928, per-unit identical |
| design, panel, strata, floor, family, stop rule | — | unchanged |

The 21-gene activation panel, the three global tertiles, the 50-cell floor, the
six-test primary family and the stop rule are untouched. Cell recovery against
`wp_human_signature_transfer_v2` is asserted by the run and identical.

## 3. The numbers

Pro-inflammatory module (authors' HVG form), paired CSF minus blood:

| stratum | v2 median | v3 median | v2 empirical p | v3 empirical p | v2 BH | v3 BH |
|---|---|---|---|---|---|---|
| act1 | +0.0549 | +0.0558 | 0.034 | 0.0098 | 0.068 | **0.032** |
| act2 | +0.0561 | +0.0498 | 0.018 | 0.0184 | 0.063 | **0.037** |
| act3 | +0.0551 | +0.0570 | 0.021 | 0.0107 | 0.063 | **0.032** |

Donors positive: 9/9, 10/10, 9/9. The **effect size barely moves**; what moves
is its position against the matched null. Scored against a correct denominator
the same difference sits further into the tail, and at 10,000 draws that
position is resolved to about ±0.001 rather than ±0.006.

So the pro-inflammatory elevation **is below BH 0.05 in all three activation
strata**. The v2 statement that it fell short of threshold was an artefact of
the normalisation error compounded by an under-powered null.

Pro-regulatory module: flat in v3 as in v2 — +0.0066, +0.0115, +0.0049, donors
positive 6/9, 7/10, 6/9, BH 0.817 throughout. **The regulatory half of A30 is
unchanged by the correction.**

Activation-stratum decomposition (pro-inflammatory, authors' form), medians over
10 donors:

| | total | composition | within-state | within sign |
|---|---|---|---|---|
| v2 | +0.0710 | +0.0063 | +0.0595 | 10/10 |
| v3 | +0.0618 | +0.0069 | +0.0496 | 10/10 |

The split is qualitatively unchanged: the paired difference is carried by the
within-state term, not by redistribution across activation strata.

De novo state decomposition (`wp_a30_state_decomposition_v3`), Leiden on 2,000
HVGs selected from the full 33,480-gene shared space minus both modules and the
activation panel:

| | states | total | composition | within-state | within sign |
|---|---|---|---|---|---|
| v2 | 23 | +0.0710 | +0.0275 (38.7 %) | +0.0400 (56.3 %) | 8/10 |
| v3 | 23 | +0.0618 | +0.0240 (38.8 %) | +0.0374 (60.5 %) | 8/10 |

The v3 contract recorded a prediction before execution: because the clustering
matrix was already normalised correctly, the states should be nearly identical
and only the means they carry should move. **That prediction held** — the same
23 states, and the composition share moves by 0.1 percentage points. The
mixture-shift reading of A30 §2 therefore stands on its own and was not an
artefact of the denominator.

## 4. A correction that cuts against the hypothesis

The activation score is the positive control: if stratifying worked, activation
should be flat *within* each stratum. On the primary matched-null test it is —
empirical p 0.70, 0.71, 0.59. But the Wilcoxon signed-rank p is **0.039, 0.037
and 0.164**, against 0.098, 0.065 and 0.106 in v2. Once scores are computed on a
correct denominator, a small sign-consistent activation difference survives
inside two of the three strata.

The claim that A30 can make is therefore weaker than "activation excluded".
Stratification **reduces** the activation difference from the +0.109 Wp-M3
reported for the unstratified comparison to about +0.008, but does not abolish
it, and the two tests of that residual disagree. Both are now reported.

## 5. Scope and what is still not addressed

- The stratified entrypoint's *internal* de novo clustering records itself as
  unavailable under a Windows kNN-backend permission error in **both** v2 and
  v3, so v3 is faithful to v2 on that point. The authoritative de novo state
  decomposition is `wp_a30_state_decomposition_v3`, which pins the exact
  scikit-learn neighbour backend and single-threaded pools, and which is
  re-run here for the same denominator reason.
- The outcome of this correction was **exposed before the contract was frozen**:
  a workspace rescan of the corrected denominator and a second draw seed was run
  and read first. Both v3 contracts record that. v3 therefore puts a known
  correction on the governed record at adequate precision; it carries no
  confirmatory weight, and A30's grade remains the owner's.
- Ten paired donors, no age, sex, treatment or disease-duration field, RNA not
  protein, one evidence lineage shared with the source paper and with Schafflick
  et al. 2020. None of that changes. Residency and recirculation remain
  unaddressed by any A30 output, because they need shared-clone comparison
  across compartments that this deposit cannot supply.

## 6. The general lesson for this package

Two independent parameters decided a registered outcome here: a normalisation
denominator and a Monte-Carlo draw count. Neither is a scientific choice, and
neither appeared in the result's interpretation until it was checked. A run
whose reported BH value sits within two Monte-Carlo standard errors of its
threshold has not measured which side of the threshold it is on, and should say
so rather than choose a side.
