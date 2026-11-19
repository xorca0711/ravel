# S1M v2: qualify compact deposit labels

17 November 2026. Supersedes only the grouping portion of the successful
[v1 run](../../analysis/research/runs/naik2017_s1m_metadata_v1/S1M_REPORT.md).
The original contract, code, receipt and outputs remain immutable and registered.

V1 verified the 28 explicit library/experiment/run joins and the 16 count-table
structures, but its word-boundary parser left compact titles such as
`D30CtrlEpdSC_R1_RNA-seq` unclassified. Thus v1 execution success did not complete
the condition/time crosswalk. Its displayed unclassified groups are retained,
not silently corrected.

V2 recognizes the observed deposit title forms (including the literal `IMQl`
spelling), retaining the original titles. It compares history labels with the
selected GEO treatment characteristic and checks explicit harvest/wound time
fields for contradictions. For recall samples, a day is assigned only when the
saved treatment characteristic explicitly gives it. Labels without a matching
characteristic retain that provenance limit. Replicate suffixes still do not
identify animals, independent preparations or paired assays.

Inputs, assays, count checks and biological scope are unchanged. The first run's
metadata and structural summaries are now additional prior exposure; no gene
effects were estimated. The question remains whether source-qualified molecular
libraries support a scoped S2 comparison. No effect threshold, sample exclusion,
biological acceptance or previously blocked source extraction is introduced.
Freeze/commit the new contract and code, then run under a new immutable run ID.

Setup note: a generic Git whitespace check flagged the 28 empty final
`disagreements` fields in v1's frozen `run_crosswalk.tsv`, so the first v2 commit
command stopped. A subsequently issued runner command correctly refused the
uncommitted v2 contract/code before execution; it created no v2 run directory or
receipt. The table's trailing separators represent valid empty cells and are
preserved with their receipt-bound bytes. Validate uniform TSV field widths and
check other changed files for whitespace; do not edit the frozen output or
change repository validators. This pre-execution refusal is not a scientific
run or a content-safety rejection.
