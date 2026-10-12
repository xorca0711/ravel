# Figure1 execution status — 12 October 2026

**Execution reported successful; evidence export and independent result review held.**
The same frozen source b656d06 and original contract were used once, under Weft's
explicit 8 GiB resource and 4 MiB transfer amendments. No methods were changed.
Run: `p001_figure1_v1_f001_d56ee41e13cd4327`.

The worker reports exit 0, no OOM, 196.03 seconds and 2,448,296 KiB peak process
RSS (about 2.33 GiB). Its highest sampled Docker memory was 2.142 GiB; this is a
different measurement scope and may miss peaks. Direct cgroup files were
inaccessible. Terminal PID was 0 and all three captured process identities were
absent. The original Ravel result verifier passed in the worker.

Reported post-QC cells: PBS 4,319; day 14 3,790; day 28 3,574; total 11,683.
Final pAT2 was absent. These are **worker reports, not independently verified
scientific results**. The output tables and images remain unreviewed by root.
Each timepoint is one pooled library; these descriptive outputs cannot establish
animal-level treatment effects, lineage or a mechanism. No claim grade or RQ changed.

The evidence archive is 105,848,914 bytes in 26 parts. Its reported SHA-256 is
`e1f8ee36d87111dc9ef7defbcddaf04f9633851c63a57ce25f03474881ae69c7`.
The transfer manifest hash is
`f73b416c381adde7022f233e62495123936d99c66b5b93da56a1ffce56a02a29`.
Automatic approval review rejected the first upload because earlier approvals
covered other archives. No successful upload or retry occurred; the attempt and
slot remain EXPORT_HELD. The owner subsequently approved the exact payload
directly in the worker. Its archive/part recheck passed, then the cloud turn
failed at a usage limit. Complete transfer remains unverified. Existing approval
remains recorded; no repeat approval is needed for the same action and payload.

Root independently verified the separate after-run ledger backup, its unchanged
21-event parent prefix, all 24 events, two scientific rows including the earlier
metadata job, database/schema/integrity and read-only restoration. Its SHA-256 is
`82e461d5ab42e04368aabef7778f7658b57a3e6e81388439f31a7ea42c123b19`.
This confirms the recorded hold; it does not substitute for result readback.
Before dispatch, stale coordinator state required explicit operator recovery to
a new active private copy after reconciliation with the original unstarted worker
container. Preserved old state and recovery ancestry remain available; the cause
is unknown and persistent coordinator storage is not guaranteed.

[Weft's execution record](https://github.com/xorca0711/weft/blob/codex/cloud-job-controls-20261011/records/choi-figure1-execution-20261012.json)
owns packet, recovery and transfer evidence. [Earlier preparation](https://github.com/xorca0711/weft/blob/codex/cloud-job-controls-20261011/records/choi-figure1-resumed-preparation-20261011.json)
preserves the mount failure, disk hold and owner-approved cleanup.

Next: after cloud access returns, reconcile existing upload receipts and remote
metadata, resume the exact approved export without duplicates, review the original receipt and every
member hash, reconcile QC/denominator/marker tables, inspect the figures, and
resolve publication of the exact outputs under existing governance. Then record
the bounded discrepancy and candidate/no-candidate review. Do not rerun the
analysis, fabricate a partial receipt, weaken validators or mark the stage complete.

## Publication dependency

The worker's inventory reports a 385,675,968-byte H5AD output. This exceeds
[GitHub's ordinary 100 MiB file limit](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
Ravel's unchanged receipt validator requires every declared output to be available
and hash-matched. After independent artifact recovery, choose and review a durable
publication route before registering this numerical receipt in a clean-clone CI
workflow. No large file was force-added, LFS storage enabled, frozen output omitted
or validator weakened. Private evidence recovery remains the immediate next step.
