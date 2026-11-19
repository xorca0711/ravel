# S3Q v1: original ATAC track and coordinate-source qualification

18 November 2026. Metadata qualification after reviewed S4B; owner `Nk17-P01`.
The coordinator authorized acquisition, supported project-local runtime preparation
and source/header/readability qualification. A biological S3 comparison still
requires review of its concrete estimand before a new numerical run.

## Decision and bounded inputs

The published accessibility premise requires a qualified deposited signal and
region definition. RNA S4/S4B cannot supply either. Determine whether the eight
original D6/D30 tracks have the expected accession identities, readable BigWig
metadata and mm10 chromosome lengths. Reuse the coordinator's bounded original
coordinate-source review rather than repeat it. This can qualify inputs or
name a precise remaining uncertainty; it does not measure retention or discover
memory domains. The main validity threat is mistaking compatible file structure
for known normalization, biological independence or the author's region universe.

The existing S1M map identifies GSM2441001–1008 as D6 control/history and D30
control/history, two deposited libraries per group. Preserve source-reported
pooled preparations and explicit biological-replicate wording alongside unknown
exact pool membership, animal overlap and cross-assay matching. No independence
is fabricated from filenames. D180, raw reads and other studies are excluded.

All eight original files were acquired before this metadata specification,
totalling 6,679,503,736 bytes. URLs are taken from the saved GSE92967 SOFT and
joined to the frozen S1M crosswalk. Two simultaneous downloads used normal
Windows curl/Schannel TLS, original sizes, unchanged response validators and
local SHA-256 records. Partial files were protected by URL/size/Last-Modified
checks; no track transfer failed or resumed. Local SHA-256 is not an asserted
author checksum. Original HEAD and transfer specifications are both preserved.
Input bytes are hash-bound in the new contract before header inspection.

The prior Python urllib TLS failure was on the separate UCSC chromosome-reference
request, after successful GEO HEAD checks. Normal Windows curl retrieved the
same HTTPS reference with verification enabled. No TLS setting was changed.
An initial acquisition-specification filename collision stopped before transfer;
the earlier specification was retained and a separate transfer specification used.

## Runtime and permitted measurements

Actual default WSL is aarch64, glibc 2.43, Python 3.14.4 without pip/compiler or
an installed reader. A project-local ignored environment now uses pinned uv
0.13.9, Python 3.13.18, pybbi 0.4.2 and NumPy 2.5.5. Both wheels matched the
CPython 3.13/aarch64 ABI and their published SHA-256 values. No global package
or independent study environment changed. A pinned upstream toy BigWig passed
recognition, exact chromosome-dictionary and first-three-value checks. A missing
preinstalled package was an environment issue, not a source hold.

Under the metadata contract, the supported reader obtains each file's chromosome
dictionary, stored header summary and zoom levels. A prespecified chr1 interval,
10,000,000–10,000,100 (zero-based, half-open), checks bounded data readability;
only length/finite/missing counts are retained, not the values. Missing values
are requested as `NaN`; no zero imputation or condition comparison occurs.
Header-wide min/mean/max/std are stored-file metadata, not newly estimated
differential accessibility. No custom BigWig parser is used.

Compare chromosome names/lengths to the canonical UCSC mm10 dictionary. Record
missing chromosomes, extras and mismatches; do not silently relabel them or infer
normalization from M/Y presence. The coordinator's 18 November original-source
review found MOESM9 Figure 3 source data contains F3d pathway binomial p-values
and an empty sheet, rather than peak coordinates; targeted reporting-PDF headings
yielded no identified coordinate table. This is bounded source coverage, not proof
that original coordinates never exist. No workbook or broad paper scan is repeated.

## Verification and interpretation limit

The runner binds the eight track hashes, source/provenance files, chromosome
reference and runtime evidence. Independent standard-library
verification checks acquisition/input identity, saved SOFT and S1M joins,
chromosome rows and compatibility flags, stored-header consistency, bounded
query shape. The reader's exact
toy-fixture checks are reused. This does not independently decode every genomic
data block or supply biological replication.

GEO's saved processing metadata states mm10 alignment and `.bw` format without
a signal unit. The coordinator supplied a bounded paper-method note concerning
per-base Z scores excluding MT/Y, 500-bp bins and peak analyses; that note does
not establish the deposited file scale or exact background filter. Do not weaken
the analysis plan's boundary: unresolved between-track scales permit within-track
visualization only. Return an explicit S3 method, assumptions, region/exposure and
missingness rules for review before biological execution. Preserve all metadata
outcomes, including failed compatibility or unavailable coordinate definitions.
