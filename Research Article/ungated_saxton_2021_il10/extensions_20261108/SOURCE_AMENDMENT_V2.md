# Source adaptation after the common-matrix qualification failed

8 November 2026. The preserved [v1 qualification](../../../analysis/research/runs/sx10_gorby_qualification_v1/qualification.json)
found 79,164 row-by-source-block repeated-control disagreements and 899,624
non-numeric/invalid abundance cells (repeated columns counted). Inspection of
non-target rows identified literal `NA` values and different numerical values
for the same control in different comparison blocks. Missing is not zero.
The proposed single normalized matrix is **not qualified**. This finding is not
reversed by the new stage, and no first/averaged control column is substituted.

GEO sample records link twelve separate CD8 comparison tables for the two dimer
ligands and doses. Each explicitly names its stimulated/control pair and contains
`log2foldchange`, two normalized values and annotations. V2 qualifies these as
**source-reported comparison estimates**, with exact stable-ID joins and no WT
significance selection. This narrower endpoint can describe whether the three
fixed targets show the same directional relationship in this different context.
It cannot recover a common expression matrix or establish a direct ligand effect.

V2 checks every table's schema, unique gene IDs, source code/dose assignment,
fixed target mapping and finite reported estimates. `NA` stays missing; an
affected target/table is held rather than replaced. Original donor identity and
replicate-label uncertainties remain. The downloaded first table's first row was
GZMB and was viewed during header inspection; this added exposure is recorded.
No target choices change and no cross-ligand target contrasts have been viewed.

The prospective numerical stage, if qualified, will report each deposited
log2foldchange, the R5A11D minus WTD difference of those **reported estimates**
within each source code/dose, and descriptive means with all code values and
single-code omissions. A secondary unpseudocounted log2(stimulated/control)
description is permitted only for positive finite pairs and is labelled a
different source-derived quantity. It cannot validate the unknown normalization
or fit, and disagreements will be retained. No primary pseudocount calculation,
DE model, p-values, new genes or mechanistic claims are introduced.

The [exact-byte correction](FREEZE_CORRECTION.md) separately repairs file
serialization. It does not resolve this biological-data qualification failure.
