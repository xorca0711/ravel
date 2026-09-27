# C5: unresolved by the declared rule, after an adversarial review rewrote the reasons

27 September 2026, **rewritten the same day after a three-lens adversarial review**. The first draft
is superseded, not preserved separately, because almost every sentence in its argument changed; its
wording is quoted below wherever it was wrong so the correction is visible. Executed under the
contract frozen at [C2](../config/gse198864_acute_injury_contract.json), gated at
[C3](../tables/acute_injury_gse198864/gate/gate_report.json), scored at [C4](../tables/acute_injury_gse198864/scores/inference.tsv), extended by the post hoc
diagnostics in this directory and by the identity restriction at [C6](../tables/acute_injury_gse198864/concordant_identity/) and [C7](../tables/acute_injury_gse198864/concordant_identity/).
**No claim row is added and no register grade changes.**

## Verdict

**Unresolved, reached by the contract's own decision rule rather than by a refusal.** The exact
interval that rule needs cannot be computed at these unit counts, and the interval that can be
computed contains the margin. What changed under review is the quality of the evidence behind that
verdict: the effect is more robust than the first draft argued, and its central weakness is not the
one the first draft named.

## What the review broke

Three lenses attacked the first draft. The bottom line held; four of its five main statements did
not, and one was backwards.

**The exact test does return a p-value and an estimate.** The first draft said it "returns no
interval and no p-value on any test". Only the interval is structurally unavailable. At four pairs
there are 16 sign patterns and the attainable two-sided confidence level tops out at 87.5 per cent,
so a 95 per cent interval does not exist and R returns an infinite one. The A11 helper requires a
finite interval and blanks all four of its output columns when any condition fails, which is why the
table shows nothing.

| Test | n | Mean | Hodges-Lehmann | Exact p | Donors positive |
|---|--:|--:|--:|--:|---|
| SARS-CoV-1, lesion_specific | 4 | +0.260 | +0.241 | 0.125 | 4 of 4 |
| SARS-CoV-1, stress_excluded | 4 | +0.258 | +0.230 | 0.125 | 4 of 4 |
| SARS-CoV-1, beyond_shared | 4 | +0.173 | +0.085 | 0.625 | 3 of 4 |
| SARS-CoV-2, lesion_specific | 3 | +0.141 | +0.159 | 0.500 | 2 of 3 |
| SARS-CoV-2, stress_excluded | 3 | +0.138 | +0.149 | 0.500 | 2 of 3 |
| SARS-CoV-2, beyond_shared | 3 | +0.008 | +0.007 | 0.250 | 3 of 3 |

The exact interval at the level that is attainable, 87.5 per cent, runs from +0.057 to +0.529 for the
primary. It contains the 0.10 margin, so the contract's `acute_induction_supported` fails and its
`margin_ruled_out` fails, and unresolved follows from the rule. The 0.125 is the floor at four pairs,
so the data are as concordant with the predicted direction as the design permits. I did not patch the
shared helper to report these, because it is A11's frozen instrument and altering it would change the
A11 result it produced; they are recorded in
[`gene_level_diagnostic.json`](../tables/acute_injury_gse198864/diagnostics/gene_level_diagnostic.json) and recomputed directly in
[C7](../tables/acute_injury_gse198864/concordant_identity/inference_concordant.tsv) instead.

**The direction count is not separate evidence.** Four of four concordant signs is the sign test, at
one-sided 0.0625 and two-sided 0.125, the same number as the exact p. The first draft and its
proposed wording presented both as if they were two supports.

**The normalisation claim was backwards.** The first draft said the effect "falls to +0.090" without
the trimmed-mean normalisation and concluded the direction was "partly a property of the
normalisation". A module score has an arbitrary zero that moves with the normalisation, so the
comparable quantity is displacement from an abundance-matched random background scored the same way.
Over 2,000 matched random 73-gene sets:

| Normalisation | Module | Null centre | Null sd | Displacement |
|---|--:|--:|--:|--:|
| Trimmed mean | +0.2596 | -0.0071 | 0.0553 | **+0.2667** |
| None | +0.0930 | -0.1762 | 0.0556 | **+0.2692** |

The displacement is invariant to about four decimal places and sits roughly 4.8 null standard
deviations out. What the normalisation moves is the baseline, not the module signal, so the first
draft's eighth verification check was measuring the wrong thing. Table:
[`null_displacement.tsv`](../tables/acute_injury_gse198864/diagnostics/null_displacement.tsv).

**The stress-excluded agreement proves nothing about stress.** A11's exclusion drops 17 of the 73
genes and retains the canonical inflammatory and stress names: TNF, RELB, IL23A, IL24, PTGS2, TRIB1,
ASNS, CHAC1, SLC1A4, SLC38A2, TP53INP1 and ZFAND2A all stay in. The two variants therefore share the
genes an acute injury would most be expected to move, and their near-identity is arithmetic. The
actual test is to drop those genes:

| Variant | Genes | Paired mean | Donors positive |
|---|--:|--:|---|
| Full module | 73 | +0.2596 | 4 of 4 |
| Without the NF-kB names | 64 | +0.2279 | 4 of 4 |
| Without the stress-response names | 66 | +0.2601 | 4 of 4 |
| Without both | 57 | +0.2245 | 4 of 4 |
| Only those 16 | 16 | +0.3845 | 4 of 4 |

The injury-responsive genes are enriched for the effect but do not carry it: the other 57 still move
+0.2245 with every donor positive. Table: [`dropout_and_null.tsv`](../tables/acute_injury_gse198864/diagnostics/dropout_and_null.tsv).

## The confound the review found, and what happened when it was removed

C3 gated gene coverage, pair eligibility and integer counts. It never gated cell identity. The
statistics lens found that the per-donor lesion difference is rank-identical to the per-donor shift in
the share of counts from cells the object's own reference transfer does not call type 2, at Spearman
+1.000, and that pat3's infected unit is the extreme case, with about 58 per cent of its counts from
cells transferred as Club and other labels against 7 per cent in its paired control.

So the pseudobulk was rebuilt over cells where the author cluster label and the reference transfer
agree, with the inherited 50-cell floor applied to the restricted counts, and the contrast re-run
with the instrument untouched.

| | Author-labelled | Identity-concordant |
|---|--:|--:|
| Type 2 explant cells | 4,732 | 3,827, 80.9 per cent |
| Units at the 50-cell floor | 11 | 10 |
| Unit dropped | none | pat3, SARS-CoV-1 |
| Primary pairs | 4 | 3 |

**The dropped unit is exactly the donor that contributed most, and removing it barely moves the
estimate.** The primary goes from a mean +0.260 with 4 of 4 positive to +0.225 with 3 of 3 positive,
and the Hodges-Lehmann estimate from +0.241 to +0.227. The secondary arm goes from +0.141 with 2 of 3
to +0.159 with 3 of 3. The confound is real and was unguarded, and it does not explain the effect.

**What the restriction does destroy is the beyond-shared contrast.** It moves from +0.173 to -0.039
with 2 of 3 positive, because the shared remodelling component moves as much as the lesion module and
in pat1 moves twice as far, +0.402 against +0.150. So the lesion module rises, and nothing here
separates that rise from the shared component rising with it. That is the central weakness, and the
first draft did not identify it.

## The cells being scored, with the field defined

The object's `virus` field is a detection call, non-none when a cell carries at least one read
assigned to that virus. It is not an infection assay, and a droplet assay can miss low-load infected
cells, so it bounds infection from below. The gene index carries 46 viral features, 14 SARS-CoV-1, 13
SARS-CoV-2, 10 influenza and 9 MERS; the first draft miscounted these and omitted the arm under test.

Restricted to each arm's eligible donors, which the first draft failed to do:

| Arm | Type 2 cells | With any viral read | Above 1 per cent viral content |
|---|--:|--:|--:|
| control | 1,171 | 0 | 0 |
| SARS-CoV-1, primary | 1,039 | 5, 0.5% | 0 |
| SARS-CoV-2 | 629 | 6, 0.9% | 0 |
| MERS-CoV | 589 | 253, 43.0% | 90 |
| influenza | 200 | 10, 5.0% | 1 |

The bystander reading survives and is stronger than the first draft argued: not one type 2 cell in the
primary arm exceeds 1 per cent viral content. The first draft's influenza figure of 15.6 per cent was
pooled over donors that are not eligible; within the one eligible donor it is 5.0 per cent. Its MERS
figure of 309 cells was likewise pooled; within the two eligible donors it is 253 of 589. Table:
[`virus_detection.tsv`](../tables/acute_injury_gse198864/diagnostics/virus_detection.tsv).

## What this establishes

**Establishes, descriptively and within one cohort.** That the frozen lesion module is higher in
infected than in medium-matched mock explant type 2 cells, by about +0.23 to +0.26 log2 CPM, in both
coronavirus arms, with every eligible donor positive after identity restriction, displaced about 4.8
standard deviations from an abundance-matched background under either normalisation, and not carried
solely by its inflammatory and stress genes.

**Does not establish acute induction of the programme**, which is the question asked. The exact
interval at the attainable level contains the margin, the smallest reachable p is 0.125 at four pairs
and 0.25 at three, and above all the beyond-shared contrast is null or negative once identity is
controlled, so the rise is not separable from the shared remodelling component rising with it.

**Does not establish tumour specificity in either direction**, which the contract ruled out in
advance. And the contract's population caveat has to travel with any reading, in its own words: these
tumour-free explants come from surgical cancer patients, so they are not a cancer-naive population.
The first draft dropped that sentence, which a reader lifting a claim row would have needed.

**A note on dependence.** The stress-excluded module is 56 of the primary module's 73 genes, and the
secondary arm reuses three of the four primary control libraries. Neither is independent corroboration
of the primary, and the report does not treat them as such.

## What would settle it

Six or more paired donors in one arm, which this deposit cannot supply for any arm, since the exact
two-sided test first reaches 0.05 at six pairs. A design that separates infected from bystander type 2
cells, which on these numbers only MERS-CoV approaches, at 253 virus-positive cells across two
eligible donors. And a contrast that can distinguish the lesion module from the shared remodelling
component, which needs either more donors or a component definition built to be separable.

## Proposed wording, not graded here

1. **Not established.** In GSE198864 lung explants, the frozen A11 lesion module in type 2 cells whose
   author label and reference transfer agree is higher in SARS-CoV-1 infected than in medium-matched
   mock explants by a mean of +0.225 log2 CPM across three paired donors, positive in all three, with
   an exact p of 0.25 which is the floor at that unit count. The beyond-shared contrast is -0.039, so
   the rise is not separable from the shared remodelling component. These explants come from surgical
   cancer patients and are not a cancer-naive population.
2. **Descriptive.** The module's displacement from an abundance-matched random background is +0.267
   with and +0.269 without trimmed-mean normalisation, about 4.8 null standard deviations, so the
   movement is not a normalisation artefact; and removing the module's NF-kB and stress-response genes
   leaves +0.225 with all four donors positive in the unrestricted pseudobulk.
3. **Descriptive, and it bounds the design.** The type 2 cells scored in the primary arm carry at
   least one viral read in 5 of 1,039 cells and none exceeds 1 per cent viral content, so the contrast
   measures a bystander response. The arms whose type 2 cells are substantially virus-positive,
   MERS-CoV at 43.0 per cent and influenza at 5.0 per cent within eligible donors, have two and one
   eligible pairs against an inherited three-unit floor.
