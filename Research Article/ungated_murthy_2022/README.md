# Kadur Lakshminarasimha Murthy et al. (2022) — Distal lung epithelial lineage potential

<a id="kadur-lakshminarasimha-murthy-et-al-2022-the-source-paper-of-gse178360"></a>

<a id="a-branch-point-between-alveolar-and-airway-epithelium"></a>

## Published findings

```text
Alveolar type 2 cell → transient AT0 state
                         ├─ Alveolar type 1 cell
                         └─ Terminal or respiratory bronchiole secretory cell

Implication: one intermediate has both alveolar and airway differentiation potential.
```

Tissue localization, cell-state trajectories and human organoid differentiation supplied distinct evidence for the AT0 intermediate and its two possible descendants. [Paper, Fig. 3 and Extended Data Fig. 11](https://doi.org/10.1038/s41586-022-04541-3)

## Ravel analyses and results

Ravel’s atlas of three healthy donors identified an epithelial group expressing both *SFTPC* and *SCGB3A2*. Reference mapping assigned AT0 to only 75 of its 328 cells. The markers locate candidates for closer inspection, while the sampled transcriptomes leave both descendant fates unobserved. [Three-donor atlas](GSE178360/README.md) · [Reference-label comparison](../gate1_04_sikkema_2023_hlca/trials/s2_reference_mapping/s2_summary.md)

## Data and methods

The Ravel atlas contains three healthy human donors. Marker coexpression identified a candidate group, and alternative scoring rules and reference labels were compared within the same data. [Three-donor atlas](GSE178360/README.md)

## Interpretation and open questions

RNA coexpression identifies candidate AT0 cells. The lineage evidence comes from tissue and organoid experiments, and each cell’s subsequent fate is unobserved in the atlas.

## Figures and supporting documentation

| Study materials | Location |
|---|---|
| Data and design | [Sources and study design](GSE178360/README.md) |
| Computational methods | [Analysis code](../../analysis/scripts/08_reference_aligned_epithelial_umap.py) |
| Results | [Study results](../gate1_04_sikkema_2023_hlca/trials/s2_reference_mapping/s2_summary.md) |
| Figures | [Figures and captions](#figure-gallery) |

<a id="read-this-study"></a>

### Study overview and references

| To understand | Read |
|---|---|
| Paper context and biological question | [Source and role of this deposit](#study-context) |
| Analysis results, claims and limitations | [Generated three-donor atlas report](GSE178360/README.md); [related HLCA mapping](../gate1_04_sikkema_2023_hlca/README.md) |
| Later results and RQ implications | [Chronological retrospective review](RQ_RETROSPECTIVE_REVIEW.md) |
| Figures and captions | [Donor map and epithelial markers](#figure-gallery) |
| Registered claim decisions and shared questions | [Claim register](../../CLAIMS.md); [question register](../../RESEARCH_QUESTIONS.md) |

<a id="study-context"></a>

*Nature* 2022, DOI [10.1038/s41586-022-04541-3](https://doi.org/10.1038/s41586-022-04541-3),
PMID [35355018](https://pubmed.ncbi.nlm.nih.gov/35355018/). Human distal lung
maps and lineage hierarchies.

This paper is not on the reading roadmap in [`../README.md`](../README.md);
its deposit was analysed before the roadmap existed, as the human series of
the Stage 0 pipeline, and the HLCA lists it as an extension dataset
(Tata_unpubl), which is why trial S2 of
[`../gate1_04_sikkema_2023_hlca/`](../gate1_04_sikkema_2023_hlca/README.md)
targets it. The folder exists to hold that series beside its source paper;
no study note is written here because the owner has not read the paper for
the roadmap, and the roadmap's rule is that study notes follow reading
(DEVELOPMENT.md, decision 23).

- [`GSE178360/`](GSE178360/README.md): the generated report, figures,
  tables, QC and the epithelial sub-analysis (three healthy donors,
  27,729 cells after QC). Current decisions are in the root
  [claim register](../../CLAIMS.md); its mouse claims do not describe this cohort.

<a id="figure-gallery"></a>

### Study figures

The human atlas contains three healthy donors. The figures below describe
donor coverage and marker distributions; they do not establish injury-related
states or lineage transitions.

![Human lung atlas UMAP coloured by donor](GSE178360/figures/umap/UMAP_sample.png)

*Sample-of-origin UMAP from the executed human analysis. Mixing and isolated
regions are diagnostics; an embedding alone cannot establish successful batch
correction or a novel cell type. [Dataset report](GSE178360/README.md).*

![Epithelial marker detection and scaled expression across human atlas clusters](GSE178360/figures/dotplots/marker_dotplot_epithelial.png)

*Dot size is the fraction expressing a marker; colour is scaled mean
expression. Column groups are marker-panel names, not validated identities
for every row. In particular, shared keratins do not identify an injury
transition. [Marker and annotation tables](GSE178360/tables/).*

The [HLCA gallery](../gate1_04_sikkema_2023_hlca/README.md#figure-gallery) shows
the subsequent reference-label and uncertainty checks on this same cohort.
The [complete original figure directory](GSE178360/figures/) also contains
integration diagnostics, quality-control plots and immune/stromal marker panels.
