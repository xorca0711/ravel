# A30: literature context and hypothesis schematic

Revised 7 October 2026 during the PR140 audit at the owner's request. This bounded
update replaces the 5 October framing; the earlier record remains in Git and the
[source derivation](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/rq_derivation/README.md).
Outcomes were exposed. Scientific acceptance remains unrecorded.

## Published starting point

| Primary study and inspected locator | Consequence for A30 |
|---|---|
| [Wang, Wagner, Fessler et al., Cell Reports 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12443480/), human-MS Results, Figure S4 and STAR Methods | The human analysis transports mouse-derived programmes to GSE138266 and compares disease groups. A30 asks a different, paired compartment question; it does not test the murine PGAM mechanism. |
| [Schafflick et al., Nature Communications 2020](https://doi.org/10.1038/s41467-019-14118-w), abstract and GSE138266 identity; full text inaccessible in this pass | CSF-associated composition and expression were already described. This is the same dataset, not independent replication. No new full-methods verification is claimed. |
| [van Puijfelik et al., EBioMedicine 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13264205/), indexed full-text Results/Figures 2–3 and functional-assay sections | A CCR5-high Th17.1 population is enriched in paired CSF. Post-natalizumab reduction concerns **blood**, not longitudinal CSF. This supports a concrete trafficking/composition alternative. Its IFN-γ/GM-CSF and cytotoxic features make an IL-17-only follow-up incomplete for this subset. |
| [Hayashi, Mittl et al., Nature Immunology 2026](https://www.nature.com/articles/s41590-025-02412-3), Figure 1 and paired RNA/TCR methods | Paired repertoire measurements address clonal overlap. The major antigen-specific work concerns CD8 cells and does not validate A30's CD4 programme. Check reused-cohort provenance before claiming independent validation. |

Compartmentalisation is a premise. The remaining question is whether the RNA
association persists after credible adjustment for activation and cell state.
Shared TCR does not demonstrate residence, migration direction or local induction.

## Repository observation

Read the [v3 erratum](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/A30_ERRATUM.md)
and [artifact audit](../../docs/audits/2026-10-07-pr140/REPORT.md) before the original
plan. Corrected pro-inflammatory contrasts are +0.0558/+0.0498/+0.0570 with BH
0.0321/0.0368/0.0321 against the implemented size-only null. Residual activation
persists. Regulatory non-significance does not show equivalence. The decomposition
is descriptive and depends on common-state support.

The earlier Wp-R4 disease contrast did not reproduce the published pattern under
this repository's gate and scoring implementation. That is a bounded reproduction
result, not a refutation of all human findings or of the paper's mouse mechanism.

## What this question could add

A measurement-validation and biological-context extension: determine whether a
CSF-associated programme has information beyond measured activation and subset
mixing in a donor-paired comparison. A robust association, attenuation after
adjustment or an unresolved estimate can each be informative. A new causal
mechanism or treatment claim is not required to make the comparison useful.

## Current hypothesis and rival

In paired CSF and blood, the inflammatory RNA programme remains higher in CSF
within comparable CD4 T-cell states after accounting for measured activation and
composition. Regulatory-associated RNA is evaluated separately, without presuming
unchanged regulatory function.

Residual activation and selective trafficking/subset or clonal composition are
biological alternatives; gating, depth and module/null construction are measurement
threats. These can coexist. Comparison tuple: human putative CD4 T cells; paired
CSF/PBMC samples; compartment contrast rather than intervention; timing incompletely
qualified; donor as unit; RNA programme difference as endpoint. A new cohort must
establish CD4 identity, paired timing, clinical covariates and assay validity.

## What the comparison would teach

| Outcome | Permitted interpretation |
|---|---|
| Difference persists with good activation balance, lineage and common-state support | Residual association beyond measured adjustment; unmeasured confounding and trafficking remain. |
| Difference attenuates after adjustment | Measured activation/composition accounts for part of the contrast under that model; no sole cause is established. |
| Estimate is unstable or imprecise | Unresolved, not no effect or equal regulatory function. |
| Paired protein/TCR supports a within-subset pattern | Better phenotypic/clonal resolution; shared clones still do not prove residence or induction. |
| A justified later intervention changes a functional endpoint | Causal inference limited to that intervention/model and its controls. |

Conditioning on activation may remove a mediator as well as confounding: adjusted
and total compartment associations are distinct estimands. Neither RNA contrast
identifies the effect of moving the same cell between compartments.

## Hypothesis schematic

![A30 proposed comparison and conditional extensions](schematics/hypothesis_v2.svg)

[Editable v2 SVG](schematics/hypothesis_v2.svg) supersedes the framing in
[v1](schematics/hypothesis_v1.svg), which is preserved. Shapes/arrows are qualitative.
Existing observations and conditional measurements are separated; no measured
figure is recategorized as an explanatory schematic.

## Next literature check

The [search/access log](../../docs/audits/2026-10-07-pr140/LITERATURE_SCAN.md) records
actual queries, versions, locators and failures. The 5 October scan is reused for
unchanged premises. Full Schafflick methods access, 2026 cohort-overlap qualification,
and assay/perturbation review for a chosen extension remain pending. No exhaustive
search, novelty certification or laboratory readiness is claimed.
