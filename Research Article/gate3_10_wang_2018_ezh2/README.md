# Wang 2018: EZH2, activated Tregs and tumor immunity

12 November 2026. **The adapted day-four RNA analysis is complete at the
deposited-library level.** The article-local owner is Wang18-P01.

[Results and measured figures](RESULTS_V1.md) · [Source qualification](SOURCE_QUALIFICATION.md)
· [Execution review](REVIEW_20261112.md) · [F1 source audit](F1_SOURCE_AUDIT_20261112.md)
· [F2 ranking sensitivity](F2_RESULTS_V1.md)
· [Stepwise analysis plan](ANALYSIS_PLAN.md) · [Literature and access record](LITERATURE_CONTEXT.md)
· [Wang et al., Cell Reports 2018](https://doi.org/10.1016/j.celrep.2018.05.050)
· [GSE114298](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114298)

## Biological purpose

How does disrupting EZH2 change activated Treg behavior, and what distinguishes
reduced suppression, active support of antitumor immunity, and changes in the
abundance or composition of the Treg population? These processes can coexist.
Wang's interventions and functional measurements address parts of this question;
the deposited RNA comparison addresses a narrower transcriptional component.

The four Ezh2-deficient day-four libraries showed lower Il10 and Tgfb1 and
higher Il2 than the deposited controls, with the same directions under strict
+/+ controls. TNF/NF-κB and inflammatory ranks stayed positive across the
tested sensitivities. Lower E2F/G2M ranks and higher apoptosis ranks leave a
specific unresolved question about the proportions and viable recovery of
activated states. Bulk RNA measures the resulting library mixture. Sparse
cytokine RNA and overlapping library values limit the interpretation of the
full inflammatory response. [Results and figures](RESULTS_V1.md).

The F2 sensitivity kept those inflammatory, cell-cycle and apoptosis
directions under the source-named Signal2Noise metric. Three other Hallmarks
reversed direction, so rank robustness applies to specific themes.
[F2 results and measured comparison](F2_RESULTS_V1.md).

## What the paper establishes, and what needs qualification

The table refers to the published experiments. The main article and publisher
supplement were recovered, including the RNA methods and S3B–C.
[Panel-level evidence and dependent holds](RESULTS_V1.md#s5--what-the-rna-changes-add-to-the-functional-evidence).

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

The count matrix, GEO, ENA and BioSample identify four fl/fl, four +/+, and one
fl/+ libraries. Figure S3C labels its five control points fl/+. Mouse/pool
membership, sex, age and processing blocks remain unresolved. The analysis
uses the deposited allele labels and describes relative RNA without estimating
animal-population uncertainty. F1 recovered the original S3B Signal2Noise
ranking label and SRA filename prefix `DuPage_667`. The public records
still lack the panel crosswalk, normalization, exact GSEA inputs and
mouse/pool and processing assignments. [F1 source audit](F1_SOURCE_AUDIT_20261112.md).

These are not deposited intratumoral single-cell perturbation measurements.
The four-versus-five comparison has neither an unactivated baseline nor matched
tumor/non-tumor arms, so it cannot estimate an activation-by-genotype,
tissue-by-genotype or time-by-genotype interaction by itself.

## Connection to existing repository evidence

[Dp1's current follow-up](../gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md)
found context-dependent signs across unmatched loss/gain sources. Tigit, Prdm1
and Ccr2 were higher in the Peeters fresh gain context but lower after culture;
Igfbp4 was lower in both. These are transformed-expression descriptions, not
comparable effect sizes or proof of an inverse mechanism. Wang's five-gene
direction comparison found reciprocal Igfbp4 directions across the compared
loss/gain settings, a fragile Ccr2 direction, and concordant Areg increases in
Wang loss and Peeters gain. The contrasts retain separate scales and designs.
[Fixed-panel comparison](RESULTS_V1.md#s4--five-exposed-genes-across-separate-activation-contexts).

[Zhang's current RNA results](../gate3_11_zhang_2026_nk/RESULTS.md) concern sorted
NK preparations after local Treg depletion. They are a complementary recipient
comparison, not another measurement of Wang's Treg state. Their block/ranking
sensitivity also demonstrates why reproducing a selected panel and establishing
a general biological program are different tasks.

## Execution and next decision

| Stage | Purpose | Current status |
|---|---|---|
| S0 | Separate published abundance, lineage and functional evidence | Supplement and functional evidence ledger complete |
| S1 | Qualify counts, genotypes and units | Nine libraries verified. Mouse/pool identity remains unknown. |
| S2 | Reconstruct the cultured RNA contrast | Adapted library description completed. Population inference and exact replay held. |
| S3 | Assess breadth and sensitivity | All 50 adapted mouse Hallmarks and the eligible gene universe reported. |
| S4 | Compare activation contexts | Fixed five-gene mouse panel completed. Human tissue association branch closed for this question. |
| S5 | Reconcile the RNA with published function | Published assays integrated. Per-animal functional inputs were not located. |
| F1 | Check original sample and analysis records | Source audit complete. Signal2Noise and a facility filename prefix were recovered. Exact replay, population inference and functional reconstruction remain held. |
| F2 | Check the effect of the source-named rank metric | All 50 sets compared. Inflammatory and culture-state themes retained their directions. Ready for checkpoint review. |

The next discriminator, if matched material becomes available, is whether the
RNA shift persists within the same recovered Treg state when viable recovery
and state composition are measured. The immediate follow-up decision is
whether to seek existing author records using the
[local draft request](F1_AUTHOR_REQUEST_DRAFT.md), after checkpoint review.
[Execution amendment](EXECUTION_AMENDMENT_V1.md) ·
[Context amendment](CONTEXT_AMENDMENT_V1.md).
