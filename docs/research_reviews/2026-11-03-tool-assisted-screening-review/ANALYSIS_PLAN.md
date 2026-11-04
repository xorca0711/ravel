# Tool-assisted screening review and prospective analysis plan

3 November 2026, Asia/Seoul. **Review and proposal only: no new biological analysis or source-qualification run was executed.** Starting revision `300a18487a5aa4f0f69171d602cf008602a4cbc8`; refreshed main `445a0ca934f2f67060fbf7faec7746612526fb92`. PR #163 remains the completed screening evidence, not a claim that every biological hypothesis is resolved.

## Decision and review scope

The tools can improve annotation completeness, distinguish technical detection from coordinated RNA context, and find genuinely different evidence. Replacing a correct custom script with Scanpy, another embedding or a larger score does not itself improve the biological answer. Favor a bounded follow-up that could narrow or weaken a target, rather than one designed to obtain a positive result.

Reviewed the seven latest numerical entrypoints, their current reports/contracts and saved endpoint definitions; the [22-owner ledger](../2026-11-03-full-priority-screening/TECHNICAL_LEDGER.md); registry navigation for all 33 RQs; and the other 12 dossiers' interpretation boundaries. This is a focused design/code review, not a fresh arithmetic audit of all 150 historical receipts or a claim that every script was inspected. The existing independent checks remain valid.

| Proposed follow-up | Recommendation | Concrete opportunity |
|---|---|---|
| A5 complete functional attribution | First | Only 18/99 members have reviewed role assignments; 81 unreviewed members dominate the unresolved interpretation |
| A31 depth-conditioned partner context | Second, bounded | Current depth halves are within each stratum, not comparable depth distributions across fibroblast labels; joint detection is not compared with its marginal expectation |
| A8 sampling-versus-component instability | Useful bounded diagnostic | The same random draw defines both the cell groups and panel detection; two seeds reveal instability but do not characterize it |
| A9 same-cell receptor/feedback context | Moderate | Current code measures marginal six-gene profiles and EGFR/ERBB2 co-detection, not receptor/negative-regulator coexistence within cells |
| A12 state-resolved recipient architecture | Conditional source-dependent extension | Pooled recipient counts cannot reveal whether receptor/accessory/decoy components coexist in the same cells |
| A3/DY1 matched temporal regulatory reference | Conditional new-source search | Averaged repeat-stimulation RNA and separately qualified cross-assay references cannot identify post-withdrawal maintenance |
| A27 independently annotated RNA plus qualified repertoire | Conditional new-source search | Better state assignment alone cannot repair sparse mice or 237 inherited blank-clone singleton conventions |

These are recommendations about additional work, not changes to canonical hypotheses, human acceptance, evidence grades or existing completion states.

## Available aids and their actual role

- **NCBI Entrez/GEO, CELLxGENE Discover and BioStudies:** installed public-API wrapper skills, useful for accessions, sample metadata and attachments. They are not installed replacements for the scientific runner. The CELLxGENE skill exposes collection/dataset metadata; a Census matrix query requires a separate compatible client or a qualified dataset download.
- **UniProt:** installed annotation-access skill. Its versioned metadata was already used for A5; extending coverage is new work, not a newly discovered capability. Curated/manual annotations may still be inferred or transferred, so retain evidence codes and organism specificity. [Official evidence documentation](https://www.ebi.ac.uk/training/online/courses/uniprot-exploring-protein-sequence-and-functional-info/where-does-the-data-come-from/data-evidence/).
- **Scanpy:** installed workflow skill, useful for explicit matrix layers, grouping, annotation diagnostics and plotting. `get.aggregate` supports sums, nonzero counts and other group summaries; it does not supply missing independent donors or select the scientific model. [Official API](https://scanpy.readthedocs.io/en/stable/generated/scanpy.get.aggregate.html).
- **NGS Analysis Workbench:** connected workflow/design/results tools. The existing same-day capability check found RNA/ATAC and related workflows; no new runtime readiness was established here. Its largest potential contribution is a justified raw-read reprocessing job after source identity/design are resolved, not replaying already-qualified count matrices.
- **Literature/citation tools:** support biological roles, close precedents and contrary findings. Reuse the valid same-day biological reviews; refresh for a changed comparison. No new full primary-paper review or novel dataset qualification is claimed in this pass.

CELLxGENE aggregation can contain duplicate cells; preserve source accessions/donors and `is_primary_data` semantics rather than counting a repackaged atlas as replication. [Official Census documentation](https://chanzuckerberg.github.io/cellxgene-census/notebooks/analysis_demo/comp_bio_census_info.html). Annotation evidence types are distinct, including experimental versus computational support. [GO evidence guide](https://geneontology.org/docs/guide-go-evidence-codes/).

## 1. A5 — what biological process accounts for the fixed component?

**Existing evidence:** [script](../../../RQ_Specified/A5_developmental_programme_reuse/scripts/component_attribution_v1.py), especially role loading and contribution aggregation; [report](../../../RQ_Specified/A5_developmental_programme_reuse/reports/COMPONENT_ATTRIBUTION_V1_RESULTS.md). The fixed 99/57/53 memberships and 24 paired mice are already reconstructed. The six annotated regulatory members have a negative net contribution to the full component; the remaining 81 are unreviewed, not nonfunctional. This does not warrant replacing the component with favorable genes.

**Biological question:** is the retained developmental-associated signal distributed across a coherent signaling/structural/regulatory process, or mostly a mixture of unrelated state markers? The leading threat is uneven annotation plus selecting a coherent-looking subset after seeing outcomes.

1. Map **all 99 genes** to species-correct, versioned UniProt/GO entries; retain unresolved symbols, evidence codes, overlapping roles and uncertain annotations. Review the role rules using source evidence without consulting the member-effect table during assignment. Prior outcome exposure remains explicitly recorded.
2. Freeze the expanded role map and rules before recalculating role summaries. Preserve the original three module denominators and overlapping-role disclosure. Do not infer an experimental annotation merely from a reviewed UniProt entry.
3. Reuse the saved per-mouse member contributions. Describe each role's signed contribution, across-mouse consistency and dispersion; distinguish a broadly distributed contribution from one driven by a few members. Describe day-specific patterns only where the existing mouse/day roster supports them; cross-sectional days are not a tracked trajectory.
4. Carry a coherent candidate subset into an independent-source eligibility search only if justified by the full positive, negative and unresolved table. If the component remains heterogeneous, retain that result and stop; do not manufacture a replacement positive module.

**Unit/endpoint:** mouse; ADI-minus-activated-AT2 detection contributions under the existing budget/denominators. **Deliverables:** full annotation/evidence matrix, member-by-mouse heatmap, role contribution plot and a short candidate-or-no-candidate decision. UniProt/GO supports functional interpretation, not measured pathway activation or productive differentiation. Formal enrichment is optional only with a justified assay gene universe and multiplicity plan; a whole-genome default is not an automatic background.

## 2. A31 — coordinated partner context or marginal detection?

**Existing evidence:** [script](../../../RQ_Specified/A31_gria1_fibroblast_response/scripts/partner_context_v1.py), lines 49–62 and 76–84; [report](../../../RQ_Specified/A31_gria1_fibroblast_response/reports/PARTNER_CONTEXT_V1_RESULTS.md). GRIA1 enrichment persists, partner directions differ, and ten donor/assay rows include repeated people. The script already retains all-cell denominators and matched region/protocol comparisons; those do not need rebuilding.

**Biological question:** does any fixed partner share a GRIA1-associated cellular context beyond what marginal abundance and RNA depth predict? Leading threats are detection depth, correlated cell state and source/assay composition, not just missing p-values.

1. Use the existing cell/count primitives. Inspect depth common support across the two fibroblast labels within each donor/region/protocol. Fix depth bins or a comparable standardization design from metadata before the new endpoint; retain unsupported strata. Do not equate SS2 reads with 10x UMIs or match cells across incompatible protocols.
2. For all eight fixed partners, compare observed joint detection with the expectation from the two marginal detection frequencies within comparable depth strata. A stratified permutation can characterize conditional association, but cells do not become independent biological replicates.
3. Summarize these residual associations and label differences by donor within assay; keep repeated-donor identities linked and inspect donor influence. No population-level significance is required where independent support is insufficient.
4. If a partner pattern remains, use CELLxGENE/source metadata to seek a nonoverlapping donor cohort with compatible fibroblast identity and assay. Travaglini or Madissoon cells inside another atlas are the same evidence. Protein/localization or acute-response data are a separate, stronger route if an appropriate source is actually found.

**Unit/endpoint:** donor within assay; depth-conditioned RNA co-detection beyond marginal expectation. **Deliverables:** all-partner observed/expected plots and donor-context effects. Persistence can narrow a candidate partner; loss favors a measurement/composition explanation. Neither establishes physical assembly or acute GRIA1-dependent function. This is a new conditional question, not another unadjusted co-detection display.

## 3. A8 — separate sampling instability from mixed biology

**Existing evidence:** [script](../../../RQ_Specified/A8_maturation_component_at1_contribution/scripts/panel_attribution_v1.py), lines 21–39; [report](../../../RQ_Specified/A8_maturation_component_at1_contribution/reports/PANEL_ATTRIBUTION_V1_RESULTS.md). The joint 2,000-count draw assigns Cldn4/Krt8 and Sftpc groups and scores the selected three/four-gene panels. Only 34/140 original contrasts qualify. Opposing members and seed-sensitive totals are already documented.

**Question:** how much of the unstable late-panel total comes from stochastic group assignment/detection rather than stable opposing member contributions?

1. Preserve raw-count provenance, the seven genes, original sampling order, depth budget and support rules. Recover the original count objects; the two saved draws alone cannot reconstruct unobserved draws.
2. Predefine a bounded repeated-draw design, computational precision target and maximum work before execution. Keep the original two seeds as landmarks, not independent observations. Do not select a seed with a favorable effect.
3. Report group-membership stability, support frequency and the distribution of member and panel contributions **within each original unit**. Label computational Monte Carlo uncertainty separately from biological uncertainty. A common reference assignment, if used as a diagnostic, is a separately stated estimand rather than a silent replacement for the original gate.
4. Distinguish stable opposing members, sampling-dominated sign changes and persistently unsupported comparisons. Stop there if no stable distinction survives. Do not reduce the 30-cell floor or count extra seeds as extra mice.

**Units:** the original pooled libraries or individual external animals, separately. **Deliverables:** membership/support stability plot and member-contribution distributions. This can prevent a noisy panel from driving target selection; it cannot recover future AT1 fate, independent neonatal replication or missing biological units. Lower priority than A5/A31 if only a biological target shortlist is wanted.

## 4. A9 — receptor and negative-regulator RNA in the same recipient cells

**Existing evidence:** [script](../../../RQ_Specified/A9_areg_recipient_competence/scripts/receptor_context_v1.py), lines 37–65; [report](../../../RQ_Specified/A9_areg_recipient_competence/reports/RECEPTOR_CONTEXT_V1_RESULTS.md). The cell primitives retain donor, disease, label, depth and six targets. EGFR and ERRFI1 are lower in all 19 supported myofibroblast-minus-fibroblast comparisons. The existing co-detection endpoint covers only EGFR/ERBB2.

1. Retain all six genes and existing donors; fix the receptor/feedback pair questions from literature, including EGFR–ERRFI1 and EGFR–LRIG1, before the new pair results. Keep ERBB3/4 as family context, not direct AREG receptors.
2. Describe whether the marginal receptor/negative-regulator patterns coexist within cells, using depth-conditioned joint versus marginal expectations and donor-level summaries. Avoid a new receptor-minus-feedback score or arbitrary ratio.
3. Retain disease labels. A disease-stratified descriptive comparison or interaction is conditional on adequate independent donor support and identifiable covariates; the present review has not established that support. Compare raw-count pseudobulk summaries with the original mean-cell-log endpoint as **different estimands**, not interchangeable normalizations.
4. If useful configuration differences survive, nominate the recipient context for a source with actual AREG response. Otherwise stop at the descriptive result. Preserve the old 7/22 complex-coverage failure and the unsuccessful ligand model.

**Endpoint:** same-cell RNA configuration and paired recipient differences; **unit:** donor. This could distinguish coordinated recipient context from different subpopulations, but neither RNA negative-regulator expression nor co-detection measures effective inhibition or AREG dependence. Moderate incremental value; no full pipeline rewrite is justified.

## 5. Source-dependent extensions

| Owner | Ordered next sequence | Required new evidence and stop condition |
|---|---|---|
| A12 | Use the existing ten-gene IL-1 component result → locate cell-level counts and independently supported epithelial states from the same source, or a clearly separate reference → fix state labels without the receptor/response endpoints → compare receptor/accessory/decoy coexistence and state-standardized patient contrasts | Current pooled counts cannot supply within-cell structure. Preserve the 12 patient pairs and uncertain labels; NFKBIA/TNFAIP3 overlap the old response. No new predictive fit on the same exposed 12 patients. Stop the state-resolved step if cell/source linkage or label evidence is absent |
| A3 / DY1-P02 | Reuse the completed source audits → search beyond the already examined deposits for a non-infectious stimulation/withdrawal time course with RNA and ATAC, actual preparation identities and suitable controls → qualify time, assay, overlap and common peaks → only then specify a new temporal comparison | Original highlighted discordance is **bulk RNA versus separate bulk ATAC**, with scRNA providing composition evidence. Averaged GSE115504 RNA lacks replicate variance; separate bulk ATAC does not identify within-state changes. STAT6–EGR2–PPARgamma/RXRA and ARG1 remain fixed candidate context, not an assumed causal chain. Without matched temporal/unit evidence, no new maintenance analysis |
| A27 | Seek an independently annotated, age-resolved CD8 RNA plus receptor source → verify actual pairing, attempted/represented receptor denominators and clone sequences/identifiers → fix reference-based labels without age/clone outcomes → estimate within-state repertoire concentration only with supported mice | Original 354 RNA/288 represented cells and 237 blank-label singleton conventions remain unchanged. Annotation transfer cannot create absent receptor evidence. Do not tune labels to make previously unsupported groups pass. A larger genuinely qualified source can improve the question; relabeling the same sparse data alone cannot resolve it |

No new source satisfying these conditions was qualified in this review. These are metadata-search plans, not ready numerical runs. New public-source access may help; metadata APIs cannot manufacture unreported preparation identities, repeated measurements or functional endpoints. Author contact and controlled-access requests are not included.

## Remaining scope: retain rather than automatically rerun

- **A32 and Wg-P06:** retain the completed RNA/tracer screens. A32 still needs supported epithelial recovery and linked biological outcomes; Wg-P06 needs the exact nutrient/isotope mapping and linked ARG1–recipient exposure–collagen measurements. More pathway enrichment does not supply them.
- **A1/A4/A7/A14/A19:** lineage/history, starting-state, withdrawal and later-output linkage remain the discriminator. A14's checked supplements lack preparation-level qPCR values and experiment mapping. Repeating its same-day repository search or inferring values from plotted bars would not resolve that gap.
- **A15/A20/A21/A22/A23/A18:** active ligand, receptor-specific function, extracellular protein, transition rates or linked spatial units are missing, respectively. Existing static RNA or structure results should not be repackaged as those measurements.
- **A28/A29:** retain heterogeneous arm transfer and metabolic alternatives; transcript scores do not supply regulatory function, PEP concentration or flux.
- **Other 12 RQs (A0/A2/A6/A10/A11/A13/A16/A17/A24/A25/A26/A30):** dossier-level triage found no reason to rerun them solely because these tools are available. Existing transfer/model limitations, unmeasured delivery/function, missing or confounded units, clone identifiability, age/sex support and compartment measurement limits remain. This pass does not claim a deep re-audit of their implementations.

## Execution handoff if these follow-ups are adopted

1. Start with A5 annotation completion, then the bounded A31 conditional screen. A8 is an optional measurement-discrimination job; A9 is moderate. Keep the three source-dependent searches separate from numerical eligibility.
2. Each new job receives a distinct versioned contract and script/output path, honest prior-exposure record, fixed endpoints/units/support and source versions. Numerical precision/design choices still unresolved above must be settled before freeze. The original scripts and reports remain immutable.
3. Use Scanpy utilities only where they fit the original matrix semantics; do not wholesale replace custom donor-aware readers, exact sampling or clone rarefaction. No generic cell-level differential-expression test, imputation-based receptor rescue, batch-integrated expression test or UMAP-based mechanistic claim.
4. Independently review the new result, including null/mixed/unsupported outcomes. Update the owning RQ README/context/dossier and the paper package when relevant. A review or execution receipt never assigns human scientific acceptance.

## Review provenance and limitations

Primary method/capability pages were checked live on 3 November 2026: the four official links above. Searches were `site.uniprot.org help evidence attribution GO annotations experimental computational`, `site.scanpy.readthedocs.io pseudobulk differential expression biological replicates`, and `site.chanzuckerberg.github.io cellxgene census raw counts donor_id datasets`. The Nature full-text page for the replicate-aware DE paper returned an access error; no full-paper read is claimed or relied on. Existing same-day biological source reviews and amendments were reused for unchanged premises. No new literature-wide novelty search, protein annotation retrieval, matrix download, package installation, workflow launch or benchmark was performed.

This plan recommends information gains, not more favorable outcomes. It changes neither the interpretation of the seven completed runs nor the remaining biological holds without new evidence.
