# Metadata execution status — 11 October 2026

The single reserved metadata attempt ran at source
`90c02bad355a52bc9b71ac84ad63a06eda52c525` using the frozen contract and reviewed
Git-equipped runtime. Root verified the private before-dispatch checkpoint and
packet before release. After direct owner approval in the executing worker, root
downloaded the exact evidence archive and independently verified its 64,399 bytes,
SHA-256, ZIP CRC, all 46 member hashes and nine exact source Git blobs. The unchanged
Ravel receipt verifier passes on the preserved local result bytes.

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

The initial private export was denied because prior direct owner approval covered
the runtime archive, not this payload. Direct approval for this archive resolved
that hold; one upload and worker/root readbacks passed, with owner-only sharing
preserved. Its SHA-256 is
`8efd014152febdd429f49632279188435fccb1196445285fe1d9959f2efdc246`.
Private runtime/file locators stay in the operator handoff. The historical
EXPORT_HELD after-run checkpoint remains preserved. The coordinator must append
the completed export/root review and verify a descendant after-run checkpoint
before closing the same attempt; no metadata rerun or restored-ledger activation.

Root accepts the observed sparse-loader memory use as the prerequisite for a
bounded descriptive attempt. This does not qualify full-workload peak memory.
[Review](config/metadata-root-review-v1.json) binds the exact findings; the
[Figure1 execution plan](config/figure1-execution-v1.json) specifies 4 CPUs,
16 GiB, a 3,600-second worker watchdog and verified multipart output recovery.
Figure1 is frozen after root review; dispatch remains held for verified multipart
transport and a new before-dispatch checkpoint. Metadata checkpoint closure passed.
No QC filtering, embedding, Figure1 result, biological inference or scientific
acceptance is claimed.
