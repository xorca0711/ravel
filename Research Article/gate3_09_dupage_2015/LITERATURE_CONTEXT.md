# Dp1-P01: literature context

The [7 November biological review](BIOLOGICAL_REVIEW_20261107.md) adds targeted
source checks of the TIGIT priming/accessory-cell context, CCR2/CD25 inference
and the IGF paper's reduced-binding ligand. Its qualifications apply to the
three candidate proposals; prior search records remain below.

Review: **7 November 2026 (Asia/Seoul)**. Base `dcee4b63e11abd27fe2bbc679993b288e913565e`.
Reason: owner completed DuPage 2015 and requested a biological sequence of
analysis decisions. This is a bounded primary-source review, not systematic
coverage, novelty certification or an experiment-ready package.

## Published starting point

| Source / version | Exact locator and access | What it changes here |
|---|---|---|
| [DuPage et al., Immunity 2015](https://doi.org/10.1016/j.immuni.2015.01.007); online 10 February, issue 17 February | Owner's complete published PDF; Figures 1-7, especially 6A-F and discussion p.236. Separate supplement not recovered. | CD28 induction, conditional Ezh2 perturbation, activated-Treg RNA changes, lineage-reporter instability and failed EAE remission motivate the sequence. The connecting molecular mediation remains unresolved. |
| [Arvey et al., Nature Immunology 2014](https://doi.org/10.1038/ni.2868); online 13 April | Primary indexed abstract and publisher supplemental inventory inspected; Supplementary Tables 3, 5 and 6 identify Foxp3 binding, accessibility and H3K27me3 quantification. Full methods/figures not audited in this pass. | The chromatin premise predates DuPage. Its reuse in Figure 6 is cross-study consistency, not matched KO chromatin evidence. |
| [Kwon et al., Nature Immunology 2017](https://doi.org/10.1038/ni.3835) | Primary abstract and figure inventory, especially Figures 4-7; full quantitative analysis not inspected. | Distinct FoxP3 cofactor complexes and context-dependent transcription caution against equating physical association with simple repression. Retain as a boundary lead, not an adjudicated refutation. |
| [Peeters et al., Cell Reports 2024](https://doi.org/10.1016/j.celrep.2024.114724); online 11 September, issue 24 September; PMC manuscript released 5 May 2025 | Primary indexed Results, Figure 6H/7/S7F-I descriptions and RNA methods/data statement inspected; direct PMC page challenged; no full supplemental-panel audit. This supersedes the April 2024 preprint for this review. | EZH2 gain of function promotes early effector features with redistributed H3K27me3. S7H already compares loss- and gain-of-function RNA. A new broad reciprocal-expression comparison would repeat an existing result; a locus/state-specific residual question is the conditional increment. RNA GSE262130 and CUT&RUN GSE262129 are source leads. |
| [He et al., JCI 2026](https://www.jci.org/articles/view/196022); published 23 April | Primary Results/legends Figures 3-6 and data-availability text inspected, especially Figure 5 RNA/accessibility and Figure 6 influenza lung-injury endpoints. No reanalysis or complete supplemental audit. | Loss of the H3K27 demethylase KDM6B also impairs activated Treg regulation and tissue function. Opposing enzymatic reactions need not produce opposite phenotypes. Local regulation and indirect effects remain important. GSE291449 is a source lead. |

Gavin 2007 Foxp3-loss, Samstein 2012 Foxp3-binding, Hill 2007 signature and
Martinez-Llordella 2013 co-stimulation datasets are identified through the DuPage
paper. Their exact data selections must be read and qualified before S1/S3 uses
them. The 2024 paper identifies GSE39595 as its co-stimulation reference; this
does not alone certify an exact match to every 2015 Figure 1 input.

No correction/retraction notice was encountered in the inspected publication
records and the bounded DuPage correction search. This is not a complete
publisher/version audit, particularly given the access restrictions.

## Repository observation at planning

The [source review](SOURCE_REVIEW.md) verifies GSE58998's 12 deposited libraries,
the excluded HET/high library and four-condition merged FPKM structure. These
are source-structure findings, not expression results. No DuPage numerical
contract, receipt or result existed in the current registry before this package.
The owner has already read the outcomes; future reconstruction is exposed.

The original Niethamer/D1 lung Treg feasibility gate remains unmet. Current
[A30 evidence](../../RQ_Specified/A30_csf_compartment_effector_state/README.md)
concerns paired human compartment-associated RNA and does not demonstrate Treg
stability, EZH2 function or a missing mediator in this murine study.

## What this question could add

First, a transparent reconstruction that distinguishes averaged displays from
replicate observations and respects the HET comparator. Then, if inputs permit,
a direct genotype-by-state estimate and a transparent separation of repression-
associated, induction-associated and unexplained changes. Any more ambitious
addition must address an unresolved comparison beyond the closest published
experiment; renaming the published mechanism is not an increment.

## Initial hypothesis and rival

Ezh2 loss may preferentially disrupt repression in activated Foxp3-positive Tregs.
Heterogeneous activation, survival and selection into the sorted gate can also
generate bulk differences. The [plan](ANALYSIS_PLAN.md#purpose-hypothesis-and-strongest-alternative)
states the full tuple and inference boundaries. The source's cross-sectional
states do not establish temporal order, a stable fate or chromatin mediation.

## What the comparison would teach

A qualified state-specific pattern would narrow the regulation question; a
state-general difference weakens activation specificity; discordant gene classes
support multiple processes; inadequate feature/unit support leaves inference
unestimated. External chromatin concordance motivates direct measurement but
cannot substitute for it. The absence of functional inputs limits downstream
claims while leaving a useful RNA reconstruction possible.

## Hypothesis schematic

The [README's qualitative Mermaid map](README.md#literature-context--visual-hypothesis)
separates published links, proposed connections and the selection/survival
alternative. It contains no measured counts. A canonical registered illustration
is not created for this article-local planning candidate.

## Initial literature search record

Actual searches used live web search on 7 November 2026, without author/lab
restriction. Coverage: foundational work plus a recent 2024-2026 window, using
year terms rather than a hard date filter. Main queries included:

- `DuPage 2015 Ezh2 regulatory T cell identity GSE58998 data Immunity`
- `Ezh2 regulatory T cells activation Foxp3 2024 2025 2026 chromatin identity`
- `Foxp3 Ezh2 Arvey 2014 chromatin`
- `DuPage 2015 GSE Arvey`
- `Ezh2 GSE58998 replicates pool`
- `DuPage 2015 Supplemental Experimental Procedures`
- `Hyperactivating EZH2 to augment GSE`
- `DuPage 2015 Ezh2 correction retraction`

Backward references were inspected in DuPage and followed to Arvey; later
primary work was found through relationship searches and the 2024/2026 primary
texts. No systematic citing-paper database export or exhaustive forward-citation
screen was performed. Some narrow quoted/multi-query searches returned irrelevant
hits; they were not treated as negative evidence of missing literature.

Access was strongest for the supplied 2015 paper, GEO and the JCI Results. Other
sources have the bounded access levels above. The [source review](SOURCE_REVIEW.md)
records publisher/PMC/Europe PMC failures and exact inspected file versions.

Stop point: enough evidence to plan source reconstruction and identify the
principal selection/chromatin validity threats. Before S3, recover and inspect
the exact older reference data and 2015 supplement. Before S4, audit the actual
2024/2026 assay/sample manifests and the relevant full supplemental comparisons.
Reopen literature review if a numerical result, chosen gene class or intended
functional claim changes the comparison. Do not infer novelty from search gaps.


## Execution update — 7 November 2026

[Current synthesis](RESULTS.md), [S3](S3_RESULT.md) and [AM01](ANALYSIS_AMENDMENT_V2.md)
supersede the initial no-result/reference-access status above. The initial
hypothesis is preserved, not rewritten as if outcomes were unexposed.

S0–S2 supply compatible per-library FPKM and a mixed, sample-sensitive state
interaction. S3 finds weak positive external chromatin consistency in 1,180
mapped loci (rho 0.162; single-gene-domain sensitivity 0.149). Most RNA loci are
uncovered; HET-defined classes share terms with the interaction. The contribution
is adapted shared-source reconstruction, not independent replication or novelty.

New completed primary reads: DuPage full XML (Figures 4/5/7 and main-text S7
account); Arvey full XML, Figures 5–6/online methods, publisher Table 6 structure;
GSE55753/55773 metadata and sequencing README. Exact source URLs, versions,
normalization, mapping and hashes are in S0/S3 and their contracts. Arvey
sequencing is GSE55773; GSE55705 is microarray. The H3K27me3 table is already
log2(RPKM+0.3), quantile normalized. Pinned UCSC mm9 RefGene is a 2020 dump,
not the original authors' gene mapping. No cross-build coordinate join was used.
The separate 2015 supplement and exact Foxp3 reference selections remain held.

Live web checks used `"ni.2868" "MOESM7"`, `"NIHMS574501" "xls"`,
`site.genome.ucsc.edu refGene txStart txEnd zero based half open name2`,
`"Hyperactivating EZH2" "S7H"`, and `site.jci.org/articles/view/196022 "KDM6B"`.
These were targeted source/method/precedent checks, not a second systematic scan.
The initial same-day broader 2024–2026 search remains valid for unchanged premises.
The [2024 primary Results passage](https://pmc.ncbi.nlm.nih.gov/articles/PMC12052300/)
describing S7H and [2026 primary Results](https://www.jci.org/articles/view/196022)
were rechecked; their full supplements and numerical assay manifests were not
audited. S4 would repeat a broad published comparison without a specific new
discriminator, so no external numerical execution is claimed or required.

The unresolved contrast is regulation within viable lineage-labelled Tregs
versus altered population survival/selection. A future common-exposure HET/KO
comparison needs direct regulatory, lineage-retention and viability readouts;
function/trafficking need separate assays if claimed. This is a proposed
model-discrimination question, not an accepted RQ or experiment-ready design.
Target, effect margin, sample-size basis and laboratory feasibility are unknown.

## DuPage-first target-screen rationale — 7 November 2026

The owner requested a new screen rooted in DuPage 2015, with Zhang 2026 optional
rather than a required tumor/NK direction. [The prospective exploratory plan](TARGET_SCREEN_PLAN_V1.md)
keeps the original Treg population and separates stable low-state differences
from state-prioritized differences. Broad mixed results do not imply that no
individual candidate is worth investigating; neither do individual RNA rows
establish a causal target. Every candidate will need literature triage and a
distinct protein/function comparison.

DuPage's Discussion (journal pp.235–236, paragraph beginning "We found that
Ezh2 functions largely...") already names Pde3b, Tcf7 and Lef1. They are
precedent anchors, not new discoveries. A targeted search on 7 November 2026
used `Ezh2 Treg Pde3b Tcf7 Lef1 2024 2025 2026 primary` and
`DuPage 2015 Ezh2 regulatory T cells downstream targets activation survival`.
It recovered [Kidani et al., 2024](https://pubmed.ncbi.nlm.nih.gov/38169425/),
on TCF7/LEF1 downregulation in tumor Tregs (search record inspected; focused
results reading remains prospective), and the already-read Peeters/He context
above. Screening ranks have not yet been inspected at this planning checkpoint.

The preceding Zhang comparison established relevant boundaries, not the chosen
screening direction: the supplied published Zhang PDF (10 April 2026,
[doi:10.1126/sciimmunol.adx4411](https://doi.org/10.1126/sciimmunol.adx4411),
SHA-256 `476c35571d5fcede9f3e32a6f53d493967f65180b3f03fbf5d0353c95d7a6b23`)
was text-read, with journal pp.8–9 visually inspected. Figures 6–7 connect local
Treg depletion to cDC2/conventional-CD4 IL-2 and NK-dependent tumor control;
the mechanism of suppression upstream of IL-2 is not fully resolved.
[Wang et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6094952/), main text
and Figure 5F–G/6 legends read via NCBI BioC, already showed altered cytokine
potential in Ezh2-deficient tumor Tregs, including IL-2 after restimulation,
and compared reprogramming with depletion. This is not evidence for spontaneous
in-situ IL-2 release in DuPage's lymphoid samples. GSE114298 is a potential future
source, not a qualified independent validation dataset in this work.

## Target-screen literature triage — 7 November 2026

[The completed target-screen report](TARGET_SCREEN_RESULT.md) now owns candidate
observations, triage of all 32 coding-frontier genes and three proposed
comparisons. [Portfolio figures](TARGET_SCREEN_FIGURES.md) preserve the full
frontier and distinguish data from proposed experiments. V1 exposed a poly-A
versus small-RNA-label mismatch; V2 added a separately frozen coding annotation
restriction rather than rewriting that result.

This was a bounded primary-literature pass, not a systematic review or novelty
clearance. Searches were not restricted to target PIs. Main sources and access:

| Primary source and exact locator | Portion actually inspected; effect on interpretation |
|---|---|
| [TIGIT tissue protection, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12571903/), Figures 3, 5–6 and associated Results | Full-text BioC retrieved; focused mechanistic passages/legends read. Published receptor-to-Blimp-1/AREG premise motivates an Ezh2-dependent response test; it is not a novel TIGIT mechanism. |
| [EZH2 gain, 2024](https://pubmed.ncbi.nlm.nih.gov/39264807/), Figures 2B, 4D, 7G | PubMed primary figure legends rechecked for TIGIT protein phenotyping. The broad EZH2–TIGIT association is also established precedent; the proposed increment concerns inducible functional output. |
| [CCR2/CD25, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC7000403/), Figure 5 and Results | Indexed primary text/legend inspected; direct full-text routes returned browser check/non-XML. Supplies fitness alternative to migration; no entire-supplement review claimed. |
| [Intestinal microniches, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11041794/), Figure 5, Extended Data 9 | Indexed primary Results/legends inspected; spatial expression/contact context does not establish receptor causality. |
| [IGF/Th17–Treg, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC8078727/), Figures 1 and 4, Discussion | Full primary page available; focused Results/legends read. Distinguishes induction from subsequent survival/maintenance; does not test the present Ezh2–IGFBP4 mechanism. |
| [IGF-1/Treg, 2014](https://pubmed.ncbi.nlm.nih.gov/25339185/), abstract and indexed figure descriptions | Treg expansion/suppression context; not a complete methods audit. |
| [Lymphoid single-cell landscape, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6069633/), core-signature paragraph containing Igfbp4/Dapl1 | Indexed primary manuscript passage inspected; PMC/BioC routes blocked/rate-limited. Supports origin/state qualification rather than a validated functional role. |
| [PDE3B, 2019](https://www.jci.org/articles/view/124725), Figures 5–6 | Primary Results/legends inspected; substantial existing mechanism makes PDE3B a comparator and bounded Ezh2-specific follow-up, not a discovery. |
| [IL1R2/Tfr, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11143922/), Figure 3; [IL1R2/tumor, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12666320/), deletion/blockade Results and Discussion | Both primary pages inspected in relevant sections. Different contexts separate functional receptor contribution from useful cell-surface marking. |
| [Tcf1/Lef1, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6446865/) and [TCF7/LEF1 tumor study, 2024](https://pubmed.ncbi.nlm.nih.gov/38169425/) | Indexed Results/abstract reviewed as context boundaries; no numerical integration or full supplement audit. |

Actual search strings for this post-screen pass (7 November 2026):

- `PDE3B regulatory T cells Foxp3 cAMP genetic deletion suppression`
- `TCF1 LEF1 regulatory T cells loss function colitis 2019 2020 2024`
- `"IGFBP4" "regulatory T" cells`; `"DAPL1" "regulatory T" cells`;
  `"ADAM8" "regulatory T" cells`; `"IL1R2" regulatory T cells 2024 2025 2026`
- `"Igfbp4" "Treg" "Ezh2"`; `"IGFBP4" "regulatory T cells" 2024 2025 2026`;
  `"Dapl1" Treg suppressive function gene deletion`; `"G0s2" regulatory T cells`
- `CCR2 regulatory T cells migration suppressive function tissue 2024 2025 2026`;
  `"CCR2" "regulatory T cells" knockout tissue homeostasis`
- `"Single-cell gene expression reveals a landscape" Igfbp4 Dapl1`;
  `"IGF-1" mature regulatory T cells protection 2014 2015`
- `TIGIT EZH2 regulatory T cells amphiregulin`;
  `"Single-cell gene expression reveals a landscape of regulatory T cell phenotypes"`
- `"CCR2 enhances CD25" "Fig." "IL-2"`;
  `"Immune microniches shape intestinal Treg function" "CCR2" "blockade"`

Search leads for G0S2, DAPL1, ADAM8 and recent IGFBP4 contexts did not receive
equivalent functional-source qualification; their status remains unresolved,
not unsupported biology or absence of precedent. Search snippets describing
predicted regulons or prognostic scores were not treated as Treg perturbation
evidence. No new shared-source dataset was counted as independent replication.
Current annotation version and molecular-identity limits are in AM02. Exact
primary reads remain distinct from planned assay/data acquisition.

## Three-candidate source qualification and numerical continuation

7 November 2026: [source audit](candidates/SOURCE_QUALIFICATION.md) records the
TIGIT accession mismatch, matching Zenodo lead, CCR2 assay-context restriction,
IGFBP4 source/processing precedents and selected-matrix limitation in GSE262130.
[Candidate comparisons](CANDIDATE_FOLLOWUP.md) distinguish proposed experiments
from the [new frozen numerical plan](CANDIDATE_ANALYSIS_PLAN_V1.md). No fresh
expression analysis was performed during the preceding literature/metadata pass.
