# A30 saved-state measurement qualification: barcode join held

3 November 2026. [Contract](../../../analysis/cut_fill_20261103/a30_join_v1.json),
[receipt](../../../analysis/research/runs/cut_fill_a30_join_v1_20261103/receipt.json),
[qualification](../../../analysis/research/runs/cut_fill_a30_join_v1_20261103/qualification.json),
[join cardinalities](../../../analysis/research/runs/cut_fill_a30_join_v1_20261103/join_cardinality.csv).
Freeze: `bad95f6`. The completed denominator, barcode export and common-support
calculations were reused; no old activation analysis or size-only null was rerun.

Both saved tables have 35,928 cells, but their only shared fields are donor and
tissue. The barcode export has unique `(gsm, barcode)` keys; the state table has
neither key. Twenty-one matching donor/compartment groups are many-to-many; all
22 state-table groups contain multiple states. Equal totals do not associate
one original barcode with one saved state. No row-order or expression-similarity
join was made.

There is also a documented source naming discrepancy. The saved state table uses
PTC45044_CSF and the barcode export uses PST45044_CSF. Inspection of the exact
hash-matched source SOFT record shows that
[GSM4104132](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM4104132)
has title/description PTC45044_CSF, while its deposited filenames use PST45044_CSF.
That primary record explains the naming origin; it does not provide cell-state
membership. This unpaired CSF sample is not an additional paired donor, and no
saved identifier was silently rewritten.

**Disposition:** the traceability gate fails for the requested saved-state
lineage/doublet assessment and matched specificity null. A provenance-keyed
membership export or independently validated reconstruction with original inputs
and runtime is required. A new clustering solution would be a new amendment, not
a repaired join. This result does not falsify the existing RNA associations.

The remaining operational non-CD8 T-lineage gate is not positive CD4 protein
identity and had no dedicated doublet detector. Those limitations remain;
additional thresholds are not invented to bypass the join. No full-background
expression/detection-matched null, Monte Carlo p-value or new donor interval was
computed. All-cell and restricted-population estimates remain separate in the
[existing report](../../portfolio_extensions/2026-10-07/g3_immune/A30_RESULTS.md).
Activation exclusion, causal CSF induction, residency and regulatory equivalence
are not reinstated. [Key/count verification](../../../analysis/research/runs/cut_fill_a30_join_v1_20261103/verification.json)
passed, establishing the limitation rather than biological acceptance.
