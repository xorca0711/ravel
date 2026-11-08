# Metadata serialization correction

V1 loaded the main Seurat RDS under the frozen contract, then failed while
recursively serializing its package-version object. No metadata inventory or
normalization samples were emitted. The failed receipt, logs, load status and
resource measurement remain unchanged in `nn26_rds_metadata_v1`.

V2 converts `numeric_version` to character before recursive list handling.
The inspected object class (Seurat) and peak operational memory were exposed;
all original sampling, QC, normalization and biological scope remain frozen.
No source bytes, annotations or thresholds were altered to obtain a result.
