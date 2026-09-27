# P4 — Source identity, recipient eligibility and signalling design

**Status: available source accounting and design audit completed; identity and mechanism gates remain closed.** The new calculation quantifies attribution ambiguity without inventing labels for the unassigned cells.

## IL1B accounting sensitivity

For each patient–histology unit, let M be the fraction of observed IL1B counts assigned to macrophages and U the unassigned fraction. Under the explicit assumptions that assigned labels and observed-cell counts are correct, the macrophage fraction can range from M to M+U. These are accounting bounds, not confidence intervals. Ambient RNA, incorrect assigned labels or secretion would require other evidence.

The [calculation specification](P4_attribution_spec.json), [every unit](P4_source_attribution_bounds.tsv), [summary](P4_source_attribution_summary.tsv) and [identity/coverage audit](P4_identity_coverage_audit.json) retain inputs and assumptions. No RNA was relabelled.

| Histology | Patient–histology units | Median unassigned fraction | Median lower–upper bounds | Units whose macrophage majority depends on unknown assignment |
|---|---:|---:|---:|---:|
| AAH | 8 | 51.7% | 36.3%–92.5% | 5 |
| AIS | 12 | 68.3% | 17.1%–89.2% | 11 |
| LUAD | 23 | 72.1% | 17.2%–89.2% | 23 |
| MIA | 4 | 66.1% | 19.6%–85.8% | 3 |
| normal | 23 | 63.5% | 18.9%–89.0% | 20 |

Across 70 patient–histology units from 23 patients, 62 majority classifications depend on how the unknown counts are attributed. Repeated histologies from one patient are not independent donors. Marginal median bounds describe the bounds across units; they are not an interval for a common biological effect.

The existing annotation retains 55.6% of QC cells under the primary confidence rule and 65.2% under its sensitivity rule. A change in retained cell count does not establish where IL1B counts move. Assigned-class marker support cannot identify the unassigned cells, and RNA source attribution does not establish mature secreted IL-1β. A12-S1 remains unresolved.

## Recipient and route gates

| Branch | What is available | Remaining required evidence / decision |
|---|---|---|
| A12 source plus recipient information | RNA compatibility and aggregate compartment data | Freeze comparable donor units and disjoint predictors/endpoints before a nested held-out comparison. Attribution assumptions must accompany any nominated-source model. |
| A13 joint fibroblast model | Existing exact-definition coverage and its refusal record | Reaggregation preserves the existing below-floor cases. No new eligible cohort is introduced; no joint fit is launched. Largest labels across donors are not automatically the same state. |
| A2/A9 ligand supply and reception | The screen and newly recovered EGF culture context | Quantified source/medium/recipient ligand, receptor-specific engagement and controlled presentation are missing. |
| A15 latent-ligand activation | ITGB6-associated screen change and separate downstream-antibody evidence | Independent preparations, active-versus-total ligand and selective source/recipient perturbations are missing; the parent is not tested. |

The focused route design should first compare ligand and integrin arms under the same recipient and medium conditions, with measured engagement and viability. Add active-ligand bypass and receptor controls only where the response retains dynamic range. Recipient blockade alone can create a floor; rescue can bypass several defects. Both routes may contribute. Do not infer mediation from a downstream change plus an epithelial null.

## Decision

The attribution audit produces a useful bound but does not close source identity. A per-cell independent annotation/ambient/doublet adjudication is needed before elevating a nominated IL1B source. Existing conditional RNA results remain conditional on recovered and assigned compartments. The next experimental priority is one selective, independently replicated route or withdrawal design, rather than another correlation panel. P5 develops the withdrawal design separately.

## Recorded confidence sensitivity and A12 readiness

The existing 0.3 confidence cutoff was also evaluated as a declared sensitivity, preserving the 0.2 primary. This measures how the classifier reallocates observed counts; it does not independently verify cell identity.

| Histology | Median unassigned IL1B, primary 0.2 | Median unassigned IL1B, sensitivity 0.3 |
|---|---:|---:|
| AAH | 51.7% | 41.4% |
| AIS | 68.3% | 45.0% |
| LUAD | 72.1% | 60.7% |
| MIA | 66.1% | 51.1% |
| normal | 63.5% | 46.9% |

The majority classification remains assignment-sensitive in 55/70 units at the sensitivity cutoff, versus 62/70 under the primary. Neither cutoff resolves the unknown-cell identity problem.

The component-table audit finds 23 normal/LUAD patient pairs for AT2-like, 23 normal/LUAD patient pairs for Fibroblasts with source and recipient-component records. These records include measured zeros and do not establish cell-floor support or comparable states. The table contains receptor/source components, not an independently frozen recipient-response endpoint. A12 remains a possible conditional descriptive extension; it is not rejected merely because unassigned cells exist. No model is fit until the independent response, state definition, precision and held-out comparison are specified and checked. [Readiness and sensitivity record](P4_confidence_and_model_readiness.json).
