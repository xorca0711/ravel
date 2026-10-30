# Frozen R1 RNA endpoint design

30 October 2026. Owner: Yd1-P01; descriptive reuse of GSE242510. This implements the
already selected RNA comparisons after the functional source reconstructions,
full-entry integrity qualification and endpoint-free conservative annotation.

The biological preparation, animal pooling, batch and suffix pairing remain
unknown. A library is the reporting unit; cells supply each library/class summary,
not independent replicates. All 24 library/QC/class combinations passed the fixed
coverage and held-out marker compatibility rule. That supports bounded calculation,
not cell purity, power, lineage or biological independence. Fibroblast-only libraries
contain macrophage-compatible cells; WT coculture 1 contains many mixed cells.
The frozen classes and QC masks are retained despite these concerns.

## Endpoints and estimands

Use nonintegrated counts with all zeros retained. Primary endpoint is the
class-specific library mean of log1p(count / all-gene cell total * 10,000).
Companions are nonzero detection fraction, mean counts per 10,000 and class-level
pseudobulk CPM. The latter is a descriptive ratio, not a replicate-level DE model.

1. Macrophage-like Arg1: P2rx4-KO fibroblast coculture minus WT fibroblast coculture.
2. Fibroblast-like Il6: the same genotype/library comparison.
3. Fibroblast-like Il6: WT coculture minus fibroblast alone.

Both frozen QC masks are reported. Use both libraries per condition and equal
library weights. Preserve all four crossed-library differences without pairing;
their range describes observed library heterogeneity and is not a confidence
interval. Do not rank endpoints by significance or choose a QC mask by direction.

## Exposure and validity limits

Published findings, functional results, count QC and annotation/composition are
already exposed. Local class-specific Arg1 and Il6 results have not been calculated
before this freeze. Neither target participated in class assignment or eligibility.
The leading threat is selection/measurement heterogeneity, including ambient RNA,
mixed cells, unvalidated class purity and unknown preparation/batch effects.
Composition is displayed separately; class selection does not remove these threats.
No genotype causality, IL-6 secretion, arginase activity, metabolic flux, mediation
or independent replication follows from the transcript summaries.

## Verification and stopping

The primary sparse-matrix reader is checked against an independent chunked
MatrixMarket reader for every cell total, detected-gene count and both raw target
vectors in all six libraries. Python scalar arithmetic independently verifies all
24 library endpoint summaries. This is numerical verification on the same source.
Preserve any failed check and stop; do not adjust labels, exclusions or target
selection after seeing outcomes. Stop after these three fixed descriptive
contrasts. Spatial/context qualification and Wg-P06/thesis synthesis remain
pending review.
