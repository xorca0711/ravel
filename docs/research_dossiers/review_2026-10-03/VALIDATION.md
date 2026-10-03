# Validation of the scientific grounding review

All ten required local checks passed on the reviewed working tree, based on repair revision `48b0631d4e9194a21e615f8caf5761293db0b670`. Remote main was fetched again before delivery and remained `0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`. No biological fit or raw-input rerun was performed.

| Check | Result |
|---|---|
| Python compilation | Passed |
| Full analysis unit suite | 104 tests run; passed with one existing skip |
| Claim contract | Passed; no claim-grade change |
| Nb1, Nb4, A16, A23 and A22/A23 extension verifiers | All five passed |
| Repository validator | Passed |
| Research gate against current main | Passed; frozen historical scientific assets preserved |
| Review-specific documentation check | 140 local targets/anchors; 24 RQs, 20 source entries and nine Nb4 candidates passed |

The required commands are defined in the repository workflows. The following SHA-256 values identify the local logs retained outside tracked research evidence; they are execution provenance, not independent scientific validation.

| Local check log | SHA-256 |
|---|---|
| compile | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | `bc8706204272626933b0b31bfaac21e6402c90d3752488774d8b34554250dea1` |
| claim_contract | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | `d50b399d09788e79431e35d4960eaf5815b83320c1efc8dca323245a525d9893` |
| research_gate | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

The one-off document check resolves relative links and heading anchors and checks full portfolio coverage. Semantic review additionally corrected the six scope/provenance issues listed in the review overview. Mechanical checks cannot certify novelty or causal identification.

GitHub integration checks should be read at the current head of [draft PR #130](https://github.com/xorca0711/scRNA_seq/pull/130); the prior repair's passing CI is not proof that a later head passed. Main remains protected by `validate` and `research-governance`; this stage does not modify protection or governance enforcement.
