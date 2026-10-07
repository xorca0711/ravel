# Ravel identity and location migration

Date: 7 October 2026. Integration baseline: `744996d` on `origin/main`.
Owner requested implementation after reviewing the migration scope. Display name:
**Ravel**; repository slug: **ravel**. The name is not an acronym.

## Scope decision

Ravel develops biological questions through critical reading, reproduction of
accessible findings and reanalysis of public omics and complementary experimental
evidence. Papers and questions determine the relevant tissues, organisms and
disease contexts. A recently read topic is not a permanent project-wide focus.
The research workflow and evidence requirements remain in force. Existing lung
studies and every other question retain their specific endpoints and limits.

## Stages and acceptance criteria

| Stage | Work | Completion evidence |
|---|---|---|
| 1. Preserve and prepare | Inspect integration base, active branches, worktrees and local edits; isolate this change | Baseline `744996d`; scoped `codex/ravel-rename-20261007` branch; unrelated primary-checkout edits retained |
| 2. Align identity and mission | Update README, citation metadata, agent entry point and research navigation | Paper-driven scope without a preferred tissue or recent study topic |
| 3. Preserve source-link compatibility | Accept current and historical repository source URLs; explicitly review the validator diff | Positive tests for both identities; negative tests for foreign owners, lookalike repositories, wrong paths and schemes; existing integrity tests pass |
| 4. Validate and publish | Run required checks, refresh base, open the migration PR, rename GitHub and update the remote | Passing repository/research CI; recorded PR and final repository URL |
| 5. Migrate local access | Inspect dependent paths, migrate the directory if available, retain a compatibility path and verify worktrees | Git state, environment access, data access and recovery tooling remain usable; unsupported application settings explicitly recorded |
| 6. Communicate | Provide a proposed LinkedIn title and description matching the new mission | Draft supplied to owner; no LinkedIn publication requested |

## Preservation and compatibility review

The old name appears in historical evidence, absolute execution paths and frozen
source links. Those occurrences are not a global replacement target. Frozen
contracts, receipts, figures, archived scripts, claim grades and question IDs
remain unchanged. No biological analysis is rerun to change branding.

The SVG validator previously allowed only the exact old repository prefix. Its
change adds the exact new prefix for the same owner and retains the old one.
It does not change the element allowlist, active-content rejection, hash checks,
source-revision field checks or immutable-illustration rules. Regression tests
exercise the complete question-guide validation path. This is an explicit
compatibility review, not a claim of independent or human scientific approval.
The migration PR exposes the validator diff for review under existing branch
protections; required checks are not bypassed.

Existing chronology and paper-specific scientific descriptions retain their
original scope. The architecture document's new dated scope paragraph supersedes
its old project-wide lung restriction without reinterpreting past measurements.

## Local migration policy

The physical project and research data stay on X:. A legacy-path directory
junction can retain access from old tasks, environments and recorded operational
paths while application registrations are updated. It is an alias, not a second
data copy. Do not recursively delete either end of a junction to remove an alias.

Codex's available task tools do not expose a project-folder/name editor. Its
supported project menu provides **Edit project**, folder selection and **Make
primary**. Any remaining UI action will be recorded rather than modifying the
application's live databases. Historical chat text and run receipts are not
rewritten.

## Execution status

Stages 1–3 implemented and explicitly reviewed above. All ten required local
validation steps passed: Python compilation; 145 unit tests (one optional skip);
claim-contract check; Nb1, Nb4, A16, A23 and A22/A23 evidence verification;
10,586 repository checks; research gate against `origin/main` at `744996d`.
The first sandbox test attempt could not write Windows temporary directories;
the complete suite passed with isolated X-drive temporary storage outside that
sandbox restriction. No test or governance requirement was weakened.

Publication and local migration are in progress. Final results and external
settings will be recorded before delivery.
