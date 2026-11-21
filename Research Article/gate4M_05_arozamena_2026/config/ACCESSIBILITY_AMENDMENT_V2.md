# Q4a prospective source-semantic amendment v2

Date: 2026-11-01. Article-local candidate: Arz1-P01. Purpose: finite-library
description of four paper-named paired RNA/locus-fragment endpoints in GSE329778.
This amendment follows the originating review in
[the frozen authorization](ACCESSIBILITY_REVIEW_FROZEN_V2.txt). It supersedes the
v1 uniqueness assumption for new execution only. The
[v1 hold](../ACCESSIBILITY_V1_HOLD.md), contract, code and run remain unchanged.

## Exposure and reason

V1 released no accessibility endpoint: each source stopped at its first repeated
coordinate/barcode key. Literal reads established that all three first offending
pairs have opposite strands. Source semantics and those six records are exposed,
as are the paper and prior RNA outcomes. This is not a claim of source corruption
or an outcome-based attempt to recover a desired contrast. ARC documentation's
deduplication description does not establish the physical identity of these
deposited opposite-strand records. The custom reference itself remains unavailable.

## Two fixed count definitions

1. Primary `strand_records`: one per unique
   `(chrom,start,end,barcode,strand)` source record. Repeated same-strand keys fail
   validation even when readSupport differs. Support is never a weight.
2. Sensitivity `coordinate_groups`: one per `(chrom,start,end,barcode)` group,
   explicitly grouping opposite-strand records. This is an alternative measurement
   definition, not a silent repair, a preferred post-outcome choice or a certified
   physical-molecule count.

Each definition applies to BOTH locus-overlap numerators and each barcode's
all-canonical-nuclear denominator. The same sorted stream calculates both, with
one count per locus/region union; overlapping TSS windows never double count a
record/group within a gene. These are fragment-overlap endpoints, distinct from
ARC Peaks feature-matrix cut-site counts. Neither independently certifies molecules.

Full gzip EOF/CRC, expected headers, six-field schema, integer coordinates/support,
positive span/support, barcode syntax, strand, contiguous contig blocks and
nondecreasing starts remain mandatory. Equal-start groups retain all coordinate/
barcode strand bits, so opposite strands need not be adjacent. Same-strand repeats
hold the entire dependent source. No endpoints use partial traversals. All source
attempts finish before any endpoint is released; valid independent source cases
can proceed when another source fails.

Collision diagnostics enumerate coordinate/barcode groups containing opposite
strands overall, canonical nuclear, canonical RNA-allowlisted and noncanonical;
two source records belong to each such group. A compressed barcode table reports
each affected barcode, canonical/noncanonical collision counts and exact RNA
allowlist membership. Locus/region tables report collision groups among all
source barcodes and among RNA-allowlisted barcodes. Count/denominator differences
must reconcile with those diagnostics. Noncanonical contigs, nonallowlisted rows
and zero-depth barcodes remain separately reported.

## Unchanged design and added axis

The original four loci, GRCm39 M33 basic-transcript TSS unions, gene bodies,
two GSE329778 contrasts, exact barcode join, RNA re-read/QC, pooled and
equal-barcode weighting, RNA-QC subset and 1e-10 prior-RNA comparison remain as in
[v1 implementation](ACCESSIBILITY_IMPLEMENTATION_V1.md). No new ATAC threshold,
state calls, inferred animals, peak sets or annotation fallback are introduced.

Verify identical positive-fragment and positive-RNA/fragment paired sets between
definitions; disagreement stops release. On equal sets, RNA is exactly reused
across count definitions and region families and is labelled as reuse in output.
Two definitions x two contrasts x two subsets x two weights x two regions x four
loci gives **128 paired rows**, all retained. Save both full summary families and
64 grouped-minus-record contrast deltas, including the zero RNA delta check.

The primary figure shows RNA and strand-record changes. The sensitivity figure
shows RNA once, every primary region/QC/weight case, and every definition delta
on an explicitly separate scale. No fitted trends, tests, CI, FDR or correlation.
First-generation SVG whitespace cleanup is part of the new plotting code;
previous SVGs remain byte-identical.

## Validation and interpretation

Twelve known-answer tests cover the preserved region/aggregation rules and all
structural failures. The opposite-strand fixture must yield primary=2 and
grouped=1 for BOTH locus counts and denominator; nonadjacent records and excluded
barcodes/contigs are checked. Same-strand duplicates remain rejected. The initial
sandbox test attempt could not write temporary fixtures; the authorized rerun
with normal temporary-directory access passed all 12 tests.

After execution, independently reconstruct M33 intervals and saved-count summary
arithmetic; distinguish that audit from a separate raw-fragment recount. Inspect
both figures. Technical execution and checks do not create human acceptance.
Unknown mouse/preparation independence, shared CTRL, composition, lineage/genotype/
sorting and sparse measurements limit all comparisons. This is a GRCm39 public-M33
adaptation, not exact author replay, state-resolved Q4, promoter validation,
causal regulation, inflammatory memory or regenerative-function evidence.
