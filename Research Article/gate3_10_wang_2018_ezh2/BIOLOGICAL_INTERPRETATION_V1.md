# Biological implications and links to existing questions

12 November 2026. Owner: **Wang18-P01**. Interpretation of the completed
S1–S5 and F1–F3 work, reviewed against `5f8caee` and refreshed main `30a4a7b`.
This note uses existing results; it performs no new numerical analysis and
does not change a canonical hypothesis, question status or claim grade.

## What was already established

Wang et al. (2018) already reported the cultured Il10/Tgfb1 decrease, Il2
increase and inflammatory enrichment in S3B–C. Figures 5–7 supply separate
tumor lineage, intracellular cytokine and functional comparisons, including
the benefit of residual deficient Tregs relative to the tested depletion
comparator. Those experiments are published evidence, not newly measured
repository outcomes. The short-course frequency result is not equivalence in
absolute numbers or survival. [Primary article](https://doi.org/10.1016/j.celrep.2018.05.050)
and [supplement, p. 5](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf).

DuPage et al. (2015), Figure 7 and the main-text account of S7, already connect
activation with later maintenance/identity difficulties, despite similar early
division in the tested antigen-specific setting. Peeters et al. (2024), Figures
4–7, supplies gain-of-function effector-Treg and suppressive-function context.
These observations make timing, starting population and perturbation relevant
before the present reanalysis. [DuPage](https://doi.org/10.1016/j.immuni.2015.01.007)
· [Peeters](https://doi.org/10.1016/j.celrep.2024.114724)
· [Existing source interpretation](../gate3_09_dupage_2015/SOURCE_REVIEW.md).

Sarmento et al. (2017; online 2016), Figure 3B–D, already measured suppression
and stimulated-culture cytokine supernatants in another Ezh2-deficient Treg
setting. The general possibility of an altered inflammatory output is therefore
an existing premise. The qualified day-four comparison still lacks linked
recovery, state and output measurements. [Primary record](https://pubmed.ncbi.nlm.nih.gov/27909059/)
· [Reading limits and exact context](F3_LITERATURE_ADDENDUM_20261112.md).

## What the repository added

The observed unit is a deposited library, not a verified independent mouse.
The comparison is relative RNA after 96 hours of culture in four deficient
libraries versus five deposited controls, with a four-library +/+-labelled
control sensitivity. The genotype labels conflict with S3C and biological-unit
and block identities remain unresolved. The labels are shared submission
metadata rather than independent allele verification. [F1 audit](F1_SOURCE_AUDIT_20261112.md).

1. **A qualified robustness result.** Lower Il10/Tgfb1 and the positive
   inflammatory set patterns survive the specified control and library
   checks. F2 also preserves the inflammatory, cell-cycle and apoptosis
   set-score directions under Signal2Noise. This adds reproducibility and
   sensitivity information to the published RNA result. It is reanalysis
   of the same source, not independent biological replication.
2. **A restricted biological interpretation.** Foxp3 RNA is higher in the
   cultured deficient libraries while Il10 and Tgfb1 are lower. This makes
   a single scalar account of lost Treg identity inadequate for these
   measurements. Bulk RNA does not show that all these changes coexist in
   the same cell, establish protein function, or contradict tumor lineage
   tracing in a different setting.
3. **A specific unresolved alternative.** Positive apoptosis and negative
   E2F/G2M RNA ranks accompany the inflammatory pattern. They motivate
   measuring recovery and composition alongside within-observed-state RNA;
   they do not demonstrate increased cell death or decreased division.
   Genotype-associated processing remains another unresolved explanation.
4. **A limit to broad pathway claims.** Glycolysis, heme metabolism and
   WNT/β-catenin set scores reverse sign when ranking changes. The result
   supports particular stable themes, not a ranking-invariant metabolic or
   signaling programme. Enrichment scores do not establish pathway activity.

Exact numerical evidence is in [S1–S4 results](RESULTS_V1.md), the
[all-gene sensitivity table](../../analysis/research/runs/wang18_s3_breadth_v1/gene_sensitivity.tsv)
and [F2 results](F2_RESULTS_V1.md). No effect in patients, mediator necessity,
direct EZH2 target or recipient repair effect was estimated here.

## What changes for A33–A35

The direct RQ links use the exposed, fixed five-gene S4 panel. Wang count
ratios, DuPage log-FPKM differences and Peeters rlog differences retain
different scales and contexts. Agreement of signs is not a common causal
effect estimate; sample independence and overlap are not resolved by paper
titles. [Exact S4 table](../../analysis/research/runs/wang18_s4_context_v1/context_directions.tsv)
· [Prospective context amendment](CONTEXT_AMENDMENT_V1.md).

| Existing question | Published premise or earlier repository evidence | What Wang adds | Remaining discriminating comparison |
|---|---|---|---|
| [A33: TIGIT-evoked AREG output](../../docs/research_dossiers/A33.md) | Panetti et al. (2025), Figures 5–6 and Extended Data 8, establishes the activation-dependent TIGIT/Blimp-1/AREG premise. The earlier DuPage/Peeters reanalysis already found context dependence. | Tigit and Prdm1 are lower, but Areg is higher in Wang loss. This further limits using receptor/regulator RNA to predict AREG output. It neither confirms nor falsifies the RQ's evoked-output hypothesis. | Measure the genotype difference in TIGIT-engagement-minus-control AREG release in a responsive common context, retaining baseline output and viable recovery. The published receptor mechanism is a premise, not a new discovery. |
| [A34: CCR2 movement and fitness](../../docs/research_dossiers/A34.md) | DuPage loss has lower Ccr2; Peeters gain changes sign with culture. Zhan et al. reports a context-dependent CCR2/CD25 relationship; Chorro et al. identifies an Il2ra/background alternative in a particular colony. | Wang's Ccr2 point estimate is positive, with an omission range crossing zero. Thus a universal Ezh2-loss-to-Ccr2-decrease account is unsupported across these comparisons. Migration and fitness remain unmeasured. | Verify CCR2 protein in the actual model; measure directed movement separately from signaling/recovery. Establish target contribution with an appropriate restricted comparison if a phenotype is found. |
| [A35: Treg-derived IGFBP4 and native-IGF response](../../docs/research_dossiers/A35.md) | The previous DuPage/Peeters contrast already showed reciprocal loss/gain RNA directions. Published IGFBP4/IGF effects include other source and differentiation contexts. | Wang adds a cultured-loss context with higher Igfbp4, consistent with the earlier direction. This supports continuing source/protein qualification, not direct EZH2 regulation, secretion, harmful IGF inhibition or benefit from blockade. | Establish intact Treg-derived extracellular IGFBP4; conditionally test its contribution to native-IGF receptor response with matched medium, IL-2, recovery and source controls. |

Primary premises are kept separate from the S4 evidence:
[Panetti](https://doi.org/10.1038/s41590-025-02300-w),
[Zhan](https://doi.org/10.1038/s41423-018-0187-8),
[Chorro, Figure 1](https://doi.org/10.1038/s41467-018-07806-6), and
[Miyagawa, abstract-level source precedent](https://pubmed.ncbi.nlm.nih.gov/28724578/).
Their fuller locators and limits remain in each RQ's literature context.
The A34 colony alternative does not establish that Zhan's colony was affected.

F3 complements all three questions by specifying how to link viable recovery,
lineage ancestry and observed-state RNA. It does not execute their AREG,
movement or IGF-response experiments, and it is not a mandatory prerequisite
for every otherwise qualified RQ experiment. Its own Il10 comparison stays
with Wang18-P01. A2/A9 share AREG source/recipient concerns, but epithelial
delivery and fibroblast competence receive no direct measurement here. A
shared cytokine or gene alone does not connect this result to the remaining
portfolio. No RQ was ranked, retired, merged or promoted.

## Completion means the recorded scope

S1 qualified the source while retaining unknowns; S2–S3 executed adapted
descriptive RNA analyses; S4 completed the mouse panel and closed the
uninformative human-association branch; S5 integrated published function.
F1 completed additional source recovery, F2 executed the ranking sensitivity,
and F3 completed and reviewed a measurement/analysis specification.

Exact replay, population inference and numerical functional reconstruction
remain input-dependent. F3 did not collect new measurements. Thus all stages
have completed dispositions and reviewed deliverables, while the biological
mechanisms and A33–A35 functional predictions remain unresolved.
[Stage/checkpoint record](FOLLOWUP_STATUS_20261112.md)
· [F3 specification](F3_MEASUREMENT_PLAN_V1.md).

## Attribution check

This explanatory pass reused the current source and RQ reviews rather than
opening a new question or claiming a new novelty search. On 12 November 2026,
targeted web queries checked the Panetti and Zhan DOIs, Wang's Figure 7,
Miyagawa PMID 28724578, DiToro DOI 10.1016/j.immuni.2020.03.013 and Peeters
Figure 5. Direct Nature routes for Panetti/Zhan and PMC for Wang challenged
or redirected; indexed primary results, Panetti's publisher PDF, Wang's
PubMed figure legends and Chorro's primary Results were available. The
Miyagawa check remains abstract/record-level, and the Peeters search returned
irrelevant hits as well as the correct source; the existing qualified paper
reading governs its interpretation. No new full supplementary audit or
numerical result is claimed. Scientific acceptance remains unassessed.
