# A16 Stage 1 erratum: the contract's population declaration did not match the pipeline under test

**Dated 28 September 2026, written before any A16 endpoint was computed.** Recorded as an erratum
rather than an edit to the freeze, following the house rule that corrections are documented and
original bytes preserved.

## What the contract said

`config/a16_question_contract.json` declares the Stage 1 population as *"Cells passing the frozen
transitional gate (Cldn4, Ndrg1, Sox9, at least two of three detected) in the round-2 Experiment-1
embedding"*, with the unit *"the sequencing library … never a pooled two-library aggregate"*.

## What the pipeline under test actually did

Reading `scripts/run_followup.py` at the FU_C block before execution shows the residual A16 exists to
interrogate was computed differently:

| | contract declaration | FU_C as implemented |
|---|---|---|
| Population | transitional gate only | **all `primary_include` cells** in each subcluster |
| Experiments | Experiment 1 | **both**, Experiment 1 and Experiment 2 |
| Libraries | per library, never pooled | **pooled within experiment** across its 10 libraries |

The 7 testable subclusters are Experiment-1 clusters 10, 12, 16, 17, 18 and Experiment-2 clusters 10
and 12, with 252 to 1,583 cells and 36 to 321 Cd177-positive cells each — an order of magnitude more
positives than the transitional gate's 79 and 60, which alone shows the gate was not applied.

## Why this matters, and what is being done about it

C3 asks whether Cd177's surviving effect is unusual **among genes matched to it, run through the
identical pipeline**. A null computed on a different population would not be a null for the residual
in question, so honouring the contract's population literally would produce a well-formed answer to
the wrong question.

Stage 1 therefore runs **two arms**, each matched to its own reference:

- **Arm A, marginal.** The transitional gate, per library, in GSM7890835 and GSM7890836. This is the
  population the contract declares and the one that produced the marginal EN5 effects (+1.60, +2.17).
- **Arm B, within-subcluster.** FU_C's own population — all `primary_include` cells in each of the 7
  testable subclusters, both experiments, pooled within experiment. This is the residual under test.

Matching for C3 is computed **within each arm unit** rather than always in the transitional gate, for
the same reason: a gene matched on its detection rate in one population is not matched in another.

## Two consequences that are disclosed, not fixed

1. **Arm B pools libraries within an experiment**, so library composition inside a subcluster is an
   uncontrolled confounder of the residual. This is a property of the result A16 inherited, not a
   choice made here. It is one of the things continuous neighbourhood matching (C1) would address if
   the residual survives C3 and C4, and per-subcluster library composition is reported alongside the
   estimates so a reader can see it.
2. **Arm B is not restricted to transitional cells**, so its Cd177 contrast is not a within-state
   contrast in the sense the A16 proposition requires. The proposition concerns transitional cells;
   the residual under test concerns all epithelial cells in a neighbourhood. Both are reported, and no
   result from Arm B may be described as a within-state effect.

## What this erratum does not change

No estimand, decision rule, floor, prohibition or permitted-conclusion wording is altered. The
primary endpoint remains priming-associated RNA, the 30-cell floor stands, and the ceiling on what
Stage 1 may conclude is unchanged.
