# Wp (Wang 2025, PGAM): literature context

Review date **4 October 2026**, this package's first pass, written against
`main` `9a49d26a`. Author: assistant, under the owner's instruction to structure
this paper's analysis. Reused without repeating: the
[2021 package's literature log](../gate2_W1_wagner_th17_autoimmunity/LITERATURE_CONTEXT.md)
and its [precedent review](../gate2_W1_wagner_th17_autoimmunity/PRECEDENT_REVIEW.md),
which already cover Compass as a method, polyamine control of T-cell identity and
the lung precedents. This pass searched only what is specific to PGAM, the serine
arm and this paper's endpoints. Access level is abstract-and-indexed-text for the
precedents below, except where a full text was read; that is stated per entry.

## Published starting point

| Source | Locator and access | What it contributes here |
|---|---|---|
| [Wang, Wagner, Fessler et al. 2025, *Cell Reports* 44, 115799](https://doi.org/10.1016/j.celrep.2025.115799) (PMID 40482033) | Full text and STAR Methods read from the owner-supplied PDF; supplement legends only | The package's source. Th17n cells, in-vitro differentiation, PGAM inhibition by EGCG and sgRNA, endpoints from RNA program to EAE |
| [Godfrey et al. 2025, *eLife* 14:RP104423](https://doi.org/10.7554/eLife.104423) (PMID 40720256; earlier bioRxiv PMID 38979375 — one study, not two) | Abstract read in full; figures not accessed | **The decisive comparison.** PGAM inhibition reduces Treg differentiation and suppressive function and induces Th17-like markers, and the effect runs through 3PG-derived de novo serine synthesis, one-carbon metabolism and methylation of Treg-associated genes |
| [Toriyama et al. 2020, *Communications Biology* 3:394](https://doi.org/10.1038/s42003-020-01122-w) (PMID 32709928) | Abstract read in full | T-cell-specific *Pgam1* deletion attenuates both CD4 and CD8 responses and ameliorates helper-T-dependent inflammation — the opposite phenotypic direction from partial inhibition, and the paper's own cited reason for distinguishing complete ablation from dose effects |
| [Wagner et al. 2021, *Cell* 184:4168](https://doi.org/10.1016/j.cell.2021.05.045) (PMID 34216539) | Held in this repository as [paper 15](../gate2_W1_wagner_th17_autoimmunity/README.md) | Compass itself, its validation requirements and its scoring conventions. Shared authors and a shared method: this is one evidence lineage with the source, not independent support |
| [Gaublomme et al. 2015, *Cell* 163:1400](https://doi.org/10.1016/j.cell.2015.11.009) (PMID 26607794) | Cited by the source for the modules; not re-read in this pass | Origin of the pro-inflammatory and pro-regulatory modules. Becomes a required input if Table S1 stays unavailable |
| [Brucklacher-Waldert et al. 2017, *Cell Reports* 19:2357](https://doi.org/10.1016/j.celrep.2017.05.052) (PMID 28614720) | **Full text read 5 October 2026** | Glycolysis blockade with 2-DG (and with 3-bromopyruvate) *promotes* Th17 differentiation — the established precedent that glycolysis inhibition is not uniformly anti-inflammatory. Its mechanism is sustained cytoplasmic calcium with a partial XBP1 contribution, and its central claim is that stress **substitutes for** TGF-β, tested against neutralising anti-TGF-β. The source's Discussion reads it as stress *activating* TGF-β networks, which inverts it; see [Wp-P02](branches/P02_serine_one_carbon_direction.md) |
| [Wu et al. 2020, *Cell* 182:641](https://doi.org/10.1016/j.cell.2020.06.014) (PMID 32615085) | Abstract-level | Niche-selective inhibition of pathogenic Th17 cells by targeting metabolic redundancy: the nearest precedent for "which metabolic step, in which niche", and the reason reaction-level selectivity is a live question rather than a novelty claim |
| [Li et al. 2017, *Front. Pharmacol.* 8:325](https://doi.org/10.3389/fphar.2017.00325) (PMID 28611670); [Huang et al. 2019, *Cell Metab.* 30:1107](https://doi.org/10.1016/j.cmet.2019.09.014) (PMID 31607564) | Cited by the source; abstract-level | EGCG as a PGAM1 inhibitor, and a separate allosteric PGAM1 inhibitor class. The existence of selective tool compounds is what makes the paper's EGCG-only chemistry a stated limitation rather than a necessity |

Contrary and boundary evidence is listed above rather than in a separate section,
because the two entries that matter most — Toriyama and Godfrey — are each partly
concordant and partly contradictory, and splitting them into "support" and
"contradiction" would misrepresent both.

## Two citation checks prompted by the owner's notes

The owner's Discussion note repeats the source's proposed mechanism chain —
glycolysis blockade, cellular stress, TGF-β, PGAM — and asks for the connection
between serine biosynthesis, cellular stress and Th17 pathogenicity. Checking the
two references that chain rests on, at **abstract level only**, 4 October 2026:

- [Brucklacher-Waldert et al. 2017](https://doi.org/10.1016/j.celrep.2017.05.052)
  (PMID 28614720) is cited for 2-DG promoting Th17 effector function "by
  activating cellular stress transforming growth factor (TGF)-ß signaling
  networks". Its own title and abstract state that cell stress in an inflammatory
  environment supports Th17 differentiation **in the absence of** TGF-β
  signalling. The citing sentence and the cited abstract characterise TGF-β's
  role differently.
- [Huang et al. 2019](https://doi.org/10.1016/j.cmet.2019.09.014) (PMID 31607564)
  is cited for PGAM being essential for TGF-β signalling in cancer cells. It is an
  allosteric PGAM1-inhibitor study in non-small-cell lung cancer, and its abstract
  does not mention TGF-β.

**Update, 5 October 2026 — both texts pursued.** Brucklacher-Waldert's full text
was read and the first check is now **confirmed, not merely flagged**: the paper
is titled for TGF-β-*independent* Th17 differentiation, its highlights state that
stress "can substitute for TGF-β", the stress inducers are tested against
neutralising anti-TGF-β, and the mechanism advanced is sustained cytoplasmic
calcium with a partial XBP1 contribution. 2-DG and 3-bromopyruvate both enhance
Th17 polarisation, so the phenotypic direction the source cites is right while
the TGF-β attribution inverts the source's claim. Huang 2019 is not open access
and no legitimate route returned the full text, so the second check stays at
abstract level and remains a flag; the owner can resolve it by supplying the PDF.

The TGF-β leg is therefore an **unverified premise whose one readable support
contradicts it**, which is how
[Wp-P02](branches/P02_serine_one_carbon_direction.md) carries it.

## Repository observation

Nothing has been computed in this package. Wp-R0's entrypoint has been dry-run
outside the governed runner and its verified source counts are in
[Datasets](DATASETS.md); no analysis of expression has been performed, and no
figure exists. The 2021 package's separate, already-executed evidence (its R0/R1
identity work and R3 RNA models) is not evidence about this paper, and its
recorded unresolved **PGAM reference-sign conflict** is the same documentation
problem recorded here in [Evidence map](EVIDENCE_MAP.md#what-is-not-available).

Outcome exposure: full. Every figure and conclusion of the source was read before
any plan was written, and the EGCG and module signatures the package would
reconstruct are published. No later freeze changes that.

<a id="directional-conflict-on-the-serine-arm"></a>
## Directional conflict on the serine arm

This is the one unresolved contrast this package can act on, and it is specified
as [Wp-P02](branches/P02_serine_one_carbon_direction.md).

**Published finding.** PGAM inhibition shifts Th17n cells toward a pathogenic
program and suppresses the least-pathogenic N1 program; Compass separately
predicts that the 3PG→serine shunt is *negatively* correlated with pathogenicity,
and the Discussion offers serine biosynthesis as a possible mediator.

**Independent finding.** In Tregs, the same enzyme's inhibition reduces
regulatory character, and that effect *depends on* 3PG-derived serine feeding
one-carbon metabolism and methylation; exogenous serine suppresses Treg
polarisation and a serine/glycine-free diet increases peripheral Tregs.

**Unresolved contrast.** Both report loss of regulatory character after PGAM
inhibition, but through opposite roles for the serine arm. If Godfrey's mechanism
holds in the Th17n compartment, the Compass sign for the serine shunt is wrong or
is not a flux statement; if the Compass sign holds, PGAM's effect in Th17n cells
is not the serine mechanism and the Discussion's suggestion is misdirected.

**Hypothesis and rival.** Comparison tuple — population: in-vitro differentiated
Th17n CD4 T cells (TGF-β + IL-6, 25 mM or 1 mM glucose, 68 h); perturbation:
PGAM inhibition, with or without PHGDH inhibition; timing: concurrent with
differentiation; comparator: solvent and single-agent arms; endpoint: Foxp3 and
IL-17 protein plus 13C serine/glycine labelling, with transcriptional arms as a
secondary readout; unit: mouse. Hypothesis: the serine arm acts *against* the
regulatory program, so blocking serine synthesis rescues it. Rival: serine-pathway
transcripts and labelling track proliferative demand, and the PGAM phenotype is
carried by loss of downstream glycolysis rather than by diversion.

**What either outcome would teach.** Rescue by PHGDH inhibition would make the
diversion model the operative one in Th17 cells as well as Tregs, unifying two
compartments and implying diet- and tissue-dependent effects. No rescue would
localise the Th17 phenotype downstream of 2PG and would mark the Compass serine
correlation as a prediction that does not survive perturbation — informative about
the method, not only the biology. An inconsistent sign across animals is an
inconclusive result and is reported as such.

**Contribution description:** model discrimination. Not novelty: both mechanisms
are published, in different compartments, and no search here establishes that the
contrast has not been tested elsewhere.

## Next literature check

Actual searches, PubMed E-utilities, 4 October 2026, relevance-sorted, publication
window 2015 onward, eight records inspected per query at title/abstract level:

| Query intent | Indexed hits | What was inspected |
|---|--:|---|
| PGAM1 or phosphoglycerate mutase with T cell, Th17 or lymphocyte | 22 | Top 8; found Godfrey 2025, Toriyama 2020 and the source itself |
| PGAM1 with inhibitor, EGCG or epigallocatechin | 26 | Top 8; allosteric inhibitor series and virtual-screening work, mostly oncology |
| Serine with PHGDH or one-carbon, and Th17 or T-cell differentiation | 6 | All 6; Godfrey 2025 is the only PGAM-linked entry |
| Compass, flux balance or metabolic flux with single-cell RNA | 57 | Top 8; method alternatives (METAFlux, scFEA-type graph models, MEBOCOST) noted as comparators, not adopted |
| Glucose with Th17 and effector or pathogenic | 63 | Top 8; GLUT3/GLUT1 and niche-redundancy precedents |
| Th17 pathogenic signature, module or heterogeneity | 167 | Top 8; module and stem-like Th17 precedents |

Not inspected, and therefore open: citing-article chains for Godfrey 2025 and for
the source (both too recent for a settled citation set at this date); full figures
and methods of Godfrey 2025; the allosteric-inhibitor literature at full text;
any non-PubMed index. The publisher's supplementary Excel files could not be
retrieved from this environment.

**Reopen this comparison when** the supplementary tables arrive, when a study
measures serine or one-carbon flux in Th17 cells under PGAM perturbation, or when
a selective PGAM1 inhibitor is used in a T-cell differentiation assay. No finite
search here clears novelty, and none is claimed.

## Hypothesis schematic

Pending. No versioned SVG exists for this package; an article-local candidate may
retain an explicit pending-figure note, and this is one. A schematic would be
registered only after the Wp-P02 direction statement is reviewed, so that the
drawing does not fix a sign the evidence has not settled.
