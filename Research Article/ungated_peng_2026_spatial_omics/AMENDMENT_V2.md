# Metadata v2 amendment — 8 November 2026

The frozen v1 run failed its independently implemented filename/description
identity check. Five GSE308103 supplementary filenames use `Normal1`, `AAH1`,
`LUAD1` or `AIS1` where the explicit author Library name uses `-1`:
GSM9237905, GSM9237907, GSM9237917, GSM9237960 and GSM9237968.
This is new exposure from the failed attempt, not an unexposed correction.

The v1 assumption that filename text equals the explicit library description was
too strong. V2 preserves both verbatim strings, records all five disagreements,
and requires their complete detection in the separate verifier. A supplementary
URL is linked to its GSM by the deposited record. That provenance does not make
the strings identical or license a global suffix normalization. Cross-platform
joins continue to use the exact author Library name, never the parsed filename.
Patient, lesion, serial-section and same-cell limitations remain unchanged.

V1 contract, scripts, receipt, partial outputs and logs remain byte-unchanged.
V2 includes a byte-identical archive of all twelve failed-run files as declared
outputs, with their hashes and explicit `execution_failed` status. A successful
archive or v2 run cannot turn v1 into a successful analysis. The original local
run may be ignored only after the registered archive is verified; no original
file is removed or moved. Repository governance and validators are unchanged.

The amended contract is frozen and committed before execution. Counts, aliases,
the five filename discrepancies and prior C3 comparisons are now outcome-exposed.
The scientific endpoint remains source/metadata qualification. No expression
analysis, biological claim, RQ identity or acceptance changes.
