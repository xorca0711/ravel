# Nb5-P07 Sex dependence of age associations

## Question and decision

For an eligible tissue/type endpoint, does the age contrast differ between
sexes? Decide whether a subsequent analysis can use a shared age effect or
needs an explicitly sex-specific question. This is an agent-proposed conditional
design branch; recorded sex does not guarantee an estimable interaction.

## Hypothesis and strongest rival

The hypothesis is an age-by-sex interaction within the same tissue/type.
The strongest rival is unequal age/assay/batch coverage or a sex-dependent
mixture of subtypes. Separate significance in one sex and non-significance
in the other does not demonstrate an interaction.

## Required metadata and measurement

Need validated sex and mouse IDs, age, tissue/type, assay, processing batch
and unit coverage for each design cell. Sex-specific organs cannot establish
a same-tissue between-sex interaction. Do not infer missing sex from expression
and then use the same genes as evidence for the endpoint without an explicit
separate validation design.

The unit is mouse. The estimand is the difference between the two within-sex
age contrasts on a declared scale. Start with one endpoint qualified by P01
or P05 and an exact age comparison; do not select the tissue with the smallest
interaction p-value.

## Bounded analysis and alternatives

1. Check age-by-sex-by-assay-by-batch support and design rank using metadata.
2. If eligible, freeze the endpoint, covariates and interaction model. Include
   the relevant main effects and show all mouse observations.
3. Report the interaction estimate and interval, balanced-support sensitivity
   and animal influence. Keep multi-tissue or multi-endpoint testing in a
   declared multiplicity family.

A supported interaction motivates independent replication and a bounded
sex-specific mechanism question. An imprecise or null interaction does not
prove equality. If one sex is absent from an age stratum, retain stratified
descriptions and hold the interaction; do not impute missing groups or add
cells as independent units.

## Further RQ frame and limit

Expression interactions cannot identify hormonal causation or sex-specific
repair outcomes. Required precision and biological effect margins remain
unknown. No current A-series question is altered; the output may instead be
a better population definition or a data-acquisition requirement.

**Additional-analysis frame:** design-support matrix, per-mouse contrasts and
an interaction interval, with any structural missingness made visible.

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
