# Human stage 7: proposed numerical specification

29 October 2026; exposed, descriptive observational extension, DY1-P01.
The source qualification at `952ea40` recovered 312,928 cells, 78 donors
(28 Control, 32 IPF, 18 COPD), 107 libraries and exact barcode order. Libraries
are combined within donor. No clinical age, sex, smoking, treatment, lung-function
or tissue-region fields are present in the supplied cell metadata. The separate
GEO clinical supplement recovered exact age and recorded-sex joins for all 78
donors and 107 libraries before numerical freeze. No neutrophil
annotation is present. These limitations remain even if expression estimates
are numerically precise. Numerical execution awaits technical reviewer inspection
and a committed, hash-bound contract.

## Source-defined choices and explicit adaptations

1. Preserve the deposited `Macrophage` and `Macrophage_Alveolar` labels without
   inferring anatomy. Their union is `AllMacrophages`. Exclude deposited
   `Multiplet` cells from analytical denominators; retain their counts in audits.
2. An explicitly **analyst-defined five-marker detection proxy**, `Proxy2`,
   consists of cells in AllMacrophages detecting at least two of SLC40A1, FOLR2,
   F13A1, STAB1 and SELENOP (positive raw count). Proxy1 and Proxy3 require one
   and three detected markers. These are not author cluster assignments or
   validated human NAMs. The coordinating review inspected the supplied article's
   Fig. 5j/ED9b and verified this marker list; the author reclustered myeloid cells
   into 27 populations. That model/annotation correspondence is unavailable.
   The primary narrative/figure population is the deposited Macrophage label at
   floor 20; all proxies and other labels are prespecified sensitivities.
   Thresholds are analyst choices made before expression outcomes; detection
   depends on depth. All proxy cells remain source-annotation-qualified.
3. Use the exact native-human panels below, separate from identity markers.
   Each score is the unweighted mean of gene-level log2(CPM + 1), with CPM based
   on **all** raw gene counts summed in that donor/population. This scoring rule
   is our adaptation, not claimed as an author's score or a validated function.
   Report all component genes as well as scores. No orthologue mapping is needed;
   missing/ambiguous human symbols are recorded and hold the affected panel.

| Name in this analysis | Exact genes | Primary provenance and locator |
|---|---|---|
| FABP4-associated panel | ATP10A, FABP4, SERPING1, SVIL | Apte et al. 2023, DOI 10.3390/ijms242015104, Results 2.1 and Fig. 1C; author's four-gene list, originally selected using GSE136831 |
| Matrix-associated macrophage panel | MMP9, LGMN, PLA2G7, RGS1 | Same source and locator; author's four-gene list, not an independent validation set |
| Fibroblast matrix panel | COL1A1, COL1A2, COL3A1, COL6A1, COL6A2, FN1, ACTA2 | Liu et al. 2024, DOI 10.1165/rcmb.2023-0363OC, Fig. 4B and Results on mesenchyme; seven-gene author list, here with donor pseudobulk scoring |
| DY1 highlighted human genes, individual results only | FN1, CCL18, SPP1, APOE, LPL, TREM2, CD9, MERTK, CD59, FABP5 | Damani-Yokota human Fig. 5n/ED9c, verified by coordinating reviewer from supplied paper; not the Apte panel |
| ARG1 | ARG1 | Requested measured transcript; excluded from identity and other panels |

FABP4-associated expression is at most lipid/resolution-related context; neither
panel measures resolution, secretion, matrix production, activity or benefit.
The study does not fit a mouse-derived infection signature. All five identity
genes are disjoint from outcome genes. Inherited labels and the Apte gene lists
were derived from RNA and partly the same atlas; this is not independent marker
validation. No pathway activity or causal biological role is inferred.

## Comparisons and eligibility

- **Abundance:** per donor, count Macrophage, Macrophage_Alveolar, Proxy1/2/3
  and AllMacrophages. Report fractions among all captured nonmultiplet cells,
  myeloid cells and AllMacrophages. Zero numerator is a valid zero; absent
  denominator is missing. Primary denominator is myeloid (source-paper context),
  macrophage and all-cell denominators are sensitivity analyses. Exact deposited
  label/category sets are bound in human_panels_v1.json. The myeloid denominator
  is our deposited-category adaptation, not the author reclustering denominator.
- **Expression:** donor pseudobulk within the six populations above. Primary
  cell floor is 20; sensitivity floors 10 and 50 are reported without replacing
  unfavorable primary results. Floors stabilize description and are not power
  calculations. All below-floor donor values/counts remain available.
  Compare IPF-Control, COPD-Control and IPF-COPD. Report unweighted donor means,
  medians and mean differences with 2,000 donor-resampled percentile bootstrap
  intervals (seed 20261029). Require at least three donors/group for intervals;
  otherwise retain values with an explicit insufficient-support status.
  Main panel/ARG1 measures use all floors; individual component and highlighted
  genes use floor 20. No p-values, significance labels or positive-result selection.
- **ARG1 attribution:** output raw counts, all-gene CPM and fraction of captured
  cells detecting ARG1 in every deposited annotation/donor. Report capture
  coverage first. Absent neutrophils prevent tissue-wide source dominance claims;
  neither sparse counts nor missing annotation means biological absence.
- **Program coupling and recipients:** within each disease, compare the two
  macrophage panels, and associate each panel/ARG1 with (a) deposited aberrant
  basaloid fraction among epithelial cells, (b) ATII fraction among epithelial
  cells, and (c) fibroblast matrix score (Fibroblast/Myofibroblast union).
  No epithelial marker score is used to relabel recipient cells. AllMacrophages,
  Macrophage and Proxy2 and floors 10/20/50 provide declared sensitivities.
  Recipient denominator/population must also meet the floor. Use Spearman rho
  with 1,000 paired-donor bootstrap intervals where n >= 8 and both variables
  vary; otherwise retain a specific sparse/constant-variable status. Pooled
  correlations are diagnostic only, explicitly compared with within-disease
  support. The pooled group is not an additional independent replication.
- **Composition/depth sensitivity:** partial rank correlation residualizes ranks
  on log1p(total captured cells), mean metadata UMI/cell and macrophage fraction;
  pooled diagnostics additionally include disease indicators. Report only with
  full-rank design and at least six residual degrees of freedom. This is a
  descriptive sensitivity estimate without a causal interpretation or separate
  confidence interval. Age and recorded sex are additionally included when
  complete; only exact clinical-supplement joins are used. Fibroblast and Myofibroblast counts and union shares are
  reported; each recipient association also has a Fibroblast-only panel sensitivity
  under the same floor. Smoking, treatment, lung function and region remain uncontrolled. Proxy abundance
  versus mean UMI is reported as a detection-bias diagnostic.

Age/recorded-sex-adjusted sensitivity for every disease contrast uses descriptive
OLS (outcome ~ group + centered age + recorded sex), with at least three donors
per group, full design rank and at least six residual degrees of freedom. No
adjusted CI or causal effect is claimed. Unadjusted contrasts remain primary.

Bootstrap requested/valid/constant replicate counts are retained. Correlation
intervals require at least 95% defined replicates; excessive constant-variable
resamples withhold the interval without suppressing the point estimate. Constant
mean-difference bootstrap distributions also withhold intervals and record why.

All intervals are pointwise exploratory descriptions, not simultaneous coverage
or multiplicity-controlled claims. Sampling, disease, composition, detection,
unmeasured clinical factors and inherited annotation can explain associations.
Same-donor pairing establishes a tissue-level association, not spatial contact,
directional signaling, later recovery, human immune history or mediation.

## Computation, verification and disposition

Stream the public integer count matrix once, retain only declared gene columns,
and calculate all-gene totals for every cell. Check totals against source nUMI,
matrix entry count, dimensions, identities and positive integer counts. Save
selected counts and donor aggregates for replay of calculations without another
full scan. Independently verify grouping, score denominators, coverage and
decision-relevant contrasts with separate arithmetic. Preserve failed runs.

Author NAM-cluster frequency/limma-voom reproduction is explicitly unsupported
without the author assignments/model correspondence. The feasible proxies and
deposited-label descriptions proceed with that limit. This stage does not test
A1's regulatory-to-later-output or A22's protein-output discriminator. Its plots
and results stay article-local; existing negative results and decisions remain.
