# DuPage execution validation

7 November 2026. **Passed against refreshed, unchanged main
`dcee4b63e11abd27fe2bbc679993b288e913565e`.** Work remains in the existing isolated
`codex/dupage-stepwise-plan-20261107` checkout; the old project-root checkout was
not edited. No push, PR, merge or external setting change occurred.

| Check | Result |
|---|---|
| `research_gate.py check --base origin/main` | Passed; registered contracts, receipts, artifacts and change provenance |
| `validate_repository.py` | **17,000 checks passed**, including local links, JSON and bound headline values |
| `unittest discover` | **167 tests, OK, 2 skipped** |
| Python compilation across analysis/article/RQ code | Passed |
| Four Dp1 receipt verifications | Passed |
| Independent numerical/source checks | S0: 277,224 exact source cells and 24-run joins; S1: 46,456 contrasts and independent PCA spectrum; S2: 11,614 interaction identities and omission extrema; S3: 4,390 domains, 5,022 edges, 1,180 gene medians and independent rank correlation |
| Visual checks | All three generated PNG figures inspected; PDF counterparts saved and tracked |
| Preservation | All 33 canonical question and guide records and 37 pre-existing article candidates preserved; all prior contracts/receipts retained; exactly four new contracts and four receipts |

The initial unit-test attempt failed because the Windows sandbox temporary
directory denied fixture writes/cleanup. Tests were rerun with `tempfile.tempdir`
set to the ignored checkout-local `raw_data/dupage_20261107/test_tmp`; all passed
with the two existing skips. No test or validator was weakened. Python compilation
and scientific runs were not repeated to resolve this environment issue.

The planning checkpoint's passing claim/archive verifiers remain applicable:
those scripts, claims and archived outputs were unchanged. New contract/registry/
documentation checks were rerun because this execution added evidence. Main was
fetched again before final checks and had no new integration changes.

The fourteen pre-existing historical files with stat/newline-related `M` status
were excluded from commits; they have no content diff. Mutable navigation text
was normalized without changing frozen contract/code/input/output bytes.

Frozen execution revisions, recorded in receipts: S0 `92ecdd7`, S1 `d89067a`,
S2 `9cc1ea4`, S3 `d66cb49`. Each run had a frozen, committed specification and
hash-matched inputs/code before execution. Stage reports document the separate
verification methods and limits. These checks establish computational consistency,
not independent biological replication, source completeness, unexposed outcomes,
scientific acceptance or enforced external branch protection.
