# A20 extension results and hypothesis refinement

30 September 2026 · extension_v1 · exploratory context analysis.
[Figures](FIGURES.md) · [Methods](METHODS.md) · [Source audit](SOURCES.md).

## Priority 1: niche persistence versus altered support activity

In [Ng-Blichfeldt et al. 2019](https://doi.org/10.1152/ajplung.00400.2018),
fibroblasts were pretreated, washed and proliferation-inactivated before co-culture
with fixed epithelial/fibroblast inputs. Reduced organoid formation motivates
an altered-support explanation beyond fibroblast expansion. Survival, residual
exposure, mechanics and secreted activity are not all separated by that design.
The authors did not detect a corresponding differentiation change in their
reported marker comparison; this is not an equivalence test.

The RNA cohort comprises four Munich donors; the organoid cohort comprises eight
Groningen donors. RNA/function measurements are not donor-matched and treatment
durations differ. No RNA-to-function regression or mediation fit is justified.
No inspected source supplies comparable Fzd1/Fzd2 loss with absolute
lineage-linked mature output.

**Refinement:** test receptor-dependent epithelial pool maintenance separately
from instructive maturation. Equal initial inputs strengthen an activity comparison
but do not remove subsequent support-cell loss. Preserve survival, expansion,
functional support and later mature contribution as separate outcomes.

## Priority 2: support and matrix are distinct responses

The new source table contains 32,734 genes and four conditions in every donor.
TMM normalization and panels were frozen before new gene estimates. Values below
are mean donor differences in log2(CPM+1), or means across fixed panel genes,
not literal log2 fold changes or quantities of function.

| Feature | CHIR without TGF | CHIR with TGF | TGF without CHIR | Direct interaction |
|---|---:|---:|---:|---:|
| FZD1 | +1.619 | +1.748 | -0.435 | +0.129 |
| FZD2 | -0.034 | +0.286 | +0.588 | +0.320 |
| Canonical-response panel | +2.455 | +3.082 | -0.726 | +0.628 |
| Selected support-ligand panel | -1.079 | -0.974 | -0.533 | +0.105 |
| Collagen panel | +0.365 | +0.172 | +0.815 | -0.194 |

All four donors show increased canonical-response RNA and reduced support-panel
RNA after CHIR in both contexts. All four show higher FZD2 and collagen-panel
RNA, but lower support-panel RNA, after TGF alone. This challenges expression
surrogates for support; it does not show that functional Fzd2 signaling is
harmful or unnecessary.

Individual genes qualify the averages. TGF alone increases WNT2 (+0.760), whereas
FGF7 (-0.363), FGF10 (-1.872) and HGF (-0.657) decrease on average. CHIR alone
lowers FGF7 and WNT2; the FGF10 mean is near zero and changes sign with total-count
normalization. A positive support-panel interaction does not imply restoration:
the CHIR effect remains negative with TGF. Collagen genes also respond differently;
their panel increase is not uniform elevation of every collagen.

The [Riccetti neonatal study](https://insight.jci.org/articles/view/152404)
offers a separate developmental counterexample to a simple “less matrix means
better repair” model: impaired matrix-related fibroblast function accompanied
reduced epithelial differentiation support. Different cues favored expansion-
associated versus differentiation-associated outcomes. Drug exposure involved
both co-culture compartments, and well/slide units are not independent donors.
This supplies context, not quantitative adult-AF1 replication.

**Refinement:** test whether receptor-dependent support activity and matrix
production/mechanics can respond differently within verified states. RNA panels
cannot establish secreted support or an ECM mediator.

## Priority 3: concurrent input modifies response

The within-donor interaction is:

    [(CHIR + TGF) - TGF] - [CHIR - vehicle]

It is positive for the canonical-response panel in 4/4 donors (+0.628), and
negative for collagen in 4/4 (-0.194). FZD1 and FZD2 interactions each have
three positive and one negative donor. Among adequately detected receptors,
FZD4 has a positive interaction in 4/4 (+1.080), while CHIR lowers its RNA in
both contexts (-1.820 without TGF, -0.739 with TGF). Positive interaction means
a less negative response here, not receptor activation.

FZD3/5/8/9 fail the fixed detection floor. FZD10 is absent from the source table:
unavailable, not assigned zero. The initial mapping gate stopped before gene
estimates; an [amendment](reports/mapping_amendment.json) records proceeding with
44 mapped genes and unchanged complete panels.

Jones GEO/BioSample records confirm one named library per Notch genotype without
resolving animal/pool identities or a matched functional-outcome table. No
cell-level test replaced replicated animals. The
[Jones study](https://pmc.ncbi.nlm.nih.gov/articles/PMC13159043/) remains a
lineage/state comparator; no Fzd2-by-Notch interaction is established.

**Refinement:** retain original H2 as receptor-by-initial-subtype dependence.
The executed comparison concerns simultaneous TGF/CHIR inputs. It cannot be
relabeled as a pre-existing state effect or FZD-selective mechanism.

## Robustness and limits

All four donors were retained. Leave-one-donor mean ranges and total-count-normalized
estimates are deposited for every contrast. Of 240 gene/panel means, 225 retain
direction under alternate normalization, including all 20 panel means. The
15 changes remain in the [sensitivity table](tables/normalization_sensitivity.tsv).
No P values, population intervals or significance categories are used.
Observed donor ranges and omission ranges are descriptive.

There are four biological donors, not 16 independent samples. The TGF/Wnt
interaction is published prior art; this reanalysis does not claim its discovery.
RNA cannot establish secretion, receptor engagement, deposited collagen,
conversion or mature epithelial function.

## Aligned hypothesis and next decision

Map **which receptor is functionally required in which receiving context**.
The original prediction remains open: in verified AF1-like fibroblasts,
comparable Fzd2 loss may reduce functional support more than Fzd1 loss.
The refinement is that dependence may concern maintenance of a competent
epithelial pool and vary with stromal signaling context; higher FZD2 RNA alone
does not identify that competence.

A decisive test requires matched source/recipient identities, receptor-specific
perturbation and engagement, prospectively defined initial state, viable-cell
abundance, independent support/matrix measurements and later lineage-linked
mature output. [Priority decisions](metadata/priority_decisions.tsv) enumerate
these gaps. No new RQ ID, biological acceptance or claim grade is assigned.
