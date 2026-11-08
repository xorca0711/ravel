# Source qualification and correction

8 November 2026. [Contract v1](contracts/qualification_v1.json) froze at `e30618c`;
it stopped on row-order annotation equality before any treatment contrast. Both
matrices contain the same 58,735 unique stable IDs and identical keyed annotations,
but 58,732 row positions differ. [Contract v2](contracts/qualification_v2.json)
froze at `ea6267a` and requires a complete, unique, exact-ID join, retaining count
order and aligning FPKM to it. No source value or filter changed. Its
[receipt](../../analysis/research/runs/sx10_qualification_v2/receipt.json) verifies.

The failed run remains in the [exact archive](../../analysis/research/runs/sx10_failure_preservation_v1/preservation.json)
under a separately frozen [preservation contract](contracts/failure_preservation_v1.json).
Its [original receipt](../../analysis/research/runs/sx10_failure_preservation_v1/failed_receipt.json)
still says execution_failed; archive success is copying only. Original local
files and commit `ea6267a` retain the same bytes. Following the existing Nb5/DY1
pattern, only duplicate index entries are retired; no local source file is deleted
or moved. The success-only registry and validators are unchanged.

| Qualification | Result |
|---|---|
| Matrix dimensions / IDs | 58,735 rows × eight libraries; unique stable IDs; identical ID-keyed annotations |
| Counts / FPKM | Finite nonnegative values; counts integer; original row order preserved for counts |
| All-zero count rows | 29,266, retained |
| Full library count sums | 15,882,574–19,697,334; all positive |
| Expression rule | CPM>=1 in at least two full libraries; 12,677 eligible |
| Repeated symbol labels | 175 labels spanning 1,741 rows; no stable-ID collapse |
| Fixed Figure5 targets | 23 unique exact symbol joins; IL2 below rule; all eight 5B targets eligible |
| Library relationships | Off-diagonal Pearson log-CPM correlations 0.99225–0.99645 on fixed eligible rows; no exclusion or donor inference |
| Source identity | Eight explicit GEO treatment attributes agree with BioSample and SRA sample chains |
| Independent donors / pairing | Unknown; source reports two biological RNA replicates but retrieved attributes lack donor/preparation/allocation keys |

[Sample crosswalk](../../analysis/research/runs/sx10_qualification_v2/sample_crosswalk.csv),
[library QC](../../analysis/research/runs/sx10_qualification_v2/library_qc.csv),
[target mapping](../../analysis/research/runs/sx10_qualification_v2/target_mapping.csv),
[correlations](../../analysis/research/runs/sx10_qualification_v2/library_correlations.csv),
and [repeated symbols](../../analysis/research/runs/sx10_qualification_v2/repeated_symbols.csv)
are immutable outputs. No source alias is guessed from a number suffix.

[Acquisition record](sources/acquisition_v1.json) contains actual routes, access
status, date and payload hashes. Public HTTPS GEO files, BioSample/SRA and PMC
HTML succeeded after sandbox network failures. Supplement routes failed as
described in [literature context](LITERATURE_CONTEXT.md). GRCh38/hg38 and STAR
v2.5 are source-reported; exact annotation release and author display processing
remain unknown. A source-access failure is not evidence of source-wide absence.

Conclusion: treatment identity and RNA measurements qualify finite-library
description. Population inference and exact author replay remain held for their
specific missing evidence; neither hold invalidates the qualified source description.
