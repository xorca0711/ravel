# D180 public-track acquisition checkpoint

19 November 2026. Owner `Nk17-P01`. The coordinator authorized acquisition and
hash recording after the [S6 assessment](S6_DECISION_V1.md). This is a transport
checkpoint, not a biological run or a reader/chromosome qualification result.
The four original GSE92967 tracks were acquired with two bounded concurrent
HTTPS transfers using Windows curl. All processes exited 0 and each local byte
length matched the prior HTTP-header length. Transport permits up to two transient
retries; no claim about the actual retry count is made here.

Acquisition started at 04:02:07 UTC; the manifest completed at
2026-11-19T04:05:24.314110+00:00. Total local track bytes: **3,118,510,945**.

| Original public file | Bytes | Local SHA-256 |
|---|---:|---|
| [GSM2652413](https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/GSM2652413/suppl/GSM2652413_PI_D180_mm10_ATAC_Rep_1_.bw) | 796,895,019 | `e0c262db9921a2c8302d13b77beb599628414d4ab1471598dfdd7eb392d953bb` |
| [GSM2652414](https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/GSM2652414/suppl/GSM2652414_PI_D180_mm10_ATAC_Rep_2_.bw) | 806,609,609 | `7064d1c2dd1eb9dc7b33cb987f954fe0862ad3da86aebed403b6c61abbd3d1c3` |
| [GSM2652415](https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/GSM2652415/suppl/GSM2652415_Ctrl_D180_mm10_ATAC_Rep_1_.bw) | 731,787,530 | `ac150ffaa673d91177ce2e17cf3d6423818865f86c4ef4c741b2c2ded1eb2d98` |
| [GSM2652416](https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2652nnn/GSM2652416/suppl/GSM2652416_Ctrl_D180_mm10_ATAC_Rep_2_.bw) | 783,218,787 | `f97e2055517bbd287f9da1f9322a232d06b97a075e9c6e589e15337e099a491a` |

Files, HTTP response headers, transfer logs and `acquisition_manifest_v1.json`
are retained under ignored `raw_data/naik2017_s6_d180_sources_v1/`. The acquisition
script is retained at `raw_data/naik2017_s6_preparation/acquire_d180_v1.py`, SHA-256
`81e299bc3baf0068f89204bcd1d6f3190979a7bb0c516deb60e21a61fa03d73b`. Source URLs above preserve the declared GEO identity;
size and hash records establish local file identity, not signal comparability.

No signal values, ranks or D180 effects have been extracted. Next, qualify file
readability and chromosome compatibility using the existing S3 runtime, then
prepare a separate reviewed contract with the exact S3 universe, both widths,
rank formula and all five fixed paper anchors. Original D180 tracks are paired-end
HiSeq2500; the D6/D30 ATAC tracks are paired-end HiSeq4000. Processing units,
original retained-domain coordinates and exact biological matching remain
unresolved. No raw FASTQs, new software, cloud executor or external inquiry was
used for this acquisition. See [S1M metadata](S1M_RESULTS_V2.md) and the
[S3 runtime](S3_RUNTIME_V1.md) for their separately qualified scope.
