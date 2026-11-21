# Follow-up validation — 10 November 2026

Integration base: refreshed main
`6b7f9a0eecfdf7e46efb0305e0efcd4b9b2b9ad6` (PR #175).
Delivery branch: `codex/navarro-gallery-wording-20261110`.
The [results report](README.md) owns interpretation and links all three receipts.

## Scientific and documentation verification

- All three new receipts passed hash verification. Source qualification and
  residual diagnostics were frozen at `557eb98`; the qualified human description
  was frozen at `8b6aef4` before execution. Published human selectivity results
  were already exposed and are recorded as a premise.
- The residual audit verified all 40 affected observations against raw workbook
  XML. Both P-value discrepancies remain unresolved; the 38/40 reconciliation
  total and all original numerical evidence are preserved.
- Human matrix qualification verified all 108 explicit sample/library joins,
  nonnegative integer counts, complete treatment strata and unique marker IDs.
  The description passed 1,368 arithmetic checks and retained every prespecified
  sample, marker, time and contrast. These checks are not biological replication.
- Both new PNG figures were visually inspected. A separate documentation check
  matched all six displayed T-cell rows against frozen summary tables and
  resolved all ten gallery images.

## Required repository checks

All passed against the integration base above:

| Check | Result |
|---|---|
| Python compilation of analysis, articles and RQ workspaces | Pass |
| Full unit suite | 175 tests, two existing skips |
| Claim contract | Pass |
| Nb1 and Nb4 archived outputs | Pass |
| A16 and A23 current evidence | Pass |
| A22–A23 extensions | Pass |
| Repository paths, links and data checks | Pass |
| Base-aware research governance | Pass; no errors |

The local Windows test runner used a writable temporary directory. Tests and
validators were not changed. Remote push- and PR-triggered workflows must both
pass on the final published revision; the PR's checks own their live status.

The optional Git whitespace check reports trailing spaces in generated path
lines of the two new Matplotlib SVGs only. Their receipt-bound bytes are retained;
no validator or whitespace configuration was changed to suppress these findings.

## Preservation and remaining work

Original frozen Navarro code, contracts, source values, outputs and failed runs
retain their paths and bytes. New work uses a dated follow-up directory and new
run IDs. Raw public matrices, SOFT files and source snapshots remain ignored;
the [source-access record](SOURCE_ACCESS.md) and manifests retain their provenance.
Unrelated checkout changes are excluded from delivery.

GitHub CLI and connector identities were verified as `xorca0711`; both new
freeze commits use Xorca author and committer identities with the verified
account email. All newly introduced commits are audited again before publishing.
Historical commits are preserved.

No source P value, dose/alias ambiguity or missing biological replicate was
invented away. The [remaining holds](README.md#5-verification-access-record-and-remaining-decisions)
specify the source corrections or study designs needed for further work. Owner
review remains distinct from successful execution, with no new claim grade or
human scientific acceptance recorded.
