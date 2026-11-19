# Stepwise plan: Naik 2017 inflammatory memory

17 November 2026. Proposed paper-driven research sequence, based on current main
`d0429d0`, the owner's notes, the supplied PDF and the linked literature review.
This is a plan, not an executed analysis, frozen numerical specification or new
canonical RQ. [Current overview](README.md) · [Paper review](PAPER_REVIEW.md)
· [Precedents and boundaries](LITERATURE_CONTEXT.md).

Scope clarified by the owner on 17 November: the bioinformatics study plan in
another session is separate. This package follows Ravel's existing progression
from paper claims and source qualification through reproduction, result-guided
analysis, biological interpretation and justified question development. Its
methods, execution and order are chosen for that research purpose. No fixed-axis
PCA exercise, learner-run restriction or study-session milestone is required.

## Purpose, estimands and exposure

The biological purpose is to distinguish **resolution of active inflammation**
from **persistence of altered response competence** in mouse epidermal EpSCs.
The first estimands are history-associated differences in baseline RNA,
accessibility and early wound-response RNA, within source-qualified comparisons.
The source-derived expectation is that many acute transcripts attenuate while
some accessible regions persist and associated genes respond after challenge.
Aim2 supplies a known sustained-RNA example, not an unbiased new target.

The biological unit is the independent mouse pool/preparation, if qualified;
otherwise analyses describe deposited libraries. Reads, genes and peaks are
features or nested measurements, not substitute biological replicates. The final
paper reports duplicates of pooled animals, which supports a pool-level design
but does not identify every animal, batch or cross-assay relationship.

The principal threats are differences in epithelial subpopulation/clone
composition, ongoing local cues, wound-edge selection, reference/processing
differences and sparse independent preparations. They may coexist with genuine
intrinsic persistence. Bulk data alone cannot separate all of them.

Published figures, mechanisms, selected loci and the four D6 RNA profiles have
already been inspected. All subsequent work is exposed reproduction/exploration.
A later contract freeze preserves choices; it does not remove that exposure.

## Stage sequence and decisions

The biological argument runs from inflammatory exposure through retained
regulatory context to altered recall and repair. This is the paper's proposed
relationship among processes; the computational stages below do not themselves
prove its causal arrows. There is no Naik Ravel result yet. The first contribution
is source reconstruction, followed by bounded tests of robustness or explanation
that the actual results justify.

| Stage | Concrete output | Decision before continuing |
|---|---|---|
| S0. Explain the paper | Claim-to-panel map and corrected reading notes | Can each claim be assigned to its measured endpoint? Initial map complete in PAPER_REVIEW. |
| S1. Qualify samples and sources | Claim-to-source map, sample/assay/contrast crosswalk and feasibility report | Which molecular or functional claims support reproduction, adaptation or only literature interpretation? Which first comparison is informative? |
| S2. Acute versus recovered RNA | Qualified D6/D30 gene-level contrasts and relevant sample QC | Which acute patterns attenuate, persist or remain uncertain? How does this qualify the recall comparison? |
| S3. Persistent accessibility | Qualified D6/D30 ATAC comparison; D180 durability extension if informative | Which regions retain signal under compatible definitions, and how sensitive is that classification? |
| S4. Recall RNA | D30 unwounded versus 6/12-hour wound-response comparisons by history | Is the post-wound difference larger than the baseline difference, or mainly a baseline offset? |
| S5. Connect the evidence | Region–gene evidence table, discordant cases and scoped biological synthesis | Does accessibility/RNA concordance support the proposed association, and what remains unmeasured? |
| S6. Develop or close a follow-up | Result-derived article-local comparison and RQ-overlap assessment, or a justified stopping note | Is there a useful reproduction, model discrimination or extension beyond the closest studies? No automatic RQ registration. |

S3 and S4 share S1 and can later be scoped independently. S5 requires both;
missing ATAC does not hold an otherwise informative RNA description.
After every substantive stage, record the published premise, actual Ravel
measurement, what it narrowed/weakened/left mixed or unestimated, the remaining
alternative, and why the next comparison could change the interpretation.
This applies throughout the sequence, not only at S6. Source replication can
remain worthwhile after an unfavorable result; do not expand the screen merely
to recover a favorable direction.

This framing follows the [DuPage biological sequence and stage decisions](../gate3_09_dupage_2015/ANALYSIS_PLAN.md),
the [Wang source-reproduction and functional-bridge plan](../gate3_10_wang_2018_ezh2/ANALYSIS_PLAN.md),
and [Arozamena's evidence-limited RQ connections](../ungated_arozamena_2026_inflammatory_memory/RQ_CONNECTIONS.md).
Their current results/amendments, linked in the overview, govern interpretation;
these historical plans supply structure rather than new execution authority.

## S1 — Source and design qualification comes first

Use [GSE92967](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE92967), its GSM,
BioSample/SRA records, final Methods/legends, correction and released source data.
Preserve retrieval date, exact URLs, version, bytes and hashes. Recover only
files needed for the next comparison; a full series tar/FASTQ download is not
the starting task.

Inventory released numerical source data for the wound/perturbation claims as
well as the sequencing deposit (especially Figures 1, 4g–h and 5). Record the
animal/experiment unit and repeated-measure structure, then decide whether a
bounded effect reproduction would clarify the paper's mechanism-to-function
argument. Do not promise a functional reconstruction before those inputs are
qualified. Missing functional source data holds that reconstruction only;
published experimental evidence and eligible molecular comparisons remain useful.

The existing local SOFT snapshot gives this **preliminary inventory**, not a
fresh certified manifest:

| Assay/condition | Control GSMs | Exposed/post-inflamed GSMs |
|---|---|---|
| RNA, D6 | 2440985–86 | 2440987–88 |
| RNA, unwounded D30 | 2440989–90 | 2440991–92 |
| RNA, D30 + 6-hour wound | 2440993–94 | 2440995–96 |
| RNA, D30 + 12-hour wound | 2440997–98 | 2440999–2441000 |
| ATAC, D6 | 2441001–02 | 2441003–04 |
| ATAC, D30 | 2441005–06 | 2441007–08 |
| ATAC, D180 | 2652415–16 | 2652413–14 |

Each numeric identifier has the prefix GSM. The snapshot lists 16 RNA and 12
ATAC libraries, not 28 animals. RNA processed files are gene-ID/count tables;
ATAC processed files are bigWigs. No wound ATAC or D180 RNA-seq appears in this
snapshot. D180 qPCR in the paper is a separate assay.

One crosswalk row must identify library, runs, assay, history, time since primary
exposure, time after wound, sampled compartment/sort, animal pool/preparation,
sex/age, batch and reference. Record unknowns, including whether R1/R2 are
independent pools and whether any assay preparations share animals. Never pair
across groups merely by the suffix. Check matrix semantics, gene IDs and coverage
without discarding samples because they separate poorly or contradict the paper.

The single-end/paired-read discrepancy holds exact raw-read reproduction until
resolved; it need not hold count-table inspection. Confirm bigWig normalization
before comparing signal. Recover source peak definitions/coordinates and
supplementary mappings; a failed web route is not evidence that they do not exist.

**Exit:** qualify each contrast explicitly. If only library identity is secure,
retain a descriptive route. If distinct pools are sufficiently supported, report
the evidence and remaining uncertainty before fitting a count model. Do not
claim single-mouse variance from pooled samples.

## S2 — Reconstruct acute and recovery-stage RNA differences

**Published anchor:** Figure 4c and the corresponding Extended Data Figure 5
RNA evidence. Recover the exact tested universe and source contrasts before
calling a reconstruction exact; otherwise label the comparison as adapted.

Use source-qualified D6 and unwounded D30 counts, with each exposed group
compared against its time-matched control. Report per-library QC, normalization,
gene-ID mapping and gene-level effects for the acute and recovered comparisons.
Their relationship asks which changes attenuate, persist or remain uncertain.
An exposure-by-time contrast can quantify the difference between these effects
if the sampling and batch design supports it; cross-sectional pools are not
paired longitudinal animals.

Choose PCA or another sample diagnostic only when it helps assess the qualified
design. Its feature selection and transformation belong to this analysis's
contract, and its output is not a differential-expression test. A full-transcriptome
comparison is not restricted to a previously inspected 500-gene subset or a
model saved elsewhere. Baseline RNA alone cannot exclude chromatin memory.

When independent pools/design are supportable, specify a count model and
uncertainty appropriate to the sparse design; include batch only if estimable.
Otherwise report normalized per-library values and descriptive effects. Keep
unresolved genes uncertain; failure to reject a D30 difference is not a
“resolved” classification. Define any effect-based class boundaries before the
new calculation and justify them rather than inventing a biological margin.

**Informative outcomes:** broad attenuation motivates latent-priming analysis;
persistent RNA motivates separating sustained activation from latent competence;
strong replicate/batch dependence restricts that interpretation. All are retained.

## S3 — ATAC persistence at a defensible resolution

**Published anchor:** Figure 3a–e and Extended Data Figure 4. Distinguish the
paper's retained-region classification from any separately specified sensitivity.

First recover the author's coordinate universe and signal/count semantics.
For an exact reproduction use its stated windows/peak rules. For an adaptation,
fix a common mm10 region universe and annotation version before comparisons,
report discovery-set exposure, and retain resolved as well as persistent regions.
Independently calling peaks per condition and intersecting them is sensitive to
depth and threshold; it is not a complete differential-accessibility analysis.

Use D6 inflammation-minus-control and D30 post-inflammation-minus-control
comparisons. Add D180 only to assess durability of a qualified result, not because
all deposited tracks must be used. With qualified raw reads/counts, preserve
replicates and evaluate alignment, usable fragments, library complexity and
accessibility QC before a differential model. A new raw pipeline needs its own
resource/runtime plan and contract.

If only compatible bigWigs are available, describe signal over fixed regions
and published loci with explicit normalization limits. Track summaries cannot
supply fragment-count dispersion or an independent replicated count pipeline.
Do not manufacture population p-values from regions as replicates. If track
scales are unresolved, retain within-track visualization only.

**Informative outcomes:** reproducible retention supports a locus-level
persistence description; weak/threshold-sensitive retention narrows the claim;
source incompatibility holds the dependent comparison. None alone identifies
the same cells or proves a memory-maintenance mechanism.

## S4 — Separate recall response from baseline offset

**Published anchor:** Figure 4c–e. The paper's post-wound comparison is the source
reproduction; baseline adjustment is an explicit comparison of its interpretation.

Qualify 6/12-hour wound RNA and its relationship to unwounded D30 sampling.
For each gene and time t, the intended descriptive contrast is:

`[PI_wound(t) - Ctrl_wound(t)] - [PI_unwounded - Ctrl_unwounded]`

The scale must be fixed in the numerical contract (for example, a log-expression
contrast). If unit/design qualification supports inference, the corresponding
history-by-challenge/time interaction belongs in an appropriate count model,
with separate contrasts for 6 and 12 hours. A single post-wound PI/Ctrl contrast
is insufficient. Cross-sectional pools are not paired longitudinal animals.

Inspect wound-edge versus unwounded compartment and sorting differences before
treating the interaction as a pure cellular response effect. Report baseline,
post-wound and interaction contrasts together. Predefine testing families and
multiplicity if inferential testing is justified; sparse pools do not warrant
elaborate trajectories or a large predictive model.

**Informative outcomes:** a baseline-adjusted response supports history-dependent
recall transcription; an offset alone supports persistent baseline RNA; mixed
gene/time patterns restrict generalization. Two post-wound times offer a sparse
temporal profile, not a precise response rate or proof of faster tissue repair.

## S5 — Link modalities without collapsing their meanings

Reconstruct the Figure 4 overlap only after recovering its region-to-gene rule,
gene/peak universe and direction definitions. If exact mappings are unavailable,
declare an adaptation, retain ambiguous/multiple links and compare a prespecified
alternative mapping. Nearest gene is a candidate assignment, not a verified
enhancer target. Do not choose a background that guarantees enrichment.

Display acute RNA, D30 RNA, D6/D30 accessibility and wound-response contrasts
side by side. Include retained-accessibility/no-detected-recall and
recall/no-retained-accessibility cases. Separate Aim2-like sustained expression
from predominantly latent patterns. Preselect published anchors for reproduction;
additional target selection is exploratory and requires an exposure record.

Across these bulk assays, concordance is a group-level association. A gene-level
enrichment or successful arithmetic replay is not biological replication, TF
occupancy, same-cell multiomics, or causal mediation. The paper's wound and
perturbation experiments are separate published evidence. They do not provide
sample-level molecular-to-functional prediction without actual unit links.

Return to the functional evidence in Figures 1, 4g–h and 5: wound closure,
re-epithelialization, outgrowth/migration, proliferation and pathway perturbation
must keep their own endpoints and denominators. If S1 qualifies animal-level
source data, specify a bounded reconstruction using the actual group structure
and repeated measurements; do not convert group means into invented animal
trajectories. Such a separate experiment can estimate its stated functional
effect without being paired to the sequencing animals. An individual-level
molecular prediction or mediation claim would require additional unit linkage
and design. If raw functional inputs are unavailable, retain the published
functional evidence and identify exactly which numerical reconstruction is held.

## S6 — Use later literature before proposing an extension

Use the actual S2–S5 results to identify what remains unexplained, then evaluate
the closest primary comparisons before developing an article-local candidate.
Larsen 2021 Figures 3–6 already supply direct establishment/maintenance/recall
precedents; inspect the relevant methods and supplementary evidence before
claiming a new mechanism. Use Arozamena, Nagaraja and Hamdan/Hammerhøj where the
specific result raises a tissue, clonal or functional boundary. Literature
qualification runs alongside interpretation; it is not a fixed reading curriculum
or a prerequisite to every eligible Naik analysis.

A possible later question concerns when retained regulatory features accompany
repair benefit versus impaired barrier/differentiation, or how selection and
within-lineage persistence contribute. These are **directions to specify**, not
novelty claims or registered hypotheses. Choose one tissue/model and one
measured outcome only after source and precedent qualification. Published AP-1
mechanisms remain premises. A faithful reproduction can be the completed product
if no defensible additional comparison is available.

## Execution and delivery requirements

Before Ravel numerical work, register an article-local owner with its relation
to A1/Arz1, complete a versioned contract with exact source/code hashes and
exposure, freeze/commit it, pass input preflight and execute through the
[research runner](../../docs/RESEARCH_GOVERNANCE.md). Qualify the inputs and
implementation for this research package, retaining the actual prior outcome
exposure. Execution follows the owner's Ravel authorization and repository
governance; no step depends on activity in the separate study session. Preserve
all original files and frozen outputs.

Each completed stage reports effects/measurement limits, independent arithmetic
or source checks, unfavorable findings and the next decision. Update this
package's current interpretation, stage disposition and PROGRESS together.
No clinical, disease-susceptibility or function claim is inferred from RNA/ATAC
alone. No scientific acceptance, lab readiness, effect margin or sample-size
justification is supplied by this plan.
