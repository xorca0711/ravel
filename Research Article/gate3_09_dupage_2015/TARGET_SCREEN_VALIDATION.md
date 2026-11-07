# Target-screen and portfolio validation

## Cross-platform preservation correction — PR #167

The first Linux CI run passed repository validation but failed the research gate:
Git had normalized three new contract files from CRLF to LF. Their working-copy
bytes still matched the frozen receipt hashes. Exact-path `.gitattributes`
entries now preserve those original CRLF bytes in Git on every platform. JSON
content, execution receipts, scripts and numerical outputs are unchanged; the
gate remains strict. Historical freeze commits are not rewritten. This is a
byte-preservation correction, not a rerun or a claim that the initial CI passed.
The PR's later CI run supplies the cross-platform verification.

## Original local checks

7 November 2026, isolated `codex/dupage-stepwise-plan-20261107` checkout.
Integration base fetched again: `dcee4b63e11abd27fe2bbc679993b288e913565e`, unchanged.

| Check | Evidence / status |
|---|---|
| Contract preflight | Passed for screen v1, annotation v2 and figure v1 with hash-matched inputs |
| Frozen execution | Screen v1 at `2fecf66`; annotation v2 at `a9aa0d0`; figure v1 at `6c4ad83` |
| Receipts | All three verified after execution |
| Independent arithmetic | Standard-library `math.log2`/`statistics.fmean` recomputation of all 11,614 genes in all 14 configurations reconciled primary low/I, extrema and sign-oriented minima to tolerance 1e−11 |
| Annotation and selection | Independent NCBI exact-symbol/chromosome/type qualification reconciled every gene; all v1 numeric fields unchanged in v2; all four coding-frontier selections reconciled |
| Figure values | All 42 displayed source rows exactly match the frozen table (32 frontier plus 10 focused rows) |
| Figure exports | Four 300-dpi PNGs visually inspected; four searchable one-page PDFs and four parseable SVGs checked |
| Repository validator | Passed: 17,058 checks, including final staged portfolio coverage |
| Research gate against refreshed main | Passed: `research_gate.py check --base origin/main` |
| Preservation | All prior canonical question/guide records, article IDs, contracts and receipts retained; original S0–S3 outputs unchanged; exactly three contracts and three receipts added |

The annotation amendment initially supplied an analysis ID where the gate
requires a predecessor file path. Preflight rejected it; the path was corrected
before freezing or executing v2. An interim full gate overlapped execution of
v1 and found its not-yet-registered receipt/assets; these were then registered.
No validator or scientific threshold was weakened to resolve either issue.

Final validation was repeated only where the new staged exports extended file
coverage. No scientific calculation was rerun for documentation or staging.

The original S0–S3 analyses, tests, frozen outputs and source contracts were not
rerun or modified. Existing infrastructure tests remain applicable; the new
scientific scripts were exercised through the gated runs and full independent
numeric/annotation verification. Public annotation is pinned and retained in
ignored raw data; primary-source access limits are documented in the literature
context. No external account-dependent write occurred.

These checks establish internal reproducibility, not independent biological
replication, source completeness, novelty, human acceptance or laboratory readiness.
