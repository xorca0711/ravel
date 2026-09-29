# Figure interpretation corrections — 2026-09-29

Use these presentations for the current figure audit. Original C5, C11 and E5
images, trial records, tables and summaries remain historical evidence states.
Only wording/layout changed; no observations, model fits or trial decisions were rerun.

| Figure | Correction and deciding evidence |
|---|---|
| [C5 F2](c5_fig2_fibrotic_programme_split.png) | Scope retention to the two observed genotype libraries; `../c5_figures_for_the_three_findings/c5_fibrotic_retention.csv` spans 39.4–97.1%. One library per genotype does not estimate reproducibility. |
| [C11 F1](c11_fig1_e6_depth_control.png) | Scope nominal significance to the two displayed tests: primary AREG–EGFR p=0.11207; TGFA–activation control p=0.044692. Other tests exist in `../e6_donor_level_axis_coupling/e6_correlations.csv`. |
| [C11 F2](c11_fig2_c7_resolution.png) | The small candidate-state margin leaves this assignment unresolved; it cannot establish that whole-profile similarity can *never* distinguish states. Source: `../c7_what_the_sort_contaminant_is/c7_profile_correlations.csv`. |
| [C11 F3](c11_fig3_c8_amplitudes.png) | Retained-pair ratios 1.196 and 1.099 lie within the 0.80–1.25 descriptive band. A zero-inflated two-gene score does not prove a biological state or guarantee a mixture result under every biology. Source: `../c8_subpopulation_or_gradient/c8_codetection_ratios.csv`. |
| [C11 F4](c11_fig4_species_divergence.png) | Rankings differ between the measured mouse tumour and human IPF deposits. Species, disease and sampling are confounded; the comparison does not isolate a species effect. Sources: `../c6_who_makes_egfr_ligands/c6_hbegf_survival.csv`, `../e2_human_fibrosis_ligand_sources/e2_ipf_ranking_by_celltype.csv`. |
| [C11 F5](c11_fig5_c9_existence_vs_size.png) | Both injury animals exceed the co-detection permutation threshold (p=0.005, 0.010); 26/27 marker directions agree and 9/27 pass the magnitude rule. The depth-half contrasts flag sensitivity without identifying depth's causal share. Sources: `../c9_the_fst_runx2_population/c9_per_library.csv`, `../c9_the_fst_runx2_population/c9_marker_replication.csv`. |
| [C11 F6](c11_fig6_c10_lead_closes.png) | Program/marker agreement supports an annotation, not definitive state identity or an irreversible loss of identity. Sources: `../c10_published_state_or_not/c10_effect_sizes.csv`, `../c10_published_state_or_not/c10_saturation_audit.csv`. |
| [E5](e5_retention_against_injury.png) | Five genes have higher detection in both injury animals than in either untreated animal. Shared injury expression makes retention alone insufficient for tumour specificity; it does not identify the mechanism sustaining expression in tumours. Source: `../e5_figure_for_the_refutation/e5_retention_against_injury.csv`. |

The independent units already displayed are retained. Aggregated source tables
cannot supply missing biological uncertainty; no cell bootstrap was introduced.

Reproduce with `python ../plot_claim_review_20260929.py` from this directory, or
give that script's full path from any directory. [Hash manifest](figure_run.json)
records every saved source table, plotting source and new image.
