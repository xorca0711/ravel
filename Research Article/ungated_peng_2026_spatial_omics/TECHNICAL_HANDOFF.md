# Technical execution handoff

Owner request, 8 November 2026: execute the structured plan in a separate technical
chat using helpful plugins/skills. Start with [PLAN.md](PLAN.md),
[SOURCE_RECOVERY.md](SOURCE_RECOVERY.md), current governance and the registry.
Read current results before historical plans. Pg1-P01 owns metadata/reproduction;
the conditional contextual extension remains A12. This is outcome-exposed work.

## Workspace and preservation

Use the existing scoped worktree
`X:/GitHub/ravel/.worktrees/peng-spatial-reading-20261108`, branch
`codex/peng-spatial-reading-20261108`. The planning chat finishes its writes before
dispatch. Inspect HEAD, upstream and actual diffs before continuing; refresh main
and account for subsequent changes before delivery. The planning base was main
`1ff71a1818be1782dede0ccd5898eea793497f73`.

The original `X:/GitHub/ravel` checkout is an older branch with unrelated dirty
PROGRESS work. Preserve it. Do not reset, stash, clean or copy its state wholesale.
Some files in this worktree have stat/line-ending status noise but no Git content
diff: 33 files were byte-restored to their existing blobs to satisfy frozen
hashes. Fifteen missing locked outputs were supplied from exact hash-matched
local copies; all 16 bound members verified. Do not normalize/replay them.

## Inputs already present

- Ignored `raw_data/peng_spatial_20261108/`: three `GSE*_family.soft.gz` files,
  Zenodo records, public PMC HTML, GEO directory HTML, author repository tree,
  Figure 1 source and `acquisition_v1.json`–`acquisition_v4.json` receipts.
- `Research Article/gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/`:
  `REPORT.md`, `RNA_spatial_demographic_crosswalk.csv`,
  `RNA_spatial_crosswalk_validation.json`, `deposited_member_inventory.csv`, and
  `possible_pathology_annotation_members.csv` (header only).
- C3 `trials/u0_geo_design_audit/sample_inventory.csv`, `human_sample_links.csv`;
  `trials/u5_human_pilot/all_series_patient_histology_crosswalk.csv`; and
  `trials/u5_human_full/library_qc_and_annotation.csv`.
- Existing large RNA cache, if a later qualified step needs it:
  `X:/GitHub/ravel/Research Article/gate2_C3_yu_lee_choi_min_2026/cache/u5_human_full/`.
  Reuse read-only; no duplicate full matrix download or unneeded expression rerun.
- Supplied VOR/supplement PDFs remain at the user-provided
  `C:/Users/dream/Documents/AC_document/GisTomics/26-2/` paths. The Notion content
  was reviewed in the parent assessment; private snapshots/notes are not public
  repository artifacts and should not be copied into source exports.

## First executable work

1. Build a bounded metadata parser and contract, register under Pg1-P01, freeze
   and commit before its new numerical output. Hash SOFT and reused inventories.
   Preserve explicit, parsed and unknown fields separately; report conflicts and
   duplicates, not guessed aliases. WES is GSE307529; there is no recovered public
   Xenium GEO accession in this record.
2. Run with `analysis/scripts/research_gate.py run`; independently verify join
   cardinality and sample/patient counts against raw records and prior C3 evidence.
   Register receipt and write `RESULTS.md` with exact outputs and narrower holds.
3. Continue eligible PLAN stages. Do not stop merely because one annotation source
   is restricted. Finish all useful metadata/source checks and draft the exact
   missing-file request; do not send it without user authorization. Avoid repeating
   documented failed downloads unless a different supported route can change the result.

Useful skills: scientific hypothesis generation for comparison framing; GEO
database/source qualification for metadata; multimodal-omics integration when
actual cross-platform objects are available. Use Notion/GitHub connectors for
supported reads, public literature tools for precise primary-source verification,
and PDF tools for unresolved figure/method details. No NGS workflow, biological
model or paid compute needs launching merely to parse metadata. Skills do not
override repository contracts or expand permissions.

## Validation and delivery

Run focused parser/join checks and the required repository/research gate checks.
The prior documentation review passed 167 tests (two skipped), compilation,
18 claim bindings, archive verifiers and repository checks; reuse these where
unchanged, and rerun checks invalidated by new code/registry edits. Test temp
files need a writable directory; the prior run used the visualization workspace's
`peng_review/test_temp` through TEMP/TMP. Do not weaken validators or overwrite
frozen outputs to resolve failures. Report execution separately from scientific
eligibility/acceptance. Update PROGRESS, current article results and affected A12
entrypoints consistently. No push, PR, merge, author message or Notion mutation
has been requested as part of this handoff.
