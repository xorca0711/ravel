# DY1 job-by-job assessment and current disposition

30 October 2026, Asia/Seoul. This is the coordinating review of article-local
DY1-P01, following the [original stages 0–8](../../docs/research_reviews/2026-10-29-nam-memory/README.md).
The question remains whether deposited measurements reproduce the published
persistent RNA/accessibility associations and distinguish RNA mixture from
within-state differences. Full context remains N. brasiliensis-associated type-2
immune history, separate baseline bulk RNA/ATAC, baseline and later IAV-challenge
scRNA, the proposed STAT6–EGR2–PPARγ/RXRA association, ARG1 and human disease context.

The earlier broad analysis turn was rejected by the platform. That historical
execution event is retained in [CLOSEOUT](CLOSEOUT.md); it is not evidence that
every mouse-data job is prohibited. Independently scoped permissible jobs were
reviewed with the full context retained. A data hold below means a specified
source/design prerequisite is unresolved; an inference limit means the proposed
claim exceeds the measurements. Neither is a completed numerical result.
Unrequested pathogen optimization and intervention prioritization are outside
this work, not extra original jobs to add to its completion checklist.

## Current disposition of every original stage

| Stage / job | Completed work | Specific remaining hold or interpretation limit |
|---|---|---|
| 0. Source provenance and versions | Source-v1 manifests, source-v2 label correction, 22 source records, original input hashes; current baseline copies verified | The replacement ATAC files' relationship to the publication pipeline remains unresolved. Code Ocean access last failed on 29 October; no new access success is claimed. |
| 0. Biological units and overlap | Published pooling statements and source-local library/tag labels reviewed | No qualified deposited-library/tag → independently collected pool crosswalk or overlap assurance. Distinct independent pools can be valid units without individual mouse names; cells/tags do not establish those pools. RNA Methods, Fig. 4 and Extended Data 8c describe different pooling levels that need source-specific reconciliation. |
| 0. CMO labels versus assignments | V2 corrected naive labels and verified feature presence; baseline raw signal inventory now complete | Counts do not supply validated cell assignments, pool identity or condition-by-library/batch support. Reused tag IDs are library-local. |
| 1. Exon-file QC | Six files share 406,850 ordered features; 143,437 all-zero rows; integer/nonnegative/duplicate and summary-row checks pass | Format eligibility does not establish unique gene/fragment counts. Exon-bin totals stay exon-bin hits. |
| 1. Sample-profile diagnostic | All six libraries retained in a frozen logCPM/full-SVD adaptation using 263,413 nonzero features | This is not the author's low-count-filtered DESeq2 VST/plotPCA. Exact filter and author gene-count preparation remain unknown; no outlier or history-effect decision follows. |
| 1. Gene-level RNA effects / exact Fig. 4 reproduction | Count-format and author-Methods assessment complete | Exact feature/counting mode, annotation provenance and fragment/bin semantics remain unresolved, as do fit-specific unit/batch qualifications. A technically full-rank design would not prove independence. No gene-level effect table is produced. |
| 1. Called-peak QC | Eight narrowPeak files pass the explicitly listed basic field/interval checks | This is not full BED/build validation, read-level depth/complexity/enrichment QC or a differential model. |
| 1. ATAC effects and outlier sensitivity | Pipeline and availability discrepancy documented | No qualified common-region read-count matrix/read-level QC in the inspected deposit; source/article pipelines disagree and the author-excluded naive library/rationale is unidentified. Peak scores cannot substitute for read counts; no outlier is guessed from a plot. |
| 2. Assay/schema interpretation | Bulk RNA versus separate bulk ATAC distinguished from the scRNA composition question; declared mm10/exon/interval representations reviewed | Exact annotation/feature compatibility and a defensible promoter/distal association rule remain unqualified. A shared build label alone is insufficient. |
| 2. Numerical RNA/accessibility discordance | Published-direction evidence matrix completed, explicitly attributed to the paper | Needs qualified assay-specific effects/uncertainty and mapping sensitivity. No paired-sample relation is established. Significance in one assay and imprecision in another do not establish poising. |
| 3. Baseline sparse integrity | Both matrices fully scanned: 67,983,499 entries; dimensions, indices, count positivity and accounting checks pass | Gene Expression duplicate coordinates were not audited; no cell/state/animal assignment follows from structural integrity. |
| 3. CMO signal / NAM labels | All 12 baseline library-tag rows have signal; duplicate stored tag coordinates absent | Very small signals coexist with much larger rows. Nonzero presence does not establish mixed assigned conditions. Defensible assignments and population/state definitions independent of tested outcomes are still missing. |
| 3. Composition versus within-state RNA | Estimand, denominators and conditioning limits specified | Needs qualified units, states, condition/batch support and shared-state coverage. No pseudobulk/decomposition fitted. scRNA cannot identify within-state ATAC in different bulk preparations. |
| 4. Regulatory model literature | Existing primary precedents and figure-level STAT6/EGR2/PPARγ/RXRA evidence reviewed | A late RNA snapshot cannot establish the early relay; TF RNA, shared motifs and external ChIP overlap do not demonstrate activity or occupancy here. |
| 4. Observational motif/target association | Published promoter/leading-edge scope distinguished from a proposed broader peak extension | Qualified contrasts, annotation, appropriate region/gene backgrounds and context-qualified independent target/binding resources are required. No target enrichment, footprint or regulon estimate is produced. |
| 5. Descriptive history-by-condition host-RNA contrast | Original estimand and separate-unit design retained | Missing qualified cell/condition/unit/batch mapping, common states and eligible target sets. No interaction estimate. This original descriptive task is data/design-gated; it is not recast as susceptibility prediction or assigned a blanket prohibition. |
| 5. Temporal/individual interpretation | Limits of one later endpoint and unpaired baseline ATAC recorded | A snapshot cannot distinguish induction speed, peak magnitude or resolution. Separate samples do not provide individual longitudinal or ATAC-to-later-response linkage. |
| 6. Mouse Arg1 RNA/state attribution | Published Fig. 4/5 evidence and program-circularity concern reviewed | Depends on the unqualified state/assay contrasts above. No mouse state-specific estimate or biochemical output measurement is produced. |
| 6. ARG1 contribution versus mediation | Conditional genotype effect, training-specific interaction, compartment and phase distinctions completed | Unlinked omics/functional cohorts do not support mediation. Missing untrained genotype comparator limits training-specific interaction, not every trained genotype comparison. Targeting includes NAMs and AMs; RNA is not enzyme activity/metabolite flux. |
| 7. Primary human context | Completed exposed 78-donor GSE136831 RNA/composition and recipient-context analysis with clinical/annotation/floor sensitivities | Exact author NAM labels/model unavailable; captured-cell fractions are not tissue abundance. Sparse ARG1 and missing neutrophil annotation prevent source-dominance/activity claims. Shared source remains one evidence lineage. |
| 7. External human description | Completed separate 12-IPF/9-control GSE135893 description and source/site sensitivities | Exact SELENOP symbol absent; full panel withheld. Common-source and recipient subsets below the frozen minimum are retained as non-estimable. No relaxed threshold or unexposed confirmation claim. |
| 8. Current-evidence integration | Published boundaries, favorable/mixed/negative human findings, three technical runs and existing RQ context integrated | Synthesis is complete at the available-evidence level; it does not establish a chromatin-memory → ARG1 → epithelial-repair mechanism or laboratory readiness. |
| 8. Existing RQ routing | A1/A2/A8/A14/A19/A22 context notes remain in their established folders | Their original linked fate, delivery, cessation/reception, functional reserve or focal protein-output requirements remain unmet by this paper's data. No canonical question, unfavorable result or human acceptance decision is changed. |

## Reviewed completed execution

See [baseline results](BASELINE_QC_RESULTS_2026-10-30.md),
[methods/input assessment](METHODS_AND_INPUT_ASSESSMENT_2026-10-30.md),
[published evidence boundaries](PUBLISHED_EVIDENCE_BOUNDARIES_2026-10-30.md),
[primary human results](HUMAN_RESULTS.md) and [external results](HUMAN_EXTERNAL_RESULTS.md).
The human reports and prior independent review remain valid; they were not rerun
for this documentation pass.

The reviewer checked the three prospective contracts/scripts before execution,
then independently verified current and frozen Git bytes for 13 contract/code
entries and all 16 output hashes. Each receipt records executed status and no
scientific acceptance. Saved arithmetic checks passed: 205 structural checks,
152 sparse aggregate checks, and the SVD/covariance, coordinate-Gram and centering
checks. These compare computations on the same input, not biological replication.
The profile figure was inspected for legibility and consistency with saved axes.

| Run | Frozen revision | Receipt SHA-256 |
|---|---|---|
| [File QC](../../analysis/research/runs/DY1_baseline_file_qc_v1/receipt.json) | fb29cd36e4137389018ab74f2dd95eadc123dc39 | 1018a20c9140224e72b1be0824565ff1ef38e16470212a2f3a66750f4e531cb0 |
| [Sparse QC](../../analysis/research/runs/DY1_baseline_sparse_qc_v1/receipt.json) | edc5e60a6ac230a471f066f5f28234553c84f713 | 26b41755ff369ae0b1d354a559efa6bed1457c663048aac53a9797975a8e7829 |
| [Exon profile](../../analysis/research/runs/DY1_baseline_exon_profile_v1/receipt.json) | d7f0f828d86b920880012f588b69b2c2fc0238fc | 704044d800b9a375d2813fe54d8792d92e7affcb13532f0edf472dbc552f129f |

## Plan changes and stopping point

1. Split file integrity, technical sample geometry and biological effects because
   their inputs, units and claims differ. This enabled the three completed runs
   without pretending the original gene/peak effects had been reproduced.
2. Replace the old blanket current-status wording with the exact holds above.
   Preserve the earlier platform event and all historical outputs.
3. Complete current-evidence synthesis now; separate it from mechanistic proof.
   Preserve the paper's regulatory and ARG1 premises and all unfavorable repository
   findings, without adding an intervention screen or new canonical RQ.

No supported job is left queued in this pass. Reopening a held numerical job
requires the specific evidence in its row and a prospective versioned contract;
repeated analysis of the same unqualified files cannot supply that evidence.
This does not claim the original numerical sequence is fully reproduced.

## Technical review and validation status

The analysis chat cross-checked this ledger against the original stages and saved
results on 30 October: no blocking completion/hold mismatch or omitted currently
qualified original job was found. Source-side validation passed 161 repository
tests (one skip), 12 targeted synthetic tests, standard evidence verifiers,
11,535 repository checks and the research gate against freshly fetched main
`78320a186b6f52426e7c7c5349a2f26492b718b7`. Integration of stable handoff `9f058bf3f77fede8ab43cfdf162df0bff78d2511` passed
11,553 repository checks and the base-aware research gate. All 32 canonical
questions/guides, infrastructure registry and protected governance match main;
no RQ file changed in this pass. The primary checkout still contains its original
PROGRESS modification. Successful checks do not confer scientific acceptance.
