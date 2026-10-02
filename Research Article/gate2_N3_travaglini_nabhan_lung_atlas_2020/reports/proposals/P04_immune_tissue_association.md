# Nb4-P04: shared lung-associated immune programs

**Status: planned; source pairing supports a descriptive pilot.**
[Master contract](README.md) · [source ledger](SOURCES.md). S01 source
lung/blood; S03 lung localization; S09 paired external cohort still unqualified.

## Question and alternatives

Is there a lung-associated transcriptional program shared by distinct immune
lineages after comparing corresponding subtypes and accounting for activation?
The directional hypothesis is shared tissue adaptation. Alternatives are
different subtype mixtures, acute recruitment/activation, processing stress
or intravascular blood contamination. “Residency” is a biological motivation,
not a duration measurement available in the atlas.

Begin with source-annotated T-cell subtypes that occur in both compartments,
then test transfer to eligible B/NK subtypes. Analyze matched monocyte contrasts
separately. Lung macrophage versus blood monocyte differences cannot identify
tissue effects independently of differentiation.

## Measurement and units

Primary measurements are paired donor lung-minus-blood pseudobulk contrasts
within an auditable subtype, plus concordance of a discovery-fixed program in
another lineage. Source blood single cells come from only **two lung donors**;
show both paired effects without population-level significance claims.
Sorted bulk reference populations aid annotation but do not add matched donors.

Lineage/subtype definitions must exclude genes used to test the tissue program.
Activation, stress and cell-cycle programs are separately specified with their
own provenance; residualization is a sensitivity, not proof that activation
is causally removed. Cells, regions and sequencing assays remain nested.

## Ordered analysis

1. Recover tissue/source and original donor pair IDs, library preparation,
   sorting and subtype coverage. Confirm that the intended lung–blood contrast
   is not perfectly confounded with processing or assay.
2. Fix a shared-subtype crosswalk without residency-marker circularity.
   Summarize lung/blood capture, lineage and activation separately. Preserve
   unclassifiable observations rather than force correspondence.
3. Estimate the two source donor contrasts and separate 10x/SS2 results.
   Derive a source-informed candidate program using the declared eligible
   genes; do not use its fitted score to redefine the tested cell states.
4. Freeze gene membership/weights, then assess direction across other eligible
   lymphoid subtypes. Leave-one-lineage and gene-omission checks distinguish
   a broad program from a single cell population or marker.
5. Seek S09 with genuinely paired tissue and blood. Repeat within-subtype
   contrasts at the donor level. A lung-only S03 atlas can test reproducibility
   and spatial localization, but cannot validate a tissue-versus-blood effect.
   Disease retention is a later IPF branch after the normal contrast is qualified.

## Decision, figures and next step

Keep a shared tissue-association question when multiple lineages and an
independent paired cohort support it. Narrow to a lineage or activation state
if that explains the signal. Missing paired replication means the result
remains exploratory; it is not evidence that tissue adaptation is absent.

Persistence requires longitudinal, tracking or other independently justified
residence evidence. Spatial localization alone does not establish duration,
homing, recruitment rate or a stable resident lineage.

Planned panels: paired donor/subtype coverage, lung–blood effect plots,
cross-lineage program heatmap, and independent spatial localization.
Caption focus: **“Matched immune populations reveal which lung-associated
features extend across lineages.”** UMAP is optional context, never a residence
test.

First deliverable: a paired sample/subtype table and an accession-level search
record for S09. Compare with A3 (memory/aging) and A6 (disease macrophage
state/amount); a shared tissue contrast is potentially distinct, whereas a
macrophage activation extension should remain with its existing owner.
