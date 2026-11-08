# Supplement qualification v2 amendment — 8 November 2026

The first supplementary-source run completed 41,017 checks but failed two checks
for the same source cell: Table S5 (`NIHMS2118436-supplement-6.xlsx`), Sheet1!A333,
in the Gene column for a cDC1 published DEG. The OOXML stores numeric serial
`45903`, style 9; the workbook number format is `d-mmm`. Independent openpyxl
reading exposes a date, 3 September 2025, rather than a gene string. This newly
observed source-format problem is now outcome-exposed.

V2 preserves the raw serial, saved number-format metadata and workbook date
system. The independent reader checks numeric/date equivalence under the verified
Windows date system, and separately requires that the gene symbol be blank with
an explicit unresolved-source flag. The displayed date is not reverse-mapped to
a gene name. Original source clarification is required. Other published DEG
values and this row's cell-type label remain preserved, not reestimated.

Every file from the failed v1 run is copied byte-for-byte into a declared archive
in the new run, including its failed receipt and verification report. V1 contract,
scripts, outputs and original workbooks remain unchanged. Archive success never
relabels the earlier attempt as successful. No repository validator or scientific
interpretation boundary changes.

The failed run also exposed P24/P25 ethnicity wording differences (Table S1
"White or Caucasian" versus GEO "White/Caucasian"). They remain reported as text
differences; no additional alias normalization is introduced to erase them.
All other source-stage scope, unknown IDs, P6/P7 holds, species/program namespaces
and custom-add-on versus full-assay distinctions remain as frozen in v1.
