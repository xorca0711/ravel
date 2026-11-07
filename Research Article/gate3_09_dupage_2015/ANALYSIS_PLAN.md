# Dp1-P01: stepwise analysis and biological aims

Version 1, 7 November 2026. **Original prospective planning record, retained.**
Current execution is in [RESULTS](RESULTS.md), [ledger](STAGE_STATUS.md) and
[AM01](ANALYSIS_AMENDMENT_V2.md). Planning-only statements below are historical.
The owner's subsequent DuPage-first target-screen follow-up is specified in
[TARGET_SCREEN_PLAN_V1](TARGET_SCREEN_PLAN_V1.md); it preserves this original
plan and the completed stage results, and does not require a tumor/NK direction.
[Current target-screen interpretation](TARGET_SCREEN_RESULT.md) and
[portfolio figures](TARGET_SCREEN_FIGURES.md) distinguish the new exploratory
candidate proposals from the original planning record below.
This is the article-local scientific dossier. [Source review](SOURCE_REVIEW.md)
and [literature context](LITERATURE_CONTEXT.md) are prerequisites to interpreting
it. The plan follows the repository's updated
[question-development sequence](../../docs/AGENT_DECISION_WORKFLOW.md#screening-as-question-development).

## Purpose, hypothesis and strongest alternative

**Organizing question:** how does Ezh2 support activated Treg identity, and which
regulatory changes can explain subsequent tissue Treg loss?

**Working hypothesis:** conditional Ezh2 loss is associated with a larger
transcriptional disturbance in CD62L-low than CD62L-high Foxp3-positive Tregs,
including failure to repress part of the normal activation-associated programme.
Some changes may align with independently defined Foxp3-associated repression
and H3K27me3-marked loci. Their mediation of identity loss or disease is untested
by the RNA deposit.

**Leading alternative:** sorting captures different mixtures of activated,
cycling, stressed or surviving cells after Ezh2 deletion. The bulk difference
may combine within-cell regulation with population selection. Both can occur.
Healthy mosaic females limit secondary systemic inflammation but do not remove
this selection problem, heterozygous-control limitations or unknown sample nesting.

**Comparison tuple:** mouse Foxp3-positive CD4+CD25+YFP+RFP+ Tregs; spleen/LN;
conditional Ezh2 KO versus HET; CD62L-high versus low at source harvest (not a
time course); measured RNA abundance; source biological preparation, with
mouse/pool identity and cross-state pairing still to recover. Published lineage
and EAE assays use animals as units and must not be pooled with RNA libraries.

**Contribution:** first, exposed source reconstruction; second, if qualified,
a direct genotype-by-state estimate and bounded explanation of its gene pattern.
This is neither independent replication nor a new discovery of the published
CD28-Ezh2 relationship. The 2024 reciprocal perturbation precedent must be
considered before proposing a new extension.

## Biological sequence and execution order

Biological model: co-stimulation → Ezh2-dependent regulation during activation
→ maintenance of a Foxp3-associated programme → identity/survival in tissues
→ inflammatory control. The order is a hypothesis about linked processes, not
a pseudotime trajectory to infer from four bulk groups.

Computational order: **S0 source qualification → S1 source reconstruction →
S2 state-dependence → S3 regulatory interpretation → conditional S4 external
discrimination → S5 functional bridge → S6 next-question decision.** S5 can
remain a source-grounded evidence map when functional inputs are unavailable.
S6's "what changed / why next" update is required after every substantive step.

## Dp1-S0 — Qualify the observation before fitting a model

**Aim:** determine exactly which biological comparison and level of uncertainty
the available files can support.

Build the twelve-library manifest with genotype, state, exclusion, GSM/SRX/run
links, source strain/sex/tissue, preparation/mouse/pool, age, batch and pairing.
Retain explicit unknowns. Recover the separate supplement and sample-level
provenance where possible; keep the published low-depth exclusion.

Inspect all expression headers, reference/feature definitions, sample-specific
Cufflinks assembly IDs, annotation versions, missingness and estimation-status
fields. A shared gene symbol or similar tracking number is not proof that two
rows represent the same quantified feature. Do not silently sum transcript FPKM
or fabricate integer counts from FPKM/coverage. Verify whether the twelve
per-sample tables support a common gene-level comparison.

**Endpoint/unit:** source eligibility and feature/sample join accuracy; no
biological effect estimate. **Threat:** misidentified comparator, pseudoreplicates
or incompatible feature definitions.

**Output:** manifest, source hashes, exclusion ledger and an explicit route:

- Common per-sample features qualified: S1 can describe the retained libraries.
- Only four merged estimates qualified: restrict S1 to group-level source
  reconstruction, with no biological-sample uncertainty or replicate PCA.
- Counts and independent biological units qualified: specify S2's count model.
- Counts unavailable: keep the FPKM route descriptive; identify exact SRA/count
  recovery work before considering reprocessing. The repository preference is
  to start from deposited matrices, not automatically launch FASTQ processing.

**Stop rule:** unresolved identity blocks only the dependent comparison. Do not
turn a failed retrieval into a source-wide absence claim. No raw-read processing
or inference is authorized by completing this planning document.

## Dp1-S1 — Reconstruct the activation-associated expression pattern

**Aim:** establish whether the source measurements support the paper's central
RNA observation and identify any discrepancy before giving it a new explanation.

Using S0-qualified expression, display all retained samples, mapping coverage,
expression distributions and sample relationships. If possible, show replicate
PCA alongside the source's four-mean PCA; label the two displays distinctly.
Respect the 2/3/3/3 retained design. The low-depth sample may appear in a clearly
separate QC sensitivity, not be silently restored to the primary comparison.

Reconstruct the Figure 6A-B contrasts: CD62L-low versus high within HET and within
KO, plus KO versus HET within each state. Recover the original DEG lists,
filtering, FDR universe, annotation and aggregation before claiming an exact
Figure 6 replay. Until then call it an adapted descriptive reconstruction.
The published 3,097/831/341 counts are audit targets, not quotas to force.

**Endpoint/unit:** directional RNA contrasts and their distribution across
qualified features/preparations; four group estimates alone have no replicate
degrees of freedom. Specify transformations and zero handling before computation,
and retain raw scale/missingness alongside any log display.

**Outcomes → decision:**

- Source-like stronger divergence in CD62L-low supports asking S2 directly.
- Uniform divergence across states weakens activation specificity; S2 tests that
  revised possibility without changing the original record.
- Discordance driven by features or a sample returns to S0/QC; do not move to
  enrichment as a way to recover a positive story.
- Broad uncertainty is an informative source limit, not equivalence.

## Dp1-S2 — Estimate whether the Ezh2 difference depends on state

**Aim:** test activation-associated specificity directly, rather than comparing
how many genes reach significance in two separate contrasts.

For each eligible gene define, on the model's log2 expression scale:

```text
delta_low  = KO_low  - HET_low
delta_high = KO_high - HET_high
interaction = delta_low - delta_high
            = (KO_low - KO_high) - (HET_low - HET_high)
```

Use a genotype + state + genotype:state design if qualified counts/estimates
and biological units permit it. Add only documented, estimable batch/block
terms. If high/low samples share preparations, model that dependence; if they do
not, do not invent paired IDs. Completely confounded batch cannot be repaired by
software. Record design rank and the actual residual degrees of freedom.

Count-based inference requires counts or supported quantified estimates with
their appropriate import/offset semantics; **FPKM is not a substitute**. A
modern re-quantification, if subsequently chosen, needs its own versioned code,
reference, resource estimate and frozen contract. It is not exact Cufflinks replay.

**Endpoint:** genotype-by-state log2 contrast, with state-specific estimates,
uncertainty and the full tested-gene universe. For an inferential route, declare
the interaction family as primary and control its multiplicity; source FDR 0.05
may be used for comparability, but is not a biological effect margin. Sparse
samples limit precision. Do not invent power or a meaningful-equivalence margin.
If only FPKM is qualified, display the same contrast descriptively without
negative-binomial p-values or animal-population confidence claims.

**Threat/limit:** CD62L state is observed after genotype perturbation. This is
effect modification by a selected state, not a randomized activation effect or
a within-cell temporal trajectory. Retained Foxp3-positive cells exclude already
destabilized cells.

**Outcomes → decision:** positive interaction for normally repressed genes
supports S3's repression question; comparable effects in both states narrow the
claim to broader Ezh2 dependence; mixed directions require separated gene
classes; imprecision preserves an unresolved hypothesis. A significant low-state
effect and nonsignificant high-state effect alone do not establish interaction.

## Dp1-S3 — Ask which regulation is disrupted

**Aim:** distinguish a specific repression-associated pattern from generic
activation, stress or compositional shifts, while retaining indirect regulation.

First recover exact versions of the reference memberships used in Figure 6:
Arvey activation-associated H3K27me3, Gavin Foxp3-loss RNA, Samstein Foxp3
binding and the source Treg-signature definition. Audit species, build, locus-to-
gene assignments, expression backgrounds, assay state and study/sample reuse.
The original combined evidence is one published analysis lineage.

Then compare signed RNA contrasts, not only thresholded overlap counts:

1. Genes normally reduced with activation versus those normally increased.
2. Foxp3-loss concordant versus discordant changes, retaining both directions.
3. Externally Foxp3-bound / H3K27me3-associated genes versus the measured eligible
   background, accounting for annotation coverage and expression detectability.

If an activation set is selected from the same HET samples used in S2, label its
enrichment as descriptive and mathematically coupled to that contrast. Prefer
an independently specified set for inferential testing. Freeze gene-set families,
backgrounds, mapping and multiplicity before examining their results. Do not
present genes as independent animal replicates or use invalid sample permutations
in the sparse design.

Inspect externally specified cycle, survival and activation memberships only to
address the stated alternative. Do not remove post-perturbation cell-cycle or
activation expression from the primary model and then claim an intrinsic effect.
Any such sensitivity changes the question and cannot establish mediation.

**Endpoint/unit:** directional gene-level RNA association and reference-locus
overlap, with sample-level support where available. **Limit:** no direct binding,
matched KO chromatin change, fate or suppressive function is measured here.

**Outcomes → decision:**

- Coherent derepression with external chromatin support prioritizes a limited
  locus-linked hypothesis, not all EZH2 targets.
- Concordant RNA without chromatin support retains an indirect explanation.
- Predominantly generic activation/cycle differences or poor coverage weaken a
  selective repression claim.
- Separate up/down classes or mixed evidence remain separate; do not force a
  single score or a winning gene. If no interpretable narrowing occurs, stop.

## Dp1-S4 — Use later studies only for an unresolved discriminator

**Aim:** determine whether a remaining pattern reflects context-specific locus
regulation rather than a universal "more methylation, more stable Treg" rule.

The 2024 gain-of-function study already examines reciprocal EZH2 RNA behaviour
(Figure S7H), chromatin redistribution and early effector differentiation.
A repeat of that broad comparison is reproduction, not novelty. If S3 leaves a
specific discordant gene class, qualify GSE262130 RNA and GSE262129 CUT&RUN and
ask whether that class tracks local chromatin redistribution in the later model.
Keep each study's controls, activation conditions and estimates separate; never
pool FPKM/normalized expression across studies as one experiment.

The 2026 KDM6B result is a contrasting perturbation: removing an H3K27 demethylase
also disrupts activated Treg regulation. Use its relevant loci/assays only if they
can distinguish the S3 explanation. Its lung-injury context motivates a boundary
question, not a presumption that EZH2 and KDM6B act as a measured antagonistic
pair at every locus.

**Endpoint/unit:** study-specific signed RNA/chromatin effects, with each study's
qualified biological units. Independent source data are a distinct perturbation
context; reuse of DuPage data in later comparisons is not fresh replication.

**Outcomes → decision:** reciprocal effects support dosage-sensitive regulation
for the eligible subset; state- or locus-specific discordance argues for context
dependence; inadequate assay matching leaves the question unestimated. Skip this
step if it only reproduces an already sufficient published comparison or adds no
decision-relevant information. No new external dataset is mandatory.

## Dp1-S5 — Connect regulation to tissue failure with the right endpoints

**Aim:** separate four biologically different outcomes: loss of Foxp3 identity,
loss of viable cells, failure to reach/remain in tissue, and failure to suppress
inflammation.

Start with a panel-by-panel evidence map of Figures 4, 5 and 7 and the recovered
S7 if accessible. Keep denominators explicit: Foxp3+ among CD4+, Foxp3-negative
among lineage-labelled cells, antigen-specific Tregs among antigen-specific CD4+
cells, viable absolute cell number, and longitudinal clinical severity are not
interchangeable. Figure 7A's clinical cohort is distinct from RNA preparations.

If raw functional data become accessible, qualify per-mouse IDs, repeated
measurements, experimental cohorts, allocation and missingness before analysis.
Do not digitize mean EAE curves into fictitious animal trajectories. Figure
digitization, if later justified, is approximate figure recovery only.

For a future mechanistic follow-up, choose the smallest comparison that resolves
the remaining link: matched control/KO Tregs with directly measured locus-level
chromatin and RNA, Foxp3 retention among lineage-labelled viable cells, division
and death, plus a relevant function assay if the claim concerns function.
Timed sampling is justified only if ordering/mediation is the target; direct
trafficking measurement is needed for a migration claim. Rescue or catalytic-
specific controls become relevant if the chosen claim requires them, not simply
because this plan contains an alternative field. No target, effect margin,
sample size, available mouse line or laboratory readiness is invented here.

**Outcomes → decision:** retained numbers with Foxp3 loss emphasizes identity;
increased death without comparable identity loss emphasizes survival; both
support a combined model; lower tissue frequency without tracking leaves homing
unresolved. Functional suppression/remission must be assessed separately.
RNA-only evidence stops at regulation-associated observations.

Any external lung-atlas extension is a separate feasibility branch: Niethamer/D1
still requires separable Tregs, qualified animal/donor units and an endpoint that
actually informs the tissue question. This source study does not pass that gate.

## Dp1-S6 — Decide what the cascade now warrants

**Aim:** convert results into a defensible next biological question rather than
an accumulation of completed analyses.

After each stage record: starting premise → measured result → what was narrowed,
weakened, mixed or unestimated → remaining alternative → next comparison and
why it could change the interpretation. Retain negative results and unresolved
links. Update this dossier, the current README and literature context together.

The eventual result may justify a bounded source reproduction, a specific
regulatory candidate, an explicitly unresolved phenotype bridge, or stopping
without a new canonical RQ. A possible future candidate is whether a qualified
activation-associated repression defect predicts identity loss independently of
selective survival in a defined model. That is a proposal requiring the paired
measurements above, not a result of this planning review.

## Before any numerical execution

Register the versioned step contract under Dp1-P01 with purpose, comparison,
source/code hashes, units, prior outcome exposure, exact exclusions, feature
mapping, transforms/model, multiplicity, expected outputs and stop rule. Freeze
and commit it with its code, preflight inputs, and run through the governed
runner. Use new versions for amendments; retain old contracts and outputs.
Verify receipts, joins, arithmetic and displays before scientific interpretation.

This review changes no governance, validator, claim grade, canonical hypothesis,
frozen asset or human retain/reject decision. A successful computational run
would establish execution only. Source/assay holds restrict the dependent stage,
not reading or an independently useful qualified descriptive comparison.
