# DY1 follow-up feasibility after the completed extensions

30 October 2026, Asia/Seoul. Documentation and source assessment only; no new
numerical analysis, frozen contract, canonical RQ or scientific acceptance.
All prior outcomes are exposed. The existing E1–E6 dispositions remain in the
[execution report](EXTENSION_RESULTS_2026-10-30.md); the suggestions below are
additional prospective work, not retroactive requirements for those runs.

## Cross-check: paper, notes, presentation and repository

Read the supplied version-of-record PDF (DOI
[10.1038/s41586-026-11060-y](https://doi.org/10.1038/s41586-026-11060-y)), its
cached extracted text and rendered Fig. 3 page, the supplied presentation text,
and the owner's current Epigenetics and Research-themes Notion pages. The notes
are source material, not execution instructions. Private source text is not
republished here. The scientific connection is regulatory state versus RNA state,
persistence versus continuing niche input, and inflammation-associated repair.
The PI-planning page was not needed or re-read for this assessment.

| Topic | Reconciled finding and implication |
|---|---|
| RNA–ATAC discrepancy | Fig. 4 compares late **bulk RNA with separate bulk ATAC**. The scRNA data address composition and RNA states; these are not paired multiome measurements. The presentation already makes this distinction. A within-state chromatin question remains open. |
| STAT6–EGR2–PPARγ/RXRA | Fig. 4d reports lower late Stat6/Egr2 RNA alongside increased Pparg/Rxra RNA; illustrated accessibility and motif/external-binding associations are different measurements. The earlier relay is a literature premise, not a newly observed temporal chain. Low late RNA cannot identify earlier signaling, occupancy or maintenance. |
| ARG1 | Baseline molecular observations and the separate functional genotype comparison support different claims. CD169 targeting includes NAMs and alveolar macrophages. They do not identify NAM-specific mediation through a linked chromatin → enzyme → outcome chain. |
| Transfer endpoint | The transfer panel in Fig. 3 measures weight change under a challenge with minimal mortality. It does not itself establish restored survival under a lethal challenge. The presentation's narrower wording is appropriate. |
| Repair/lipid language | RNA panels, lipid-handling genes and efferocytosis-associated genes do not measure lipid flux, efferocytosis, epithelial repair or secretion. Human chronic-disease associations do not establish the acute-to-chronic causal transition. |

Exact article/repository boundaries are retained in the
[published evidence matrix](../PUBLISHED_EVIDENCE_BOUNDARIES_2026-10-30.md).

The completed results narrow what a useful next analysis should ask:

- The [external RNA/ATAC benchmark](EXTENSION_RESULTS_2026-10-30.md) reports
  55.908% same-direction mapped rows with the author Ensembl assignments,
  versus 62.890% in the source-nearest-TSS ≤2 kb subset. These are different,
  pair-weighted universes, not independent gene trials or evidence against a
  50% null. Offset and mapping sensitivities already exist. They do not establish
  a NAM mechanism or reproduce the source paper's selected-feature correlations.
- The synthetic examples establish that detection-label disagreement depends on
  precision and signal. They are not fitted to NAMs. The repeated-stimulation
  RNA table supplies group-average response descriptions, not replicate variance
  or matched RNA–ATAC trajectories.
- The [primary human result](../HUMAN_RESULTS.md) and
  [external description](../HUMAN_EXTERNAL_RESULTS.md) both retain a positive
  matrix-associated macrophage-panel difference in IPF. FABP4-associated findings
  depend more on annotation/site; pooled macrophage–fibroblast coupling does not
  persist in the same form within IPF. ARG1 is sparse and does not show the proposed
  simple human increase. These unfavorable distinctions remain part of the question.

## Additional work with a clear increment

The ordering below concerns this requested follow-up, not the canonical RQ
portfolio. Each numerical step requires a new versioned contract through the
existing runner, with this note as exposed prior evidence. Preserve every original
output; do not alter frozen scripts, relax eligibility or select a favorable result.

### F1 — representation sensitivity of the qualified external benchmark

**Status:** existing qualified inputs support a new bounded descriptive analysis.
**Purpose/question:** does the aggregate direction agreement depend on genes being
represented by different numbers of mapped regions? This adds to, rather than
repeats, the existing offsets, distance subsets and mapping-rule comparisons.

**Comparison/endpoint:** compare the saved pair-weighted summary with an equal-gene
summary of each gene's fraction of mapped regions agreeing with its RNA direction;
retain within-gene mixed directions and mapping-rule agreement on common support.
Report annotation coverage and regions per gene. Keep zero/ambiguous cases explicit;
freeze their treatment and the source-defined distance subsets before execution.

**Units:** descriptive genes/regions nested in the same source libraries, not new
biological replicates. Original preparation reuse, assay pairing and batch remain
unknown. **Main rival:** unequal representation or annotation coverage produces
some of the aggregate pattern. A large change supports that explanation; stability
bounds this particular explanation but does not establish causal regulation.

**Inputs:** [membership](../../../analysis/research/runs/DY1_P02_reference_benchmark_v1/mapping_membership.tsv.gz),
[RNA effects](../../../analysis/research/runs/DY1_P02_reference_benchmark_v1/rna_descriptive_effects.tsv.gz),
[ATAC effects](../../../analysis/research/runs/DY1_P02_reference_benchmark_v1/atac_descriptive_effects.tsv.gz),
and existing qualification. No new biological data are needed. Do not attach a
binomial significance test treating repeated gene/peak rows as independent.

A separate, explicitly chosen library/normalization sensitivity is technically
possible from the qualified counts if the mapping audit leaves a concrete issue.
The previous offset check is not a normalization audit. Without an absolute scale,
additional normalization cannot identify global accessibility or transcriptional
output. Do not choose normalization by how well it restores the expected axis.

### F2 — fragility of the human panel-level interpretation

**Status:** primary-cohort inputs support a new robustness analysis; external
component-level confirmation needs reaggregation from the qualified source counts.
**Question:** is the reported panel difference or panel anticorrelation broadly
supported by its components, or dependent on one component or donor?

Individual gene contrasts, annotation/cell-floor sensitivities, disease contrasts,
and composition/depth sensitivities were **already completed**. The new endpoint is
leave-one-component-out panel contrasts/coupling and leave-one-donor-out influence,
with all omissions reported and the original full-data result retained. No donor
is discarded from the primary analysis and no reduced panel becomes a replacement
because its result is favorable. The donor remains the biological sampling unit.

**Hypothesis/rival:** a distributed panel association versus concentration in a
single component or influential donor. Stability supports a more reliable RNA
summary; fragility limits the panel interpretation. Neither outcome measures
matrix production, macrophage-to-fibroblast signaling or repair.

The primary [donor table](../../../analysis/research/runs/DY1_human_observational_v1/donor_expression.tsv.gz)
contains component columns. The [external donor table](../../../analysis/research/runs/DY1_external_human_observational_v1/donor_expression.tsv)
exports panel scores and ARG1, not individual panel components. External
component analysis therefore needs a new governed reaggregation, retaining the
existing source/site rules, missing-symbol record and fixed donor eligibility.
The original panel-selection atlas is reused evidence, not independent validation.

### F3 — qualify a paired-modality time-course reference

**Status:** promising source lead; numerical work is held on access and metadata.
[Lobato-Moreno et al., Nature Methods 2025](https://doi.org/10.1038/s41592-025-02700-8)
uses same-nucleus RNA/accessibility in iPSC-derived macrophages. Fig. 2 describes
baseline and 1/6/10/24-hour measurements, including an IL-4 arm; its motif result
is not direct TF occupancy. This is a closer measurement comparison than separate
bulk assays. The published biological analysis is prior evidence, not a new discovery.

The exact macrophage accession is
[EGAD50000001206](https://ega-archive.org/datasets/EGAD50000001206), not the species-mix
GEO accession. Its public record describes demultiplexed FASTQs and controlled
access. The paper names duplicates, but independent donor/differentiation identity,
paired barcode files and suitable processed matrices have not been qualified.
The public analysis GitLab page and API timed out. No access request was submitted.

**Proposed comparison:** within comparable, adequately supported macrophage states,
compare time-labelled RNA/accessibility associations with their aggregate mixture.
**Units:** qualified independent preparations, with nuclei nested within them;
same-nucleus pairing is not longitudinal tracking. **Endpoint:** residual
cross-modal association and its observed timing. **Rival:** mixture, sampling or
measurement effects explain apparent discordance. It remains an external context
extension; this time course does not establish post-withdrawal memory or lung-NAM
causality. Qualify data rights, files, pairing, preparation identities, annotation,
QC and common-state support before choosing an estimand or treating duplicates as n.

### F4 — cofactor dependence in the already acquired external reference

**Status:** qualified source matrices contain the required groups; a new contrast
contract and group-specific provenance check are needed. E2 analyzed wild type
only. The [sample map](../../../analysis/research/runs/DY1_P02_reference_source_v1/sample_map.tsv)
also identifies NCOA2/GRIP1 cKO IL4 and control libraries in both assays.
This GRIP1 is the nuclear-receptor cofactor NCOA2, not the unrelated glutamate
receptor-interacting protein with a similar name.

**Question/comparison:** describe cKO versus WT within the source-labelled IL4
condition, separately for RNA and accessibility, with the control comparison
reported to distinguish baseline differences. A stimulus-by-genotype interaction
would be a separate estimand requiring its own justified model; it is not needed
to state the conditional genotype comparison. Freeze the full eligible feature
universe and mapping rules before analysis rather than selecting loci by outcome.

**Endpoint/unit:** direction and magnitude of source-labelled transformed-mean
contrasts and their cross-modal association, with source libraries nested within
qualified biological preparations. **Published premise:**
[Deochand et al. 2024](https://doi.org/10.1038/s41467-024-52942-x), Fig. 5 and
Supplementary Fig. 5, already examine cofactor-dependent transcription/chromatin.
The increment is reproduction and measurement sensitivity using the current
count/mapping framework, not discovery of cofactor dependence.

**Hypothesis/rival:** cofactor-dependent transcription can differ from accessibility;
shared changes, baseline genotype differences and measurement uncertainty are
alternatives. No change must be reported as an estimated contrast with uncertainty,
not inferred from nonsignificance. This remains an external non-infectious reference,
not evidence for a direct NAM PPARγ–ARG1 chain or post-withdrawal memory.

The deposited map has three WT and three cKO IL4 RNA libraries, whereas Fig. 5c's
caption broadly states cKO n=4; cKO control has four. ATAC has four per relevant
group. Reconcile the caption/deposit distinction before claiming exact author
reproduction; do not invent a fourth IL4 RNA sample. Existing pairing, batch,
annotation and vehicle-time ambiguities remain. The earlier E2 conditional
uncertainty recipe cannot be copied unchanged across unequal group sizes. A
bounded descriptive analysis is feasible; unqualified population or causal-effect
claims are not. No additional source download is needed for the deposited counts.

## Focused question and relation to the established framing

A defensible continuation of DY1-P02 is:

> Does RNA–accessibility discordance persist within comparable macrophage states
> after accounting for feature assignment, representation and sampling, and how
> does it vary across directly observed stimulation times?

F1 addresses representation with current evidence; F4 provides a cofactor reference
comparison; F3 would address same-nucleus and state/time support if its prerequisites resolve. STAT6/EGR2 and PPARγ/RXRA
remain literature-grounded contexts for later interpretation, not a compulsory
positive chain. ARG1 remains a distinct measured transcript and an unresolved
functional mediator. Any targeted analysis must declare coverage and background
before interpreting these loci. F2 addresses whether the human disease bridge is
a stable RNA association. This connects to A1/A8's regulatory-state/output
separation and A14's persistence/input distinction without revising those RQs.
A2/A22 recipient-output requirements and A19 functional requirements remain unmet.

## Original-source work and exact remaining holds

| Held claim or operation | Missing evidence; useful next action |
|---|---|
| Original NAM gene-level effects | Qualified exon-count semantics, counting/annotation provenance and independent library-to-animal/pool/overlap map; author outputs could permit a narrower published-values audit if acquired |
| Original differential ATAC | Common-region read counts, processing version and the author's excluded-sample identity/rationale; narrowPeak calls alone are insufficient |
| Original within-state RNA–ATAC | Qualified cell assignments, biological units, common state support and state-resolved ATAC; CMO signal cannot invent the animal/pool map |
| Temporal initiation versus maintenance | Phase-resolved molecular evidence and verified cessation/continuing-input information; late RNA and group averages do not identify either mechanism |
| ARG1 mediation | Linked molecular, enzyme/output and outcome evidence with adequate compartment specificity and a defensible causal design; extra regression across separate cohorts cannot supply linkage |
| Human repair/recipient causality | Measured recipient function and a suitable causal comparison; current RNA/annotation associations and sparse external donor support are insufficient |

Author-code recovery remains worthwhile metadata work. The paper cites
[capsule 5968231](https://codeocean.com/capsule/5968231/tree) and
[capsule 7939720](https://codeocean.com/capsule/7939720/tree). Both were inaccessible
through this turn's web reader; their contents were not inspected. This is an
access limitation, not evidence that the requested files do not exist. A CMO
assignment-confidence audit is computationally possible under a new declared
method, but should not be mistaken for recovered biological identity.

## Literature refresh and access record

Search date: **30 October 2026**, live web search. Reused the
[existing literature context](LITERATURE_CONTEXT.md), including the older
STAT6/EGR2/PPARγ precedents and 2024 reference. Searched recent 2024–2026 work
without a hard date filter; focused on closer measurement designs and alternative
measurement explanations. No PI filter or systematic citation-index census.
Followed the new paper's data/code links. No claim of exhaustive coverage or novelty.

SUM-seq: version of record, online 26 May 2025; *Nature Methods* 22, 1213–1225.
Inspected indexed primary Fig. 2/associated Results and data/code statements, plus
the live EGA catalogue. Publisher direct access failed and PMC challenged access;
this is not a complete supplement or raw-file audit. The 2026 protocol article is
not an independent biological replication. Correction/retraction search returned
no explicit notice; this is not a comprehensive integrity certification.

Deochand 2024: reused the qualified source-method assessment and re-opened the
version-of-record PMC text; checked Fig. 5c/e and the deposited sample-map groups.
The caption/deposit difference is explicitly retained in F4. Exact-title queries
recovered the source after overly restrictive path searches returned unrelated
hits; those unrelated hits were not used.

Actual query groups (web search, with domain restriction expressed where shown):

- `"s41586-026-11060-y" "Supplementary" "Source Data"`
- `macrophage chromatin accessibility transcription discordance normalization peak gene mapping 2024 2025 2026`
- `"Single-cell ultra-high-throughput multiplexed chromatin and RNA profiling reveals gene regulatory dynamics" "GSE"`
- `"Single-cell ultra-high-throughput multiplexed" "Nature" 2025`
- `"Integrated time-series analysis and high-content CRISPR screening" "GSE"`
- `"s41592-025-02700-8" "Data availability"`
- `"s41592-025-02700-8" "macrophages" "donors"`
- `"s41592-025-02700-8" "IL-4" "time"`
- `"s41592-025-02700-8" correction retraction`
- `"SUM-seq" "E-MTAB" macrophage`
- `"s41592-025-02700-8" "EGA" "data"` and `"s41592-025-02700-8" "GEO"`
- `"s41592-025-02700-8" "replicates" "same"`
- `"s41592-025-02700-8" "donors" macrophage`
- `"s41592-025-02700-8" "Fig. 2" "STAT6"`
- `site.nature.com/articles/s41467-024-52942-x "GRIP1" "Fig. 5"`
- `site.nature.com/articles/s41467-024-52942-x "IL4" "accessibility" "knockout"`
- `"Mechanisms of epigenomic and functional convergence" "GRIP1"`

Discovery-only leads, not supporting numerical inputs: IGN normalization
(10.1016/j.csbj.2025.01.018) and the integrated time-series/CRISPR study
(10.1016/j.cels.2025.101346). Their full source methods/files were not audited.
No biological claim here depends on those leads. Search stopped after identifying
a closer paired-modality source and its concrete access/identity limitations.

**Next:** F1 is the smallest new measurement audit; F4 adds a cofactor reference
comparison with explicit provenance/model limits; F2 is a modest human-panel
robustness addition; F3 needs source access/qualification before computation.
These are proposed additions, not completed runs or a reason to reopen every
closed E1–E6 job. New results could justify a later question amendment; execution
alone cannot promote a scientific claim.
