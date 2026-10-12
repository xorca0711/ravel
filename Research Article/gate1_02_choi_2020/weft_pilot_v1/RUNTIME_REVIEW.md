# Git-equipped runtime review — 11 October 2026

The executing worker uploaded the approved 156,333-byte sanitized archive once
to the existing owner-only private Drive folder. It downloaded and verified the
bytes. Root independently fetched it through Drive and verified SHA-256
`40acb134342e3aab355d1537f64cf796e7d488dbf0733bcd6bc817955ca0a7b4`,
ZIP CRC, all 28 manifest entries, safe paths and 395,703 expanded bytes.
Metadata showed the expected parent and only an owner permission. Private file
locators remain outside public Git.

[runtime_git_v3](runtime_git_v3/README.txt) preserves the exact archive contents.
Its internal statements that it was not uploaded describe its creation time;
this dated review records the subsequent transfer. The old `runtime/` recipe
and `config/preparation-checks.json` remain historical evidence, superseded for
execution by this review and [metadata execution plan](config/metadata-execution-v1.json).

The pinned image is
`sha256:253c1935ee7245153d8a4d88197e3f2b47055a2fcf743eaf4f00d255efde6ecc`.
Root reviewed the recipe, locks, public package provenance, source and watchdog
harnesses, and qualification reports. The worker verified three signed Debian
indexes, 31 package hashes/sizes and 61 wheels before its offline final build.
The reports record Git 2.47.3, GNU timeout 9.7, package consistency, the unchanged
numerical fixture, committed-source checks and unchanged Ravel runner test.
The new-image launcher-loss fixture terminated in 7.14428 seconds, with no OOM
and all four captured process identities absent. These are synthetic checks,
not evidence of real-input memory readiness or biological validity.

The metadata contract is now frozen for integrity and sparse loading only,
with a 4-CPU, 8-GiB, 256-PID, 1,200-second offline container and a one-second
kill-after watchdog. Source, Git metadata and inputs are read-only. One fresh
output allocation and bounded temporary storage are writable. The actual source
commit, contract hash, attempt and verified before-dispatch checkpoint must be
bound by the sole manual coordinator before execution. No gate is bypassed.

The separate descriptive contract remains draft. Review metadata structure,
loader memory and actual run receipts before freezing it. Known prior outcomes
remain exposed; pooled libraries do not become independent animal replicates.
