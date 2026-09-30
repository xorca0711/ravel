# A20 extension source audit

Reviewed 30 September 2026. [Assay evidence](metadata/assay_evidence.tsv) ·
[Priority decisions](metadata/priority_decisions.tsv) ·
[Retrieval provenance](metadata/intake.json).

## Executed RNA source: Ng-Blichfeldt et al. 2019

[TGF-β activation impairs fibroblast ability to support adult lung epithelial
progenitor cell organoid formation](https://doi.org/10.1152/ajplung.00400.2018).
[Author manuscript](https://pure.rug.nl/ws/files/93432135/ajplung.00400.2018.pdf) ·
[Versioned count deposit](https://doi.org/10.6084/m9.figshare.7740071.v1).

The count deposit has four matched human fibroblast donors, each with vehicle,
CHIR, TGF and concurrent combined inputs: 16 libraries. RNA donors and functional
organoid donors belong to separate cohorts with different treatment durations.
They cannot be joined for donor-level RNA/function regression. Functional
experiments motivate altered fibroblast support beyond initial abundance;
they do not eliminate later survival or mechanics as explanations.

CHIR acts downstream of FZD and does not identify receptor-specific dependence.
The combined condition does not establish an initially verified TGF-induced
state. Our frozen descriptive normalization/panels differ from the source's
inferential analysis; this is a contextual reanalysis, not an exact reproduction.
Annotation lookup and the FZD10 absence amendment are retained with provenance.

## What “Jones Notch study” means

**Dakota L. Jones et al., “An injury-induced mesenchymal-epithelial cell niche
coordinates regenerative responses in the lung,” Science 386, eado5561 (2024).**
[Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13159043/) ·
[DOI](https://doi.org/10.1126/science.ado5561) ·
[GSE249931](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE249931).

Mesenchymal Notch inhibition improved repair and AT2 organoid support. Pdgfra
lineage includes several fibroblast populations; it is not exclusive to AF1.
Organoid expansion does not establish mature epithelial output. This is a
lineage/context comparator for A20, not a FZD1/FZD2 perturbation study or proof
of FZD2–Notch interaction.

GSM7967329 and GSM7967330 identify the wildtype and Notch-KD libraries.
The inspected GEO/BioSample records do not resolve independent animal/pool
identities or a matched functional-output join. We therefore did not treat
cells as replicated animals or run a new Notch differential-expression test.

## Developmental functional comparator: Riccetti et al. 2022

[Maladaptive functional changes in alveolar fibroblasts due to perinatal
hyperoxia impair epithelial differentiation](https://insight.jci.org/articles/view/152404).
[Data series GSE171812](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171812).

The neonatal study links impaired matrix-related function with reduced
differentiation support and distinguishes expansion-associated from
differentiation-associated outcomes. Whole-co-culture drug exposure leaves
direct epithelial effects possible. This is not adult AF1 replication.
GEO supplies 18 RNA libraries across three ages and two exposures; inspected
sample records do not resolve animal/pool units. Functional well/slide counts
must not be counted as independent animals. No new numerical fit was executed.

## Receptor-specific motivation: Zhou et al. 2025

[Mesenchymal Fzd2 study](https://doi.org/10.1186/s12964-025-02501-8).
The [parent audit](../../SOURCES.md) retains the repair phenotype, absence of
a comparable Fzd1 arm, unresolved perturbation-data accession and contradictory
transition-direction wording. It motivates the original hypothesis without
supplying a direct test of A20 H1/H2.

## Evidence boundary

Only the Ng-Blichfeldt raw-count cohort was newly analyzed numerically.
The other studies supply biological context or eligibility decisions.
Source findings and our hypothesis refinements remain distinct. No author
was contacted and no individual values were reconstructed from published bars.
