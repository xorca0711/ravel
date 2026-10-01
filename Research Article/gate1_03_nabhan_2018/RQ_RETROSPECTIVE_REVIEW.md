# Retrospective RQ review: Nabhan 2018 / Nb1

Reviewed 2026-10-01 against saved outputs and the current RQ cards on
`origin/main` at `f61343cc16c83e979b071393adccdcf8084ea294`. The source paper
supplies spatial and perturbation motivation; the repository supplies
descriptive transcript measurements and explicit feasibility gates.

## Analysis sequence and its consequences

| Date / order | Saved evidence | Consequence for framing |
|---|---|---|
| 2026-09-22, source reproduction | [Source report](source_reproduction/README.md), [summary](source_reproduction/summary.json), [download provenance](source_reproduction/provenance.json) | Forty-seven deposited mesenchymal cells show frequent Wnt5a/Pdgfra co-detection, varying from 72.2% to 90.3% under fixed thresholds. Exact reproduction of 74% remains unresolved. These are cells, not established animal replicates; widespread Sftpc requires a carryover/identity caveat. |
| 2026-09-22, Nb1 coverage then expression | [Protocol](nb1/PROTOCOL.md), [report](nb1/README.md), [animal coverage](nb1/tables/animal_compartment_coverage.csv), [paired ligands](nb1/tables/paired_fibroblast_ligands.csv), [marker summaries](nb1/tables/animal_marker_summaries.csv) | AF1 Wnt2 exceeds AF2 and AF2 Wnt4 exceeds AF1 in all 21 eligible within-animal pairs, including equal-depth detection. Wnt5a spans several fibroblast populations. AT2 Wnt7b occurs at baseline and after injury. Source identity, receiver response, AT2 identity and cycling remain different measurements. |
| 2026-09-22, independent-cohort feasibility and acquisition | [Report](external_feasibility/README.md), [gate record](external_feasibility/feasibility.json), [acquisition audit](external_feasibility/GSE129605_acquisition_audit.json) | GSE129605's eight libraries were acquired; independent mouse mapping, annotations and compartment coverage remain unresolved. GSE141259 day-3 fibroblast coverage fails. This adds feasibility information, not an external expression result. |
| 2026-09-29–30, later RQ context on main | [A20 narrowed hypothesis](https://github.com/xorca0711/scRNA_seq/blob/f61343cc16c83e979b071393adccdcf8084ea294/RQ_Specified/A20_fibroblast_fzd_context/NARROWED_HYPOTHESIS.md) | A20 asks whether comparable Fzd2 loss impairs AF1 epithelial support more than Fzd1 loss. That receptor-necessity question must not be inferred from Nb1 ligand expression or duplicated as a new ligand-source RQ. |

## Conditional candidate — related to A4, source-context branch

**Working hypothesis.** Fibroblast source context may modify whether a
Wnt-supported AT2 lineage subsequently enters an IL-1-responsive transition.
The AF1-biased Wnt2 and AF2-biased Wnt4 profiles nominate distinct source
contexts; the current data do not identify either ligand as the causal switch.

**Why this adds a distinct branch.** A4 primarily contrasts sequential states
within one lineage with fixed opposing subsets. This conditional branch asks
whether the surrounding ligand-source context modifies that sequence. It is
not the A20 comparison of Fzd2 versus Fzd1 requirements inside AF1 fibroblasts.

**Evidence and limit.** The paired 21-animal directions motivate source
heterogeneity, together with the [source paper's niche biology](https://doi.org/10.1126/science.aam6603).
No local observation measures secretion, spatial contact, IL-1 responsiveness
or a lineage-linked state sequence. GSE262927 is also used by Niethamer
follow-ups, so those analyses do not independently corroborate this branch.
The single eligible baseline and day-11 AT2 units and first injured sample at
day 6 prevent an acute source-switch inference.

**Rivals and discriminating evidence.** Source populations may differ in
location, matrix or other trophic signals; epithelial competence alone may
explain the sequence; Wnt2/Wnt4 RNA could simply mark those contexts. Resolve
source identity and proximity independently of the nominated transcripts,
measure current epithelial Wnt and IL-1 responses separately from reporter
history, and compare lineage-linked mature descendants across independent
biological units. A verified source-specific change in the sequence at
comparable receiver competence would support the proposed modifier. Mere
co-expression or a failed activity assay would not decide it.

**Review decision.** Accept as a **conditional, untested candidate under A4**;
no new global ID and no claim promotion. Do not nominate a specific Wnt ligand
as mechanism before ligand-specific functional evidence exists. The external
cohort's unresolved gates remain in force.

## Other proposed transfers

| RQ / proposed transfer | Decision |
|---|---|
| A4: acute injury induces epithelial autocrine Wnt | **Not established.** Baseline Wnt7b detection and late first sampling cannot test acute induction; Porcn/Wls RNA does not establish secretion or an autocrine loop. |
| A8/A19: Wnt-response markers predict mature AT1 output or retained AT2 reserve | **Context only.** Distinct marker dimensions motivate separate measurements, but Nb1 has no mature-descendant or reserve endpoint. Existing canonical cards already require them. |
| A20: Wnt2/Wnt4 expression establishes Fzd2 dependence | **Reject this inference.** Ligand-source expression does not establish receiver receptor requirement, comparable perturbation or functional epithelial support. |
