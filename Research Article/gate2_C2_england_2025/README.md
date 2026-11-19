# England et al. (2025) — Regenerative epithelial states and mutant clone expansion

<a id="england-et-al-2025-mutant-at2-cells-and-the-repair-programme"></a>

<a id="when-a-repair-state-supports-clone-growth"></a>

## Published findings

```text
Kras-mutant AT2 cells
  ├─ Lineage tracing → clones with different growth rates
  └─ IL1R1-dependent entry into a regenerative state
       └─ Sustained NF-κB activity → persistence of mixed epithelial identity

Implication: mutant cells can reuse a repair program during early clonal expansion.
```

Mouse lineage tracing revealed heterogeneous clone expansion. Tissue and organoid experiments connected persistence of the repair-like state to sustained NF-κB activity and tested differentiation after inhibition. [Paper, Figs. 1–4 and 7](https://doi.org/10.1016/j.stem.2025.01.011)

## Ravel analyses and results

Ravel found that a permissive AT1 marker rule also counted many cells in AT2 clusters. The fraction called AT1-like therefore depends on how the state is defined. The deposited RNA can describe mixed identities, while the paper’s functional experiments carry the evidence for differentiation. [State and maturation results](EVIDENCE_REVIEW.md#state-and-maturation)

<details>
<summary>Additional analysis results</summary>

<a id="claims-at-a-glance"></a>

### Evidence by biological question

| Biological topic | Current reading | Evidence and limits |
|---|---|---|
| Mixed identity and maturation | RNA states depend on their definition; functional AT1 maturation is not measured by a score | [State and maturation](EVIDENCE_REVIEW.md#state-and-maturation) |
| CD177-associated priming | An RNA association is observed; depth, composition, specificity and contamination remain unresolved | [CD177 attribution](EVIDENCE_REVIEW.md#cd177-attribution) |
| Il1r1 and NF-kB | Genotype-associated RNA differences are reproduced; this is a different comparison from post-entry NF-kB inhibition | [Signalling and timing](EVIDENCE_REVIEW.md#il1r1-and-nf-kb) |
| Unequal clone growth | Deposited distributions and an implementation defect are recoverable; discrete founder classes are not uniquely identified | [Clone growth](EVIDENCE_REVIEW.md#clone-growth) |
| WT neighbours | Pooled distance profiles are descriptive; they do not establish two causal signalling channels | [WT response](EVIDENCE_REVIEW.md#wild-type-neighbours) |
| Repair versus oncogenesis | External repair comparisons are available; insufficient CD177 coverage leaves its transfer test unassessed | [Repair comparison](EVIDENCE_REVIEW.md#repair-transfer) |

</details>

## Data and methods

Lineage measurements and pooled epithelial transcriptomes describe different units. The RNA reconstruction compared state definitions across source libraries. [Samples and biological units](#data-and-biological-units)

<details>
<summary>Experimental and computational methods</summary>

### Data and biological units

| Material | What is available | Unit and limitation |
|---|---|---|
| Epithelial scRNA-seq | 20 libraries; 44,196 cells after the source-QC implementation | Libraries pool lungs; pool identities and reporter pairing remain unresolved. Cells are not independent mice |
| Nonspatial clone measurements | 164,453 measurements; 44 source-indexed mice across cohorts | Mouse/lobe hierarchy is retained; cross-sectional clone measurements do not follow individual-cell fate |
| Spatial pair arrays | 25,173 pooled rows | Mouse/clone identifiers are absent; neighbours may recur across pairs |
| Source functional assays | Published tracing, sorted-state organoids/transplantation and perturbation observations | They motivate biology; a new RNA score does not independently reproduce their functional endpoints |

### Analysis stages

These are execution stages, not independent replication cohorts.

| Stage | What ran | Original report | Current interpretation |
|---|---|---|---|
| First batch | Library contrasts, clone distributions and pooled spatial descriptions | [Batch 1](RESULTS_BATCH1.md) | [Evidence review](EVIDENCE_REVIEW.md) |
| Continuation, EN0–EN7 | State gates, CD177 contrasts, model implementation and repair transfer | [Continuation](RESULTS_CONTINUATION.md) | [Source/claim audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md) |
| Follow-up, FU blocks | Depth, gate, neighbourhood, topology and spatial sensitivities | [Follow-up](RESULTS_FOLLOWUP.md) | [Source/claim audit](../../docs/audits/2026-09-28-england-paper-rqs/REPORT.md) |
| A16 Stage 1 | Marker attribution sensitivities in the question-specific workspace | [A16 original results](../../RQ_Specified/A16_cd177_state_attribution/reports/STAGE1_RESULTS.md) | [A16 integration review](../../RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md) |

Two later computational tasks have their own versioned records:

- [Corrected A16 C1](../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md): fixed populations and gene-excluded local matching; no full attribution claim.
- [A17 source accounting](../../docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md): all 58 saved count rows reproduced, 11 primary source-indexed mice; no stochastic refit.

</details>

## Interpretation and open questions

A mixed RNA identity can describe sampled cells. It does not identify which founder produced a fast-growing clone or whether those cells later acquired mature AT1 function.

<details>
<summary>Interpretation and related questions</summary>

<a id="questions-and-next-decisions"></a>

### Outstanding research questions

**A16** remains biologically inconclusive. Its [corrected C1 comparison](../../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md)
now retains fixed populations in separate libraries and excludes tested genes
before neighbourhood construction; priming attenuates, with substantial residual
imbalance. **A17** now has [verified raw-source counts and code mapping](../../docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md).
Manuscript/curve provenance and a fully specified fair stochastic refit remain
open. **A18** still needs spatial mouse/clone identities for animal-level inference.
The [candidate cards](CANDIDATE_HYPOTHESES.md) explain the feasible E-N1/E-N2
mouse-level extensions and the additional RNA/mechanistic hypotheses.

The [opportunity record](ANALYSIS_OPPORTUNITIES.md) records remaining data gates.
The broader connections to A4, A8, A11, A12 and A14 are in the shared
[question register](../../RESEARCH_QUESTIONS.md); paper-specific work stays here,
while question-specific execution stays in `RQ_Specified/`.

</details>

## Figures and supporting documentation

| Study materials | Location |
|---|---|
| Data and design | [Sources and study design](SOURCE_AUDIT.md) |
| Computational methods | [Analysis code](scripts/) |
| Results | [Study results](EVIDENCE_REVIEW.md) |
| Figures | [Figures and captions](FIGURES.md) |

### Study context and analysis history

**Subsequent evidence — 7 October 2026:** The [source-parameter ascertainment extension](../../docs/portfolio_extensions/2026-10-07/g1_epithelial/RESULTS.md) now separates founder, retained-clone and expected-cell fractions. At week 4, 8% fast founders yield 8.24% of retained size>=2 clones and 95.01% of expected retained cells under the fixed model. This is a mathematical ratio of expectations, not measured tissue composition or a fitted founder-versus-switching result.

[England et al., *Cell Stem Cell* 32, 375–390.e9](https://doi.org/10.1016/j.stem.2025.01.011).
*Sustained NF-kB activation allows mutant alveolar stem cells to co-opt a
regeneration program for tumor initiation.* Reading branch 2C, item 2; stable
roadmap paper 12.

AT2 cells make surfactant and can replenish the thin AT1 gas-exchange surface
after injury. The paper asks how oncogenic Kras redirects that regenerative
response into persistent, plastic epithelial states and alters neighbouring
wild-type cells. It combines lineage tracing, clone measurements, RNA profiles
and functional perturbations. Our reanalysis tests selected RNA and clonal
patterns; the paper's functional experiments remain a separate evidence source.

**Current status: three paper-analysis stages and A16 Stage 1 have run.**
The source and subsequent interpretation reviews are complete. Founder identity,
CD177-specific function and separate spatial signalling mechanisms remain open.
Historical result reports retain their original wording and numbers; the
evidence review below gives the current interpretation.

<a id="read-this-study"></a>

### Study overview and references

| To understand | Read |
|---|---|
| How later analyses revise existing questions | [Chronological RQ review and conditional candidates](RQ_RETROSPECTIVE_REVIEW.md) |
| What the paper claims, what we recovered, and what remains unresolved | [Claims and evidence review](EVIDENCE_REVIEW.md) |
| The generated plots, their units, tables and current captions | [Complete figure gallery: 15 figures](FIGURES.md) |
| What each execution stage produced | [Analysis stages](#analysis-stages) |
| The three derived questions | [A16–A18 in the shared register](../../RESEARCH_QUESTIONS.md#a16) |
| Eight further biological hypotheses and their feasibility | [Candidate hypotheses](CANDIDATE_HYPOTHESES.md); [supporting checks](CANDIDATE_CHECKS.md) |
| Source metadata and original design | [Source audit](SOURCE_AUDIT.md); [library manifest](metadata/geo_library_manifest.csv); [original analysis plan](ANALYSIS_TRIAL_PLAN.md) |

<a id="figure-gallery"></a>

### Study figures

The [full gallery](FIGURES.md) groups all **15 original figures by biological
question**, with the generating stage, observational unit, data and current
interpretation beside each image. Image files and numeric results are unchanged.
Some embedded image titles retain superseded interpretations, explicitly
identified in their captions.

| Browse by question | Figures |
|---|---|
| [State and maturation](FIGURES.md#state-and-maturation) | EN_C01, EN_C02, FU_F01, FU_F04 |
| [CD177 attribution](FIGURES.md#cd177-attribution) | EN_C03, FU_F02, FU_F03 |
| [Il1r1 and genotype context](FIGURES.md#il1r1-and-nf-kb) | EN_F02, EN_F03, EN_C04 |
| [Clone growth and models](FIGURES.md#clone-growth) | EN_F05, EN_C05 |
| [WT neighbours and distance](FIGURES.md#wild-type-neighbours) | EN_F06, FU_F05 |
| [Repair comparison](FIGURES.md#repair-transfer) | EN_C06 |

<a id="identifier-guide"></a>

### Study and analysis identifiers

| Label | Meaning |
|---|---|
| Paper Figure 3 | A figure published by England and colleagues |
| EN_F02 / EN_C03 / FU_F02 | Repository figures from the first batch / continuation / follow-up |
| A16–A18 | Proposed repository-wide research questions |
| England/E-N1–E-N8 | Paper-local candidate extensions; not new global registrations |
| C31, C136, etc. | Historical claims in the root [claim register](../../CLAIMS.md); distinct from paper-local trial or figure labels |

<a id="question-literature-and-visual-companions"></a>

### Related literature and hypotheses

- [A17: published premises, proposed increment and hypothesis schematic](../../docs/research_dossiers/literature_context_2026-10-03/A17.md)
- [A18: published premises, proposed increment and hypothesis schematic](../../docs/research_dossiers/literature_context_2026-10-03/A18.md)
