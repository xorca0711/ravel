# Nb4-P02: cellular redistribution of expression across species

**Status: planned; comparative inputs require the P01 source audit.**
[Master contract](README.md) · [source ledger](SOURCES.md). Sources S01/S02;
S08 is a candidate third species, not a validated new input.

## Question and alternatives

Can a gene have a similar standardized lung-expression summary but a different
cellular source across species? The hypothesis concerns allocation among
homologous cell classes. P01 instead tests classification consequences.

The 2020 source already reports switches such as HHIP/SERPINA1; treat those as
positive reconstruction controls, not novel findings. RAMP3 and broader
source-noted programs are candidates only after exact gene/ortholog reconciliation.
Competing explanations include unmatched cell classes, rare-class capture,
normalization, age, assay, gene annotation and species-specific paralogs.

## Measurement and units

For each donor/animal, estimate linear expression in a frozen set of matched
cell classes. Use equal class weights for the primary standardized expression
summary and report the class set. Divide each class contribution by their sum
to define an **expression-allocation profile**; compare profiles with
Jensen–Shannon divergence and class-specific contrasts. Exclude genes below
a predeclared coverage floor before computing unstable proportions.

An equal-class summary is not whole-lung abundance. A captured-composition
weighted sensitivity describes the sequenced mixture only. A tissue-level
conservation claim needs independent tissue weights or bulk measurements.
Do not equate a nonsignificant abundance difference with conserved expression.

## Ordered analysis

1. Reuse P01's units, orthology and metadata audit. Freeze a common class
   crosswalk independent of the genes whose conservation is tested. Report
   omitted classes and unresolved orthologs.
2. Reconstruct source examples separately from discovery. Calculate per-unit
   standardized expression, allocation and uncertainty. For any “similar
   expression” gate, define a biologically justified equivalence margin before
   new results; otherwise present a continuous two-axis comparison.
3. Estimate species-by-class expression contrasts within identifiable
   assay/region strata; use a gene-level omnibus screen then controlled
   class contrasts. Assess donor/animal omission, alternative stable class
   sets, depth and orthology choices. Avoid pooled cell-level inference.
4. Qualify S08 and repeat the frozen class/gene definitions. Audit whether
   its human/mouse comparisons reuse S01/S02. Use third-species observations
   as a phylogenetic comparator only where orthology and anatomy are valid.
5. Evaluate expression redistribution at the program level with fixed
   membership and measured-gene backgrounds. Check whether one sentinel
   drives the result; a marker switch alone does not prove functional replacement.

## Decision, figures and next step

A replicated allocation difference supports a comparative cellular-context
question. If it disappears with class matching, narrow to compositional or
annotation differences. Human–mouse data alone cannot establish the direction
of evolution. One third species may help discriminate patterns, but ancestral
state, adaptive selection or gain/loss claims require broader phylogenetic
and gene-annotation evidence; missing RNA is not genomic gene loss.

Planned panels: standardized-expression difference versus allocation divergence;
donor-resolved class heatmaps; selected matched-class profiles across species;
sensitivity to the common class set. Caption focus: **“Comparable aggregate
expression can conceal different cellular sources across species.”**
No alluvial plot should imply cell lineage conversion.

First deliverable: eligible matched-class universe and a reproduction-versus-
discovery gene list. Targeted novelty review must include the
[2025 lemur study](https://doi.org/10.1038/s41586-025-09114-8). This may become
a distinct RQ if its cellular-context discriminator survives that review;
do not automatically create an evolutionary-mechanism A-number.
