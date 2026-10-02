# Inputs, versions and biological units

## Public resources actually used by Nb4

This is the article-level provenance register. The shared
[repository dataset inventory](../../docs/DATASETS.md) indexes the study deposits;
numerical methods and outcomes remain here. Matrices below were downloaded and
analyzed, not merely shortlisted.

| Resource | Version and scale | Role / evidence |
|---|---|---|
| [Travaglini CELLxGENE collection](https://cellxgene.cziscience.com/collections/5d445965-6f1a-4b68-ba3a-b8f765155d3a) | SS2 dataset e04daea4-4412-45b5-989e-76a9be070a89, version c0ee0004-7bd1-4986-9b66-8a9d3593c0e6; 9,409 cells | Curated source reproduction; three original donors |
| Same source collection | 10x dataset 8c42cfd0-0b0a-46d5-910c-fc833d83c45e, version f5568ea3-c249-4e4e-91f8-46abc30a5612; 65,662 cells | Curated source reproduction, new stromal UMAP and donor contrasts |
| [Madissoon CELLxGENE collection](https://cellxgene.cziscience.com/collections/c1241244-b22d-483d-875b-75699efb9f3c) | Fibroblasts dataset e871881f-b42d-4500-906d-0972a14ba47d, version 460b3fe9-f623-4299-a745-78beba61c3d8; 20,515 cells/nuclei | Independent-study pilot; ten donor labels, four eligible cell donors and two nuclear donors |
| [MSigDB human collections](https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp) | Existing local 2024.1.Hs Hallmark (50 sets) and GO BP (7,608 sets) GMT files | Annotation resources, not biological datasets; source/external genome-wide enrichment |
| Publisher workbooks and author metadata below | Twelve workbooks and six library metadata files | Computational source intake and source-concordance audit |

[Source matrix hashes](config/expression_sources_v1.json),
[external matrix hash](config/external_source_v1.json),
[gene-set hashes](runs/extended_visual_v1/gene_set_sources.json), and
[external design](runs/external_pilot_v1/design_record.json) identify exact inputs.
No new MSigDB download was required. Synapse objects and EGA accessions below
describe the original release; the Synapse expression files were not downloaded
because anonymous access returned 403. Controlled human raw reads were not used.

## Initial document and supplement inventory

The [manifest](config/source_manifest.json) records 32 inspected local files,
their original URLs where public, sizes and SHA-256 hashes. All source payloads
remain in ignored `raw_data/travaglini_nabhan_2020/sources/`. The
[schema inventory](runs/intake_v1/supplement_schema.json) records sheet names,
dimensions and headers; it does not substitute for expression matrices.

## Published supplement map

All assets below were downloaded from the publisher links on the
[article page](https://www.nature.com/articles/s41586-020-2922-4).
The MOESM number is a file identifier, not the supplementary-table number.

| Resource | File identifier | Role and constraint |
|---|---|---|
| Supplementary Figure 1 | MOESM1 PDF | Sampling/enrichment design context |
| Reporting summary | MOESM2 PDF | Design and reproducibility context |
| Table 1 | MOESM3 | Canonical populations, abundance estimates and markers; abundance is not a captured-cell fraction |
| Table 2 | MOESM4 | Human identities and donor-by-assay counts; discrepant totals retained |
| Table 3 | MOESM5 | Bulk immune-reference population definitions; not extra lung donors |
| Table 4 | MOESM6 | Cluster marker results, TF and functional annotations; selected DE results, not raw counts |
| Table 5 | MOESM7 | CellPhoneDB significant-means output: 1,791 declared rows, 1,948 columns including metadata; not a complete unfiltered p-value matrix |
| Table 6 | MOESM8 | Mouse labels and count coverage across source datasets/animals; age is part of the design |
| Table 7 | MOESM9 | Human-mouse expression comparisons; reset malformed sheet dimensions before parsing |
| Table 8 | MOESM10 | Summary of evolutionary expression-pattern classes |
| Table 9 | MOESM11 | Per-gene evolutionary/functional classes; sheet named Table_S8, so filename/table/sheet numbering differ |
| Source Fig. 1 | MOESM12 | Image-scored AT2 and fibroblast counts; do not infer RNA donor matching |
| Source ED3 | MOESM13 | Basal-state imaging quantification |
| Source ED4 | MOESM14 | Spatial marker quantification |

## Primary data routes

The paper's data statement identifies
[Synapse syn21041850](https://www.synapse.org/Synapse:syn21041850/wiki/600865)
for count/UMI tables, cellular metadata and Seurat/Scanpy objects. Its inspected
wiki points to `syn21560406` (expression), `syn21043647` (metadata), and
`syn21560554` (objects). Current file-level entity versions, matrix sizes and
cell-metadata joins still need inspection. No large processed matrix was
downloaded and no access agreement was accepted during this setup.

The wiki reports a historical FACS metadata column shift and corrected FACS
gene-count objects. Record entity ID, version number, source hash, retrieval
date and whether the target is the published release or a corrected release.
The pinned author download script lists Seurat assets, but it does not by
itself establish which corrected versions reproduce the publication.

Human raw reads: **EGAS00001004344**, controlled access as stated in the paper.
Mouse reads: **PRJNA632939**. Raw-read reconstruction is unnecessary for this
initial structure. Do not assign an unrelated GEO accession to the atlas.

The author repository is pinned at
[`899dd282c36db5b09ded8f522fa3ba239fad1347`](https://github.com/krasnowlab/HLCA/tree/899dd282c36db5b09ded8f522fa3ba239fad1347).
Six library metadata files, SS2 author annotations, the two analysis notebooks,
README and download-script text were inspected/downloaded as source material.
The library files include diseased-region entries that require explicit
exclusion; their `region` field encodes normal/tumor status, while `location`
is anatomical. Library metadata is not a cell-to-donor crosswalk.

## Canonical cell schema

One row per cell in a UTF-8 TSV:

| Field | Meaning |
|---|---|
| cell_id | Original barcode/well ID; retain source spelling |
| donor_id | Verified subject, not sample, plate, region or assay |
| assay / counts_unit | 10x/UMI or SS2/read_count; never conflate them |
| sample_id / raw_library_id | Tissue-sample and sequenced-library nesting |
| tissue / condition | Lung versus blood; histologically_normal versus source-defined other status |
| anatomical_region | Proximal, medial, distal or another verified anatomical field |
| author_cell_type | Original source label or explicitly audited crosswalk |

Metadata preparation must produce a JSON mapping record with `source_version`,
`source_sha256`, `field_mapping`, `author_label_mapping`, and
`matrix_cell_join_status`. Unresolved IDs remain unresolved and fail the
relevant gate. Do not fill missing anatomy from a cell-type name. The identity
key is `(assay, raw_library_id, cell_id)`; duplicate barcodes across independent
libraries are allowed, duplicate composite keys are not.

TN2 additionally requires the original gene-ID/symbol map, matrix orientation,
complete cell-key join, assay/layer semantics, integer nonnegative count checks,
library totals, filtering history and raw-versus-normalized status. Stored
`.X`, `raw`, or `counts` names alone do not establish measurement semantics.
Corrected/integrated/scaled values cannot stand in for raw pseudobulk counts.

Future external studies need their own donor identifiers, disease definition,
count provenance and overlap audit. The 2023 HLCA may include this study; it
is not automatically a held-out replication set.
