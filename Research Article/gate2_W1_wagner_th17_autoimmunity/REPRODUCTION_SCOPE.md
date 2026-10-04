# Wg-R01: staged source reproduction

**Status:** pre-RQ checkpoint. R0/R1 and [paired plus source-aligned model R3](MODEL_RESULTS.md)
have executed, with [eight figure plates](FIGURES.md). R2/R4/R5 source eligibility
is documented with explicit numerical holds in the [current disposition](PRE_RQ_EVIDENCE.md).
Exact historical reproduction remains unresolved; published and local outcomes
are exposed. The specifications below remain the stage contract requirements.
The decision is which source findings can be reconstructed numerically and at
which level, before extending their biological interpretation.

**Strongest rival to apparent success:** similar-looking plots arise from a
different cell set, preprocessing version, reaction grouping or pseudoreplicated
test. **Units:** source biological preparations/animals for inferential contrasts;
cells, genes and peaks remain nested measurements. **Endpoint:** exact source
identity plus declared panel-level numeric concordance. **Limit:** source-data
reanalysis and tutorial reproduction are not independent biological replication.

## R0: source and environment qualification

Qualify the [listed datasets](DATASETS.md), including all biological-unit joins,
assay scales and exclusions. Match 290 intended sorted cells to the author input;
do not treat the entire parent series as a cohort. Recover numerical tables S1-S7,
reaction metadata/metareaction definitions and the original analysis settings.
Record unavailable inputs explicitly. The historical installation guide specifies
the full IBM CPLEX Python API; local access/license and compatibility are untested.
Inspect software licensing, solver support,
runtime and memory requirements before choosing a pinned environment.

Completion means a verified manifest, exact joins and a stage-specific eligibility
report. Missing independence can permit descriptive reproduction but blocks
population inference. Unknown raw-processing settings block exact raw-to-result
claims; they need not block the author-output route.

## R1: author-output reproduction, then manuscript concordance

Start from the pinned author example's `reactions.tsv`, `cell_metadata.csv` and
Recon2 reaction metadata. Verify raw penalties versus transformed scores. The
demo uses `-log(1 + penalty)` followed by a global shift and removes nearly
constant reactions. Do not interpret a larger raw penalty as greater activity.

Reproduce Figures 2C/2E's tutorial analogues, with source cell lists, effect-sign
convention, reaction identifiers/directions and all filters retained. Then run
the manuscript's metareaction route: recover grouping, test the full declared
family, apply BH as specified, and assign group statistics to member reactions.
STAR Methods use q < 0.1 for source comparisons; this is a reproduction setting,
not a new confirmatory threshold. Core metabolism includes confidence 0 or 4
plus an EC annotation; 0 means unevaluated, not biochemically verified.

Report per-panel number of observations/features, effect signs, effect magnitudes,
adjusted values and mismatches against available author tables. Fix numeric
tolerances from published precision and solver/statistical behavior in the
contract before inspecting new residuals. Do not choose a correlation cutoff
after seeing results. Missing source numbers permit qualitative concordance only.
Cells-as-unit source statistics must be labelled as such, without endorsing
them as animal-level inference. Biological-unit sensitivities are separate.

## R2: expression-to-Compass rerun

Only after the exact expression matrix is identified: freeze gene identifiers,
mouse/human mapping, transcript scale, normalization, Recon2 version, reaction
direction/compartment, media/exchange constraints, smoothing and solver settings.
The paper's gene/reaction aggregation is source-specific (OR sum, AND mean
before its transformation); do not substitute a textbook minimum rule.
Neighbor information uses transcriptome-wide structure, creating a potential
route for outcome-associated nonmetabolic genes to influence scores.

Run a bounded computational smoke check under its own frozen contract before
scaling. Compare regenerated penalties with R1's inputs, diagnosing version,
mapping and configuration differences. A modern Compass run may be an informative
sensitivity, but it cannot silently replace the paper version. Runtime, memory,
solver availability and exact historical settings remain unknown today.

## R3: bulk RNA reproduction

Use GSE162300 and GSE162382 as distinct experiments. Recover the source analysis
scale and design from the paper and deposited metadata. Source-defined untreated
Th17/Treg partitions support source reproduction; their shared controls and gene
selection make subsequent program-shift distributions non-independent.

Reconstruct Fig. 6A-C/H and S6E-F using eligible treatment-by-lineage and
treatment-by-genotype contrasts. Preserve pairing where verified; diagnose
rank deficiency and confounding before modeling. Keep gene-wise multiplicity
families explicit. A gene-distribution summary is not biological-unit precision.
Estimate per-unit contrasts or a suitable source-aligned model when units permit.

## R4: ATAC reproduction

Qualify GSE165088's genome build, peak count matrix, interval set and preparation
map. Reconstruct Fig. 6D-F with frozen source peak partitions and annotation
universes. Separate external ChIP annotations from sequence motifs. Avoid
deriving a peak set from a contrast and treating that same contrast as independent
validation. Cross-assay linking requires documented sample correspondence.
Without coordinate/annotation fidelity, restrict to the available count contrasts.

## R5: biochemical and disease source panels

Inventory numerical source data for Figures 3-5/7. Use the assay's real unit and
denominator; keep pool size, fractional isotope labeling, cytokine concentration,
cell fraction and absolute viable output distinct. For disease courses, repeated
time points remain within mouse. A digitized plot, if later used, must be a
separate approximate reconstruction with extraction uncertainty, never raw data.
No wet-lab reproduction or experimental operating conditions are specified here.

## Completion and failure reporting

Classify each panel as exact-input numerical reproduction, processed-output
reproduction, qualitative concordance, discordant, or unavailable. Preserve
failed joins, unfavorable comparisons and unresolved source differences. Every
executed stage needs a committed contract, immutable receipt, independent
arithmetic/unit verification and a result report. A stage can finish with a hold;
the whole paper cannot be called reproduced just because 2C/2E run.
