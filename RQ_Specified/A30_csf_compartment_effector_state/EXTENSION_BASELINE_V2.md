# A30 extension baseline v2 — 7 October 2026

This replaces the future-development framing of [PLAN.md](PLAN.md), not its
historical design or outputs. The [v3 runs](../../Research%20Article/gate2_W2_wagner_Th17_PGAM/A30_ERRATUM.md)
have executed. All motivating outcomes are exposed. This is an agent-proposed
baseline for review, not a frozen contract or human acceptance.

## Question and rationale

Does the inflammatory RNA difference between paired CSF and blood persist within
comparable CD4 T-cell states after accounting for measured activation/composition?
Selective trafficking can enrich existing populations; local context may also be
associated with state. The first comparison allows both explanations and estimates
an association. Regulatory RNA is separate; non-significance is not preserved
suppressive function. See [primary-source context](LITERATURE_CONTEXT.md).

## Stage 1: qualify the existing measurement

Export original barcodes and the per-library QC cascade: input, UMI/gene/mitochondrial
filters, doublet assessment, T-lineage evidence, putative CD4 gate and paired support.
Hard-zero CD8A/CD8B alone is not positive CD4 identification. Qualify gate/depth
sensitivity under a bounded amended design.

Assess continuous activation balance within donor/state rather than treating a
non-significant random-set p-value within a broad tertile as balance. Distinguish
total association from association conditional on measured activation: adjustment
may remove a mediator, and neither estimand establishes a causal compartment effect.

The current null draws from loaded panel genes and matches size only. For a new
sensitivity, justify the gene background and expression/detection matching; save
sampled IDs or draw statistics and seed. Separate Monte Carlo uncertainty from
donor uncertainty. Freeze the test family and stopping rule before new outcomes.
More draws alone do not validate the null.

Report donor decomposition components and common-state coverage. Distinguish
ratio of medians from median donor fractions. A state absent from one compartment
has no observed within-state counterpart; pooled-mean filling assigns its
contribution to composition by convention. PTC41540 has 82.3% of retained CSF cells
in such states in the saved output. Specify the estimand and sensitivity under
missing support rather than impute certainty.

Unit: ten paired donors, 9/10/9 qualifying per stratum; cells are nested observations.
Report effects and donor-level uncertainty. New exploration requires a registered
amendment, qualified source/code hashes and exposure record. No effect margin or
sample-size claim is invented here. The [audit](../../docs/audits/2026-10-07-pr140/REPORT.md)
verifies saved values and does not execute this new analysis.

## Stage 2: conditional phenotypic extension

If suitable samples/collaboration become available, use paired CSF/blood from
identified donors with timing, treatment and relevant covariates. Establish CD4/subset
identity and independently measured activation. Choose protein/function endpoints
for that population: IL-17 alone is insufficient for the cited human Th17.1 candidate.
FOXP3/CTLA4 describe phenotype; a regulatory-function claim needs a validated
functional assay. Exact panel, timing, feasibility, variance and precision are open.

Paired TCR/RNA can test whether a pattern persists among observed shared clones;
cells/clones do not replace donor replication. Overlap does not prove residence,
migration direction or induction. Qualify cohort overlap before external validation.

## Stage 3: conditional intervention

If the question becomes causal, specify a manipulable context/gene and functional
endpoint. A justified perturbation-versus-control comparison may suffice for its
effect estimand. Rescue, crossover, withdrawal or factorial arms are conditional
on the intended mechanistic inference. No current evidence selects a required
mutant, culture model or sample size. PGAM is not automatically A30's intervention
merely because this question originated in the Wang paper.

## Decisions and stopping

Report persistence, attenuation, mixed contributions or imprecision at the measured
endpoint. Do not force a winner. Hold numerical work with inadequate input identity
or paired support; continue independent reading/design work. Preserve unfavorable
results and all v1–v3 artifacts. Scientific adoption and claim promotion remain
separate human decisions.
