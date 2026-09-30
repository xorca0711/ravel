# A21 extension methods

## Scope and exposure

The owner authorized priorities 1-3 after the completed parent analysis. The
[extension contract](config/exploratory_v1.json) was frozen before new all-family
estimates, after exposure to parent results and Bian's narrative and figures.
This is exploratory, not a preregistered confirmation. The separate
[perfusion comparator](config/perfusion_comparator.json) was frozen after
workbook structure inspection but before numerical extraction. The
[source mapping](config/source_mapping.json) resolves columns, n and axis units.

## RNA analysis

Reuse the parent GSE211335 raw H5 files, deposited endothelial metadata and
12-animal barcode map. All files are hash-checked. Extract all ten Fzd genes,
Foxf1 and the 26 parent targets (36 unique genes). Symbols must map uniquely in
all three matrices before estimates proceed. No new clustering, filtering,
trajectory, cell-cycle regression or pooled association is fitted.

Aggregate all-gene raw totals and selected gene counts per animal/state across
technical pools. Report CPM, log2(CPM+1), raw counts and detected cells. Use
within-animal transitional1-minus-major0 and gCap-minus-aCap contrasts separately
by condition. Twenty cells/state is primary; 10 and 50 are fixed sensitivities.
Retain the parent denominator amendment and repeat its author-denominator
sensitivity without changing target numerators. Biological units are animals;
condition labels do not create longitudinal matching.

Report all values, means, medians, observed ranges and positive/negative counts.
There are no population intervals or new significance tests. For an alternative
Fzd to be an RNA nominee, a condition must have at least two pairs, a positive
mean, at least two-thirds positive pairs and at least five detected transitional
cells across eligible animals. At least two injury conditions must pass at both
20- and 10-cell floors. The 50-cell result is displayed separately. These are
transparent exploratory prioritization criteria, not biological effect margins
or evidence that a failing receptor cannot function. Independent validation
requires a compatible state contrast independent of the nominated genes.

## Published source workbooks

Read Figure 7D-G and the separate Figure 3F comparator directly from publisher
ZIP archives; no graph digitization. Record archive/member hashes and every
source cell. Import only specified data columns with Data-row labels, excluding
published comparison statistics. Confirm numbers of data values against source
legends. Report source-reported biological replicates; anonymous rows cannot
establish identity across panels. Do not join rows by ordinal position or count
nested images as additional animals.

Calculate unpaired group mean/median/range and the frozen raw mean differences.
Percentage outcomes use percentage-point differences; tumor volume uses mm^3.
The perfusion proxy is lectin-positive area divided by CD31-positive area.
Figure 7E has a source statistical-method discrepancy, so no P values or stars
are imported. Neither phenotype reconstruction nor equality to control is a
new inference. Figure selection is exploratory; all prespecified tables remain.

## Reproduction

Python requires numpy, pandas, scipy, h5py and matplotlib. PDF visual review uses
PyMuPDF. Run from the repository root with these dependencies:

    python RQ_Specified/A21_fzd4_capillary_function/scripts/00_fetch.py
    python RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/scripts/00_fetch_sources.py
    python RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/scripts/01_family_context.py
    python RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/scripts/02_source_analysis.py
    python RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/scripts/03_figures.py
    python RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/scripts/04_verify.py

Completed scientific runs refuse overwrite; preserve/version outputs before a
new run. The verifier operates on existing output. Cache payloads are ignored;
contracts, scripts, tables, hashes and figure exports are retained. The fetcher
restores immutable numerical source archives; dynamic HTML is an intake snapshot.
The independent verifier recalculates raw-matrix summaries and checks workbook
cells, source statistics, candidates and prior evidence preservation. Required
repository checks and rendered-PDF review accompany the final package.
