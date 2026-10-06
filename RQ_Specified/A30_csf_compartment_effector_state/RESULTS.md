# A30 reanalysis leg: the elevation is not activation, and it is not only composition

> **Superseded in part — read
> [A30_ERRATUM.md](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/A30_ERRATUM.md)
> first.** The v2 runs below divided each cell by the row sum of the loaded gene
> subset instead of its all-gene library size, and drew only 1,000 matched random
> sets, which gives a Monte-Carlo standard error larger than the distance from
> the reported BH values to 0.05. Corrected and re-run at 10,000 draws as
> `wp_a30_activation_stratified_v3` and `wp_a30_state_decomposition_v3`, the
> pro-inflammatory arm is at **BH 0.032, 0.037, 0.032 — below 0.05 in all three
> strata**, and the activation positive control is flat on the matched null but
> marginal on Wilcoxon in two of three strata. **Everything below is the v2
> record, kept unchanged; the erratum carries the current values.** The
> conclusions that reverse are in §1 (the primary clears BH after all), §2 (the
> totals move; the composition *shares* do not), §3 (two of the four
> pre-declared decision rows read differently) and §5 (the limitation is
> resolved). Each is flagged in place below.

Executed 5 October 2026 under the governed runner. Two outcome rows of the
question card fire together, which the card did not anticipate, and the honest
reading is weaker than either row alone.

| | |
|---|---|
| Stratified contrast | [config](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/config/a30_activation_stratified_v2.json) · [receipt](../../analysis/research/runs/wp_a30_activation_stratified_v2/receipt.json) |
| State decomposition | [config](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/config/a30_state_decomposition_v2.json) · [receipt](../../analysis/research/runs/wp_a30_state_decomposition_v2/receipt.json) |
| Superseded runs, preserved | `wp_a30_activation_stratified_v1`, `wp_a30_state_decomposition_v1` |

All four receipts `verify` clean. Per-unit cell recovery was asserted identical
to [Wp-R4](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/R4_RESULTS.md) v2
(35,928 cells) before anything was stratified, so the strata attach to the
cells already analysed.

## 1. The elevation survives activation matching

The activation score was rebuilt from a **21-gene panel verified disjoint from
both module gene lists**, because the panel Wp-R4 used contains *ZFP36*, a
pro-regulatory module gene, and stratifying on a score that shares genes with
the endpoint is circular. Cells were cut into global tertiles of that score, so
a low-activation CSF cell is compared against a low-activation blood cell.

| Stratum | Pro-inflammatory CSF − blood | Donors up | Wilcoxon | Null p | BH |
|---|---|---|---|---|---|
| act1 (low) | **+0.055** | 9/9 | 0.0039 | 0.034 | 0.068 |
| act2 (mid) | **+0.056** | 10/10 | 0.0020 | 0.018 | 0.063 |
| act3 (high) | **+0.055** | 10/10 | 0.0020 | 0.021 | 0.063 |

Pro-regulatory, in the same cells and strata: +0.021 (7/9), +0.011 (6/10),
−0.002 (4/10); null p 0.86, 0.74, 0.42; BH 0.86, 0.86, 0.63. The arm asymmetry
holds inside every stratum.

**The stratification worked.** The activation score itself is flat within
strata — +0.009, +0.006, +0.015, null p 0.78, 0.66, 0.92 — so within a stratum
CSF and blood cells are genuinely activation-matched, and the module difference
is not riding on an activation difference. That is the positive control, and it
passes.

The effect is also remarkably constant across the activation range: +0.055,
+0.056, +0.055. An activation-driven artefact should grow with activation.

**But the primary does not clear its matched null after correction.** Against
1,000 matched-size random gene sets, with BH across the pre-declared family of
2 arms × 3 strata, the pro-inflammatory arm sits at BH 0.063 to 0.068 — above
0.05 in all three strata. The direction is consistent (29 of 30 donor-stratum
comparisons positive; only MS71658 is near zero throughout, at +0.002, +0.002,
+0.001), and the Wilcoxon p values are 0.002 to 0.004, but a matched random set
of 57 genes reproduces an effect this size about 2 to 3 per cent of the time
and the stratified test has less power than the unstratified one it checks.

So: **activation is excluded as the explanation; the elevation itself is
directionally robust but no longer passes the package's own null threshold
once the design is corrected and the family adjusted.**

## 2. About 40 % of the difference is a mixture shift

Each donor's paired difference was split by the symmetric Kitagawa identity on
two independent bases. The identity is exact; the largest residual across all
donors is 2 × 10⁻¹⁷.

| Basis | Total | Composition | Within-state | Within sign |
|---|---|---|---|---|
| Activation strata (3) | +0.0710 | +0.0063 (9 %) | **+0.0595 (84 %)** | 10/10 donors |
| De novo cell states (23) | +0.0710 | **+0.0275 (39 %)** | +0.0400 (56 %) | 8/10 donors |

The two bases disagree, and the disagreement is the finding: activation strata
carry almost none of the difference, but **cell-state composition carries about
two fifths of it**. The CSF pool is not a reshuffled blood pool — three states
make up 56 % of CSF cells and under 1 % of blood, and two states are ~25 % of
blood and absent from CSF. A mixture that different will move a module score
without any cell changing state.

A majority of the difference is still within-state, and that term is positive
in 8 of 10 donors, so this is not purely composition either. Both mechanisms
contribute.

> **v3 update.** The corrected denominator lowers both totals (+0.0710 → +0.0618
> on the activation-stratum basis, +0.0710 → +0.0618 on the de novo basis) but
> leaves the **shares essentially identical**: composition 38.7 % → 38.8 % and
> within-state 56.3 % → 60.5 % over the same 23 states, within sign 8/10
> unchanged. The v3 contract predicted this before execution, because the
> clustering matrix was already normalised over all genes and only the means it
> carried were wrong. **This section's conclusion is unaffected.**

### The version that would have misled

The first state decomposition clustered on the 285 genes the scoring pass
happens to load — mostly Th17 programme markers. On that space composition
looked like 9 % and within-state sign agreement was 10/10, i.e. it would have
supported a clean compartment-state reading. Those states were not independent
of the biology under test and could not resolve a subset defined by genes
nobody had scored, which is exactly the named rival. Rebuilding the clustering
from 2,000 highly variable genes drawn from the full 33,480-gene shared space
quadrupled the composition term. The v1 run is preserved and its contract
records why it was superseded.

## 3. Against the pre-declared decision rows

The card fixed four outcomes. Two fire.

| Pre-declared row | Fired? |
|---|---|
| Elevation persists within matched activation strata, pro-regulatory flat → compartment-associated effector state | **Partly.** It persists with the regulatory arm flat and the activation control flat, but does not clear its matched null after BH. |
| Elevation collapses once activation is held → activation correlate | **No.** It does not move at all across the activation range. |
| Composition term carries the paired difference → mixture shift | **Partly.** 39 % on independent states, not a majority but not dismissible. |
| Ten donors cannot separate the strata → precision-limited | **Yes, in part.** The stratified test has less power than the contrast it checks, and the primary lands just above threshold. |

The defensible statement: **the CSF pro-inflammatory elevation is not explained
by local activation, and is partly but not mostly a cell-mixture shift. What
remains is a within-state difference of about +0.04, consistent across donors,
that this deposit cannot push past its own matched-null threshold.**

A30's working hypothesis — a compartment-imposed effector state with regulatory
competence unchanged — is **not refuted and not established**. The regulatory
half of it holds up well; the effector half is attenuated by composition and
left short of the threshold by precision.

> **v3 update — two of the four rows read differently, and the concluding
> paragraph above is withdrawn.** With the corrected denominator and 10,000
> draws:
>
> | Pre-declared row | v2 reading | v3 reading |
> |---|---|---|
> | Elevation persists within matched activation strata, pro-regulatory flat | Partly — does not clear its matched null | **Fires.** BH 0.032, 0.037, 0.032, below 0.05 in all three strata, regulatory arm flat at BH 0.82 |
> | Elevation collapses once activation is held → activation correlate | No | **No**, unchanged |
> | Composition term carries the paired difference | Partly, 39 % | **Partly, 39 %**, unchanged |
> | Ten donors cannot separate the strata → precision-limited | Yes, in part | **No longer the binding limit** for the primary; it remains the limit for any covariate adjustment and for the residual activation difference, whose two tests disagree |
>
> The statement this leg supports is therefore: *the CSF pro-inflammatory
> elevation clears the package's own matched-null threshold inside every
> activation stratum, the regulatory arm is flat, about 39 % of it is a mixture
> shift, and activation is reduced but — on the Wilcoxon test — not eliminated.*
> The effector half of the hypothesis is **supported with a residual activation
> caveat** rather than left short of threshold. A30's grade remains the owner's
> and is still `not_assessed`.

## 4. What this does not address

- **Residency.** Nothing here distinguishes a state the compartment imposes
  from cells that were already different before they arrived. That needs
  shared-clone comparison across compartments, which this deposit cannot
  supply, and it is the reason no causal language appears above.
- **Protein, secretion, function.** Module scores are RNA, and the modules are
  mouse-derived, transported by symbol identity (57 of 63 and 24 of 30 genes).
- **Donor covariates.** The deposit carries no age, sex, treatment or
  disease-duration field, so nothing is adjusted for them.
- **Independence.** This reanalyses the deposit already analysed by Wp-R4 and
  by Schafflick et al. 2020. One evidence lineage, never independent
  replication.
- **Cluster identity.** The 23 states are a partition of these cells, not
  validated cell types. That three of them are near-exclusive to CSF is a
  composition fact, not an annotation.

## 5. A limitation found during execution

The inherited Wp-R4 scoring convention computes the CP10K denominator over the
**loaded gene subset** rather than total counts, so a score depends slightly on
which other gene sets are being scored in the same run. Correcting the Table S5
parse changed the loaded set and moved the act1 pro-inflammatory value from
+0.0588 to +0.0549. The convention was kept unchanged because the contract
binds it and because changing it would break comparability with Wp-M3, but it
should be fixed before any future run, and the two values are reported here
rather than only the later one.

**Resolved 6 October 2026.** It was fixed, and it mattered: see
[A30_ERRATUM.md](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/A30_ERRATUM.md).
Correcting the denominator moved the pro-inflammatory BH values from 0.063–0.068
to 0.032–0.037 with the effect size essentially unchanged, so the §1 conclusion
that the primary "does not clear its matched null" was an artefact of this
convention compounded by an under-powered null. The judgement recorded above —
that comparability with Wp-M3 outweighed correctness — was the wrong call, and
is recorded as such rather than edited away.

## 6. Next useful step

Not more analysis of this deposit. The within-state residual is the part worth
testing, and the measurement that would settle it is the one A30 already names:
paired CSF and blood CD4 T cells from the same donors, sorted on activation,
with intracellular IL-17A and Foxp3 protein and TCR sequencing, so shared
clones can be compared across compartments. That addresses residency, protein
and composition in one design, with the donor as unit.
