# A16: does Cd177 mark a cell-intrinsic priming programme, or the transcriptional neighbourhood a cell occupies

**Registered as proposed on 28 September 2026, pending the owner's retain or reject. Stage 1 was
authorized and executed the same day** — see [STAGE1_RESULTS.md](reports/STAGE1_RESULTS.md). The
question adds no claim row, and no graded claim is available.

## The question in one sentence

When a transitional alveolar cell is Cd177-positive, is that a fact about the cell, or a fact about
where the cell sits in the transcriptional landscape?

## What it stands on, and what that is worth

The founding observation is owned by the [England re-analysis](../../Research%20Article/gate2_C2_england_2025/RESULTS_FOLLOWUP.md),
not by this question. In the two libraries that carry the contrast at all, Cd177-positive cells
inside the frozen transitional gate score higher on priming-associated RNA (+1.60 and +2.17), on AT2
identity (+0.94, +1.41) and on AT1 identity (+0.85, +0.52), and lower on Itga2 (−0.48, −0.75) and on
both remodelling modules. Those directions survive depth control: under the three methods available
in both libraries all seven associations keep their sign, and residualising on log depth and detected
genes retains 87 to 159 per cent of each effect.

Then conditioning on position largely dissolves them. Repeating the same contrast **within** each
round-2 subcluster, Itga2 flips positive in 5 of 7 testable subclusters and AT2 identity ranges from
−0.36 to +1.27, while priming-associated RNA persists in 5 of 7 (+0.36, +0.36, +0.60, +1.31, +2.32).

That is the entire basis of this question: one study, two libraries, one marker measured as RNA.
**It is not evidence for A16.** The register's own rule is that reuse never adds independent
evidence. The England package owns those numbers and the interpretation recorded there, and A16 opens
with a question about them rather than with support for an answer.

## Why it is a question and not a footnote

Both readings predict exactly the observation above, so the marginal association cannot choose
between them. The residual after conditioning is not self-interpreting either: cluster boundaries are
arbitrary, so a surviving within-cluster effect may be composition at a finer scale. There are also
two ways for the residual to be an artefact rather than a state. Cd177 is canonically a neutrophil
surface protein and the priming module (Lcn2, Lrg1, Retnla, Ptgs1) is inflammation-associated, so
ambient RNA from neutrophils would produce a residual association with no cell state behind it. And
Cd177 UMIs in positive cells spread from 1 to 53 with no break, so the positive/negative split is a
detection threshold rather than a bimodal population.

The distinction matters biologically, not only statistically. If Cd177 carries information beyond
position, it is a candidate handle for isolating primed cells prospectively. If it does not, it is a
coordinate, and an experiment that sorts on it is selecting a neighbourhood — still useful, but a
different claim.

## Register readiness: partly computable, discriminating test blocked

| Layer | State |
|---|---|
| Attribution within the existing matrices | **Executed, inconclusive on specificity.** Ambient neutrophil origin and threshold dependence are excluded; the detection-matched null could not settle generic gradient behaviour because Cd177 is hard to match. [Results](reports/STAGE1_RESULTS.md) |
| External transfer | **Blocked.** No deposit pairs surface CD177 separation with a proliferation or fate readout in lung; see [PUBLIC_DATA_SEARCH.md](reports/PUBLIC_DATA_SEARCH.md) |
| The discriminating measurement | **Not computable from any RNA matrix.** Needs prospective separation on CD177 protein with a measured outcome |

Stage 1 has now run. It did not close the question and did not reach the conclusion its contract
permits: ambient origin and threshold dependence are excluded, but the specificity clause failed in
the best-powered unit and was underpowered elsewhere. Stage 1's ceiling is reached, so the next action
is the data request or the experiment, not another conditioning analysis.

## Layout

| Path | Contents |
|---|---|
| [RATIONALE.md](RATIONALE.md) | Why attribution is a separate question, what the England work supports, and the rivals |
| [PLAN.md](PLAN.md) | Stage 0 to Stage 4, with the frozen estimands and decision rules |
| [config/a16_question_contract.json](config/a16_question_contract.json) | The machine-readable freeze, including exposure |
| [reports/PUBLIC_DATA_SEARCH.md](reports/PUBLIC_DATA_SEARCH.md) | The 28 September 2026 search, recorded as a negative result |
| [reports/STAGE1_ERRATUM.md](reports/STAGE1_ERRATUM.md) | The population correction, why Stage 1 runs two arms |
| [reports/STAGE1_RESULTS.md](reports/STAGE1_RESULTS.md) | Executed C1 to C5, the verdict and what changes |

## Seven things a later session must not do

1. Do not report the England FU_C result as independent confirmation of anything here. It is the
   observation that raises the question, and it was seen before this folder was written.
2. Do not treat a within-neighbourhood association that survives conditioning as cell-intrinsic
   function. Surviving conditioning makes a marker informative about position-independent RNA state;
   function needs a measured outcome.
3. Do not substitute a cycling RNA score for a proliferation readout. The cycling contrast is
   library-discordant in the founding data (−0.04 against +0.48), which is itself why the outcome
   must be measured rather than inferred.
4. Do not pool the two libraries to gain power. GSM7890835 and GSM7890836 are the only two carrying
   the contrast, they disagree on the cycling endpoint, and pooling would hide that.
5. Do not lower the 30-cell-per-side floor, or relax the transitional gate, to make a subcluster
   testable. Under thinning one library already falls to 26 positives; the honest report of that is
   "not assessed", which is what the England follow-up recorded.
6. Do not change the gate or module definitions. The transitional gate is Cldn4, Ndrg1, Sox9 with at
   least two of three detected, and the modules are frozen in the England continuation contract.
7. Do not add or regrade a claim row. This question has no measured endpoint of its own until the
   owner retains it and Stage 1 runs, and no graded claim until a prospective readout exists.
