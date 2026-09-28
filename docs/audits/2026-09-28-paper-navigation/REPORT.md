# Article navigation and England evidence presentation

Date: 28 September 2026. Base: `37e5f1b`. This is a documentation review,
following the owner's request to distinguish article context, claims and figures.

## Result and document responsibilities

- [Article index](../../../Research%20Article/README.md#studies-with-executed-analyses):
  one context/evidence/figures table for eight papers with executed analyses,
  plus a separately identified cross-study specificity module.
- [England overview](../../../Research%20Article/gate2_C2_england_2025/README.md):
  biological context, six claim summaries, biological units, execution stages
  and the distinction between published figures, repository figures, C claims,
  global A questions and paper-local E-N candidates.
- [England evidence review](../../../Research%20Article/gate2_C2_england_2025/EVIDENCE_REVIEW.md):
  published evidence, our analysis and current limits for each biological topic.
- [England gallery](../../../Research%20Article/gate2_C2_england_2025/FIGURES.md):
  all 15 original images grouped by biological question, with units, corrected
  captions, underlying tables, plotting scripts and run/render provenance.

The seven other paper overviews and the cross-study page link directly to
their existing source context, analysis evidence, claim register and galleries.
Their historical scientific interpretations were not comprehensively re-audited.
Murthy remains a deposit-analysis folder without an owner-read roadmap note.
The root claim register and shared question register retain their authority.

## Corrections justified by existing evidence

The England page mixed initial plans, completed execution and later review.
Its claimed total of 14 figures omitted one from the actual count: four batch,
six continuation and five follow-up images. A blanket description of pooled
units also obscured the 44 source-indexed mice in the nonspatial clone arrays.
Spatial exports still lack those identities; RNA captures still pool lungs.

Current captions apply the already completed
[source/claim audit](../2026-09-28-england-paper-rqs/REPORT.md) and
[A16 integration review](../../../RQ_Specified/A16_cd177_state_attribution/reports/INTEGRATION_REVIEW.md).
They explicitly qualify depth attribution, same-cell gate calibration,
cycling equivalence, projected topology and distance independence. Original
image labels remain intact, with conflicting claims identified in the captions.
Sparse CD177 coverage leaves repair transfer unassessed. No new mechanistic
claim, hypothesis registration or grade is introduced.

The England roadmap row and JSON now both list all three paper-analysis stages
and the integrated A16 results. Murthy's incorrect wholesale reference to
C4–C7 and C9 is replaced by the report and claim-register links; mouse claims
were never evidence for that human cohort.

## Preservation and validation

The [before inventory](inventory.json) records README sizes/image counts and
England image hashes. The original README text remains in Git at the pinned
base. The [verification record](verification.json) confirms that all 56 embedded
image references across the nine inspected folders are retained and their
image bytes match the base. All 15 England figures also match the inventory
hashes previously checked against the render/run records.

Frozen reports, protocols, data, figures, numerical outputs, code and claim
grades are unchanged. The existing England README `#figure-gallery` and article
index `#figure-galleries` entry points remain usable. No scientific workflow was
rerun: only documentation/provenance checks are appropriate to this change.

Local validation passed: 3,544 repository checks (Markdown links/anchors,
JSON, selected numeric bindings and claim summaries), plus `git diff --check`.
The PR workflow also runs the existing code and evidence checks before merge.
