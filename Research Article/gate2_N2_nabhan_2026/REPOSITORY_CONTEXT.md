# Repository context and reuse decisions

Inspected 1 October 2026 at `main`, HEAD `33b27cf`. The initial checkout had
untracked `.claude/` and `docs/audits/2026-09-28-rq-adversarial-review/`; those
were preserved. No earlier `gate2_N2_nabhan_2025` folder was found.

## Purpose and established workflow

The [root overview](../../README.md) asks which epithelial and immune-state
programmes distinguish productive repair from persistent remodelling. RNA
states motivate hypotheses; repair requires an independently measured outcome.
Paper evidence belongs in `Research Article/`, while shared question execution
belongs in [RQ_Specified](../../RQ_Specified/README.md). The
[question register](../../RESEARCH_QUESTIONS.md) remains canonical.

The established sequence is source/design audit -> dated computational contract
-> bounded source reproduction -> sensitivity and competing explanations ->
external eligibility -> separately specified extension -> logged verdict.
Original outputs, failed tests and frozen contracts are retained. Later
interpretation corrections govern reuse without rewriting old runs.

| Existing work | What it established or limited | Reuse here |
|---|---|---|
| [Nabhan 2018 source reproduction](../gate1_03_nabhan_2018/source_reproduction/README.md) | FPKM source-expression reconstruction; exact 74% co-expression claim was not recovered under declared thresholds | Keep source measurement semantics, denominators and unrecovered parameters explicit |
| [Nb1](../gate1_03_nabhan_2018/nb1/README.md) | Animal-level Wnt-source/response summaries; local timing and AT2 coverage do not support the acute switch | Reuse the experimental-unit and depth-control discipline, not a presumption that the 2026 screen validates Nb1 |
| [England plan](../gate2_C2_england_2025/ANALYSIS_TRIAL_PLAN.md) and [current review](../gate2_C2_england_2025/EVIDENCE_REVIEW.md) | Source reproduction before state/clone extensions; pooled libraries and mice require different interpretation | Separate paper claims, computed observations and proposed mechanisms; preserve controls and source labels |
| [A10](../../RQ_Specified/A10_organoid_growth_outcome/README.md) | 886 libraries; 885 paired imaging wells; RNA-growth models already run. Revised epithelial increment 0.0426 is a within-screen association; held-out plate R-squared remains negative on three plates | Reuse joins, provenance and prior-exposure record. No repeat growth-model search under a new paper label |
| [P1 design recovery](../../docs/roadmap_runs/2026-09-27/P1_SCREEN_DESIGN.md) | Shared cell-mixture split across four wells; EGF in medium; preparation/lot crosswalk unresolved | Governs replication and ligand-context limits; supersedes older claims that the supplement was inaccessible |
| [A2 interpretation](../../RQ_Specified/A2_areg_source_delivery/reports/INTERPRETATION_AUDIT_2026-09-27.md) | Screen comparisons do not identify delivery, recipient route or a precise null | E6 must address recipient identity and medium context, rather than refitting the same AREG screen effect |
| [A13](../../RQ_Specified/A13_fibroblast_beyond_macrophage_il1b/README.md) | Multi-compartment claims depend on complete donor/compartment coverage | E1/E7 are candidate links; missing immune cells in the organoid cannot be inferred from fibroblast chemokines |

## What changes now

The owner has now read this paper and requested its structure. That supersedes
the unread-paper restriction for a new study synthesis. The historical reading
status inside A10's frozen configuration remains untouched. A10's living README
links to this package so future sessions do not treat that old restriction as
current.

No new A-number is assigned. E1–E8 below are paper-local questions. Shared work
can attach to A1/A8 (state and fate), A10 (growth), A2/A12 (recipient context),
and A13 (fibroblast contribution), after its own design contract. Paper-local
reproduction stays here. Existing score definitions are reused only when the
measurement matches; otherwise the new definition receives a distinct version.

The A10 count workbook and selected-gene cache were not found at their recorded
locations in this checkout. Tracked reports prove earlier execution, not current
input availability. Recover and verify the recorded workbook hash before a new
whole-transcriptome stage. Large spatial downloads are unnecessary for planning.
