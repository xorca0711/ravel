# RNA implementation choices before endpoint exposure

1 November 2026. Implements the parent-authorized Q3a/Q5a brief from commit
`7d7b721`. Its exact Git-blob bytes are preserved in
`RNA_EXTENSION_BRIEF_FROZEN_V1.txt` under this byte-preserving config directory.
It is an archival text copy; embedded relative references retain the original
parent brief's directory context.
The original parent brief remains untouched; Windows checkout newlines do not
define a second scientific specification. Previous freezes remain unchanged.

The seven libraries, four contrasts, eight selected targets, all-source RNA
denominators, transformation after averaging, and at most four cases are fixed
by that brief. Common IDs are read from the frozen metadata v2 output, never used
as normalization denominators. All positive-count source RNA entries contribute
to depth and detection; ATAC entries never do. Output CSVs use explicit empty
numeric fields for undefined endpoints; summary JSON uses null where relevant.
Exact zeros remain zero; no sign threshold or population uncertainty is added.

Source-feature reading before this freeze found the same unique stable ID for
each selected symbol across all seven libraries. The script rechecks those joins
and holds any target that becomes ambiguous. It writes all source RNA ID/symbol
mappings, not only the selected panel. Panel medians/counts use defined selected
targets and explicitly enumerate held values; no replacement targets are allowed.

All seven sources have the same 13 stable IDs named with the exact `mt-` prefix.
HDF5 intervals are `NA` for these genes; MatrixMarket feature coordinates are
empty/-1/-1. Thus the operational mitochondrial definition is the **case-sensitive
source symbol prefix `mt-`**, not a validated chromosome assignment. The script
requires identical nonempty mitochondrial ID/symbol maps across sources; otherwise
only RNA-QC sensitivity is held. This naming definition covers the deposited
mitochondrial coding-gene labels and does not certify complete mitochondrial
transcript annotation. No external reference or alias guess is introduced.

HDF5 is read in 128-column blocks; MatrixMarket entries are streamed in their
already-qualified strict column order. Each barcode's all-RNA depth, positive-gene
count and operational mitochondrial fraction determine its membership before
aggregation. Store only gene-sized accumulation arrays and barcode QC records,
not a dense gene-by-barcode matrix. Counts sum to pooled numerators; fractional
barcode CPMs sum before division by retained barcode count and log2(mean+1).
Empty/zero-depth subsets remain undefined. Complete tables are gzip CSV with
fixed gzip metadata, while small panel/plotting tables are plain CSV.

Two figure families are fixed: primary all-barcode pooled selected-target signed
contrasts, and all four weighting/QC cases for the same targets. Both use signed
log2(CPM+1) differences and separate accession labels, shared scales and no
significance annotations. Their saved panel table is the numerical plotting input.
Eight synthetic tests distinguish denominator, transform order, weighting,
inclusive QC boundaries, mapping holds, zero/empty subsets and sparse formats.

Q4a is a separate source/resource feasibility assessment. It does not alter the
RNA comparisons, select accessibility intervals from RNA outcomes or execute
fragment counting under this contract. Later accessibility work requires its own
source-qualified coordinates, reviewed estimand and freeze.

Before this numerical freeze, bounded 64-KiB fragment-prefix reads revealed that
all three GSE329778 fragment headers identify ARC 2.1.0 and the custom
GRCm39-2024-A_TdTomato reference, conflicting with article/GEO ARC 2.0.2/mm10
statements. The source prefixes/request records are bound as context. RNA joins
remain stable-ID/symbol comparisons without genomic interval transfer; reference
and processing differences further limit cross-deposit interpretation. No mm10
coordinate assumption enters this RNA implementation. Q4a must resolve its own
coordinate/reference compatibility before a recount specification.
