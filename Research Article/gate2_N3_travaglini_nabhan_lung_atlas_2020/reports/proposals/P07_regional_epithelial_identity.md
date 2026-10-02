# Nb4-P07: regional epithelial programs in diseased distal lung

**Status: planned.** [Master contract](README.md) · [source ledger](SOURCES.md).
S01 regional reference; full S03 normal spatial context; S05/S06 IPF cohorts.
Reuse the P03 disease-source audit, without depending on its result.

## Question and alternatives

Does distal IPF epithelium redeploy a normal proximal/basal regional program
beyond a generic injury/plasticity program? Alternatives are proximal tissue
contamination, expansion of pre-existing airway cells, unrelated activation
and differences in basal-cell subtype mixture.

Start with source basal and differentiating-basal contexts. Treat
ALOX15/ADH7/SNCA and POSTN/ISLR/PCDH7 as source-informed marker candidates
requiring cell-specific verification. Use the corrected source interpretation:
differentiating basal cells reduce KRT5 while increasing HES1/KRT7/SCGB3A2.
Marker expression alone cannot locate a cell anatomically.

## Measurement and units

Primary endpoint: a normal-region-derived expression contrast in disease
epithelial states that remains distinguishable from an independently specified
shared injury/plasticity program. Use donor × measured region × subtype
pseudobulks. Region must come from sampling records or independent pathology;
never infer region from the expression signature being tested.

Disease-state assignment, normal-region program and generic injury program
must have separate provenance. Report their gene overlap explicitly. Examine
region-only, shared and nonoverlapping components without selecting whichever
best separates disease after viewing results.

## Ordered analysis

1. Verify region labels and matched normal donor coverage in S01/S03, then
   audit distal IPF sampling and epithelial-state coverage in S05/S06.
   If normal region and subtype are inseparable, report that confounding
   instead of fitting an unsupported region effect.
2. Derive the normal regional program within comparable basal subtypes, using
   donor-held-out selection. Freeze genes/weights and gene-overlap handling.
   Reuse A0/A5/A11 programs with their original measurement definitions.
3. Project the frozen regional and injury programs into independently annotated
   disease populations. Estimate IPF/control contrasts and region-by-state
   patterns only where the design has support; show individual donors.
4. Repeat after basal-subtype matching, amount/capture checks, marker omissions
   and exclusion of ambiguous tissue pieces. Separate sample contamination
   from actual distal localization using independently annotated sections.
5. Transfer the fixed comparison into S06 or another nonoverlapping cohort.
   A spatial spot may contain several cell types: require cell-resolved
   evidence or qualify deconvolution uncertainty before assigning coexpression.

## Decision, figures and next step

Retain regional redeployment as a molecular association when the normal
reference transfers and independently located distal disease cells carry the
program beyond generic plasticity. Narrow to shared injury, airway admixture
or a basal-subtype question when these explain the result.

This does not establish airway-to-alveolar migration, transdifferentiation
or the ancestral origin of a lesion. Those need lineage/time evidence.
If the discriminator reduces to A0/A5 program reuse or A11 lesion addition,
merge with that existing RQ instead of renaming it.

Planned panels: measured-region coverage; normal regional dot plot; paired
regional-versus-injury score view; donor effect plots; independent tissue
localization. Caption focus: **“Normal regional identity provides a reference
for interpreting epithelial remodeling in fibrotic distal lung.”**

First deliverable: a region-label audit and a three-way gene-overlap table
(normal regional, tested disease-state, existing injury programs). A first
positive spatial image without an independent sampling framework is
illustrative evidence, not validation.
