# Executed Nb2 branch analysis

29 September 2026. Exploratory extension after exposure to the paper, owner notes
and previous Nb2 results. **No branch is biologically validated.** The computations
sharpen the questions and identify the comparisons the available data cannot make.
Stable results below mean stability within the stated data and checks.

## N1: withdrawal supplies a maturation-associated lead, not a dosing answer

In GSE208770, the six-gene AT1-associated score is lower at 24 than 48 hours after
CHIR withdrawal: mean difference **−1.863 log2CPM units**, conditional 95% interval
−5.450 to +1.723. Every single-library omission retains the direction (−2.322 to
−1.027), as do the nine leave-one-per-arm comparisons. The Wnt-clean and cycling
directions change under omissions. This is not a demonstrated, coordinated
Wnt-off/cycle-off/maturation sequence. The cultures are not linked serially, and
source treatment timing remains unreconciled.

Fzd5 and Fzd6 have higher AT1-associated scores than CHIR (+2.176 and +1.625),
but lower point estimates than withdrawal48 (−0.258 and −0.808). Thus the apparent
advantage depends on the comparator. AT1-associated RNA is not mature gas-exchange
function, and there are no Fzd pulse/washout or second-bout data. [N1](candidate_questions/Nb2-N1.md).

## N2: the source YAP-associated component does not establish a common broad state

The resolved three-gene source panel is higher for Fzd5−CHIR (**+1.870**, single
omission range +1.535 to +2.173) and Fzd6−CHIR (**+1.313**, +0.977 to +1.797).
Leave-one-per-arm ranges also retain these directions. Conditional 95% intervals
are +0.325 to +3.415 and −0.430 to +3.056, respectively. The first-pass genome-wide
gene FDRs remain nonsignificant; these exploratory score intervals are not
multiplicity-adjusted gene discoveries. Printed **Crim2** remains unresolved.

We independently fitted [Gaona et al. 2026, GSE327565](https://insight.jci.org/articles/view/198113)
within each culture medium: 3 versus 3 source-reported mice in SFFFM and 4 versus
4 in ADM, 16,005 genes retained. The top 50 up and 50 down SFFFM genes were frozen
before projection; 44/50 per direction agree in ADM. Removing prespecified panel
genes and Hallmark E2F/G2M overlap leaves 49 up/48 down, of which **34 up/47 down**
map to the filtered Nb2 matrix. Missing genes restrict the comparison.

This disjoint sustained-YT-associated score gives Fzd5−CHIR **−0.372** (conditional
95% interval −2.061 to +1.318; single omission −0.687 to +0.068) and Fzd6−CHIR
**+0.004** (−1.616 to +1.623; omission −0.311 to +0.443). Both are unstable in
direction. Relative to withdrawal48, all three agonist/CHIR arms have positive
point estimates with intervals spanning zero. There is no supported receptor-
specific broad sustained-YT response or evidence of its absence.

The reference is a **Stk3/4-loss-associated response**, not purified TEAD targets.
It cannot separate YAP from TAZ or direct effects from altered identity. In the
mouse atlas, its disjoint score is also higher in AT1 than AT2 in all four eligible
day-42 pairs (median +2.532). That is an internal warning against calling this
score a classifier of maladaptive persistence. [N2](candidate_questions/Nb2-N2.md).

## N3: receptor RNA and canonical target RNA do not order epithelial states alike

At day42, eligible source samples number AT2 **8**, AT1 **4**, AT1_AT2 **1** and
Alveolar_transitional **0** at the 50-cell floor. Across all days, the transitional
label has only one eligible unit at day11 (two at floor20). Its state-response
question remains ineligible for a cohort-level comparison.

Within four matched AT1/AT2 samples, AT1−AT2 Fzd5 CPM is positive in **4/4**, median
**+31.994 CPM** (range +16.406 to +52.346); the Wnt-clean score is lower in **4/4**,
median **−1.323 mean log2(CPM+1)** (−2.166 to −0.657). Fzd6 differences are positive
in 3/4 and span zero. These scales are different and are not compared numerically
to one another. Sparse canonical targets, state labeling and niche differences
remain explanations. Neither RNA measurement establishes functional signaling.
The result motivates testing **state context beyond receptor abundance**, not a
claim that Fzd5 disappears during differentiation. [N3](candidate_questions/Nb2-N3.md).

## N4: the compensation contrast is not identifiable

All 18 GSE208770 libraries are input/withdrawal conditions: **zero deletion and
zero inhibitory-antibody libraries**. The source reports an Fzd5 knockout score
of 65%, not a verified fraction of biallelic-null cells with absent protein.
The antibody inhibits **Fzd5/8**, whereas the genetic condition targets Fzd5.
The editing-to-growth preparation map and early-to-sustained response series
were not recovered. Residual/unedited cells, receptor persistence and target
breadth are therefore unresolved rivals before adaptation is invoked.

The [receptor/feedback table](trials/extension_v1/tables/nb2_receptor_feedback_effects.tsv)
preserves all measured agonist contrasts; they are not mislabeled as compensation
after loss. This branch completes an evidence/design audit and **does not perform
a fictitious KO differential-expression test**. [N4](candidate_questions/Nb2-N4.md).

## N5: compare response profiles before attributing ligand routing

Against withdrawal48, Wnt-clean score differences are Wnt3a **+0.566**, CHIR
**+4.235**, Fzd5 **+3.258**, Fzd6 **+3.259**. Against CHIR, both Fzd agonists show
lower Wnt-clean but higher source-YAP and AT1-associated scores under all single
and leave-one-per-arm omissions. The profiles therefore motivate a selective-
output question rather than assuming all inputs are interchangeable canonical
amplitude controls.

Nevertheless, exposure and target engagement are unmatched, and CHIR has effects
outside receptor ligation. Fzd6−Fzd5 Wnt-clean is only +0.001 (conditional interval
−0.457 to +0.459), while the source-YAP difference is −0.557 (−2.611 to +1.496).
Similar point estimates are not equivalence; differing RNA components do not
prove different signaling routes. Synthetic Fzd–Lrp agonists, recombinant Wnt3a
and a GSK3 inhibitor are different inputs, not a comprehensive ligand panel.
No PCP, calcium, polarity or migration measurement is present. [N5](candidate_questions/Nb2-N5.md).

## N6: fibroblast subtype changes the Fzd1 interpretation

At day42, AF1 has 8 eligible samples, AF2 5, adventitial fibroblasts 8 and
peribronchial fibroblasts 2. In the **five paired AF1/AF2 samples**, AF1−AF2:

| Endpoint | Median difference | Range | Direction |
|---|---:|---:|---|
| Fzd1 CPM | −74.673 | −147.258 to −19.980 | lower in 5/5 |
| Fzd2 CPM | +39.533 | +37.733 to +60.436 | higher in 5/5 |
| Fzd7 CPM | −2.638 | −3.719 to +16.132 | mixed |
| Support-ligand score | +3.572 | +2.604 to +4.239 | higher in 5/5 |
| ECM score | +1.114 | +0.801 to +2.588 | higher in 5/5 |

Scores are mean log2(CPM+1). At floor20, all eight pairs retain the Fzd1/Fzd2 and
support directions, with and without predicted doublets; **floor100 has no eligible
AF1/AF2 pairs**. Within AF1, Fzd1–support rho is +0.286 and changes sign on omission
(−0.071 to +0.536). AF2 correlations are highly unstable. This does not support a
unique positive Fzd1–support relationship. More Fzd1 is not automatically a more
supportive niche, nor does more ECM RNA establish harmful fibrosis. The newer
[Fzd2 perturbation study](https://pubmed.ncbi.nlm.nih.gov/41257888/) provides a
specific comparator, not validation of these expression associations. [N6](candidate_questions/Nb2-N6.md).

## N7: a vascular association weakens under experimental-round scrutiny

The source CAP1/CAP2 marker crosswalk is consistent at day42: CAP1−CAP2 CAP1-marker
score is positive in 8/8 samples; CAP2-marker score is negative in 8/8. This supports
gCap-like/aerocyte-like annotation compatibility, not the progenitor capacity of
each cell. Coarse CAP1 also contains injury-associated heterogeneity.

Fzd4 is higher in CAP1 than CAP2 in **8/8 pairs**, median +196.758 CPM; arterial and
venous expression remains high. Within CAP1, Fzd4–cycling rho is **+0.738**, retains
sign on omission, and persists across cell floors, doublet settings and 500-UMI
receptor detection. Its junction-score association is only +0.071.

A **post hoc** check prompted by that positive association finds opposite
within-round patterns: **−0.400** in the 2021 round and **+1.000** in the 2022 round
(four samples each). Depth does not resolve this inconsistency. Tamoxifen tracing
window, genotype, sex, cohort and capillary substate remain entangled. The pooled
association is a candidate to challenge, not evidence of a Fzd4 progenitor mechanism.
[N7](candidate_questions/Nb2-N7.md); [rival audit](trials/extension_v1/tables/vascular_depth_round_audit.tsv).

## N8: endogenous Fzd6 input remains a distinct missing perturbation

The extra pre-existing branch is retained as [N8](candidate_questions/Nb2-N8.md). Synthetic
receptor activation and ligand RNA coexistence do not establish an endogenous
Fzd6 ligand or dependence. Current counts lack ligand-selective perturbation
crossed with Fzd6 dependence. This companion remains an eligibility result.

## What changed in the hypothesis priority

Prioritize N1–N3/N5 as a connected question about reversible, state-dependent
responses with **linked later maturation**. The strongest present leads are
selective source-panel changes and receptor/target dissociation. N6 is supported
as a subtype-comparison question. N4 needs matched loss/blockade evidence first;
N7 needs replication that separates experimental round and capillary substate.
None of these results warrants a clinical benefit claim or an evidence-grade change.

Numerical checks, the preserved depth-schema failure/amendment, provenance and
current scope are in [EXECUTION.md](EXECUTION.md). All tables remain available,
including sparse states and unfavorable sensitivities; no outlying library was removed.
