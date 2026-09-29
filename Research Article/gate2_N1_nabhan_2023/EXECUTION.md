# Nb2 execution and replay

Initial run: 29 September 2026, managed branch `codex/nabhan-2023-plan`, based on
fetched `origin/main` `17c0859`. The original checkout's unrelated local material
was preserved. Current results: [overview](RESULTS.md), [bulk](trials/bulk_v1/REPORT.md),
[atlas](trials/atlas_v1/REPORT.md). Namespace: **Nb2**.

## Verify existing evidence

From the repository root, with Python 3.12 and NumPy/Pandas installed:

```powershell
python "Research Article/gate2_N1_nabhan_2023/scripts/00_intake.py" --check
python "Research Article/gate2_N1_nabhan_2023/scripts/verify_plan.py"
python "Research Article/gate2_N1_nabhan_2023/scripts/07_verify_execution.py"
python analysis/scripts/validate_repository.py
```

The numerical verifier requires the small ignored bulk inputs and the recorded
local atlas input paths. It independently recomputes table arithmetic/BH values
and verifies code/contract provenance. It checks existing atlas file sizes; the
multi-GB raw hashes were calculated at freeze and are not repeatedly recomputed.
This is not raw-count re-execution or biological validation. The
[validation record](metadata/execution_validation.json) records the actual scope.

## Runtime used

Python 3.12.14 amd64, NumPy 2.4.6, Pandas 2.3.3, SciPy 1.18.0, h5py 3.16.0,
and the locally installed anndata/Matplotlib stack. The existing compatible
package directory was reused without rebuilding the environment:

```powershell
& 'C:\Users\dream\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  analysis/scripts/run_with_environment.py `
  --site-packages 'X:\GitHub\scRNA_seq\.venv-x64\Lib\site-packages' `
  'Research Article/gate2_N1_nabhan_2023/scripts/07_verify_execution.py'
```

R 4.6.1, limma 3.68.5, edgeR 4.10.5, jsonlite 2.0.0. Existing R libraries came
from `analysis/corrections/statistics/.tools/R-library` in the original checkout;
jsonlite was installed into the study's ignored `raw/Rlibrary`. Set `R_LIBS_USER`
to that directory when using the recorded portable R executable. The run's locale
warnings did not prevent numeric computation.

## Re-execute in a new version, preserving this evidence

The freeze/model scripts refuse to overwrite a frozen/completed run. For a new
analysis, copy the study scripts/config to a new run version and explicitly update
their output run IDs. Preserve `bulk_v1` and `atlas_v1`, including the schema-failure
record, rather than deleting completion markers to make them rerunnable.

1. `00_fetch_counts.py` restores the 18 GEO files and Ensembl GRCm38 release102
   annotation against the recorded hashes. `01_prepare_bulk.py` audits schema,
   aligns gene IDs and emits the ignored count matrix. Its gzip container hash
   is a run artifact; a fresh preparation may have a different gzip timestamp.
2. `02_freeze_bulk.py --gmt-root <existing-msigdb-directory>` freezes the new
   design after schema checks. Required gene sets are
   `mh.all.v2024.1.Mm.symbols.gmt` and `m5.go.bp.v2024.1.Mm.symbols.gmt`, with
   exact hashes in the contract. They were reused from local `raw_data/msigdb`.
3. `Rscript 03_bulk.R <study-absolute-path> <R-library-path> <GMT-directory>`
   fits the count adaptation and writes every contrast, source panel and enrichment
   result. Model inference is conditional on unresolved library independence.
4. `04_atlas.py --data-root <original-data-checkout>` freezes/streams the existing
   human matrix and mouse counts layer. Their exact paths/hashes are in
   [the atlas contract](trials/atlas_v1/contract.json). No integration or reclustering
   is run. The completed v1 needed `--resume-schema-fix` once; the saved amendment
   documents why. A fresh version uses the corrected code and requires no resume.
5. `06_atlas_synthesis.py` creates post-run descriptive receptor ordering and
   within-subtype association tables. `05_figures.py --section all` renders figures
   from saved results; neither script refits the bulk model.
6. Run the package/repository verifiers and inspect the figures. Record new input,
   code and output hashes, dates and any deviation before interpreting a new run.

Raw inputs, full reading notes, the supplied annotated PDF and transient runtimes
remain ignored or outside the repository. Compact evidence, figures, contracts,
scripts and reports are retained. The source culture map, timing discrepancies,
unresolved Crim2, original-atlas access and functional data gaps remain explicit;
additional computation alone cannot fill these missing measurements.
