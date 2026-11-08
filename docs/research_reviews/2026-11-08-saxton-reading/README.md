# Saxton IL-10 / IL-22: reading and computational scope

**Execution follow-through:** [IL-10 completed results and holds](../../../Research%20Article/ungated_saxton_2021_il10/RESULTS.md)
and [IL-22 Osmr results](../../../Research%20Article/gate3_08_saxton_2021_il22/osmr_v1/RESULTS.md)
now own the numerical status. The planning record below remains historical.

8 November 2026 (Asia/Seoul). Documentation review against fetched main
`32ab85e87bee788e62bec4e1b7ce5bad6df84d30`. No new biological analysis, execution
contract, canonical RQ or scientific acceptance is created. The current
Sx22-P01 results supersede the execution status in the
[31 October reading assessment](../2026-10-31-saxton-il22/README.md).

**Follow-up planning:** [stepwise IL-10 plan](IL10_ANALYSIS_PLAN.md),
[additional IL-22 work](../../../Research%20Article/gate3_08_saxton_2021_il22/FOLLOWUP_ASSESSMENT_20261108.md)
and [refreshed literature context](LITERATURE_CONTEXT.md). These are proposals,
not new runs. The initial access record below is supplemented by that context.

## Reading judgment and source distinction

Both papers merit reading for the connection between receptor engagement,
recipient context, intracellular signaling and function. Detailed structural
methods are optional for understanding that biological argument.

- **IL-10:** Saxton et al., *Science* 371, eabc8433 (19 March 2021),
  [DOI](https://doi.org/10.1126/science.abc8433). The supplied 13-page PDF contains
  the summary, main paper and methods. The structure uses cryo-EM at 3.5 angstrom.
  Prioritize Figures 3-5: receptor-dependent cellular responses, myeloid
  suppression and T-cell outputs. Figures 1-2 explain the perturbation design.
- **IL-22:** Saxton et al., *Immunity* 54, 660-672.e9 (13 April 2021),
  [DOI](https://doi.org/10.1016/j.immuni.2021.03.008),
  [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8054646/).
  The local 23-page published PDF includes STAR Methods. Its stabilized complex
  was solved by X-ray crystallography at 2.6 angstrom. Read Figures 4-5 closely,
  then 6-7 and their methods; Figures 1-3 establish how the perturbation works.

The IL-22 PDF's Figures 3-7 (PDF pp. 6-10) were visually inspected during this
review. Selected Results, Discussion and methods passages were read in both
papers; this is not an exhaustive supplement audit.

## What the comparison actually shows

| Feature | IL-10 | IL-22 |
|---|---|---|
| Main biological separation | Myeloid suppression versus T-cell stimulation, with different cellular response thresholds | STAT bias within responsive cells plus different activity across tissues |
| Shared receptor contribution | IL-10Rbeta availability modifies sensitivity to ligand affinity | IL-10Rbeta availability shifts the STAT response window across recipient contexts |
| Intracellular evidence | pSTAT3/pSTAT1 responses and downstream function; STAT1 mediation of IFN-gamma is interpreted with prior evidence | Figure 4 tests receptor phosphorylation and receptor mutants, supporting distinct STAT recruitment requirements |
| Functional evidence | Inflammatory cytokine suppression and selected T-cell outputs; acute mouse sepsis model | Organoid metabolic viability, irradiated intestinal crypt measurements, acute pancreatic injury markers and inflammatory outputs |

IL-22 is not a purely within-cell counterpart to cross-lineage IL-10. In Figure 5,
22-B3 retains strong STAT3 bias in colon, weaker bias in pancreas and little
detectable activation in liver/skin. Antagonism is demonstrated in HepG2 cells;
absence of tissue activation alone is not an antagonism assay. The receptor
expression perturbation in Figure 5I supports a role for IL-10Rbeta availability;
whole-tissue receptor RNA is not a cell-resolved surface-protein measurement.

Figure 4 adds a mechanistic distinction: STAT3 can associate with the IL-22Ralpha
C-terminal domain independently of receptor phosphotyrosines, whereas STAT1
depends on receptor phosphorylation. The Y-to-F and C-terminal-deletion receptor
comparisons support different activation thresholds. The ligand variants exploit
existing recruitment modes; no newly engineered intracellular docking site is
required. A generic affinity-times-density description alone misses this evidence.

The IL-10 Discussion describes stronger super-10 STAT1 activation as a likely
explanation for enhanced IFN-gamma and cites prior STAT1 evidence. That is more
specific than an incidental correlation, but is not a new isolated STAT1
necessity/sufficiency experiment in this paper. Likewise, STAT3 is not universally
protective: the IL-22 Discussion identifies STAT3-dependent hepatic acute-phase
outputs as an inflammatory route. Selected acute protection does not establish
durable regeneration or chronic safety.

Use the existing [source-panel correction](../../../Research%20Article/gate3_08_saxton_2021_il22/SOURCE_CORRECTION_2026-10-31.md)
when reading: the visible Figure 5H is receptor qPCR and 5I is receptor-expression
immunoblotting; Figure 7G is labelled liver and 7H skin. Caption references contain
inconsistencies. No numerical reconstruction from those panels was attempted.

## What ravel already established for IL-22

The registry locates Sx22-P01 and its
[current results](../../../Research%20Article/gate3_08_saxton_2021_il22/reassessment_v1/RESULTS.md),
[gallery](../../../Research%20Article/gate3_08_saxton_2021_il22/reassessment_v1/FIGURES.md)
and [review](../../../Research%20Article/gate3_08_saxton_2021_il22/reassessment_v1/ORIGINATING_REVIEW.md).
These are exposed reanalyses of the paper's source data, not independent replication.

- GSE160217 contains six deposited colon libraries for PBS, WT IL-22 and 22-B3
  at six hours. The completed description includes source QC, fixed author
  memberships, two broader IFN memberships, three expression scales and
  individual-library omission sensitivities.
- The primary median direct B3-minus-WT differences are **-1.345** for the
  seven-gene selected IFN panel, **-0.459** for the six-gene tissue-protection
  panel and **-0.163** for each broader IFN membership. These are gene-wise
  differences of group means of log2(CPM+1), not animal-level fitted log-fold
  changes, independent replicates or tests of equivalence.
- A broad response reduction accompanies the selected-panel pattern. The
  Reg3b/Reg3g/Muc1 RNA subset is sensitive to library omission. The result
  supports a bounded transcriptional distinction, not proof of preserved function
  or a genome-wide STAT1/STAT3 switch.
- The [Choi recipient-context description](../../../Research%20Article/gate3_08_saxton_2021_il22/recipient_context_v1/RESULTS.md)
  found only two single-count Il22ra1 detections among 11,683 retained cells in
  pooled libraries. It cannot rank responsive lung cell states; zero capture
  does not prove receptor absence. More scoring of that matrix does not resolve
  the missing protein or response measurements.

Population inference remains held on unit/allocation evidence. Exact author
processing replay, raw signaling/function reconstruction and exposure-to-later-
function linkage retain their separate requirements in the
[current ledger](../../../Research%20Article/gate3_08_saxton_2021_il22/COMPLETION_LEDGER.md).
The historical platform failures are not a current blanket execution hold.

## Useful next computational scope

The most direct additional reading companion is **IL-10 GSE160332**. The
[GEO series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160332) and
[BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA672965) describe human
CD8 T cells activated for three days, then exposed to PBS, WT IL-10, super-10 or
10-DE for 24 hours. GEO lists eight libraries and processed read-count and FPKM
files. This review did not download matrices or qualify sample-code mapping,
donor independence, pairing, batches or treatment doses. Library suffixes do not
establish those facts. No IL-10 execution package was located in the current
registry/article index during this bounded check.

**Purpose:** describe how the variants alter the activated CD8 transcriptional
response, including whether selected inflammatory targets differ from broader
response attenuation. This is a source-reproduction question, not a novelty claim.
**Comparison:** 10-DE versus WT and super-10 versus WT, with each versus PBS for
context. **Biological unit:** original human donor/preparation, pending mapping;
the descriptive measurement unit can remain the deposited library if mapping is
unresolved. **Endpoint:** RNA abundance at 24 hours. **Validity threats:** sparse
replication, donor/processing confounding, panel selection and general attenuation.

A bounded future package would qualify metadata first, then show per-library
expression and direct contrasts for the published Figure 5 targets, followed by
fixed broader memberships and limited normalization/omission sensitivities.
Gene mapping and measurability must precede target interpretation. The contract
must record prior exposure and preserve all outcomes. Population tests require
the relevant unit/design evidence; a fixed two-library count is not itself a
proof of independence or a universal prohibition on exploratory differential
expression.

If selected differences persist across broader memberships and sensitivities,
that supports further examination of transcriptional selectivity. If they mainly
track attenuation, or depend on individual libraries/panel choice, narrow the
conclusion. Mixed findings remain informative. None of these outcomes demonstrates
STAT1 causality, secretion, cytotoxicity or preserved myeloid suppression: the
deposit contains CD8 cells, not the myeloid comparison. D25K is not a listed arm.

Further IL-22 work should reopen a specific held comparison when its missing
evidence becomes available. Pooling the IL-10 human CD8/24-hour and IL-22 mouse
colon/6-hour matrices would confound cytokine with species, tissue and timing.
An annotated conceptual comparison is appropriate; a common quantitative
selectivity score is not justified. Cryo-EM movie reprocessing would answer a
different structural question and has low value for this transcriptional scope.

## Access and review record

Search/access date: 8 November 2026. Web queries included
`Saxton 2021 IL-22 tissue protective pro inflammatory decoupling receptor biased agonist`,
`GSE160332`, and an official Berkeley/Saxton research-profile query. NCBI browser
challenges prevented some direct opens; indexed GEO/BioProject records and local
published PDFs supplied the stated evidence. The existing IL-22 literature context
is reused for unchanged premises. No new RQ, experiment package, comprehensive
literature refresh or novelty clearance is claimed. Private reading/career notes
and account information are not copied into this repository record.
