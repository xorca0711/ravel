# Current project state

Update this before stopping work, every session. Current reports and the
research registry own scientific status; older checkpoints are history.

## Schematic implementation — 2 November 2026

Technical chat `01a199c1-39af-7b92-bdf0-32711480c2eb` is implementing the
review on the existing `codex/rq-schematic-quality-20261102` worktree, starting
at `671c284`. Entry was clean; no upstream is configured. Main fetched at
`96e6a8d033b11da2599e0fd5d91f87d16817f58c`; PR #158 remains unmerged.

BioRender authentication is complete. The coordinator observed an
[Alveolar Epithelium template copy](https://app.biorender.com/illustrations/6ae7e244fcbb6b190eaacce7)
in the editor; the selected **BioRender** connector returned the same figure as
**Your file**, confirming the browser/connector account match for the human's
xorca connection. It is an uncustomized template copy, not a completed A3 figure.

Four earlier generation jobs failed. A later figure-context attempt using
`6ae7e244fcbb6b190eaacce7` failed before job creation because its thumbnail was
unavailable; unchanged arguments will fail again. Browser observation stalled:
recovery hit an automatic security-review timeout (not an unsafe judgment), and
the permitted single retry hit a CDP `Emulation.setFocusEmulationEnabled`
timeout. Do not bypass the approval gate or repeat browser/generation attempts
under this documentation handoff. Exact history and blockers are in the
[implementation record](docs/audits/2026-11-02-rq-schematic-review/IMPLEMENTATION.md).

The owner rejected the rough native SVG solution; three pilots remain local
backups only. The [pilot storyboards](docs/audits/2026-11-02-rq-schematic-review/BIORENDER_STORYBOARDS.md)
and [A0–A32 ledger](docs/audits/2026-11-02-rq-schematic-review/LEDGER.md) are ready
for real BioRender assembly. No artwork, registry or hypothesis changed.
The full checks recorded at `36dab95` remain valid; this status-only correction
runs affected documentation link and whitespace checks only. Integration base
last verified at `96e6a8d033b11da2599e0fd5d91f87d16817f58c`; no fetch is needed
for this record correction.

Next action: restore the approved browser session through its normal recovery
path, then open the existing figure in BioRender so a thumbnail can be generated
and customize/review it against the A3 storyboard. The user can also open the
same figure manually. Thumbnail availability and finished customization must be
verified separately; neither is established by account matching. Export/reuse
qualification remains before integration. No additional browser action, generation,
artwork integration, numerical analysis, push, PR rewrite or merge in this update.

## Registered RQ schematic review — historical checkpoint, 2 November 2026

The owner requested review of all registered questions and their schematics,
then a new technical chat for better biological illustrations using attached
connectors, preferably BioRender. The [33-question review and technical brief](docs/audits/2026-11-02-rq-schematic-review/README.md)
records question-specific boundaries and redesign needs. Every registered SVG
was rendered; all six contact sheets and selected full-size views were inspected.
No hypothesis, registered figure, source evidence or claim grade changed.

The scoped branch is `codex/rq-schematic-quality-20261102`, starting from
`9e7fe4d`, the clean PR #158 head. Refreshed main remains `96e6a8d`; #158 is
open and its earlier CI passed. Preserve the pending PR and unrelated work.
At that checkpoint BioRender was not exposed in the coordinating chat, so the
technical chat was asked to check its live tools and permissions independently.
That historical limitation is superseded by the implementation status above. The handoff forbids automatic molecular or
functional claims for questions with unresolved features/endpoints.

The then-planned next step was to launch the technical chat on this worktree,
starting with A31, A3 and A28, then cover the remaining registered questions. Use new versions and preserve old drawings. Keep precise connector,
license or biological holds; no numerical rerun or main merge is requested.

## Navigation hygiene and proposed A32 — 2 November 2026

The owner requested repository-wide navigation hygiene, ungated notation for
Damani–Yokota, verification of the illustrated RQ index, and assessment/registration
of distinct recent candidates. Work is scoped to `codex/docs-navigation-hygiene-20261102`
on freshly checked main `96e6a8d033b11da2599e0fd5d91f87d16817f58c`, which merged
PR #157. No unrelated work was present at entry.

The root README now routes through collection indexes; selective paper galleries
and paper-specific outcome prose are removed. The article index owns study/gallery
discovery, with repeated older checkpoint prose archived at the same directory
level. DY1 is explicitly **ungated** in navigation and outside-roadmap metadata.
Its historical `gate2_DY1_...` path remains for frozen provenance. Agent navigation
and this handoff are concise; prior snapshots retain their history.

All original A0–A31 guide entries were present. A28/A29 diagram shortcuts were
stale and now point to their registered v2 images. A31 was missing from the
canonical summary table; that omission is corrected. The
[six-candidate assessment](docs/audits/2026-11-02-navigation-hygiene/RQ_ASSESSMENT.md)
registers **proposed A32** from Yd1-P02's joint ARG1/matrix/mature-output question.
The [illustrated guide](docs/research_dossiers/literature_context_2026-10-03/README.md)
now has 33 canonical questions and a separate recent article-local crosswalk.
All 37 source candidates remain registered. Existing hypotheses/illustrations,
frozen runs and scientific acceptance states are preserved.

A32's literature refresh and biological v2 schematic are documented; the owner's
rejected text-box draft remains in documentation history. No biological analysis
was run. BioRender was connected in ChatGPT Apps, but no BioRender tools were
exposed in this Codex chat; the replacement is original editable SVG artwork. Its empirical effects remain held for linked model/data,
qualified source restriction, mature endpoint, actual biological units and
precision. DY1/Arozamena/Saxton measurement work stays with its source owners;
existing RQ links do not turn it into mechanism or functional evidence.

## Validation and delivery

The [audit](docs/audits/2026-11-02-navigation-hygiene/REPORT.md) records navigation
coverage, preservation, checks and residual limitations. Navigation reconciliation,
base-aware research gate, 18 claim bindings and 37 governance tests passed. The
strict canonical-sequence validator was extended to A0–A32 with rejection cases
retained. Full repository validation passed all 13,321 checks.
[PR #158](https://github.com/xorca0711/ravel/pull/158) is open for review; its
GitHub checks own current remote CI status. No main merge has been performed.
No numerical rerun, existing PR rewrite or main merge is part of this work.

## Current research navigation

Use the [paper index](Research%20Article/README.md), [question workspaces](RQ_Specified/README.md),
[dossiers](docs/research_dossiers/README.md) and
[remaining-work ledger](docs/research_dossiers/REMAINING_WORK.md). The reviewed
Arozamena/Saxton work is merged through PR #157; its exact source/state/function
holds remain in the owning reports. Reopen a held analysis only for its named
new source/design evidence; registration does not supply missing measurements.

## Preserved handoff history

The [pre-cleanup handoff](docs/history/2026-11-02-navigation-hygiene/PROGRESS.md)
retains the complete earlier checkpoint text with links rebased for its archive.
The [prior agent entrypoint](docs/history/2026-11-02-navigation-hygiene/AI_CONTEXT.md)
is also retained. Dated pending/authorization statements there describe their
original revisions and do not override current result reports.
