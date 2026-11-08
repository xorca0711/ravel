# Top-level documentation dependency cleanup

8 November 2026; base `60537cdbaff97f4e6728c58ea97e16a6b265db13`, after merged
PRs #170 and #171. The owner pointed out that compatibility files still cluttered
the `docs/` listing. Ordinary incoming references are movable; only concrete
frozen/generated consumers justify retaining an old path.

## Changes

- Five current guides moved into `docs/guides/`, `docs/governance/` and
  `docs/portfolio/`, with incoming links updated and no new root-level stubs.
- Three unnecessary locators were removed: `DOUBLETS_AND_SCRUBLET.md`,
  `LOGICAL_RATIONALE_REVIEW.md` and `scRNAseq_workflow_Niethamer2025.md`.
  Their full documents were already organized by PR #170; all non-link content
  is preserved, with link destinations updated where needed.
- The two mutable roadmap references now use the actual destinations. Claim C7's
  artifact path points directly to the existing full doublet report; the claim
  wording, status and numeric bindings are unchanged. Its manifest/summaries were
  regenerated using the existing tools.
- The `docs/` root now has 17 Markdown files, down from 25. Seven are necessary
  compatibility locators; two more remain under `research_dossiers/`.

[Migration record](migration.json) lists paths, original hashes and frozen files.
Historical manifests keep their original path lists; a dated validation snapshot
is not a current runtime consumer and no longer justifies an otherwise unused stub.

## Why the remaining root paths exist

| File(s) | Concrete reason |
|---|---|
| `README.md`, `DATASETS.md` | Deliberate stable documentation/source entry points |
| `CLAIM_SUMMARY.md`, `NEGATIVE_RESULTS.md` | Current generated outputs and existing generator/checker paths |
| `PIPELINE_AS_RUN.md`, `ANALYSIS_RATIONALE.md` | Original pipeline outputs/references, including generator and validation consumers |
| `RESEARCH_ARCHITECTURE.md` | Linked from the exact-byte A10 report bound by A22 identity-amount run records |
| `RESEARCH_GOVERNANCE.md` | Referenced by a hash-bound A8 document and frozen provenance |
| `RQ_MEASUREMENT_CONTRACTS.md`, `NEXT_DATASET_GATE.md` | References inside preserved legacy question contracts |
| `PORTFOLIO.md` | Referenced by hash-bound dossier A13 |
| `SCDS.md`, `SCRUBLET.md`, `SLINGSHOT.md`, `SOUPX.md`, `TRADESEQ.md` | Original pipeline generator and its saved output use these relative links |
| `UMAP_AND_FIGURES.md` | Original phase/time-course generator still emits this link |

Moving these remaining paths without replacement requires a separate migration
of generated-output contracts and frozen-reference handling. This cleanup does
not edit frozen records, introduce an integrity exception or change a validator.
The previous source register, raw caches, numerical outputs and source contracts
are preserved. No biological analysis was rerun.

## Validation and delivery

Validation passed against refreshed, unchanged main `60537cd`: 82 focused
move/preservation checks and 15,053 local links, 18,222 repository checks,
167 unit tests (two skips), all 18 claim numeric bindings, the unchanged
base-aware provenance gate and whitespace checks. The manifest diff contains
only C7's two artifact-path fields and the updated source-document checksum.
Existing CRLF serialization in the generated manifest is retained.

CI exposed an additional exact-byte dependency: the A22 extension records bind
the A10 endpoint report, whose architecture links must remain unchanged. The
report was restored byte-for-byte and `RESEARCH_ARCHITECTURE.md` retained at its
original path. The unchanged A22/A23 archive verifier was rerun after repair.
No archive hash or validator was relaxed. [Focused result](validation.json).
[PR #172](https://github.com/xorca0711/ravel/pull/172) is open for owner review;
its [checks page](https://github.com/xorca0711/ravel/pull/172/checks) records remote
validation. No merge was performed.

[Current documentation](../../README.md).
