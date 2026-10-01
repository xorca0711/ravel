# Reproduce the A23 external pilot

Use Python 3.12 with the versions in the [environment file](../../config/external_requirements.txt).
Create an isolated environment; raw data stay under ignored `raw_data/GSE199329`.
Run from the repository root:

```bash
python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/01_acquire_external.py
python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/02_external_pilot.py --check
python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/04_verify_external.py --with-raw
```

Acquisition reuses matching cached files and checks the recorded source hashes.
The archive is 146,329,600 bytes; the workbook is 12,350,306 bytes. Three filtered
HDF5 matrices are extracted from nested per-library archives. No FASTQs are used.
The NCBI homology responses, parsed metadata and exact selected map are tracked.
Their URLs and retrieval times are recorded; failed Ensembl calls remain visible.

To recompute, use a separate checkout and fresh versioned output paths before
running `02_external_pilot.py` without `--check`. It refuses to overwrite saved
outputs. `03_figures.py` renders all current figures into a fresh figure folder.
The first F3 layout is retained for history; use F3_sensitivity_v2 for display.
Read `external_pilot_v1.json`, the failed-attempt note and `external_pilot_v2.json`
together for the feature-availability amendment. No outcome was used to select
that amendment. The biochemical contract explicitly records prior value exposure.

Tracked-only verification needs Python's standard library:

```bash
python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/02_external_pilot.py --check --tracked-only
python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/04_verify_external.py
```

These checks verify provenance and arithmetic; they do not validate cell typing,
transport mechanisms or causal inference.

## Complete published-cell sensitivity

`05_published_cell_audit.py` reconstructs the complete published cell set from the
raw HDF5 matrices in the same archive. It extracts exact recorded members if
missing, verifies their hashes, and refuses to overwrite its saved outputs.
`06_published_cell_figure.py` renders the supplementary figure. These scripts
also require fresh, versioned output paths for recomputation. The source-cell
contract explicitly records exposure to the prior pilot outcomes. The standard-
library verifier checks both batches and figures; `--with-raw` also checks raw
source hashes and the original pilot's independent coordinate/count calculations.
