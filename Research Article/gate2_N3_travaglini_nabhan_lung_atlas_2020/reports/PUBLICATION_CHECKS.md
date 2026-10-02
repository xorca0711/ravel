# Nb4 publication checks

**2 October 2026.** Publication branch `codex/nb4-lung-atlas`, based on main
`ceb6ffc`. Analysis outputs were copied byte-for-byte from the completed study;
raw inputs and private note snapshots were excluded. Shared edits are limited
to navigation, dataset/source records, handoff notes, byte-preservation rules
and the archive CI step. The repository's main README is unchanged.

All commands below passed in the publication worktree using Python 3.12.14.
The existing numerical validation is documented separately in
[VERIFICATION.md](VERIFICATION.md) and [its immutable record](../runs/validation_v1/checks.json).

| Check | Result |
|---|---|
| `python -m compileall -q -x '[/\\]\.tools[/\\]' analysis "Research Article" RQ_Specified` | Passed |
| `python -m unittest discover -s analysis/tests -q` | 79 tests, one skipped; no failures |
| `python analysis/scripts/claim_contract.py --check` | 18 numeric bindings passed |
| Nb1 `verify_outputs.py` | Passed |
| A16 `verify_stage1_evidence.py` | Passed; its documented raw-input limitations remain |
| A23 `08_verify_external_current.py` | Passed |
| `python analysis/scripts/verify_a22_a23_extensions.py` | Passed |
| `python analysis/scripts/validate_repository.py` | 6,612 checks passed before this check note was added |
| Nb4 `python -m unittest discover -s "Research Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/scripts" -p 'test_*.py' -q` | Nine tests passed |
| Nb4 `scripts/verify_archive.py` | 14 run records; 119 output hashes; archived code, configurations and local links passed |

`verify_archive.py` uses only the Python standard library and is included in
repository CI. It checks evidence integrity without network access or matrices.
The hash records preserve historical script snapshots when presentation code
changes. Successful archive checks do not imply functional validation,
independent annotation or complete reproduction of the original paper.
