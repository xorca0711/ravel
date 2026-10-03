# Qualification verification

The four runs executed only after their contracts and code were committed at `6ef2cf9d3017722297d3b5f4a3f5cbb8e1d9cee1`. Input, code and output hashes were independently rechecked. The source-block verification used a separate regular-expression split of the original SOFT records and compared exact accession/title pairs against the generated tables, without importing the production parser. This is mechanical verification, not independent biological replication.

- GSE169125: 18 source IDs and titles match independently split SOFT blocks; no biological-unit inference.
- GSE303646: 56 source IDs and titles match independently split SOFT blocks; no biological-unit inference.
- GSE247130: 12 source IDs and titles match independently split SOFT blocks; no biological-unit inference.
- GSE310539: 8 source IDs and titles match independently split SOFT blocks; no biological-unit inference.
- GSE307351: 890 source IDs and titles match independently split SOFT blocks; no biological-unit inference.
- MesSTIM: nine named population/input groups each contain two deposited records; numeric suffixes are not interpreted as animal IDs.
- A5: all 56 deposited IDs/titles exactly match the preserved 28 September library crosswalk; this is source consistency, not a new replication cohort.
- A7: CEBPA source has six RNA and six ATAC records; AP-1 source has four of each. Assay totals are not biological replication.
- Nb3: 890 parent records partition into 886 screen and four spatial records; mixed-species annotations are not additional donors.

All four receipts retain `scientific_acceptance: not_assessed` and their original execution records. Verification is recorded here without rewriting frozen receipts. The input snapshots are ignored local source files with recoverable public URLs and hashes in SOURCES.md. Five synthetic parser tests cover missing/duplicate membership, paired assays and superseries nesting; a runner regression checks portable commands without machine paths. The targeted pre-freeze suites passed (five parser tests and 26 governance tests).

All ten repository-required local checks passed after the qualification reports and receipt registrations were written. No expression analysis or wet experiment forms part of these checks.


## Final local verification

- Full unit suite: 110 tests run, passed with one existing skip.
- Compilation, claim-contract consistency, Nb1/Nb4/A16/A23 and extension evidence verifiers, repository validation and the research gate against current main: passed.
- Qualification documentation: 174 local paths, all 24 question rows, nine Nb4 candidates and four registered contract/receipt pairs checked.
- Remote main was fetched before delivery and remained `0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`.
- Frozen historical scientific assets, prior contracts, claim grades and original checkouts were preserved.

| Check log | SHA-256 |
|---|---|
| compile | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| unit_tests | `a2e74a49bec796346413a845eced94dc2d82b3f402dfe3b479dd0ae9e23d0184` |
| claim_contract | `e7e5f0ebd3bf271a341d901717c00c42f4e1d9796f60ed75b73748bb28f9508d` |
| nb1_evidence | `d03213acc17a89d450846ff26196a2b759ba885d32a647ef10c7a81c8fdc7bd9` |
| nb4_archive | `7aba818f40898d07fce2ccf100424282519761b37fede97991cc01a26b8652a0` |
| a16_evidence | `a30ed2397f3f61825e0976c22b69d8d19393890fa5fde7ef8ce4f9aae115f838` |
| a23_external | `72a202c7e329e0e49c9b26da0c16d5173fb5d1a1a6bfb4122bee0ec3393da34f` |
| a22_a23_extensions | `9820d60ceaff0991a8b3467599c534cfb6afa68ac8d87c1aa7a9fbeef284b85e` |
| repository | `f8b47007faaf4e1694e2db0755ef4f38d615204c52dc42ca36401d6bda47e7d3` |
| research_gate | `ab495baa1e177b79bdf7250b934a2d5a119cf81e6e11b93ab4f009e2d1a21bc1` |

Inspect required GitHub checks at the current head of [draft PR #130](https://github.com/xorca0711/scRNA_seq/pull/130). Earlier-head CI is not evidence for a later revision. The draft remains unmerged and scientific acceptance remains pending.
