# Repository grounding and state reconciliation

Baseline: `0e03fa296eac2ddc4e8f02f5389d85c0f1058c2f`, fetched from main
after PR #129 completed. Branch: `codex/research-governance`.

## Diagnosis and repair

The repository already contains substantial source review, negative results,
corrections and qualified analyses. The problem is the uneven connection from
those observations to a discriminating biological question, combined with stale
working copies and duplicated status prose. Rewording titles alone would leave
both problems in place.

The repair adds [24 evidence dossiers](../../research_dossiers/README.md), links
proposed development scopes into the canonical A0–A23 cards and their workspaces,
and registers all nine newly merged Nb4 proposals without assigning global IDs.
Every dossier names the known result, repository evidence, remaining gap,
hypothesis, rival, discriminating outcomes, next investigation, experimental
bridge and interpretation limit. No RQ is chosen or declared experimentally ready.

The [governance contract](../../RESEARCH_GOVERNANCE.md) and
[registry](../../../analysis/research/registry.json) establish authority and
execution requirements. A typed prospective contract binds source and code
hashes, biological units, exposure, endpoints, design, validation scope and stop
rules. The runner checks the saved specification and records execution without
claiming scientific acceptance. CI checks dossiers, changed scientific assets,
contracts, receipts and historical artifact hashes. Agent entry points and a PR
template make the same requirements visible to different tools.

## Preserved repository state

The old primary checkout was at `33b27cf1f03da706ee987f3fd00b7127eaaff79e`
with 46 short-status entries. Other worktrees included detached analysis work.
All original checkouts remain in place. Work was performed in a fresh managed
worktree based on the fetched main, preventing interleaving with prior sessions.

A private preservation package contains binary staged/unstaged patches,
null-delimited status, changed/untracked file archives, per-file hashes and a
verified 450,322,230-byte Git history bundle covering refs and detached tips.
Archive integrity and member hashes were checked. The public
[reconciliation ledger](reconciliation.json) records classifications and hashes
without publishing machine settings or personal planning.

For the primary checkout, 646 changed/untracked file contents already existed
on fetched main after text line-ending normalization, 39 differed, and one was
private configuration. Thirteen of the 39 differing files exactly matched
historical main blobs after normalization. The remaining 26 received semantic
comparison: newer corrections and navigation were retained, while the unique
reading-readiness decision was selectively integrated. The ledger records a
disposition for every preserved primary file. Other worktree heads, archive
hashes and classified counts are also recorded there.

Ignored raw inputs and caches are **preserved in place, not copied into the
snapshot**. Do not remove old worktrees on the assumption that the private
package contains their ignored data. The stale primary checkout has not been
reset, cleaned or made to appear current. Continue this branch in its attached
worktree; migration of local raw inputs and eventual checkout retirement remain
separate storage operations.

## Selective reconciliation

- 3A/3B literature reading is open. Niethamer/S1 and D1 remain unrun with their
  numerical gates intact; W1 is pseudobulk, not completed flux inference.
- The X1–X4 comparison references and reading queue are retained without
  creating analysis workspaces or inventing owner reading completion.
- Newer main retains Nb2/Nb3/Nb4 execution, corrected A16 and source accounting,
  current ligand interpretation, A22/A23 extensions and the nine Nb4 plans.
- The current README retains its owner-requested general scope. Old claim-heavy
  README prose and stale “unexecuted” descriptions are not restored.
- Long AI_CONTEXT/PROGRESS snapshots remain in existing Git history, located under
  [history](../../history/2026-10-03-pre-governance/README.md). Exact working-copy bytes are preserved privately. Short current
  entry points link the evidence authorities instead of duplicating them.
- The older execution roadmap is labelled historical; it no longer overrides
  the owner's current decision to develop all questions before prioritization.

The two private Notion planning pages informed feasibility and the distinction
between lab fit and scientific merit. PI/funding/contact details stay private.
They do not establish novelty, causal identification or assay validity. Public
dossiers draw their biological evidence from the linked repository/source records.

## Enforcement and its limits

The GitHub configuration inspected at the start had no main protection and no
rulesets. Local instructions alone therefore could not enforce integration
discipline. The intended required checks are `validate` and
`research-governance`, with PR integration and no force pushes/deletion.
Applied server state is recorded in [integration settings](integration.json);
this report must not be read as proof that intended settings are active.

A single-owner account cannot provide independent review of its own PR. An agent
using owner credentials can also change policy unless credential scope is
restricted outside the repository. CODEOWNERS assigns visibility; it does not
solve that identity problem. The execution wrapper is cooperative, not an OS
sandbox. Schema checks can reject missing provenance and obvious contradictions;
they cannot establish that a hypothesis is novel or its declarations true.

## Verification and remaining decisions

The [validation receipt](validation.json) records actual commands and outcomes.
Frozen scientific artifacts and claim grades are preserved. No new biological
fit was run, and no existing result was retrospectively preregistered.

Next, review each promising discriminator against primary literature and source
eligibility. Then qualify assay validity, timing, independent units, meaningful
effect and lab feasibility. Only this evidence can justify a prospective
confirmatory design or a real experimental commitment. Those scientific
decisions remain open; the repair supplies a traceable process for making them.
