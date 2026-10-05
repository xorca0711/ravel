# Overlap of the three Wp candidates against the 28 registered questions

Compiled 5 October 2026 against `RESEARCH_QUESTIONS.md` at branch revision
`924999dca7bad11b9da6feddadc87dfc6a312db7`, which carries A0 to A27.

**What this screen does.** It compares each candidate to each registered
question on the five attributes the repository uses to keep questions distinct:
population, tissue or model, perturbation or exposure, measured endpoint and
biological unit. A candidate is reported as **covered** when a registered
question would answer it, and as **distinct** when it would not — regardless of
whether the two share vocabulary. The screen records no retain or reject
decision and certifies no novelty.

**Result.** No candidate is covered. The three nearest neighbours by reasoning
pattern, rather than by biology, are A1, A6/A22 and A27; each is examined
individually below because a shared reasoning pattern is the way an overlap is
most easily missed.

## The structural separation

Every one of A0 to A25 is a **lung, bladder or brain tissue question** about
epithelium, fibroblasts, macrophages, capillaries, urothelium or microglia.
A26 and A27 are **murine T-cell ageing** questions about TCR repertoire
concentration across lymphoid organs. The three candidates here are about
**CD4 T helper 17 differentiation under metabolic perturbation in culture, and
the same programmes in human CSF**. No registered question involves T helper
polarisation, a cytokine-driven differentiation condition, glycolytic
inhibition, or cerebrospinal fluid.

That separation is necessary but not sufficient, because the repository's own
rule is that shared mixture reasoning or a shared word must not collapse
distinct biology — and the converse also holds: a different tissue does not by
itself make a distinct question. The individual comparisons are therefore made
on the reasoning, not the tissue.

## Candidate-by-question screen

| Registered | Its population / endpoint | Nearest candidate | Verdict and reason |
|---|---|---|---|
| A0 | Cross-tissue epithelial transition programme; mature intestinal endpoint | Wp-Q1 | Distinct. A0 asks whether one programme transfers across tissues; Wp-Q1 asks whether two arms of one score move independently within one cell type. A0's pilot failed on an epithelial endpoint that does not exist here. |
| A1 | Lung transitional epithelial states; regulatory marks, lineage, CD44 context | Wp-Q1 | **Nearest in reasoning, still distinct.** Both ask whether RNA-similar states are functionally separable. A1's discriminator is chromatin and lineage history in lung epithelium; Wp-Q1's is a joint protein distribution in cytokine-polarised CD4 T cells. Neither test informs the other, and A1's missing feature (matched replicated regulatory/fate linkage) is not what Wp-Q1 needs. |
| A2, A9 | Fibroblast response to AREG; delivery versus abundance, receptor context | Wp-Q1 | Distinct. Ligand delivery and recipient competence in fibroblasts; no module-arm or T-cell content. |
| A3, A6 | Macrophage programmes: injury history, and IPF within-state versus mixture | Wp-Q1, Wp-Q3 | **A6 is the nearest reasoning neighbour for composition.** A6 asks whether IPF changes macrophage states beyond abundance — the same within-state-versus-mixture form that Wp-P03 applied to the mouse glucose effect and that Wp-Q3 names as a rival. Distinct because the population, perturbation and endpoint all differ, and because for the candidates the composition question is a *rival to defeat*, not the question asked. |
| A4 | AT2 lineage: Wnt maintenance preceding IL-1 response | Wp-Q1 | Distinct. Temporal ordering in an epithelial lineage with lineage tracing; no T-cell or metabolic content. |
| A5 | Developmental programme reuse in adult alveolar repair | — | Distinct on every attribute. |
| A7 | Cebpa loss: across states versus within a transitional state | Wp-Q1 | Distinct. Genotype-by-state interaction in AT2 identity. Shares only the across-versus-within form, which is a statistical shape, not a biological question. |
| A8, A11 | Maturation component for AT1 output; lesion programmes beyond shared plasticity | — | Distinct. Both are added-information questions about epithelial programmes. |
| A10 | Epithelial programmes and measured organoid growth | Wp-Q2 | Distinct, and worth stating because both touch growth. A10 asks whether programmes predict an organoid growth outcome; Wp-Q2 asks whether slowing growth *causes* effector output in T cells. Opposite direction, different population, different unit. |
| A12, A13, A15 | IL-1 recipient context; fibroblast programmes beyond macrophage IL1B; integrin versus ligand | — | Distinct. Lung niche signalling; no overlap with glycolysis or T-helper polarisation. |
| A14 | Exposure duration and fibroblast IL-1 reception in recovery after withdrawal | Wp-Q2 | Distinct. A14's two hypotheses concern withdrawal and recovery in an epithelial-fibroblast system with separate control requirements; Wp-Q2 has no withdrawal arm. |
| A16, A17, A18 | Mutant clone priming, founder effects, WT expansion near clones | — | Distinct. Clonal epithelial genetics. |
| A19, A20, A21 | Fzd signalling: response reversibility, AF1 support, capillary integrity | — | Distinct. |
| A22 | NKX2-1 identity versus epithelial amount for fibroblast chemokine competence | Wp-Q1 | **Nearest reasoning neighbour for identity-versus-amount.** A22 separates a cell's identity from how much of it there is. Wp-Q1 separates two programmes within one cell. Distinct: A22's unit is the fibroblast response to an epithelial source; Wp-Q1's is the T cell's own joint protein state. |
| A23 | SLC34A2 phosphate homeostasis constraining entry into a transition state | Wp-Q2 | Distinct, and the closest *metabolic* question in the register. A23 concerns a transporter and mineral homeostasis in lung epithelium, with entry-versus-exit timing as its contrast. Wp-Q2 concerns glycolytic restriction and biosynthetic demand in T cells. Neither a shared word (metabolism) nor a shared shape (entry into a state) makes them one question. |
| A24 | Bladder stromal ageing and urothelial barrier maintenance | — | Distinct. |
| A25 | Regional microglial configuration in middle age | — | Distinct. |
| A26 | CD8 repertoire concentration: spleen versus marrow within comparable states | Wp-Q3 | Distinct, and the nearest *compartment* question. A26 contrasts two lymphoid organs for TCR repertoire concentration during ageing, with the animal as unit. Wp-Q3 contrasts CSF against paired blood for module expression in human disease, with the donor as unit. Repertoire concentration and module expression are different endpoints, and the word "compartment" does not join them. |
| A27 | Spleen CD8: state redistribution versus within-state change | Wp-Q3 | **Nearest reasoning neighbour overall.** A27 is exactly a redistribution-versus-within-state attribution, which is the decomposition Wp-Q3 proposes for its paired difference. Distinct on every measured attribute: murine spleen TCR clones during ageing against human CSF-versus-blood module expression in autoimmunity. The shared method does not make a shared question, and Wp-Q3's primary contrast is activation adjustment, not the decomposition. |

## Candidate-to-candidate separation

The three must also be distinct from each other, because all three read the
same score construction.

- **Wp-Q1 against Wp-Q3.** Q1 asks whether the two arms are separately
  regulated as a property of the cell, tested in mouse culture under two
  perturbation classes with a joint protein readout. Q3 asks whether one arm's
  elevation in one human compartment survives activation adjustment. Q1's
  answer does not settle Q3: separately regulated arms could still move in CSF
  purely through activation. Q3's answer does not settle Q1 either, because a
  compartment contrast is not a perturbation class.
- **Wp-Q1 against Wp-Q2.** Q1 is about which arm moves; Q2 is about why the
  effector programme rises under one specific inhibitor. Q2's effector gain is
  measured against an expression-matched null on bulk libraries and is not an
  arm contrast at all.
- **Wp-Q2 against Wp-P02.** The branch card asks whether the 3PG-to-serine arm
  runs with or against the regulatory programme, and its decisive measurement
  is ¹³C labelling with PHGDH inhibition. Q2 asks whether the effector gain
  needs PGAM at all, and its decisive factor is growth slowing by an unrelated
  route. They share cultures, not a question; Wp-P02 stays a branch card and is
  not proposed for registration.

## Honest limits of this screen

It compares written questions, not the full content of every linked result, and
it was compiled by the same agent that wrote the candidates — which is the
condition under which an overlap is most likely to be rationalised away rather
than found. Three nearest neighbours are therefore named explicitly above
(A1, A6/A22, A27) so a reviewer can go straight to the comparisons most worth
challenging. Absence of a registered match is not evidence of novelty, and no
part of this file records a human decision.
