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

## Biological screening and question progression

- Distinguish the organizing biological question, the current hypothesis or estimand, and the executable comparison. An available dataset, score or tool must not silently replace the biological purpose. Keep the work-type distinctions above; replication and description can be worthwhile aims in their own right.
- Before adding a screen, connect the published premise and actual repository observation to the next unresolved biological link or comparison. State the relevant alternative or validity threat and how informative positive, negative, mixed or unsupported outcomes would change the next decision. Use the existing owning plan/dossier and contract fields; this does not require another document, invented mechanism or numerical threshold.
- Choose methods and source searches for that decision. Annotation, normalization, enrichment, embeddings and robustness checks support screening when they can change a candidate, interpretation or measurement decision. Their availability or successful execution alone does not justify extending the analysis queue. Reuse sufficient existing results.
- Treat newly proposed roles and causal links as provisional. Mark published premises, repository observations, proposed explanations and unmeasured links separately. Broad annotation categories or marker changes alone do not establish a coherent functional programme. Biological sequences may concern regulation, state transitions, prediction or population dynamics; do not force every RQ into a ligand-receptor cascade or a complete causal mechanism.
- After each substantive step, record what was narrowed, weakened, left mixed or remained unestimated, then explain the next comparison from that finding. Revise the current synthesis when the evidence changes it, preserving earlier versions and exposure. If the result adds no biological or stated measurement information, say so rather than automatically adding another score or source. Execution completion and biological resolution are separate statuses.
- A missing downstream functional measurement limits the claim it would support. An informative upstream or partial descriptive screen may proceed within its own qualified scope. Name the exact missing input and dependent step; a failed access route or one file's missing fields does not establish source-wide absence. Preserve valid stop rules and do not relax them to obtain a favorable result.
- Keep the question README's current biological progression easy to read: organizing question, literature/visual evidence, what screening changed, and next biological decision, followed by execution history. Link related RQs by the distinct comparisons they own; do not merge, retire or duplicate IDs to tidy the narrative. Keep current README/context/dossier statements aligned rather than stacking contradictory completion banners.

Apply the [decision workflow](docs/governance/AGENT_DECISION_WORKFLOW.md#screening-as-question-development)
before expanding a screening sequence. These instructions guide review; they do
not replace the research contract, change claim authority or guarantee compliance.

## Skills, plugins and source tools

- Select a skill or connector for an identified biological, source, annotation or implementation need. Discover what is actually available in the current session and read the selected skill's instructions before applying it. Repository mentions are examples, not proof that a plugin is connected or a workflow is ready. Use the [capability guide](docs/governance/AGENT_DECISION_WORKFLOW.md#using-skills-and-connectors) when choosing a route.
- Prefer a suitable connected tool or existing qualified local implementation when it can do the work. Preserve the intended comparison, matrix semantics and biological units; switching to a familiar package or rerunning a pipeline is not automatically an improvement. Skill guidance does not override the owner's scope, research contracts or service permissions.
- Retain the source/accession/version, relevant request parameters, access limits and saved evidence needed to reproduce consequential tool-derived findings. Distinguish metadata retrieval, annotation, workflow execution and scientific interpretation. An unavailable connector or failed API call is not proof of absent data: consider an appropriate documented API, public source file or local method within scope before recording the exact limitation. Do not run a portfolio-wide tool census or source search for every question.

## Literature-grounded question development

- When deriving or materially reframing an RQ from reproduction/branch evidence, or preparing an experiment package, follow [docs/LITERATURE_WORKFLOW.md](docs/governance/LITERATURE_WORKFLOW.md). Search relevant recent primary literature beyond the existing bibliography and target PIs, together with the closest older precedents and contrary findings.
- Record actual search date, queries, coverage, source version, access and exact figure/result locators. Explain published finding → repository observation → remaining question → fit-for-purpose comparison → informative outcomes. For hypothesis-driven work, include the prediction and relevant alternatives. Separate completed reads from planned searches and shared-source reanalysis from replication.
- Keep published mechanisms as explicit premises. State whether the contribution is replication, model discrimination or a justified extension; do not infer novelty from absent search hits or a changed label/context alone.
- After reviewing literature relevant to a completed/committed analysis, annotate the current result interpretation when a primary study explicitly addresses an observed pattern. Name the authors and year, cite the exact figure/result, and state which repository observation it addresses: for example, "This pattern was already reported by Author et al. (year), Fig. X, in [context]." Distinguish directly tested explanations, consistent/related evidence, contradictions and unresolved overlap; correlation alone does not establish that the literature explains our result. Record source-version and access limits, and explicitly flag reused datasets rather than count them as independent support.
- Where that connection supports further work, state what the cited paper already resolves, what remains unanswered, and the specific comparison or screen that could go beyond it, with informative outcomes and required evidence. A justified replication or boundary test is allowed; neither a new mechanism nor a follow-up must be manufactured. If no informative extension is currently supported, say so.
- Apply these literature annotations prospectively to analyses being interpreted or revisited; do not silently reopen the whole portfolio. Add a dated interpretation note or versioned addendum linked from the current result entrypoint, literature context and README/dossier; do not edit a hash-bound historical result to add the link. Preserve frozen numerical results, contracts and historical interpretations, and do not rerun an analysis solely to add attribution. Keep any proposed RQ development separate from human scientific acceptance.
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

See [the decision workflow](docs/governance/AGENT_DECISION_WORKFLOW.md) for work-type routing,
the mutant/control example and the distinction between instructions, runtime
checks and human scientific decisions. Topic-specific assays and designs belong
in their own question plans, not in repository-wide agent policy.
