# Q4a implementation before fragment endpoint exposure

1 November 2026. Implements the exact parent brief from `fd1b8e4`, preserved as
`ACCESSIBILITY_EXTENSION_BRIEF_FROZEN_V1.txt` in this byte-preserving directory.
Its original relative references retain the parent brief's directory context.
Q3a results, reference conflicts and named Figure 5 loci are already exposed.
Complete compressed files and M33 were acquired without calculating endpoints;
literal M33 gene/header records were read. No fragment intervals were counted.

The current source map binds three MatrixMarket RNA triples, three complete
fragment files, their request records and saved-prefix comparisons, M33, the
frozen RNA barcode/gene outputs, and the reference notes. The direct ARC HTML
download returned HTTP 429; already-read primary documentation and independent
parent reading support the dated reference note. This limitation does not change
the acquired fragment/GTF bytes. The custom TdTomato reference hash is not claimed
to match the public M33 GTF.

All GTF parsing, region tabulation, full fragment traversal and numerical outputs
occur through the new committed contract. A locus qualifies only with one M33
gene record, consistent target ID/symbol/chromosome/strand, coherent transcript
boundaries, and three matching source RNA feature records whose TSS spans lie
within the M33 gene body. Exact source-versus-M33 TSS-span agreement is recorded;
coherent annotation differences are explicit, not silently corrected. Incoherence
holds only that locus. Basic-transcript selection/fallback, strand conversion,
clipped +/-2kb window unions and gene-body intervals follow the parent brief.

The full compressed stream validates gzip EOF/CRC, expected file-local headers,
six fields, nonnegative half-open coordinates, positive integer readSupport,
ACGT barcode plus numeric suffix, and +/- fragment strand. Contig blocks must be
contiguous and start coordinates nondecreasing; end ordering is not assumed.
Within each equal-start group, chromosome/start/end/barcode keys must be unique,
as supported by the ARC 2.1 algorithm source in `Q4A_REFERENCE_NOTES_V1.md`.
ReadSupport is never a weight and strand does not create a new duplicate key.
The group-local set avoids storing all fragment keys in memory. No malformed,
duplicate or truncated source is repaired. A failed source receives its exact
line/error and no dependent endpoints; eligible independent sources continue.

Canonical nuclear chromosomes are exactly chr1-19, chrX and chrY. All other
contigs are enumerated separately. Valid canonical rows, including those outside
the four regions, define each allowed barcode's fragment denominator. Barcode
joins preserve the existing translated GEX strings without another translation.
All source attempts finish before library endpoints or count tables are written;
only sources that reached valid EOF/CRC contribute endpoints. Failed partial
attempts remain explicitly distinct in source validation and the summary wording.

RNA is re-read for all source depths, operational mitochondrial counts, detected
genes, the frozen QC membership and four target counts. Every barcode's RNA QC
must equal the frozen Q3a output. Paired sets require both positive RNA and valid
nuclear-fragment depths. The QC subset intersects the identical prior RNA-QC
membership with that paired set. Selection changes are enumerated. For unchanged
sets, counts/denominators/barcode counts must equal prior gene summaries exactly;
transformed RNA summaries must agree within absolute/relative 1e-10, allowing only
floating summation order. Changed sets are recomputed and shown against prior RNA.

The fixed output family has 64 paired rows: two contrasts, two subsets, two
weighting choices, two region definitions and four loci. RNA is repeated across
region families only as a table join, not as new evidence. Source/locus/subset
holds remain explicit and undefined values are empty/null rather than zeros.
Two figure families show primary paired changes and RNA/fragment sensitivity;
the latter shows RNA once because its values do not depend on region definition.
For these new SVGs only, trailing line whitespace is stripped during their first
generation before runner hashes are recorded. Old figures/runs are untouched.

Nine synthetic tests passed before freeze: strand/coordinate conversion, basic
selection/fallback, merging/clipping/boundaries, single counting over multiple
windows, support-weight exclusion, exact barcode/canonical denominator handling,
duplicates/malformed/order/truncation failures, zero-depth/weighting, and RNA
summary behavior under identical versus reduced paired sets. The numerical
equations and literal output tables remain subject to originating independent
review; no population inference or biological acceptance is created here.
