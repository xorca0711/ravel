# Join and annotation qualification schema

The [current samples](../../analysis/research/runs/Pg1_metadata_v3_20261108/samples.csv)
are one row per actual GSE/GSM library record. `record_id` and `cohort_id` are
local bookkeeping labels, not author section identifiers. Raw strings and parsed
components must remain separate. [Results and limits](RESULTS.md).

| Fields | Provenance / interpretation |
|---|---|
| `GSE`, `GSM`, `platform` | Deposited series/sample identity; WES is not Xenium |
| `library_name_author`, `title_author` | Exact Library name description and deposited title |
| `patient_id_author` | Author patient number explicitly stated in title; not genotype verified |
| `patient_id_parsed_alias`, `histology_alias_parsed`, `library_alias_suffix` | Parsed alias components under the recorded rule; never collapsed by patient/histology |
| `filename_library_alias`, `filename_alias_status`, `filename_discrepancy_type`, `file_identity_status` | Separate filename text and its agreement/hold; GSM supplies file linkage, not equivalence of aliases |
| `histology_deposited` | Current tissue title category; not a spot/cell label |
| `histology_original`, `histology_reviewed` | Unrecovered per-library review history, deliberately blank; P7 case-level review remains in a note |
| `lesion_id_author`, `block_id`, `section_id`, `ROI_id`, `core_id`, `cell_or_spot_id`, `coordinate_frame` | Unknown here; blanks have explicit reasons, not implied equality or absence |
| `join_level`, `join_status`, `annotation_source`, `source_locator`, `unknown_reason` | Evidence tier and exact boundary; normal versus adjacent-normal context is not guessed |

The crosswalk contains every alias in the union for each platform pair, including
unmatched records. Matching alias strings cannot populate unknown lesion/block/
section fields. `patients.csv` is a separate patient-label membership view.

Future author exports need these minimum schemas before a new contract:

| Product | Keys and required fields | Qualification check / narrow failure |
|---|---|---|
| Specimen manifest | Cohort, patient, lesion, block, section, platform/library/GSM, section order/distance, original/reviewed diagnosis and review source | Unique sample-level identity; unresolved edges stay unknown; no discovery/TMA patient collision |
| Visium annotation table | Section + full barcode; author pathology, state and clone in separate columns; label dictionary, source/version, exclusions/QC | Unique keys and matrix/coordinate coverage; no gene-score replacement; exclusions remain counted |
| Image/ROI table | Section + image ID/hash; image dimensions; physical units/origin/axes; ROI polygon vertices and pathology | Validate bounds, transformations, orientation and overlays using actual images; do not infer geometry from a figure |
| Xenium cell/region export | Section + full cell ID, centroid/boundary, ROI IDs, author states, QC flags, gene panel/count semantics; polygon/registration source | Cell/region uniqueness, membership, overlap and transform agreement; serial sections are not same-cell joins |
| Neighborhood specification | Radius and physical units, center inclusion, eligible cells, edge handling, density denominator, state mapping | Reproduce one prespecified 80-micrometer comparison; nested overlapping neighborhoods are not independent replicates |
| TMA manifest/panel | Distinct cohort + TMA/core→lesion→patient map, retained/excluded cores, exact base/add-on genes | Patient nesting and endpoint coverage before transport; unmeasured genes cannot be imputed as zero |

These are input requirements, not completed QC or a frozen downstream statistical
design. KAC state, RPII morphology, inferred clone, ligand RNA and later fate are
separate fields and measurements. Patient-level precision and inference remain
for each qualified stage's prospective contract.
