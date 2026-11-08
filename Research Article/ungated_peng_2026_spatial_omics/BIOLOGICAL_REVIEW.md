# Peng: biological review and job synthesis

8 November 2026. Coordinating review of technical delivery `65627dc` and
publication record `1ef5bef`, for [PR #173](https://github.com/xorca0711/ravel/pull/173).
This is an outcome-exposed interpretation and documentation review. Numerical
results, contracts and receipts are unchanged; this is not independent biological
validation, a new experiment package or a human acceptance decision.

## What the completed work contributes

The organizing question is how epithelial populations, pathological location and
inflammatory surroundings relate across the sampled lesion contexts. The public
analyses contribute an epithelial predictive lead's RNA distribution and a
tissue-organization description. They separate candidate explanations without
yet deciding among changing population abundance, arrangement or within-state
response. These can coexist; cell composition is not automatically a nuisance.

A12 retains its specific question about added recipient information beyond the
specified ligand/mixture comparison. A population-associated pattern could inform
the broader article question while failing to establish that A12 increment.
The source-recovery endpoint and the ultimate functional questions are supporting
and downstream branches respectively, not replacements for the biological aim.

**A12:** in the original 12 paired patients, candidate AT2 nuclei have more
frequent IL1RAP detection in LUAD, but lower normalized intensity among detected
nuclei. IL1R1 detection is heterogeneous and changes direction with the candidate
population. Joint detection increases by 1.01 percentage points, falling to 0.16
under the prespecified depth sensitivity. These distributional descriptions
neither algebraically explain the old predictive improvement nor identify
intrinsic receptor regulation in a validated state. Independent state identity
and a measured response remain missing. [Exact results and denominators](PUBLIC_DATA_RESULTS.md).

**Pg1-P01/C3:** spatial lag describes RNA arrangement beyond the previous
whole-section means. Among ten patient-matched LUAD/AAH pairs, the mean
depth-adjusted IL1B–CLDN4 one-hop contrast is +0.0279, with 7/10 positive; broad
RNA-composition covariates reduce it to +0.0095. The one-minus-two-hop contrast
has only 5/10 positive differences. This does not isolate an immediate-neighbor
biological process. Adjustment can remove relevant biology as well as mixture;
attenuation is not a causal fraction explained. Contrary examples P1 and P2
remain visible. [Exact spatial results](PUBLIC_DATA_RESULTS.md).

### Why this is not a reproduction of the early-lesion result

Peng reports enrichment of IL1B-high macrophages around specified epithelial
populations in early lesions, using cell-centroid neighborhoods of 80 micrometers
(Fig. 5D–F/J–K; STAR Methods, cellular neighborhood analysis). The new Visium
contrast is higher on average in LUAD than AAH. Its different direction must be
reported, but does not directly contradict that cellular result: the measurements
are not interchangeable. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12980502/).

| Dimension | Published neighborhood analysis | Completed public Visium branch |
|---|---|---|
| Feature | Counts/composition of annotated neighboring populations | Standardized IL1B–CLDN4 RNA cross-products |
| Recipient | Author epithelial states and lesion context | CLDN4 transcript, without a KAC or RPII assignment |
| Scale | Cell centroids within 80 micrometers | Adjacent mixed-cell lattice spots; no physical-radius equivalence |
| Comparison | Defined epithelial/lesion groups in discovery and TMA analyses | Patient-paired whole-section LUAD minus AAH; AIS/MIA secondary |
| Missing bridge | Qualified labels, geometry and sample identities | Cannot be inferred from the positive RNA statistic |

This is a measurement distinction to resolve, not a reason to select genes until
the published direction appears. A faithful reproduction must retain the author
endpoint and separately report patient contributions, nesting, density and edge
sensitivity. Molecular state, morphological region, clone and eventual fate
remain distinct observations.

## Job-by-job status and implication

Stages refer to the [original plan](PLAN.md). “Done” names the actual deliverable,
not completion of every possible analysis of this paper.

| Job | Current status | What it establishes or still needs |
|---|---|---|
| 0. Source ledger | **Done for inspected/received sources** | Versions, access routes and inventories recorded. Zenodo access is user-reported requested, pending and unverified. |
| 1. Sample joins | **Metadata done; specimen relationships partial** | 185 GEO records and S1 support declared patient/library joins. Exact block/section equivalence, P6 WES identity and P7 diagnostic history remain unresolved. |
| 2. Pathology/ROI and assay definitions | **Definitions/tables done; exports missing** | S1–S6 recover cohort structure, namespaced programs/signatures and add-on panels. Author barcode labels, polygons, full measured panels and core identities remain missing. S5 Gene A333 remains unresolved. |
| Public A12 cell branch | **Done without restricted exports** | 75 libraries qualified; original 12-patient comparison retained. Detection, conditional intensity, co-detection and selection/depth sensitivities described. Within-state signaling remains unestimated. |
| Public Pg1-P01/C3 spatial branch | **Done without restricted exports** | All 56 sections/25 patient labels described; ten patients enter the primary paired contrast. This shared-source lattice description is not the original 80-micrometer reproduction. |
| 3. Author spatial alignment | **Held by missing exports/joins** | Requires author coordinates, frames/transforms, labels, geometry and exact section mappings. Public lattice QC does not complete this job. |
| 4. Pathology/state composition and 80-micrometer reproduction | **Held; plausible after stage 3** | Requires qualified author endpoints. Published definitions and public maps cannot reconstruct them faithfully. |
| 5. Within-state A12 context | **Held; plausible conditionally** | Needs comparable state/pathology strata, measured endpoint coverage and a state-label/endpoint overlap audit. Access alone does not ensure identifiability. |
| 6. TMA transport | **Aggregate structure done; endpoint transport held** | S1 qualifies 19 patient labels, 188 aggregate cores, eight TMAs/four slides. Exact core nesting, full panel and compatible outcome remain needed. |
| 7. Persistence, withdrawal and mature output | **Not executed; beyond the access block** | Requires linked longitudinal/experimental outcomes. Cross-sectional exports cannot establish later AT1 output or recovery after withdrawal. |
| Figures, provenance and review | **Done for this delivery** | Measured plots/maps and 25-patient atlas support inspection. Frozen failures and unfavorable results remain; technical verification is not scientific acceptance. |

Evidence: [GEO audit](RESULTS.md), [supplement qualification](SUPPLEMENTS_RESULTS.md),
[public results](PUBLIC_DATA_RESULTS.md), [gallery](PUBLIC_DATA_FIGURES.md) and
[validation](PUBLIC_DATA_VALIDATION.md). Source restrictions block specific
original jobs, not all useful work. Both accessible numerical branches are now
completed rather than merely proposed.

## Connections with neighboring articles and questions

Published experiments and repository reanalyses are separate evidence below.
The contribution is an extension under existing owners, not a new global RQ.

| Neighbor | Published premise and local observation | Peng connection and distinction |
|---|---|---|
| [C3 human niche work](../gate2_C3_yu_lee_choi_min_2026/trials/u5_spatial_context/REPORT.md) | C3 already describes all 56 human spatial sections and the RNA companion. | New spatial lag and sensitivity extend section means; author exports could add pathology. GSE307534/GSE308103 remain the same evidence lineage. |
| [Choi 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/), Fig. 7E–H; [local package](../gate1_02_choi_2020/README.md) | IL-1 persistence/withdrawal and maturation have an experimental precedent. Local pooled-library state maps do not recreate replicated treatment effects. | Peng supplies lesion context for A1/A8/A14. Generic withdrawal is already studied; repair-versus-lesion persistence needs a specific comparison and linked output. KAC loss is not AT1 recovery. |
| [Cardoso 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13149335/), Fig. 3h–p/Extended Data 7o–v; [local correction](../../analysis/corrections/ligand/RESULTS.md) | EGFR inhibition in fibroblast co-culture alters mutant epithelial state; fibroblast-free and mutant-pathway comparisons constrain interpretation. Locally, AREG source ranking changes with annotation/depth. | Reciprocal stromal effects are an alternative to a one-way macrophage narrative. Peng iCAF abundance and A13's unfavorable TGF-proxy prediction are different endpoints; neither verifies nor negates that circuit. |
| [Han 2024](https://www.nature.com/articles/s41586-024-07113-9), Fig. 4; [prior source review](../../docs/research_reviews/2026-11-08-peng-spatial-reading/README.md) | KAC identity/lineage has a prior source; Peng reuses GSE222901 and the KAC signature. | Preserve shared provenance. Agreement is not automatically independent replication or proof of each human cell's fate. |
| [Hill 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC7614604/), Fig. 3e–g/Extended Data 5 | Macrophage IL-1 and promotion of mutant epithelium have a functional precedent. | Peng adds lesion/pathology localization. The public IL1B–CLDN4 statistic does not reproduce an exposure-driven tumor-promotion experiment. |
| [Jaiswal 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12985369/), Fig. 4F–J/S8K | Human AT2 organoids show a stronger aberrant phenotype under combined TGF-beta/IL-1beta/TNF-alpha than individual ligands in that assay. | Multiple inputs are relevant alternatives for A12/A13. Fibrotic aberrant trAT and cancer-associated KAC are not established equivalents; the combination does not prove statistical synergy or its operation in Peng's patients. |

For [A11](../../RQ_Specified/A11_lesion_programme_addition/README.md), pathology
could clarify where the frozen lesion feature is expressed; it does not fix the
unfavorable capacity-control diagnostic. The three MP families are not
interchangeable, and no Peng MP6 replaces that feature. For
[A12](../../RQ_Specified/A12_recipient_context/README.md), high IL1R1 in an author
state and LUAD-minus-normal in transferred AT2 candidates are different contrasts.
For [A13](../../RQ_Specified/A13_fibroblast_beyond_macrophage_il1b/README.md),
preserve the worsened held-out MSE and absence of a nominated source product.
New measurement context does not rescue prior unfavorable tests.

## Possible extensions and their decision value

These are conditional follow-ups under existing owners, not new numerical
contracts or bench-ready protocols. All current outcomes have been seen.

The nearest decision is which biological populations and regions carry the
observed pattern. With qualified labels and geometry, differences in abundance
could identify a changing population context; differences in arrangement among
comparable populations could motivate a spatial-organization explanation; a
within-state RNA association could motivate recipient-context work. These are
possible interpretations, not effects established by residualizing broad RNA
covariates. Independent prediction and functional response address different
claims and need not be presented as a compulsory assay sequence.

| Extension | Feasibility and prerequisite | Comparison and informative outcomes |
|---|---|---|
| State abundance and tissue organization | **Await qualified author labels/geometry for the planned pathology-resolved version.** Pg1-P01/C3 retain the source description; new numerical choices require a contract. | Identify populations/regions carrying the pattern, retaining abundance as an endpoint and distinguishing arrangement where the design supports it. A population-associated result informs tissue biology but does not establish A12's beyond-mixture increment or a causal niche effect. |
| Author endpoint, then within-state context | **Await exports.** Pg1-P01 stages 3–4 precede A12 stage 5. Qualify geometry, pathology, states and overlap with outcome genes before freezing the endpoint. | Patient summaries within comparable strata could distinguish an association retained within state from one dependent on mixture/density. Either is informative; unresolved labels leave it unestimated. Reverse recruitment and other inputs remain. |
| TMA transport | **Await core/full-panel qualification.** Use a compatible endpoint, verified patient/core nesting and source independence. | A fixed comparison in separate patients assesses transport. Coverage failure is non-estimability; discordance is a boundary result. Discovery reuse does not become independent evidence. |
| Recipient response and niche dependence | **New measurements needed.** A12/A13 need independent epithelial state, justified source/ligand perturbation and separately measured response; model, timing, replication and precision remain unspecified. | A response difference linked to verified receptor configuration at matched state could support recipient dependence. Dependence on mixture or additional inputs narrows that account. Cardoso/Jaiswal motivate alternatives, not an automatic large factorial experiment. |
| Persistence and mature output | **Longitudinal/experimental inputs needed.** A1/A8/A14 retain ownership; Choi is an established precedent. | Compare continued input with verified withdrawal in the chosen repair/lesion context, linking starting cells to later output and measuring survival/growth separately. Persistence, cell loss and mature AT1 production answer different questions. |

Accessible work now is the completed source qualification, both public
descriptions and comparative synthesis. Further public calculation needs a named
unresolved question and suitable inputs; another score sweep or spot-level
p-value would not close the biological gap. Future numerical work needs a new
frozen contract and retained exposure history. No automatic rerun, additional
global RQ or expanded experiment is proposed.

## Review coverage and reading order

Read this synthesis, then the [gallery](PUBLIC_DATA_FIGURES.md),
[results](PUBLIC_DATA_RESULTS.md) and [validation](PUBLIC_DATA_VALIDATION.md).
[Connections](RQ_CONNECTIONS.md) and [plan](PLAN.md) retain original ownership and
dependencies; frozen contracts and receipts own calculation details.

This review reuses the same-day [paper/source review](../../docs/research_reviews/2026-11-08-peng-spatial-reading/README.md)
and [public-branch literature search](PUBLIC_DATA_CONTEXT.md), including their
queries, versions and access limits. No new broad search or novelty claim is made.
On 8 November 2026, direct web retrieval rechecked Peng's PMC author-manuscript
Results/Fig. 4–5 legends and neighborhood methods; Jaiswal's PMC Results and
Fig. 4/S8 references; and Cardoso's PMC Results around Fig. 3/Extended Data 7–8.
The Cardoso publisher route failed; PMC supplied the passages. This extends the
earlier indexed Cardoso read only for these passages, not to a full methods or
supplement audit. Choi/Hill/Han remain reused prior reads. No exhaustive
forward-citation or correction/retraction search was repeated.

Current C3, A11, A13 and Cardoso correction/retrospective summaries were checked
alongside Peng specifications/results. The two principal measured PNG plots were
visually inspected; technical gallery/atlas validation is reused. No scientific
script was rerun, frozen artifact edited, canonical hypothesis or claim grade changed.
