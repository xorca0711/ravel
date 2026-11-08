# TIGIT–PRDM1: genotype-dependent inducible output

**Current development owner (7 November): [A33](../../../RQ_Specified/A33_ezh2_tigit_areg_output/README.md).**
This article-local card retains its earlier design checkpoint. The new home integrates
the executed RNA result and [reframing/literature correction](../rq_derivation/README.md).
The older proposal below is not the current instruction to execute.

7 November 2026. Exploratory Dp1-P01 subquestion; not an accepted new RQ.
[Follow-up overview](../CANDIDATE_FOLLOWUP.md) · [Source audit](SOURCE_QUALIFICATION.md).

**Completed numerical follow-up:** [gain-context results](../CANDIDATE_ANALYSIS_RESULT_V1.md).
The experimental stages below remain proposed; interpret their RNA premise with that result.

## Published finding → repository observation → remaining question

TIGIT-associated Blimp-1/AREG output is an established premise, with activation
and priming dependence in [Panetti et al., 2025](https://doi.org/10.1038/s41590-025-02300-w),
Figures 5–6 and Extended Data 8. Anti-CD28 co-stimulation licensed responses in
otherwise naive cells. Parts of the Blimp-1 perturbation evidence use broader
T-cell deletion; they do not alone identify a Treg-restricted mediation effect.
[Peeters et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39264807/), Figure 7F–G,
already links Ezh2 gain to TIGIT expression.

The exposed DuPage [coding table](../../../analysis/research/runs/dupage_target_screen_v2/all_annotated.tsv)
has lower Tigit and Prdm1 in KO-low versus HET-low, with stable signed
interactions under the recorded sensitivity set. Both retain positive high-to-low
state contrasts; the observations indicate attenuation, not disappearance.
Areg's interaction is unstable. These are mean-log RNA differences among
Foxp3-positive survivors, not measured response kinetics or secretion.

**Question:** under a common, demonstrably responsive activation context, does
Ezh2 loss change the incremental AREG output associated with TIGIT engagement?
The potential contribution is an Ezh2-context boundary/effect-modification test,
not discovery of a TIGIT–Blimp-1 mechanism or proof of tissue repair.

## Comparison tuple and estimand

| Element | Prospective specification |
|---|---|
| Population/model | Viable lineage-identified murine lymphoid Tregs; anatomical source, age, sex, allele and genetic background must be fixed before execution |
| Exposure/comparator | Common TCR/co-stimulatory context, TIGIT engagement versus matched reagent control, within Ezh2-deficient and matched control preparations |
| Source comparator | DuPage is KO versus HET; a new study must name its actual genetic control and cannot silently relabel HET as WT |
| Timing | Baseline plus a qualified response window before major differential cell loss; exact window unresolved |
| Primary output | AREG released into supernatant, with assay background and absolute live-cell recovery; intracellular AREG is a distinct supportive endpoint |
| Main contrast | Difference between genotypes in the engagement-minus-control output response; retain each genotype's baseline and simple response |
| Biological unit | Independently obtained mouse/preparation; paired aliquots within preparation; wells/cells nested, not independent animals |
| Limit | Even a positive response contrast does not establish PRDM1 mediation, direct Ezh2 regulation, suppressive function or recipient tissue repair |

## Hypothesis, alternatives and informative outcomes

The working prediction is a smaller inducible output response in Ezh2-deficient
Tregs. General state composition, survival/selection and inadequate receptor
engagement are consequential alternatives that can coexist.

| Observation | What it would teach |
|---|---|
| Control Tregs respond; KO response is smaller while recovery is comparable | Supports an output-response deficit in this assay; candidate mediation remains to be tested |
| Genotype difference disappears under common exposure | Weakens persistence of the proposed deficit; consistent with source-state/context differences |
| Output difference follows cell loss or broad loss of activation responses | Favors a general fitness explanation; per-cell normalization alone cannot resolve it |
| Neither genotype responds | Assay-context failure, not falsification of an Ezh2-specific mechanism |
| Target-restricted perturbation changes output after specificity controls | Supports contribution of that target in this context; a separate PRDM1 test is needed to claim mediation |

## Staged experimental design

1. Qualify TIGIT surface protein, Blimp-1 and assay response under a common
   activation history. Demonstrate a responsive control. Record whether the
   assay uses purified Tregs or a defined accessory population; the latter can
   affect ligand presentation, costimulation and measured supernatant.
2. Run the genotype-by-engagement comparison only after that qualification.
   Allocate aliquots within each preparation, block preparation/batch and
   blind readout where feasible. Reagent action and possible Fc/accessory-cell
   effects need a matched control and a target-specific check. Measure total
   output and viable recovery, not only output per surviving cell.
3. Only if the output contrast is reproducible, ask whether PRDM1 or receptor
   availability contributes through a Treg-restricted perturbation. AREG-mediated
   recipient effects require a separate recipient assay with carryover controls
   and AREG dependence; an RNA score or AREG concentration is not repair function.

## Data and readiness decision

The paper's named ArrayExpress accession does not currently identify the claimed
single-cell experiment. Zenodo record 14041419 matches its WT/Tigit-KO description,
and a header preview contains sample, genotype, tissue and condition fields.
Those fields do not establish animals or pooling. The published methods include
sorted-cell remixing, hashtags and transferred T cells, all requiring explicit
mapping. No cell-level population test or matrix import was attempted.

Required before new numerical execution: source/animal mapping, Treg annotation
provenance, transferred-cell handling, and biological-unit availability. Required
before laboratory execution: model/reagent access, qualified detection/response,
variance and precision rationale. No sample size or effect threshold is invented.
