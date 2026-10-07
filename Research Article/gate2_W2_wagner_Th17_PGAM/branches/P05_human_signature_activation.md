# Wp-P05 — Does the human signature separate disease beyond generalised activation?

**Current evidence:** [7 October corrections](../CORRECTIONS_2026-10-07.md) supersede the older Compass sign and human-score summaries cited below. Retain source-paper premises separately from the corrected repository results; the source study and its reanalysis are not independent replication.

**Status:** proposed, outcome-exposed. Transport of an exposed signature with a
competing explanation in the same model.

**Owner's framing, 4 October 2026.** The Results note marks the two-module result
in MS with "Verification? And extensions?" — and reads it, correctly, as a higher
activation level spanning multiple T-helper programs. That reading is the rival
this card puts into the model rather than into a caveat, so the note's question
and the card's design are the same thing. See
[note reconciliation](../NOTE_RECONCILIATION.md#the-owners-own-marked-questions-and-where-each-one-lives).

## Proposition, stated so it can fail

In donor-level CD4 pseudobulk from MS and control cerebrospinal fluid and blood,
the EGCG-response and N1-program signatures distinguish disease groups after a
generalised T-cell activation score is included in the same model. If the
signatures lose their separation once activation is accounted for, the human
panel supports activation differences, not a PGAM- or N1-specific axis.

## Why this is open in the source

The paper's own result contains the rival. Both the pro-inflammatory *and* the
pro-regulatory modules were elevated in MS blood and CSF, which the authors
interpret as "a higher activation level of T helper cells in MS that spans across
multiple T helper programs". Two modules that are defined as opposites moving in
the same direction is the signature of a shared third factor. The EGCG signature
was then up in MS blood but not CSF, and N1, P1 and P4 were all higher in MS
blood. None of those comparisons included an activation covariate, and the paper
states as its first limitation that the human analysis is preliminary.

## Strongest rivals

1. **Activation.** A shared activation axis raises every T-helper program score.
2. **Composition.** Pseudobulk over CD4 cells mixes naive, memory, Th subsets and
   Tregs; a disease difference in subset proportion moves any signature without
   any cell changing program.
3. **Tissue and ascertainment.** CSF and blood differ in cell yield, viability and
   subset composition; MS CSF is also pleocytic, so cell-number differences are
   expected a priori.
4. **Clinical covariates.** Age, sex, disease duration and treatment are not in
   the deposit, so they cannot be adjusted for and remain open alternatives.

## What would distinguish them

Rebuild the pseudobulk from the deposited matrices with CD4 identity, minimum
cells per donor and tissue, and the activation score all frozen beforehand. Then,
within tissue, compare disease groups for each signature with and without the
activation score, and report the paired within-donor CSF-minus-blood contrast for
the 10 donors who contribute both tissues. Also report subset composition per
donor, so rival 2 is measured rather than assumed. Donor-level points, not group
means, with 6 donors per group — the precision ceiling is stated before the test,
not after.

## Unit, endpoint, limit

Unit: **donor** (6 MS, 6 idiopathic intracranial hypertension; 10 with both
tissues), recovered from sample titles because the deposit has no donor field.
Endpoint: signature difference by disease within tissue, before and after
activation adjustment, and the paired tissue contrast. Limit: the signatures were
derived from the mouse data this package also analyses, so this is transport of an
exposed construct, not validation; and an RNA signature in circulating or CSF CD4
cells is not evidence of PGAM activity or of a metabolic flux in those cells.

## Decision this would inform

Whether the human arm of this paper is worth developing into a question at all.
If activation absorbs the separation, the useful human question becomes a
different one — whether a serine/one-carbon or PGAM-proximal readout tracks
disease within an activation-matched subset — and that changes which cohort would
be needed.

## Stop condition

Freeze the CD4 definition, inclusion floors, activation score and model before
any disease contrast is computed. If fewer than four donors per group survive the
inclusion floor in a tissue, report that tissue as not assessable rather than
lowering the floor.

## Resolved, 4 October 2026: resolved against the disease interpretation

[Wp-R4](../R4_RESULTS.md) ran this card's discriminating analysis. In CSF no score
separates MS from idiopathic intracranial hypertension: nothing reaches BH <= 0.05,
the modules and signatures all sit at BH 0.93, and the smallest adjusted value is
programme N3 at BH 0.147 (lower in MS). In blood both modules, three programmes and a
proliferation set separate the cohorts, the activation set separates them in the
*opposite* direction, and the activation score correlates with each module across
the ten blood donors at Spearman -0.61 to -0.87. The deciding measurement -
1,000 random gene sets of matched size, scored identically - puts the
pro-inflammatory module (observed +0.055, null interval +0.004 to +0.070,
empirical p = 0.29), the pro-regulatory module (p = 0.19), programme N1
(p = 0.10) and proliferation (p = 0.40) inside the null, and the Table S3 EGCG
signature *below* it (p = 0.000). Only the activation set (p = 0.001), programme
P4 in blood (p = 0.020) and programme P1 in CSF (p = 0.003) exceed their null.

**Conclusion.** The human dataset does not provide module-specific support for
the pathogenicity claim; the Figure S4 blood result is a donor-level axis that
moves any gene set of comparable size. The axis itself is unidentifiable because
GSE138266 deposits no batch, run or processing field. What survives is a
disease-independent compartment effect: the pro-inflammatory module, the
pathogenicity score and both EGCG signatures are higher in CSF than in the same
donor's blood (9-10 of 10 paired donors, Wilcoxon p 0.002-0.006), alongside a
rise in the activation score. This card is closed as **resolved in the negative**
for the disease reading; the compartment effect is handed to Wp-P01 as a question
about what the score measures, not to a new human card.
