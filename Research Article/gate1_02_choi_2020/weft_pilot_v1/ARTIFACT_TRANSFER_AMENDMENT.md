# Artifact recovery amendment — 11 October 2026

Numerical source and frozen contract remain at `b656d06`. The initial artifact
plan used 16 MiB parts; that trial uploaded successfully but could not download
the large part. Its failure and uploaded files remain preserved.

A separate 4 MiB+7 deterministic trial passed cloud upload, authenticated raw
download, per-part hashes and fresh full reconstruction. Root independently
downloaded the canonical manifest and recomputed its deterministic hash anchors.
This supports a bounded transfer attempt, not a retention guarantee.

The [Weft operational amendment](https://github.com/xorca0711/weft/blob/a8da990cca57bdcc19435ff57f0f018a51f5f1a5/records/figure1-artifact-transfer-v2.json)
(SHA-256 `978be234d6a60096bc70cd8a76634540a008fb99797f5ffc6502b0d066356a88`)
supersedes only the artifact part size and effective archive limit in the frozen
execution plan: **4 MiB per part, at most 256 parts / 1 GiB**. The new immutable
job packet must bind this amendment and its qualification record.

The source, scientific contract, methods, output serialization, 4-CPU/16-GiB
budget, one-hour watchdog and offline container controls remain unchanged.
Compression/splitting happens outside the scientific container after preserving
the exact run outputs. Every actual output archive must independently pass its
own downloaded byte hashes, reconstruction, ZIP CRC and member manifest.
Oversize, rejected or uncertain exports hold the job without a blind retry.

This operational change does not authorize a numerical start. A verified
before-dispatch checkpoint and root release are still required.
