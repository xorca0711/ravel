# Pre-RQ checkpoint: what is settled, and the extension candidates worth weighing

Dated 5 October 2026. **No research question is derived here and no candidate
below is authorised.** This document exists so that the eventual derivation
starts from an explicit account of what the executed work established, what it
closed, and which further analyses are plausible — with the unattractive ones
named as such rather than quietly omitted.

## 1. Settled by execution

Seven governed runs, each with a verified receipt and an independent arithmetic
check. The [claim-by-claim table](REPRODUCTION_SCOPE.md#claim-by-claim-outcome-4-october-2026)
is the authority; the short form:

| Established | Where |
|---|---|
| The undeclared single-cell library order is recoverable from markers, 8/8 | [Wp-R1](R1_RESULTS.md) |
| Pathogenicity rises at low glucose through the pro-regulatory arm, 4/4 animal pairs | [Wp-R1](R1_RESULTS.md), [Figure 3](FIGURES.md#figure-3-the-pathogenicity-score-rises-at-low-glucose-through-the-pro-regulatory-arm) |
| N1 is least pathogenic, and stays so after overlap removal and under every score variant | [Wp-R1](R1_RESULTS.md), [Wp-P01](P01_RESULTS.md) |
| Table S3 reproduces on the first-division gate, r 0.83–0.92 | [Wp-R3](R3_RESULTS.md), [Figure 1](FIGURES.md#figure-1-the-published-bulk-contrasts-reproduce-on-the-first-division-gate) |
| The Th17n EGCG module shift is **not** selective once the global shift is centred out | [Wp-R3](R3_RESULTS.md), [Figure 2](FIGURES.md#figure-2-in-th17n-pgam-inhibition-moves-both-gene-groups) |
| The human blood separation is **not** module-specific against matched random sets | [Wp-R4](R4_RESULTS.md), [Figure 4](FIGURES.md#figure-4-in-blood-random-gene-sets-separate-the-two-human-cohorts-as-well-as-the-modules-do) |
| PGAM keeps its sign under a modern Compass but is 11th of 83 and fails BH | [Wp-R2](R2_RESULTS.md), [Figure 5](FIGURES.md#figure-5-pgam-keeps-the-published-negative-sign-but-is-not-the-most-distinctive-reaction) |
| The low-glucose rise is a change of mixture; the within-state term is inconclusive at n = 2 | [Wp-P03](P03_RESULTS.md) |
| The cell ranking is stable to gene selection; the glucose **effect size** is not | [Wp-P01](P01_RESULTS.md) |

**Closed, with reasons.** Wp-R5 and Wp-P04 are permanently blocked — no numeric
values are deposited for the protein, labelling or disease panels, and the owner
declined both routes out. Wp-P05 is resolved in the negative. Wp-P06 stays
conditional on four unmet requirements. The RNA arm of Wp-P02 is closed as
uninformative for discrimination, and its stress premise is contradicted by the
one cited text that can be read in full.

## 2. The one question a new measurement could still move

[Wp-P02](branches/P02_serine_one_carbon_direction.md): does the 3PG serine arm
run with or against the regulatory programme? Three independent readouts now
agree on the Compass *sign* — the reaction correlation (ρ −0.26), the bulk
transcripts (all serine and one-carbon genes fall under EGCG), and the paper's
own prediction — and none of them can distinguish it from Godfrey's opposite
mechanism, because none measures flux and PGAM inhibition is expected to raise
3-phosphoglycerate regardless. The discriminating experiment is a culture
experiment: PGAM and PHGDH inhibition alone and together in Th17n, with Foxp3
and IL-17 protein and ¹³C serine/glycine labelling from [U-¹³C]glucose.

## 3. Extension candidates, ranked by information per unit of effort

None of these is authorised. Each states what it would change, what it needs,
and why it might not be worth running. **E1–E3 are reanalysis of deposited data.
E4–E6 need something this project does not hold. E7–E9 are named so they are not
mistaken for good ideas later.**

### E1 — Does the score's instability reach the reaction ranking?

The one consequence [Wp-P01](P01_RESULTS.md) could not test. Wp-R2 scored
micropools without saving pool membership, so no variant score can be projected
onto the reactions. Re-running Compass with membership saved, then recomputing
every reaction correlation under the five score variants, would show whether
PGAM's rank of 11 is itself a property of the gene filter.

*Needs:* about an hour of solver time plus a contract amendment fixing the
pooling seed defect recorded in the Wp-R2 report. *Changes a conclusion if:* the
rank moves substantially under the unfiltered module lists, which would mean the
paper's reaction selection inherits the HVG filter. *Argument against:* the
whole plate is already labelled a sensitivity, so a sensitivity of a sensitivity
has limited reach.

### E2 — Is the composition shift a boundary artefact?

[Wp-P03](P03_RESULTS.md) could not run the card's resolution sweep because the
authors' clustering is not deposited. A graded version is available: assign
programmes at several marker-score margins, from a hard winner-takes-all to a
confidence-weighted soft assignment, and watch the mixture term. If the term
survives soft assignment it is not a boundary effect; if it collapses, the
decomposition was cutting a continuum.

*Needs:* the existing per-cell table only, under a new contract. *Changes a
conclusion if:* the mixture term is an artefact of hard labels, which would
retract the strongest statement Wp-P03 makes. *Argument against:* it still
cannot show that a cell changed state, so the lineage limit is untouched.

### E3 — Which genes carry the non-selective Th17n EGCG shift?

[Figure 2](FIGURES.md#figure-2-in-th17n-pgam-inhibition-moves-both-gene-groups)
shows both gene groups rising together under EGCG in Th17n. The question that
opens is what the global shift *is*: a stress or ribosomal programme, a
proliferation arrest signature, or a technical compositional effect of TPM
renormalisation. Ranking the non-partition genes by their contribution and
testing a small set of declared programme definitions against them would say
which.

*Needs:* the tracked contrast table, plus gene sets frozen in advance. *Changes
a conclusion if:* the shift is a recognisable stress programme, which would
connect directly to the [Wp-P02](branches/P02_serine_one_carbon_direction.md)
stress arm — now known to rest on a mis-cited premise, and therefore in need of
its own evidence. *Argument against:* TPM renormalisation alone can produce a
global shift, and the deposit has no spike-ins or counts to rule that out, so a
negative result would be uninterpretable.

### E4 — Is the donor-level axis in human blood a batch effect?

[Wp-R4](R4_RESULTS.md) showed the blood separation is non-specific but could not
identify the axis, because GSE138266 deposits no batch, run or processing field.
The original publication or its authors may hold the processing dates. With
them, the axis could be named rather than merely demonstrated.

*Needs:* metadata this project does not hold — author contact, which the owner
has already judged implausible for this package. *Changes a conclusion if:* it
would convert "non-specific" into "explained", which is a stronger negative
result. *Status:* parked, not proposed.

### E5 — Does the pro-regulatory arm fall at low glucose in an independent Th17 dataset?

The single strongest reproduced finding rests on two mice. Any independent Th17
single-cell dataset with a nutrient or glucose contrast would test whether the
arm-specific direction generalises, using the same frozen module definitions.

*Needs:* a dataset search this package has not performed, and a frozen
inclusion rule written before any candidate is opened. *Changes a conclusion
if:* the direction fails to replicate, which would make the paper's central
single-cell claim condition-specific. *Argument against:* "similar Th17 culture"
is exactly the kind of equivalence this project does not grant by name alone;
the search could easily return nothing admissible.

### E6 — The discriminating wet experiment

Section 2. It is the highest-value step in the package and it is not reanalysis.

### E7 — Rerun Compass on the full reaction set *(named to be refused)*

Tempting because it would produce a ranking comparable to Figure 1A. It would
not: the published input was scVI-imputed and is not deposited, so a full-scope
run would still differ from the paper on the input, while costing many hours of
solver time. The scope restriction is not what makes Wp-R2 a sensitivity.

### E8 — Score the Compass reactions in the lung datasets *(named to be refused)*

This is the move [Wp-P06](branches/P06_epithelial_transfer_condition.md) exists
to prevent, and the Wp-R2 result makes it worse: the reaction whose transfer
would be proposed is not distinctive even in its own compartment.

### E9 — Digitise the published figure panels *(named to be refused)*

The owner declined this on 4 October 2026. A digitised series is never raw data
and never enters a claim as a measurement.

## 4. What a derivation should start from

Three asymmetries in what the package found, each a candidate seed and none of
them yet a question:

1. **The score's two arms behave differently depending on the contrast.** They
   are anti-correlated across cells within a condition (ρ −0.41) but move
   together under EGCG in bulk. A single difference score cannot represent both.
2. **Glucose acts on the mixture; the inhibitor acts on everything at once.**
   The two perturbations the paper treats as pointing the same way have
   different signatures in the deposited data.
3. **The published reaction prediction survives as a sign but not as a
   ranking.** What the paper selected PGAM *for* is the part that does not
   reproduce under substituted input.

Any derived question should name which of these it is about, which unit it would
use, and what result would make it fail — and should be checked against the
existing A-series register for overlap before it is allocated an identifier.
