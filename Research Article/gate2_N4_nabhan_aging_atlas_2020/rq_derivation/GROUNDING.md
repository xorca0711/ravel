# Grounding decisions before further numerical analysis

3 October 2026. The derivation stage used existing frozen results, primary
papers and public deposit descriptions. That work changed candidate framing
and exposed source limitations. It did not execute a new biological fit,
produce a new estimate or confirm a candidate.

## What can change a decision

| Branch | Consequential uncertainty | Current action and stopping point |
|---|---|---|
| P01/P05 | Normal differentiated phenotype versus impaired barrier maintenance; broad mesenchymal label versus a defined stromal population | Source review completed. Next qualify identities and availability of an independent functional endpoint. RNA-only availability restricts the question to localization/association; more marker scores do not resolve function. |
| P02 | Additional microglial configuration versus endpoint mixture, continuous response or region/sex imbalance | All-age input recovery is complete, but the model is unrun. First specify a bounded, exposed model comparison with the requirements below. Missing old females prevents a full-age sex interaction. |
| P03 | Can the proposed history contrast be distinguished from age, origin and current context? | Normal-age reference identified. Require a compatible independent history design and fixed endpoint; no pathway rescan to rescue prior negatives. |
| P04 | Are comparable states observed in paired organs from the same animals? | Exact non-spleen CD4/CD8 support is insufficient in the completed follow-up. New source qualification must establish common support before a cross-organ model. |
| P06 | Within-state concentration versus state redistribution and receptor recovery | Broad subtype follow-up completed previously. Next qualify fine states and receptor denominators. Public GSE145562 pooling prevents treating its contributing mice as separate replicates without recovered identity. |
| P07 | Does the selected parent endpoint have a supported age-by-sex contrast? | Current full-age interaction is unidentifiable. Qualify an external complete design; do not fill missing older females through regression. |
| P08 | Does an interval difference reflect age, cohort composition or selective survival? | Current results remain cross-sectional. Seek the relevant inclusion/attrition and age-cohort information before an age-window inference. |

This prioritizes decision-changing evidence, not preferred RQs. Negative,
ineligible and ambiguous outcomes remain in their existing records. No new
generic QC panel, whole-atlas gene scan or flexible age-curve fit is needed to
initiate the current proposals.

## Microglial model requirements

This is a design brief for scientific review, not a frozen executable contract.
It addresses the main unfinished numerical job explicitly.

1. **Population and unit:** use exact source-labelled microglia with qualified
   mouse, age and brain region. Keep macrophages distinct. Declare any literal
   region-label normalization. Record processing metadata availability. All
   regions and cells from a held-out mouse must stay out of training.
2. **Sex scope:** separate the all-sex descriptive question from a male-only
   sensitivity question. The former retains sex confounding at 24 months; the
   latter has sparse middle-age animals. Neither estimates the missing female
   old-age trajectory or supplies independent study validation.
3. **Competing models:** define an endpoint-distribution mixture, a smooth
   age-response baseline and an additional middle-age component. Prespecify
   the likelihood/scale, model complexity, feature family and tuning rules.
   These choices remain unresolved; the model should not be frozen while they
   are placeholders. A middle-age component winning on training fit is not
   evidence against simpler models.
4. **Training isolation:** fit normalization-dependent parameters, variable-gene
   selection, state definitions and tuning only in training animals. Age-label
   use and previously exposed signatures must be declared. Do not discover a
   middle-age signature on all animals and then call its held-out score a test.
5. **Endpoint and interpretation:** aggregate predictive performance at the
   animal level and display animal variation. Mean-profile mixture inadequacy
   alone supports a limitation of that mean model, not a discrete cell state.
   Separate distributional evidence, state coherence and nonlinear age response.
   A three-age dataset gives weak information about the shape of a continuum.
6. **Stop or narrow:** if animal support cannot identify the competing models,
   report non-identifiability or a bounded feasibility result. Do not expand
   gene searches or relax eligibility to obtain a state. No arbitrary effect
   margin, power claim or disease function is supplied by this brief.
7. **External test:** qualify individual units and baseline controls in a new
   study before testing a prespecified transferable endpoint. Different middle
   ages, whole-brain versus region sampling, and sex differences may require a
   narrower comparison. Internal animal holdout remains exposed exploration.

The source availability problem is resolved. Defining an identifiable model
and qualifying its biological interpretation are the next tasks. The novelty
review makes an indiscriminate all-sex cluster fit a poor substitute for them;
it does not make the unfinished model complete or technically impossible.

## Execution transition

After the scientific scope is settled, write a new versioned contract with
exact source/code hashes, units, outcomes, exclusions, exposure, multiplicity
and stop rules, commit its freeze, then use the research runner. Keep historical
outputs intact. A future exploratory run can proceed without pretending that
the proposal has already received global RQ acceptance; confirmation requires
its additional design conditions. Laboratory feasibility, assays and precision
remain separate from public computational access.
