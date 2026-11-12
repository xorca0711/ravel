# F3 day-four recovery and state-resolved RNA measurement plan

12 November 2026. Article-local owner **Wang18-P01**. This is a specification
for a future comparison. Its agent specification review passed at `5f8caee`;
input qualification remains required before execution.
The completed public-data work is the [Wang reconstruction](RESULTS_V1.md)
and [F2 ranking sensitivity](F2_RESULTS_V1.md). The
[literature addendum](F3_LITERATURE_ADDENDUM_20261112.md) traces the closest
precedents and the assessed-source boundary.

## Question and comparison

Do Ezh2-deficient Tregs show different net viable recovery or FOXP3-state
representation after four days of activation, and does the lower bulk Il10
direction also appear among recovered FOXP3-positive descendants? Recovery,
composition and within-observed-state RNA differences can coexist. The
strongest biological alternative is preferential expansion or recovery of
states, including subpopulations that remain inside the same observed FOXP3
gate. Genotype-linked background, developmental selection before sorting,
and processing confounding could also explain the comparison.

| Comparison field | Prospective specification |
|---|---|
| Starting population | Viable, initially FOXP3-positive, CD62L-high mouse Tregs from the same predeclared tissue source and sort gate in both groups. Record tissue, age, sex, litter or background and initial sort composition. |
| Perturbation and comparator | Two groups. Treg Ezh2 loss versus a genetically matched control with verified functional wild-type Ezh2 and the same driver and ancestry reporter background. Qualify the proposed allele, driver timing, and means of verifying Ezh2 status before selecting a model. A different control allele requires a prospective change of comparator. |
| Setting and time | A common in-vitro TCR/CD28 and IL-2 activation context aligned with Wang's question. Record viable input at day zero and endpoints at 96 hours. An additional time point or tissue is unnecessary for this comparison. |
| Biological unit | One independent mouse-derived preparation per mouse by default. If yield requires pooling, use the same prospectively justified pool-based design in both groups, with disjoint membership and documented pool sizes. The pool is then the biological unit. |
| Measured endpoints | Net recovery of viable Treg descendants per viable Treg input, recovery and proportions by observed current FOXP3 state, and relative RNA from linked recovered populations. |
| Interpretation | The contrast pertains to the starting population, chosen perturbation history, and day-four culture. The state-specific RNA comparison is conditional on the cells that reached the measured state. |

Published S3B–C and Figures 5–7, the S1–S5 results, F1–F2 and the exposed
DuPage and Peeters directions are already known. Il10 is a prespecified
source anchor, selected because the deposited bulk difference was lower
in the deficient group and the assay target was appreciably detected in
the original bulk libraries. This choice is exposed. The prediction is
lower relative Il10 in the recovered FOXP3-positive compartment if the
bulk direction persists within that observed state. The recovery and
composition estimates remain two-sided. DuPage's earlier division and
later apoptosis findings make changes in net recovery plausible, but
they do not fix the day-four direction or size in this culture.

## Linked measurements

Measure the viable input and the absolute number of all viable recovered
descendants. Descendant identity must remain observable if FOXP3 is lost.
Qualify a stable ancestry label and a separate current FOXP3 readout,
including its correspondence to FOXP3 protein, assignment reliability,
and compatibility with recovery and RNA measurement. The primary RNA
population is viable ancestry-positive, current-FOXP3-positive cells.
Record viable ancestry-positive FOXP3-low/negative and unassigned cells
in the recovered total. Freeze the positive and low/negative assignment
rule and the unassigned category before comparing genotypes. A panel that
only collects current-FOXP3-positive survivors cannot estimate total
lineage recovery or the frequency of marker-losing descendants.

The planned RNA route is low-input bulk counts from an aliquot of the
complete viable ancestry-positive recovered population and from a matched
FOXP3-positive aliquot. Both come from the same identified preparation
and the same day-four sampling frame. The whole-descendant aliquot keeps
the bulk direction interpretable in the new setting. A FOXP3-low/negative
RNA aliquot is a secondary endpoint only if both groups have adequate
recovered cells and validated assay support. Group-specific absent states
still contribute to the recovery result. Record each sampled fraction and
RNA cell input. If fractions are estimated from a separate counting
aliquot, validate that it represents the parent well and record the
scaling and uncertainty.

Net recovery integrates division, cell loss and physical harvest efficiency.
Equal starting inputs alone give no information about later survival.
Distinct division-history and death measurements with timing are required
to estimate those processes separately. Day-four RNA and the published
Hallmark signs remain motivation for this comparison.

## Required analysis tables and stable joins

These tables specify minimum data content. The collection team must confirm
methods, calibration and assay feasibility before using this specification.
IDs are immutable and de-identified. Parent keys refer to the same actual
unit and processing history.

| Table and key | Required fields and units | Join and validation |
|---|---|---|
| `units`, `unit_id` | Genotype and verification record, allele/driver/reporter, timing, source tissue, mouse or pool, age, sex, background and litter/matching block. | One row per biological unit. Preserve source verification and provenance. |
| `unit_members`, `unit_id + mouse_id` | De-identified contributing mouse, genotype, age, sex, litter and contribution or pooling rule. | A mouse appears in one biological unit only. For pools, confirm disjoint membership, within-pool genotype and documented pool size. Shared litter is tracked as a design dependency. |
| `cultures`, `well_id` | `unit_id`, `prep_id`, plate/position, sort and culture batch, planned/actual timing, initial gate and purity, viable lineage-positive input as cells placed, harvest status and deviations. | Wells and repeat preparations remain nested. Never infer joins from row order or genotype labels. Require positive input for an eligible well. |
| `recovery`, `well_id + timepoint + gate_id` | Viable lineage-positive total and state counts, with raw event/volume or calibration records, measured fraction, gating version and corrections. Keep FOXP3-positive, low/negative and unassigned gates mutually exclusive. | Link to original well and clock time. Reconcile state totals to the recovered total within a prespecified calibration tolerance. Record true zeros, incomplete harvests and unavailable measurements separately. |
| `aliquots`, `aliquot_id` | Source well or explicitly combined wells from one `unit_id`, parent fraction, timepoint, ancestry and state, cell input, handling, extraction and processing blocks. | A bridge lists each contributing well for combined aliquots. The recovered total is captured before splitting or corrected using traceable fractions. Keep RNA and counting sample frames linkable. |
| `rna_libraries` and `rna_counts`, `library_id` and `library_id + gene_id` | `aliquot_id`, library/batch and run identifiers, count assay/reference version, library and gene QC, raw nonnegative integer counts with stable gene IDs. | Verify unique keys, exact column-to-library joins, matching aliquot state and genotype, compatible features, and no technical duplication. Distinguish unmeasured genes from measured zeros. Retain prespecified detection and QC flags. |

Record all planned and completed wells, including failures. The primary
recovery summary pools compatible, designated wells within a unit by
summing their absolute input and recovery counts before taking a ratio.
Eligibility and partial-well handling are fixed before outcome access.
An incomplete harvest or a missing paired input and recovery record cannot
be imputed as zero. Split sequencing runs of the same library may be summed
once feature and sample identity are confirmed. Plan one analyzed library
per unit and RNA population, with any planned aggregation of compatible
within-unit aliquots frozen in advance. Multiple technical wells, cells,
aliquots and runs never increase the biological sample count.

## Estimands and analysis sequence

1. **Qualify design and endpoint support.** Validate input files, units and
   disjoint pooling, genotype evidence, timepoints, lineage and FOXP3
   gates, counts and denominators. Allocate both genotypes across the
   planned processing blocks, with matched litter/background as feasible.
   Assess contrast estimability and state support per biological unit,
   blind to expression outcomes where possible. Missing unit identity or
   complete genotype–processing confounding holds the affected inferential
   contrast. Adding covariates cannot repair a perfectly confounded
   comparison. A constitutive model may have selected a different starting
   Treg population even with the same observed sort gate.
2. **Primary recovery contrast.** For unit `i`, let `N0_i` be the verified
   sum of viable input cells and `N4_i` the verified sum of all viable
   lineage-positive descendants. Compare the genotype group means of
   `R_i = N4_i / N0_i` in cells recovered per cell placed. With planned
   mixed-genotype blocks, estimate mutant-minus-control differences within
   blocks and combine with weights proportional to the number of independent
   units planned in each block. Fix these weights before outcome access. If a
   planned block loses its genotype overlap, report the supported block results
   and flag the planned weighted contrast as incomplete. Keep the unit-level
   absolute counts and input denominator visible. Report each state's
   absolute recovery `N4_i,state`, recovery per input `N4_i,state / N0_i`,
   and fraction `N4_i,state / N4_i` as linked secondary composition endpoints,
   including unassigned cells in the total denominator. If `N4_i = 0` is
   verified, recovery is zero and state fractions and RNA are unestimable.
3. **Primary observed-state RNA contrast.** Within recovered viable
   ancestry-positive, current-FOXP3-positive cells, estimate the
   deficient-minus-control log₂ relative Il10 abundance. Use the
   biological-unit-by-state counts, a prespecified count-based model with
   library normalization and estimable design blocks. A negative-binomial
   mean with a log size-factor offset and genotype and supported block
   terms is the planned route, contingent on actual assay and precision.
   Fix reference/filtering rules and the uncertainty method before freeze.
   Require measured state support and gene detection in enough independent
   units in both groups for the planned model. Retain measured zero counts in
   qualified libraries and report which units lack the state or assay by
   genotype. The observed-state RNA estimate applies to contributing units
   with assay support. If a genotype loses that
   state or its RNA is unmeasurable, preserve the abundance result and
   record the within-state contrast as unestimable. Do not replace it with
   a different state, gene or zero-filled library.
4. **Link both estimates to the whole recovered population.** Estimate
   the corresponding relative Il10 contrast in the matched total-lineage
   aliquot as the prespecified context check. Keep Tgfb1 and sparse Il2
   as secondary, exposed RNA anchors on the same populations, retaining
   detection limits and discordance. Report state-specific and whole
   contrasts separately, including differences in supported units.
   State fractions alone cannot reconstruct normalized bulk RNA because
   total RNA per cell and assay capture can differ across states and
   groups. A quantitative accounting would need matched absolute transcript
   output or calibrated RNA contribution and capture per state, full
   coverage of the recovered population, and a prespecified mass-balance
   check against the linked total. This plan uses the linked contrasts
   descriptively and makes no quantitative decomposition.
5. **Report joint results without a single composite.** Show each
   biological unit, block-level contrasts where support permits, missing
   and unsupported endpoints, estimates and design-appropriate
   uncertainty. Specify simultaneous reporting and any multiplicity
   treatment before freeze. For recovery or RNA, a near-zero estimate
   with poor precision leaves meaningful changes unresolved. Interpret an
   adequately precise near-zero result only against justified precision
   targets set before outcome access.

## Informative outcomes and stop rules

| Joint observation | What it would establish or leave open |
|---|---|
| Linked whole-lineage Il10 is lower and the retained-state Il10 contrast is lower | The RNA direction extends to that recovered observed state. Residual state mixture and selection before or within that gate can still contribute. |
| Whole-lineage Il10 is lower, measured state yields/fractions differ, and the retained-state contrast is precisely near zero | Consistent with a contribution from recovery or state representation. Contributions from other states and RNA/capture weights remain unresolved. |
| Recovery/composition and retained-state RNA both differ | Both measured components accompany the bulk shift. Their relative contributions and causal ordering remain unresolved. |
| Whole-lineage Il10 does not recover the expected direction in a well-supported comparison | The Wang anchor did not transfer to this qualified culture/model. Preserve any state and recovery differences. Do not present them as an explanation for the original bulk contrast. |
| Recovery, state representation and both Il10 contrasts are near zero with prespecified meaningful precision | The planned measurements show no meaningful day-four difference within the precision and scope of this qualified comparison. |
| Neither contrast is well supported, or units, state overlap, detection or calibration fail | Report the supported endpoints and their limits. Stop inference for the dependent contrast. Wide intervals, an unobserved state or an invalid count denominator supply no evidence of equivalence. |

Freeze only after resolving the actual cohort and genotype/control design,
tissue and sort/lineage specificity, reporter and current-FOXP3 assay
compatibility, counting and fraction calibration, feasible RNA yield,
detection, sample linkage and batch allocation. The planning record must
then identify the independent units, support per genotype and state,
variance assumptions from fit-for-purpose external or separately documented
feasibility evidence, and the precision needed to distinguish informative
outcomes. Set justified QC thresholds, weights, uncertainty, multiplicity
and missingness rules prospectively, with exact input and code hashes.
The unidentified Wang libraries do not supply an independent variance
estimate, a justified sample size or an effect margin for this plan.

## Conditional functional questions

The recovery/state comparison can answer its own measurement question.
Each additional functional branch needs a separate decision and data.

| Additional question | Required comparison and linked data |
|---|---|
| Does the cultured deficient population suppress less or actively enhance a specified recipient output? | A defined recipient and functional endpoint, matched viable Treg input and recovery, and control versus deficient cultures. An appropriate no-Treg comparator is needed for a claim of active enhancement beyond reduced suppression. Wang Figure 7 already tests a related in-vivo depletion comparator. |
| Is a specified secreted mediator necessary for that effect? | First measure the relevant source-specific protein output and recipient response under a matched recovery/state design. A later mediator-restricted comparison must identify its source and test necessity for the specified response. Sarmento Figure 3B–D already supplies a stimulated-culture supernatant precedent. |
| Does the response depend on recipient, tissue or perturbation timing? | A linked, matched comparison for that particular recipient, tissue or timing interaction. Wang's acute/developmental and depletion experiments, and Zhang's different NK recipient context, retain their original scope. |

This specification completes the feasible public-data follow-up. The
[stage and dependency record](FOLLOWUP_STATUS_20261112.md) identifies the
next inputs needed for each held question and the current review checkpoint.
