# Arz1-P01 Q4a: prospective deposited-GRCm39 locus comparison

1 November 2026. Originating review of Q4a feasibility authorizes source acquisition
and the bounded description below, after an exact-input numerical freeze. Q3a RNA
outcomes, the article's Figure 5d/e interpretation and all source conflicts are
exposed. This extension does not replace within-state Q3/Q4 or exact author replay.

## Question and units

For the four loci named in the published Figure 5d/e text (Cd74, Tiam1, Cd83,
Ciita), do RNA and common-region fragment-count changes differ in the deposited
GSE329778 libraries, and how sensitive is that description to region definition,
RNA-QC selection and barcode-depth weighting? Keep LGR5 minus CTRL and KRT20 minus
CTRL separate; they share CTRL. Each library is a finite descriptive unit, with
barcodes nested within it. No population tests, confidence intervals, fitted
four-gene correlation, cell-state attribution or independent replication count.

Composition, lineage/genotype/sorting selection, processing, sparse counts and
region choice are consequential alternatives. A nonparallel RNA/fragment pattern
does not distinguish those from regulatory priming. The four loci come from the
paper, not favorable RNA outcomes; the prior eight-target RNA panel is unchanged.

## Source qualification and coordinate choice

Acquire and hash the three complete compressed GSE329778 fragment files and
GENCODE M33 primary-assembly GTF from the qualified public URLs. Recheck actual
disk capacity; retain compressed inputs without creating full uncompressed files
or downloading the multi-gigabyte reference archive. Verify full sizes and saved
prefix agreement. Bind complete hashes, acquisition records, reference documentation,
M33 source/version and all three processed RNA triples in the prospective contract.

Use the fragments' actual GRCm39 reference and ARC 2.1 coordinate convention. The
article/GEO ARC 2.0.2/mm10 statement conflicts with file-local headers. No liftOver
or mm10 region transfer is authorized. Public M33 is an explicit annotation
adaptation, not a claim to reproduce the custom TdTomato GTF/hash or the paper's
integrated peak object. Require matching stable IDs, symbols and chromosomes for
the four loci; inspect gene strand and source TSS-span correspondence. Record
annotation/filter differences. An incoherent source/coordinate mapping holds its
locus rather than permitting a guessed alias or interval.

Primary regions: for each target gene, take every M33 transcript carrying the
`basic` tag; if a gene has none, take all its M33 transcripts and record that
fallback. Derive each transcript's strand-aware TSS, convert to zero-based
coordinates, and use [TSS - 2000, TSS + 2000), lower bound clipped at zero. Merge
overlapping/adjacent windows within each gene. A fragment overlapping several
windows of one gene counts once for that gene. These are annotation-defined
TSS-proximal windows, not experimentally validated promoters or the original
Figure 5 peak intervals. Do not expand a source TSS envelope into one long promoter.

Regional sensitivity: the M33 gene-record body interval, converted from GTF
one-based inclusive to zero-based half-open. Gene-body overlap is a different
locus-level proxy, not a second replicate or a promoter mechanism. Freeze both
rules before counts; no outcome-driven windows, peak selection or additional loci.

## Fragment counting, common barcodes and RNA correspondence

Stream each complete gzip file. Validate headers, six-field structure, coordinates,
read-support and strand fields against qualified ARC 2.1 documentation, gzip
completion/CRC, exact barcode correspondence and source coordinate ordering.
Count each documented collapsed fragment row once; read-support multiplicity is
not a weight. Detect duplicate fragment keys in the supported sorted groups; do
not silently repair or collapse unexpected duplicates. A malformed/truncated or
incompatible source stops dependent endpoints and records the exact failure.

Valid-fragment denominator: collapsed rows on nuclear canonical mouse chromosomes
chr1 through chr19, chrX and chrY. Enumerate exclusions including mitochondrial,
reporter and other contigs. Restrict biological summaries to exact deposited RNA
barcodes, preserving suffixes. Record non-allowlisted rows, zero-fragment barcodes,
depth and fragment-covered fractions. Fragment coverage does not certify singlets,
author QC or animal identity. Overlap uses half-open interval intersection and
counts once per fragment/gene/region family; counts may overlap between genes,
so their sum is never the normalization denominator.

Paired primary population: deposited positive-RNA barcodes with positive valid
fragment depth. Sensitivity population: that same set additionally passing the
already frozen RNA-only QC. Reuse its exact definitions and barcode membership;
do not introduce ATAC-count thresholds or pretend to reconstruct complete author
QC. Enumerate changes from the original RNA populations. Empty populations or
unsupported target mappings yield explicit local holds, not zero-valued effects.

For both RNA and fragments use the same eligible barcodes in each case. Re-read
the three RNA matrices for the four target counts; verify all-source RNA depths
and RNA-QC membership against the frozen Q3a outputs. If no barcodes change, the
recomputed RNA summaries must match the corresponding prior all-gene summaries.
If fragment absence changes the paired set, report that selection and its RNA
consequence explicitly. Do not substitute unpaired library RNA values silently.

## Fixed endpoints, outputs and checks

Pooled fragment CPM = 1e6 * summed overlapping unique fragments / summed valid
nuclear fragments. Equal-barcode fragment CPM averages each eligible barcode's
fragment CPM. Apply log2(CPM + 1) after either aggregation. RNA uses the previously
specified all-source RNA denominators and the same transformation. Report each
post-minus-CTRL transformed difference separately; RNA and fragment measurements
remain distinct modalities despite the shared scale notation.

The fixed family is two contrasts x two barcode subsets x two weighting choices
x two region definitions for four loci. RNA values reused across region families
are not new measurements. Retain complete region provenance, barcode-level counts
and denominators, all library summaries, raw counts/detection fractions, all
paired contrasts, source/structural qualification and local holds. Sparse or tiny
differences remain visible; a sign alone is not a meaningful biological effect.

Use a committed contract and runner. Full fragment parsing/structural validation
and counting may share one frozen streaming pass, with endpoints released only
after complete valid input traversal. This avoids a redundant full parse while
retaining stop conditions and immutable failed-run evidence. No endpoint is
calculated during source acquisition or interval selection. Test known-answer
GTF coordinate/strand conversion, basic/fallback rules, window merging and boundary
overlap; double-overlap counting; read-support exclusion; duplicate/malformed
records; canonical denominator and barcode selection; weighting/zero-depth cases;
and RNA reuse on identical versus reduced barcode sets.

Produce at most two substantive PNG/SVG figure families from saved plotting
tables: paired RNA/fragment changes and bounded regional/weighting/QC sensitivity.
No fitted trend or significance marks. Parent numerical and individual visual
review precede gallery integration. Keep all metadata and RNA freezes unchanged.
Successful execution remains a deposited-data measurement adaptation, not
scientific acceptance, causal memory, TF occupancy or later regeneration linkage.
