# A13 rationale: from a broad niche idea to one predictor pair, and why its failure is narrow

Written 28 September 2026 over completed work. Nothing here rescores or refits. A13 began as a
broad question about fibroblast contributions to epithelial plasticity and was narrowed, through
two coverage gates and one amended pilot, to a single predictor-outcome pair that did not work.
This document traces that narrowing, states what the negative result covers, and is explicit that
it covers much less than the original question.

## The original proposition

Fibroblasts are not passive neighbours in alveolar injury. If they contribute to whether
epithelial cells enter or persist in a transitional state, then a fibroblast programme should
carry information about an epithelial plasticity readout beyond what macrophage IL-1 signalling
and shared inflammation already carry.

That proposition is about the niche. What was actually tested is much narrower, and the gap
between the two is the main point of this document.

## How the question narrowed

**Step 1: the compartment rule changed.** The historical gate required each donor's largest
single macrophage label. The executed pilot uses a **broad assigned macrophage aggregate** with
fixed AT2 and fixed alveolar-fibroblast labels instead. This is an
[explicit amendment](../../docs/roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md),
not a reinterpretation of the old gate: fixed labels avoid choosing each donor's largest
fibroblast population, which would have made the fibroblast definition donor-dependent. The
consequence is that the executed pilot **does not demonstrate eligibility for the original
test**, and the [historical coverage result](reports/COVERAGE_RESULTS.md) retains its own scope.

**Step 2: the outcome became an RNA proxy.** Epithelial plasticity is not measured in this
cohort. The outcome is the fixed HPCS-without-ADI-or-operational-markers module: 91 original
mouse genes, 73 frozen human mappings, 72 present in the assay. It is an RNA proxy for a
transitional state. It is **not lineage potential**, not a fate measurement, and not the same
instrument as A11's TMM-normalized score — it is a newly declared mean log2(1+CPM) measurement.

**Step 3: the predictor became one hallmark module.** The fibroblast programme is the MSigDB
TGF-beta hallmark minus the overlapping outcome gene TGIF1: 53 frozen, 52 assayed. It is
**TGF-beta pathway RNA, not active TGF-beta** — the distinction A15 exists to pursue, and the
reason this predictor cannot speak to latent-TGF-beta activation.

So the tested pair is: *does TGF-beta pathway RNA in fixed alveolar fibroblasts add information
about an HPCS-proxy RNA score in fixed AT2 cells, beyond macrophage IL1B, macrophage mixture and
TNF?* That is one instantiation of the niche idea, chosen for availability.

## The result

The primary comparison — joint against source-plus-TNF on identical held-out patients — **worsens
by 0.004181 MSE** (RMSE 0.2283 to 0.2373), and worsens in every eligible predeclared sensitivity
(ridge 0.1 and 10, the 30-cell floor, confidence 0.3). At the 100-cell floor fewer than ten
patients remain and no model is fit. Eight of twelve patients have smaller individual errors,
which does not overturn the aggregate loss: votes are not the frozen loss function, and reporting
them as if they were would be selecting a favourable statistic after the fact.

Panel (c) of the [shared ladder figure](../A12_recipient_context/figures/A12_F01_heldout_model_ladder.png)
carries the result in its proper context, and that context weakens the instrument considerably:
**no model in A13's ladder beats the training mean.** The mean baseline is 0.2167; the best
fitted model is 0.2113 at alpha=10 and 0.2283 at the primary alpha. A comparison between two
models that both predict worse than a constant is a poor test of whether a programme contributes.

**Decision, unchanged:** do not expand this fibroblast programme on this cohort. The fixed test
gives no predictive reason to prefer it over the source-and-TNF comparator.

## What the negative result does and does not cover

It covers: this programme, this outcome proxy, this cohort, these twelve paired patients, this
fixed procedure.

It does not cover:

1. **Fibroblast contributions in general.** One hallmark module is not the fibroblast
   compartment's repertoire, and a pathway module is not a cell state.
2. **A zero effect.** No equivalence margin was set and none can be inferred from twelve
   dependent leave-one-patient-out fold losses. "No predictive gain" is not "no effect".
3. **Active TGF-beta signalling.** Pathway RNA does not measure latent-TGF-beta activation;
   [A15](../A15_epithelial_integrin_tgfb_activation/README.md) owns that question and is
   unaffected by this result.
4. **Epithelial plasticity.** The outcome is an RNA proxy; a fate or lineage measurement could
   behave differently.
5. **Other cohorts.** Both named external candidates were resolved as ineligible on design, not
   on outcome — GSE233844 is a PBMC study and cannot supply a lung triad, and GSE122960 yields
   **3 of 16** subjects passing the 50-cell floor across all diagnoses under exact author labels
   (2 restricting to donor/IPF, with no represented IPF subject passing). At floors 30 and 100 the
   all-diagnosis totals are 9 and 0. Even granting the separate cryobiopsy one subject cannot
   reach ten.

## Rivals to the negative result itself

Stated because a null needs its alternatives examined as much as a positive does.

1. **The comparator is too strong or the outcome too noisy.** With no model beating the mean, the
   design may lack the resolution to detect an increment of any plausible size. This is the most
   likely explanation of the result and it is not a biological finding.
2. **The proxy is the wrong outcome.** An HPCS-derived RNA module in AT2 cells may not track the
   plasticity the niche idea is about.
3. **The programme is the wrong predictor.** A hallmark pathway module averages over genes that
   need not move together in fibroblasts.
4. **Twelve patients.** A real but modest increment would not be recoverable at this size, and
   the sensitivities repeat the same twelve or eighteen units rather than adding independent ones.
5. **Shared inflammation and composition.** As in A12, a single disease axis and within-compartment
   mixture remain uncontrolled, and paired differencing does not remove them.
6. **Assigned-source conditionality.** The macrophage source is the assigned compartment; cells
   without confident labels carry most of the recovered IL1B RNA
   ([map](../A12_recipient_context/reports/A12_S1_SOURCE_IDENTITY_MAP.md)).

## Why this does not contradict A12

A12's positive epithelial result and A13's negative result share a cohort, a normalization and a
fit, and they are not in tension. They differ in predictor (a recipient receptor index against a
fibroblast pathway module), in recipient compartment for the added term, and in outcome (an
inflammatory hallmark against an epithelial transitional proxy). A12's own fibroblast arm also
failed to improve, so the pattern across both pilots is consistent: in this cohort, added terms
measured **in the recipient epithelium** helped, and added terms measured **in fibroblasts** did
not. Whether that asymmetry is biological or a residual-variance artefact is open, and is stated
as such in [A12's rationale](../A12_recipient_context/RATIONALE.md).

## What would justify reopening A13

Not a search for a better-performing signature on this cohort — that is tuning, and it is
prohibited. Reopening needs: an independently motivated fibroblast programme nominated on
biological grounds before any fit; complete comparable triads in a cohort with enough units; an
outcome that is not an RNA proxy of the same compartment's state, or a stated argument for why a
proxy suffices; and an evaluation not used to choose the programme. Absent a stronger case, there
is no new computational task here.

## Connections and boundaries

- **A12** shares the cohort, normalization and fit; see its
  [rationale](../A12_recipient_context/RATIONALE.md) and
  [plan](../A12_recipient_context/PLAN.md).
- **A12-S1** owns the identity of the unlabelled IL1B-carrying cells and conditions the source
  term used here.
- **A15** owns epithelial integrin-mediated activation of latent TGF-beta. A13's TGF-beta pathway
  RNA in fibroblasts is a different measurement in a different compartment.
- **A11** owns the lesion-associated programme against shared plasticity and the TMM-normalized
  instrument; A13's score is separately declared and is not a rerun of it.
- **A14** owns fibroblast IL-1 reception as a perturbation; A13's null on an RNA association does
  not bear on that design.
- **A2** and **A9** own the AREG source and receptor-competence questions in fibroblasts.

Measurement contracts: [MC1](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1) for units, confounding
and endpoints; [MC3](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc3) for state and source identity;
[MC5](../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc5) for programme dependence and validation.