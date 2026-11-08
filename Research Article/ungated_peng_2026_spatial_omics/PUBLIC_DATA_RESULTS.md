# Public-data results: candidate recipient configuration and spatial RNA

8 November 2026. Both authorized public-data branches are complete and independently
verified. [Measured figure gallery](PUBLIC_DATA_FIGURES.md). The owner reports the Zenodo access request submitted;
approval remains pending and unverified. No second request was sent.

## A12: detection and intensity are different parts of the aggregate pattern

[Contract](contracts/public_cells_v1.json), freeze `8c22904`,
[immutable receipt](../../analysis/research/runs/A12_public_cells_v1_20261108/receipt.json),
[specification](PUBLIC_CELLS_SPEC_V1.md) and [literature rationale](PUBLIC_DATA_CONTEXT.md).
All 75 libraries, 555,480 QC nuclei and source-index joins qualified. The primary
comparison retains the original 12 patients and 24 normal/LUAD AT2-candidate units
(39,051 nuclei), with exact parity to all 240 prior component primitives.
The independent sparse/scalar verifier passed 7,677 checks (maximum numerical
error 3.56e-15). The nuclei and blocks are nested observations, not extra patients.

| Fixed primary endpoint | Mean LUAD minus normal across 12 patients | Interpretation |
|---|---:|---|
| IL1R1 detection fraction | -0.75 percentage points | Heterogeneous: 6 patients increase and 6 decrease; the mean changes sign under leave-one-patient-out sensitivity. |
| IL1RAP detection fraction | +2.45 percentage points | 8 patients increase; a detection-frequency component accompanies the earlier aggregate increase. |
| IL1R1 positive-cell mean log2(1 + normalized RNA) | -0.071 | Conditional intensity differs from detection and from summed-count CPM. |
| IL1RAP positive-cell mean log2(1 + normalized RNA) | -0.196 | Its aggregate increase is not an increase in average normalized intensity among detected nuclei. |
| IL1R1/IL1RAP joint detection fraction | +1.01 percentage points | 7 patients increase; barcode co-detection is not receptor assembly. |
| IL1RAP detected conditional on detected IL1R1 | +3.33 percentage points | 9 patients increase; denominator is the observed IL1R1-positive barcodes. |

Normalized RNA in positive-cell rows uses each full-library denominator and
10,000 scaling, followed by log2(1+x). The old pseudobulk values use summed
counts/full-library sums and 1,000,000 scaling. They are different estimands;
this analysis does not algebraically attribute the old predictive improvement
or exactly decompose its nonlinear pseudobulk transformation.

![Fixed components and individual paired patients](../../analysis/research/runs/A12_public_cells_v1_20261108/cell_components.png)

The depth common-support sensitivity reduces joint detection from +1.01 to
+0.16 percentage points; IL1RAP detection remains +1.49 points and IL1R1 is
-1.58 points. Common support retains 87.5–100% of normal and 89.0–100% of LUAD
candidate nuclei across patients. This is a sensitivity to the measured depth
and detected-gene distribution, not a causal correction or an equivalence result.

Candidate selection matters: AT2 all-QC gives +5.49 points IL1RAP and +2.65 points
joint detection; the broad Epithelial all-QC view gives +8.01 and +4.21 points.
IL1R1 detection changes from -0.75 points in primary AT2 candidates to +1.68 in
confident broad epithelial candidates (+1.72 in broad all-QC). Equal-block
weighting is close to the primary pooled-block description (-0.88, +2.40 and
+0.98 points for IL1R1, IL1RAP and joint detection respectively). These checks
localize dependence on selection/depth without proving its biological cause.

![Selection and depth sensitivities](../../analysis/research/runs/A12_public_cells_v1_20261108/cell_sensitivity.png)

All ten genes and four fixed pairs are retained in the
[patient gene table](../../analysis/research/runs/A12_public_cells_v1_20261108/patient_gene_components.csv),
[co-detection table](../../analysis/research/runs/A12_public_cells_v1_20261108/patient_codetection.csv),
[all paired summaries](../../analysis/research/runs/A12_public_cells_v1_20261108/paired_summary.csv),
[common-support record](../../analysis/research/runs/A12_public_cells_v1_20261108/depth_support.csv)
and [label/confidence inventory](../../analysis/research/runs/A12_public_cells_v1_20261108/label_confidence_inventory.csv).
IL1R2 and IL1RN have zero detections in some primary units; their conditional
positive-cell means remain missing. No absent gene was imputed as zero.

**Biological consequence:** the earlier IL1RAP-up/IL1R1-down aggregate contrast
cannot be described as uniformly increased receptor expression or signaling.
There is a measured detection-frequency component, heterogeneous IL1R1 behavior,
and sensitivity to candidate population and depth. Transferred labels include
some IL-1 targets, broad cross-lineage RNA persists, and epithelial mixtures are
unresolved. This is candidate-compartment description, not intrinsic within-state
regulation. NFKBIA/TNFAIP3 overlap the old response and supply no independent
validation. The unfavorable fibroblast prediction and old A11/A12/A13 evidence
remain unchanged.

## Visium: spatial organization depends on the measured context

[Final contract](contracts/public_spatial_v3.json), freeze `bf2f841`,
[immutable receipt](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/receipt.json)
and [fixed specification/amendments](PUBLIC_SPATIAL_SPEC_V3.md).
All 56 sections from 25 patient labels qualified: 629,799 QC tissue spots, with
629,578 retained in 62 connected components. The 221 spots in smaller components
remain in QC tables/maps; no gap is bridged. Every section is estimable.
Independent coordinate-neighbor, regression, scalar edge and patient aggregation
checks passed 3,782,624 comparisons (maximum error 3.92e-11).

The endpoint is a symmetric standardized cross-product across adjacent lattice
spots. It is not a cell-contact frequency, ligand-receptor test or physical radius.

| Prespecified paired spatial comparison | Patients | Depth-adjusted mean delta | With broad RNA-composition covariates |
|---|---:|---:|---:|
| **LUAD minus AAH — primary** | 10 | +0.0279 | +0.0095 |
| LUAD minus AIS — secondary | 12 | +0.0269 | +0.0193 |
| LUAD minus MIA — secondary | 4 | +0.0537 | +0.0251 |

Patient sets overlap and cannot be added as independent cohorts. For the primary
comparison, 7/10 patients increase; individual deltas range from -0.0302 to
+0.1315. The leave-one-patient-out mean range is +0.0164 to +0.0344, an influence
check, not a confidence interval. Patients 1, 2 and 4 have negative primary deltas;
patient 20 contributes the largest positive value. All are retained.

![Matched patient spatial results](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/spatial_paired.png)

Depth adjustment reduces the primary mean delta from +0.0453 for centered RNA
fields to +0.0279. Adding the fixed C1QA/COL1A1/KRT8 RNA covariates gives +0.0095;
this is sensitivity to broad RNA organization, not a percentage of mechanism
explained or a complete adjustment for cell composition. Equal-section and
spot-weighted summaries are close (+0.02791 versus +0.02792), as is the interior-
focal-spot sensitivity (+0.02777).

The primary two-hop delta is +0.0192; the one-minus-two-hop delta is +0.0087 with
only 5/10 patients positive. Thus the results do not isolate a unique immediate-
neighbor process. Same-spot delta (+0.0308) remains separately reported. Individual
transcripts are spatially autocorrelated: across sections, depth-adjusted one-hop
Moran-style values range 0.010–0.302 for IL1B and 0.062–0.633 for CLDN4. No naive
spot shuffle or independent-spot significance test was used.

[All section statistics](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/section_statistics.csv),
[patient values](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/patient_statistics.csv),
[paired deltas](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/paired_deltas.csv),
[graph support](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/graph_components.csv)
and the [25-patient map atlas](../../analysis/research/runs/Pg1_public_spatial_v3_20261108/spatial_all_patients.pdf)
retain the underlying heterogeneity. Each of the 56 compact spot tables is in the
receipt's `spots/` outputs. Example patients 1 and 2 were chosen from metadata
before outcome inspection; both have contrary primary paired directions.

**Biological consequence:** public Visium adds a modest, heterogeneous spatial
RNA association beyond old section means. Its magnitude depends on depth and
broad composition proxies. It does not identify macrophage-to-KAC communication,
within-state receptor regulation, IL-1-specific signaling or a progression effect.
C1QA/COL1A1/KRT8 adjustment can also remove biologically relevant variation; it is
a sensitivity, not the uniquely correct analysis. Mixed spots, shared normalization
and missing pathology/state annotations remain consequential.

Two source-format failures were retained, not hidden: v1 rejected nonunique gene
symbols despite unique Ensembl IDs; v2 verified 43 sections then encountered stored
zero entries. V3 preserves the complete v2 archive (including v1), reuses those
43 verified extracts and qualifies the remaining 13 matrices. Four stored zeros
occur in two sections. The original biological QC, fixed genes and graph statistic
never changed. [Validation and preservation](PUBLIC_DATA_VALIDATION.md). The separate
[source-binding receipt](../../analysis/research/runs/Pg1_public_source_bindings_v1_20261108/receipt.json)
verifies all 131 library/section identities and 542 file bindings against the
prior GEO qualification and successful input-hash records.

## Biological rationale, in text

The functional question remains whether recipient configuration changes IL-1
response in an independently established state. The detection/intensity plots
and measured spatial maps are the visual aids: they show why mixture, depth and
spatial organization remain alternatives to intrinsic receptor regulation.
They do not test receptor assembly or functional signaling. Independent state
identity and appropriate protein/functional measurements remain necessary for
that inference.

Per the owner's presentation direction, text-box rationale diagrams are not
displayed. The previous renderings remain immutable historical artifacts only.
The current [figure gallery](PUBLIC_DATA_FIGURES.md) contains measured results
and actual spatial maps; rationale remains in prose.

## Completed versus deferred work

The source tables and both public-data branches are complete. The new spatial
branch uses public masks/coordinates, not restricted author pathology annotations.
Author-dependent stages 3–6 (state/pathology/ROI alignment, exact 80-micrometer
reproduction, within-state A12 estimation and TMA endpoint transport) remain held.
Stage 7 still needs linked functional outcomes. P6 WES identity, P7 diagnostic
history and S5 date-cell identity remain local holds, not RNA-analysis exclusions.
No new global RQ, accepted claim, independent replication or clinical conclusion.

Next input-driven work is to qualify the pending author exports under a new
contract. Do not rerun these descriptions or relax their boundaries to substitute
for the missing state/pathology/geometry, exact section/core joins or measured
panels. User-reported requested access is not access approval.
