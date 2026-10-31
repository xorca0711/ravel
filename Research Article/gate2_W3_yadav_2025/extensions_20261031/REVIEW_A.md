# Checkpoint A review and next bounded jobs

31 October 2026, Asia/Seoul. Reviewed execution commit:
`49f2023be3eba264d45020d2fe9060acf730100c`.
Disposition: **X0-X2 pass technical review within their descriptive scope**.
Scientific acceptance remains unassessed. The original results, source caches,
spatial holds and canonical RQs remain unchanged.

## Evidence checked

- Read the result/amendment record, all source/replicate maps, X1/X2 main and
  independent verification code, source-qualification code, contracts and receipts.
  Verified 65 input hash references, 11 code references and all 28 new output
  hashes; three contract/code bundles match their recorded freeze commits.
  These counts include reused references, not independent sources.
- Reused the inspected independent verifiers without rerunning the analyses:
  X1 passed 288 library values, 120 attribution rows, 48 contrasts, 192 crossed
  differences and all 12,519 memberships; X2 passed direct workbook OOXML checks
  of 213 positions, 111 numeric observations, 24 groups, 120 summary values and
  16 differences. The original saved-core checks remain valid.
- Independently reread X3 metadata/barcodes: exact order and coverage agree for
  50,785 unique barcodes and twelve reported sample labels. This does not establish
  twelve independent animals or an author state/QC mapping.
- Verified all 76 outputs from the eleven original Yadav receipts; unchanged
  canonical question/guide records and all parent registry entries are retained.
- Visually checked all four new PNGs and rendered source PDF pages 7 and 9.
  Labels, mapped arms, supplied normalizers and absence of factorial arms agree.
  The Figure 4C workbook/PDF amplitude discrepancy is real and remains explicit;
  the workbook values were neither rescaled nor replaced to match the plot.

Review script and JSON evidence are preserved in this chat's read-only planning
cache under `yadav/extension_scan_20261031/review_checkpoint_a.py` and
`checkpoint_a_independent_review.json`. The reviewed execution cache remains at
`raw_data/Yd1_extension_20261031` in the execution worktree. No raw cache is moved.

## Scientific interpretation

The primary fibroblast-like Il6 KO-minus-WT mean difference changes from
-0.050556 to +0.036220 when the existing mixed class is included under primary
QC, with the same sign change under broad QC. Detection remains metric-dependent.
This restricts any claim of a stable lower Il6 RNA average; it does not establish
an opposite causal genotype effect. Macrophage-like Arg1 remains lower, and
fibroblast-like Il6 remains higher in WT coculture than alone, under this fixed
diagnostic. Unknown preparations and class/ambient/composition effects remain.

The Fig. 6C workbook coculture protein difference remains -339.98655 pg/mL for
KO minus WT. This is a source-marginal observation in unlinked preparations;
RNA/protein disagreement cannot identify mediation or post-transcriptional control.
Fig. 4C supports a workbook-only reconstruction while exact plot amplitude
reproduction is held for a reconciled source version. All prior unfavorable
findings and normalization/unit restrictions remain authoritative.

## Checkpoint B authorization

### B1 / X3: recover author retention and state metadata

The conditional sample-level design in [EXTERNAL_FEASIBILITY.md](EXTERNAL_FEASIBILITY.md)
is suitable in principle, but actual author state names, retention joins and state
support must be reviewed before expression extraction. A missing day-0 state must
not be repaired by dropping samples, relabeling cells or weakening the support rule.

First seek a linked small author metadata export. If none is available, acquisition
of the specifically listed `GSM6428697_seurat_v4_obj.rds.gz` (1,553,376,346 listed
compressed bytes) is justified for metadata recovery. Check local storage/runtime
capacity, preserve URL/date/size/hash and failed attempts, and use a new governed
metadata contract. The source record describes this object as filtered, merged
and clustered. Deserializing it may load an expression-bearing container; record
that access honestly, but do not extract, export or summarize expression values.

Return exact author state labels and provenance, retained/dropped barcode and
sample/day joins, state occupancy for every sample, demultiplex ambiguity fields
if present, and a precise mapping of proposed states to author fields. If only
cluster IDs exist, do not invent named states. Preserve the fixed four targets,
three day-versus-day-0 contrasts, sample weighting, zero-cell handling and no-test
scope. No separate 541 MB matrix or full RAW archive is authorized at this stage.

### B2 / X5: bounded remaining source access

The public code README explicitly links the [SCAHN web app](https://scahn.khatrilab.org/).
Inspect its FAQ/source/download metadata and any directly linked primary source
table, plus a bounded primary supplement route. The reviewer web tool could not
open the app; this is an access failure, not evidence the metadata are absent.
New targeted searches on 31 October were the article DOI with `data Zenodo` and
`Supplementary Table`; the indexed publisher record still points to Table 1.

Do not query ARG1/IL6R expression, download the full atlas or substitute app means
for raw donor/cell evidence. Return source IDs and overlap/capture/donor support
if recovered, or exact attempted URLs/outcomes and a specific source hold. This
is one bounded remaining source pass, not permission for an unbounded search.

### B3 / X6: begin evidence-to-decision synthesis

Proceed independently of source access. Build the planned matrix for unchanged
Wg-P06 (arginine preservation versus ornithine delivery, with OAT/PRODH/ROS,
cytokine and viability alternatives) and a separate A13/A20/A8/A19 epithelial
bridge. Use reviewed X1/X2, original results and valid literature scans; specify
what each measured endpoint discriminates and what measurement remains absent.
Keep X3/X5 pending where appropriate. This is a provisional synthesis, not a
bench-ready protocol or final extension closeout. Refresh literature only if the
comparison is materially changed or an experiment-readiness package is proposed.

X4 culture/native and stage comparisons retain their documented source/design
holds. Both native and cultured assays are described as fixed-RNA profiling;
FFPE tissue versus fixed cultured cells still require assay and donor joins.
No substitute native-only disease contrast is requested. The executor returns
one clean checkpoint-B commit with metadata contracts/receipts, source maps,
the provisional matrix and exact remaining jobs. All external numerical
comparisons continue to require a specific reviewed design.

## Integration and validation

Fresh main remains `8cb50dd15a12a41abc6d5edb36349d33fc512661`.
Local checkpoint integration preserves both dispatch and execution histories.
The executor's 158 tests (two documented skips) remain valid. Required repository
and current-base integration checks passed: 12,153 repository checks and
`research_gate.py check --base origin/main` returned `ok: true`, no errors.
No remote publication, Notion write, external outreach, new RQ or gate change.
