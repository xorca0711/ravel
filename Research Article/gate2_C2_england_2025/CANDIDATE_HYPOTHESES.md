# Eight biological hypotheses motivated by England et al. 2025

**Reframed 28 September 2026. Proposed explanations, not established findings.**
The shared [question register](../../RESEARCH_QUESTIONS.md#england-candidates)
indexes these candidates. E-N1–E-N8 remain paper-local labels; they do not create
A19–A26. Several extend existing questions and should be developed there.

AT2 cells produce surfactant and can replenish damaged alveolar epithelium.
AT1 cells form the thin gas-exchange surface. A **clone** is the descendants of
a labelled cell. Here **wild-type (WT)** means the neighbouring population
without induced oncogenic Kras. Losing an AT2 marker does not by itself mean
that a cell has become a functional AT1 cell.

## Which questions are biological, and which began as technical checks?

“Technical” describes what the original analysis could establish; it does not
mean the observed biology has been proved to be an artefact. For example, a
clone-weighted average describes the typical clone, whereas a cell-weighted
average gives large clones more influence. Both can be correct.

| Candidate | Assessment of original framing | Biological hypothesis in plain language | Where it belongs |
|---|---|---|---|
| [E-N1](#e-n1) | Biology mixed with an averaging check | AT2 identity is lost across many clones, including small clones | Candidate extension of A8/A17/A18 |
| [E-N2](#e-n2) | Biological association | Lungs carrying more mutant cells show a stronger response in neighbouring WT AT2 cells | A18 extension |
| [E-N3](#e-n3) | Mainly a sampling/model check | Differential survival of mutant lineages contributes to the dominance of large clones | Survival alternative within A17; no separate RQ for counting rules |
| [E-N4](#e-n4) | Biology mixed with an expression/composition check | Some mutant epithelial states coordinate several signals that change their surroundings | A2/A9/A11/A12 extension |
| [E-N5](#e-n5) | Mainly a cell-classification check | Mutant hybrid cells start an AT1 programme but fail to complete its maturation component | Biological extension of A1/A8; classifier is a supporting tool |
| [E-N6](#e-n6) | Biological second-hit question mixed with a transfer check | Additional p53 loss gives particular plastic states a lasting growth advantage | Candidate second-hit question; A16 transfer is only preliminary |
| [E-N7](#e-n7) | Biological mechanism | Mutant cells fail to induce the normal feedback that turns NF-kB signalling down during maturation | A1/A12/A14 extension |
| [E-N8](#e-n8) | Biological mechanism | SPP1 and DLK1 activate responses that interfere when both signals are present | A9/A12/A18 extension |

The cards below distinguish the paper's evidence from each proposed extension.
[Technical checks and data gates](CANDIDATE_CHECKS.md) specify what is currently
measurable. The [source audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md)
contains the claim-by-claim assessment and the corrections to A16–A18.

<a id="e-n1"></a>
## E-N1. Is loss of AT2 identity widespread across clones?

**Hypothesis.** Many clones acquire cells with reduced AT2 identity, including
clones that remain small. Expansion of a few large, altered clones accounts for
only part of the tissue-wide change.

**Biological context.** Tissue composition can change through altered cell
identity within clones or unequal expansion of clones. England's Figures 1J,
2H–J and 6A–C motivate that distinction. Figure 4A already reports no detectable
mutant size–composition correlation at two and four weeks. Thus a hypothesis
that only large clones lose identity has contrary source evidence; it should
not be advertised as a new positive finding.

**Prediction and rival.** Identity loss should remain visible among comparable
clone sizes and in summaries that weight each clone equally. If most of the
tissue change disappears when large clones lose their extra weight, unequal
expansion is the stronger explanation. Both contributions can coexist.

**Feasibility.** Mouse-indexed nonspatial measurements permit this descriptive
decomposition after the source counts are reconciled. Separate mutant and WT
analyses. Cross-sectional clones do not trace individual differentiation or
prove mature AT1 function. This extends A8/A17/A18 rather than introducing a
new cell type.

<a id="e-n2"></a>
## E-N2. Does a larger mutant burden evoke a stronger WT response?

**Hypothesis.** Within the same disease stage, lungs with more mutant cells have
greater WT AT2 expansion and more WT cells losing AT2 identity.

**Biological context.** Figures 5–6 establish that mutant tissue changes WT
neighbours. The extension is whether the response scales with mutant burden
across mice, beyond the reported pooled distance profiles.

**Prediction and rival.** Paired mutant and WT measurements from the same mouse
should covary within a time point. Little association, or an association
explained by labelling density or shared injury, weakens the burden-response
explanation. Growth and identity loss may respond differently and must be read
separately.

**Feasibility.** A small descriptive mouse-level analysis is possible after
channel and lobe mapping checks. Three or four mice per time point cannot
support an elaborate adjustment model. A positive association would not show
whether WT expansion helps or restrains tumour growth. This belongs under A18.

<a id="e-n3"></a>
## E-N3. Does survival help determine which mutant lineages dominate?

**Hypothesis.** Preferential survival of some mutant lineages contributes to
their later dominance, alongside differences in cell division.

**Biological context.** The source shows apoptosis in small remote mutant clones
(Figure S3). Methods S1 also analyses expanded clones. A lineage that disappears
cannot contribute to a later size distribution; one that stays as a single cell
may be excluded by the analysis. Counting only expanded survivors changes what
a fitted population fraction means.

**Prediction and rival.** Models allowing differential loss may reproduce the
observed tail without the same initial frequency of fast-dividing founders.
Independent lineage survival measurements would distinguish this from a
division-rate explanation. Similar fits to surviving clones alone may leave
both explanations possible.

**Feasibility.** The feasible work is an A17 identifiability and sampling check.
It can show that several biological explanations fit; it cannot establish
selective survival from repeated cross-sectional samples. The denominator
correction is a technical result and does not deserve its own biological RQ.

<a id="e-n4"></a>
## E-N4. Do mutant cells coordinate several signals to their neighbours?

**Hypothesis.** Some mutant epithelial states coordinate multiple signalling
outputs, creating a distinct capacity to change neighbouring cells.

**Biological context.** Figure S7F highlights EGFR ligands and Figure S6
implicates SPP1/DLK1. A coordinated source-cell programme would differ from a
tissue in which separate populations supply separate signals.

**Prediction and rival.** The candidate signals should vary together among
comparable cells within a state, beyond sequencing depth or the abundance of
that state. If they occur in different populations, a division of labour among
cells is more plausible than one common source-cell programme.

**Feasibility.** Existing counts support an exploratory co-expression test
within libraries. RNA does not measure secretion or recipient activation;
those remain necessary for the biological mechanism. This extends
A2/A9/A11/A12, with the expression check serving as a screening step.

<a id="e-n5"></a>
## E-N5. Which part of AT1 maturation remains incomplete in mutant cells?

**Hypothesis.** Mutant hybrid cells activate early AT1-associated features but
fail to acquire a late maturation programme found during productive repair.

**Biological context.** Mixed identity and impaired completion are already part
of the source's model (Figures 3, 4 and 7). The extension is to identify the
missing maturation component and connect it to an independent mature endpoint.
Finding a better threshold for an RNA label alone would not answer that question.

**Prediction and rival.** Early and late AT1 features should separate in mutant
cells, while late features should associate with independently measured mature
phenotypes in repair. If the difference disappears with comparable sequencing
depth, independent annotation or matched sampling, a classification/context
effect is the stronger explanation.

**Feasibility.** Existing England, Choi and Niethamer data permit an RNA pilot
with held-out evaluation. Functional maturation remains unmeasured by that
pilot. Keep the biology in A1/A8 and the classifier as supporting work; do not
turn a new cell label into a new biological finding.

<a id="e-n6"></a>
## E-N6. Does p53 loss make particular plastic states more competitive?

**Hypothesis.** Additional loss of p53 gives particular plastic epithelial states
a lasting growth advantage, changing the broadly comparable proliferative
potential reported in the Kras-only model.

**Biological context.** England's Discussion raises additional drivers as a
possible explanation for differences from Kras/Trp53 studies. This is a
source-motivated hypothesis, not a novel mechanism established by this review.

**Prediction and rival.** In comparable genetic backgrounds and conditions,
the additional change should alter the long-term contribution of particular
states. Differences confined to unmatched culture systems, stages or capture
methods would not establish a p53 effect.

**Feasibility.** Public candidate datasets allow metadata review and possibly
descriptive transfer of CD177-associated RNA. A matched genetic comparison and
lineage-linked growth outcomes are needed for the full hypothesis. A16's
marker-transfer test addresses only a small part of this question.

<a id="e-n7"></a>
## E-N7. Why does the normal NF-kB shutoff programme fail in mutant cells?

**Hypothesis.** Mutant reprogramming impairs induction of the normal feedback
programme that reduces NF-kB activity as cells mature.

**Biological context.** Figure 7 and Figure S7 connect sustained signalling to
mutant states and show effects of NF-kB inhibition. The paper leaves the control
of endogenous feedback-regulator induction unresolved. A brake can fail because
it is not induced, or because continuing stimulation overwhelms an intact brake.

**Prediction and rival.** The hypothesis predicts weaker feedback induction
under comparable pathway stimulation, followed by persistent activity and
incomplete maturation. Normal induction with excessive ongoing stimulation
would favour the alternative. A single Nfkbia RNA measurement cannot separate
them.

**Feasibility.** Current data nominate associated RNA features. Linked
measurements of activity, feedback response and later maturation are needed to
distinguish mechanisms. This belongs with A1/A12/A14; marker changes after
inhibition are not evidence of durable functional repair in vivo.

<a id="e-n8"></a>
## E-N8. Do SPP1 and DLK1 interfere with each other's WT growth response?

**Hypothesis.** SPP1 and DLK1 activate recipient responses that interfere when
both are present, reducing WT expansion relative to either signal alone.

**Biological context.** Figure S6Q–S shows increased WT organoid output with
either ligand and a smaller organoid-size effect with the combination. This
motivates interference, but does not establish it. Saturation, altered survival
or a change in organoid shape could also affect the measured size.

**Prediction and rival.** A combined response below a prespecified
non-interacting expectation, with appropriate recipient and viability evidence,
would support interference. An outcome explained by saturation or changes in
cell number/shape would favour those alternatives. Formation, size and
maturation are separate outcomes.

**Feasibility.** Existing figures provide descriptive motivation. Suitable
factorial data and recipient measurements are needed for mechanism; necessity
in vivo requires separate evidence. The Areg public-data series is not such a
test. This is a bounded extension of A9/A12/A18.

## Practical priority

First repair A16's population comparison and specify A17's model and source
accounting. E-N1 and E-N2 then offer bounded uses of the existing mouse hierarchy.
E-N3 supports A17. E-N4 and E-N5 are RNA pilots within existing questions. E-N6
needs an eligibility review; E-N7 and E-N8 need additional mechanistic data.
No literature-wide novelty or new claim grade is asserted.

Source throughout: [England et al., Cell Stem Cell (2025)](https://doi.org/10.1016/j.stem.2025.01.011),
main article and supplements. Figure references identify the source motivation;
the hypotheses and decision rules above are proposed extensions.
