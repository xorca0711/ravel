# Public source register

**Consolidated 8 November 2026 against main `1d7c814` (including merged Saxton PR #169).** This is the single
repository-wide list of public sources used, screened, rejected for a particular
comparison, held pending qualification, or cited as leads. Update this page when
source use or disposition changes. Article/RQ reports remain the evidence for
each decision; their inventories describe their local inputs rather than a second
repository-wide list. The former November supplement is archived after its
contents were incorporated here.

## Read the statuses

| Status | Meaning |
|---|---|
| Used | A numerical analysis, source reconstruction or reference-product calculation is recorded; the row states which |
| Inspected / qualified | Metadata, files, headers or annotations were examined; this alone is not a completed biological contrast |
| Rejected for comparison | A stated design, assay, unit or coverage rule failed; the source may still support another question |
| Pending / blocked | A specific source or comparison remains unqualified, inaccessible or gated; no execution is implied |
| Search hit / reference / alias | A query returned the identifier, a paper cited it, or a deposit linked it; this is not proof of dataset inspection or use |

One source can appear in several question-specific rows. Shared samples, parent
series, reanalyses and alternative downloads do not become independent cohorts.
Rows group sources where the same comparison/decision applies. Search-hit and
identifier totals must not be reported as numbers of utilized datasets.

- [Used expression and multiome sources](#used-expression-and-multiome-sources)
- [Other used measurements and author products](#other-used-measurements-and-author-products)
- [Used source families and detailed boundaries](#used-source-families-and-detailed-boundaries)
- [Inspected sources and comparison failures](#inspected-sources-and-comparison-failures)
- [Pending sources and unresolved access](#pending-sources-and-unresolved-access)
- [Recorded screens and search candidates](#recorded-screens-and-search-candidates)
- [Reference resources and deposit aliases](#reference-resources-and-deposit-aliases)
- [Local storage and historical inventories](#local-storage-and-historical-inventories)

No biological analysis or new remote availability search was performed for this
consolidation. A reported access failure retains the date/scope of its evidence;
it does not establish present-day or global unavailability. Sample-level GSMs,
individual files and versions remain in linked run/source records.

## Used expression and multiome sources

| Accession | Species and design | Source study | Executed use and evidence | Unit and current limit |
|---|---|---|---|---|
| [CELLxGENE: Travaglini lung atlas](https://cellxgene.cziscience.com/collections/5d445965-6f1a-4b68-ba3a-b8f765155d3a) | human normal lung/blood, 10x and SS2; 3 donors | Travaglini, Nabhan et al., Nature 2020; original source Synapse syn21041850 | [Nb4 dataset register](../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/DATASETS.md) | donor within assay/anatomy; curated versions, hashes and coverage recorded locally |
| [CELLxGENE: Madissoon lung atlas](https://cellxgene.cziscience.com/collections/c1241244-b22d-483d-875b-75699efb9f3c) | human normal lung, fibroblast cells/nuclei subset; 10 donor labels | Madissoon et al., Nature Genetics 2023 | [Nb4 external-source register](../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/DATASETS.md) | donor within matched anatomy/assay/protocol; four eligible cell donors and two nuclear donors for the defined comparison |
| [GSE262927](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262927) | mouse, respiratory-virus (H1N1) injury time course, uninjured to 366 dpi, 33 samples, 162,175 cells | Niethamer et al., *Cell Stem Cell* 2025 | [`Research Article/gate1_01_niethamer_2025/GSE262927/`](../Research%20Article/gate1_01_niethamer_2025/GSE262927/README.md), [Stage 1 follow-ups](../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md), [HLCA trials S4, S5](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md) | animal; 2 per active-repair day, 8 at 42 dpi |
| [GSE178360](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178360) | human, healthy distal lung, 3 donors, 27,729 cells | Kadur Lakshminarasimha Murthy et al., *Nature* 2022 | [`Research Article/ungated_murthy_2022/GSE178360/`](../Research%20Article/ungated_murthy_2022/GSE178360/README.md), [Nb4 MYRF reference check](../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/RQ_SEQUENCE_RESULTS.md), [HLCA trials S1 to S3](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md) | donor; 3 |
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

**Peng source follow-through, 8 November 2026:** [Ungated paper qualification](../Research%20Article/ungated_peng_2026_spatial_omics/SOURCE_RECOVERY.md) recovers GEO metadata and author pathology/ROI methods. GSE307529 is WES; Xenium annotations are not recovered from that accession. Exact pathology exports and section-level joins remain pending.

Nb4 also reuses the existing MSigDB 2024.1.Hs Hallmark and GO BP annotation resources; [versions and hashes](../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/runs/extended_visual_v1/gene_set_sources.json). These are gene-set annotations, not independent biological cohorts.

## Other used measurements and author products

These include normalized expression, chromatin tracks, source measurements and
derived author assets. They should not all be called independent scRNA cohorts.

| Input | Material and repository use | Unit or limit | Evidence |
|---|---|---|---|
| [GSE109444](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE109444) | Nabhan 2018 source mesenchymal FPKM; Wnt expression-panel reproduction | Deposited normalized expression, not UMI counts; exact published percentage remains unresolved | [Source reproduction](../Research%20Article/gate1_03_nabhan_2018/source_reproduction/README.md) |
| [GSE190821](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190821) | Auyeung 2022 bulk/enriched epithelial counts; distinct A1 intervention and A15 antibody contrasts | Biological mice; enriched epithelium is not a pure fixed cell state. A15 retains 4 versus 4 mice in its selected comparison | [A1 map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md); [A15 corrected normalization](../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/NORMALIZATION_ERRATUM_2026-09-28.md) |
| [GSE198864](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198864) | Mixed lung/explant/organoid collection; restricted A11 acute-injury RNA comparison | Current identity-concordant primary comparison has 3 paired donors; does not establish tumour specificity | [A11 current results](../RQ_Specified/A11_lesion_programme_addition/reports/ACUTE_INJURY_RESULTS.md) |
| [GSE215898](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215898), scRNA child [GSE215895](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215895); UCSC lung-dev | Sountoulidis 2023 developmental airway data used in A0 | Donor-labelled developmental arm; different species and lineage axis from adult mouse alveolar repair | [Source recovery](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/SOURCE_RECOVERY.md) |
| [GSE289683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289683) / [GSE291333](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291333); PRJDB37980 / PRJDB37983 | Tsutsui regulatory data: deposited CUT&Tag tracks, library metadata and source endpoints used by A1 | One iPSC line; CPM and figure-specific spike-in scaling cannot be interchanged; source preparation/endpoint definitions remain distinct | [A1 reference and outcome map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE150527](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150527) | Normal AT2-to-AT1 culture methylation context in A1 | One-donor domain comparison; mixed differentiating culture is not purified DATP | [A1 evidence map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE273123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273123) | CD44-associated bulk RNA; A1 paired WT/mutant and interaction analysis | 16 columns from 8 mice; same-cohort extension, not independent replication | [A1 reference map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| [GSE277777](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277777) and pinned HPCS author notebooks/source tables | HPCS composition, tracing and specificity inputs used in A1 and cross-study analyses | Technical GEX/hash records are not mice; source-table recovery resolves 22 retained aliases while library/chase confounding remains | [A1 regulatory/fate report](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/REGULATORY_FATE_REPORT.md) |
| [GSE300288](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300288) | Early mouse niche analyses in the IL-1 review branch | Eligible sample/compartment contrasts only; primary KAC/coverage and later-history questions remain gated | [Executed package register](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/WORK_PACKAGES.md) |
| [GSE307534](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307534) | 56 human spatial sections, companion to the human lesion study | Sections nest within patients; not independent replication of GSE308103; independent pathology-region labels remain a gate | [Spatial/context evidence](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/EVIDENCE_REVIEW.md) |
| [GSE267226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE267226) / [GSE267228](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE267228) | Nine human/mouse post-viral spatial matrices processed for context | 3 human disease/2 controls; mouse arms 2/2. The deposited mouse perturbation is anti-CD8, not an IL-1 intervention | [Source-design inventory](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md); [completed packages](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/WORK_PACKAGES.md) |
| [Zenodo 14673088, v1.1](https://doi.org/10.5281/zenodo.14673088) | England MATLAB source, nested clone measurements and pooled spatial arrays | Nonspatial data retain 44 source-indexed mice; A17 primary uses 11. Spatial pair rows lack mouse/clone identifiers | [Raw-source reconciliation](roadmap_runs/2026-09-28-gap-fill/a17_source_accounting/REPORT.md); [England overview](../Research%20Article/gate2_C2_england_2025/README.md) |
| Published source workbooks and frozen gene lists | A1 PATS/HPCS/AP-1/iATC outcome reconstructions; Guo developmental lists used in A5 | Microscopy/culture units and published lists are distinct from sequencing cohorts; list reuse does not add independent observations | [A1 source map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md); [A5 instrument](../RQ_Specified/A5_developmental_programme_reuse/PLAN.md) |

### Saxton source uses merged on 8 November

| Source / product | Recorded use | Unit, qualification and evidence |
|---|---|---|
| GSE160332 / PRJNA672965 | Sx10 activated human CD8 RNA qualification and finite-library descriptions | Eight libraries with explicit arm joins and aligned counts/FPKM; donor/preparation identities remain unknown. [Source qualification](../Research%20Article/ungated_saxton_2021_il10/SOURCE_QUALIFICATION.md), [current results](../Research%20Article/ungated_saxton_2021_il10/RESULTS.md). The modeling preprint reuses this source; it is not independent validation. |
| GSE160217, reused colon libraries | Sx22 acute Osmr RNA extension | Six existing PBS/WT/B3 colon libraries; no IFN-priming arm or independent replication. [Extension result](../Research%20Article/gate3_08_saxton_2021_il22/osmr_v1/RESULTS.md). |
| GSE146438 / Gorby deposited comparison workbooks | Sx10 description of 36 fixed target records across twelve author comparison tables | Reported estimates only; common-expression-matrix qualification failed and remains held. Source codes D85/D93/D36 lack an independently recovered donor crosswalk. No population inference or certification of upstream normalization. [Current result and amendment](../Research%20Article/ungated_saxton_2021_il10/extensions_20261108/RESULTS.md). |

### Additional source families

| Public source / deposit | Repository use | Evidence and important limit |
|---|---|---|
| [GSE160876](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160876), [GSE165063](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165063), author developmental viewer | A0 developmental transfer description | [Exposed pilot](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/EXPLORATORY_PILOT_REPORT.md); viewer/barcode groups do not supply independent animal replication |
| [GSE154966](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154966) | A1 HPCS bulk-ATAC count audit and sample PCA | [First batch](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/FIRST_BATCH_REPORT.md); eight libraries/four source aliases, animal/pool independence unresolved |
| [GSE199329](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE199329) | A23 human pulmonary alveolar microlithiasis external pilot | [Current pilot](../RQ_Specified/A23_slc34a2_transition_homeostasis/reports/external_pilot_v2/RESULTS.md); one disease subject and one control, disease/donor/age inseparable |
| [GSE306184](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE306184) | Nb3 external epithelial-response description, fourteen library workbooks | [E5 report](../Research%20Article/gate2_N2_nabhan_2026/reports/E5_EXTERNAL_FEASIBILITY.md); seven source groups, unresolved protocol and donor independence |
| [GSE307351](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307351), organoid child GSE307112; source datasets S1–S7 | Nb3/A22/A23 organoid counts, plate/imaging joins and source summaries; extends previously listed A10 use | [Nb3 register](../Research%20Article/gate2_N2_nabhan_2026/DATASETS.md); parent is not another cohort; wells share source preparations. Spatial child GSE307128 is separately qualified |
| [Tabula Muris Senis, Figshare 8273102 v2](https://doi.org/10.6084/m9.figshare.8273102.v2), author Figure 4 brain object and supplementary/receptor products | Nb5/A24–A27 tissue composition, RNA, microglial occupancy and repertoire descriptions | [Results](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/RESULTS.md), [extensions](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/EXTENSION_RESULTS.md), [source register](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/DATASETS.md); overlapping releases, noninteger normalized layers, pooled lung labels and repeated tissues are not independent raw-count cohorts |
| [GSE75109](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75109), [GSE75111](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75111), pinned Wagner/Compass author matrices | Wg 290-cell identity, RNA and author-score reproduction | [Source results](../Research%20Article/gate2_W1_wagner_th17_autoimmunity/RESULTS.md), [score results](../Research%20Article/gate2_W1_wagner_th17_autoimmunity/SOURCE_SCORE_RESULTS.md); cells are not 290 independent animals, author-normalized matrices differ from arbitrary GEO products |
| [GSE162300](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162300), [GSE162382](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162382) | Wg bulk estimated-count/TPM qualification and source-aligned RNA models | [Bulk results](../Research%20Article/gate2_W1_wagner_th17_autoimmunity/BULK_RESULTS.md), [models](../Research%20Article/gate2_W1_wagner_th17_autoimmunity/MODEL_RESULTS.md); technical runs collapse to libraries, split cultures/animal labels remain explicit |
| [GSE343897](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE343897) | DY1 scRNA/CMO baseline inspection; human numerical follow-ups reuse GSE136831/GSE135893 | [Corrected source result](../Research%20Article/gate2_DY1_damani_yokota_2026/SOURCE_V2_RESULTS.md), [stage ledger](../Research%20Article/gate2_DY1_damani_yokota_2026/README.md); feature-tag presence does not assign cells, pools or animals; condition/batch support unresolved |
| [GSE247223](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247223), [GSE248042](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248042), [GSE115504](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115504) | DY1-P02/A3 external RNA/ATAC benchmark, genotype/source-response and averaged-RNA descriptions | [Results and source routes](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/README.md); cross-condition reuse/cross-assay pairing unqualified; averaged CPM lacks replicate variance; not demonstrated NAM persistence |
| [GSE247943](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247943) | A3 bounded RNA-context display | [A3 dossier and evidence](research_dossiers/A3.md); source-specific expression context does not supply a matched memory assay |
| [GSE242510](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE242510) and Yadav source workbook | Yd1 six-library QC/annotation and RNA endpoint descriptions; separate workbook summaries | [Technical results](../Research%20Article/gate2_W3_yadav_2025/TECHNICAL_RESULTS.md), [qualification](../Research%20Article/gate2_W3_yadav_2025/SOURCE_QUALIFICATION.md); animal/pool/pair maps unresolved; scRNA archive does not contain the spatial measurements |
| [GSE234197](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE234197) | A32 external resolution-context description | [A32 dossier](research_dossiers/A32.md); source-defined units/coverage, not ARG1 perturbation or repair-function validation |
| [Hamanaka Figshare 28087574 v1](https://doi.org/10.6084/m9.figshare.28087574.v1) | Wg-P06/Yd1 selected processed-isotope description after workbook qualification | [T0 sources](../RQ_Specified/Yadav_followups_20261031/T0_RESULTS.md), [follow-up workspace](../RQ_Specified/Yadav_followups_20261031/README.md); source-version/block limits remain, no flux or donor-joined collagen/repair effect. GSE273882 RNA was metadata-only in T0 |
| [GSE160217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160217) | Saxton colon bulk counts/FPKM qualification and bounded transcript description | [Saved evidence](../Research%20Article/gate3_08_saxton_2021_il22/RESULTS.md), [current reassessment](../Research%20Article/gate3_08_saxton_2021_il22/reassessment_v1/README.md); six columns do not prove animals, receptor protein or repair function |
| [GSE302685](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302685), [GSE302687](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302687), [GSE329778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE329778) | Arz1 seven epithelial multiome libraries: RNA/QC and bounded chromatin descriptions | [Current results](../Research%20Article/ungated_arozamena_2026_inflammatory_memory/README.md), [qualification](../Research%20Article/ungated_arozamena_2026_inflammatory_memory/SOURCE_QUALIFICATION.md); article/GEO Multiome 1/2 names disagree, inferred donors are not validated animals, peak sets differ |
| [GSE347791](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE347791), [ImmGenT Zenodo 21839963](https://zenodo.org/records/21839963) | A27 processed receptor/annotation joins and operational-key concentration by nominal source code | [Result and corrected join](../RQ_Specified/A27_cd8_repertoire_state_redistribution/reports/SOURCE_CODE_CONCENTRATION_V1_RESULTS.md); nine source mice, receptor-independent state construction unproven, no age-effect inference |
| [GSE150068](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150068), [GSE150247](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150247) | A12 sorted ERBB-reference expression description | [Results](../RQ_Specified/A12_recipient_context/reports/ERBB_SORTED_RESULTS_V1.md); reference context, not the paired human precursor contrast |
| [GSE58998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58998) / PRJNA254138 | DuPage S0–S3 reconstruction and exploratory target screen | [Stage synthesis](../Research%20Article/gate3_09_dupage_2015/RESULTS.md), [screen](../Research%20Article/gate3_09_dupage_2015/TARGET_SCREEN_RESULT.md); deposited FPKM, twelve libraries/eleven retained, HET versus KO in CD62L strata; unknown mouse/pool/pairing, no raw-count or population inference |
| [GSE55773](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55773), parent GSE55753 | DuPage adapted Arvey chromatin-table comparison | [S3 result](../Research%20Article/gate3_09_dupage_2015/S3_RESULT.md), [amendment](../Research%20Article/gate3_09_dupage_2015/ANALYSIS_AMENDMENT_V2.md); pinned within-mm9 annotation, partial coverage and cross-study association. GSE55705 is the microarray companion, not this chromatin assay |
| [GSE262130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262130) | Executed DuPage candidate follow-up using Peeters' author-selected rlog matrix | [Current result](../Research%20Article/gate3_09_dupage_2015/CANDIDATE_ANALYSIS_RESULT_V1.md), [source qualification](../Research%20Article/gate3_09_dupage_2015/candidates/SOURCE_QUALIFICATION.md); twelve libraries and seven fixed genes/anchors. Mean-rlog differences are not log2 fold changes or comparable effect sizes to DuPage FPKM; no independent-validation claim |

| Source / product | Recorded use and limit | Evidence |
|---|---|---|
| GSE335749 / GSE335750 selected author differential-expression lists | A8 source-list sign audit and candidate interpretation; this is selected-list inspection, not a new full-matrix contrast. | [evidence](research_dossiers/followup_2026-10-03/SOURCES.md) |
| GSE297097 annotation table within ImmGenT Zenodo 21839963 | A27 source annotation/receptor join accompanying GSE347791; overlapping products are not independent cohorts. Receptor-independent state construction remains unproven. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A27_SOURCE_FOLLOWTHROUGH_V2.md) |

## Used source families and detailed boundaries

These source-specific descriptions retain normalization, units and reuse limits
from the earlier inventory. They belong to the used-source list above; they are
not a chronological queue of new work.

### Nb2 organoid bulk RNA

[GSE208770](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208770) has 18 mouse
AT2-organoid **bulk RNA-seq** libraries across six treatments, three labeled
replicates each. All counts were acquired and analyzed in the conditional
[Nb2 bulk adaptation](../Research%20Article/gate2_N1_nabhan_2023/trials/bulk_v1/REPORT.md).
The [study inventory](../Research%20Article/gate2_N1_nabhan_2023/DATASETS.md) distinguishes
this treatment experiment from the original single-cell receptor-map atlases.
The paper calls the replicates biological, but animal/preparation identity, pairing
and discrepant treatment timing still require reconciliation. This is not a
single-cell agonist-response dataset or an independently measured fate endpoint.

### Nb2 Stk3/4 and YAP/TAZ comparator

[GSE327565](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327565) now supplies
an executed mouse organoid Stk3/4-loss/YAP-TAZ comparator:14 bulk libraries,
separate3v3 SFFFM and4v4 ADM genotype contrasts. Source Figure8 reports mice;
cross-medium identities remain unresolved. This is distinct from GSE327686
multiome and GSE326359 human data. The existing A1 catalog was reused and the
processed count table downloaded publicly; no pooled multiome well was counted
as an independent bulk mouse. [Methods and source hashes](../Research%20Article/gate2_N1_nabhan_2023/branch_analysis/METHODS.md).
The same workspace reuses GSE208770 and GSE262927; these are additional analyses,
not independent validation cohorts.

### A19 human organoid counts and qPCR

[GSE197949](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE197949) supplies
eight analyzed alveolar-organoid bulk libraries (GSM5934407–GSM5934414), crossing
control/GSK3B-knockdown backgrounds with CHIR presence/absence in two source
blocks. The paper describes two donor cultures; GEO batches do not explicitly
map to donors, and knockdown hairpin differs by block. No population-level
DEG or interaction test was fitted. Of 60,662 count rows, 14,581 pass the frozen
expression filter. Other GEO samples are outside this analysis.

Supplementary Data 3 from [the associated 2022 human organoid paper](https://www.nature.com/articles/s42003-022-03828-5)
provides 143 extracted qPCR rows across five differentiation sheets, with exact
donor-code pairing and non-detects retained. These public source observations
support A19's lineage-context question; they do not measure Fzd withdrawal,
traced mature output or retained reserve. This is secondary analysis, not an
independent replication of Nb2. [Sources and hashes](../RQ_Specified/A19_fzd_response_reversibility/SOURCES.md) ·
[Results](../RQ_Specified/A19_fzd_response_reversibility/RESULTS.md).

### A20 atlas reuse and context eligibility

A20 reuses the GSE262927 author-annotated count object for 21 predefined genes,
with five paired AF1/AF2 day42 source samples at the primary 50-cell floor.
This is the previously exposed Nb2 atlas, not independent replication. Additional
identity probes and individual support/collagen measurements are reported under
[A20 results](../RQ_Specified/A20_fibroblast_fzd_context/RESULTS.md).

Zhou2025 supplies published Fzd2 perturbation evidence but no accession-linked
Fzd1/Fzd2 functional outcome join in the inspected article/supplement. Jones2024
GSE249931 supplies 17 public library records, including one named library each
for the Notch genotype contrast; animal replication remains unresolved. CellRef
LMEX0000004397/GSE122332 and human GSE135893 are reference/context candidates,
not newly executed intervention analyses. [Eligibility and identifiers](../RQ_Specified/A20_fibroblast_fzd_context/SOURCES.md).

### A20 matched fibroblast input cohort

[Ng-Blichfeldt et al. 2019](https://doi.org/10.1152/ajplung.00400.2018) deposited
[raw counts, figshare version 1](https://doi.org/10.6084/m9.figshare.7740071.v1):
32,734 genes, four human fibroblast donors, four concurrent input conditions
per donor (16 libraries). A20 extension_v1 uses all-gene TMM normalization and
44 of 45 frozen requested genes; FZD10 is absent and explicitly unavailable.
The source count SHA256, frozen Ensembl mapping and retrieval metadata are
under [extension metadata](../RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/metadata/intake.json).
All four donors are retained with donor contrasts, leave-one-donor means and
total-count sensitivity; no inferential model was fit.

The source's functional cohort comprises eight different donors. RNA and
function cannot be donor-joined. CHIR is downstream of FZD; simultaneous TGF
does not define prior state. Jones GEO/BioSample and Riccetti GEO metadata were
audited for units, with no additional numerical fits.
[Assay-level eligibility](../RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/metadata/assay_evidence.tsv)
preserves these boundaries.

### A21 capillary RNA context

[Godoy et al. 2023](https://doi.org/10.7554/eLife.80900),
[GSE211335](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE211335):
12 animal barcodes, three per condition, across three technical library pools.
A21 aggregates raw counts for 26 predefined genes over the 5,423 deposited
endothelial cells and preserves source-defined clusters. All-gene raw denominators
are used; a [documented discrepancy](../RQ_Specified/A21_fzd4_capillary_function/reports/denominator_amendment.json)
with deposited QC totals prompted a recorded sensitivity, not exclusions.
This is independent expression context for the prior GSE262927 lead, not Fzd4
perturbation or traced lineage evidence. No cell/pool is treated as an animal.

The [source eligibility inventory](../RQ_Specified/A21_fzd4_capillary_function/SOURCES.md)
also distinguishes Gillich's lineage rationale, Bian's tumor endothelial FZD4
restoration and epithelial FZD4 repair evidence. Failed source-table downloads
remain in the intake record; those studies were not numerically reanalyzed.

### A21 functional source workbooks

[Extension sources](../RQ_Specified/A21_fzd4_capillary_function/extensions/extension_v1/SOURCES.md)
add numerical reconstruction from Bian 2024 Figure 3F and Figure 7D-G workbooks.
The 88 observations are panel records, not 88 distinct animals; anonymous rows
cannot be joined across outcomes. Fzd4 restoration occurs in tumor endothelium;
perfusion is measured in a separate Foxf1-loss comparison. GSE255969 has four
control/four Foxf1-deficient bulk samples and no rescue arm; no bulk fit was run.
The existing GSE211335 cohort now has 36 predefined genes, including all ten Fzd
receptors and Foxf1. It is reused evidence. GSE262927 coarse CAP labels do not
validate the Godoy major/transitional contrast. A 2026 retinal preprint supplies
cross-organ literature context only. No joined adult-lung functional test is added.

### Wp mouse and human source reconstruction

Executed source reconstruction for [paper 17](../Research%20Article/gate2_W2_wagner_Th17_PGAM/README.md);
full inventory and limits in its
[dataset register](../Research%20Article/gate2_W2_wagner_Th17_PGAM/DATASETS.md).

| Accession | Design as deposited | Recorded use | Unit and current limit |
|---|---|---|---|
| [GSE289733](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289733) | mouse Th17n/Th17p single-cell RNA at 1 mM and 25 mM glucose; 8 sample records, 2 animal labels, one aggregated matrix of 19,203 barcodes x 31,053 genes | Wp-R1 single-cell reconstruction | cells nested in 8 libraries from 2 animals crossed with all four conditions (two libraries per condition); aggregation suffix-to-GSM order is not declared, and the 5,192-cell analysed set is not deposited. A paired within-animal contrast exists at n = 2; no population inference |
| [GSE290297](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290297) | mouse Th17n/Th17p population RNA with EGCG, DHEA and solvent controls, split by division gate; 79 libraries joining one-to-one to 79 TPM columns over 20,465 genes | Wp-R3 bulk contrasts | library; no animal or culture field is deposited and the values are TPM, not counts. Div.1 and Total are different gated populations, not replicates |
| [GSE138266](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138266) | human MS and idiopathic-intracranial-hypertension blood and CSF leukocytes; 22 samples resolving to 12 donor codes, 10 with both tissues | Wp-R4 signature transport | donor, paired across tissue where available; reused cohort from Schafflick 2020, and no age, sex or treatment field is deposited |

Original published scVI inputs and the listed functional/source measurements
were not recovered in the documented source search. This does not establish
source-wide absence or mean that the repository's substituted Compass
computation was unrun; use the current correction report linked above.
Raw caches stay ignored under `raw_data/wagner_pgam_w2_20261004/`.

**Current correction:** R0–R4 and selected extensions executed. [The correction report](../Research%20Article/gate2_W2_wagner_Th17_PGAM/CORRECTIONS_2026-10-07.md) records corrected Compass orientation and full-library human normalization. The substituted Compass run is distinct from unrecovered published scVI inputs and recovered author scores.

## Inspected sources and comparison failures

A source used above can remain ineligible for a different comparison below. The latest owning result/amendment controls execution status; a historical screen is retained with its scope.

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

### Metadata and assay qualification

| Source(s) | Recorded role and authority |
|---|---|
| GSE141635 | A1 direct-histone interval/header qualification and source context; calling/scaling limitations in [first batch](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/FIRST_BATCH_REPORT.md) and [current reference map](../RQ_Specified/A1_transitional_epithelial_state_distinction/reports/ANALYSIS_REFERENCE_MAP.md) |
| GSE215824; GSE307128 | A22/Nb3 source/assay and spatial qualification; source study already reused the first; spatial blocks do not prove animals. [Context audit](../Research%20Article/gate2_N2_nabhan_2026/reports/CONTEXT_ELIGIBILITY.md), [source register](../Research%20Article/gate2_N2_nabhan_2026/DATASETS.md) |
| GSE165088 | Wg ATAC qualification; unresolved joins and independence. [Pre-RQ dispositions](../Research%20Article/gate2_W1_wagner_th17_autoimmunity/PRE_RQ_EVIDENCE.md). GSE164999/GSE74833 are umbrella locators, GSE75110 is outside the intended 290-cell subset |
| GSE280183 | DY1 eight-library ATAC source qualification; see [source correction](../Research%20Article/gate2_DY1_damani_yokota_2026/SOURCE_QUALIFICATION_CORRECTION.md) |
| GSE210341; GSE331144 | Yd1 injury/repair source and annotation qualification with bounded extension work. [Extension dispositions](../Research%20Article/gate2_W3_yadav_2025/extensions_20261031/README.md); no automatic promotion to an independent repair-effect cohort |
| GSE302684; GSE329696; GSE329965 | Arz1 bulk-ATAC listing, bulk-RNA and immune-scRNA schema qualification. [Report](../Research%20Article/ungated_arozamena_2026_inflammatory_memory/SOURCE_QUALIFICATION.md); merged tracks cannot supply sample variance, Salmon estimates are fractional, immune cohort is separate from epithelial multiome |
| GSE145230/GSE145231; GSE188288 | Yd1 neutrophil source records, assay and sample joins. [Checkpoint C](../Research%20Article/gate2_W3_yadav_2025/extensions_20261031/CHECKPOINT_C_RESULTS.md); no donor-independent numerical biological comparison admitted |
| GSE110465; GSE115085; GSE115502; GSE115505; GSE151015 | DY1-P02 temporal source audit. [Source review](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/E6_SOURCE_REVIEW.md); no qualified matched temporal RNA-ATAC panel |
| GSE169125; GSE304587/E-MTAB-13526; GSE306194/GSE306714 | A2, A12 and A8 source qualification respectively; exact registered analysis IDs/receipts in the [census](audits/2026-11-07-public-data-inventory/snapshot_v2/accession_references.csv). A metadata input is not a newly executed expression contrast |
| GSE67602 | A0 skin fallback feasibility only; [original feasibility report](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/PILOT_REPORT.md), superseded for broader A0 execution by its later reports |

### A5 unchanged replication screen

The day 2–21 window, three-mouse floor and fixed measurement apply to this A5 comparison. Later amended work is a separate comparison. [Recorded assessment](roadmap_runs/2026-09-27-followthrough/EXPANDED_CANDIDATE_AUDIT.md).

| Additional cohort | Source finding | Decision for unchanged A5 |
|---|---|---|
| GSE262927 | Six retained, author-annotated early samples; transitional counts 4, 23, 14, 11, 127, 10 before the depth filter | Only one reaches 30; activated-AT2 label also absent. Stop for the current annotated population. Unknown/unannotated cells are not relabelled to rescue it. |
| GSE243124 | Day 10; multiple mice pooled into one GEM lane per treatment | No recovered mouse-resolved contrasts |
| GSE243135 | Demultiplexed individual samples exist, but day 28 | Outside fixed day 2–21 window; eight sequencing sublibraries are not eight animals |
| GSE252588 | Three lineage-sorted populations at four weeks | Outside window; populations are not independent mice |
| GSE132771 | Two bleomycin mice, each split GFP+/−, day 14 | Below three-mouse floor; sorted fractions do not add mice |
| GSE129605 | Four numbered bleomycin samples, day 11, counts locally available | No deposited per-cell state annotation or independently verified sample-to-animal crosswalk established by this pass; no invented activated comparator |
| GSE202325 | Three young and three aged samples at days 3/9; original code uses broad AT2 annotations and local RDS files | Strong candidate for an amended annotation/transport study, not a ready unchanged state contrast. Lack of uninjured controls is not the A5 exclusion. |
| GSE292515 | Fixed-RNA/probe profiling, day 7, three infected samples per age | Assay transport and population correspondence not established; do not silently equate a fixed-probe budget with the frozen full-transcript UMI measurement |
| GSE184854 | Silica; TAS-Seq processing describes read counts, two pooled sequencing records | Frozen 500-UMI measurement not established; read counts are not molecule counts |
| GSE264278 | Five biological replicates described, with sample tags; TAS-Seq read-count processing | Replication is not the only gate: unchanged UMI instrument fails assay correspondence |
| GSE201698 | Six time-point records; processing says reads counted, despite raw-read UMI description | Deduplicated UMI provenance not established; time-point GSMs do not prove animal replication |
| GSE303646 | 56 samples, with 24 young/old bleomycin samples at days 3/10/20 | Promising candidate requiring barcode-level author state labels, sample identity and raw-count provenance; deposited dge/summary files alone do not provide the required state contrast |

### A0 developmental and cross-epithelium recovery

Source recovery distinguishes rejected discovery roles, access holds and selected alternatives. Completed Sountoulidis/Haber analyses are listed above. [Recorded assessment](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/SOURCE_RECOVERY.md).

| Candidate | New check | Decision |
|---|---|---|
| Original Negretti developmental atlas | Separate endpoint comparisons permitted by the original plan | Counting pairwise comparisons cannot supply three intermediate-versus-AT1 units; animal mapping remains missing |
| Guo P1, reused as a list by A5 | [Source Figure 1](https://www.nature.com/articles/s41467-018-07770-1) has two mice | Useful list source, below A0's three-unit discovery floor |
| Zhang/Chuang Hippo 2026 | [GSE319370](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE319370) has one control deposit at each of two ages, plus mutants | Two normal observations cannot provide three independent normal comparisons; do not count mutants as normal development |
| He 2022 fetal lung | Downloaded author-linked 9,096-cell epithelial object; read metadata only | Late-tip/late-stalk/AT1 coverage fails, including separate endpoint comparisons; no expression effects inspected |
| Quach 2024 fetal lung | [Author resource](https://github.com/The-HQQ/Human_fetal_lung_atlas) identifies a smaller epithelial object | Anonymous Synapse file download returned 403; GEO whole object is 7,981,428,892 bytes. Local free memory was about 1.8 GB at inspection. Eligibility remains unknown; this is not evidence of insufficient replication |
| Sountoulidis 2023 | [Paper-linked UCSC atlas](https://cells.ucsc.edu/?ds=lung-dev) supplies donor IDs, annotations and matched integer counts | Select the declared early airway axis; 11 complete donor triplets before expression-based discovery |
| Miller 2020 | A similarly named UCSC entry was initially reached; its description identifies a different study | Retain the retrieval trail, but do not misattribute it or select it as D2 |
| Original Haber immature-proximal branch | Four mapped mice; two complete triplets | Historical proposal remains ineligible |
| Revised Haber late-progenitor branch | Same four mapped mice; three complete triplets | Freeze this earlier commitment-stage comparison before any programme effects; do not claim the progenitors are uniquely proximal |

### A15 activation-versus-ligand comparison

These candidates do not provide the required integrin perturbation / recipient activation comparison. GSE190821 nevertheless supports the separately recorded expression contrast. [Recorded assessment](../RQ_Specified/A15_epithelial_integrin_tgfb_activation/reports/PUBLIC_DATA_SEARCH.md).

| Deposit | Size | What it is | Why it cannot test A15 |
|---|--:|---|---|
| **GSE190821** | 48 libraries, 24 mice | Lung epithelial translatome and whole lung under bleomycin, with the 3G9 anti-integrin-beta6 antibody (4 mice) against the inert antibody Axum8 (7 mice), plus an IRE1a arm; RiboTag with ShhCre, day 7 | The nearest. It has replication and the mouse as the unit, but **no activation readout**, and its only fibroblast-containing sample is whole-lung homogenate, which confounds the fibroblast compartment with fibrosis extent. No ligand arm exists, so the partition cannot be formed |
| GSE298207 | 6 | Reconstructed human epidermis; inflammation driving TGF-beta1 activation through the alphaVbeta6 integrin and mechanotransduction | Skin keratinocytes, no fibroblast recipient in the deposit, and the deposited measurement is RNA |
| GSE224401 | 12 | ITGB6 induced through a TET-On system in breast myoepithelial cells | Gain of function on the epithelial side only, with the epithelial transcriptome as the readout and no recipient cell |
| GSE2255, indexed as GDS1874 | 15 | Alveolar macrophages from the Itgb6-null mouse emphysema model, on arrays | An Itgb6-null lung, but the readout is the macrophage, and the phenotype in that model is Mmp12-driven emphysema rather than fibroblast activation |
| GSE253494 | 4 | Itgb6 interference in renal proximal tubular epithelial cells under hypoxia and reoxygenation | Wrong organ, epithelial readout only, no recipient, and four samples |
| GSE307128 | 4 | A sibling series of the screen A2 used, in the same superseries GSE307351, mouse, type recorded as Other | Four samples, and its content is not a replicated integrin perturbation with an activation readout. Its series summary states the source paper's conclusions; that text is deliberately not used here, since the owner has not read roadmap paper 14 |

### A10 independent growth-screen replication

These inspected candidates do not replicate the fibroblast-supported growth screen. [Recorded assessment](../RQ_Specified/A10_organoid_growth_outcome/reports/PUBLIC_DATA_SEARCH.md).

| Series | Samples | Why it is not a replication cohort |
|---|--:|---|
| GSE271971 | 72 | Alveolar epithelial growth supported by microvascular endothelium. The niche partner is endothelial, not fibroblast, so the dialogue being modelled differs. The nearest candidate of the set. |
| GSE213975 | 14 | A type 2 organoid platform for lung adenocarcinoma subtypes. Too few samples, and the outcome is tumour modelling. |
| GSE162859 | 8 | An alveolar organoid model on arrays. Too few samples, no perturbation series. |
| GSE313671 to GSE313673 | 2 to 6 | Alveolar regeneration mechanism studies, not organoid growth screens. |
| GSE221402, GSE223664, GSE183423 | 1 to 6 | Fibroblast biology in lung; no organoid growth endpoint. |

| Additional comparison / source | Disposition and reason | Evidence |
|---|---|---|
| A3 / GSE303646 | Inspected; age-by-postinjury association is definable, but elapsed aging/harvest and persistent injury are not isolated; no same-cell memory inference. | [evidence](roadmap_runs/2026-09-27-followthrough/EXPANDED_CANDIDATE_AUDIT.md) |
| A5 / GSE113049 | Rejected for unchanged replication: injured samples are split sorted fractions rather than sufficient independent mice. | [evidence](roadmap_runs/2026-09-27/P2_REPLICATION_ELIGIBILITY.md) |
| P3/P5 / GSE215824, GSE286986, GSE295566 | Inspected; no qualified replicated early-mark/descendant linkage or IL1-withdrawal crossed with a post-entry recipient intervention. | [evidence](roadmap_runs/2026-09-27-followthrough/EXPANDED_CANDIDATE_AUDIT.md) |
| A0 / GSE215896 | Rejected mistaken identity: an initial guessed accession had an unrelated title; the authoritative parent is GSE215898 and the scRNA child GSE215895. | [evidence](../RQ_Specified/A0_conserved_epithelial_transition_program/reports/SOURCE_RECOVERY.md) |
| A16 / GSE260762, GSE155166 | Rejected hits in the dated Cd177/lung metadata search: unrelated subjects; no evidence of source-wide absence. | [evidence](research_dossiers/followup_2026-10-03/SOURCES.md) |
| A27 / GSE154935 | Inspected and unsuitable as the proposed young/old paired scRNA/TCR source: sorted bulk RNA from four old mice. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A27_SOURCE_INTAKE_V1.md) |
| A27 / GSE145562, GSE155006 | Inspected; pooled organ/age data, not independently resolved animals. GSE155006 is a source locator; descriptive source-product qualification remains possible. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A27_SOURCE_INTAKE_V1.md) |
| A27 / GSE155005, GSE275967 | Inspected; transfer/genotype contrasts do not replace an unperturbed age comparison. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A27_SOURCE_INTAKE_V1.md) |
| DY1 E6 / GSE115502 | Excluded from repeated-IL4 cultured-macrophage history comparison: muscle-injury populations and time points are a different design. | [evidence](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/E6_SOURCE_REVIEW.md) |
| A20 / GSE171812 | Metadata/assay context only; neonatal hyperoxia fibroblast data do not supply a donor-joined FZD response/function comparison. | [evidence](../RQ_Specified/A20_fibroblast_fzd_context/extensions/extension_v1/SOURCES.md) |
| A19 / GSE221343, GSE246243, GSE150068 | Inspected external reference candidates, not numerical A19 extension inputs. GSE150068 is used separately by A12 above. | [evidence](../RQ_Specified/A19_fzd_response_reversibility/EXTERNAL_EVIDENCE.md) |

## Pending sources and unresolved access

Pending is an evidence status, not an authorized execution queue. Explicitly
unselected or gated comparisons remain so. Used products above do not qualify
every other assay, cell population or proposed comparison in the same study.

### A1 inspected assay catalog and remaining joins

These rows preserve source/assay qualification and comparison limits. Several source products now have bounded executed uses listed above; proposed uses in the catalog do not supersede those results. [Recorded assessment](../RQ_Specified/A1_transitional_epithelial_state_distinction/STUDY_MAP.md).

| Study/resource | Deposited evidence | Role and limitation for A1 |
|---|---|---|
| [Kobayashi PATS study, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7461628/); [GSE141635](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141635) | 20 GSM: H3K4me3, H3K27ac, H3K36me3 and H3 in injured CTGF-positive epithelium versus homeostatic AT2; TP53/input in the transitional population; two replicate labels | Direct histone/TF evidence. Injured state, injury exposure and sorting are confounded; pooled tracks alone do not support replicated differential occupancy. |
| [Tsutsui et al., 2026](https://www.nature.com/articles/s41467-026-68909-z); [GSE289683](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289683), [GSE291333](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291333) | 12 + 12 GSM: iATC/iAT2/iAT1, two replicate labels, H3K27ac/H3 or H3K4me3/H3K27me3 | Direct modification comparisons in an iPSC model, not evidence for all human donors. Keep culture preparations and cell-line independence distinct. |
| Same study: [GSE290014](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290014), [GSE289846](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289846) | Three scATAC libraries; six scRNA libraries | Separate assays, not paired multiome. Baseline RNA culture day 7 differs from ATAC day 14; state/culture alignment must be explicit. |
| Same study: [GSE289676](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289676), [GSE289678](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289678), [GSE289679](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289679), [GSE289682](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289682) | Epithelial and fibroblast bulk RNA; 9/9/6/6 GSM. BLM ± p300/CBP inhibitors; TRF2 epithelial DOX ± CBP30; fibroblast PBS versus DOX coculture | Response/compartment comparisons after preparation IDs are resolved. GSE289682 is not an inhibitor contrast. |
| Same study: [PRJDB37980](https://www.ebi.ac.uk/ena/browser/view/PRJDB37980), [PRJDB37982](https://www.ebi.ac.uk/ena/browser/view/PRJDB37982), [PRJDB37983](https://www.ebi.ac.uk/ena/browser/view/PRJDB37983) | ENA lists 26/6/32 runs; RNA/CUT&Tag-related sequencing | Run existence verified; mark/treatment/pair mapping is incomplete. Sequence runs are not biological replicates. Do not infer a mapping from the order in the article's data statement. |
| [Zhou et al., 2021](https://link.springer.com/article/10.1186/s12864-021-08152-6); [GSE150527](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE150527) | 48 GSM: histone marks, FAIRE, CTCF, RNA and WGBS across human AT2-to-AT1 culture | Normal differentiation comparator. RNA has three donor labels, selected histones two, WGBS only one donor at D0/D4/D6. No population DMR inference. D4 culture is not a purified DATP/PATS sample. |
| [Marjanovic HPCS study, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7745838/); [GSE154966](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154966) | Eight bulk ATAC GSM and deposited counts/merged peaks; four apparent TIGIT-positive/negative source blocks | First processed-count candidate. Resolve the pooled `106621_106642` source and independence of all blocks. Cancer context and Kras/Trp53 genotype constrain interpretation. |
| Same study: [GSE154965](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154965), [GSE154978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154978) | Two scATAC GSM with fragments; six sorted/transplant scRNA GSM | scATAC titles and file suffixes conflict; label-dependent analysis is on hold. Transplant samples require source/outcome pairing, not assumed matching. |
| Choi DATP-associated ATAC: [GSE144598](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144598) | Four ATAC GSM; two pooled processed BigWigs; SRA relations listed | IL1R1-positive AT2 versus control AT2, not a purified DATP comparison. Raw-read reprocessing is potentially possible; the processed-track limitation is not absence of raw data. |
| Existing local multiome: [GSE310539](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310539), [GSE247130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247130) | Eight/twelve RNA+ATAC GSM correspond to four/six wells | Paired RNA/accessibility and depth controls. Preserve the repository's corrected well/genotype map; pooled animals and one well per condition do not support animal-level effects. Same laboratory is not independent replication. |
| [GSE309751](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE309751) | 14 bulk ATAC GSM; post-viral time points and Kras perturbation; processed peak calls and SRA relations | Two 49-day control GSM have contradictory treatment fields. Peak-call presence alone is not quantitative accessibility or same-cell reopening. |
| [GSE327686](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327686), [GSE327565](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE327565) | Eight RNA/ATAC GSM in four multiome conditions; separate 14-GSM organoid bulk-RNA series | GSE327686 series design describes bulk cultured AT2 despite whole-lung RNA/ATAC GSM; resolve before use. GSE327565 must not be labelled multiome. |
| Study/resource | Distinguishing measurement | Planned use and limitation |
|---|---|---|
| [Strunz et al., 2020](https://www.nature.com/articles/s41467-020-17358-3); [GSE141259](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259) | Injury chronology, epithelial enrichment and published lineage/velocity analyses; 60 GSM across preparation types | Reconstruct time-associated state paths with sample-aware uncertainty. Resolve preparation overlap. Ordinary count matrices cannot supply splicing layers or measured lineage histories. [Author code](https://github.com/theislab/2019_Strunz). |
| [Auyeung et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35170357/); [GSE190821](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190821) | Krt19 pulse/chase and AGER endpoint under IRE1α inhibition; separate day-7 RiboTag RNA; 48 GSM representing epithelial and whole-lung libraries from 24 mice | First RNA contrast completed: five KIRA8 versus five vehicle mice with batch/sex adjustment. Axum8 is a separate antibody control. RiboTag expression does not identify traced DATPs, fate transitions or chromatin changes. |
| [Chan et al., 2026](https://www.nature.com/articles/s41586-025-09985-x); [GSE277777](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277777) | HPCS tracing/ablation, GEX and HTO, processed objects; 32 GSM | Distinguish lineage origin, chase and perturbation from a shared RNA programme. Some animals are pooled. HTO is sample hashing, not a protein-phenotyping panel. Existing A11 projection is not a reanalysis of lineage outcomes. |
| [Krt8 perturbation study](https://www.jci.org/articles/view/165612); [GSE223302](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE223302) | 24 bulk-RNA GSM, WT/KO time course | Time-by-genotype response after replicate verification. Links molecular state to perturbation; bulk expression alone cannot prove irreversible fate. |
| [Aberrant intermediate epithelial cells, 2025](https://www.nature.com/articles/s41467-025-63735-1); [GSE273123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273123) | 16 CD44-positive/negative sorted AT2 RNA GSM, WT and SP-C mutant; published fibroblast-response assays | Protein-enriched populations provide an orthogonal selection axis. Four candidate pairs per genotype require animal-ID confirmation. This is not mass-spectrometry proteomics. |
| Same study: [GSE273122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE273122), [GSE272862](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272862) | Four mouse scRNA GSM; two iAT2 genotype/corrected GSM | Mouse titles and genotype characteristics are reversed relative to each other: hold genotype tests. One library per human genotype limits inference. |
| [Ke developmental transition study](https://doi.org/10.1016/j.devcel.2024.11.017); [GSE254356](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE254356) | Three embryonic sorted epithelial scRNA GSM and published lineage evidence | Developmental reference coordinated with A5; two-versus-one preparation design, not an adult repair validation cohort. |
| [Konkimalla et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10762634/); [GSE218665](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218665), [GSE218666](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218666), [GSE235212](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE235212) | BHT injury, AT1 ablation and AT2 Mdm2 deletion; 2/4/1 GSM | Tissue topology, mechanics and perturbation anchors. Deposits alone do not encode every imaging or fate endpoint; one sample per time is descriptive. Shared external controls are not new independent cohorts. |
| [IPF regenerating-niche atlas, 2025](https://www.nature.com/articles/s41467-025-61880-1); [Zenodo 10930946](https://zenodo.org/records/10930946) | 33-channel imaging mass cytometry; 22 MCD files (~15.55 GB) | Cell proteins, morphology and neighbourhoods. Prefer [processed cell data](https://mdv.molbiol.ox.ac.uk/projects/mdv_project/7430) after donor/ROI/mask/channel audit; 22 files are not 22 donors. Pathology stages are cross-sectional. [Code](https://github.com/LingPeiHo/Ho_Taylor_Byrne-SpOOx-2.0). |
| [MUC5B regional proteomics study, 2025](https://insight.jci.org/articles/view/189636); [PXD058626](https://www.ebi.ac.uk/pride/archive/projects/PXD058626) | Laser-capture microdissection mass spectrometry of defined lung regions, including epithelium over fibroblastic foci | Regional protein corroboration with donor/genotype blocking. Project metadata verified; processed abundance matrix and donor-region map remain unverified. Mixtures are not a purified transitional-cell proteome. |
| [SAGE Perturb-seq preprint, 2026](https://www.biorxiv.org/content/10.64898/2026.03.13.711474v1) | Time-resolved TF perturbation and repair/pathological epithelial branches | Literature anchor. Version 1 promises deposition; no new public accession was verified. Human reference accessions cited there are not its new perturbation data. |

### Nb5 external proposal sources

These are proposal/qualification sources. Existing TMS/author-product execution is listed above; no new external comparison is implied. [Recorded assessment](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/rq_derivation/SOURCES.md).

| Primary source | Established precedent | Consequence for these proposals |
|---|---|---|
| [Li et al., Nature Aging 2023](https://www.nature.com/articles/s43587-023-00479-x) | Sex-divergent microglial ageing, including a female middle-age pattern | P02/P07 must specify region, sex and a discriminator beyond generic age states. The [2024 correction](https://www.nature.com/articles/s43587-024-00571-w) changes an acknowledgment grant number, not this result. |
| [Hammond et al., Immunity 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6655561/) | Microglial states across lifespan and injury | State diversity is prior knowledge; a P02 configuration must be independently reproducible and distinguishable from alternatives. |
| [Jin et al., Nature 2025](https://www.nature.com/articles/s41586-024-08350-8) | Region- and cell-type-resolved brain ageing in young and old mice of both sexes | Useful external context, but two ages cannot validate an intermediate-age configuration. Young reference reuse also requires overlap accounting. |
| [Mogilenko et al., Immunity 2021](https://pubmed.ncbi.nlm.nih.gov/33271118/) | Clonal GZMK-positive ageing-associated CD8 populations | P06 cannot claim the existence of clonal older CD8 cells as new; test the within-state versus redistribution question. |
| [Al-Naggar et al., Aging Cell 2025](https://doi.org/10.1111/acel.14399) | Senescence-like features in polyploid umbrella cells across the lifespan | P01/P05 must separate normal differentiation from dysfunction; marker positivity is not sufficient. Article published online in 2024. |
| [Meguro et al., Nature Aging 2024](https://www.nature.com/articles/s43587-024-00704-1) | Age-associated fibroblast context and CXCL12 in bladder tumour permissiveness | The cancer mechanism is established precedent, not evidence of the proposed normal barrier mechanism. |
| [Angelidis et al., Nature Communications 2019](https://www.nature.com/articles/s41467-019-08831-9) | Independent normal-age lung RNA and proteomic profiles | Candidate reference for P03 endpoint specificity; it does not by itself identify a prior-injury effect. |
| [Zhang et al., eLife 2021](https://elifesciences.org/articles/62293) | Shared and cell-type-specific ageing programmes from TMS | Same-atlas reuse is not replication; broad shared-program discovery is insufficient novelty for P04. |
| [Schaum et al., Nature 2020](https://pubmed.ncbi.nlm.nih.gov/32669715/) | Organ-dependent temporal ageing signatures | Broad nonlinear ageing is already prior knowledge; P08 needs a specified endpoint and a selection-aware design. |
| Deposit | Design or access confirmed | What it can support after qualification; remaining limit |
|---|---|---|
| [GSE207932](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207932) | Li single-cell microglia: female 3/14/24-month baseline-control and acute-challenge contexts; processed archive listed | Potential female age-state comparison using baseline controls only. Exact cell-to-animal map and regional compatibility are pending; not a matched both-sex 3/18/24 design. |
| [GSE208386](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE208386) | Li bulk microglial age series in both sexes; processed CSV listed with `after_combatseq` in its name | Sex context at bulk level. Need original scale, batch and animal metadata; do not treat adjusted bulk values as unprocessed single-cell counts. |
| [GSE121654](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE121654) | Hammond lifespan and injury groups; record describes animal replicates and processed files | Candidate independent microglial context. Age schedule and cell-to-animal, sex and anatomical mapping must match the specified comparison; not an exact three-age regional replication. |
| [GSE145562](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145562) | Mogilenko multi-organ immune expression plus receptor libraries; three mice per age pooled before sequencing | State/clone context. A pooled library does not provide three independent mouse observations without individual demultiplexing. No mouse-level replication claim here. |
| [GSE180128](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE180128) | Bladder single-cell, single-nucleus, spatial and bulk sources; processed archive and bulk files listed | Cell and spatial context candidate for P01/P05. Exact age/sex/animal and modality matching pending. Al-Naggar reuses this atlas: that reuse is not a second replication. |
| [GSE247123](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247123) | Female bladder bulk at 2/10/26 months plus intervention arms; count and TPM files listed | Whole-bladder contextual evidence only until controls, units and treatment histories are qualified. Cannot directly validate a male cell-state or stromal/barrier association. |
| [GSE253338](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253338) | Aged reporter-positive and reporter-negative bladder stromal populations | Selected stromal context. The deposited comparison is not a young-versus-old normal whole-bladder replication; individual-animal and reporter-selection limits must be retained. |
| [GSE124872](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE124872) | Normal-age lung single-cell and bulk sources, with metadata and expression files listed | P03 normal-age reference after macrophage identity and animal mapping. Separate assay cohorts are not cell-matched RNA/protein observations or an injury-history contrast. |
| Snapshot | Bytes | SHA-256 |
|---|---:|---|
| GSE207932 | 2749 | `5e32152ec3d72e4b46ece8e31c7d6c95b70a68884370ac7fd76b555745f08963` |
| GSE208386 | 4551 | `4bbfdf0fd472ae13d1f72f0b6fad5e26001dd792abade7089e546823130bb2bf` |
| GSE145562 | 3433 | `28529f6a85b88b7cc44e10869de53638fee4dd4b82ea9f12454cf3fb8b568ea9` |
| GSE180128 | 2908 | `3cca94e75e4d648f052825e12c5b8c5922122b7241b8ab68e976e42df37c9f1c` |
| GSE247123 | 4664 | `fa649580f18115f7780b4738a7ef4277d71ff8d5af1d39bad8080197b928801d` |
| GSE253338 | 1710 | `b090cdc510b197a4a0d0ddf9c1523129060dc0f0aa00e4bb36ece24374bf2069` |
| GSE124872 | 3714 | `dd07e9555b7a8a8567b41ddee1857777b4d3b4c0b271bc93b034d1a352c11729` |
| GSE121654 | 3063 | `a72a5c94ac82c441557dd834efa2b7098b579991657a2979e785d7bab1a6c096` |

### Nb4 proposal-specific reuse and missing sources

Prior use and exposure remain explicit. S09/S10 have no qualified source identifier; they are gaps rather than invented datasets. [Recorded assessment](../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/proposals/SOURCES.md).

| ID | Source and current evidence | Proposed role | Qualification needed before fitting |
|---|---|---|---|
| S01 | [Travaglini/Nabhan 2020](https://doi.org/10.1038/s41586-020-2922-4); Nb4 used pinned human CELLxGENE releases, source supplements and author code | Discovery and selected source reconstruction across P01–P09 | Verify each newly extracted compartment, full-gene layer, sample nesting and label exclusions; prior Nb4 effects are exposed |
| S02 | Original mouse atlas, [PRJNA632939](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA632939); source metadata inspected in Nb4 | P01 mouse reference; P02/P06 comparative context | Individual versus pooled animals, age/anatomy, assay and gene maps remain unresolved for the new matched comparison; published differential-gene tables are not a complete ortholog universe |
| S03 | [Madissoon 2023](https://doi.org/10.1038/s41588-022-01243-4); Nb4 used only its pinned fibroblast subset | P09/P03 fibroblast context; full release is a candidate for immune, epithelial and vascular validation | Existing fibroblast subset cannot supply missing compartments. Full expression: PRJEB52292; spatial: E-MTAB-11640; imaging: S-BIAD570. Recover exact version, cell/nucleus modality, region, donor overlap and independent image annotation |
| S04 | [Sikkema HLCA 2023](https://doi.org/10.1038/s41591-023-02327-2); neighboring repository article available | Annotation crosswalk, cohort discovery, independent study selection | Trace source-study and donor IDs; an integrated object can contain S01, S03 and disease cohorts. Exclude overlaps and document annotation-training exposure; return to original counts for expression tests |
| S05 | [Adams GSE136831](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136831); already used in neighboring article analyses | P03 IPF discovery, P05 immune context, P07 disease epithelium | Re-audit diagnosis, regional sampling, raw layer, donor joins and prior exposure; use source-defined IPF/control groups, not a mixed diagnosis bucket |
| S06 | [Habermann GSE135893](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135893); already used in neighboring analyses | P03/P07 second-cohort transport | Restrict primary disease comparison to verified IPF and controls; exclude other fibrotic diagnoses from that estimand; reconcile donor overlap, anatomy and labels |
| S07 | [Murthy GSE178360](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178360); three source filtered matrices joined in the completed Nb4 MYRF diagnostic | Candidate epithelial reference for P01/P06/P07 | Prior candidate epithelial labels and sparse AT1 coverage do not establish basal/AT2-s coverage, regional validity or independence for the new endpoint |
| S08 | [Mouse lemur atlas 2025](https://doi.org/10.1038/s41586-025-09114-8); primary paper inspected, no new matrix used | P02 third-species qualification and updated novelty screen | Audit actual lung biological units, age, orthology release, raw layers and reuse of human/mouse sources. Published expression-based mappings must not define the same alignment used to test expression conservation |
| S09 | Independent matched human lung–blood cohort | P04 external validation | **No qualified accession selected.** Find paired donor/subtype coverage and tissue-processing details; a lung-only atlas can validate localization but not the lung–blood contrast |
| S10 | Independently annotated spatial or functional observations | P05/P07/P08/P09 specificity; P04 persistence; P06 fate | **No linked functional dataset qualified.** Spatial candidate S03 does not by itself measure duration, ancestry, stemness, perfusion or electrophysiology |

| Source / owner | Pending or reference disposition | Evidence |
|---|---|---|
| GSE262129, GSE291449 / DuPage–A33–A35 | Later-study source leads; not executed inputs in the GSE262130 candidate follow-up. | [evidence](../Research%20Article/gate3_09_dupage_2015/candidates/SOURCE_QUALIFICATION.md) |
| E-MTAB-8861 / TIGIT study | Identity-conflicted stated accession; recovered metadata do not match the cited study. Single-cell data were not analyzed. | [evidence](../Research%20Article/gate3_09_dupage_2015/candidates/SOURCE_QUALIFICATION.md) |
| GSE114298, GSE39595, E-MTAB-6156, GSE79339, GSE121838 / DuPage | Literature/reuse leads and co-stimulation references; not new independent validation cohorts. | [evidence](../Research%20Article/gate3_09_dupage_2015/LITERATURE_CONTEXT.md) |
| GSE322520 / A3 pulse-versus-continuous IL4 | Access hold at the recorded review: author repository has scripts, no count payload; accessible counts, treatment/harvest and preparation identities remain required. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A3_SOURCE_FOLLOWTHROUGH_V2.md) |
| GSE247938 / A3; GSE247946 parent | ATAC normalized bigWigs and umbrella links inspected; no new ATAC count analysis or automatic RNA/ATAC pairing. RNA source GSE247943 has the bounded use listed above. | [evidence](research_reviews/2026-11-03-tool-assisted-screening-review/A3_SOURCE_FOLLOWTHROUGH_V2.md) |
| GSE328925 / A3 | Publication/deposit access discrepancy remains a recorded source hold; no public-data numerical reproduction claimed. | [evidence](research_reviews/2026-11-03-primary-candidate-literature/SOURCE_READS_AND_HOLDS.md) |
| GSE232628, GSE263817 / Niethamer V1 | Planned human myeloid transport qualification; source-defined donor/state mapping required. No V1 execution inferred. | [evidence](../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) |
| GSE292440, GSE277256, GSE277226, GSE300399 / Niethamer D1 | External lung-Treg leads; D1 remains unrun/gated. Recorded refresh timeouts do not prove public data absence. | [evidence](../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) |
| GSE287581 / Treg ablation | Reading/source lead awaiting comparison-specific cell, condition and unit qualification; no numerical run in this register. | [evidence](portfolio_extensions/2026-10-07/SOURCE_ONLY_REVIEW.md) |
| GSE335257 / HSC training; BioProject 984020 / CD8 nutrient–chromatin study | Unqualified cross-context leads; assay/sample mapping and primary methods remain required. | [evidence](portfolio_extensions/2026-10-07/SOURCE_ONLY_REVIEW.md) |
| GSE227136, GSE264151, GSE264162, GSE341505 / A21 | Published endothelial-context leads; not a new joined adult-lung Fzd4 functional dataset or numerical reuse. | [evidence](research_reviews/2026-11-03-full-priority-screening/A21_SOURCE_REFRESH.md) |
| GSE290806 / A25 | Cerebellar microglial literature/source lead; not an additional normal-aging replication. | [evidence](portfolio_extensions/2026-10-07/g3_immune/A25_CONTEXT.md) |
| GSE260769 / Nb5 sensory-response candidate | Candidate source; source/assay and biological-unit qualification remains required. | [evidence](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/rq_derivation/SOURCES.md) |
| GSE167207 / Nb4 TBX5 | Fetal-lung ChIP reference; not qualified adult pericyte anatomy/function evidence. | [evidence](research_dossiers/packages_2026-10-03/SOURCES.md) |
| GSE70866, GSE70867, GSE286182 / Yd1 | Inspected spatial/BAL or cited study context, not a new donor-qualified external count contrast. | [evidence](../Research%20Article/gate2_W3_yadav_2025/SPATIAL_CONTEXT_AUDIT.md) |
| GSE154692 / Yd1 | Aortic-study marker convention reference, not lung-context validation. | [evidence](../Research%20Article/gate2_W3_yadav_2025/ANNOTATION_STRATEGY.md) |
| GSE97053, GSE158201, GSE36473 / Nb3–A22 | Expression/chromatin or tumor-context sources; no new linked epithelial-identity/functional response comparison admitted. | [evidence](../RQ_Specified/A22_epithelial_identity_niche_response/SOURCES.md) |
| GSE222901, GSE300293, GSE307529 / IL1 review branch | Metadata/design or WES crosswalk sources; not completed expression analyses. | [evidence](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| GSE247271, GSE264098 / Hassan | Companion ChIP/source locators; not used in the deposited multiome analysis listed above. | [evidence](../Research%20Article/gate1_02_choi_2020/datp_epigenetics/README.md) |

## Recorded screens and search candidates

The tables below centralize previously scattered screening records. Decisions
remain attached to the named screen and its date. A search result or a title-level
rule failure is not a full matrix inspection. A later use elsewhere in this page
does not erase the earlier screen or make the two comparisons equivalent.

### Saxton interaction-source screens, 8 November

Both requested interaction contrasts remain held. The GSE146438 common-matrix
route failed qualification because repeated controls disagreed and abundance
cells were invalid/non-numeric; the narrower reported-estimate use above is a
separate amended endpoint. The following candidates did not qualify for the
specified interactions. Inspection depth is retained in each recorded reason.

**Sx10 engineered IL10 × IL18** — [current result](../Research%20Article/ungated_saxton_2021_il10/extensions_20261108/RESULTS.md); [frozen source screen](../analysis/research/runs/sx10_coinput_qualification_v2/source_candidates.csv).

| Source | Recorded comparison-specific disposition |
|---|---|
| GSE248984 | Not qualified: mouse infection/genetic-background CD11c-enriched comparison; no engineered IL-10 by IL-18 intervention in full SOFT. |
| GSE162791 | Not qualified: pancreatic primary/metastatic tumor comparison; IL10 and IL18 biological context is not a controlled engineered-ligand co-input experiment. |

**Sx22 epithelial B3/WT × IFN priming** — [current result](../Research%20Article/gate3_08_saxton_2021_il22/priming_extension_20261108/RESULTS.md); [frozen source screen](../analysis/research/runs/sx22_priming_qualification_v2/source_candidates.csv).

| Source | Recorded comparison-specific disposition |
|---|---|
| GSE232204 | Not qualified from inspected summary/sample titles: Delayed engagement of host defenses enables SARS-CoV-2 viremia and productive infection of distal organs; no documented epithelial B3-by-IFN priming comparison. |
| GSE307670 | SuperSeries for the stromal study; not an independent cohort of its RNA/ATAC subseries. No qualified epithelial B3-by-priming design. |
| GSE307635 | Ccd18-Co fibroblast cytokine panels; single IFNA and IL22 labels do not form B3-by-priming arms. RNA and ATAC are distinct assays; full RNA SOFT verifies fibroblast identity. |
| GSE307526 | Ccd18-Co fibroblast cytokine panels; single IFNA and IL22 labels do not form B3-by-priming arms. RNA and ATAC are distinct assays; full RNA SOFT verifies fibroblast identity. |
| GSE277730 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cell in lupus [Time_coure_RNAseq]; no documented epithelial B3-by-IFN priming comparison. |
| GSE252917 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cells in lupus [JUN IFN]; no documented epithelial B3-by-IFN priming comparison. |
| GSE233050 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cells in lupus; no documented epithelial B3-by-IFN priming comparison. |
| GSE233048 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cells in lupus [JUN OE]; no documented epithelial B3-by-IFN priming comparison. |
| GSE233047 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cells in lupus [JUN AHR modulation]; no documented epithelial B3-by-IFN priming comparison. |
| GSE233045 | Not qualified from inspected summary/sample titles: Interferon subverts an AHR-JUN axis to promote CXCL13+ T cells in lupus [AHR]; no documented epithelial B3-by-IFN priming comparison. |
| GSE214633 | Full SOFT: mouse PBMC cytokine atlas with pooling/hashtag libraries; IL18_IL22 library labels are not the requested epithelial B3-by-IFN design. |
| GSE161938 | Not qualified from inspected summary/sample titles: Clonotypic analysis of protective influenza M2e-specific lung resident T helper memory cells reveals extensive functional plasticity; no documented epithelial B3-by-IFN priming comparison. |
| GSE89610 | Full SOFT: Huh7.5 individual-cytokine/time comparisons; no B3 or documented IFNA-then-IL22 factorial challenge. Shared generic IL27 protocol text also limits exact arm interpretation. |
| GSE65231 | Not qualified from inspected summary/sample titles: Genome wide host gene expression analysis in chicken lungs infected with avian influenza viruses; no documented epithelial B3-by-IFN priming comparison. |
| GSE31652 | Not qualified from inspected summary/sample titles: IL-17A is an essential cytokine to sustain pathogenic cell activation and inflammatory gene circuits in psoriasis vulgaris; no documented epithelial B3-by-IFN priming comparison. |
| GSE160217 | Existing Saxton source: PBS/WT/B3 acute colon RNA, but no IFN-priming arm. Same source, not new replication. |

### Wp E5 nutrient-contrast screen

[Assessment and R1–R6 rules](../Research%20Article/gate2_W2_wagner_Th17_PGAM/E5_RESULTS.md); [frozen candidate records](../analysis/research/runs/wp_e5_external_screen_v1/candidates.csv). 114 candidates: 64 rule failures and 50 requiring record inspection. None was admitted as independent validation by this screen.

<details>
<summary>64 candidates rejected by recorded screening rules</summary>

| Source | Deposited title at screen | Recorded rule failure / next step |
|---|---|---|
| [GSE332623](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE332623) | Immunological Differences in Atopic Dermatitis Across Age Groups: Insights from Single-Cell Multi-Omics | R2_no_nutrient_contrast_in_record |
| [GSE317764](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317764) | High-Fat Diet Causes Rapid Loss of Intestinal Group 3 Innate Lymphoid Cells Through Microbiota-Driven Inflammation | R1_no_th17_evidence_in_record |
| [GSE284562](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284562) | Transport stress induces immune dysregulation and exacerbates Mycobacterium tuberculosis infection in mice | R2_no_nutrient_contrast_in_record |
| [GSE289733](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289733) | Single-cell RNA-seq from Th17 cells differentiated in vitro under pathogenic (Th17p) and non-pathogenic (Th17n) conditions with high (25mM) or low (1mM) glucose media concentration | R6_own_deposit |
| [GSE218081](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE218081) | DC vaccines loaded with glioma killed by photodynamic therapy induce Th17 anti-tumor immunity and provide a 4-gene signature for glioma prognosis | R2_no_nutrient_contrast_in_record |
| [GSE206311](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE206311) | Gene expression in human keratinocytes from psoriatic skin (directly into the lesion or in area without lesion) or healthy person (control) used for human tissue-engineered skin substitutes and co-cultured with T-lymphocyte | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE163572](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163572) | Targeting In Vivo Metabolic Vulnerabilities of Th2 and Th17 Cells Reduces Airway Inflammation | R4_fewer_than_four_samples |
| [GSE42914](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42914) | Gene expression profiling for 2 cell samples | R2_no_nutrient_contrast_in_record;R4_fewer_than_four_samples |
| [GSE11924](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE11924) | Gene expression in TFH cells | R2_no_nutrient_contrast_in_record |
| [GSE277138](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277138) | Nonvesicular sterol transport is a metabolic immune checkpoint that guards dietary lipid uptake (scRNA-Seq) | R4_fewer_than_four_samples |
| [GSE175494](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE175494) | RNA-seq of in vitro differeentiated Th subsets and IL-27+TGF-β-treated CD4+ T cells | R1_no_th17_evidence_in_record |
| [GSE318366](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318366) | Localized fever mimicry within lymph node potentiates cancer vaccine efficacy | R2_no_nutrient_contrast_in_record |
| [GSE312091](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE312091) | RNA-seq of TCR-stimulated CD4⁺ T cells from SKG mice treated with the Nr4a1 agonist Cytosporone B | R2_no_nutrient_contrast_in_record;R4_fewer_than_four_samples |
| [GSE297075](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE297075) | Integration of Phospho-Signaling and Transcriptomics in Single Cells Reveals Distinct Th17 Cell Fates | R2_no_nutrient_contrast_in_record;R4_fewer_than_four_samples |
| [GSE290467](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290467) | Functional Targeting of ILC2s and ILC3s reveals selective roles in intestinal fibrosis and homeostasis. | R2_no_nutrient_contrast_in_record;R4_fewer_than_four_samples |
| [GSE277028](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277028) | Secretory IgA binding to FCRL3 triggers shared inflammatory cytokine secretion by human regulatory T cells and effector T cells | R2_no_nutrient_contrast_in_record |
| [GSE243323](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243323) | Subset-specific mitochondrial and DNA damage shapes T cell responses to fever and inflammation | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE243064](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243064) | RORA proximal enhancer regulates its expression during early human Th17 cell differentiation | R2_no_nutrient_contrast_in_record |
| [GSE242000](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE242000) | Selective requirement of 3D genomic organization for the Mdm1-Il22-Ifng locus regulation in initial Th1 cell lineage specification and differentiation [ATAC-Seq] | R2_no_nutrient_contrast_in_record |
| [GSE215181](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215181) | Selective requirement of 3D genomic organization for the Mdm1-Il22-Ifng locus regulation in initial Th1 cell lineage specification and differentiation | R2_no_nutrient_contrast_in_record |
| [GSE215178](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215178) | Selective requirement of 3D genomic organization for the Mdm1-Il22-Ifng locus regulation in initial Th1 cell lineage specification and differentiation | R2_no_nutrient_contrast_in_record |
| [GSE211389](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE211389) | Multi-scale epigenomic priming of inflammatory genes enables rapid recall in human memory T helper cells | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE234594](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE234594) | Autoimmunity and infection give rise to distict inflammatory Th17 subsets | R2_no_nutrient_contrast_in_record |
| [GSE234593](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE234593) | Autoimmunity and infection give rise to distict inflammatory Th17 subsets [bulk RNA-seq] | R2_no_nutrient_contrast_in_record |
| [GSE196904](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE196904) | The impact of G9a-inhibitors in T-cell and Treg differentiation | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE196903](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE196903) | The impact of G9a-inhibitors in T-cell and Treg differentiation [ATAC-seq] | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE192473](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE192473) | The EMT-regulator ZEB1 shapes bone marrow immunological niches in AML suppressing T-cell activity and fostering Th17 expansion | R2_no_nutrient_contrast_in_record |
| [GSE146253](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE146253) | Targeting HDAC6-Mediated Deacetylation of STAT4 Is Critical for T helper Type 1 Cell Differentiation and Capability | R1_no_th17_evidence_in_record |
| [GSE163342](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163342) | RORa enforces stability of the T-helper-17 cell effector program | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE163341](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163341) | RORa enforces stability of the T-helper-17 cell effector program (ChIP-Seq (2)) | R2_no_nutrient_contrast_in_record |
| [GSE163340](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163340) | RORa enforces stability of the T-helper-17 cell effector program (ATAC-Seq) | R2_no_nutrient_contrast_in_record |
| [GSE163339](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE163339) | RORa enforces stability of the T-helper-17 cell effector program (ChIP-Seq) | R2_no_nutrient_contrast_in_record |
| [GSE207603](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207603) | An LKB1-mitochondria axis controls Th17 effector function | R2_no_nutrient_contrast_in_record |
| [GSE183918](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183918) | Chromatin accessibility analysis of MIAT sufficient and MIAT deficient Th17 cells by ATAC-seq | R2_no_nutrient_contrast_in_record |
| [GSE183664](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183664) | Long Intergenic Noncoding RNA MIAT Contributes to Human Th17 Cell Differentiation | R2_no_nutrient_contrast_in_record |
| [GSE176065](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE176065) | Global gene-regulatory targets and Genome-wide binding sites of FOSL1, FOSL2 and BATF in human Th17 cells | R2_no_nutrient_contrast_in_record |
| [GSE174810](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174810) | Genome-wide binding sites of FOSL1, FOSL2 and BATF in human Th17 cells [ChIP-seq] | R2_no_nutrient_contrast_in_record |
| [GSE174809](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174809) | Global gene-regulatory targets of FOSL1, FOSL2 and BATF in human Th17 cells [RNA-seq] | R2_no_nutrient_contrast_in_record |
| [GSE154467](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE154467) | Time-course transcriptome analysis of in vitro differentiated Th17 cells from wild-type C57BL/6 mice | R2_no_nutrient_contrast_in_record |
| [GSE157598](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE157598) | Polyamine metabolism regulates the T cell epigenome through hypusination | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE157597](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE157597) | Polyamine metabolism regulates the T cell epigenome through hypusination [ATAC-seq] | R2_no_nutrient_contrast_in_record |
| [GSE157596](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE157596) | Polyamine metabolism regulates the T cell epigenome through hypusination [RNA-seq] | R2_no_nutrient_contrast_in_record |
| [GSE171186](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171186) | BMI1 Maintains the Regulatory T cell Epigenomic Landscape to Prevent Inflammatory Bowel Disease (Human ATAC-Seq) | R4_fewer_than_four_samples |
| [GSE115103](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115103) | The CD4+ alike CD8+ memory T cell compartment diversification reveales CD8+ T cell subsets with cytotoxic and non-cytotoxic properties | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |
| [GSE148669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE148669) | Sodium chloride generates anti-inflammatory Th17 cell responses but amplifies Th17 cell pathogenicity in pro-inflammatory cytokine microenvironments | R2_no_nutrient_contrast_in_record |
| [GSE118094](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE118094) | Cancerous inhibitor of PP2A (CIP2A) Constrains Th17 Differentiation by Modulating STAT3 Signaling | R2_no_nutrient_contrast_in_record |
| [GSE133426](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE133426) | Human memory Th17 cell populations change into anti-inflammatory cells with regulatory capacity upon exposure to active Vitamin D | R2_no_nutrient_contrast_in_record |
| [GSE118974](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE118974) | Quantitative mass spectrometry-based proteomics reveals the dynamic protein landscape during initiation of human Th17 cell polarization | R2_no_nutrient_contrast_in_record |
| [GSE122210](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122210) | An AKBA derivative (CKBA) regulates mRNA expression of naive mouse CD4+ T cells in vitro under TH17-polarizing conditions | R2_no_nutrient_contrast_in_record |
| [GSE110097](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110097) | Analysis of Th17 gene signature in the presence of CD28 costimulation in human CD4 naïve T cells | R2_no_nutrient_contrast_in_record |
| [GSE98414](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE98414) | Role of JunB in Th17 cell effector stability | R2_no_nutrient_contrast_in_record |
| [GSE98413](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE98413) | Role of JunB in Th17 cell effector stability [RNA-seq] | R2_no_nutrient_contrast_in_record |
| [GSE98412](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE98412) | Role of JunB in Th17 cell effector stability [ChIP-seq] | R2_no_nutrient_contrast_in_record |
| [GSE312949](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE312949) | CQMUH-011 mitigated LPS-induced acute lung injury in neonatal rabbits | R1_no_th17_evidence_in_record |
| [GSE306976](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE306976) | Divergent CNS–Peripheral Signaling Reflects Astrocyte Dysfunction and Contributes to Insulin Resistance in Early Aβ Pathology | R2_no_nutrient_contrast_in_record |
| [GSE295290](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295290) | Id2 acts as a metabolic checkpoint underpinning Th17 cell fate decision [scRNA-seq] | R2_no_nutrient_contrast_in_record;R4_fewer_than_four_samples |
| [GSE295289](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295289) | Id2 acts as a metabolic checkpoint underpinning Th17 cell fate decision [CUT&Tag] | R2_no_nutrient_contrast_in_record |
| [GSE295288](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295288) | Id2 acts as a metabolic checkpoint underpinning Th17 cell fate decision [RNA-seq] | R2_no_nutrient_contrast_in_record |
| [GSE269846](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269846) | Phosphoglycerate mutase regulates Treg differentiation through control of serine synthesis and one-carbon metabolism | R2_no_nutrient_contrast_in_record |
| [GSE129489](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129489) | Pro-survival Lipid Sphingosine-1-Phosphate Metabolically Reprograms T cell to Limit its Anti-Tumor Activity | R1_no_th17_evidence_in_record |
| [GSE207265](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207265) | Transcriptional programing of helper T cell metabolism by the IL-2-STAT5 axis | R1_no_th17_evidence_in_record |
| [GSE176235](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE176235) | Foxp3-dependent and -independent functions of peripherally-induced Treg cells [08075] | R2_no_nutrient_contrast_in_record |
| [GSE48978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE48978) | Comparison of RNA-Seq and Microarray in Transcriptome Profiling During T Cell Activation | R2_no_nutrient_contrast_in_record |
| [GSE143322](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE143322) | Methionine metabolism shapes T helper cell responses through regulation of epigenetic reprogramming | R1_no_th17_evidence_in_record;R2_no_nutrient_contrast_in_record |

</details>

<details>
<summary>50 candidates pending record inspection</summary>

| Source | Deposited title at screen | Recorded rule failure / next step |
|---|---|---|
| [GSE337240](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE337240) | GDP-Driven purine metabolic rewiring promotes Th17-like polarization of CD4⁺ T cells and reveals a RANBP1-associated nucleo-metabolic program | Full record/sample inspection required; no admitted contrast |
| [GSE334206](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE334206) | STK25 m6A modification regulates CD4+ T cell glycolysis mediated immune imbalance in systemic lupus erythematosus | Full record/sample inspection required; no admitted contrast |
| [GSE314698](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE314698) | Pancreatic volume and immunological biomarkers predict checkpoint inhibitor-associated autoimmune diabetes in humans. | Full record/sample inspection required; no admitted contrast |
| [GSE275152](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE275152) | GLUT1 overexpression in CAR-T cells induces metabolic reprogramming and enhances potency | Full record/sample inspection required; no admitted contrast |
| [GSE241099](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE241099) | The lysine acetyltransferase KAT6A epigenetically facilitates glucose metabolic programming and CD4+ T-cell responses in autoimmunity | Full record/sample inspection required; no admitted contrast |
| [GSE222881](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE222881) | Pyruvate dehydrogenase fuels a critical citrate pool that is essential for Th17 cell effector functions (RNA-Seq II) | Full record/sample inspection required; no admitted contrast |
| [GSE222880](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE222880) | Pyruvate dehydrogenase fuels a critical citrate pool that is essential for Th17 cell effector functions (RNA-Seq I) | Full record/sample inspection required; no admitted contrast |
| [GSE222878](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE222878) | Pyruvate dehydrogenase fuels a critical citrate pool that is essential for Th17 cell effector functions (ATAC-Seq) | Full record/sample inspection required; no admitted contrast |
| [GSE185478](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE185478) | OXPHOS Promotes Apoptotic Resistance and Persistence in T­H17 cells | Full record/sample inspection required; no admitted contrast |
| [GSE127768](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127768) | Inhibition of glycolysis in pathogenic TH17 cells through targeting a miR-21-Peli1-c-Rel pathway prevents autoimmunity | Full record/sample inspection required; no admitted contrast |
| [GSE129028](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129028) | Glycosylation-dependent modulation of the IL-2 signaling axis determines Th17 differentiation and IL-10 production | Full record/sample inspection required; no admitted contrast |
| [GSE128008](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE128008) | Histone H3K27 demethylases regulate human Th17 cell maturation and effector functions by impacting on metabolism [III] | Full record/sample inspection required; no admitted contrast |
| [GSE127766](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127766) | Histone H3K27 demethylases regulate human Th17 cell maturation and effector functions by impacting on metabolism [II] | Full record/sample inspection required; no admitted contrast |
| [GSE126991](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE126991) | Histone H3K27 demethylases regulate human Th17 cell maturation and effector functions by impacting on metabolism [I] | Full record/sample inspection required; no admitted contrast |
| [GSE335775](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE335775) | Single-cell RNA sequencing reveals endothelial STING-dependent immune remodeling in murine metabolic dysfunction-associated steatohepatitis | Full record/sample inspection required; no admitted contrast |
| [GSE277067](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277067) | T cell cholesterol transport links intestinal immune responses to dietary lipid absorption | Full record/sample inspection required; no admitted contrast |
| [GSE166430](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE166430) | Expression data from TH17 cells cultured in the presence or absence of glutamine | Full record/sample inspection required; no admitted contrast |
| [GSE207602](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207602) | An LKB1-mitochondria axis controls Th17 effector function [ATAC-Seq] | Full record/sample inspection required; no admitted contrast |
| [GSE207601](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207601) | An LKB1-mitochondria axis controls Th17 effector function [RNA-Seq 2] | Full record/sample inspection required; no admitted contrast |
| [GSE156742](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE156742) | An LKB1-mitochondria axis controls Th17 effector function [RNA-Seq 1] | Full record/sample inspection required; no admitted contrast |
| [GSE143321](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE143321) | Methionine metabolism shapes T helper cell responses through regulation of epigenetic reprogramming [ChIP-Seq] | Full record/sample inspection required; no admitted contrast |
| [GSE143320](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE143320) | Methionine metabolism shapes T helper cell responses through regulation of epigenetic reprogramming [RNA-Seq] | Full record/sample inspection required; no admitted contrast |
| [GSE144813](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144813) | Exosomal Transfer of Mitochondria Reprograms T Helper Cell Function In Chronic Airway Inflammation | Full record/sample inspection required; no admitted contrast |
| [GSE291839](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291839) | Impact of RORgt in regulating CD4 T cells primed under Th17 conditions | Full record/sample inspection required; no admitted contrast |
| [GSE285363](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE285363) | Effects of NorUDCA on the Transcriptomic Landscape of Differentiating Murine Pathogenic Th17 Cells In Vitro | Full record/sample inspection required; no admitted contrast |
| [GSE240979](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240979) | Deciphering the role of IRF4 and its interacting proteins in differentiated regulatory and T helper 17 cells | Full record/sample inspection required; no admitted contrast |
| [GSE241823](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE241823) | Effect of androgen receptor signaling on H3K27 trimethylation in Th17 cells | Full record/sample inspection required; no admitted contrast |
| [GSE243062](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243062) | RORA proximal enhancer regulates its expression during early human Th17 cell differentiation [ChIP] | Full record/sample inspection required; no admitted contrast |
| [GSE243058](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243058) | RORA proximal enhancer regulates its expression during early human Th17 cell differentiation [ATAC] | Full record/sample inspection required; no admitted contrast |
| [GSE175470](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE175470) | Soluble adenylyl cyclase induces type 17 inflammation and is a potential therapeutic target in psoriasis | Full record/sample inspection required; no admitted contrast |
| [GSE171188](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE171188) | BMI1 Maintains the Regulatory T cell Epigenomic Landscape to Prevent Inflammatory Bowel Disease (ChIP-Seq) | Full record/sample inspection required; no admitted contrast |
| [GSE137229](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE137229) | Body fluid from the parasitic worm Ascaris suum inhibits broad-acting pro-inflammatory programs in dendritic cells | Full record/sample inspection required; no admitted contrast |
| [GSE112244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112244) | Th1 and T17 activation with and without CB839 treatment | Full record/sample inspection required; no admitted contrast |
| [GSE102045](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE102045) | G-Protein-Coupled Receptor 68 Negatively Regulates IL-22 Production in Human Th17 Cells | Full record/sample inspection required; no admitted contrast |
| [GSE307907](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307907) | A Human RORγt Mutant Enhances Th17-Mediated Inflammation via Increased HIF-1α Recruitment | Full record/sample inspection required; no admitted contrast |
| [GSE303700](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303700) | Autoimmune Disease Risk Gene ANKRD55 Promotes Th17 Effector Function Through Metabolic Modulation [ATAC-Seq] | Full record/sample inspection required; no admitted contrast |
| [GSE303699](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303699) | Autoimmune Disease Risk Gene ANKRD55 Promotes Th17 Effector Function Through Metabolic Modulation [RNA-Seq] | Full record/sample inspection required; no admitted contrast |
| [GSE164959](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164959) | Glycolysis Promotes Phosphoinositide 3-Kinase Signaling In Support of T Helper 17 Cell-Mediated Autoimmunity | Full record/sample inspection required; no admitted contrast |
| [GSE310711](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310711) | Bifidobacteria infantis and human milk oligosaccharides have independent effects on immune response and amino acid metabolism in germ-free mouse models | Full record/sample inspection required; no admitted contrast |
| [GSE190131](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190131) | In vivo CRISPR screening in autoimmune disease model reveals differential dependence of Th1 and Th17 cells on amino acid transporter SNAT1 | Full record/sample inspection required; no admitted contrast |
| [GSE237555](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237555) | Boosting NAD preferentially blunts TH17 inflammation via arginine biosynthesis and redox regulatory control in control and psoriasis subjects [NR or placebo] | Full record/sample inspection required; no admitted contrast |
| [GSE237552](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237552) | Boosting NAD preferentially blunts TH17 inflammation via arginine biosynthesis and redox regulatory control in control and psoriasis subjects [healthy or psoriasis] | Full record/sample inspection required; no admitted contrast |
| [GSE135428](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135428) | Physiomimetic model of the human Gut-Liver axis for studies of inflammatory diseases | Full record/sample inspection required; no admitted contrast |
| [GSE145007](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145007) | Single residue in CD28-costimulated CAR-T cells limits long-term persistence and antitumor durability | Full record/sample inspection required; no admitted contrast |
| [GSE15624](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE15624) | Regulation of T cell gene expression by Halofuginone (HF) | Full record/sample inspection required; no admitted contrast |
| [GSE290580](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE290580) | Restriction of innate Tgd17 cell plasticity by an AP-1 regulatory axis [CUT&Run] | Full record/sample inspection required; no admitted contrast |
| [GSE252771](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252771) | Persistent dysfunction of Th17 cells in people with HIV on ART and in elite controllers | Full record/sample inspection required; no admitted contrast |
| [GSE243096](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243096) | HELIOS identifies an HLA-E-restricted CD8 T cell population and is associated with low effector functions. | Full record/sample inspection required; no admitted contrast |
| [GSE174521](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174521) | Aire+ Cell Depletioin Results in Expansion of Activated T Cells in Pregnant Mice | Full record/sample inspection required; no admitted contrast |
| [GSE147045](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147045) | IL-17A Promotes HIV-1 Dissemination/Replication and abrogates the Interferon-Mediated Antiviral Immunity in Intestinal Epithelial Cells | Full record/sample inspection required; no admitted contrast |

</details>

### Register-wide search return, 27 September

[Original query return](audits/2026-09-27-register-gate-audit/candidates.tsv). These 102 question–source rows contain 97 distinct source identifiers. The gate column states the question’s missing comparison, not proof that each returned study was fully inspected or individually rejected. Later inspected/use decisions above take precedence for their stated comparison.

<details>
<summary>102 search-return rows with question and unresolved gate</summary>

| Source | Question | Title at search | Question-level gate; individual eligibility unestablished |
|---|---|---|---|
| [GSE293600](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE293600) | A1 | The Polycomb Protein EED Constrains the SCLC Neuroendocrine Phenotype and Drives Lung Cancer Histological Transformation [ATAC-seq] | matched replicated regulation-to-fate linkage remains missing |
| [GSE268368](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE268368) | A1 | Alterations in Monocyte Reprogramming and Ontogeny Enhance Lipopolysaccharide-Induced Lung Injury in Sepsis Survivor Mice [ATAC-Seq] | matched replicated regulation-to-fate linkage remains missing |
| [GSE310084](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310084) | A1 | Runx1 Promotes Myofibroblast Cell Fate during Development and Fibrosis | matched replicated regulation-to-fate linkage remains missing |
| [GSE286986](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286986) | A1 | Single-cell Multiomics Analysis Reveals CTCF as a Key Regulator of Lung Morphogenesis and Progenitor Maintenance | matched replicated regulation-to-fate linkage remains missing |
| [GSE286984](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286984) | A1 | Single-cell Multiomics Analysis Reveals CTCF as a Key Regulator of Lung Morphogenesis and Progenitor Maintenance | matched replicated regulation-to-fate linkage remains missing |
| [GSE261082](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261082) | A1 | Mouse lung injury-repair induces Ntrk2-tk in CAP1 endothelial cells (scRNA-Seq) | matched replicated regulation-to-fate linkage remains missing |
| [GSE303646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303646) | A3 | Single-cell RNA-seq of Lung Regeneration in Young and Aged Mice After Injury | age-matched controls and comparable sampling needed |
| [GSE271578](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271578) | A3 | Kinetical scRNAseq Analysis Reveals Immune Mechanisms Underlying Hindered Lung Recovery following Influenza Virus Infection in Aged Hosts | age-matched controls and comparable sampling needed |
| [GSE288730](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE288730) | A3 | Organism-wide cellular dynamics and epigenomic remodeling in mammalian aging | age-matched controls and comparable sampling needed |
| [GSE274828](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE274828) | A3 | Impact of aging on pulmonary cellular responses during mechanical ventilation | age-matched controls and comparable sampling needed |
| [GSE277799](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277799) | A3 | An ageing bone marrow exacerbates lung fibrosis via a dysregulated regulatory T cell driven axis, fuelling profibrotic macrophage persistence | age-matched controls and comparable sampling needed |
| [GSE225166](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE225166) | A3 | Predicting age in single cells and low coverage DNA methylation data [RRBS] | age-matched controls and comparable sampling needed |
| [GSE311141](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE311141) | A3 | Molecular Mechanism of Oncostatin M-Mediated Bronchopulmonary Dysplasia Induced by Intrauterine Inflammation [scRNA-seq] | age-matched controls and comparable sampling needed |
| [GSE310065](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310065) | A3 | Molecular Mechanism of Oncostatin M-Mediated Bronchopulmonary Dysplasia Induced by Intrauterine Inflammation | age-matched controls and comparable sampling needed |
| [GSE303646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303646) | A3 | Single-cell RNA-seq of Lung Regeneration in Young and Aged Mice After Injury | age-matched controls and comparable sampling needed |
| [GSE295628](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295628) | A3 | Miconazole attenuates  LPS-induced lung inflammation by modulating alveolar macrophage polarization  through the regulation of lipid metabolism | age-matched controls and comparable sampling needed |
| [GSE271578](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271578) | A3 | Kinetical scRNAseq Analysis Reveals Immune Mechanisms Underlying Hindered Lung Recovery following Influenza Virus Infection in Aged Hosts | age-matched controls and comparable sampling needed |
| [GSE312462](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE312462) | A3 | Influenza hijacks circulating myeloid cells to inflict Type-I Interferon-fueled damage in the heart | age-matched controls and comparable sampling needed |
| [GSE190934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190934) | A4 | Recombinant FGF10-induced de novo alveologenesis in neonatal mice after hyperoxia exposure is associated with enhanced AT2’s resident mesenchymal cell niche activity | measured activity/history and lineage-linked response needed |
| [GSE162859](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162859) | A4 | Alveolar organoid model | measured activity/history and lineage-linked response needed |
| [GSE147358](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE147358) | A4 | Fragmentation of Small-cell Lung Cancer Regulatory States in Heterotypic Microenvironments | measured activity/history and lineage-linked response needed |
| [GSE97055](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE97055) | A4 | Regeneration of the lung alveolus by an evolutionarily conserved epithelial progenitor. | measured activity/history and lineage-linked response needed |
| [GSE97052](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE97052) | A4 | Regeneration of the lung alveolus by an evolutionarily conserved epithelial progenitor [ATAC-seq] | measured activity/history and lineage-linked response needed |
| [GSE92699](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92699) | A4 | Distinct mesenchymal lineages and niches promote epithelial self-renewal and myofibrogenesis in the lung | measured activity/history and lineage-linked response needed |
| [GSE247505](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247505) | A4 | Sustained NF-kB activation allows mutant alveolar stem cells to co-opt a regeneration program for tumor initiation | measured activity/history and lineage-linked response needed |
| [GSE247504](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247504) | A4 | Sustained NF-kB activation allows mutant alveolar stem cells to co-opt a regeneration program for tumor initiation [Expt2] | measured activity/history and lineage-linked response needed |
| [GSE247503](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247503) | A4 | Sustained NF-kB activation allows mutant alveolar stem cells to co-opt a regeneration program for tumor initiation [Expt1] | measured activity/history and lineage-linked response needed |
| [GSE145031](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145031) | A4 | Inflammatory Signals induce AT2 Cell-Derived Damage-Associated Transient Progenitors that Mediate Alveolar Regeneration | measured activity/history and lineage-linked response needed |
| [GSE144598](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144598) | A4 | Inflammatory Signals induce AT2 Cell-Derived Damage-Associated Transient Progenitors that Mediate Alveolar Regeneration | measured activity/history and lineage-linked response needed |
| [GSE144553](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE144553) | A4 | Inflammatory Signals induce AT2 Cell-Derived Damage-Associated Transient Progenitors that Mediate Alveolar Regeneration | measured activity/history and lineage-linked response needed |
| [GSE271578](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271578) | A5 | Kinetical scRNAseq Analysis Reveals Immune Mechanisms Underlying Hindered Lung Recovery following Influenza Virus Infection in Aged Hosts | needs another eligible adult-injury cohort for generality |
| [GSE264278](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264278) | A5 | TIme-cource single-cell RNA-seq analysis of bleomycin and LPS-induced lung injury and fibrosis | needs another eligible adult-injury cohort for generality |
| [GSE201698](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE201698) | A5 | Time-course cellular interactome analysis by single-cell RNA-seq in bleomycin-induced pulmonary fibrosis | needs another eligible adult-injury cohort for generality |
| [GSE141259](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE141259) | A5 | Longitudinal single-cell transcriptomics analysis of mouse lung upon bleomycin-induced injury | needs another eligible adult-injury cohort for generality |
| [GSE345596](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE345596) | A5 | Time-resolved single-cell RNA sequencing of mouse lungs during acute Pseudomonas aeruginosa pneumonia | needs another eligible adult-injury cohort for generality |
| [GSE313673](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE313673) | A5 | Prostaglandin I₂ Receptor Activation Promotes Alveolar Regeneration via the JUN/p53 Pathway [CUT&Tag] | needs another eligible adult-injury cohort for generality |
| [GSE313672](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE313672) | A5 | Prostaglandin I₂ Receptor Activation Promotes Alveolar Regeneration via the JUN/p53 Pathway [Multiome-seq] | needs another eligible adult-injury cohort for generality |
| [GSE313671](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE313671) | A5 | Prostaglandin I₂ Receptor Activation Promotes Alveolar Regeneration via the JUN/p53 Pathway [scRNA-seq] | needs another eligible adult-injury cohort for generality |
| [GSE304531](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304531) | A5 | Age-dependent immune responses and resident cell dynamics in young mice following pneumonia [RNA-Seq] | needs another eligible adult-injury cohort for generality |
| [GSE295484](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295484) | A5 | Age-dependent immune responses and resident cell dynamics in young mice following pneumonia | needs another eligible adult-injury cohort for generality |
| [GSE305107](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE305107) | A7 | Small activating RNA AW1-51 (CEBPA-51) elicits targeted DNA demethylation to promote gene activation [EPIC array] | replicated age-matched animals; current data is one well per condition |
| [GSE305099](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE305099) | A7 | Small activating RNA AW1-51 (CEBPA-51) elicits targeted DNA demethylation to promote gene activation [RNA-seq] | replicated age-matched animals; current data is one well per condition |
| [GSE245650](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245650) | A7 | The Heme-regulated transcriptional repressor, BACH1 safeguards macrophage enhancer selection, activation andtissue adaptation [Capture Hi-C] | replicated age-matched animals; current data is one well per condition |
| [GSE245649](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245649) | A7 | The Heme-regulated transcriptional repressor, BACH1 safeguards macrophage enhancer selection, activation andtissue adaptation [RNA-seq_muscle] | replicated age-matched animals; current data is one well per condition |
| [GSE245648](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245648) | A7 | The Heme-regulated transcriptional repressor, BACH1 safeguards macrophage enhancer selection, activation andtissue adaptation [RNA-seq_BMDM] | replicated age-matched animals; current data is one well per condition |
| [GSE245647](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245647) | A7 | The Heme-regulated transcriptional repressor, BACH1 safeguards macrophage enhancer selection, activation andtissue adaptation [ChIP-seq] | replicated age-matched animals; current data is one well per condition |
| [GSE284147](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE284147) | A7 | Establishing competence for trophectoderm specification in mouse embryos before the first lineage bifurcation | replicated age-matched animals; current data is one well per condition |
| [GSE278751](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278751) | A7 | A stem cell model identifies two alternative cell fates in CBFA2T3::GLIS2-driven acute megakaryoblastic leukemia initiation (Multiome scRNA-seq/scATAC-seq) | replicated age-matched animals; current data is one well per condition |
| [GSE277485](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277485) | A7 | A stem cell model identifies two alternative cell fates in CBFA2T3::GLIS2-driven acute megakaryoblastic leukemia initiation (scRNA-seq) | replicated age-matched animals; current data is one well per condition |
| [GSE277468](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE277468) | A7 | A stem cell model identifies two alternative cell fates in CBFA2T3::GLIS2-driven acute megakaryoblastic leukemia initiation (RNA-seq) | replicated age-matched animals; current data is one well per condition |
| [GSE276998](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE276998) | A7 | A stem cell model identifies two alternative cell fates in CBFA2T3::GLIS2-driven acute megakaryoblastic leukemia initiation (ATAC-seq) | replicated age-matched animals; current data is one well per condition |
| [GSE276996](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE276996) | A7 | A stem cell model identifies two alternative cell fates in CBFA2T3::GLIS2-driven acute megakaryoblastic leukemia initiation (ChIP-seq) | replicated age-matched animals; current data is one well per condition |
| [GSE261508](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261508) | A8 | Identification of mesenchymal cell populations during neonatal lung development and their regulation by Fgf18 | independent mature endpoints needed |
| [GSE215824](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE215824) | A8 | Alveolar epithelial progenitor cells drive lung regeneration via dynamic changes in chromatin topology modulated by lineage-specific Nkx2-1 activity | independent mature endpoints needed |
| [GSE73861](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73861) | A8 | Development and Plasticity of Alveolar Type 1 Cells | independent mature endpoints needed |
| [GSE318967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE318967) | A8 | Secreted Frizzled-Related Protein 1 Controls Distal Lung Formation via Wnt and PDGF Signaling | independent mature endpoints needed |
| [GSE27964](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE27964) | A8 | Age-dependent decline in lung regeneration with loss of clonogenicity and myofibroblastic differentiation of lung fibroblasts | independent mature endpoints needed |
| [GSE348037](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE348037) | A9 | TSPAN13 spatially organizes epidermal growth factor signaling to support divergent functional outcomes in senescence and cancer | RNA screen possible; protein/function data needed |
| [GSE330326](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE330326) | A9 | NAB2::STAT6 Fusion Proteins Drive Nuclear Condensate Formation and Transcriptional Reprogramming in Solitary Fibrous Tumors | RNA screen possible; protein/function data needed |
| [GSE324380](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324380) | A9 | scRNA-seq of fibroblasts from inducible Cdh11 reporter mice | RNA screen possible; protein/function data needed |
| [GSE294583](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294583) | A9 | Cold-inducible RNA-binding protein promotes lung fibroblast activation via TLR2/4-dependent IL-6 signaling: implications in pulmonary fibrosis | RNA screen possible; protein/function data needed |
| [GSE306080](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE306080) | A9 | Extracellular Vesicle Cargo from Lipofibroblasts Mitigates COPD by Alveolar Type II Cell Restoration | RNA screen possible; protein/function data needed |
| [GSE293962](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE293962) | A9 | STL1267 Inhibits Myofibroblast Differentiation in a TGFβ1-Driven Human Lung Fibroblast Model | RNA screen possible; protein/function data needed |
| [GSE348037](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE348037) | A9 | TSPAN13 spatially organizes epidermal growth factor signaling to support divergent functional outcomes in senescence and cancer | RNA screen possible; protein/function data needed |
| [GSE310335](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310335) | A9 | Early fibrotic niches establish tumour-permissive microenvironments | RNA screen possible; protein/function data needed |
| [GSE288758](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE288758) | A9 | Spatial dynamics of the tumor microenvironment associated with emerging resistance to targeted therapy in EGFR-mutated non–small cell lung cancer | RNA screen possible; protein/function data needed |
| [GSE130807](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE130807) | A9 | Activation of Epidermal Growth Factor Receptor Pathway in Slow-Flow Vascular Malformations | RNA screen possible; protein/function data needed |
| [GSE77764](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE77764) | A9 | Fibroblast growth factor receptor 3 overexpression mediates ALK inhibitor resistance in ALK-rearranged non-small cell lung cancer | RNA screen possible; protein/function data needed |
| [GSE106151](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106151) | A9 | Differential Gene Expression in Erlotinib-Treated Fibroblasts | RNA screen possible; protein/function data needed |
| [GSE312053](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE312053) | A11 | Bridge to transplant using a flow-adaptive extracorporeal total artificial lung system following bilateral pneumonectomy | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE214770](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214770) | A11 | An autonomous intrapulmonary inflammatory feedback response, mediated by surfactants, operates as an inherent viral defense mechanism: evidence from acute SARS-CoV-2 infection [Pseudovirus Infected Proximal Lung Organoid scRNA-seq] | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE214762](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214762) | A11 | An autonomous intrapulmonary inflammatory feedback response, mediated by surfactants, operates as an inherent viral defense mechanism: evidence from acute SARS-CoV-2 infection [Prox, Distal, and Whole Lung Organoid scRNA-seq] | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE214752](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214752) | A11 | An autonomous intrapulmonary inflammatory feedback response, mediated by surfactants, operates as an inherent viral defense mechanism: evidence from acute SARS-CoV-2 infection [Combined Proximal, Distal, and Whole Lung Organoid scRNA-seq] | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE214482](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214482) | A11 | An autonomous intrapulmonary inflammatory feedback response, mediated by surfactants, operates as an inherent viral defense mechanism: evidence from acute SARS-CoV-2 infection [bulk RNA-seq] | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE198864](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198864) | A11 | Human lungs show limited permissiveness for SARS-CoV-2 due to scarce ACE2 levels but virus-induced expansion of inflammatory macrophages | lack of a non-neoplastic injury comparator limits specificity claims |
| [GSE292495](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292495) | A12 | Macrophage-specific targeting of histone demethylases with small-molecule inhibitors suppresses inflammatory responses in vivo [CUT&Run] | conditional component model; activation unmeasured |
| [GSE292494](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292494) | A12 | Macrophage-specific targeting of histone demethylases with small-molecule inhibitors suppresses inflammatory responses in vivo [RNA-seq] | conditional component model; activation unmeasured |
| [GSE317298](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317298) | A12 | Multi-omics profiling reveals microenvironmental remodeling as a key driver of house dust mite-induced lung cancer progression | conditional component model; activation unmeasured |
| [GSE308855](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308855) | A12 | Multi-omics profiling reveals microenvironmental remodeling as a key driver of house dust mite-induced lung cancer progression | conditional component model; activation unmeasured |
| [GSE296097](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296097) | A12 | NF-κB-dependent redistribution of the GR cistrome recruits GR to inflammatory gene loci and correlates with reduced repression by glucocorticoid [GR_IkBaDN_ChIPseq] | conditional component model; activation unmeasured |
| [GSE296101](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296101) | A12 | NF-κB-dependent redistribution of the GR cistrome recruits GR to inflammatory gene loci and correlates with reduced repression by glucocorticoid [RNAP2_ChIPseq] | conditional component model; activation unmeasured |
| [GSE240911](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240911) | A13 | A single-cell gene expression analysis in an in vitro co-culture model containing fibroblast cells directly mixed with NMU-manipulated lung adenocarcinoma cells | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE276934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE276934) | A13 | Image-based spatial transcriptomics identifies molecular niche dysregulation associated with distal lung remodeling in pulmonary fibrosis [Visium] | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE149878](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE149878) | A13 | Persistent viral activity, cytokine storm and lung fibrosis in severe COVID-19 | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE292589](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292589) | A13 | Type I interferon–activated myeloid states are associated with less fibrotic stages in idiopathic pulmonary fibrosis | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE285246](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE285246) | A13 | Spatially resolved atlas of IPF fibroblastic foci identifies that PAK2 kinase activation is involved in fibrogenesis | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE264038](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264038) | A13 | WI-38 cell line as model for myofibroblast and lipofibroblast switch | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE233844](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE233844) | A13 | Single-cell profiling reveals immune aberrations in progressive idiopathic pulmonary fibrosis | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE136831](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136831) | A13 | IPF Cell Atlas | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE122960](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960) | A13 | Single-Cell Transcriptomic Analysis of Human Lung Reveals Complex Multicellular Changes During Pulmonary Fibrosis II | IPF has six and three complete triads, below the ten-unit joint-model floor |
| [GSE271370](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271370) | A14 | Spatial transcriptomics unveils the in situ cellular and molecular hallmarks of the lung in fatal COVID-19 | withdrawal and recipient-specific data needed |
| [GSE292589](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292589) | A14 | Type I interferon–activated myeloid states are associated with less fibrotic stages in idiopathic pulmonary fibrosis | withdrawal and recipient-specific data needed |
| [GSE331432](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE331432) | A14 | Characterizing Cellular Heterogeneity and Transcriptomic Features of Senotype Using Deep Graph Representation Learning | withdrawal and recipient-specific data needed |
| [GSE296682](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296682) | A14 | Single-cell transcriptomics of bronchoalveolar lavage reveals divergent macrophage subpopulations and trajectories in interstitial lung disease | withdrawal and recipient-specific data needed |
| [GSE317902](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317902) | A14 | Monocyte Subset Predicts Clinical Outcomes in Fibrotic Hypersensitivity Pneumonitis | withdrawal and recipient-specific data needed |
| [GSE295566](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295566) | A14 | Persistence of alveolar fibroblast-derived ADAMTS4+ cells during delayed resolution of pulmonary fibrosis | withdrawal and recipient-specific data needed |
| [GSE326497](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE326497) | A14 | DNA N6-methylation orchestrates the pathogenicity of Mucorales fungi | withdrawal and recipient-specific data needed |
| [GSE292712](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292712) | A14 | Fibroblast STAT3 activation drives organ-specific premetastatic niche formation | withdrawal and recipient-specific data needed |
| [GSE299635](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299635) | A14 | Metastatic site influences driver gene function in pancreatic cancer [[InVitro ATAC-Seq]] | withdrawal and recipient-specific data needed |
| [GSE245827](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245827) | A14 | Metastatic site influences driver gene function in pancreatic cancer | withdrawal and recipient-specific data needed |
| [GSE245822](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245822) | A14 | Metastatic site influences driver gene function in pancreatic cancer [RNA-seq] | withdrawal and recipient-specific data needed |
| [GSE245821](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245821) | A14 | Metastatic site influences driver gene function in pancreatic cancer [ATAC-seq] | withdrawal and recipient-specific data needed |

</details>

### G0 enrichment feasibility screen

[Original 16-source assessment](../Research%20Article/gate1_01_niethamer_2025/trials/g0_gsea_feasibility/g0_deposits.csv). Verdicts concern the requested enrichment contrast, not whether the source was used elsewhere. "Plausible" does not mean the proposed run executed.

<details>
<summary>16 inspected source/contrast verdicts</summary>

| Source | Asked by / contrast | Recorded verdict | Reason |
|---|---|---|---|
| GSE262927 | A3; proposals W1, S1; phase against phase within a compartment (myeloid, capillary, alveolar epithelium); days with three or more animals: 42 dpi, 90 dpi, 366 dpi | plausible | the only mouse deposit with animal-level replication; baseline (2 animals) stays a reference band; the two-animal active-repair days enter only as a pooled phase |
| GSE136831 | A2 (C48, C49); A3 in human fibrosis; IPF against control within a compartment (AT2 and transitional epithelium, fibroblasts, macrophages) | plausible | the largest donor-replicated contrast in reach; per-donor cell floor of trial E6 (50) applies |
| GSE135893 | A2, A3; proposal V1 names held-out human validation; IPF against control within a compartment, as the held-out replication of GSE136831 | plausible | second fibrosis cohort; a gene set that clears in GSE136831 and not here is not established |
| GSE131907 | A2 (C40); tumour against paired normal lung within the epithelial compartment | plausible | paired design; the raw UMI matrix is on disk although trials E1 and E1b read the deposited log2 TPM, so a pseudobulk trial must stream the raw file |
| GSE132771 | C42 (trial E4); bleomycin against untreated, collagen-producing cells | not admissible | two animals per arm: directions only, as E4 reported |
| GSE247505 | A4 (C136, C149); trial C3; any timed or genotype arm against another | not admissible | 10 libraries in 6 arms, at most 2 per arm; pooling arms across time or colour would break the design that makes the deposit a time course |
| GSE145031 | A5, trials D0 to D7; bleomycin against PBS by day | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE144468 | trials D5, D5b; IL-1beta against control organoids | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE316241 | trials C0 to C2b; Red2Kras against Confetti | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE316243 | trials C0 to C2b; genotype against genotype | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE316244 | trial C2; Areg-flox against control | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE310335 | trial C0; KRAS G12D organoid against control | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE310539 | A1, A4; trials M0 to M4; Sendai virus against PBS; AP-1 mutant against wildtype | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE247130 | A1, A5; trials M0 to M4; Cebpa mutant against control; stage against stage | not admissible | one library per condition; no within-group replication, as the reality-check trial recorded |
| GSE178360 | the human series report; none; three healthy donors and no condition | not admissible | no contrast exists in the deposit |
| GSE309751 | A1, deliverable 1; injured against mock at 14 and 49 days, bulk ATAC on sorted AT2 | marginal | assessed and not opened; bulk ATAC peak calls, not counts; two mice in the 49-day arms; peak presence at frozen loci is the admissible object, not a ranked GSEA |

</details>

## Reference resources and deposit aliases

The used-source sections above include Travaglini and Madissoon CELLxGENE collections,
England Zenodo 14673088 v1.1, Ng-Blichfeldt Figshare 7740071 v1 and source
workbooks. The register also includes the [HLCA reference model/embedding,
Zenodo 7599104](https://doi.org/10.5281/zenodo.7599104) through its [mapping
trials](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md).
MSigDB, ligand/receptor resources, NicheNet priors, gene annotations and author
code are versioned reference assets, not new biological replicates. TMS GEO
GSE132042/GSE149590 are release locators; the executed Figshare products and
their overlaps are identified above. Nb5's [completion audit](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/EXTENSION_COMPLETION.md)
also qualifies an official S3 brain object and full/raw atlas metadata. Its
count-valued brain layer is distinct from the earlier normalized Figshare
objects; the source release and layer must travel with any reuse.

### Remaining accession locators

Every identifier in the preserved 544-identifier census appears in this page.
The merged Saxton sources and screens add 19 identifiers, for 563 source/project
identifiers represented here; these remain distinct from utilized-dataset counts.
The remaining rows below record aliases, metadata relations and search/literature
locators that lack a separate executed-use disposition in the reviewed summaries.
Their linked records show the actual mention; explicit metadata decisions are
retained in the role column. A locator alone does not establish numerical use
or individual eligibility. BioProjects describe source
projects and may overlap a listed GEO series. The census is a bounded tracked-text
scan, not a count of independent cohorts or every sample/file accession.

<details>
<summary>132 remaining source-project, search and alias locators</summary>

| Identifier | Recorded role | Traceable mention |
|---|---|---|
| [GSE107455](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE107455) | Inspected E6 source relation: RXR/ChIP context; no matched temporal RNA–ATAC contrast | [Recorded mention](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/E6_SOURCE_REVIEW.md) |
| [GSE107456](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE107456) | Inspected E6 source relation: earlier RNA material; shared-source reuse is not independent replication | [Recorded mention](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/E6_SOURCE_REVIEW.md) |
| [GSE109774](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE109774) | Tabula Muris/Senis release locator; used processed products and overlap are listed above | [Recorded mention](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/DATASETS.md) |
| [GSE110464](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110464) | Inspected E6 GRO subseries; not a matched RNA–ATAC panel | [Recorded mention](../Research%20Article/gate2_DY1_damani_yokota_2026/rq_discordance/E6_SOURCE_REVIEW.md) |
| [GSE115083](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115083) | Recorded E6 umbrella/subseries relation; no separate admitted comparison | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [GSE131252](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE131252) | Prior-art source citation for macrophage history; no new numerical reuse recorded here | [Recorded mention](../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) |
| [GSE132040](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE132040) | Tabula Muris/Senis release locator; not an additional independent cohort | [Recorded mention](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/DATASETS.md) |
| [GSE145033](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145033) | Gupta source-relation/metadata reference; not the qualified single-cell series GSE145230 | [Recorded mention](../Research%20Article/gate2_W3_yadav_2025/extensions_20261031/REVIEW_B.md) |
| [GSE148992](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE148992) | A19 external reference-map locator; no numerical A19 extension admitted | [Recorded mention](../RQ_Specified/A19_fzd_response_reversibility/metadata/external_reference_map.json) |
| [GSE149563](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE149563) | A0 inspected, not selected: matching intermediate-state annotations were not recovered | [Recorded mention](../RQ_Specified/A0_conserved_epithelial_transition_program/DATASET_CANDIDATES.md) |
| [GSE152607](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE152607) | Parent/source relation for the HPCS subseries; not an additional cohort | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE154965.json) |
| [GSE169127](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE169127) | GEO sample membership/alias recorded during A2 metadata qualification | [Recorded mention](../analysis/research/runs/a2_source_qualification_v1/samples.tsv) |
| [GSE178405](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178405) | A19 source inspection: engineered-tissue sequencing locator; no recovered unit-level Figure 6/7 outcome join | [Recorded mention](research_dossiers/followup_2026-10-03/OUTCOMES.md) |
| [GSE193093](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE193093) | Nb5 companion/release locator; no additional executed cohort inferred | [Recorded mention](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/DATASETS.md) |
| [GSE210347](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE210347) | Reanalysis relation in GSE131907 metadata; not an independent source cohort | [Recorded mention](../RQ_Specified/A12_recipient_context/external_validation_20260928/sources/GSE131907_metadata.json) |
| [GSE221342](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221342) | A19 related source locator; no admitted A19 numerical extension | [Recorded mention](../RQ_Specified/A19_fzd_response_reversibility/metadata/external_reference_map.json) |
| [GSE221344](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221344) | A19 related source locator; no admitted A19 numerical extension | [Recorded mention](../RQ_Specified/A19_fzd_response_reversibility/metadata/external_reference_map.json) |
| [GSE227719](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227719) | Inspected EN10 lead: no qualified genotype/background-matched causal comparison | [Recorded mention](../Research%20Article/gate2_C2_england_2025/CANDIDATE_CHECKS.md) |
| [GSE243129](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE243129) | Parent/companion metadata for the GSE243124 pooled-library screen | [Recorded mention](../DEVELOPMENT.md) |
| [GSE247272](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247272) | GEO sample membership/alias recorded during A7 metadata qualification | [Recorded mention](../analysis/research/runs/a7_source_qualification_v1/samples.tsv) |
| [GSE247939](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247939) | Inspected GSE247946 subseries relation; no separate admitted A3 analysis | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_SOURCE_LINKS_V1.json) |
| [GSE247940](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247940) | Inspected GSE247946 subseries relation; no separate admitted A3 analysis | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_SOURCE_LINKS_V1.json) |
| [GSE247944](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247944) | Inspected GSE247946 subseries relation; no separate admitted A3 analysis | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_SOURCE_LINKS_V1.json) |
| [GSE247945](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247945) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE253136](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253136) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE253461](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253461) | Inspected A16/EN10 candidate; no qualified CD177 protein-sorted outcome or matched genotype comparison | [Recorded mention](../RESEARCH_QUESTIONS.md) |
| [GSE261696](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261696) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE261697](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261697) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE264398](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264398) | A0 metadata retrieval/source locator; no selected developmental contrast | [Recorded mention](../RQ_Specified/A0_conserved_epithelial_transition_program/continuation_source_manifest.json) |
| [GSE264407](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264407) | A0 metadata retrieval/source locator; developmental eligibility remains unresolved | [Recorded mention](../RQ_Specified/A0_conserved_epithelial_transition_program/continuation_source_manifest.json) |
| [GSE267731](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE267731) | England cell-of-origin source lead; no new qualified outcome analysis | [Recorded mention](../Research%20Article/gate2_C2_england_2025/ANALYSIS_OPPORTUNITIES.md) |
| [GSE270704](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE270704) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE278048](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278048) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE278050](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278050) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE278051](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278051) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE286981](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286981) | Subseries relation from inspected embryonic GSE286986; not a qualified adult-injury outcome source | [Recorded mention](roadmap_runs/2026-09-27-followthrough/metadata/GSE286986.json) |
| [GSE286982](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286982) | Subseries relation from inspected embryonic GSE286986; not a qualified adult-injury outcome source | [Recorded mention](roadmap_runs/2026-09-27-followthrough/metadata/GSE286986.json) |
| [GSE286983](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286983) | Subseries relation from inspected embryonic GSE286986; not a qualified adult-injury outcome source | [Recorded mention](roadmap_runs/2026-09-27-followthrough/metadata/GSE286986.json) |
| [GSE286985](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286985) | Subseries relation from inspected embryonic GSE286986; not a qualified adult-injury outcome source | [Recorded mention](roadmap_runs/2026-09-27-followthrough/metadata/GSE286986.json) |
| [GSE287605](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE287605) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE291215](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291215) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE295269](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE295269) | Source-listed perinatal Cebpa candidate; animal/pool and state map required before eligibility | [Recorded mention](audits/2026-09-28-rq-adversarial-review/epithelial-programs.md) |
| [GSE307874](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307874) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE307901](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307901) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE324239](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324239) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE324240](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE324240) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_SEARCH_SUMMARIES_V1.json) |
| [GSE325226](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE325226) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE330826](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE330826) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [GSE347939](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE347939) | Search-return locator; no individual eligibility decision recorded in the linked search summary | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A27_SEARCH_SUMMARIES_V1.json) |
| [PRJNA1013615](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1013615) | BioProject/source-project locator | [Recorded mention](remediation/2026-09-22/dataset_metadata/GSE242510.json) |
| [PRJNA1016394](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1016394) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE243124.json) |
| [PRJNA1016405](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1016405) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE243129.json) |
| [PRJNA1036384](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1036384) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/a7_source_qualification_v1/inventory.json) |
| [PRJNA1036655](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1036655) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_reference_source_v1/source_series.json) |
| [PRJNA1039244](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1039244) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C2_england_2025/metadata/continuation_intake.json) |
| [PRJNA1040945](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1040945) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_SOURCE_LINKS_V1.json) |
| [PRJNA1040951](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1040951) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_LINKED_SOURCE_METADATA_V1.json) |
| [PRJNA1041449](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1041449) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_reference_source_v1/source_series.json) |
| [PRJNA1070005](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1070005) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE254356.json) |
| [PRJNA1110274](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1110274) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE267226.json) |
| [PRJNA1110281](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1110281) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE267228.json) |
| [PRJNA1139141](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1139141) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE272862.json) |
| [PRJNA1140210](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1140210) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE273123.json) |
| [PRJNA1140211](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1140211) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE273122.json) |
| [PRJNA1164164](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1164164) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE277777.json) |
| [PRJNA1181768](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1181768) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/A27_SOURCE_INTAKE_V1.md) |
| [PRJNA1223922](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223922) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289676.json) |
| [PRJNA1223928](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223928) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289678.json) |
| [PRJNA1223934](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223934) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289683.json) |
| [PRJNA1223935](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223935) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289682.json) |
| [PRJNA1223938](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1223938) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289679.json) |
| [PRJNA1225182](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1225182) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE289846.json) |
| [PRJNA1225736](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1225736) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE290014.json) |
| [PRJNA1232855](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1232855) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE291333.json) |
| [PRJNA1280038](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1280038) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE300293.json) |
| [PRJNA1280046](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1280046) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE300288.json) |
| [PRJNA1291723](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1291723) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1291724](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1291724) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1291737](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1291737) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1314575](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1314575) | BioProject/source-project locator | [Recorded mention](remediation/2026-09-22/dataset_metadata/GSE307112.json) |
| [PRJNA1314603](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1314603) | BioProject/source-project locator | [Recorded mention](remediation/2026-09-22/dataset_metadata/GSE307128.json) |
| [PRJNA1315700](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1315700) | BioProject/source-project locator | [Recorded mention](remediation/2026-09-22/dataset_metadata/GSE307351.json) |
| [PRJNA1321929](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1321929) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE307529.json) |
| [PRJNA1321930](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1321930) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE307534.json) |
| [PRJNA1328749](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1328749) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE308103.json) |
| [PRJNA1336875](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1336875) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE309751.json) |
| [PRJNA1366485](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1366485) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/a7_source_qualification_v1/inventory.json) |
| [PRJNA1451232](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1451232) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE327565.json) |
| [PRJNA1451861](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1451861) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE327686.json) |
| [PRJNA1460731](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1460731) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1461803](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1461803) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1462284](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1462284) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/arz1_source_qualification_v1/series_records.csv) |
| [PRJNA1531181](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1531181) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_GEO_SELECTED_METADATA_V1.json) |
| [PRJNA302457](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA302457) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/wg_source_qualification_v1/qualification.json) |
| [PRJNA302459](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA302459) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/wg_source_qualification_v1/qualification.json) |
| [PRJNA318630](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA318630) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [PRJNA430888](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA430888) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate1_03_nabhan_2018/source_reproduction/provenance.json) |
| [PRJNA433822](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA433822) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [PRJNA449866](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA449866) | BioProject/source-project locator | [Recorded mention](roadmap_runs/2026-09-27/GSE113049_sample_metadata.json) |
| [PRJNA471894](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA471894) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [PRJNA476688](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA476688) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [PRJNA507000](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA507000) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_human_evidence_preservation_v1/independent_human_candidates.json) |
| [PRJNA560492](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA560492) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_human_evidence_preservation_v1/independent_human_candidates.json) |
| [PRJNA592973](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA592973) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE141259.json) |
| [PRJNA594274](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA594274) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE141635.json) |
| [PRJNA603749](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA603749) | BioProject/source-project locator | [Recorded mention](roadmap_runs/2026-09-27/GSE144468_sample_metadata.json) |
| [PRJNA604180](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA604180) | BioProject/source-project locator | [Recorded mention](roadmap_runs/2026-09-27/GSE144598_sample_metadata.json) |
| [PRJNA605766](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA605766) | BioProject/source-project locator | [Recorded mention](roadmap_runs/2026-09-27/GSE145031_sample_metadata.json) |
| [PRJNA606472](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA606472) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/Yd1_extension_c_v1/series_relations.csv) |
| [PRJNA607553](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA607553) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_LINKED_SOURCE_METADATA_V1.json) |
| [PRJNA632640](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA632640) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE150527.json) |
| [PRJNA634372](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA634372) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/DY1_P02_temporal_source_v1/source_series.json) |
| [PRJNA647901](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA647901) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_TARGETED_SUMMARIES_V1.json) |
| [PRJNA648132](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA648132) | BioProject/source-project locator | [Recorded mention](research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites/A3_A27_SOURCE_LINKS_V1.json) |
| [PRJNA681345](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA681345) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/wg_source_qualification_v1/qualification.json) |
| [PRJNA681803](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA681803) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/wg_source_qualification_v1/qualification.json) |
| [PRJNA693243](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA693243) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/wg_source_qualification_v1/qualification.json) |
| [PRJNA715241](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA715241) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/a2_source_qualification_v1/inventory.json) |
| [PRJNA778206](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA778206) | BioProject/source-project locator | [Recorded mention](../analysis/research/runs/Yd1_extension_c_v1/series_relations.csv) |
| [PRJNA788524](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA788524) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE190821.json) |
| [PRJNA860972](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA860972) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_N1_nabhan_2023/metadata/additional_source_intake.json) |
| [PRJNA865889](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA865889) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA904776](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA904776) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE218665.json) |
| [PRJNA904777](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA904777) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE218666.json) |
| [PRJNA923805](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA923805) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/trials/u0_geo_design_audit/GSE222901.json) |
| [PRJNA925549](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA925549) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE223302.json) |
| [PRJNA940730](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA940730) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA940746](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA940746) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA940973](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA940973) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA940986](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA940986) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA940992](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA940992) | BioProject/source-project locator | [Recorded mention](../Research%20Article/gate2_C3_yu_lee_choi_min_2026/DATASETS.md) |
| [PRJNA985564](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA985564) | BioProject/source-project locator | [Recorded mention](../RQ_Specified/A1_transitional_epithelial_state_distinction/metadata/GSE235212.json) |

</details>

## Local storage and historical inventories

Source use above and local file presence are separate facts. Raw caches are
ignored; a fresh clone does not contain them. No fresh cache scan was performed
for this documentation consolidation.

- [7 November storage audit](audits/2026-11-07-public-data-inventory/RECONCILIATION_V2.md): 4,197 files / 74.04 GB across the root and registered worktree caches at scan time. Copies and derived cache products count separately.
- [Directories at that scan](audits/2026-11-07-public-data-inventory/snapshot_v2/local_directories.csv) and [individual files](audits/2026-11-07-public-data-inventory/snapshot_v2/local_files.csv).
- [544-identifier reference census](audits/2026-11-07-public-data-inventory/snapshot_v2/accession_references.csv): references and aliases, not 544 utilized datasets. It remains a dated provenance artifact.
- [Original 51-file inventory](../analysis/raw_data_inventory.txt): historical two-series snapshot, preserved unchanged.
- [Consolidation and documentation move record](audits/2026-11-08-source-consolidation/README.md): scope, retained evidence, link checks and archival locations.

Exact URLs, versions, hashes, units and inclusion rules remain in the linked
source reports and [registered receipts](../analysis/research/registry.json).
Add new source/disposition rows here and link the owning result; retain dated
audits as evidence rather than creating another current inventory supplement.