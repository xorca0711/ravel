# Nb3: human S5 numeric concordance is unresolved

**1 October 2026; post-hoc source-consistency audit.** This audit was triggered
by the completed DE comparison. It neither changes the frozen analysis choices
nor relabels source data to improve agreement.

The numeric human S5 table is **not reproduced**. Its up/down summary fields,
however, strongly agree with the reconstructed directions for the five checked
targets. These evidence layers must remain distinct. The checks identify an
internal source-table discrepancy; they do not establish how the original table
was assembled or supply a justified repair.

## What disagrees

Across the source-selected gene universes, median Pearson logFC correlation is
**0.9606** for mouse S4 and **0.0035** for human S5. Human labeled-target
correlations range from **−0.0647 to 0.0409**, and median sign agreement is
**0.5048**. These are comparisons against the source's numeric fields, not
independent biological validation.

An audit performed directly on the original workbooks compares each target
listed in `whichKOs_up`/`whichKOs_down` with that row's labeled numeric logFC:

| Source | Listed gene/target directions | Matching numeric signs | Conflicting numeric signs |
|---|---:|---:|---:|
| S4 mouse | 12,897 | 12,897 | 0 |
| S5 human | 18,976 | 9,989 | 8,987 |

The stated up/down counts equal their list lengths in both files, and no listed
pair lacks its numeric value. For example, human **RGS5**, stable ID
`ENSG00000143248`, lists **NKX21 as down**, but its labeled numeric NKX21 logFC
is **+0.47701928** (numeric adjusted p **0.02324416**). The sign conflict is
within S5 itself and does not depend on the Nb3 fit.

Evidence: [internal consistency](../runs/concordance_audit_v1/source_internal_consistency.tsv)
and [selected conflicts](../runs/concordance_audit_v1/source_direction_conflicts.tsv).

## What agrees

For the primary NKX21 comparison and four diagnostic targets chosen from the
existing screen/extension set, the source **direction lists** agree closely
with the count-derived logFC signs:

| Target | Source-listed directions checked | Matching reconstructed signs |
|---|---:|---:|
| NKX21 | 4,558 | 4,558 |
| MET | 59 | 59 |
| ACOXL | 6 | 6 |
| TRP53 | 437 | 437 |
| ERBB3 | 194 | 193 |
| Total | 5,254 | 5,253 |

This supports the directional reconstruction for these selected comparisons.
It does not recover the numeric effect sizes/p-values in S5, extend the audit
to every target, or establish independent biological replication.
See [source-summary comparison](../runs/concordance_audit_v1/source_summary_vs_reconstructed_signs.tsv).

## Checks on extraction and mapping

The full count extraction already matches all archived A10 species/library
totals and uses unique stable IDs. A second parser, Python's XML ElementTree
rather than the extraction script's row/cell regular expressions, reread the
original human workbook rows for **RGS5, PLIN2 and CXCL8**. All **2,658 count
entries** (three genes across 886 libraries) and their symbols exactly match
the extracted binary matrix. This is a targeted independent extraction check,
not an assertion that every individual count was reread by two parsers.

RGS5 also labels an antisense feature in the source annotation. The initial
audit stopped on this ambiguity before writing outputs, then used the exact
three S5 stable IDs. No count row, score, gene DE result or source label changed.

To check a simple target-column swap, each of the same five reconstructed
profiles was compared with all 195 numeric S5 target columns. The largest
Pearson correlations were only **0.037–0.047**. A straightforward target-label
permutation therefore does not explain the inspected discrepancies. No
best-matching label was adopted.

Evidence: [independent count checks](../runs/concordance_audit_v1/independent_count_checks.tsv),
[target-column diagnostic](../runs/concordance_audit_v1/target_swap_diagnostic.tsv),
[audit record](../runs/concordance_audit_v1/run_record.json) and
[audit implementation](../scripts/12_audit_concordance_discrepancy.py).

## Consequence for Nb3

Keep the verified count-derived expression/panel results and the original S5
fields separately. Report the fibroblast arm as **descriptive count reanalysis
with directional source support for the checked targets, but failed numeric S5
reproduction**. Do not substitute the correct-looking direction summaries for
the unresolved numeric source table.

Before an exact human DE reproduction claim, obtain the original generating
code or a reconciled gene/target-to-value mapping/corrected S5 table. Record
which source fields and model settings it supersedes. A new reconstruction
version may then be compared without rewriting these v1 records. No author
contact or external message was sent during this work.
