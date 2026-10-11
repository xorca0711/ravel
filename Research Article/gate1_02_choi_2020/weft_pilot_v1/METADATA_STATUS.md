# Metadata execution status — 11 October 2026

The single reserved metadata attempt ran at source
`90c02bad355a52bc9b71ac84ad63a06eda52c525` using the frozen contract and reviewed
Git-equipped runtime. Root verified the private before-dispatch checkpoint and
packet before release. These statements summarize the completed worker report;
root has **not yet downloaded the numerical result bytes**.

- One NCBI download matched 349,204,480 bytes and the expected archive SHA-256.
- All nine selected compressed files passed size/hash checks. Three libraries
  passed sparse integrity checks with identical feature ordering.
- Loader elapsed: 190.460 seconds. Cumulative process peak RSS: 945,848 KiB
  (approximately 924 MiB). This is a process high-water mark, not a separate
  independently measured peak for each library.
- Container elapsed: 192.417 seconds; exit 0, no OOM, PID zero and all captured
  process identities absent. The maximum observed cgroup peak was 948,580,352
  bytes; sampling does not establish the final cgroup peak.
- Reported SHA-256: `receipt.json`
  `8b5764789d125d8e785563206e56a33e39240ab84631b8f42936766762b25a0e`;
  `input-readiness.json`
  `e80f61bf465925cadbb043284d34c26cf1f44714903f0d9ee215d739a7e3b86f`.

The new 64,399-byte private evidence archive passed the worker's ZIP CRC and 46
manifest-entry checks, but automatic review denied upload: the prior direct owner
approval covered the runtime archive, not this payload. Its SHA-256 is
`8efd014152febdd429f49632279188435fccb1196445285fe1d9959f2efdc246`.
No upload/readback or alternate transfer occurred. Private runtime/file locators
stay in the operator handoff. The existing attempt remains held for export and
independent result readback; no retry or slot release is authorized. The separate
after-run ledger checkpoint has been uploaded and verified by the coordinator,
with independent root hash/ancestry/integrity and single-attempt state checks.
It records EXPORT_HELD and does not contain the denied evidence archive.

Next: direct approval in the existing worker for this exact archive; verified
upload/readback; root receipt and memory review.
Only then consider freezing the separate descriptive contract. No QC filtering,
embedding, Figure 1 output, biological inference or scientific acceptance is
claimed. A successful metadata run does not qualify the full analysis workload.
