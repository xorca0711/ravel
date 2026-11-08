# RNA execution readiness — 8 November 2026

The owner requested a cloud attempt after the local resource check, and guidance
in the repository-root AGENTS.md for future hardware constraints. This is an
operational record, not an RNA qualification receipt.

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

## Minimal resumption requirements

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

The local source and animal branches are complete within their recorded scope;
cloud readiness is the exact outstanding technical dependency for stages 4–5.
