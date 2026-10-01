# Nb3 reproduction review

**1 October 2026. Analysis ID Nb3; folder `gate2_N2_nabhan_2026`.** This package
implements a source-informed reconstruction and first descriptive extension
pass after the owner read the paper. It preserves previous A10/A2 fits and the
original intake record. The [execution guide](../EXECUTION.md) gives commands,
versions, frozen choices and output locations.

**Material finding:** mouse source-selected DE effects have median Pearson r
**0.9606**, while human labeled S5 effects have median r **0.0035**. Human S5 also
contains internal sign conflicts between its up/down lists and numeric logFC
columns. The published human numeric DE table is **not reproduced**. Nb3's
count-derived results remain separately recorded; see the
[concordance audit](CONCORDANCE_AUDIT.md) before interpreting the fibroblast arm.

## Stage ledger

| Stage | Current output | Verdict and boundary |
|---|---|---|
| Nb3_00 | Exact-hash counts/Xenome recovery, S1–S7 recovery, 886-library design/feature audit | Executed; 203 labels resolve to 201 targets plus two references. Preparation identities remain unresolved. |
| Nb3_R1 | Both imaging days, three endpoints, two declared scaling variants | Executed source-informed reconstruction; original source scaling details remain ambiguous. SAM/embedding morphology not regenerated. |
| Nb3_R2 | Full counts, QC/TMM and 395 eligible per-target limma-voom fits | Computation complete; mouse source concordance is high, human numeric S5 reproduction fails. Source-table internal conflicts trigger an explicit hold. |
| Nb3_R3 | S6 activities, S7 projections, fixed-marker rows from both S3 budding comparisons | Partial source-table reconstruction. Exact cPCA/JADE refit, component stability and source gene-set enrichment remain incomplete. |
| Nb3_R4 | Paired marker-panel contrasts, depth/growth and leave-target-out diagnostics | Executed descriptive reconstruction; not exact source high/low-growth grouping or independently identified cell states. |
| Nb3_R5 | Three public GEO metadata audits | Spatial/external fitting held pending named design/source mappings. |
| Nb3_R6 | This ledger, discrepancy audit, extension review, figures and verification | Completed first-pass review with a failed human numeric reproduction and other named holds; no claim-grade upgrade. |

## Source identity, counts and QC

The count workbook contains **52,636 mouse genes** and **58,302 human genes**,
each across **886 libraries**. Full integer count extraction exactly reproduces
every archived A10 species/library total. Under the declared `count > 0`
detection definition and the source cutoffs, **850 mouse** and **771 human**
libraries pass. The paired intersection is **771**, including **99 paired
reference wells**. These are bulk read-count libraries, not single-cell UMIs.

Supplement S2 resolves **856 libraries** to mouse gene IDs by plate/position;
all IDs exist in the count annotation and all target labels agree after
punctuation normalization. The **30 unmapped libraries are tdTomato references**.
NKX21 maps to source Nkx2-1; CTNNB1 is an activating edit. Guide pools, well
positions and targets are largely confounded. RNA changes do not establish
protein editing efficiency.

All **886 Xenome partitions sum exactly to their input reads** and join correctly.
The median unambiguous-assignment fraction is **0.778**. Deposited host/graft
labels are retained where their species mapping is undocumented. Neither read
fractions nor species-specific library totals are direct cell-count estimates.

Evidence: [extraction](../runs/R2_v1/extraction_record.json),
[library QC](../runs/R2_v1/library_qc.tsv),
[target identities](../runs/00_v1/target_identity.tsv),
[Xenome audit](../runs/R2_v1/xenome_QC_record.json).

## Imaging: broad source pattern recovered under declared choices

The primary day-14 reconstruction finds **30 count**, **17 mean-size** and
**26 coverage** target contrasts with technical BH q below 0.05. These are
diagnostics of the source-informed well-level model, not independent biological
discoveries. Excluding tdTomato from the scaling population leaves those counts
unchanged; effect sizes from both variants remain available.

| Target | Count effect | Mean-size effect | Coverage effect |
|---|---:|---:|---:|
| NKX21 | +1.329 | +5.373 | +6.397 |
| CTNNB1-active | −0.078 | +2.419 | +2.383 |
| ERBB2 | −0.479 | −1.636 | −1.393 |
| ERBB3 | −1.790 | −2.012 | −2.331 |
| EGFR | +0.044 | +0.106 | +0.098 |

Units are within-plate SD contrasts against matched-plate TIGIT. Size retains
the deposited measurement scale; coverage is the source bounding-box union
measurement. The exact original transformation, scaling set, joint-day handling
and multiplicity family are not fully specified. Consequently this is a declared
reconstruction variant, not an assertion of pixel-for-pixel or coefficient-exact
reproduction. Original images/embeddings are needed for the SAM/cPCA morphology arm.

Evidence: [all effects and technical intervals](../runs/R1_v1/imaging_effects.tsv),
[run record](../runs/R1_v1/run_record.json), [figure gallery](../FIGURES.md).

## Expression and source agreement

The frozen model uses species-wide TMM, per-target voom/limma with in-plate
TIGIT/tdTomato controls, a plate covariate when necessary, BH across the full
nonzero fitted gene universe, then AveExpr > 1.5 for the diagnostic DE count.
The source's exact TMM recomputation and filter/BH order are unresolved. All
choices and the installed limma/edgeR versions are recorded rather than
silently equated with the original implementation.

The complete run fits **200 mouse** and **195 human** target contrasts, with
**47,210/51,742** nonzero genes in the respective fitted universes. Seven
species/target combinations do not meet the declared design floors. The source
comparison uses 5,136 S4-selected mouse genes and 7,195 S5-selected human genes.

| Source-selected comparison | Mouse, 200 targets | Human, 195 targets |
|---|---:|---:|
| Median Pearson logFC correlation | 0.9606 | 0.0035 |
| Pearson range | 0.7682 to 0.9989 | −0.0647 to 0.0409 |
| Median Spearman logFC correlation | 0.9495 | 0.0034 |
| Median sign agreement | 0.9039 | 0.5048 |

NKX21 mouse has Pearson r **0.9989**; NKX21 human has **−0.0647**. This is
conditional on genes selected by the authors, not independent validation. The
human discrepancy cannot be treated as successful reproduction or concealed
by the mouse agreement. A targeted audit checks source-table consistency and
count extraction; no source label is silently repaired.

The audit finds 8,987 sign conflicts inside S5, compared with zero in S4. Human
source **direction lists**, separately, match our signs in 5,253/5,254 pairs for
five inspected targets. Three exact human gene rows (2,658 count entries) match
an independent XML reread. These support the count-derived directional analysis
while leaving numeric S5 reproduction unresolved.

Evidence: [source concordance](../runs/R2_v1/source_concordance.tsv),
[gene-DE design summary](../runs/R2_v1/DE_summary.tsv),
[focal gene-level results](../runs/R2_v1/focal_gene_DE.tsv),
[complete run record](../runs/R2_v1/expression_record.json),
[DE-file hashes](../runs/R2_v1/DE_manifest.json).

Large fold changes are not automatically eligible or precise. For example,
Hnf4a in the NKX21 mouse fit has logFC about **+6.962** but AveExpr **0.923**, below
the declared downstream expression filter. Sftpc has logFC about **−4.139** but
technical adjusted p about **0.312**. The fixed gastric/AT2 marker summaries use
their separately declared score definition; they do not override gene-level
uncertainty or the DE expression filter.

## What was reconstructed from source tables

S6 supplies **200 target profiles across 20 components**. S7 supplies **10,589
gene projections per component**. Original component identities and signs were
retained, with the declared 200 largest absolute projections displayed per
component. These values were not independently learned again from the new DE.
Both S3 budding contrasts contain **47,246 gene rows**; **62 fixed-marker rows**
were recovered across the two comparisons without redefining morphology.

The Wnt/AT1 panels were visually checked against Fig. S7 before scoring. The
complete panels include Tgfb3 and Cav1, respectively; the exact amendment is
recorded. The hypoxia panel uses Aldoa from the figure. Fixed-panel presence in
the count matrix does not imply presence in the more restricted source ICA
universe. Missing ICA genes stay missing.

Source-table outputs: [activities](../runs/R3_v1/source_ICA_activities.tsv),
[projections](../runs/R3_v1/source_ICA_panel_projections.tsv),
[top projections](../runs/R3_v1/source_ICA_top200.tsv),
[budding markers](../runs/R3_v1/source_budding_markers.tsv).

## Paired fibroblast reconstruction and extension boundary

All required fixed-panel genes were present. Of 4,221 planned panel contrasts,
4,150 meet the technical design floors. NKX21 pairs decreased epithelial AT2
markers with decreased fibroblast chemokines and increased wound markers.
The [extension review](EXTENSION_REVIEW.md) reports effect sizes, technical
intervals, the modest cross-target associations and counterexamples. These
marker summaries do not reproduce the exact author-selected high/low-growth
groups in Fig. 4G or measure fibroblast heterogeneity.

The normalized-panel branch completed before the whole-transcriptome DE loop.
Its inputs were hashed in [panel_input_record.json](../runs/R4_v1/panel_input_record.json)
before extension fitting; no downstream DE result was required to choose or
change a panel. The source-wide comparison remains part of the final review.

## Holds that remain concrete

- **Exact cPCA and JADE:** original cPCA alpha, transform/background details,
  ICA input-selection/scaling details and source component-stability settings
  are not recovered. The paper's availability statement points to GEO and the
  supplement, not a separately identified analysis-code release. Ordinary PCA
  or FastICA was not substituted. Complete pathway enrichment also needs the
  original gene-set/version definition.
- **Human numeric S5:** recover a reconciled gene/target-to-value mapping,
  corrected table or original generating code before claiming human DE
  reproduction. Keep the source numeric fields, source direction summaries and
  Nb3 count-derived results as distinct evidence layers.
- **Spatial Fig. 5:** all four GSE307128 records say bleomycin, while the source
  experiment describes AAV perturbation. Sample-to-animal mapping, treatment/
  timing and grid/region definitions need reconciliation. The current metadata
  do not establish that these are interchangeable designs.
- **External source comparisons:** Toth GSE215824 and Reyfman GSE122960 were
  identified. Exact source cell/PCA annotations and independent biological
  units remain necessary; reuse of cohorts already used by the paper is source
  reconstruction rather than fresh validation.
- **DepMap and receptor mechanism:** the release, assay and 93/96 line-count
  discrepancy remain unresolved. Expression and growth effects do not establish
  AT1 receptor function, the EGF recipient, AT2 cancer origin or clinical fibrosis.

See the [context eligibility audit](CONTEXT_ELIGIBILITY.md) for retrieved GEO
records. No large spatial archive, controlled-access human FASTQ or clinical
causality analysis was needed for the completed descriptive work.

## Verification and provenance

The full-count totals, stable identifiers, library joins, species QC, design
ranks and source hashes were checked during execution. The final
[verification script](../scripts/11_verify_execution.py) independently recomputes
18 imaging effect/SE pairs and all NKX21 panel contrasts, then checks run and
DE-file provenance. Figure QA preserved the initial association export and
created a layout-only revision to separate overlapping labels.

The [computation verifier](Nb3_computation_verification.json) passes **709 checks**,
including all 395 DE-file hashes, source ICA activity values, figure integrity,
18 independent imaging effect/SE recalculations and all 21 NKX21 panel contrasts.
This verifies computation/provenance; it does not make the human source-table
comparison pass. Repository tests pass (52 passed, one skipped), as do existing
claim/Nb1/A16 provenance checks. The full repository validator currently reports
24 links in the untouched, untracked adversarial-audit file; no Nb3 link failure
was reported in that run. The [repository verification record](Nb3_repository_verification.json)
also records 521 passing checks across the 18 changed/new Markdown documents,
JSON parsing and the discrepancy-audit hashes.
The original intake verification is historical. Source PDFs, private notes,
full matrices and full DE files remain ignored.
