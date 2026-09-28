# Mature epithelial outcome inventory for A1, A8 and A14

Prepared 28 September 2026 as a documentation pass. No analysis was run and no
dataset searched. Every entry is copied from a document or table in this A1
folder or from the canonical register cards for A1, A8, A10 and A14, and each row
names its source. Values are reproduced at the precision of the source.

Purpose and reading rule. This inventory lists every independently measured
mature epithelial outcome that the A1 documents and those register cards name,
whether or not it has been reanalysed here. "Independently measured" means
measured by an assay other than the early RNA or regulatory feature that would
serve as the predictor; it does not mean independently replicated. An outcome is
recorded as *published* when the source study measured it and this repository has
not reanalysed its numerical values, and as *reanalysed here* when a tracked
table in this folder reproduces it. The last two columns state linkage, not
quality: they record whether an early measurement exists in the same
experimental units, and whether the outcome could serve as a noncircular
endpoint for an early-feature-to-later-outcome test. Nothing here nominates a
test.

Companion document: [A1_BRANCH_INVENTORY.md](A1_BRANCH_INVENTORY.md).
Register cards read from the canonical register:
[A1](../../../RESEARCH_QUESTIONS.md#a1), [A8](../../../RESEARCH_QUESTIONS.md#a8),
[A10](../../../RESEARCH_QUESTIONS.md#a10),
[A14](../../../RESEARCH_QUESTIONS.md#a14). Unit rules:
[MC1](../../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc1),
[MC5](../../../docs/RQ_MEASUREMENT_CONTRACTS.md#mc5).

## Outcome table

| Outcome | Dataset or study | Assay layer | Biological unit and n | Timing | Linked to any EARLY measurement in the same units? | Usable as a noncircular endpoint for an early-feature-to-later-outcome test? | Source |
|---|---|---|---|---|---|---|---|
| O1. KRT8-positive fraction among alveolar tdTomato-labelled cells | Kobayashi PATS, Extended Data 4 source workbook (reanalysed here) | Imaging plus lineage label (protein immunostain on genetically labelled cells) | Three explicitly named mice; fields nested within mouse; four, three and four fields | Krt19-CreER pulse 7 days after bleomycin, harvest day 12 | No. Chromatin in that study comes from a separate day-12 CTGF-positive sort and a separate day-8 TP53 sort, not these animals | Partly. KRT8 is a transitional rather than mature marker, so it is an entry or persistence readout; it is noncircular with respect to chromatin but not with respect to a KRT8-containing RNA panel | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [pats_mouse_endpoints.tsv](../tables/lineage/pats_mouse_endpoints.tsv) |
| O2. AGER-positive fraction among alveolar tdTomato-labelled cells | Kobayashi PATS, Extended Data 4 (reanalysed here) | Imaging plus lineage label | Three explicitly named mice; three fields each | Same pulse day 7, harvest day 12 | No, same reason as O1 | Yes in principle: AGER is a mature AT1 marker measured as protein on labelled cells, independent of any RNA predictor panel. No early measurement exists in these three mice | [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md), [pats_source_fields.tsv](../tables/lineage/pats_source_fields.tsv) |
| O3. Day-14 labelled-cell AGER endpoint under KIRA8 | Auyeung 2022 (published; not reanalysed numerically here) | Imaging plus lineage label under perturbation | Not recorded in this folder as a verified unit count | Krt19-CreERT2 pulse on injury days 3-4, day-14 endpoint | Partial. The same study deposits day-7 epithelial RiboTag RNA (GSE190821), but those are different experimental units from the microscopy mice | Yes as an endpoint type; not yet as a linked endpoint, because the RNA and microscopy experiments are not the same animals | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [FIRST_BATCH_REPORT.md](FIRST_BATCH_REPORT.md) |
| O4. Epithelial IRE1alpha integrin and TGF-beta measurements (profibrotic function) | Auyeung 2022 (published) | Protein and function, as described by the source study | Not recorded in this folder | Source-study design | No | Not as recorded here: the folder does not hold its numerical values, units or timing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O5. HOPX-positive fraction among GFP-labelled cells, injured in-situ regions | Lynch AP-1 preprint v2 Fig. 4I source workbook (reanalysed here) | Imaging plus lineage label | Three mice per genotype, three fields per mouse per region | Microscopy endpoint of the source design | No. The same study's mutant RNA/ATAC experiment has one pooled library per condition and cannot be paired to these microscopy animals | Yes as a differentiation readout on labelled cells. The report states it measures HOPX acquisition, not completed functional AT1 differentiation | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ap1_mice.tsv](../tables/regulatory_fate/ap1_mice.tsv) |
| O6. HOPX-positive fraction among GFP-labelled cells, intact de-novo regions | Lynch AP-1 preprint v2 Fig. 4I (reanalysed here) | Imaging plus lineage label | Three mice per genotype, three fields per mouse per region | Same microscopy endpoint | No, same reason as O5 | Yes, with the same limit; region is a context axis that changes the direction of the genotype effect | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [ap1_group_summary.tsv](../tables/regulatory_fate/ap1_group_summary.tsv) |
| O7. Medium-switch AT2 differentiation capacity (SFTPC, NAPSA, SLC34A2 induction) | Tsutsui 2026 Fig. 6c/6d source workbook (reanalysed here) | RNA (qPCR ratio to adult lung) | Author-declared independent culture experiments, n=7 at day zero and n=6 after switching; one parental iPSC line | Medium switch from culture day zero | No. Chromatin was measured in separate CUT&Tag preparations of the same study, and cross-panel pairing is not assumed | Partly. The layer is RNA, so it is circular against an RNA predictor panel containing the same markers; it is noncircular against a chromatin predictor if preparations were linked, which they are not | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv) |
| O8. Medium-switch AT1 differentiation capacity (AGER, CLIC5, RTKN2 induction) | Tsutsui 2026 Fig. 6g/6h (reanalysed here) | RNA (qPCR ratio to adult lung) | n=7 at day zero, n=5 after switching; one parental iPSC line | Medium switch from day zero | No, same reason as O7 | Partly, same reason as O7 | [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O9. AGER HiBiT reporter luminescence under AT1 versus AT2 induction | Tsutsui 2026 Fig. 6i (reanalysed here) | Reporter luminescence; absolute unit unspecified in the source workbook | Three experiments per condition; derived reporter lines add no independent donor | After medium switch | No | Partly. It is a reporter rather than an RNA panel, so less circular than O7/O8, but the descriptive-ratio table labels it AGER reporter induction, not mature AT1 function | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O10. Normalized gel-contraction inhibition by AP-1 inhibitors | Tsutsui 2026 Fig. 9d (reanalysed here) | Function (contraction assay); DMSO and BLM anchors are 100 and 0 by construction | Three experiments per condition | Inhibitor-treated culture | No | Yes as a function readout, but it is a co-culture contraction phenotype rather than a mature epithelial outcome, and the anchors are not measured zero-variance controls | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_endpoint_summary.tsv](../tables/regulatory_fate/tsutsui_endpoint_summary.tsv) |
| O11. siRNA suppression of transitional markers (ATF3, HNF1B, TP63, MMP7, ITGB6, KRT17, COL1A1) | Tsutsui 2026 Fig. 9f/9g (reanalysed here) | RNA relative to siCont | n=3 or n=4 per condition; one parental iPSC line | Separate siRNA experiments | No | No. This is transitional-program suppression, not a mature outcome; the report states it does not show rescue of the fate of the same cells followed in the medium-switch assay | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tsutsui_descriptive_ratios.tsv](../tables/regulatory_fate/tsutsui_descriptive_ratios.tsv) |
| O12. HPCS descendant AT1-like and AT2-like RNA-state fractions among traced cells | Chan 2026 HPCS, GSE277777 observation metadata (reanalysed here) | RNA state label on trace-sorted cells | 5,333 retained traced cells across 22 source labels and six deposited groups; cells are not biological replicates and sources are not verified animals | Slc4a11 and Hopx tracing in established KP tumours; 3-day and 14-day chase | Partial. The predictor and the outcome are both RNA labels on the same cells, so no separate early measurement exists | No. Both layers are RNA on the same cells, mouse and pool independence is unverified, and the fractions are not cell-production or transition rates | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [source_state_counts.tsv](../tables/hpcs_source_composition/source_state_counts.tsv) |
| O13. HPCS growth reporters and selective ablation | Chan 2026, source workbook panels from Figures 3, 4 and Extended Data 10 (inventoried, not fitted) | Growth reporter and ablation outcome | Not resolved in this folder; some scRNA conditions pool two mice | Source-study tumour timeline | No | Not as recorded here. The lineage audit states the workbook supplies growth and ablation panels rather than the Figure-2 lineage fractions, and that ablation tests population dependency rather than a chromatin mechanism | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O14. HPCS current mScarlet reporter-positive state | Chan 2026 GSE277777 (absent) | Would be current-state reporter protein | Not available for traced rows | Same tracing design | No | No. Current mScarlet status is absent from the traced observation rows, so permanent lineage inheritance cannot be distinguished from ongoing reporter-positive state | [SECOND_BATCH_REPORT.md](SECOND_BATCH_REPORT.md), [SOURCE_REQUEST_DRAFTS.md](SOURCE_REQUEST_DRAFTS.md) |
| O15. CD44-sorted fibroblast-response assays (profibrotic capability) | Rodriguez 2025 CD44 study (published) | Function (conditioned-medium fibroblast response) | Not recorded in this folder as a verified unit count | Source-study model | Partial. The same study deposits the 16-library sorted RNA matrix, now identity-resolved to eight mice, but the folder does not record whether the functional assays used those same animals | Yes as a function readout; the lineage audit states that expression of mediators is not the conditioned-medium response itself, and that CD44 sorting is not lineage tracing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O16. CD44-sorted mature and transitional marker RNA (Sftpc, Ager and six others) | GSE273123 (reanalysed here) | RNA (sorted bulk) | Eight mice, four paired per genotype, 16 libraries | As deposited; no explicit injury time axis in the count matrix | Yes, but in the same layer: the early feature and this outcome would both be RNA from the same libraries | No. Same-assay, same-library measurement; Ager passes neither contrast and Sftpc's interaction is fragile | [EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md), [focus_effects.tsv](../tables/cd44_closure/focus_effects.tsv) |
| O17. DATP day-28 differentiated descendants | Choi 2020 (published) | Lineage label plus marker phenotype | Not recorded in this folder | Day-9 transitional populations and day-28 differentiated descendants | No | Yes as an endpoint type. The lineage audit notes that AT1 contribution and labelled AT2 descendants are distinct endpoints and that exact induction schedules are figure-specific and must be transcribed before quantitative comparison | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O18. DATP organoid reformation and IL-1beta manipulation | Choi 2020 (published) | Organoid formation and growth under perturbation | Not recorded in this folder | Source-study culture design | No | Partly. The lineage audit states that organoid capacity is not an in-vivo single-cell reversal measurement | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O19. Origin convergence among Krt8-high alveolar cells | Strunz 2020 Fig. 7 (published) | Lineage label | Two mice per lineage and multiple sampled regions | Sftpc-CreERT2 and Sox2-CreERT2 induced before injury with washout | No | No as a later mature outcome: it measures labelled origin among transitional cells, which the lineage audit keeps separate from descendant composition. Regions cannot become biological replicates, and two driver experiments do not form a jointly calibrated mixture fraction | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O20. Human AT2 organoid transplantation into injured mice; alveolar versus basal output | Kathiriya 2022 (published) | Imaging, morphology and graft-origin nuclear labelling | Not recorded in this folder | Culture and transplantation timeline of the source study | No | Partly. The lineage audit records it as experimental conversion capacity and niche dependence, not endogenous human lineage tracing | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md) |
| O21. Transitional-state accumulation under Krt8 genetic perturbation | Krt8 perturbation study 2023, GSE223302 (published; not fitted here) | RNA (bulk time course) | 24 bulk-RNA GSM library records, WT and KO time course; replicate verification pending | Injury time course | No | No. A changed state frequency can reflect altered entry, proliferation, survival or exit, and the lineage audit states it is not automatically a measured lineage-transition rate | [LINEAGE_AUDIT.md](../LINEAGE_AUDIT.md), [STUDY_MAP.md](../STUDY_MAP.md) |
| O22. AT1-specific Mdm2 perturbation with lineage tracing and live imaging | Morowitz TP53 preprint (published; inputs private) | Lineage label and live imaging | Not recorded; no biological sample manifest recovered | Source-study design | No. Only selected signed differential-expression lists are available | No at present. GSE335749 and GSE335750 are private with a displayed scheduled release of Jun 01, 2027, and mouse-level lineage or imaging counts with nested-field IDs were requested but not obtained | [REGULATORY_FATE_REPORT.md](REGULATORY_FATE_REPORT.md), [tp53_accessibility.tsv](../tables/regulatory_fate/tp53_accessibility.tsv) |
| O23. BHT injury, AT1 ablation and AT2 Mdm2 deletion topology and mechanics | Konkimalla 2023; GSE218665, GSE218666, GSE235212 (published) | Imaging, tissue topology and mechanics | 2, 4 and 1 GSM respectively; one sample per time is descriptive | Source-study injury and perturbation timelines | No | No as recorded. The study map states that deposits alone do not encode every imaging or fate endpoint and that shared external controls are not new independent cohorts | [STUDY_MAP.md](../STUDY_MAP.md) |
| O24. Cell protein abundance, morphology and neighbourhood in IPF tissue | IPF regenerating-niche atlas 2025; Zenodo 10930946 (not acquired) | Imaging mass cytometry, 33 channels | 22 MCD files, approximately 15.55 GB; 22 files are not 22 donors | Cross-sectional pathology stages | No | No as recorded. The plan makes IMC an optional phenotype and context extension that cannot validate ancestry, reversibility or epigenetic memory, and requires a donor and ROI crosswalk first | [STUDY_MAP.md](../STUDY_MAP.md), [PLAN.md](../PLAN.md) |
| O25. Regional epithelial protein abundance over fibroblastic foci | MUC5B regional proteomics 2025; PXD058626 (project metadata verified only) | Laser-capture microdissection mass spectrometry | Donor and region map unverified; measures a regional mixture rather than a single cell | Cross-sectional | No | No as recorded. Processed abundance matrix and donor-region map remain unverified, and mixtures are not a purified transitional-cell proteome | [STUDY_MAP.md](../STUDY_MAP.md) |
| O26. Organoid size (A10) | GSE307112 organoid screen, per the A10 register card | Imaging (organoid mean area), with RNA predictors | 885 wells in 15 deposited plate-replicate groups; independent preparations remain unidentified; 886 GEO sample records still lack preparation IDs | Fixed day-14 area conditional on day-7 area; outcome-time RNA supports concurrent association | Partial, per the card: outcome-time RNA is concurrent rather than earlier | PLACEHOLDER: to be bound to A10's endpoint statement in the next phase. The card states that organoid mean area measures size and morphology, not total tissue production, mature AT1 fate or in vivo repair | [A10 register card](../../../RESEARCH_QUESTIONS.md#a10), [A10 follow-up](../../A10_organoid_growth_outcome/reports/FOLLOWUP_RESULTS.md) |
| O27. Measured mature AT1 protein, morphology or traced descendant yield (A8 requirement) | Not available; required by the A8 decision rule | Would be protein, imaging or lineage label | Would require independent animals | Predictor timing must be specified | No | Required but absent. The A8 card states that both predictor and mature outcome must not be defined with the same RNA panel, and that score-versus-score comparisons cannot meet the requirement | [A8 register card](../../../RESEARCH_QUESTIONS.md#a8), [PROPOSAL.md](../../../docs/audits/2026-09-28-rq-development-proposal/PROPOSAL.md) |
| O28. Mature-cell yield, viability, traced descendants and function after IL-1beta withdrawal (A14 requirement) | Not available; the A14 design is unexecuted | Would be lineage label, viability, protein and function | Would require independent animals or culture preparations | Comparable post-withdrawal intervals with time-matched controls | No | Required but absent. The A14 card states that loss of a transitional score cannot by itself distinguish maturation, reversion, death or replacement | [A14 register card](../../../RESEARCH_QUESTIONS.md#a14), [RESULTS.md](../../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md) |
| O29. EdU incorporation or label retention | Not named in any document in this evidence package | Would be label-retention imaging | Not applicable | Not applicable | Not applicable | Not available. No EdU, BrdU or label-retention assay is named in the A1 documents or in the A1, A8, A10 and A14 register cards; the only Ki67-related record is an Mki67-tagRFP sorting gate in the GSE141635 sample metadata, which is a sorting gate rather than an outcome | [GSE141635.json](../metadata/GSE141635.json) |

## Linkage gaps

Per outcome, the element that is missing before it could serve as the later term
of an early-feature-to-later-outcome test. The missing elements are of four
kinds: an early measurement, the same experimental units, documented timing, and
biological replication.

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
- **O12 (HPCS descendant state fractions).** Missing layer separation,
  replication and timing identifiability. Predictor and outcome are both RNA
  labels on the same cells; the 22 source labels are not verified animals or
  disjoint pools; chase is completely aliased with source library, so the
  library-adjusted chase coefficient is not separately estimable
  ([ROBUSTNESS_REPORT.md](ROBUSTNESS_REPORT.md)).
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
- **O26 (organoid size, A10).** PLACEHOLDER. Per the A10 card the outstanding
  elements are preparation identity, imaging calibration and the choice between
  concurrent association and future prediction; outcome-time RNA supports
  concurrent association only. The endpoint statement itself is to be bound in
  the next phase ([A10 register card](../../../RESEARCH_QUESTIONS.md#a10)).
- **O27 (A8 mature AT1 endpoint).** Missing the outcome measurement entirely, in
  independent animals, with predictor timing specified and with the predictor not
  defined from the outcome's own genes
  ([A8 register card](../../../RESEARCH_QUESTIONS.md#a8)).
- **O28 (A14 recovery endpoints).** Missing the experiment. Required are
  independent preparation-level observations linking the exposure or reception
  comparison to viable traced mature output with documented timing
  ([RESULTS.md](../../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)).
- **O29 (EdU or label retention).** Missing from the record: no such assay is
  named in this evidence package, so its absence is a coverage gap rather than a
  measured negative.

## Cross-cutting note on linkage

Across O1 to O25, no outcome in this inventory currently has an early regulatory
measurement recorded in the same experimental units. The closure ledger states
the same conclusion for the branch as a whole: "Histone, lineage and intervention
observations currently come from different experiments."
([EVIDENCE_CLOSURE_REPORT.md](EVIDENCE_CLOSURE_REPORT.md)). The repository-level
gate for A1 is recorded as "Early regulatory and RNA measurements linked to
independent later fate at clone/animal/preparation level; RNA-only replacement
does not qualify"
([RESULTS.md](../../../docs/roadmap_runs/2026-09-28-gap-fill/RESULTS.md)), and
A8 and A14 are recorded there as sharing A1's missing-outcome gate.
