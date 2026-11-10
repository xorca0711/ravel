# Zh26-P01: released RNA reproduction and bounded sensitivity

10 November 2026 (Asia/Seoul). **Exposed source reproduction, not independent
replication or scientific acceptance.** [Figure guide](FIGURES.md) ·
[reviewed plan](ANALYSIS_PLAN.md) · [validation](VALIDATION.md).

The dated [interpretation/access addendum](INTERPRETATION_AND_ACCESS_V1.md)
explains these figures and narrows the next steps after fresh public-source
inspection: raw reads are accessible for a separately qualified adapted count
comparison; exact count/voom provenance and functional supplement acquisition
remain unresolved. Numerical findings and frozen evidence below are unchanged.

## What this work changed

The released TPM/limma-trend analysis is numerically reproducible. Every field
of all three 12,708-gene contrast tables agrees with the authors' exports within
the prospectively declared tolerance; the largest absolute discrepancy is
`9.95e-14`. This resolves the concern that the available matrices cannot
reconstruct the released RNA implementation. It does **not** resolve the
disagreement with the paper's count/log-CPM/voom description.

The fixed source panels retain their effect directions in all three
leave-one-experimental-block-out refits. Magnitudes vary, and many other genes
change sign. The three displayed enrichment sets retain their directions under
the prespecified moderated-t ranking, but their weights, leading edges and
P values change. In particular, the IFN-gamma response set for ITDT+aCD4 minus
ITDT has BH-adjusted P `0.1201` with released logFC ranking and `0.001024` with
moderated-t ranking. Its threshold-based description is method-sensitive.

The organizing biological question remains local immune regulation of NK tumor
responses. Zhang et al. already report the cDC2/CD4/IL-2-associated circuit
(Figures 6–7); their Figure 3 reports the RNA patterns reproduced here. These
are shared-source measurements, not new mechanistic evidence. The existing
[literature context](LITERATURE_CONTEXT.md) remains applicable without a new
literature search or new canonical RQ.

## Scope, units and threats

The two main comparisons are ITDT minus PBS and ITDT+aCD4 minus ITDT; the
released ITDT+aCD4 minus PBS output is also retained. The endpoint is a
modelled difference in transcript abundance in sorted pooled NK preparations.
There are nine libraries in three reported experimental blocks. Pool-member
mouse IDs, exact membership and animal reuse across assays remain unknown.
Blocks are not paired longitudinal mice; mice within a pool, genes and reused
source data do not add independent replication.

Input/version mismatch was the primary reproduction threat. It is narrowed
for these released outputs. Selection of recovered NK cells and differences
in their state composition remain biological alternatives. Neither bulk RNA
nor enrichment distinguishes those alternatives from within-state regulation.
The two main contrasts share ITDT libraries; opposite signs do not demonstrate
independent replication, rescue or mediation.

## Stage dispositions and evidence

| Stage | Disposition | Frozen contract and verified receipt |
|---|---|---|
| S0 | TPM source and crosswalk qualified; dependent count/functional holds retained | [Contract v3](contracts/S0.qualification_v3.json) · [receipt](../../analysis/research/runs/zh26_s0_qualification_v3/receipt.json) |
| S1 | Released numerical implementation reproduced across all genes/fields; source-derived panels and library diagnostics reconstructed | [Contract](contracts/S1.reproduction_v1.json) · [receipt](../../analysis/research/runs/zh26_s1_reproduction_v1/receipt.json) |
| S2 | All pathway ES, NES, sizes and leading-edge sets concordant; Monte Carlo P values not exactly reproduced; two source NA patterns retained | [Contract v2](contracts/S2.enrichment_v2.json) · [receipt](../../analysis/research/runs/zh26_s2_enrichment_v2/receipt.json) |
| S3 block | Completed; all fixed-panel directions retained, variable magnitudes and broader sign changes retained | [Contract v2](contracts/S3.block_sensitivity_v2.json) · [receipt](../../analysis/research/runs/zh26_s3_block_v2/receipt.json) |
| S3 ranking | Completed on the identical universe; 18 of 472 pathway/contrast ES signs change; displayed sets keep their signs | [Contract](contracts/S3.ranking_sensitivity_v1.json) · [receipt](../../analysis/research/runs/zh26_s3_ranking_v1/receipt.json) |
| S3 counts | Held: no qualified count-scale matrix, transcript annotation and length/aggregation treatment | [S0 qualification](../../analysis/research/runs/zh26_s0_qualification_v3/qualification.json) |
| S4 | Source-grounded endpoint synthesis complete below; numerical functional reconstruction held | No new numerical run; [paper evidence map](PAPER_REVIEW.md) and source-access evidence |
| S5 | Current synthesis and figure guide complete; no new target/RQ or acceptance decision | This report and [figure guide](FIGURES.md) |

## S0 source reconciliation

The [manifest](../../analysis/research/runs/zh26_s0_qualification_v3/source_manifest.json)
binds source URLs, exact SHA-256 values and author Git blob identities at commit
`61ac9a440ba3f9db754ff8b8ad5008b450e647c0`. All source acquisition occurred on
10 November 2026. Entries marked reused were preserved downloads from the
first acquisition attempt before its manifest completed; they do not claim a
separately recorded original request timestamp. Originals remain in ignored
`raw_data/zhang_2026/` and were not overwritten.

The 32,621-by-nine GitHub and GEO matrices have exactly equal numerical values.
GEO changes 2,682 symbols through R's `make.names(unique=TRUE)` convention;
the exact one-to-one conversion was verified with R, not a broad stripping of
prefixes. No missing, negative, nonfinite or duplicate sample/feature entries
were found. Source code explicitly identifies TPM, and library totals near
one million are consistent with that provenance; they are not qualified counts.
Refreshed GEO SOFT content matches the prior snapshot.

The [crosswalk](../../analysis/research/runs/zh26_s0_qualification_v3/sample_crosswalk.csv)
joins unique GSMs, named matrix columns, conditions and replicate keys, with
an independent sample-name check. The released design has rank five and four
residual degrees of freedom. The paper's three-to-four-tumor description and
the methods/GEO two-to-four-mouse description remain distinct; no pool sizes
or animal IDs were invented.

The current supplied PDF differs from the planning hash: SHA-256
`473c4e89ee0b6abdedf9ab6e1ba0ecb184283ecac42c4df0d9cb6f1856fa1a8e`,
16 PDF pages. Its first page identifies Zhang, Science Immunology 11 eadx4411,
10 April 2026. Byte equivalence to the recorded 15-page planning version is
not established. The [identity record](../../analysis/research/runs/zh26_s0_qualification_v3/paper_identity.json)
preserves both hashes without guessing why the file changed.

The [PMC author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC13334847/),
available since 7 July 2026, lists supplemental tables, figures/materials,
MDAR and data files S1–S17. Direct downloads returned HTML challenge responses;
the official Europe PMC supplementary-file API reported that this manuscript
is not available through its open-access retrieval service. The files are
**located but not acquired**, not proven absent. The PMC manuscript cites
“Zenodo” as reference 95 while pointing to bioRxiv DOI
`10.1101/2025.06.26.661417`; the supplied final article has the analogous
reference 89 discrepancy. Neither is a verified Zenodo accession. Publisher
access remains unavailable; a complete supplement/preprint/final-version
comparison has not been certified.

## S1 numerical fidelity and diagnostics

The source filter retains TPM greater than one in at least three libraries:
12,708 included and 19,913 excluded features, each with a retained reason.
The model uses `log2(TPM+0.5)`, `~0 + condition + replicate`, sum contrasts for
replicate, `lmFit`, `contrasts.fit` and `eBayes(trend=TRUE)`. All six exported
fields and all genes were compared with absolute tolerance `1e-8` plus relative
`1e-7`, fixed before the run for floating-point/CSV precision, not effect size.

| Released contrast | BH < 0.05 | Source display: up / down at BH < 0.05 and absolute log2FC > 1.5 |
|---|---:|---:|
| ITDT − PBS | 87 | 73 / 6 |
| ITDT+aCD4 − PBS | 1 | 0 / 1 |
| ITDT+aCD4 − ITDT | 152 | 7 / 120 |

These are reproduced source-model conventions, not newly validated population
discoveries. The [comparison report](../../analysis/research/runs/zh26_s1_reproduction_v1/comparison.json)
records zero missing/excess genes and independent NumPy least-squares and BH
checks. Maximum independent coefficient error is `5.55e-14`; BH error is below
`3.3e-15`. Block correction was also independently verified.

Source PCA uses centered and scaled log-transformed features. Per-library
profiles and the four fixed source panels retain all individual preparations
alongside group means. Heatmaps are labelled by their actual TPM transform;
the source's “log2CPM” legend is not reproduced as a semantic claim. IDE paths,
table plumbing and visual styling were adapted; source model choices were not.
PCA separation is diagnostic and supplies no hypothesis test.

## S2 enrichment fidelity and its limit

The pinned `msigdbr 7.5.1` / `babelgene 22.9` Hallmark and CP:KEGG membership,
uppercase rules, `AveExpr > 1`, logFC ranking, seed 42, `gseaParam=1`,
`scoreType="std"`, `minSize=0`, `maxSize=Inf` and `nPermSimple=3000` were retained.
Every pathway was kept: 236 per contrast. No uppercase duplicate was accepted.
[Membership and coverage](../../analysis/research/runs/zh26_s2_enrichment_v2/coverage.csv)
and all rank vectors are preserved.

The [full source comparison](../../analysis/research/runs/zh26_s2_enrichment_v2/source_comparison.csv)
has no pathway identity, size or leading-edge-set mismatches. Maximum absolute
ES and NES differences are `6.11e-15` and `1.45e-14`. Independent weighted
running sums verify all 472 ES values to `1.83e-13`.

P values are **not an exact replay**: maximum absolute P and BH differences
are `0.0533` and `0.0925`. The deterministic inputs/settings and normalization
agree; the original parallel backend/R environment is unreported, while this
run explicitly uses `SerialParam`. Backend/random-stream differences are a
plausible explanation, not a demonstrated attribution. Exact stochastic
reproduction remains unresolved; no extra permutations or alternative version
were chosen to obtain agreement. `KEGG_OXIDATIVE_PHOSPHORYLATION` and
`KEGG_PARKINSONS_DISEASE` have unestimated P/NES for the second contrast in both
source and replay because of unbalanced gene-level statistics. Their NA values
and fgsea warning are retained.

## S3 measurement sensitivity

Leave-one-block-out refits keep the original feature universe and model form.
Each retains six libraries, two blocks and two residual degrees of freedom.
All 76,248 coefficients independently agree with the balanced within-block
arithmetic (maximum error `1.18e-14`). All 54 panel/contrast rows retain the
full-fit sign for every omission (27 panel memberships, with Tigit appearing
in two panels). This is not 54 independent genes. Across all features, at least
one omission changes a sign for 5,015 genes in ITDT−PBS and 3,799 in
ITDT+aCD4−ITDT. No stability percentage or significance cutoff is used to
promote a claim; the ranges are not confidence intervals.

The separate signed-moderated-t sensitivity keeps exactly the same genes and
pathways. All 472 running-sum scores were independently checked, with maximum
error `1.75e-13`. Eighteen pathway/contrast ES directions change; the fixed
IL2/STAT5, TNF/NF-kappaB and IFN-gamma sets retain their directions in both
contrasts. Their [complete comparison](../../analysis/research/runs/zh26_s3_ranking_v1/ranking_comparison.csv)
retains changed magnitudes, leading edges and adjusted P values. The IFN-gamma
second-contrast result illustrates why a directionally consistent RNA pattern
can still have a ranking-dependent threshold-based description.

## S4 RNA and functional evidence remain distinct

| Published evidence | What remains supported by the source experiments | What this reconstruction adds or cannot resolve |
|---|---|---|
| Figure 3 | Sorted pooled NK transcript differences | Released numerical fidelity and bounded sensitivity only; bulk-state composition remains unresolved |
| Figure 5B–D | Granzyme/perforin protein, separate target-cell lysis and perforin-dependent tumor control | Reproduced granzyme RNA is compatible with the reported pattern; it does not measure cargo protein, killing or mediation |
| Figure 5E–G; main Results | Increased IFN-gamma and killing coexist with no CD107a increase in the stated stimulation assay | Retain the non-increase; higher cargo is the authors' explanation, not a measured release-rate result. Axes/main text identify F as IFN-gamma and G as CD107a; caption order differs |
| Figure 6B,D,F,H–M; Figure 7 | DC context, CD4 IL-2, NK CD25/pSTAT5 and IL-2 dependence/rescue in the tested models | Enrichment is transcript-set association. It cannot reconstruct secretion, receptor occupancy or signaling. Figure 6J's Tconv FOXP3-positive legend still needs gating/source clarification |
| Figures 1–2 and 7 | Mouse tumor trajectories, cell requirements and tested toxicity/model boundaries | RNA contains no paired multilevel mediator dataset or human therapeutic efficacy/safety endpoint |

Exact assay units and cross-panel cohort reuse cannot be recovered from the
unacquired data files/raw FCS. Tumor days stay within mouse, technical lysis
wells stay within preparation, and pooled sorts stay pooled. Numeric functional
reconstruction remains held; this does not erase the source-grounded synthesis.

## S5 decision, preservation and exact next steps

The authorized contribution is now a reproducible released RNA measurement
with explicit method sensitivity and access limits. No informative new
biological question beyond the published circuit is established here. No
target ranking, canonical RQ, wet-lab package, acceptance decision or portfolio
change is created. A33–A35 and the original D1 lung gate are unchanged.

Further count-model work needs qualified counts plus annotation/length and
aggregation provenance. Functional reconstruction needs the actual supplemental
tables/data files and assay/cohort identities, including the two figure-label
ambiguities. Exact GSEA P replay needs the source runtime/backend/random-stream
provenance. None requires repeating this completed RNA replay or literature
review. Author contact, publication and merge remain outside authorization.

The separate [failure-preservation contract](contracts/failure_archive_v1.json)
and [verified metadata receipt](../../analysis/research/runs/zh26_failure_archive_v1/receipt.json)
bind the complete [original-to-archive map](../../analysis/research/runs/zh26_failure_archive_v1/archive_manifest.json).
Original failed-run locations were retired from tracked delivery only after
exact-copy verification; their original bytes also remain locally under ignored
`raw_data/zhang_2026/failed_runs_v1/`. Historical contracts/receipts retain their
original input paths. If a historical preflight/replay is needed, restore those
inputs from the archive to the manifest's `original_path` and verify its SHA-256;
do not rewrite frozen records or replay into an old run ID.

Failed S0 v1 (BOM header), S0 v2 (unreconciled syntactic gene names), S3 block v1
(NumPy integer JSON serialization) and S2 v1 (NA report parsing) are preserved
with their receipts/logs and hash-bound as inputs to successor contracts.
The latter two calculations were reused byte-for-byte; reporting amendments
did not refit models, increase permutations or overwrite outcomes. Every
successor keeps the explicit prior-outcome exposure. Successful receipts mean
execution, not scientific acceptance.
