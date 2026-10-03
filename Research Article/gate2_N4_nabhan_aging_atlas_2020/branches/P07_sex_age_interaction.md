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

First outcome-exposed pass completed 3 October 2026. Age-by-sex coverage and male-only descriptive sensitivity executed. The missing old female stratum blocks a 3-versus-24-month interaction model.

Read the [current result and amendments](../RESULTS.md),
[figures](../FIGURES.md) and [execution ledger](../EXECUTION_VALIDATION.md)
before extending the original plan above. No human retain/reject decision,
claim promotion or global RQ allocation is recorded. All branches remain
available; a further numerical stage requires a new frozen contract.

## Provisional RQ derivation

The [current P07 derivation](../rq_derivation/P07.md) develops the observation,
biological gap, strongest rival and discriminating prediction, with primary-source
precedent and independent-evidence limits. It is a proposal for scientific review;
no global RQ registration or human acceptance is recorded.
