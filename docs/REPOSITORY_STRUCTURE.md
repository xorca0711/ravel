# Repository structure and label scope

**Current scope — 7 October 2026:** 31 canonical questions (A0–A30). A24–A27 derive from Nb5; A28–A30 from Wp. Wg is the 2021 Wagner/Compass paper, Wp is Wang/Wagner 2025 PGAM, and Niethamer W1 is a separate macrophage analysis. The [readiness audit](audits/2026-10-07-repository-readiness/REPORT.md) reconciles current execution and historical plans.

Updated 7 October 2026; September layout conventions retained. This contract follows the existing shared-analysis
and paper-study layout. It defines where current material belongs; dated
protocols, original trial names and immutable run records remain historical evidence.

| Material | Canonical location | Rule |
|---|---|---|
| Repository-wide scientific questions | [RESEARCH_QUESTIONS.md](../RESEARCH_QUESTIONS.md) | One current register, A0–A30; proposed refinements are linked to evidence dossiers; link to source studies rather than maintaining a second register |
| Question-specific plans and analyses | `RQ_Specified/A<id>_<topic>/` | Prospective plan, source metadata, configuration, scripts, tables, reports and gallery; reference the root question register |
| Shared question figures | [analysis/figures/rq/README.md](../analysis/figures/rq/README.md) | Curated gallery/captions; assets, tables and provenance alongside; fresh script-16 runs under `renders/` |
| Cross-question measurement checks | [RQ_MEASUREMENT_CONTRACTS.md](RQ_MEASUREMENT_CONTRACTS.md) | Reusable checks and legacy-ID crosswalk; biological decisions stay in the root register |
| Shared plotting and pipeline entrypoints | `analysis/scripts/` | Numbered entrypoints; reusable utilities in `analysis/lib/` |
| Palette, reusable settings and contracts | `analysis/config/` | Shared configuration, independent of a paper's local trial ID |
| Paper notes, contracts, inference and galleries | `Research Article/<paper>/` | Preserve the paper-specific source evidence, scripts, tables and figure gallery |
| Cross-study specificity analysis | `Research Article/epithelial_state_specificity/` | Existing substantive analysis module, referenced by the global questions |
| Corrective scientific analyses | `analysis/corrections/` | Keep original results and corrections distinguishable |
| Graded evidence and negative results | [CLAIMS.md](../CLAIMS.md), [NEGATIVE_RESULTS.md](NEGATIVE_RESULTS.md) | Claims change only with supporting evidence; current question reports may narrow historical interpretations without promoting grades |
| Original two-atlas findings | [FINDINGS.md](../FINDINGS.md) | Historical scope; not a summary of every later question or correction |
| Dataset roles, units and eligibility | [DATASETS.md](DATASETS.md) | Link to run-specific provenance and gates; shared deposits and companion assays are not independent replications |
| Methods, structure, portfolio and communication drafts | `docs/` | Each page identifies whether it describes execution, reference methods or proposed work |
| Reading order and paper status | [Research Article/ROADMAP.json](../Research%20Article/ROADMAP.json), [Research Article/README.md](../Research%20Article/README.md) | Stable paper identifiers differ from the reading sequence; update the two views together |
| Current handoff and operating context | [PROGRESS.md](../PROGRESS.md), [AI_CONTEXT.md](../AI_CONTEXT.md) | Concise current handoff; prior long checkpoints are archived under docs/history |
| Raw inputs, caches and private reading annotations | Ignored local directories | Do not copy them into public figure or documentation directories |

See [research governance](RESEARCH_GOVERNANCE.md) for authority, contract and immutable evidence rules. [Dossiers](research_dossiers/README.md) develop all 31 questions; the registry locates their evidence and the 31 article-local candidates across Nb4, Nb5, Wg and Wp.

## Identifier namespaces

- `A0`–`A30` identify the current repository-wide question cards. A15–A18
  retain their pending proposals; A19–A21 derive from Nb2 and A22–A23 from Nb3.
  Registration is not biological acceptance or confirmatory readiness.
  Figures use the associated question ID, with panel/group suffixes where needed.
- `England/E-N1`–`England/E-N8` are paper-local candidate extensions indexed
  from the root register, not A19–A26. Biological cards and supporting checks
  stay in the England paper package; executable plans belong under their
  relevant global question once specified. Performed cross-document audits
  and evidence remain under `docs/audits/<date>-<topic>/`.
- Paper-local IDs require paper context: `Niethamer/W1`, `Niethamer/S1`,
  `Sikkema/S1`, `Choi/D1`, `Yu/N1`, `Yu/U5`, `Yu/F01`. Equal short labels do
  not mean equal analyses. Existing historical scripts are not renamed solely
  to make all short labels globally unique.
- `W1` is the historical Niethamer macrophage pseudobulk trial label. It is
  neither a statistical evidence grade nor evidence that Compass flux modelling ran.
- The former Yu follow-ups `RQ1`–`RQ4` are now `A11`–`A14`.
  Display labels D1, D2a–c, D0 and D4 map to A11, A12a–c, A12-S1 and A14.
  Historical D0/D1/D2 CSV basenames are retained and documented by the
  [relocation manifest](../analysis/figures/rq/il1b_context/relocation_manifest.json).
- `C1` onward identifies claims. Reading-order paper numbers, trial IDs,
  global questions, figure groups and claim IDs are different namespaces.

## Paths and historical provenance

On 25 September 2026, `Thesis/` was renamed to `Research Article/` and
`RQ_Specified/` was introduced at the owner's request. Paper folder identifiers,
scientific results and historical run identities are unchanged. The
[migration record](migrations/2026-09-25-research-layout/README.md) lists preserved
hashes and archives original bytes of updated code and documentation. Historical
paths are resolved by `analysis/lib/repository_paths.py`; this is a record check,
not evidence that the updated scripts have rerun. Quote paths containing
`Research Article` in commands; Markdown links encode the space as `%20`.

`ROADMAP.json` paper `folder` values are relative to `Research Article/`, without a
trailing slash; other artifact fields are repository-relative. The owner-selected
`gate2_C3_yu_lee_choi_min_2026/` is branch 2C item 3, stable paper 13.
This documented exception does not renumber the roadmap.

Shared IL-1 figures now use scripts 19–21. Their recorded UMAP/PCA preparation
was executed before relocation; the original script bytes and identities
remain archived alongside the [current figure report](../analysis/figures/rq/il1b_context/REPORT.md).
Original preparation input paths are study-relative; current rendering input
and output paths are repository-relative. No execution date or original hash
is rewritten to make an old run appear new. Future render records archive
their predecessor; visual review hashes must match the current PNGs.

Current summaries take status from stage reports and validation artifacts.
Older plans and first-batch reports do not override a completed continuation.
“Feasible analyses complete” does not mean that unavailable biological
identities, independent validation, spatial regions or causal endpoints are resolved.

The main README provides universal repository context and shared navigation.
Its Start here section links to repository-wide indexes, not individual papers
or paper-specific results, branches or derived RQs. Those links belong in the
research-article and question indexes. The main README links to galleries without
embedding a partial selection.
PI fit, contact preferences and personal outreach planning stay in the owner's
Notion workspace; public documents contain scientific questions and portfolio text.

## Nabhan branch registration, 29 September 2026

`Research Article/gate2_N1_nabhan_2023/` is the owner-selected Gate 2N item 1,
with stable roadmap paper ID 6. `Nb2-P1`–`Nb2-P10` identify its published propositions;
`Nb2-R*` and `Nb2-B*` identify reproduction and exploration stages;
`Nb2-N1`–`Nb2-N8` are paper-local candidate hypotheses linked from the root register.
They do not renumber A0–A18, the earlier Nabhan/Nb1 trial or other papers' N1 labels.
Private reading annotations stay local. Source metadata and prospective contracts
are distinct from executed biological results. Question-specific continuations use
an owning `RQ_Specified/` contract once their scope and endpoints are specified.
## Nb2 branch analysis: corrected hierarchy, 29 September 2026

`Research Article/gate2_N1_nabhan_2023/branch_analysis/` owns the branch analyses,
including cross-study comparisons used to interpret the paper. Its candidate
notes retain Nb2-N1–N8 as provisional interpretations. `RQ_Specified` is populated
later with questions warranted by the analysis and synthesis; branches are not
automatically promoted to RQs. The premature Nb2-RQ1–RQ8 registration is retired.
The move preserves measured results, source records and existing A-series scope. [Index](../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/README.md).

## Nb2 result-derived questions, 29 September 2026

The subsequent [synthesis](../Research%20Article/gate2_N1_nabhan_2023/RQ_DERIVATION.md)
proposes A19–A21 after the paper analyses. Their new plans live under
`RQ_Specified/A19_fzd_response_reversibility/`,
`RQ_Specified/A20_fibroblast_fzd_context/` and
`RQ_Specified/A21_fzd4_capillary_function/`. Earlier analyses stay paper-local.
N1/N2/N3/N5 combine in A19; N6 and N7 inform A20/A21; N4/N8 remain deferred.
The older Nb2-RQ1–RQ8 identities remain retired. No A0–A18 scope or C-grade changes.


## A19 question-specific execution, 30 September 2026

The owner subsequently authorized A19 analysis. Its new cross-source context
results, methods, figure set, scripts and verification live under
`RQ_Specified/A19_fzd_response_reversibility/`. Prior Nb2 paper analyses remain
unchanged in `Research Article/`. The root README retains universal navigation;
A19 discovery belongs in the question register and question/figure indexes.
Supporting RNA execution does not imply a completed direct Fzd/fate/reserve test
or change any existing scientific claim grade.

## A21 question-specific execution, 30 September 2026

A21 now contains a source/cohort audit, independent GSE211335 animal-level
expression analysis, methods, three figures and verification under
RQ_Specified/A21_fzd4_capillary_function. Prior Nb2 measurements remain paper-local;
the reused cohort comparison is explicitly labelled. Functional Fzd4-dependent
lineage and maintenance hypotheses remain untested.

The A21 priorities extension is versioned under
`RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/`, with its own
contracts, source provenance, tables, scripts, figures, results and functional
design. Parent scientific evidence is preserved; revised parent navigation and
contracts have pre-extension snapshots under the extension metadata/history.
