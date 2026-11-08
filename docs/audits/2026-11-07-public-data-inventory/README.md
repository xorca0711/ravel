# Public-data and local deposit reconciliation

**Initial snapshot v1, retained as history.** The [current v2 reconciliation](RECONCILIATION_V2.md)
includes merged PR #167, later GSE262130 use, a fresh cache census and navigation
cleanup. Counts and unmerged-branch statements below describe the original scan.

7 November 2026 (Asia/Seoul). Documentation/storage audit of merged main
`dcee4b63e11abd27fe2bbc679993b288e913565e`, freshly fetched from origin.
Worktree: `X:/GitHub/ravel/.worktrees/public-data-inventory-20261107`, branch
`codex/public-data-inventory-20261107`. The older project-root checkout at
`78320a1` and its existing PROGRESS edits were preserved.

## Result

The central inventory was mostly a 28 September source-use list with scattered
additions through 7 October. The raw inventory described only the original two
GEO series: 51 files, roughly 7.8 GiB. It was not a current repository-wide cache
census. Its three original files and scanner remain unchanged.

[DATASETS](../../DATASETS.md) now routes to the [current source-use additions](../../DATASET_UPDATES_2026-11-07.md)
and this inventory. Eighteen grouped entries document omitted or expanded
numerical/source-reconstruction use, followed by ten grouped qualification
entries, non-cohort references and a separate unmerged DuPage record. Wp's stale
blanket absence wording is corrected using its existing correction report.
No scientific eligibility, claim grade, contract, receipt or frozen output changed.

## What is actually stored locally

The read-only scan found **4,181 files / 74,039,394,025 apparent bytes
(74.04 GB; 68.95 GiB)** across **15 existing cache roots** in ten worktrees.
There were no traversal errors or skipped nested links. The source roots contain
metadata, downloaded matrices/archives, references and derived cache products;
the totals are neither unique data volume nor a dataset/sample count.

| Storage scope | Files | Apparent bytes |
|---|---:|---:|
| Project-root `raw_data/`, 33 first-level directories | 955 | 34,520,206,615 |
| Other conventional source/reference caches in project root | 2,595 | 28,328,488,848 |
| Caches in the other registered worktrees | 631 | 11,190,698,562 |
| Total | 4,181 | 74,039,394,025 |

| Worktree storage ID | Files | Apparent bytes |
|---|---:|---:|
| project-root | 3,550 | 62,848,695,463 |
| macrophage-memory-review-20261029 | 149 | 3,627,069,523 |
| full-priority-screening-20261103 | 11 | 2,924,582,713 |
| saxton-metadata-recovery-20261031 | 133 | 2,260,825,612 |
| ravel-rename-20261007 | 27 | 1,950,317,850 |
| wagner-continuation-20261004 | 220 | 374,117,410 |
| dupage-stepwise-plan-20261107 | 34 | 31,536,250 |
| saxton-il22-execution-20261031 | 17 | 10,269,890 |
| yadav-analysis-plan-20261030 | 37 | 9,948,692 |
| sharp-margulis-5e858e | 3 | 2,030,622 |

The [directory list](snapshot_v1/local_directories.csv) identifies individual
deposit/cache folders, sizes and accession tokens from paths. The [file list](snapshot_v1/local_files.csv)
preserves relative names and byte sizes. [Snapshot metadata](snapshot_v1/snapshot.json)
maps storage IDs to exact worktree roots/revisions and records UTC scan times.
Ninety-two distinct accession tokens occur in local paths; filenames alone do
not authenticate source identity or establish that a biological analysis used them.

Copies in different worktrees count separately. Resolved duplicate cache roots
would be deduplicated, but contents were not hashed or deduplicated. Byte counts
are not physical disk allocation. Presence is not integrity or rerun readiness.
No raw inputs were modified, moved, deleted, redownloaded or committed.

## Tracked source-reference coverage

The scan inspected **5,419 tracked text files** and all **155 registered receipts**;
the registry locates 33 questions and 37 article-local candidates. It found
**530 accession identifiers: 440 GEO series, two ArrayExpress and 88 BioProject**.
The [reference CSV](snapshot_v1/accession_references.csv) retains every matched
file path, a short example locator, registered analysis IDs/receipt links and
legacy run-record references.

- 52 identifiers occur in a registered receipt's input **path**. These include
  metadata-only inputs; they are not all expression cohorts or successful effects.
- 18 additional identifiers occur in a legacy `run_record.json` or
  `provenance.json`; occurrence alone does not prove that a matrix was consumed.
- 460 others occur only in the broader scanned text. Many are search results,
  study relations, literature leads or parent/project aliases.

These are lexical evidence classes, not scientific-use grades. A receipt may use
a generic filename that contains no accession. CELLxGENE UUIDs, Figshare/Zenodo
numbers, workbooks and reference resources are covered in the human source-use
tables, not conflated with GEO accessions. A generic number search would incorrectly
turn paper IDs and file IDs into additional datasets. Read the owning current
result/amendment to decide actual use and eligibility.

## Method and limits

[Scanner](scan_inventory.py), Python standard library, read-only inputs. The
tracked census covers `.md`, `.json`, `.py`, `.r`, `.csv`, `.tsv` files up to
2,000,000 bytes; excludes `/history/`, the legacy artifact hash baseline and this
audit itself. Of 7,771 tracked paths, 2,269 had other suffixes, 35 were excluded
history/baseline paths and 48 exceeded the size limit. Large matrices were not
opened to infer use. Saved source manifests/results and manual source-family
review supplement the lexical census; it is not an exhaustive historical-Git or
remote-deposition search.

Local inventory covers `raw_data/` in registered worktrees and conventional
`RQ_Specified/*/{cache,reference}`, `Research Article/*/{cache,reference}` and
`analysis/corrections/*/cache` roots. All files inside these roots are counted,
including ancillary or derived products; the names are not a promise of rawness.
Arbitrary `tmp/`, processed/model directories, runtimes outside these roots,
unregistered checkouts, external/cloud storage and deleted historical caches are
outside coverage. Raw-data absence from this new worktree says nothing about the
other caches. No remote availability or full content-integrity audit was run.

To create a future snapshot, use a **new output directory**; the script refuses
to overwrite an existing snapshot:

```powershell
python docs/audits/2026-11-07-public-data-inventory/scan_inventory.py --repo . --storage-repo X:/GitHub/ravel --output docs/audits/NEW-DATE-public-data-inventory/snapshot_v1
```

## Newer local work

The registered `codex/dupage-stepwise-plan-20261107` branch was inspected at
`b207aef` (nine commits beyond the same main base), under
`X:/GitHub/ravel/.worktrees/dupage-stepwise-plan-20261107`. Its own unrelated
working-tree edits were preserved. The main-based reference CSV intentionally
does not import that branch's research registry or claim merged execution.

| Source | Branch-local evidence at the pinned revision | Role and limit |
|---|---|---|
| GSE58998 / PRJNA254138 | `Research Article/gate3_09_dupage_2015/S0_RESULT.md`, `S1_RESULT.md`, `S2_RESULT.md`, `RESULTS.md` | Deposited processed FPKM; twelve libraries, eleven retained under author exclusion; HET/KO by CD62L strata, unknown mouse/pool/pairing. Not twelve independent animals or raw counts |
| GSE55773, parent GSE55753 | `Research Article/gate3_09_dupage_2015/S3_RESULT.md`, `ANALYSIS_AMENDMENT_V2.md` | Adapted Arvey chromatin-table comparison and pinned within-mm9 annotation; partial locus coverage and cross-study association |
| GSE55705 | Same S3/source review | Arvey microarray companion, not the chromatin assay |
| GSE262130, GSE262129, GSE291449 | `Research Article/gate3_09_dupage_2015/RESULTS.md`, S4 disposition | Future comparison leads; no later-study matrices pooled or new numerical run admitted |

These paths are available with `git show b207aef:"Research Article/gate3_09_dupage_2015/RESULTS.md"`
in the shared repository. Local DuPage raw-cache filenames are included in the
storage census. Integration and any subsequent research remain separate work.

## Validation and remaining work

Snapshot row uniqueness, file/directory byte-count reconciliation, accession
filename-boundary checks and exact registry receipt membership passed. All new
local links resolve. Repository validation passed **16,934 checks**; the research
gate passed against freshly re-fetched, unchanged main `dcee4b6`. Required claim,
Nb1/Nb4 archive, A16, A23 and A22/A23 extension verifiers passed. Compilation and
the unit suite passed (**167 tests, two environment/platform skips**). Whitespace
checks passed. No validator or governance rule was edited.

The first unit run failed because the sandbox's default temporary directory
denied writes/cleanup; using a writable task-owned temporary root resolved it.
The public-output restorer's attempted network route failed with sandbox DNS
and temp cleanup errors. Instead, fifteen absent published outputs were supplied
from existing local files after matching the unchanged release lock's lengths
and SHA-256 values. Fourteen frozen files needed their exact Git bytes restored
after Windows checkout line-ending conversion; normalized text matched before
restoration. The initial provenance failures resolved without changing scientific
content, hashes or receipts, or rerunning any biological script.

The update is complete locally, uncommitted on the scoped branch. No push/merge
or external-setting change occurred. Later cache changes or integration of the
DuPage work require a new dated snapshot/reconciliation; no new source acquisition
or biological analysis is required for this documentation update.
