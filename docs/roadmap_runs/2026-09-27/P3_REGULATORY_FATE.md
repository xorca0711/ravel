# P3 — Regulatory-to-fate linkage feasibility

**Status: feasibility audit and feature/outcome nomination completed; predictive fitting remains blocked by missing linkage.** No available candidate reviewed here supplies the required replicated earlier regulatory feature and later independent outcome on linked biological units.

| Candidate | Available evidence | Why it cannot pass the intended linkage gate |
|---|---|---|
| Tsutsui direct marks and culture outcomes | 24 histone tracks, two preparation labels, one parental line; separate culture endpoint summaries and 64 sequencing records | No verified early-assay-to-later-descendant pairing; no compatible normalized perturbation inputs established |
| HPCS lineage/RNA | 22 named mice reconstructed | Chase remains aliased with sequencing library; matched earlier regulatory assay absent |
| AP-1 regional lineage endpoint | Three mice per genotype with fields nested within mouse | HOPX acquisition is an endpoint description; no paired early regulatory feature or independent mature function |
| Choi ATAC GSE144598 and scRNA GSE145031 | Two ATAC biological sample labels per cell population; processed bigWigs combine replicates; independent sorted scRNA pools | Different sampling/pooled units, no individual early regulatory sample to future endpoint crosswalk |
| PATS chromatin/field source | Historical pooled chromatin and independent lineage-field evidence | Pooling/normalization limitations and no paired early-mark/later-outcome unit |
| TP53 selected gene lists | Previously audited selected directions | Selected significant lists are neither complete regulatory measurements nor linked future outcomes |

The [audit record](P3_linkage_audit.json) retains source hashes and verified dimensions. Existing A1 audits were reused. The additional Choi check uses [GEO ATAC metadata](GSE144598_sample_metadata.json) and [primary methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC7487779/): replicate-labelled bulk ATAC and pooled single-cell experiments cannot be joined by the fact that they appear in one paper.

## One bounded feature/outcome nomination

The [contract](P3_feature_outcome_contract.json) nominates **SFTPC-promoter H3K27ac relative to matched H3**, using the existing native-assembly locus and exact interval rule. SFTPC reflects AT2 identity, so the biological question is whether an earlier local regulatory measurement contains information about later mature contribution beyond the early RNA state. It could simply duplicate RNA; that is the comparison to test. The feature was chosen with prior source exposure and is not an independently discovered predictor.

The outcome is an independently gated mature descendant yield per initial labelled input, with absolute survival and descendant counts. A protein/morphology endpoint supports lineage contribution; it does not supply an unmeasured functional assay. Assay/time compatibility and independent-unit precision must be fixed before scoring a future cohort. This document does not pretend those missing design fields are already resolved.

A different paper, different preparation or destructive assay cannot be silently paired to a later fate observation. For prediction, hold out the biological level to which the claim will generalize. For causation, a separate regulator perturbation with engagement and survival checks is required. A genotype effect should not be estimated by conditioning on a treatment-created state without acknowledging that change in estimand.

## Decision

Keep the current regulatory and lineage descriptions separate. No feature search, integrated embedding or predictive fit is launched. The next necessary acquisition is a verified early-feature/late-outcome crosswalk with compatible measurements; its absence is the explicit data requirement. This is a bounded feasibility result, not evidence that no suitable study exists anywhere.
