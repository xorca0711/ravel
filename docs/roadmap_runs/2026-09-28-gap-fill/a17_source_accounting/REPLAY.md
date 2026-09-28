# Replay without changing the executed script

The executed [script](account_sources.py) deliberately writes only beside itself and refuses existing output names. The archived [report](REPORT.md) suggests changing its output confinement for a later replay; that is unnecessary. Copy the **unchanged script** to a new empty workspace directory, supply the original repository as `--reference-root`, and run it there. The direct source archive and reference files remain read-only. Absolute output paths and run times will differ; the count and parameter tables are the comparison targets.

Example from this repository root, using an unused ignored directory and the available runtime:

```powershell
$replayDir = Join-Path (Get-Location) '.tools/a17-source-replay'
if (Test-Path -LiteralPath $replayDir) { throw 'Choose a new empty replay directory' }
New-Item -ItemType Directory -Path $replayDir | Out-Null
Copy-Item -LiteralPath 'docs/roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/account_sources.py' -Destination $replayDir
& 'C:/Users/dream/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' analysis/scripts/run_with_environment.py --site-packages 'X:/GitHub/scRNA_seq/.venv-x64/Lib/site-packages' (Join-Path $replayDir 'account_sources.py') --reference-root (Get-Location).Path --archive 'X:/GitHub/scRNA_seq/raw_data/england_continuation_inputs/zenodo_v1.1.zip'
```

This recipe does not modify the script or replace the completed run. It is provided for future replay; the recorded execution and overwrite-refusal check are in [verification.json](verification.json).
