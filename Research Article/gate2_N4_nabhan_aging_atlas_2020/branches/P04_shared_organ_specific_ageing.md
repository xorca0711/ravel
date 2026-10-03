# Nb5-P04 Shared and organ-specific ageing within immune identities

## Question and decision

Within source-qualified immune identities, are age-associated RNA changes
consistent across organs or dependent on the organ context? Decide whether a
future question should target a shared response or an organ-specific mechanism.
This is an agent-proposed extension from the multi-organ design, distinct from
reproducing published clusters and from the owner's microglial trajectory idea.

## Hypothesis and strongest rival

The working hypothesis is a bounded common component plus organ-specific
deviations. The strongest rival is comparison of non-equivalent resident cell
identities or different subtype mixtures. Processing, gene detection, sex and
unmatched mice could also create apparent organ specificity.

## Required metadata and measurement

Need original mouse IDs shared across organs, tissue/region, matched age and
sex, assay and batch, source-supported identity mapping, raw-count eligibility
and per-animal type coverage. Microglia, Kupffer cells and lung macrophages
must retain their distinct identities; broad myeloid labels do not establish
a common baseline. Blood contamination and ambiguous identities remain explicit.

The biological unit is mouse; organs and assays are repeated observations.
The endpoint is an organ-specific age contrast in a predeclared gene/programme
within each eligible identity, followed by the difference between those age
contrasts. A pooled organ mean is not that endpoint.

## Bounded analysis and alternatives

1. Construct overlap and identity-compatibility tables before fitting outcomes.
2. Freeze a small family of endpoints and organ/identity comparisons from
   independent biological rationale. Analyze technologies separately.
3. Estimate within-organ age associations, then a supported age-by-organ
   interaction with mouse blocking or a suitable repeated-measure model.
   Preserve mouse blocks in resampling; show unpaired strata separately.
4. Repeat after subtype accounting and removal of ambiguous source labels.
   Report complete-pair sensitivity and how selective organ missingness changes
   the target population. Do not turn an absent type into zero expression.

Consistent within-organ contrasts motivate a shared-response candidate;
supported interaction motivates organ-context work; disappearance under identity
control favors composition/annotation. A wide interval cannot establish that
two organs have the same response. Complete organ-by-batch confounding stops
the interaction; incomplete pairing restricts the evidence.

## Further RQ frame and limit

Ask what tissue-context measurement could distinguish a systemic association
from a local one. An independent cohort and a direct functional endpoint would
be needed before a shared regulator or circulating cause is asserted. Organs
from one animal are not independent replication.

Relation: [A3](../../../docs/research_dossiers/A3.md) and
[Nb4-P05](../../gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/proposals/P05_immune_identity_state.md)
offer history/state questions but do not own this new cross-organ estimand.
No claim that the broad question is novel is made.

**Additional-analysis frame:** paired coverage map, per-organ mouse-level
contrasts and interaction intervals, with identity/mixture sensitivities.

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
