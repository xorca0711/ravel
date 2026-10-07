# Wp-M result: three phenotypes in metadata the package had not used

**Supersession — 7 October 2026:** the [versioned correction report](CORRECTIONS_2026-10-07.md) owns current Compass and human-score interpretation. The numerical values and conclusions below describe the earlier run and must not be reused as current corrected evidence. Original contracts, scripts, receipts and tables are preserved.

> **Naming correction, 5 October 2026.** This work was first committed as
> `E_RESULTS.md` with sections labelled E-B1 to E-B3, which wrongly implied the
> extension candidates E1 to E9 of the
> [pre-RQ checkpoint](PRE_RQ_EVIDENCE.md) had been executed. They had not. This
> is separate work on unused metadata fields, now labelled **Wp-M1 to Wp-M3**;
> the real [E3](E3_RESULTS.md) and [E5](E5_RESULTS.md) were executed afterwards.

Executed 5 October 2026 under the governed runner. Contract
[config/metadata_phenotypes_v1.json](config/metadata_phenotypes_v1.json),
entrypoint [scripts/metadata_phenotypes_v1.py](scripts/metadata_phenotypes_v1.py),
receipt
[analysis/research/runs/wp_metadata_phenotypes_v1/receipt.json](../../analysis/research/runs/wp_metadata_phenotypes_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

## Why these three, and how they relate to the E list

The [pre-RQ checkpoint](PRE_RQ_EVIDENCE.md) listed nine candidates. Three of
them — E1 (does score instability reach the reaction ranking), E2 (is the
composition term a label-boundary artefact) and E4 (name the human batch axis) —
are **validation or technical-artefact work**: each asks whether a number we
already reported is an artefact of a method choice. They were excluded, and the
reason matters: a package that keeps auditing its own estimators stops producing
biology. **E3 was also excluded here and that was wrong** — the exclusion
argued its negative would be uninterpretable because TPM renormalisation can
produce a transcriptome-wide shift, but that confound is a function of
expression level and is absorbed by an expression-matched null. E3 has since
been executed under its own contract; see [E3_RESULTS.md](E3_RESULTS.md).

What is left is the question of which **deposited metadata fields were never
used as biological variables at all**. The deposits declare exactly these:

| Deposit | Declared biological fields | Used by Wp-R1 … Wp-P03 |
|---|---|---|
| GSE290297 bulk | cell type, treatment, **divisions** | cell type, treatment; `divisions` only as a gate sensitivity |
| GSE289733 single cell | cell type, glucose, animal | all three |
| GSE138266 human | donor, **tissue**, disease | donor, disease; `tissue` reported but never tested for specificity |

So `divisions` and `tissue` are unexploited, and `treatment` has never been read
as a **drug-class** variable — EGCG and DHEA were each compared to their own
solvent and never to each other. Those are the three analyses below.

## Wp-M1. Both inhibitors restructure, rather than remove, the transcriptional distinction between first-division cells and the bulk population

The paper gates on division-1 cells to control for proliferation. Treating that
gate as a readout instead: within one treatment arm, Div.1 minus Total is a
*gate signature* — what separates a just-divided cell from the whole population.
Four arms per cell type give four such signatures from disjoint library groups.

Pairwise agreement of gate signatures (Pearson, per cell type):

| Comparison | Th17n | Th17p |
|---|---|---|
| **Vehicle vs vehicle** (DMSO vs Methanol) | **+0.40** | **+0.48** |
| Drug vs drug (EGCG vs DHEA) | +0.22 | +0.16 |
| DMSO vs EGCG | −0.08 | −0.02 |
| DMSO vs DHEA | −0.16 | −0.13 |
| Methanol vs EGCG | +0.02 | −0.05 |
| Methanol vs DHEA | −0.06 | −0.16 |

**The two vehicle arms agree with each other at +0.40 and +0.48.** That is the
measurement ceiling, from five libraries per group, and it establishes that a
division-linked signature is reproducibly measurable in this deposit. Against
that ceiling, every drug-versus-vehicle comparison is at or below zero: the gate
signature under either inhibitor carries no relationship to the gate signature
under vehicle. The two drugs agree with each other only weakly (+0.16, +0.22),
below the vehicle ceiling.

This is the clean form of the result, and it is not what the first draft of the
analysis said. The original metrics correlated the drug effect, and the
drug-minus-vehicle interaction, against the vehicle gate signature, and returned
−0.06 to −0.82. Those quantities **share solvent libraries** with the vehicle
gate signature, so a large negative correlation was partly algebraic. Every
correlation above is built from disjoint library groups, and the interaction term
is reported as a distribution only (SD 0.26–0.31 log₂ units). The correction is
recorded in the contract's exposure record.

**Reading.** Division history leaves a reproducible transcriptional mark in
vehicle-treated Th17 cultures, and PGAM inhibition or G6PD inhibition replaces it
with a different one. The signature does not shrink — its spread under drug
(SD 0.146-0.187) is comparable to vehicle (0.176-0.232); what falls to
approximately zero is its agreement with the vehicle signature.
The drug effect itself is *not* gate-specific — the EGCG effect in Div.1 and in
Total correlate at 0.57 (Th17n) and 0.80 (Th17p), with comparable median
magnitudes — so the inhibitors are not acting only on recently divided cells.
What changes is the *structure*: whatever distinguishes a first-division cell
from the bulk under vehicle is no longer the thing that distinguishes it under
either drug.

This also qualifies the paper's own design choice. Gating on division 1 is only
a control for proliferation if the gate means the same thing in treated and
untreated cultures, and in this deposit it does not.

## Wp-M2. PGAM and G6PD inhibition do not converge, and their cell-type selectivity is reciprocal

EGCG (PGAM) and DHEA (G6PD) block two branches leaving the same
hexose-phosphate pool. Comparing their effects directly, within cell type and
gate, on shared genes:

| Cell type | Gate | Pearson | Concordant genes | Discordant |
|---|---|---|---|---|
| Th17n | Div.1 | 0.35 | 104 | 11 |
| Th17n | Total | 0.50 | 328 | 11 |
| Th17p | Div.1 | 0.41 | 349 | 26 |
| Th17p | Total | 0.46 | 403 | 26 |

Correlations of 0.35–0.50 are modest: the two inhibitors share a substantial
component but do not produce one phenotype. Discordant genes are few (11–26),
so the shared component is real rather than cancelling.

The sharper result is in the pathogenicity gene groups, centred on the
non-significant genes so the global shift is removed (division-1 gate):

| | EGCG on Th17p-assoc | DHEA on Th17p-assoc |
|---|---|---|
| In Th17n cells | +0.15 | **+0.40** |
| In Th17p cells | **+0.70** | +0.08 |

**The selectivity is reciprocal.** In the non-pathogenic culture it is DHEA, not
EGCG, that selectively raises the pathogenic gene group; in the already
pathogenic culture it is EGCG, not DHEA. Each inhibitor's module-level
selectivity appears in the cell type where the other's does not.

This matters for the paper's thesis, which rests on EGCG in Th17n, one of the
two cells of this 2 × 2 where the module-level effect is *not* selective — the
other being DHEA in Th17p (+0.082 on Th17p-associated genes against +0.217 on
Th17n-associated, i.e. reversed)
([Wp-R3](R3_RESULTS.md), [Figure 2](FIGURES.md#figure-2-in-th17n-pgam-inhibition-moves-both-gene-groups)).
The single genes still move as published; it is the module readout that does not
distinguish EGCG's effect in Th17n from a transcriptome-wide shift, while DHEA's
in the same cells does. The caveat is that the two drugs have different solvents
(DMSO and methanol), so a solvent-specific contribution cannot be excluded from
the comparison.

## Wp-M3. In human CSF, the pro-inflammatory arm is specifically elevated — and the pro-regulatory arm is not

[Wp-R4](R4_RESULTS.md) found several scores higher in CSF than in the same
donor's blood, and recorded that this paired contrast had never been tested
against the matched random-set null that defeated the disease contrast. Running
that test on the ten paired donors:

| Gene set | Genes | CSF − blood | Donors up | Random-set 95 % | Empirical p |
|---|---|---|---|---|---|
| Pro-inflammatory (S1 HVG) | 58 | +0.061 | 10/10 | −0.005 to +0.046 | **0.003** |
| Programme N3 | 25 | +0.081 | 10/10 | −0.018 to +0.058 | **0.007** |
| Activation set | 10 | +0.109 | 8/10 | −0.035 to +0.079 | **0.013** |
| Pro-inflammatory (all genes) | 101 | +0.041 | 9/10 | +0.002 to +0.040 | **0.043** |
| Programme P1 | 27 | +0.059 | 10/10 | −0.018 to +0.058 | 0.052 |
| Proliferation set | 10 | −0.013 | 4/10 | −0.044 to +0.079 | 0.235 |
| Th17n EGCG signature (Table S3) | 805 | +0.021 | 8/10 | +0.019 to +0.027 | 0.297 |
| Programme N2 | 78 | +0.010 | 8/10 | −0.001 to +0.042 | 0.302 |
| Pro-regulatory (S1 HVG) | 25 | +0.007 | 6/10 | −0.019 to +0.059 | 0.394 |
| Programme P2 | 81 | +0.013 | 6/10 | +0.001 to +0.044 | 0.399 |
| Programme P3 | 45 | +0.019 | 7/10 | −0.006 to +0.050 | 0.795 |
| Programme N1 | 37 | +0.026 | 7/10 | −0.009 to +0.052 | 0.795 |
| Programme P4 | 85 | +0.022 | 8/10 | +0.002 to +0.041 | 0.904 |
| Pro-regulatory (all genes) | 58 | +0.022 | 7/10 | −0.002 to +0.045 | 0.931 |

**This is the first module-specific result in the package.** The
pro-inflammatory arm exceeds its own matched-size null (p = 0.003) and rises in
every one of the ten donors, while the pro-regulatory arm does not move at all
(p = 0.39, six donors up). The arm asymmetry is the opposite of the mouse
glucose experiment, where the pro-regulatory arm fell and the pro-inflammatory
arm did not rise ([Wp-R1](R1_RESULTS.md)) — both are arm-asymmetric, but in
different arms, which is a statement about two different perturbations rather
than a contradiction.

All fourteen gene sets the run scored are listed, ordered by empirical p, as
the contract requires. Bold marks p ≤ 0.05 against the matched null. Note that
the pro-regulatory arm fails on both definitions — the authors' HVG set
(p = 0.394) and all 58 mapped genes (p = 0.931).

Note also what fails: the Table S3 EGCG signature, 805 mapped genes, sits inside
its null (p = 0.30). A large transported signature does not separate the
compartments beyond what any 805 genes would.

**The limit that cannot be removed by this design.** The activation set also
exceeds its null (p = 0.013), in the same direction. CSF T cells being more
activated than blood T cells is the expected finding, and nothing in a paired
donor-level contrast on ten donors can separate "the pro-inflammatory module is
specifically elevated" from "activation is elevated and the module overlaps it".
What the null does establish is that *both* are specific — neither is what an
arbitrary gene set of the same size would do — and that the pro-regulatory arm
is not.

## Independent arithmetic check

Two quantities recomputed outside the pipeline from different files than the
ones checked. The Th17n vehicle-versus-vehicle gate-signature correlation,
recomputed from the TPM matrix with the library annotation re-parsed from the
GEO SOFT records: 0.397665 against the run's 0.397665 (deviation 5.6 × 10⁻¹⁷).
The paired CSF-minus-blood pro-inflammatory median, recomputed from the Wp-R4
donor z-matrix with the gene set rebuilt from Table S1: 0.06144131 against the
run's 0.06144131 (deviation 3.5 × 10⁻¹⁷), over 58 mapped genes.

## Limits

- M1 and M2 are library-level on deposited TPM with no animal field;
  neither supports animal-level or causal inference.
- Div.1 and Total are overlapping sorted populations of the same cultures with
  no pairing field, so every gate quantity is attenuated and describes two gated
  populations rather than a cell's division history.
- EGCG and DHEA have different solvents; a solvent-specific contribution to
  their agreement cannot be excluded.
- M3 is donor-level and paired — the strongest unit in the package — but the
  signatures are the mouse study's own and the cohort was collected for another
  purpose. A compartment difference is not evidence about disease, and
  activation cannot be separated from the module here.
- Ten pairs; a Wilcoxon signed-rank test cannot fall below p = 0.002.
