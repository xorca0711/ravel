# A1 branch inventory: evidence per branch

Prepared 28 September 2026 as a documentation pass over the existing A1 evidence.
No new analysis was run, no model refitted and no dataset searched. Every number
below is copied from a document or table already tracked in this folder, or from
the canonical register card, and each row and paragraph names its source file.
Values are reproduced at the precision of the source.

Scope and separation of evidence status. Rows marked *published* report a result
of the source study. Rows marked *this repository* report a reanalysis or audit
performed here, which reuses the source cohorts and is not independent
replication. The "current verdict" column copies the wording of the cited
document, with markdown emphasis removed and no other change; it is not a
restatement or a grade. Nothing here nominates a primary test, changes a claim
grade or amends a frozen contract.

Companion document: [A1_A8_A14_OUTCOME_INVENTORY.md](A1_A8_A14_OUTCOME_INVENTORY.md).
Governing documents: [PLAN.md](../PLAN.md), [STUDY_MAP.md](../STUDY_MAP.md),
[LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [JOBS.md](../JOBS.md),
[NEXT_SESSION.md](../NEXT_SESSION.md),
[canonical A1 card](../../../RESEARCH_QUESTIONS.md#a1),
[MC1-MC2](../../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1).

## Branch table

| Branch | Regulatory or RNA feature measured | Population / state definition | Timing relative to injury or culture | Biological unit and n | Endpoint measured so far | Principal rival | Current verdict (copied wording) | What is missing for a linked later outcome | Source document(s) |
|---|---|---|---|---|---|---|---|---|---|
| B1. Native-assembly histone tracks (iATC / iAT2 / iAT1 CUT&Tag), with H3 and window sensitivity | H3K27ac, H3K4me3, H3K27me3 and matched H3 CPM signal at 23 frozen promoters; raw mark and mark/H3 ratios at +/-1 kb and +/-5 kb | Induced culture states iATCs, iAT2 and iAT1 from one B2-3 iPSC line; author state labels retained | Culture states of the deposited induction protocol; no injury axis | Two CUT preparations per state, one parental iPSC line; 24 tracks; 1,104 contrasts | Locus-level direction concordance between preparations and windows; CDKN1A H3K27ac/H3 higher and H3K27me3/H3 lower in iATCs versus iAT2; CLDN4 and KRT8 reverse under H3 adjustment | Technical preparation and H3 denominator effects rather than a state-specific regulatory programme | "The result is a locus-specific descriptive lead in one iPSC line and two preparations per state." | Independent preparations or donors, a later measured epithelial outcome in the same cultures, and spike-in-scaled occupancy | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [direct_mark_run.json](direct_mark_run.json), [sample_manifest.tsv](../tables/direct_marks_2026-09-25/sample_manifest.tsv), [histone_window_and_H3_sensitivity.tsv](../tables/second_batch_verification/histone_window_and_H3_sensitivity.tsv) |
| B2. Histone promoter-definition / alternative transcript-start robustness | Same three marks re-quantified at annotated alternative transcript starts | Same iATC / iAT2 / iAT1 states | Same culture states | 46 TSS positions over 23 loci; 11 genes have an alternative position; 2,208 signal rows, 1,104 contrasts | Direction changes per mark at both windows; CDKN1A H3K27ac/H3 reverses in CUT1 at the second start | Promoter annotation choice rather than gene-level regulatory difference | "The defensible follow-up is therefore a promoter-resolved candidate, not gene-wide CDKN1A activation." | A promoter-resolved measurement in independent preparations paired to a later outcome | [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md), [tss_manifest.tsv](../tables/robustness_2026-09-25/histone/tss_manifest.tsv), [contrasts.tsv](../tables/robustness_2026-09-25/histone/contrasts.tsv) |
| B3. PATS deposited histone-track normalization | H3K4me3, H3K27ac, H3K36me3 and H3 in deposited bedGraph tracks (GSE141635) | Injured CTGF-positive AT2-lineage epithelium versus homeostatic AT2 | Sort at day 12 after bleomycin; separate day-8 TP53 ChIP preparation | 20 GSM library records; two replicate labels; not a verified independent-unit count | Timing documented; no quantitative between-condition amplitude comparison performed | Scaling and control-association differences between deposited tracks rather than biological occupancy difference | "Normalization hold remains: 20 SRA experiments and raw files exist; the paper describes MintChIP/BWA/HOMER and H3-normalized peak calling, but not a recoverable executed scale/control contract for every deposited track." | Executed per-library scale factors, mark-to-H3 association and matched control definitions, or a new matched cohort | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md) |
| B4. PATS H3K4me3 called-interval geometry audit (technical) | Deposited called-interval size and merging parameters | Homeostatic AT2 versus CTGF-positive injured epithelium | As deposited | Deposited interval files; no biological unit claimed | Different caller settings verified in the original headers: homeostasis size 1000 / minDist 2000, CTGF-positive size 4000 / minDist 4000 | Caller parameter difference, which is a technical explanation of any peak-count contrast | "Peak-count/overlap contrasts are therefore technical diagnostics only; biological comparison waits for common-region quantification or consistent re-calling." | Common-region quantification or consistent re-calling before any state comparison | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [PLAN.md](../PLAN.md), [H3K4me3_technical_geometry.tsv](../tables/descriptive/H3K4me3_technical_geometry.tsv) |
| B5. PATS raw-read reprocessing (pruned) | Would be raw ChIP reads for common quantification | Injured CTGF-positive versus homeostatic AT2 | As deposited | 20 SRA experiments; deposited original files total 54.86 GB, 48.01 GB for 16 histone/H3 libraries | Resource audit only; no raw download started | Injury, sort and state remain confounded whatever the processing | "Pruned from this discriminating sequence: deposited original files total 54.86 GB (48.01 GB for 16 histone/H3 libraries), before reference/alignment storage." | A defined useful contrast with reconciled preparation identity plus an adequate compute and storage plan | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [PATS_raw_resource_audit.tsv](../tables/evidence_closure/PATS_raw_resource_audit.tsv) |
| B6. PATS measured lineage endpoint (Kobayashi Extended Data 4) | None; RNA and chromatin are not measured in these animals | Krt19-labelled alveolar cells scored for KRT8 and AGER protein among tdTomato-labelled cells | Krt19-CreER pulse 7 days after bleomycin, harvest day 12; nominal five-day interval | Three explicitly named mice per marker, fields nested within mouse; 38 source fields; 18 zero-denominator control fields excluded | Mouse-level KRT8-positive and AGER-positive fractions among labelled cells | Denominator and field-weighting choices; marker panels are not mutually exclusive | "Published source reproduction; no new tracing experiment or exit-rate measurement" | An early regulatory or RNA measurement in the same animals, and defined non-zero control denominators | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [pats_mouse_endpoints.tsv](../tables/lineage/pats_mouse_endpoints.tsv), [pats_source_fields.tsv](../tables/lineage/pats_source_fields.tsv) |
| B7. IRE1alpha primary ten-mouse RNA contrast | Epithelial ribosome-associated RNA; eight frozen transitional markers and three published signatures | Whole epithelial RiboTag compartment, not a sorted transitional population | Bleomycin, day-7 harvest; KIRA8 versus vehicle | Ten mice, five per arm, across batches S061 and S135; design rank 4, 6 residual df; 14,811 tested genes of 42,548 input features | Four genes pass whole-family BH FDR 0.05, all lower with KIRA8; no frozen marker and no eligible pathway passes | Cell-composition and translation-associated change rather than within-state response | "14,811 genes tested; four pass whole-family BH FDR < 0.05, all lower with KIRA8" | A later measured outcome in these same mice; the published day-14 AGER endpoint is a different experiment | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [ire1_run.json](ire1_run.json), [fit_summary.tsv](../tables/ire1/fit_summary.tsv), [gene_set_camera.tsv](../tables/ire1/gene_set_camera.tsv) |
| B8. IRE1alpha omission and batch sensitivity | Same RNA features, re-estimated | Same epithelial compartment | Same day-7 harvest | Ten leave-one-mouse-out fits retaining nine mice (4 versus 5); S061 within-batch fit with three mice per arm; S135 two mice per arm, descriptive only | Direction retained in all ten omissions for seven of eight markers, nine of ten for Ager; whole-family discoveries 1 to 264 versus 4 in the primary model; omission effect correlations 0.928-0.973 | Batch structure and individual-mouse influence rather than a stable treatment effect | "The strongest permissible interpretation is directional follow-up, not a confirmed pathway or a replacement primary analysis." | A treated and control cohort with linked later fate in the same units; sensitivity ranges are not confidence intervals | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [ire1_stability_run.json](ire1_stability_run.json), [fit_diagnostics.tsv](../tables/ire1_stability_2026-09-25/fit_diagnostics.tsv), [ire1_pathway_comparison.tsv](../tables/second_batch_verified/ire1_pathway_comparison.tsv) |
| B9. IRE1alpha cell-resolved follow-up screen (GSE243124) | Would be epithelial scRNA under saline, epithelial IRE1 knockout, KIRA8 or bleomycin | Day-10 epithelial cells; no recovered author cell annotations | Day-10 harvest | One pooled GEM library per condition, 2/2/3/3 contributing mice | Eligibility screen only; no test fitted | Pooling removes independent treatment replication; cell-level testing cannot recreate it | "Design screen complete; replicate-level test not eligible: GSE243124 pools 2/2/3/3 mice into one GEM library per saline/KO/KIRA8/bleomycin condition." | Demultiplexed mice, independent pooled-library replicates, or a new replicated treated/control dataset | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| B10. AP-1 mouse-level regional HOPX response | None measured here; genotype is the perturbation and HOPX protein the readout | GFP lineage-labelled cells in injured in-situ regions and intact de-novo regions | Microscopy endpoint of the source design; region is the context axis | Three mice per genotype, three fields per mouse per region; 12 mouse/region fractions | Mouse-mean HOPX-positive fraction among GFP-labelled cells: wild type 17.30% in situ and 3.63% de novo; AP-1 mutant 1.24% and 12.12%; interaction 24.55 percentage points; exact two-sided permutation p=0.10 over 20 allocations; nine omissions span 19.07 to 27.62 points | Regional sampling, labelling efficiency and unrandomized genotype assignment | "This supports a consistent direction in the observed animals, not precise population inference." | Replicated animals with an early chromatin or RNA measurement in the same mice; the mutant RNA/ATAC experiment has one pooled library per condition | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ap1_mice.tsv](../tables/regulatory_fate/ap1_mice.tsv), [ap1_group_summary.tsv](../tables/regulatory_fate/ap1_group_summary.tsv), [ap1_region_interaction.tsv](../tables/regulatory_fate/ap1_region_interaction.tsv) |
| B11. AP-1 bulk ATAC regulatory context (GSE309751) | Published peak calls across post-viral time points and Kras perturbation | Bulk lung accessibility, not a purified transitional population | 14-day and 49-day post-viral time points | 14 bulk ATAC GSM library records | Context only; no contrast launched here | Two 49-day mock-PBS titles conflict with Sendai-infection treatment fields; adjacent-time contrasts share a middle time point | "provides additional regulatory context, not a fully matched fate experiment" | Verified control identity and a matched fate experiment in the same animals | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ANALYSIS_REFERENCE_MAP.md](ANALYSIS_REFERENCE_MAP.md), [metadata/README.md](../metadata/README.md) |
| B12. HPCS descendant source-composition table | RNA state labels only, from the deposited observation metadata | Author-designated trace-sorted cells with eight deposited RNA-state categories | Slc4a11 and Hopx tracing in established KP tumours; 3-day and 14-day chase groups | 5,333 retained traced cells across 22 source labels and six deposited groups; cells are not biological replicates | Equal-source and cell-pooled state fractions per group, e.g. 6wk_3d 93.08% and 92.83% HPCS, 14wk 43.73% and 31.79% | Source weighting and capture depth rather than a descendant-composition difference | "These are descendant RNA-label compositions among retained trace-sorted cells, not new measurements of cell production, clone size or transition rates." | An early regulatory measurement in the same animals, verified pool membership, and a current-state reporter | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [hpcs_source_composition_run.json](hpcs_source_composition_run.json), [source_state_counts.tsv](../tables/hpcs_source_composition/source_state_counts.tsv), [group_descriptive_summary.tsv](../tables/hpcs_source_composition/group_descriptive_summary.tsv) |
| B13. HPCS alias-to-mouse verification | None; identity evidence only | Same 22 retained source aliases | Same tracing design | 22 distinct animals covering all 5,333 retained traced cells; four additional listed animals have no retained traced alias | Exact animal tag, library and driver agreement for every join; sex and reporter genotype recorded per animal | A sample-name pattern could resemble an animal without being one | "This is stronger evidence than inferring animals from the shape of a sample name." | Pool membership and non-overlap are separate questions; the library/chase confounding and the missing current reporter remain | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [hpcs_mouse_crosswalk.tsv](../tables/regulatory_fate/hpcs_mouse_crosswalk.tsv), [hpcs_named_mouse_summary.tsv](../tables/regulatory_fate/hpcs_named_mouse_summary.tsv) |
| B14. Hopx harvest-timing reconciliation | None; schedule evidence only | Hopx-driver traced group IGO17543 | Induction at 12 weeks, 14-day chase, harvest at 14 weeks | One library / two source aliases / 911 retained cells in that group | Primary animal table Mice!A90:M92, the main Fig. 2 tracing design and GEO agree | The earlier README wording said a 12-week harvest; study labels are rounded, not exact chronological ages | "the main Fig. 2 tracing design and GEO agree on a 14-week harvest following induction at 12 weeks and a 14-day chase" | A clarified induction/harvest schedule for the remaining groups, plus libraries spanning chase within matched designs | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [source_manifest.tsv](../tables/hpcs_source_composition/source_manifest.tsv) |
| B15. HPCS annotation partition and confidence-abstention audit | RNA cluster and biological label partitions | All deposited cells and the traced subset | Same tracing design | 28,402 deposited label rows; 5,333 traced cells | Notebook 01 cell 142 reproduces all 28,402 labels; all 1,282 traced-cell stringent changes (24.04%) and all 11,133 object-wide changes are abstentions; ARI 0.6331 / 0.5723 / 0.7148 across the three partitions | Three label columns could be mistaken for three independent classifiers | "Completed: explicit author mapping and confidence-abstention audit. Independent-classifier interpretation retired." | Independent labels or features, or a genuinely separate validation cohort | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md), [hpcs_annotation_audit.tsv](../tables/evidence_closure/hpcs_annotation_audit.tsv), [partition_agreement.tsv](../tables/robustness_2026-09-25/hpcs/partition_agreement.tsv) |
| B16. HPCS source-influence sensitivity | Same RNA state labels | Same traced cells and 22 sources | Same groups | 22 distinct source omissions, 704 source/category omission rows, 192 group/category summaries | Omission ranges per group, e.g. 14wk cell-pooled HPCS 29.36-51.11%; omitting BF1303_B0301_GFP+ (811/991 cells) raises the pooled fraction from 31.79% to 51.11% | A few large sources dominate the pattern | "These are sensitivity ranges, not confidence intervals or temporal effect estimates." | Verified animals or disjoint pools before any weighting scheme becomes an estimand | [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md), [leave_one_source_out.tsv](../tables/robustness_2026-09-25/hpcs/leave_one_source_out.tsv), [group_influence_summary.tsv](../tables/robustness_2026-09-25/hpcs/group_influence_summary.tsv) |
| B17. HPCS design identifiability (chase versus library) | None; design algebra only | Same 22 source aliases | 3-day and 14-day chase intervals | 22 source aliases across six libraries; every library contains only one chase interval | Adding chase to unrestricted library indicators adds zero rank: 6 to 6 overall, 5 to 5 within Slc4a11, 2 to 2 within Hopx; driver adds one dimension (6 to 7) | Library effects are perfectly aliased with chase, so an apparent chase effect is not separable | "Thus the proposed library-adjusted chase coefficient is not separately estimable." | Independent libraries spanning chase within matched designs; recovering identities alone does not fix this | [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md), [design_rank_audit.tsv](../tables/robustness_2026-09-25/hpcs/design_rank_audit.tsv), [library_group_support.tsv](../tables/robustness_2026-09-25/hpcs/library_group_support.tsv) |
| B18. TIGIT paired bulk ATAC (held) | Would be paired accessibility, TIGIT-positive versus negative | TIGIT-sorted tumour cells in the HPCS 2020 cancer context | As deposited | Eight bulk ATAC GSM mapping to four deposited source blocks; the compound alias 106621_106642 is unresolved against four reported replicates | Identity audit complete; no paired inference fitted | The compound alias may be one animal, a pool or overlapping sources | "Targeted recovery exhausted: all eight SRA full records recover original sort/source filenames but no additional pool membership." | Explicit disjoint animal or pool membership and pairing for all four source blocks | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [GEO_ENA_sample_audit.tsv](../tables/identity_audit/GEO_ENA_sample_audit.tsv), [SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md) |
| B19. Tsutsui regulatory perturbation library identities | Treatment, mark and author-declared preparation labels for CUT&Tag and RNA libraries | Inhibitor-treated iATCs, epithelial organoids and NHLF co-cultures | Inhibitor CUT&Tag; organoid days 14 and 17; fibroblast RNA | 64 runs: 26 inhibitor CUT&Tag (PRJDB37980), 32 organoid CUT&Tag (PRJDB37983), six fibroblast RNA libraries (PRJDB37982, three author-declared preparations per condition) | Two explicitly numbered CUT preparations with their treatment and H3 controls identified | Figure tracks use E. coli DNA normalization while deposited baseline tracks use CPM, so amplitudes are not comparable | "The published, perturbation-associated regulatory analysis can be placed in the evidence chain. No new normalized track comparison or peak-count fit is claimed." | Per-preparation peak counts or normalized tracks plus spike-in and H3 scaling provenance | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_sequencing_crosswalk.tsv](../tables/regulatory_fate/tsutsui_sequencing_crosswalk.tsv) |
| B20. Tsutsui culture endpoints and program suppression | RNA and reporter readouts, plus a gel-contraction functional readout | iATC- and iAT2-derived cultures from one parental iPSC line; derived reporter lines add no independent donor | Medium switch from day zero; separate siRNA and inhibitor experiments | 65 endpoint/condition summaries from 317 source measurements; n per condition 3 to 7 author-declared independent culture experiments | SFTPC 229.88-fold and AGER 33.32-fold mean increases versus day-zero values; AGER HiBiT 158.45-fold higher in AT1 versus AT2 induction (three experiments per condition); ITGB6 0.455 and 0.319 of siCont after ATF3 and HNF1B knockdown, KRT17 0.369 and 0.192; AP-1 inhibitors give 59.64% and 57.89% mean normalized gel-contraction inhibition | These are separate experiments, so program suppression and differentiation capacity cannot be joined | "The combined evidence supports modifiable programs and population-level differentiation capacity. It does not show that p300/CBP inhibition or knockdown rescues the fate of the same cells followed in the medium-switch assay." | Independent donors, and chromatin plus outcome measured in the same preparations | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| B21. Tsutsui predicted regulatory gene-set audit | Author-selected predicted AP-1/HNF1B-associated gene lists | Inhibitor-treated iATC chromatin predictions with an RNA-upregulated subset | Same inhibitor experiments | Supplied gene lists, not biological units | 325 shared predicted genes; 126-gene RNA-upregulated subset, all within the shared set; HNF1B-only column has 317 rows but 313 unique genes (ZNF608, ZNF609, ZNF710, ZNRF3 duplicated) | A selected prediction list can be mistaken for measured binding | "These are the author's selected predictions, not a new discovery or a binding assay." | A measured binding or perturbation-linked outcome assay in the same preparations | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_gene_set_audit.tsv](../tables/regulatory_fate/tsutsui_gene_set_audit.tsv) |
| B22. TP53 / Mdm2 source-list direction audit | Signs of supplied selected differential-expression lists | AT2-origin and AT1-origin lineage-labelled responses to Mdm2 perturbation | Source-study perturbation design; full manifest unavailable | Supplied gene lists only; no biological sample manifest recovered | AT2-origin-only set 3,984 genes with 2,049 increased and 1,935 decreased; AT1-origin-only set 686 with 245 and 441; shared set 868 with 493 increased in both, 266 decreased in both and 109 opposite | A shared significance list can be read as shared activation | "A gene unique to one significant list is not a tested origin interaction; an unlisted coefficient is unknown, not zero." | Full count matrix and sample manifest; GSE335749 and GSE335750 are private with a displayed scheduled release of Jun 01, 2027 | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tp53_signed_set_summary.tsv](../tables/regulatory_fate/tp53_signed_set_summary.tsv), [tp53_accessibility.tsv](../tables/regulatory_fate/tp53_accessibility.tsv) |
| B23. CD44 eight-mouse paired contrasts and genotype interaction | Sorted bulk RNA; eight transported transitional markers within a whole-transcriptome family | CD44-protein-sorted AT2 populations, positive versus negative, in WT and SP-C mutant lungs | As deposited; no explicit injury time axis in the count matrix | Eight mice, four paired per genotype, 16 libraries; design rank 10, six residual df; 15,516 genes after the shared filter; TMM factors 0.897-1.084; raw library totals 9.02-21.36 million | Per-contrast FDR<0.05 counts 6,615 (WT), 8,739 (mutant) and 5,023 (interaction); pooled-family counts 6,659 / 8,480 / 5,321 over 46,548 gene-contrast tests; seven of eight transported markers change in both genotypes; Cldn4 interaction -1.722 (pooled q 3.39e-13); Sftpc interaction -0.239 shrinks to -0.0046 when WT2 is omitted | Bulk fractions can contain different cell mixtures; technical alignment and RNA-integrity QC are unavailable | "Completed: SRA originals resolve the crosswalk; paired contrasts and direct interaction run. Shared marker directions retire using this panel alone as a disease-specific label." | An independently defined state, protein or fate outcome in these same mice | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [cd44_closure_run.json](cd44_closure_run.json), [fit_summary.tsv](../tables/cd44_closure/fit_summary.tsv), [focus_effects.tsv](../tables/cd44_closure/focus_effects.tsv), [cd44_focus_stability.tsv](../tables/closure_verification/cd44_focus_stability.tsv) |
| B24. One-donor methylation-domain reference | Author-called UMR, LMR and PMD overlap of promoters | Normal human AT2-to-AT1 culture; D4 is not a purified injury transitional population | Culture days D0, D4 and D6 | One WGBS donor; 414 domain intersections; hg19 +/-1-kb promoters | Promoter fractions overlapping each domain class, under both coordinate conventions; the alternative BED interpretation changes an overlap fraction by at most 0.0005 | Coordinate convention and domain-class overlap rather than promoter CpG methylation | "No replicated DMR test, purified transitional-state assignment or injury/tumour fate conclusion follows from this normal-culture reference." | Independent donors and a state-defined population with a later measured outcome | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [methylation_domain_overlap.tsv](../tables/direct_marks_2026-09-25/methylation_domain_overlap.tsv) |
| B25. Descriptive deposited-source profiles (HPCS ATAC, CD44 RNA) | Integer-count QC and sample-level principal components | Deposited source blocks of GSE154966 (112,729 features, eight libraries, four aliases) and GSE273123 (27,179 features, 16 libraries, eight aliases) | As deposited | Library records and source aliases, not verified independent units at the time of the run | Integer-count audit and sample PCA completed for both | Sample structure can reflect batch or pooling rather than state | "neither plot supplies biological replication or an inferential contrast" | Verified units; CD44 identities have since been resolved, TIGIT pooling has not | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [figures/README.md](../figures/README.md), [GSE154966_source_PCA_QC.tsv](../tables/descriptive/GSE154966_source_PCA_QC.tsv), [GSE273123_source_PCA_QC.tsv](../tables/descriptive/GSE273123_source_PCA_QC.tsv) |
| B26. Independent direct-mark comparator screen (GSE150527) | Would be donor-matched input and H3K27ac BigWig amplitude | Human AT2-to-AT1 culture at D0, D4 and D6 | Culture days | RNA has three donor labels, selected histones two, WGBS one donor | Eligibility screen only; no quantitative comparison run | Unspecified quantitative track scale, and D4 is mixed differentiation rather than a purified transitional state | "Context screen complete; quantitative comparison not eligible: GSE150527 has donor-matched input and H3K27ac BigWigs across D0/D4/D6, but catalog text says aligned BigWigs without specifying their quantitative scale." | Verified track scaling plus an appropriate state definition | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| B27. SAGE perturbation deposition (public-input hold) | Would be time-resolved transcription-factor perturbation with repair and pathological branches | Epithelial branches as defined by that preprint | Time-resolved perturbation | None available | Availability check only | Promised deposition is not measured data | "Public-input hold: current primary text still promises later GEO/Single Cell Portal/code deposition; no new accession was verified in this bounded check." | Published processed data, guide and sample identities, and animal-level design | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [ANALYSIS_REFERENCE_MAP.md](ANALYSIS_REFERENCE_MAP.md) |

## Branch notes

### B1. Native-assembly histone tracks, with H3 and window sensitivity

GSE289683 and GSE291333 contribute 24 CPM tracks covering three induced states,
two CUT labels and H3K27ac, H3K4me3, H3K27me3 and H3, from the B2-3 iPSC line
([sample_manifest.tsv](../tables/direct_marks_2026-09-25/sample_manifest.tsv),
24 rows). The frozen contract fixes 23 loci
([loci.tsv](../tables/direct_marks_2026-09-25/loci.tsv) holds 23 distinct genes
across the T2T-CHM13v2.0 and hg19 rows;
[direct_mark_loci.json](../config/direct_mark_loci.json) is the contract), and
the run produced 1,104 measurements over two windows
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). Concordance between the two
preparations is 36/45 eligible locus-contrast pairs for H3K27ac, 36/42 for
H3K4me3 and 38/42 for H3K27me3, with 91, 86 and 87 eligible preparation-contrasts
at +/-1 kb out of 92 possible, and H3 reversing the raw-mark direction in 26, 15
and 18 of them
([histone_sensitivity_counts.tsv](../tables/second_batch_verification/histone_sensitivity_counts.tsv)).
The predefined CDKN1A promoter has higher H3K27ac/H3 in iATCs versus iAT2 (+0.84,
+1.27 log2) and lower H3K27me3/H3 (-1.38, -0.89), while CLDN4 changes from higher
raw H3K27ac (+0.36, +0.41) to lower H3-adjusted signal (-0.94, -0.89), and CLDN4
H3K27me3/H3 disagrees between preparations (+0.85, -1.27)
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). Sixteen comparisons are
ineligible and listed in
[held_histone_ratios.tsv](../tables/identity_audit/held_histone_ratios.tsv).

### B2. Histone promoter-definition and alternative transcript starts

The cached native-CHM13 RefSeq Liftoff v5.3 annotation supplies 150 eligible
parent-linked transcript features at 46 distinct gene/TSS positions for the 23
frozen loci, of which 11 genes have an alternative position and 12 have only the
baseline ([ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md),
[tss_manifest.tsv](../tables/robustness_2026-09-25/histone/tss_manifest.tsv)).
Requantifying the 24 tracks at both windows produced 2,208 signal rows and 1,104
contrasts, with direction changes in 13/87 (H3K27ac), 7/75 (H3K4me3) and 18/90
(H3K27me3) eligible alternative-TSS comparisons at +/-1 kb, and 18/92, 10/84 and
20/92 at +/-5 kb. For CDKN1A the two plus-strand starts are chr6:36,497,107 and
chr6:36,499,358 (zero-based CHM13, 2,251 bp apart); at +/-1 kb the iATCs-minus-iAT2
H3K27ac/H3 effect moves from +0.837 to -0.654 in CUT1 and from +1.273 to +0.860
in CUT2, while H3K27me3/H3 remains lower at both starts in both preparations
(-1.383 to -2.566 and -0.888 to -1.783). Verification compared 264 alternative
windows with base-resolution reader values
([robustness_verification.json](robustness_verification.json)).

### B3. PATS deposited histone-track normalization

GSE141635 deposits 20 GSM records covering H3K4me3, H3K27ac, H3K36me3 and H3 in
injured CTGF-positive epithelium versus homeostatic AT2, plus TP53 and input in
the transitional population, with two replicate labels
([STUDY_MAP.md](../STUDY_MAP.md)). The histone experiment sorts CTGF-positive
cells on day 12 while the TP53 ChIP uses a distinct day-8 Sftpc-lineage sort, so
they are different experiments
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). The methods describe
H3-normalized peak calling and the cached generic MintChIP pipeline calls HOMER
`makeUCSCfile`, but neither establishes each deposited track's scaling factors
and paired controls. Four bedGraphs were acquired and the two larger
CTGF-positive mark files remain outside the frozen 256-MiB per-file ceiling; the
required input is specified in
[SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md) and has not been sent.

### B4. PATS H3K4me3 called-interval geometry

The first payload audit found different peak-caller settings between conditions:
homeostasis uses size 1000 / minDist 2000 and CTGF-positive injury uses size 4000
/ minDist 4000, with other parameter differences
([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)). The geometry is retained as a
technical table,
[H3K4me3_technical_geometry.tsv](../tables/descriptive/H3K4me3_technical_geometry.tsv),
and no biological peak-overlap figure was made
([figures/README.md](../figures/README.md)). The plan states that biological
comparison waits for common-region quantification or consistent re-calling
([PLAN.md](../PLAN.md)).

### B5. PATS raw-read reprocessing

The resource audit records 20 SRA experiments whose deposited original files
total 54.86 GB, of which 48.01 GB belongs to 16 histone/H3 libraries, before
reference and alignment storage
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md);
[PATS_raw_resource_audit.tsv](../tables/evidence_closure/PATS_raw_resource_audit.tsv)
has 20 rows summing to 54,858,327,209 bytes). No raw download was started and no
runtime estimate is presented as measured. The closure ledger prunes the branch
because raw processing could standardize a descriptive injury-versus-homeostasis
comparison but does not separate injury, sort and state or resolve A1's matched
regulatory-to-fate gap. The regulatory-fate report repeats the prune, noting that
reprocessing approximately 48 GB of histone/H3 reads would still leave
injury/sort/state inseparable
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)).

### B6. PATS measured lineage endpoint

The Kobayashi Extended Data 4 workbook labels the injury fields `BleoD12` and
identifies three named mice per marker. Mean within-mouse field fractions
averaged across three mice reproduce 64.69% KRT8-positive and 32.84%
AGER-positive among alveolar tdTomato-labelled cells
([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)); the per-mouse values are in
[pats_mouse_endpoints.tsv](../tables/lineage/pats_mouse_endpoints.tsv), which
records 12 rows, six injury and six control. Thirty-eight fields were
reconstructed and 18 zero-denominator control fields were excluded from fraction
estimates: their numerator and denominator are both zero despite stored
percentages of zero, so their fractions are undefined and they cannot serve as
zero-percent controls. The published article specifies a Krt19-CreER pulse seven
days after injury and a day-12 harvest, a nominal five-day interval rather than
an estimated transition rate
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)).

### B7. IRE1alpha primary ten-mouse RNA contrast

The frozen contract [ire1_kira8.json](../config/ire1_kira8.json) preceded
expression fitting. The primary model is `~ batch + sex + group` on GSE190821
epithelial RiboTag counts, five vehicle and five KIRA8 mice, with both arms
containing three S061 and two S135 mice and the four Axum8 antibody controls
excluded ([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)).
[fit_summary.tsv](../tables/ire1/fit_summary.tsv) records 42,548 input features,
14,811 tested, design rank four, six residual degrees of freedom, four genes at
FDR 0.05 all lower with KIRA8, and a sex-omitted sensitivity log-fold-change
correlation of 0.999193913654951. None of the eight predefined markers passes the
all-gene BH threshold (Itgb6 -0.811 at FDR 0.143 through Krt7 -0.526 at 0.128),
the TGF-beta set gives 47 genes at BH FDR 0.125 and the general unfolded-protein
set 94 genes at 0.529, while the terminal-UPR set is held at 6/8 source symbols
(75%) below the frozen 80% coverage rule
([gene_set_coverage.tsv](../tables/ire1/gene_set_coverage.tsv),
[gene_set_camera.tsv](../tables/ire1/gene_set_camera.tsv)). PC1 explains 89.5% of
unadjusted sample variance and separates the two batches.

### B8. IRE1alpha omission and batch sensitivity

All ten distinct omissions retain nine mice (4 versus 5), a full-rank four-column
design and five residual degrees of freedom, and each fit retains exactly the
primary 14,811 genes; S061 has three mice per arm with rank three and three
residual degrees of freedom
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md),
[fit_diagnostics.tsv](../tables/ire1_stability_2026-09-25/fit_diagnostics.tsv)).
Seven of eight frozen markers keep their primary direction in all ten omissions
and Ager in nine, with ranges such as Itgb6 -1.016 to -0.683 around a primary
-0.811. Whole-family significant-gene counts range from 1 to 264 across omissions
versus 4 in the primary model, omission Pearson effect correlations are
0.928-0.973, S061 yields 112 discoveries and S135, with two mice per arm,
receives descriptive normalized-CPM ratios with a 0.5 offset and no p-values.
TGF-beta points downward throughout but passes FDR 0.05 only when mouse 148 is
omitted (q=0.04490 versus primary q=0.12463)
([ire1_pathway_comparison.tsv](../tables/second_batch_verified/ire1_pathway_comparison.tsv)).

### B9. IRE1alpha cell-resolved follow-up screen

GSE243124 provides day-10 epithelial scRNA after saline, bleomycin, epithelial
IRE1 knockout or KIRA8, with each group pooled into one GEM library from 2/2/3/3
contributing mice and no recovered donor labels or author cell annotations
([STUDY_MAP.md](../STUDY_MAP.md),
[EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). The ledger records
that deconvolution adds assumptions without fixing the lack of independent
treatment libraries, and that descriptive reproduction of the published
single-cell panel remains possible but cannot fill the inferential gap. The
linked GSE243129 was excluded because it is a neonatal Tgfbr2 knockout/hyperoxia
cohort rather than an IRE1 intervention. The reference map records this as a
prelaunch check rather than an executed analysis
([ANALYSIS_REFERENCE_MAP.md](ANALYSIS_REFERENCE_MAP.md)).

### B10. AP-1 mouse-level regional HOPX response

Numerical values come from the Lynch preprint v2 Fig. 4I source workbook, which
is DC5/media-5.xlsx rather than the similarly named DC9 marker-gene tables
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). There are three mice
per genotype and three fields per mouse in each region; the endpoint sums
HOPX-positive and GFP-labelled counts within each mouse and region and then
weights each mouse equally
([ap1_mice.tsv](../tables/regulatory_fate/ap1_mice.tsv), 12 mouse/region rows).
Group means are 17.30% and 3.63% for wild type in situ and de novo, and 1.24% and
12.12% for the AP-1 mutant, giving differences of -16.06 and +8.49 percentage
points and a genotype-by-region difference of 24.55 percentage points;
equal-field weighting gives 24.27 points
([ap1_group_summary.tsv](../tables/regulatory_fate/ap1_group_summary.tsv),
[ap1_region_interaction.tsv](../tables/regulatory_fate/ap1_region_interaction.tsv)).
All nine leave-one-mouse-per-genotype omissions remain positive, from 19.07 to
27.62 points, and the exhaustive permutation over 20 possible 3-versus-3
allocations gives a two-sided p-value of 0.10, the smallest possible resolution
here. The 26 September interpretation clarification states that the contrast is
descriptive and that the observed opposite directions do not establish a
replicated regional mechanism.

### B11. AP-1 bulk ATAC regulatory context

GSE309751 deposits 14 bulk ATAC GSM records across post-viral time points and a
Kras perturbation, with processed peak calls and SRA relations
([STUDY_MAP.md](../STUDY_MAP.md)). Two 49-day mock-PBS sample titles conflict
with their treatment fields stating Sendai infection, and the affected records
are GSM9278491 and GSM9278492
([metadata/README.md](../metadata/README.md)). Correlating the published
14-day-minus-PBS and 49-day-minus-14-day changes reuses the middle time point
with opposite signs, so a negative correlation alone is not evidence of
biological reversal; that shortcut was not launched and animals were not inferred
from library suffixes ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)).

### B12. HPCS descendant source-composition table

The pinned author code identifies the Figure-2 input as `combined_data.h5ad`, and
a bounded metadata-only read recovered 28,402 observation rows using 7,405,568
transferred bytes in 113 byte-range requests over 158.61 seconds from an
8,045,265,618-byte object
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md),
[hpcs_metadata_recovery.json](hpcs_metadata_recovery.json)). Under
[hpcs_descendant_reconstruction.json](../config/hpcs_descendant_reconstruction.json)
the reconstruction retains 5,333 author-designated traced cells, 22 source labels
and all eight RNA-state categories, and reproduces group totals, 11 early HPCS
fractions and four Hopx means. Group values are 586 cells at 93.08% equal-source
and 92.83% cell-pooled HPCS for Slc4a11 6wk_3d, 742 at 24.00% and 23.99% for 8wk,
877 at 67.86% and 66.82% for 12wk_3d, 991 at 43.73% and 31.79% for 14wk, 1,226 at
4.77% and 4.81% for Hopx_12wk3d, and 911 at 4.32% and 3.84% for Hopx_12wk14d
([group_descriptive_summary.tsv](../tables/hpcs_source_composition/group_descriptive_summary.tsv),
48 rows). One source supplies 811 of the 991 cells in the 14wk group, current
mScarlet is absent from the traced observation rows, and the 22 source labels
must not be promoted to 22 independent animals.

### B13. HPCS alias-to-mouse verification

Joining the exact tag component of each author-demultiplexed alias to
Supplementary Table 4's `Mice` sheet resolves 22 distinct animals and all 5,333
retained traced cells, with library and driver agreeing for every join
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md);
[hpcs_mouse_crosswalk.tsv](../tables/regulatory_fate/hpcs_mouse_crosswalk.tsv)
has 22 rows carrying mouse tag, group, library, GSM, driver, chase, harvest week,
sex and three genotype fields). The retained groups contain 5/4 Slc4a11 mice at
the early 3/14-day chase, 6/3 at the late chase and 2/2 Hopx mice. Four
additional animals listed for these experiments lack a retained traced alias in
the recovered subset: BO1534, BR1311, BL1241 and BH1719, recorded without
assigning an exclusion mechanism or a zero-cell outcome. Sex and reporter dosage
vary between groups, with one male and four females in the early 3-day retained
Slc4a11 group versus three males and one female at the 14-day chase, and the
previously established library/chase rank deficiency is unchanged
([hpcs_named_mouse_summary.tsv](../tables/regulatory_fate/hpcs_named_mouse_summary.tsv)).

### B14. Hopx harvest-timing reconciliation

For Hopx IGO17543, `Mice!A90:M92`, the main Fig. 2 tracing design and GEO agree
on a 14-week harvest following induction at 12 weeks and a 14-day chase, which
supersedes the old README's 12-week-harvest wording
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). The separate 3-day
harvest-week labels are rounded study labels rather than exact chronological ages
calculated from dates of birth. The earlier second-batch record had noted that
the README said 12 weeks while GEO said 14 weeks, and that the code's `12wk14d`
label did not settle the discrepancy
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). Related age handling remains
flagged rather than harmonized: the generic `time` field for Hopx_12wk3d inherits
`6wk_3d` from its mixed sequencing lane, and the 8wk/14wk Slc4a11 harvest labels
correspond to 6wk/12wk induction labels in the figure code
([source_manifest.tsv](../tables/hpcs_source_composition/source_manifest.tsv)).

### B15. HPCS annotation partition and confidence-abstention audit

Both previously oversized notebooks were retrieved at 69,091,594 and 49,691,834
bytes from pinned commit `b52d53c984e21d3bb3a163041fdb3f56b54c19c0`, with git
blob hashes and lengths matching and only cell source text extracted
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). Notebook 01 cell 142
maps `newleiden` to the eight biological labels and reproduces all 28,402
deposited labels including all 5,333 traced cells, while cell 116 sets
`clusterK12_stringent` to `other` unless classifier confidence is at least 0.8.
Every one of the 1,282 traced-cell changes (24.04%) is an abstention and none
switches between retained K12 codes; across the whole object all 11,133 changes
are also abstentions
([hpcs_annotation_audit.tsv](../tables/evidence_closure/hpcs_annotation_audit.tsv)).
Abstention is uneven at 146/1,717 HPCS-labelled cells (8.50%), 538/1,277 AT2-like
cells (42.13%) and 331/531 lung-endoderm-like cells (62.34%)
([hpcs_abstention_summary.tsv](../tables/evidence_closure/hpcs_abstention_summary.tsv),
36 rows). The robustness batch reports label-invariant agreement over all 5,333
cells as ARI 0.6331 for `cell type` versus `clusterK12`, 0.5723 versus
`clusterK12_stringent` and 0.7148 between the two cluster fields, across 87
partition comparisons ([ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md)).

### B16. HPCS source-influence sensitivity

Each of the 22 sources was omitted once within its group across three annotation
fields, giving 22 distinct source omissions, 704 source/category omission rows
and 192 group/category summaries, with no cells resampled as independent animals
and no p-values calculated ([ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md)).
Equal-source omission ranges are 92.24-93.98% (6wk_3d), 22.74-25.72% (8wk),
65.78-72.12% (12wk_3d), 38.54-51.84% (14wk), 3.98-5.56% (Hopx_12wk3d) and
2.00-6.65% (Hopx_12wk14d); cell-pooled ranges are 92.50-93.33%, 23.22-25.17%,
62.54-73.42%, 29.36-51.11%, 3.98-5.56% and 2.00-6.65%. Omitting
`BF1303_B0301_GFP+`, which supplies 811/991 cells in the 14wk group, raises the
pooled HPCS fraction from 31.79% to 51.11% among the remaining 180 cells and the
equal-source fraction from 43.73% to 51.84%. The Hopx groups have only two source
aliases, so each omission leaves a single source
([leave_one_source_out.tsv](../tables/robustness_2026-09-25/hpcs/leave_one_source_out.tsv)).

### B17. HPCS design identifiability

The source-level design audit uses the existing 22 source aliases and six
libraries, and every library contains only one chase interval
([ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md)). Adding chase to unrestricted
library indicators adds zero rank: 6 to 6 overall, 5 to 5 within Slc4a11 and 2 to
2 within Hopx, so the proposed library-adjusted chase coefficient is not
separately estimable; driver adds one algebraic dimension overall (6 to 7),
supported by the mixed IGO17402 library
([design_rank_audit.tsv](../tables/robustness_2026-09-25/hpcs/design_rank_audit.tsv),
six rows with `independent_biological_units_verified` false throughout). The
library/group support table records the seven library-group rows and their
retained-cell counts, including IGO17402 contributing to both a Slc4a11 and a
Hopx group
([library_group_support.tsv](../tables/robustness_2026-09-25/hpcs/library_group_support.tsv)).
A model omitting or constraining library effects would require additional
assumptions and none was fitted.

### B18. TIGIT paired bulk ATAC

GSE154966 deposits eight bulk ATAC GSM records with counts and merged peaks
across four apparent TIGIT-positive/negative source blocks
([STUDY_MAP.md](../STUDY_MAP.md)). The published article describes four mouse
replicates and a paired `~ Mouse + Tigit_status` analysis, but the sample and
experiment XML repeats `106621_106642` without an explicit pool-membership or
non-overlap statement against YY1181, YY1916 and 106623
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). The closure pass recovered
original sort and source filenames from all eight SRA full records without adding
pool membership, and the previously uninspected 2020 author repository was pinned
and inspected but provides single-cell computational methods rather than the
needed ATAC pool crosswalk
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md),
[REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). No paired inference was
fitted and the required input is drafted in
[SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md).

### B19. Tsutsui regulatory perturbation library identities

Full DDBJ SRA records identify all 64 Tsutsui runs as 26 inhibitor CUT&Tag, 32
organoid CUT&Tag and six fibroblast RNA libraries
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md);
[tsutsui_sequencing_crosswalk.tsv](../tables/regulatory_fate/tsutsui_sequencing_crosswalk.tsv)
has 64 rows with project, experiment, run, biosample, title, antibody,
biological replicate and treatment). PRJDB37980 covers DMSO, CBP30 and GNE781
across two CUT preparations and H3, H3K27ac, H3K4me3 and H3K27me3 plus two DMSO
p300 libraries; PRJDB37983 covers 32 epithelial organoid libraries spanning
DMSO/BLM, days 14/17 and inhibitor conditions; PRJDB37982 covers NHLFs alone or
with iATCs at three author-declared biological preparations per condition. The
published Fig. 8/9 track captions specify E. coli DNA normalization, which
differs from the deposited baseline CPM tracks analyzed earlier in A1, so
absolute amplitudes must not be compared. No scaled per-replicate signal matrix,
peak-count matrix or spike-in factors were recovered, and no raw sequencing was
downloaded.

### B20. Tsutsui culture endpoints and program suppression

The source reconstruction checks 317 measurements across 65 endpoint/condition
summaries against the workbook's averages and sample standard deviations
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md);
[tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv)
has 65 rows across panels 6c, 6d, 6g, 6h, 6i, 9d, 9f and 9g, with
`unit_of_replication` recorded as author-declared independent culture experiments
from one parental iPSC line). After medium switching, iATC-derived cultures show
a 229.88-fold mean SFTPC increase under AT2 induction and a 33.32-fold mean AGER
increase under AT1 induction relative to day-zero population values, and the AGER
HiBiT reporter is 158.45-fold higher in AT1 versus AT2 induction from iATC origin
with three experiments per condition
([tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv),
28 rows). In separate siRNA experiments ITGB6 averages 0.455 of siCont after ATF3
knockdown and 0.319 after HNF1B knockdown, and KRT17 averages 0.369 and 0.192;
AP-1 inhibitors give mean normalized gel-contraction inhibition of 59.64% and
57.89% in three experiments. The workbook spells the first compound `SR11392`
while the figure and methods identify SR11302, the table preserves the original
label, the workbook repeats an adult-lung-ratio heading above luminescence values
whose absolute unit is left unspecified, and normalized siCont entries of 1 and
contraction anchors of 0/100 were not treated as measured zero-variance controls.

### B21. Tsutsui predicted regulatory gene-set audit

Supplementary Data 2 contains 325 shared predicted AP-1/HNF1B-associated genes
and a supplied 126-gene RNA-upregulated subset, all 126 of which are in the
shared set ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). The
HNF1B-only column has 317 rows but 313 unique genes because ZNF608, ZNF609,
ZNF710 and ZNRF3 each occur twice; raw row memberships are preserved and unique
counts are reported separately in
[tsutsui_gene_set_audit.tsv](../tables/regulatory_fate/tsutsui_gene_set_audit.tsv),
which also records 1,339 rows and 1,339 unique genes for the ATF3-unique set. The
first numerical launch stopped before writing results when an assumed unique-gene
count exposed the four duplicate HNF1B symbols, and the corrected audit preserves
those source rows explicitly. These are author-selected predictions from existing
DiffBind, HOMER and GREAT analyses, not a binding assay performed here.

### B22. TP53 / Mdm2 source-list direction audit

The Morowitz preprint reports AT1-specific Mdm2 perturbation, lineage tracing and
live imaging, and compares AT1- and AT2-origin RNA responses; its supplied
selected differential-expression table was audited even though GSE335749 and
GSE335750 are private ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)).
[tp53_accessibility.tsv](../tables/regulatory_fate/tp53_accessibility.tsv)
records both accessions as private with a scheduled release of Jun 01, 2027 and a
manuscript claim of publicly available, checked at 2026-09-25T10:38:03.676483+00:00.
The paper's table description calls 3,984/686/868 genes upregulated, whereas the
signed values give 2,049 increased and 1,935 decreased in the AT2-origin-only
set, 245 and 441 in the AT1-origin-only set, and 493 increased in both, 266
decreased in both and 109 opposite in the shared set
([tp53_signed_set_summary.tsv](../tables/regulatory_fate/tp53_signed_set_summary.tsv),
seven rows). Cldn4 and Cdkn1a increase in both supplied contrasts, and no
enrichment analysis, independent differential-expression fit or causal regulatory
claim was made from selected lists without the full tested universe.

### B23. CD44 eight-mouse paired contrasts and genotype interaction

Sixteen NCBI SRA full records retain original FASTQ filenames that connect the
count matrix's R26/OG identifiers and CD44 gates to exact GSM records, with the
only spelling normalization being `R26_1` to `R261` and likewise 2/7/8, giving a
one-to-one join and four paired mice per genotype
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md);
[cd44_sample_manifest.tsv](../tables/evidence_closure/cd44_sample_manifest.tsv)
has 16 rows). In `~0 + mouse + positiveWT + positiveMutant` the interaction is
`positiveMutant - positiveWT`, the design has rank 10 with 16 libraries and six
residual degrees of freedom, and genotype main effects cannot be estimated
separately from the mouse intercepts
([contrasts.tsv](../tables/cd44_closure/contrasts.tsv),
[fit_summary.tsv](../tables/cd44_closure/fit_summary.tsv)). From the deposited raw
integer matrix 15,516 genes survive the shared `filterByExpr` rule, TMM factors
span 0.897-1.084, raw library totals span 9.02-21.36 million counts and no mouse
was removed; per-contrast FDR<0.05 counts are 6,615, 8,739 and 5,023 and pooled
three-contrast counts are 6,659, 8,480 and 5,321 over 46,548 gene-contrast tests.
Seven of the eight transported IRE1 marker genes change significantly in both
genotypes with Itgb6, Krt8, Krt19, Cldn4, Cdkn1a and Krt7 increasing and Sftpc
decreasing while Ager passes neither contrast; four interactions are detected
(Cldn4 -1.722 at pooled q 3.39e-13, Krt19 -0.483 at 5.55e-8, Sftpc -0.239 at
0.0251, Krt7 +0.198 at 0.0191, with Cdkn1a +0.157 at 0.0559), and all seven
shared directions and all four interaction directions persist in all eight
leave-one-pair-out fits, although Sftpc's interaction shrinks from -0.239 to
-0.0046 after removing WT2
([focus_effects.tsv](../tables/cd44_closure/focus_effects.tsv),
[cd44_focus_stability.tsv](../tables/closure_verification/cd44_focus_stability.tsv)).

### B24. One-donor methylation-domain reference

All 414 domain intersections were independently reconstructed with per-base
boolean unions from one donor at D0, D4 and D6, using separate hg19 annotation
and +/-1-kb promoters
([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md);
[methylation_domain_overlap.tsv](../tables/direct_marks_2026-09-25/methylation_domain_overlap.tsv)
has 414 rows carrying gene, gene group, day, domain class, coordinates, the
coordinate assumption and the overlap fraction). Author starts at 1 suggest
one-based inclusive intervals, the metadata do not conclusively establish this
convention, and the alternative BED interpretation changes an overlap fraction by
at most 0.0005, one base in a 2,000-base window. UMR, LMR and PMD overlap is
genomic context rather than promoter-wide CpG methylation, the classes are
displayed separately and need not partition a promoter, and segment methylation
summaries present in some source tables were not used to estimate promoter
methylation. GSE150527's WGBS has only one donor at D0/D4/D6 and D4 is mixed
cultured AT1-like differentiation rather than a purified transitional population
([STUDY_MAP.md](../STUDY_MAP.md)).

### B25. Descriptive deposited-source profiles

The first batch completed an integer-count audit and sample PCA for GSE154966
(112,729 features, eight libraries, four deposited source aliases) and GSE273123
(27,179 features, 16 libraries, eight deposited source aliases)
([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)). The gallery records that the
PCA uses deposited integer counts after CPM and log2 transformation with 2,000
variable features and that lines connect literal source aliases
([figures/README.md](../figures/README.md)). At the time of the run ATAC pool
independence and the CD44 alias-to-genotype mapping were both unresolved; CD44
identities were subsequently recovered (B23) while TIGIT pooling remains
unresolved (B18). Coordinates and labels are retained in
[GSE154966_source_PCA_QC.tsv](../tables/descriptive/GSE154966_source_PCA_QC.tsv)
and
[GSE273123_source_PCA_QC.tsv](../tables/descriptive/GSE273123_source_PCA_QC.tsv).

### B26. Independent direct-mark comparator screen

GSE150527 deposits 48 GSM records covering histone marks, FAIRE, CTCF, RNA and
WGBS across human AT2-to-AT1 culture, with three donor labels for RNA, two for
selected histones and one donor for WGBS at D0/D4/D6
([STUDY_MAP.md](../STUDY_MAP.md)). The closure screen found donor-matched input
and H3K27ac BigWigs across the three days but catalog text describing aligned
BigWigs without specifying their quantitative scale, so a quantitative comparison
was not made eligible; donor 2 provides published enhancer replication and D4 is
not a purified injury transitional population
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). The existing
one-donor methylation-domain context is retained and is explicitly not replicated
DMR evidence. The required input is verified track scaling plus an appropriate
state definition.

### B27. SAGE perturbation deposition

The SAGE Perturb-seq preprint is recorded as a literature anchor providing
time-resolved transcription-factor perturbation and repair/pathological
epithelial branches, with version 1 promising deposition and no new public
accession verified ([STUDY_MAP.md](../STUDY_MAP.md)). The reference map records
the current-text check: data and code availability still promise future
deposition, so the source is used as a literature hypothesis rather than an
executed or independently verified analysis
([ANALYSIS_REFERENCE_MAP.md](ANALYSIS_REFERENCE_MAP.md)). The closure ledger
keeps the branch on a public-input hold pending published processed data, guide
and sample identities, and an animal-level design
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). Human reference
accessions cited in that preprint are not its new perturbation data.

## Pruned or closed analyses and their closing reasons

Each entry copies the closing reason recorded in the cited document, with
markdown emphasis removed.

| Analysis | Closing reason (copied wording) | Source |
|---|---|---|
| PATS raw reprocessing | "Pruned from this discriminating sequence: deposited original files total 54.86 GB (48.01 GB for 16 histone/H3 libraries), before reference/alignment storage. Raw processing could standardize a descriptive injury-versus-homeostasis comparison, but does not separate injury, sort and state or resolve A1's matched regulatory-to-fate gap." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| Independent direct-mark comparator (GSE150527) quantitative comparison | "Context screen complete; quantitative comparison not eligible: GSE150527 has donor-matched input and H3K27ac BigWigs across D0/D4/D6, but catalog text says aligned BigWigs without specifying their quantitative scale." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| IRE1 cell-resolved follow-up and bulk deconvolution | "Design screen complete; replicate-level test not eligible: GSE243124 pools 2/2/3/3 mice into one GEM library per saline/KO/KIRA8/bleomycin condition. No recovered donor labels or author cell annotations. Deconvolution adds assumptions without fixing the lack of independent treatment libraries." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| GSE243129 as another KIRA8 experiment | "Excluded: the linked accession is neonatal Tgfbr2 knockout/hyperoxia, not an IRE1 intervention cohort." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| New SAGE perturbation analysis | "Public-input hold: current primary text still promises later GEO/Single Cell Portal/code deposition; no new accession was verified in this bounded check." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| More embeddings, pooled cross-study DE, marker-derived "validation", repeated IRE1 fits | "Unnecessary for the remaining questions: they reuse dependent evidence or change the estimand without resolving the recorded gaps." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| Universal epigenetic taxonomy / regulatory causality / same-cell fate linkage | "New measurements or a suitable independent cohort required. Histone, lineage and intervention observations currently come from different experiments." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| HPCS driver-excluded label recomputation (notebook 02 `cell type_noSH`) | "Recomputing them would require the expression/model workflow and would still be same-data annotation sensitivity. It cannot resolve mouse/pool identity, current mScarlet protein, chase/library aliasing or the IGO17543 age discrepancy. Accordingly, it is not needed to close the independent-validation question." | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md) |
| HPCS semantic cluster recoding into an alternative HPCS fraction | "Semantic recoding of cluster categories into an alternative HPCS fraction stays held." | [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md) |
| Library-adjusted HPCS chase contrast | "Thus the proposed library-adjusted chase coefficient is not separately estimable. A model omitting or constraining library effects would require additional assumptions; none was fitted." | [ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md) |
| AP-1 adjacent-time peak-correlation shortcut | "correlating the published 14-day-minus-PBS and 49-day-minus-14-day changes reuses the middle time point with opposite signs; negative correlation alone is not evidence of biological reversal. We did not launch that shortcut" | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md) |
| Repeated cell-level tests and refits of completed CD44/IRE1 models | "Repeating cell-level tests, refitting already completed CD44/IRE1 models, or adding adjacent-time peak correlations would not resolve these requirements." | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md) |
| Complete-archive IMC download and re-segmentation | "Complete-archive IMC download/re-segmentation is removed from the initial execution scope." | [PLAN.md](../PLAN.md) |
| Biological peak-overlap figure for GSE141635 | "No biological peak-overlap plot was made for GSE141635: the deposited histone calls use incompatible region settings." | [figures/README.md](../figures/README.md) |
| Packages 1-2 of the earlier remaining-options queue | "The table below is historical rationale, not a remaining execution queue." and "Do not repeat packages 1-2 merely to obtain the same evidence." | [REMAINING_ANALYSIS_OPTIONS.md](REMAINING_ANALYSIS_OPTIONS.md) |
| A1 linked regulatory/fate comparison, at repository level | "Hold the linked regulatory/fate comparison" with the evidence needed being "Early regulatory and RNA measurements linked to independent later fate at clone/animal/preparation level; RNA-only replacement does not qualify" | [docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md](../../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md) |

## Remaining external requirements

The regulatory-fate report's final table is the current list of external
requirements and is not reproduced or reworded here; the open questions it lists
are paired TIGIT inference, HPCS current-state retention or adjusted chase
effect, PATS histone-amplitude comparison, quantitative inhibitor chromatin
effect, origin-specific TP53 interaction and causal regulation-to-fate mediation
([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). Prepared but unsent
requests for those inputs are in
[SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md).
