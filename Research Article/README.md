# Research article roadmap

**Wagner, Gate 2W paper 15:** [Th17/Compass package](gate2_W1_wagner_th17_autoimmunity/README.md),
[reproduction scope](gate2_W1_wagner_th17_autoimmunity/REPRODUCTION_SCOPE.md) and
[six proposed branches](gate2_W1_wagner_th17_autoimmunity/BRANCH_REGISTER.md).
Owner reading completed 4 October 2026; source review and planning complete,
numerical reproduction unrun. Wg identifiers are separate from Niethamer W1.

**Nb5, Gate 2N N4:** [mouse ageing atlas](gate2_N4_nabhan_aging_atlas_2020/README.md) · [analysis plan](gate2_N4_nabhan_aging_atlas_2020/ANALYSIS_TRIAL_PLAN.md) · [handwritten-note reconciliation](gate2_N4_nabhan_aging_atlas_2020/NOTE_RECONCILIATION.md).
Owner reading completed 3 October 2026. [Eight article-local candidates](gate2_N4_nabhan_aging_atlas_2020/BRANCH_REGISTER.md) are
structured separately from source reproduction. [First analysis results](gate2_N4_nabhan_aging_atlas_2020/RESULTS.md)
and [six figure plates](gate2_N4_nabhan_aging_atlas_2020/FIGURES.md) are available; source discrepancies and branch-specific holds remain explicit.

**Nb4, Gate 2N N3:** [article package](gate2_N3_travaglini_nabhan_lung_atlas_2020/README.md) · [15-figure gallery](gate2_N3_travaglini_nabhan_lung_atlas_2020/FIGURES.md) · [execution and provenance](gate2_N3_travaglini_nabhan_lung_atlas_2020/EXECUTION.md).

**Cross-article review, 1 October 2026:** [chronological evidence and RQ contributions](../docs/audits/2026-10-01-cross-article-rq-review/README.md)
cover all 12 folders including the source archive and Nb2 on main. Accepted
conditional branches are integrated under their existing questions; later
corrections and rejected transfers remain explicit.

**Nb3 follow-up, 1 October 2026:** [12-figure gallery](gate2_N2_nabhan_2026/FIGURES.md), [completed additional analyses](gate2_N2_nabhan_2026/reports/FOLLOWUP_RESULTS.md), [external E5 pilot](gate2_N2_nabhan_2026/reports/E5_EXTERNAL_FEASIBILITY.md), and [A22/A23 derivation](gate2_N2_nabhan_2026/reports/RQ_DERIVATION.md). Source and biological-design holds remain explicit; no claim grade changed.

This index connects the owner's reading order with source-study context,
executed analyses and figure galleries. The same stable paper identifiers,
reading order and status fields are maintained in [ROADMAP.json](ROADMAP.json).
The [dataset inventory](../docs/DATASETS.md) maps deposits to all their uses;
the [question register](../RESEARCH_QUESTIONS.md) and
[question workspaces](../RQ_Specified/README.md) own the derived biological tests.

Current source status is maintained in ROADMAP.json and the linked article reports. Nb2/Nb3/Nb4 reading and execution updates supersede the older September checkpoint; reading, execution and acceptance remain separate.

Paper folders hold study notes, extracted variables/criteria and analysis
reports. Question-specific continuations can live outside the source-paper
folder. Historical entry, withdrawal and reading-order decisions remain in
the [decision log](../DEVELOPMENT.md). The former `Thesis/` directory was renamed
on 25 September 2026. Private reading annotations and large raw inputs remain
outside the tracked documentation.

## Nabhan branch: Nb2 initial execution

Subsequent [result-derived RQ synthesis](gate2_N1_nabhan_2023/RQ_DERIVATION.md)
proposes A19–A21; their later question-specific analyses and remaining functional gaps are linked from the question workspaces. N4/N8 remain paper-local.
All existing Nb2 analyses and figures stay under this paper.

Completed continuation: [paper-local Nb2 branch analysis](../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/README.md)
examines state/duration, receptor-output, fibroblast and vascular branches; its
results now motivate the subsequent A19–A21 synthesis.
The [new results](../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/RESULTS.md) retain failed
coverage/comparability gates and the vascular experimental-round rival.

[Nabhan 2023, Gate 2N item N1](gate2_N1_nabhan_2023/README.md) now has a source-grounded
three-track plan, ten published propositions to reproduce and eight owner-ordered
[Nabhan hypothesis cards](gate2_N1_nabhan_2023/HYPOTHESIS_REGISTER.md#nabhan-branch).
The PDF and three private context pages were reviewed. The 18-library bulk adaptation,
partial human atlas comparison and mouse extension are now executed.
[Results](gate2_N1_nabhan_2023/RESULTS.md), [six-figure gallery](gate2_N1_nabhan_2023/FIGURES.md)
and [remaining functional/design gates](gate2_N1_nabhan_2023/FUNCTIONAL_SOURCE_AUDIT.md)
separate measured observations from unvalidated hypotheses.

## Current reading decision, 1 October 2026

Reconciled with main on 3 October 2026.


Reading and analysis now have separate readiness rules. The foundation,
2C and 2N packages support synthesis; they are no longer a reason to postpone
all wider reading. **3A and 3B are open for literature exploration, while
Niethamer/S1 and D1 remain unrun and their data gates remain unmet.** W1 is
animal-level pseudobulk, not Compass flux inference. A12/A13 exploratory
results do not substitute for S1/D1 or establish a cytokine/Treg mechanism.

The current queue is a comparison exercise, not a new ranking of scientific
claims. Stable paper numbers and the historical full order remain below.

| Step | Read or review | Output that makes the next choice useful |
|---|---|---|
| Refresh | Relevant Nb3 (14) and Nb2 (6) figures and limitations | One measured result, one rival, one missing functional endpoint; no repeat full read |
| First comparison round | Yadav (16), Wheeler (X1), Dhillon-Richardson (X2), Saxton IL-22 (8), DuPage EZH2 (9) | One short evidence card per paper, comparing repair biology, immune-state regulation and functional/computational methods |
| Follow the strongest question | Compass (15), IL-10 (7), Zhang (11), Mu (X3), Ma (X4), then Wang (10) as relevant | Choose based on the biological uncertainty and the work desired, not only on available datasets |

Current evidence: use the Nb2, Nb3 and Nb4 packages in this checkout. Their completed analyses do not establish scientific acceptance or remove functional evidence gaps.

### 2X: cross-field literature comparison

New literature references have X identifiers so papers 1–16 and global RQ IDs
are not renumbered. These are reading candidates, not owner-completed notes
or newly authorized analysis workspaces. Public source checks: 1 October 2026.

| ID | Paper | Question to carry back to the lung work | Boundary |
|---|---|---|---|
| X1 | [Wheeler et al. 2023, functional astrocyte–microglia screening](https://doi.org/10.1126/science.abq4822) | What evidence beyond compatible ligand/receptor RNA supports a functional interaction? A2/A9/A12/A13/A22 | CNS assay logic does not validate a lung circuit |
| X2 | [Dhillon-Richardson et al. 2025, embryonic profile reuse in heart regeneration](https://doi.org/10.1073/pnas.2423697122) | How are developmental programme reuse and regenerative contribution distinguished? A1/A5/A8 | Zebrafish cardiac evidence is not mammalian lung fate evidence |
| X3 | [Mu et al. 2026, trained immunity and stem-cell aging](https://doi.org/10.1038/s43587-026-01175-2) | What separates durable inflammatory memory from continuing exposure? A3/A14 | Hematopoietic stem-cell findings do not establish epithelial memory |
| X4 | [Ma et al. 2025, nutrient-driven histone code and CD8 T-cell fate](https://doi.org/10.1126/science.adj3020) | How are metabolism, chromatin and functional immune states connected? | CD8 exhaustion is distinct from Treg stability and epithelial maturation |

Use the five-question note contract below, adding one sentence on whether the
question remains interesting outside the original tissue. PI matching,
personal reflection and contact planning stay in private Notion, consistent
with the earlier removal of outreach planning from this repository.

## Studies with executed analyses

Start with a study overview, then use its evidence report and gallery. Source
paper findings, repository reanalyses and proposed research questions are
different evidence layers. The [claim register](../CLAIMS.md) retains formal
decisions; the [question register](../RESEARCH_QUESTIONS.md) holds shared RQs.
An executed analysis does not mean every biological question is resolved or
that a study note has been accepted. Each overview states its limits.

<a id="figure-galleries"></a>

The [29 September figure audit](../docs/FIGURE_CLAIM_CORRECTIONS_2026-09-29.md)
records presentation corrections, preserved historical versions and review
coverage across the galleries. Study-specific additions and later updates are
linked in each study's gallery.

| Study and biological context | Analysis claims and evidence | Figures |
|---|---|---|
| [Niethamer 2025: viral injury and repair](gate1_01_niethamer_2025/README.md) | [Atlas report](gate1_01_niethamer_2025/GSE262927/README.md); [follow-up outcomes](gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) | [Gallery](gate1_01_niethamer_2025/README.md#figure-gallery) |
| [Choi 2020: AT2–DATP–AT1 transition](gate1_02_choi_2020/README.md) | [Trial outcomes](gate1_02_choi_2020/ANALYSIS_TRIAL_PLAN.md); [follow-up branches](gate1_02_choi_2020/README.md#branches-of-this-paper) | [State maps and branch galleries](gate1_02_choi_2020/README.md#figure-gallery) |
| [Nabhan 2023: Nb2](gate2_N1_nabhan_2023/README.md) | [Results and limits](gate2_N1_nabhan_2023/RESULTS.md); adapted bulk and descriptive atlas context | [Gallery](gate2_N1_nabhan_2023/FIGURES.md) |
| [Nabhan 2026: Nb3](gate2_N2_nabhan_2026/README.md) | [Reproduction review](gate2_N2_nabhan_2026/reports/REPRODUCTION_REVIEW.md), [follow-up](gate2_N2_nabhan_2026/reports/FOLLOWUP_RESULTS.md) and [external E5 pilot](gate2_N2_nabhan_2026/reports/E5_EXTERNAL_FEASIBILITY.md); descriptive, with source/design holds | [12-figure gallery](gate2_N2_nabhan_2026/FIGURES.md) |
| [Nabhan 2018: Wnt niche biology](gate1_03_nabhan_2018/README.md) | [Findings and limits](gate1_03_nabhan_2018/README.md#findings-that-motivate-research-questions); [animal-level report](gate1_03_nabhan_2018/nb1/README.md) | [Gallery](gate1_03_nabhan_2018/README.md#figure-gallery) |
| [Sikkema 2023: lung reference annotation](gate1_04_sikkema_2023_hlca/README.md) | [S1–S5 outcomes](gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md); [interpretation framework](gate1_04_sikkema_2023_hlca/PIPELINE_FRAMING.md) | [Gallery](gate1_04_sikkema_2023_hlca/README.md#figure-gallery) |
| [Cardoso 2026: tumour-associated niches](gate2_05_cardoso_2026/README.md) | [Analysis sequence](gate2_05_cardoso_2026/ANALYSIS_TRIAL_PLAN.md); [current ligand correction](../analysis/corrections/ligand/README.md) | [Gallery](gate2_05_cardoso_2026/README.md#figure-gallery) |
| [England 2025: mutant AT2 states and clone growth](gate2_C2_england_2025/README.md) | [Current claims and evidence review](gate2_C2_england_2025/EVIDENCE_REVIEW.md) | [15 figures by biological question](gate2_C2_england_2025/FIGURES.md) |
| [Yu, Lee, Choi_Min 2026: IL-1beta and niches](gate2_C3_yu_lee_choi_min_2026/README.md) | [Current evidence review](gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md); [completion register](gate2_C3_yu_lee_choi_min_2026/WORK_PACKAGES.md) | [Gallery](gate2_C3_yu_lee_choi_min_2026/README.md#figure-gallery) |
| [Murthy 2022: healthy human distal-lung atlas](ungated_murthy_2022/README.md) | [Generated atlas report](ungated_murthy_2022/GSE178360/README.md); deposit analysed, roadmap study note not written | [Gallery](ungated_murthy_2022/README.md#figure-gallery) |

The [epithelial-state specificity module](epithelial_state_specificity/README.md)
is a cross-study analysis, with its own [results](epithelial_state_specificity/results/SUMMARY.md)
and [figure](epithelial_state_specificity/README.md#figure-gallery).
Choi's [chromatin](gate1_02_choi_2020/datp_epigenetics/README.md#figure-gallery)
and [Axin2/Il1r1](gate1_02_choi_2020/axin2_il1r1/README.md#figure-gallery)
branches retain their separate galleries. Papers without executed analyses
remain in the roadmap below.

## Order and status

| # | Gate | Paper | DOI | PMID | Role in the roadmap | Folder | Study note | Analysis trial |
|--:|---|---|---|---|---|---|---|---|
| 1 | 1 | Niethamer et al. 2025, *Cell Stem Cell* | [10.1016/j.stem.2024.12.002](https://doi.org/10.1016/j.stem.2024.12.002) | 39818203 | source paper for GSE262927: animals, time points, annotations, known findings, limits | [`gate1_01_niethamer_2025/`](gate1_01_niethamer_2025/README.md) | done (in `docs/`) | done (`Research Article/gate1_01_niethamer_2025/GSE262927/`); phase and myeloid follow-ups N1 to N4 run 2026-09-10, Descriptive only, owner review pending: [`ANALYSIS_TRIAL_PLAN.md`](gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) |
| 2 | 1 | Choi et al. 2020, *Cell Stem Cell* | [10.1016/j.stem.2020.06.020](https://doi.org/10.1016/j.stem.2020.06.020) | 32750316 | biological spine: IL-1beta/HIF1alpha-driven AT2 to DATP to AT1 transition | [`gate1_02_choi_2020/`](gate1_02_choi_2020/README.md) (re-entered 2026-09-15 at the owner's direction after reading, decision 23; the AI-written note of 2026-09-13 was withdrawn first and stays in git history, PR #19) | done (2026-09-15, owner-directed) | trials D0 to D7 run 2026-09-15 with a corrected annotation pass D2b beside D2; Gate 1 not fully recovered from the deposit (four of five states; primed AT2 never assigned as a cluster); Descriptive only, owner review pending: [`ANALYSIS_TRIAL_PLAN.md`](gate1_02_choi_2020/ANALYSIS_TRIAL_PLAN.md). Two branches opened 2026-09-20 on other laboratories' multiome deposits, because this paper's ATAC deposit is coverage tracks only: [`datp_epigenetics/`](gate1_02_choi_2020/datp_epigenetics/README.md) (M0 to M4; one validated deposit error, the chromatin question Not established with a direction) and [`axin2_il1r1/`](gate1_02_choi_2020/axin2_il1r1/README.md) (this paper's own closing Discussion question; assessed, two routes run and refused). Rows C116 to C154 |
| 3 | 1 | Nabhan et al. 2018, *Science* | [10.1126/science.aam6603](https://doi.org/10.1126/science.aam6603) | 29420258 | fibroblast Wnt niches maintain AT2 stemness; niche exit permits AT1 differentiation | [`gate1_03_nabhan_2018/`](gate1_03_nabhan_2018/README.md) | owner completed reading 2026-09-22; notes remain private | Source reproduction, descriptive Nb1 and external cohort eligibility: [analysis report](gate1_03_nabhan_2018/README.md) |
| 4 | 1 | Sikkema et al. 2023, *Nature Medicine* (HLCA) | [10.1038/s41591-023-02327-2](https://doi.org/10.1038/s41591-023-02327-2) | 37291214 | reference framework: annotation hierarchy, reference mapping, uncertainty handling, donor coverage, shared profibrotic macrophage states | [`gate1_04_sikkema_2023_hlca/`](gate1_04_sikkema_2023_hlca/README.md) | done, owner review pending | S1 to S5 run (Descriptive only); see [`ANALYSIS_TRIAL_PLAN.md`](gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md) |
| 5 | 2C | Cardoso, Lee et al. 2026, *Nature* | [10.1038/s41586-026-10399-6](https://doi.org/10.1038/s41586-026-10399-6) | 42020743 | early fibrotic niches; regenerative-like mutant AT2 states coordinate fibroblast and immune remodelling through AREG-EGFR | [`gate2_05_cardoso_2026/`](gate2_05_cardoso_2026/README.md) | done, owner review pending | Original C/E trials completed; later annotation, depth and resource corrections supersede the initial E1 reading. Use the [current ligand correction](../analysis/corrections/ligand/README.md) and [A2 synthesis](../RQ_Specified/A2_areg_source_delivery/reports/STAGE5_SYNTHESIS.md); historical sequence in the [trial plan](gate2_05_cardoso_2026/ANALYSIS_TRIAL_PLAN.md). Independent genotype/engagement inference remains limited. |
| 12 | 2C | England et al. 2025, *Cell Stem Cell* | [10.1016/j.stem.2025.01.011](https://doi.org/10.1016/j.stem.2025.01.011) | 39978341 | NF-kappaB feedback, Il1r1 reprogramming, mutant-WT context and clone distributions; two pooled-lung sequencing experiments | [`gate2_C2_england_2025/`](gate2_C2_england_2025/README.md) | owner read confirmed 2026-09-27; synthesis prepared | Batch1, continuation, follow-up and original Stage1 retained. [Corrected A16 C1](../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md) and [A17 source accounting](../docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md) completed; residual matching imbalance, source discrepancies, full refit and independent functional evidence remain open. [Current review](gate2_C2_england_2025/EVIDENCE_REVIEW.md). |
| 13 | 2C | Yu, Lee, Choi_Min and Choi 2026, *Seminars in Immunology* (review) | [10.1016/j.smim.2026.102050](https://doi.org/10.1016/j.smim.2026.102050) | 42497497 | review-motivated IL-1beta perturbation, state specificity and niche-context questions | [`gate2_C3_yu_lee_choi_min_2026/`](gate2_C3_yu_lee_choi_min_2026/README.md) | owner read; synthesis prepared; staged execution authorized 2026-09-24 | [Feasible paper analyses complete](gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md). Derived A11 acute assay and A12/A13 exploratory pilots completed; [later A12 cohort recovery](../RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md) admits no unchanged validation cohort. Causal/fate, annotation and region gates remain. |
| 6 | 2N | Nabhan et al. 2023, *Cell* | [10.1016/j.cell.2023.05.022](https://doi.org/10.1016/j.cell.2023.05.022) | 37321220 | Receptor-selective Wnt response, growth and differentiation | [`gate2_N1_nabhan_2023/`](gate2_N1_nabhan_2023/README.md) | owner completed reading 2026-09-29; PDF and private context reviewed | [Nb2 results](gate2_N1_nabhan_2023/RESULTS.md), [gallery](gate2_N1_nabhan_2023/FIGURES.md) and [candidates](gate2_N1_nabhan_2023/HYPOTHESIS_REGISTER.md#nabhan-branch); adapted/partial analysis executed, exact/functional reproduction open |
| 14 | 2N | Nabhan et al. 2026, *PNAS* | [10.1073/pnas.2606113123](https://doi.org/10.1073/pnas.2606113123) | 42418498 | an alveolosphere screen of 201 genes with chimeric RNA-seq of stem-cell effects on the fibroblast niche | [`gate2_N2_nabhan_2026/`](gate2_N2_nabhan_2026/README.md) | owner finished reading 2026-10-01; source synthesis prepared | **Nb3:** [source-informed reproduction](gate2_N2_nabhan_2026/reports/REPRODUCTION_REVIEW.md) and [descriptive extensions](gate2_N2_nabhan_2026/reports/EXTENSION_REVIEW.md); exact-source/spatial gates retained; prior A10/A2 preserved |
| 15 | 2W | Wagner et al. 2021, *Cell* | [10.1016/j.cell.2021.05.045](https://doi.org/10.1016/j.cell.2021.05.045) | 34216539 | Reaction-level metabolic potential; separate from Niethamer W1 | [paper package](gate2_W1_wagner_th17_autoimmunity/README.md) | owner read 2026-10-04; notes reconciled | Wg reproduction and six branches planned; numerical work unrun |
| 16 | 2W | Yadav et al. 2025, *JCI* | [10.1172/JCI188734](https://doi.org/10.1172/JCI188734) | 40875483 | the lung-fibrosis myeloid-to-mesenchymal ARG1 and ornithine circuit, with Wagner as co-author; the comparison proposal W1 names | not started | not started; current comparison queue; owner reading unconfirmed | W1 pseudobulk completed; Compass flux analysis not run (Stage 2 of paper 1's plan) |
| 7 | 3A | Saxton et al. 2021, *Science* | [10.1126/science.abc8433](https://doi.org/10.1126/science.abc8433) | 33737461 | structure-based decoupling of IL-10 pro- and anti-inflammatory functions | paused (Gate 3A paused 2026-09-15; opens if proposal S1 separates repair phases at the animal level) | not started; reading open 2026-10-01; analysis remains gated | not started |
| 8 | 3A | Saxton et al. 2021, *Immunity* | [10.1016/j.immuni.2021.03.008](https://doi.org/10.1016/j.immuni.2021.03.008) | 33852830 | IL-22 tissue-protective vs pro-inflammatory functions decoupled | paused (Gate 3A paused 2026-09-15; opens if proposal S1 separates repair phases at the animal level) | not started; reading open 2026-10-01; analysis remains gated | not started |
| 9 | 3B | DuPage et al. 2015, *Immunity* | [10.1016/j.immuni.2015.01.007](https://doi.org/10.1016/j.immuni.2015.01.007) | 25680271 | Ezh2 maintains regulatory T cell identity after activation | paused (Gate 3B paused 2026-09-15; opens if proposal D1 finds Tregs separable in an external series) | not started; reading open 2026-10-01; analysis remains gated | not started |
| 10 | 3B | Wang et al. 2018, *Cell Reports* | [10.1016/j.celrep.2018.05.050](https://doi.org/10.1016/j.celrep.2018.05.050) | 29898397 | targeting EZH2 reprograms intratumoral Tregs | paused (Gate 3B paused 2026-09-15; opens if proposal D1 finds Tregs separable in an external series) | not started; reading open 2026-10-01; analysis remains gated | not started |
| 11 | 3B | Zhang et al. 2026, *Science Immunology* | [10.1126/sciimmunol.adx4411](https://doi.org/10.1126/sciimmunol.adx4411) | 41961946 | intratumoral Treg ablation elicits NK-mediated control | paused (Gate 3B paused 2026-09-15; opens if proposal D1 finds Tregs separable in an external series) | not started; reading open 2026-10-01; analysis remains gated | not started |

The `#` is a stable identifier assigned when a paper enters the roadmap, and
folder names normally carry it. England uses branch 2C item 2 (`gate2_C2`, stable order 12),
and Yu uses branch 2C item 3 (`gate2_C3`, stable order 13). The row order above is the reading order. Papers 12 to
16 were added on 2026-09-15 (see the re-ranking bullet below).

### Methods references, read at the backbone step that uses them

Not gated papers: each is read when the backbone step it supports is built.
Identifiers verified against PubMed on 2026-09-15.

| Ref | Paper | DOI | PMID | Backbone step | Used in this repository |
|---|---|---|---|---|---|
| M1 | Squair et al. 2021, *Nature Communications*: confronting false discoveries in single-cell differential expression | [10.1038/s41467-021-25960-2](https://doi.org/10.1038/s41467-021-25960-2) | 34584091 | 3, sample-aware pseudobulk | the animal-as-unit rule throughout; animal/donor pseudobulk completed in W1 and IPF/human extensions |
| M2 | Lotfollahi et al. 2022, *Nature Biotechnology*: scArches reference mapping | [10.1038/s41587-021-01001-7](https://doi.org/10.1038/s41587-021-01001-7) | 34462589 | 2, reference mapping | trial S2 |
| M3a | Dimitrov et al. 2024, *Nature Cell Biology*: LIANA+ | [10.1038/s41556-024-01469-w](https://doi.org/10.1038/s41556-024-01469-w) | 39223377 | 5, communication | trial C12 (liana) |
| M3b | Jin et al. 2021, *Nature Communications*: CellChat | [10.1038/s41467-021-21246-9](https://doi.org/10.1038/s41467-021-21246-9) | 33597522 | 5, communication | the Cardoso paper's tool; R-only, never run here |
| M4 | Zaiss et al. 2015, *Immunity*: amphiregulin in immunity, inflammation and repair | [10.1016/j.immuni.2015.01.020](https://doi.org/10.1016/j.immuni.2015.01.020) | 25692699 | 5, the constraint on epithelium-centric AREG readings | claim C45 |
| M5a | Kobayashi et al. 2020, *Nature Cell Biology*: the transitional (PATS) state | [10.1038/s41556-020-0542-8](https://doi.org/10.1038/s41556-020-0542-8) | 32661339 | 4, the Krt8 transitional programme | `docs/DOUBLETS_AND_SCRUBLET.md`; the displaced Krt8 trajectory |
| M5b | Strunz et al. 2020, *Nature Communications*: the Krt8+ transitional state | [10.1038/s41467-020-17358-3](https://doi.org/10.1038/s41467-020-17358-3) | 32678092 | 4, the Krt8 transitional programme | A0 discovery, A5 external-signature test, shared specificity work; [A5](../RQ_Specified/A5_developmental_programme_reuse/README.md) records the current interpretation |
| M6 | Tsukui et al. 2020, *Nature Communications*: collagen-producing lung cell atlas | [10.1038/s41467-020-15647-5](https://doi.org/10.1038/s41467-020-15647-5) | 32317643 | 4, fibroblast states | trials E4, C9, C10 |
| M7 | Vaughan et al. 2015, *Nature*: lineage-negative progenitors after major injury | [10.1038/nature14112](https://doi.org/10.1038/nature14112) | 25533958 | 4, the KRT5 dysplastic programme | not used |
| M8 | van den Brink et al. 2017, *Nature Methods*: dissociation-induced gene expression in tissue subpopulations | [10.1038/nmeth.4437](https://doi.org/10.1038/nmeth.4437) | 28960196 | 2, the dissociation-stress list any stress-like programme reading needs | named by Choi 2020 attack A3 (trial D7), not attempted because the list is in the paper's supplement and not on disk |


Outside the roadmap but already in the repository: Kadur Lakshminarasimha
Murthy et al. 2022, *Nature* (DOI
[10.1038/s41586-022-04541-3](https://doi.org/10.1038/s41586-022-04541-3),
PMID 35355018), the source paper for GSE178360, analysed in
[`Research Article/ungated_murthy_2022/GSE178360/`](ungated_murthy_2022/GSE178360/README.md). The HLCA lists
that series as one of its extension datasets (Tata_unpubl), which is why the
Sikkema trial S2 targets it.

DOIs and PMIDs were verified against PubMed on 2026-09-09.

## Gate rules carried over from the roadmap

- **Analysis gate.** After papers 1 to 4, write a one-page analysis contract
  and begin with deposited count matrices plus metadata, not FASTQ. The
  initial question stays narrow: do early versus late KRT8 transitional
  epithelial states associate with different macrophage and fibroblast niche
  programmes in GSE262927?
- **Stop rule.** Finish papers 1 to 4, write the contract, start the pilot.
  Read papers 5 to 16 only when a specific pilot result makes their branch
  relevant.
- **Gate 3A** opens only if the cytokine or resolution signal is strong.
  **Gate 3B** opens only if regulatory T cells are sufficiently represented;
  note that the HLCA core could not separate Tregs from other T cells, which
  is a known ceiling for any reference-based route to that branch.
- **Re-ranking of 2026-09-15.** The owner re-ranked the reading order.
  Consequences for this roadmap: papers 3 and 6 (Nabhan 2018 and
  2023) move to the front of the queue, with proposal Nb1 as their trial;
  Gate 3A and 3B are paused rather than closed, since their opening
  conditions stand and are exactly what proposals S1 and D1 test; the
  analysis contract and the KRT8 pilot of the analysis gate are still
  unwritten and remain the stop rule's precondition. Paper 5 was completed
  out of order before this re-ranking and is not affected.
- **Gate 2 branches (2026-09-15).** Gate 2 is split into 2C (the Choi
  axis: paper 5 done, papers 12 and 13 added), 2N (Nabhan: papers 6 and
  14) and 2W (Wagner: papers 15 and 16, added because the method behind
  proposal W1 had no paper in the original order). England and Yu use branch-position labels `gate2_C2` and `gate2_C3`
  while retaining stable paper IDs 12 and 13. Nabhan 2023 uses the owner-selected
  `gate2_N1` (branch 2N item 1), retaining stable paper ID 6. Other Gate 2 folder names keep
  the plain `gate2_` prefix; branch membership is recorded in this table and
  `ROADMAP.json`. Papers in 2C and 2N are read while interpreting the pilot
  figures, as before; 2W is read alongside proposal W1.

## Folder contract

```
Research Article/
  README.md                       this index
  ROADMAP.json                    the same table, machine-readable
  gateG_NN_firstauthor_year/       G is 1, 2 (any Gate 2 branch), 3A or 3B
    README.md                     study note: five questions, plus the extracts the roadmap names for that paper
    *.json                        parameters and decision criteria extracted from the paper, reviewable
    PIPELINE_FRAMING.md           (when a paper is a methods reference) what this repository adopts, adapts, declines
    ANALYSIS_TRIAL_PLAN.md        pre-registered trial(s): rule, threshold, dataset, success and failure criteria, outcome
    trials/                       trial scripts and their logged artefacts (small tables and JSON are tracked)
    <accession>/                  the deposit itself, when this paper produced it (paper 1 holds GSE262927)
  ungated_firstauthor_year/       a source paper outside the roadmap, made only to hold its deposit beside it
    README.md                     a pointer note, not a study note; the study note waits for the reading (Murthy 2022 holds GSE178360)
```

Reading/workflow statuses in `ROADMAP.json` describe progress, not evidence
grades. Scientific status belongs in the [claim register](../CLAIMS.md) or the
linked question report. An executed analysis needs a report and logged artifacts
in its paper or question workspace; a plan alone is not a result. Each run
records its freeze or exposed-data amendment and interpretation limits.

## Local, untracked material

The PDFs and supplementary files for the roadmap papers live in the owner's
external thesis-study folder (organised by gate) and, for the earlier
papers, directly under this directory; both locations are ignored by git.
`docs/scRNAseq_workflow_Niethamer2025.md` records a filing correction for
one mislabelled local PDF.
