# Topic navigation and architecture review

4 November 2026. Owner-requested application of overlapping biological-topic
navigation and review of the existing folder architecture. Base: main `3f70489`,
which contains merged PR #165. Work is isolated on
`codex/topic-navigation-20261104`; earlier dirty review worktrees are preserved.

## Implemented navigation

The [shared topic map](../../RESEARCH_TOPICS.md) defines nine overlapping routes
across all 33 canonical question homes and 18 paper packages. The
[RQ index](../../../RQ_Specified/README.md) and
[article index](../../../Research%20Article/README.md) expose matching tag columns.
The root README, documentation index, agent entrypoint, question register,
dossier index and historical guide route readers to that shared map.

Tags describe biological scope, including proposed questions; they are separate
from scientific findings, execution status, reading status and acceptance.
Topic membership does not claim that every linked paper directly supports every
linked RQ. Evidence connections remain in the owning contexts and reports.
No physical evidence directories, question IDs, hypotheses, figures, contracts,
scripts, outputs or source-reading records are moved or revised.

## Architecture findings and disposition

| Finding | Resolution |
|---|---|
| The earlier topic routes listed 21 of 33 RQs. A4, A7, A8, A11, A13, A15, A16, A18, A19, A20, A22 and A23 were absent. | All 33 now have explicit tags, with overlapping memberships and links to the same stable homes. |
| RQ and article discovery did not share a complete topic vocabulary. | One topic map connects both collections; all 18 paper inventory rows have tags. Existing result and reading columns are preserved. |
| An earlier conversational suggestion placed A16 among immune-effector questions. | A16 concerns prospective epithelial CD177 response context; its implemented tag is epithelial states. A24 remains bladder stromal/urothelial biology, with ageing, epithelial and stromal tags. |
| The root README and dossier index still routed current status through the historical remaining-work ledger. | Current-status links now use PROGRESS and current question arguments; dated package/ledger links remain explicitly historical. |
| The documentation index called 7 October the latest portfolio analysis checkpoint despite later reviewed work. | It is labelled a historical integrated checkpoint, with current 4 November navigation above it. |
| The architecture page routed open gaps through the September audit without dating that status. | The audit and six-package roadmap are historical checkpoints; current owner arguments and amendments carry later work. |
| The architecture page said A15 registration remained pending, although A15 is in the canonical register. | ID registration is distinguished from proposed scientific status and owner acceptance; no claim grade is changed. |
| The dossier index presented source-mapping deferrals from 3 October as current. | The deferral is scoped to that checkpoint; owner pages supply subsequent work and remaining limits. |
| Primary source archive discovery was absent from the main article study route. | The article index and topic map link the archive and explicitly distinguish it from a study package. |

## Physical layout retained

| Collection | Current structure | Interpretation |
|---|---|---|
| `RQ_Specified/` | 33 registered question homes plus `A5_A11_shared_component_contract/` and `Yadav_followups_20261031/` | The two supporting workspaces are shared definitions/history, not extra canonical RQs. A32 owns the registered joint outcome question; historical Yd1/Wg work keeps its owner. |
| `Research Article/` | 18 paper packages, `epithelial_state_specificity/`, and `Primary/` | The latter two are a cross-study analysis and source archive, not two additional papers. |
| `docs/research_dossiers/` | One dossier per A-series question, with dated package/review directories | Dossiers develop the scientific argument; dated directories preserve historical scope rather than becoming active status registries. |
| `analysis/` | Shared methods, figures, contracts and immutable runs | Cross-question evidence stays at its registered location; topic browsing does not duplicate it beneath every RQ. |
| `archive/` and `weft_intake/` | Historical artifacts and the separately labelled pilot intake | Preserved; no topic folder is substituted for their role. |

DY1 remains **ungated** despite the historical `gate2_DY1_...` folder. Nb4/Nb5
folder aliases and shared workspace names remain documented provenance
exceptions. Four reading-roadmap entries have no local package; this is an
explicit roadmap state, not a missing executed-analysis folder. Current artwork
is still distinguished from measured-result figures by existing ownership.

This is an architecture/navigation audit, not a fresh scientific validation of
every historical artifact. No new biological analysis, literature search,
portfolio ranking, hypothesis retirement or execution queue follows from it.

## Validation

- **854 focused checks passed:** all 33 RQ and 18 paper tag sets match the topic
  map; the 51 original inventory rows retain their scientific/evidence cells;
  all 99 registered RQ README/context/image files are byte-identical to main.
  The 37 article-local plans, 163 contracts and 155 receipts have their registered
  paths, and the physical-directory inventory matches the ownership accounting.
- **16,870 repository checks passed:** local Markdown paths and anchors, JSON
  artifacts, claim summaries and existing numerical bindings pass the unchanged
  `python analysis/scripts/validate_repository.py` check.
- **Provenance gate passed, zero errors:**
  `python analysis/scripts/research_gate.py check --base 3f7048963857097524b0eeab18fd06369e5c5da6`.
- **Whitespace check passed:** `git -c core.autocrlf=false diff --check`.
  Main was fetched again and remained at the same base.

Sixteen public Choi output files were checked against the existing release lock;
15 missing files were copied exclusively from the already validated local
publication checkout to support the checks. No new download, scientific run or
overwrite was required. Registered images, scientific owner documents, roadmap,
registry, governance and validators are unchanged. Validation establishes
navigation/provenance consistency, not scientific acceptance or biological
resolution. No additional physical relocation is needed within the audited
ownership map; legacy names remain documented exceptions.
