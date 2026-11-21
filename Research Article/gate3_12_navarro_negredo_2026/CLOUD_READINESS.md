# RNA execution readiness — 8 November 2026

**Execution addendum (8 November 2026):** the retained runtime and exact RDS were reverified, and frozen metadata/descriptive stages have now executed. See [RNA_RESULTS.md](RNA_RESULTS.md) for actual peak memory, warnings, receipts and scientific holds. The readiness-only state below is historical.

The owner requested a cloud attempt after the local resource check, and guidance
in the repository-root AGENTS.md for future hardware constraints. This is an
operational record, not an RNA qualification receipt.

## Earlier checkpoint: runtime and acquisition verified

On 8 November 2026 the owner started cloud chat
`01a1ba3e-f795-73e9-aa71-4c20e962d094` (**Acquire authorized IL10 RDS**) with
explicit scope to prepare an isolated runtime and acquire the main RDS without
biological inspection. Its completed execution logs were checked from the
Ravel chat. They supersede the initial network/runtime blockers below.

- **Network:** the launched policy includes `zenodo.org`; the exact authorized
  file endpoint returned HTTP 200 and matching publisher metadata.
- **Runtime:** isolated R 4.5.0, Matrix 1.7-3 and SeuratObject 5.0.2 under
  `/tmp/navarro_2026`. SeuratObject was rebuilt against this runtime after
  binary-version warnings. Synthetic v3 and v5 Seurat serialization and sparse
  access tests both passed. **Full Seurat is not installed.** The launcher is
  `/tmp/navarro_2026/bin/Rscript`; runtime instructions are in
  `/tmp/navarro_2026/README.txt` on that executor.
- **Acquisition:** only `/tmp/navarro_2026/data/IL10_svz_seurat.rds`, made
  read-only (`0444`), was acquired. Exact size **2,188,161,276 bytes** and MD5
  **`ce9bf02e41665e00e11cd1b262114506`** match Zenodo. SHA-256 is
  **`b1fa0ce7c6ff19e5d207caff9548e5ec2dacd5a3cdb4fa0fc01b5874a15d2559`**.
  Independent `stat`, GNU `md5sum` and GNU `sha256sum` checks passed at
  **2026-11-08 08:38:17 UTC**. Zenodo supplies no SHA-256 reference; that hash
  matched two full-file reads, not an external publisher hash.
- **Resources at completion:** 16 GiB cgroup memory limit; 2,623,672,320 bytes
  used and 14,556,196,864 bytes headroom; CPU quota four cores; 6,895,386,624
  bytes free under `/tmp`. `/tmp` is **tmpfs**, so the retained RDS consumes
  memory. These observations do not establish peak memory for `readRDS`.
- **Scope:** no acquired biological object was deserialized, no RNA analysis
  ran, no additional biological file was acquired, and the mounted Weft
  repository was untouched. Ravel code has not yet been transferred there.

Source evidence on that cloud executor: `evidence/acquisition.json`,
`evidence/readiness.json`, `logs/r-smoke-test.log`, and
`logs/independent-verification.log`, all relative to `/tmp/navarro_2026`.
The checked chat output for command `exec-574b0805-1acc-4006-985e-2c08db284c5b`
contains the acquisition manifest and readiness/resource/scope fields; command
`exec-2f53c4a8-3662-4123-92b2-5d0c849a2d82` records both successful synthetic
tests after the rebuild. This is a record of that completed run, not a new
live resource probe or a guarantee that temporary files survive replacement
of the executor.

**No further environment-setting change is currently demonstrated as necessary
for metadata qualification.** A separately named Ravel pilot is not required.
The local machine's missing R and memory pressure remain; the cloud supplies
the working runtime. Actual object compatibility and loading memory remain
untested. The overall scientific plan is therefore not complete.

Next: refresh the executor's state and confirm retained inputs; transfer the
scoped Ravel code through an authorized path, freeze the metadata contract
against the verified SHA-256, and use the repository runner for bounded sparse
object qualification. Any concrete missing dependency or resource failure must
be recorded. Resolve aliases/doses/layers before a separately frozen pooled
RNA description. Preserve the one-pool-per-condition interpretation limit.

## Initial reconnaissance — superseded operational snapshot

The following records the earlier attempt, before the owner's new cloud chat
successfully acquired the file and prepared R. Its failed access observations
remain historical evidence, not the current blocker.

Local Windows ARM64 observations: 16.76 GB total RAM, approximately 1.82 GB
available at inspection; approximately 113 GB free workspace disk. Rscript was
absent from PATH and checked ordinary R/Conda locations; WSL was not installed.
No registered SSH compute target exists in NGS Analysis Workbench. A normal
load of the 2.19 GB compressed RDS was not attempted under that memory pressure.

The cloud launcher exposed only `weft-pilot` (runnable) and `weft` (not runnable),
both configured for Weft. At the owner's request to try a separate cloud session,
readiness chat `01a1ba23-44bd-73e1-8811-d8ebb699b0b6` used an isolated temporary
workspace. **No Weft repository, account, or environment setting was changed.**
The selected environment was a compute reconnaissance route, not the Ravel
project's source checkout. This distinction was clarified with the owner.

That cloud reported Debian 13 x86_64, five available CPUs, a 16 GiB cgroup memory
limit with about 50 MiB used at inspection, no swap, 9,441,325,056 bytes free
under /tmp and approximately 32 GB free on the root filesystem. Sparse object
qualification is plausible there, but compressed size cannot establish peak
readRDS memory. R/Rscript and Seurat packages were not present; no packages
were installed. The approved Debian package route responded, but local APT
metadata did not yet provide an R candidate.

Zenodo was absent from the enforced network allowlist; both exact metadata and
RDS requests failed with HTTP CONNECT 403. The cloud session lacked environment
change tools. **No RDS was downloaded, no checksum was verified for its contents,
and no biological object inspection occurred.** The owner was subsequently told
to leave Weft configuration unchanged. A distinct environment named “Ravel
pilot” is not required; a suitable authorized Ravel workspace/executor is.

### Original resumption checklist (items 1–3 now completed for the new executor)

1. Select or provision a suitable cloud/remote environment for Ravel, preserving
   unrelated repositories. The available local connector lists/launches saved
   environments but does not create their configurations. Refresh actual
   resource and network observations on that executor.
2. Permit public `zenodo.org` access through the environment's normal approved
   policy flow. Preserve unrelated domains and settings; do not bypass a denial.
   Prepare R plus compatible Matrix/SeuratObject/Seurat through allowed package
   sources, recording versions. Additional domains need actual dependency
   evidence rather than broad speculative allowlisting.
3. Acquire **only** `IL10_svz_seurat.rds` from
   [Zenodo's exact file](https://zenodo.org/api/records/17594828/files/IL10_svz_seurat.rds/content).
   Manifest size: 2,188,161,276 bytes; MD5:
   `ce9bf02e41665e00e11cd1b262114506`. Stream acquisition/hashes; record SHA-256,
   memory and disk. Do not infer content verification from the manifest.
4. Transfer the scoped Ravel specification/code by an authorized path without
   pushing this branch automatically. Register, freeze and commit a separate
   object-metadata contract with exact input/code hashes; use the repository
   runner on the verified executor. Preserve runtime facts and receipts.
5. Inspect slots/layers, identities, counts/alignment and exclusions without a
   dense whole-transcriptome copy. Resolve actual alias/dose mappings before
   the separately frozen pooled RNA description. Resource/runtime readiness
   does not relax biological units or permit population inference.

The local source and animal branches are complete within their recorded scope.
Runtime/acquisition readiness is now established by the newer evidence above;
the frozen object-qualification stage and subsequent description remain pending.
