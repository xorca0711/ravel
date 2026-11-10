# Execution and validation record

10 November 2026. Worktree `zhang-nk-plan-20261110`, branch
`codex/zhang-nk-plan-20261110`. Starting reviewed commit
`389c217341a0c4754df6729ff7f1c880856347e1`; integration base
`1a6769fc3d808ccf6b27aed3ecedc71341026f33`.

## Identity and preservation

The current CLI route was verified as `xorca0711`. Effective Git author and
committer were checked before each local freeze: `Xorca` with the existing
email independently mapped to that account in both roles on GitHub commit
`1078ce6`. No GitHub connector/browser write route was used. Public source
downloads did not use an alternate service identity. The AI-host session and
main checkout's unrelated work were preserved. No push, merge, author contact,
personal-note edit, governance change or scientific acceptance occurred.

## Runtime

An isolated ignored R 4.3.3 runtime was installed under `.tools/zhang/`.
Actual primary package versions are limma 3.58.1, edgeR 3.42.4, fgsea 1.26.0,
msigdbr 7.5.1; gene orthology uses babelgene 22.9. Full sessions accompany
each calculation. R 4.3.3 installer SHA-256 is
`f1f8c839b143571a696383de5a91a4692363a2e7a4e77ce697743bef10692ae5`.
The installed R 4.4.3 diagnostic runtime and newer dependency test library
remain ignored and were not used for the recorded numerical analyses.

Initial dependency installation encountered missing statmod/locfit and failed
source lazy loading. Missing dependencies were installed; archived msigdbr
7.5.1 was acquired as a Windows binary with a retained archive hash. Loading
cli-dependent packages caused Windows status `0xC00000FF`, including under
the newer diagnostic runtime. The package maintainer's documented
[`CLI_NO_THREAD=true` workaround](https://github.com/r-lib/cli/issues/494)
resolved clean process termination and preserved the original package versions.
It disables the progress tick thread, not a numerical algorithm or failure
check. Enrichment wrappers set it explicitly and still require exit code zero.
Both Hallmark and CP:KEGG API calls were checked. No global PATH or environment
setting was changed. Optional installer associations/shortcuts were disabled.

Only a local NGS target was registered. Saved cloud environments targeted weft;
no attached Ravel executor was available. No cloud run, new remote environment,
or service identity transfer occurred.

## Numerical verification

All five successful analysis-stage receipts verify: S0 v3, S1 v1, S2 v2,
S3 block v2 and S3 ranking v1. A sixth metadata receipt verifies byte-for-byte
failure preservation. [RESULTS](RESULTS.md) links every contract/receipt and reports
independent all-gene contrast/BH checks, 76,248 block-refit arithmetic checks
and 472 independent ES checks in each enrichment stage. Six resulting figures
were visually inspected. The near-null volcano's two small labels overlap;
its exact numerical table is linked in the figure guide.

Four failed runs remain immutable in the verified public failure archive,
including their logs and partial outputs; successors bind the original bytes
as inputs. Original copies remain in ignored raw storage, with restoration
paths in the archive manifest. Reporting fixes reuse prior numerical outputs.
All freeze commits and explicitly recorded exposure are retained. Passing a
receipt or check does not imply scientific acceptance.

## Repository delivery checks

Refreshed `origin/main` remained `1a6769fc3d808ccf6b27aed3ecedc71341026f33`;
no new remote commits appeared. Required checks completed:

- Analysis suite: 175 tests, two existing skips.
- Session suite: 25 tests passed.
- Python compilation and all 18 claim-contract numeric bindings passed.
- Nb1, Nb4, A16, A23 and A22/A23 extension archive/evidence verifiers passed.
- Every new successful receipt verifies; every local freeze author/committer
  has the verified Xorca identity.

The first delivery check found five links to a validation document mistakenly
created at repository root; it was moved into this package. Base-aware governance
also rejected 16 failed-run asset paths because input binding alone does not
authorize them as outputs. The existing metadata-preservation mechanism was
used: exact public copies and a verified receipt, with original bytes retained
in ignored storage. No validator, baseline or governance rule was changed.
After these corrections, repository validation passed **19,039 checks** and
base-aware research governance passed with no errors against the refreshed main
revision above. `git diff --check` passed. Main was fetched again at delivery
and remained unchanged. Valid test/archive results were reused; no biological
calculation was rerun for final documentation. The final delivery is local to
the scoped branch and requires owner authorization before publication or merge.

## Owner-requested publication and folder audit

The owner subsequently authorized commit, push and PR creation. The canonical
roadmap identifies this exact DOI/PMID as stable paper 11 in Gate 3B, matching
the package and the existing `gate3_07`, `gate3_08`, `gate3_09` naming convention.
The folder is retained. The roadmap's stale null folder and not-started states
are corrected to the completed article-local work; the independent D1 gate and
scientific acceptance are unchanged.

Both CLI and connector authenticate as `xorca0711`. All 13 existing publication
commits have Xorca author and committer identities with the previously verified
email; new navigation commits receive the same effective-identity check.
The changed paths are confined to the Zhang package/runs and shared progress,
article/source/registry navigation. Targeted credential-pattern/private-note
checks found no matches in the publication text. The largest new tracked file
is about 4.1 MB; raw downloads, full FASTQs and private fit notes remain local.
No frozen calculation, output, contract, validator or governance rule changed
during this naming audit. Live PR checks and final head determine remote status.

After the roadmap correction, repository validation passes **19,051 checks**
and base-aware research governance returns `ok: true`, with no errors, against
refreshed main `1a6769f`. Whitespace checks pass. The unchanged analysis/session/
archive checks above remain applicable; no biological rerun was needed.
