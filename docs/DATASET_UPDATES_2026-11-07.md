# Public-data use: additions and reconciliation, 7 November 2026

Companion to the [central dataset inventory](DATASETS.md), based on merged main
`32ab85e87bee788e62bec4e1b7ce5bad6df84d30`. This fills omissions in the September
list and distinguishes actual numerical use from metadata qualification. Source
links establish deposit identity; linked repository reports establish use. This
review does not refresh remote availability, rerun analyses or change eligibility.

The [complete accession-reference census](audits/2026-11-07-public-data-inventory/snapshot_v2/accession_references.csv)
also retains search leads, parent/child aliases and metadata-only records. It is
not a list of independent cohorts. Exact versions, hashes, transformations and
units remain in the owning contracts/manifests/results. One source reused by
several questions is not several replications.

## Numerical use and source reconstruction missing from the central list

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

## Qualified or inspected sources without an admitted biological contrast

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

## Resources that are not additional cohorts

The existing central list retains Travaglini and Madissoon CELLxGENE collections,
England Zenodo 14673088 v1.1, Ng-Blichfeldt Figshare 7740071 v1 and source
workbooks. Add explicit discovery routes for the [HLCA reference model/embedding,
Zenodo 7599104](https://doi.org/10.5281/zenodo.7599104) through its [mapping
trials](../Research%20Article/gate1_04_sikkema_2023_hlca/ANALYSIS_TRIAL_PLAN.md).
MSigDB, ligand/receptor resources, NicheNet priors, gene annotations and author
code are versioned reference assets, not new biological replicates. TMS GEO
GSE132042/GSE149590 are release locators; the executed Figshare products and
their overlaps are identified above. Nb5's [completion audit](../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/EXTENSION_COMPLETION.md)
also qualifies an official S3 brain object and full/raw atlas metadata. Its
count-valued brain layer is distinct from the earlier normalized Figshare
objects; the source release and layer must travel with any reuse.

## Integration and remaining source leads

[PR #167](https://github.com/xorca0711/ravel/pull/167) merged on 7 November at
`32ab85e`. DuPage's GSE58998/GSE55773 use and later GSE262130 follow-up are now
included above and in the refreshed receipt census. The preserved initial
snapshot described the earlier local branch correctly at its scan time; it is
superseded for current integration/use status by this update.

GSE262129 and GSE291449 remain later-study leads, not executed inputs in this
follow-up. The TIGIT study's stated E-MTAB-8861 conflicts with the recovered
metadata; its single-cell data were not used. E-MTAB-6156 and GSE79339/GSE121838
are cited reuse/source leads, not new independent validation cohorts. See the
[qualified candidate sources](../Research%20Article/gate3_09_dupage_2015/candidates/SOURCE_QUALIFICATION.md)
and [reconciliation record](audits/2026-11-07-public-data-inventory/RECONCILIATION_V2.md).
