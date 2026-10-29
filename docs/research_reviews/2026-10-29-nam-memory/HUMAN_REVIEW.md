# Independent review of the DY1 human extension

29 October 2026. Coordinating reviewer; technical and interpretation review, not human scientific acceptance.

## Verified execution

The separate analysis chat completed the exposed GSE136831 descriptive run from freeze `aad1d86c13d989dc12a1aaff08ef7f3c2297f71a`. The reviewer checked the numerical specification and code before execution, then inspected saved tables and both figures. All 312,928 cells matched deposited total counts and detected-gene counts; 107 libraries were nested within 78 donors. Age and recorded sex were recovered through exact public GEO joins before numerical freeze.

The reviewer independently matched the contract and five code/configuration files to frozen Git blobs and all 13 declared outputs to receipt hashes. Receipt SHA-256: `838fd62f55345949c332b1bf61b729800cfc2d8a3298d880f0d1ef52bbe51255`. The run's separate arithmetic verifier passed 27,545 scalar/array checks, including 52 primary correlation rows. These are computational checks on the same source, not independent biological replication. Bootstrap procedures have synthetic arithmetic tests; pointwise intervals do not establish multiplicity-controlled discoveries.

[Run receipt](../../../analysis/research/runs/DY1_human_observational_v1/receipt.json) · [Numerical specification](../../../Research%20Article/gate2_DY1_damani_yokota_2026/HUMAN_NUMERICAL_PLAN.md) · [Current article ledger](../../../Research%20Article/gate2_DY1_damani_yokota_2026/README.md)

## Findings that constrain interpretation

The frozen primary population is deposited **Macrophage**, with at least 20 cells per donor for expression. All other annotations, marker proxies and cell floors remain sensitivities. These are not validated NAM labels.

| Primary observation | Estimate and support | Interpretation |
|---|---|---|
| IPF minus Control matrix-associated macrophage panel | +1.139 mean-log2(CPM+1) score units; pointwise 95% interval 0.824 to 1.459; 32 versus 28 donors | RNA-panel difference in this atlas. The direction persists across the six prespecified population definitions at floor 20; not matrix production or regulatory activity. |
| IPF minus Control FABP4-associated panel | +0.172; interval -0.250 to 0.591; age/sex-adjusted descriptive coefficient -0.266 | Weak, adjustment- and annotation-sensitive disease contrast. No general protective-program conclusion. |
| FABP4 versus matrix-associated panel within IPF | Spearman rho -0.624; interval -0.804 to -0.339; n=32 | Negative association persists in the declared proxy/all-macrophage sensitivities. Inherited RNA labels, source-selected genes and cell mixture remain explanations; no causal antagonism inferred. |
| Macrophage matrix panel versus fibroblast-union matrix panel | Pooled rho 0.485, n=49; within IPF rho -0.073, n=26; pooled adjusted rho 0.049 | Pooled coupling is not stable evidence of a within-disease source-to-recipient mechanism. IPF uncertainty remains wide; this is not proof of no association. |
| IPF minus Control ARG1 RNA | -0.250; interval -0.451 to -0.032 | Sparse captured-cell transcript measurement. Only 143 of 60,483 IPF primary-annotation cells detect ARG1, versus 126 of 40,747 Control cells. No enzyme activity, metabolite transfer or tissue-wide source inference. |

All predefined comparisons remain in the saved tables, including null, negative, sparse and constant-variable results. No neutrophil annotation exists in this atlas. Multiplets are retained only for audit, not source attribution. The scores are analyst adaptations of published human gene lists; the Apte lists reused this same atlas. The analysis cannot independently validate those lists.

## External-cohort review

The exposed GSE135893 comparison executed from freeze `d4ee3cb474784ea9125aa945a14f107a52583a42`: 12 IPF and nine eligible Control donors, with the inherited 50-cell floor and different source macrophage annotations. The reviewer checked the code and contract before execution, inspected its figure and tables, and matched five frozen code/configuration files and all eight outputs to their hashes. The independent arithmetic check passed 184 comparisons. Receipt SHA-256: `47ba5433a1bc301441876e9b116a0017b7e6e5e9dd57be282b68fc6e9722a95c`.

The matrix-panel IPF–Control difference is +2.230 [1.394, 3.111] score units. Restriction to the common Vanderbilt source (seven IPF/six Control donors) retains a positive difference, +2.509 [1.337, 3.662]. FABP4-panel differences are negative, but its common-source interval crosses zero. Within-IPF panel covariance has rho -0.545 [-0.889, 0.090]; this is less precise than the primary atlas. ARG1 is sparse and its external mean-difference interval spans zero. These pointwise descriptive intervals do not certify replication of a mechanism.

Qualification preserved an initial historical-script hash failure, then bound the exact historical Git blob and independently reaggregated current raw counts. All 85 cached units matched raw totals and nCount_RNA; all 29 exactly mapped selected genes matched. SELENOP remains unqualified under its exact symbol. The numerical comparison uses only the nine verified outcome genes, without aliases or a marker-proxy claim. Other fibrosis diagnoses are excluded from IPF. No external recipient correlation is fitted: its available seven IPF/three Control fibroblast donors fail the fixed eight-donor minimum. Source labels, selection, annotation and unqualified clinical covariates remain limitations.

[External receipt](../../../analysis/research/runs/DY1_external_human_observational_v1/receipt.json) · [External plan](../../../Research%20Article/gate2_DY1_damani_yokota_2026/HUMAN_EXTERNAL_PLAN.md)

## Consequence for the next question

The completed human work supports a bounded question about the transport of **measured macrophage RNA differences and covariance** across donor cohorts and annotation choices. It does not yet nominate a new mechanism. The remaining alternatives include disease mixture, captured cell composition, source-dependent labels, depth and unmeasured clinical factors. The external comparison supports transport of the matrix-associated RNA difference while leaving panel covariance less precise. It cannot turn RNA into enzyme activity or establish signaling direction.

The paper's STAT6–EGR2–PPARγ/RXRA premise and ARG1 functional contribution retain the original review's distinctions. This human run does not estimate that regulatory chain, chromatin memory or a training-specific genotype interaction. The broader mouse numerical stages remain separately unresolved; their platform restriction must not be relabeled a biological data failure.

Existing A1/A2/A8/A14/A19/A22 retain their endpoints and current evidence. The RQ-local context notes link to the article-owned results; they do not add RQ estimates, change registered hypotheses or supply missing lineage, timing, ligand availability, protein-output or functional-reserve measurements.

External-source qualification, executed comparison and their retained limitations are recorded in the current article ledger. Full stage-8 mechanistic integration remains conditional on the unresolved original stages; this review completes only the human-context interpretation.

## Diagnostic preservation review

The reviewer independently checked all seven original-to-archive byte identities in the [preservation record](../../../analysis/research/runs/DY1_human_evidence_preservation_v1/preservation.json). The failed qualification receipt still says `execution_failed`. The successful wrapper records archival copying only, following the existing Nb5 convention. Original local bytes and commits remain available; exact local Git exclusions cover duplicate originals while registered archive outputs remain tracked. Root `.gitignore`, validators and governance were not changed. The separate analysis chat also reviewed the six RQ context notes and primary reviewer interpretation without a blocking finding.
## Final integration validation

Stable handoff `0fb28f0c6dc1a4398140f1e0098b91b7857344be` was integrated into the review worktree. The added RQ notes, roadmap, current-state summary and review navigation passed **11,482 repository checks** and the base-aware research gate against fetched main `78320a186b6f52426e7c7c5349a2f26492b718b7`. All 32 canonical question and guide records match that base; root ignore, governance, schema and validator files are unchanged. The source chat's 161 repository tests (one skip), 27 targeted tests and required evidence verifiers were reused because integration changes documentation only. Both numerical output sets and all seven preserved diagnostic/source files were independently hash-checked; no biological analysis was rerun. The original mouse numerical components and full mechanistic integration remain incomplete under the explicitly recorded restriction.