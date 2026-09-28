# A16 Stage 1 results: the residual survives both analyses that could have closed the question, and the specificity test is inconclusive

**Executed 28 September 2026** on the owner's authorization, in the frozen order: C3 and C4 first,
then C1, C2 and C5. Exposure is FULL — the founding FU_C residual was seen before the contract was
written and this reuses the same processed matrices, so Stage 1 is an amendment, not independent
confirmation. Population correction in [STAGE1_ERRATUM.md](STAGE1_ERRATUM.md); two arms are reported
throughout, Arm A being the transitional gate per library and Arm B being FU_C's own population.

## Verdict

**Stage 1 neither closed A16 nor reached the conclusion its contract permits.** The two analyses that
could have closed the question did not: ambient neutrophil RNA is excluded as the explanation, and the
effect does not depend on the detection threshold. But the permitted positive conclusion requires the
residual to be *specific to Cd177 among detection-matched genes*, and that clause fails in the
best-powered unit and is underpowered in most others. The honest state is an **inconclusive estimate
on specificity**, which is neither missing evidence nor evidence against.

| Analysis | Could it close A16? | Result |
|---|---|---|
| C4 ambient neutrophil origin | yes | **Did not close.** Conditioning retains 87–139% of the effect; Cd177 detection barely tracks the neutrophil panel (\|ρ\| ≤ 0.27) |
| C3 detection-matched gene null | yes | **Inconclusive.** Cd177 exceeds every control in 4 of 9 units and sits inside the null in the best-powered unit; 6 of 9 nulls have fewer than 40 control genes |
| C1 neighbourhood matching | no | Positive in 8 of 9 units, but retains only 18–34% of the unmatched difference where that is well defined |
| C2 resolution ladder | no | No monotone decay; a plateau, on 3 resolutions with 1–6 testable clusters |
| C5 threshold sensitivity | no | Stable; no sign change where the effect is non-trivial |

## C4: ambient neutrophil RNA is excluded

This was the rival I expected to win, because Cd177 is a neutrophil surface protein and the priming
module (Lcn2, Lrg1, Retnla, Ptgs1) is inflammation-associated. It does not win.

| Arm | Unit | n pos | priming SMD | residual on neutrophil panel | on panel + depth | retained |
|---|---|--:|--:|--:|--:|--:|
| A | GSM7890835 | 79 | +1.600 | +1.557 | +1.478 | 0.97 |
| A | GSM7890836 | 60 | +2.168 | +2.149 | +1.984 | 0.99 |
| B | exp1 sub 10 | 36 | +0.358 | +0.360 | +0.466 | 1.00 |
| B | exp1 sub 12 | 108 | −0.077 | −0.107 | −0.153 | 1.39 |
| B | exp1 sub 16 | 321 | +0.015 | +0.014 | −0.043 | 0.93 |
| B | exp1 sub 17 | 114 | +0.359 | +0.311 | +0.313 | 0.87 |
| B | exp1 sub 18 | 80 | +2.323 | +2.112 | +1.935 | 0.91 |
| B | exp2 sub 10 | 80 | +0.597 | +0.625 | +0.599 | 1.05 |
| B | exp2 sub 12 | 55 | +1.308 | +1.316 | +1.084 | 1.01 |

Spearman correlation between Cd177 UMI and the neutrophil panel score runs −0.08 to +0.27, so the
marker is not reading neutrophil signal. The priming module does share some signal with that panel
(ρ 0.07 to 0.36, positive in 8 of 9 units), which is worth recording as a property of the module, but
conditioning on it changes nothing. **Ambient origin is not the explanation.** This bears on the RNA
side only and cannot touch the source's immunofluorescence or sorted-organoid evidence.

## C3: the specificity test, and why it is inconclusive

| Arm | Unit | Cd177 priming SMD | null median | null p95 | controls ≥ Cd177 | n controls |
|---|---|--:|--:|--:|--:|--:|
| A | GSM7890835 | +1.600 | −0.159 | +1.061 | **0.000** | 14 |
| A | GSM7890836 | +2.168 | −0.191 | +1.545 | **0.000** | 25 |
| B | exp1 sub 10 | +0.358 | +0.097 | +0.519 | 0.139 | **500** |
| B | exp1 sub 12 | −0.077 | +0.203 | +0.203 | 1.000 | 1 |
| B | exp1 sub 16 | +0.015 | +0.135 | +0.593 | 0.750 | 12 |
| B | exp1 sub 17 | +0.359 | −0.020 | +0.416 | 0.182 | 11 |
| B | exp1 sub 18 | +2.323 | **+0.963** | +1.900 | 0.091 | 11 |
| B | exp2 sub 10 | +0.597 | −0.071 | +0.377 | **0.000** | 36 |
| B | exp2 sub 12 | +1.308 | −0.022 | +0.392 | **0.000** | 284 |

Three readings, and they do not agree.

**Cd177 is exceptional in 4 of 9 units**, including the marginal contrast in both libraries and two
Experiment-2 subclusters, one of which has a well-populated null of 284 control genes.

**It is not exceptional in the best-powered Experiment-1 unit.** In exp1 sub 10, with 500 matched
controls, 13.9 per cent of them exceed Cd177's effect. In exp1 sub 17 the figure is 18 per cent. So
where Experiment 1 can be tested properly, the residual looks like ordinary gradient behaviour.

**In exp1 sub 18 most of the apparent effect is generic.** The median matched control gene shows a
priming SMD of +0.963 in that subcluster — a typical gene of Cd177's detection profile produces a
large positive association there. Cd177's +2.323 is elevated above that, but the baseline, not the
marker, accounts for most of it. This is exactly what the null was for.

**The binding limitation is that Cd177 is hard to match.** Requiring both detection rate (±25 %
relative) and mean expression (±35 % relative) leaves fewer than 40 control genes in 6 of 9 units, and
a single gene in one. That is a fact about the marker rather than a coding accident: Cd177 is detected
in about 9 per cent of transitional cells but carries 1 to 53 UMIs where detected, so its
expression-per-detection ratio is unusual and few genes sit in the same band. A null of 11 or 14 genes
cannot place an observation in a tail with any confidence. **Widening the band would be a post-hoc
relaxation after seeing this result and has not been run.**

## C1: most of the association is positional, and a residue is not

Matched differences are in raw score units, mean log1p(CP10k). The standardised column in the table is
divided by the paired-difference SD and is **not** comparable to an SMD; the retention column below is
a post-hoc rescaling computed for interpretability, comparing the matched difference with the raw
unmatched difference in the same units.

| Arm | Unit | raw unmatched | matched, k=10 | retained |
|---|---|--:|--:|--:|
| A | GSM7890835 | +1.256 | +0.346 | 0.28 |
| A | GSM7890836 | +1.332 | +0.236 | 0.18 |
| B | exp1 sub 17 | +0.289 | +0.150 | 0.52 |
| B | exp1 sub 18 | +1.397 | +0.470 | 0.34 |
| B | exp2 sub 12 | +0.910 | +0.308 | 0.34 |
| B | exp1 sub 10 | +0.203 | +0.236 | 1.16 |
| B | exp2 sub 10 | +0.370 | +0.484 | 1.31 |
| B | exp1 sub 16 | +0.010 | +0.209 | 21.7 |
| B | exp1 sub 12 | −0.043 | −0.079 | 1.85 |

The sign is positive in 8 of 9 units and stable across k = 5, 10 and 20. Where the unmatched
difference is substantial, local matching removes two thirds to four fifths of it — the marginal
association is largely positional, which is what FU_C already concluded.

The lower block is a methodological finding worth keeping: in three units the matched difference is
**larger** than the unmatched one, extremely so in exp1 sub 16 where an unmatched difference of +0.010
becomes +0.209 after matching. Discrete cluster conditioning and local matching are not the same
operation and can move in opposite directions, because a subcluster is internally heterogeneous and
comparing positives against all of its negatives can mask a locally consistent difference. A
within-cluster estimate near zero is therefore not evidence that position explains everything.

**Contract deviation, declared.** C1 as frozen asks for the round-2 *integrated* embedding. Only the
UMAP coordinates, sub_r* labels and diffusion ordering were persisted, so this ran in UMAP space — a
local-neighbourhood proxy, defensible because kNN uses only local relations, but not the frozen space.
The integrated-space version remains deferred.

## C2: no monotone decay, on a ladder too short to lean on

| Experiment | conditioning | testable clusters | pooled priming SMD |
|---|---|--:|--:|
| 1 | none (marginal) | 1 | +0.635 |
| 1 | r = 0.5 | 5 | +0.649 |
| 1 | r = 1.0 | 5 | +0.358 |
| 1 | r = 1.5 | 6 | +0.380 |
| 2 | none (marginal) | 1 | +1.188 |
| 2 | r = 0.5 | 1 | +0.478 |
| 2 | r = 1.0 | 2 | +0.887 |
| 2 | r = 1.5 | 2 | +0.573 |

The frozen rule reads a plateau as favouring a component that is not positional at any resolution the
data resolve, and that is what appears in Experiment 1: the effect drops from the marginal value and
then flattens at about +0.36 to +0.38 rather than decaying toward zero. Experiment 2 is
non-monotone with 1 to 2 testable clusters and is uninformative. Three persisted resolutions is a
short ladder, so this is weak support and is not treated as more.

## C5: the arbitrary cut is not driving anything

Priming SMD at Cd177 ≥ 1, ≥ 2 and ≥ 3 UMIs: GSM7890835 +1.599, +1.619, +1.681; GSM7890836 +2.165,
+2.346, +2.407; exp1 sub 18 +2.323, +2.337, +2.384; exp1 sub 17 +0.359, +0.463, +0.479; exp2 sub 10
+0.597, +0.630, +0.688. Two units move the other way — exp2 sub 12 +1.308, +1.180, +1.087, and exp1
sub 12 stays negative at −0.077, −0.153, −0.188 — and exp1 sub 16 stays at zero. **No sign change
occurs where the effect is non-trivial**, and effects tend to strengthen slightly at stricter
thresholds, which is what a real association diluted by detection noise should do. Under 1,000-UMI
thinning, exp1 sub 16 flips between seeds (−0.119, +0.201) but its full-depth value is +0.015, and
exp2 sub 12 reproduces at +1.239 against +1.308.

## What this changes, and what happens next

The readiness row moves from *blocked* to **partly measured and inconclusive on specificity**. No
claim row is added; no graded claim is available, and none is requested.

Three named rivals from the contract are now resolved: **ambient neutrophil origin is excluded**, a
**detection-threshold artefact is excluded**, and **single-resolution dependence is not supported**.
Two remain live and are the reason the question stays open: **generic gradient behaviour**, which the
specificity test could not settle for lack of matchable control genes, and **finer-scale composition**,
which local matching reduces but does not remove.

The next useful action is not another conditioning analysis on these matrices — Stage 1's ceiling has
been reached, and the honest conclusion is that the RNA cannot decide this. Three options, in the
order I would take them:

1. **Ask the source authors for the sorted-CD177 organoid and transplantation input fractions.** They
   performed the separation this question needs, and the inputs were never deposited.
2. **Re-derive the round-2 integrated embedding** and run C1 in the frozen space. This is bookkeeping
   rather than new evidence, and would firm up one number.
3. **A disclosed post-hoc specificity re-run** with a wider matching band, which would raise the
   control-gene counts but must be labelled as post-hoc and cannot be reported as the frozen C3.

The discriminating experiment is unchanged and its prediction is unchanged: sort on surface CD177
within a transitional gate from a comparable neighbourhood, measure EdU or Ki67 protein and short-term
clone growth, and expect enrichment for primed, identity-retaining cells and **not** for more cycling
ones.

## Outputs

[C3 summary](../tables/stage1/A16_C3_matched_gene_null.csv) ·
[C3 per-control-gene detail](../tables/stage1/A16_C3_control_gene_detail.csv) ·
[C4](../tables/stage1/A16_C4_ambient_neutrophil_control.csv) ·
[C1](../tables/stage1/A16_C1_neighbourhood_matched.csv) ·
[C2](../tables/stage1/A16_C2_resolution_ladder.csv) ·
[C5](../tables/stage1/A16_C5_threshold_sensitivity.csv) ·
[C3/C4 script](../scripts/01_stage1_c3_c4.py) ·
[C1/C2/C5 script](../scripts/02_stage1_c1_c2_c5.py) ·
[run record](../tables/stage1/run_record.json) ·
[run record, second script](../tables/stage1/run_record_c1_c2_c5.json)
