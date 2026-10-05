# Wp-P03 — Is the low-glucose pathogenicity shift composition or within-state change?

**Status:** proposed, outcome-exposed. Decomposition of a published aggregate.

**Owner's framing, 4 October 2026.** The Discussion note marks this as "a role
for PGAM in maintaining a niche pro-regulatory state in Th17n cells?" The
decomposition below is the measurable form of *maintaining*: a maintenance claim
needs the N1 population to persist, not merely the condition average to move.
See [note reconciliation](../NOTE_RECONCILIATION.md#the-owners-own-marked-questions-and-where-each-one-lives).

## Proposition, stated so it can fail

The higher Th17n pathogenicity score under 1 mM glucose is produced mainly by a
change in the *mixture* of programs — fewer N1 cells, more N2 — rather than by
the same program shifting its score. If instead the score rises within every
program, the glucose effect is a within-state change and N1 loss is a consequence
rather than the mechanism.

## Why this is open in the source

The paper reports both components but never separates them. The score is higher
at low glucose (p < 10⁻³³, cell-wise), and that increase is attributed to
"mitigation of the pro-regulatory module". Separately, N1 is described as the one
Th17n program "robustly detected under both glucose conditions" while N2 is
"mostly restricted to low-glucose conditions", and N1 has the lowest
pathogenicity score. Those two facts are jointly sufficient to produce a higher
average score at low glucose *without any cell changing state*. The Discussion
then builds on the composition reading ("loss or reprogramming of the N1 subset
may underlie the shift"), so the distinction matters for the paper's own
mechanism.

## Strongest rivals

1. **Pure composition.** Program proportions change; within-program scores do
   not. Then PGAM's relevance is about which cells survive or are generated, and
   "shifting cells toward a pathogenic state" is the wrong description.
2. **Pure within-state.** Every program's score rises at low glucose. Then the
   cluster redistribution is a secondary consequence of a continuous shift being
   cut into discrete clusters.
3. **Proliferation.** Low glucose suppressed proliferation, cell-cycle phase
   composition differs between conditions, and phase was regressed out of the
   latent space as a nuisance covariate. A score difference could follow the
   cycle-phase difference rather than either of the above.
4. **Clustering artefact.** Clusters derived on the same data that defines
   conditions can absorb the condition effect; a program "restricted to" one
   condition may be a boundary drawn through a continuum.

## What would distinguish them

A decomposition computed on the re-derived single-cell data: total score
difference between glucose arms split into a between-program (composition) term
and a within-program term, with the programs' proportions held at the
pooled-condition values for the within term. Report each program's within-program
score difference with its cell count, both score arms separately, and the same
decomposition recomputed (a) with cell-cycle phase as a stratum instead of a
regressed-out covariate and (b) at a coarser and finer Leiden resolution, so the
cluster-boundary rival is visible rather than assumed away.

## Unit, endpoint, limit

Unit: cells within 8 libraries from **2 animals**, crossed so that both animals
appear in all four conditions with two libraries each. A within-animal paired
contrast is therefore available, but at n = 2 it caps the result at descriptive,
and the published cell-wise p value has the same ceiling. Endpoint: the
composition and within-state terms as proportions of the total score difference,
reported per library so that library-to-library consistency is visible. Limit: a
decomposition on derived clusters cannot establish that a cell changed state or
that a program was lost; both require lineage or time-resolved measurement, which
this deposit does not contain.

## Decision this would inform

Whether the testable consequence of PGAM inhibition is "the N1 population
shrinks" or "cells within N1 move", which are distinguishable at the bench by a
Foxp3-reporter time course with division tracking — and which imply different
readouts for any intervention aimed at preserving the regulatory program.

## Stop condition

Freeze the decomposition estimator, the resolutions to be reported and the
covariate treatment before computing any term. If composition and within-state
terms disagree in sign across the two animals, report inconclusive; two animals
cannot adjudicate that.

**Repository connection:** this is the same composition-versus-within-state
discipline applied across the lung questions; see the
[repository context](../REPOSITORY_CONTEXT.md). Nothing about the Th17
compartment makes it exempt.

## Evidence added 4 October 2026

[Wp-R1](../R1_RESULTS.md) separates the two mechanisms this card distinguishes.
**Within-state change:** the pathogenicity score rises at 1 mM glucose in 4/4
animal-paired library comparisons, and in all four the pro-regulatory arm falls
while the pro-inflammatory arm does not rise. **Composition change:** the
marker-assigned programme composition shifts drastically with glucose - in Th17n,
N2 is 58-65 % of cells at 1 mM and 1-5 % at 25 mM, with N1 and N3 taking its
place. Both are present, so the card's premise holds; what the deposit cannot
settle is which is primary, because the programme labels here are marker-score
assignments rather than the authors' clusters, and proliferation also differs by
condition (higher at 25 mM in 4/4 pairs). A sorted-population experiment, not a
reanalysis, is the discriminating measurement.

## Executed 5 October 2026 — see [P03_RESULTS.md](../P03_RESULTS.md)

Outcome: **composition**, with the within-state term **inconclusive** under this
card's own stop condition. The composition term is positive in both animals and
under every labelling and stratification (share 0.68 to 3.45); the within term is
+0.034 in Mo1 and -0.037 in Mo2 under the primary labelling, so the card's rule —
report inconclusive if the terms disagree in sign across the two animals — fires
and no further labelling or stratum was added. Proliferation stratification moves
the split by less than 0.02 of share, which addresses rival 3 directly. Rival 4,
the clustering artefact, is not defeated: programmes are assigned on the same
expression that defines the score, so some composition term is guaranteed by
construction, and the informative content is the term's stability across
labellings rather than its size.

Two substitutions were forced by the deposit and are declared in the contract:
marker-assigned programmes instead of the authors' undeposited Leiden clusters
(so the two available labellings replace the resolution sweep), and
within-library proliferation terciles instead of cell-cycle phase.

The Foxp3-reporter time course with division tracking that this card names is now
better motivated, because the deposited data favour the population reading and
the within-state term is not estimable at n = 2.
