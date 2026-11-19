# S6B: fixed-marker D6 source consistency check

19 November 2026. Owner `Nk17-P01`. The coordinator approved this bounded scope
and its implementation/freeze/governed execution after closing reviewed S6A at
`ccc91cd`. This is exposed descriptive source QC, not a new sex classifier,
mechanism or independent study. No complete new D6 five-marker profile has been
read by this implementation before freeze. Earlier S2 counts/Xist profiles and
S4 marker results are already exposed.

## Purpose, comparison and unit

[S4](S4_RESULTS_V1.md) found near-zero Xist/high four Y-linked marker profiles in
two D30 baseline libraries despite recorded female metadata. [S2](S2_RESULTS_V1.md)
and [S5M v2](S5M_RESULTS_V2.md) retain an acute D6 comparison, including stronger
D6 RNA–ATAC proxy association, but neither establishes RNA/ATAC animal matching.
The bounded question is whether the same fixed RNA-marker readout also raises
source-consistency questions in the four original D6 RNA libraries. Consistency
would localize the observed discrepancy without proving D6 free of confounding;
discordance would widen uncertainty without identifying its cause.

The unit is a deposited RNA library, with published pooled biological-replicate
evidence and unresolved exact pool/animal membership. The endpoint is each
fixed transcript's supplied count and its normalized RNA abundance. Metadata,
mixture, mapping/annotation, background or expression changes can contribute to
a marker pattern. This readout does not determine biological sex, pairing,
contamination, mislabeled animals or the source of an RNA/ATAC association.
There is no group-effect test, fitted threshold or high/low classifier.

## Exact scope and source joins

| Library | Source state | Run | Frozen S2 display label |
|---|---|---|---|
| GSM2440985 | D6 control | SRR5133553 | D6_C1 |
| GSM2440986 | D6 control | SRR5133554 | D6_C2 |
| GSM2440987 | D6 acute inflamed | SRR5133555 | D6_A1 |
| GSM2440988 | D6 acute inflamed | SRR5133556 | D6_A2 |

All four are recorded as female in the frozen S1M v2 characteristics, and as
HiSeq4000 paired-end. Preserve the complete recorded characteristics and source
filename. The `Postinflamed` filename/metadata history field does not replace
the qualified acute D6 state label. Check GSM/run/BioSample/assay/day/history/
instrument/layout/count-filename joins against S1M and frozen S2 sample QC.
Replicate suffixes are accession labels, not cross-assay matching evidence.

Use exactly these previously fixed M9 identities, in this order:

| Marker | Versioned M9 ID | Chromosome | Gene type |
|---|---|---|---|
| Xist | ENSMUSG00000086503.3 | chrX | lincRNA |
| Ddx3y | ENSMUSG00000069045.11 | chrY | protein_coding |
| Eif2s3y | ENSMUSG00000069049.11 | chrY | protein_coding |
| Kdm5d | ENSMUSG00000056673.14 | chrY | protein_coding |
| Uty | ENSMUSG00000068457.14 | chrY | protein_coding |

Recheck the exact gene-feature name/ID/chromosome/type against the already acquired
GENCODE M9 GTF, SHA-256 `93406cb8e6835339b0e64d0ad904a6d3e4527333f62a3a24f9a53c16083ca9fa`.
Each must be unique and present in the count files. An absent, version-changed or
ambiguous identity stops dependent calculation; never substitute another marker.
Read four original two-column count files already bound by S2. Require 47,729
unique nonnegative integer-count rows in the same exact versioned order. Recheck
each full-library count total against frozen S2; do not use a five-marker subtotal.

## Arithmetic, outputs and limits

Reuse each exact S2 D6 median-of-ratios factor and total-count factor from frozen
`sample_qc.tsv`; do not re-estimate either factor. For each of the twenty
marker/library combinations save raw count, raw/frozen MOR factor,
raw/frozen total-count factor, `CPM = raw * 10^6 / full-library gene-count total`,
and `log2(CPM+1)`. Zero remains a measured zero, and log2(0+1)=0. Store original
metadata, annotation fields and an explicit raw-zero flag. No ratio between
markers, fitted classifier, new marker, exclusion, batch correction, sex
assignment, RNA/ATAC pairing or upstream numerical rerun is allowed.

Save `annotation.tsv` (5), `sample_qc.tsv` (4), `marker_qc.tsv` (20),
`metadata.json`, `runtime.json`, `verification.json`, and
`fig01_fixed_d6_markers.png`/`.pdf` (eight declared outputs). The figure shows all
raw counts and one shared-scale log2(CPM+1) heatmap, without row scaling,
clustering, significance marks or per-marker outcome selection. All other
normalizations remain in the table. Record metadata as recorded, not inferred.

The primary implementation uses pandas for counts and a GTF attribute parser;
the independent verifier uses stdlib gzip/CSV, a separate attribute parser and
50-digit Decimal arithmetic including the logarithm. It checks all count-file
structure/full totals, source joins, frozen factors, exact marker identities,
all output values/semantics and metadata. Use scaled tolerance 1e-10 only for
floating arithmetic; labels/counts/IDs/zeros and joins are exact. Verify receipt
integrity and inspect the actual figure separately. These are computational
checks, not independent biological replication or animal-level validation.

Five artificial tests passed before freeze: full-library CPM denominator and
fixed factors, zero/log semantics, source/metadata join drift, malformed/negative/
noninteger/duplicate counts and gene order, ambiguous/version-changed annotation,
and semantic/numeric output tampering. The main artificial fixture passed 477
independent checks, maximum scaled error 1.04349e-16. A test initially exposed
blank-line handling in a rewritten GTF fixture; both readers now skip blank lines
and reject malformed records, without relaxing exact annotation requirements.
No real QC run failed or actual new marker value was inspected in these tests.

Bind four count files, M9 annotation, the S1M v2 crosswalk, frozen S2 sample QC
and this method (eight inputs), together with the three scripts. Freeze and
commit before the governed run `naik2017_s6b_d6_marker_qc_v1`. Stop on source/hash/
unit/join/annotation/arithmetic disagreement and retain failed/partial evidence.
Return all twenty rows and the actual figure for coordinator review. Preserve
S2/S3/S4/S5/S6A evidence, the EDF6g mapping hold, and the original-domain and
individual-animal limits. No human scientific decision or external action follows.
