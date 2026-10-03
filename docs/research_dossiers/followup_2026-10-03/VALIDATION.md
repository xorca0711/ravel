# Follow-up validation

All ten required local checks passed against fetched integration base
`0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`. Main was fetched again after the checks;
its revision was unchanged. The checks cover the current scientific/code changes;
the subsequently written status and validation prose records their results.

| Check | Result | Local log SHA-256 |
|---|---|---|
| compile | Passed | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | Passed | `c8dbb8efa688a528a7836fc4cf9e9948e88bf58dc80fdd7c0d866bcfdf5a4b59` |
| claim_contract | Passed | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | Passed | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | Passed | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | Passed | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | Passed | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | Passed | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | Passed | `70f2445eab23d7d38112a073106e60e86d4af33d035e0835aff77fa3c38eff97` |
| research_gate | Passed | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

The suite ran **123 tests, with one existing skip**. Thirteen new adversarial
tests cover missing/duplicate/contradictory BioSample identities and the A5 alias
scheme. The 3,401 frozen historical scientific assets and all previous contracts
and receipts passed the integrity gate. No biological analysis was rerun.

The documentation check covered 197 local paths, all 24 novelty-ledger rows,
nine Nb4 candidates, nine frozen contracts and eight successful registered
receipts. One failed A5 attempt is separately archived, never reported as a
successful receipt. Source and access limits remain explicit.

## Metadata verification

A separate verification implementation recalculated every input/code/output
SHA-256 and joined the output rows directly against the SOFT and XML records.
All 984 matched rows passed: A2 18, A5 56, A7 20, A22 890. For A5, every MUC alias
matches its GEO title prefix and absent reverse GEO links remain absent. For the
other sources, every reverse GEO ID and title agrees. Every biological-unit count
remains null. This is mechanical verification by the same agent, not independent
scientific review or biological replication. Immutable receipt verification
fields remain unchanged; this document records the later verification.

The first A5 run stopped before producing an inventory. Its original receipt
and log hashes remain in [the failure archive](A5_FAILED_RUN.md). The amendment
was frozen before execution and does not relax source-unit eligibility.

## Checkout and integration

The [checkout report](CHECKOUT.md) records the original 686-file archive match,
local-only recovery commit, unchanged main, private settings and ignored-file
verification. The normal checkout is handed the final PR revision on
`codex/workspace-ready`; old worktrees remain retained. New metadata inputs are
copied with exact-hash checks into ignored raw_data for replay from that checkout.

A real Windows checkout exposed CRLF conversion of hash-bound metadata code.
Exact-byte attributes now cover the six bound script/test paths. No frozen code
logic, contract hash or result was rewritten. The handoff verifies all code/input/
output hashes in the normal checkout and preserves any unrelated local files.

Final GitHub checks must be read at the PR's actual head. The owner merges the PR;
passing tests and agent review do not record human scientific acceptance.

The consolidated Windows checkout passed the research gate. All 18 copied
metadata inputs, six bound code files and eight successful receipt outputs
matched their recorded hashes; all 62,350 original ignored files and private
settings remained unchanged. Both push and PR CI checks passed at `b2fd4ca`.
A final exact-byte check then found Git newline normalization in the separately
archived failed receipt. Its own exact-byte attribute restores the original
receipt bytes and SHA-256; this does not change its failed status or any result.
The final PR checks cover that archival correction as well.
