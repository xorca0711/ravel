# S3 v1: finite-track ranks near annotation-based TSS proxies

18 November 2026. Prospective, exposed description under the approved
[S3 amendment](S3_AMENDMENT_V1.md). No adapted ATAC window means or ranks have
been calculated at this specification. S3Q headers and its fixed 100-base
readability counts, prior RNA outcomes and published findings were exposed.

## Purpose, unit and estimand

The organizing question remains what accompanies epithelial inflammatory history
after recovery. The executable question here is narrower: how do control/history
libraries differ in relative signal ordering near annotated protein-coding gene
boundaries at D6 and D30, and how sensitive is that pattern to window width?
The measured unit is a deposited ATAC library, two per history/time group.
Source-reported biological replication/pooling is retained, with exact animal
membership, overlap and cross-assay matching unresolved. Windows and genes are
dependent features, never extra biological replicates.

Unknown processing and bulk composition can change ordering without a within-cell
regulatory change. A stable ordering pattern would support this finite-source
description only; weak or width-sensitive differences would narrow it. No outcome
establishes endogenous memory, repair, absolute opening or the original distal
retained-region classification.

## Annotation-fixed universe

Use the existing GENCODE mouse M9 GTF, SHA-256
`93406cb8e6835339b0e64d0ad904a6d3e4527333f62a3a24f9a53c16083ca9fa`.
Retain every `gene` feature with `gene_type=protein_coding` on chr1–19/X.
For one-based inclusive GTF coordinates, the zero-based proxy is `start−1` on
the plus strand and `end−1` on the minus strand. It is an **annotation-based
TSS proxy**, not necessarily the dominant or only transcript promoter.

Primary windows are `[TSS−1000,TSS+1000)`; the sole width sensitivity uses
`[TSS−2000,TSS+2000)`. Clip to the qualified chromosome bounds and retain flags.
Collapse identical coordinates before ranking; preserve all gene-to-window
mappings, strands and overlapping nonidentical windows. Annotation-only preview
found **21,775 genes / 21,760 distinct windows** at each width, 15 additional gene
mappings and no clipping. Mechanically verify those counts in the governed run.
No expression/outcome filter, peak calling or region winner selection is used.
Y/M and unmapped noncanonical contigs are outside this stated universe. Noncoding
examples such as Xist are unassayed, not assigned zero signal.

## Exact signal, ranks and contrasts

Read each window at base resolution through pinned pybbi, keeping an open file
handle per library. Use no zoom approximation. Preserve encoded zeros; request
unreported values as `NaN`. Fail on unexpected missing/nonfinite values inside
a valid clipped window, preserving progress for review. Do not discard a window
or substitute zero to obtain a complete matrix. Retain the exact arithmetic
window mean and number of encoded-zero bases for every library/window/width.

For N unique windows in a library, ascending one-based average ranks give
`P = 100 × (average_rank − 1)/(N − 1)`. Exact equal exported means are tied;
no biological rounding threshold is introduced. The library mean of P is
**50 percentile points** (equivalently mean unit-scaled rank 0.5), including ties.
Thus the average history/control rank contrast over the whole universe is zero
by construction and cannot represent global opening.

At each time, `Delta_t = mean(P_history) − mean(P_control)`, in percentile points.
Retain all four unpaired `H_i−C_j` contrasts and their min/max; they are spread
diagnostics, not independent replicates or confidence intervals. Use `1e-10`
percentile points only as a computational zero rule. No population p-values,
equivalence margin, response classes or original memory-domain counts are produced.

Positive affine changes to an individual track's window means preserve ranks.
Unknown nonlinear base processing, clipping, smoothing and mixture changes may
not. Relative rank changes depend on this universe, and a higher rank does not
require increased local signal. Protein-coding boundary windows cannot adjudicate
distal memory domains or noncoding loci.

## Frozen summaries, examples and figures

For each width/time report signed/absolute Delta quantiles (0, .25, .5, .75, .9,
.95, 1), four-contrast range widths/zero inclusion, and computational-zero
fractions. Describe the fraction with smaller absolute D30 than D6 displacement
without labeling recovery/equivalence. Compare widths using continuous Delta
shifts, sign changes and the same complete window anchors. Library diagnostics
retain zero-mean/tied-window counts, largest tie groups and average rank.

Fixed examples are published **Aim2** (M9 `ENSMUSG00000037860.15`) and the six
already frozen S4 examples, in their original order. Retain every requested
example with eligibility/reason; never substitute a new winner. Their earlier
selection is exposed and they do not estimate representative biological behavior.
Two PNG/PDF figures show (1) D6/D30 rank contrasts, absolute-displacement
distributions and width sensitivity; (2) every eligible example's eight library
ranks at both widths, with explicit unassayed panels. No lines imply matched
animals or trajectories; no absolute deposited-signal differences are inferred.

## Verification and resource boundary

Artificial tests cover ties/constant vectors, rank-average constraints, monotone
affine scaling, duplicate mappings, strand/coordinate conversion, boundary clipping,
noncoding omission, unpaired contrasts, missing/nonfinite rejection and sensitivity
sign handling. Reuse the qualified upstream toy reader test; verify its interval
iterator before freezing. Do not calculate real window outcomes in tests.

Independent verification reparses the GTF and checks every interval/mapping,
recomputes all tie-aware ranks, contrasts and summaries from exported means, and
checks fixed example selection. Independently reread 32 annotation-order-spaced
windows per width plus all eligible fixed examples, in every library. Integrate
the reader's exact interval iterator with overlap lengths and `math.fsum`, separately
from the primary base-array mean. Require complete nonoverlapping coverage and
agreement at scaled tolerance `1e-10`. This verifies arithmetic, not independent
biological replication or a different binary-decoder implementation.

The two widths require 1,044,480,000 base-value visits across eight libraries
(8.36 GB if all float64 values were materialized). Stream individual windows;
do not materialize that array. Preserve compressed means/mappings, summaries,
progress, verification and two figures within **50 MiB** of derived artifacts.
The provisional analysis-entrypoint budget is **two hours**; the WSL extraction
and exact reread stop at **2 GiB peak RSS**. Check resources periodically and
preserve valid partial output on failure. Runtime is not yet benchmarked, and
input-hash/runner overhead is recorded separately. Exceeding a budget triggers
review of the concrete bottleneck, not a biological/source-unavailability finding.

## Pre-freeze implementation check

The final artificial fixture passed 12,238 independent checks on 71 eligible
genes and 70 windows per width, including clipped/duplicate mappings. Maximum
scaled arithmetic error was `6.5370e-15`; a corrupted contrast was rejected.
The supported toy BigWig passed base-array versus interval integration and
missing/nonfinite rejection. No research-track window was read. Exported means
are parsed with float round-trip preservation so serialization cannot change ties.
