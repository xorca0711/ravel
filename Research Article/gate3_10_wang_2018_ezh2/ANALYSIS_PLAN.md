# Stepwise analysis plan: Wang 2018 EZH2/Treg study

11 November 2026. Proposed from the owner's completed reading, Notion notes,
the stored main paper, current Dp1/Zhang evidence and a bounded primary-literature
scan. This document authorizes no numerical run by itself. No canonical RQ,
frozen contract, analysis result or scientific acceptance is created.

## Purpose, comparison and exposure

The biological purpose is to understand how EZH2 perturbation changes the
contribution of activated Tregs to tumor immunity. The first estimand is the
Ezh2-deficient-minus-control difference in transcript abundance in day-4 cultured
Treg preparations. GEO reports four deficient and five WT biological replicates;
the actual independent biological unit and control construction await S1.

The source-derived prediction is an inflammatory shift with lower suppressive
transcripts. The paper itself reports an incomplete cytokine response. A
consequential alternative is that culture selects different surviving/expanded
Treg states, yielding a bulk difference without uniform reprogramming of every
cell. Background, sex, pooling and processing batch can also confound the contrast.
The RNA comparison can characterize that difference without excluding these
alternatives or inventing an additional experimental arm.

Exposure is already present: published outcomes and selected genes are known;
Dp1's candidate directions and Zhang's results have been read. Future work is
exposed reproduction/exploration, not unexposed confirmation. Reanalysis and the
source article are one evidence lineage. A later freeze preserves choices but
does not erase this exposure.

## S0 — Construct the claim-to-measurement map

**Inputs:** main Results/legends/methods; obtain the supplement, and any released
source data for Figures 1–7/S1–S6. The initial map is in the [README](README.md).

**Work:** distinguish systemic CPI-1205, constitutive Treg deletion, inducible
deletion and the DTR/chimera comparison. For each relevant panel record tumor
model, tissue, timing, denominator, assay, reported mouse/preparation counts and
whether animals are shared across endpoints. Separate exFoxp3 lineage history,
FOXP3-positive frequency, absolute numbers, restimulated cytokine production and
tumor control. Record unavailable information as unknown.

**Output:** a source evidence ledger with exact panel locators and an unresolved
input list. This is reading/source qualification, not numerical reproduction.

**Decision:** Figure 7 already supplies a tested comparison beyond depletion;
there is no need to claim that question is newly unanswered. Figure 6 supports a
functional change without a detected frequency reduction, but does not exclude
selection, altered absolute numbers or later attrition. The first RNA task remains
the day-4 contrast. Failure to obtain functional raw data holds only their
numerical reconstruction, not the RNA route or source interpretation.

## S1 — Qualify the source and the biological unit

**Inputs:** GSE114298 series/sample SOFT or equivalent metadata, processed count
matrix, SRA experiment/run mapping, supplement and library-processing description.
The listed count file is `GSE114298_counts.STARMOUSE.GEO_05_08_2018.txt.gz`.
Record acquisition date, URL/version, bytes and SHA-256 before analysis.

**Checks and output:** produce a one-row-per-preparation sample crosswalk:
matrix column → GSM → sequencing run(s) → genotype → mouse/pool/preparation →
block. Technical runs of the same preparation are not new replicates. Recover
sorting gates, initial cell state, post-culture selection, sex, age, controls,
pooling, litter/culture allocation, stimulation duration and any batch.
Inspect matrix dimensions, identifiers, duplicate mappings, nonnegative/integer
count semantics, missing values and count-library totals. Separate gene symbols
from stable IDs; retain an explicit mapping and unmapped rows.

**Eligibility decision:**

- If independent preparations and the genotype contrast are supported, specify
  the statistical unit and design. Known blocks enter only if estimable and
  scientifically justified; do not invent matching from sample-number suffixes.
- If independence is unresolved, preparation-level descriptions may proceed
  under a descriptive contract. Population-level P values/intervals and the
  nominal four-versus-five biological sample size remain unqualified.
- If genotype is completely confounded with batch, report the non-identifiability;
  batch correction does not repair the design.
- If the deposited matrix is not counts, preserve its actual scale and hold the
  count model. Raw-read reconstruction is a separate scoped option only if it
  resolves a necessary source problem; it is not the default first step.

Recovery of the authors' exact normalization, gene-set release, ranking and
code determines whether an exact replay is possible. If these remain missing,
label the later analysis an adapted source reproduction before it runs.

## S2 — Reproduce the day-4 genotype RNA contrast

**Comparison:** deficient minus control at day 4, within GSE114298. Do not relabel
the control genotype until verified. No within-study untreated/time-zero or
tumor-tissue contrast is assumed.

**Primary implementation:** replay a fully recovered author pipeline when
possible. Separately specify a count-based adaptation using a negative-binomial
model (planned DESeq2), library-size normalization and a frozen low-expression
filter. The formula is genotype-only unless S1 establishes a supported block or
other pre-treatment design variable. Freeze software versions, filtering, ID
aggregation, design, contrast and exclusion rules in the contract. Do not insert
a downstream activation/cell-cycle score as an automatic primary covariate.

Estimate log2 fold changes and uncertainty where the biological-unit design
supports them; adjust across the full tested gene family with BH. Report all
tested genes, low-count/non-estimable rows and any outlier handling. Do not select
a biological effect margin or call equivalence merely to complete the analysis.
The available precision, rather than an arbitrary minimum count of replicates,
limits interpretation.

**Source anchors:** Il10, Tgfb1 and Il2 are explicitly discussed for S3C. Inspect
Tnf and Ifng as the corresponding protein/cytokine context, retaining weak,
sparse and discordant RNA findings. Recover the full S3C panel before calling
this a figure reproduction. Anchor selection is exposed and is not a target screen.

**Planned outputs:** source/QC report; library-level distributions and PCA;
complete contrast table; per-preparation expression panels; MA/volcano display
with effect estimates; an exact-versus-adapted implementation comparison if both
routes exist. PCA separation is descriptive and not an exclusion rule.

**Decision:** agreement supports reproducibility of the stated RNA contrast.
Disagreement first triggers a bounded identity/implementation check. A verified
weak or contrary result is retained; no replacement gene or exclusion is chosen
to recover the published direction. RNA agreement does not reproduce the tumor
or functional experiments.

## S3 — Determine breadth, specificity and sensitivity

**Question:** does the source support a broad, consistent transcriptional shift,
or a smaller set of gene changes with mixed inflammatory components?

1. Recover the exact TNF/inflammatory gene sets used in S3B, including version,
   species mapping and ranking. If unavailable, freeze explicitly named modern
   sets as an adapted analysis; do not label them the original definitions.
2. Use one prespecified primary ranking, normally the signed model statistic
   for the count adaptation. Report coverage, effect direction, enrichment and
   leading-edge members. Adjust across the full tested set family. A planned
   effect-size ranking sensitivity can show whether a threshold-based description
   depends on the ranking; it is not a second biological replication.
3. Display suppressive/identity and inflammatory transcripts separately. Avoid
   an unvalidated scalar "Treg reprogramming" score. Foxp3 RNA, methyltransferase
   RNA, cytokine RNA and cytokine production remain different endpoints.
4. Examine activation/proliferation, survival/stress and lineage-marker patterns
   as descriptive alternatives, with source/versioned sets and all findings
   retained. Bulk RNA cannot identify cell-state mixture versus within-cell
   regulation or estimate absolute Treg abundance from a sorted-cell library.
5. Perform leave-one-independent-preparation/block-out sensitivity only after
   S1 defines the unit. Report effect/direction ranges and influential units;
   do not replace the primary fit or relabel these ranges confidence intervals.

**Planned outputs:** source-set reconstruction, leading-edge/coverage table,
fixed-gene estimate plots, sensitivity display and a result-by-interpretation
table. Classification is qualitative and evidence-led; there is no invented
percentage threshold for "complete reprogramming."

**Informative outcomes:** a broad stable shift supports the cultured RNA premise;
a few stable anchors plus mixed cytokines narrows it to a partial response;
dependence on one preparation, mapping or ranking makes it fragile; low counts or
missing units leave it unestimated. All four outcomes can complete S2–S3. None
requires adding datasets until a positive result appears.

## S4 — Optional comparison across contexts

Run only if the completed RNA result raises a specific context question or if
faithful source extension is the agreed aim. Two branches have different purposes.

**A. Mouse activation/perturbation context.** Reuse current Dp1 outputs before
considering reruns. Compare Wang's cultured loss contrast with DuPage's
CD62L-high/low loss contrasts and Peeters' fresh/cultured gain contrasts. Preserve
control alleles, initial sorting states, culture, sex/background and measurement
scale. Do not concatenate count, FPKM and rlog matrices or meta-analyze their
unmatched transformed differences as a shared effect size. Use separate estimates
and a declared common measurable gene universe, including discordant genes.
Tigit/Prdm1, Ccr2, Igfbp4 and Areg are a secondary, previously selected panel from
Dp1/A33–A35; any new whole-transcriptome nomination is a distinct exposed screen.

Reciprocity between gain and loss is a question, not a required filter. Stable
agreement supports transfer of a direction within its qualified context; opposite
or culture-dependent signs narrow transferability. Cross-study differences cannot
estimate a causal genotype-by-context interaction without a suitable common design.
Check animal/source overlap before describing any independent evidence.

**B. Original human relevance contrast.** If reproducing Figure 2D–E is desired,
qualify the actual De Simone/Plitas samples and donor IDs first. Keep tumor Treg
versus tumor Teff and tumor Treg versus normal-tissue Treg as different contrasts.
Use donor pairing only where documented; analyze studies/cancer types separately.
The endpoint is EZH2 expression and, if separately justified, RNA-state similarity.
These reused sources do not validate an EZH2 perturbation response or predict
clinical benefit. A new tumor scRNA-seq search is warranted only for a specific
donor-level tissue/state question, not to retrofit single-cell analysis to this paper.

## S5 — Return to function and decide the next question

Combine S0 and the actual S2–S4 results in a claim ledger: reproduced RNA,
published protein/function, unknown discriminator and proposed next measurement.
Do not claim a common-cell lineage chain by connecting unrelated assay cohorts.

| Possible unresolved claim | Fit-for-purpose next comparison, if pursued | What is still required |
|---|---|---|
| Deficient Tregs actively enhance a specified effector output beyond reduced suppression | A controlled comparison of the specified effector system with control Tregs, deficient Tregs and an appropriate no-Treg comparator, with viable input/recovery measured | The paper's Figure 7 already supplies an in-vivo precedent. A new assay must state the additional endpoint/context; equal starting numbers alone do not control later survival. |
| A particular cytokine mediates that enhancement | First establish source-specific protein/output; add a mediator-restricted perturbation or receptor blockade only for the claimed causal link | RNA and restimulation capacity do not establish which signal reaches the recipient. Actual assay, timing, interference and meaningful precision remain to be qualified. |
| The response is specific to the tumor environment | A matched genotype-by-tissue comparison at a common time, with separate abundance and within-state endpoints | Day-4 culture versus unrelated tumor experiments is not that interaction. Shared animals/pools and altered recovery must be accounted for. |
| Acute inhibition differs from developmental loss | A comparably controlled timing/perturbation comparison, if this is the chosen question | Wang and later primary work already establish timing as consequential. One endpoint at day 4 cannot determine a transition sequence or persistence after withdrawal. |

These are alternatives selected by the remaining inference, not mandatory extra
arms or an instruction to conduct every experiment. No sample size, effect margin
or laboratory readiness is asserted. A mutant/control comparison is sufficient
for its own effect estimand; the additional comparisons above are needed only for
the stronger indicated claims.

The checkpoint-combination idea is not a default new RQ: Goswami already tested
anti–CTLA-4 combinations, and direct effector/tumor effects of inhibitors remain
relevant. Likewise, Zhang's local depletion/NK circuit cannot be treated as a
direct contradiction of Wang's particular global depletion comparison. Specify
the different tumor models, depletion methods, timings and recipient populations.

## Execution and stopping rules

First deliver S1's source/eligibility record and qualify S2–S3. Before computation,
register the article-local owner and new stage contracts in the existing registry;
freeze source/code hashes, method choices, exposure, endpoints and stop rules;
verify commit identity; then preflight, execute and verify through the repository
runner. Do not replay archived Dp1/Zhang scripts over their outputs.

No numerical contract is fabricated during this planning task. Missing RNA
metadata holds dependent statistical inference; missing FCS/tumor source data
holds their numerical reconstruction only. A source-qualified mixed or null
result is a valid stopping point. A new hypothesis or functional experiment is
proposed only after explaining what it would resolve beyond the closest published
comparison. Current acceptance and every existing RQ remain unchanged.
