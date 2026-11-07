# DuPage-first target screen and proposal portfolio

7 November 2026. **Exploratory candidate development, not target validation.**
Dp1-P01 remains article-local. The owner requested a fresh screen from DuPage
2015 and explicitly made the Zhang 2026 direction optional. Scientific
hypothesis-generation, literature-review and academic-plotting skills informed
the rationale, source checks and figures. None grants scientific acceptance.

## What the analysis now says

The [completed S0–S6 reconstruction](RESULTS.md) remains mixed: activation-state
differences depend appreciably on the retained libraries, and external chromatin
consistency is weak and covers only part of the RNA universe. It established
neither a direct EZH2 target nor a mechanism of tissue Treg loss.

The new screen asks which *specific* RNA observations justify a functional
question despite those aggregate limits. [V1 specification](TARGET_SCREEN_PLAN_V1.md)
was frozen at `2fecf66`, before ranking. All 11,614 loci and 11 retained
preparations were preserved. Two signed tracks consider low-state KO–HET
differences and differences stronger in that state, with sample-omission and
pseudocount stability. Forty display slots represented 26 distinct loci; only
three qualified as protein coding in the subsequent annotation. Most of the
largest entries carried small-noncoding-RNA labels, despite the source protocol
being poly-A selection. That is an assay-qualification finding, not evidence
for a mature-miRNA mechanism.

[V2 amendment](TARGET_SCREEN_AMENDMENT_V2.md), frozen at `a9aa0d0`, retains v1
and adds a current, pinned NCBI symbol/chromosome audit. Of 11,614 loci, 9,845
qualify as protein coding; 646 have other exact gene types, 1,107 are unmatched,
and 16 have chromosome disagreement. No aliases were silently repaired. Four
signed reading lists yield **32 distinct protein-coding candidates**. Their
ordering is a sensitivity-based reading aid, not a biological validity score.

The selected patterns include lower Tigit, Prdm1, Il10 and several chemokine
receptors, alongside higher Igfbp4. Separately declared reference genes include
higher Bach2, Klf2, Tcf7, Lef1 and Bcl2. This motivates a distinction between
altered effector-state acquisition and a particular functional bottleneck.
It does not establish a uniform programme, a cell fate, or a migration defect.

## Candidate observations and decisions

Values below are differences of **mean log2(FPKM + 1)**, not ordinary log2 fold
changes. I = low-state KO–HET minus high-state KO–HET. No p-values or confidence
intervals are claimed. Every featured candidate was selected after viewing
outcomes; anchors and the full screened frontier remain distinguishable.

| Candidate | Low contrast | I | Why investigate / limit |
|---|---:|---:|---|
| Tigit | −1.777 | −1.043 | Functional receptor candidate; protein and inducible output unmeasured |
| Prdm1 | −1.357 | −1.153 | Possible downstream effector regulator; a broad differentiation change is a rival |
| Ccr2 | −1.966 | −1.513 | Strong receptor change; localization and fitness must be measured separately |
| Igfbp4 | +1.514 | +1.043 | Growth-factor-buffer candidate; first qualify Treg source, protein and cell-state dependence |
| Il1r2 | −1.412 | −0.935 | Useful marker-versus-mediator counterexample; context-dependent published function |
| Adcy6 | +0.849 | +0.930 | cAMP synthesis candidate; RNA is not net cAMP production |
| Pde3b (prior-paper anchor) | +0.864 | +0.607 | cAMP degradation route already has substantial prior biology; not a new discovery |
| Areg (endpoint anchor) | −0.293 | −0.161 | I changes sign under sensitivity; no established loss of AREG/repair function |
| Il2ra (endpoint anchor) | +0.004 | +0.030 | Fragile contrast; no support for a simple generalized CD25-transcript-loss explanation |
| Bcl2 (endpoint anchor) | +0.625 | +0.577 | Direction cautions against explaining later death by a simple Bcl2 RNA decrease |

Igfbp4, Adcy6 and Pde3b have positive activation-associated H3K27me3 context
in the adapted Arvey mapping. Tigit and Ccr2 are uncovered; Prdm1 is mapped with
a nonpositive change. These are different-study annotations already reused by
DuPage, not matched KO chromatin or proof of direct EZH2 targeting.

All 32 coding-frontier entries received a bounded disposition:

| Entries | Current reading disposition |
|---|---|
| Tigit, Prdm1, Ccr2, Igfbp4 | Focused primary-source review; proposed comparisons below |
| Il10, Il1r2 | Known output/marker comparators; IL1R2 genetic findings caution against equating a marker with a mediator |
| Adcy6 | Consider with the separately declared Pde3b anchor; opposing synthesis/degradation annotations do not determine net cAMP |
| H2-Aa, H2-Ab1, H2-Eb1, Ly6c2, Ly6d, Dapl1 | Qualify lineage/state composition and cell-source expression; neither contamination nor a new Treg function is established |
| Rps27 | Large ribosomal-gene estimate merits locus/quantification qualification before a target story |
| Ccr4, Ccr5, Cxcr3, Cxcr6, Klrg1, S100a4, S100a6 | Context for a broader state difference; not seven independently verified mechanisms |
| Rnf130, Klk1b22, G0s2, Ntn4, Khdc1c, Ager, Myo1f, Adam8, Il4, Ly6a, Lsr | Retained unresolved. No sufficiently qualified Treg-specific functional explanation was established in this bounded pass; no novelty or irrelevance claim |

## Three proposed research directions

### 1. TIGIT–PRDM1: inducible functional competence

**Question:** does Ezh2 loss reduce TIGIT-dependent Blimp-1/AREG output within
viable activated Tregs, beyond shifting their activation-state composition?

The [2025 TIGIT study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12571903/),
Figures 3 and 6, establishes a tissue-protective role and TIGIT/TCR-dependent
Blimp-1–AREG regulation in its infection/stimulation settings. That mechanism is
a premise, not this screen's discovery. Our RNA changes motivate testing the
upstream Ezh2 connection in a common activation context. Areg RNA alone does not
answer whether an inducible response is intact.

The [2024 EZH2 gain-of-function study](https://pubmed.ncbi.nlm.nih.gov/39264807/)
already includes TIGIT protein phenotyping (Figures 2B, 4D and 7G). Thus, even
the broad EZH2–TIGIT association has precedent. The proposed increment is the
**genotype-dependent inducible output and its functional contribution**, beyond
the established effector-state phenotype; novelty remains unverified.

First compare lineage-labelled HET/KO Tregs under the same activation, with and
without defined TIGIT engagement. Measure surface TIGIT, Blimp-1 protein and
secreted AREG per viable cell, with absolute viable recovery, division and Foxp3
retention reported separately. The principal comparison is the genotype
difference in the response to TIGIT engagement; genotype-only and response
effects should remain visible. Because activation is itself potentially
affected by Ezh2, this estimates a response under common exposure, not a causal
effect conditioned on an unaffected activation state.

A reproducible output deficit motivates a Treg-restricted receptor/restoration
or downstream perturbation chosen to locate the defect. A general activation
deficit, altered survival or unchanged output despite RNA changes weakens a
TIGIT-specific account. A recipient barrier-recovery assay would be necessary
before claiming repair; secretion alone is insufficient. This is the clearest
functional extension in the present local shortlist, not a portfolio-wide
priority or a demonstrated new mechanism.

### 2. CCR2: localization versus cellular fitness

**Question:** does the Ccr2 decrease contribute to defective localization, altered
IL-2 responsiveness/fitness, or merely identify a different activated Treg state?

The [CCR2 study](https://pmc.ncbi.nlm.nih.gov/articles/PMC7000403/), particularly
Figure 5 and its CD25-stimulation results, supplies a non-migration alternative.
The [2024 intestinal microniche study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11041794/),
Figure 5 and Extended Data 9, adds spatial context; receptor–ligand inference is
not itself a demonstration that CCR2 causes the observed positioning.

Start with CCR2 protein, direct chemotaxis and CD25/IL-2 response plus viable
recovery in matched activated HET/KO preparations. If a genotype difference is
qualified, a Treg-restricted CCR2 perturbation/restoration can test contribution.
Direct tracking is required for an in-vivo homing claim. Preserved migration
with altered fitness, or coordinated loss of multiple effector markers, changes
the interpretation. Tissue frequency is never the migration endpoint.

### 3. IGFBP4: growth-factor buffering versus compensation

**Question:** is increased Igfbp4 a functional contributor to altered IGF response
in activated Ezh2-deficient Tregs, a protective compensation, or a source/state
marker without a necessary role?

The [2020 IGF study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8078727/), Figures 1
and 4, supports IGF-system expression and shows that induction, maintenance and
viability can respond differently. [2014 IGF-1 experiments](https://pubmed.ncbi.nlm.nih.gov/25339185/)
also report Treg expansion and preserved suppression. These contexts do not
justify a universal direction from Igfbp4 RNA to Treg failure. A
[2018 lymphoid single-cell study](https://pmc.ncbi.nlm.nih.gov/articles/PMC6069633/)
reports Igfbp4/Dapl1 contrasts that further motivate cell-source qualification;
its relevant text was inspected through the indexed primary manuscript, not a
new numerical reanalysis.

First verify locus-specific RNA and IGFBP4 protein from rigorously identified
Tregs under common activation. If confirmed, compare candidate reduction with
matched control in HET and KO cells under defined IGF exposure, measuring IGF
signaling, viable recovery and suppression separately. Improved KO function
would support contribution; worsening would support compensation; absent
protein or no functional change would weaken the mediator claim. Additional
orthogonal specificity checks depend on the chosen perturbation. This is a
measurement-first exploratory branch, not the most validated target.

## Established comparators and consequential contrary findings

DuPage already named Pde3b/Tcf7/Lef1. The [2019 PDE3B study](https://www.jci.org/articles/view/124725),
Figures 5–6, links miR-142 loss, PDE3B, cAMP and suppressive function, including
genetic/pharmacological intervention. A useful Ezh2-specific question would
measure net cAMP and function, particularly because Adcy6 also rises, rather
than rediscover PDE3B's general relevance.

[2019 Tcf1/Lef1 deletion](https://pmc.ncbi.nlm.nih.gov/articles/PMC6446865/)
and [2024 tumor-Treg work](https://pubmed.ncbi.nlm.nih.gov/38169425/) make
"more TCF7/LEF1 always means worse Tregs" an unsuitable general rule. These
serve as context boundaries, not proposed extra datasets or required groups.

IL1R2 is especially instructive: [2024 Tfr deletion](https://pmc.ncbi.nlm.nih.gov/articles/PMC11143922/),
Figure 3, altered germinal-center responses, whereas the
[2025 tumor study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12666320/), genetic
deletion/blockade results and Discussion, found little requirement for the
receptor in its tumor settings despite its marker value. The studies address
different contexts; neither converts our lower Il1r2 RNA into a mechanism.

## Experimental unit, readiness and decision limits

Future experimental units must be independently obtained mice/preparations,
with matched allocation and batch blocking; wells and cells are technical or
nested observations. HET is the source comparator, not ordinary WT. A future
genetic control needs to match the selected perturbation design explicitly.
An early feasible measurement window should separate candidate output from
gross cell loss without pretending the source samples form a time course.

No sample size or meaningful effect margin is invented. Reagent specificity,
lineage reporter availability, model access, assay variation and feasible
precision must be established before a laboratory-ready protocol. None of the
three questions is accepted as a canonical RQ. No new source dataset, biological
replication, experimental validation, or novelty clearance is claimed.

## Portfolio figures and reproducibility

The companion [figure gallery](TARGET_SCREEN_FIGURES.md) presents the entire
screen, focused sensitivity values and proposed comparisons. Figure 4 is
qualitative; no depicted experiment has been executed. Numerical tables remain
the primary evidence, including unfavorable and unannotated entries.

- [V1 full table](../../analysis/research/runs/dupage_target_screen_v1/all_candidates.tsv),
  [frontier](../../analysis/research/runs/dupage_target_screen_v1/review_frontier.tsv),
  [receipt](../../analysis/research/runs/dupage_target_screen_v1/receipt.json).
- [V2 full annotation](../../analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv),
  [coding frontier](../../analysis/research/runs/dupage_target_screen_v2/protein_frontier.tsv),
  [original-frontier audit](../../analysis/research/runs/dupage_target_screen_v2/v1_frontier_audit.tsv),
  [receipt](../../analysis/research/runs/dupage_target_screen_v2/receipt.json).

Validation and search-access details are in [literature context](LITERATURE_CONTEXT.md)
and [target-screen validation](TARGET_SCREEN_VALIDATION.md). The underlying S0–S3 frozen records and all
canonical questions remain unchanged.
