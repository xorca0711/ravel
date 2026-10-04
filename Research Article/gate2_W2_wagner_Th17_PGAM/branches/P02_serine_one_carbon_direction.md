# Wp-P02 — Does the 3PG serine arm run with or against the regulatory program?

**Status:** proposed, outcome-exposed. Model discrimination between two published
directions. This is the highest-information candidate in the package.

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
looking at any association. If the association is inconsistent in sign across
libraries, report it as inconclusive and stop; do not add conditions, change the
module or pool libraries until a sign appears.
