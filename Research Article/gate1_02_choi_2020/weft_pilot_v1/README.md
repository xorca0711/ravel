# P001 Choi Figure 1B-D: checkpointed manual pilot

Owner A0, with A1 context. Base Ravel bfe26b876221cf6c6fa6f9b16a90cfb516b5998d;
input inventory from Weft d031cef02ab4a417760bca46e90a63917d215d31.
The metadata-only run executed once and its exact outputs passed independent root
readback and unchanged receipt verification. [Current metadata review](METADATA_STATUS.md)
records scope, resource observations and the resolved export hold. No new question
or biological interpretation is claimed.
The metadata contract is **frozen** after [runtime review](RUNTIME_REVIEW.md);
the descriptive contract is **frozen** after root review. Dispatch remains held
pending final packet review and a new verified before-dispatch checkpoint.
Multipart transport qualified at 4 MiB; root has accepted sparse-loader
memory readiness only; full-workload memory remains to be measured.
The exact manual checkpoint and committed source must be bound before dispatch.

## Current execution readiness

The owner-selected 8 GiB analysis cap and 12 GiB host floor passed the memory
check. Pro provides a documented 16 GiB VM; root's earlier 20 GiB host requirement
was a planning error. Frozen scientific files remain unchanged. All 56 code
bindings, three frozen-file hashes and nine retained inputs matched.

After repairing ignored mount placeholders, Docker VFS container allocations
caused a disk hold. The owner approved retirement of the two audited containers;
about 4.2 GiB was recovered, preserving source, inputs, image and all evidence.
The existing second container passed offline preflight once before retirement:
ok=true, exit 0, no OOM, 0.616 seconds. Exact process identities were not captured
in that short run; its terminal Docker evidence is retained without claiming
exact disappearance proof. Numerical-job process evidence remains required.

[Current preparation evidence](https://github.com/xorca0711/weft/blob/codex/cloud-job-controls-20261011/records/choi-figure1-resumed-preparation-20261011.json)
records failures, explicit cleanup approval, cgroup-v2 field review and root-verified
held-checkpoint ancestry. Figure1 has not started. Final packet review, actual
numerical-container controls/capacity and a verified before-checkpoint precede release.

## Stages and inputs

[Metadata contract](config/metadata.contract.json) precedes the separate
[descriptive contract](config/figure1.contract.json). [Input manifest](config/inputs.json)
binds exactly nine compressed Tomato-positive triplets for PBS, day 14 and day 28.
Fresh inputs belong in ignored `raw_data/GSE145031/weft_pilot_v1/inputs/`.
The existing archive has a recorded local digest, while the provider publishes no
content digest; the accepted Weft member hashes are the integrity authority for this
pilot. The metadata worker has now verified the archive and selected inputs; see current
status above for independent result readback and review.

The loader fully reads gzip streams (CRC), rechecks compressed hashes, validates
MatrixMarket integer/general dimensions, line counts, coordinate bounds and positive
integers, and rejects duplicate coordinates **before** sparse CSR construction.
Feature IDs and barcodes must be unique, lengths match axes, and exact uncompressed
feature/barcode hashes bind their order. Both stages explicitly require identical
feature ID/order across libraries, independently of those per-file hashes. Duplicate gene symbols use frozen D1 ID/index
handling. Cells use GSM-prefixed barcode IDs. Raw whitelists are never densified or
silently summed. One raw library is loaded/validated/QC-filtered and released before
the next; only QC-retained cells are combined. Metadata separately measures each
library's loader time and the cumulative process peak RSS after each load.
The preserved metadata receipt and raw readiness output are registered in Ravel;
root verified their original bytes. Private runtime locators remain outside Git.

## Fixed methods and exposure

[Source bindings](config/source-bindings.json) records exact pinned legacy source and
function-segment hashes. [Frozen methods](scripts/frozen_methods.py) contains inert
AST source extracts, not historical-module imports. D1 `call_and_qc`, MAD bounds,
shared `qc_metrics`, D2 `embed` and corrected `annotate_clusters_b` are frozen.
The D1 expected rate is 0.008 times post-QC cells / 1000; its historical undefined
threshold quantile fallback is retained and explicitly logged. Exceptions do not
trigger a new fallback. Missing or unusable cells stop the job.

Normalization target 10,000, log1p, seurat_v3 HVGs (2,000 on counts), HVG-only scaling
max10, PCA30, neighbors30, igraph Leiden n_iterations2 and seed0 follow D2.
Scaling densifies the retained HVG embedding only; full-data peak memory still needs
qualification. Analyst-fixed/predeclared primary resolution **1.0** differs explicitly from historical
outcome-dependent primary selection. Sensitivities 0.3/0.5/1.0 are all reported.
D2b DATP subclustering at 0.5 occurs only if pAT2 is absent and DATP present; states
other than pAT2/DATP inside this subcluster remain DATP, as in D2b. No thresholds,
markers or resolutions are tuned to recover five states. Conditional subcluster
output is additional when triggered and must be retained, including failures.

The historical benchmark is exposed: D2b recovered hAT2/cAT2/DATP/AT1, with pAT2
unassigned. This new adapter does not override that result or imply independent
replication. There is one pooled two-mouse library per condition, with no animal
identities available for independent inference. No animal-level p-values or new
mechanism claim. A0's failed cross-tissue transfer and A1's regulatory/fate evidence
limits remain unchanged. Here the validity threat is selection/annotation bias.

## Denominators and discrepancies

Record whitelist, paper-rule and sensitivity-floor counts, floor-only and paper-only
barcodes, each MAD bound and its removals, post-QC cells, doublet scores/threshold/
fallback, flagged doublets and retained cells per library. Report corrected cluster
tables for every resolution, final assigned/unassigned/contaminant counts,
per-marker detection with missing marker availability, state composition and pAT2
absence. The alveolar denominator excludes contaminants and **includes unassigned**;
also report fractions of all post-doublet cells and exact counts. Count partitions
and fraction arithmetic are software invariants, not biological success tolerances.
Fresh numerical differences are described, never thresholded into reproduction success.

The paper used Cell Ranger 2.0.2 cell calling, Scanpy 1.3.6/Louvain, manual contaminant
removal, Scrublet rate0.1/neighbors30 and score0.7/cluster-mean0.6. The repository
applies paper cell filters directly to the raw whitelist, per-library MAD filtering,
Scanpy Scrublet's expected rate/automatic threshold (logged fallback), Leiden and
corrected marker-based contaminant annotation. [Runtime route](runtime/dependency-route.json)
substantiates the official Scanpy internal Scrublet route; standalone scrublet/annoy
are unused. scikit-misc supports seurat_v3; scikit-image supports automatic thresholding.
No method-equivalence claim is made.

## Review and manual checkpoints

Review code, targeted synthetic tests, [watchdog proof](config/watchdog-qualification.json)
and all input/memory readiness before freezing/committing either contract.
Then use the unchanged research gate with exact inputs. Each stage additionally
requires a root-reviewed cooperative job record at
`raw_data/GSE145031/weft_pilot_v1/checkpoints/<stage>-job-v1.json`, with `stage`,
`approved`, unique `job_id`, exact `contract_sha256` and `before_backup_verified`.
The descriptive job also needs `metadata_loader_memory_pass`. These fields do not
cryptographically establish human approval: root supplies and reviews the actual
receipt. Never fabricate it. The coordinator owns one manual job at a time; private
Drive checkpoints before/after each job preserve exact contract/code/input/output
hashes, terminal status, interruption and recovery decisions. Restore and reconcile
an interrupted attempt explicitly before another attempt; never blindly rerun or
overwrite outputs. Private Drive locators and task/process identities remain outside
these public scientific materials.

Use new runner run IDs `p001_metadata_v1_<attempt>` and `p001_figure1_v1_<attempt>`;
all outputs go under the fresh runner `{run_dir}`. The cooperative adapter refuses
a draft or missing checkpoint. The unchanged runner requires frozen committed code
and inputs. Neither cooperative check is a service, lease implementation or OS sandbox.
Actual worker invocation must additionally bind the exact numeric image, resource
limits, read-only repository/input mounts and worker GNU timeout with kill-after.
Only the allocated fresh output directory may be writable. A host-only timeout is
insufficient. [Worker case](runtime/watchdog_case.py) is synthetic and has no biology.

## Rebuild and validation

[Current exact lock](runtime_git_v3/locks/requirements.lock), [wheel provenance](runtime_git_v3/provenance/wheels.json),
[recipe](runtime_git_v3/recipe/Dockerfile), [synthetic fixture](runtime_git_v3/recipe/synthetic.py) and
[image identity](runtime_git_v3/reports/summary.json) bind the qualified Linux amd64 Python3.12.15
stack including Git. The build context also needs the 31 verified Debian packages,
SHA256SUMS and package lock as named in the recipe; see the runtime archive README.
Package/wheel binaries are excluded from Git. Download only locked binary wheels from PyPI with `--require-hashes`, TLS
verification and managed proxy/CA trust into `runtime/wheels/`; no wheel binaries
are committed. Build the recipe with `--platform=linux/amd64 --network=none` after
wheel retrieval. Runtime synthetic compatibility does not qualify full-data memory,
scientific results or author-method equivalence.

Run `scripts/test_synthetic.py` in that image with no network and bounded CPU/RAM;
these tests use only newly generated tiny fixtures. Contract preflight without
`--inputs` verifies source/schema only; with `--inputs` must hold until the real
triplets are independently available and checked. Full repository checks need a
complete tracked source checkout; no historical analysis is replayed.

The earlier provider HEAD failure is preserved. The approved NCBI-only update
is published; the fresh cloud check returned HTTP 200 and the expected
349,204,480-byte archive length. Source bytes still require verification on download.
Retention guarantees and literal desktop-power-off testing remain separate from
 demonstrated private Drive recovery.

## Review corrections to d779520

The resolution-to-state dictionary is retained separately from per-library assigned
counts. `qc_cell_counts.png` is a diagnostic. `figure1B_state_umap.png` is an
adapted descriptive state embedding showing every observed category, including
unassigned and contaminants; `qc_library_timepoint_umap.png` exposes mixing.
Figure 1C composition and Figure 1D marker detection are adapted descriptive panels.
The detection-fraction panel is not the published expression heatmap. Primary 1.0
is analyst-fixed/predeclared, not personally selected by the owner. No tuning occurred.

The bounded synthetic describe integration reaches real frozen annotation,
denominators, marker tables, all plots and JSON serialization with absent pAT2,
unassigned and an immune contaminant. Coordinates/connectivities are synthetic;
only conditional DATP neighbors/Leiden are mocked, with exact arguments checked.
It does not validate graph construction, biological embeddings or scientific results.
Thirteen targeted tests passed in 1.504 seconds. Synthetic output hashes are recorded
in source bindings separately from biological outputs, which do not yet exist.

The scoped `.gitattributes` rule preserves exact pilot bytes on Windows/Linux.
Legacy modules are never imported: source bindings preserve their pinned Git
blob identities and extraction hashes as provenance, while contracts bind the
actual inert adapter and runtime materials. Committed-source checks remain required.

**Resolved runtime hold:** the original image lacked Git. The reviewed Git-equipped
revision and exact transfer evidence are in [RUNTIME_REVIEW.md](RUNTIME_REVIEW.md).
The unchanged runner committed-source checks remain mandatory.

The [artifact recovery amendment](ARTIFACT_TRANSFER_AMENDMENT.md) records the
failed 16 MiB trial and successful 4 MiB alternative. It changes only external
artifact transfer; the frozen scientific source and contract remain unchanged.
