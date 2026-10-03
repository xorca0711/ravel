# Source-mapping closeout: verification

3 October 2026. Documentation/source-inspection continuation from PR #132 head `7ccdd6f06f8134ce1e3473364805f8ee05e17b98`, checked against fetched main `76dc9b47f72e774e51502162b2f8ba9d0dc02f17`. No frozen biological analysis was replayed.

## Required checks

| Check | Result | Exact log SHA-256 |
|---|---|---|
| compile | Passed | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | Passed | `78292872a9c22f91407ecf294c5029f955729d63b88eff24bcba1897191037cd` |
| claim_contract | Passed | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | Passed | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | Passed | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | Passed | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | Passed | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | Passed | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | Passed | `73b74d08e9015703c37dd1a04bea59839607fff4ff907560e13c42a45d5d4f14` |
| research_gate | Passed | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

Full suite: **134 tests, one existing skip**. Targeted documentation validation resolved 187 local paths before this record was populated. The private log directory is `mapping-closeout-validation/`; GitHub checks must pass at the final PR revision.

## Preservation and source inspection

- All earlier registered contracts/receipts are byte-identical to the preceding PR head. The registry change adds only the closeout reference to 13 relevant RQs; scientific IDs, code, configurations, outputs and claim grades are unchanged.
- Recomputed lengths and SHA-256 values for all **260 retained HTTP fragments** from the two HDF5 inspections. Their exact inspected root attributes and source-record hashes are in [SOURCES.md](SOURCES.md). These checks establish fragment preservation, not a whole-matrix hash or independent biological replication.
- The file inspection enumerated HDF5 metadata and read eight barcode strings per file; it did not decode expression-array values, build a full per-cell mapping or produce biological statistics. Neighboring bytes in retained HTTP blocks were not interpreted.
- Changed paths are the current documentation/decision log, a registry reference update and the three closeout documents. The normal checkout, unrelated local metadata changes, raw inputs, private settings and older worktrees were not modified. No raw-data backup is claimed.
- Scope review confirms all 13 dependency rows retain their scientific holds; the owner-deferred A17 technical work is explicitly unfinished. No governance, validator, eligibility threshold or claim was weakened.
- No private lab-planning paths or placement dates were copied into public closeout documents. The private handoff retains the placement context and lab-comparison path.

## Completion limit

This verifies the bounded repository-grounding/source-recovery checkpoint. Scientific review, new evidence, later analytical implementation and actual laboratory qualification remain distinct. Owner merge and scientific acceptance are not fabricated. See [current remaining work](../REMAINING_WORK.md).
