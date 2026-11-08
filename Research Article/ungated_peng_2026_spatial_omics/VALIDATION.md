# Peng execution validation — 8 November 2026

Validation targets [the current v3 result](RESULTS.md), not scientific acceptance.
Main was refreshed to `1ff71a1818be1782dede0ccd5898eea793497f73`, unchanged from
the planning integration base. Work stays on `codex/peng-spatial-reading-20261108`.

- Frozen v1/v2/v3 contract input/code preflights passed before their respective
  local commits and execution. V1/v2 failed verification and remain failed.
- Five focused parser tests passed for v3. Its independently implemented full
  data verification passed 3,961 checks, including all six discrepancies and
  byte-identical failure archives. The successful runner receipt verifies.
- Original checkout: its one pre-existing modified file is byte-identical to
  the session start. All 33 pre-existing worktree files also match their initial
  byte hashes. Their stat/line-ending status noise is not reset or normalized.
- Scoped Git attributes preserve exact frozen Peng code/contract bytes across
  platforms; existing attributes already preserve every research run output.

- Repository validation passed **18,340 checks**, including local links and JSON,
  selected numeric bindings and the claim register. All **46 governance tests**
  passed. The five article-local parser tests are separate from those tests.
- Whitespace checks passed. All nine frozen v1/v2/v3 code files match their
  committed Git blob hashes; all 53 v3 contract/code/output hashes match the
  staged bytes. Canonical questions, registered question guides, illustration
  provenance and infrastructure allowances are unchanged from planning.
- The first base-aware provenance check detected that an old Weft contract pins
  the root `.gitignore` and `.gitattributes`. Our additions were removed and both
  roots restored to their exact previously frozen hashes. Peng rules now live in
  package-local `.gitattributes` and `analysis/research/runs/.gitignore`; no frozen
  contract, validator or interpretation boundary was changed to clear the failure.

The final `research_gate.py check --base origin/main` **passed** after that
correction. Unchanged historical numerical/archive checks from the planning
revision are reused; no biological analysis is rerun
for documentation changes. The final documentation and receipts are local only;
no push, PR, merge, Notion mutation or author/access request was made.
