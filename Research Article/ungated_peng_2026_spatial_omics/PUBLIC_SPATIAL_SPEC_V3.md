# Pg1-P01/C3 public Visium spatial RNA v3

Prospective exposed description, 8 November 2026. Existing section means and
maps were exposed; the first 43 sections now have exposed v2 lattice outputs. These are reused under
exact hashes; the remaining sections and aggregation keep the same frozen design. Primary
question: does IL1B RNA covary with CLDN4 RNA in neighboring tissue spots, and how
does this measured organization differ in patient-matched LUAD versus AAH?
CLDN4 is a fixed epithelial-associated transcript, not a KAC/RPII classifier.
No cellular ligand-source, receptor recipient or pathology-region assignment.

Use all 56 deposited GSE307534 sections. Recompute counts, full-library totals,
detected genes and mitochondrial percentages from matrix.mtx.gz. Qualify unique
Ensembl feature IDs/barcodes and both coordinate versions, compare cached QC/normalized
display values, and retain original QC: tissue mask 1, >=500 counts, >=200 genes,
<=15% mitochondrial RNA. All five fixed genes IL1B, CLDN4, C1QA, COL1A1, KRT8
must occur exactly once on the original symbol axis; absent coverage holds the affected section, never zero-fill.
For full-library QC, sum feature rows sharing a symbol before counting detected
genes, exactly as the original C3 processing did. Preserve all source feature IDs,
report duplicated symbols and verify total counts unchanged. Targets are not
duplicated; no target aggregation or gene substitution is introduced.
Malformed source/identity/count/join disagreement stops rather than relabeling.

Array adjacency is the six offsets (0,+/-2), (+/-1,+/-1). No calibrated physical
radius is claimed. Construct the induced undirected graph on QC tissue spots;
never bridge gaps, detached tissue or excluded spots. Report all component sizes,
isolates and retained fraction. Components with >=20 spots supply the endpoint;
smaller components remain in QC counts and maps, with endpoint missing. This is
a numerical support guard, not a biological region or power justification.
If fewer than 100 retained spots, report the section endpoint unestimated.

Primary transforms are log1p(10000*count/full-library), residualized separately
within each retained connected component against intercept, log1p(total counts)
and log1p(detected genes). Standardize each residual transcript by its pooled RMS
across retained spots. Zero residual variance gives a missing statistic. Report:

1. Same-spot mean standardized cross-product, distinct from cross-spot association.
2. Primary symmetric one-hop cross-product: mean over focal spots of
   (z_IL1B * neighbor-mean(z_CLDN4) + z_CLDN4 * neighbor-mean(z_IL1B))/2.
   Each focal spot has equal weight; neighbors have equal weights within focal spot.
3. The same statistic at exactly two graph hops and the one-minus-two-hop difference.
   This is a scale contrast, not an autocorrelation-preserving null distribution.
4. Both transcripts' univariate one-hop Moran-style cross-products, documenting
   spatial autocorrelation. These statistics are not converted to spot p-values.

Fixed sensitivities: component-centered values without depth residualization;
depth plus C1QA/COL1A1/KRT8 log-RNA covariates (broad myeloid/stromal/epithelial
RNA proxies, not estimated cell proportions); one-hop averages restricted to focal
spots having all six neighbors (same residuals, no new bridges). The latter is an
edge sensitivity, not erosion-based anatomy. No gene search, threshold tuning,
new score, deconvolution or purported exact composition adjustment.

Compute each section statistic once; average repeated sections equally within
patient/histology. Primary paired contrast LUAD minus AAH; AIS and MIA comparisons
are secondary exposed descriptions. Retain every qualified match and all patient
values. A spot-weighted section aggregation is a fixed sensitivity. Record section
counts and non-estimability. Report equal-patient mean/median/range and leave-one-
patient-out mean range, not a confidence interval. With few pairs, no power,
equivalence, progression trajectory or population-null claim is made.

No independent-spot shuffle is valid for these autocorrelated fields. This design
uses observed graph-distance comparisons and patient units, not a claimed spatial
null test. Spatial autocorrelation, broad composition, field geometry and mixed
spots remain limitations even after the named sensitivities. No contact, direction
of signaling, 80-micrometer Xenium replay, or causal IL-1 reception conclusion.

Independent verification uses coordinate-key neighbor lists and scalar edge
arithmetic for every section/mode, separate from production sparse graph products;
it reconstructs patient aggregation and matched contrasts. All-patient maps are
retained; illustrative PNG sections are the numerically first two patients with
AAH/LUAD matches, selected by metadata before endpoint inspection. Raw identities,
cached-value parity, graph symmetry/components and numerical range checks are
required. A narrow spatial failure does not invalidate the completed A12 branch.

[Literature/measurement context](PUBLIC_DATA_CONTEXT.md). Author-defined states,
pathology geometry, exact serial-section equivalence and TMA transport remain held.

## Prospective correction and exposure

V1 stopped before expression calculation because it required globally unique
gene symbols. Every feature axis has unique Ensembl IDs and all five fixed targets are unique.
Source feature/symbol counts are either 18,085/18,082 or 18,120/18,087. In the
first failed section, TBCE, HSPA14 and TMSB15B each label two IDs; other sections
can contain additional duplicate symbols, which are inventoried per section. The original C3 code explicitly collapsed symbols before detected-gene
QC. V2 restores that documented representation and requires exact cached-QC
parity. No outcome, gene, population, QC threshold or spatial estimand changes.
The complete failed v1 receipt/logs are copied byte-exact into the v2 run.

## Stored-zero correction and continuation

V2 verified 43 sections, then GSM9226211 failed the raw sparse-entry positivity
check. Its 18,120 x 13,372 matrix contains 63,556,922 stored entries, exactly two
of which are zero; none are negative, fractional or nonfinite. A stored numeric
zero is a valid measured count. V3 retains nonnegative integer validation and
removes explicitly stored zeros before detected-gene QC, without altering library
sums. Unique feature IDs, unique target symbols and exact cached-QC parity remain
required. No biological threshold or endpoint changes.

V3 binds and archives every failed v2 file (including its retained v1 archive).
It reuses the 43 hash-bound, independently verified spot extracts rather than
rereading their full matrices; their original source hashes remain bound and
unchanged, and cache parity is checked again at the resumption boundary. Graph
and summary arithmetic are recomputed and verified consistently for all sections.
The remaining 13 matrices receive full read/QC qualification. This is exposed
continuation, not a new untouched experiment or exclusion of failed samples.
