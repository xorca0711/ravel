# Nb4: genome-wide visual and functional annotation analyses

**Executed 2 October 2026 after the owner's request for further visual aids.**
[Specification](../config/extended_visual_v1.json) was frozen after the targeted
nine-gene external pilot but before genome-wide ranks, projections or enrichment.
These are additional analyses, not original-paper figure reproductions.

## Projections and genome-wide comparison

The source objects provide **t-SNE**, not UMAP. Figure 6 retains the deposited
coordinates for 60,993 normal-lung 10x cells. A separate new stromal UMAP uses
5,033 cells, 1,500 mean-bin-normalized dispersion genes, 30 centered unscaled
PCs, 30 neighbors, minimum distance 0.4 and seed 20261002. Mitochondrial and
ribosomal-prefix genes are excluded from variable-gene selection. Donor and
region overlays retain possible confounding; no integration, clustering,
trajectory, spatial relation or tissue prevalence was inferred.

Pseudobulk PCA and enrichment use primary-floor fibroblast pairs: source 10x
distal P1/P3, and the four eligible external single-cell donors. External
within-donor subtype profiles average eligible matched-stratum log profiles
equally. The background includes **11,113 common expression-eligible genes**:
at least 1 CPM in either subtype in both source donors and at least three
external donors. Full library denominators are calculated before filtering;
duplicate symbols, if present, are collapsed by count sums. No marker-panel
restriction determines the background.

PCA uses the top 2,000 variable genes per cohort from that common universe.
Axes are fitted separately; visual separation is descriptive. Across genes,
the source/external mean paired contrast has Spearman r **0.365**. Genes are
dependent observations, so no donor-level inference follows from that number.
[Ranks](../runs/extended_visual_v1/source_gene_ranking.tsv),
[external ranks](../runs/extended_visual_v1/external_gene_ranking.tsv),
[PCA](../runs/extended_visual_v1/pseudobulk_pca.tsv),
[embedding specification](../runs/extended_visual_v1/embedding_model.json).

## GSEA and GO

Reused the repository's MSigDB **2024.1.Hs** Hallmark and GO BP GMTs, already
used in the Niethamer G2 analysis. Byte hashes, not an assumed current release,
identify these inputs. [Library provenance](../runs/extended_visual_v1/gene_set_sources.json).
Human collection definitions are documented by
[MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp).

Hallmark GSEA ranks all eligible genes by mean within-donor alveolar-minus-
adventitial log2(CPM+1). GSEApy uses weight 1, 1,000 gene-set permutations,
seed 20261002 and overlap sizes 15–500; **49 of 50** Hallmark sets meet the
size rule in each cohort. Its p/q values concern the competitive gene-set null,
not a biological donor-population hypothesis. Engine-reported zero permutation
p-values are finite-resolution outputs, not zero probabilities. The
[GSEA guide](https://docs.gsea-msigdb.org/GSEA/GSEA_User_Guide/)
distinguishes gene-set from phenotype permutation.

GO BP uses separate positive/negative foregrounds with absolute mean paired
difference at least 1 and sign agreement in 2/2 source or at least 3/4 external
donors. These are effect-selected genes, **not statistically established DE
genes**. Hypergeometric tests use the common expressed background and BH
correction over all size-eligible GO terms and both directions within cohort.
All results are retained; displayed top terms were selected after calculation.
Related GO terms overlap. Vascular, contractile and extracellular-structure
annotations contextualize subtype differences; they do not demonstrate
physiological function or identify a newly discovered cell type.

## Complement-wide hypothesis does not follow from C3

| HALLMARK_COMPLEMENT | Source, 2 donors | External cells, 4 donors |
|---|---:|---:|
| Set overlap | 141 genes | 141 genes |
| Enrichment score | +0.288 | −0.311 |
| Normalized enrichment score | +1.14 | −1.19 |
| Gene-set FDR q | 1.00 | 0.321 |
| Expression-matched random-set p | 0.094 | 0.076 |

The complementary null draws 1,000 sets matched for set size and mean-expression
bin (20 bins), with a plus-one two-sided empirical p. Neither null is donor
permutation. C3's consistent negative contrast does not generalize to a coherent
whole-set complement shift. External inflammatory/TNF sets show stronger
adventitial enrichment, but the same program-level direction is not recovered
in the source cohort. Do not rescue a broad mechanism by reporting only the
external enrichment.

About 15% of source scores are tied. A targeted reversed-tie-order diagnostic
changed the largest Hallmark ES by only **0.000271**; external ES changes were
zero. Independently calculated ES values agree with engine outputs to less than
7×10⁻⁹ for all tested sets. This resolves the specific tie warning without
claiming that all ranking uncertainty has disappeared.
[Tie diagnostic](../figures/extended_v2/gsea_tie_diagnostic.tsv).

[Figures 6–12](../FIGURES.md), [all GSEA results](../runs/extended_visual_v1/hallmark_gsea.tsv),
[all GO results](../runs/extended_visual_v1/go_bp_ora.tsv), and
[RQ consequences](RQ_DERIVATION.md) retain both favorable and contrary evidence.
