# Mature epithelial outcome inventory for A1, A8 and A14

Prepared 28 September 2026 as a documentation pass. No analysis was run and no
dataset searched. Every entry is copied from a document or table in this A1
folder or from the canonical register cards for A1, A8, A10 and A14, and each row
names its source. Values are reproduced at the precision of the source.

Corrected 29 September 2026 after the delivery review.

Purpose and reading rule. These **29 records** include measured mature endpoints,
contextual or non-mature readouts, inaccessible source material and unmet
requirements. They are not 29 measured mature outcomes. The status column
distinguishes what is measured or available; biological-unit verification,
timing, predictor linkage and endpoint eligibility are separate columns.
A published endpoint is not necessarily numerically recovered here, and a
measured endpoint is not necessarily linked to the required predictor.

A1 requires early regulatory **and** RNA measurements linked to a later mature
endpoint. A8 can test incremental association with a concurrent independently
measured mature endpoint, or prospective prediction with earlier RNA; either
requires compatible linked biological units and a noncircular endpoint. A14
requires the relevant exposure/reception contrast, withdrawal timing and
viable traced mature output. Availability of an endpoint type alone satisfies
none of those complete contracts. No new dataset search or analysis was run.

Companion document: [A1_BRANCH_INVENTORY.md](A1_BRANCH_INVENTORY.md).
Register cards read from the canonical register:
[A1](../../../RESEARCH_QUESTIONS.md#a1), [A8](../../../RESEARCH_QUESTIONS.md#a8),
[A10](../../../RESEARCH_QUESTIONS.md#a10),
[A14](../../../RESEARCH_QUESTIONS.md#a14). Unit rules:
[MC1](../../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC5](../../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

## Outcome table

| Outcome | Record status / current coverage | Dataset or study | Assay layer | Biological unit and n | Timing | Predictor linkage and timing | Question-specific use / limits | Source |
|---|---|---|---|---|---|---|---|---|
| O1. KRT8-positive fraction among alveolar tdTomato-labelled cells | Measured; transitional fraction reanalysed | Kobayashi PATS, Extended Data 4 source workbook (reanalysed here) | Imaging plus lineage label (protein immunostain on genetically labelled cells) | Three explicitly named mice; fields nested within mouse; four, three and four fields | Krt19-CreER pulse 7 days after bleomycin, harvest day 12 | No. Chromatin in that study comes from a separate day-12 CTGF-positive sort and a separate day-8 TP53 sort, not these animals | Partly. KRT8 is a transitional rather than mature marker, so it is an entry or persistence readout; it is noncircular with respect to chromatin but not with respect to a KRT8-containing RNA panel | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [pats_mouse_endpoints.tsv](../tables/lineage/pats_mouse_endpoints.tsv) |
| O2. AGER-positive fraction among alveolar tdTomato-labelled cells | Measured; mature fraction reanalysed | Kobayashi PATS, Extended Data 4 (reanalysed here) | Imaging plus lineage label | Three explicitly named mice; three fields each | Same pulse day 7, harvest day 12 | No, same reason as O1 | Yes in principle: AGER is a mature AT1 marker measured as protein on labelled cells, independent of any RNA predictor panel. No early measurement exists in these three mice | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [pats_source_fields.tsv](../tables/lineage/pats_source_fields.tsv) |
| O3. Day-14 labelled-cell AGER endpoint under KIRA8 | Published measurement; numerical source/units not fully recovered | Auyeung 2022 (published; not reanalysed numerically here) | Imaging plus lineage label under perturbation | Not recorded in this folder as a verified unit count | Krt19-CreERT2 pulse on injury days 3-4, day-14 endpoint | Partial. The same study deposits day-7 epithelial RiboTag RNA (GSE190821), but those are different experimental units from the microscopy mice | Yes as an endpoint type; not yet as a linked endpoint, because the RNA and microscopy experiments are not the same animals | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md) |
| O4. Epithelial IRE1alpha integrin and TGF-beta measurements (profibrotic function) | Published assay; local numerical inputs absent | Auyeung 2022 (published) | Protein and function, as described by the source study | Not recorded in this folder | Source-study design | No | Not as recorded here: the folder does not hold its numerical values, units or timing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O5. HOPX-positive fraction among GFP-labelled cells, injured in-situ regions | Measured; HOPX fraction reanalysed | Lynch AP-1 preprint v2 Fig. 4I source workbook (reanalysed here) | Imaging plus lineage label | Three mice per genotype, three fields per mouse per region | Microscopy endpoint of the source design | No. The same study's mutant RNA/ATAC experiment has one pooled library per condition and cannot be paired to these microscopy animals | Yes as a differentiation readout on labelled cells. The report states it measures HOPX acquisition, not completed functional AT1 differentiation | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ap1_mice.tsv](../tables/regulatory_fate/ap1_mice.tsv) |
| O6. HOPX-positive fraction among GFP-labelled cells, intact de-novo regions | Measured; HOPX fraction reanalysed | Lynch AP-1 preprint v2 Fig. 4I (reanalysed here) | Imaging plus lineage label | Three mice per genotype, three fields per mouse per region | Same microscopy endpoint | No, same reason as O5 | Yes, with the same limit; region is a context axis that changes the direction of the genotype effect | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ap1_group_summary.tsv](../tables/regulatory_fate/ap1_group_summary.tsv) |
| O7. Medium-switch AT2 differentiation capacity (SFTPC, NAPSA, SLC34A2 induction) | Measured; RNA differentiation readout reanalysed | Tsutsui 2026 Fig. 6c/6d source workbook (reanalysed here) | RNA (qPCR ratio to adult lung) | Author-declared independent culture experiments, n=7 at day zero and n=6 after switching; one parental iPSC line | Medium switch from culture day zero | No. Chromatin was measured in separate CUT&Tag preparations of the same study, and cross-panel pairing is not assumed | Partly. The layer is RNA, so it is circular against an RNA predictor panel containing the same markers; it is noncircular against a chromatin predictor if preparations were linked, which they are not | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv) |
| O8. Medium-switch AT1 differentiation capacity (AGER, CLIC5, RTKN2 induction) | Measured; RNA differentiation readout reanalysed | Tsutsui 2026 Fig. 6g/6h (reanalysed here) | RNA (qPCR ratio to adult lung) | n=7 at day zero, n=5 after switching; one parental iPSC line | Medium switch from day zero | No, same reason as O7 | Partly, same reason as O7 | [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O9. AGER HiBiT reporter luminescence under AT1 versus AT2 induction | Measured; reporter values reanalysed | Tsutsui 2026 Fig. 6i (reanalysed here) | Reporter luminescence; absolute unit unspecified in the source workbook | Three experiments per condition; derived reporter lines add no independent donor | After medium switch | No | Partly. It is a reporter rather than an RNA panel, so less circular than O7/O8, but the descriptive-ratio table labels it AGER reporter induction, not mature AT1 function | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O10. Normalized gel-contraction inhibition by AP-1 inhibitors | Measured; contraction values reanalysed | Tsutsui 2026 Fig. 9d (reanalysed here) | Function (contraction assay); DMSO and BLM anchors are 100 and 0 by construction | Three experiments per condition | Inhibitor-treated culture | No | Yes as a function readout, but it is a co-culture contraction phenotype rather than a mature epithelial outcome, and the anchors are not measured zero-variance controls | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv) |
| O11. siRNA suppression of transitional markers (ATF3, HNF1B, TP63, MMP7, ITGB6, KRT17, COL1A1) | Measured; RNA suppression reanalysed | Tsutsui 2026 Fig. 9f/9g (reanalysed here) | RNA relative to siCont | n=3 or n=4 per condition; one parental iPSC line | Separate siRNA experiments | No | No. This is transitional-program suppression, not a mature outcome; the report states it does not show rescue of the fate of the same cells followed in the medium-switch assay | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O12. HPCS descendant AT1-like and AT2-like RNA-state fractions among traced cells | Measured; RNA-state composition and animal identities recovered | Chan 2026 HPCS, GSE277777 observation metadata (reanalysed here) | RNA state label on trace-sorted cells | 5,333 retained traced cells from 22 distinct animals verified against Supplementary Table 4, across six deposited groups; cells are not biological replicates | Slc4a11 and Hopx tracing in established KP tumours; 3-day and 14-day chase | No separate early measurement: the putative predictor and outcome are RNA labels on the same cells | Not a linked later mature endpoint. Mouse identities are resolved, but library/chase confounding and missing current mScarlet remain; fractions are not cell-production or transition rates | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [hpcs_mouse_crosswalk.tsv](../tables/regulatory_fate/hpcs_mouse_crosswalk.tsv) |
| O13. HPCS growth reporters and selective ablation | Source workbook inventoried; endpoints not fitted | Chan 2026, source workbook panels from Figures 3, 4 and Extended Data 10 (inventoried, not fitted) | Growth reporter and ablation outcome | Not resolved in this folder; some scRNA conditions pool two mice | Source-study tumour timeline | No | Not as recorded here. The lineage audit states the workbook supplies growth and ablation panels rather than the Figure-2 lineage fractions, and that ablation tests population dependency rather than a chromatin mechanism | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O14. HPCS current mScarlet reporter-positive state | Measurement absent from recovered traced rows | Chan 2026 GSE277777 (absent) | Would be current-state reporter protein | Not available for traced rows | Same tracing design | No | No. Current mScarlet status is absent from the traced observation rows, so permanent lineage inheritance cannot be distinguished from ongoing reporter-positive state | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md) |
| O15. CD44-sorted fibroblast-response assays (profibrotic capability) | Published functional measurement; linkage unverified | Rodriguez 2025 CD44 study (published) | Function (conditioned-medium fibroblast response) | Not recorded in this folder as a verified unit count | Source-study model | Partial. The same study deposits the 16-library sorted RNA matrix, now identity-resolved to eight mice, but the folder does not record whether the functional assays used those same animals | Yes as a function readout; the lineage audit states that expression of mediators is not the conditioned-medium response itself, and that CD44 sorting is not lineage tracing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O16. CD44-sorted mature and transitional marker RNA (Sftpc, Ager and six others) | Measured; marker RNA reanalysed | GSE273123 (reanalysed here) | RNA (sorted bulk) | Eight mice, four paired per genotype, 16 libraries | Same harvest; no explicit injury time axis in the count matrix | Same-library RNA is available, but there is no separate earlier predictor measurement | No independent mature endpoint. Same-assay, same-library measurement; Ager passes neither contrast and Sftpc's interaction is fragile | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [focus_effects.tsv](../tables/cd44_closure/focus_effects.tsv) |
| O17. DATP day-28 differentiated descendants | Published descendant endpoint; local units unverified | Choi 2020 (published) | Lineage label plus marker phenotype | Not recorded in this folder | Day-9 transitional populations and day-28 differentiated descendants | No | Yes as an endpoint type. The lineage audit notes that AT1 contribution and labelled AT2 descendants are distinct endpoints and that exact induction schedules are figure-specific and must be transcribed before quantitative comparison | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O18. DATP organoid reformation and IL-1beta manipulation | Published formation/growth assay; local units unverified | Choi 2020 (published) | Organoid formation and growth under perturbation | Not recorded in this folder | Source-study culture design | No | Partly. The lineage audit states that organoid capacity is not an in-vivo single-cell reversal measurement | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O19. Origin convergence among Krt8-high alveolar cells | Published origin readout; not mature output | Strunz 2020 Fig. 7 (published) | Lineage label | Two mice per lineage and multiple sampled regions | Sftpc-CreERT2 and Sox2-CreERT2 induced before injury with washout | No | No as a later mature outcome: it measures labelled origin among transitional cells, which the lineage audit keeps separate from descendant composition. Regions cannot become biological replicates, and two driver experiments do not form a jointly calibrated mixture fraction | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O20. Human AT2 organoid transplantation into injured mice; alveolar versus basal output | Published graft-output measurement; linkage unverified | Kathiriya 2022 (published) | Imaging, morphology and graft-origin nuclear labelling | Not recorded in this folder | Culture and transplantation timeline of the source study | No | Partly. The lineage audit records it as experimental conversion capacity and niche dependence, not endogenous human lineage tracing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O21. Transitional-state accumulation under Krt8 genetic perturbation | Published RNA time course; unit verification pending | Krt8 perturbation study 2023, GSE223302 (published; not fitted here) | RNA (bulk time course) | 24 bulk-RNA GSM library records, WT and KO time course; replicate verification pending | Injury time course | No | No. A changed state frequency can reflect altered entry, proliferation, survival or exit, and the lineage audit states it is not automatically a measured lineage-transition rate | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O22. AT1-specific Mdm2 perturbation with lineage tracing and live imaging | Published tracing/imaging; required inputs inaccessible at recorded audit | Morowitz TP53 preprint (published; inputs private) | Lineage label and live imaging | Not recorded; no biological sample manifest recovered | Source-study design | No. Only selected signed differential-expression lists are available | No at present. GSE335749 and GSE335750 are private with a displayed scheduled release of Jun 01, 2027, and mouse-level lineage or imaging counts with nested-field IDs were requested but not obtained | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tp53_accessibility.tsv](../tables/regulatory_fate/tp53_accessibility.tsv) |
| O23. BHT injury, AT1 ablation and AT2 Mdm2 deletion topology and mechanics | Published imaging/mechanics; local endpoint inputs unbound | Konkimalla 2023; GSE218665, GSE218666, GSE235212 (published) | Imaging, tissue topology and mechanics | 2, 4 and 1 GSM respectively; one sample per time is descriptive | Source-study injury and perturbation timelines | No | No as recorded. The study map states that deposits alone do not encode every imaging or fate endpoint and that shared external controls are not new independent cohorts | [STUDY_MAP.md](../STUDY_MAP.md) |
| O24. Cell protein abundance, morphology and neighbourhood in IPF tissue | External imaging named; not acquired | IPF regenerating-niche atlas 2025; Zenodo 10930946 (not acquired) | Imaging mass cytometry, 33 channels | 22 MCD files, approximately 15.55 GB; 22 files are not 22 donors | Cross-sectional pathology stages | No | No as recorded. The plan makes IMC an optional phenotype and context extension that cannot validate ancestry, reversibility or epigenetic memory, and requires a donor and ROI crosswalk first | [STUDY_MAP.md](../STUDY_MAP.md), [PLAN.md](../PLAN.md) |
| O25. Regional epithelial protein abundance over fibroblastic foci | Project metadata only; processed measurements unverified | MUC5B regional proteomics 2025; PXD058626 (project metadata verified only) | Laser-capture microdissection mass spectrometry | Donor and region map unverified; measures a regional mixture rather than a single cell | Cross-sectional | No | No as recorded. Processed abundance matrix and donor-region map remain unverified, and mixtures are not a purified transitional-cell proteome | [STUDY_MAP.md](../STUDY_MAP.md) |
| O26. Organoid size (A10) | Measured; imaging/RNA analysed, preparations unresolved | GSE307112 organoid screen (reanalysed here) | Imaging (organoid mean area), with RNA predictors | 885 analysed wells in 15 deposited plate-replicate groups across four plates; 886 GEO records; independent preparations remain unidentified | Day-14 area conditional on day-7 area; RNA at day 14 | RNA and outcome are concurrent in the same well; only baseline imaging is earlier and is itself post-perturbation | Supports A10 concurrent size association within the recorded design. Not a later outcome for an early-RNA test, a mature AT1 contribution endpoint for A8, or withdrawal/reception recovery for A14; biological preparation identity remains unresolved | [A10 endpoint statement](../../A10_organoid_growth_outcome/reports/ENDPOINT_TIMING_UNITS_2026-09-28.md), [A10 follow-up](../../A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md) |
| O27. Eligible linked mature AT1 endpoint dataset (A8 requirement) | Requirement; no eligible linked dataset identified | No eligible linked dataset identified in the surveyed evidence; measured endpoint types already exist in O2/O3 | Protein, morphology or genetic lineage label; independently measured from RNA components | Requires verified independent animals or other explicitly justified biological units; O2 has three named mice | Specified timing for association; earlier predictor for prospective prediction | Compatible RNA components and mature endpoint have not been identified in the same biological units | Missing linkage/eligibility, not the endpoint measurement category. Freeze the shared/disjoint components and use an independently measured endpoint; score-versus-score comparisons do not qualify | [A8 register card](../../../RESEARCH_QUESTIONS.md#a8), [A8 plan](../../A8_maturation_component_at1_contribution/PLAN.md), O2/O3 above |
| O28. Mature-cell yield, viability, traced descendants and function after IL-1beta withdrawal (A14 requirement) | Requirement; no eligible recovery dataset identified | No eligible recovery dataset identified in the surveyed evidence; A14 remains unexecuted | Lineage label, viability, protein and function | Requires independent animals or culture preparations with identities | Comparable post-withdrawal intervals with time-matched controls | The relevant exposure/reception comparison is not linked to eligible recovery observations in the reviewed record | Existing or author-provided data may qualify if the full contract is met; new data generation is not established as necessary. Loss of a transitional score cannot distinguish maturation, reversion, death or replacement | [A14 register card](../../../RESEARCH_QUESTIONS.md#a14), [A14 plan](../../A14_withdrawal_recovery_and_reception/PLAN.md) |
| O29. EdU incorporation or label retention | Assay coverage not established in reviewed record | Not documented in the surveyed A1 evidence | Would measure incorporation or label retention; distinct from genetic lineage tracing | Not established | Not established | Not established | A bounded assay-coverage gap, not absence of genetic lineage-labelled mature outcomes (O2/O3). The Ki67-related record is an Mki67-tagRFP sorting gate in GSE141635, not a proliferation outcome | [GSE141635.json](../metadata/GSE141635.json) |

## Linkage gaps

The gaps below distinguish measurement availability, verified biological units,
predictor linkage and documented timing. Early-to-later linkage is required for
A1 and A8's prospective route; A8's association route permits concurrent timing.
Each candidate must also meet its question-specific endpoint and contrast rules.

- **O1, O2 (PATS KRT8 and AGER fractions).** Missing early measurement in the
  same units. The three named mice per marker have no chromatin or RNA
  measurement; the study's histone data come from a separate day-12 CTGF-positive
  sort and its TP53 ChIP from a separate day-8 sort
  ([SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md)). Timing is documented
  (pulse day 7, harvest day 12). Replication is three mice per marker, and the 18
  zero-denominator control fields cannot supply a comparison arm
  ([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)).
- **O3 (day-14 AGER endpoint under KIRA8).** Missing same units. The day-7
  epithelial RiboTag RNA and the day-14 microscopy endpoint are different
  experiments and different experimental units
  ([FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md)). Timing is documented for
  both. The folder does not record a verified unit count for the microscopy arm.
- **O4 (integrin and TGF-beta measurements).** Missing numerical values, units
  and timing in this folder; the lineage audit names the assays but the folder
  holds none of their values ([LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md)).
- **O5, O6 (AP-1 regional HOPX fractions).** Missing early measurement in the
  same units. The mutant RNA and ATAC experiment has one pooled library per
  condition, so it can supply neither independent genotype replication nor a
  pairing to these microscopy animals
  ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). Replication is three
  mice per genotype, which fixes the permutation resolution at p=0.10.
- **O7, O8 (medium-switch differentiation capacity).** Missing layer separation
  and same units. The outcome is RNA, so an RNA predictor panel containing the
  same markers would be circular; the chromatin measurements are separate CUT&Tag
  preparations and cross-panel pairing is not assumed
  ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). Replication is
  author-declared culture experiments from one parental iPSC line, so derived
  reporter lines do not add independent donors.
- **O9 (AGER HiBiT luminescence).** Missing same units and an interpretable
  absolute scale. The workbook repeats an adult-lung-ratio heading above the
  luminescence values and the absolute unit is left unspecified
  ([tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv)).
- **O10 (gel-contraction inhibition).** Missing an epithelial outcome definition
  and same units; the readout is a co-culture contraction phenotype, and the
  DMSO/BLM anchors are 100 and 0 by construction rather than measured controls
  ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)).
- **O11 (siRNA marker suppression).** Missing a mature outcome. This measures
  suppression of the transitional program itself, in a separate experiment from
  the medium-switch differentiation assay.
- **O12 (HPCS descendant state fractions).** Animal identity is resolved:
  Supplementary Table 4 verifies 22 distinct animals for all 5,333 retained cells.
  Separate early measurements and a non-RNA mature endpoint remain missing.
  Chase is aliased with source library; a library-adjusted chase coefficient is
  not separately estimable, and current mScarlet status remains unavailable
  ([REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md)). Verified mice permit
  mouse-level descriptive summaries, not a within-animal transition rate.
- **O13 (HPCS growth reporters and ablation).** Missing recovered numerical
  endpoint values and units. The downloaded workbook supplies growth and ablation
  panels rather than the Figure-2 lineage-composition values, and has not been
  fitted as a lineage-transition dataset
  ([LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md)).
- **O14 (current mScarlet state).** Missing the measurement itself. A
  trace-linked current fluorescence readout with a barcode or index-sort
  crosswalk is the specified requirement
  ([SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md)).
- **O15 (CD44 fibroblast-response assays).** Missing same units. The folder does
  not record whether the functional assays used the same eight mice whose sorted
  RNA is now identity-resolved
  ([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)).
- **O16 (CD44 marker RNA).** Missing layer separation. Predictor and outcome
  would come from the same libraries, which the closure report identifies as the
  reason an independently defined state, protein or fate outcome is required for
  specificity beyond the sorting comparison.
- **O17, O18 (DATP descendants; organoid reformation).** Missing an early
  measurement in the same units and transcribed induction schedules; the lineage
  audit requires figure-specific schedules to be transcribed before quantitative
  comparison ([LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md)).
- **O19 (origin convergence).** Missing outcome direction: it measures origin
  among transitional cells rather than a later mature outcome. Replication is two
  mice per lineage, and sampled regions cannot serve as biological replicates.
- **O20 (organoid transplantation).** Missing endogenous-lineage interpretation
  and same units; it is an experimental conversion-capacity test with graft-origin
  labelling ([LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md)).
- **O21 (Krt8 perturbation state accumulation).** Missing an outcome that
  separates entry, proliferation, survival and exit, plus replicate verification
  of the 24 deposited libraries ([STUDY_MAP.md](../STUDY_MAP.md)).
- **O22 (Mdm2 perturbation tracing and imaging).** Missing data access and a
  sample manifest; both cited accessions are private with a displayed scheduled
  release of Jun 01, 2027, and the supplied lists are selected rather than
  complete
  ([tp53_accessibility.tsv](../tables/regulatory_fate/tp53_accessibility.tsv)).
- **O23 (topology and mechanics).** Missing per-endpoint deposited values and
  replication; one sample per time is descriptive
  ([STUDY_MAP.md](../STUDY_MAP.md)).
- **O24 (IMC protein and neighbourhood).** Missing a donor, ROI, mask and channel
  audit and a declared biological contrast before acquisition
  ([PLAN.md](../PLAN.md)).
- **O25 (regional proteomics).** Missing a verified processed abundance matrix and
  donor-region map; the measurement is a regional mixture
  ([STUDY_MAP.md](../STUDY_MAP.md)).
- **O26 (organoid size, A10).** Bound to the completed
  [endpoint statement](../../A10_organoid_growth_outcome/reports/ENDPOINT_TIMING_UNITS_2026-09-28.md).
  Day-14 RNA and area support concurrent association; earlier day-7 imaging is a
  baseline covariate. Preparation identities and independent-preparation validation
  remain unresolved. Size is not mature AT1 contribution or withdrawal recovery.
- **O27 (A8 mature AT1 endpoint).** O2/O3 already contain relevant measured
  protein/genetic-lineage endpoint types. Missing is an eligible linked dataset
  with the required RNA components, independent biological units and a noncircular
  mature endpoint. Concurrent measurements may serve association; prospective
  prediction additionally requires earlier RNA. The component partition must also
  be frozen before endpoint analysis ([A8 plan](../../A8_maturation_component_at1_contribution/PLAN.md)).
- **O28 (A14 recovery endpoints).** No eligible recovery observations are identified
  in the reviewed record. Existing or author-provided data may satisfy the required
  exposure/reception contrast, viable traced mature output, verified units and
  post-withdrawal timing. This is not proof that a new experiment is needed
  ([A14 plan](../../A14_withdrawal_recovery_and_reception/PLAN.md)).
- **O29 (EdU or label retention).** This specific assay class is not documented in
  the surveyed evidence. Its absence is a coverage gap, not a measured negative
  and not absence of genetic lineage-labelled endpoints such as O2/O3.

## Cross-cutting note on linkage

Across O1 to O25, no outcome in this inventory currently has an early regulatory
measurement recorded in the same experimental units. The closure ledger states
the same conclusion for the branch as a whole: "Histone, lineage and intervention
observations currently come from different experiments."
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). The repository-level
gate for A1 is recorded as "Early regulatory and RNA measurements linked to
independent later fate at clone/animal/preparation level; RNA-only replacement
does not qualify"
([RESULTS.md](../../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)).
A8 and A14 share endpoint sourcing, but their eligibility rules remain distinct:
A8 permits association or prospective prediction, and A14 requires its specified
exposure/reception and recovery observations. Neither inherits A1's regulatory
predictor requirement merely by sharing this inventory.
