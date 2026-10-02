# Nb4: execution and verification

**Completed 2 October 2026:** source intake, metadata gates, bounded expression
reproduction, internal sensitivities, external pilot, genome-wide visual
analyses and research-question derivation. The [gallery](FIGURES.md) owns the
figures. Historical TN2020 schemas identify early Nb4 runs; their bytes are
preserved. This is partial source reproduction, not a complete paper refit.

## Recorded stages

| Stage | Script | Immutable evidence |
|---|---|---|
| Supplements and library design | 00_source_intake.py | [intake_v1](runs/intake_v1/run_record.json) |
| Metadata/biological units | 03_prepare_metadata.py, using 01_metadata_gate.py | [metadata_v1](runs/metadata_v1/run_record.json) |
| Counts, source panels, matched donor effects | 04_expression_reproduction.py | [reproduction_v1](runs/reproduction_v1/run_record.json) |
| Source table and imaging denominator checks | 05_source_concordance.py | [source_concordance_v1](runs/source_concordance_v1/run_record.json) |
| Floors, donors, assays, comparators and depth | 06_followup_analysis.py | [followup_v1](runs/followup_v1/run_record.json) |
| Independent fibroblast pilot | 08_external_pilot.py | [external_pilot_v1](runs/external_pilot_v1/run_record.json) |
| New UMAP, donor PCA, GSEA and GO | 11_extended_analysis.py | [extended_visual_v1](runs/extended_visual_v1/run_record.json) |
| Base/extended figures and readability refinements | 09, 12 and 14 scripts | [figure gallery](FIGURES.md) |
| Captions and combined PDF atlas | 13_build_gallery.py | [gallery_v2](figures/gallery_v2/run_record.json) |
| Independent arithmetic, hash and link checks | 10_validate_execution.py | [validation](runs/validation_v1/checks.json) |

Frozen specifications record when source results had already been seen.
Follow-ups are exploratory; the external cohort is not independent of all
annotation knowledge. No gene-set p-value is presented as donor-population
significance. Failed biological gates remain documented in the reports.

## Environment and commands

The repository .venv-x64 launcher points to a missing base Python in this
session. The bundled Python 3.12.14 runtime was combined with the existing
scientific site-packages through the repository launcher. No installation or
environment mutation was needed. Software versions for the extended fit are
in its run record. Imports include numpy, pandas, scipy, h5py, anndata,
scikit-learn, umap-learn, gseapy, statsmodels, matplotlib, openpyxl and pypdf.

```powershell
$Python = 'C:\Users\dream\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$Package = 'Research Article\gate2_N3_travaglini_nabhan_lung_atlas_2020'
& $Python "$Package\scripts\verify_archive.py"
& $Python "$Package\scripts\verify_package.py" --with-sources
& $Python -m unittest discover -s "$Package\scripts" -p 'test_*.py' -q
# Pattern used to execute scientific scripts:
& $Python analysis\scripts\run_with_environment.py `
  --site-packages '.venv-x64\Lib\site-packages' `
  "$Package\scripts\10_validate_execution.py"
```

The validator creates a fresh immutable validation directory and refuses to
overwrite an existing run, like the analysis scripts. Read the delivered
validation record for this execution. `verify_archive.py` is the repeatable,
read-only verifier for all deposited run outputs, archived code, configurations
and links; it requires only standard Python and runs in CI. `verify_package.py`
checks intake evidence and can additionally verify locally available sources. For a new numerical execution, choose new run/output
versions and update downstream references in a new specification/code version;
the delivered scripts intentionally pin their recorded output paths. Do not
delete old evidence simply to reuse a command. The original intake also accepts
an explicit fresh `--outdir`.

## Input recovery and access

`fetch_sources.py` reports missing small public computational inputs without
network access; `--download` restores the twelve workbooks and six library
metadata files with hash verification. Optional private context is not required
for computational replay. `02_acquire_expression.py` and
`07_acquire_external.py` document the selected public matrix acquisitions;
existing payloads and manifests are not overwritten. The public CELLxGENE
versions were used after anonymous Synapse downloads returned 403. Controlled
EGA reads were not accessed. Existing MSigDB 2024.1.Hs GMTs must be supplied
under their recorded hashes; source files remain ignored.

## Verification scope

The package input-gate tests and repository analysis unit tests passed during
this task (nine package tests; 53 repository tests with one skipped).
Independent checks cover source hashes, recorded outputs/code/config snapshots,
direct raw-count/pseudobulk spot checks, hypergeometric detection against SciPy,
external donor matching, genome-wide focal-effect agreement, GO/BH arithmetic,
GSEA score/tie diagnostics, UMAP coordinates, gallery links and PDF page count.
Figure renders were visually inspected, with crowded labels refined separately
without altering numerical fits.

The publication branch was prepared from current main (`ceb6ffc`), preserving
unrelated work in the original checkout. All required repository checks passed:
79 repository tests (one skipped), nine Nb4 input tests, 6,612 repository
validation checks, compilation, the claim contract and existing evidence
verifiers. The portable Nb4 archive verifier checks 14 run records and 119
output hashes. See the [publication checks](reports/PUBLICATION_CHECKS.md).

The earlier 25 failures belonged to the original, stale checkout; they are not
failures on this publication branch. No numerical fit or historical run record
was changed while reconciling with current main. No claim-grade promotion or
Notion write was performed. See the [verification report](reports/VERIFICATION.md).
