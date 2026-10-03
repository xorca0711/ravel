# Conditional-package validation

3 October 2026. Documentation continuation from
`a0c8189e361306e6d08c4f927b2a7365f8f95f6c`, checked against refreshed
`origin/main` at `0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`.
All changes in this continuation are Markdown. Final GitHub status belongs to
the pushed revision and must be read there; these are local verification facts.

## Required checks

Commands follow repository-checks.yml and research-governance.yml.
No biological pipeline was replayed. The complete unit suite includes the
research-governance tests, so that subset was not run redundantly.

| Check | Result | Exact log SHA-256 |
|---|---|---|
| compile | Passed | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | Passed | `6cd6f11b1712c424fc8444d500c12582b02e4366ba93324bce885fab0fc2b838` |
| claim_contract | Passed | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | Passed | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | Passed | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | Passed | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | Passed | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | Passed | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | Passed | `c9169f8b74636cccf930b67b95644b7a2a9c41b21fa4a108ab5ff7bd6855c6cc` |
| research_gate | Passed | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

The unit suite reports **123 tests, one existing skip**. Private logs retain
the exact outputs; hashes above identify them. Research gate used
`check --base origin/main`, which also performs current contract/historical
integrity validation.

## Mechanical preservation and documentation review

- 59 Markdown paths changed: 29 new package-stage files and 30 existing files.
- Every existing changed file retains its entire pre-continuation content as
  a prefix; continuation sections are appended. No existing line is removed.
- The targeted audit resolved 391 local reference paths across packages and
  dossiers, found 24 A-package files and exactly nine Nb4-P01–P09 sections.
  Required hypothesis/evidence/unit/outcome/control/stop/precision fields
  were checked for presence; field presence alone is not scientific validity.
- Staged whitespace checking passed. Scope review found no code, configuration,
  registry, contract, receipt, claim-grade or governance modification.
- New public package files contain no private local-planning paths or Notion
  profile links. Original PDFs and private planning were not modified.
- The newly downloaded support workbook's SHA-256 was unchanged after read-only
  sheet/header inspection. No effect calculation, model fit or significance
  test was performed on it.

## Scientific consistency review and limits

The authoring agent checked the packages against current dossiers, amended
results, source audits and the stated handoff boundaries. This is self-review,
not independent scientific review or human acceptance.

Targeted corrections made during drafting: A11 now proposes one patient-held-out
log-loss increment rather than interchangeable primary estimands; A21 requires
division evidence and retained gCap identity rather than equating later counts
with renewal. A0 remains stopped. A14 keeps history and fibroblast reception
separate; A19 keeps mature output and reserve; A20 keeps the total Fzd2/Fzd1
contrast and does not adjust away its proposed early-pool mediator. A13 has
no invented output/mediator; A16/A22/A23 retain their adverse or unresolved evidence.

Nearest-source comparisons are bounded, with access/coverage documented in
SOURCES.md. Missing measurement choices are explicit evidence-decision packages,
not pretend complete bench protocols. Owner scientific review, actual resource
access, assay validity and meaningful-effect/precision justification remain open.

## Write-safety handling

Automatic approval review rejected two proposed broad documentation rewrites:
first potential truncation of dossier tails, then replacement of PROGRESS.
Those commands did not execute. The implemented alternative appends all
existing-document updates; direct prefix checks confirm preservation.
No permission-dependent work remains blocked by those rejections.

## Integration and external settings

The final pre-validation fetch found main and PR130 unchanged at the revisions
above. No normal/repair checkout, old worktree or ignored dataset was modified.
This continuation uses a separate worktree/branch and is intended as a
fast-forward addition to PR130; the owner retains merge. No branch-protection
setting was changed or independently reverified this session.
