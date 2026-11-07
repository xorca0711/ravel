# Source inventory and documentation reconciliation v2

7 November 2026. Current integration base: `32ab85e87bee788e62bec4e1b7ce5bad6df84d30`.
[PR #167](https://github.com/xorca0711/ravel/pull/167) merged at 19:59 KST; its
published head passed both GitHub workflows. The source-inventory branch
integrates that base at `4d6f96c`, preserving both progress records. The owner
then requested publication and documentation/navigation cleanup in this PR.

## Current source-use and storage records

[Central inventory](../../DATASETS.md) · [source-use additions](../../DATASET_UPDATES_2026-11-07.md)
· [accession references](snapshot_v2/accession_references.csv)
· [local directories](snapshot_v2/local_directories.csv)
· [local files](snapshot_v2/local_files.csv) · [snapshot metadata](snapshot_v2/snapshot.json).

The [initial v1 audit](README.md) and its CSV/JSON files remain historical.
V2 supersedes v1 for current integration/use status and local file presence.
DuPage's GSE58998 and Arvey GSE55773 are now merged evidence. The later
**GSE262130** candidate follow-up executed after the earlier screen and uses an
author-selected rlog matrix. It is no longer classified as a future lead.
GSE262129/GSE291449 remain leads. The stated TIGIT ArrayExpress identifier has
a recorded identity conflict; that single-cell dataset was not analyzed.

| Census | Current snapshot v2 |
|---|---:|
| Tracked paths considered | 7,908 |
| Text files scanned | 5,501 |
| Registered receipts inspected | 163 |
| Accession identifiers referenced | 544: 451 GEO, 4 ArrayExpress, 89 BioProject |
| Identifiers in registered receipt input paths | 55 |
| Additional identifiers in legacy run/provenance records | 18 |
| Reference-only identifiers | 471 |
| Local cache roots / worktrees containing inventoried files | 15 / 10 |
| Local files / apparent bytes | 4,197 / 74,042,250,114 (74.04 GB; 68.96 GiB) |
| Root `raw_data/` | 955 files / 34,520,206,615 bytes / 33 first-level folders |
| Distinct accession tokens in local paths | 94 |

The local change from v1 is sixteen additional files in the DuPage worktree's
cache, totaling 2,856,089 bytes. This audit inventories their presence; it does
not independently validate their scientific contents. The project-root raw
inventory is unchanged. Copies, metadata, archives and derived cache products
count separately; these are not counts of unique datasets or independent samples.

The [scanner](scan_inventory.py) records its SHA-256, integration base, checkout
revision and working-tree status. V2 includes edited navigation/source documents
on the integrated branch; it is not asserted to be an untouched main checkout.
The scan excludes inventory-audit directories to avoid citing its own generated
tables as evidence. Other exclusions: 2,312 non-text paths, 41 history/baseline/
inventory paths and 54 text files above 2 MB. No traversal failures or skipped
nested links were reported. The initial audit's scope limits still apply:
conventional source/reference cache roots only, no full content hashing, no
remote availability refresh, no cloud/arbitrary temporary-storage census.

## Documentation hygiene and link ownership

| Finding | Correction |
|---|---|
| Root README described the historical remaining-work ledger as current dependencies | Current work routes to project state and owning question/article reports; the older ledger is explicitly historical |
| Central data list omitted later source families and local inventory context | Twenty-one grouped numerical/source-reconstruction entries plus qualification/reference roles; current CSV links and separate source/use/presence counts |
| Documentation index said 18 paper packages | Corrected to 19, with a compact current entry table and a separate dated-review section |
| Structure guide said 37 article-local candidates | Corrected to 38; 33 canonical questions, 35 RQ directories and 21 article directories remain distinct from paper/question counts |
| September roadmap routed current work through October historical packages | Direct current owner routes; dated priorities and checkpoints retained |
| Next-dataset gate called a September ledger current | Historical label plus current question route; original design/gates retained |
| Article index presented the October queue and original gate rules without enough temporal context | Clarified dated queue/rules versus continuing reading permissions and owner-specific execution; existing S1/D1 gates unchanged |
| DuPage roadmap omitted the executed candidate follow-up | README and ROADMAP.json synchronized for GSE55773/GSE262130, current result and limits; reading order and all other paper records preserved |
| Documentation index claimed no PDFs were tracked and gave inconsistent license counts | Distinguished ignored source papers from generated figure PDFs; removed unsupported counts |
| A representative portfolio summary could be read as complete coverage | Linked the complete current question/article indexes, without rewriting its scientific findings |

Physical evidence layout and historical paths are unchanged. The topic map already
included DuPage and 19 packages on main, so it was reused. All question identities,
owner hypotheses, registered illustrations, result tables, article galleries,
reading permissions and research-governance rules remain unchanged. The root
README's measured-figure panel is preserved. Source-specific roadmap status
metadata is updated from already merged evidence; this is not a new analysis.

## Validation and publication

The integrated revision passed:

- [772 focused navigation, count and preservation checks](navigation_checks.json).
- 17,230 repository validation checks.
- 167 unit tests (two environment/platform skips), with a writable temporary directory.
- Python compilation and net PR whitespace checks.
- The unchanged base-aware research provenance gate against main `32ab85e`.

The gate caught an inventory-pointer comment edit in `.gitignore`, which is a
hash-bound input to an older run. It was restored exactly; the new inventory
guidance remains in the documentation. Seven newly merged DuPage scripts needed
their original Git bytes restored locally after Windows line-ending conversion.
Neither frozen inputs nor validators change in the PR. The initial checkpoint's
archive/claim checks remain valid for preserved evidence. No biological analyses
were rerun and no source files were downloaded.

GitHub connector and CLI identities were verified as `xorca0711`. Publication is
pending; this request authorizes opening the PR, not merging it. The PR link and
remote checks will be recorded in the handoff.
