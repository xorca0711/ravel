# Continued qualification: verification

3 October 2026. Checked against refreshed main `76dc9b47f72e774e51502162b2f8ba9d0dc02f17`. Both prospective contracts and their hash-bound sources/tests were committed at `78845fc` before execution.

## Required repository checks

| Check | Result | Exact log SHA-256 |
|---|---|---|
| compile | Passed | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | Passed | `d2ceca74a2a8bf94d7f61a884c616647945f45753ac36c4c11c9b9eb06277a95` |
| claim_contract | Passed | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | Passed | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | Passed | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | Passed | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | Passed | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | Passed | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | Passed | `375feb23b05204c012bbca1185b634add095821d0ef6c489ad920f7ca4b95c08` |
| research_gate | Passed | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

The complete suite reports **134 tests, one existing skip** (11 new targeted tests). No old biological analysis was replayed. Targeted documentation checking resolved 280 local paths before this record was populated. Logs remain in the private handoff workspace under `qualification-validation/`.

## Execution and independent checks

- Both new receipts pass the research runner verifier and retain the frozen commit/input/code/output hashes. Registry: 24 RQs, nine Nb4 candidates, 11 contracts and 10 successful receipts. The separately archived failed A5 attempt is retained.
- Every earlier registered contract and receipt is byte-identical to integrated main; the research gate and archived evidence verifiers also passed.
- A separately written regex parser matched all 12 source sample rows, titles and individual/group labels without importing the production parser.
- A separate standard-library RK4 integration checked the five synthetic reference cases. Equations: `m'= (b-d)m`, `E2'=2(b-d)E2+(b+d)m`, `q'=b*q^2-(b+d)*q+d`, starting from `(1,1,0)`. Mean, variance-derived tolerances and extinction reference values agreed within `1e-8`; all ten observed case/seed checks passed.
- The initial private verifier failed to import SciPy before performing checks. It was replaced with standard-library RK4, without package installation or frozen-code changes. This is an environment limitation, not a failed biological analysis.
- Independent verifier SHA-256: `57eb3abe3188c1e021ab4dcbe38a025bd8778d30a01c59fcd0b6e904d50acc5b`; result SHA-256: `70549c915538530275a36409ab4f5ae0d38b2a988e2d27e0f380fb1687aa15f9`. This is numerical verification, not independent biological replication.
- New frozen Python/test paths have exact-byte Git attributes; analysis/research assets already inherit exact-byte preservation. No validator or governance requirement changed.

## Review scope and limits

The main agent reviewed endpoint/unit/stop consistency across the 24 conditional packages and nine Nb4 supplements. Fresh primary-source retrieval was targeted to Rochelle metadata and a branching-inference abstract; this is not a fresh full-text review of every precedent or independent human acceptance. Proposed A4/A17 clarifications retain the current biological holds.

The [checkout report](CHECKOUT.md) specifies hash versus file-stat preservation; raw inputs were not backed up or deleted. Public reports contain no private lab planning. Actual access, assay validation, meaningful effects and biological-fit eligibility remain unresolved as recorded in [remaining work](../REMAINING_WORK.md). GitHub checks must pass at the final PR revision; owner merge remains pending.
