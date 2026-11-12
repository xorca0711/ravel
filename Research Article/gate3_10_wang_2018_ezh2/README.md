# Wang 2018: EZH2, activated Tregs and tumor immunity

11 November 2026. **Source interpretation and proposed analysis plan. No numerical
analysis has run.** Owner reading is complete. This package does not register a
new canonical RQ or change the separate Niethamer/D1 gate.

[Stepwise analysis plan](ANALYSIS_PLAN.md) · [Literature and access record](LITERATURE_CONTEXT.md)
· [Wang et al., Cell Reports 2018](https://doi.org/10.1016/j.celrep.2018.05.050)
· [GSE114298](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114298)

## Biological purpose

How does disrupting EZH2 change activated Treg behavior, and what distinguishes
reduced suppression, active support of antitumor immunity, and changes in the
abundance or composition of the Treg population? These processes can coexist.
Wang's interventions and functional measurements address parts of this question;
the deposited RNA comparison addresses a narrower transcriptional component.

The immediate executable question is: **which transcript-abundance differences
between Ezh2-deficient and control Treg preparations are reproducible after four
days of activation, and how complete is the reported inflammatory shift?** Its
contribution is source reproduction and sensitivity assessment. A tumor-specific
mechanism, time trajectory or new target does not follow automatically.

## What the paper establishes, and what needs qualification

The table refers to the published experiments, not new repository results.
Main-text Results, legends and methods were read from the stored paper. Supplement
plots and their RNA-specific methods have not yet been recovered in this task.

| Evidence | Implication | Boundary that matters for the plan |
|---|---|---|
| Figure 1A–G: systemic CPI-1205 in MC38 hosts; immune-deficient and competent settings; Treg H3K27me3/FOXP3 measurements | Antitumor activity depends on host context; drug exposure reaches Tregs | Systemic drug effects are not Treg-specific. Rag1 deficiency affects adaptive immunity broadly. Higher EZH2 RNA is not a direct assay of enzyme activity. |
| Figure 2A–E: mouse/human protein and human RNA comparisons | TI-Tregs show an EZH2-associated phenotype in the sampled settings | Human RNA in 2D–E reuses De Simone/Plitas sources. Association does not measure response to EZH2 perturbation. |
| Figures 3–4 and S2: Treg-restricted genetic disruption, several tumor models and effector-cell readouts | Treg EZH2 contributes to suppression in the tested models | B16F10 is restrained but not rejected without the additional vaccination context. Constitutive deletion and acute treatment are different interventions. |
| Figure 5A–G: lineage reporter, FOXP3 retention/loss and restimulated cytokines | Foxp3 instability and altered cytokine capacity among FOXP3-retaining cells both occur | Lower FOXP3-positive frequency is not synonymous with death or physical depletion. Restimulated intracellular cytokines do not directly measure unstimulated secretion in situ. |
| S3B–C, described in the main Results: day-4 activated naive Treg RNA | An inflammatory transcriptional component is detectable outside tumors | The authors report lower Il10/Tgfb1, higher Il2 and enrichment, while many other inflammatory cytokines are not significantly changed. Partial/mixed responses must be retained. |
| Figure 6 and S4–S5: inducible deletion after Treg development | Cytokine changes and tumor protection can occur without a detected reduction in Treg frequency at the examined time | A nonsignificant frequency difference is not equivalence in absolute numbers, survival, composition or later behavior. The experiments do not establish an RNA time course. |
| Figure 7F–H and S6: chimeric females with residual Ezh2-deficient Tregs during WT depletion | Already tests the contribution of remaining deficient Tregs beyond the particular depletion comparator | This is an established premise, not an untested novelty claim. It does not identify the necessary cytokine or generalize to every local depletion strategy. |

The absence of apparent autoimmunity in the tested acute setting is a bounded
mouse observation. Constitutive/developmental loss has different consequences;
the paper does not establish universally safe systemic inhibition or human safety.
Checkpoint-associated EZH2 induction is proposed in Wang's Discussion; related
anti–CTLA-4 combination work was already reported by Goswami et al. (2018).
See the [literature record](LITERATURE_CONTEXT.md).

## Available source and missing inputs

GEO lists bulk mouse RNA-seq, four Ezh2-deficient and five WT biological
replicates, after four days of anti-CD3/CD28 activation with IL-2. The main paper
specifies starting CD62L-positive naive Tregs. GEO lists a processed count file
and raw SRA reads. The actual count file, sample sheets and supplementary RNA
methods have not been audited here. A reported biological replicate is not yet
a verified individual mouse: pooling, donor reuse, sex, genotype/control details,
batch and any paired preparation remain to be established.

These are not deposited intratumoral single-cell perturbation measurements.
The four-versus-five comparison has neither an unactivated baseline nor matched
tumor/non-tumor arms, so it cannot estimate an activation-by-genotype,
tissue-by-genotype or time-by-genotype interaction by itself.

## Connection to existing repository evidence

[Dp1's current follow-up](../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md)
found context-dependent signs across unmatched loss/gain sources. Tigit, Prdm1
and Ccr2 were higher in the Peeters fresh gain context but lower after culture;
Igfbp4 was lower in both. These are transformed-expression descriptions, not
comparable effect sizes or proof of an inverse mechanism. A33–A35 retain their
existing ownership; Wang can provide a later, separately qualified context check.

[Zhang's current RNA results](../gate3_11_zhang_2026_nk/RESULTS.md) concern sorted
NK preparations after local Treg depletion. They are a complementary recipient
comparison, not another measurement of Wang's Treg state. Their block/ranking
sensitivity also demonstrates why reproducing a selected panel and establishing
a general biological program are different tasks.

## Proposed order and present status

| Stage | Purpose | Current status |
|---|---|---|
| S0 | Separate published perturbation, abundance, lineage and functional evidence | Main-text/notes synthesis complete; supplementary detail pending |
| S1 | Qualify GSE114298 inputs, sample identities and model eligibility | Proposed; must precede numerical work |
| S2 | Reproduce the day-4 genotype RNA contrast | Conditional on S1; no results |
| S3 | Test breadth and sensitivity of the inflammatory/suppressive description | Conditional on S2; retain partial and unfavorable outcomes |
| S4 | Compare activation contexts and optionally the original human source contrast | Optional, question-dependent extension; sources stay separate |
| S5 | Integrate with the published functional evidence and select any justified follow-up | Reading synthesis can proceed independently of RNA holds |

The [plan](ANALYSIS_PLAN.md) specifies comparisons, outputs and decisions. Start
with S1, then S2–S3 if qualified. S4 is not an automatic expansion queue. Any
numerical stage needs a registered article owner, frozen source/code contract,
preflight and runner under [research governance](../../docs/RESEARCH_GOVERNANCE.md).
