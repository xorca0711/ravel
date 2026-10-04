# Wp-P03 — Is the low-glucose pathogenicity shift composition or within-state change?

**Status:** proposed, outcome-exposed. Decomposition of a published aggregate.

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
