# Repository readiness audit — 7 October 2026

The audit corrects two numerical defects in the latest Wang/Wagner 2025 package,
synchronizes the live indexes and reviews all 31 question baselines. It prepares
the repository for a deliberate next analysis; it does not certify every
historical biological claim, establish new mechanisms or accept all proposals.

Start with the [return checklist](RETURN_CHECKLIST.md). Current scientific details
are in the [Wp correction report](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md),
with the [all-question review](QUESTION_REVIEW.md) covering the rest of the portfolio.

## Scope and evidence

The starting main revision was `cc5ce7e09bc03df49a982569236d572407ecb195`, including
merged PR #145. The initial inventory contained **5,900 tracked files, 778 Markdown
documents, 31 questions, 31 article candidates, 64 contracts and 59 receipts**.

- **Whole tracked repository:** path inventory, conflict markers, tracked JSON
  parsing, Python compilation, document links, claim bindings, registry coverage,
  historical artifact integrity, governed receipts and the required archive checks.
  The [machine inventory](inventory.json) records final coverage and input availability.
- **Current text and scientific framing:** all root Markdown and documentation
  entrypoints; the canonical register and all 31 dossiers' hypotheses, current
  evidence and interpretation boundaries; registered qualitative schematics were
  screened for unconditional mechanism and arbitrary sample-size labels. Dated
  plans and archived checkpoints were assessed as history, not rewritten into
  present-tense results. The [question ledger](QUESTION_REVIEW.md) records decisions.
- **Deep analysis/QC review:** latest Wp R0–R4, metadata follow-ups and A30; source
  and interpretation work from the [same-day PR140 audit](../2026-10-07-pr140/REPORT.md)
  was reused. It already checked 24 Wp receipts and 85 saved numerical statements.
  New corrections add [91 independent checks / 4,999 values](correction_verification.json).
- **Operational readiness:** local checkout reconciliation, raw-cache paths,
  input preflight, scientific runtime, versioned runs, current-result locators and
  explicit conditions for returning in approximately two weeks.

No fresh systematic review of every source paper, visual audit of every historical
PDF, independent reannotation of all datasets, or rerun of every biological pipeline
is claimed. Mechanical integrity cannot establish source truth or scientific merit.
The detailed primary-source access limits remain in the linked literature records.

## Findings and disposition

| Finding | Correction or disposition | Evidence |
|---|---|---|
| Raw Compass penalties labelled as consistency; sign interpretation reversed | New orientation v3 reproduces all 1,328 prior summary values before transforming; PGAM rho is now +0.291, nominal BH q=0.181 | [Correction report](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md) |
| Human R4 CP10K denominator used selected genes | New R4 v3 uses full-gene totals, preserves all cell gates, and exports original barcode/QC identity | [Receipt](../../../analysis/research/runs/wp_human_signature_transfer_v3/receipt.json) |
| M3 human context depended on incorrect R4 scores | New M3 v2; M1/M2 bulk outputs verified identical. Constant-gene eligibility differs from R4 and is now explicit | [Receipt](../../../analysis/research/runs/wp_metadata_phenotypes_v2/receipt.json) |
| Old human/Compass figures repeated superseded values | Current v4 correction panel rendered and visually checked; original package and v3 footer-overlap render preserved | [Figure](../../../analysis/research/runs/wp_correction_figures_v4/corrected_scores.png) |
| “No regulatory movement”, “TPM confound absorbed”, exact-zero empirical p and isotope-label/pool conflation | Canonical A28/A29 evidence, dossiers and local contexts corrected; historical derivations carry supersession notices | [A28](../../research_dossiers/A28.md), [A29](../../research_dossiers/A29.md) |
| A28/A29 schematic outcomes over-identified mechanisms; A28 showed an unjustified minimum mouse count | Versioned v2 schematics qualify rescue, matching, precision, marker/function distinction and coexistence of explanations | [A28](../../../RQ_Specified/A28_th17_arm_asymmetry/schematics/hypothesis_v2.svg), [A29](../../../RQ_Specified/A29_pgam_effector_mechanism/schematics/hypothesis_v2.svg) |
| Live indexes still had 24/28 questions and Wp “no expression analysed”/solver hold | Current navigation and roadmap synchronized to A0–A30, executed Wg/Wp stages and correction reports; dated package counts retained | [Dossiers](../../research_dossiers/README.md), [paper index](../../../Research%20Article/README.md) |
| PROGRESS mixed draft, ready, closed and merged states as live instructions | Short current handoff replaces the chronological accumulation; original checkpoint preserved at a pinned Git revision | [PROGRESS](../../../PROGRESS.md) |
| Primary checkout was behind main with two apparent local metadata edits | Both contents exactly matched current main. Safe fast-forward succeeded; no reset, stash, force checkout or loss of local content | [Reconciliation](#checkout-and-environment-reconciliation) |

## Remaining scientific qualifications

These restrict the next analysis rather than invalidate the repository's ability
to hold new work. They must not be hidden behind “ready” or a passing receipt.

1. **A30:** state overlap and missing-state imputation remain material. One donor
   had 82.3% of CSF cells in states absent from paired blood. Activation binning and
   residualization do not rule out activation biology; no residency claim follows.
   Size-only loaded-gene nulls and lack of dedicated doublet sensitivity remain.
2. **R4/M3:** the inherited random-set universe is restricted; R4's signed S3 score
   is compared with unsigned random sets. Those tail fractions cannot certify
   signature specificity. QC now has barcode provenance, not a new doublet result.
3. **R2:** no original scVI matrix/model or complete published reaction universe;
   modern pooled sensitivity is not Figure 1 reproduction, and pool p values are
   not animal-level inference. The recovered file is a v1 cache, verified against
   v2 summaries, not a recovered v2 solver output.
4. **R3/E3:** missing animal identity, compositional TPM ambiguity and different
   drug vehicles restrict causal/absolute-output claims. Expression matching and
   numerical verification do not remove these limitations.
5. **Portfolio:** exact unit/state/outcome linkage, independent preparation,
   meaningful effect/precision, actual laboratory access and A17 implementation
   remain question-specific requirements in the [ledger](QUESTION_REVIEW.md).
   A failed or null result is retained; no preferred RQ is selected.

## Checkout and environment reconciliation

Work was isolated on `codex/repo-readiness-audit-20261007` in the existing X-drive
audit worktree. In the primary checkout, two unstaged metadata files were verified
byte-equivalent after newline normalization to current main before any alignment:

| File | Normalized SHA-256 |
|---|---|
| `analysis/scripts/qualify_geo_metadata_v1.py` | `cf8fb66e45192775e132390fd54bd44c38cca5f598f6bfee1fbdafc1bdcdc5e7` |
| `analysis/tests/test_geo_metadata_qualification.py` | `a2e4cec00ac147f064a10db9b978dc5c50ed8ba2ba441c0ac2fb8d3af8de21df` |

An empty primary `.git/index.lock` dated 5 October 10:12 KST blocked fast-forward;
no Git process was running. It was preserved as
`.git/index.lock.preserved-20261007`, and ordinary `git merge --ff-only origin/main`
succeeded from `76dc9b4` to `cc5ce7e`. No existing worktree was retired and no raw
data, local ignored work or biological output was deleted. The audit remains a
separate branch until reviewed and merged. The two original paths can still show
stat-only modifications in a restricted status call; their diffs are empty and
the verified contents are preserved.

The ARM64 X-drive Python environment executed the corrections. Its missing
`openpyxl` dependency was installed (3.1.5, with et-xmlfile 2.0.0); the broken x64
launcher was not repaired. The first raw-cache junction was rejected by the gate's
within-root check. Only that newly created junction was replaced with hard links
to the existing 21 Wp cache files; raw bytes were not modified or duplicated.

## Validation and review boundary

See [validation results](VALIDATION.md) for exact checks and integration revision.
The full scan, saved arithmetic and visual QA are complementary; none certifies
biological truth. New contracts retain exposure and all failed/superseded artifacts.
No validator, legacy hash baseline, CI workflow or repository-wide agent policy
was weakened. Question-guide metadata changes register new inert SVG versions;
their interpretation changes remain explicit in the PR for review.

Human retain/reject decisions, claim-grade promotion, laboratory eligibility and
remote branch-protection settings are not created by this audit. Local settings
and runtime checks do not prove server-side enforcement. No scheduled follow-up
or automatic analysis was created.
