# Analysis pipeline: reproduce, distinguish, extend

**Source-informed plan v1, 1 October 2026; analysis ID Nb3.** The owner subsequently
authorized execution. The [execution contract](config/Nb3_execution_v1.json)
and [source-panel amendment](config/Nb3_panel_amendment_v1.json) were recorded
before the corresponding new fits. The initial plan below preserves the original
scope after paper reading and A10/A2 exposure; it is not unseen-data preregistration.
Source claims below are reproduction targets, not automatically repository results.
See the current [reproduction review](reports/REPRODUCTION_REVIEW.md) for measured
outputs and stage-specific holds.
The machine-readable stage graph is [pipeline.json](config/pipeline.json).

## Reproduction stages

| ID | Purpose and source target | Deliverable | Gate / interpretation ceiling |
|---|---|---|---|
| Nb3_00 | Audit sources, aliases, source tables, units and existing work | Source hashes; library/target/species manifest; discrepancy log; prior-exposure map | Initial inventory done; full assay intake remains open |
| Nb3_R1 | Reconstruct Fig. 2A–C/F growth phenotypes from deposited imaging | Per-target count, mean-size and covered-area effects against matched-plate TIGIT; source comparison table | Source-model numerical reproduction only; split wells cannot provide independent-preparation inference |
| Nb3_R2 | Recover the species-separated RNA and source QC/DE pipeline | Per-species retention waterfall, normalization audit, target/reference design and DE tables | Full workbook, species identities and control joins required; no scRNA clustering of bulk wells |
| Nb3_R3 | Recover epithelial axes and modules, Fig. 3 / Fig. S7 | Source cPCA, signature map, ICA stability/matching and budding/Slc34a2 comparison | Missing original settings or gene sets produce partial reproduction, not invented exact replication |
| Nb3_R4 | Reproduce growth/identity-associated fibroblast programmes, Fig. 4 / Fig. S8 | Paired well summaries, growth-versus-identity contrasts, source heatmap reconstruction | Distinguish selected-gene source display from new independent tests |
| Nb3_R5 | Recover Fig. 5 / Figs. S9–S10 spatial and non-AAV context | Sample/animal map, region-composition summaries, source-method and animal-level views | Treatment and bin/region discrepancy unresolved; no pooled-bin biological p-values |
| Nb3_R6 | Integrate reproducibility and nominate extensions | Figure-by-figure reproduced/partial/unavailable ledger, negative results and next measurements | Separate author evidence, our computation and inference; no automatic C-register upgrade |

### Nb3_00: finish design recovery first

Reuse the [P1 crosswalk](../../docs/roadmap_runs/2026-09-27/P1_library_crosswalk.tsv)
and [A10 audit](../../RQ_Specified/A10_organoid_growth_outcome/reports/FOLLOWUP_DESIGN_REPORT.md).
Keep all 886 library records; account for the 885 paired imaging wells, 203
deposited target labels, 15 RNA plate-repeat groups, four plate layouts, and
30 tdTomato libraries without guide rows. Do not turn any of these counts into
biological n. Reconcile candidate/control counts and aliases against S1/S2.

Build an explicit source-to-analysis feature crosswalk for NKX21/NKX2-1,
CTNNB1-active and ATP6V0E, using species and stable identifiers. Check other
figure/text spelling differences (for example the hypoxia-panel gene) against
assayed features before freezing signatures. Maintain missing versus zero.
Inspect supplementary tables and software availability, not expression trends,
to resolve source settings. Any author-code recovery gets a pinned version.

### Nb3_R1: imaging reproduction

Use deposited day-7 and day-14 measurements; preserve the segmentation label
and every exclusion. SI p. 3 centers/scales by plate and fits each target
against same-plate TIGIT. Recover the exact day handling, scaling population,
design matrix and BH family before matching the published effects. Record
any remaining ambiguity as a named reproduction variant, without choosing the
variant closest to the figure after inspecting results.

Keep organoid count, mean segmented size, bounding-box union coverage and
morphology distinct. Raw images/embeddings are required to reproduce SAM/cPCA
morphology; tabulated size/coverage alone cannot reproduce dense/cystic/budding
classification. Do not transform the deposited area twice. Source-model
intervals can be compared to the paper but must be labeled as its well-level
model, with independent preparation uncertainty unavailable.

### Nb3_R2: species RNA and differential expression

Start with deposited full gene-level **read counts**. Smart-seq3 here does not
license treating the values as droplet UMIs. Audit dimensions, library IDs,
nonnegative count semantics, stable gene IDs and duplicate symbols.

Source SI p. 4 keeps mouse libraries with at least 7,500 detected genes and
human libraries with at least 10,000, normalizes by TMM, and fits per-target
limma-voom models with plate and in-plate TIGIT/tdTomato references. It uses
average expression >1.5 for further analyses and cameraPR on t-statistics.
Recover the precise detected-gene definition, expression scale, gene-filter
timing and design coding before execution. Species-specific retention and the
paired intersection must be visible. Check rank/estimability rather than
assuming plate adjustment resolves target-position or preparation confounding.

Only exploratory cPCA inputs receive the source plate-effect removal; do not
feed batch-corrected expression back as raw counts to the DE model. Preserve
the source control combination and separately label any TIGIT-only sensitivity.
No de novo fold-change or significance threshold is chosen from paper plots.

### Nb3_R3: epithelial programmes and ICA

Recover the exact cPCA inputs, Tigit background, contrast parameter and signature
aggregation. Source methods select 3,000 variable genes with scran and run scPCA.
The ICA path is limma-voom t -> `zscoreT` -> JADE, not logFC -> generic FastICA.
S6 is target-by-component activity; S7 contains per-component gene projections.
Their 20 components do not settle the original rank-selection rule,
orientation, scaling or module-membership cutoff; recover these before use.

Compare components by aligned loadings/activity and gene overlap, allowing
sign and permutation changes. ICA5/8/12/13/17/18 are source IDs, not guaranteed
labels in a rerun. Prespecify rank/seed stability diagnostics where appropriate.
Retain source markers as display panels; full provenance-backed signatures
are required for module-level claims. No pseudotime is fitted to wells.

### Nb3_R4: the central epithelial-to-fibroblast comparison

Recover the source high/low-growth grouping, Nkx2.1 treatment, gene selection
and transformations before Fig. 4G. Quantify paired epithelial identity/gastric,
growth, fibroblast lung-associated, chemokine, wound-response and metabolic
programmes. Record human-compartment depth and species assignment quality.

NKX2.1, BECN1 and KEAP1 provide identity/stress contrasts; TRP53, CDKN2B and
CTNNB1-active provide candidate growth-with-retained-identity contrasts. These
are nominated from the paper, not randomized matched controls. Confirm design
overlap and measurement reliability. If identity is effectively carried by
one target, a multi-covariate model cannot identify a general identity effect.
Use leave-target-out and leave-plate-out diagnostics only when estimable.

Growth is downstream of perturbation. Report total target-associated contrasts
before any growth-conditioned comparison; conditioning changes the estimand
and can introduce bias. A conditional residual is neither mediation nor a
direct effect. Gene sets selected by the same source contrasts are descriptive
reproduction sets, not held-out validation features.

### Nb3_R5: spatial and external source evidence

Resolve GSE307128 sample/block/animal, bleomycin/AAV, timing and physical grid
mapping first. Reuse processed ZARR/RCTD weights if provenance supports them;
do not retrain scVI simply to recreate an attractive map. SI p. 5 uses 8-micron
bins, RCTD doublet mode, >=75 transcripts/spot, and >20% phenotype weight to
define enrichment. The threshold was chosen empirically in the source; it is
not an independently validated biological boundary.

Source logistic/bin-neighborhood analyses may be reconstructed for method
comparison. Biological interpretation must show each animal/section, shared
neighborhoods and spatial dependence. Two reported animals per group support
a limited descriptive comparison, not significance rescued by thousands of
bins. The source's inferred second-cell neighbor is a mixture-based estimate.
Sensitivity to reference labels, bin/region size and depth is required.

Toth's conditional-Nkx2.1 single-cell data are already used by the paper and
its reference: reproduce that arm with the actual animal design, and label it
as previously exposed source evidence. New validation requires a separate
cohort/endpoint whose selection and exposure are documented.

## Extension cards

Priority 1: E1/E8 as one analysis with distinct outcome families, then E2.
Priority 2: E3/E4 after reliable modules. E5/E6/E7 start with feasibility;
their strongest questions require additional measurements. These are proposed
tests, not authorization inferred from old plans or completed conclusions.

| ID / owner item | Question and proposed endpoint | Controls, rival explanation and stop condition | Shared question link |
|---|---|---|---|
| E1 / 1 | Does identity loss associate with a selective fibroblast chemokine/immune-support programme change beyond a generic growth response? Estimate paired target-associated programme changes, then a separate growth-conditioned diagnostic | Compare E8 outcomes and non-identity growth targets; control depth in both compartments. If target/design overlap or gene coverage fails, keep descriptive. No immune-function claim from organoid RNA | [A13](../../RESEARCH_QUESTIONS.md#a13) |
| E2 / 2 | Do IFN-rich and hypoxia/gastric-rich Krt8-associated programmes remain distinguishable within comparable epithelial states across donors/times? Freeze disjoint source-backed scores and quantify joint distributions | Adjust/check AT2 identity, cycle, depth and composition; independent signatures and sample-level contrasts. Fate interpretation stops without lineage/recovery/AT1-function endpoints. Current screen is bulk | [A1](../../RESEARCH_QUESTIONS.md#a1), [A8](../../RESEARCH_QUESTIONS.md#a8) |
| E3 / 3 | Do Elovl1/Atp6v0e effects resemble the Wnt/budding module or a broader stress/growth response? Compare fixed component profiles and AT1 programme changes | CTNNB1-active/CSNK2A1 are source positive patterns; FZD5/PORCN opposite-direction controls. No mechanism ranking if edits, morphology or module mapping are unresolved | [A4](../../RESEARCH_QUESTIONS.md#a4), [A10](../../RESEARCH_QUESTIONS.md#a10) |
| E4 / 4 | Is Slc34a2 associated with an identity/transition programme distinct from generic growth suppression? Estimate fixed ICA5/AT2/AT1/stress pattern contrasts | Growth-decreasing controls, exclusion of the targeted gene from its score, and independent SLC34A2 disease evidence. One guide pool cannot establish transport mechanism or human fibrosis causation | [A1](../../RESEARCH_QUESTIONS.md#a1) |
| E5 / 5 | How do normal AT2/AT1 receptor expression and cancer ERBB2/3 dependence differ? Separate donor-level expression from release-pinned cell-line dependency summaries | Resolve 93/96 denominator, assay and lineage, copy number/expression and growth-rate confounding. Cell lines are not proof of AT2 origin; no inference of pulmonary toxicity or AT1 function from these endpoints | [A8](../../RESEARCH_QUESTIONS.md#a8), [A10](../../RESEARCH_QUESTIONS.md#a10) |
| E6 / 6 | Which compartment/context accounts for the EGF requirement? First audit receptor detection, editing evidence and medium, then seek compartment-selective evidence | Read A2/P1 first. EGFR RNA absence/null screen effects do not establish dispensability. Without validated recipient-specific perturbation and measured outcomes, stop at an unresolved compartment requirement | [A2](../../RESEARCH_QUESTIONS.md#a2), [A12](../../RESEARCH_QUESTIONS.md#a12) |
| E7 / 7 | Does epithelial growth associate with fibroblast heterogeneity after separating identity and cell composition? Use fixed fibroblast state/composition endpoints in eligible single-cell/spatial data | Bulk programme changes alone cannot quantify heterogeneity. Compare lung-associated and CTHRC1 programmes, depth, injury and immune context; require independent samples and coverage | [A10](../../RESEARCH_QUESTIONS.md#a10), [A13](../../RESEARCH_QUESTIONS.md#a13) |
| E8 / 8 | Which lung-associated fibroblast programmes change with epithelial identity while generalized wound programmes persist? Compare prespecified paired programme effects | Share E1 data/model, avoid duplicate testing. Lung-specific requires tissue/context comparators; PLIN2 alone does not establish a lineage. Contact versus soluble signaling remains unresolved | [A13](../../RESEARCH_QUESTIONS.md#a13) |

## Execution and decision rules

- No pseudoreplication: wells, spots, cells and animals are different units.
  Resolve biological replication before inferential models; report descriptive
  source-model effects when that resolution is impossible.
- Freeze feature membership, coverage minimums, cell floors, matching,
  covariates, depth controls on both paired variables and endpoint families
  before a new endpoint. Inherit an existing contract only when applicable;
  unresolved thresholds remain null in the draft configuration.
- Record every inspected cohort and previous result. Leave-one-plate-out is
  combined target/plate distribution shift here, not independent-preparation
  validation. Do not select a signature and claim confirmation on the same data.
- Use source methods for reproduction and separately named repository
  sensitivities. Keep sign reversals, missing inputs, nonestimable contrasts
  and incomplete reproduction in the final ledger.
- Put new numerical outputs in a versioned, non-overwriting run directory with
  command, environment, config/input/output hashes and a figure-caption unit.
  Figures follow successful calculations; no mock result figures are evidence.
- Optional arms do not block unrelated work. A held spatial stage does not
  prevent organoid source reconstruction; it prevents spatial validation claims.

**Current next work after v1:** reconcile the human S5 numeric fields against
their direction summaries using original source code/mapping or a corrected
table; preserve the failed comparison. Count recovery, contracts and the first
descriptive pass are complete. Exact cPCA/JADE settings, spatial design and
external annotations remain separate gates. See the
[current review](reports/REPRODUCTION_REVIEW.md). No A10 re-fit, clinical
conclusion or experimental protocol is implied by these next steps.
