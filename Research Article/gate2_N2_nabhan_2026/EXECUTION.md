# Execute and verify Nb3

The owner authorized reproduction and extensions on 1 October 2026 and assigned
the analysis ID **Nb3**. The folder remains `gate2_N2_nabhan_2026` (Gate 2N item 2,
roadmap paper 14). These are separate naming systems.

The [execution contract](config/Nb3_execution_v1.json) fixes numerical choices
before the new fits. The [panel amendment](config/Nb3_panel_amendment_v1.json)
adds the complete visually checked Fig. S7 panels before scoring. Existing
A10/A2 runs and their frozen specifications are preserved. Nb3 reconstructs
the article-wide assays and addresses the eight annotated questions; it does
not create a second copy of A10's predictive growth analysis.

## Inputs and runtime

- Full count workbook and Xenome statistics: download/check via
  [02_acquire_inputs.py](scripts/02_acquire_inputs.py). Their hashes match the
  previously recorded A10 inputs; the new location is ignored `raw_data/GSE307112/`.
- S1–S7: exact members of the existing supplement archive, checked by
  [01_inspect_supplements.py](scripts/01_inspect_supplements.py). No additional
  user upload is needed for these datasets.
- Imaging and library design: tracked P1 input and crosswalk paths in the
  frozen contract. Original counts, source PDFs, private annotations and full
  DE tables remain ignored. Compact derived tables and figures are retained.
- Python 3.12.14 with NumPy, pandas, SciPy, openpyxl and matplotlib; the local
  scientific packages are loaded through `analysis/scripts/run_with_environment.py`
  from `.venv-x64/Lib/site-packages`. The R session is recorded separately.
- Local R runtime and library: `analysis/corrections/statistics/.tools/`;
  edgeR 4.10.5 and limma 3.68.5. These are the installed versions, not a recreation
  of all original article package versions.

## Run order

Run from the repository root. Below, `python` means a compatible environment
containing the listed packages. On this Windows checkout the environment bridge
is used for scripts needing SciPy/matplotlib. Read each script's output policy
before rerunning: numerical run directories refuse overwrite.

```powershell
python "Research Article/gate2_N2_nabhan_2026/scripts/02_acquire_inputs.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/03_extract_full_counts.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/02b_target_identity.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/03b_species_assignment_qc.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/04_imaging_reproduction.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/05_run_expression.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/06_source_components.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/06b_source_budding.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/07_supplement_concordance.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/08_fixed_panel_extensions.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/09_context_metadata.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/10_figures.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/10b_refine_association_labels.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/12_audit_concordance_discrepancy.py"
python "Research Article/gate2_N2_nabhan_2026/scripts/11_verify_execution.py" --full-de-hashes
```

The first script's saved acquisition record is also immutable. To repeat an
analysis with changed choices, create a new versioned contract/output location;
do not delete or rewrite v1 results. Public metadata and source-component
extraction can run independently of DE. `07_supplement_concordance.py --prepare-only`
caches S4/S5 without fitting anything; its comparison step waits for R2 completion.
`08_fixed_panel_extensions.py` requires completed R1, both R2 normalized-panel
branches and source-component records. It hashes its exact completed inputs and
may run while the independent whole-transcriptome DE loop finishes; the final
review and verification require the complete DE record and source concordance.
`11_verify_execution.py` is read-only unless given a new `--out` path.

## Recorded interpretations

| Output | Meaning |
|---|---|
| R1 effects, intervals and BH diagnostics | Declared source-informed imaging reconstruction; intervals describe technical wells |
| R2 gene DE and source concordance | Full-count limma-voom reconstruction; concordance is conditional on the source-selected S4/S5 genes |
| R3 source component activities/projections | Deposited S6/S7 component values with source signs, not newly fitted cPCA/JADE coordinates |
| R4 marker-panel contrasts | Mean log2(TMM CPM + 0.5) across fixed source marker panels; not full pathways, cell fractions or exact source heatmap groups |
| E1–E8 tables | Descriptive target contrasts, shared E1/E8 analysis, growth/depth and leave-target-out diagnostics; mechanistic and external-validation limits retained |
| R5 metadata | Eligibility evidence and named holds; no spatial genotype test or new external single-cell fit |

Source uncertainty is explicit: imaging scaling/day handling, full-species
versus within-comparison TMM, filtering/BH order and source software choices
are not fully specified. A close numerical match does not recover those missing
implementation details or establish independent biological replication.

The completed source comparison found a material human S5 mismatch. Script 12
is the post-hoc source-consistency/extraction audit prompted by that result; it
does not relabel source data or refit any endpoint. Human numeric reproduction
remains failed even when computation and file-integrity checks pass.

The repository's `.gitattributes` preserves this package's recorded bytes across
Windows/Linux checkouts, including text line endings used by the run hashes.

For current results, read the [reproduction review](reports/REPRODUCTION_REVIEW.md),
[extension review](reports/EXTENSION_REVIEW.md) and
[context eligibility audit](reports/CONTEXT_ELIGIBILITY.md).
The original [intake](reports/INTAKE.md) is a historical snapshot taken before
count recovery and execution; its old missing-cache flags are not current status.

## Publication figures and pre-RQ follow-up, 1 October 2026

The [additional-analysis proposal](reports/PRE_RQ_ANALYSIS_PLAN.md) and frozen
`config/Nb3_followup_v1.json` precede the new fits. The follow-up reuses v1
normalization and DE outputs; it does not rerun 395 whole-transcriptome models.

```powershell
python analysis/scripts/run_with_environment.py --site-packages .venv-x64/Lib/site-packages "Research Article/gate2_N2_nabhan_2026/scripts/13_publication_figures.py"
python analysis/scripts/run_with_environment.py --site-packages .venv-x64/Lib/site-packages "Research Article/gate2_N2_nabhan_2026/scripts/14_followup_analysis.py"
python analysis/scripts/run_with_environment.py --site-packages .venv-x64/Lib/site-packages "Research Article/gate2_N2_nabhan_2026/scripts/15_followup_figures.py"
python analysis/scripts/run_with_environment.py --site-packages .venv-x64/Lib/site-packages "Research Article/gate2_N2_nabhan_2026/scripts/16_verify_followup_package.py"
python analysis/scripts/run_with_environment.py --site-packages .venv-x64/Lib/site-packages "Research Article/gate2_N2_nabhan_2026/scripts/17_S03_layout_revision.py"
```

These are provenance/reproduction entrypoints, not commands to replay over
existing results: output directories and verification records refuse overwrite.
For drafts, plotting scripts 13/15 accept `--output` with a fresh temporary
folder. Script 14 invokes the portable R runtime for `14b_hallmark_context.R`;
limma 3.68.5 and species-appropriate cached MSigDB Hallmark 2024.1 files are
recorded. No packages or gene-set versions were silently updated.

The final [11-figure atlas](figures/Nb3_complete_figure_atlas_v2.pdf) retains
300-dpi PNG and editable SVG/PDF counterparts in article-local versioned
folders. Script 17 shortens one clipped title without changing data; original
exports and the first atlas remain preserved. See the
[layout receipt](figures/publication_v1/S03_layout_v2/layout_revision.json).

The [verification](reports/Nb3_followup_verification.json) checks 223 provenance,
arithmetic, coverage, global-BH and export properties; it does not turn the
human source mismatch into successful reproduction. Read
[follow-up findings](reports/FOLLOWUP_RESULTS.md) and [RQ derivation](reports/RQ_DERIVATION.md)
before continuing into A22/A23.

## External E5 pilot and later RQ review, 1 October 2026

Scripts `18_e5_external_intake.py` and `19_e5_external_pilot.py` acquire the
public GSE306184 metadata/count workbooks and execute the separate frozen
`config/Nb3_E5_external_v1.json` contract. Both refuse to overwrite their run
directories. The intake needs NCBI network access; analysis uses the bundled
Python runtime with numpy, pandas and openpyxl. Script 20 renders the original
external figure; script 21 preserves it and widens the left margin in v2.
Use the environment wrapper above for matplotlib, which is absent from the
bundled Python but available in the recorded repository scientific environment.

[External results and metadata conflicts](reports/E5_EXTERNAL_FEASIBILITY.md)
limit this run to descriptive library contrasts. Neither replicate suffixes
nor the generic epithelial annotation establishes independent AT2 donors.
The [RQ integration review](reports/RQ_INTEGRATION_REVIEW.md) adds conditional
branches to existing questions without changing earlier results or the atlas.
