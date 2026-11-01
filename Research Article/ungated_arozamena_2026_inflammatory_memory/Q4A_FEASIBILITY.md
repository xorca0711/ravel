# Q4a: third-deposit fragment feasibility

1 November 2026. **Source/resource assessment only; no accessibility endpoint.**
A streamed, four-locus **GSE329778-only GRCm39 adaptation is technically feasible**,
subject to a separate reviewed interval/normalization specification and full input
qualification. Exact mm10 author replay is held by a newly observed reference
conflict. This does not justify a blanket hold on every fragment-based extension.

## Source conflict and bounded acquisition

Ordinary public HTTPS byte ranges returned HTTP 206 for the first **65,536 bytes**
of each linked fragment file, 196,608 compressed bytes total. Full files were not
downloaded. Original prefixes and response headers remain under ignored
`raw_data/Arz1/q4a_source_reading_20261101/`; these six files are bound as context
in the [RNA contract](config/rna_contract_v1.json). Their hashes certify only the
saved prefixes, never the complete fragment files.

| File / source accession | Full size from Content-Range | Prefix SHA256 |
|---|---:|---|
| CTRL / GSM9711145 | 402,473,208 | `02d6c6e6e11e348e169888fd0d612a73d9e86aa0719e053238e729bea1447dae` |
| KRT20 / GSM9711147 | 512,718,078 | `f43d5f15e48ca4e30eb4050513d245816bcfa4c2770dafba4ae5bfd8db9e33a6` |
| LGR5 / GSM9711149 | 793,731,383 | `635ea52e30dc1e7af9be3dda9695a9dde78b7420b65247e85d00ced7e37c21d5` |

URLs follow `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM9711nnn/{GSM}/suppl/{GSM}_atac_fragments_{condition}.tsv.gz`.
Exact request times, Last-Modified values, ranges and URLs are in the saved JSON
records. Original GEO SOFT/file-list versions remain in the source intake manifest.

All three fragment headers identify `cellranger-arc-2.1.0`, reference version
`2024-A`, and a custom reference path ending in
`refdata-cellranger-arc-GRCm39-2024-A_TdTomato/GRCm39`. They share source-reported
FASTA hash `0a38e50e7b7b743504ba5e83f12b6076c5090224` and GTF hash
`b25e6d75b49c486fe87988387b4fa7209f6060bc`. These are literal header hash strings,
not independently verified checksums of reference files acquired here.

Article Sec26 and GSE329778 SOFT instead say ARC 2.0.2 / mm10. The SOFT also
describes HDF5 output filenames although this deposit supplies MatrixMarket
triples. Preserve both statements: the deposited fragment headers are stronger
file-local evidence for their actual reference, but do not reconstruct how the
paper's integrated objects were generated. First/second-deposit reference and
processing provenance remain separate; no guessed liftOver or mm10 recount.

## Coordinates, barcodes and annotation

The [ARC 2.1 fragment specification](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/outputs/fragments-file)
defines zero-based, end-exclusive fragment coordinates, one row per collapsed
unique fragment, read-support multiplicity, and a sixth fragment-strand field.
The inspected source records have that six-field structure. Read support must
not silently multiply distinct-fragment counts. Fragment strand is not gene strand.

Literal records from the saved prefixes match exact filtered-matrix barcodes:
CTRL `CAACTAGGTAATCGGC-1`, KRT20 `TGCTTCATCAAGCTTA-1`, LGR5
`CGCCACACAGAAATGC-1`. This demonstrates compatibility without suffix stripping
or inferred translation. It is not a full-file barcode join or a guarantee that
every filtered barcode has fragments; that must be checked at acquisition/counting.
Fragments may include additional non-filtered barcodes; retain an explicit source
barcode allowlist and report unmatched/zero-coverage barcodes in the later design.

Source feature records for the four Fig. 5d/e loci agree across the three triples:

| Symbol / stable ID | Literal feature coordinate fields |
|---|---|
| Cd74 / ENSMUSG00000024610 | chr18, 60936919, 60936928 |
| Tiam1 / ENSMUSG00000002489 | chr16, 89615239, 89940657 |
| Cd83 / ENSMUSG00000015396 | chr13, 43938250, 43938251 |
| Ciita / ENSMUSG00000022504 | chr16, 10297922, 10307647 |

The [ARC 2.1 matrix specification](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/feature-barcode-matrices)
defines those fields as a zero-based interval spanning selected transcript TSSs,
using basic-tagged transcripts when available. They are not automatically a gene
body, a single promoter or a strand-specific annotation. Tiam1 spans many bases
between alternative TSSs; expanding that envelope and calling it a promoter would
misstate the measurement. No interval was chosen from the RNA results.

A concrete matched annotation source exists. [ARC reference build notes, mouse
2024-A section](https://www.10xgenomics.com/support/software/cell-ranger-arc/downloads/ref-build-steps)
specify GRCm39 Ensembl release 110 FASTA and **GENCODE M33 primary-assembly GTF**,
with ID-version removal and biotype/readthrough filtering. The linked source is
`https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M33/gencode.vM33.primary_assembly.annotation.gtf.gz`;
[GENCODE M33](https://www.gencodegenes.org/mouse/release_M33.html) documents the
assembly/version. The study's custom TdTomato augmentation and GTF hash are not
yet reproduced. A public M33 annotation can define an explicitly adapted endpoint
without claiming exact identity to that custom reference.

As a separate bounded cross-check, five small Ensembl REST records (release query
and four stable-ID lookups) were acquired with request logs under
`raw_data/Arz1/q4a_annotation_reading_20261101/`. They report **release 116,
GRCm39**, matching symbols/chromosomes and gene strands (Cd74 +; Tiam1 −;
Cd83 +; Ciita +). This newer annotation is not substituted for M33 or the custom
reference, and no numerical coordinate-validation result is claimed. The REST documentation
web open timed out; ordinary public API responses succeeded. No access bypass.

## Fit-for-purpose design and remaining qualification

For parent review, use only the paper-named Cd74/Tiam1/Cd83/Ciita loci and the two
separate GSE329778 LGR5-minus-CTRL and KRT20-minus-CTRL descriptions. A coherent
adaptation could count unique fragments overlapping **M33-defined gene bodies**,
or a separately justified, fixed strand-aware TSS-region rule. The next brief
must choose one interpretation and specify multi-transcript handling, overlap
boundaries, zero depth, valid contigs, denominators and any bounded sensitivity.
Gene-body overlap is a locus-level accessibility proxy, not promoter activation,
TF binding, causal RNA regulation or persistent memory. Published nonparallel
RNA/accessibility is already an exposed premise, not a new mechanism.

Before freezing numerical Q4a: acquire/hash M33 and the three complete compressed
fragment files; verify target ID/symbol/strand/assembly records and zero-based
conversion; reconcile source TSS spans with that chosen annotation; validate full
six-field fragment structure, header identity and exact barcode overlap. Freeze
common intervals once for all three conditions. Preserve any annotation-version
disagreement and custom-reference uncertainty. A conflict that prevents a coherent
coordinate mapping is a local locus/source hold, not permission to invent an alias.

Counting can stream one compressed file at a time, filter to that library's exact
barcodes, accumulate four fixed interval counts plus each barcode's complete
valid-fragment denominator, and write a small barcode-by-locus table. This requires
no genome-sized array, no full uncompressed copy, no all-peak reanalysis and no
intersection of independently called peak rows. The same barcode axis permits
bounded RNA/accessibility descriptions; it does not supply missing epithelial
states or independent animals. Coverage/denominator definitions remain part of
the next reviewed estimand, not an executed choice here.

The three compressed files total **1,708,922,669 bytes**. C had **5,019,049,984 bytes
free** during assessment; preserving all compressed sources would leave about
3.31 GB before annotation and small outputs. Existing Python gzip/streaming tools
are sufficient; four loci across the deposited barcodes need little count-array
memory. Full throughput/wall time has not been benchmarked. No `.tbi` was listed
in the inspected deposit, so sequential reading is the supported plan. No storage
or software blocker is currently established. Recheck free space at acquisition;
do not manufacture a resource hold or download the multi-gigabyte reference archive.

**Disposition:** source-supported conditional feasibility for a deposited-GRCm39
four-locus adaptation; exact author replay held. Remaining work is a reviewed
region/counting brief and explicit full-source qualification, not discovery of a
nonexistent universal peak intersection. No accessibility counts or biological
contrasts were calculated in this assessment.
