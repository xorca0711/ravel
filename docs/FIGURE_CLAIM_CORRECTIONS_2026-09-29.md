# Figure claim corrections, 2026-09-29

A repository-wide audit of every in-figure title, panel title and footnote against the table the
figure is plotted from. 112 figures across 51 live figure-producing scripts were examined on two
separate axes: whether the display is the one its analysis type is conventionally reported in, and
whether the text baked into the figure is true of the table beneath it.

The audit was prompted by a narrower correction. Rewriting the A16 CD177 figures into conventional
forms forced each title to be stated as a checkable claim, and two of those claims turned out to be
false. This document records what the same procedure found everywhere else.

Method note: a claim is recorded as **false** when the deciding table contradicts it, **overstated**
when the table supports a weaker statement than the one displayed, and **undecidable** when the
deciding table is not available here. No verdict was inferred. Consolidated table:
`FIGURE_AUDIT_CONSOLIDATED.csv` (118 rows, with deciding values per row).

## Summary

| verdict | count |
| --- | --- |
| claim supported | 71 |
| claim overstated | 9 |
| claim false | 6 |
| claim undecidable from available tables | 14 |
| no claim-bearing text | 18 |
| display conventional | 93 |
| display conventional for a reproduction | 4 |
| display borderline | 13 |
| display wrong for the analysis | 8 |

## False claims

### 1. A12_F03 panel b — "Both models compress the range"

`docs/roadmap_runs/2026-09-27-followthrough/A12_heldout_predictions.csv`
(recipient AT2, floor 50, uncertainty 0.2, alpha 1).

Observed response spans -0.5323 to 0.5477, width **1.0800**. The source+TNF predictions span width
**1.4275** and the joint predictions **1.3410** — both *wider* than the observed range, and the
source+TNF predictions are more dispersed than the data (sd 0.3869 against 0.3478). Neither model
compresses anything.

Corrected to the property the table does support: neither model tracks the extremes, with
regression slopes of 0.33 and 0.51 against the observed response, and a note that both predicted
ranges are wider than observed. **Re-rendered.**

### 2. A16_F02 panel b — "Exceptional in 4 entries, unexceptional in the best-powered one" (already corrected on main)

`RQ_Specified/A16_cd177_state_attribution/tables/stage1/A16_C3_matched_gene_null.csv`,
endpoint `priming_associated`.

Four entries do have `frac_control_ge_cd177 = 0`, so the count of four is arithmetically right. But
one of those four, `exp2_sub_r1.0=12`, holds **284 control genes** — seven times the figure's own
40-gene floor. The figure's own criterion therefore admits **two** interpretable entries, not one,
and they disagree: `exp1_sub_r1.0=10` (500 controls) puts Cd177 at the 86th percentile of its null
(SMD 0.358380, null median 0.096928, p95 0.518926, 13.87% of controls reaching it), while
`exp2_sub_r1.0=12` puts it above every control gene and above the null maximum (SMD 1.307680
against null max 1.237905, quantile 1.000). "The best-powered one" (singular) misstates the power
structure and assigns the exceptional result to the under-powered side.

**No change is made here.** The `2026-09-29-rq-delivery-review` package on main had already reached
the same conclusion under finding R2 and resolved it with a preservation convention: the original
figure and script stay untouched, and the corrected presentation output lives beside them in
`figures/revision_20260929/` with `scripts/plot_amendment_figures_20260929.py`. Its revised panel b
reads "Above all controls in 4 entries; inside the null with the most controls: specificity
unresolved", which is consistent with the values above. This audit independently confirms that
wording. Editing the preserved original in place would have destroyed the very record R2 chose to
keep, so the in-place A16 F01/F02 edits prepared during this pass were reverted and excluded.

### 3. EN_C02 — "the AT1 gate fires in every AT2 cluster"

`trials/continuation/EN1/cluster_gate_crosstab.csv` (resolution 0.5) joined to
`EN1/cluster_marker_panels.csv`.

In Experiment 2, seven of the seventeen plotted clusters carry `top_panel_by_detection == AT2_gate`,
and `gate_AT1_frac` is exactly **0.0000** in two of them — cluster 1 (n=228) and cluster 8 (n=80).
That is five of seven, not every. Across all seventeen Experiment-2 clusters `gate_AT1_frac` is zero
in five (c1, c2, c8, c12, c16). Experiment 1 does satisfy the claim (8/8, 0.069-0.511).

Corrected to: the AT1 gate fires in every cluster where the AT2 gate itself fires, and is zero in
two sparsely-AT2 Experiment-2 clusters. **Re-rendered.**

### 4. FU_F02 — "survive every available adjustment"

`trials/followup/FU_A_verdicts.csv`, column `verdict`.

The frozen rule records `depth_dependent_or_inconclusive` for **12 of 12** endpoints. No endpoint is
depth-robust, including priming, AT2 identity and AT1 identity. The cause is mechanical:
`GSM7890836_thinned_3000_UMI` is NaN for all twelve endpoints because thinning leaves 26 Cd177+
cells, below the 30-cell floor, so the rule's requirement of sign agreement across all methods in
both libraries cannot be satisfied.

The figure's own footnote already disclosed this, so the figure contradicted itself: the title
claimed survival while the footnote reported "inconclusive" for every endpoint.

Corrected to state the frozen verdict first and the post-hoc relaxation second.
**Script corrected; the tracked PNG is stale — see "Stale figure files" below.**

### 5. FU_F03 — "a connected graph with populated intermediates"

`trials/followup/FU_T1_paga_connectivity.csv` and `FU_T2_intermediate_density.csv`.

Of the seven mutant subcluster nodes, cluster 14 has connectivity **0.0000** to all six others
(pairs 11-14, 12-14, 14-15, 14-16, 14-17, 14-18), so at the drawn threshold of 0.05 it is an
isolated node and only six of seven nodes form one component. This is visible in the rendered panel:
c14 is drawn with no edges. "Populated intermediates" is also weaker than stated — the median share
of cells in the middle 40% of the inter-centroid axis is 0.197 (Experiment 1, 21 pairs) and 0.252
(Experiment 2, 45 pairs), i.e. *below* the 0.40 that a uniform axis would give.

Corrected to name the exception and give the intermediate shares against the uniform expectation.
**Script corrected; the tracked PNG is stale.**

### 6. FU_F05 panel c — "The two profiles do not track each other"

`trials/followup/FU_W_distance_slopes.csv`, columns `size_relative_slope_pct_per_100um` and
`spcneg_relative_slope_pct_per_100um` — the thirteen plotted points.

The two slope columns are **positively correlated** across the thirteen points: Pearson r = +0.609,
p = 0.027. The panel asserts the opposite of what its own points show.

The figure's suptitle is separately fine: the growth slope is negative in 12 of 13 datasets while
the differentiation proxy splits 8 positive / 5 negative. That sign pattern is the reproduction of
the source's decoupling claim; the pooled correlation is not, and with no mouse or clone identifiers
deposited, co-variation is not identified from pooled bins at all.

Corrected to the per-dataset sign pattern, with co-variation left unstated rather than reversed.
**Script corrected; the tracked PNG is stale.**

## Overstated claims

| figure | displayed | table |
| --- | --- | --- |
| A16_F01 panel a | "removes most of each marginal difference" | true for 12 of 14 endpoint x library entries; both cycling entries keep over half (GSM7890835 40.6% removed, GSM7890836 45.7% with a sign flip). Already addressed on main under R2: the revised output in `revision_20260929/` reads "Matched contrasts are smaller than marginal contrasts; the priming contrast remains positive", which avoids the overclaim. **No change here.** Two residual vaguenesses in that revision are recorded but not defects: panel b keeps "Attenuation is not a choice of k" (true - attenuated at every k - though the matched value itself varies 2.1x in GSM7890836) and panel c keeps "Residual positional imbalance stays substantial" where the computable statement is 25 of 40 components above 0.1. |
| A12_F01 panel b | "the same index does not" | supported for the primary alternative-to-joint contrast (0.2098 to 0.2283), but the recipient-only model in the same panel (0.364795) does beat the training mean (0.408475). Scoped to "no gain over source + TNF". **Re-rendered.** |
| A12_F02 | "Most recovered IL1B RNA ... in every histology" | holds at the median in all five histologies (51.7-72.1%) but 14 of 70 patients fall below half. Retitled to "the median patient in every histology", with the 14-of-70 count in the title and an interquartile bar added. **Re-rendered.** |
| EN_F02 | "Il1r1 deletion changes reprogramming-associated RNA" | 17 of the 32 displayed cross-library ranges include zero; direction is consistent in 15 of 32. Cd177-associated RNA is the endpoint that holds (4/4 panels, -2.26 to -2.74). Retitled. **Stale PNG.** |
| EN_C01 | "transition states are mutant-specific" | falsified as exclusivity: 7 of 8 non-mutant libraries contain transition-gated cells (1-10 each, 32 total), and 5 of 12 mutant libraries sit inside that range. Only 5 mutant libraries clear the 30-cell floor. Retitled to the floor statement. **Re-rendered.** |
| FU_F04 panel b | "Cycling differences between states are small and inconsistent" | "small" holds only for AT2 vs mixed (12 libraries, median -0.015, all \|SMD\| <= 0.134). The two 4-library comparisons are not small: AT2 vs transition median +0.357 (to +0.628) and transition vs mixed median -0.30 (to -0.81). Retitled. **Stale PNG.** |
| rq_a1_chromatin panels e, g, h, i | "by group" | **Corrected.** **GSE310539 contributes one wildtype PBS well (7,340 nuclei) and one wildtype SeV well (8,093).** The three compared groups are PBS reference n=7,284, SeV reference n=7,507 and SeV transitional n=586 — two libraries, not two animal groups. The spread shown is across nuclei. No panel title, axis label or footnote says so, and the caveat string "cell SD is a scale, not uncertainty across animals" appears in only one A0 script elsewhere in the repository. Between-group differences here have no biological replication. A footnote now states the well count, that the SeV reference and SeV transitional groups are subsets of one library, and that violin spread is a scale rather than uncertainty across animals. **Script corrected; PNG stale (script 16 needs --figures with --replot or --rebuild-embeddings).** |
| rq_a11 gallery decision | "Shared score increases motivate a shared-component hypothesis" | increases in LUAD (19/23 patients, mean +0.327), AIS (9/12, +0.100) and MIA (3/4, +0.183) versus matched normal, but **not in AAH** (median -0.078, only 3/8 patients, range -0.456 to +0.640). **Corrected** in the gallery decision text. |
| icap_origin_by_cre_line | "Origin of the injury-induced capillary state" | direction is consistent in every animal (Kit-MerCreMer +1.70, +7.26, +10.41 points; Car4 -7.23, -1.45; Ednrb -2.12, -1.99, -2.12) but this is n = 2-3 animals per line at one timepoint with no recombination-efficiency control. Consistent with a CAP1 origin, not a test of it. Retitled to "Lineage-label frequency ...", with the enriched-in count computed at render time and the missing control named; the display now draws the two same-animal values as paired slopes instead of offset clouds, and per-line n is on the axis. **Script corrected; PNG stale (needs GSE262927/processed/final_clustered.h5ad).** |

## Stale figure files

These scripts were corrected but could not be re-rendered here, because their inputs are outside
this checkout: `plot_batch1.py` and `plot_followup.py` need
`Research Article/gate2_C2_england_2025/processed/`, which is not tracked. **The tracked PNG and SVG
for the figures below still carry the uncorrected text.** Re-run with `--data-root` pointed at an
environment that has the processed directory, then commit the regenerated assets.

- `trials/batch1/figures/EN_F02_genotype_contrasts.{png,svg}`
- `trials/followup/figures/FU_F02_depth_control.{png,svg}`
- `trials/followup/figures/FU_F03_topology_and_within_cluster.{png,svg}`
- `trials/followup/figures/FU_F04_controls.{png,svg}`
- `trials/followup/figures/FU_F05_growth_differentiation.{png,svg}`

## Displays corrected

- **`rq_a6_composition` panel c** previously joined cell share, E2F transcript share and G2M
  transcript share with a line across non-ordinal categories on one "mean donor share" axis,
  reading a composition measure and a within-state expression measure off a shared scale. Now
  drawn as two grouped measures separated by a dashed rule, with the axis label naming which side
  is composition and which is transcript share, and no connecting line. **Re-rendered.**
- **`rq_a2_source_rank` panel c** previously showed one median rank per resource as a bare
  lollipop. Per-donor ranks are *not* deposited — `resource_summary.csv` carries only the median
  across 22 donors — so no dispersion can honestly be drawn. The panel now shows where AREG-EGFR
  sits inside each resource's full rank range on a log axis (rank 6 of 208 in cellphonedb to 44.5
  of 518 in italk), with the median-only limitation stated in the axis label. **Re-rendered.**
- **`A12_F02`** converted from a jittered strip to per-patient points with median and
  interquartile bars on a deterministic offset. **Re-rendered.**

## Not yet corrected

Recorded here rather than silently left out.

- Five remaining wrong-display figures and thirteen borderline ones. The substantive remainder is
  `A12_F01`, still an RMSE ladder where the leave-one-patient-out design supports a paired
  per-patient display (the table has one held-out loss per patient, and 7 of 12 improve under the
  joint model in the AT2 arm). Changing it alters what the figure shows rather than how it is
  worded, so it is left for a deliberate decision.
- Fourteen claims whose deciding table is not available here, listed in the consolidated CSV with
  the missing input named per row. These are recorded as undecidable, not as supported.
- Ten frozen Cardoso figures under `gate2_05_cardoso_2026/trials/` have their claim strings
  catalogued; three were verified numerically and the rest were not. Scripts under
  `reports/execution_sources/**` are archival copies of scripts as executed and were not touched.

## Coverage limits of the geometric collision check

Text-collision checks were run on 19 of 36 RQ figures, 21 of 44 Research Article figures and 12 of
42 gallery figures. The remainder could not be re-rendered from the inputs available. Collision
counts in the consolidated CSV are therefore a lower bound, and a blank means unassessed, not clean.
