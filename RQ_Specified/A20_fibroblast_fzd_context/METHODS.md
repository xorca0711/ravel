# A20 methods and reproduction

## Scope and exposure

The [exploratory specification](config/exploratory_v1.json) was frozen at
2026-09-30 01:44:46 UTC after earlier Nb2 results and source narratives were known,
before new A20 marker/gene estimates were computed. It is exploratory, not a
preregistered confirmation. Original README, PLAN and question-contract bytes are
preserved in [history](reports/history/pre_execution/README.md.txt) as text snapshots.

## Counts, units and comparisons

The input is the existing author-annotated GSE262927 count object, whose full
SHA-256 and path are in [the run record](reports/analysis_complete.json). Source
preparation IDs, original subtype labels, day, doublet flag and experimental round
are retained. Receptor or outcome RNA never selects/relabels the subtypes.

Integer counts are summed by source sample and subtype. CPM uses the sum of all
genes in the actual counts layer, not stored QC totals. Values are log2(CPM+1).
The 21-gene set is fully mapped. Panels are equal-weight means of their fixed
genes on that scale. Support: Wnt2/Fgf7/Fgf10/Hgf; earlier ECM:
Cthrc1/Lrrc15/Col1a1/Col3a1; source collagen: Col1a1/Col1a2/Col3a1/Col5a1/Col5a2/
Col6a1/Col6a2/Col6a3. Panel magnitudes are not comparable measures of function.

Only matched AF1-minus-AF2 pairs at day42 are compared. The primary floor is 50
cells per subtype with predicted doublets removed. All combinations of floors
20/50/100 and doublet removal/retention are retained, including zero eligible
pairs. Other days contribute coverage tables only. We report every primary pair,
median, range and signs; no new inferential fit or cell-level test is used.

Independent reconciliation matched 1,000 shared rows to the earlier Nb2 extraction
for integer counts, cell counts, all-gene totals and CPM. A second script uses
standard-library arithmetic to verify transformations, panels, contrasts, summary
statistics and eligibility. Source checksums remained unchanged across extraction.

## Commands

Run from the repository root with Python and numpy/pandas/scipy/anndata/h5py/
matplotlib installed. The repository environment launcher can provide those
packages when needed. Downloaded papers and PDF review images stay in ignored cache.

```powershell
python RQ_Specified/A20_fibroblast_fzd_context/scripts/00_fetch_sources.py
python RQ_Specified/A20_fibroblast_fzd_context/scripts/01_analyze_context.py --data-root <source-repository-root>
python RQ_Specified/A20_fibroblast_fzd_context/scripts/02_figures.py
python RQ_Specified/A20_fibroblast_fzd_context/scripts/03_verify.py
```

The source count object is derived by the existing
[Niethamer pipeline](../../Research%20Article/gate1_01_niethamer_2025/README.md).
The analysis refuses to overwrite a completed run: preserve/version the package
before reproducing a fresh extraction. Verification can run against saved tables.
A19 files were snapshotted by hash before analysis and left byte-identical.
See [verification](reports/verification.json) and [figure export hashes](reports/figure_manifest.json).
