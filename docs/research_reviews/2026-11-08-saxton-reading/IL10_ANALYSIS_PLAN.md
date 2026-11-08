# IL-10: stepwise source-analysis plan

**Execution follow-through:** [IL-10 completed results and holds](../../../Research%20Article/ungated_saxton_2021_il10/RESULTS.md)
and [IL-22 Osmr results](../../../Research%20Article/gate3_08_saxton_2021_il22/osmr_v1/RESULTS.md)
now own the numerical status. The planning record below remains historical.

8 November 2026. Requested planning work, **not an executed analysis or frozen
contract**. This review folder holds the proposal until source intake establishes
its article package and registered article-local owner. No global A identifier or
roadmap position is assigned. [Review](README.md) · [Literature context](LITERATURE_CONTEXT.md) ·
[IL-22 follow-up](../../../Research%20Article/gate3_08_saxton_2021_il22/FOLLOWUP_ASSESSMENT_20261108.md).

## Biological purpose and executable question

The organizing question concerns separation of myeloid suppression from
lymphocyte stimulation. GSE160332 supports only the CD8 RNA part:

**In activated human CD8 T-cell libraries, does 10-DE mainly weaken the WT
transcriptional response, and does super-10 amplify that same response or alter
the relative responses of particular genes?**

The paper already reports weaker 10-DE responses and mixed super-10 responses:
IFNG/IL18RAP increase more, whereas GZMB/IL22/SOCS3 increase less than with WT
in the presented RNA comparison. These are exposed reproduction targets.
General attenuation, selected-gene presentation, donor/processing confounding
and library sensitivity are consequential alternatives. Stronger affinity is not
assumed to increase every transcript. The contribution is source verification and
interpretation, not a novel mechanism or independent biological replication.

| Field | Planning specification |
|---|---|
| Source | Saxton 2021 Science, Figure 5A/B, S9 and relevant methods; GSE160332 |
| System | Human CD8 cells activated with anti-CD3/CD28 for three days, then treated for 24 hours according to GEO; exact assay-specific conditions to cross-check |
| Arms | PBS, WT IL-10, super-10, 10-DE; eight deposited libraries, two labels per arm; explicit sample-code mapping still to qualify |
| Biological unit | Human donor/preparation; donor independence and repeated-donor pairing remain unknown |
| Descriptive unit | Deposited library if treatment identity qualifies; genes are features, not replicates |
| Primary contrasts | 10-DE minus WT; super-10 minus WT |
| Context contrasts | Each of WT, 10-DE and super-10 minus PBS |
| Endpoint | RNA abundance and fixed-membership summaries at 24 hours |
| Limits | No myeloid suppression, receptor protein, pSTAT activity, secretion, cytotoxicity, kinetics or persistence measurement |

## Reading needed

Read the biological Results through Figures 3-5 and their legends, plus the
relevant culture, phospho-flow, functional-assay and RNA methods (supplied PDF
pp. 5-8 and 10-11). Figure 5A/B is RNA; 5C/D is separate functional evidence.
Obtain S9 before claiming exact reproduction. Read Figures 1-2 conceptually to
understand what was perturbed; detailed cryo-EM processing is needed only for a
structural job. Figures 3-5 were visually checked in this planning review.

Arm coverage matters: **D25K is not a deposited RNA arm, and Figure 4E sepsis
survival tests WT and 10-DE, not D25K.** Record doses, times and donor sets for
each assay separately. Partial reading permits metadata inventory; a complete
biological Results read is strongly recommended before interpreting selectivity
or choosing a follow-up. This is advice, not a new repository-wide reading gate.

## Sequential analysis stages

| Stage | Work and deliverable | Decision / stop rule |
|---|---|---|
| **0. Evidence map** | Map Figure 3-5 claims to variant, cell, dose/time, assay, unit and source file. Inspect S9 and exact RNA methods. Record outcome exposure and current literature. | Reading can proceed with missing raw data. Do not call an assay reproduced without the appropriate source. |
| **1. Source/unit qualification** | Establish the article-local owner/package and freeze a metadata contract. Recover GEO/GSM/BioSample/SRA metadata, count/FPKM files and annotation; hash sources. Map Unt/BS-coded labels using explicit treatment attributes. Produce a sample/assay crosswalk. | Treatment identity must qualify for contrasts. Unknown donor pairing restricts inference but need not stop library description. Suffixes do not establish donor identity. |
| **2. Technical eligibility** | Check dimensions, library totals, count type/range, stable IDs, repeated symbols and all-zero rows; inspect library relationships as QC. Reuse stage 1 mappings. | Document a technical correction or hold. QC clustering is not proof of independent donors; unfavorable samples are not automatically excluded. |
| **3. Figure 5 RNA description** | Freeze a descriptive contract and exact Figure 5A/B memberships. Retain every library value and compute the five contrasts above. Display fixed targets with missing/ambiguous mappings explicit. Figure 5B targets: IFNG, IL18RAP, IL9, GZMB, CCL1, CCL17, CCL22, SESN3. | Call this adapted source description unless author processing is fully recovered. No invented zeros, favorable substitutions or transfer of RNA results to ELISA. |
| **4. Attenuation/pattern robustness** | Evaluate 10-DE and super-10 separately using a fixed expressed-gene background, source targets and a small fixed set of human IFN memberships if qualified before freeze. Report membership overlap/member disagreement. Compare primary expression, count-normalization sensitivity and deposited FPKM; retain full data and each single-library omission. | No further signature search to rescue agreement. Omission ranges are not confidence intervals. Shared-PBS response-vector residuals are descriptive, not causal STAT effects. |
| **5. Conditional population inference** | With verified donor/preparation units and an identifiable allocation/design, specify an appropriate count model, paired terms if justified, contrast families, uncertainty and FDR. | Two library labels neither prove independence nor universally prohibit exploratory DE. Unknown units/confounding/precision restrict claims. No equivalence without justified margin and precision. This stage is optional for a useful descriptive report. |
| **6. Synthesis and review** | Compare RNA with published pSTAT/function evidence while preserving assay/sample distinctions. Verify joins, arithmetic and plotted values; visually review figures. Deliver results, limits and all stage dispositions; update PROGRESS. | Numerical verification is not biological replication or human acceptance. Preserve discordant and unfavorable outcomes. |

Stage 4's future contract must specify feature universe, low-count filter,
normalization, pseudocount, symbol resolution, membership versions and summaries.
They are not already frozen here. An amplitude reference, if used, excludes the
tested memberships and retains noisy-axis/shared-control limits. Include both
upregulated and downregulated genes: movement of a suppressed chemokine toward
PBS is weaker suppression. Do not average opposing directions into a purported
functional score. Additional gene sets must answer a stated decision before
execution, not be selected after inspecting favorable results.

## Informative outcomes

- Broadly weaker 10-DE responses support attenuation in these CD8 libraries;
  they neither measure nor invalidate separately tested myeloid activity.
- A stable subset-specific difference can nominate a later signaling question,
  but does not establish STAT1 mediation from RNA.
- Mixed super-10 effects indicate response composition rather than a simple
  monotonic strength ladder; retain genes pointing in both directions.
- Panel/library dependence narrows the reproduction claim and identifies the
  missing replication. Source/mapping failure closes only the affected stage.

## Execution requirements and bounded scope

Before a run, refresh main/registry, create the source-qualified article package
and article-local owner, and bind exact input/code hashes in a new contract with
unit, contrast, endpoint, exposure, exclusions, multiplicity and stop rule.
Freeze and commit before using the repository runner. Run `preflight`, `run`,
receipt `verify` and the base-aware research gate. Amendments use new versions
and supersession links; existing IL-22 evidence remains unchanged.

Start with processed matrices on a qualified local CPU runtime. Raw FASTQ
realignment is conditional on a concrete discrepancy that could change the
decision. No GPU, raw cryo-EM reprocessing or model training is justified here.
Expected deliverables: source/unit ledger, fixed-target figure, response-pattern
and sensitivity figure, concise results/limits, and immutable contracts/receipts
when executed. Do not add figures that duplicate the same conclusion.

An ODE/threshold model is a separate possible project. Single-timepoint RNA and
aggregate panels cannot identify receptor/turnover kinetics. Such work needs
qualified dose/time signaling data, parameter-identifiability and validation
plans, and examination of the close 2026 modeling lead. Geometry and kinase-
dependence studies also limit any universal affinity-only explanation.
