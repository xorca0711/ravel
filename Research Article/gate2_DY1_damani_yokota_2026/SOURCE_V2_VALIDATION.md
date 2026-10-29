# Source-v2 validation record

29 October 2026. Metadata-only correction; no scientific acceptance inferred.

## Confirmed execution checks

- Exact handoff base: `d62612ba0975e60f6b9d03e00ef22c3924af898b`.
- Frozen specification/code commit: `015b339808b004210c9983ae8b9e35cd5bb6d2ed`.
- Integration base freshly fetched before delivery checks:
  `78320a186b6f52426e7c7c5349a2f26492b718b7`; no new remote commits.
- Nine targeted synthetic parser tests passed; input preflight passed for all
  20 bound metadata files. No failed metadata execution; stderr is empty.
- Pre-freeze base-aware research gate and source-v2 receipt verification passed.
- Separate computation verified 18 reference rows, 24 feature-tag rows,
  72 membership rows and eight accession/title records.
- All nine v1 files matched the preserved execution checkout byte-for-byte.

## Cooperating reviewer

The parent reviewer found no blocking scope or correctness issue before freeze.
After execution, the reviewer checked the receipt at `015b3398`, every bound code
hash against its frozen Git blob, every saved output hash, four reference-label
summaries and four feature inventories. The reviewer independently checked all
72 unique `(feature_file, reference_file, tag_id)` membership rows against tag
sets established by prior direct source inspection; all matched. The reviewer
also confirmed no tracked v1 code/contract/output changes from `d62612b`.
This is bounded technical review of the same sources, not independent biological
replication, biological acceptance or approval of restricted analyses.

## Required repository checks

All required final-branch checks passed against the unchanged freshly fetched
integration base:

| Check | Result |
|---|---|
| Python compilation | Passed |
| Repository unit suite | 161 tests passed, one skip |
| Source-v2 synthetic regressions | Nine passed before freeze; unchanged tests/code reused |
| Claim contract | 18 numeric bindings passed |
| Saved Nb1, Nb4, A16, A23 and A22/A23-extension evidence | All passed; no biological rerun |
| Repository validation | 11,348 checks passed |
| Research gate against `origin/main` | Passed with v2 contract and receipt registered |
| Scope and preservation audit | All nine v1 files byte-identical to handoff Git blobs; 32 canonical questions, guides, infrastructure and prior contracts/receipts unchanged |
| Whitespace/staging check | `git diff --check` passed |

Only the existing DY1 candidate gained the new results evidence link. All changed
paths are confined to the paper package, new v2 run directory, registry and
PROGRESS. The two existing handoff worktrees and their ignored inputs remain
preserved. No validation or execution failure was suppressed. Initial shell
attempts could not access linked-worktree Git metadata under the sandbox; the
authorized operations succeeded through normal escalation without changing gates.

Full local check logs, `summary.json` and `preservation.json` are retained in the
task's 29 October visualization workspace under `source_v2/validation/`.
The last edits record these results and clarify persistent owner authorization;
they introduce no new links, code, inputs, outputs or analytical changes, so
passing computational checks are reused without a redundant full rerun.

The unchanged historical checks from the handoff remain supporting evidence;
new checks are not biological reruns. Fifteen missing historical Choi outputs
were restored from existing local copies with published-lock SHA-256 checks.
No original evidence, governance, validator, RQ decision or claim grade changed.

## Remaining work and settings

The bounded correction is complete and ready for the cooperating reviewer's
local integration/reconciliation. The parent review branch's documentation-only
`436b6cf` commit is
separate; the reviewer will reconcile its progress prose during integration.
Do not merge or edit that branch from this execution checkout.
Numerical stages 1–7 and results-based stage 8 remain unfinished; prior source
reading/design audits remain completed review work. No broader analysis is
queued. External service settings are unchanged; earlier Code Ocean access
limits were not retested. No GitHub publication or other external-service write.
