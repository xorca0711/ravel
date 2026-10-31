# T1-A review and T1-B authorization

31 October 2026. Exact execution return
`bc17da15f9e62fb657ba06642c65542517b857c0`, frozen numerical specifications
`5e1d7dbbfac8ae3ba41046b1b3542e1cec5d716c`.
[T1-A](T1A_RESULTS.md) passes technical verification of its frozen calculations.
B1 native-label descriptions are reviewed complete. R1's conservative vector
qualification is preserved, with the measurement interpretation below.
[T2](T2_DISPOSITION.md) passes bounded design/access review; its empirical
holds remain. No scientific acceptance or biological effect test follows.

## Review evidence

Read the exact contracts, source/QC/summary tables, parser and descriptive code,
figures, independent verification, [R2 design](R2_DESIGN.md) and T2 disposition.
Verified both receipt/freeze identities, 12 input references, eight code
references and all 13 expected output hashes. Canonical questions/guides,
infrastructure declarations, older contracts/receipts and non-scope files are
unchanged. Reused the valid 6,306 independent openpyxl/arithmetic checks and
ten pre-freeze boundary checks rather than rerunning the whole analysis.
The reviewer inspected both PNGs and independently checked the native source
unit headers and R2's nine distinct header sequences against immutable T0 data.
No R2 numerical values were inspected for this review.

The review integrity record is `t1a_review_integrity.json` in the review chat's
follow-up staging folder. Fresh main is unchanged at
`8cb50dd15a12a41abc6d5edb36349d33fc512661`.

## What the holds mean

R1 retains 1,440 literal cells, 160 of them missing. Its 95 held summaries and
59 held sample-metabolite vectors follow the frozen rules. There is no evidence
here of a parsing/arithmetic error, a biological negative, or invalidity of every
reported value in a held vector. B1's 144 literal values and 36 means/ranges are
qualified only under the source's native labels; the nutrient key stays unknown.

The v1 rule combines three different questions: is a channel supplied and valid,
what unit does the source declare, and does a complete vector close numerically?
The source explicitly declares percentages at Figure 3B K2/J13/K24/O35/M46 and
Figures 3D/3H/4D J1. Thus failure of `64*n*ulp(scale)` closure does not by itself
erase the declared unit or prevent description of separately supplied channels.
Likewise, an absent higher channel is not a zero and prevents a complete-vector
claim, but does not make a different fully supplied channel unobservable.

Small 4D residuals may reflect export/processing, but that cause is unproven.
Do not tune the old tolerance, infer precision from decimal length, fill channels,
renormalize, or call the vectors validated. The v1 outputs and all their holds
remain immutable. The next job has a narrower **literal reported-channel**
endpoint, explicitly separating that description from vector validation.
This source-grounded amendment is reviewed here; no repository gate is changed.

## Exact next checkpoint: T1-B

Use new exposed frozen contracts/code and new run directories. Bind this review,
the same workbook hash, exact unit cells and approved coordinate/header maps.
Record all T1-A outcome exposure; no retrospective confirmation claim. Preserve
the originals with explicit amendment/supersession links explaining scope.

### R1 channel-description companion

- Use only the existing R1 15-block fraction coordinates and exact sample maps.
  Do not rerun B1 or duplicate the already verified R1 area summaries.
- The endpoint is **source-reported isotope-channel percentage**, as declared
  in the exact header cells above. Freeze these literals; a changed/ambiguous
  source header holds the affected block. No 0–1/0–100 conversion inferred from
  observed outcomes, no automatic rescaling and no revalidated normalization.
- Per isotope/condition, retain all four supplied labels and compute count,
  unweighted mean and range only when all four cells are numeric, finite and
  valid in the declared percent domain. A missing, formula, negative, out-of-
  domain or otherwise invalid cell holds that channel summary; do not reduce n.
  Missing cells in other channels remain visible but do not block a fully
  supplied channel. Keep every channel in the output, including held ones.
- Preserve completeness and the **unchanged v1 closure diagnostic** separately.
  A partial-channel subtotal must be labelled incomplete and never presented
  as a complete sum. Record observed complete sums/residuals without treating
  them as biological margins or relaxing the original closure rule.
- Descriptive TGF-minus-UT differences may use two complete channel summaries;
  units are percentage points. No paired effects, p-values, confidence intervals,
  inferred donors or cross-medium pooled effects. Use unstacked channel plots
  with missing/held annotations and a caption that vector completeness and
  normalization are not established. No inferred detection limit or absence.

### R2 source descriptions

Approve the exact **14 area and 13 percentage blocks** in R2_DESIGN.md:
3F's three area/two percentage blocks; six 4B pairs; five 4F pairs. The reviewer
checked their header sequences, not their numerical outcomes. Freeze each unit
header, sample string, source coordinate and isotope sequence before extraction.

Use the same separation of literal-channel description from full-vector QC.
Areas require all supplied values valid within that isotope/condition; percentages
also require their explicit source unit. Use the source's native area wording:
4F says `Peak Area`/`Percent`, not explicitly corrected. Preserve the general
Methods correction claim separately. No arbitrary cross-metabolite area comparison.

All 3F argininosuccinate percentage channels and **all 4B putrescine** remain
held for ambiguous mapping. Do not repair or selectively discard duplicates.
4F has three supplied labels per condition; retain all three, report observed
means/ranges only, and preserve the published n=4 plus SEM/SD disagreement.
No invented fourth observation or exact published-error-bar reconstruction.
Retain the 3F D4-versus-Methods tracer discrepancy without a biochemical repair.
Any source mismatch holds its affected block; independent eligible blocks continue.

R1/R2 must include independent source/arithmetic checks of the new endpoint,
especially a valid individual channel with missing neighbors, unchanged failed
closure diagnostics, invalid target cells and full supplied-n requirements.
Reuse valid parser/tests where applicable. No original Yadav pipeline replay.
No raw-MS correction, kinetic flux, calibrated pool, source ARG1 effect,
collagen incorporation, route necessity or mature repair claim is authorized.

## T2/T3 and completion boundary

T2 identifies no confirmed host model/assay access or linked source-ARG1 exposure,
collagen and mature-output data. Its exact reopening requirements are adequate:
actual compatible model/data, preparation/donor crossing, validated intervention,
measured exposure and relevant functional endpoints, timing and justified
precision/oversight. Published precedent is not access. No repeated Atg5 search,
new proxy, broad atlas work, outreach or bench execution is warranted.

Return T1-B with contracts/receipts, source-cell and unit provenance, independent
verification, complete tables/figures and a combined follow-up disposition.
Distinguish completed source descriptions and design work from empirical holds.
Do not declare the whole scope complete until the reviewer checks the return
and confirms no other feasible authorized job remains. Original human-source,
spatial/X3–X5, collagen/Lee source, raw-MS/flux and joint-function holds persist.

## Integration

T1-A is integrated locally, with both versions of the dispatch/return ledger
preserved. Two current-status documentation conflicts were reconciled; frozen
scientific files had no conflicts or edits. Current-main integration passed
12,463 repository checks and the research gate (`ok: true`, no errors). Logs are
`t1a_integration_repository.log` and `t1a_integration_gate.log` in review staging.
No remote push, PR, outreach or scientific acceptance.
