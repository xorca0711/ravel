# A27: fixed CD8 RNA states and source-table representation

Completed 3 November 2026 under freeze `c09108f`. [Receipt](../../../analysis/research/runs/A27_state_representation_v1_20261103/receipt.json) verifies. All exact joins and partition checks passed; original broad CD8 depth-five mouse results reconstruct within 9.71e-17. Independent scalar and synthetic-enumeration rarefaction checks agree within 1.11e-16. This is an exposed descriptive extension, not scientific acceptance or independent replication.

**The main naive-associated versus effector-associated age comparison remains unestimated.** None of its four predeclared age contrasts meets the support rule. Four mixed/indeterminate contrasts qualify, but cannot establish that state redistribution explains the prior broad CD8 result. Sparse state support, RNA dropout and source representation remain live alternatives. No fixed-composition attribution was attempted.

The 354 official post-QC FACS spleen CD8 RNA cells come from 13 mice (6/3/4 at 3/18/24 months). Only the original 288 repertoire-table rows enter clone analysis, from 11 mice (4/3/4). Every row joins by the previously qualified exact official_lookup; no formerly unassigned source row or RNA-only cell was assigned a clone. The two additional young RNA-only mice remain in the denominator. With no assembly-attempt denominator, the measured proportion is **prior repertoire-table representation**, not verified productive assembly success or a recovery rate.

Raw FACS counts are reads, not UMIs. The analyst-defined rule uses Tcf7/Lef1/Ccr7/Il7r as naive-associated and Nkg7/Ccl5/Gzmk/Gzmb/Prf1 as effector-associated markers: at least two from one panel and zero from the other gives the corresponding label; at least two from each gives mixed; all remaining patterns are indeterminate. Labels were fixed without age or clone outcomes and no new depth filter was applied. They are not validated naive/memory identities; Il7r/Ccr7 can occur in memory contexts. [Primary-source roles](../../../docs/research_reviews/2026-11-03-full-priority-screening/A27_TARGET_SOURCE_REVIEW.md) and [exact specification](../../../docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A27_STATE_RECOVERY_SPEC_V1.md) retain that distinction.

All observed RNA and represented source counts are shown below. These pooled counts describe the deposited cells; the age contrasts below use equally weighted eligible mice, not cell-level replicates.

| Age (months) | Operational state | RNA cells | Represented source rows | Blank-label singleton convention |
|---:|---|---:|---:|---:|
| 3 | effector_associated | 3 | 1 | 1 |
| 3 | indeterminate | 78 | 57 | 56 |
| 3 | mixed | 64 | 44 | 42 |
| 3 | naive_associated | 8 | 3 | 3 |
| 18 | effector_associated | 7 | 6 | 1 |
| 18 | indeterminate | 23 | 21 | 17 |
| 18 | mixed | 55 | 48 | 33 |
| 18 | naive_associated | 0 | 0 | 0 |
| 24 | effector_associated | 32 | 28 | 18 |
| 24 | indeterminate | 35 | 33 | 27 |
| 24 | mixed | 48 | 46 | 38 |
| 24 | naive_associated | 1 | 1 | 1 |

**237 of 288 represented rows have a blank source clonal_group.** They retain the historical singleton:cell_name convention solely to reproduce the source analysis. This is conditional on deposited labels and is not proof of 237 sequence-unique biological clones. RNA-only cells never receive this convention. Clone keys remain nested within mouse/age, and [cross-state clone occupancy](../../../analysis/research/runs/A27_state_representation_v1_20261103/clone_state_occupancy.tsv) preserves keys spanning operational states.

All 52 mouse/state combinations are retained, including zeros and unsupported states. Seventeen have at least five represented cells. The exact expected fraction belonging to repeated source keys at sampling depth five is calculated only in those combinations. Each planned age contrast requires at least two qualified mice in both age groups; no depth, label or threshold was relaxed. The table retains all eight attempted contrasts.

| State | Age minus 3 months | Qualified mice: young / older | Depth-five difference (percentage points) |
|---|---:|---:|---:|
| naive_associated | 18 | 0 / 0 | unestimated |
| naive_associated | 24 | 0 / 0 | unestimated |
| effector_associated | 18 | 0 / 0 | unestimated |
| effector_associated | 24 | 0 / 1 | unestimated |
| mixed | 18 | 3 / 2 | +5.8571 |
| mixed | 24 | 3 / 2 | +0.0000 |
| indeterminate | 18 | 4 / 2 | +0.0000 |
| indeterminate | 24 | 4 / 3 | +1.7094 |

These estimates are conditional on the restricted mouse rosters in [the complete age-contrast table](../../../analysis/research/runs/A27_state_representation_v1_20261103/state_age_contrasts.tsv). Zero differences do not establish equivalence. The supported strata are mixed and indeterminate; they do not become clean naive/effector populations after inspection. Pooled depth-five and within-state depth-five samples represent different populations, so smaller conditional differences or shifted state fractions cannot quantify redistribution. Age/sex imbalance, dropout, source selection and clone-label uncertainty remain. No absolute clone expansion, immune function, causal mediation, p-value or cell-level confidence interval is inferred.

[All cell/read/state primitives](../../../analysis/research/runs/A27_state_representation_v1_20261103/cell_state_primitives.tsv), [mouse/state denominators](../../../analysis/research/runs/A27_state_representation_v1_20261103/mouse_state_representation.tsv), [supported and held repetition rows](../../../analysis/research/runs/A27_state_representation_v1_20261103/mouse_state_repetition.tsv) and [old broad parity](../../../analysis/research/runs/A27_state_representation_v1_20261103/original_broad_parity.tsv) make the full result reviewable. The next biological discriminator requires adequately supported, independently qualified state and receptor measurements with known source representation/assembly-attempt semantics; this screen does not invent those missing observations. Independent coordinator numerical and biological report review passed 6,325 state, exact source-identity, representation, inherited-singleton, clone-occupancy, repetition, roster and contrast checks (maximum error 1.11e-16). All four main naive/effector holds and the redistribution-attribution limit are retained; integration clearance does not promote a scientific claim.
