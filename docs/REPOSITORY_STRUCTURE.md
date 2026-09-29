# Repository structure and label scope

Updated 28 September 2026 (project navigation, dataset inventory and current execution links). This contract follows the existing shared-analysis
and paper-study layout. It defines where current material belongs; dated
protocols, original trial names and immutable run records remain historical evidence.

| Material | Canonical location | Rule |
|---|---|---|
| Repository-wide scientific questions | [RESEARCH_QUESTIONS.md](../RESEARCH_QUESTIONS.md) | One current register, A0–A18 (A15–A18 proposed, pending retain/reject); link to source studies rather than maintaining a second register |
| Question-specific plans and analyses | `RQ_Specified/A<id>_<topic>/` | Prospective plan, source metadata, configuration, scripts, tables, reports and gallery; reference the root question register |
| Shared question figures | [analysis/figures/rq/README.md](../analysis/figures/rq/README.md) | Curated gallery/captions; assets, tables and provenance alongside; fresh script-16 runs under `renders/` |
| Cross-question measurement checks | [RQ_MEASUREMENT_CONTRACTS.md](RQ_MEASUREMENT_CONTRACTS.md) | Reusable checks and legacy-ID crosswalk; biological decisions stay in the root register |
| Shared plotting and pipeline entrypoints | `analysis/scripts/` | Numbered entrypoints; reusable utilities in `analysis/lib/` |
| Palette, reusable settings and contracts | `analysis/config/` | Shared configuration, independent of a paper's local trial ID |
| Paper notes, contracts, inference and galleries | `Research Article/<paper>/` | Preserve the paper-specific source evidence, scripts, tables and figure gallery |
| Cross-study specificity analysis | `Research Article/epithelial_state_specificity/` | Existing substantive analysis module, referenced by the global questions |
| Corrective scientific analyses | `analysis/corrections/` | Keep original results and corrections distinguishable |
| Graded evidence and negative results | [CLAIMS.md](../CLAIMS.md), [NEGATIVE_RESULTS.md](../NEGATIVE_RESULTS.md) | Claims change only with supporting evidence; current question reports may narrow historical interpretations without promoting grades |
| Original two-atlas findings | [FINDINGS.md](../FINDINGS.md) | Historical scope; not a summary of every later question or correction |
| Dataset roles, units and eligibility | [DATASETS.md](DATASETS.md) | Link to run-specific provenance and gates; shared deposits and companion assays are not independent replications |
| Methods, structure, portfolio and communication drafts | `docs/` | Each page identifies whether it describes execution, reference methods or proposed work |
| Reading order and paper status | [Research Article/ROADMAP.json](../Research%20Article/ROADMAP.json), [Research Article/README.md](../Research%20Article/README.md) | Stable paper identifiers differ from the reading sequence; update the two views together |
| Current handoff and operating context | [PROGRESS.md](../PROGRESS.md), [AI_CONTEXT.md](../AI_CONTEXT.md) | Current section first; older dated checkpoints remain historical |
| Raw inputs, caches and private reading annotations | Ignored local directories | Do not copy them into public figure or documentation directories |

## Identifier namespaces

- `A0`–`A18` identify the current repository-wide question cards. A15–A18
  remain proposals pending retain/reject; an identifier is not claim acceptance.
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
- `W1` is the historical Wagner-branch myeloid pseudobulk trial label. It is
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

The main README links to galleries without embedding a partial selection.
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
