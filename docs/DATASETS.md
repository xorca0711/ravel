# Dataset inventory and eligibility

Synchronized from tracked execution records on **28 September 2026**, after the
gap-fill work merged in PR #107. This is a map of repository use, not a new
survey of public availability. Linked run records retain exact URLs, versions,
hashes and inclusion rules. Local raw caches are generally ignored by Git.

An accession can support one question and fail another. A downloaded matrix,
an author label and an independently eligible biological unit are distinct
requirements. Reuse of a cohort or its spatial companion is not replication.
Study-reading status is recorded separately in the [paper roadmap](../Research%20Article/README.md).

## Expression and multiome datasets with executed analyses

This table retains the former main-README inventory, updates its current uses,
and separates full-series record counts from the selected analytical units.

| Accession | Species and design | Source study | Executed use and evidence | Unit and current limit |
|---|---|---|---|---|
| [GSE262927](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262927) | mouse, respiratory-virus (H1N1) injury time course, uninjured to 366 dpi, 33 samples, 162,175 cells | Niethamer et al., *Cell Stem Cell* 2025 | [`Research Article/gate1_01_niethamer_2025/GSE262927/`](../Research%20Article/gate1_01_niethamer_2025/GSE262927/README.md), [Stage 1 follow-ups](../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md), [HLCA trials S4, S5](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md) | animal; 2 per active-repair day, 8 at 42 dpi |
| [GSE178360](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178360) | human, healthy distal lung, 3 donors, 27,729 cells | Kadur Lakshminarasimha Murthy et al., *Nature* 2022 | [`Research Article/ungated_murthy_2022/GSE178360/`](../Research%20Article/ungated_murthy_2022/GSE178360/README.md), [HLCA trials S1 to S3](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md) | donor; 3 |
| [GSE145031](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145031) | mouse, AT2 lineage-traced epithelium, PBS and bleomycin day 14 and 28, 6 libraries | Choi et al., *Cell Stem Cell* 2020 | [trials D0 to D7](../Research%20Article/gate1_02_choi_2020/ANALYSIS_TRIAL_PLAN.md) | one library per condition; six matrices are raw barcode whitelists |
| [GSE144468](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144468) | mouse, AT2 organoids with and without IL-1beta, 2 libraries | Choi et al., *Cell Stem Cell* 2020 | [trials D5, D5b](../Research%20Article/gate1_02_choi_2020/ANALYSIS_TRIAL_PLAN.md) | one library per arm |
| [GSE316241](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316241), [GSE316243](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316243), [GSE316244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE316244) | mouse, Confetti against Red2Kras mesenchyme and niche, and the Areg-flox arm; 8 libraries, 3 mice pooled each | Cardoso, Lee et al., *Nature* 2026 | [trials C0 to C2b, C5 to C11, C13](../Research%20Article/gate2_05_cardoso_2026/trials/README.md) | one pooled library per genotype/sort; descriptive comparisons do not supply independently replicated genotype inference |
| [GSE310335](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310335) | human, KRAS G12D alveolar organoids, 2 libraries | Cardoso, Lee et al., *Nature* 2026 | [trial C0](../Research%20Article/gate2_05_cardoso_2026/trials/README.md) | one library per arm |
| [GSE247505](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247505), with GSE247503/GSE247504 records | mouse epithelial scRNA; 20 pooled-lung libraries across genotype/time contexts | England et al., Cell Stem Cell 2025 | [England analyses](../Research%20Article/gate2_C2_england_2025/README.md); [corrected A16 C1](../RQ_Specified/A16_cd177_state_attribution/correction_20260928/reports/CORRECTED_C1_REPORT.md); earlier Cardoso/Choi reuse including GSE247504 | library; animal/pool identities remain unresolved. Clone arrays are a separate source below; the [series-linkage caveat](../Research%20Article/gate2_C2_england_2025/ANALYSIS_OPPORTUNITIES.md#blocked-with-the-specific-missing-item) remains |
| [GSE131907](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE131907) | human LUAD and normal lung; 10 verified primary-lung patient pairs | Kim et al., Nature Communications 2020 | [Ligand correction](../analysis/corrections/ligand/README.md); [A11](../RQ_Specified/A11_lesion_programme_addition/README.md); [A12 gate](../RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md) | patient; 8 eligible A11 pairs. All 10 A12 tumour arms have zero author-labelled AT2 cells, so none passes that unchanged comparison |
| [GSE136831](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136831) | human, idiopathic pulmonary fibrosis and control, 312,928 cells | Adams et al., *Science Advances* 2020 | [trials E2, E6, C12, C14](../Research%20Article/gate2_05_cardoso_2026/trials/README.md) | donor; 26 in the resource scans, 22 in the coupling test, 7 and 3 in the rare-state comparisons |
| [GSE135893](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893) | human, pulmonary fibrosis and control, 114,396 cells | Habermann et al., *Science Advances* 2020 | [trial E3](../Research%20Article/gate2_05_cardoso_2026/trials/README.md) | donor |
| [GSE132771](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132771) | mouse, bleomycin against uninjured, collagen-producing cells | Tsukui et al., *Nature Communications* 2020 | [trial E4](../Research%20Article/gate2_05_cardoso_2026/trials/README.md) | animal |
| [GSE310539](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310539) | mouse, 10x multiome, sorted epithelium 14 days after Sendai virus or PBS, wildtype and AP-1 mutant, 4 wells, 39,849 nuclei | Lynch et al., *Am J Respir Cell Mol Biol* 2026 | [trials M0 to M4](../Research%20Article/gate1_02_choi_2020/datp_epigenetics/trials/README.md), [A1 to A1c](../Research%20Article/gate1_02_choi_2020/axin2_il1r1/trials/README.md) | one well per condition, two mice pooled |
| [GSE247130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247130) | mouse, 10x multiome, AT2 lineage, Cebpa mutant against control at P9, 7 weeks and after Sendai virus, 6 wells, 64,294 nuclei | Hassan and Chen, *Nature Communications* 2024 | [trials M0 to M4](../Research%20Article/gate1_02_choi_2020/datp_epigenetics/trials/README.md), [A1 to A1c](../Research%20Article/gate1_02_choi_2020/axin2_il1r1/trials/README.md) | one well per condition; **deposited suffix order inverted** |
| [GSE308103](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308103) | human precursor lesions/LUAD with normal tissue; 75 libraries, 23 patients | Peng et al., Cancer Cell 2026 | [Human niche analyses](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md); A11 discovery; [A12](roadmap_runs/2026-09-27-followthrough/A12_PILOT.md) and [A13 pilots](roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md) | patient; repeated histologies/tissue pieces are dependent. A12/A13 use 12 eligible paired units under their amended definitions |
| [GSE141259](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259) | mouse bleomycin time course; selected 32 epithelial samples within a 60-record series containing multiple experiments | Strunz et al., Nature Communications 2020 | [A5](../RQ_Specified/A5_developmental_programme_reuse/README.md); [A0](../RQ_Specified/A0_conserved_epithelial_transition_program/README.md); [specificity](../Research%20Article/epithelial_state_specificity/README.md) | mouse for the verified selected subset; 24 in A5 primary and 9 in A0. Do not interpret all series records as independent mice |
| [GSE92332](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92332) | mouse, small intestinal epithelium atlas | Haber et al., *Nature* 2017 | [A0 transfer arm](../RQ_Specified/A0_conserved_epithelial_transition_program/README.md) | mouse; 3 |
| [GSE307112](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307112) | mixed-species alveolosphere knockout screen; 886 well libraries and day-7/day-14 imaging | Roadmap paper 14; deposited data used, owner reading/study note not recorded as completed | [A10 growth results](../RQ_Specified/A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md); [A2 synthesis](../RQ_Specified/A2_areg_source_delivery/reports/STAGE5_SYNTHESIS.md); [P1 design recovery](roadmap_runs/2026-09-27/P1_SCREEN_DESIGN.md) | well, not independent preparation; repeats share a starting mixture. Preparation/guide/position and image-calibration limits remain |

## Additional executed inputs

These include normalized expression, chromatin tracks, source measurements and
derived author assets. They should not all be called independent scRNA cohorts.

| Input | Material and repository use | Unit or limit | Evidence |
|---|---|---|---|
| [GSE109444](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE109444) | Nabhan 2018 source mesenchymal FPKM; Wnt expression-panel reproduction | Deposited normalized expression, not UMI counts; exact published percentage remains unresolved | [Source reproduction](../Research%20Article/gate1_03_nabhan_2018/source_reproduction/README.md) |
| [GSE190821](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190821) | Auyeung 2022 bulk/enriched epithelial counts; distinct A1 intervention and A15 antibody contrasts | Biological mice; enriched epithelium is not a pure fixed cell state. A15 retains 4 versus 4 mice in its selected comparison | [A1 map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md); [A15 corrected normalization](../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/NORMALIZATION_ERRATUM_2026-09-28.md) |
| [GSE198864](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198864) | Mixed lung/explant/organoid collection; restricted A11 acute-injury RNA comparison | Current identity-concordant primary comparison has 3 paired donors; does not establish tumour specificity | [A11 current results](../RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md) |
| [GSE215898](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215898), scRNA child [GSE215895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215895); UCSC lung-dev | Sountoulidis 2023 developmental airway data used in A0 | Donor-labelled developmental arm; different species and lineage axis from adult mouse alveolar repair | [Source recovery](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/SOURCE_RECOVERY.md) |
| [GSE289683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289683) / [GSE291333](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291333); PRJDB37980/37983 | Tsutsui regulatory data: deposited CUT&Tag tracks, library metadata and source endpoints used by A1 | One iPSC line; CPM and figure-specific spike-in scaling cannot be interchanged; source preparation/endpoint definitions remain distinct | [A1 reference and outcome map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE150527](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150527) | Normal AT2-to-AT1 culture methylation context in A1 | One-donor domain comparison; mixed differentiating culture is not purified DATP | [A1 evidence map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE273123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273123) | CD44-associated bulk RNA; A1 paired WT/mutant and interaction analysis | 16 columns from 8 mice; same-cohort extension, not independent replication | [A1 reference map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE277777](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277777) and pinned HPCS author notebooks/source tables | HPCS composition, tracing and specificity inputs used in A1 and cross-study analyses | Technical GEX/hash records are not mice; source-table recovery resolves 22 retained aliases while library/chase confounding remains | [A1 regulatory/fate report](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md) |
| [GSE300288](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300288) | Early mouse niche analyses in the IL-1 review branch | Eligible sample/compartment contrasts only; primary KAC/coverage and later-history questions remain gated | [Executed package register](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/WORK_PACKAGES.md) |
| [GSE307534](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307534) | 56 human spatial sections, companion to the human lesion study | Sections nest within patients; not independent replication of GSE308103; independent pathology-region labels remain a gate | [Spatial/context evidence](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md) |
| [GSE267226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE267226) / [GSE267228](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE267228) | Nine human/mouse post-viral spatial matrices processed for context | 3 human disease/2 controls; mouse arms 2/2. The deposited mouse perturbation is anti-CD8, not an IL-1 intervention | [Source-design inventory](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md); [completed packages](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/WORK_PACKAGES.md) |
| [Zenodo 14673088, v1.1](https://doi.org/10.5281/zenodo.14673088) | England MATLAB source, nested clone measurements and pooled spatial arrays | Nonspatial data retain 44 source-indexed mice; A17 primary uses 11. Spatial pair rows lack mouse/clone identifiers | [Raw-source reconciliation](roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md); [England overview](../Research%20Article/gate2_C2_england_2025/README.md) |
| Published source workbooks and frozen gene lists | A1 PATS/HPCS/AP-1/iATC outcome reconstructions; Guo developmental lists used in A5 | Microscopy/culture units and published lists are distinct from sequencing cohorts; list reuse does not add independent observations | [A1 source map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md); [A5 instrument](../RQ_Specified/A5_developmental_programme_reuse/PLAN.md) |

## Recovered or assessed inputs that do not pass the proposed comparison

The status applies to the named question and inspected evidence. Some matrices
were acquired for feasibility; others were stopped after metadata. A failed
gate does not mean a dataset has no scientific value or does not exist.

| Candidate | Material inspected and current decision | Exact remaining gate / evidence |
|---|---|---|
| [GSE303646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303646) | A5 author code, GEO and library metadata; no new expression score | 56 matched libraries and relevant author labels recovered, but barcode-to-state/mouse map and 55-mice/56-libraries reconciliation remain missing. [Recovery](../RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/REPORT.md) |
| [GSE123902](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123902) | A12 metadata-only gate fails; no matrix opened | Three title-matched normal/tumour pairs, at most four possible pairs; below unchanged ten-pair floor. [Recovery](../RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md) |
| [GSE148071](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE148071) | A12 metadata/source gate fails; no matrix opened | 42 tumour biopsies, no separate matched normal arm. [Recovery](../RQ_Specified/A12_recipient_context/external_validation_20260928/reports/RECOVERY_REPORT.md) |
| [GSE129605](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129605) | Eight samples acquired for Wnt feasibility; A5 candidate also inspected | No admitted expression test without supported animal provenance, state labels and compartment coverage. [Nb1 gate](../Research%20Article/gate1_03_nabhan_2018/external_feasibility/README.md); [A5 audit](roadmap_runs/2026-09-27-followthrough/EXPANDED_CANDIDATE_AUDIT.md) |
| [GSE243124](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243124) | A1 sample/replication assessment | One pooled GEM library per condition; contributing mice cannot be recovered as independent treatment replicates. [Evidence map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE202325](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE202325) and other A5 leads | Earlier source/assay audits; not newly scored in the 28 September recovery | Broad AT2 labels do not supply the unchanged transitional/activated comparator. Other assay/unit failures remain in the [candidate audit](roadmap_runs/2026-09-27-followthrough/EXPANDED_CANDIDATE_AUDIT.md); the later recovery's bounded scope is explicit |
| [GSE233844](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE233844) / [GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960) | A13 candidate checks completed | First is blood; the inspected author annotations in the second fail the ten-unit gate. [Coverage report](roadmap_runs/2026-09-27-followthrough/A13_PILOT_AND_COVERAGE.md) |
| [GSE144598](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144598) / [GSE309751](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE309751) | ATAC source/metadata context, not a new regulatory-to-fate fit | Choi coverage tracks cannot support the proposed cell-level route; AP-1 bulk metadata include a treatment/title discrepancy. [Chromatin branch](../Research%20Article/gate1_02_choi_2020/datp_epigenetics/README.md); [A1 source map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE150957](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150957) | Proposed bulk-array route withdrawn by the owner; deposit not opened | Bulk sorted fractions cannot answer within-cell Axin2/Il1r1 co-occurrence. Preserved as a rejected design, not analysed data. [Route C rationale](../Research%20Article/gate1_02_choi_2020/axin2_il1r1/README.md) |

Further searched candidates and rejected accessions stay in the question-specific
source ledgers; this page is not an exhaustive list of every search hit. The
[IL-1 branch shortlist](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md)
also distinguishes its mouse/spatial companions and WES crosswalk from analysed
expression cohorts. In particular, GSE222901/GSE300293/GSE307529 metadata should
not be promoted to completed expression analyses.

## Reference resources and reproducibility

HLCA mapping references, curated ligand/receptor resources, NicheNet priors and
published gene sets are reference assets, not additional biological cohorts.
Use their analysis-specific version/coverage records. [References](../REFERENCES.md)
and the linked source reports identify publications; [reproducibility](../REPRODUCIBILITY.md)
describes local input layout. The [current per-question ledger](roadmap_runs/2026-09-28-gap-fill/RESULTS.md)
governs what missing input would permit a new analysis.

## Nabhan 2023 source intake, 29 September 2026

[GSE208770](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208770) has 18 mouse
AT2-organoid **bulk RNA-seq** libraries across six treatments, three labeled
replicates each. All counts were acquired and analyzed in the conditional
[Nb2 bulk adaptation](../Research%20Article/gate2_N1_nabhan_2023/trials/bulk_v1/REPORT.md).
The [study inventory](../Research%20Article/gate2_N1_nabhan_2023/DATASETS.md) distinguishes
this treatment experiment from the original single-cell receptor-map atlases.
The paper calls the replicates biological, but animal/preparation identity, pairing
and discrepant treatment timing still require reconciliation. This is not a
single-cell agonist-response dataset or an independently measured fate endpoint.
## Nb2 branch-analysis input, 29 September 2026

[GSE327565](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327565) now supplies
an executed mouse organoid Stk3/4-loss/YAP-TAZ comparator:14 bulk libraries,
separate3v3 SFFFM and4v4 ADM genotype contrasts. Source Figure8 reports mice;
cross-medium identities remain unresolved. This is distinct from GSE327686
multiome and GSE326359 human data. The existing A1 catalog was reused and the
processed count table downloaded publicly; no pooled multiome well was counted
as an independent bulk mouse. [Methods and source hashes](../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/METHODS.md).
The same workspace reuses GSE208770 and GSE262927; these are additional analyses,
not independent validation cohorts.
