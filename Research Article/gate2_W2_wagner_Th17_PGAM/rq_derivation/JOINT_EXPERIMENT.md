# Can A28, A29 and Wp-P02 be run as one preparation?

> **Design clarification, 7 October 2026:** shared preparation is optional. The five listed A29/P02 arms do not constitute a complete PGAM × PHGDH × PEP factorial, and a PEP rescue interpretation needs an explicit control strategy. Each question keeps its own estimand and unit; A30's human compartment comparison is not part of this mouse preparation. See the [audit](../../../docs/audits/2026-10-07-pr140/REPORT.md).

A screen of what the three cards actually require, written because an earlier
summary asserted they share a perturbation. **They do not.** This records the
corrected overlap and what it is worth, so the owner can decide whether to
merge them. It proposes no contract and changes no registered question.

## What each card fixes, read from its own plan

| | A28 | A29 | Wp-P02 |
|---|---|---|---|
| Culture | Th17n at 1 mM and 25 mM glucose, **plus Th17p** | Th17n | Th17n |
| Perturbation axis | **glucose; polarisation** | **PGAM restriction; PEP add-back** | **PGAM × PHGDH inhibitor 2×2** |
| Protein readout | joint Foxp3/CTLA4 **and** IL-17A/IL-17F, per cell | IL-17A per cell | Foxp3 and IL-17 |
| Non-protein readout | — | intracellular **PEP pool**, matched parallel wells | **¹³C serine/glycine** from [U-¹³C]glucose |
| Unit | mouse; wells are technical replicates | mouse; wells are technical replicates | mouse |
| Eligibility | live single CD4, division-tracker gate | live cells, division gate | — |

## The correction

A29 and Wp-P02 **do** share a perturbation axis: both restrict PGAM in Th17n
culture and both need a metabolite measurement from parallel wells of the same
preparation. P02's 2×2 is PGAM × PHGDH; A29 is PGAM ± PEP add-back. These are
compatible perturbation blocks that may share a preparation; they need not be
run together and do not, as listed, form a complete three-factor design.

A28's primary comparison is **glucose 1 mM versus 25 mM**, with polarisation as
its second. It shares the culture system, the animal, the harvest time point,
the division-tracker gate and most of the staining panel — but **not the
perturbation**. Describing all three as "one experiment with a PGAM/PHGDH
perturbation" was wrong about A28, and the error mattered: it would have put a
glucose titration under a PGAM contract.

## What a shared preparation actually buys

The dominant costs here are mice, the harvest, and the stain — not the
treatment arms. One preparation can therefore carry all three if the arms are
laid out as a shared block:

- **Shared:** mice, Th17n differentiation, harvest time point, division
  tracker, and one staining panel that is the union of the three
  (Foxp3, CTLA4, IL-17A, IL-17F) — a superset each card can read its own
  subset from.
- **Arm block 1 (A29 + P02):** vehicle, PGAM-restricted, PHGDH-restricted,
  PGAM+PHGDH, and PGAM + PEP add-back. Parallel wells for metabolomics: PEP /
  2PG / 3PG pools, and ¹³C serine/glycine from [U-¹³C]glucose.
- **Arm block 2 (A28):** Th17n at 1 mM and 25 mM glucose, plus Th17p — same
  mice, same stain, different treatment.

The saving is real but it is a **shared preparation and panel**, not a shared
contrast. Each card keeps its own primary comparison and its own multiplicity
family; nothing is pooled across blocks.

## What must not be merged

- **Multiplicity families stay separate.** A28 declares four tests (two
  comparisons × two protein axes). Folding A29's PEP and IL-17 endpoints into
  that family would silently enlarge it.
- **No cross-block contrast without declaring it first.** Glucose × PGAM is an
  interesting factorial, but it is a *new* question, not one of these three,
  and comparing a glucose arm against a PGAM arm post hoc is the kind of
  unplanned contrast the stop rules in all three cards forbid.
- **The division gate is an eligibility rule, not a power guarantee** (A28's
  own wording). Low glucose slows division; PGAM restriction may too. Each
  block needs its own division matching.

## Feasibility caveats the cards already carry

Two mice and no independent dataset. A28 nominates no effect margin for exactly
that reason and declares itself descriptive until pilot variance is available.
Prior outcome exposure is **full** on all three, so any execution is
exploratory unless it uses evidence that was unexposed when its contract was
written. A shared preparation does not change any of that; it reduces animal
cost and removes between-preparation variance as a confounder between the
blocks.

## The open scientific question this would settle

A29's hypothesis is that PGAM restriction raises IL-17 by **lowering PEP**,
releasing the JunB/BATF/IRF4 complex
([Ishikawa and colleagues 2023](https://doi.org/10.1016/j.celrep.2023.112205)).
The source paper's own ¹³C tracing (Fig. 1E) reports 2PG collapsing from 51 % to
7 % while **3PG and PEP are not significantly changed**, which argues against
that route as stated — but that measurement is a 15-minute label ratio in one
condition, not a pool size, and a labelling ratio can hold steady while the
absolute pool falls. **Measuring the absolute PEP pool is the discriminating
observation, and the PEP add-back arm is its control.** That is the single
strongest reason to run block 1 at all, and it is why A29 and P02 belong
together: the ¹³C arm and the pool-size arm answer the same question from two
directions.

## Decision requested

1. Merge **A29 and Wp-P02** into one factorial design — they share a
   perturbation axis and a preparation. Recommended.
2. Run **A28** off the same mice, stain and harvest as a separate arm block,
   keeping its own contract and family. Optional; the saving is animals and
   between-preparation variance, not design.
3. Leave all three independent.

No contract is frozen and no card is edited by this document.
