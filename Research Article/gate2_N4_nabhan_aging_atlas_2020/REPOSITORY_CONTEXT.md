# Repository purpose and article workflow

Inspected 3 October 2026 from fetched `origin/main`
`76dc9b47f72e774e51502162b2f8ba9d0dc02f17` (PR #131).
This is a planning map, not a new scientific status register.

## Purpose and ownership

The [root README](../../README.md) describes critical article reading and public
single-cell and multiome reanalysis to develop testable lung repair hypotheses.
The workflow is reading, paper analysis, question derivation, question-specific
investigation, cross-question synthesis and discriminating tests. Work can stop
or revise a hypothesis when data are inadequate or results oppose it.

| Repository location | Responsibility for this article |
|---|---|
| [Article roadmap](../README.md) and [ROADMAP.json](../ROADMAP.json) | Reading completion, requested folder label and planning status |
| This article folder | Source context, exposed reproduction and bounded exploratory candidates |
| [Question register](../../RESEARCH_QUESTIONS.md) and [RQ_Specified](../../RQ_Specified/README.md) | Existing global questions and any later evidence-supported continuation |
| [Research registry](../../analysis/research/registry.json) | Candidate ownership now; exact contracts and receipts when ready |
| [Research governance](../../docs/RESEARCH_GOVERNANCE.md) | Units, decisions, contracts, versioning and inference gates |
| [CLAIMS.md](../../CLAIMS.md) | Existing evidence grades; this plan changes none |
| [PROGRESS.md](../../PROGRESS.md) | Current handoff and unresolved dependencies |

## Existing evidence that constrains the plan

These are repository evidence locators, separate from the primary literature
in [the source note](NOTE_RECONCILIATION.md).

| Existing work | Consequence for Nb5 |
|---|---|
| [A3 current conditional package](../../docs/research_dossiers/packages_2026-10-03/A3.md) and [current W1 interpretation](../gate1_01_niethamer_2025/README.md) | An ageing reference is potentially useful, but age/processing and origin remain unresolved. Preserve negative CAMERA and ineligible ornithine results; no new pathway search to rescue them. |
| [Nb4 sequential results](../gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_SEQUENCE_RESULTS.md) | Separate captured mixture from within-state expression. C3, chemokine output and a whole-complement score remain different endpoints. |
| [A22 current result](../../RQ_Specified/A22_epithelial_identity_niche_response/reports/identity_amount_v2/RESULTS.md) | Weak transport is not repaired by an ageing association. Normal reference RNA cannot test an epithelial perturbation or secretion endpoint. |
| [Nb4 myeloid identity/state proposal](../gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/proposals/P05_immune_identity_state.md) | Useful measurement precedent; microglia are not interchangeable with lung myeloid populations or independent evidence for that proposal. |
| [A0 current pilot result](../../RQ_Specified/A0_conserved_epithelial_transition_program/reports/PILOT_V1_RESULTS.md) and [dossier](../../docs/research_dossiers/A0.md) | The failed operational transfer remains stopped; Nb5 is not a substitute cohort for post hoc signature rescue. |

The owner's CNS question is retained as an article-local candidate even though
the repository's main organizing question is lung repair. It does not receive
an A24 identifier or displace another question. Cross-organ agreement within
the same mice is repeated measurement, not independent replication.

## Checkout preservation

The normal checkout was `codex/workspace-ready` at the same revision, with
pre-existing changes in the GEO qualification script and its test and an
untracked `.claude/` directory. This package is developed in a separate managed
worktree on `codex/nb5-aging-atlas-plan`. Existing worktrees, ignored data,
frozen outputs, governance rules and validators are preserved.
