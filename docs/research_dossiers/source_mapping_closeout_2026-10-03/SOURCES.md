# Final source-inspection scope

3 October 2026. These are file-structure observations, separate from the prior frozen numerical metadata outputs.

## Evidence reused without another search

- The [GEO results](../qualification_2026-10-03/RESULTS.md), [BioSample audit](../followup_2026-10-03/METADATA.md) and [retrieval hashes](../followup_2026-10-03/SOURCES.md) cover the five original deposits and exact outstanding export requirements.
- The pinned A5 author tree/object audit and same-day unchanged-HEAD check are reused. The full annotated object remains unrecovered within that scope; a generic repository re-search was not repeated.
- The [outcome audit](../followup_2026-10-03/OUTCOMES.md) and [Rochelle workbook locators](../packages_2026-10-03/SOURCES.md#rochelle-supporting-data-inspection) remain the authority for endpoint/preparation gaps.
- No new full-paper novelty review, inaccessible-accession retry or source-author contact was performed.

## Additional inspected files

The two combined H5 files were the explicitly uninspected file candidates in the preceding stage. The browser tool could not open their FTP-over-HTTPS directory pages. Direct HTTPS byte ranges succeeded. The reader enumerated HDF5 object names/shapes/attributes and inspected only the first eight barcode strings; it did not decode expression-array values or derive a full barcode assignment. Downloaded blocks can include adjacent uninterpreted bytes.

Every requested range required HTTP 206, an exact Content-Range and exact length, with a 24 MiB ceiling per file. The private reader and inspection records retain each range SHA-256. These are fragment hashes, **not full-file hashes**. No downloaded whole-matrix integrity or universal absence claim follows.

### GSE306194

[Published HDF5 file](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE306nnn/GSE306194/suppl/GSE306194_filtered_feature_bc_matrix.h5). Inspected 2026-10-03T07:07:36.118483+00:00; source Last-Modified: Thu, 21 Aug 2025 19:46:06 GMT. Full source size: 289,585,465 bytes; retrieved metadata-range bytes: 6,732,089.

Verbatim root attributes:

```json
{
  "filetype": "matrix",
  "group": [
    "uncultured",
    "P0",
    "P2",
    "uncultured",
    "P0",
    "P2",
    "uncultured",
    "P0",
    "P2"
  ],
  "library_ids": [
    "Donor1_UC",
    "Donor1_P0",
    "Donor1_P2",
    "Donor2_UC",
    "Donor2_P0",
    "Donor2_P2",
    "Donor3_UC",
    "Donor3_P0",
    "Donor3_P2"
  ],
  "original_gem_groups": [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  ],
  "software_version": "cellranger-9.0.0",
  "version": 2
}
```

Enumerated objects: `matrix`, `matrix/barcodes`, `matrix/data`, `matrix/features`, `matrix/features/_all_tag_keys`, `matrix/features/feature_type`, `matrix/features/genome`, `matrix/features/id`, `matrix/features/name`, `matrix/indices`, `matrix/indptr`, `matrix/shape`.

Inspection-record SHA-256: `733a497a69edb2a1c660edfdcc9287ad53ed15b9508f45f67fed638808c843e1`. Range manifest retained privately with that record.

### GSE306714

[Published HDF5 file](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE306nnn/GSE306714/suppl/GSE306714_filtered_feature_bc_matrix.h5). Inspected 2026-10-03T07:09:05.142616+00:00; source Last-Modified: Fri, 22 Aug 2025 14:47:59 GMT. Full source size: 411,573,088 bytes; retrieved metadata-range bytes: 10,230,624.

Verbatim root attributes:

```json
{
  "filetype": "matrix",
  "group": [
    "T1-Base",
    "T1-Base",
    "T1-Base",
    "T1-Base",
    "T1-Diff",
    "T1-Diff",
    "T1-Diff",
    "T1-Diff",
    "T2-Max",
    "T2-Max",
    "T2-Max",
    "T2-Max"
  ],
  "library_ids": [
    "L1035_1",
    "L1035_2",
    "L1036_1",
    "L1036_2",
    "L1037_1",
    "L1037_2",
    "L1041_1",
    "L1041_2",
    "L1042_1",
    "L1042_2",
    "L1043_1",
    "L1043_2"
  ],
  "original_gem_groups": [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
  ],
  "software_version": "cellranger-9.0.0",
  "version": 2
}
```

Enumerated objects: `matrix`, `matrix/barcodes`, `matrix/data`, `matrix/features`, `matrix/features/_all_tag_keys`, `matrix/features/feature_type`, `matrix/features/genome`, `matrix/features/id`, `matrix/features/name`, `matrix/features/target_sets`, `matrix/features/target_sets/Chromium Human Transcriptome Probe Set v1.1.0`, `matrix/indices`, `matrix/indptr`, `matrix/shape`.

Inspection-record SHA-256: `b764b67fc5bac3ed374b57a1c66fbe571b2fbcb14fae66bfcadb27c870d13af3`. Range manifest retained privately with that record.

## Interpretation boundary

GSE306194 explicitly repeats the nine Donor1/2/3-by-stage library labels and the stage group strings, improving provenance agreement between the matrix and SOFT metadata. This is not independent biological evidence. Scaffold library IDs are kept literally as stored; no unqualified alias repair or Donor1/2/3-to-D7V/R0G correspondence is made.

The enumerated objects are expression-matrix components and feature/barcode fields. This inspection recovered no explicit cross-assay preparation/outcome table. Barcode suffixes, sample titles and root library labels are not by themselves the missing mature-function/lineage join. Unread data values, external sidecars, raw reads and unknown author exports were not exhaustively excluded. No large raw-data download or expression fitting is justified merely to repeat this conclusion.

Read-only inspection helper SHA-256: `fd83f2c3c5a4093be3d90c9ca1f6db17319bdf9b65696c88e1082d1ff2f6a05f`. Runtime reader: h5py 3.16.0, installed only in private task scratch storage. The helper is an inspection aid, not a registered analytical runner or a new source of biological units.
