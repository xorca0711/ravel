# Nb5-P05 Marker specificity and assay dependence

## Question and decision

Does an age-associated marker endpoint remain interpretable after separating
cell identity, detection depth and assay? Decide which measurements can support
a biological candidate and which need orthogonal validation first. This is an
agent-proposed measurement branch; it need not become a biological RQ.

## Hypothesis and strongest rival

The hypothesis is that a bounded source-nominated marker or panel carries an
age association within comparable types across independently measured assay
strata. The strongest rival is assay/depth-dependent detection coupled with
composition, rather than a specific biological state. Generic inflammation,
dissociation and developmental identity are further rival constructs.

## Required metadata and measurement

Need mouse, age, sex, cell identity, assay, library depth, genes detected,
sample preparation, original gene IDs and matrix scale. Recover the exact
source marker list and aliases before scoring. Shared mice across assays are
technical/measurement corroboration, not independent biological replication.

The unit is mouse. Keep three endpoints distinct: detected-cell fraction,
expression conditional on detection, and unconditional expression within a
fixed type. The latter two answer different questions; conditioning on detection
can change the sampled cell set with age. A gene-level Cdkn2a result must not
be reported as isoform-specific p16 protein measurement.

## Bounded analysis and alternatives

1. Audit marker availability, count layers and assay-dependent floor effects.
2. Freeze one primary marker endpoint and a small source-backed sensitivity
   panel. State the expected alternatives and measurement controls before fitting.
3. Compute per-mouse endpoints within type and assay, show unit-level coverage
   and examine supported depth/sex/batch covariates. Use within-assay depth
   sensitivity; do not treat full-length reads as droplet UMIs.
4. Where pairing exists, report within-mouse assay agreement on the compatible
   endpoint. Test whether conclusions depend on a single marker, rare detected
   cells, or an annotation defined by the same panel.

Cross-assay and within-type agreement supports measurement robustness only.
Loss with depth or identity control favors the technical or mixture rival.
Insufficient detection yields an uninformative endpoint, not biological absence.
Unrecoverable scale or gene mapping stops the affected comparison.

## Further RQ frame and limit

A later question could ask whether a robust RNA-defined population co-occurs
with an independently measured phenotype. Durable arrest, secretion and tissue
function need distinct measurements. The atlas cannot make a generic marker
panel a senescence ground truth. This branch supplies measurement qualification
for P01/P03/P04 rather than creating duplicate A-series ownership.

**Additional-analysis frame:** per-mouse frequency/intensity panels, assay
agreement and depth sensitivity with the denominator shown in each panel.

## Execution and RQ status

First outcome-exposed pass completed 3 October 2026. Detection, positive-cell mean, unconditional mean and assay-specific composition accounting executed. Raw-count models and biological marker-function claims remain unqualified.

Read the [current result and amendments](../RESULTS.md),
[figures](../FIGURES.md) and [execution ledger](../EXECUTION_VALIDATION.md)
before extending the original plan above. No human retain/reject decision,
claim promotion or global RQ allocation is recorded. All branches remain
available; a further numerical stage requires a new frozen contract.
