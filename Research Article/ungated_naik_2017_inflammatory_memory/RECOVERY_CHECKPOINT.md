# Naik recovery checkpoint

17 November 2026. **Recovery and preservation only.** Scientific source
qualification and numerical work remain paused. This audit does not resolve the
service restriction or authorize resumption of the [analysis plan](ANALYSIS_PLAN.md).

## Verified repository state

- Checkout: `X:/GitHub/ravel/.worktrees/naik-memory-plan-20261117`;
  branch: `codex/naik-memory-plan-20261117`; upstream: `origin/main`.
- HEAD and freshly fetched `origin/main` both resolve to
  `d0429d0205fab3e079ea949d0cb0b3a0c1a4a4be` (zero commits ahead or behind).
  The GitHub CLI identity was verified in this executor as `xorca0711`.
- Before recovery edits, tracked modifications were `PROGRESS.md` and
  `Research Article/README.md`. This article directory contained five untracked
  drafts: [plan](ANALYSIS_PLAN.md), [literature context](LITERATURE_CONTEXT.md),
  [paper review](PAPER_REVIEW.md), [README](README.md), and
  [stage status](STAGE_STATUS.md). All were retained; none was committed.
- Recovery adds this file and updates only the stage status and the existing
  Naik entry in [PROGRESS](../../PROGRESS.md). The unrelated root checkout was
  not edited. No commit, push, PR, publication or account-setting change occurred.

## Saved files and integrity

The ignored `raw_data/naik2017_s01_sources/` directory contains **41 files,
6,399,880 bytes**. File reads were limited to acquisition JSON records and raw
bytes for hashing; no biological table, workbook, PDF or source-method content
was parsed during recovery.

| Saved group | Files | Verification |
|---|---:|---|
| Compressed RNA count tables | 16 | Recorded SHA-256 and byte counts match |
| Source-data workbooks, MOESM7 through MOESM17 | 11 | Recorded SHA-256 and byte counts match |
| Supplementary PDF, MOESM1 | 1 | Recorded SHA-256 and byte count match |
| GEO, SRA, ENA, BioSample and paper/correction snapshots | 8 | Recorded SHA-256 and byte counts match |
| Acquisition JSON records | 2 | Retained; current hashes below |
| Existing `private_review/` PDF-derived files | 3 | Retained; not listed in either acquisition record |

All 5 records in the local `acquisition_initial.json` and all 31 records in
`acquisition_followup.json` match. There are 36 unique recorded paths, no missing files, hash/size
mismatches, duplicate paths or unhashed acquisition entries. All records contain
HTTP status 200; this audit does not verify remote contents or establish that a
saved response contains the intended scientific source.

The following hashes were computed **at recovery**, not supplied retroactively
as acquisition or generation provenance. Paths are relative to the ignored
source directory.

| File | Bytes | SHA-256 at recovery |
|---|---:|---|
| `acquisition_initial.json` | 2,468 | `d784de3461f8093f88b701fb325c67dd47ceeb0fcec0d4d14fd172af7d4415d8` |
| `acquisition_followup.json` | 23,403 | `ff3106a0969aea32081a6936aa576ef950cfb8cc9f1dfcc656ee392baa9bdfa9` |
| `private_review/final_pdf_fitz_text.txt` | 105,809 | `96aca458077196106c3c0c36b7c269017b4a8500092c14e2c8bacdd59d45246f` |
| `private_review/final_pdf_page4.png` | 406,407 | `6e28d7bc710e737f835599b1a82a5f557e1005388ea2dca1c0aca9f0b90c14cb` |
| `private_review/final_pdf_text.txt` | 103,870 | `9a550ba1e627730173678566712e35edab7c5a345c67dfc85dcefa5f77a2937d` |

These five hashes identify the current saved bytes. No prior independent hashes
were available for these files in the acquisition records. The origin and
generation history of the three derived files remain unverified by this audit.
Saved-byte agreement does not qualify biological units, source identity or
analysis eligibility. Ignored files remain local and outside Git preservation.

## Execution artifacts and unfinished work

The [research registry](../../analysis/research/registry.json) has no matching
owner/candidate, contract, receipt or evidence reference for `Naik`,
`nature24271`, `GSE92967` or `PMC5808576`. Targeted identifier searches of
`analysis/research/`, `analysis/scripts/` and this article's code/configuration
files, including ignored files in those locations, found no matching artifacts.
Before recovery edits, a checkout filename search excluding raw inputs and
runtime directories found only the five existing article drafts. No Naik script, contract, receipt or
result was found within those audited scopes; this is not a claim about files
outside this checkout or artifacts stored under unrelated identifiers. The
article package is untracked and the branch has no commits beyond main.

The [stage record](STAGE_STATUS.md) remains authoritative for unfinished work:
S0 has a draft reading map, S1 source/unit qualification is incomplete, S2-S5
have not run, and S6 has not been reached. The existing plan still requires
claim-to-source links, pool/preparation/run and assay relationships, repeated
measurement structure, the scoped read-layout discrepancy, and cross-assay
pairing to be qualified. None of those questions was investigated here. No
completed scientific stage, numerical result, accepted claim or conclusion about
the availability/value of further extensions is claimed.

## Preserved service restriction and next decision

The originating handoff reports three failed turns in technical chat
`01a1e9ce-1f7f-74e2-b3e1-bff403b13a12`, each returning:

> Invalid prompt: we've limited access to this content for safety reasons.

The latest turn, `01a1e9e3-208c-7551-b31c-65c6d82747c0`, briefly resumed on the
owner's `proceed` request and failed at `2026-11-17T14:24:11Z`
(23:24:11 KST on 17 November). The handoff describes the last successful command
as source-text snippet and workbook-sheet-name inspection, not an effect or
endpoint calculation. These execution-history facts are retained from the
handoff and existing stage record; the underlying chat/tool trace was not
independently re-read or replayed in this audit. Earlier failure times and a
specific cause of the restriction remain unverified.

This chat performed only the recovery audit. No restricted scientific action
was retried or repackaged, and no safeguards changed. The originating chat reviewed
this report, its stated audit boundaries, current worktree status and the
interrupted chat record on 17 November. No recovery revision was required; this
review does not supply scientific source qualification or claim acceptance.
A supported resolution of the service restriction is still
required before blocked scientific work can resume; any later execution also
retains the existing source-qualification and contract requirements. Recovery
stops here. No scientific tests or broad portfolio audits were rerun.

## Recovery validation

The three affected documentation scopes (this file, stage status and the Naik
PROGRESS entry) passed local-link, whitespace and conflict-marker checks:
18 local links resolved. The tracked-document Git whitespace check also passed.
A before/after SHA-256 comparison confirmed that all 41 saved input/record/derived
files and 10 protected documentation/registry files were unchanged. The protected
set includes the analysis plan, literature context, paper review, article README,
article index, AGENTS, AI_CONTEXT, research governance, question register and
research registry. Prior plan-stage test reports were retained as historical
reports, not rerun or represented as fresh scientific validation.
