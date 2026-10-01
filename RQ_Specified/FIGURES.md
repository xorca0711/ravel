# Question figure gallery

An index of figures tracked under `RQ_Specified/`, with the document that
captions each set. A question ID is a navigation label, not an evidence grade.
Some questions have tables or proposed designs without figures. Where small
samples are plotted, every observed unit and its limits must remain explicit;
a plot does not turn a few observations into a supported population distribution.

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
| A10 | 2 | [reports/FOLLOWUP_RESULTS.md](A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md), [reports/ENDPOINT_TIMING_UNITS_2026-09-28.md](A10_organoid_growth_outcome/reports/ENDPOINT_TIMING_UNITS_2026-09-28.md) |
| A12 | 3 | [RATIONALE.md](A12_recipient_context/RATIONALE.md) (held-out model ladder for the A12 and A13 pilots; patient-level relationship and predictions), [reports/A12_S1_SOURCE_IDENTITY_MAP.md](A12_recipient_context/reports/A12_S1_SOURCE_IDENTITY_MAP.md) (per-patient IL1B allocation) |
| A16 | 5 | [RATIONALE.md](A16_cd177_state_attribution/RATIONALE.md#figures-for-the-amendment) (two summary panels) and [the evidence behind them](A16_cd177_state_attribution/RATIONALE.md#the-evidence-behind-those-two-summaries) (a matched-null histogram set, per-cell violins and a balance Love plot) |
| A19 | 4 | [FIGURES.md](A19_fzd_response_reversibility/FIGURES.md): three main figures and one supplementary figure, each as PNG/PDF/SVG; donor-paired qPCR, passage persistence and source-block bulk RNA |
| A20 | 6 | [Atlas gallery](A20_fibroblast_fzd_context/FIGURES.md): three paired-context figures; [extension gallery](A20_fibroblast_fzd_context/extensions/extension_v1/FIGURES.md): three four-donor FZD/input/individual-gene figures, each PNG/PDF/SVG |
| A21 | 6 | [Parent gallery](A21_fzd4_capillary_function/FIGURES.md): three cohort/context figures; [extension gallery](A21_fzd4_capillary_function/extensions/extension_v1/FIGURES.md): three vascular-source, Fzd-family and receptor-context figures; each PNG/PDF/SVG |
| A5 and A11 shared contract | 1 | [reports/REVISED_TEST_RESULTS.md](A5_A11_shared_component_contract/reports/REVISED_TEST_RESULTS.md) |

Each PNG has an SVG beside it except the three A0 planning and coverage panels
and the A10 per-plate performance panel, which are raster only.

A0 keeps its pilot panels in a gallery of their own because the pilot has a
frozen figure set; its later exploratory and eligibility panels are captioned in
the reports that decided them, which is where their gates are stated.

A1 keeps a curated gallery organised newest first. A19 keeps its new four-figure
set with full captions and source links in its question workspace. Fifteen of A1's nineteen images are displayed
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
| A8 | A rationale, a plan and a frozen component partition specification under [A8_maturation_component_at1_contribution](A8_maturation_component_at1_contribution/README.md). Its founding overlap diagnostics live in the register's own gallery at [analysis/figures/rq/README.md#a8](../analysis/figures/rq/README.md#a8), because they belong to the package that owns claim C168 |
| A5 developmental reuse | A data audit and enrichment tables under [A5_developmental_programme_reuse](A5_developmental_programme_reuse/README.md); the shared-contract figure above covers the component test |
| A11 | The Kim test and the GSE198864 acute-injury assay, both as tables and reports under [A11_lesion_programme_addition](A11_lesion_programme_addition/README.md). The acute-injury assay reached three to four paired donors, below any count that supports a plotted distribution |
| A13 | Triad counts, a reproduction check, and since 28 September 2026 a rationale and plan under [A13_fibroblast_beyond_macrophage_il1b](A13_fibroblast_beyond_macrophage_il1b/README.md). The result is a coverage arithmetic and a closed predictor cycle; its held-out ladder is plotted in panel c of [A12's figure](A12_recipient_context/figures/A12_F01_heldout_model_ladder.png) rather than duplicated here |
| A15 | A plan, a rationale and a side-branch report; the question has no result of its own and is pending the owner's retain or reject |
| A14 | Two frozen hypotheses and their arms under [A14_withdrawal_recovery_and_reception](A14_withdrawal_recovery_and_reception/README.md). Its experimental schematic is in the register's own gallery at [analysis/figures/rq/README.md#a14](../analysis/figures/rq/README.md#a14); its outcome panels require the unexecuted experiment |

## What this page does not do

It does not render anything. Figures are produced by the scripts inside each
question folder, and a new render belongs in a fresh output directory with its
own run record, never in place of a curated asset. It also does not grade:
several figures above accompany results the register holds as descriptive or
unresolved, and the captions carry those limits.

## Nb3-derived questions, 1 October 2026

A22 and A23 have rationale/test plans and no new question-specific data figures. Their completed source-screen evidence remains in the [Nb3 gallery](../Research%20Article/gate2_N2_nabhan_2026/FIGURES.md), with 12 paper-style figures and source tables. No duplicate image assets or claim grades are created here.
