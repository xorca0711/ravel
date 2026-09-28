# Question figure gallery

An index of every figure tracked under `RQ_Specified/`, with the document that
captions it. A question ID is a navigation label, not an evidence grade. Six of
the eleven questions here hold no figure at all, which is a fact about what those
analyses produced rather than a gap waiting to be filled: a paired median with
three readable units is reported as a table because a plot of three points would
imply a distribution the design cannot support.

Captions stay next to the analysis that produced them, so this page points and
does not restate. Restating a caption here would create a second, drifting copy
of the caveats that matter more than the images.

The register's own cross-question gallery is separate, at
[analysis/figures/rq/README.md](../analysis/figures/rq/README.md). It carries
supporting panels and proposed designs for the A1 to A14 register and is
generated largely by `analysis/scripts/16_research_question_figures.py`; this
page covers only assets that live inside the question folders.

## Questions with figures

| Question | PNG | Captioned in |
|---|--:|---|
| A0 | 10 | [figures/pilot_v1/README.md](A0_conserved_epithelial_transition_program/figures/pilot_v1/README.md) (4), [reports/EXPLORATORY_PILOT_REPORT.md](A0_conserved_epithelial_transition_program/reports/EXPLORATORY_PILOT_REPORT.md) (3), [reports/PILOT_REPORT.md](A0_conserved_epithelial_transition_program/reports/PILOT_REPORT.md) (2), [reports/P0_ELIGIBILITY_REPORT.md](A0_conserved_epithelial_transition_program/reports/P0_ELIGIBILITY_REPORT.md) (1) |
| A1 | 19 | [figures/README.md](A1_transitional_epithelial_state_distinction/figures/README.md), the question's own curated gallery, plus [reports/REGULATORY_FATE_REPORT.md](A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md) |
| A10 | 1 | [reports/FOLLOWUP_RESULTS.md](A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md) |
| A16 | 2 | [RATIONALE.md](A16_cd177_state_attribution/RATIONALE.md#figures-for-the-amendment), the dated amendment that they support |
| A5 and A11 shared contract | 1 | [reports/REVISED_TEST_RESULTS.md](A5_A11_shared_component_contract/reports/REVISED_TEST_RESULTS.md) |

Each PNG has an SVG beside it except the three A0 planning and coverage panels,
which are raster only.

A0 keeps its pilot panels in a gallery of their own because the pilot has a
frozen figure set; its later exploratory and eligibility panels are captioned in
the reports that decided them, which is where their gates are stated.

A1 is the only question whose figure count justifies a curated gallery, and that
gallery is organised newest first. Fifteen of its nineteen images are displayed
there or in the regulatory-fate report. The remaining four, under
`figures/second_batch/`, are deliberately displayed nowhere: they are the
superseded renders, preserved beside the corrected `second_batch_verified/` set,
and the gallery says so at the point where the corrected versions appear. Three
of those four PNGs are byte-identical to their corrected counterparts, so the
correction there was to the SVG and to one raster panel, not to every image.

## Questions with no figures

| Question | What it produced instead |
|---|---|
| A2 | Both delivery legs, as tables and staged reports under [A2_areg_source_delivery](A2_areg_source_delivery/README.md). The readable leg-1 result is a median across three split wells, and the depth-standardised leg-2 correlation rests on four donors |
| A5 developmental reuse | A data audit and enrichment tables under [A5_developmental_programme_reuse](A5_developmental_programme_reuse/README.md); the shared-contract figure above covers the component test |
| A11 | The Kim test and the GSE198864 acute-injury assay, both as tables and reports under [A11_lesion_programme_addition](A11_lesion_programme_addition/README.md). The acute-injury assay reached three to four paired donors, below any count that supports a plotted distribution |
| A12 | A README only; its executed pilot was recorded under the roadmap run that produced it |
| A13 | Triad counts and a reproduction check under [A13_fibroblast_beyond_macrophage_il1b](A13_fibroblast_beyond_macrophage_il1b/README.md). The result is a coverage arithmetic: no Kim patient holds a complete paired triad under the type 2 epithelial definition, three do under a wider one, against a ten-patient floor |
| A15 | A plan, a rationale and a side-branch report; the question has no result of its own and is pending the owner's retain or reject |

## What this page does not do

It does not render anything. Figures are produced by the scripts inside each
question folder, and a new render belongs in a fresh output directory with its
own run record, never in place of a curated asset. It also does not grade:
several figures above accompany results the register holds as descriptive or
unresolved, and the captions carry those limits.
