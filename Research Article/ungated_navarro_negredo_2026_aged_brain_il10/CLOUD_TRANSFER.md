# Scoped cloud RNA handoff

8 November 2026. Integrate the new Nn26-P01 cloud commits with the desktop
source/animal branch. The cloud base is
`471d0c2f8b3b5fef287aea5173325436901fceac`, also confirmed as remote main at
delivery. Checkout: `/workspace/navarro_2026/ravel`, branch
`codex/navarro-cloud-rna`. No push was performed.

## Review entrypoints

- [RNA report and four SVGs](RNA_RESULTS.md).
- [Seven-stage ledger](STAGE_STATUS.md).
- [Machine-readable completion summary](../../analysis/research/runs/nn26_completion_archive_v1/completion_summary.json).
- [All marker summaries](../../analysis/research/runs/nn26_pooled_rna_description_v1/summaries.tsv)
  and [all contrasts](../../analysis/research/runs/nn26_pooled_rna_description_v1/contrasts.tsv).
- [Description receipt](../../analysis/research/runs/nn26_pooled_rna_description_v1/receipt.json),
  frozen at `bdead215f9f9882ab187659c5241f4118ed3dff7`.
- [Source/code and alias qualification](../../analysis/research/runs/nn26_qualification_review_v1/qualification.json).

The bundle includes new scoped commits and their exact frozen scripts, configs,
contracts, receipts, numerical tables, sparse audit extracts and plots. It omits
the RDS, raw author archive, runtime, installed dependencies and older animal
plots/scripts/receipts. The small transferred context is retained in Git history;
Git stores identical blobs once. Existing desktop evidence must be preserved
during integration, including all earlier registered contracts and receipts.
Do not replace the parent registry wholesale with the scoped executor registry.

## Input provenance and restoration

The exact fourteen transferred files were verified against supplied SHA-256
values at import commit `6012e06d2f48abcf52c16a5f999b60c0db7a25af`.
Three texts had entity escaping from transport; one HTML/XML entity decode
recovered the original supplied hashes. Expected hashes were never revised.
The four earlier source-qualification JSONs remain byte-identical, including
their CRLF line endings. Current prose entrypoints now link the RNA addendum;
their original imported bytes remain in that commit.

Three supplied/operational JSON inputs are preserved byte-for-byte in the
[registered completion archive](../../analysis/research/runs/nn26_completion_archive_v1/source_archive_manifest.json).
Their original `source_context/*.json` locations are ignored acquisition-input
paths. The runner's frozen contracts retain those original paths and hashes.
For a new executor, restore each archive file to its manifest `restore_path`
before running preflight with `--inputs`. This is a copy of exact bytes, not a
revision of frozen evidence. The registered archive keeps source provenance
covered by the unchanged gate instead of misclassifying source inputs as code
or registering them as scientific outputs before execution.

The main RDS remains read-only in both the original tmpfs location
`/tmp/navarro_2026/data/IL10_svz_seurat.rds` and the cloud runner's disk-backed
`raw_data/navarro_2026/IL10_svz_seurat.rds`. Size: 2,188,161,276 bytes; MD5:
`ce9bf02e41665e00e11cd1b262114506`; SHA-256:
`b1fa0ce7c6ff19e5d207caff9548e5ec2dacd5a3cdb4fa0fc01b5874a15d2559`.
Zenodo supplies MD5; SHA-256 was established by full local byte reads, not an
external publisher reference. Exact source:
<https://zenodo.org/api/records/17594828/files/IL10_svz_seurat.rds/content>.

The allowed author ZIP is 46,370 bytes, MD5
`d34352f0ef77547f8f7f9180edeffd5d`, SHA-256
`32a26233f686adc621fb8da27d68bb7935395ba44be0380cb27b3325277c1481`.
Its version is v1.0.0, archive prefix commit `c08010b`; exact source:
<https://zenodo.org/api/records/18174039/files/PalomaNavarro/TargetingImmuneCellsSVZ-v1.0.0.zip/content>.
The cloud raw-input path is `raw_data/navarro_2026/source_v1/code_v1.zip`.
The three inspected IL10 R files were extracted to `source_v1/author_code/`
without running author code. Exact file hashes and vector locators are retained
in the marker manifest. No missing external hallmark `.rda` was acquired.

For archival preflight, failed-v1 input files can likewise be restored from
`analysis/research/runs/nn26_failure_preservation_v1/failed_v1/` to
`raw_data/navarro_2026/failed_metadata_v1/`. Their original failed receipt must
remain `execution_failed`; only the preservation operation succeeded.

## Validation and scope

The unchanged repository validator passed all **seven new stage contracts**;
**six successful receipts** verify, while the original failed execution is
preserved as archive evidence. Thirty-five unique input identities were hashed,
eleven frozen code/config files checked, and runner/schema/library bytes compared
with the integration base. Existing registry entries remain logically unchanged.
All cloud-created scientific assets are bound to frozen code or registered
outputs. The four imported source JSONs are already governed by the desktop
source-stage receipt and must remain registered there.

The isolated sparse checkout intentionally lacks earlier animal assets and
unrelated repository paths. Full repository/integration validation belongs to
the parent after integration; it was not represented as passing here. Frozen
metadata and descriptive runs used the repository runner. No validator or
governance rule was weakened. Independent numerical checks and warning details
are in the report and immutable receipts. Four SVGs were rendered for inspection
outside the repository; previews are not additional numerical evidence.

Runtime was isolated under `/tmp/navarro_2026`: R 4.5.0, Matrix 1.7-3,
SeuratObject 5.0.2 and jsonlite 1.9.1. Full Seurat was absent. The RDS was read
only after the committed metadata freeze. No new biological object, optional
cohort, author contact, publication, policy/account modification or mounted
Weft edit occurred. The final export manifest reports bundle SHA-256, size,
prerequisite, HEAD and 32 KiB chunk count; transport chunks are emitted only
in later requested batches.

## Desktop import completed — 8 November 2026

The verified bundle and all eight cloud commits are imported into the parent
scoped branch. Transport used 287 pieces of at most 12,288 bytes, superseding
the original export manifest's proposed 32 KiB chunking. Full bundle size/hash,
nine successful receipt checks and exact Git-byte verification are recorded in
[local integration validation](VALIDATION.md). The large RDS/runtime remain
in the cloud; frozen outputs and reproducible code are now retained locally.
