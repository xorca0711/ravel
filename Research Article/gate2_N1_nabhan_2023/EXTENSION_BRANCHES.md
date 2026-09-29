# Nb2 extensions focused on the owner's biological questions

29 September 2026. This proposal is preserved as the pre-extension plan. The owner
subsequently authorized execution; current [results and paper-local candidates](branch_analysis/README.md)
supersede its readiness statements. This document refines the Nb2-N1–N7 cards in the owner's order:
the unnumbered intermittent-dosing question is N1; the six numbered questions
follow as N2–N7. Nb2-N8 remains the separate endogenous-Fzd6-input question.

The organizing question is: **under which starting state, signaling duration and
receptor context does Fzd stimulation produce durable alveolar maturation rather
than persistent remodeling?** This follows the repository's repair-versus-remodeling
purpose. The [current results](RESULTS.md) supply premises and limits, not proof
of any branch below.

## Terms and evidence that change the design

"Hippo activation" and "YAP/TAZ activation" are not interchangeable. Active
MST/LATS kinase signaling generally restrains YAP/TAZ; the source's RNA panel
concerns YAP/TAZ-associated output. Alternative Wnt-to-YAP/TAZ signaling has been
demonstrated in other systems, providing a mechanistic precedent, not proof of
that route in Nb2 AT2 organoids. [Park et al., 2015](https://pubmed.ncbi.nlm.nih.gov/26276632/).

Later results make duration and cellular context central. A human iPSC study
reported AT1 differentiation with YAP/TAZ activation together with AKT inhibition.
A 2026 study instead associated sustained epithelial YAP/TAZ activation with
aberrant transitional/airway states and persistent remodeling in its models.
These are different interventions and contexts; they do not establish that
Fzd agonists behave identically. [Stem Cell Reports, 2024](https://doi.org/10.1016/j.stemcr.2024.02.009);
[Gaona et al., 2026](https://insight.jci.org/articles/view/198113).

This was a targeted literature check, not a systematic novelty review. No claim
is made that every question remained unanswered after the original 2023 paper.

## Nb2-N1: withdrawal, maturation and capacity for another regenerative bout

**Question.** Is a period without agonist administration a biologically effective
off-period, and does it permit mature differentiation while preserving subsequent
regenerative capacity?

**Computational branch.** After the bulk robustness audit, characterize how the
source withdrawal contrasts change canonical-Wnt, proliferation, AT2, transitional
and mature-AT1-associated programs. Compare these with time-anchored regeneration
and persistent-transition references already used in A4/A8. Quantify distinct
programs rather than equating loss of AT2 markers with successful maturation.
The 24/48-hour CHIR-withdrawal libraries provide descriptive leads; they are not
an intermittent Fzd-agonist experiment or a measured sequence within one culture.

**Decisive comparison.** Continuous versus intermittent exposure, with verified
target engagement and subsequent lineage-linked mature output. Prespecify whether
the estimand concerns schedule at comparable cumulative exposure or at comparable
initial expansion; these answer different questions. Track mature descendants
per starting labeled population, survival, remaining AT2 capacity and persistent
abnormal states separately. A calendar off-period cannot be assumed to terminate
receptor signaling.

**What would weaken it?** Only reduced growth or selective cell loss, without
greater mature descendant output, or loss of capacity to respond to a later bout.
**Readiness:** source-based lead analysis possible; sufficiency requires additional
schedule/lineage/function data. **Links:** A4/A8; timing analogy to A14 only.

## Nb2-N2: receptor-associated YAP/TAZ output while retaining AT2 identity

**Question.** Does receptor stimulation create a reversible, differentiation-
competent state, or a persistent stress/transitional state that happens to retain
some AT2 markers?

**Computational branch.** Extend the Fzd5–CHIR and Fzd6–CHIR contrasts beyond the
three resolved source genes with independently defined YAP/TEAD-associated targets.
Keep canonical Wnt/TCF, proliferation, matrix/mechanical stress, TGFbeta-associated
and AT2-identity measurements separate. Test sensitivity to shared genes and
library influence. Compare the response profile with maturation-promoting and
maladaptive perturbation references; do not choose target sets to maximize the
existing Fzd5 difference. Do not statistically remove treatment-induced cycling
and interpret the residual as a causal direct effect.

**Decisive comparison.** Treatment-linked single-cell/protein and later-fate evidence
showing whether AT2 identity and the proposed output coexist in the same cells,
and whether that state yields mature progeny. Resolve YAP versus TAZ only where
the measurements distinguish them; shared RNA targets alone do not.

**What would weaken it?** The extra signature is explained by growth, mechanical
stress or cell mixture, or resembles sustained abnormal transition without later
maturation. **Readiness:** strongest immediate computational branch, with library
independence and Crim2 limitations retained. **Links:** A1/A5/A8/A10.

## Nb2-N3: canonical Wnt effects depend on the starting epithelial state

**Question.** Does an equivalent intervention have different consequences in
quiescent AT2, activated/cycling AT2, transitional epithelium and AT1-like states?

**Computational branch.** Build source-supported state crosswalks using actual
collection times and existing lineage evidence where available. Estimate receptor/
co-receptor availability and canonical-Wnt response within donor/animal and state.
Project a fixed agonist-response signature onto these states as exploratory
similarity, not predicted drug efficacy. Keep productive and persistent transition
as separate outcomes rather than assuming every intermediate lies on a successful
AT2-to-AT1 path. Pseudotime cannot substitute for a treatment experiment.

**Decisive comparison.** Estimate a treatment-by-baseline-state interaction with
replicated starting-state assignments and later endpoints. A state defined after
treatment can itself be an outcome and should not silently be treated as baseline.
Distinguish altered state occupancy from altered expression within a state.

**What would weaken it?** Differences disappear after accounting for measured
exposure/receptor availability or reflect differential survival rather than fate.
**Readiness:** context mapping possible; treatment interaction requires appropriate
perturbation data. Current transitional-IPF coverage is inadequate. **Links:** A1/A4/A8.

## Nb2-N4: genetic loss versus receptor blockade

**Question.** Does adaptation after verified Fzd5 loss explain the phenotypic
discrepancy, rather than incomplete deletion, retained protein or unequal target scope?

**Computational branch.** First audit allele/editing identity, receptor loss, timing,
antibody target spectrum and which measurements belong to the same preparation.
Then compare early versus sustained perturbation responses if eligible data exist:
alternative receptors, downstream regulators, ligand feedback and selection of
unedited cells are distinct explanations. The source's Fzd5 editing score is 65%,
and the comparator antibody targets Fzd5/8; neither difference can be ignored.

**Decisive comparison.** Functional recovery after confirmed loss, accompanied by
a measured alternative mechanism whose contribution can be distinguished from
unedited-cell expansion. Transcriptional adaptation is a known possibility and
can depend on mutant-transcript handling; it is not automatic for every deletion.
[El-Brolosy et al., 2019](https://www.nature.com/articles/s41586-019-1064-z).

**What would weaken it?** Residual activity tracks unedited cells, persistent
receptor protein or the broader blockade target scope. **Readiness:** source/design
audit; no deletion-response RNA is present in GSE208770. Untreated receptor
coexpression cannot demonstrate compensation. **Home:** Nb2, without a duplicate A-series RQ.

## Nb2-N5: ligand, receptor and cellular context as determinants of Wnt output

**Question.** Is diverse output explained by distinct downstream routing, different
activation strength/duration, or a different starting regulatory state?

**Computational branch.** Curate direct perturbation datasets into a comparison
matrix: ligand/input, receptor/co-receptor context, starting state, exposure,
canonical-Wnt readout, YAP/TEAD-associated output and noncanonical functional
readouts where measured. Analyze within-study contrasts before comparing effects
across studies. Separate synthetic Fzd–Lrp agonism from physiological Wnt-ligand
signaling. Receptor RNA and ligand–receptor database links are compatibility
evidence, not demonstrated routing.

**Decisive comparison.** Different inputs within the same cellular context, and
the same input across supported receptor/state contexts. Ask whether downstream
differences persist at comparable measured canonical activation. Expression
signatures alone cannot establish PCP, calcium dynamics, polarity or migration.

**What would weaken it?** A common amplitude/time response adequately accounts
for the apparent differences. **Readiness:** literature/perturbation-resource
curation and receptor-context analyses; definitive routing needs matched response
measurements. **Links:** N2/N3 and A4; A12 is a conceptual context link only.

## Nb2-N6: fibroblast Fzd1 in acute repair and persistent remodeling

**Question.** Does Fzd1 contribute to a fibroblast state that supports epithelial
repair, persistent matrix remodeling, both at different stages, or neither uniquely?

**Computational branch.** Resolve fibroblast subtype and injury stage, then compare
Fzd1 with Fzd2/7 within each animal/donor. Measure epithelial-support programs
and ECM-associated programs separately; do not define beneficial repair by fibroblast
proliferation alone. Test whether associations survive subtype control and occur
in adequately sampled control and injury groups. The current five IPF myofibroblast
samples and one eligible control cannot settle a disease interaction.

**Decisive comparison.** Receptor-specific effects on epithelial maturation/support
and durable matrix outcomes in acute versus persistent settings. The source mixed-
culture growth result does not already establish benefit from Fzd1 stimulation.
**What would weaken uniqueness?** Similar effects for Fzd2/7 or disappearance of
the association after controlling for subtype composition.

Later evidence reinforces these comparators: a 2025 Fzd2 study reports a role
in maintaining an alveolar-fibroblast state that supports epithelial regeneration.
A 2024 broad FZD1/2/5/7/8 agonist study reports repair benefits, but does not isolate
Fzd1's contribution. [Zhou et al., 2025](https://pubmed.ncbi.nlm.nih.gov/41257888/);
[Respiratory Research, 2024](https://doi.org/10.1186/s12931-024-02786-2).

**Readiness:** additional eligible fibroblast cohorts and perturbation evidence
needed for the main claim; current longitudinal mouse profiles permit descriptive
context work. **Links:** A13/A15, with separate support and matrix endpoints.

## Nb2-N7: Fzd4 in capillary progenitors versus general endothelial function

**Question.** Does Fzd4 contribute specifically to gCap renewal or aerocyte production,
or principally to survival, barrier function or other broadly endothelial processes?

**Computational branch.** First validate source CAP1/CAP2 crosswalks to gCap/aerocyte
identities using the original study and species-appropriate markers. Compare Fzd4
and response/co-receptor context within capillary states and against arterial,
venous and lymphatic endothelium. Relate response programs to time-supported repair
states without treating all Fzd4-positive endothelial cells as stem cells.

Gillich et al. established gCap stem/progenitor behavior in alveolar capillary
maintenance and repair; that result alone does not establish a requirement for
Fzd4. [Gillich et al., 2020](https://pubmed.ncbi.nlm.nih.gov/33057196/).

**Decisive comparison.** Verified receptor perturbation linked to gCap self-renewal,
descendant identity and vascular performance, separating altered survival/barrier
integrity from changed regenerative contribution. Broad receptor expression does
not rule out a context-specific function, but it is not evidence for one.
**What would weaken progenitor specificity?** Effects follow general endothelial
survival/barrier changes without a distinct lineage contribution. **Readiness:**
descriptive profiling possible; original lineage/function evidence must be recovered.
**Home:** Nb2 vascular extension.

## Concrete order of computational work

| Order | Deliverable | Decision it supports |
|---|---|---|
| 1 | Bulk library-influence audit and independent YAP/TEAD target-set contract for N2 | Is the receptor-associated component sufficiently stable to pursue? |
| 2 | N3 state/reference eligibility map, linked to A1/A4/A8 and fixed before projection | Does the component resemble maturation, persistent transition or generic stress? |
| 3 | N1 withdrawal-response report with explicit timing/target-engagement gaps | Which maturation question is supported, and which schedule measurements are still needed? |
| 4 | N6 fibroblast and N7 vascular subtype/coverage contracts | Which contextual mechanisms have enough independent units for a useful comparison? |
| 5 | N4 perturbation-identity audit and N5 input/receptor-response evidence matrix | Can a mechanism be distinguished from mismatched perturbation or starting context? |

The first three deliverables form one connected scientific branch; they should
not become three redundant global questions. Paper-specific computations remain
under Nb2, and existing A1/A4/A8 etc. retain ownership of their cross-paper endpoints.

## Reuse the existing A1 resource audit

Gaona's paper lists GSE326359 (human) and GSE327686 (mouse) genomic data. The
repository already records GSE327686 alongside the separate GSE327565 organoid
bulk series. Its [A1 study map](../../RQ_Specified/A1_transitional_epithelial_state_distinction/STUDY_MAP.md)
and [metadata audit](../../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/README.md)
flag conflicting series-level assay descriptions and pooled/single-library limits.
Eight RNA/ATAC GSM do not mean eight independent animals. Reuse those audits;
do not relabel these resources as newly discovered independent validation.
The human deposit remains a candidate until its units and design are checked.

Candidate-specific contrasts, sample eligibility, orthologue mapping, target sets,
uncertainty and falsification criteria must be frozen before the next expression
run. No new expression fitting, dose optimization or biological validation was
performed for this focused roadmap.
