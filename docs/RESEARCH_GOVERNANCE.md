# Research governance and prospective analysis contracts

Effective 3 October 2026. This implements the owner's request to ground all
questions before choosing a project. It changes research development and execution
requirements, not historical results, claim grades or scientific acceptance.

## Authority and scope

`RESEARCH_QUESTIONS.md` owns the current A0–A27 questions. The dossiers under
`docs/research_dossiers/` develop their rationale, rivals and experimental bridges;
they do not create additional global questions. `analysis/research/registry.json`
locates each card, dossier, current evidence and future contract. Article-local
candidates retain their paper namespace, including the nine Nb4 proposals.

Paper packages own published-source synthesis and paper-specific measurements.
Versioned contracts own analysis choices; immutable run records own execution
facts; the designated evidence reports own their current interpretation.
`CLAIMS.md` retains historical grading authority. New exploratory results do not
automatically add or promote a claim. `PROGRESS.md` carries current handoff state;
older entries in its archive describe their original revisions only.

Every substantive numerical analysis must state what result could change which
decision. A descriptive question is legitimate when its biological or measurement
value is explicit. Missing experimental evidence must not be disguised by extra
scores, more elaborate models, mechanistic wording or a new RQ identifier.

## Develop a question before executing an analysis

Read the canonical card, dossier and current result together. Establish the
published result, this repository's additional evidence, prior exposure and the
precise remaining gap. Assess the leading explanation against the strongest
rival. A source paper's conclusion, its reanalysis and a reused atlas are not
independent evidence. A literature gap is provisional until a targeted primary
source review examines the actual proposed discriminator.

The dossier names a next investigation and experimental bridge. It need not
invent a molecular mediator before there is evidence. A useful first experiment
can discriminate population selection from within-state change, or continued
input from persistence after withdrawal. Endpoint choices must distinguish fate,
growth, survival, secretion and activity rather than exchange these labels.

Assay choice, biological effect margin and sample-size justification may be
unresolved during development. Record these unknowns. Before a confirmatory run,
justify precision using the actual biological-unit variance and meaningful effect;
a minimum eligibility count is not a power calculation. Bench implementation
requires model-specific feasibility, assay validation and the lab's applicable
experimental oversight; a repository proposal does not provide those facts.

## Literature context and explanatory illustrations

Question development follows the [literature workflow](LITERATURE_WORKFLOW.md):
recent primary work, older close precedents, contradictions and actual repository
observations must be connected to the proposed discriminator. The
[context index](research_dossiers/literature_context_2026-10-03/README.md) provides
the current bounded application; it is not portfolio-wide novelty clearance.

`question_guides` in the registry binds every canonical question to a context
note, illustrated entrypoint and exact versioned qualitative SVG. The gate checks
coverage, required context sections, a primary URL, a local SVG embed, content
hash, source revision and full working-hypothesis hash. Only these declared inert
SVGs qualify as explanatory documentation; scripts, data tables and measured
figures still require their existing contract/run provenance. Do not place a
measured result in this category to bypass the analysis gate. Changes to this
declaration and its validation require explicit review.

Existing registered illustrations are retained unchanged; corrections use a new
path/version. Mechanical checks can catch missing context and drift, but cannot
establish source support, search completeness or scientific merit. No analysis
contract or run receipt is invented for an editorial drawing. Branch protection
and mandatory review settings remain external to the repository.

## Work types and gates

| Work | Required scope | What can proceed |
|---|---|---|
| Documentation / reading | Source-grounded correction and explicit current authority | No numerical rerun required; reading is open even if analysis is gated |
| Metadata recovery | Source identity, joins, units and a feasibility decision | Unknown biological independence is allowed; no population inference |
| Exploration | Bounded question, measured endpoint, rivals and exposure record | Exposed data are allowed; findings remain exploratory |
| Descriptive estimation | Population, contrast, denominator and uncertainty limits | Sparse units can be described without cell-based population inference |
| Prediction | Timing, baseline, split units, train-only transformations and intended transport | Internal holdout and independent-study validation remain distinct |
| Confirmation | Unexposed outcomes, frozen choices, independent units and justified precision | Failed eligibility records a hold; thresholds cannot be relaxed to rescue an effect |

A causal interpretation additionally needs a justified identification or
intervention design and an appropriate functional endpoint. Passing a schema is
not evidence that these scientific justifications are correct.

## Prospective contract and execution

Copy `analysis/research/contract.template.json` to a new versioned question or
article config path. The template is deliberately unfinished and cannot run.
Complete every field in `analysis/research/contract.schema.json`, including exact
input/code SHA-256 values, study and biological-unit identities, exclusions,
methods, multiplicity, interpretation limit and stop rule. References are portable
repository-relative paths. Raw inputs may live in ignored `raw_data/`; they must
be available and hash-matched at execution, but need not ship in the repository.

Register the contract in `analysis/research/registry.json`. The owner is either an
existing A identifier or a registered article-local candidate. To add a genuinely
new candidate, document its relation to existing questions and evidence; do not
silently allocate the next global A number from a stale checkout.

```bash
python analysis/scripts/research_gate.py preflight path/to/contract.json --inputs
python analysis/scripts/research_gate.py check --base origin/main
```

Before running, freeze the contract (`status: frozen`) and commit it with the
hash-bound entrypoint and dependencies. Commit identity establishes the saved
specification, not proof that nobody previously viewed outcomes. The explicit
exposure record remains necessary. Use a new analysis ID and `amendment_of` link
when the design changes; retain the old contract and the reason for change.

```bash
python analysis/scripts/research_gate.py run path/to/contract.json --run-id question_stage_v1
python analysis/scripts/research_gate.py verify analysis/research/runs/question_stage_v1/receipt.json
```

The runner invokes Python or Rscript without a shell. It supplies `{run_dir}` in
declared arguments, refuses an existing run directory, verifies code and raw
inputs, records the Git revision and environment, captures logs, and hashes
expected outputs. Register its receipt and point a results report to it. A
successful receipt means execution, not scientific validation. Independent checks
of units, joins, arithmetic and the primary endpoint must precede interpretation;
their method and results belong in the evidence report. A second calculation
using the same data is numerical verification, not biological replication.

The wrapper is a cooperative execution gate, not an OS sandbox. A script with
write privileges could write elsewhere. Required CI and restricted integration
credentials protect accepted repository state; read-only source mounts or a
restricted runtime are needed where arbitrary local writes must be prevented.

## CI and changes to existing work

The research gate checks all canonical IDs and dossier sections, references,
registered prospective contracts, recorded outputs, and historical artifact
hashes. Its change check requires new or modified scientific code, configuration,
tables and figures to be bound to a contract/receipt. Exact infrastructure paths
are separately listed and reviewed; they are not evidence of a biological run.

`legacy_artifacts.json` preserves the pre-migration scientific scripts, configs,
tables and figures in article/RQ workspaces. Text line endings are canonicalized;
binary hashes are exact. These records are historical, with their original
exposure and interpretation limits. They are not converted into prospective
contracts. New corrections use new paths and a documented supersession link.

Run the ordinary repository checks as well as the new gate. A dossier with all
headings can still contain a weak hypothesis. Review must assess source fidelity,
novelty, identification, meaningful outcomes and conclusions. No automatic
validator or AI review may fabricate human acceptance.

GitHub should require the repository and research checks for PRs into main,
disallow force pushes/deletion and avoid administrator bypass. Policy, workflow,
validator, claim and baseline changes have explicit code ownership. On a
single-owner repository, an agent using the owner's credentials is not a separate
human reviewer: adding required self-review would make legitimate PRs impossible.
Record this limitation rather than claim independent review is enforced.

## Session and migration discipline

Start with branch, HEAD, upstream and dirty-state inspection. Work in an isolated
checkout. Preserve unrelated work and inspect the reconciliation ledger before
retiring any checkout. At delivery, check the latest integration base and record
what changed. Do not automatically merge competing scientific interpretations.

Current machine-readable metadata has one authority; narrative summaries link
it. Frozen outputs never change merely to make an old report look current. Update
`PROGRESS.md` before stopping, including precise external blockers. Routine
reading, metadata recovery and reversible fixes do not need repeated approvals;
scientific acceptance and protected policy changes retain their recorded review.

See [migration and reconciliation](audits/2026-10-03-repository-repair/REPORT.md)
and the [dossier index](research_dossiers/README.md). Private backups, local machine
settings and PI/contact planning remain outside the public repository.
