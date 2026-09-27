# A0 reproduction and required inputs

Current result: the repair-first exploratory expression pilot is executed.
The authoritative status is [readiness.json](readiness.json), with interpretation
in the [expression report](reports/EXPLORATORY_PILOT_REPORT.md). Original-design
replication gaps remain separate in [feasibility_readiness.json](feasibility_readiness.json).

## Reproduce the exploratory analysis

The original configuration and gene programs are frozen. Reproduction must not
retune them using transfer outcomes. Use Python 3.12 and the repository's numerical
packages; versions and hashes are in [the execution record](exploratory_execution_record.json).
Downloads and processed matrices are ignored by Git. Start from the public inputs
in [expression_source_manifest.json](expression_source_manifest.json) and the
metadata cache in [source_manifest.json](source_manifest.json). Fetch a missing
expression file with `scripts/fetch_expression.py NAME URL --max-bytes LIMIT`
and the recorded Accept header when needed; the helper records and checks SHA-256.
`fetch_developmental_transfer.py` regenerates the documented read-only API queries.
Network access is required only when input caches are absent.

From the repository root in PowerShell:

```powershell
$a0Python = 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$a0Root = 'RQ_Specified/A0_conserved_epithelial_transition_program'
function Invoke-A0Stage($a0Script) {
  & $a0Python analysis/scripts/run_with_environment.py `
    --site-packages .venv-x64/Lib/site-packages "$a0Root/scripts/$a0Script"
  if ($LASTEXITCODE -ne 0) { throw "A0 failed at $a0Script" }
}
Invoke-A0Stage 'exploratory_repair.py'
# Review stage_E1_result.json against EXPLORATORY_PLAN.md before proceeding.
Invoke-A0Stage 'exploratory_specificity.py'
# Review stage_E2_result.json before proceeding.
Invoke-A0Stage 'fetch_developmental_transfer.py' # Reuses verified cached chunks.
Invoke-A0Stage 'exploratory_transfer.py'
# The recorded E3 review justified this explicitly post-transfer sensitivity:
Invoke-A0Stage 'exploratory_transfer_check.py'
Invoke-A0Stage 'plot_exploratory.py'
Invoke-A0Stage 'write_exploratory_report.py'
# Inspect changed figures before updating exploratory_figure_review.json hashes.
Invoke-A0Stage 'verify_exploratory.py'
```

`exploratory_freeze.py` documents how the existing configuration was created from
source feature identities and pre-existing control definitions. Keep the saved
configuration for reproduction. The query manifest links developmental downloads
to the pre-transfer primary-program hash. Every stage decision is recorded in
[stage_decisions.json](stage_decisions.json). Failures should stop the pipeline;
the commands above are the path actually warranted in this run, not permission to
ignore a failed gate in another dataset.

The transfer scorer validates all intestinal input counts while streaming the
matrix, retains only needed scoring features, and checks every developmental
API chunk's hash and feature indices. The final verifier reuses those ingestion
checks and hashes; it does not repeat a costly full expression scan. Sampling
draws, endpoint mixtures and cells are never counted as biological replicates.

## Reproduce the historical feasibility audit

Run from the repository root in PowerShell using the working x64 Python runtime.
The repository environment launcher supplies the numerical packages. These
commands reuse the source cache and do not access the network or score expression.

```powershell
$a0Python = 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$a0Root = 'RQ_Specified/A0_conserved_epithelial_transition_program'
$a0Scripts = @('audit_local_coverage.py', 'audit_public_metadata.py',
  'plot_p0_coverage.py', 'write_p0_report.py', 'audit_extended_coverage.py',
  'write_feasibility_report.py', 'verify_a0.py')
foreach ($a0Script in $a0Scripts) {
  & $a0Python analysis/scripts/run_with_environment.py `
    --site-packages .venv-x64/Lib/site-packages "$a0Root/scripts/$a0Script"
  if ($LASTEXITCODE -ne 0) { throw "A0 failed at $a0Script" }
}
```

The historical generator writes `feasibility_readiness.json` so it cannot reset
the current expression status. Its `validation.json` and `execution_record.json`
describe the metadata audit only; current records have the `exploratory_` prefix.

`audit_public_metadata.py` refreshes the GEO metadata inventory, including the
skin study. `write_feasibility_report.py` applies the current reviewed candidate
decisions. The initial P0 report remains historical. After changing a figure,
visually inspect it before updating the figure-review record.

Public cache files are excluded from Git. `source_manifest.json` contains their
URLs, sizes, retrieval modes, dates and SHA-256 hashes. To fetch a missing source,
use `scripts/fetch_source_metadata.py NAME URL --max-bytes LIMIT`, setting LIMIT
above its recorded size. Add `--gzip-first-line` only for the intestinal matrix
header and `--accept application/octet-stream` for `Negretti_obs.bin`. The header
hash covers the saved decompressed header, not the remote expression matrix.
Full PDF downloads are source documents, not expression data.

Metadata downloads require network access in a sandboxed session. Previously
observed failures: NCBI's main www host did not resolve; its public FTP host over
HTTPS worked. Some PMC and publisher pages were unavailable to automated tools;
author code, GEO, the author viewer and accessible primary-study copies were used.
Do not treat an inaccessible document as evidence that metadata do not exist.

## Required cohort metadata

Provide one row per cell, with these fields or an explicit mapping to them:

| Field | Requirement |
|---|---|
| `cell_id` | Unique and matches the count matrix exactly |
| `library_id` | Original capture/sequencing library |
| `biological_unit_id` | Verified mouse/donor or prespecified independent pool |
| `unit_type` | Individual animal, donor, or independent pool |
| `pool_members` | If pooled, membership and evidence of non-overlap across units |
| `technical_replicate_of` | Connects multiple libraries from the same unit |
| `time_or_age` | Sampling time with units and a defined biological stage |
| `condition`, `genotype`, `sort_strategy` | Establish comparable sampling and exclusions |
| `author_state` | Source label, preserving uncertain/unassigned labels |
| `state_role` | Source-supported starting, intermediate or destination state for one branch |
| `label_evidence_source` | Paper/table/code and independent temporal, fate or tissue evidence |
| `qc_or_doublet_status` | Source QC provenance; missing status must be explicit |

Do not fill missing animal identities with library IDs. Combine technical repeats
only when their shared biological origin is documented. A donor with two libraries
is one unit. Independent pools count as pools, not as the number of their members.

## Conditions for resuming P1

1. D2 and V1 each have ≥3 independently identified units with ≥30 cells in all
   three states. Same-day replication is not obligatory if the paired across-time
   estimand and limits are explicitly frozen.
2. State definitions and transition evidence are reviewed without examining the
   candidate program's enrichment. Early embryonic and postnatal branches stay distinct.
3. Matching raw counts, gene IDs, technical-replicate relationships and assay
   coverage are available. The developmental viewer's SCT export is not raw counts.
4. Freeze selected cohorts, exclusions, label-gene exclusions, scoring, effect
   criteria and source hashes before discovery. Record all prior exposure.
5. Run the original P2–P4 sequence only after these requirements pass.

Capture estimates in `tables/developmental_capture_planning.csv` are illustrative
sampling calculations. They neither satisfy these conditions nor estimate power
for detecting or transferring a gene program.
