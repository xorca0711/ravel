# S6C prospective method: D180 on the exact frozen S3 TSS-proxy universe

19 November 2026. Owner `Nk17-P01`. **Coordinator-approved for implementation, tests,
freeze and governed execution after D6; D180 effects have not run.** The coordinator permits one exposed
contract with fail-closed metadata qualification before dependent extraction.
This avoids a redundant metadata-only full run while preserving every check and
its output. [Acquisition](D180_ACQUISITION_V1.md) is complete; the existing
[S3 runtime](S3_RUNTIME_V1.md) is reused without installation or a S3 rerun.

## Question, estimand and interpretation boundary

The published premise is long-lived accessibility after inflammation (Naik 2017,
Fig.3 and the established Larsen/Cowley literature). Frozen [S3](S3_RESULTS_V1.md)
shows heterogeneous relative TSS-proxy displacement with smaller aggregate
absolute D30 than D6 contrasts. The remaining descriptive question is how those
same windows behave at D180, relative to the frozen D30 description, with D6 as
the acute reference. Mixed, smaller, larger or opposite rank differences all
remain informative. This is shared-source durability description, not an original
retained-domain reproduction, global opening, absolute signal decay, repair or
chromatin-memory maintenance mechanism. No D180 RNA is available in this map.

The measured endpoint is within-library percentile rank of the exact annotation-
boundary window mean, then mean PI minus mean control rank in percentile points.
Library is the computational sampling unit. Published pooled biological-replicate
evidence is retained, but exact pool/animal identities and cross-time/cross-assay
matching remain unresolved. D180 is HiSeq2500 paired-end; D6/D30 ATAC is HiSeq4000
paired-end. Unknown processing units, mixture and this platform/time difference
are major validity threats. A rank comparison does not resolve them or create
independent replication. Prior published D180 displays, S3 effects and all fixed
anchors are exposed; freeze does not make this confirmatory.

## Exact inputs and ordered qualification

The four acquired original tracks are GSM2652413/14 (PI; SRR5657347/48) and
GSM2652415/16 (Ctrl; SRR5657349/50), with the exact URLs/lengths/SHA-256 values in
the acquisition checkpoint. Bind those files and manifest, S1M v2 library
crosswalk, existing mm10 chromosome sizes, S3Q header/qualification evidence,
project-local runtime locks/smoke record, this method, and the frozen S3
`windows.tsv`, `gene_window_map.tsv.gz`, `window_effects.tsv.gz` and receipt.
No additional download or raw-read workflow is included.

Before reading any research-window values, verify all four track hashes/source
identity and unique D180 assay/history/run joins; recognize BigWig; save complete
header/chromosome dictionaries. Every chromosome required by frozen S3 windows
must be present at exactly the saved mm10 length. Report all other chromosome
matches/differences separately without adding unused chromosomes to the universe.
Check the preserved S3 window IDs/coordinates/flanks and mapping count against
its receipt and annotation identity. Any required dictionary/identity mismatch
stops all dependent D180 extraction; retain the failed qualification record.

The extraction itself checks readability for every required interval, failing on
missing/nonfinite values without dropping windows or silently substituting zero.
This provides a fail-closed full-window readability result; preliminary header
success alone is not called complete signal qualification. Save file metadata,
identity joins, qualification decisions and extraction progress in the same run.

## Frozen universe, signal and rank semantics

Use the exact S3 interval file, not a regenerated or RNA-selected universe:
21,760 unique windows and 21,775 protein-coding M9 gene mappings at each flank,
chr1–19/X. The primary flank is 1,000 bp, sensitivity 2,000 bp. Preserve every
interval, annotation boundary, duplicate-gene mapping and clipping flag. The
original S3 file has no clipping. No retained-domain BED, peak calls, selected
positive loci, new genomic widths or noncoding/Y/M expansion are introduced.

Use the already qualified pybbi base-array reader with open file handles, no zoom
approximation, and missing values requested as NaN. Stream exact window means
and encoded-zero-base counts, retaining round-trip float serialization. Rank
exact equal exported means with ascending average ranks in each library/width:
`P = 100 * (average_rank - 1) / (N - 1)`. Exact ties are not biologically rounded.
Each library's mean P is 50 and each complete-universe mean PI−Ctrl difference is
zero by construction. Neither is evidence of unchanged global accessibility.

For D180 save four ranks, `Delta180 = mean(PI ranks) - mean(Ctrl ranks)`, all four
unpaired PI_i−Ctrl_j contrasts and their min/max/width. Their range is a spread
diagnostic, not a CI or four independent replicates. Reuse S3's 1e-10 percentile-
point computational zero rule and range-zero inclusion. Keep encoded-zero/local-
mean-zero, contrast computational zero and range-includes-zero flags separate.
A locally constant-zero window can change rank when the rest of the distribution
or tie mass changes; preserve those observations without calling local opening.

## Exact summaries, cross-time comparisons and anchors

For each width save signed and absolute Delta180 quantiles at
0, .25, .5, .75, .9, .95, 1 using S3's linear interpolation; range-width quantiles;
fraction whose four-contrast range includes zero; computational-zero fraction;
and the constrained whole-universe mean contrast. Save per-library zero-mean
counts, tied-window fraction, largest tie group and mean rank.

Join the frozen S3 D6/D30 values by exact window/anchor/flank keys, checking all
coordinates and a one-to-one complete join. Do not re-extract or rerun either
old timepoint. For each width, primary D180-versus-D30 and reference D180-versus-
D6 summaries are: signed `Delta180-DeltaT` and absolute-magnitude difference
`abs(Delta180)-abs(DeltaT)` quantiles at the same seven probabilities; fractions
with smaller/larger absolute displacement or a difference within the 1e-10
computational rule; opposite-sign fraction using the S3 rule (both nonzero,
opposite signs, denominator all 21,760 windows); and computational-zero status
change fraction. These are comparisons of finite relative-order descriptions,
not matched-animal longitudinal effects, recovery classes or equivalent states.
No extra correlation model, population test or selected persistent subset is fit.

For width sensitivity, join on the same anchor IDs and save D180 signed/absolute
2-kb-minus-1-kb contrast-shift quantiles, sign-flip fraction and computational-zero
status-change fraction, with the same all-anchor denominator as S3.

Retain all five previously fixed paper anchors in this exact order at both widths:

| Anchor | Exact M9 ID | Frozen anchor key |
|---|---|---|
| Aim2 | ENSMUSG00000037860.15 | chr1:173350878 |
| Casp1 | ENSMUSG00000025888.5 | chr9:5298516 |
| Il1b | ENSMUSG00000027398.13 | chr2:129371138 |
| Il1r1 | ENSMUSG00000026072.12 | chr1:40225079 |
| Il18 | ENSMUSG00000039217.12 | chr9:50575272 |

Save all twelve D6/D30/D180 library ranks, the three group contrasts and their
four-unpaired-comparison ranges, both widths, local means and zero flags for
these anchors. No unfavorable anchor is dropped or replaced. These are exposed
published examples, not representative or independent evidence. The older S3
six outcome-selected RNA examples remain preserved in S3 but are not a new
D180 selection list.

Two PNG/PDF figures are planned: (1) complete-window D180 versus frozen D30/D6
rank contrasts, absolute-displacement distributions at all three times, and
D180 width sensitivity; (2) all five anchors at both widths with each library's
rank, grouped by time and condition. No lines imply matched animals; group
means/contrast-range diagnostics are labeled as such. Raw signal magnitudes are
not compared across tracks as normalized accessibility.

## Verification, resources and return

Artificial tests must verify unchanged window/mapping joins, complete source
membership, dictionary failure before extraction, ties/rank-average constraints,
zero/range semantics, all four unpaired contrasts, all summary rules and the
fixed five-anchor manifest. Reuse the existing qualified reader/toy semantics.
No actual D180 window values are read before the reviewed method and exact
input/code-bound contract are committed frozen.

Independently verify every coordinate/join, tie-aware rank, contrast, zero/range
flag, summary and fixed-anchor value from exported means, separately from the
main reducer. Reread the union of 32 annotation-order-spaced frozen windows per
width and the five fixed anchors in each of four libraries (at most 296 rereads),
using the reader's interval iterator, overlap lengths and math.fsum rather than
the primary base-array mean. Require complete nonoverlapping coverage and scaled
agreement within 1e-10; this is not a second binary decoder or biological replicate.
Verify receipt integrity separately and inspect both actual figures.

The two widths require 522,240,000 base-value visits across four libraries;
stream windows rather than materializing approximately 4.18 GB of float64 values.
Reuse the S3 envelope: at most 2 GiB extraction/readback peak RSS, a provisional
two-hour analysis-entrypoint budget, and at most 50 MiB of derived artifacts.
Record actual timing/peak RSS/storage and preserve failure/partial evidence. A
resource failure triggers a specific feasibility review, not a source-wide
absence claim. Return the verified result and figures for coordinator review
before final S6 synthesis. Preserve original-domain, processing and individual-
animal/mapping limits; no external inquiry, publication or human claim acceptance.

## Implementation checkpoint before freeze

19 November: S6B is reviewed and preserved at `ba5afa4`. Seven constructed-source
tests passed, including 14,235 independent fixture checks (maximum scaled error
1.24701e-14). Tests cover complete source membership, metadata/hash/length drift,
unchanged window/mapping/anchor identities, exact ties, local-zero versus rank-zero
and range-zero semantics, missing/duplicate/nonfinite signal, full coverage, all
summary arithmetic and tampering. A required chromosome mismatch in the last of
four artificial headers caused zero signal fetches and preserved the failed
qualification record. Both artificial layouts were inspected. Figure labels
explicitly distinguish acute D6 from D30/D180 prior inflammation and unresolved
pool membership. No real D180 window signal was read for these tests.

The implementation binds seventeen inputs and eight code dependencies (five new
scripts plus three immutable S3 helper modules). It preserves twenty-one declared
outputs: exact windows/mapping copies, source manifest, all headers and ordered
qualification, verification-window manifest, all D180 means/zeros and progress,
interval readbacks/progress, complete twelve-library effects, D180 diagnostics,
summary, all five anchor identities/values, two PNG/PDF pairs, runtime and
independent verification. Existing S3 values remain bit-for-bit equal as decoded
floats in the combined export. A single exposed contract precedes all dependent
source qualification and extraction; header success alone is not full signal
qualification. Extraction completion and independent interval checks supply the
separate full-window coverage result.
