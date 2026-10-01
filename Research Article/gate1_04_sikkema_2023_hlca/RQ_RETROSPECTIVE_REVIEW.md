# HLCA: retrospective review of contributions to research questions

Reviewed 1 October 2026 against the completed article trials and the canonical
RQ cards on `origin/main` at `f61343cc16c83e979b071393adccdcf8084ea294`.
This is a documentation review: no new numerical fit, annotation replacement,
claim-grade change or biological acceptance is recorded.

## Analysis sequence and what changed

The [trial plan](ANALYSIS_TRIAL_PLAN.md) dates all five trials to 9 September
2026 and explicitly records that S2 ran last. Trial numbers are therefore not
execution order. The available records establish S1 and S3–S5 before S2;
they do not establish a finer within-day order for S3–S5.

| Stage | Observation in the saved evidence | Consequence for later framing |
|---|---|---|
| S1, entropy audit | Mouse clusters 5, 7, 10 and 22 have high deposited-label entropy; cluster 23 is donor-private within a relevant stratum. Unstratified donor entropy does not recover that flag | Heterogeneous or animal-private groups require review before a biological state comparison. Entropy is a diagnostic, not a lineage or fate measurement |
| S3, source-marker annotation | Flat and hierarchical assignments give markedly different AT0 counts. The 328-cell candidate subcluster has 280 flat AT0 assignments and zero hierarchical AT0 assignments | A marker-derived AT0 label is definition-sensitive. Agreement between methods sharing markers is not independent biological confirmation |
| S4, cluster-23 QC | Median counts are 1,867.5 versus 6,790 in other cells; broad cross-lineage detection and sample concentration satisfy the frozen low-count, ambient-like rules | Do not nominate a mixed-lineage repair state from this cluster. Ambient-like is the diagnostic conclusion; the amount or physical source of ambient RNA was not measured |
| S5, cluster-5 refinement | The primary resolution puts 59.6% of labelled cells into sufficiently pure subclusters; the higher-resolution sensitivity reaches 94.3%. The IFN-rich monocyte-like group is 75% from one animal | Preserve the failed primary and favorable sensitivity. A private IFN-rich population is not replicated evidence for an injury programme or an immune mediator |
| S2, reference mapping, run last | Confident AT0 calls total 119 across three donors. The candidate subcluster contains 75 AT0, 126 AT2 and 117 unknown cells. Transfer agrees closely with the HLCA authors' mapping of the same cells | This narrows the original AT0 interpretation to a minority and a mixed candidate group. Same-cell mapping agreement checks implementation, not independent replication of cell fate |

Evidence: [S1](trials/s1_entropy_criteria.md),
[S3](trials/s3_hlca_marker_annotation/s3_summary.md),
[S4](trials/s4_cluster23_qc/s4_summary.md),
[S5 primary](trials/s5_cluster5_subclusters/s5_summary.md),
[S5 resolution sensitivity](ANALYSIS_TRIAL_PLAN.md),
[S2](trials/s2_reference_mapping/s2_summary.md).

## Strict RQ disposition

| Related question | Contribution and review decision | Conditional biological claim and discriminator |
|---|---|---|
| [A1: regulatory distinction](../../RESEARCH_QUESTIONS.md#a1) | **Retain as a measurement constraint, not a new biological branch.** S3 followed by S2 shows why overlapping RNA or alternative labels cannot establish distinct regulatory states. The current A1 already separates source definitions, regulatory evidence and functional response | A regulatory distinction is meaningful only if it persists within independently supported epithelial populations and predicts a separately measured response. Reference coverage, cell mixture and technical quality remain rivals. HLCA supplies no linked regulatory-to-function test |
| [A3: injury versus aging](../../RESEARCH_QUESTIONS.md#a3) and [A6: within-state macrophage change](../../RESEARCH_QUESTIONS.md#a6) | **Retain subtype/animal eligibility cautions; reject a new IFN or profibrotic mechanism from S5.** Resolution-sensitive mixtures and one-animal enrichment cannot identify a phase or disease effect | Compare matched, adequately covered states across independent animals and appropriate age/condition groups. Failure to detect the SPP1-high panel in cluster 5 does not establish its absence from the whole lung |
| [A8: maturation information](../../RESEARCH_QUESTIONS.md#a8) | **Retain endpoint and identity constraints only.** An AT0/AT1 transfer label is neither measured mature AT1 contribution nor a predictor–outcome linkage | Use independently measured mature contribution with documented timing and biological units. Do not convert label-transfer confidence into an outcome |

No additional biological hypothesis survives as a distinct new branch in this
package. The later S2 result **narrows** the earlier AT0 interpretation rather
than expanding it. The paper's human core is not a validated mouse reference;
these findings do not authorize transferring its labels directly to mouse data.
This review does not reverse or silently edit historical annotations.

## Proposed register note

Under A1, a compact cross-reference is sufficient: **"Related measurement
constraint — HLCA S3-to-S2 review: alternative marker rules and reference mapping
give different AT0 assignments, so a regulatory-state comparison must first
establish its population independently of the tested outcome. This is not a
new fate hypothesis."** The other links above document scope boundaries;
duplicating them as new hypotheses would add no distinct biological prediction.
