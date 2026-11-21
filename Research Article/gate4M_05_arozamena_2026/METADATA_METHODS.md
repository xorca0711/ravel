# Prospective source and input qualification

1 November 2026. **Arz1-P01, Q0-Q2 only.** Parent scope is fixed by commit
`565d8a95339593ca1f6da3385b08eb1f62e4c03d`, [README](README.md) and
[literature context](LITERATURE_CONTEXT.md). The purpose is to decide which
deposited comparisons can be described and which require missing source evidence.
The measured objects are source records, library matrices and identifiers, not
independent animals or biological effects. The principal threat is a mistaken
source/assay/unit join, especially treating inferred donors or repeated barcodes
as validated mice or the same cell across libraries.

## Prior reading and exposure

Published interpretations, indexed Results and source metadata were exposed.
Before this freeze, the technical chat retrieved exact GEO SOFT records, linked
BioSamples, public directory/file lists, Europe PMC full-text XML and supplementary
archive, Crossref metadata, processed files and request logs. It read literal
source records and selected source-file headers, article Methods Sec22/Sec26 and
the donor-related supplementary/peer-review text. Reporting-summary page 3 and
peer-review page 30 were rendered and visually inspected. No processed-matrix
dimensions, expression contrasts, state calls or numerical biological endpoints
were computed before freeze. Synthetic matrices alone exercise the parser.

The article and GEO reverse the labels Multiome 1/2 for the two lineage cohorts.
Run-number equivalence is unresolved; retain the accession and source condition
instead of silently swapping names. The article describes pooled preparations
and inferred donor groupings. The peer-review response says independent SNP
validation was unavailable and qualifies the groupings as consistency checks.
Neither source statements nor this audit certify mouse-level independence.

## Frozen inputs and acquisition

[Intake manifest](sources/intake_v1.json) fixes all acquired bytes, provenance
records and seven multiome library file groups. Public HTTP request dates, URLs,
headers, sizes, hashes and exact failures are retained in the source directory.
Source downloads are acquisition, not biological analysis. All six accessions
stay separate; the immune scRNA dataset does not become epithelial state data.
Processed files are preferred; no FASTQ, BAM, large fragment or bulk bigWig is
downloaded for this metadata contract. Deferred remote links remain inventoried.
The article PDF URL returned HTML, publisher supplementary CDN DNS failed, and
the PMC OA-package manifest returned 404. Europe PMC's ordinary public full-text
and supplementary endpoints succeeded. No authentication/challenge bypass.

## Metadata operations

1. Preserve literal series/sample fields, repeated characteristics, deposited-file
   links and exact GEO-to-BioSample relations. Check each sample has one matching
   public BioSample source crosswalk. A BioSample accession is not an animal ID.
2. Validate seven processed multiome matrices: declared shape, unique stable
   feature IDs and barcodes, feature types, sparse pointers/index bounds and
   finite nonnegative integer entries. Repeated gene names remain separate IDs.
   HDF5 data are checked in bounded chunks. MatrixMarket files are streamed.
3. Verify HDF5 coordinate uniqueness through strict within-column ordering. For
   MatrixMarket, strict row- or column-major ordering proves uniqueness; otherwise
   report uniqueness unverified rather than silently deduplicating entries.
   No zero-filling, feature merging, normalization or filtering is performed.
4. Report source feature counts/fingerprints, shared matrix-column axes and the
   number of columns with observed entries in both RNA and Peaks feature types.
   This qualifies count-level modality pairing only. It does not prove a singlet,
   a cell-state identity, a donor or an animal/preparation crosswalk.
5. Report all pairwise feature-ID and barcode overlaps, including self-pairs.
   Exact coordinates are the feature identity; no inferred gene links or peak
   union is constructed. Reused 10x barcodes across libraries do not establish
   same-cell or same-animal overlap, and distinct files do not prove independence.
6. Check immune DGE matrix widths, finite nonnegative values, unique gene IDs,
   and exact barcode-list order. Inspect bulk RNA headers, identifiers and numeric
   validity; fractional Salmon estimates are recorded, not coerced to integers.
   No expression totals, gene programs, library comparisons or statistical tests.
7. Inventory the HDF5 schema and the source workbook's text-cell labels with
   sheet/cell locators. Do not compute workbook figure values. These delimit
   available annotation/unit fields; no absence claim extends beyond inspected
   source coverage. Index article identity and section/supplement locators.

## Runtime, validation and limits

Use existing Python 3.12.10, NumPy 2.5.1 and h5py 3.16.0 from the already
qualified isolated runtime. `ARZ1_H5PY_PATH` can identify that existing dependency
directory; no package installation. Physical memory was about 16.76 GB total and
1.17 GB available at the source-read checkpoint. Free workspace-drive space was
about 5.48 GB before acquisition and 5.06 GB after processed acquisition; these
are changing runtime observations, not guaranteed capacity. No dense multiome
matrix or all-entry coordinate set is materialized.

Synthetic checks cover repeated source fields, stable-ID/barcode uniqueness,
shared RNA/peak axes, unsigned CSC column resets, duplicate coordinates, invalid
values, MatrixMarket entry counts, fractional bulk estimates and LF/no-overwrite
output behavior. Freeze contract, code, tests, manifest and this specification
before running in a new directory. A source hash mismatch stops the run. A
qualified file's local schema failure is retained as a component hold while
independent source inspection continues. Existing run directories are refused.
All authored text uses LF prospectively; source bytes remain exact.

Inspect actual source-to-output identities and numerical metadata independently
after execution. Return separate eligibility for exact author replay, narrower
fixed-library description, within-state/composition analysis, paired-feature
analysis and later-function linkage. Q3-Q6 biological estimands remain subject
to a source-supported parent brief and a separate freeze. No population inference,
state assignment, donor demultiplexing, pathway/memory claim or scientific
acceptance is created by metadata completion. A current service refusal stops
its affected dependent scope and is recorded verbatim.
