# Peng spatial-omics: paper assessment and connection to Ravel

Reading assessment, 8 November 2026. Based on main `60537cdbaff97f4e6728c58ea97e16a6b265db13`.
Documentation only: no biological analysis, new candidate registration, hypothesis
replacement or scientific acceptance. The owner's linked reading notes were
read, including the linked Figure 3 note, and remain unchanged.

## Assessment

This paper fits Ravel's investigation of how cellular states acquire different
meanings in injury, repair and disease. Its useful addition is a joint view of
**molecular state, tissue pathology, inferred clonal context and local cellular
neighborhood**. A KRT8-high intermediate signature alone cannot distinguish
productive repair, persistent injury-associated states and a tumor-associated
state. Peng et al. supply spatial and pathological context, with experimental
support for an IL-1 contribution in mouse carcinogenesis. They do not establish
the eventual fate of each human KAC or a clinical progression predictor.

The connection is already concrete: Ravel uses this paper's GSE308103 human
snRNA-seq cohort and GSE307534 spatial companion. The opportunity is to recover
additional interpretable measurements from an existing evidence lineage.
Reusing those patients cannot be counted as independent validation.

## What was read

- Peng et al., *Cancer Cell* 44, 321-339.e13 (2026),
  [DOI](https://doi.org/10.1016/j.ccell.2025.10.004). Published online
  6 November 2025; issue date 9 February 2026. The supplied 33-page PDF includes
  STAR Methods. Its bibliographic metadata gives a misleading end page; the
  article and indexed record give 339.e13.
- The supplied 17-page supplemental PDF: Figures S1-S8 and their legends.
  Separate supplementary table workbooks S1-S6 were not audited in this pass.
- Main Results, Discussion, relevant methods and all supplemental legends;
  visual inspection of Figures 2, 3, 5, 6, 7 and S8. Figure 7B was inspected
  at enlarged resolution to verify treatment comparisons.
- Current registry, relevant dossiers/results, source intake and spatial report;
  selected primary-literature records and author-code/data landing pages.
  This is a critical reading assessment, not a complete reproduction or systematic review.

## Evidence and its limits

| Evidence | What it supports | What remains unestablished |
|---|---|---|
| Visium: 56 tissue samples from 25 patients; 486,519 retained spots. Matched snRNA-seq: 75 samples, 23 patients (Fig. 1; Results). | Spatially heterogeneous epithelial and niche programs across pathological categories. | Samples and spots are nested within patients. Cross-sectional categories are not successive observations of one lesion. |
| RNA-based SpatialInferCNV, paired lesions and pathology (Fig. 2; S1-S3). | Full sharing (5 cases), partial sharing (13), or no shared clone detected (5); P22 stable and P7 uncategorized. Selected CNA patterns have snRNA/WES support (S2B). | Human lineage tracing, obligatory linear progression and absence of deeper shared ancestry. Spot mixing, reference selection and clone thresholds matter. |
| Nine epithelial snRNA-derived MPs; KAC/RPII correspondence (Fig. 3; S4-S5). | RPII regions retain alveolar features while sharing tumor/KAC and inflammatory/stress features. | A universal one-to-one identity between morphology and molecular state; tumor specificity of KRT8 or MP6; proof of an individual cell's fate. |
| Xenium: 12 sections from 6 discovery patients, plus a reported independent 19-patient TMA cohort with 36 lesions and 188 cores (Fig. 5). | In situ localization and enrichment of IL1B-high macrophages around KACs/early lesions; a separate cohort supports the spatial pattern. | All six discovery patients are not new replication. Cores and millions of cells are not independent patients. RNA proximity does not measure mature cytokine delivery or receptor activation. |
| Recombinant IL-1beta and macrophage coculture with AT2-derived KRT8-lineage organoids (Fig. 6H-K). | Increased organoid formation/size under the tested conditions. | Completed malignant conversion, restored AT1 function, or proof that the entire macrophage effect is mediated exclusively by IL-1beta. |
| Conditional Il1r1 loss in the CCSP-Cre/Kras model (S8G-I; Methods e4); antibody interventions after NNK (Fig. 7). | Perturbation evidence for an IL-1 contribution to tumor development and KAC abundance in specified mouse contexts. | KAC-exclusive mediation of all treatment benefit, human prevention efficacy, or conversion of disappearing KACs into functional AT1 cells. |

The title's “co-evolution” is best read as linked changes in epithelial states,
inferred clone distributions and inflammatory neighborhoods across sampled
contexts. Reciprocal evolutionary selection and a longitudinal human trajectory
are stronger claims than these measurements establish.

### Pathology and ST make different contributions

Pathology supplies lesion class, RPII morphology, normal-appearing regions and
interfaces. The study used three experienced pathologists and detailed ROI
selection (Methods e4-e5). This is materially more informative than assigning a
whole specimen's diagnosis to every epithelial cell. Nevertheless, adjacent
normal-appearing tissue can carry field effects; it is not automatically healthy
population baseline tissue.

Visium measures mixed spots. **iStar predicts** finer-resolution expression using
histology as well as measured expression (Methods e6); predicted pixels are not
new independently measured cells, and histology agreement is partly built into
the method. Xenium supplies directly localized transcript measurements subject
to panel coverage, segmentation and alignment limits. Its H&E alignment and
pathologist-selected polygons are described in Methods e8-e9. These modalities
should be distinguished in a presentation, even when displayed side by side.

Xenium neighborhoods use an **80-micrometer centroid radius** (Methods e9).
This is a measurement definition, not a demonstrated cytokine diffusion range
or direct-contact criterion. Regional cell density, epithelial packing, lesion
edges and overlapping neighborhoods can affect counts. Figure 5E/K legends
describe cell-neighborhood comparisons with unpaired tests; a patient-aware
reanalysis would need the underlying unit map. Very small cell-level p values
do not alone establish transport across patients.

### Intervention results deserve their own reading

Figure 7 has two precancerous treatment windows: immediately after NNK to
3 months, or from 3 to 7 months after NNK. For tumor volume in Fig. 7B,
anti-IL-1beta versus control has p=0.017 at 3 months and p=0.11 at 7 months;
combination versus control has p=0.017 and p=0.015. The displayed brackets are
comparisons with control, not proof of superiority of combination over each
monotherapy or a formal interaction/synergy test. KAC fractions at 3 months are
significantly reduced only in the combination group (Fig. 7F; n=4 per group,
except n=3 for anti-IL-1beta). Distinguish this from tumor-volume sample sizes.

Anti-IL-1beta did not suppress established subcutaneous 344SQ tumor growth
(S8J). This is a useful boundary observation, but stage, model, genotype and
anatomical site differ from NNK-induced lung lesions. It is not an isolated test
of treatment timing. The study motivates a stage-dependent interception
hypothesis; it does not supply a human treatment recommendation.

For numerical reproduction, clarify unit reporting before inference: Fig. 6J/K's
legend calls dots wells, while the size panel displays many more observations
than the number panel; S8G/H sample counts also differ from some methods
descriptions (e4/e11). Retain these discrepancies rather than treating every
organoid, field or TMA core as an independent animal.

## Suggested corrections and additions to the reading notes

The main note's revised distinction between KAC state, RPII morphology and CNA
clone identity is sound, especially its qualified interpretation of pattern 2.
Carry that precision into the older Figure 3 and Discussion notes.

| Current emphasis | More defensible formulation |
|---|---|
| KACs occupy an intersection of repair and cancer routes. | The inferred expression manifold is compatible with these routes; pseudotime and CytoTRACE do not observe conversion or establish lineage direction. |
| RPII are the exact spatial counterpart of KACs. | In the studied tissues, pathology and molecular measurements support correspondence between RPII-rich regions and KAC-like states. |
| Early clone locations confirm events before recognizable precursors. | Their inferred ancestry and RPII localization suggest an early role; synchronous sampling cannot date the emergence of each human lesion. |
| High IL1R1 makes cells more receptive. | High IL1R1 RNA supports a receptor-context hypothesis; the mouse perturbations provide separate functional support, with model-specific limits. |
| Nine MPs describe the full spatial analysis. | Fig. 3 uses nine epithelial snRNA-derived MPs; Fig. 4B uses eleven Visium-derived MPs. Their numbers are not interchangeable identities. |
| Inflammation plus checkpoint blockade should be more clinically effective early. | Early mouse interventions motivate clinical investigation; human prevention benefit and combination synergy are unestablished here. |

The Results note stops at the heading introducing proinflammatory niches. Add
four short evidence blocks: Fig. 4's candidate axis and KRAS-associated context;
Fig. 5's measured neighborhoods and separate TMA cohort; Fig. 6/S8G-I's
functional experiments; and Fig. 7/S8J's intervention and negative boundary.
Also use **snRNA-seq** for the human adjacent-FFPE assay. The KRAS-associated
precursor enrichment in S5H-I is a contextual result, not evidence that every
human LUAD genotype uses the same dependence.

## Connection to current Ravel evidence

The [source register](../../DATASETS.md) and
[spatial report](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/REPORT.md)
already identify 56 GSE307534 sections and 25 patient labels, with all 23
GSE308103 RNA patient labels represented in the spatial cohort. This is
metadata-supported linkage; adjacent pieces are not the same cells.

| Existing question | Current repository observation | What this paper could add |
|---|---|---|
| [A11: lesion-associated information](../../research_dossiers/A11.md) | GSE308103 is part of discovery history. The later eight-patient comparison retains lesion association but fails to establish distinct residual information; a duplicate-p53-feature control matches the prediction gain. | Pathology/state qualification could clarify what a lesion association measures. Peng's MP6 is not automatically the frozen A11 component. Returning to discovery patients is exposed characterization, not validation of the later result. |
| [A12: recipient context](../../research_dossiers/A12.md) | The 12-patient pilot improves epithelial prediction (RMSE 0.4271 to 0.3244), while the fibroblast prediction worsens. | Cell state and local source proximity can address whether the epithelial association reflects configuration, mixture or general inflammation. Neither supports a new positive fibroblast conclusion. |
| [A13: fibroblast contribution](../../research_dossiers/A13.md) | The TGF-hallmark addition worsens held-out MSE by 0.004181. | Early iCAF enrichment is a relevant published observation, not evidence that the failed proxy works or that a specific fibroblast product mediates recovery. |
| [A1](../../research_dossiers/A1.md), [A8](../../research_dossiers/A8.md), [A14](../../research_dossiers/A14.md): state distinction, later AT1 output, post-withdrawal recovery | Early molecular measurements are not adequately joined to later mature output; the A14 withdrawal effect remains unestimated locally. | A precancer context makes those distinctions biologically consequential, but this paper's human snapshots and organoid growth endpoints do not supply the missing linked mature-output measurements. |

### A12: related evidence, different estimands

Peng et al. (2026), Fig. 4D and Fig. 5E/K, report high IL1R1 in KACs and
early-lesion enrichment of IL1B-high macrophage neighborhoods. This addresses
the biological plausibility of state-dependent epithelial reception. It does
**not directly explain** the repository's LUAD-minus-normal recipient index.

The [A12 component result](../../../RQ_Specified/A12_recipient_context/reports/IL1_COMPONENTS_V1_RESULTS.md)
has epithelial IL1RAP increasing but IL1R1 decreasing. High expression in a
specific state and a decrease across histologies within a transferred candidate
compartment can coexist. They condition on different populations and comparisons;
state mixture and stage dependence remain possible explanations, not findings.
The [source intake](../2026-11-03-tool-assisted-screening-review/A12_SOURCE_INTAKE.md)
also records healthy-reference label uncertainty and overlap of some IL-1 genes
with transfer features. It confirms that cell-level counts exist; the limitation
is state/endpoint independence and exact joins, not simply missing matrices.

The [A12 dossier](../../research_dossiers/A12.md) preserves substantial unassigned
IL1B RNA and the difference between RNA context and active ligand reception.
Spatial macrophage enrichment cannot silently assign that unassigned RNA or
prove secretion. This paper and Ravel's same-cohort analyses share provenance.

## A bounded next comparison, proposed only

Organizing question: **When does a transitional epithelial state mark a
repair-associated response, and when is it embedded in a lesion-associated
environment?** The first executable step would be measurement qualification
within the existing A12/C3 evidence, before any progression prediction.

1. Recover author cell/spot pathology, sample IDs and coordinate/ROI joins.
   Compare author-supported KAC/RPII and other epithelial definitions with the
   current broad transferred compartment. Keep uncertain cells explicit and
   avoid defining states with the same genes used as the response.
2. If those joins qualify, describe local IL1B-high myeloid abundance and a
   separate epithelial inflammatory RNA endpoint within matched epithelial
   states and pathology strata. Biological unit: patient, with sections/ROIs
   nested beneath it. Address density, cell mixture, lesion boundary and spatial
   dependence. Panel coverage must support the selected outcome; no unmeasured
   gene is treated as zero. This estimates contextual association, not IL-1 flux.
3. If an association survives that qualification, assess a fixed procedure in
   a genuinely separate cohort with compatible measurements. The reported TMA
   cohort is a candidate for a narrow spatial endpoint, not automatically an
   eligible replication of A12's whole-transcriptome index. Its smaller panel
   and repeated cores require explicit qualification.

These steps could distinguish three explanations without pretending to settle
all of carcinogenesis:

| Explanation | Informative result | Interpretation limit |
|---|---|---|
| Local inflammatory context accompanies the state. | A reproducible within-state neighborhood association across patients. | Supports spatial context; reverse recruitment and other signals remain possible. |
| Apparent association reflects epithelial mixture or regional packing. | Association attenuates after independent state and density qualification. | Narrows the old contextual predictor; does not prove IL-1 is biologically irrelevant. |
| Intrinsic or exposure-dependent persistence contributes beyond current input. | In a separately qualified longitudinal model, persistence after verified signal cessation with linked lineage, survival and mature-output measurements. | Human snapshots cannot test this. This belongs with existing state/recovery questions and needs its own design. |

An absent association under an adequately measured comparison is informative;
insufficient states, panel coverage or units instead leaves the contrast
unestimated. Effect margin, precision and model feasibility are unknown here.
No new analysis is authorized by this proposal; execution requires a versioned
contract with the existing outcome exposure retained. Generic IL-1 withdrawal
and macrophage-supported growth already have close precedents.

## Literature context and actual search coverage

Bounded live search on **8 November 2026**, using web search and primary-source
pages; recent coverage targeted 2024-2026 alongside older close precedents.
The following sources constrain the framing:

- **Choi et al. (2020)**, [Fig. 7E-H](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/):
  persistent IL-1beta and withdrawal/metabolic interventions distinguish
  transitional accumulation from AT1 maturation. Generic reversibility is
  already published; KAC depletion cannot substitute for mature recovery.
- **Hill et al. (2023)**, [Fig. 3e-g and Extended Data 5](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614604/):
  pollution-exposed macrophages, IL-1beta and EGFR-mutant AT2/tumor outcomes
  provide a close functional precedent. Peng's contribution is the precursor
  pathology/spatial organization and additional model context, not first
  discovery of an inflammation-to-progenitor relationship.
- **Han et al. (2024)**, [Fig. 4 and associated lineage-labeling results](https://www.nature.com/articles/s41586-024-07113-9):
  the preceding KAC atlas supplies the mouse lineage premise. Peng explicitly
  reuses GSE222901 and the earlier KAC signature; that arm is not independent
  replication of the earlier source.
- **Cardoso et al. (2026)**, [Fig. 4 and Extended Data 8-10](https://doi.org/10.1038/s41586-026-10399-6):
  a recent primary study directly tests mutant-epithelial AREG, fibroblast EGFR
  and niche remodeling. It makes reciprocal stromal/immune organization a
  concrete alternative to a one-direction macrophage-only story. It does not
  validate A13's different TGF-hallmark proxy or establish that circuit in
  Peng's exact patients.

Queries actually issued included:

```text
"10.1016/j.ccell.2025.10.004"
KRT8 alveolar intermediate lung cancer progenitors Sinjab 2024 2025 lineage tracing
Choi 2020 inflammatory signals AT2 damage associated transient progenitors IL1beta withdrawal
Hill 2023 lung adenocarcinoma promotion air pollutants interleukin 1 beta macrophages
2024 2025 2026 alveolar transitional cells repair cancer IL1R1 inflammatory niche persistence
"Early fibrotic niches establish" "2026"
"An atlas of epithelial cell states" "lineage" "2024"
"Inflammatory Signals Induce AT2" "withdrawal"
"15670280" "Zenodo"
```

Access: Peng's supplied full article and supplement were available. The other
primary sources were inspected through indexed Results/figure text and source
records; several direct PMC requests returned browser challenges and the
Cardoso publisher page redirected to an inaccessible identity endpoint.
Cardoso's indexed source includes the specific Fig. 4/Extended Data results;
its full methods/supplement were not audited here. Backward references to the
closest Peng precedents were followed; no comprehensive forward-citation or
correction/retraction audit was completed. No exhaustive novelty claim follows.

## Data readiness and next decision

The current [C3 spatial report](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/REPORT.md)
already computed whole-section comparisons but found no verified independent
spot-level pathology/ROI annotations in its inspected archive inventory.
Replotting those counts cannot solve that missing regional definition.

The [author GitHub repository](https://github.com/FuduanPeng/LungPCA_Code)
was accessible. Its README and Figure 5 script were read: the script loads
processed RDS files and identifies some panels as Xenium Explorer outputs.
That is not a recovered end-to-end annotation/neighborhood pipeline. The
paper's code DOI [17172149](https://zenodo.org/records/17172149) currently
exposes a public record with restricted files. Its human-data DOI 15670280
could not be fetched through this access route. The README instead names
17148540, which also could not be fetched. These identifiers should be
reconciled, not treated as interchangeable or proof that all data are absent.
The GSE307529/GSE307534 direct web pages returned browser challenges in this
pass; no new archive was downloaded or exhaustively inventoried.

The next justified action, if taken forward, is a **targeted metadata and
annotation recovery** for the existing spatial cohort: exact author polygons,
spot/cell annotations, patient/section crosswalk, gene-panel coverage and access
to the processed objects. If those cannot be obtained, preserve the current
whole-section descriptive scope. Independent-cohort confirmation and
repair-versus-cancer fate experiments remain separate, unqualified steps.

## Journal-club discussion prompts

1. Which claim needs pathology, which needs spatial RNA, and which needs a perturbation?
2. Could damaged epithelium recruit inflammation rather than inflammation initiating every observed state?
3. How would patient-level effects differ from millions of overlapping cell neighborhoods?
4. Does treatment reduce state entry, expansion or survival, or increase exit toward mature AT1 cells?
5. What is learned beyond Choi's repair model, Hill's promotion model and Han's KAC atlas?

For a short presentation, retain Figures 2-3 for state/pathology/clones,
Figure 5 for spatial context and Figure 7 with S8J for intervention/boundary.
Use the distinction between shared repair programs and context-dependent
outcomes as the thread connecting the paper to Ravel.
