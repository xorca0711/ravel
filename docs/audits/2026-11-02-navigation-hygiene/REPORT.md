# Navigation hygiene and RQ registration audit

2 November 2026. Owner-requested correction, not a biological reanalysis.
Base main `96e6a8d033b11da2599e0fd5d91f87d16817f58c` includes merged PR #157.
The clean scoped branch is `codex/docs-navigation-hygiene-20261102`.

## Coverage and decisions

Initial inventory: 976 tracked Markdown files and 129 README files. Review
covered root entrypoints, article/question/dossier/figure indexes, roadmap and
registry classifications, current counts, moved-section backlinks and all
canonical guide mappings. Repository validation covers local links/JSON across
the repository. This is navigation/ownership hygiene, not a reread or new
scientific audit of every historical report or figure.

| Finding | Correction and owner |
|---|---|
| Root README highlighted selected Saxton/Arozamena galleries and results despite universal-navigation ownership | Removed the duplicate branch-gallery section and direct gallery shortcuts; use article/question collection indexes. Updated Saxton's sole backlink to the removed section. Actual galleries/assets remain in place. |
| Article index opened with repeated old execution checkpoints and duplicated study captions | Retained current study/gallery table and reading roadmap; moved older checkpoint prose to [same-level history](../../../Research%20Article/INDEX_HISTORY_2026-11-02.md), preserving relative links and wording. |
| DY1's legacy `gate2_` path implied roadmap membership | Owner explicitly classified it ungated. Current entrypoints and ROADMAP outside-source metadata now say so. Historical path is documented as an exception; no frozen path is renamed. Arozamena is also included in outside-roadmap metadata. |
| Agent entrypoint duplicated paper-specific execution status; PROGRESS had 2,212 lines | Replaced current entrypoints with concise routing/handoff and preserved both full previous snapshots with rebased links under docs/history. |
| Structure/figure summaries carried stale counts (28/31) and a fixed no-figure count | Reconciled current inventories; qualitative guides and earlier measured-file inventory are explicitly separate. Historical scientific figures and captions remain unchanged. |
| Illustrated canonical guide coverage was questioned | All A0–A31 were present once. A28/A29 diagram shortcuts still pointed to v1; corrected to registered v2 without altering either drawing. A31 was absent from the root question summary table; restored its navigation row. |
| Six recent article-local owners lacked guide navigation | Added a separate crosswalk. Following owner authorization and [scope review](RQ_ASSESSMENT.md), Yd1-P02 develops into proposed A32; all source IDs/runs remain. |

## A32 registration and scientific boundaries

The distinct proposed comparison estimates source-restricted myeloid ARG1
effects on matrix and mature epithelial output separately in one qualified
non-infectious design. [A32](../../../RQ_Specified/A32_myeloid_arg1_matrix_epithelial_recovery/README.md)
has a card, dossier, plan, dated primary-source context and versioned qualitative
SVG. The owner rejected the first text-box draft as insufficiently biological.
The active version 2 depicts myeloid source, enzyme/metabolites, fibroblast,
collagen fibres and alveolar AT2/AT1 epithelium. A same-coordinate/font preview
was checked visually; membrane/label overlaps were corrected. Solid published
premises and dashed proposed effects remain separate. The exact initial draft
is retained in documentation history and commit `cecdabad`; it was never a
merged registered guide. Only the current illustration enters the canonical
guide, without adding an infrastructure exemption or changing SVG validation.

The owner connected BioRender in ChatGPT Apps. Current Codex tool discovery
exposed no BioRender capability and the plugin search returned no match; this
does not prove that the ChatGPT connection failed. No BioRender creation/export
was tested or claimed. The replacement is original editable SVG artwork.

The guide binds source revision `cecdabad8e97a257d1954ecaa84b8af35cd5f97b`, its
complete dossier comparison text and the SVG hash. No empirical A32 effect,
novelty certification, automatic human acceptance or existing-RQ retirement is
claimed. Source qualification and laboratory/functional holds remain explicit.
Other candidates retain article-local scope or support existing RQs, as the
assessment explains. No biological execution is part of this documentation work.

## Preservation

All frozen contracts, code, receipts, measured figures, tables, raw sources,
legacy baseline and A0–A31 hypothesis/illustration bindings are preserved.
No validator, research gate, claim grade or execution boundary is weakened.
The structure document clarifies existing navigation ownership and the
owner-directed DY1 path exception. Registration and illustration use the
existing governance mechanism. The only validator edit extends its strict
expected identity sequence from A0–A31 to the owner-authorized A0–A32.
Targeted review confirmed exact order, missing/duplicate ID rejection and
unregistered-ID rejection remain enforced. Tests cover missing A31 and A32
separately and reject A33; no evidence criterion, SVG rule, contract or claim
boundary changes. This is an inventory amendment, not scientific acceptance.

Original working-tree snapshot SHA-256 before archive link rebasing:

- AI_CONTEXT.md: `f7d6c0be6e6e54e84f4781c1ce0525df0867ecba265e693c964244a90c7095e1`.
- PROGRESS.md: `04462f79ba22514903948d94c3b47dbc5e99240154856ac8ad08b872c0343880`.

These describe the original files, not hashes of the rebased archive copies.
Historical checkpoint statements are retained as history, not current instructions.
No ignored/untracked user data was cleaned, moved or deleted.

## Verification and delivery

Completed checks against refreshed main `96e6a8d`:

- Deterministic navigation audit: 33 canonical questions, 99 exact guide targets,
  all 37 source candidates retained, all 32 prior hypothesis/illustration bindings
  preserved, ordered roadmap fields unchanged and no selective root gallery links.
- Base-aware research gate: passed with no errors.
- Claim contract: all 18 numeric bindings passed; claims unchanged.
- Governance tests: 37 passed, including strict inventory rejection cases.
- Whitespace check against the current base: passed.
- Biological v2 illustration: visual preview checked and label overlaps corrected;
  archived first draft matches its original SHA-256 exactly.

The initial repository validation rejected only the old A0–A31 inventory
expectation (1 failure among 13,321 checks). The explicit inventory amendment
above resolves that mismatch. The first targeted-test attempt could not create
sandbox temporary fixtures; the authorized unsandboxed retry passed. Neither
failure was a biological result or a reason to weaken a scientific requirement.
Full repository validation after the amendment passed all 13,321 checks.
The scoped branch is prepared for a new PR (PR #157 is already merged); remote
CI and the final PR locator are checked on delivery.
No biological analyses were rerun.
