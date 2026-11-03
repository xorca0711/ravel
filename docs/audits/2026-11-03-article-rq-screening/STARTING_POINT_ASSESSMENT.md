# Starting-point assessment: metadata that could change an RQ decision

Artifact type: `starting_point_assessment`. Date: 3 November 2026.
Objective: identify useful additional screening for existing RQs and incomplete
article work, without relabeling a source hold as a negative finding or a
metadata inventory as completed biological analysis. All prior results are
exposed. No new RQ, numerical contract, biological outcome or acceptance decision
was created in this assessment. No pending owner decision is needed to report it.

## Observed material and supportable tasks

| Screen / owner | Observed starting material and provenance | Decision-changing next check | Conditions, endpoint and stop rule |
|---|---|---|---|
| A30 identity recovery | [Frozen state code](../../../Research%20Article/gate2_W2_wagner_Th17_PGAM/scripts/a30_state_decomposition_v3.py) and [receipt](../../../analysis/research/runs/wp_a30_state_decomposition_v3/receipt.json). Code uses a fixed seed and single-worker processing, then exports donor/tissue/stratum/state/scores without GSM/barcode identity. Six named raw inputs exist under `X:/GitHub/ravel/raw_data/wagner_pgam_w2_20261004/`; the two derived inputs are tracked. Raw files are absent at the equivalent paths in this worktree. | Hash-qualify the cache against the original receipt and inspect the exact dependency/runtime record. If adequate, design an isolated reconstruction that carries raw identifiers through the original transformations and validates saved memberships/output correspondence. | Metadata endpoint: proven source-cell-to-state mapping. No row-position, equal-count or expression-similarity join. Do not replay the old overwrite-prone entrypoint in place. If runtime or membership reproduction fails, preserve that result and retain the hold; a new clustering is a different amendment. File presence is not hash or runtime qualification. |
| Nb5-P06 / A26/A27 receptor ascertainment | [Source manifest](../../../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/SOURCE_MANIFEST.md), [completion report](../../../Research%20Article/gate2_N4_nabhan_aging_atlas_2020/EXTENSION_COMPLETION.md). Main-cache full/FACS metadata headers contain cell, mouse, age, sex, tissue and annotation fields. The pinned notebook references separate `cell_data_tracer_3m/18m/24m.csv` files and age-specific identifier transformations. | Qualify all captured CD8 cells against attempted and successfully reconstructed receptor records, with productive-chain/multiple-chain status if actually available. Verify each age-specific ID transformation rather than copying it blindly. Inspect whether any marrow/CD8 pairing exists before a tissue contrast. | Animal is the biological unit; cell-level recovery is a measurement endpoint. The inspected metadata headers do not contain productive-chain or recovery-status fields. If these records or fine states cannot be recovered, keep only the already established conditional-on-recovery result. Do not infer failed reconstruction from absent rows without knowing the attempted-cell universe. |
| Nb4-P03/P05 / A6 | Existing [proposal scope](../../../Research%20Article/gate2_N3_travaglini_nabhan_lung_atlas_2020/reports/proposals/README.md), [A6 boundary](../../../RQ_Specified/A6_ipf_macrophage_state_composition/README.md) and reused IPF source records. | One source-overlap/donor/diagnosis/author-state crosswalk; then count support for a source-justified shared macrophage state without inspecting its outcome to choose it. | Donor, not library or cell, is the unit. Primary control support failed for the old proliferating-state comparison. A qualifying fixed contrast can justify a new exposed descriptive design; another pathway or merged state chosen to pass the gate cannot. Already reused cohorts are not newly independent evidence. |
| Nb1 / A4/A19 context | [Existing GSE129605 eligibility record](../../../Research%20Article/gate1_03_nabhan_2018/external_feasibility/README.md); primary series metadata freshly read below. Eight libraries were acquired previously; exact animal/state qualification remains incomplete. | Retrieve sample/BioSample/author annotation correspondence and resolve whether saline and injury libraries represent independent mice; inspect fixed AT2/fibroblast support. | Keep the existing three-animal/arm and 50-cell/compartment gates. These are eligibility floors, not power calculations. A qualified day-11 expression contrast cannot establish Wnt-history switching, secretion, receptor specificity or fate. No expression matrix was opened in this refresh. |
| Wg-R4 / Wg-P03/P04; A1/A14 measurement analogy | [Current Wg hold record](../../../Research%20Article/gate2_W1_wagner_th17_autoimmunity/PRE_RQ_EVIDENCE.md): 12 source ATAC records, exact peak/count and S7 problems; historical runtime exit. | One bounded source-access check for GSE165088 count/interval files and S7, then exact sample/coordinate/reference/replicate mapping if recovered. | Current refresh did not recover a usable record. Even successful access would not establish cross-assay physical pairing, a lung mechanism or function. R2 model/runtime qualification is separate; the Wp solver does not certify Wg's historical model/configuration. |
| Niethamer D1 / immune-state context | [Stage-2 plan](../../../Research%20Article/gate1_01_niethamer_2025/ANALYSIS_TRIAL_PLAN.md) names GSE292440/GSE277256/GSE277226 and GSE300399. | Establish actual Treg purification/author identity, disease/time/context and independent sample map before deciding whether the old D1 question is supported. This pass attempted the two named series below, not all four. | Access failed for the attempted records; no Treg presence/absence or completed gate is inferred. S1 is separate: phase separation after looking at scores cannot become independent confirmation or STAT activity. |
| DY1 / Arz1 / Sx22 source-dependent jobs | Their current ledgers already identify missing CMO/pool/state maps, exact reference/pipeline versions, raw panel identities and early-to-later unit links. | Inspect a newly located export/supplement or a specifically justified operational-annotation amendment, rather than repeat the recent inventories without a new route. | Operational annotation is an adaptation and must avoid circular target-based state definition. It does not recover author identity, independent animals or missing functional units. No extra RNA/locus panel is an answer to an absent join. |

For A30 the old receipt records Python 3.12.14 on AMD64; the recent cut-or-fill
run used Python 3.12.10 on ARM64. Seeds and file existence alone therefore do
not certify reproducible clustering. No raw cache was moved, no receipt was
changed, and no reconstruction or score was calculated here.

## Coverage of all 33 existing questions

This reuses the [all-question cut-or-fill decisions](../2026-11-03-rq-evidence-trajectory/CUT_OR_FILL_PLAN.md).
It is a screening disposition, not a portfolio keep/reject decision.

| RQs | Additional screening disposition |
|---|---|
| A0, A10, A11, A13 | Same-input rescue routes stay closed. Only a new independently justified source/endpoint/unit relationship can reopen a distinct comparison. |
| A1, A7, A8, A14, A16, A18 | Source screening should seek the missing baseline/lineage/time/protein or spatial-unit links. New RNA signatures do not supply these measurements. |
| A2, A9, A15, A20, A21, A22, A23, A24, A28, A29, A31, A32 | Screen actual assay and unit metadata: effective input/engagement, active ligand, function, extracellular output, transport, barrier, metabolic or mature-output endpoints as appropriate to the existing plan. No generic atlas scoring package is justified. |
| A3, A6 | Qualify age/origin/current-context or donor/state support. Niethamer and Nb4/DY1 source context remain distinct contrasts; avoid interpreting unmatched residuals as memory. |
| A4, A19 | Nb1 external metadata is an expression-context opportunity only. The registered lineage/receptor/functional questions still require their specific measurements. |
| A5, A12 | Fresh bounded source passes just completed. Reopen with the named mapping/eligible paired-cohort evidence, not another identical search or threshold relaxation. |
| A17, A25 | New bounded analyses complete. A17 needs justified observation/model constraints; A25 needs independent support for a new comparison. Do not launch another fit or tune the representation after its mixed result. |
| A26, A27 | Receptor-recovery and fine-state/source pairing are useful next qualifications. Existing public-source reuse stays distinct from independent replication. |
| A30 | The local archive/code inspection identifies a concrete reconstruction-feasibility route; original hash/runtime/membership gates still need to pass. |

## Primary-source refresh and exact access coverage

Search date: **3 November 2026**. Discovery query through web search:
`mouse aging spleen bone marrow paired single cell TCR RNA sequencing dataset GEO`.
No date/domain restriction was applied on discovery; secondary hits were not
used as final evidence. Three subsequent accession-specific discovery searches
(`site.ncbi.nlm.nih.gov/geo GSE165088 supplementary count`,
`site.ncbi.nlm.nih.gov/geo GSE292440 Loffredo`, and
`site.ncbi.nlm.nih.gov/geo GSE300399`) returned no usable accession record.
This is a bounded source-eligibility screen, not a systematic literature review,
novelty search or completed paper-methods review. Older close candidates and a
2026-updated candidate were retained, including unfavorable eligibility findings.

Browser-service GEO opens returned challenge pages or internal access errors.
The restricted shell then failed DNS. A single authorized read-only retry of
the six public GEO text records outside that network restriction recovered
three series records and timed out on three. Each request used
`acc.cgi?acc=<accession>&targ=self&form=text&view=full`; no authentication,
challenge-solving, author contact or account write was involved. Full series
metadata is not the sample-level independence/state crosswalk.

| Primary source / exact locator | Observed result and implication | Source version and acquisition evidence |
|---|---|---|
| [GSE275967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE275967), Title, Summary, Overall design and supplementary-file inventory | Aged WT versus muMT splenic T cells, with expression, clonotype and filtered-contig files listed. No young group or paired marrow comparison in this series design. Do not admit it as direct A26/A27 age replication. Mouse-level pooling/identity would additionally need qualification. | Series last update 2 April 2026. Full text record 3,111 bytes; SHA-256 `c31ce94494b97103846879fd23a79bebdb42657d7d28dc830b3c93706116241b`. Listed data were not downloaded or analyzed. |
| [GSE155005](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155005), Summary and Overall design | Young donor CD8 cells pooled from three mice, transferred into an aged recipient, with donor/recipient cells sampled from spleen later. This is a transfer-context design, not independent baseline young/old replication or spleen/marrow pairing. | Last update 6 December 2020. Full record 3,500 bytes; SHA-256 `6b689a4b8f6b4f92fdcac2e60799bde07ffcef7bec11dace78a0eaa67ba65509`. No raw archive opened. |
| [GSE129605](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129605), Overall design and supplementary-file inventory | Saline, injury and treatment groups, male mice and day-11 isolation are recorded. This confirms the existing Nb1 context; it does not resolve library-to-animal or author-state mapping. The treatment arm is not added to the frozen saline/injury contrast. | Last update 14 April 2019. Full record 3,068 bytes; SHA-256 `80fa986124540a1a141fab8bbad249ed2f3261a2008561524a9016eb3d2eaeec`. |
| [GSE165088](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165088) | Current primary-record read timed out. Old exact count/annotation/source holds remain; no new availability conclusion. | No validated source bytes recovered in this refresh. |
| [GSE292440](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292440), [GSE300399](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300399) | Both text-record reads timed out. D1 eligibility was not assessed from these attempts. GSE277256/GSE277226 were not refreshed. | No validated source bytes recovered. These are access failures, not biological/data-absence findings. |

Task-local snapshots and acquisition errors are retained under ignored
`.tools/article_metadata_screen/`; the exact URLs, hashes and interpretation
above are the portable record. No paper version, accession or additional sample
identity was invented to compensate for a failed retrieval.

## Justified next handoff

The next technical assignment should start with the A30 hash/runtime feasibility
and the Nb5 receptor-assembly field/identity inventory. Each can terminate with
a concrete qualification result before any biological model. A6 or Nb1 screening
can proceed independently only with their unchanged source/state/animal gates.
Convert a successful qualification into a small prospective execution contract;
retain a failed one as a specific hold. The question-level outcome and article
reproduction remain owned at their existing paths. This document does not start
that execution, assert complete readiness or silently revise the RQ hypotheses.
