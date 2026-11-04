# A8: fixed early/late AT1 panel attribution

Completed 3 November 2026 under freeze `14e7ea4`. [Receipt](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/receipt.json) verifies. All 1,960 original-score/support checks passed (maximum error 9.71e-17). This is a measurement attribution on exposed source data, not independent validation or scientific acceptance.

The repository-selected three-gene early panel is Lmo7/Pdpn/Hopx; the selected four-gene late panel is Aqp5/Vegfa/Cav1/Spock2. These are subsets of the published marker context, not complete early/late programmes. In particular Choi Figure 7B/E contains additional late-associated markers; this exact reproduction does not add them. [Source review](../../../docs/research_reviews/2026-11-03-full-priority-screening/A14_SOURCE_MANIFEST.md) and [prospective specification](../../../docs/research_reviews/2026-11-03-full-priority-screening/prerequisites/A8_ATTRIBUTION_SPEC_V1.md) distinguish source scope from the frozen repository measurement.

All 35 original units were retained: 10 pooled multiome libraries and 25 external animals. The same 1,503-gene sampling order, RNA budget of 2,000, seeds 17/29, original source cell order, airway/alveolar filter and Cldn4/Krt8 versus Sftpc gate were used. Each seed restarts within the same unit; seeds are technical sensitivity, not independent replicates. Both groups require at least 30 cells and panel coverage at least 0.8. Only 34 of 140 unit/seed/panel contrasts qualify; all 106 unsupported contrasts remain output.

Constituent attribution explains heterogeneous late-panel totals. In the SeV_control well Aqp5 contributes positively while Vegfa and Spock2 contribute negatively at both seeds; Cav1 is small and changes sign. The injured Cebpa-mutant late total changes sign between seeds, with Vegfa changing direction. The wildtype injured total also changes sign although all four member signs are stable, because positive and negative contributions shift in magnitude. The sole external animal eligible at both seeds, EEM-scRNA-167, changes late-total sign with Aqp5/Vegfa direction changes. None of these patterns establishes coordinated maturation or later AT1 contribution. Every member, including the early comparator, is retained in the [complete member display](PANEL_ATTRIBUTION_V1_ALL_MEMBERS.md) and [numerical contrasts](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/member_contrasts.tsv).

The following table shows **all units**. Values are two-marker minus reference detection percentage points, with equal member weights within each selected panel. A dash is unestimated under the original support rule; the saved primitives still retain its measured counts and descriptive value. No seeds are averaged.

| Unit | Early: seed 17 / 29 | Late: seed 17 / 29 | Both groups supported: seed 17 / 29 |
|---|---:|---:|---|
| P9_control | +0.906 / +0.577 | -7.333 / -6.159 | yes / yes |
| P9_Cebpa_mutant | +1.255 / +0.700 | -1.061 / -0.659 | yes / yes |
| 7wk_control | +11.866 / — | -4.448 / — | yes / no |
| 7wk_Cebpa_mutant | -2.536 / -0.588 | -0.766 / -2.515 | yes / yes |
| SeV_control | +24.793 / +21.424 | +0.867 / +1.660 | yes / yes |
| SeV_Cebpa_mutant | +8.297 / +5.856 | -0.203 / +1.194 | yes / yes |
| wildtype_PBS | — / — | — / — | no / no |
| wildtype_SeV | +14.786 / +17.684 | -0.563 / +0.976 | yes / yes |
| AP1mut_PBS | — / — | — / — | no / no |
| AP1mut_SeV | +8.834 / +3.708 | -4.663 / -5.241 | yes / yes |
| EEM-scRNA-113 | — / — | — / — | no / no |
| EEM-scRNA-116 | — / — | — / — | no / no |
| EEM-scRNA-117 | — / — | — / — | no / no |
| EEM-scRNA-118 | — / — | — / — | no / no |
| EEM-scRNA-124 | — / — | — / — | no / no |
| EEM-scRNA-125 | — / — | — / — | no / no |
| EEM-scRNA-126 | — / — | — / — | no / no |
| EEM-scRNA-127 | — / — | — / — | no / no |
| EEM-scRNA-158 | — / — | — / — | no / no |
| EEM-scRNA-162 | — / — | — / — | no / no |
| EEM-scRNA-166 | — / — | — / — | no / no |
| EEM-scRNA-167 | +14.244 / +19.125 | +1.762 / -2.727 | yes / yes |
| EEM-scRNA-170 | — / — | — / — | no / no |
| EEM-scRNA-172 | — / — | — / — | no / no |
| EEM-scRNA-179 | — / — | — / — | no / no |
| EEM-scRNA-180 | — / — | — / — | no / no |
| EEM-scRNA-181 | — / — | — / — | no / no |
| EEM-scRNA-182 | — / — | — / — | no / no |
| EEM-scRNA-236 | — / — | — / — | no / no |
| EEM-scRNA-237 | — / — | — / — | no / no |
| EEM-scRNA-238 | — / — | — / — | no / no |
| EEM-scRNA-239 | — / — | — / — | no / no |
| EEM-scRNA-310 | — / — | — / — | no / no |
| EEM-scRNA-311 | — / — | — / — | no / no |
| EEM-scRNA-312 | — / — | — / — | no / no |

The seven-week control qualifies only at seed 17; both PBS wells fail both seeds. Twenty-four of 25 external animals fail the two-marker support requirement. One eligible external animal is not replicated confirmation, and that cohort has no neonatal arm. All cells, exclusions and source identities are in [filter primitives](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/cell_filter_primitives.tsv.gz), [draw primitives](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/cell_draw_primitives.tsv.gz), [retention](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/retention.tsv) and [original parity](../../../analysis/research/runs/A8_panel_attribution_v1_20261103/original_parity.tsv).

The biological next step still requires a qualified early-measurement-to-later-AT1-outcome link in independent biological units. Conditional RNA labels, shared marker programmes and pooled libraries cannot supply that endpoint. No target ranking, replacement positive panel, significance test or claim promotion was introduced. Independent coordinator numerical review passed all filter, draw, member and module reconstructions (maximum contribution error 1.11e-16). Biological report review also passed all 140 displayed values/support labels and the stated member/sign interpretations. This clears integration without promoting a scientific claim.
