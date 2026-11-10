# Codex research session assistance

This implements the existing AGENTS.md decision workflow for Ravel sessions.
It is an assistance layer, not a new research contract or scientific acceptance
gate. The owner requested a project skill, lifecycle hooks and focused evaluation
on 8 November 2026. Policy wiring and hook scripts remain explicit review material.

## What runs

- [The hook sidecar](../../.codex/hooks.json) is the single source for SessionStart
  (startup, resume, clear, compact and fork) and the bounded Stop reminder.
- [Project config](../../.codex/config.toml) only enables hooks for this trusted project
  without changing model, sandbox, approval or service settings.
- [The project skill](../../.agents/skills/ravel-research-reasoning/SKILL.md) is
  discoverable for research tasks. Startup also injects its short body directly,
  so the preparation does not depend on implicit skill selection.
- [The hook implementation](../../tools/codex/research_session.py) reads Git state
  and registry locators. It writes only session-specific state in the OS temporary
  directory, outside scientific evidence. It makes no network calls and does not
  launch another model, run an analysis, send messages or modify repository files.

The Git root is resolved at execution, including when launched in a subdirectory
or worktree with spaces. Startup reports the actual checkout and revision. It
does not choose a question for the user or treat registry order as recency.

## Delivery behavior and limits

The reminder detects content changes to Markdown under Research Article,
RQ_Specified and docs/research_dossiers, including new, deleted and committed
documents. It excludes work already present at startup. LF/CRLF differences alone
do not count. Resume and compaction preserve the session baseline.

One Stop continuation asks the agent to review the changed synthesis and its
registry owners, or explain why the current interpretation remains valid.
The continuation is suppressed when stop_hook_active is true. No identical
boilerplate, additional experiments or scientific approval is required.
Respect user cancellation and pending approvals/input; the reminder does not
grant authority to continue dependent work.

This is a document-change reminder: it does not detect semantic correctness,
read-only reasoning failures or numerical-only changes. Existing contracts,
runner and CI retain those responsibilities. A missing/corrupt baseline or hook
error is reported without inventing a review pass; it does not block authorized
work. Sessions without a startup baseline initialize one without attributing old
work. Temporary-state eviction therefore loses delivery coverage until a new
baseline exists.

## Activation and trust

For a standalone/main checkout, Codex reads its own hook declarations. In a
linked Git worktree, the tested local hosts deliberately read hook declarations
from the **main/root checkout**, not the worktree's `.codex` files. The remaining
project configuration and the executed handler still use the session checkout.
A branch-only installation therefore does not activate hooks. The root-checkout
configuration applies across worktrees; the launcher returns an empty response
when a checkout has no `tools/codex/research_session.py`, rather than borrowing
another checkout's research state.

`python tools/codex/install_session_hooks.py` shows the root destination without
writing. With explicit setup approval, `--install` creates missing root-checkout
declarations only. It refuses a different existing sidecar, inline root hooks or
an explicit disabled-hooks setting. It never writes hook trust or changes model,
sandbox, approval or service settings. The source is the repository sidecar,
not a second inline copy. Running against its own main checkout or matching
installed declarations is an idempotent no-op. Duplicate source inline hooks
are rejected rather than installed.

Use Codex's normal project/hook trust review:
CLI /hooks, or the Desktop hook review/settings interface when available.
Do not edit the trust store or bypass review. Hook changes may require review
again. A running session need not reload new configuration; test a fresh session
and resume/compaction on the intended host.

Official references inspected on 8 November 2026:
[hooks](https://learn.chatgpt.com/docs/hooks),
[skills](https://learn.chatgpt.com/docs/build-skills).
Command and MCP handlers are supported; prompt/agent hook handlers are not a
substitute for an actual reasoning review. Host validation is separate from
calling the Python handler with synthetic events.

## Validation and evaluation

Run the deterministic tests:

```powershell
python -m unittest discover -s tools/codex -p "test_*.py" -q
```

They cover lifecycle events, subdirectories and spaces, preexisting work,
committed/new/deleted documents, session isolation, compaction, line endings,
owner routing, malformed input and the single-continuation bound.

Use the [case prompts](../../tools/codex/evals/cases.json) and separate
[evaluation rubric](../../tools/codex/evals/RUBRIC.md) for a bounded behavioral
trial. Do not expose the rubric to the candidate. Preserve an unfavorable trial.
Deterministic tests are not evidence that a model will reason correctly.

See PROGRESS.md for the actual activation and validation status.
The first [behavioral trial and activation finding](../../tools/codex/evals/REVIEW_2026-11-08.md)
is retained, including the unresolved live-hook discovery result.

## Live discovery repair, 8 November 2026

The empty hook list was reproduced on CLI 0.166.0 and the Desktop-bundled
0.167.0-alpha.3.2, including a new ephemeral read-only local thread. Changing
client identity and adding a worktree-local JSON sidecar did not fix discovery.
The implementation was valid; the discovery location was wrong for a linked
worktree. The official [loader implementation](https://github.com/openai/codex/blob/748ab55ca7de0b647d9a7a9d9a8e70e00f28666d/codex-rs/config/src/loader/local.rs)
removes worktree hook tables and loads the matching root-checkout source.

Only missing `.codex/config.toml` and `.codex/hooks.json` were created in the main
checkout. The existing main-checkout PROGRESS edit was preserved. The actual
[host response](../../tools/codex/evals/discovery_2026-11-08.json) now lists exactly
SessionStart and Stop from that root sidecar, with no warnings or errors, both
**untrusted**. No hook trust was granted and no actual lifecycle execution is
claimed. All 23 deterministic tests passed.

Automatic approval review stopped a later single-source configuration cleanup
before execution, requiring explicit authorization for the persistent setup.
That step was not retried without new authorization. This was the status on
8 November; the approval, cleanup and live validation below supersede that
pending state. Synthetic tests and discovery alone do not establish delivery
or scientific reasoning quality.

[Official hook documentation](https://learn.chatgpt.com/docs/hooks) distinguishes
local Codex execution from cloud-coordinated tasks: local command hooks do not
become available in a cloud task merely because tools run on the local computer.

## Approved consolidation and live validation, 9-10 November 2026

After the owner approved the two hooks, the installed Desktop host reported both
as trusted. [Live events](../../tools/codex/evals/live_2026-11-09.json) establish
startup-context delivery, successful real compaction, reinjection on the next
turn and normal Stop completion. A
[disposable-worktree test](../../tools/codex/evals/stop_2026-11-09.json) added only
a synthetic Markdown fixture: Stop requested one bounded review, then completed
without another continuation. The
[verification summary](../../tools/codex/evals/stop_summary_2026-11-09.json) records
zero model tool calls and removal of that temporary checkout.

On 10 November the owner separately approved consolidation. The branch now keeps
its declarations only in `.codex/hooks.json`; the installer reads that source and
refuses inline duplicates. The installed root declarations and their trust hashes
were unchanged, and the installer returned `already-installed`. The
[post-cleanup live check](../../tools/codex/evals/cleanup_2026-11-10.json) discovered
exactly two trusted hooks and observed startup injection plus Stop completion.
All 25 focused tests passed; final repository/provenance results are recorded in
the [validation log](../../tools/codex/evals/validation_2026-11-10.json). The checkout
integrity gate passes, but comparison with refreshed main `14449c0` reports 144
findings for newer Navarro assets absent from this older branch. This is a branch
integration limit, not permission to remove those assets. Preserve that failed
comparison and reconcile newer commits before integration.

Live resume remains unverified: the isolated sessions were ephemeral and were not
saved for disk resume. Behavioral delivery does not establish scientific reasoning
quality or human acceptance. No research result, validator, trust store, sandbox
or approval policy was changed, and this work does not merge or push the branch.
