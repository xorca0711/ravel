# England 2025: continuation results through EN7 and CD177

**Completed 28 September 2026 (Asia/Seoul); run timestamps are UTC.** Executed under the [frozen continuation contract](CONTINUATION_CONTRACT.md) ([exact rules](config/continuation_contract.json), [amendments CA1-CA3](config/continuation_amendments.json)), after [batch1](RESULTS_BATCH1.md). Descriptive, source-exposed re-analysis; libraries and animals are the units, biological pool identities remain unknown, and no p values are reported. Existing claim grades are unchanged. Every number below is read from a table under `trials/continuation/`; the [verification record](trials/continuation/verification.json) recomputed 1,178 checks from cached counts (maximum discrepancy 1.8e-15).

**Main finding.** Within an independently defined transitional compartment, Cd177 RNA detection marks cells with higher priming-associated and AT2/AT1 identity RNA and lower Itga2 and shared/lesion remodelling RNA, in both eligible libraries; its association with cycling is library-dependent and shrinks under depth matching. The Il1r1 genotype lowers transition-gate occupancy and within-state Cd177 RNA without raising AT1 identity. The deposited stochastic simulator contains a branch error that materially changes the mutant (q = 0.7) clone-size law. The CD177 question does not transfer to the two repair datasets, because Cd177-positive transitional cells are essentially absent there.

## What ran

| Stage | Script | Scope | Output |
|---|---|---|---|
| EN0 / prep | `scripts/prepare_continuation.py`, `en0_ledger.py` | 20 libraries, 44,196 source-QC cells (identical to batch1), CA3 doublet join, primary 41,811 / strict 39,583, gates, mapped-gene scores, two exact 1,000-UMI thinnings | `trials/continuation/prep/` |
| EN1 | `run_clustering_continuation.py` | Per-experiment clustering (CA2 igraph multilevel, seed 20260928, r 0.5/1.0/1.5) | `trials/continuation/EN1/` |
| EN2-EN5 | `run_rna_continuation.py` | Composition, within-state pseudobulks, separated axes, WT-YFP context, CD177 contrasts; 5 variants | `trials/continuation/EN2_5/` |
| EN6 | `run_simulation_en6.py` | Three simulator implementations, analytic check, LOMO spread | `trials/continuation/EN6/` |
| EN7 | `run_external_en7.py` | Choi 2020 and Niethamer 2025 transfer | `trials/continuation/EN7/` |
| Verification, figures | `verify_continuation.py`, `plot_continuation.py` | 1,178 checks; six inspected figures | `verification.json`, `figures/` |

Matrix checks: one identical feature table for all libraries (31,053 genes, 36 duplicated symbols summed), integer counts, no duplicate barcodes, **no reporter features** (RFP/YFP are library metadata only). The [EN0 ledger](trials/continuation/prep/EN0_availability_ledger.json) records pool, pair, batch, author-annotation and spatial identities as unknown or absent; nothing in the continuation changed that.

## 1. State reliability (EN1): the transition gate is coherent, the AT1 gate is not

![Cluster versus gate cross-tabulation](trials/continuation/figures/EN_C02_cluster_gate_crosstab.png)

At resolution 0.5, Experiment 1 gives 13 clusters and Experiment 2 gives 17 ([sizes](trials/continuation/EN1/cluster_sizes.csv), [cross-tab](trials/continuation/EN1/cluster_gate_crosstab.csv)).

- **Transition gate** (>=2 of Cldn4/Ndrg1/Sox9): 88% (Exp 1) and 96% (Exp 2) of gated cells sit in two clusters. Exp 1 cluster 11 (2,456 cells) is 98% mutant RFP and holds 79% of Exp 1 mutant transition cells; Exp 2 cluster 15 holds 90% of Exp 2 mutant transition cells. WT-baseline libraries contribute no cells to these clusters.
- **AT1 gate** (>=2 of Ager/Hopx/Clic5) is not cluster-concentrated: 17-18% of cells in Exp 1's largest AT2 clusters and 29-43% in Exp 2's AT2 clusters pass it, and the two richest clusters hold only 43-51% of AT1-gate cells. No distinct AT1 cluster exists in these sorted libraries. The exclusive **mixed** state therefore mostly reflects low-level Ager/Hopx detection in AT2 cells and must not be read as AT1 differentiation or as the paper's mixed-identity population.
- **Cd177-positive cells** concentrate in one high-depth mutant cluster per experiment (Exp 1 cluster 12: 1,819 cells, 96% 2-week mutant RFP, 21% Cd177 >= 1, 51% AT1 gate, 25% cycling >= 2 markers, median 13.8k UMIs versus 4-6k in AT2 clusters).
- Immune clusters retain 30-56% of their cells under the primary rule; the strict variant removes more.

This is a sensitivity reconstruction, not an author-label reproduction, and no resolution was chosen on an outcome.

![Exclusive-gate state occupancy](trials/continuation/figures/EN_C01_state_occupancy.png)

## 2. Il1r1 genotype (EN2): lower transition occupancy and within-state Cd177 RNA, no AT1 rise

![Genotype contrasts](trials/continuation/figures/EN_C04_genotype_contrasts.png)

Homozygous deletion minus heterozygous, two libraries per side, difference of library means with the range of the four cross-library differences ([composition](trials/continuation/EN2_5/EN2_composition_contrasts.csv), [within-state](trials/continuation/EN2_5/EN2_within_state_contrasts.csv)):

| Quantity | 2 weeks | 12 weeks | Reading |
|---|---:|---:|---|
| Transition-gate fraction (primary) | -0.057 | -0.123 | Lower in every cross-library comparison at both times; -0.007 / -0.014 at 1,000 UMIs |
| AT2-state fraction (primary) | +0.077 | +0.244 | Directions agree only at 12 weeks |
| Cd177 pseudobulk within AT2 state | -3.96 | -3.94 | Also -4.28 / -2.30 within mixed state; log2(CPM+1) units |
| AT1 identity within AT2 state | -0.50 | -0.60 | No maturation shift |
| Response / Nfkbia within AT2 state | -0.05 / -0.04 | -0.19 / -0.05 | Near zero |

Within-state contrasts for the **transition state are unavailable**: homozygous libraries hold 0-12 transition-gated cells. Composition and conditional expression answer different questions; the difference is not causal mediation.

## 3. Separated RNA axes (EN3): library heterogeneity exceeds condition effects

Per library, with a threshold fixed as the pooled 90th percentile of the two Experiment-1 WT-baseline libraries ([table](trials/continuation/EN2_5/EN3_axes_by_library.csv)): the response-high fraction ranges 3-52% across libraries and differs 2-3x between replicate libraries of the same condition (GSM7890835 0.52 versus GSM7890836 0.22 at 2 weeks; GSM7890837 0.28 versus GSM7890838 0.10). Nfkbia-high fractions (2-15%) do not track response. The within-library Spearman correlation between response and Nfkbia is 0.24-0.54 in every library including WT baseline, so no library-specific decoupling of feedback from response is visible. Snapshot RNA is not NF-kB activity or duration.

## 4. WT cells in oncogenic tissue (EN4)

At 2 weeks, WT-in-oncogenic-tissue YFP libraries exceed the single Confetti-YFP baseline library in Spp1 (+3.3), Dlk1 (+4.0), Cd177 (+1.3), transition RNA (+1.0) and priming (+1.7) log2(CPM+1) units, with response +0.1, Nfkbia -0.7 and cycling -0.2 ([table](trials/continuation/EN2_5/EN4_wt_yfp_contrasts.csv)). Contemporaneous mutant RFP exceeds oncogenic YFP on Cd177 (+3.4), Areg (+2.0), cycling (+1.1) and AT1 identity (+0.8). One baseline library, unverified pairing, no cell-to-clone distance; the 4-day arm has no matched baseline.

## 5. CD177 within the transitional compartment (EN5, idea 6)

![CD177 contrasts](trials/continuation/figures/EN_C03_cd177_transition.png)

The primary contrast (Cd177 >= 1 UMI versus zero, >= 30 cells on each side, within transition-gated primary-included cells) is **available in two libraries only**: GSM7890835 (79 vs 799) and GSM7890836 (60 vs 598), both 2-week mutant RFP ([groups](trials/continuation/EN2_5/EN5_cd177_groups.csv)). No Il1r1 library, no WT library and no 1,000-UMI-thinned variant qualifies (the transition gate collapses to 90 and 47 cells at 1,000 UMIs). Standardized mean differences are cell-level effect descriptions within one library, not tests ([contrasts](trials/continuation/EN2_5/EN5_cd177_contrasts.csv), [matched](trials/continuation/EN2_5/EN5_cd177_matched.csv)).

| Endpoint | GSM7890835 | GSM7890836 | Consistency |
|---|---:|---:|---|
| Cycling score (primary) | -0.04; matched -0.05 (4 strata, 63 vs 408) | +0.48; matched +0.19 (2 strata, 35 vs 111) | Library-dependent; shrinks under depth x hypoxia matching |
| Fraction with >= 2 cycling markers, Cd177-detected vs zero | 0.38 vs 0.33 | 0.47 vs 0.17 | Same pattern |
| Priming (Lcn2/Lrg1/Retnla/Ptgs1) | +1.60 | +2.17 | Positive in all four cycling strata (0.89-2.47) |
| AT2 identity | +0.94 | +1.41 | Positive in all four strata (0.47-1.37) |
| AT1 identity | +0.85 | +0.52 | Positive in all four strata (0.36-1.04) |
| Itga2 | -0.48 | -0.75 | Negative in all four strata (-0.39 to -0.79) |
| Shared / lesion remodelling modules (disjoint) | -0.70 / -0.88 | -1.21 / -1.10 | Negative in all four strata (-0.41 to -1.20) |
| Transition RNA | -0.18 | -0.79 | |
| Response, Nfkbia, Tonsl, hypoxia, p53 controls | within +-0.2 | -0.4 to -0.8 | No shared direction |

Within cycling strata the secondary directions hold but magnitudes are smaller in the cycling-high stratum; depth x hypoxia-matched secondary strata fall under the floor, and Cd177-detected cells are deeper-sequenced (section 1), so **sequencing depth remains an alternative explanation** for the identity-module differences. Cd177 counts among detected cells spread from 1 to 53 UMIs without a break; no bimodality is claimed. The >= 2-UMI sensitivity reproduces every direction. The co-detection permutation null at 1,000 UMIs is uninformative (0 observed, ~0 expected).

**Reading.** Cd177 RNA detection marks a primed, identity-retaining subset of transition-gated mutant cells rather than a more cycling one. Association cannot show that Cd177 sustains division; Cd177 RNA is not surface CD177; and the paper's Cd177 mixed state is not equivalent to this gate.

## 6. Deposited simulator (EN6, idea 5)

![Simulator implementations](trials/continuation/figures/EN_C05_simulator_implementations.png)

Three implementations of `sim_two_pop_model.m` were run with the script's literal parameters, 100 replicates x 1,000 clones, two seeds ([summary](trials/continuation/EN6/simulation_summary.csv), [differences](trials/continuation/EN6/implementation_differences.csv)). The boundary-correct Gillespie reproduces the analytic one-lineage birth-death law (extinction-probability error <= 0.0013, conditional CCDF error <= 0.007; [check](trials/continuation/EN6/analytic_birth_death_check.csv)).

| Block | Literal vs corrected S-loss branch (CA1), KS | Literal vs Gillespie, KS | Reading |
|---|---:|---:|---|
| Confetti (q = 0.5), 12-72 wk | 0.000 | 0.004-0.025 | Branch inert; horizon/rate-switch effects small |
| Red2Kras YFP (q = 0.5), 1-4 wk | 0.000 | 0.003-0.100 | Same |
| Red2Kras RFP (q = 0.7), 1 / 2 / 4 wk | 0.104 / 0.281 / 0.281 | 0.098 / 0.278 / 0.293 | **Branch error dominates**: slow-population loss never fires, so 91-96% of clones reach size >= 2 (literal) versus 57-59% (corrected) and 50-55% (Gillespie); conditional mean size 66 vs 80 cells and P90 66 vs 36 at 2 weeks |

Seed-to-seed KS distances are <= 0.011, so these are not Monte Carlo fluctuations. Batch1 leave-one-mouse-out fits ([spread](trials/continuation/EN6/lomo_parameter_spread.csv)): kras two-component mixtures have non-overlapping components in every held-out fit, but the fast component varies by cohort (kras1w geometric p 0.037-0.071, weight 0.14-0.28; kras2w p 0.004-0.005, weight 0.30-0.34; kras4w p 0.001, weight 0.22-0.25), and Confetti mixture weights range 0.09-0.89 with overlapping components, i.e. not identifiable. Which implementation produced the published RFP curves is not established from the deposit; clone merger/segmentation is not modelled; the joint spatial analysis (EN6c) stays blocked without mouse and clone identifiers.

## 7. Repair transfer (EN7)

![Repair transfer](trials/continuation/figures/EN_C06_repair_transfer.png)

The Cd177 contrast is **unavailable in every repair unit** ([groups](trials/continuation/EN7/EN7_cd177_groups.csv)): Choi day-14 has 117 transition-gated cells with 2 Cd177-detected, day-28 21/1, PBS 0; the six Niethamer day-0/11/25 samples hold 1-50 transition-gated cells with 0-1 Cd177-detected. Unit-level pseudobulks ([contrasts](trials/continuation/EN7/EN7_contrasts.csv)) show the shared repair programme rising transiently in both studies: cycling +2.8 (Choi d14 - PBS) and +3.7 (Niethamer d11 - d0, all 2x2 directions agree), transition RNA +2.1 / +3.0, shared disjoint module +1.1 / +1.4, lesion disjoint module +0.35 / +0.39 and Itga2 +0.55 / +2.8, all reversing by d28 / d25. Cd177 rises transiently in Choi (+2.0 then -1.7) but not consistently in Niethamer (-0.33 with disagreeing directions). The TNF/NF-kB disjoint response is flat (about +0.1) and Nfkbia is lower at peak repair. Against author labels ([cross-tab](trials/continuation/EN7/EN7_author_state_crosstab.csv)), the transition gate captures 10% of Choi DATP cells (88/880) and 27% of Niethamer Alveolar_transitional cells (62/229); the AT1 gate is specific where AT1 cells exist (Niethamer AT1 1,677/1,759) but the mixed state covers 15% of Choi hAT2 and 52% of Niethamer AT2. Descriptive transfer on already exposed data with single pooled libraries (Choi) or two animals per day (Niethamer); not independent A11 validation and no injury-cancer axis.

## Verdicts on Notion ideas 4-6

| Idea | Verdict from these deposits | What would change it |
|---|---|---|
| **4** Distinct AT2 founders yield distinct AT1 progeny | **Not testable here.** No founder-to-descendant link, no reporter features in the matrices, and no mature AT1 population in the sorted libraries; the AT1 gate leaks into 17-43% of AT2-cluster cells. The mixed state is an AT2 co-detection phenotype, not AT1 progeny. | Barcoded lineage recording with AT1-resolved endpoints; matched surface CD177/ITGA2 sorting with clone readout |
| **5** Stochastic cycling versus Itga2 plasticity/selection | **Model audit changes the picture.** The deposited RFP simulation's S-loss branch never fires, and its literal clone-size law differs from a correct implementation (KS 0.28). Batch1's held-out comparison already favoured a continuous-heterogeneity alternative at 2-4 weeks. Within transition-gated cells Itga2 RNA is lower where Cd177 is detected (SMD -0.4 to -0.8), so the two markers do not label the same cells. | A refit of the two-population model with a corrected implementation against the deposited CCDFs; matched Kras/Trp53 arms with Itga2 fate tracing |
| **6** CD177 mixed state sustains division | **Not supported as a general association; partially supported in one library.** Cycling is higher among Cd177-detected transition cells in GSM7890836 (SMD +0.48, matched +0.19) and not in GSM7890835 (-0.04). The consistent signal is priming/identity RNA up and Itga2 and remodelling modules down. Causality, protein positivity and persistence are out of reach. | Surface CD177 sorting from the same transitional gate with EdU/Ki67 protein and short-term clone growth; Il1r1-mutant and repair contexts with enough Cd177-positive transitional cells |

## Identifiers and data that would unblock conclusions

1. Biological pool, animal and reporter-pair identities for the 20 libraries (the ENA run map does not supply them); this alone would allow biological replication instead of library ranges.
2. Author per-barcode state labels for the six-state reconstruction and the exact 29,563 / 9,211 retained-cell sets.
3. Mouse, central-clone and neighbour-clone identifiers for the spatial pair arrays (EN6c).
4. The Mendeley Figure 1 PDF (HTTP 403, never inspected) and confirmation of which simulator implementation produced the published best-fit curves.
5. A repair or injury dataset with a sizeable Cd177-positive transitional population, or a targeted experiment sorting surface CD177 within Cldn4/Ndrg1/Sox9-defined transitional cells.

## Status ledger

| Trial | Status after continuation | Remaining boundary |
|---|---|---|
| EN0 | Matrix checks and availability ledger complete | Pool/pair/batch/spatial identities unknown |
| EN1 | Source-inspired clustering complete, gate reliability characterised | Not an author-label reproduction |
| EN2 | Composition and within-AT2/mixed contrasts complete | Transition within-state contrast unavailable |
| EN3 | Separated axes with declared threshold complete | Snapshot RNA only |
| EN4 | 2-week contrasts complete | Single baseline library; 4-day arm unavailable |
| EN5 | CD177 contrasts complete in two libraries | Depth confound unresolved; other contexts unavailable |
| EN6 | Simulator audit and LOMO spread complete | EN6c spatial joint analysis blocked |
| EN7 | Choi and Niethamer transfer complete | Cd177 contrast unavailable; descriptive only |

Run records, contract/script/input/output hashes and interpreter details are in each stage's `run_record.json`; regenerable caches sit under the ignored `processed/continuation/`. Batch1 files are unchanged.
