# Repository structure and label scope

**Current scope — 3 November 2026:** 33 canonical questions (A0–A32) and 37 retained article-local candidates. A32 develops Yd1-P02; registration does not imply scientific acceptance. The [registry](../analysis/research/registry.json) and [question homes](../RQ_Specified/README.md) own the current inventory.

Navigation and label scope reconciled 2 November 2026; existing evidence ownership retained. This contract follows the existing shared-analysis
and paper-study layout. It defines where current material belongs; dated
protocols, original trial names and immutable run records remain historical evidence.

| Material | Canonical location | Rule |
|---|---|---|
| Repository-wide scientific questions | [RESEARCH_QUESTIONS.md](../RESEARCH_QUESTIONS.md) | One current register, A0–A32; proposed refinements are linked to evidence dossiers; link to source studies rather than maintaining a second register |
| Topic-based navigation | [Biological topic map](RESEARCH_TOPICS.md), with matching RQ/article index tags | Overlapping biological scope; one stable home per owner. Tags are separate from current findings, reading status and execution status. |
| Question homes | `RQ_Specified/A<id>_<topic>/` for all 33 RQs | README starts with Organizing Biological Q, then Literature context & visual hypothesis; local context, plan and schematics. Add analysis subdirectories only where work exists; link paper-owned and frozen evidence. |
| Full scientific argument | `docs/research_dossiers/A<id>.md` | All 33 dossiers retain hypotheses, alternatives and experimental bridges; each links its question home. |
| Qualitative RQ illustrations | [RQ schematic gallery](../RQ_Specified/SCHEMATIC_GALLERY.md) and each home’s `schematics/` | Current matte PNG and prompt, with preserved source artwork; separate from measured-result figures. |
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

See [research governance](RESEARCH_GOVERNANCE.md) for authority, contract and immutable evidence rules. [Dossiers](research_dossiers/README.md) develop all 33 questions; the registry locates their evidence and the 37 retained article-local candidates; their IDs do not automatically become canonical RQs.

The question README is the reader's current scientific entrypoint: biological
purpose, published premise, performed comparison, actual result, changed
interpretation and the next uncertainty. The local context supplies source
support; the dossier develops the complete reasoning and proposed comparisons.
An unchanged registered hypothesis can describe a narrower branch than the broad
purpose, so its scope remains explicit. Old plans are retained as history rather
than treated as a second current execution queue. The collection index offers
biological-topic and contribution-based reading routes; neither replaces IDs or
assigns scientific acceptance. Frozen source evidence stays with its owner.

The [topic map](RESEARCH_TOPICS.md) spans all 33 question homes and 19 paper
packages. The 35 directories under `RQ_Specified/` comprise those 33 homes plus
two shared/historical workspaces; the 21 under `Research Article/` comprise 19
paper packages, the cross-study specificity module and the Primary source archive.
These supporting directories do not create extra RQs or papers. Topic changes
update navigation rather than moving evidence into status or theme folders.
The [4 November architecture audit](audits/2026-11-04-topic-navigation/README.md)
records current coverage, repaired navigation and preserved path exceptions.

## Identifier namespaces

- `A0`–`A32` identify the current repository-wide question cards. A15–A18
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

Damani–Yokota 2026 (DY1) is **ungated**, outside the ordered reading roadmap,
as clarified by the owner on 2 November 2026. Its historical
`gate2_DY1_damani_yokota_2026/` folder is a provenance-preserving path exception,
not a Gate 2 assignment. Current article navigation and ROADMAP outside-source
metadata record that classification; frozen contracts and receipts are unchanged.

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
Dated analysis checkpoints belong with their report packages and are linked
from the documentation index; they do not form sections of the root README.
Its Start here section links to repository-wide indexes, not individual papers
or paper-specific results, branches or derived RQs. Those links belong in the
research-article and question indexes. Gallery discovery routes through the owning article/question indexes; the root
README does not maintain selected paper galleries or result summaries.

**Owner-requested methods showcase — 3 November 2026:** the root README also
embeds six existing measured figures in a two-column portfolio panel covering
UMAP, patient-paired expression, CUT&Tag, enrichment, spatial RNA and paired
RNA/accessibility. This is a bounded methods presentation, with captions and
links to the owning reports; study inventories,
complete galleries and RQ-specific status remain in their collection indexes.
No figures are copied or reclassified as qualitative schematics. The Weft pilot
description is excluded from the root README at the owner's request; its
intake records remain preserved.
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
