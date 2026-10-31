# T1-R2: exact proposed source-description whitelist

31 October 2026, Asia/Seoul. **Design qualification complete; no R2 numerical
run or value inspection was performed.** This proposal implements
[REVIEW_T0](REVIEW_T0.md). It must be reviewed before a new exposed contract,
code freeze and execution. It neither amends nor overwrites T0 or T1-A.

Owner Wg-P06; purpose is descriptive source reconstruction supporting RQ2.
Endpoint: supplied isotope-channel peak areas and reported percentages,
with counts/means/ranges within literal condition labels. The biological unit
remains unknown beyond a source sample string. The principal validity threat
is repairing ambiguous headers or missing channels by inference, followed by
treating source-label suffixes as independent donors or paired observations.

## Source and mapping authority

Use the same Hamanaka Figshare v1 workbook, SHA-256
`d8d3365b226323d3ebe7300c481625049ae1cae3f78948938956240b8ea79f4f`.
All maps below come from the immutable T0
[text-cell layout](../../analysis/research/runs/Wg_P06_followup_t0_br_v1/workbook_layout.json),
not numerical values. Primary locators and assay conflicts remain in
[T0_RESULTS](T0_RESULTS.md): Hamanaka Figs. 3F/4B/4F and S4/S5, and Methods.
The published 3F panel/sample strings identify D4-citrulline while Methods
also name 13C5-citrulline. Preserve that discrepancy; no tracer identity repair
or pathway assignment follows from this map.

## Figure 3F

In each block, A contains sample IDs, B the supplied group field and C the
metabolite. The first four rows have `Pos_D4_Citrln_01` through `_04`; the
next four have `Pos_D4_Citrln_TGFb_01` through `_04`. Retain B literally;
do not replace group metadata or infer pairing from suffixes.

| Metabolite | Value rows | Isotope header row | Proposed area columns and exact sequence | Proposed percent columns and exact sequence |
| --- | --- | --- | --- | --- |
| Citrulline | 4–11 | 3 | D:R, M+0 through M+14 | S:AG, M+0 through M+14 |
| Argininosuccinate | 16–23 | 15 | D:W, M+0 through M+19; area-only eligible | **Held:** X:AQ has duplicate isotope headers |
| Arginine | 28–35 | 27 | D:S, M+0 through M+15 | T:AI, M+0 through M+15 |

Unit headers are D2/D14/D26 = `Natural abundance corrected peak area` and
S2/X14/T26 = `Natural abundance corrected percentages`. These are source
processing labels, not validation of correction settings or calibrated amounts.
For the held argininosuccinate fractions, X15:AO15 runs M+0 through M+17,
but AP15/AQ15 repeat M+14/M+15 already present at AL15/AM15. Do not rename
them M+18/M+19, discard duplicate channels or normalize the remaining vector.
The independently clear D:W area map may proceed if separately approved.

## Figure 4B

Header row 2: A `Sample`, B `Group`, C `Metabolite`, D `Formula`.
Unit headers E1/P1 are `Natural abundance corrected peak area` /
`Natural abundance corrected percentages`. For each of the six blocks below,
the **exact common whitelist** is area E:O (M+0 through M+10 in E2:O2) and
percentage P:Z (M+0 through M+10 in P2:Z2).

| Metabolite | Value rows | First four labels | Last four labels |
| --- | --- | --- | --- |
| Arginine | 3–10 | TG_01–TG_04 | untreated_01–untreated_04 |
| Argininosuccinate | 13–20 | TG_01–TG_04 | untreated_01–untreated_04 |
| Citrulline | 23–30 | TG_01–TG_04 | untreated_01–untreated_04 |
| Dimethylarginine | 33–40 | TG_01–TG_04 | untreated_01–untreated_04 |
| Ornithine | 43–50 | TG_01–TG_04 | untreated_01–untreated_04 |
| Proline | 53–60 | TG_01–TG_04 | untreated_01–untreated_04 |

This is a header whitelist, not a claim that all eleven channels are populated
in every row. Any blank higher channel remains missing, not structural zero;
complete-vector qualification must be decided under the future frozen rule.
Area summaries can remain eligible independently by isotope where complete.

**Putrescine rows 63–70 remain entirely held.** Metadata repeats in P:S
(sample/group/metabolite/formula), followed by values at T:X, while E:I is
area-like. There is no dedicated isotope/unit header establishing this shifted
map. The common P:Z header would misidentify metadata as percentages. Neither
magnitude, chemical expectation nor similarity to another block resolves it.

## Figure 4F: three-label description only

Header row 2: A `sample`, B `metabolite`; C:H and I:N each read M+0 through
M+5. C1 = `Peak Area`, I1 = `Percent`. Unlike 3F/4B, these headers do not
explicitly say corrected; report the literal unit wording and retain the
general Methods correction claim separately.

| Metabolite | Value rows | First three labels | Last three labels |
| --- | --- | --- | --- |
| Glutamate | 3–8 | 13C5Q_TGFb_01–03 | 13C5Q_untreated_01–03 |
| P5C | 11–16 | 13C5Q_TGFb_01–03 | 13C5Q_untreated_01–03 |
| Ornithine | 19–24 | Pos_13C5Q_TGFB_01–03 | Pos_13C5Q_Untreated_01–03 |
| Proline | 27–32 | Pos_13C5Q_TGFB_01–03 | Pos_13C5Q_Untreated_01–03 |
| Putrescine | 35–40 | Pos_13C5Q_TGFB_01–03 | Pos_13C5Q_Untreated_01–03 |

The proposed value whitelist is C:H area and I:N percent for these rows only.
There are three supplied labels per condition, not four. Published Fig. 4
states n=4 with SEM; S5 states n=4 with SD. Preserve all three facts. Do not
fabricate suffix 04, infer the error-bar convention, or describe a three-label
mean/range as exact published replication. P5C and all other metabolite labels
must remain literal; no cross-metabolite area pooling is eligible.

## Proposed execution rules and review decision

The proposed map contains **14 area blocks and 13 fraction blocks**: three
3F areas/two fractions, six 4B pairs and five 4F pairs. Only those coordinates,
headers, unit cells and full label strings would enter a future contract.
An exact source-map mismatch holds its affected block. All literal invalid,
negative, formula and missing cells are retained and flagged. Means/ranges
require every supplied label valid; no filling or partial-n mean. Areas and
fractions have separate qualification paths.

Freeze scale candidates and numerical tolerance before any R2 value inspection,
with their numerical representation basis stated. T1-A already exposed small
closure discrepancies and missing channels in different sheets; this is part
of the future exposure record, not justification to tune tolerances to R2
outcomes. No automatic inference of precision from a short decimal or of zero
from a blank is permitted. Source clarification would be a new evidence
version and amendment, not a repair of frozen outputs.

If authorized, report every eligible isotope/condition count, mean and observed
range, with explicitly descriptive TGF-minus-UT differences only if included
in the reviewed contract. Use separate source-cell maps, QC and figures;
independent source/arithmetic verification precedes interpretation. No p-values,
donor CI, pairing, cross-medium pooling, raw correction replay, flux, collagen
incorporation or source ARG1 effect. Complete and unfavorable outputs remain.

Next decision: approve, narrow or amend this exact proposed whitelist and its
future descriptive rules. Until that review, R2 numerical execution is held;
unambiguous design qualification is complete and does not require new outreach.
