# Retrospective RQ review: Murthy 2022 / GSE178360

Reviewed 2026-10-01 against saved reports and the RQ register on `origin/main`
at `f61343cc16c83e979b071393adccdcf8084ea294`. This folder contains a healthy
human data reanalysis, not an owner-completed roadmap study note. The review
does not infer that the source paper has now been read by the owner.

## Analysis sequence and its consequences

| Date / order | Saved evidence | Consequence for framing |
|---|---|---|
| August 2026, Stage 0 atlas | [Generated atlas report](GSE178360/README.md), [deposited format](GSE178360/inventory/detected_format.json), [QC and donor checks](GSE178360/qc/) | Three healthy donors yield 27,729 retained cells. Ensembl-ID intersection addresses different reference feature lists. Blind marker labels and epithelial subclusters are descriptions; no injury, treatment, time or functional outcome contrast exists. The phase date follows the repository's Stage 0 record, not file modification times. |
| 2026-09-09, S1 and S3 annotation checks | [HLCA trial sequence](../gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md), [S3 report](../gate1_04_sikkema_2023_hlca/trials/s3_hlca_marker_annotation/s3_summary.md), [donor-level AT0 comparison](../gate1_04_sikkema_2023_hlca/trials/s3_hlca_marker_annotation/s3_at0_check_per_donor.csv) | Flat and hierarchical marker transfer disagree strongly about AT0. Shared secretory/alveolar markers cannot establish a distinct transitional population; donor-private clusters require caution. |
| 2026-09-09, S2 run after other HLCA trials | [Reference-mapping report](../gate1_04_sikkema_2023_hlca/trials/s2_reference_mapping/s2_summary.md), [AT0 donor table](../gate1_04_sikkema_2023_hlca/trials/s2_reference_mapping/s2_at0_check_per_donor.csv), [uncertainty table](../gate1_04_sikkema_2023_hlca/trials/s2_reference_mapping/s2_uncertainty_per_donor.csv) | Only 119 cells meet the confident AT0 transfer rule across donors; the earlier 328-cell candidate subcluster is largely AT2 or uncertain. Agreement with the HLCA authors' own transfer uses the same cells and is not independent biological validation. |

## Strict contribution decisions

| Existing RQ | Possible contribution | Decision, rival and discriminator |
|---|---|---|
| **A1, regulatory differences between transitional states** | Healthy AT0-like cells might provide a comparison for injury-associated transitional states. | **Reference context only; no new biological branch.** RNA labels are uncertain and this cohort supplies neither chromatin nor a functional response. Healthy regional identity and annotation ambiguity compete with an injury-transition interpretation. Independent source-defined states and regulatory/function measurements would be needed. |
| **A5, development versus adult repair** | Shared epithelial markers might imply reuse of a developmental programme. | **Reject this inference from this cohort.** Healthy adult donors are neither a developmental series nor an injury contrast. The collection can serve as healthy adult context only. |
| **A8, maturation-specific information** | A healthy AT0-like state might connect shared transition to mature AT1 differentiation. | **Not established.** The atlas is cross-sectional and has no traced fate or mature-output endpoint. Requiring independently measured fate/function already belongs to A8; marker transfer adds no distinct hypothesis. |

No canonical hypothesis addition is warranted. The later mapping usefully
**narrows which labels may be used as context** and prevents a healthy
marker-positive compartment from being presented as evidence of injury repair
or a measured intermediate fate. No local analysis in this folder is an
independent replication of the HLCA's transfer of GSE178360.
