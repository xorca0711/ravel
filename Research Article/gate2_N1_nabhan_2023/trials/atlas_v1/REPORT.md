# Nb2 atlas v1: receptor geography and state-dependent questions

Executed 29 September 2026. This is a **descriptive, partial source comparison**
using Habermann 2020 (a dataset reused by Nabhan), plus an exposed Niethamer 2025
mouse extension. Neither is independent confirmation. The original Travaglini
processed atlas was located in Synapse, but its metadata download endpoint returned
403; the exact healthy-atlas reconstruction remains open. The cited HLCA release,
additional fibroblast atlases and original Gillich vascular data were not admitted
as newly analyzed data in this run.

## Design and coverage

The human source matrix has 220,213 barcodes; all 114,396 annotated cells are
present. Their recomputed all-gene UMI totals match source `nCount_RNA` exactly.
The remaining 105,817 barcodes have no source annotation and were excluded, not
assigned new identities. The first run stopped before expression extraction
because it expected equal barcode sets; the [schema amendment](schema_amendment.json)
and [original script](failed_attempt/04_atlas.py) preserve that failure and fix.
The frozen scientific endpoints were unchanged.

The mouse counts layer contains 162,175 cells; 54,549 lack the author-label/condition
information required here. The primary mouse summaries remove the existing
predicted doublets, with retained-doublet summaries as sensitivity. The human
source did not supply a comparable doublet flag; no new ambient-RNA/doublet model
was fitted. Marker-gene context is retained in the tables, but author labels were
not independently revalidated or relabeled from this selected panel.

The [contract](contract.json) specifies 41 receptor/context genes, biological-unit
aggregation, a primary floor of 50 cells per unit/state, sensitivity floors of
20 and 100, and analytic detection after sampling 500 UMIs per eligible cell.
Forty requested genes map in the human source and all 41 in mouse. The simple
symbol mapping did not resolve mouse Car4's human orthologue: CAR4 was not a
source symbol, and CA4 was not extracted. This is a mapping limit, not biological
absence; no conclusion uses that marker. The unit is a source participant/sample identifier,
not an individual cell. All diagnoses are retained separately; IPF was not pooled
with other interstitial lung diseases. Mouse injury time, sex, genotype and batch
are not adjusted here, so time profiles do not estimate a causal time effect.

The [unit table](tables/unit_receptor_context.tsv.gz) retains CPM, detection,
depth, and same-cell-subset comparisons. [Coverage](tables/unit_coverage.tsv)
and [state summaries](tables/state_summary.tsv.gz) show the complete tested
context, including rare or unsupported states. Figures require at least three
eligible units. No cell-level p-values or hypothesis validation is claimed.

## B2/B3: epithelial selectivity is state-dependent, but the rare-state comparison is limited

At the primary floor, human control AT2 has six eligible participants; IPF AT2
has eight. Median FZD5 CPM is 27.86 and 22.92, respectively; median FZD6 CPM is
13.94 and 16.09. These unadjusted differences are descriptions, not evidence of
a disease-caused receptor switch. Ciliated cells retain appreciable FZD6 with
much less FZD5: control median CPM 54.74 versus 0.82, IPF 64.30 versus 1.69.
This supports receptor-context differences between captured airway and alveolar
states without demonstrating their responses to an agonist.

IPF KRT5−/KRT17+ cells have three eligible participants. FZD1 is detectable
(median CPM 19.84; median detection 15.6%), while FZD6 remains higher
(63.98 CPM; 42.9%). Within each of those three participants, FZD6 exceeds FZD1
in CPM and observed detection. That ordering persists after 500-UMI standardization
and at the 20-cell floor. At the 100-cell floor, only two participants remain:
the direction persists but cohort coverage no longer meets the plotting rule.
This supports the source's nuanced pattern, not complete loss of epithelial
receptor selectivity or epithelial-to-stromal conversion.

Only **one IPF participant** has at least 50 transitional-AT2 cells, versus three
controls. The planned within-state disease comparison is therefore coverage-limited.
These data cannot distinguish treatment-by-starting-state response, nor can bulk
GSE208770 supply that missing interaction. The existing
[A4 Axin2/Il1r1 work](../../../gate1_02_choi_2020/axin2_il1r1/README.md) remains the
home for subset/co-detection questions; this run adds receptor context only.

## B4: fibroblast FZD1 is a context lead, not a demonstrated unique mechanism

IPF myofibroblasts have five eligible participants. Median CPM is FZD1 **61.51**,
FZD2 **4.15**, and FZD7 **20.59**. Only one control participant passes the same
myofibroblast floor, so a robust within-subtype disease comparison is unavailable.
Other fibroblast subtypes also have sparse primary-floor coverage; their values
remain visible in the full tables instead of being combined into a larger
biologically ambiguous group.

A **post-run descriptive** association compares each receptor with a four-gene
ECM-associated summary (CTHRC1, LRRC15, COL1A1, COL3A1) within those five IPF
myofibroblast samples. Spearman rho is 0.7 for FZD1, −0.6 for FZD2 and 0.6 for
FZD7. This small exposed screen has no adjusted inference and shares an RNA
denominator; severity and sample composition remain rivals. The FZD7 association
also argues against presenting this as a uniquely FZD1-linked program. These are
candidate-forming measurements, not collagen deposition or receptor function.
See [associations](tables/fibroblast_context_associations.tsv).

## B5: Fzd4 fits broad endothelial identity as well as a capillary question

In the mouse day-42 extension, eight eligible samples each support CAP1, CAP2
and venous endothelium; three support arterial endothelium. Median Fzd4 CPM is
**326.26**, **138.39**, **322.45** and **404.16**, respectively. Fzd4 exceeds Fzd6
within every eligible sample in all four of these source-defined states.
The observation therefore does not isolate a capillary progenitor-specific signal.

The homeostatic mouse group has only two eligible samples for these states.
Figures show days 42 and 90 because those groups offer better unit coverage;
this is a post-run presentation choice, not a discovery/validation split. All
other days and both doublet modes remain in the tables. CAP1/CAP2 retain their
source labels: no unverified conversion to a regenerative gCap or functional
aerocyte identity is used to claim vascular repair.

## Sensitivity and interpretation ceiling

[Observed detection](figures/01_receptor_context.png) and
[500-UMI expected detection](figures/02_receptor_depth500.png) use the same
author-defined states. Depth matching changes detection magnitude and sometimes
eligible coverage; absence of detection is not absence of a receptor. The
[within-unit ordering table](tables/within_unit_receptor_ordering.tsv.gz) preserves
all eight receptor pairs across the three cell floors, three measurements and
available doublet modes. Those summaries were specified as a post-run descriptive
follow-up and must not be called a blinded confirmation.

This initial pass completes the accessible context measurements for B2–B5. It
does not complete label-validation, ambient-RNA exclusion, treatment response,
ligand engagement, physiological flux or lineage/function tests. The strongest
next steps are an eligible state-response design for Nb2-N3, adequate control and
subtype coverage for Nb2-N6, and capillary-versus-general-endothelial functional
discrimination for Nb2-N7. See [the updated candidate register](../../HYPOTHESIS_REGISTER.md#nabhan-branch).
