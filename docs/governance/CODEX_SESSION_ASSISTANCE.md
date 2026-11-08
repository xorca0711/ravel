# Codex research session assistance

This implements the existing AGENTS.md decision workflow for Ravel sessions.
It is an assistance layer, not a new research contract or scientific acceptance
gate. The owner requested a project skill, lifecycle hooks and focused evaluation
on 8 November 2026. Policy wiring and hook scripts remain explicit review material.

## What runs

- [Project config](../../.codex/config.toml) registers SessionStart for startup,
  resume, clear, compact and fork, plus a bounded Stop reminder.
- The same config enables hooks for this trusted project
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

The files must exist in the checkout a session opens. A local branch does not
change main or other worktrees. Use Codex's normal project/hook trust review:
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
