# Nb5-P08 Age shape versus developmental and survivor selection

## Question and decision

Does a qualified endpoint support a monotonic adult-age association, a plateau
or a change in shape? Decide whether binary young/old pooling is an adequate
description and which age interval deserves independent follow-up.
This is an agent-proposed branch, distinct from inferring a single-cell trajectory.

## Hypothesis and strongest rival

The hypothesis is a reproducible nonlinear association within a stable cell
identity. The strongest rival is changing animal-cohort composition, including
developmental differences at the youngest age and selective survival at the
oldest, together with batch and sex imbalance. Cross-sectional data cannot
fully distinguish these from within-animal change.

## Required metadata and measurement

Need exact source ages, unique mice, sex, assay, batch, tissue/type, health or
exclusion information when recorded, and comparable cell support across ages.
Unrecorded cohort, housing or survival histories remain unknown rather than
inferred from transcription. P01/P05 supply the qualified endpoint.

The unit is mouse. Endpoints are per-age animal means/fractions on a fixed
scale and prespecified differences between age contrasts. Primary shape
assessment concerns adult strata; the youngest and oldest groups require
separate inclusion sensitivities. No cell-level pseudotime is a substitute
for age or for repeated observation of an animal.

## Bounded analysis and alternatives

1. Display metadata coverage before examining endpoint shape; freeze eligible
   ages and the distinction between adult and developmental comparisons.
2. Report each age separately. Compare a small declared family, such as a
   linear adult-age description versus categorical age effects, only when
   independent-unit coverage and residual degrees of freedom permit it.
3. Use whole-mouse held-out assessment where supported; show influence of the
   oldest group and supported sex/batch restrictions. Do not search flexible
   spline knots or a best breakpoint through sparse data.

A reproducible shape difference motivates a targeted age-window study.
If it depends on one mouse, a missing stratum or complete batch confounding,
hold the shape claim. An apparent oldest-age reversal cannot be called
rejuvenation, and a fitted breakpoint is not a measured biological switch.

## Further RQ frame and limit

The missing discriminator is independent longitudinal or cohort-balanced
evidence with an appropriate functional endpoint. A cross-sectional atlas
cannot estimate an individual's ageing rate or survival benefit. This branch
may refine sampling and contrasts without becoming a new mechanism RQ.

**Additional-analysis frame:** age-stratified mouse observations, a bounded
model-comparison summary and youngest/oldest-group sensitivity panels.

## Execution and RQ status

Planned, outcome-exposed and unrun. Apply the [shared plan](../ANALYSIS_TRIAL_PLAN.md)
and [data qualification rules](../DATASETS.md). A separate committed contract,
input/code hashes, verified receipt and result report are required for execution.
Source counts, exact filtering and independent-unit precision are unqualified.
No numerical eligibility floor, meaningful-effect margin or sample size has
been invented. New settings chosen after results require a prospective amendment.

The [branch register](../BRANCH_REGISTER.md) defines the later RQ-development
decision. This card does not establish novelty, human acceptance, a new global
question or experimental access.
