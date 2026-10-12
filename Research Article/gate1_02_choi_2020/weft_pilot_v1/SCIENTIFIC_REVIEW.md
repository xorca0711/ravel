# Choi P001: scientific QC and Figure 1 interpretation

**12 October 2026: artifact-based review complete; descriptive findings only.**
The recovered run is internally consistent, but does not recover the paper's
five-state partition or establish its mechanism. No analysis was rerun, label
changed, output redrawn, claim grade promoted or human acceptance recorded.
The complete numerical receipt remains unregistered pending the
[publication dependency](FIGURE1_STATUS.md#publication-dependency).

## Scope and evidence

Owner **A0**, with **A1** as context; article-local descriptive benchmark,
`A0.P001_choi_figure1_v1`. The question is whether the selected GSE145031
Tomato-positive inputs support a bounded, fixed-method adaptation of Fig. 1B-D.
Endpoints are retained cells, annotation/marker support, composition and method
sensitivity. Each condition has **one library pooling two mice**. Library and
timepoint are inseparable; cells are not animal replicates. Prior D1/D2/D2b outcomes
were known before this run. This is shared-source reanalysis, not independent
replication or an unseen-paper test.

- **Published evidence:** [Choi et al., Cell Stem Cell (2020)](https://doi.org/10.1016/j.stem.2020.06.020),
  Fig. 1A-D, S1A-C and STAR Methods sections on library preparation, alignment/QC,
  contaminant exclusion and doublets. Fig. 3-4 and 7 supply separate lineage,
  perturbation and maturation evidence outside this pilot.
- **Source review:** [Weft's source/figure/supplement audit](https://github.com/xorca0711/weft/blob/78c1f167d36aec10df008e0622e9082d3ee60098/docs/PILOT_CHOI_REVIEW.md).
  Reused the audited institutional Fig. 1 image, official supplement render (S1,
  PDF pages 3-4) and source text; inspected Fig. 1 and S1 again for this comparison.
  A fresh PMC page request returned a browser challenge. Institutional main-figure
  byte equivalence to publisher images is not established; the earlier documented
  supplement edition comparison is retained.
- **Repository evidence:** frozen source `b656d06cc9f2cfdd61a6dd1f6570ec01331abf91`,
  [contract](config/figure1.contract.json), [methods](scripts/frozen_methods.py),
  [adapter](scripts/figure1.py), and the original recovered outputs listed below.
  Historical [D2b](../trials/d2b_corrected_annotation/d2b_summary.md) is a separate
  result, not the source of the fresh values reported here.

## QC and arithmetic

Independent read-only inspection reconciled the original receipt's 15 output
hashes, CSV/JSON denominators and the saved H5AD. Its count matrix has **11,683
cells x 27,998 genes**, positive integer sparse entries, unique genes and unique
GSM-prefixed cell IDs. Saved total counts, detected genes, mitochondrial fractions,
retained doublet flags, ordered metadata, marker detection, every cluster table,
DATP subcluster membership, 2,000 HVGs, finite PCA/UMAP coordinates and the saved
neighbor diagnostic agree. **1,497 assertions passed**. Marker fractions slightly
above one are floating-point accumulation error (maximum absolute discrepancy
from integer detection counts, `6.80e-14`), not extra detected cells. These checks
verify internal consistency; they do not certify true cell identities.

No raw-input loading, normalization, PCA, neighbor fitting, clustering or UMAP
was repeated. A temporary audit reader initially lacked support for H5AD nullable
strings; that reader was corrected before completion. The source outputs were
opened read-only and remained unchanged. The expected sparse-centering warning
in stderr concerns the frozen HVG embedding; the saved count layer remains sparse.

| Stage / count | PBS | Day 14 | Day 28 | Total |
|---|---:|---:|---:|---:|
| Raw whitelist barcodes | 737,280 | 737,280 | 737,280 | 2,211,840 |
| Paper numeric filter applied to raw barcodes | 4,418 | 4,226 | 4,221 | 12,865 |
| Removed by additional MAD filter | 98 | 436 | 646 | 1,180 |
| After MAD | 4,320 | 3,790 | 3,575 | 11,685 |
| Flagged by adapted doublet procedure | 1 | 0 | 1 | 2 |
| Post-doublet cells | 4,319 | 3,790 | 3,574 | 11,683 |
| Labelled contaminants at primary resolution | 83 | 198 | 1,003 | 1,284 |
| Composition denominator, non-contaminants including unassigned | 4,236 | 3,592 | 2,571 | 10,399 |

All MAD removals arise from the upper mitochondrial-fraction bound: 17.91%,
8.46% and 7.94%, respectively. Removal rates among paper-filter cells are 2.2%,
10.3% and 15.3%. This condition-dependent selection can affect composition; the
saved retained-cell matrix cannot recover the identities of removed cells for
an exclusion-bias analysis. Scrublet used automatic thresholds 0.429/0.380/0.360
and expected rates 0.03456/0.03032/0.02860; the quantile fallback was **not used**.
Only two flags do not demonstrate that remaining cells are doublet-free.

The paper reports 12,514 captured cells, 255 contaminants and 12,086 displayed
cells. The unexplained arithmetic remainder is 173; it is not an identified
doublet set. The pilot's raw-whitelist filtering, MAD, doublet method, Leiden and
rule-based annotation differ from Cell Ranger calling, old Scanpy/Louvain and
the paper's manual exclusions. Neither the 11,683 retained cells nor the 10,399
composition denominator is directly equivalent to the paper's 12,086.

## Composition and comparison with the paper

Entries below are **counts (percent of the non-contaminant denominator)**.
Unassigned cells number zero in all three libraries; the denominator still permits
them. hAT2 is the pipeline label and is not an established match to published AT2.

| Pipeline label | PBS, n=4,236 | Day 14, n=3,592 | Day 28, n=2,571 |
|---|---:|---:|---:|
| hAT2 | 4,166 (98.35%) | 2,555 (71.13%) | 2,109 (82.03%) |
| cAT2 | 5 (0.12%) | 265 (7.38%) | 47 (1.83%) |
| pAT2 | 0 | 0 | 0 |
| DATP | 17 (0.40%) | 672 (18.71%) | 228 (8.87%) |
| AT1 | 48 (1.13%) | 100 (2.78%) | 187 (7.27%) |

The paper's Fig. 1C labels show AT2 at 97.69%/37.39%/72.43%; day-14 primed AT2
38.13%, cycling AT2 6.19% and DATP 16.83%; day-28 primed AT2 18.13% and AT1
4.04%. These are published plot labels, not recovered author cell assignments.
The coarse direction agrees: AT2-like dominance in PBS, more cycling/DATP labels
at day 14, and a larger AT1 fraction at day 28. The missing primed state and different
exclusions prevent quantitative state-for-state equivalence. Do not combine
published AT2 and primed AT2 post hoc to claim an exact hAT2 match.

**Day-28 denominator sensitivity is substantial.** Contaminant-labelled cells
are 1.92%/5.22%/28.06% of post-doublet cells. Of 1,003 excluded day-28 cells,
907 are labelled club/airway. Using all post-doublet cells, day-28 hAT2/DATP/AT1
fractions are 59.01%/6.38%/5.23%, versus 82.03%/8.87%/7.27% after exclusions.
These are two already-emitted denominators, not a new exclusion analysis.

The club/airway rule uses mean detection of Scgb1a1, Scgb3a2 and Cyp2f2 and takes
priority over AT2 assignment. Across its 1,026 cells, detection is 96.78%, 5.85%
and 53.12%, while Etv5/Abca3/Cebpa remain detected in 88.79%/94.64%/75.44%.
This supports an airway-marker signal but does **not** independently establish
off-target contamination rather than mixed identity, ambient RNA, doublets or
annotation error. Scgb1a1 is also detected in 72.98% of hAT2 cells. Retain the
literal pipeline labels without presenting these exclusions as validated sorting
failures or evidence of a new airway-derived repair population.

## State support and annotation limits

| Primary state / diagnostic | Direct support in saved marker counts | Interpretation boundary |
|---|---|---|
| cAT2, 317 cells | Mki67 45.43%, Cdk1 57.73%; hAT2 0.75%/0.54% | Supports a cycling-associated RNA label, not proliferation rate or repaired tissue output |
| DATP, 917 cells | Cldn4 54.85%, Krt8 92.80%; hAT2 2.91%/86.30% | Krt8 detection alone is poorly discriminating; Ndrg1 is detected in only 15.81% of DATP-labelled cells |
| AT1, 335 cells | Pdpn/Hopx/Cav1 68.66%/81.49%/62.99%; DATP 30.10%/26.72%/24.97% | Supports a relative AT1-marker distinction, not maturity, ancestry or function |
| pAT2, zero cells | Every declared marker is available; no cluster meets the fixed assignment rule | Failure to recover the label, not evidence that published primed AT2 biology is absent |

Sftpc is detected in every retained cell, including contaminant-labelled groups.
The nearly saturated hAT2-canonical detection set cannot establish purity. Ambient
RNA is a possible explanation, not proven here. The frozen D2b rule drops its
Sftpc-low clauses when Sftpc is uninformative; its correction remains outcome-exposed.

At primary resolution, the selected hAT2 reference is cluster 7. The pAT2 rule
requires identity detection <=0.5874 and inflammatory detection >=0.5809 relative
to that reference. No remaining candidate cluster qualifies. Other residual
clusters default to hAT2, so **zero unassigned cells is not evidence of confident
annotation**. The stricter cell-level diagnostic finds 19/8,830 hAT2 cells (0.215%)
with no detected identity genes and at least two inflammatory genes; this is not
the paper's expression-based definition of primed AT2.

| Leiden resolution | Clusters | hAT2 | cAT2 | DATP | AT1 | Contaminant-labelled |
|---|---:|---:|---:|---:|---:|---:|
| 0.3 | 8 | 11,309 | 82 | 0 | 0 | 292 |
| 0.5 | 10 | 10,770 | 306 | 0 | 0 | 607 |
| 1.0, fixed primary | 14 | 8,830 | 317 | 917 | 335 | 1,284 |

pAT2 is absent throughout. DATP and AT1 are only separately labelled at 1.0;
their recovery is not robust across the declared resolution settings. Conditional
DATP subclustering produces 397 cells in DATP-labelled subclusters and **520 in
hAT2-labelled subclusters**. The frozen rule retains both as DATP unless a
subcluster is pAT2. Thus the final 917-cell label is intentionally broader than
the subcluster annotation and should not be treated as a homogeneous progenitor
population. No labels were changed in this review.

Historical D2b had the same post-doublet total but different annotations: day-28
contaminants 414 versus 1,003 here, alveolar denominator 3,160 versus 2,571, and
DATP 199 versus 228. This is not exact numerical regression equivalence. Saved
summaries cannot isolate the cause; equal seeds do not establish equal partitions
across runtime/source settings. Both runs retain the absent-pAT2 limitation.

## Figure interpretation and presentation review

All five frozen PNGs were visually inspected; the underlying tables and H5AD
were reconciled separately.

| Saved panel | Reading | Limitation / presentation issue |
|---|---|---|
| `figure1B_state_umap.png` | Four alveolar labels, adjacent DATP/AT1 regions, separate cycling/ciliated regions and small contaminant groups | UMAP distance/adjacency is not temporal transition, lineage or a statistical separation test; drawing order hides some overlapping cells |
| `figure1C_composition.png` | Adapted stacked fractions above | Alphabetical order is day 14, day 28, PBS; long y-label is clipped and legend overlaps a bar. Use the chronological table above when interpreting |
| `figure1D_marker_detection.png` | Mean detection across genes in each marker set | Does not show relative expression, gene-specific discordance or per-library marker variation; shared genes make sets non-independent |
| `qc_library_timepoint_umap.png` | Library/timepoint-associated neighborhoods; saved neighbor enrichment 2.079 | Same biological grouping appears twice with different color mappings. Libraries and times are confounded; 2.079 is not a batch-effect test or correction target |
| `qc_cell_counts.png` | 3,790/3,574/4,319 post-doublet cells | Alphabetical order; clipped y-label. Does not depict earlier QC losses or later exclusions |

**Figure terminology correction:** published Fig. 1D is a **dot plot**, whose
color indicates relative expression and size indicates fraction expressing;
S1B-C contain heatmaps. Earlier pilot wording calls the published Fig. 1D an
"expression heatmap." The scientific distinction was appropriate but the plot
type was inaccurate. This note corrects that wording while preserving frozen
contract/source/output bytes. The pilot's marker-set detection heatmap does not
reproduce both original channels or the exact gene panel.

Do not use p53/hypoxia/glycolysis/Il1r1 column names as evidence of pathway
activation, metabolic flux, cytokine response, regulatory competence or fate.
Those claims require the paper's separate perturbation, metabolic or lineage
experiments. The pilot does not reproduce Fig. 3-4, 6-7 or corresponding supplements.

## Disposition and next decision

**No new canonical RQ or mechanistic phenotype is proposed from this pilot.**
The review records a bounded descriptive similarity plus unresolved cell/state
correspondence. It neither refutes the paper nor validates its five-state model.
A0's failed cross-tissue transfer remains stopped; A1's missing linked regulatory
state-to-later-output evidence remains missing. This is an agent review disposition,
not a human retain/reject decision or scientific acceptance.

Before any future comparative extension, qualify author cell/cluster correspondence
where available and predeclare an expression-aware annotation comparison, with
ambient/doublet and exclusion sensitivity assessed on matched cells. Those would
require a new amended analysis and exposure record; none ran here. Independent
biological units or appropriate perturbation/lineage assays are needed for effects
or mechanisms, and cannot be supplied by additional clustering of these libraries.

The immediate remaining engineering decision is durable availability of **all**
15 outputs, including the 385,675,968-byte H5AD, under the unchanged receipt
validator. Keep PR #149 draft and the numerical receipt unregistered until that
route and the review are resolved. Private recovery is verified. No partial receipt,
automatic acceptance, new dispatch, scheduling or reservation release follows.

## Exact audit anchors

Archive SHA-256: `e1f8ee36d87111dc9ef7defbcddaf04f9633851c63a57ce25f03474881ae69c7`.
Original receipt SHA-256: `24aaaaef907519391ba3c8650f96795ebe2dff4a27cd4ad9e9977852cdc5974b`.
Private read-only reconciliation report SHA-256:
`cda68a0523a103ca187ba0673f2dfe2ded8d92b807190e4311de7f7a5f7907e9`;
audit-reader SHA-256: `a0791ed427e829e43af27b2b8d295bc2952f5b3893fca2e692c37cb548e05b89`.
These audit files are local supporting records, not a new registered scientific run
or cloud checkpoint. The original manifest/receipt binds every output below.

| Original output | SHA-256 |
|---|---|
| `descriptive-summary.json` | `e37c79d695111755fa456829fb7fe2caa51b4bdf37e47cd18fd321c1e85f17a3` |
| `qc_denominators.csv` | `61e33dbaf2d3b10d28cce9851216cfe2a692d969ad699234e8bcd80f9d5432ad` |
| `composition.csv` | `f821a94e83d8516c27fb6c67d3b13d6d8ec574f9e23a8a16bd463192f3b00da3` |
| `marker_evidence.csv` | `1e8929841d28b57a15e727c48a37ef412d33f8e18d42b32410b2bba97e60b2d4` |
| `cell_states.csv` | `642e97141d8e7baef60600cc2cdb94e8cfb52c0343483cfeb111533a0d3bf7ff` |
| `clusters_0.3.csv` | `d58020d75d002cde26ee8209a51cd505b26975e0d5df98bf77044f9b8d114bde` |
| `clusters_0.5.csv` | `ef5303f39b48371297fe72cc148faa18ba62ed25b1d9e0d87f5ee57cf464cf70` |
| `clusters_1.0.csv` | `3cee779d7a0028d6617b39e34109ab08129187926108d316d35438f377431ea9` |
| `datp_subclusters.csv` | `c58e7d4040d06d80fc5f3d319d273a72630bfc5e036de60405b643192f75291c` |
| `figure1_descriptive.h5ad` | `6d2ab27a98543d3f03c941907729af69ca9ce22295e51cff67e329ce8c1644ca` |
| `figure1B_state_umap.png` | `44c44ba1f82cc40038622ef1e25bc4deddb3a828d5365fcbb30faebb381d04a8` |
| `figure1C_composition.png` | `a41a93f0c0f78b6eccbe0d211d6f2735731ee5deead381449baa15aa6f88be4f` |
| `figure1D_marker_detection.png` | `8661e42cf2048260530946773d2c04c1801ddeeb64bb6666588a5d8bc30bc1b0` |
| `qc_library_timepoint_umap.png` | `84ea7f2982aaee3c71bcd93af61f0c9c3a9ee8c0e92dfa5b38dfcc2cc53f634d` |
| `qc_cell_counts.png` | `54d2667c4ba9b8c0d37a6d23768c35024c2099e08925bd0f012bb3d2d47986ee` |
