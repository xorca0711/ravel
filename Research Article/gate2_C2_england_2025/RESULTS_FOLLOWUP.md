# England 2025 follow-up: depth control, state topology and the transition model

**Completed 28 September 2026 (Asia/Seoul).** Executed under the [follow-up contract](config/followup_contract.json), frozen at commit `71f8ba0` before any endpoint was computed, on top of the [continuation results](RESULTS_CONTINUATION.md).

**Exposure is full and declared.** Every batch1 and continuation endpoint had already been evaluated and reported before this contract was written. This is an openly exploratory follow-up on exposed data. It cannot constitute independent validation, and nothing here changes a claim grade.

**Main outcome.** The CD177 phenotype reported in the continuation is not a sequencing-depth artefact: the priming and identity associations survive every depth adjustment available, in both eligible libraries. But it is largely a *compositional* effect — within individual subclusters the contrast mostly dissolves, with priming-associated RNA the one endpoint that persists. Separately, the paper's reversible-transition model is only partly reflected in RNA: the state graph is connected with populated intermediates, and depth-matched cycling differences between states are small and inconsistent (compatible with their equipotency claim), but the data cannot address direction or reversibility at all.

## On trajectory analysis: what was and was not possible

The paper reports **no computational trajectory**. Its STAR Methods describe Seurat v4.3.0, 5,000 highly variable genes, Louvain clustering, UMAP and a two-round integration with contaminant removal on Ptprc/Pecam1/Col1a1/Foxj1 — and nothing else. The reversible-transition claim rests on CD177/Itga2 double-positive immunofluorescence, organoids and orthotopic transplants from sorted states, EdU, and the absence of a clone-size-versus-composition correlation.

RNA velocity is **not computable on this deposit**: GEO supplies CellRanger filtered count matrices with no spliced/unspliced layers. The only route to splicing-based direction is re-quantifying the 68 ENA runs, which needs remote compute and separate authorization.

Accordingly this follow-up reproduces the paper's *pipeline* (two-round subclustering and UMAP) and then tests **predictions** of its transition model, rather than measuring transitions. The following were deliberately excluded, with reasons recorded in the contract: optimal-transport couplings (impose the time direction they would be asked to test), and CellRank or any directed Markov chain on a pseudotime or similarity kernel (their arrows follow from the kernel and root choice, not from the data). **No direction of state conversion is computed or claimed anywhere below, and no figure carries a transition arrow.**

## 1. Depth control of the CD177 associations (FU_A)

![Depth control](trials/followup/figures/FU_F02_depth_control.png)

Within transition-gated cells of the two eligible libraries, Cd177-detected versus Cd177-zero, under five prespecified treatments ([table](trials/followup/FU_A_depth_control.csv), [verdicts](trials/followup/FU_A_verdicts.csv)).

**The frozen decision rule returns "inconclusive" for every endpoint, for a mechanical reason.** It required agreement across all four adjustment methods in both libraries, but thinning to a common 3,000-UMI budget leaves GSM7890836 with 26 Cd177-positive cells, below the contract's 30-cell floor, so that method yields no value there. This is a floor artefact, not evidence of depth dependence. Reported below as a **disclosed post-hoc relaxation** to the three methods available in both libraries:

| Endpoint | GSM7890835 unadj / resid / decile | GSM7890836 unadj / resid / decile | Sign stable in both |
|---|---|---|---|
| Priming (Lcn2/Lrg1/Retnla/Ptgs1) | +1.60 / +1.51 / +1.38 | +2.17 / +1.99 / +1.96 | yes |
| AT2 identity | +0.94 / +0.87 / +0.67 | +1.41 / +1.27 / +1.38 | yes |
| AT1 identity | +0.85 / +0.74 / +0.86 | +0.52 / +0.48 / +0.54 | yes |
| Itga2 | −0.48 / −0.41 / −0.34 | −0.75 / −0.74 / −0.97 | yes |
| Transition RNA | −0.18 / −0.28 / −0.26 | −0.79 / −0.83 / −0.87 | yes |
| Shared remodelling module | −0.70 / −0.77 / −0.70 | −1.21 / −1.19 / −1.21 | yes |
| Lesion remodelling module | −0.88 / −0.81 / −0.57 | −1.10 / −1.05 / −1.13 | yes |
| TNF/NF-κB, Nfkbia, hypoxia control | ≈0 | −0.28 to −0.46 | no |

In GSM7890835 the 3,000-UMI thinning also ran (38 vs 834 cells) and reproduced every direction: priming +1.50, AT2 identity +0.96, AT1 identity +0.73, Itga2 −0.33, shared −0.66, lesion −0.73.

**Verdict:** the priming, identity, Itga2 and remodelling associations of Cd177 detection are not explained by sequencing depth. Residualizing on log depth and detected genes retains at least 87 % of each effect (range 87–159 %; several effects are slightly larger after adjustment). The depth confound flagged in the continuation is resolved against the artefact explanation.

**Cycling remains library-discordant** (−0.04 / −0.20 / −0.34 in GSM7890835 versus +0.48 / +0.36 / +0.30 in GSM7890836) and the near-zero reference value in GSM7890835 makes its formal "sign stability" uninformative. Depth control does not reconcile the two libraries.

## 2. Two-round subclustering and state topology (FU_E, FU_T1, FU_T2)

![Round-2 UMAP](trials/followup/figures/FU_F01_round2_umap.png)

The paper's pipeline shape was followed: round-1 clusters failing the contaminant rule were discarded (Exp 1: 4 clusters, 1,311 cells; Exp 2: 10 clusters, 2,099 cells; [waterfall](trials/followup/FU_E_round1_contaminant_waterfall.csv)), the remainder renormalized and re-clustered, giving 19 (Exp 1, 31,387 cells) and 15 (Exp 2, 9,399 cells) clusters at resolution 1.0 ([clusters](trials/followup/FU_E_round2_clusters.csv)). Cd177 and Itga2 mark adjacent, partly overlapping territories of the mutant compartment, with the cycling signal concentrated elsewhere.

![Topology and within-cluster contrast](trials/followup/figures/FU_F03_topology_and_within_cluster.png)

| Prediction | Result | Reading |
|---|---|---|
| **T1 topology** — reversible mixing predicts mutual adjacency; a cascade predicts a chain | Among mutant-dominated clusters, connectivity exceeds 0.1 in 12 of 21 pairs (Exp 1) and 30 of 91 (Exp 2); the largest spanning path carries 70 % and 69 % of total connectivity ([table](trials/followup/FU_T1_paga_connectivity.csv)) | Neither a clean chain nor a fully mixed pool. **Uninformative** between the two descriptions; PAGA is undirected and a connected graph is equally compatible with rapid mixing and with a static continuum |
| **T2 intermediates** — the RNA analogue of their double-positive staining | Cells in the middle 40 % of the axis joining two cluster centroids: median share 0.20 (Exp 1, 21 pairs) and 0.25 (Exp 2, 45 pairs), range 0.00–0.91 ([table](trials/followup/FU_T2_intermediate_density.csv)) | Intermediates are **populated**, consistent with their model. Removing doublet-flagged cells changes each value by ≤0.002, so they are not doublet artefacts. Ambient RNA remains an untested alternative |
| **T3 composition stationarity** | Total variation between timepoints 0.289 (Exp 1 day 4→14) and 0.336 (Exp 2 day 14→84) does **not** exceed the variation between replicate libraries at a single timepoint (0.35 and 0.48) ([table](trials/followup/FU_T3_composition_stationarity.csv)) | **Uninformative.** Library-to-library heterogeneity swamps the time signal, so drift and stationarity cannot be separated |

The diffusion ordering is reported as a cluster ordering only ([table](trials/followup/FU_E_diffusion_ordering.csv)); two small Experiment-2 clusters (24 and 74 cells) are disconnected from the root component and carry infinite values.

## 3. The CD177 phenotype is mostly compositional (FU_C)

Repeating the Cd177 contrast *within* each round-2 subcluster that meets the 30-cell floor on both sides gives seven testable clusters ([table](trials/followup/FU_C_within_subcluster_cd177.csv)). The gate-level pattern largely dissolves: AT2 identity ranges −0.36 to +1.27, Itga2 flips to **positive** in five of seven clusters (up to +1.01), and the shared and lesion modules change sign between clusters. The one endpoint that persists is **priming-associated RNA**, positive in five of seven clusters (+0.36, +0.36, +0.60, +1.31, +2.32) and near zero in the other two.

**Reading.** Most of the CD177 phenotype reported in the continuation reflects *which subcluster* Cd177-detected cells occupy, not a within-neighbourhood difference. This is a compositional phenotype. Priming-associated RNA is the component that survives conditioning on the local transcriptome and is the strongest candidate for a genuine CD177-linked program.

## 4. Controls on the continuation conclusions (FU_B, FU_T4, FU_D)

![Controls](trials/followup/figures/FU_F04_controls.png)

**AT1 gate definition (FU_B).** The AT1 identity module (Pdpn/Cav1/Aqp5/Spock2) separates Niethamer author-labelled AT1 from AT2 almost perfectly: threshold 1.01 mean log1p(CP10k), sensitivity 0.99, specificity 0.99 ([calibration](trials/followup/FU_B_at1_gate_calibration.csv)). Applying it to England collapses the mixed state from 7–36 % of cells per library under the Ager/Hopx/Clic5 detection gate to 0–8 % ([composition](trials/followup/FU_B_state_composition_both_definitions.csv)). This confirms the continuation's warning quantitatively: the large "mixed" population is an artefact of a permissive detection gate, and AT2/AT1 co-expression at the module level is rare.

**Cycling equipotency (FU_T4).** Across mutant libraries with at least three usable depth strata ([table](trials/followup/FU_T4_cycling_equipotency.csv)), the only state pair with broad coverage is AT2 versus mixed: 12 libraries, median depth-matched SMD −0.01, split 6 positive / 6 negative. AT2 versus transition (4 libraries, median +0.36) and transition versus mixed (4 libraries, median −0.29) are inconsistent in sign. **Consistent with** the paper's claim of comparable proliferative potential across states for the one well-covered comparison; underpowered for the others. RNA cycling markers are not a proliferation assay, and the paper measured potential with organoids, transplantation and EdU.

**Library quality (FU_D).** A five-predictor model (median log depth, median genes, mitochondrial percent, doublet fraction, immune-high fraction) explains R² = 0.57 of the between-library variance in the response-high fraction across 20 libraries, adjusted R² = 0.42 ([summary](trials/followup/FU_D_model_summary.csv)). Technical quality accounts for a large share of the 3–52 % spread reported in EN3. Condition is confounded with library, so this bounds rather than proves a technical origin.

## Revised verdicts on the transition model and ideas 4–6

| Claim | Status after follow-up |
|---|---|
| Cd177+ cells are a distinct primed state | **Supported and depth-controlled**, but largely compositional: priming-associated RNA is the component that survives within-subcluster conditioning |
| Cd177+ mixed state sustains division | **Still not supported.** Depth control does not reconcile the discordant cycling association between the two libraries |
| Mutant states have equivalent proliferative potential | **Consistent** for AT2 versus mixed across 12 libraries (median SMD −0.01); other pairs underpowered |
| Reversible / bidirectional transitions | **Not addressable with this deposit.** Intermediates are populated and not doublets, which is consistent with their model, but no direction, rate or reversibility can be estimated from snapshot matrices without splicing information |
| Mixed identity as AT2→AT1 infidelity | **Weakened.** Under a module-based AT1 definition calibrated on labelled data, the mixed state nearly disappears |

## FU_W — the source's growth versus differentiation decoupling, recovered from the deposit

England et al. report the decoupling explicitly: loss of pro-Sftpc was independent of proximity to
mutant clones up to a 300 um resolution, in contrast to wild-type expansion, suggesting that
alternate mechanisms control self-renewal versus differentiation (Figures 5G–5J and 6E–6F). This
block is a **reproduction of that comparison** on the deposited pooled pair arrays, not an
independent contrast. What it adds is that the claim is recoverable from what was deposited, both
readouts on a common relative scale, the homeostatic slope for each, and an audit of the
bin-occupancy limitation the source methods name. Bins require at least ten pair rows and a midpoint
within 400 um; slopes are pair-row-weighted, expressed as a percentage of the distal level per
100 um, and repeated on bins with at least 100 pair rows.

| context | dataset | pair rows | size near / far | size slope | dense-bin | pro-Sftpc− near / far | pro-Sftpc− slope | dense-bin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| oncogenic | kras4d | 520 | 2.55 / 2.10 | −16 | n/a | 0.28 / 0.33 | −2.5 | n/a |
| oncogenic | kras1w | 7,576 | 4.88 / 2.77 | −109 | −109 | 0.20 / 0.25 | −49 | −49 |
| oncogenic | kras2w | 6,986 | 4.76 / 2.31 | −78 | −69 | 0.14 / 0.22 | +12 | +12 |
| oncogenic | kras4w | 4,557 | 5.25 / 3.16 | −41 | −43 | 0.22 / 0.21 | +3.5 | +5.5 |
| homeostatic | nine Confetti | 201–1,058 | 2.15–6.71 / 2.06–5.36 | −22 to +0.2 | −56 to −1.4 | 0.03–0.09 / 0.00–0.14 | −13 to +40 | −48 to +55 |

![Growth and differentiation distance profiles](trials/followup/figures/FU_F05_growth_differentiation.png)

Three readings hold. The size gradient is robust: restricting to well-occupied bins leaves the
oncogenic values essentially unchanged, so it is not an artefact of the sparse distal bins. The two
early oncogenic timepoints fall faster than any homeostatic dataset, while kras4w sits inside the
homeostatic range because one late dataset, conf60w, is itself steep — the context separation is
clear at one and two weeks and not at four. And the differentiation proxy is raised two- to five-fold
over homeostatic tissue at every distance while its slope is inconsistent in sign in **both**
contexts, so the deposit is consistent with proximity independence without being strong evidence for
it; an absent slope in a noisy readout is not a demonstration of independence.

**What this does not establish.** Pooled rows carry no mouse or clone identifiers and one neighbour
clone may contribute to several rows, so there is no mouse-level effect, no significance and no
causal reading. Pair rows collapse with distance (kras1w: 4,953 at 25 um to 13 at 225 um), which the
source methods name as limiting statistical power. Clone merger near large lesions would inflate
short-distance neighbour size without any change in division rate and cannot be excluded from these
rows; the pro-Sftpc-negative fraction already sits near 0.2 to 0.3 close to the clone and has less
room to rise; and distance in Confetti tissue is clone-to-clone rather than clone-to-mutant, making
that reference analogous rather than matched. The exposure is disclosed in the contract: these slopes
were computed as scoping before the FU_W block was frozen, so this is an openly exploratory
extension. The mechanistic question it motivates is written up as A18 in
[RESEARCH_QUESTIONS.md](../../RESEARCH_QUESTIONS.md).

## Derived research questions

Three questions were proposed to the shared index on 28 September 2026, each pending the owner's retain or reject:
**A16** (does Cd177 mark a cell-intrinsic priming programme or the transcriptional neighbourhood a cell occupies) — blocked for its discriminating sorted-CD177 test, with GSE253461 and GSE316244 identified as partially eligible external routes for the attribution question alone; **A17** (does support for two founder classes survive a boundary-correct simulation) — ready to run as the deferred FU_S refit, no new data required; **A18** (are wild-type growth and wild-type identity loss under separate control near a mutant clone) — descriptively complete from FU_W above and inferentially blocked without mouse-level and clone-level rows. See [RESEARCH_QUESTIONS.md](../../RESEARCH_QUESTIONS.md), and [ANALYSIS_OPPORTUNITIES.md](ANALYSIS_OPPORTUNITIES.md) for the analyses the deposits can and cannot still support.

## What would change these conclusions

1. **Spliced/unspliced quantification from the 68 ENA runs** — the only route to directional evidence from this deposit; needs remote compute.
2. **Surface CD177 sorting within a Cldn4/Ndrg1/Sox9 transitional gate**, with EdU or Ki67 protein and short-term clone growth — tests the division claim directly, and the RNA result predicts enrichment for primed, identity-retaining cells rather than cycling ones.
3. **Biological pool and animal identities** for the 20 libraries — without them every estimate here stays a library-level description.
4. **A repair or injury cohort with a sizeable Cd177-positive transitional population** — none exists in Choi or Niethamer.

## Deferred

**FU_S, the corrected-implementation simulator refit,** is specified in the frozen contract but not executed here: the prespecified grid is 560 parameter points × 20 replicates × 2,000 clones × 2 implementations, which needs a dedicated run. The EN6 finding stands on its own — the deposited script's S-loss branch changes the q = 0.7 clone-size law — and the refit would establish what the corrected model's best-fit parameters are.

Run records, contract and output hashes are in `trials/followup/run_record.json`; regenerable embeddings are under the ignored `processed/followup/`.
