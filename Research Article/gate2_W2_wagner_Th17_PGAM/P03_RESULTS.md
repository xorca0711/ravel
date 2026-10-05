# Wp-P03 result: composition, with the within-state term inconclusive

Executed 5 October 2026 under the governed runner. Contract
[config/glucose_decomposition_v1.json](config/glucose_decomposition_v1.json),
entrypoint [scripts/glucose_decomposition_v1.py](scripts/glucose_decomposition_v1.py),
receipt
[analysis/research/runs/wp_glucose_decomposition_v1/receipt.json](../../analysis/research/runs/wp_glucose_decomposition_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

Unit: cells within 8 libraries from 2 animals, crossed over all four conditions.
Two animals cap this at descriptive. No new expression was read.

## The estimator, fixed before any term was computed

Kitagawa decomposition of the animal-paired 1 mM − 25 mM difference in mean
score: `within = Σ p̄ₖ[mₖ(low) − mₖ(high)]`, `composition = Σ [pₖ(low) − pₖ(high)]·m̄ₖ`,
with pooled-condition proportions and means, and the residual reported as an
interaction term.

**Two substitutions the deposit forces,** both declared in the contract rather
than worked around: the authors' Leiden clustering is not deposited, so Wp-R1's
Table S5 marker assignments stand in and the two available labellings replace
the card's coarser-and-finer resolution sweep; cell-cycle phase is not
deposited, so within-library proliferation terciles are the stratum.

## Result

Th17n pathogenicity score, all-marker labelling:

| Animal | Total | Composition | Within | Interaction | Composition share |
|---|---|---|---|---|---|
| Mo1 | +0.133 | **+0.099** | +0.034 | −0.000 | 0.74 |
| Mo2 | +0.109 | **+0.146** | −0.037 | +0.000 | 1.34 |

**Composition carries the effect, in both animals and under every sensitivity.**
Its sign agrees across animals in all four combinations of labelling and
stratification, and its share of the total ranges from 0.68 to 3.45 across
animals, cell types and labellings — a share above 1 meaning the within term
pushes the other way.

**The within-state term is inconclusive, by the card's own stop rule.** Under
the primary labelling it is +0.034 in Mo1 and −0.037 in Mo2: opposite signs in
the only two animals available. The card says to stop there rather than add
conditions until a sign appears, and that is what this run does. Under the
overlap-excluded labelling the within term is negative in both animals
(−0.003, −0.085), which is sign-consistent but in the direction *opposite* to a
within-state rise, and the disagreement between labellings is itself the
reason not to read it.

Sensitivities, Th17n pathogenicity, composition share:

| Variant | Mo1 | Mo2 |
|---|---|---|
| All-marker labelling (primary) | 0.74 | 1.34 |
| Overlap-excluded labelling | 1.02 | 1.78 |
| Proliferation-tercile strata | 0.73 | 1.29 |

Stratifying on proliferation barely moves anything, so the card's
rival 3 — that the score difference follows the cycle-phase difference — is not
what is producing the composition term.

## What is actually moving

| Programme | Proportion at 1 mM | at 25 mM | Score at 1 mM | at 25 mM |
|---|---|---|---|---|
| N1 | 0.22 / 0.24 | 0.57 / 0.59 | −0.53 / −0.55 | −0.50 / −0.45 |
| N2 | 0.65 / 0.59 | 0.05 / 0.01 | +0.02 / +0.06 | −0.01 / +0.12 |
| N3 | 0.13 / 0.18 | 0.38 / 0.40 | +0.41 / +0.39 | +0.26 / +0.32 |

(Mo1 / Mo2.) The mixture turns over almost completely — N1 falls from ~58 % to
~23 % of cells at low glucose while N2 rises from ~3 % to ~62 % — and each
programme's own score barely moves, by 0.03 to 0.15. So the higher average score
at 1 mM is produced by having fewer of the low-scoring N1 cells, not by cells
scoring higher within their programme.

## Why this is weaker evidence than it looks

Programmes are assigned by marker score on the same expression that defines the
pathogenicity score. A composition term is therefore partly guaranteed by
construction: any continuous shift, cut into discrete labels, reappears as a
change in label proportions. This is the card's clustering-artefact rival and
this run does not defeat it. The informative content is the *stability* of the
term — it survives both labellings and the proliferation stratification — not
its bare size.

What a decomposition cannot show at all is that any cell changed state or that
the N1 population was lost. Those are lineage claims. The card's own translation
remains correct: distinguishing "the N1 population shrinks" from "cells within N1
move" requires a Foxp3-reporter time course with division tracking, and that
experiment is now better motivated — the deposited data favour the population
reading, and the within-state term is not estimable at n = 2.

## Bearing on the paper's mechanism

The Discussion builds on the composition reading ("loss or reprogramming of the
N1 subset may underlie the shift") and this decomposition is consistent with it.
But "PGAM inhibition shifts cells toward a pathogenic state" is then the wrong
description of what the glucose data show: the score moves because the mixture
moves. Combined with [Wp-P01](P01_RESULTS.md) — where the pro-inflammatory arm
carries no reliable glucose signal and the whole effect shrinks tenfold without
the HVG filter — the testable consequence to carry forward is about which cells
are present, not how far each cell has travelled.

## Independent check

The reported total difference was recomputed outside the pipeline as the raw
animal-paired difference of mean score: Mo1 0.13333597 and Mo2 0.10895999
against identical reported values (deviations 5.6 × 10⁻¹⁷ and 2.8 × 10⁻¹⁷).
Additivity of the three terms holds to 1.1 × 10⁻¹⁶ across all 24 decompositions.

## Limits

- Two animals. Every term is two numbers; the within term's sign disagreement is
  reported, not resolved.
- Programme labels are not the authors' clusters, so the composition term is not
  comparable to their figure.
- Labels and score share an expression matrix; see above.
- Proliferation score substitutes for cell-cycle phase, which is not deposited.
