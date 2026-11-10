# Paper interpretation and repository fit

10 November 2026. Reading synthesis, not a new biological result.
Primary source: [Zhang et al., Science Immunology 11, eadx4411](https://doi.org/10.1126/sciimmunol.adx4411),
published 10 April 2026. The supplied 15-page PDF was inspected, including
rendered Figures 4–7. Exact source identity and access limits are in
[SOURCE_REVIEW.md](SOURCE_REVIEW.md).

## What the paper establishes in its tested models

The study asks why MHC-I-deficient tumors can progress despite NK recognition
potential. Local Treg removal is associated with NK-dependent control in the
tested mouse tumors. The authors combine cell-dependence experiments, sorted
bulk RNA, protein/signaling measurements and functional endpoints. These are
complementary measurements, not interchangeable validation of every arrow.

| Evidence locator | Measured endpoint and unit | Inference and boundary |
|---|---|---|
| Figures 1–2 | Tumor trajectories, local/systemic immune changes and cell-dependence comparisons in mice | Supports local tumor control with NK and conventional CD4 requirements in the tested models. Does not establish a universally safe human intervention. |
| Figure 3; RNA methods pp.12–13 | Bulk RNA from sorted tumor NK preparations; three experimental replicates, each treatment preparation pools tumors | Describes transcript differences and dependence on the CD4-containing setting. Pool constituents and technical measurements are not independent RNA replicates. |
| Figure 4B–F | BrdU, CD69, SCA-1, KLRG1 and CD11b/CD27 phenotypes; animal-level summaries at the indicated times | Distinguish recent DNA synthesis, marker expression and maturation-associated phenotypes. KLRG1 alone does not prove senescence/exhaustion; SCA-1 alone does not prove stemness. |
| Figure 5B–D | Granzyme/perforin staining, target-cell lysis from pooled NK preparations, and tumor growth with perforin dependence | Direct functional evidence is separate from the RNA results. Assay wells, targets and pooled animals must retain distinct denominators. |
| Figure 5E–G, p.5 Results | IFN-gamma and CD107a after the stated stimulation | Higher IFN-gamma and killing coexist with no increased CD107a in this assay. Greater granule cargo is the authors' explanation, not a measurement of release rate. |
| Figure 6B,D,F; H–M | Tumor growth in different DC contexts; NK CD25/pSTAT5; CD4 IL-2 staining | Supports cDC2 involvement and local IL-2-associated signaling. Enrichment in 6G alone would not establish that mechanism. |
| Figure 7B,J; G–H; K–N | Tumor control under IL-2 dependence/rescue, other cytokine comparisons and antibody-based/model extensions | Supports a major IL-2 contribution within these contexts. Rescue does not quantify the relative contributions of IL-2 production versus sequestration or exclude every other regulatory route. |

**Figure-label discrepancy:** the displayed Figure 5 axes and main Results
identify F as IFN-gamma and G as CD107a. The caption reverses F/G.
Figure 6J's legend calls CD4 Tconv FOXP3-positive; conventional CD4 identity
must be checked against the actual gating/supplement before reusing that label.
Neither discrepancy licenses relabeling raw data by assumption.

## Implications and unresolved biology

The organizing insight is multicellular local regulation: Tregs can constrain
NK antitumor responses through conventional CD4 help and a DC-dependent setting.
The cDC2–CD4–IL-2 circuit is a published result, not a new Ravel hypothesis.

The paper leaves room for direct Treg effects, other cytokine inputs and NK–DC
interactions. Removing a cell population and altering its regulatory identity
are distinct interventions. Bulk NK RNA can also change through shifts in the
recovered NK-state mixture, survival or sorting composition. It cannot establish
a per-cell transition or identify the mediator of tumor control.

Local pSTAT5 supports a localized signaling response. Independence from
recruitment out of secondary lymphoid organs rests on the paper's separate
trafficking experiment, not pSTAT5 alone. Mouse toxicity observations and
antibody activity do not establish clinical safety or general human efficacy.

## Fit with Ravel and neighboring papers

Ravel's current mission is paper-driven biological research across tissues,
organisms and molecular layers, with explicit evidence and inference limits.
It is not restricted to scRNA-seq or a single lung hypothesis; sorted bulk RNA
is an appropriate paper-specific input here.

| Neighbor and current repository authority | Useful comparison | Boundary |
|---|---|---|
| [DuPage 2015 current results](../gate3_09_dupage_2015/RESULTS.md), [candidate follow-up](../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md), [annotation amendment](../gate3_09_dupage_2015/TARGET_SCREEN_AMENDMENT_V2.md) | Activated Treg identity/selection versus local Treg removal; existing loss/gain RNA directions depend on context | DuPage KO comparator is HET, and selected CD62L states are not experimental timepoints. Peeters reuse is not independent confirmation. Do not pool with Zhang NK RNA. |
| [Wang 2018](https://doi.org/10.1016/j.celrep.2018.05.050), primary abstract/indexed Results | Tumor Treg reprogramming versus depletion; immune effector context differs | Related precedent, not proof that EZH2 perturbation reproduces Zhang's NK circuit. Complete supplemental audit was not performed. |
| [Peeters 2024 and DuPage literature record](../gate3_09_dupage_2015/LITERATURE_CONTEXT.md) | Gain/loss and activation context complicate monotonic identity models | Its published reciprocal comparison already exists. No new broad inverse-EZH2 claim is proposed. |
| [Saxton IL-22 reassessment](../gate3_08_saxton_2021_il22/reassessment_v1/RESULTS.md), [recipient context](../gate3_08_saxton_2021_il22/recipient_context_v1/RESULTS.md) | Separate cytokine-associated RNA from recipient competence and tissue function | Its program separation does not establish signaling selectivity; pooled Choi cells are not independent animals. |
| [Saxton IL-10 extensions](../gate3_07_saxton_2021_il10/extensions_20261108/RESULTS.md) | RNA direction can depend on source and context; preserve mixed findings | The unestimated IL-10-variant × IL-18 interaction is not resolved by Zhang. |
| [Yadav current extension synthesis](../gate2_W3_yadav_2025/extensions_20261031/FINAL_SYNTHESIS.md) | Trace cell interaction claims to the exact functional assay and unit | Shared-source reconstruction is not replication; no mature repair conclusion transfers to this tumor setting. |

[A33–A35](../gate3_09_dupage_2015/rq_derivation/README.md) own Treg output,
movement/fitness and IGFBP4 source/response questions. Zh26-P01 owns source
reproducibility of NK RNA. No canonical question is merged, retired or promoted.

**Current execution interpretation:** the [released RNA replay](RESULTS.md)
reproduces the Figure 3 source tables and narrows measurement uncertainty.
Fixed-panel directions survive block omission, while enrichment P values and
the IFN-gamma threshold-based description depend on computational/ranking
choices. These observations are already tied to Zhang's reported transcript
patterns, not a new circuit. Count-model reconciliation and numerical functional
reconstruction require the exact inputs listed in the result report. Neither
outcome adjudicates the whole functional mechanism or identifies a new target.
