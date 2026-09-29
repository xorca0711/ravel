# Execution and reproducibility

Run: `extension_v1`, 29 September 2026. The complete branch-analysis bundle now
lives under `Research Article/gate2_N1_nabhan_2023/branch_analysis/`. The owner
corrected its premature placement under `RQ_Specified`; derived RQ registration
is a later synthesis step. Tables, figures, contracts and original run records
were moved without changing their bytes or rerunning scientific analyses.

[Relocation metadata](metadata/relocation.json) preserves the original paths,
artifact hashes and pre-relocation scripts. The three live script changes only
resolve the new location and retain access to historical provenance. Frozen
contracts and run manifests intentionally retain their original paths. The
numerical verifier resolves the documented alias and writes a new verification
file on future execution, preserving the earlier successful record.

[Relocation verification](metadata/relocation_validation.json) checks preserved
artifact hashes, runnable path resolution and candidate/index placement without
repeating biological analyses. [07_verify_relocation.py](scripts/07_verify_relocation.py)
implements that structural check.

## Executed sequence

| Stage | Implementation | Output |
|---|---|---|
| Freeze inputs, exposure and rules | [00_freeze.py](scripts/00_freeze.py) | [contract.json](trials/extension_v1/contract.json),11 input hashes |
| Contextual perturbation reanalysis | [01_gaona.R](scripts/01_gaona.R) | [Gaona completion](trials/extension_v1/gaona_complete.json),14 libraries,16,005 genes |
| Derive reference and source score/influence analysis | [02_bulk_extensions.py](scripts/02_bulk_extensions.py) | [signature freeze](trials/extension_v1/signature_freeze.json),182 program contrasts |
| Mouse subtype/state context | [03_mouse_context.py](scripts/03_mouse_context.py) | [mouse completion](trials/extension_v1/mouse_complete.json),183/189 requested genes mapped |
| Figures | [04_figures.py](scripts/04_figures.py) | Five PNG/SVG pairs, visually reviewed |
| Targeted round/depth rival audit | [05_targeted_audit.py](scripts/05_targeted_audit.py) | [post hoc contract](trials/extension_v1/targeted_audit_contract.json) and36 comparisons |
| Numerical/provenance verification | [06_verify.py](scripts/06_verify.py) | [verification.json](trials/extension_v1/verification.json) |

Reference full counts are in the original paper's ignored `raw/` folder; public
download URL and hash are recorded in the contract. No private PDF, full Notion
notes or single-cell object was added to tracked artifacts. No Notion page was
edited. Completed stages refuse to overwrite their own run; use a new version
and exposure record for changes to an analysis contract.

## Preserved failure and amendment

The first mouse run stopped before aggregation because stored `total_counts`
did not equal the counts-layer sum. The
[failed script](trials/extension_v1/failed_attempt/03_mouse_context.py) and
[schema amendment](trials/extension_v1/schema_amendment.json) preserve the event.
Of162,175 cells,4,909 have a difference:5,532 total UMIs, maximum28 per cell,
maximum relative difference0.554%. Stored QC totals may cover a different gene
universe; that exact cause was not established from metadata alone.

The resumed run retains the originally specified **actual count-layer denominator**,
quantifies the discrepancy and verifies57,380 shared unit/gene rows against the
independent earlier Nb2 extraction. Counts, cells and denominators match exactly.
This is a schema-check amendment, not changed endpoints or an outcome-based
sample exclusion. [Depth audit](trials/extension_v1/depth_audit.json).

The later Fzd4 round check was prompted by an observed association and is explicitly
post hoc. It weakened the interpretation. No analysis was rerun to select a
favorable p-value, cell floor or library subset.

## Runtime and replay

Python3.12.14 amd64 uses the existing compatible numerical packages through
`analysis/scripts/run_with_environment.py`. R4.6.1 uses limma3.68.5 and edgeR4.10.5;
Gaona is a voom adaptation of a source DESeq2 analysis. Startup locale warnings
did not affect execution. Local runtime roots are recorded here for this checkout;
they are environment paths, not tracked dependencies.

Example verification from the repository root in PowerShell:

```powershell
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' `
  'analysis/scripts/run_with_environment.py' `
  --site-packages 'X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages' `
  'Research Article/gate2_N1_nabhan_2023/branch_analysis/scripts/06_verify.py'
```

For a new analysis version, stages00/02/03 accept `--data-root X:/GitHub/scRNA_seq`;
stage01 takes the workspace path and existing R-library path. Set `R_LIBS_USER`
to Nb2's ignored `raw/Rlibrary` to locate jsonlite. Runtime launch details and
output/script hashes are preserved in [run.json](trials/extension_v1/run.json).

Checks validate source units, mappings, arithmetic and reproducibility within the
declared scope. They do not establish experimental exchangeability, later fate,
clinical benefit or mechanism. A source-reported mouse count is not a recovered
cross-medium mouse identity map; a passed consistency check does not repair that gap.
