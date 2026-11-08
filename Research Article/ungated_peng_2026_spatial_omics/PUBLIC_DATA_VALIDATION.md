# Public-data validation and preservation

8 November 2026. Execution validation is not human scientific acceptance.

- A12 contract/code freeze: `8c22904`; 156 declared inputs, 17 expected outputs.
  Three focused tests passed for zero-positive missingness, joint denominators
  and confidence-boundary inclusion. The immutable run passed 7,677 independent
  sparse/scalar checks, including exact old primary count/library parity.
- Spatial v1 freeze: `8888216`; its first source failed before expression because
  symbols were not globally unique. V1 code, specification, receipt and logs remain
  unchanged. V2 freeze: `1b7df32`; unique Ensembl IDs and unique fixed targets are
  required, while symbol-level QC follows the documented original C3 processing.
  Four focused geometry/count tests passed, including disconnected tissue,
  two-hop separation and duplicate-symbol count/detection preservation.
- Source files are reused through local hardlinks under ignored raw_data, with
  explicit source paths and SHA-256 manifests. Scripts open them read-only.
  No full-matrix copy, redownload or historical script replay was performed.
- All 34 pre-existing dirty-file content hashes remain unchanged. Canonical
  question IDs, registered explanatory images and infrastructure allowances match
  the starting `58dd73b` state. No governance or validator change.

Spatial v2 then verified 43 sections and stopped on two explicit zero sparse
entries in GSM9226211. V3 (`bf2f841`) retains nonnegative integer validation,
eliminates stored zeros before detection QC and reuses those 43 exact extracts.
It binds 447 inputs and 122 expected outputs, including the complete failed v2
archive and its nested v1 archive. Five focused tests pass. Targets, thresholds
and graph statistics remain fixed. Scoped Git attributes preserve the exact new
contract-bound context/specification and manifest bytes on Windows checkouts.

- Spatial v3 completed all 56 sections and passed 3,782,624 independent checks;
  maximum absolute discrepancy 3.92e-11. The complete failed archives are retained
  byte-exact, including all 43 verified partial spot extracts. Four explicit zero
  entries in two fresh sections were handled without changing QC or totals.
- The initial base-aware gate caught two manifests registered only as inputs.
  The explicit source-binding contract (`7ee773a`) registers them as configuration
  and verifies 131 GEO library/section identities and 542 immutable receipt input
  bindings. No infrastructure allowance or validator was changed.
- Result PNGs were decoded/inspected, paired figures and example maps reviewed,
  and all PDFs parsed. The map atlas has 25 patient pages. A rendering-only
  correction passed ten text-bound checks, but the owner subsequently requested
  rationale in prose; both text-box renderings are now historical artifacts only
  and are omitted from the current gallery. Measured plots/maps remain displayed.
- Prior GEO and supplement result reports, old A12 component report and root
  hash-bound Git rules are byte-preserved. Governance/validator Git content is
  unchanged; existing checkout CRLF explains a raw Git-blob/working-byte mismatch.
- Source SciPy deprecation messages contain trailing-space lines in immutable
  current/archived stderr logs. Those exact logs are preserved, not edited to
  satisfy an optional whitespace check. Authored-file whitespace is checked
  separately. This is not a changed scientific or governance check.

The staged-byte audit passes for all 172 new frozen contract/configuration, code,
context and output assets. Scoped attributes plus explicit renormalization restore
the exact already-hashed manifest/specification bytes in Git; runtime bytes did
not change. The 105 declared PDF/compressed outputs omitted by generic cache
ignore rules were explicitly staged, without changing those rules or including
raw caches. All 34 unrelated starting-file hashes remain unchanged.

Final validation passed: **18,490 repository checks**, the unchanged base-aware
research provenance gate, and authored/staged whitespace checks. Final refetch
confirmed `origin/main` is still `1ff71a1818be1782dede0ccd5898eea793497f73`; no
integration update was required. The exact staged-byte audit covers all 172
new frozen assets. Successful source-binding verification records **2,979 checks**.
No scientific acceptance or claim-grade change follows from these checks. Previous passing governance tests and unchanged historical archive/claim
checks are reused; focused new tests and independent measured checks cover this
implementation. No biological computation was replayed for documentation edits.

At analysis delivery, the owner-reported Zenodo request remained pending and
unverified; no external message/request, push, PR, merge or Notion mutation had
been made. The owner subsequently authorized publication: delivery commit
`65627dc` was pushed and [PR #173](https://github.com/xorca0711/ravel/pull/173)
opened against main on 8 November 2026, with both GitHub connections verified as
`xorca0711`. The integration base is unchanged. The owner also requested a
completion handoff to the coordinating chat for biological-rationale review,
neighboring-article comparison, possible extensions and job implications. This
publication update changes no scientific outputs or interpretation boundaries.
Publication validation again passed all 18,490 repository checks and the
base-aware provenance gate. The 34 unrelated file hashes remain unchanged.
Both GitHub Actions workflows passed for analysis commit `65627dc`; the final
publication-record commit requires its own remote CI result.
