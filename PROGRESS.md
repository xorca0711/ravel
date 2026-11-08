# Current project state

Update this before stopping work, every session. Current reports and the
research registry own scientific status; older checkpoints are history.

## Saxton reading and computational assessment - 8 November 2026

Reviewed the current Sx22-P01 results, amendments, source-panel corrections and
both published papers against fetched main `32ab85e`. The
[reading comparison and feasibility note](docs/research_reviews/2026-11-08-saxton-reading/README.md)
explains IL-22 intracellular STAT recruitment plus tissue selectivity, retains the
RNA attenuation/panel-sensitivity qualifications, and links the requested
[stepwise IL-10 plan](docs/research_reviews/2026-11-08-saxton-reading/IL10_ANALYSIS_PLAN.md)
and [IL-22 follow-up assessment](Research%20Article/gate3_08_saxton_2021_il22/FOLLOWUP_ASSESSMENT_20261108.md).
The latter proposes a bounded Osmr RNA comparison grounded in a refreshed primary
literature review. Plans are unexecuted; no biological rerun or new accepted RQ.
Next: qualify IL-10 sample-code/donor/design metadata and establish its article-local
owner before a frozen contract; qualify Osmr mapping before any Sx22 amendment.
Existing IL-22 unit, raw-function and persistence holds remain endpoint-specific.
Work is isolated on `codex/saxton-reading-assessment-20261108`; unrelated original
checkout edits are preserved. Final validation passed against refreshed unchanged
main `32ab85e`: 17,155 repository checks, the base-aware preservation/research gate,
23 local links in the new planning documents and whitespace checks. The unchanged
claim manifest's 18 numeric bindings also passed. Initial gate
failures were checkout CRLF drift and missing published display outputs: 21 untouched
files restored to exact recorded Git bytes; 15 outputs restored from local copies
against the release manifest hashes, without a scientific rerun or validator change.
External settings unchanged;
NCBI direct-page challenges were supplemented by indexed primary records/local PDFs.

## DuPage RQ placement and rationale audit — 7 November 2026

Owner requested review against the earlier reframing chat, published-target
literature checks, three distinct RQ homes, and removal of proposed comparisons
from the measured gallery. At the owner's later instruction, this work builds
on PR #168 (`4ae13c0`) rather than a separate PR; main is `32ab85e`.
[Derivation, overlap scan and corrections](Research%20Article/gate3_09_dupage_2015/rq_derivation/README.md)
now links proposed A33–A35. Current inventory is 36 RQs, 38 article-local
candidates and 19 paper packages. All A0–A32 identities and hypotheses remain.

The refresh found a missed CCR2/CD25 Il2ra-background counterexample and corrected
causal-sounding loss/gain wording. It does not invalidate the numerical results.
Figure 4 is preserved as a historical proposal outside the measured gallery;
Figures 1–3 and 5–6, contracts, scripts and receipts remain unchanged. New
qualitative diagrams live with the question homes, separate from measured plots.
No biological rerun, target validation, scientific acceptance or laboratory
execution is implied. Full CCR2 supplements, the IGFBP4 2017 full methods,
actual experimental models and biological-unit precision remain unresolved.

**8 November approved revision:** the owner approved matching neighboring RQs.
A33–A35 now follow A28/A31/A32's reasoning order, with local primary-source tables,
existing measured-value summaries, explicit narrowing assessments and staged
plans. Three biological matte illustrations and exact prompts replace the displayed
workflow drafts, which remain as provenance sources. The common derivation and
literature audit now live in the DuPage article's `rq_derivation/` directory;
there are 36 question homes and two supporting workspaces under `RQ_Specified/`.
The A34 link is repaired. No biological rerun or hypothesis change was needed.

Validation passed: 17,481 repository checks and the provenance gate against
refreshed unchanged main `32ab85e`; 167 prior tests remain valid (two skipped),
including exact RQ inventory rejection cases. All 18 displayed values match the
frozen tables. Earlier 33 cards/guides and original registry evidence are preserved;
three selected PNGs were visually reviewed and their provenance registered. The validator's expected sequence now
includes A33–A35 while retaining equality/order and rejection checks; this inventory
assertion and the interpretation changes are explicit PR review items. The revisions were committed as `2631fc9` and pushed onto the existing PR #168
branch, preserving its source-inventory work. Both GitHub workflows passed for
that revision. The PR title/body now describe the combined scope and explicit
review items; it remains open and unmerged. GitHub identity is verified as
`xorca0711`. Next scientific work is the comparison/model qualification in each
RQ plan if the owner chooses to pursue it; no automatic analysis queue is created.
External settings are unchanged and were not audited.

## Source inventory publication and documentation hygiene — 7 November 2026

Owner authorized updating the inventory to current main, opening a PR, and
cleaning the root README, documentation structure, links and superseded roadmap
routes. Main is `32ab85e` after merged PR #167; the scoped branch integrated it
at `4d6f96c`. [Current reconciliation and artifacts](docs/audits/2026-11-07-public-data-inventory/RECONCILIATION_V2.md).
DuPage GSE58998/GSE55773 and the later executed GSE262130 comparison are now
included. V1 remains preserved; v2 records 544 accession references and 4,197
local cache files / 74.04 GB. Root raw_data remains 955 files / 34.52 GB.

Current owner routes replace historical ledgers presented as current work.
Collection counts are 33 RQs, 38 article-local candidates and 19 paper packages.
The article README/roadmap agree on DuPage's follow-up; old gates/reading order,
frozen scientific evidence and root measured figures remain preserved.
GitHub connector and CLI identities are verified as `xorca0711`. Validation
passed: 772 focused navigation/count/preservation checks, 17,230 repository
checks, 167 unit tests (two skips), compilation, whitespace checks and the
base-aware provenance gate against `32ab85e`. The gate caught a hash-bound
`.gitignore` comment edit; the file was restored exactly and its guidance kept
in the docs. Seven newly merged DuPage scripts also required exact Git bytes
locally after Windows checkout line-ending conversion. No frozen input or
validator was changed. [PR #168](https://github.com/xorca0711/ravel/pull/168)
is open against main; [remote checks](https://github.com/xorca0711/ravel/pull/168/checks)
are the live CI record. Next: review and merge only with owner authorization.
No external settings are unresolved, and no merge was performed.

## Initial source inventory checkpoint — 7 November 2026

The following paragraph records the first local delivery before PR #167 merged;
the reconciliation above supersedes its integration and publication status.


Updated the [central dataset list](docs/DATASETS.md) and its
[source-use additions](docs/DATASET_UPDATES_2026-11-07.md) on isolated branch
`codex/public-data-inventory-20261107`, based on freshly fetched main `dcee4b6`.
[Audit, scan scope and artifacts](docs/audits/2026-11-07-public-data-inventory/README.md).
The original root checkout and unrelated edits remain preserved.

The tracked-text census records 530 accession identifiers, including metadata,
search leads and aliases; it does not claim 530 utilized cohorts. The local
source/reference census contains 4,181 files / 74.04 GB across 15 cache roots;
the project-root `raw_data/` alone contains 955 files / 34.52 GB in 33 folders.
The original 51-file inventory remains historical and unchanged. Newer DuPage
use is recorded separately at its inspected branch revision, not merged.

Inventory/link checks, required archive/claim checks and 167 unit tests passed
(two environment/platform skips with an explicit writable temporary directory).
Compilation passed. Fifteen published outputs were restored from existing
hash-matched local copies; fourteen frozen checkout files were restored to exact
Git bytes to resolve Windows line-ending mismatches, without semantic changes.
Final validation passed 16,934 repository checks and the unchanged provenance
gate against refreshed main `dcee4b6`; whitespace checks passed. No biological
reruns, source downloads, scientific-status changes, commit, push or merge were
performed. The inventory update is complete locally and remains uncommitted in
the scoped worktree. Future changes to caches or unmerged research require a
new snapshot/reconciliation; no external setting is needed for this update.

## Biological review and executed candidate continuation — 7 November 2026

[PR #167](https://github.com/xorca0711/ravel/pull/167) merged on 7 November at `32ab85e`. Biological review,
source qualification and three experimental question cards are committed.
The [numerical candidate follow-up](Research%20Article/gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md)
executed from frozen `8f7fa76`: all four candidate genes and three anchors were
available in the selected Peeters rlog matrix. Tigit/Prdm1/Ccr2 reverse direction
between fresh and cultured gain contexts; Igfbp4 stays lower. No target is
validated, accepted or removed. Two new figures have been visually inspected.
Independent checks passed for 84 source values, 455 contrasts, 35 ranges/sign
records, six figure hashes and the new receipt. Repository validation passed
17,122 checks; refreshed main is unchanged at `dcee4b6`. The final preservation
gate and both GitHub workflows passed for the published results at `0578490`.
All 14 expected new outputs and the receipt match Git byte-for-byte. The original contract-byte
issue was corrected with article-local attributes; frozen pilot inputs and all
historical outputs remain preserved. GitHub identity verified as `xorca0711`.
Results are merged; the validation/revision statements above describe publication. Future biological work requires the protein/response
qualification in the candidate cards. TIGIT animal/source mapping remains unknown;
no wet-lab experiments or scientific acceptance are implied.

## DuPage-first target-screen follow-up — 7 November 2026

Completed the owner-requested DuPage-first exploration; Zhang 2026 is optional.
[Report and proposal](Research%20Article/gate3_09_dupage_2015/TARGET_SCREEN_RESULT.md)
and [four-figure portfolio](Research%20Article/gate3_09_dupage_2015/TARGET_SCREEN_FIGURES.md)
own details. V1 exposed small-RNA-label dominance in poly-A RNA-seq. A frozen
amendment retained v1 and qualified 9,845 coding loci, yielding 32 displayed
candidates. Proposed routes: TIGIT–PRDM1 inducible output, CCR2 localization
versus fitness, IGFBP4 buffering versus compensation. Literature includes
nearest precedent and contrary findings; no novelty or target validation claimed.

Three new frozen contracts/receipts preserve screen v1, annotation v2 and four
figures (PNG/PDF/SVG). Independent arithmetic/annotation checks and plotted-value
checks passed; all four figures visually inspected. Final repository validation
passed (17,058 checks and research gate against refreshed main); details are in
the [validation note](Research%20Article/gate3_09_dupage_2015/TARGET_SCREEN_VALIDATION.md).
Next: qualify candidate protein/output under common activation, then specify
the selected functional perturbation, biological units and feasible precision.
No new RQ/claim grade, independent replication, paid compute, wet-lab work or
external setting change. Local scoped commits only; original frozen evidence
and unrelated work preserved. Refreshed main remains `dcee4b6`.

## DuPage S0–S6 complete within qualified scope — 7 November 2026

One technical chat completed all stage dispositions on the isolated branch
`codex/dupage-stepwise-plan-20261107`; the old root checkout is untouched.
[Current report](Research%20Article/gate3_09_dupage_2015/RESULTS.md),
[ledger](Research%20Article/gate3_09_dupage_2015/STAGE_STATUS.md) and
[validation](Research%20Article/gate3_09_dupage_2015/VALIDATION.md) own details.
S0–S3 ran under four frozen contracts; receipts, arithmetic, PCA/mapping and
figures were checked. S4 was not informative beyond the published broad
loss/gain comparison; S5–S6 completed endpoint/next-question synthesis.

11 retained libraries, 11,614 eligible loci. Low/high genotype RMS ratio 1.087
but 0.812–1.235 under library omission. External chromatin mapping covers 1,180
loci, interaction rho 0.162 (single-gene domains 0.149). Mixed results retained.
Arvey inputs recovered; 2015 supplement/exact Foxp3 sets, mouse/pool identities
and raw functional data remain unresolved. No count/population inference.

Next scientific decision: develop a common-activation HET/KO comparison to
separate regulation within viable lineage-labelled cells from Foxp3 loss and
selective death. Target, precision and laboratory feasibility remain unknown;
this is a proposal, not an accepted RQ. Canonical questions/grades/frozen assets
and Niethamer/D1 gate preserved. Local commits only; no push/PR/merge, external
message, paid compute or wet-lab work. External settings unchanged/unaudited.
Final validation passed against refreshed unchanged main dcee4b6: 17,000
repository checks; 167 tests OK (2 skipped); compilation and provenance gate.
Sandbox test-temp failures were resolved with checkout-local scratch space.

## Historical DuPage S0 checkpoint — 7 November 2026

S0 executed under its frozen contract and passed receipt/source arithmetic checks.
[Current stage ledger](Research%20Article/gate3_09_dupage_2015/STAGE_STATUS.md) and
[S0 result](Research%20Article/gate3_09_dupage_2015/S0_RESULT.md) own details.
23,102 unique gene-labelled spans match across all 12 libraries; 22,997 are OK
in the 11 retained libraries. ENA links 24 runs to 12 libraries; mouse/pool and
pairing identities remain unknown. Descriptive FPKM is eligible; count/population
inference is held. Article XML recovered exact supplement names, but downloads
remain challenged/forbidden; no claim of source-wide absence. Next: frozen S1
adapted reconstruction, then result-guided S2–S6 in this single technical chat.
The temporary separate-chat interpretation was superseded by the owner's latest
instruction. No push, external settings change, claim promotion or wet-lab work.

## Historical DuPage execution authorization — 7 November 2026

The owner requested a separate technical chat in Ravel to launch every planned
Dp1 step, explain progress during execution, and report/adopt justified
between-step adjustments based on actual results. This supersedes the earlier
planning-only scope. It authorizes sequential source qualification, eligible
reproduction/descriptive analyses, qualified inferential or external comparisons,
functional-evidence synthesis and final question development under the existing
AGENTS and contract/runner rules. Conditional steps must receive an evidence-based
execution/hold/not-informative disposition, not forced unsupported analyses.
Necessary local commits of scoped plans, frozen contracts, code and results are
part of compliant execution; push, PR, merge, external messages, wet-lab work,
paid compute and scientific acceptance are not included.

The technical chat will use the existing isolated DuPage worktree and own its
execution files and PROGRESS updates. The originating chat monitors and explains
stage results and adjustments. It does not run a competing analysis. Preserve
the original plan and all outcomes; substantive changes use prospective versioned
amendments and explicit exposure records.

## Historical DuPage reading review and plan — 7 November 2026

Owner reading is complete. The [Dp1 package](Research%20Article/gate3_09_dupage_2015/README.md)
connects the annotated published paper, private reading notes, verified GSE58998
file structure and bounded current literature to a seven-step biological plan.
The source has 12 libraries but 11 retained samples (2/3/3/3); merged FPKM is
four condition estimates, and the archive contains per-library FPKM, not counts.
The plan distinguishes state-associated regulation, chromatin consistency,
identity retention, survival and functional tissue control. Dp1-P01 is article-local;
all 33 canonical questions, frozen evidence and the Niethamer/D1 gate are preserved.

Work is isolated on `codex/dupage-stepwise-plan-20261107` from fetched main
`dcee4b63e11abd27fe2bbc679993b288e913565e`; root-checkout edits are untouched.
No numerical analysis or Notion write was performed. The separate 2015 supplement
was not recovered through the attempted publisher/archive routes. Next: qualify
sample/pool/pairing and feature identities under Dp1-S0, then choose descriptive
FPKM reconstruction or a separately qualified count-based route. Exact external
chromatin references and raw functional data remain dependent-stage holds.
Validation passed: 16,906 repository checks; 167 tests completed (two skipped);
Python compilation, claim/archive verifiers and the research provenance gate
against refreshed unchanged main `dcee4b6`. Fifteen missing hash-locked published
outputs were restored (16 verified); fourteen historical files needed exact HEAD
bytes restored after newline-only checkout drift. They have no content diff;
Git may still report stat/line-ending dirtiness under `core.autocrlf=true`.
All canonical question/guide/contract/receipt records, existing article candidates
and roadmap gate rules are unchanged. Only Dp1-P01 and paper-9 navigation/status
were added or updated. Work remains local and uncommitted; no push or PR was made.
External branch-protection settings and scientific acceptance were not changed
or audited.

## Topic navigation and architecture review — 4 November 2026

Applied the owner's overlapping-topic navigation across all 33 RQs and 18 paper
packages, on `codex/topic-navigation-20261104` from merged main `3f70489` (PR #165).
The [topic map](docs/RESEARCH_TOPICS.md) and collection tag columns keep biological
scope separate from current evidence and reading/execution status. Twelve RQs
missing from the earlier topic routes are included. Current-status links no
longer route through historical package ledgers; stale A15 registration and
October-current wording are clarified. A16 is correctly tagged as epithelial.
[Architecture findings and validation](docs/audits/2026-11-04-topic-navigation/README.md).

The physical layout remains 33 RQ homes plus two supporting workspaces, and 18
paper packages plus a cross-study module and source archive. No evidence paths,
owner README/context/figure bytes, hypotheses, registry, roadmap or governance
are changed. Existing dirty review worktrees are preserved. The 854 focused
coverage/preservation checks, repository link/artifact validation and provenance
gate against refreshed main passed. There are no remaining navigation/provenance
holds in this scope. This documentation work starts no biological analysis queue.
The owner subsequently authorized commit, push and a PR for this reviewed scope.
Publication uses `X:/GitHub/ravel/.worktrees/topic-navigation-20261104`; the PR
records its published head and remote checks. Earlier local/uncommitted handoff
statements describe the pre-publication checkpoint. Merge is a separate decision.

## RQ restructuring publication — 4 November 2026

The owner authorized commit, push and a PR for the reviewed all-33 restructuring
and validated fixes. Publication uses the isolated branch
`codex/rq-reasoning-restructure-20261104`, with current main `acefbced` integrated.
The original C: review worktree remains preserved. The reviewed screening
dependencies missing from main are retained in separate commits so result links
and frozen provenance remain usable. [Integration scope and validation](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/PUBLISHING.md).
Restructuring/fixes are committed at `0bb57ef`; reviewed dependencies are in
`57f6dea`, following the main reconciliation at `1b7049c`. Fresh isolated-tree
validation passed 16,450 repository checks, 170 unit tests (one Windows skip),
required archive/claim checks and the research gate against `acefbced`. Fourteen
historical checkout files needed their unchanged Git bytes restored to match
frozen hashes; no scientific source or validator was changed. All 255 pending
source-file contents were preserved during export.
No new biological analysis or policy change is introduced by publication, and
the resulting PR is not authorized for automatic merge. Earlier no-push and
uncommitted statements below describe their original review checkpoint.

## Portfolio reasoning restructuring — 4 November 2026

**Follow-up findings validated and corrected.** The owner's requested recheck
found A9's comparison already proposed in the earlier biological-link map; the
defect was its omission from current owner arguments. That connection is restored.
A3's ambiguous axis phrase now states only the measured RNA restriction. Seventeen
dossier preambles and the historical ledger now distinguish current work from
dated package status. [Validated scope and repairs](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/FOLLOWUP_REVIEW.md#validated-scope-and-repairs).
This does not establish a new mechanism, nominate a target, or mean that every
RQ has a fully developed next experiment. The prior coverage milestone remains
valid; its blanket substantive-completion wording was qualified. No biological
run or hypothesis change was made. Fresh validation passed **16,449 repository
checks** and the provenance gate against refreshed main `acefbced`; 224 protected
sections, 36 assets and all 33 registered hypothesis/image pairs are preserved.
The three focused corrections are complete, with scientific unknowns retained.
Raw evidence and unrelated local work remain preserved; changes are uncommitted.

The owner approved the cross-chat direction after reviewing this coordinator's
explanation, including useful new/versioned figures. A fresh technical chat,
**Ravel RQ reasoning — A5 pilot and rollout**
(`01a1a468-11ec-7533-bc5c-3b82d00c7b3c`, local), completed its delegated queue.
[Approved plan, all-33 work order and ownership](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/README.md).
The purpose is to expose defensible question → comparison → result → changed
interpretation → next-decision reasoning, including negative/diagnostic findings.
No mandatory target count or causal discovery is imposed. Registered hypotheses,
figures and frozen evidence remain preserved; substantive changes are separate
proposals. This task does not restart old numerical queues or request push/merge.

The authoritative research worktree remains `codex/tool-assisted-screening-review-20261103`
at `0b67a80`, with no upstream and pending reviewed local research. The saved
project root `X:/GitHub/ravel` was verified at older `78320a1`; all edits use this
worktree. All 33 README/context/dossier narratives have completed scientific and
editorial cross-review. [Coordinator review and batch evidence](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/COORDINATOR_REVIEW.md).
The [all-33 rationale assessment](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/RATIONALE_ASSESSMENT.md)
distinguishes supported findings, exploratory leads, negative/measurement
diagnostics and untested proposals without treating uncertainty as random noise.
Collection navigation and the current register/architecture pointers are aligned.
Existing measured figures were reused with bounded captions; no new images or
biological runs were needed. Registered hypotheses, illustrations and frozen
evidence remain unchanged. Final validation passed **16,391 repository checks**
and the provenance gate against refreshed main `acefbced`; all 33 registered
hypothesis/image pairs, required opening headings and visible rationale sections
passed the scoped preservation check. [Validation record](docs/research_reviews/2026-11-04-portfolio-reasoning-restructure/COORDINATOR_REVIEW.md#final-integration-validation).
Biological holds remain question-specific and do not imply unfinished editorial
work. No commit, staging, push or merge was performed for this task.

## Research skills and plugin audit — 4 November 2026

Inventoried 212 SciAgent skill files and 95 recently modified AI/ML skill files;
reviewed selected research workflows and live connector capabilities. The
[usage review](docs/research_reviews/2026-11-03-tool-assisted-screening-review/NEW_SKILLS_USAGE_REVIEW_2026-11-04.md)
maps useful annotation, interaction, motif, multiomics and figure tools to current
biological decisions. Generic autonomous-pivot and always-mechanistic instructions
must not override repository governance. Workbench's local runtime currently
discovers no workflow controller; existing Python research runs remain separate
and unaffected. Package metadata is recorded, not asserted as tested readiness.
No installation, external figure job, new analysis or governance change followed
from this audit. The technical chat received the usage boundaries.

A3 (`43f633f`) and A27 (`0b67a80`) now pass independent numerical, visual and
biological report review: 374 and 358,840 reconstruction checks respectively,
zero numerical discrepancy, 33 verified hashes and 84 report checks. All three
figures passed. [Review and exact limits](docs/research_reviews/2026-11-03-tool-assisted-screening-review/COORDINATOR_REVIEW.md).
Owner-context synthesis is now complete and reviewed across A3/A27 READMEs,
literature contexts, dossiers and the DY1-P02 source connection; both result
reports link the review. The Pparg trajectory wording and DY1 inference limit
are corrected. All 194 synthesis/report links resolve; protected framing and
registered illustrations are preserved. Both receipt verifications and the
provenance gate against main `acefbced` pass. A3/A27 join A5/A31 as complete
reviewed bounded branches; broader unresolved biological questions remain explicit.
The three audit/status documents passed 74 local-link checks, and the
repository validator passed 15,931 checks; no biological analysis was rerun for
this documentation audit. These status updates supersede prospective wording below without
claiming A3 coordinator acceptance.

## Authorized restart after guidance merge — 4 November 2026

[Agent-guidance PR #164](https://github.com/xorca0711/ravel/pull/164) merged into
main as `acefbced` after both remote CI workflows passed. Its isolated three-file
change passed 46 local governance tests, 15,328 repository checks, local links
and the provenance gate. A fresh Windows checkout needed exact existing Git
bytes restored for 14 newline-only hash mismatches; no scientific content changed.
The research checkout uses the merged guidance, and the existing technical chat
confirmed restart under the owner's explicit instruction. Earlier halt records
below are historical; all modified/untracked research evidence remains preserved.

A5's approved branch is complete: exact source-map review, frozen numerical
display (`53820f0`), rendering-only correction (`e076aeb`), independent numerical/
visual/report review, and current README/context/dossier synthesis. All 27,324
independent numerical checks passed (maximum discrepancy 3.553e-15 pp); 85 local
links and preserved framing-marker contents passed final synthesis checks.
The result narrows toward junction/polarity-associated RNA with selected matrix
context, retaining heterogeneous signaling/matrix members and negative original
transport means. No assembly, maturation, repair-function or independent-replication
claim follows. [Result and figures](RQ_Specified/A5_developmental_programme_reuse/reports/FEATURE_CONTEXT_DISPLAY_V1_RESULTS.md)
· [Coordinator review](docs/research_reviews/2026-11-03-tool-assisted-screening-review/COORDINATOR_REVIEW.md).

A3's recovered source/methods passed bounded review and report biological
replication, but exact preparation/batch sharing and control harvest alignment
remain unknown. The SI identifies Salmon counts, so actual count/estimate
semantics must be qualified rather than imposing a raw-integer-only rule. The
six-library RNA-context specification has now passed exact source/hash/mapping
review and is cleared for frozen descriptive execution; numerical/visual/report
review must precede current A3/DY1 synthesis. A27's 13,332-row source/annotation
join passed independent review; the next bounded qualification covers CD8 label
construction and per-mouse/state chain eligibility before choosing clone
conventions and an endpoint. Its versioned 354-row receptor-only mouse-metadata
correction passed independent review; those cells remain outside RNA-state
denominators. The exact nominal-source-code concentration proposal is now cleared
for prospective frozen execution, with single-pair primary/complete-set sensitivity,
full support/NA reporting and no aging or independently defined state-redistribution
claim. A3/A27 numerical, visual and report review must precede synthesis updates.
Reuse reviewed A31; A8/A9 still need an explicit biological decision before a
new run, and A12 remains coordinator-owned. Each further comparison must follow
what the preceding result narrowed, with exact dependent holds.

Integration remains coordinator-owned. PR #163 merged into its former stacked
branch, not main; its research content is retained on this continuation and must
be explicitly reconciled in the later research PR. Do not reset, stash or clean.

## Historical owner-requested halt — 4 November 2026

Research execution, annotation expansion and source searches are halted at the
owner's request while agent reasoning flow is reframed. Prior continuation
instructions are superseded. [Preserved current-state handoff](docs/research_reviews/2026-11-03-tool-assisted-screening-review/HALT_HANDOFF_2026-11-04.md)
distinguishes reviewed A31 results, reviewed A5 source preparation, incomplete
source joins/proposals and the unstarted jobs. All existing modified/untracked
artifacts remain in place; no commit, push, merge, reset, stash or cleanup was
performed for this halt. Both chats confirmed no active owned scientific process.
The targeted compressed TCR download finished during halting; no decompression,
barcode join or repertoire calculation followed. The latest A5 feature map is
saved but unreviewed. Do not resume scientific work without the owner's new
direction. Earlier research checkpoints below remain historical;
instruction-only updates do not resume that queue.

## Agent instruction revision — 4 November 2026

The owner subsequently requested changes to the repository's agent instructions
to prevent recurrence of analysis accumulation without biological narrowing.
[AGENTS.md](AGENTS.md#biological-screening-and-question-progression) and the
[decision workflow](docs/AGENT_DECISION_WORKFLOW.md#screening-as-question-development)
now connect starting evidence, the next unresolved comparison, informative
outcomes and the next step after a result. They preserve legitimate descriptive/
replication work, informative partial screening and existing execution safeguards.
At the owner's follow-up request, they also add task-specific skill/connector
selection, live availability checks, provenance and appropriate fallback routes.
This authorization is for instruction work only; the research halt remains in
effect. No RQ, frozen evidence, validator, contract schema or claim grade was
changed. Agent wording/compatibility review covered legitimate replication,
partial descriptive screens, mixed results, tool availability and the active
halt. The 46 existing governance tests passed with normal temporary-directory
access after sandbox temp-file permissions prevented the first attempt.
Repository validation passed 15,808 checks and the research gate passed against
refreshed `origin/main` (`99670da`). The final tool-guidance additions passed
targeted local-link/anchor and whitespace checks; unchanged tests were reused.
These instruction edits are saved locally and remain explicit policy-review
material for integration. No commit, push or merge was performed.

## Tool-assisted screening review — 3 November 2026

Reviewed the seven latest screening implementations/results, the full 22-owner
disposition and all 33 RQ dossier boundaries against available source,
annotation, Scanpy and NGS tools. [Review and stepwise plan](docs/research_reviews/2026-11-03-tool-assisted-screening-review/README.md).
The owner clarified screening as progressive biological hypothesis narrowing,
using Cardoso's cell-state/signaling/recipient/feedback sequence as an example.
[Prospective amendment](docs/research_reviews/2026-11-03-tool-assisted-screening-review/BIOLOGICAL_SCREENING_AMENDMENT_V1.md)
and [RQ folder diagnosis](docs/research_reviews/2026-11-03-tool-assisted-screening-review/RQ_FOLDER_DIAGNOSIS_V1.md)
record the change. All 33 README organizing sections/structures were inspected;
the main gap is synthesis of biological progression, not directory ownership.
The existing technical chat prepared the 22-owner biological-link map; detailed
per-job review precedes further numerical work. A8/A9 unstarted runs are held for a biological decision;
A5 source annotation now covers all 99 members. Coordinator review cleared the
metadata preparation but found that broad GO associations redefine the prior
regulatory group. The original-role crosswalk and source-grounded architectural
remodeling comparison are now reviewed in principle; the exact exhaustive feature
map/display specification remains required before its freeze. It will reuse
immutable member estimates without a new architecture score. A3/A27 source
intakes found partial temporal and paired RNA/TCR leads. Coordinator review
requested one bounded check of the linked RNA sample/count identities and
VDJ-specific public products before closing those source dispositions; no new
RNA or repertoire outcome was calculated.

A31's conditional partner run completed under freeze `6b1fe38`; independent
arithmetic, biological-report and figure review passed. Partner context remains
source-dependent, with no uniform receptor architecture or functional claim.
[Execution review](docs/research_reviews/2026-11-03-tool-assisted-screening-review/COORDINATOR_REVIEW.md).
[A12 intake](docs/research_reviews/2026-11-03-tool-assisted-screening-review/A12_SOURCE_INTAKE.md)
located 75 cell-level count stores and annotation files on X:; state evidence
and the next candidate-discriminating comparison remain unresolved.
Follow-through is isolated on `codex/tool-assisted-screening-review-20261103`
from `300a184`. Main refreshed to `99670da` (PR #162 merged); its tree equals
`f54ad29`, already contained in this branch, so no new scientific content needs
reconciliation. Next: review the technical
biological-link mapping, finish A5 source-role qualification, and approve only
exact new comparisons that could change a named biological inference. No bulk
RQ rewrite, claim promotion or new PR has occurred in this continuation.

## Full primary/moderate screening sequence — 3 November 2026

All 22 owner plans (21 canonical RQs plus Wg-P06) have reviewed rationale,
ordered steps and final dispositions: seven new numerical screens, fourteen
reused completed screens and the A14 source intake.
[Coverage and implications](docs/research_reviews/2026-11-03-full-priority-screening/README.md)
· [Independent review](docs/research_reviews/2026-11-03-full-priority-screening/COORDINATOR_REVIEW.md).
A3, A5, A12, A31, A9, A8 and A27 passed independent numerical and biological
report review. A8 retains 34 supported/106 unsupported module contrasts;
A27 retains all four unsupported main naive/effector age contrasts. Focused
RNA context survives some screens, but no uniform regulatory programme,
functional receptor response, causal repair or redistribution mechanism is inferred.

All owning README/context/dossiers and Wg-P06 entrypoints are reconciled.
A14 still lacks Fig7E preparation-level qPCR values and experiment/condition
mapping in the checked attachments. Each remaining biological limit and
reopening condition is retained in the plans/ledger. No human scientific
acceptance or claim promotion is implied.

Work is isolated on `codex/full-priority-screening-20261103`, from `f54ad29`.
Last refreshed main is `445a0ca`; PR #162 remains open on its original branch.
Larger runs executed at `X:/GitHub/ravel_execution/full-priority-screening-20261103`
because C: lacks matrix-copy capacity. Relative input hashes and runtime gates
are unchanged; compact verified outputs returned to this authoring checkout.
Existing source/annotation/literature tools suffice; no plugin was installed.
Integration checks passed: 15,650 repository checks, all seven receipts,
required archive/claim checks, and 170 distinct tests with one host-specific
symlink skip. [Validation details](docs/research_reviews/2026-11-03-full-priority-screening/VALIDATION.md).
Reviewed results are committed at `9cab415` and published in
[PR #163](https://github.com/xorca0711/ravel/pull/163), stacked on still-open
PR #162. No merge was performed. Initial remote repository checks passed;
governance identified nine CRLF-bound configuration checkout mismatches.
Exact-path checkout rules restore the recorded bytes; contracts and outputs
are unchanged. Current remote CI status is tracked in PR #163. No scientific analysis step remains
queued, only the documented measurement holds.
No frozen output or governance rule has been changed.

## Remaining public-reference screening reviewed — 3 November 2026

The existing technical chat completed the available A12-adjacent ERBB RNA
reference, reusing A19's public-source intake. Missing cell-state labels narrowed
execution to one fresh HTII-280-sorted preparation; the broader state comparison
remains unestimated. Operational QC retains 11,352 barcodes: ERBB4/ERBB2
detection is 13.65%/13.46%, with both in 2.03%. This is a preparation-level RNA
reference, not receptor function, state selection or an IL-1 result.
[Results and corrected figure](RQ_Specified/A12_recipient_context/reports/ERBB_SORTED_RESULTS_V1.md).

The [coordinator review](docs/research_reviews/2026-11-03-primary-candidate-literature/REMAINING_SCREENING_REVIEW.md)
records original-matrix R/Python agreement, 68,488 independent table checks and
visual review. Freeze `5daa3de` owns the numerical work; `1c39f57` corrects only
the figure legend; `89dd772` verifies unchanged configuration provenance after
an initial asset-registration gate failure. All three receipts verify. Final
checks passed: 15,317 repository checks, changed-asset research gate against
refreshed main `445a0ca`, 170 unit tests (one skipped), compilation, claim and
required archived-evidence checks. No biological rerun or validator change.

This reviewed follow-through extends [PR #162](https://github.com/xorca0711/ravel/pull/162)
on `codex/a32-resolution-screen-20261103`; the PR owns live CI status. A32's
completed outputs remain frozen. Lin reproduction, A31 and Wg-P06 still need
their [specific missing inputs](docs/research_reviews/2026-11-03-primary-candidate-literature/HOLD_RESOLUTION_OPTIONS.md).
Next: PR review and those external source/measurement requirements. No merge,
author contact or controlled-access application occurred; request drafts remain
private and unsent.

## A32 public resolution follow-through reviewed — 3 November 2026

The approved GSE234197 screen recovered 45,311 cells and 36 mouse identities,
then completed 88 of 306 planned RNA contrasts; 218 remain explicitly
unestimated. Sparse epithelial/later fibroblast support required narrowing to
myeloid comparisons and young D14 fibroblasts. Source-labelled AM2/AM3 in early
injury carry the useful Arg1 RNA population lead; their PBS comparisons remain
unsupported. Late AM1 Arg1 is only 2-5 UMIs per injured mouse, not a maintained
programme. [Results and three measured figures](RQ_Specified/A32_myeloid_arg1_matrix_epithelial_recovery/reports/RESOLUTION_CONTEXT_RESULTS_V1.md).

The [coordinator review](docs/research_reviews/2026-11-03-primary-candidate-literature/A32_COORDINATOR_REVIEW.md)
records independent metadata/arithmetic checks, native-R original-matrix
verification and visual review. Original Speth access and A32 joint functional
holds remain. Metadata/expression freezes are `7132cc0`/`f63050d`; no frozen
results, governance, canonical hypothesis or scientific acceptance changed.

The owner merged PR #161; this follow-up uses `codex/a32-resolution-screen-20261103`
from main `445a0ca`, preserving the earlier hold-resolution notes. The existing
technical chat `01a1a00c-8680-7fd2-a7ea-4bf804005da8` executed the work.
Lin, Hamanaka and Speth request drafts are private local files and remain unsent.
Validation passed: 15,249 repository checks, research gate against refreshed
main `445a0ca`, 170 unit tests (one skipped), required archived-evidence checks
and both receipt verifications. The reviewed deposit is committed as `3740df1`
and published in [PR #162](https://github.com/xorca0711/ravel/pull/162); the PR
owns live CI status. Next: PR review and the specific missing measurements or
source access recorded in the hold-resolution note. No merge or author contact
was performed.

## Hold-resolution assessment — 3 November 2026

Historical checkpoint; the reviewed follow-through above supersedes its
unexecuted-candidate and integration status.

The owner asked how to reopen the four remaining primary-screening holds.
[Concrete routes](docs/research_reviews/2026-11-03-primary-candidate-literature/HOLD_RESOLUTION_OPTIONS.md)
separate recovery of existing data from missing functional measurements.
Lin HRA009633's public page now loads: sequencing is controlled access under
HDAC001467. Speth GSE328925 remains private with 1 May 2027 scheduled release.
Public GSE234197 is a new candidate for an A32 resolution-context screen;
its expression and hashing files are listed, not yet inspected or analyzed.
Next: inspect that candidate's compartments/mouse mapping, and prepare focused
Lin/Wg-P06 data requests if the owner chooses outreach. A31 still needs a direct
response measurement. No contact, access application or numerical run occurred.
Main was refreshed and remains `115f3c5`; prior PR #161 CI passed at `85ccb8f`.
This follow-up is a documentation/source-access update; frozen evidence is intact.
Validation passed: 15,217 repository checks, the research gate against
`origin/main` and all six local links in the new note. These follow-up notes
remain uncommitted; PR #161's previously published analysis is unchanged.

## Reviewed screening published in PR #161 — 3 November 2026

The [coordinator review](docs/research_reviews/2026-11-03-primary-candidate-literature/COORDINATOR_REVIEW.md)
accepts the two new screening deposits for integration at their descriptive
scope, preserving all four specific limits. Independent table arithmetic, both
figures, source-hold evidence and the exact-file portability rule were checked.
The technical validation suite is reused; no numerical rerun was needed.
Main was refetched after handoff and remains `115f3c5`. GitHub identity was
verified as `xorca0711`. The owner authorized commit, push and an overall PR;
the reviewed integration is committed as `a11267a` and pushed on
`codex/rq-evidence-trajectory-audit-20261103`.
[PR #161](https://github.com/xorca0711/ravel/pull/161) includes the earlier
trajectory/cut-or-fill work, article hygiene and portfolio methods panel.
Next: PR review and the exact scientific inputs recorded in the six-job ledger.
No merge, new scientific acceptance or automatic follow-up was performed.

The first published CI found an older full-file `.gitattributes` hash dependency
and one ignored A25 compressed output missing from Git. The original attribute
bytes were restored and the receipt-matching output was added explicitly;
[correction record](docs/research_reviews/2026-11-03-primary-candidate-literature/COORDINATOR_REVIEW.md#ci-packaging-correction).
Numerical outputs and scientific validation rules were not changed.

## Literature-informed biological screening — 3 November 2026

Two actual numerical comparisons completed under freeze `94f6efb`:
[A5 named features](RQ_Specified/A5_developmental_programme_reuse/reports/DESTINATION_SCREEN_V1_RESULTS.md)
show mixed transitional identity RNA, with Klf4/5 above activated AT2 but no
single destination assignment (24 primary mice; ten common reference mice).
Basal support remains below floor; this panel does not explain the fixed Guo result.
[DY1 six-target reference](Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/IDENTITY_TARGETS_V1_RESULTS.md)
shows co-increased Irf4/Pparg RNA under WT IL4 and heterogeneous mapped-region
point differences; no NAM mechanism or replication/refutation of alveolar IL13.

The [six-job ledger](docs/research_reviews/2026-11-03-primary-candidate-literature/EXECUTION_LEDGER.md)
records receipts, adverse results and exact holds. Lin source reproduction lacks
recovered preparation-level values/map; Speth's cited GEO series is currently
private until 1 May 2027 despite its public-data statement. A31 and Wg-P06 retain
their specific missing functional/linkage measurements; old extractions were not
rerun. Relevant primary texts/supplements and source hashes are recorded.

Both receipts and independent arithmetic checks pass; the coordinator reviewed
both reports and figures. Refetched main stayed `115f3c5`. Final validation passed:
15,199 repository checks, research gate, 170 unit tests (one skipped), compilation
and all required evidence checks. The ledger records exact immutable empty-field/
log-whitespace exceptions and the one-file line-ending preservation rule.
No canonical hypothesis, frozen prior evidence, governance or acceptance changed.
Only the narrow pre-execution commit was made; all results remain for review.
The coordinator owns overall commit, push and PR. Next: review/integrate the
returned reports and exact holds; no execution job or rescue analysis remains.

## Recent literature for biological target screening — 3 November 2026

The [reading map](docs/research_reviews/2026-11-03-primary-candidate-literature/README.md)
connects eight newly located primary papers to A3/DY1-P02, A5, A12 and A32,
and distinguishes the already-reviewed direct context for A31 and Wg-P06.
The main additions are IRF4-associated loss of macrophage PPARgamma identity,
epithelial maturation versus airway diversion, ERBB4-dependent identity stability,
and the separation of ARG1-positive repair states from ARG1 catalytic effects.
Queries, publication versions, exact available locators, the Lin Fig. 3m
correction and partial-access limits are recorded. No numerical analysis or
canonical hypothesis/priority change was made. Next: complete figure/methods
reads for an adopted candidate, then synchronize its context/dossier/README
before specifying a new analysis. Fetched main remained `115f3c5`; no push.
Repository validation passed (15,115 checks), the research gate against
`origin/main` passed, and all eight local links in the new review resolve.
Biological analyses were not rerun for this documentation-only update.

## Reviewed results committed; article/RQ screening — 3 November 2026

Owner-requested result commit: `fe0316c`, following the three scoped freeze
commits. All reviewed audit/result/run deposits and owning-page updates are now
committed. Refetched integration base remained `115f3c5`; nothing was pushed.
Staging exposed cosmetic trailing spaces in two immutable Matplotlib SVGs;
their original hashes were preserved and the exact whitespace exception is
recorded in the technical ledger. Other staged files passed whitespace checks.

The [new assessment](docs/audits/2026-11-03-article-rq-screening/README.md)
covers all 33 RQ homes and 20 article directories (18 study packages, one shared
module and one archive), using current ledgers before historical plans. Useful
next qualifications are A30 archival identity reconstruction, A26/A27 receptor
recovery, A6 fixed donor/state support and the acquired Nb1 external source.
All six raw A30 inputs exist in the main checkout cache, but hash/runtime and
membership reconstruction are not yet qualified. No old analysis was replayed.

Three primary GEO text records were recovered: GSE275967 and GSE155005 do not
supply the existing independent age/paired-organ comparison; GSE129605 confirms
the prior day-11 design without resolving its animal/state map. GSE165088,
GSE292440 and GSE300399 refreshes timed out after the sandbox DNS failure was
addressed. Source absence is not inferred. Exact queries, hashes, coverage and
per-RQ next conditions are in the starting-point assessment.

Hygiene corrects Yadav's stale unrun status in both roadmap views; adds missing
article-gallery navigation; links A25's completed comparison ahead of the Nb5
unrun checkpoint, P09/A31 and Wg-P06's later work; and makes the A17/A25 measured
figures discoverable from the RQ index. At the owner's subsequent request,
the root README now excludes the Weft pilot description and shows six existing
reviewed method examples in a two-column portfolio panel: UMAP, patient-paired
expression, CUT&Tag, enrichment, spatial RNA and paired RNA/accessibility.
LinkedIn media were inspected only as a style reference; current repository
evidence determined the selection. The [curation record](docs/audits/2026-11-03-article-rq-screening/PORTFOLIO_FIGURE_SELECTION.md)
links every unchanged asset and its current caption. The structure document
records this bounded showcase; full galleries remain with their analyses.
Existing frozen paths, canonical IDs,
hypotheses, schematics, claims and research governance are preserved.
No new numerical analysis, chat dispatch, account setting, message, PR or merge.
Next technical work is qualification, followed only by a newly frozen eligible
analysis; spent same-input rescue branches remain closed. Documentation
validation passed **15,106 repository checks**, the research gate and whitespace
checks. A local GitHub-style layout preview showed all six images loaded and
the complete two-column panel; this was a local rendering, not a GitHub-page
verification. The first preview attempt was sandbox-blocked; a loopback-only
server exposing just the preview and six images resolved it. Refetched
`origin/main` remained `115f3c5`. The numerical test/receipt evidence from the
reviewed result commit was reused. No biological analyses were rerun for these
edits. The scoped documentation/portfolio commit contains these updates;
nothing was pushed. No required analyses remain in this curation task.

## Coordinator review of technical results — 3 November 2026

The separate technical chat is complete and idle. The review chat has now read
all five result reports and checked the key implementation/output boundaries;
its [interpretation review](docs/audits/2026-11-03-rq-evidence-trajectory/TECHNICAL_STATUS.md#coordinator-interpretation-review--3-november-2026)
distinguishes A25's mixed empirical prediction result, A17's conditional synthetic
identifiability result and the three completed source/join qualifications whose
downstream analyses remain held. A25 does not establish a distinct middle-age
state; A17 does not establish actual detection bias or empirical model equivalence.
Technical validation was reused without rerunning biological analyses. No new
claim grade, human acceptance, push, PR or merge; enabling inputs remain those
in the ledger. Next work requires those inputs or an independently justified
prospective amendment, not rescue fitting on the unchanged evidence.

## Cut-or-fill technical execution — 3 November 2026

All five bounded packages now have executed research-runner receipts in the
[technical ledger](docs/audits/2026-11-03-rq-evidence-trajectory/TECHNICAL_STATUS.md).
A25 completed a male-cortex whole-mouse-held-out comparison: gain over endpoint
mixture in both middle mice, but mixed gain over flexible continuous age; no
distinct-state claim. A17 completed a new probability/observation qualification:
unknown detection admits equivalent observed laws, so empirical mechanism
selection remains held pending justified ascertainment and model domains.
A5 refreshed primary sources successfully but still lacks the mouse/state map;
A12's new candidate has only five paired nonimmune-inclusive capture opportunities
and an unrecovered author-row map; A30's saved states have no barcode join.
Exact holds, source coverage, code/input hashes, results and adverse outcomes are
linked in the ledger. A17/A25 figures are embedded in their owning RQ homes.

Freeze commits are `bad95f6`, `5a792bc` (figures) and `750f7bb` (A12 source).
Prior dirty audit work, old pipelines and source evidence were preserved; no push,
PR, merge, external message or account setting change. Scientific acceptance is
unassessed. Validation passed: 15,008 repository checks, research gate, 167 unit tests
(2 skipped), all seven receipts and whitespace/preservation checks.
Next actions are the exact package-specific enabling inputs above, not another
rescue fit on unchanged evidence. No execution job remains running.

## Technical execution chat launched — 3 November 2026

At the owner's request, a separate local technical chat was created:
`01a19fa0-97c0-7011-826c-320f94a73809`. The app confirmed an active turn;
creation is not evidence of an analysis result. Its assignment is to execute
the five conditional packages in the
[cut-or-fill plan](docs/audits/2026-11-03-rq-evidence-trajectory/CUT_OR_FILL_PLAN.md):
A5 source qualification, A17 recoverability, A25 held-out model comparison,
A12 independent fixed-procedure replication and A30 measurement qualification.
Each must finish with verified evidence or a specific evidenced limitation.

The technical chat was directed to use this existing review checkout on
`codex/rq-evidence-trajectory-audit-20261103`, preserve the 38 modified Markdown
files and five untracked audit files, and freeze only its new analysis assets
before numerical runs. The review chat retains result review; no push, PR or
merge was requested. The technical execution ledger will be
`docs/audits/2026-11-03-rq-evidence-trajectory/TECHNICAL_STATUS.md`.
No numerical result is asserted at launch. Next: verify input qualification,
then inspect new contracts, receipts, outputs and exact hold reasons.

## Cut-or-fill follow-through — 3 November 2026

The owner requested an action structure for the trajectory audit's concerns.
The [cut-or-fill plan](docs/audits/2026-11-03-rq-evidence-trajectory/CUT_OR_FILL_PLAN.md)
now covers all 33 RQs with the unsupported affirmative claim, smallest useful
fill, stop rule and reopening evidence. All 33 current READMEs link their row
and display the claim boundary without changing the organizing hypothesis or
figure. Existing scientific dossiers already carry the key A11/A25/A30
corrections; no duplicate correction report or new RQ folder was created.

Five conditional packages cover A5 source-qualified fixed-component transfer,
A17 recoverability before fitting, A25 held-out model comparison, A12 independent
fixed-procedure epithelial replication and A30 measurement qualification. None
is a frozen or executed numerical contract. Repeated rescue fitting/scoring on
the spent A0/A10/A11/A13/A22/A23 inputs is excluded from this follow-through;
their questions and negative evidence remain. Functional/linkage questions need
their named measurements, not substitute RNA scores. The direct GEO refresh
failed to recover an A5 map; no new source eligibility is claimed.

Implementation identified a remaining current A29 overclaim: the pool
measurement was described as the single mechanism discriminator, with an
assumed small addition to shared cultures. Its README, literature context and
dossier now withdraw that interpretation and unqualified readiness language.
The registered working hypothesis, source results and illustration are unchanged.

Existing local audit work is preserved on
`codex/rq-evidence-trajectory-audit-20261103`; refreshed main remains `115f3c5`.
The first documentation check found 33 unsupported inline table anchors; they
were replaced by standard question headings without changing the validator.
Validation passed after correction: all 33 decisions and README notes, original
text preservation with the documented A29 exception, 1,160 local links, 14,889
repository checks, the research gate against unchanged refreshed `115f3c5`, and
whitespace checks. Registry bytes and the A29 working hypothesis are unchanged.
Exact next actions and unresolved source/model/measurement choices are in the
plan; no numerical run, external setting change, commit or PR was made.

## RQ evidence and hypothesis trajectories — 3 November 2026

The [all-33 audit](docs/audits/2026-11-03-rq-evidence-trajectory/README.md)
compares first registered wording with current dossiers, corrections, numerical
reports and recent article connections. Its editorial assessment identifies
8 questions with bounded empirical narrowing, 11 whose main progress is a
useful limit/negative diagnostic, and 14 with the decisive current comparison
untested. These categories are not claim grades or human acceptance decisions.
A5 and A31 provide the clearest component/candidate narrowing; A11's capacity
control, the corrected Compass sign and A30's support restrictions limit earlier
affirmative interpretations. Historical framing drift is documented without
attributing every stalled question to AI.

All hypotheses, registry records, figures, source artifacts and frozen analyses
remain unchanged. No biological run was performed. The audit records exact
per-question next decisions and data limits; no new source access, laboratory
capability or external setting was established. Work is on
`codex/rq-evidence-trajectory-audit-20261103`, based on merged PR #160 (`115f3c5`).
Validation passed: 33-question/origin coverage, 373 local links, 14,796 repository
checks, the research gate against freshly fetched unchanged `115f3c5`, and
whitespace checks. The [validation record](docs/audits/2026-11-03-rq-evidence-trajectory/VALIDATION.md)
distinguishes saved-evidence inspection from numerical reproduction. The review
is saved locally, uncommitted; no PR or external settings changed. Exact next
steps are the missing discriminator or source qualification in each audit entry;
no new numerical analysis or automatic portfolio retirement is proposed.

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
