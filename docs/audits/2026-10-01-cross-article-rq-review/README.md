# Cross-article review of analysis history and RQ contributions

**1 October 2026.** At the owner's request, three subagents reviewed separate
article groups and the primary agent reviewed Nb3, checked proposed transfers
against current RQ scope and integrated accepted conditional branches. Dates
come from reports/run records and later corrections, not file modification
times. Within-day order is stated only where dependencies establish it.

The review covers **12 folders**: 11 present at the start, plus Nb2 on remote
main. `origin/main` was checked at `f61343cc16c83e979b071393adccdcf8084ea294`;
local HEAD remains `33b27cf`. Remote-only evidence uses commit-pinned links.
This is a targeted documentation integration, not a merge of the whole dirty
checkout with main. A19–A21 belong to Nb2; Nb3 is corrected to A22/A23.

## Complete folder coverage

| Folder / study | Chronological review | Contribution after strict review |
|---|---|---|
| Niethamer 2025 | [Review](../../../Research%20Article/gate1_01_niethamer_2025/RQ_RETROSPECTIVE_REVIEW.md) | A3/A6 already incorporate phase, composition and replication corrections; no duplicate hypothesis |
| Choi 2020 | [Review](../../../Research%20Article/gate1_02_choi_2020/RQ_RETROSPECTIVE_REVIEW.md) | Later regulatory/lineage limits already constrain A1/A4/A5/A8/A14; no new causal mechanism |
| Nabhan 2018 / Nb1 | [Review](../../../Research%20Article/gate1_03_nabhan_2018/RQ_RETROSPECTIVE_REVIEW.md) | Add a conditional source-context modifier under A4; ligand expression does not establish a switch or A20 receptor necessity |
| Sikkema / HLCA | [Review](../../../Research%20Article/gate1_04_sikkema_2023_hlca/RQ_RETROSPECTIVE_REVIEW.md) | Later S2 narrows earlier AT0 calls; add an A1 population-definition constraint |
| Cardoso 2026 | [Review](../../../Research%20Article/gate2_05_cardoso_2026/RQ_RETROSPECTIVE_REVIEW.md) | Specify A2 source-state decomposition; reject tumour-specific second-signal, new-lineage and RNA-inferred shedding promotions |
| England 2025 | [Review](../../../Research%20Article/gate2_C2_england_2025/RQ_RETROSPECTIVE_REVIEW.md) | Add conditional A2 coordinated-output, A8 incomplete-maturation, A14 feedback and A18 interaction branches; retain later A16/A17 corrections |
| Yu / Lee / Choi 2026 | [Review](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/RQ_RETROSPECTIVE_REVIEW.md) | A11 specificity and A12 validation limits remain; A13's tested programme worsens prediction. No new positive mechanism |
| Nabhan 2023 / Nb2, originally remote-only | [Review](../../../Research%20Article/gate2_N1_nabhan_2023/RQ_RETROSPECTIVE_REVIEW.md) | A19–A21 already contain September 30 refinements; do not replace them with older summaries. Only the review file was added locally |
| Nabhan 2026 / Nb3 | [Review](../../../Research%20Article/gate2_N2_nabhan_2026/reports/RQ_INTEGRATION_REVIEW.md) | Conditional A1/A8 candidates, A9 recipient boundary, A13 reverse-direction rival, A22 spatial/specificity branches and A23 homeostasis question; E5 separately specified |
| Epithelial state specificity | [Review](../../../Research%20Article/epithelial_state_specificity/RQ_RETROSPECTIVE_REVIEW.md) | Existing A5/A7/A8 already own surviving contributions; overlap diagnostics do not establish fate |
| Murthy 2022 | [Review](../../../Research%20Article/ungated_murthy_2022/RQ_RETROSPECTIVE_REVIEW.md) | Annotation/reference limitations; no separate biological hypothesis |
| Primary source archive | [Review](../../../Research%20Article/Primary/RQ_RETROSPECTIVE_REVIEW.md) | No independent run; do not double-count source copies as evidence |

## Integration decisions

Accepted branches are added under the specific [canonical RQs](../../../RESEARCH_QUESTIONS.md)
and linked from question workspaces where present. A branch must add a distinct
biological prediction or a consequential interpretation constraint. It must
name its evidence, rival and missing discriminator. “Conditional candidate”
does not change claim grades or mark an experiment complete.

| RQ | Integrated contribution |
|---|---|
| A1 | Nb3 IFN/hypoxia response differences nominate a regulatory/functional comparison; HLCA supplies independent population-definition constraints. Neither is a demonstrated fate branch |
| A2 | One upstream source-state branch combines Cardoso's mixture/expression decomposition and England's coordinated-output screen. They remain separate observations, not independent confirmation of delivery |
| A4 | Nb1 source context may modify sequential responsiveness. Nb3 ELOVL1/ATP6V0E do not establish Wnt independence or a Wnt-to-IL-1 sequence |
| A8 | Nb3 E2/E3 and England E-N5 nominate different maturation-competence comparisons; require independent mature output and preserve missing-linkage status |
| A9 | Keep epithelial EGFR requirement distinct from fibroblast response, and EGF distinct from AREG |
| A13 | Add epithelial-to-fibroblast induction/selection as a reverse-direction rival. Preserve the later negative pilot rather than promote feedback |
| A14 | Separate deficient endogenous feedback from persistent input overwhelming intact feedback |
| A18 | Make the SPP1/DLK1 interaction candidate explicit; saturation, survival and geometry remain alternatives |
| A22 | Keep local state induction versus selection, lung specificity and immune/clinical links as distinct unresolved branches |
| A23 | Retain transition/homeostasis hypothesis; no broader identity-loss absence or phosphate-mediation claim |

The review also reconciles stale A1/A13/A16/A17 status text with their completed
main-branch corrections where it would otherwise contradict the new additions.
Unchanged cards receive no duplicate hypothesis. The original analysis files,
historical responsibility rows and claim register are preserved.

## E5 external work

The [public-data feasibility report](../../../Research%20Article/gate2_N2_nabhan_2026/reports/E5_EXTERNAL_FEASIBILITY.md)
records dataset screening and a new descriptive GSE306184 pilot: 14 libraries,
four knockdown/context contrasts and two normalizations. It refines E5 to
epithelial receptor/context dependence while retaining normal-renewal, cancer
dependency and clinical-injury claims separately. It is the only new numerical
analysis in this retrospective-review batch. No new global RQ ID is assigned.

Verification of edits and the E5 calculation is recorded in
[verification.json](verification.json). Original Nb3 runs and the 11-page atlas
are preserved; the external figure is separately versioned.
