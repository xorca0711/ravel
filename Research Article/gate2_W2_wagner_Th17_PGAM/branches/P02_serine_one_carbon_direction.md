# Wp-P02 — Does the 3PG serine arm run with or against the regulatory program?

**Current evidence:** [7 October corrections](../CORRECTIONS_2026-10-07.md) supersede the older Compass sign and human-score summaries cited below. Retain source-paper premises separately from the corrected repository results; the source study and its reanalysis are not independent replication.

**Status:** proposed, outcome-exposed. Model discrimination between two published
directions. This is the highest-information candidate in the package.

**Scope note, 4 October 2026.** The owner's Discussion note marks the open
question as the connection between *serine biosynthesis, cellular stress
(TGF-β) and Th17 pathogenicity* — the same three-way question the source's own
Discussion closes on. This card originally covered only the serine arm. The
stress and TGF-β leg is added below as a **separate, weaker arm**, because its
cited support does not survive an abstract-level check; see
[note reconciliation](../NOTE_RECONCILIATION.md#source-checks-on-the-notes-content).

## The conflict

Both statements are published, and they point opposite ways.

- **This paper.** Compass predicted that the serine shunt leaving
  3-phosphoglycerate correlates *negatively* with the pathogenicity score, i.e.
  positively with the pro-regulatory Th17n phenotype, and the Discussion proposes
  that PGAM's effect "may also be mediated through serine biosynthesis" (main
  text pp. 4 and 10).
- **[Godfrey et al., *eLife* 2025](https://doi.org/10.7554/eLife.104423)
  (PMID 40720256).** PGAM is overexpressed in Tregs; pharmacological or genetic
  PGAM inhibition reduces Treg differentiation and suppressive function while
  inducing markers of a Th17-like state — and that effect *requires* the
  contribution of 3PG to de novo serine synthesis. Blocking serine synthesis from
  3PG reverses it, exogenous serine inhibits Treg polarisation, and the mechanism
  runs through one-carbon metabolism and methylation of Treg-associated genes.

The phenotypes agree: less PGAM, less regulatory character. The *mechanism's
direction* does not. In this paper's model, PGAM inhibition should raise 3PG and
therefore raise serine-shunt availability — which Compass associates with the
regulatory phenotype. In Godfrey's model, raised 3PG-derived serine is precisely
what *suppresses* the regulatory program. One of these cannot be the explanation
for the other's phenotype.

## Proposition, stated so it can fail

Within Th17n cells, serine-synthesis and one-carbon transcript abundance is
associated with the *pro-inflammatory* arm of the pathogenicity score and with
the EGCG-response direction, as Godfrey's mechanism predicts, rather than with
the pro-regulatory arm as the Compass serine-shunt correlation implies. If the
association instead follows the pro-regulatory arm, the Compass direction is
supported at RNA level and Godfrey's mechanism does not extend to this
compartment.

## Strongest rivals

1. **Biosynthetic demand.** Serine-pathway transcripts track proliferation and
   biomass demand. Cells differ in cycle phase by condition, and phase was
   regressed out of the published latent space — so a positive association with
   the inflammatory arm may be a growth association.
2. **RNA is not flux.** Neither direction is measurable from transcript
   abundance. Compass "potential activity" and a serine-pathway RNA module are
   both network- or list-derived summaries of the same transcriptome.
3. **Compartment difference.** Godfrey worked in Tregs (TGF-β/IL-2) and this
   paper in Th17n (TGF-β/IL-6). Both can be right in their own compartment, which
   is itself a finding worth stating rather than a failure of the test.

## What would distinguish them

**In deposited data (Wp-R1/R3 products, descriptive):** the sign and magnitude of
the association between a frozen serine-synthesis/one-carbon module
(*Phgdh, Psat1, Psph, Shmt1, Shmt2, Mthfd1, Mthfd2, Mthfd1l, Mtr, Mat2a, Ahcy,
Dnmt1, Dnmt3a*) and (a) each score arm separately, (b) the EGCG-response
signature, (c) membership of the N1 program — each computed within library and
within glucose condition, with cell-cycle phase and detected-gene count as
declared covariates. Report per-cell distributions, not condition means.

**The decisive experiment (not available here).** Th17n differentiation with
PGAM inhibition alone, PHGDH inhibition alone (for example NCT-503), and both
together, reading out Foxp3 and IL-17 protein plus 13C serine/glycine labelling
from [U-13C]glucose, with the mouse as the unit. Godfrey's model predicts PHGDH
inhibition *reverses* the PGAM-inhibition phenotype; the Compass reading predicts
it does not, or deepens it. One two-by-two factorial with a labelling arm
separates them, and it is a culture experiment, not an animal study.

## The second arm: cellular stress and TGF-β

The source proposes a molecular link — PGAM is said to be essential for TGF-β
signalling in cancer cells, and glycolysis blockade with 2-DG is said to promote
Th17 effector function by activating cellular-stress TGF-β signalling networks —
and concludes that the PGAM, serine, stress and pathogenicity connection needs
further study. Before that chain is used as a premise, two things must be true,
and at abstract level neither is established:

1. The stress study cited for the 2-DG effect reports that cell stress supports
   Th17 differentiation **in the absence of** TGF-β signalling, which is not the
   same claim as TGF-β networks being activated.
2. The reference cited for PGAM's role in TGF-β signalling is an allosteric
   PGAM1-inhibitor study in non-small-cell lung cancer whose abstract does not
   mention TGF-β.

Neither full text was read in this pass, so this is a **flag, not a refutation**.
The consequence for the design is concrete: the stress arm cannot be entered as
an assumed mechanism. The cheap first step is to read both full texts and record
what each actually measured; only then is a stress readout worth adding. If it
is, the measurable form in deposited data is an integrated-stress-response and
TGF-β-target module (for example *Atf4, Ddit3, Trib3, Sesn2, Eif4ebp1* against
*Smad7, Skil, Serpine1, Tgfb1*) scored per cell within library and compared
across the glucose arms, where the low-glucose condition is itself a nutrient
stressor. That is an association, and it cannot separate stress-driven TGF-β
signalling from TGF-β-independent stress effects — which is precisely why the
decisive version is a perturbation with a signalling readout (phospho-SMAD2/3 or
a TGF-β reporter) rather than another transcript module.

## Decision this would inform

Whether PGAM is a candidate target because of what it *removes* (2PG and
downstream glycolysis) or because of what it *diverts* (3PG into serine and
one-carbon metabolism). Those two readings imply different companion targets,
different tissue dependencies — serine is dietary and tissue-variable — and
different off-target risks.

## Unit, endpoint, limit

Unit: cells within library for the RNA analysis, so the outcome is descriptive;
mouse for the proposed experiment. Endpoint: signed association of the frozen
serine module with each score arm and with the EGCG signature. Limit: an RNA
association cannot establish flux direction and cannot adjudicate the mechanism
on its own. What it *can* do is show whether the two published directions are
even compatible with the same transcriptomes — and that is enough to decide
whether the wet experiment is worth running.

## Stop condition

Freeze the module gene list, the covariates and the within-library design before
looking at any association. The stress arm does not open at all until the two
cited full texts are read and what they measured is recorded; a stress module
scored first and justified afterwards is exactly the move this card refuses. If the association is inconsistent in sign across
libraries, report it as inconclusive and stop; do not add conditions, change the
module or pool libraries until a sign appears.

## Evidence added 4 October 2026

[Wp-R3](../R3_RESULTS.md) supplies the transcript-level half of this card from the
authors' own bulk libraries: every measured serine-synthesis and one-carbon gene
falls under EGCG in both cultures (PHGDH -0.46 in Th17n and -0.65 in Th17p, SHMT2
-0.51 and -0.73, PSAT1, SHMT1, MTHFD2, all BH <= 0.05 where marked), and falls
under DHEA as well. PGAM inhibition is expected to *raise* 3-phosphoglycerate, so
a coordinated transcriptional decrease is compatible with feedback to substrate
excess or with a genuinely reduced pathway, and it does not discriminate between
this paper's serine-shunt sign and the opposite direction reported for Tregs by
Godfrey et al. 2025. The discriminating measurement named on this card is
unchanged: labelled serine and formate flux under PGAM inhibition, not expression.

## Stress-arm prerequisite discharged, 5 October 2026

The card held the stress and TGF-β arm closed until the two cited texts were read
and what each actually measured was recorded. That step is now done, and the
flag raised at abstract level is **confirmed for the first citation and
unresolved for the second**.

**1. Brucklacher-Waldert et al. 2017, *Cell Reports* 19:2357 (PMID 28614720),
full text read.** Its title is "Cellular Stress in the Context of an Inflammatory
Environment Supports **TGF-β-Independent** T Helper-17 Differentiation". The
paper's own highlights state that cellular stress "can substitute for TGF-β in
Th17 cell differentiation", and the stress inducers are tested explicitly against
neutralising anti-TGF-β. On glycolysis specifically, 2-deoxyglucose and the
GAPDH inhibitor 3-bromopyruvate both *enhance* Th17 polarisation, and the
mechanism the paper advances is sustained cytoplasmic calcium with a partial
contribution from XBP1 — not activation of TGF-β signalling. So the chain "2-DG
promotes Th17 effector function by activating cellular-stress TGF-β signalling
networks" inverts this source's claim: stress substitutes for TGF-β rather than
activating it.

**2. Huang et al. 2019, *Cell Metabolism* 30:1107 (PMID 31607564), full text not
obtained** — the article is not open access and no legitimate route returned the
text. From the abstract, the allosteric PGAM1 inhibitor HKB99 acts through the
PGAM1-ACTA2 interaction and shifts JNK/c-Jun, AKT and ERK signalling with raised
oxidative stress, in non-small-cell lung cancer. TGF-β does not appear. This
remains a **flag, not a refutation**: a TGF-β result could sit in the body of the
paper. Resolving it needs the PDF, which the owner can supply.

**Consequence for the design, unchanged in substance but now evidenced.** The
stress arm cannot be entered as an assumed mechanism, and the specific premise
the source's Discussion rests on — stress acting *through* TGF-β networks — is
contradicted by the one text that can be read in full. The integrated-stress and
TGF-β-target module scored across the glucose arms remains available as an
association, but the decisive version is still a perturbation with a signalling
readout (phospho-SMAD2/3 or a TGF-β reporter), and the low-glucose arm of this
deposit is itself a nutrient stressor, which makes the association confounded by
design.

## RNA arm: answered as far as deposited data allow, 5 October 2026

Two executed stages have now delivered the transcript- and reaction-level
evidence this card specified, and they agree with each other and with the
paper's sign: [Wp-R3](../R3_RESULTS.md) shows every serine-synthesis and
one-carbon transcript falling under EGCG in both cultures, and
[Wp-R2](../R2_RESULTS.md) shows the 3PG-to-serine reactions (PGCD, PSERT, PSP_L,
rho -0.26) associating negatively with the pathogenicity score, i.e. with the
pro-regulatory side, alongside PGAM itself at -0.29.

That is the Compass direction, not Godfrey's. It does **not** resolve the
conflict, for the reason the card already gave: reaction scores and transcript
modules are two summaries of the same transcriptome, and PGAM inhibition is
expected to *raise* 3-phosphoglycerate, so a coordinated transcriptional
decrease is equally compatible with feedback to substrate excess. A further
per-cell module score would restate the same evidence a third time and is
therefore **not worth running**; the card's RNA arm is closed as
uninformative-for-discrimination rather than unexecuted. The decisive
measurement is unchanged and is now the single highest-value open step in this
package: the PGAM x PHGDH-inhibitor two-by-two in Th17n culture with Foxp3 and
IL-17 protein readout and 13C serine/glycine labelling from [U-13C]glucose.

## Stress arm modulated and the E3 evidence recorded, 5 October 2026

The stress arm is modulated rather than opened as the card originally framed it.
Three changes, each with its basis.

### 1. The card's own stress readout is retired as confounded

The card proposed, conditionally, an integrated-stress-response and
TGF-β-target module "scored per cell within library and compared **across the
glucose arms**", and conceded in the same sentence that the low-glucose
condition is itself a nutrient stressor, so the association would be confounded
by design. That readout is withdrawn. It cannot distinguish a stress response to
PGAM inhibition from a stress response to glucose withdrawal, which is the only
contrast it looks at.

### 2. It is replaced by the drug-arm readout already executed

[Wp-E3](../E3_RESULTS.md) scored a declared ISR set across the **drug** arms of
the bulk deposit, against a null matched on expression decile. That contrast
carries no nutrient-stress confound, because glucose is held at the culture
concentration in every library it compares. In Th17n division-1 libraries under
EGCG:

| Stress axis | Genes | Centred median | Expression-matched null p |
|---|---|---|---|
| Integrated stress response | 13 | **−0.491** | 0.000 |
| Unfolded protein response (incl. *XBP1*) | 13 | +0.063 | 0.121 |
| NRF2 oxidative stress | 13 | −0.069 | 0.419 |
| Heat shock | 56 | +0.025 | 0.372 |

All four axes either fall or do not move. The UPR row bears directly on the
citation chain examined above: Brucklacher-Waldert's mechanism was sustained
cytoplasmic calcium with a partial XBP1 contribution, and *XBP1* sits in that
flat set.

### 3. The overlap limitation is discharged

The Wp-E3 contract disclosed that its stress and serine sets share members —
ATF4 targets that are also serine enzymes — without resolving it. Because this
card now depends on which genes carry the stress shift,
[a sensitivity was frozen and executed](../../../analysis/research/runs/wp_e3_isr_sensitivity_v1/results.json)
under its own contract, with the stop rule written before any reduced-set value
existed: if the shift did not survive removal of the shared genes, the ISR
observation would not enter this card.

The shared genes are *MTHFD2* and *SHMT2*, computed from the Wp-E3 membership
table rather than assumed. Removing them:

| Variant | Genes | Centred median | Null p |
|---|---|---|---|
| ISR, as Wp-E3 scored it | 13 | −0.491 | 0.000 |
| **ISR minus shared** | 11 | **−0.491** | 0.000 |
| Serine/one-carbon, as scored | 13 | −0.299 | 0.000 |
| Serine/one-carbon minus shared | 11 | −0.262 | 0.004 |
| Shared genes alone | 2 | −0.474 | 0.034 |

The ISR median is unchanged to four decimals, because it falls on *EIF4EBP1*
whether the two shared genes are present or not. The stop rule is therefore not
triggered: the stress shift is not an artefact of double-counting serine genes,
and the serine decrease is not an artefact of counting ATF4 targets. The run
asserts that its full-set recomputation reproduces Wp-E3 exactly, which it does
(worst absolute difference 0.0).

### What the ISR set actually does, gene by gene

The median conceals real heterogeneity, and the card records it rather than the
summary alone. In Th17n + EGCG the canonical ATF4 output falls hard — *CHAC1*
−2.03, *TRIB3* −1.75, *NUPR1* −1.28, *DDIT3* −1.11, *ASNS* −0.87 — while *ATF4*
itself barely moves (−0.19, adjusted p 0.77), which is what a translationally
regulated transcription factor should do. Two members move the other way, and
one of them is among the most significant genes in the set: *SESN2* +1.53
(adjusted p 0.0004) and *ATF3* +0.21. So the set is not moving as one block, and
the correct statement is that ATF4 *output* falls while two stress-inducible
genes rise.

### The arm asymmetry

The ISR is **−0.491 under EGCG and +0.412 under DHEA** in the same Th17n
division-1 libraries (both null p ≤ 0.001, after removing the shared genes).
The paper reads EGCG and DHEA as two routes to one pathogenic state; at the
level of ATF4 output they move in opposite directions. Whatever the two
inhibitors share, it is not a common stress response.

### Consequence for the decisive experiment

The experiment named on this card is unchanged — PGAM × PHGDH inhibition
two-by-two in Th17n with Foxp3 and IL-17 protein and ¹³C serine/glycine
labelling from [U-¹³C]glucose, mouse as the unit. What changes is the status of
one readout on it. The card previously held a stress readout as worth adding
only if the cited texts supported the premise; they do not, and the authors'
own libraries move ATF4 output the wrong way. A phospho-eIF2α and ATF4 protein
panel therefore moves from an optional addition to a **falsifiable prediction
with a stated direction**: if PGAM inhibition raises pathogenicity through
cellular stress, ATF4 output should rise under EGCG in Th17n; the deposited
transcriptome predicts it will not. On arms the experiment already runs, this is
one blot or one flow panel.

### What none of this does

It does not touch the paper's phenotype. PGAM inhibition raising Th17
pathogenicity, and the adoptive-transfer EAE result, are reproduced as far as
the deposits allow ([Wp-R1](../R1_RESULTS.md), [Wp-R3](../R3_RESULTS.md)); the
evidence here bears on the Discussion's proposed *mechanism*, not on that
phenotype.

It does not resolve the Compass-versus-Godfrey conflict, and it does not reopen
the RNA arm. Wp-E3 and this sensitivity are further summaries of the same
transcriptome that closed that arm, and the limits stated there hold here:
library-level bulk TPM with no animal field, so descriptive only; and transcript
abundance of ISR target genes is a downstream proxy for a response set by
eIF2α phosphorylation and ATF4 translation, so no value above measures
stress-response activity. The evidence lowers the prior on the stress
explanation. It does not settle it, and only the perturbation with a protein
readout can.
