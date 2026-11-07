# IGFBP4: source verification before buffering or compensation

7 November 2026. Exploratory Dp1-P01 subquestion; not an accepted new RQ.
[Follow-up overview](../CANDIDATE_FOLLOWUP.md) · [Source audit](SOURCE_QUALIFICATION.md).

## Published finding → repository observation → remaining question

The DuPage [coding table](../../../analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv)
shows higher Igfbp4 in KO-low than HET-low. Both genotypes have lower expression
in the observed low state than high state: the KO pattern is less downregulation,
not demonstrated activation induction. Chromatin overlap supplies context, not
direct Ezh2 regulation or evidence of intact secreted protein.

[DiToro et al., 2020](https://doi.org/10.1016/j.immuni.2020.03.013), Figures 1–4,
supports context-dependent IGF responses but uses desIGF1 to reduce binding-protein
interference. [Karino et al., 2025](https://doi.org/10.1002/art.43313), Figure 3G–I,
reports Th17-selective expression in its polarization panel and IGFBP4 cleavage.
These are context boundaries, not proof that DuPage's Treg RNA is contamination.
[Miyagawa et al., 2017](https://pubmed.ncbi.nlm.nih.gov/28724578/) also provides an
older IGFBP4/Treg precedent from human MSC-derived factors; its protein source
differs from the proposed Treg-autonomous route (abstract-level access here).

**Question:** is the KO-low Igfbp4 signal produced by Tregs, and does their intact
IGFBP4 alter IGF responsiveness or instead compensate for dysfunction? This is
source/measurement validation followed by a possible context extension. It is
not discovery of IGFBP4 binding IGF or of any IGFBP4–Treg relationship.

## Comparison tuple and estimands

| Element | Prospective specification |
|---|---|
| Population/model | Rigorously identified murine lymphoid Tregs from Ezh2-deficient and matched control preparations; retain a source/purity comparison |
| Stage-one comparison | Genotypes under common activation, with RNA identity, cell-associated protein and supernatant protein assessed separately |
| Stage-two exposure | Candidate-specific reduction versus matched control in a defined native-IGF condition, if source and protein qualify |
| Primary mechanistic endpoint | Receptor-proximal IGF response, with downstream AKT as supportive rather than uniquely IGF-specific evidence |
| Separate functional endpoint | Treg suppressive capacity at matched viable input, alongside absolute recovery; not inferred from Foxp3 frequency or phosphorylation |
| Biological unit | Independent mouse/preparation; paired aliquots nested; source of recipient/responder cells fixed or blocked |
| Timing | Protein/source baseline and early signaling before gross cell loss; later recovery/function distinct; exact windows unresolved |
| Limit | A signaling change does not establish beneficial function, lineage stability, autocrine action or a direct Ezh2 target |

## Hypothesis, alternatives and informative outcomes

The buffering hypothesis predicts that intact Treg-derived IGFBP4 changes the
response to native IGF. Functional direction is not prespecified from RNA alone:
reduced signaling might be harmful, protective or incidental. State composition,
non-Treg protein source, serum carryover and proteolytic processing are leading
alternatives.

| Qualified observation | Interpretation |
|---|---|
| RNA difference lacks Treg-derived intact protein | Does not support a secreted Treg-mediator model; investigate source/processing before perturbation |
| Candidate reduction changes native-IGF signaling, with receptor specificity | Supports IGF modulation in this context; functional consequence remains separate |
| Signaling and suppressive function improve after specific reduction in KO | Supports a harmful contribution, subject to viability and specificity checks |
| Function worsens after reduction | Consistent with protective compensation; retain this result |
| Functional effect persists without an IGF-response effect | Weakens the specified IGF-buffering account; off-target or other actions remain possibilities |
| No effect with adequate perturbation, responsive controls and precision | Weakens necessity for the tested context; an imprecise null is unresolved |

## Staged experimental design

1. Verify locus-specific RNA and protein in lineage-identified cells. Include
   medium/background controls and a source comparison that can expose carryover
   or mixed-cell expression. A total-protein assay alone may not distinguish
   intact binding protein from fragments; qualify its molecular specificity.
2. Qualify native IGF response under defined medium and IL-2 exposure. Keep
   activation history and established-Treg maintenance separate from naive-cell
   Foxp3 induction. [Shapiro et al., 2023](https://doi.org/10.4049/jimmunol.2200651),
   Results on IGF1 plus IL-2, makes cytokine context consequential for expansion.
   A reduced-binding IGF analogue can serve as a bypass/competence comparison,
   but cannot be the sole ligand in an IGFBP4-buffering test.
3. If source and assay qualify, test target-specific reduction within each
   genotype. Measure intact protein, receptor response and recovery, then
   suppression as a distinct outcome. Recipient-cell exposure and residual
   ligand/perturbant carryover must be controlled before assigning a Treg effect.
   Orthogonal specificity or add-back is conditional on a positive effect, not
   a substitute for establishing the protein source.

## Data and readiness decision

The DiToro RNA-seq contrast is sorted Th17, not a validation dataset for mature
Ezh2-deficient Tregs. Karino's polarization assay is also not a matched DuPage
replication. The 2021 TCF1-deficient Treg study is an additional Igfbp4 expression
lead (Figure 4B/Extended Data 5H), inspected only through indexed primary text;
it does not resolve the current protein-source question.

The immediate next step is source and intact-protein qualification, not presumed
benefit from blockade. Reagent selectivity, detection limit, endogenous ligand
context, protease effects, genetic control and biological-unit variance remain
unknown. No intervention direction, sample size or functional effect is claimed
as established by the screen.
