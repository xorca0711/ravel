# Repository research instructions

Read `AI_CONTEXT.md`, `PROGRESS.md`, and `docs/RESEARCH_GOVERNANCE.md` before substantive work.
Use `analysis/research/registry.json` to locate the current question card, dossier and evidence.
Do not infer current state from an old checkout, an old plan or a chat summary.

## State and preservation

- Inspect HEAD, upstream and working-tree changes before editing. Fetch the requested base when network access is available; otherwise state its last verified revision.
- Work on a scoped branch/worktree. Preserve unrelated, staged, untracked and ignored work. Never reset, clean, stash, delete or move someone else's work to obtain a clean state.
- Inspect the reconciliation record before retiring an old worktree. Do not mistake local untracked paths for new work: they may already exist on main.
- Before delivery, rerun checks against the current integration base and account for new remote changes.

## Scientific work

- Every substantive analysis must identify its question or article-local candidate, purpose, comparison or estimand, biological unit, measured endpoint and interpretation limit. Match the framing to the work type; description, replication, prediction and perturbation-effect estimation need not invent a mechanism.
- For a hypothesis-driven study, state the hypothesis and the most consequential alternative explanation or validity threat. A mutant-versus-control design can be sufficient for its stated effect question. A rival is an explanation to assess, not a mandatory extra experimental group; add rescue, factorial, time-course or orthogonal assays only when needed for the intended inference. Record unresolved alternatives without claiming to exclude them.
- Read the current result and amendment before the original plan. Cite primary sources and exact repository evidence separately. Shared samples and reused source data never become independent replication.
- Use the research contract and runner described in `docs/RESEARCH_GOVERNANCE.md`. Metadata recovery, exploration, prediction, confirmation and documentation have different requirements.
- Exploratory work is allowed. Record prior outcome exposure honestly; a later freeze does not erase exposure. Amend designs prospectively and retain unfavorable results.
- Do not invent an effect margin, mechanism, sample size, source identity or independent replicate to complete a template. An explicit unknown restricts the permitted analysis.
- No score is automatically fate, secretion, pathway activation, lineage or repair function. Specify the measured endpoint and the missing biological discriminator.
- Preserve frozen outputs, source contracts and scripts. Corrections use a new version and a supersession link. Do not replay overwrite-prone historical scripts over archived evidence.
- Question IDs and execution completion do not imply scientific acceptance. Do not create a human retain/reject decision or promote a claim grade without its recorded authority.
- Preserve every current RQ and its evidence. Work on the owner's requested question; do not rank or retire the portfolio without authorization, or expand a failed analysis merely to obtain a positive result. A justified follow-up after an unfavorable result is allowed with a new rationale and exposure record.

## Literature-grounded question development

- When deriving or materially reframing an RQ from reproduction/branch evidence, or preparing an experiment package, follow [docs/LITERATURE_WORKFLOW.md](docs/LITERATURE_WORKFLOW.md). Search relevant recent primary literature beyond the existing bibliography and target PIs, together with the closest older precedents and contrary findings.
- Record actual search date, queries, coverage, source version, access and exact figure/result locators. Explain published finding → repository observation → remaining question → fit-for-purpose comparison → informative outcomes. For hypothesis-driven work, include the prediction and relevant alternatives. Separate completed reads from planned searches and shared-source reanalysis from replication.
- Keep published mechanisms as explicit premises. State whether the contribution is replication, model discrimination or a justified extension; do not infer novelty from absent search hits or a changed label/context alone.
- Maintain the local literature-context note, dossier and illustrated README together; use the registry's question guide. Reuse valid prior scans, refresh when the comparison or evidence changes, and link the context in prospective numerical contracts. No search or schematic certifies novelty or laboratory readiness.

## Delivery

- Keep tool output and handoffs concise. Batch independent reads, reuse valid checks and avoid duplicate audits. Run additional checks when a change or unresolved risk justifies them.
- Prefer deterministic scripts for mechanical checks. Do not delegate overlapping scans; use subagents only when authorized and their independent work improves the result.
- Distinguish confirmed findings, uncertainty and proposed actions. Ask again only when essential information or authorization is missing.

- Run the targeted tests and required repository checks. Do not rerun biological analyses for documentation-only changes.
- Update `PROGRESS.md` before stopping. Record work completed, failures, exact next steps and unresolved external settings.
- Keep current summaries short and link evidence. Historical checkpoints remain historical.
- Changes to governance, validators and interpretation boundaries need explicit review; agents must not weaken checks to make their own work pass.
- Instructions assist compliant agents; runtime gates and protected integration provide enforcement. Never claim these files control arbitrary tools or guarantee scientific truth.

See [the decision workflow](docs/AGENT_DECISION_WORKFLOW.md) for work-type routing,
the mutant/control example and the distinction between instructions, runtime
checks and human scientific decisions. Topic-specific assays and designs belong
in their own question plans, not in repository-wide agent policy.
