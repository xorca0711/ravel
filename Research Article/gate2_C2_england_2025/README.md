# England et al. 2025: regeneration, NF-kB feedback and mutant AT2 states

**Questions derived, 28 September 2026:** the follow-up proposes [A16 and A17](../../RESEARCH_QUESTIONS.md) (Cd177 as intrinsic programme versus transcriptional position; founder-class support under a boundary-correct simulation), both pending the owner's retain or reject.

**Follow-up executed, 28 September 2026:** [RESULTS_FOLLOWUP.md](RESULTS_FOLLOWUP.md) adds depth control of the CD177 associations, a calibrated AT1 module gate, two-round subclustering with UMAP and undirected topology tests of the paper's transition model, under the [follow-up contract](config/followup_contract.json). No trajectory direction is claimed; the paper itself ran no trajectory method.

**Continuation executed, 28 September 2026:** [RESULTS_CONTINUATION.md](RESULTS_CONTINUATION.md) reports EN0-EN7 under the frozen [contract](CONTINUATION_CONTRACT.md) and amendments, with 1,178 verification checks and six figures; the [handoff](../../docs/handoffs/2026-09-28-england-en7-cd177.md) records the sessions. Batch1 results below remain unchanged.

**Execution update, 28 September 2026:** the owner authorized the actual analysis after planning. The [first execution batch and four figures](RESULTS_BATCH1.md) are complete: 20 libraries, 44,196 source-QC cells, and 164,453 clonal measurements across 44 source-indexed mice. Numerical verification passed; exact source-state reproduction, independent pool identities and inferential spatial joins remain unresolved. The text below records the original planning/source-intake state.

**Reading gate 2C, item 2; stable roadmap paper 12. Owner read confirmed 27 September 2026.**
[Paper](https://doi.org/10.1016/j.stem.2025.01.011), Cell Stem Cell 32, 375-390.
This assistant-authored synthesis follows the owner's request to structure re-analysis and further analysis after reading. It is a plan with a completed source/design audit, not a completed biological re-analysis or an owner-approved interpretation.

**Recommended focus:** determine whether Il1r1-dependent reprogramming, NF-kB feedback-associated RNA and acquisition of AT1 identity separate across mutant and neighboring wild-type populations. In a complementary branch, use the deposited clone measurements to ask whether growth heterogeneity and proximity-dependent expansion are robust at the mouse level. Keep molecular state, clone growth and mature fate as separate endpoints.

Start with the [analysis plan](ANALYSIS_TRIAL_PLAN.md), [source/design audit](SOURCE_AUDIT.md), and [20-library manifest](metadata/geo_library_manifest.csv). The [extracted parameters](england_2025_extracts.json) distinguish paper settings from proposed choices. All EN identifiers below are paper-local.

## How this fits the repository

The repository uses public lung single-cell RNA, chromatin and complementary measurements to discover reproducible distributions and molecular phenotypes and turn them into discriminating biological questions. It does not yet have a common measured repair outcome across all datasets. England supplies a mechanistic source study and two complementary data modalities, not a universal repair-to-cancer trajectory.

| Layer | Existing authority | Placement of England work |
|---|---|---|
| Purpose and question definitions | [Root overview](../../README.md), [question register](../../RESEARCH_QUESTIONS.md) | Relate source findings to existing questions; do not create new A identifiers from every marker |
| Paper-specific evidence | [Paper roadmap](../README.md) | This folder owns England source synthesis, EN trials and eventual paper-specific figures |
| Question-specific execution | [RQ_Specified](../../RQ_Specified/README.md) | A new cross-study test belongs with its owning question once specified |
| Shared measurement and code | [Architecture](../../docs/RESEARCH_ARCHITECTURE.md), [measurement contracts](../../docs/RQ_MEASUREMENT_CONTRACTS.md), analysis/lib and analysis/config | Reuse count readers, provenance and palette; preserve study-specific scales and biological units |
| Evidence and corrections | [Claims](../../CLAIMS.md), analysis/corrections | Existing Cardoso C3 measurements stay where they ran; this plan adds no graded claim |
| Current versus historical work | [Progress](../../PROGRESS.md), [AI context](../../AI_CONTEXT.md), archive | Record new source corrections prospectively; preserve frozen reports and unrelated A11 continuation |
| Raw inputs and private annotations | Ignored local raw_data and external reading folder | Reference inputs; do not relocate counts, copy private reading notes or track source PDFs |

The folder uses stable paper number 12, following the existing naming contract. Gate item C2 is not global question A2 or a Cardoso trial. Older Notion links still use the historical `Thesis/` prefix; the current repository prefix is `Research Article/`.

## Study note: five questions

1. **What question did the paper test?** How do AT2 clonal dynamics and fate change after Kras activation, and which regenerative mechanisms permit early tumor formation? The paper links homeostatic growth heterogeneity, Il1r1-dependent state entry, differentiation-associated NF-kB feedback, and changes in neighboring wild-type AT2 behavior.
2. **What is the evidence?** Clone-resolved lineage tracing and mathematical modeling; scRNA-seq of sorted lineage-labeled epithelium; Il1r1 loss of function; organoid and transplantation assays; and NF-kB perturbation with morphological/marker endpoints. Published functional evidence is stronger than any RNA-only reproduction, but does not transfer causal authority to a new score.
3. **Which variables are reusable?** Experiment, reporter-sorted population, genotype and collection time; AT2, primed, cycling, DATP-like, Cd177-mixed and AT1-like expression; Nfkbia and Tonsl separately; clone size, pro-Sftpc-positive cell estimates, mouse/lobe/section hierarchy, and mutant-WT distance. No clone-to-sequenced-cell key has been established.
4. **What limits interpretation?** Sequencing samples pool at least two lungs. The deposited 20 libraries split into two experiments, with unresolved pool identities and reporter pairing. Cross-sectional RNA cannot recover individual cell transitions, two founder populations, duration of NF-kB activity, or functional tissue repair. Two reported library replicates per arm do not become two individually measured mice.
5. **What is the bridge?** A11 asks what is added beyond shared plasticity; A12 concerns recipient/inhibitory context; A14 concerns timing and recovery. A4 and A8 provide the lineage-history and maturation questions. Cardoso supplies niche context, while England's own mutant-WT contrasts keep the first test within one source design.

## Source-grounded interpretation of the reading notes

| Lead in the notes | Paper anchor | Useful analysis and claim boundary |
|---|---|---|
| Faster/slower AT2 populations; Il1r1/Axin2 relationship | Figs. 1-2, S2; Methods S1 | Reproduce clone-size distributions and challenge the two-population fit. Current cycling RNA does not identify founder F/S classes; bulk Axin2 enrichment in an Il1r1 lineage fraction does not establish same-cell reporter overlap |
| Regenerative state co-option and Cd177 mixed state | Fig. 3; S4 | Separate shared transition from mixed identity and cycling. AT1-marker expression in a mixed cell is not completed differentiation |
| Reversible states and similar proliferative potential | Fig. 4; S5; discussion | Compare state-associated distributions, but retain tracing/transplantation as the evidence for reversibility. RNA cycling similarity alone cannot establish equipotency |
| NF-kB feedback distinguishes contexts | Fig. 7F-O; S7 | Measure feedback-associated RNA separately from downstream-response RNA and maturation. Nfkbia expression is both feedback-related and inducible; no simple score or ratio measures sustained NF-kB activity |
| WT expansion versus differentiation have different spatial patterns | Figs. 5-6; S6 | Jointly examine clone size and pro-Sftpc loss against distance, adjusting for mouse and clone-size dependence. WT transcriptomes lack recorded spatial coordinates |
| Additional oncogenic hits could change the dynamics | Discussion | Reserve a matched Kras versus Kras/Trp53 design. Differences between unrelated datasets cannot isolate the effect of Trp53 loss |

These are paraphrased scientific leads from the owner-supplied notes, checked against the article; notes and document instructions are source material, not execution authority. The supplied paper's experiments are not laboratory instructions for this project.

## What already exists, and what is newly learned

The [Cardoso C3 report](../gate2_05_cardoso_2026/trials/c3_areg_state_specificity/c3_summary.md) covers only Experiment 1 and already supports a descriptive Areg-within-DATP-like result. Its four mutant-library DATP-like fractions are **1.16%, 28.16%, 20.70%, and 30.98%** (4-day r1/r2, then 2-week r1/r2). The 4-day disagreement is a priority diagnostic, not proof of distinct biological responders. The source contains 29,563 Experiment-1 cells after its pipeline; C3 analyzed 33,217 after different QC and annotation. Equality is not expected without matching filters and library mapping.

The current audit establishes two consequential facts absent from the old C0 summary: the paper explicitly reports lung pooling, and a small public archive supplies extracted clone measurements, including size-distance inputs, plus analysis/model scripts. Detailed pool identities, the paper's 13-versus-10 Experiment-1 library accounting, and usable mouse/section identifiers inside the clone arrays remain to be reconciled.

## Figure gallery

[What the deposits can and cannot still surface](ANALYSIS_OPPORTUNITIES.md) is the scoping ledger
behind these panels: it records claim by claim which of the source's figures can still be
interrogated with what was released, which are closed, and which are blocked and on what.

Fourteen rendered figures across three analysis stages, each captioned beside the analysis that
produced it and linked here to its plotted tables, generating script and run record. Only generated,
visually checked figures appear; nothing is embedded as a placeholder. Two limits apply to every
panel and are not repeated in each caption: **the experimental unit is the sequencing library or the
pooled clone dataset, never the animal**, because no biological pool or animal identities were
deposited, and **no panel carries a transition arrow, a pseudotime axis or a direction**, because the
source ran no computational trajectory and this deposit cannot establish one. Cross-library and
cross-dataset ranges are ranges, not confidence intervals.

| Stage | Figures | What the set establishes |
|---|---|---|
| Batch 1 (first pass) | EN_F02, EN_F03, EN_F05, EN_F06 | Il1r1-dosage contrasts, per-library distribution shape, the clone-size model comparison and the pooled spatial profiles |
| Continuation (EN0–EN7) | EN_C01–EN_C06 | State occupancy, cluster-versus-gate concentration, CD177 contrasts, genotype contrasts, the simulator audit and transfer to two external repair cohorts |
| Follow-up (FU_A–FU_W) | FU_F01–FU_F05 | Round-2 embedding, depth controls, within-subcluster conditioning, calibration and equipotency controls, and the growth-versus-differentiation distance profiles |

The batch-1 identifiers are not sequential: no EN_F01 or EN_F04 exists in the render record, the
visual review or the plotting script, so the set is complete as recorded.

### EN_F02, EN_F03: Il1r1 genotype contrasts and per-library distributions

![Il1r1 genotype contrasts](trials/batch1/figures/EN_F02_genotype_contrasts.png)

![Per-library RNA distributions](trials/batch1/figures/EN_F03_library_distributions.png)

First-pass library contrasts by Il1r1 dosage, and the per-library distributions behind them. The
distributions are shown because between-library spread of the same condition is large enough that a
contrast of means alone would misrepresent it.
[Library contrasts](trials/batch1/rna/library_contrasts.csv) ·
[per-library expression](trials/batch1/rna/library_expression.csv) ·
[occupancy](trials/batch1/rna/phenotype_occupancy.csv) ·
[generating script](scripts/plot_batch1.py) ·
[run record](trials/batch1/rna/run_record.json) ·
[visual review](trials/batch1/figures/visual_review.json)

### EN_F05, EN_F06: clone-size models and pooled spatial profiles

![Clone distributions and model comparison](trials/batch1/figures/EN_F05_clone_models.png)

![Pooled spatial profiles](trials/batch1/figures/EN_F06_spatial_profiles.png)

Clone-size distributions with the two-population comparison, and the pooled distance profiles.
Sparse spatial bins are marked on the figure; all 25,173 deposited pair rows are `pooled_only` with
`biological_inference_allowed = False`, so these are descriptions of deposited profiles.
[CCDF by mouse](trials/batch1/clones/clone_CCDF_by_mouse.csv) ·
[leave-one-mouse-out fits](trials/batch1/clones/model_LOMO_by_mouse.csv) ·
[spatial bin profiles](trials/batch1/clones/spatial_pooled_bin_profiles.csv) ·
[generating script](scripts/plot_batch1.py) ·
[run record](trials/batch1/clones/run_record.json)

### EN_C01, EN_C02: state occupancy and cluster-versus-gate concentration

![Exclusive-gate state occupancy](trials/continuation/figures/EN_C01_state_occupancy.png)

![Cluster versus gate cross-tabulation](trials/continuation/figures/EN_C02_cluster_gate_crosstab.png)

Occupancy under the frozen exclusive gates, and how those gates sit across unsupervised clusters.
The cross-tabulation is the panel that matters most for what follows: the transition gate is
cluster-concentrated (88% of gated cells in two Experiment-1 clusters, 96% in Experiment 2), while
the AT1 gate is not (17–18% of cells in the largest Experiment-1 AT2 clusters and 29–43% in
Experiment 2 pass it), which is what motivated the calibrated module gate in FU_B.
[Composition](trials/continuation/EN2_5/EN2_composition.csv) ·
[cluster-gate crosstab](trials/continuation/EN1/cluster_gate_crosstab.csv) ·
[generating script](scripts/plot_continuation.py) ·
[run record](trials/continuation/figures/render_record.json)

### EN_C03, EN_C04: CD177 and genotype contrasts

![CD177 contrasts](trials/continuation/figures/EN_C03_cd177_transition.png)

![Genotype contrasts](trials/continuation/figures/EN_C04_genotype_contrasts.png)

The Cd177-positive versus Cd177-negative contrast within the transitional gate, available in only
two libraries, and the wild-type-versus-mutant genotype contrasts. Priming-associated RNA, AT2
identity and AT1 identity are consistently positive across both libraries while the cycling score is
library-discordant (SMD −0.04 against +0.48) — the discordance that the depth controls in FU_F02 and
the within-subcluster conditioning in FU_F03 were designed to resolve.
[CD177 contrasts](trials/continuation/EN2_5/EN5_cd177_contrasts.csv) ·
[matched contrasts](trials/continuation/EN2_5/EN5_cd177_matched.csv) ·
[composition contrasts](trials/continuation/EN2_5/EN2_composition_contrasts.csv) ·
[generating script](scripts/plot_continuation.py) ·
[run record](trials/continuation/figures/render_record.json)

### EN_C05: the deposited simulator's two implementations

![Simulator implementations](trials/continuation/figures/EN_C05_simulator_implementations.png)

The deposited MATLAB model run literally against the same model with its S-loss branch corrected,
both validated against the analytic birth–death law. The two agree exactly for Confetti and for
Red2Kras YFP (KS 0.000) and diverge for Red2Kras RFP at q = 0.7 (KS 0.104–0.281; size ≥ 2 fraction
0.91–0.96 literal against 0.57–0.59 for the fixed branch and 0.50–0.55 for the boundary-correct
Gillespie reference). Which implementation produced the published curves
is not established.
[Simulated CCDFs](trials/continuation/EN6/simulation_ccdf.csv) ·
[analytic check](trials/continuation/EN6/analytic_birth_death_check.csv) ·
[implementation differences](trials/continuation/EN6/implementation_differences.csv) ·
[generating script](scripts/plot_continuation.py) ·
[run record](trials/continuation/figures/render_record.json)

### EN_C06: transfer to two external repair cohorts

![Repair transfer](trials/continuation/figures/EN_C06_repair_transfer.png)

The shared repair programme in Choi 2020 (GSE145031) and Niethamer 2025 (GSE262927): cycling,
transition RNA and the disjoint remodelling modules all rise transiently and reverse by day 28 and
day 25. The Cd177 contrast is unavailable in both cohorts — 2 Cd177-positive cells among 117
transitional cells in Choi, 0–1 among 1–50 in Niethamer — which is the result that closed the
CD177-transfer question rather than a gap to be filled.
[Pseudobulk](trials/continuation/EN7/EN7_pseudobulk.csv) ·
[composition](trials/continuation/EN7/EN7_composition.csv) ·
[author-state crosstab](trials/continuation/EN7/EN7_author_state_crosstab.csv) ·
[generating script](scripts/plot_continuation.py) ·
[run record](trials/continuation/figures/render_record.json)

### FU_F01, FU_F02: round-2 embedding and depth controls

![Round-2 UMAP](trials/followup/figures/FU_F01_round2_umap.png)

![Depth control](trials/followup/figures/FU_F02_depth_control.png)

The two-round embedding reproducing the source's documented pipeline, and the depth controls for the
CD177 contrast. The frozen four-method rule returned "inconclusive" for every endpoint only because
3,000-UMI thinning leaves one library at 26 positive cells, below the pre-set 30-cell floor; under
the three methods available in both libraries all seven associations keep their sign, and
residualisation on log depth and detected genes retains 87–159% of each effect. The CD177
associations are not depth artefacts.
[Depth control](trials/followup/FU_A_depth_control.csv) ·
[verdicts](trials/followup/FU_A_verdicts.csv) ·
[round-2 clusters](trials/followup/FU_E_round2_clusters.csv) ·
[generating script](scripts/plot_followup.py) ·
[run record](trials/followup/run_record.json)

### FU_F03, FU_F04: within-subcluster conditioning, calibration and equipotency controls

![Topology and within-cluster contrast](trials/followup/figures/FU_F03_topology_and_within_cluster.png)

![Controls](trials/followup/figures/FU_F04_controls.png)

The most consequential panel in the package: repeating the Cd177 contrast **within** each round-2
subcluster largely dissolves it — Itga2 flips positive in 5 of 7 testable subclusters and AT2
identity ranges −0.36 to +1.27 — while priming-associated RNA persists in 5 of 7 (+0.36 to +2.32).
Cd177 therefore marks a position in the transcriptional landscape more than a cell-intrinsic
programme. The controls panel carries the AT1 module-gate calibration against author labels
(sensitivity 0.99, specificity 0.99), the intermediate-density and stationarity checks, and the
depth-matched cycling comparison across twelve libraries (median SMD −0.01, six positive and six
negative), which is consistent with equipotency.
[Within-subcluster contrasts](trials/followup/FU_C_within_subcluster_cd177.csv) ·
[AT1 gate calibration](trials/followup/FU_B_at1_gate_calibration.csv) ·
[intermediate density](trials/followup/FU_T2_intermediate_density.csv) ·
[cycling equipotency](trials/followup/FU_T4_cycling_equipotency.csv) ·
[generating script](scripts/plot_followup.py) ·
[run record](trials/followup/run_record.json)

### FU_F05: growth against differentiation with distance from a mutant clone

![Growth and differentiation distance profiles](trials/followup/figures/FU_F05_growth_differentiation.png)

A reproduction of the source's own comparison (Figures 5G–5J against 6E–6F) on the deposited pooled
pair arrays, not an independent contrast. Neighbour clone size falls with distance in all four
Red2Kras datasets and survives restriction to well-occupied bins, while the pro-Sftpc-negative
fraction is raised two- to five-fold at every distance with a slope inconsistent in sign in both
oncogenic and homeostatic tissue. Pair rows collapse with distance (4,953 at 25 um to 13 at 225 um in
kras1w), the limitation the source methods name, so the deposit is consistent with proximity
independence without being strong evidence for it.
[Distance slopes](trials/followup/FU_W_distance_slopes.csv) ·
[spatial bin profiles](trials/batch1/clones/spatial_pooled_bin_profiles.csv) ·
[generating script](scripts/run_spatial_decoupling.py) ·
[run record](trials/followup/FU_W_run_record.json) ·
[frozen rules](config/followup_contract.json)

## Connection to shared questions

| Question | England contribution | What would still be missing |
|---|---|---|
| [A4](../../RESEARCH_QUESTIONS.md#a4) | F/S growth and Il1r1 lineage context | Simultaneous Wnt/IL-1 activity history linked to lineage |
| [A8](../../RESEARCH_QUESTIONS.md#a8) | Mixed identity versus independent AT1 maturation panel | A linked mature fate/function outcome |
| [A11](../../RESEARCH_QUESTIONS.md#a11) | Genotype-associated additions to shared transitional RNA | Independent context transfer and separation from cycling/stress; England is already exposed through C3 |
| [A12](../../RESEARCH_QUESTIONS.md#a12) | Mutant versus WT feedback-associated context | Selective activation evidence; this sorted epithelial deposit does not supply matched immune/fibroblast triads |
| [A14](../../RESEARCH_QUESTIONS.md#a14) | Timing hypothesis motivated by the perturbation results | Withdrawal/post-entry perturbation linked to later fate, not just different harvest times |
| [A2](../../RESEARCH_QUESTIONS.md#a2), [A9](../../RESEARCH_QUESTIONS.md#a9) | Existing Areg result and candidate WT-response ligands | Delivery, receptor engagement and independently matched recipient outcomes |

The next executable task is EN0: recover the pool/batch map and clone-array schema, then freeze the first EN1/EN2 contrast. This work does not replace the separate computational research pipeline already recorded in the handoff.
