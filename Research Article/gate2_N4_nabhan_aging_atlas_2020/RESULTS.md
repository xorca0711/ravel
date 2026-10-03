# Nb5 first analysis: results and branch decisions

3 October 2026. **Bounded, outcome-exposed descriptive analysis completed;
scientific acceptance is not assessed.** Read this report and the amendments
before the original plan. The owner's handwritten note remains context, not
an independent dataset. [Figures and captions](FIGURES.md) provide six plates;
[execution validation](EXECUTION_VALIDATION.md) records checks.

**Later stage:** [biological extension results](EXTENSION_RESULTS.md) and
[figures 7–10](EXTENSION_FIGURES.md) add within-type/composition and local-repertoire
comparisons. This report preserves the first-pass endpoints and values.

## What this analysis establishes

The deposited data support mouse-level descriptions of captured composition,
RNA measurement, microglial cluster occupancy and reconstructed T-cell
clonality. They do not yet establish a distinct intermediate microglial state,
Alzheimer-related function, a conserved ageing mechanism or an age-adjusted
lung injury effect. All eight article-local branches remain available; none
has been promoted to a global RQ or selected over A0–A23.

The fixed analysis retained the full marker family and unfavorable or missing
results. There are no cell-level hypothesis tests, significance stars, fitted
count models, post hoc effect-size thresholds or confirmatory claims.

## Source qualification and permitted measurements

Five versioned Figshare objects contain 57,897 observations from bladder,
kidney, brain myeloid cells and the two lung assays. A separate author Figure 4
brain object contains 13,576 observations, many overlapping the general brain
release. These counts must not be added as independent cells or animals.
The combined metadata has 36 differently formatted deposited mouse labels;
that is not a verified count of distinct animals across assays.

All 73 tissue/assay/mouse-label records join to supplementary Table 1a or 2a;
47 cell totals differ. The five general objects have noninteger `raw.X` values
and row totals approximately 10,000. They qualify for normalized-expression
description, not raw-count likelihood models. The author brain object contains
transformed `X` only. Its all-age transformation and final-paper cluster
correspondence remain unresolved. See the [scale audit](../../analysis/research/runs/nb5_metadata_v3/layer_audit.tsv)
and [release concordance](../../analysis/research/runs/nb5_descriptive_v1/release_concordance.tsv).

Two young lung droplet labels (`3-M-5/6`, `3-M-7/8`) denote pooled samples.
They remain in source descriptions but are excluded from individual-mouse
weighting and contrast calculations. No 24-month female is represented in
these tissue objects. Lung droplet has no 24-month observations; the missing
contrast is not replaced by 30 months. Repeated tissues/assays and source
releases do not supply independent replication. Figure 1 exposes this design.

## Findings, with their rivals

### P01: composition changes survive equal mouse weighting

In bladder, the mean captured urothelial fraction rises from **44.03% at 3 months
to 75.90% at 24 months**; the mesenchymal fraction falls from **50.29% to 15.71%**
(three mice at each age). The broad ontology label `bladder cell` maps entirely
to source free annotations `bladder mesenchymal cell (Car3+)` and
`bladder mesenchymal cell (Scara5+)`, documented in the
[annotation dictionary](../../analysis/research/runs/nb5_descriptive_v1/annotation_dictionary.tsv).
Figure 2 compares individual mice, equal-mouse and pooled-cell weights.

This recovers the direction highlighted in the paper, not an exact universal
threefold change under every denominator. The strongest rival remains
differential capture and tissue composition. Captured fractions cannot show
absolute cell loss, proliferation or repair. The one-month and 18-month bladder
strata each contain one mouse and are displayed without population inference.

### P02: deposited cluster occupancy is measurable; the intermediate-state claim is held

The explicit source `microglial cell` annotation retains 4,488, 4,375 and 4,267
cells from 6, 4 and 4 mice at 3, 18 and 24 months. These differ from the paper's
4,532/4,461/4,424 panel counts. The author object additionally contains macrophage
annotations and 159 unannotated old cells. The
[annotation audit](../../analysis/research/runs/nb5_source_audit_v1/case_annotation_audit.tsv)
preserves every field rather than silently choosing labels to match the paper.

Equal-mouse occupancy of deposited Leiden labels 1/6 is 58.70%, 6.35% and 6.93%;
labels 10/12/14 occupy 0.50%, 1.28% and 6.77%. Thus importing the paper's named
cluster interpretation into this deposit is not yet justified. Figure 3 is
explicitly a **deposited-label concordance audit**, not a reconstruction of the
paper's old-state fraction. No cluster numbers were remapped using observed age.
The UMAP was supplied by the authors, not newly fitted here.

The source notebook concatenates 100 old-up and 100 young-up genes. That exact
selection intersects the 500-row deposited disease list in **56 unique genes**,
whereas the manuscript reports 55. The earlier one-direction arithmetic is
superseded only for source interpretation by the
[bidirectional audit](../../analysis/research/runs/nb5_source_audit_v1/source_audit.json).
Neither overlap is independent validation: both lists and the published
relationship were already exposed. A distinct state versus changing mixture
has **not** been tested. Required next evidence is an exact final-figure cell
and cluster map plus qualified unintegrated all-age expression, followed by a
prospective mouse-held-out comparison. Independent disease/control data and
functional outcomes would be separate later requirements.

### P03–P05: lung and organ context support measurement questions

Lung FACS all-cell Cdkn2a detection averages **0.650% versus 1.421%** at 3 versus
24 months (6 versus 4 mice). Unconditional normalized expression is
0.006125 versus 0.021784 per 10,000. The male-only detection values are 0.521%
versus 1.421% (4 versus 4 mice). Figure 4 separates detection, mean among
positive cells and mean across all cells. Two young mice have no detected
Cdkn2a and therefore no positive-cell mean; they are not assigned a zero
conditional mean. This RNA observation does not establish senescence or p16
protein. Il1b RNA does not measure cytokine secretion.

Lung composition accounting uses an equal mixture of types present in every
retained mouse, separately within assay. The eight common FACS types cover
91.34–99.01% of captured cells; the ten common droplet types cover all retained
cells. The observed mean uses all cells, while the standardized mean uses the
common types. This is an explicit descriptive reweighting with incomplete FACS
coverage, not a full decomposition or causal mediation claim. See
[accounting data](../../analysis/research/runs/nb5_descriptive_v1/lung_accounting.tsv).

Figure 6 shows a fixed marker subset with the complete family retained in
[contrast data](../../analysis/research/runs/nb5_descriptive_v1/expression_contrasts.tsv).
Brain microglia, lung macrophages and kidney macrophages have differing
directions and support. Some lung macrophage strata have very few captured
cells and only two old mice; mouse counts alone do not imply precision.
Resident identities and assays cannot be exchanged to claim conserved ageing.
`Msrb1` and `Spex1` are absent from these general expression objects; no alias
substitution was made. `Itga1` and `Itgal` remain separate genes.

No compatible injury cohort was newly qualified, so P03 provides baseline
context only. Existing A3/W1 results and negative/ineligible endpoints remain
unchanged. P04 is additionally constrained by prior work: the author repository's
`2_aging_signature` analyses support the later Zhang et al. paper on global and
cell-type-specific ageing signatures, not a new result of Nature 2020. Broad
shared-age signature discovery alone is not a substantiated novelty claim.

### P06: older reconstructed repertoires remain concentrated after depth standardization

The author-documented young-cell conversion and within-mouse clone partition
recover clonal-cell numerators **55, 479 and 348** at 3/18/24 months. The matched
source denominators are **2,076, 2,056 and 1,868**, yielding 2.65%, 23.30% and
18.63%. The manuscript denominators are 1,895/2,056/1,780; the discrepancy is
retained. Eight 18-month and three 24-month source rows lack metadata matches
and remain in the audit. All young rows match after the exact source conversion.

Equal-mouse means are **2.30%, 22.53% and 18.94%** (7/4/4 mice). At a common
depth of 60 reconstructed cells per mouse, exact expected nonsingleton
fractions are **0.62%, 8.41% and 7.82%**. Figure 5 shows all mice and unequal
denominators. The common depth is the observed minimum, not a power threshold.
The sampling calculation conditions on observed within-mouse source clone
assignments; it does not rerun receptor assembly. Tissue mixture and
reconstruction selection remain strong rivals. The result cannot establish
immune competence, antigen specificity or response to a new infection.
B-cell assembly-based clonality and whole-atlas reclustered Shannon diversity
were not reproduced in this pass.

### P07–P08: design support restricts sex and age-shape interpretation

A 3-versus-24-month sex interaction is not estimable with the missing old female
stratum. Male-only descriptions are a sensitivity check, not an interaction
test. Some 3-versus-18-month brain and kidney strata contain both sexes; that
different estimand would need its own contract and precision justification, not
a substitution chosen to rescue the missing 24-month comparison.
Cross-sectional ages are displayed categorically without an ageing-rate
model. Kidney thick-ascending-limb annotations are absent at 24 months in this
processed object but present again at 30 months; that observation must not be
called biological elimination and recovery. Annotation/capture concordance is
required before a nonlinear age-shape claim. The one-month stratum remains
developmental context; survival and cohort selection are unresolved.

## Branch disposition and next discriminators

| Branch | Current evidence | Next bounded decision |
|---|---|---|
| P01 composition/expression | Captured composition and equal-mouse sensitivity executed | Qualify absolute abundance and distinguish within-type change from capture before a mechanism claim |
| P02 owner's microglial idea | Source occupancy, marker context and list audit executed; cluster correspondence unresolved | Recover final-figure identity and all-age unintegrated scale before distinct-state/mixture comparison |
| P03 ageing/injury | Lung baseline description executed; injury transport held | Qualify compatible within-study age/injury contrasts; preserve A3's current boundaries |
| P04 organ specificity | Fixed within-population markers described; no shared-program discovery | Define a genuinely homologous population and novel discriminator after targeted prior-art review |
| P05 marker/assay | Detection/conditional/unconditional endpoints and assay coverage separated | Validate the biological endpoint; obtain raw counts only if a count model is required |
| P06 clonality/sampling | Corrected T-cell joins, clone numerators and common-depth expectation executed | Resolve denominator version and tissue/assembly selection; function requires independent evidence |
| P07 sex | Coverage audit and male-only sensitivity executed | Obtain the missing old female stratum before the planned 3-versus-24-month interaction |
| P08 age shape | All-age source descriptions executed; nonlinear/rate model held | Reconcile annotation discontinuities, cohort and survival effects before curve selection |

These are development dispositions, not human retain/reject decisions. No
meaningful biological margin, experimental model access or confirmatory
sample-size justification has been invented.

## Primary-source authority versus repository evidence

Primary sources: [Nature paper](https://doi.org/10.1038/s41586-020-2496-1),
[author manuscript](https://escholarship.org/content/qt7429b0mh/qt7429b0mh_noSplash_89b9fb4f64c194de0a3c9dd6bc608d3d.pdf?t=rvx87f),
[Figshare release v2](https://doi.org/10.6084/m9.figshare.8273102.v2), and the
[author code at 5ee7b62](https://github.com/czbiohub-sf/tabula-muris-senis/tree/5ee7b62ec7208c240634946180a8a105a7356816).
The [later ageing-signature paper](https://elifesciences.org/articles/62293)
is prior art, not independent replication of these reused samples.

Repository evidence consists of the linked output tables, frozen contracts,
receipts and verification records. [Source manifest](SOURCE_MANIFEST.md)
records exact input identities. All outcomes remain exposed. The original
plan is retained; the [execution ledger](EXECUTION_VALIDATION.md) explains
parser, identifier and source-list corrections without overwriting old results.
