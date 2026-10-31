# Yadav second checkpoint: prospective execution decisions

30 October 2026. Technical source checkpoint d1d3677 was reviewed and approved
for these bounded jobs. Human scientific acceptance remains unassessed.
The source [qualification](SOURCE_QUALIFICATION.md) remains authoritative for
units, missingness, label reconciliation and source limitations.

## Functional source reconstruction

Five separate contracts (F1-F5) bind the shared runner and a per-job JSON
specification with every panel, source cell, condition, donor grouping, unit and
ordered contrast. These values and published outcomes were previously exposed.
No significance filtering or outcome-dependent endpoint selection is permitted.

- F1: 3B human PCLS, 3D, 5A. Show supplied slices and arithmetic mean differences
  in published normalization. No patient means, standard errors or confidence
  intervals without the slice/patient map.
- F2: 5D-F, plus 6G as a separate endpoint. Describe each of two donor
  combinations with technical/culture points and condition means. Differences
  compare group means, never inferred pairs of wells. Keep 5D D2 blank.
  Shared 5D-F cultures do not constitute replication; 6G donor overlap is unknown.
- F3: 3B mouse and 3E. Mean differences and two-sided 95% Welch t intervals,
  conditional on independent reported source animals. These are sampling-model
  intervals, not recovered allocation or batch information. No p-values,
  pairing, meaningful-effect threshold, source mediation or causal certification.
  Fig. 3E's combined control genotypes remain disclosed.
- F4: S3C-D and 3J. Retain all conditions and fixed coculture, inhibition,
  rescue and genotype contrasts. Source-culture means/differences only.
  Alpha-SMA remains separate from collagen; nonsignificance is not equivalence.
- F5: 3K proline and hydroxyproline relative abundance. Show supplied normalized
  values and differences. No de-normalization, isotope incorporation or flux.

For all jobs, preserve real zeros and blank cells. The frozen source-cell inventory
is a derived view of the official workbook, not a second biological source.
Plot points and means without arbitrary well-level lines or inferred unit labels.
Record numerical-library versions and independently verify arithmetic against the
original workbook using a different reader.

## RNA sequence after functional reconstruction

First execute a separate full count-entry integrity contract for all six libraries:
complete decompression/parse, dimensions, actual versus declared entry counts,
integer/nonnegative values, index bounds, duplicate coordinates, feature/barcode
joins and per-library QC summaries. This is not transcript-effect estimation.

Then freeze a justified annotation/QC strategy after inspecting technical QC,
with outcome exposure recorded. Conservatively retain mixed/ambiguous/unassigned
cells and distinguish an adapted marker approach from the author's SingleR method.
Arg1 and Il6 must not be annotation features. Report composition separately from
within-class expression. No preparation-population DE, suffix pairing, Compass
or CellChat is in scope. Spatial/context qualification and final Wg-P06/thesis
synthesis remain pending review.
