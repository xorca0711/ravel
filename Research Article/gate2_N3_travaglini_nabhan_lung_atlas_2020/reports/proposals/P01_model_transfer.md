# Nb4-P01: species-dependent model transfer

**Status: planned.** [Master contract](README.md) · [source ledger](SOURCES.md).
Primary sources: S01/S02; independent human reference to qualify from S03/S04/S07.

## Question and alternatives

Does a mouse-derived alveolar marker model misclassify human AT1/AT2 identity
because individual markers change specificity across species, while a broader
orthologous program transfers better? The useful outcome is a changed
annotation or program interpretation, not another list of species DE genes.
Alternatives are incompatible labels, age/anatomy, capture depth, dissociation,
or assay differences. Species and study can be inseparable in these sources.

Start with normal adult AT1 versus AT2, retaining mesothelium as an explicit
out-of-domain specificity challenge where available. Analyze AT2-s only after
P06 establishes an interpretable label; do not force it into a mouse stem-cell
class. HOPX/MYRF are source-informed sentinels, not independent discoveries.

## Measurement and units

The primary estimand is the difference in **donor-level balanced classification
accuracy** between a fixed source-marker classifier and a broader ortholog
classifier on the same eligible human observations. Also report class-specific
recall, confusion, rejection/uncertainty and calibration where sample size
allows. Equal donor weighting prevents high-cell donors dominating.

Reference labels must have an auditable source and a sensitivity annotation
excluding tested marker genes. Without an independent reference, report
agreement with author labels rather than biological accuracy. Human and mouse
are separate cohorts; animals/pools are the mouse units, donors the human units.

## Ordered analysis

1. Resolve S02 individual/pool IDs, adult age, lung region, count layers and
   one-to-one orthologs. Freeze genome builds, mapping release and exclusions.
   Missing orthologs remain missing; paralog mappings form a separate sensitivity.
2. Recover the original marker comparator and labels. Train a simple fixed
   nearest-centroid classifier for both feature representations with the same
   scaling/model family. Select broader features and tune any rejection rule
   using mouse training units only; no selection on human outcomes.
3. Benchmark held-out mouse units, then transfer without human refitting.
   Compare within-species human training as a descriptive attainable reference,
   with donor-held-out splits. It is not evidence of a species cause.
4. Repeat fixed predictions after source-marker omission, equal-depth sampling,
   matched-region/assay restrictions and alternative auditable labels. Preserve
   all eligible contrasts. Internal folds do not supply independent donors.
5. Validate the frozen difference in a nonoverlapping human study and, where
   possible, another mouse study. Separate within-assay species contrasts from
   cross-assay ones. No batch integration may erase the effect being tested.

## Decision, figures and next step

Retain a transfer-risk question if marker-specific disagreements recur in an
independent cohort and change a prespecified interpretation. Narrow to an
annotation or assay question if that rival explains the result. If study and
species remain confounded, call the result cross-dataset transfer failure;
do not attribute it uniquely to species. No gain with imprecise estimates
does not establish equal transfer.

Planned panels: donor/age/assay coverage; donor-weighted confusion matrices;
paired classifier performance; ortholog marker dot plot; PCA of donor
pseudobulks. Caption focus: **“Marker choice can alter how a mouse alveolar
reference recognizes human epithelial identity.”** This states the comparison,
not an observed result.

First deliverable: an animal/pool and orthology audit plus label-independence
table. P02 reuses this audit. Route biological maturation/repair claims to
A8/A4/A19; keep the transfer estimand distinct. Before promotion, screen
comparative atlas and annotation-transfer literature for this exact contrast.
