# Current project state

Update this before stopping work, every session. Current reports and the
research registry own scientific status; older checkpoints are history.

## Uniform RQ homes and reading order — 3 November 2026

All 33 canonical RQs now have one home under [RQ_Specified](RQ_Specified/README.md).
Every README begins with **Organizing Biological Q**, then **Literature context &
visual hypothesis**, followed by evidence and next steps. Seven new homes cover
A3, A4, A6, A7, A9, A17 and A18; each has local context, planning navigation and
the unchanged reviewed matte figure. Central dossiers retain the full scientific
argument. The live gallery is now under the RQ collection; dated guide/context/
gallery paths remain compatibility pages. Shared and paper-owned evidence stays
at its original paths.

The [migration record](docs/audits/2026-11-03-rq-structure/README.md) and its
validation record preserve all 33 hypothesis/artwork bindings and 21 asset-copy
crosswalk entries. Checks passed for all 33 README orders and contexts, preserved
analysis text in the 26 existing READMEs, all previous artwork/prompts, and 167
HTML references. Repository validation and the research gate passed against
refreshed `origin/main` (`179e413`). No numerical analysis, scientific
code, claim grade or governance rule changed. The branch is
`codex/rq-structure-review-20261103`; delivery uses a separate structure PR
because PR #159 is merged.

## RQ structure review — 3 November 2026

PR #159 is merged; `origin/main` is `179e413` and its tree matches reviewed
figure commit `1d4de41`. A tracked-file/registry review found 33 canonical RQs:
26 dedicated folders and seven dossier-led homes (A3, A4, A6, A7, A9, A17, A18).
`RQ_Specified` also contains the shared A5/A11 workspace and the historically
retained Yadav follow-up package. All 33 scientific dossiers remain central;
contexts and schematics follow the 26-local/seven-central split.

Confirmed navigation drift: the RQ index says 24 rather than 26 dedicated
folders, its figure index still describes SVGs, and the dossier index introduces
a 31-question historical review as current evidence. Dedicated folders are not
a maturity indicator: A24–A32 have no tracked local scripts/tables/reports
directories, although some link completed analyses elsewhere. Recommendation:
standardize one question home for every A ID and clarify separate ownership of
schematics, measured figures, shared work and frozen evidence. No restructuring,
scientific change, commit or PR publication was performed in this review. Next
step is a scoped migration plan if the owner requests implementation. The review
branch is `codex/rq-structure-review-20261103`; only this session log is changed.

## Matte figures applied to PR branch — 3 November 2026

All 33 reviewed matte PNGs replace the displayed SVGs on 66 owning question/context
pages. The old SVGs remain hash-preserved source artwork, not parallel displays.
The [RQ gallery](docs/research_dossiers/literature_context_2026-10-03/FIGURE_GALLERY.md)
is linked from the illustrated question index; the root README is unchanged.
See the [publication review](docs/audits/2026-11-02-rq-schematic-review/MATTE_PUBLICATION_2026-11-03.md).
Exact PNGs and selected edit prompts are tracked beside their owning schematics.

The registry/validator extension for primary PNGs is proposed for explicit review
in PR #159 before merge. It binds exact source artwork, hypothesis, prompt and
image hashes and preserves historical files; scientific-analysis requirements and
claim grades are unchanged. Validation passed: repository checks; 167 unit tests
(2 skipped); research gate against refreshed `origin/main` (`5eb710d`); compile
and whitespace checks; 33 PNG/source/hypothesis checks; 66 sole-display checks;
and 167 HTML references. Delivery uses existing PR #159 on
`codex/rq-schematic-quality-20261102`; no merge is authorized or performed. No
biological run was performed, and no scientific/data hold was removed.

## GPT matte figure drafts complete — 3 November 2026

All 33 RQ illustrations A0–A32 were generated and visually reviewed in the owner's
requested matte style. The local searchable gallery is
`.tools/rq_imagegen_20261102/GALLERY.html`; exact prompts, earlier versions, hashes
and per-image review decisions are retained beside it. See the
[production review](docs/audits/2026-11-02-rq-schematic-review/GPT_IMAGEGEN_REVIEW_2026-11-03.md)
for biological corrections and limits. Local validation passed for 33 distinct
decoded PNGs, 33 source bindings and 233 gallery references. Registered SVGs,
hypotheses and the root README remain unchanged. These local drafts have not been
committed or added to PR #159. No generation hold remains; existing data/scientific
holds are unchanged. Validation passed: 14,023 repository checks, the research
gate against refreshed `origin/main` (`5eb710d`), and whitespace checks. No
biological analysis was rerun. Tracked publication of these raster drafts remains
a separate integration step.

## Schematic publication — 2 November 2026

[PR #159](https://github.com/xorca0711/ravel/pull/159) is open against `main`.
Figure commit `a827db6` contains all 33 reviewed cellular SVGs, owning guide/context
updates, registry bindings and supporting audit records. The branch is
`codex/rq-schematic-quality-20261102`, published using verified `xorca0711`.
Publication validation passed: 14,021 repository checks, research gate against
refreshed `origin/main` (`5eb710d`), all 33 original/new SVG and hypothesis checks,
and the complete PR whitespace check. One whitespace-only issue in the historical
Claude handoff was corrected before push. No scientific/data hold was changed.
The PR is open for review; no merge was performed. The checkpoint below describes
the completed figure review before publication.

## Cellular SVG figures integrated — 2 November 2026

The fresh BioRender browser trial again failed at Reviewing prompt, so the
owner-authorized SVG fallback was used. All 33 original cellular figures A0–A32
are integrated into their owning guides, contexts and registry after actual-render
review. See the [all-33 review/index](docs/audits/2026-11-02-rq-schematic-review/CELLULAR_FIGURE_REVIEW.md)
and [redesign record](docs/audits/2026-11-02-rq-schematic-review/RAW_SVG_REDESIGN_2026-11-02.md).
The earlier handoff/stop/no-SVG preference is historical. No biology was rerun.
All 33 old figure and hypothesis bindings are retained in the audit baseline.

The owner's [biological-detail audit](docs/audits/2026-11-02-rq-schematic-review/BIOLOGICAL_DETAIL_AUDIT_2026-11-02.md)
corrected inappropriate receptor-symbol reuse, AT2 features in unspecified cells,
ARG1 location and lost named premises. Distinct comparisons and unresolved
mechanisms remain explicit. Editorial clearance is not scientific acceptance.

GitHub confirms PR #158 is merged: main is `5eb710d`, whose tree exactly matches
local `9e7fe4d`. Checks will use that content-equivalent base. Active branch/HEAD
remain `codex/rq-schematic-quality-20261102` / `862f333`; unrelated and prior
uncommitted work is preserved. Root README remains unchanged. Verification passed: 14,019 repository checks,
research gate against the current content-equivalent base, all 33 old SVG and
hypothesis hashes preserved, all 33 new hashes matched, and whitespace checks.
Nothing has been committed or pushed. Figure production has no remaining hold;
BioRender's generation failure and all existing scientific/data limitations remain
recorded. The technical chat is idle after handoff.

## RQ figures: BioRender account limit blocks production (2 November 2026, 13:41 KST)

A Claude Code session took over the [handoff](docs/audits/2026-11-02-rq-schematic-review/CLAUDE_HANDOFF_2026-11-02.md)
on `codex/rq-schematic-quality-20261102` (HEAD `862f333`, prior uncommitted
work preserved; nothing committed or pushed). The `X:/GitHub/ravel` checkout was
not modified.

- The BioRender connector is connected and returns the A3 draft as **Your file**.
  Two new jobs failed with `All preview generations failed`: A3 prompt revision
  3a and a one-sentence diagnostic prompt. That makes eight terminal connector
  failures, independent of prompt length, content or canvas context.
- The editor works through Claude in Chrome once its window is not minimized.
  The saved A3 canvas was reviewed directly: 14 of 50 objects, and it fails the
  revision 3 brief. No edit was made.
- **Blocker 1:** File > Make a copy returned "You've reached your illustration
  limit on your current plan". The first account (13 illustrations, free-plan
  50-object cap, watermark) cannot create new figures, so 32 RQs cannot start
  there and A3 can only be redesigned in place.
- **Blocker 2:** on a second account the owner signed in (displayed 준일 변),
  new figures can be created, but Leo still failed twice with the same message.
  So the illustration limit does not explain the AI failures; a free-plan AI
  entitlement gate is the leading, unconfirmed hypothesis. Generate Editable
  Figure there stopped at a BioRender data-use notice and a 24-hour AI access
  offer, both left unaccepted pending the owner's consent.

- **Owner steering (later the same session):** cell-level composition (cell
  types and crosstalk, not tissue structure), start from reference templates,
  and use the BioRender connector from Claude rather than browser control or
  hand-written SVG. A manual cell-level pilot on the second account
  (`6ae81519634432cb2a07dae2`) stopped unfinished at 8 of 50 objects. The
  connector then reported its connection **invalidated**; the owner must
  reconnect it before any connector generation.

- **Connector on the second account (14:21 KST):** after the owner reconnected
  it, two more jobs failed the same way (A3 prompt revision 4 with the
  "Origin and Development of Macrophages" template; a one-sentence diagnostic).
  Ten connector failures in total; generation fails on both free accounts
  regardless of prompt or context. Leading, unconfirmed hypothesis: an AI
  entitlement gate (the second account offers 24 hours of AI All Access).

- **24-hour AI access unlocked, still failing (14:31 KST):** with owner
  approval the second account's onboarding unlocked 24 hours of AI All Access
  and the AI data-use notice was accepted. Generation still failed on the
  connector (A3 revision 4 with template; one-sentence diagnostic) and in the
  browser (manifest A3 revision 3 verbatim reached "Generating 1 of 3
  previews", then errored). The entitlement hypothesis is refuted; a
  BioRender-side fault is suspected, not established. Twelve connector
  failures, zero generated images.

- **Template copy and Leo (14:38 KST):** a "Use as template" copy of
  "Origin and Development of Macrophages" was cleared to an empty page; Leo's
  pre-checks now run, but building fails for the manifest A3 prompt and for a
  one-line prompt alike. The second account has also hit its illustration
  limit (three illustrations). All BioRender AI building paths fail on both
  accounts; the cause is not established.

- **AI tools check (about 14:45 KST):** Restyle Icon hung without a result.
  BioRender's text steps work, but every image-generation step fails or
  hangs. Manual editor assembly and template copies still work.

- **New network re-test (about 14:47 KST):** connector and Restyle Icon
  failed the same way after the owner changed network connection; the local
  network is not the cause. Thirteen connector failures.

Zero new figures are completed, accepted or registered. **Next step needs the
owner:** re-probe generation later inside the 24-hour window (until about
14:26 KST on 3 November), raise the job IDs with BioRender support, or change
route. Then produce the A3
pilot against prompt revision 3 before batching. Details:
[implementation record](docs/audits/2026-11-02-rq-schematic-review/IMPLEMENTATION.md),
[ledger](docs/audits/2026-11-02-rq-schematic-review/LEDGER.md).

## RQ illustration work stopped; Claude handoff prepared — 2 November 2026

The owner explicitly stopped Codex figure work and requested a self-contained
handoff for a Claude session with only repository access. Both Codex chats are
stopped/idle, with no browser production or file write continuing. Start with the
[Claude handoff](docs/audits/2026-11-02-rq-schematic-review/CLAUDE_HANDOFF_2026-11-02.md)
and [all 33 figure briefs](docs/audits/2026-11-02-rq-schematic-review/CLAUDE_FIGURE_BRIEFS_2026-11-02.md).

All A0–A32 remain in scope. **Zero new BioRender figures are accepted or
registered.** A3 has an editable, unfinished draft; the other 32 have no new
completed custom art. The owner rejected equal space for an incidental control:
use the original A32 SVG's biological focus and compact comparison as a layout
reference, without transferring its ARG1 biology. All 33 layouts were reviewed;
A3 prompt v3 and A6/A7 layout amendments preserve previous revisions and all
scientific hypotheses. The latest A3 has a small uninjured reference and larger
post-injury macrophage, but the inset label, comparison connector and separate
readouts remain unresolved. It has no final visual clearance.

Six connector jobs and two distinct UI generation routes failed without images;
the historical missing-thumbnail pre-job failure is superseded. A PNG download
was attempted but not verified. Exact failures and remaining design/export/
integration holds are in the handoff and
[implementation record](docs/audits/2026-11-02-rq-schematic-review/IMPLEMENTATION.md).

Changes remain local and uncommitted on `codex/rq-schematic-quality-20261102`
(HEAD `862f333`). A later GitHub DNS check failed; last verified main is
`96e6a8d`. Original SVGs, registry, hypotheses and biological outputs are
unchanged. The next step belongs to the receiving Claude session: inspect the
current repo and actual capabilities/account, produce one acceptable focal
biological design, then proceed across all 33. No old-chat memory is required.

Handoff validation: all 33 briefs and local links verified; all registered SVG
canonical hashes preserved; repository validator passed 13,863 checks and the
unchanged research gate passed against last-verified main `96e6a8d`. These checks
qualify the documentation package, not artwork quality or scientific acceptance.

## Prior schematic implementation checkpoint — 2 November 2026

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
runs affected documentation link and whitespace checks only. The coordinator
successfully fetched `origin/main` again on 2 November 2026 and verified it remains
`96e6a8d033b11da2599e0fd5d91f87d16817f58c`.

The review covers **all 33 registered RQs, A0–A32**. A31, A3 and A28 are three
visual design pilot cases only, not a research shortlist or portfolio ranking.
The full portfolio remains in scope for redesign; pilot completion is not
portfolio completion.

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
