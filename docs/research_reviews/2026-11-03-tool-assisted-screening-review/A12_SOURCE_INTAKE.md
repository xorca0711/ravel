# A12 cell-level source intake

3 November 2026. Coordinator-owned metadata/file-structure review, preceding any
new cell-level endpoint. No matrix expression analysis, state classifier or pilot
refit was run. This qualifies available material, not a new biological result.

## What exists

The same-source [GSE308103 record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308103)
describes human single-nucleus RNA sequencing of normal lung, precursor lesions
and invasive adenocarcinoma. The existing local package records 75 libraries from
23 patients. A fresh NCBI GDS esummary for `200308103` confirmed accession, study
title and platform GPL24676; it was a metadata read, not a full-paper assessment.

All 75 `raw_counts.csc.h5` stores and 75 `cell_annotations.csv.gz` files are present
under `X:/GitHub/ravel/Research Article/gate2_C3_yu_lee_choi_min_2026/cache/u5_human_full/`.
Their absence from the C: authoring cache does not mean cell-level data are absent.
Counts use the custom `review_gene_row_CSC_v1` format, not an AnnData matrix.
Annotations retain GSM, patient, histology, barcode-derived cell ID,
`source_cell_index`, full-library QC and transferred labels/uncertainty. The
source index joins the annotation to the original count-store cell column.

Existing provenance: [processing specification](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_full/processing_specification.json),
[processing record](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_full/processing_run_record.json),
[annotation review](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_full/ANNOTATION_REVIEW.md),
[cell join implementation](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_full_run.py)
and [count-store implementation](../../../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_human_count_store.py).
The local files were counted and their headers/format inspected; a new complete
input-hash manifest has not been generated.

## What this changes for screening

The precise next biological question is whether the epithelial recipient
association reflects receptor/accessory/inhibitory configuration within cells,
different epithelial populations, or broader inflammatory state. Raw counts make
a descriptive cell-level configuration screen possible in principle. They do not
by themselves establish IL-1 specificity or independently defined lesional states.

The existing labels were transferred from a healthy HLCA reference. The review
allows broad candidate compartments, not validated malignant/KAC/HPCS labels.
An independent check of the 2,000 reference gene symbols found IL1R1, IL1R2,
IL1RN and TNFAIP3 among the mapping features. Thus independence of state labels
from all candidate endpoints cannot be assumed. This feature overlap is a
potential circularity concern, not evidence that it caused the observed labels
or that the broad compartment assignments are necessarily wrong.

The existing annotation review also records substantial cross-lineage RNA and
histology-dependent confidence retention; the source uncertainty is already
documented in A12-S1. These concerns affect a precise within-state comparison,
not the mere existence of the matrices.

## Disposition and reopening condition

Preserve the closed 12-patient pilot and the
[ten-gene component result](../../../RQ_Specified/A12_recipient_context/reports/IL1_COMPONENTS_V1_RESULTS.md).
No new predictive fit or malignant-state claim is justified by this intake.
For a new descriptive screen, first specify which receptor/context candidate
decision would change, retain ambiguous labels, and qualify the exact count joins
and input bytes. For a state-standardized biological comparison, provide suitable
independent state evidence or explicitly narrow the inference to the transferred
candidate compartment. Functional IL-1 dependence remains a separate missing
measurement. Do not report this hold as missing cell-level data.

The NCBI request used the installed Entrez wrapper. Initial restricted-network
DNS access failed; the same read succeeded under the approved network execution
path. No author contact, controlled access or external write occurred.
