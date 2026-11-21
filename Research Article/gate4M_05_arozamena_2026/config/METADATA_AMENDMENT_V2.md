# Empty-record adapter and bounded reuse

1 November 2026. **Arz1-P01 metadata amendment, before v2 execution.**
[V1 methods](../METADATA_METHODS.md) and its immutable
[receipt](../../../analysis/research/runs/arz1_source_qualification_v1/receipt.json)
remain authoritative for the first execution. V1 checked four HDF5 libraries
and held the three GSE329778 files with `Missing feature-type column`.

Targeted source reading found valid six-column feature records, including an
explicit third-column modality, interleaved with empty lines. The v1 reader
treated those empty lines as malformed feature records. This is a parser-coverage
limitation, not evidence of missing biological information. Initial source byte
inspection showed LF line endings, not CRCRLF. All original bytes, v1 code,
contract and outputs are preserved. Metadata counts from v1 and these literal
source rows are now exposed; no biological endpoint has been computed.

V2 skips **only empty/whitespace-only records**, counts them separately for each
features/barcodes/MatrixMarket file, and retains nonempty-record order. Nonempty
feature records must still contain an explicit, nonempty third-column type.
Malformed records, duplicate identifiers/barcodes, dimension disagreement or
invalid numeric entries remain errors; no modality is guessed or repaired.
The number of nonempty feature and barcode records must equal the declared matrix
dimensions. Every stored matrix entry is streamed and validated. Strict row- or
column-major coordinate order certifies uniqueness; unsorted uniqueness remains
explicitly unverified. Record feature-field widths and comment/empty counts.

Reuse the four successful HDF5 qualifications from the preserved v1 receipt and
matrix inventory. Read only their feature IDs/types and barcodes to establish
cross-format overlaps, checking the v1 ordered fingerprints; do not repeat their
count-integrity scans, dense-table checks or source-document parsing. Consolidate
the four preserved records with the three amended inspections in a fresh v2 run.
Report all seven-library pairwise barcode/feature overlaps and, only if all seven
qualify structurally, the exact feature-ID intersection across all seven. This
intersection is metadata availability, not a selected biological program or
proof that peak calling/coverage is identical. No peak union or missing-zero fill.

Five new synthetic tests cover interleaved empty records, explicit type retention,
the preserved v1 failure, malformed nonempty records, post-removal dimensions,
duplicate barcodes and invalid count values. The v2 input/code set and this
amendment are committed before execution. V1 is a historical completed metadata
run with component holds; v2 supersedes only those holds if its checks pass.
No state/donor inference, normalization, biological comparison or Q3-Q6 execution
is introduced. Parent review still determines the later numerical brief.
