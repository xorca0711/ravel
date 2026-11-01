# Recovery validation and local handoff

31 October 2026 (Asia/Seoul). Starting revision:
`c60848a43e32640b6921ab2f7c42ba801b5cec14`. Fetched integration base:
`4df267d3f5035b249df2e587c70a8b9e9253b049` (`origin/main`).

- Worktree: `C:/Users/dream/.codex/worktrees/saxton-metadata-recovery-20261031/ravel`
- Branch: `codex/saxton-metadata-recovery-20261031`
- Original technical source: `C:/Users/dream/.codex/worktrees/saxton-il22-execution-20261031/ravel`
- Preserving review source: `C:/Users/dream/.codex/worktrees/macrophage-memory-review-20261029/ravel`
- Interpreter: Python 3.12.10 ARM64. Git author remains `Xorca`; no account-dependent external write was made.

The primary checkout's unrelated modified PROGRESS and all other worktrees/caches
were left intact. The managed checkout began clean at the requested revision.
Only three declared, hash-verified raw inputs were copied here by exclusive
creation. Original source/result bytes were read, not rewritten. No old chat
history was loaded and no replacement chat or subagent was created.

## Preservation correction

The originating reviewer found four base-aware gate hash failures inherited from
`ff09fab`: its root `.gitattributes` additions changed a file bound in both Weft
metadata/figure1 contracts and their receipts. Independently inspected the diff
and those bindings, then restored root `.gitattributes` directly from main
`4df267d` using Git blob bytes. Restored SHA-256:
`7d8c3f661fc051fd893696c376480870de6498ac49ea8937427735572f097614`.

The Saxton source rule now lives in this article's `.gitattributes`. The existing
root `analysis/research/** -text whitespace=cr-at-eol` already covers its run
files, so no file was added inside the frozen eight-file run directory.
`git check-attr text` confirms `unset` for script, test, contract and receipt.
No Weft contract, receipt, validator or analysis design was edited. The parent
review of this scoped correction remains separate from passing mechanical checks.

## Targeted checks already completed

| Command / check | Result |
|---|---|
| `python <TEMP>/sx22_independent_review.py` | PASS: eight run files byte-equal across all three checkouts; three input hashes in both sources/new copy; two code and five output hashes; full matrix/metadata/QC checks in [R1_REVIEW](R1_REVIEW.md) |
| `python analysis/scripts/research_gate.py verify analysis/research/runs/sx22_r1_v2/receipt.json` | PASS |
| `python analysis/scripts/research_gate.py preflight "Research Article/gate3_08_saxton_2021_il22/config/r1_contract_v2.json" --inputs` | PASS; no runner invocation |
| `python -m unittest discover -s "Research Article/gate3_08_saxton_2021_il22/tests" -q` | 3 tests PASS |
| `python analysis/scripts/restore_published_outputs.py` | PASS: 16 locked members verified, 15 restored; byte restoration only, no analysis rerun |
| Supplied PDF SHA-256 and Poppler renders | PASS: pp. 6–11 visually inspected; methods pp. 22–23 text-checked; [source correction](SOURCE_CORRECTION_2026-10-31.md) |

The temporary independent checker's local path is
`C:/Users/dream/AppData/Local/Temp/sx22_independent_review.py`; it is a session-local
review aid, not a new scientific run or frozen repository entrypoint. Its method,
hash and findings are recorded in R1_REVIEW. Published-output restoration is the
unchanged CI prerequisite and does not add a new Choi analysis.

## Required repository checks

All required check families passed against freshly fetched main `4df267d`.
The base-aware gate includes the ordinary contract/historical-integrity checks;
the full unit suite includes the governance tests, so neither was duplicated.
No scientific rerun is part of these checks.

| Exact command / check | Outcome |
|---|---|
| `python analysis/scripts/validate_repository.py` | 12,630 checks PASS |
| `python analysis/scripts/research_gate.py check --base origin/main` | PASS, zero errors; inherited root-attribute failures resolved |
| `python -m unittest discover -s analysis/tests -q` | 158 tests, PASS; two host symlink-privilege skips (Linux CI exercises these) |
| `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified` | PASS |
| `python analysis/scripts/claim_contract.py --check` | 18 numeric bindings PASS |
| `python "Research Article/gate1_03_nabhan_2018/nb1/verify_outputs.py"` | PASS, 17 output hashes plus archived provenance/units |
| `python "Research Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/scripts/verify_archive.py"` | PASS, package and archive; 20 run records / 164 output hashes |
| `python RQ_Specified/A16_cd177_state_attribution/scripts/verify_stage1_evidence.py` | PASS, 1,867 archive/table checks; verifier's raw-input/biological limitations retained |
| `python RQ_Specified/A23_slc34a2_transition_homeostasis/scripts/08_verify_external_current.py` | PASS |
| `python analysis/scripts/verify_a22_a23_extensions.py` | PASS, tracked inputs only |
| `git diff --cached --check` | PASS for the scoped recovery changes |
| Direct Git-blob preservation comparison against `c60848a` | PASS: all preexisting Saxton files, eight run files and historical README tail unchanged |
| Direct Git-blob source comparison at receipt execution commit `ff09fab` | PASS: contract and both code blobs match original receipt hashes |
| Root attribute working/staged bytes versus `4df267d` | Exact match; historical SHA-256 restored |
| Parsed registry comparison against `c60848a` | Only two Sx22-P01 evidence links added; canonical questions, contracts, receipts and governance registrations unchanged |

The final integration-base fetch still resolves to
`4df267d3f5035b249df2e587c70a8b9e9253b049`; no newer main changes needed integration.
The scoped commit is returned in the chat handoff (a commit cannot contain its
own final hash). Final status/whitespace inspection follows staging of this
validation text; unchanged scientific checks are not rerun for prose alone.

## Tool failures and remaining boundaries

Initial sandbox Git operations could not access the managed worktree/index and
fetch could not write FETCH_HEAD; scoped approved execution resolved those tool
permissions. They are distinct from the original biological-content restriction.
`pdftotext` was unavailable; Poppler rendered successfully and pypdf supplied the
limited methods text check. One overlong Windows document-writing command failed
before process creation; smaller patches completed the files without partial
scientific output. Original R1 v1 failures remain in [AMENDMENTS](AMENDMENTS.md).

Next action is independent review by the originating chat. R2/R3 and other
numerical extensions remain as dispositioned in [COMPLETION_LEDGER](COMPLETION_LEDGER.md).
No external settings changed; no push, PR, main merge, author contact, Notion edit
or bench activity occurred. Scientific acceptance remains unassessed.
