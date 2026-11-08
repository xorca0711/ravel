# Stepwise analysis plan — ungated aged-brain IL-10

8 November 2026. Owner-requested plan following the [paper fit review](README.md)
and [metadata follow-up](METADATA_FOLLOWUP.md). This is the current sequence for
possible numerical reuse, superseding the README's initial object-first
suggestion. **Execution status is now in [STAGE_STATUS.md](STAGE_STATUS.md): source and
animal stages executed under Nn26-P01; RNA stages remain pending.** This original
sequence does not itself confer scientific acceptance. Frozen contracts and
receipts are linked from [RESULTS.md](RESULTS.md).

## Purpose and scope

**Article-local question:** what can the deposited data reproduce about the
separation between WT/D25K-associated immune responses and measured neural or
behavioral outcomes in aged male mice, at each reported exposure?

The contribution is source qualification, published-result reproduction and
bounded description. The T-cell/IFN mechanism is a published premise, not a new
Ravel discovery. Previous exposure includes Figs. 1–7, their reported outcomes,
the correction, Methods and author code. Later freezing does not turn this
into an unexposed confirmatory study.

| Analysis branch | Comparison and measured endpoint | Unit and interpretation limit |
|---|---|---|
| Animal outcomes, priority | D25K versus old vehicle for cognition; D25K versus WT and each versus vehicle for eligible neurogenesis/nesting panels | Individual mouse, with nested sections/repeated tasks and cohort identity preserved. Different assays, doses and cohorts are separate estimands |
| Pooled RNA | Within each verified dose: D25K minus WT, and each minus old vehicle, within retained cell types | One observed pool/library per condition; finite-pool expression/recovery description, without animal-population inference |
| Young reference | Young versus old vehicle | Context for age-associated differences; not an age-by-treatment interaction |

Main validity threats are source/dose misidentification, treatment-confounded
pool variation, cell recovery/composition, attrition and outcome-dependent
selection. The steps below test identity, units, denominators and arithmetic;
they cannot resolve missing biological replication or prove mediation.

## Step 1 — Complete the source and exposure crosswalk

**Available now:** six BioSample records, 20-run inventory, five-object manifest,
frozen code, article and correction. **Still required:** readable S1/S4 and
supplemental figures, or an equivalently explicit source for a particular
field. An inaccessible functional table need not prevent independent metadata
qualification of the RNA object.

Create a provenance table with study/cohort, source accession, run/library,
code alias, dose and units, vehicle, infusion/recovery duration, age, sex,
tissue, mice per pool, number of pools, sequencing chemistry and exact source
locator. Keep unknowns explicit. Match C1–C8 and WT1/WT5/WT50 labels to actual
deposits; resolve whether the extra code labels ever entered the public object.
Do not interpret barcode prefixes as donors.

For S4, inventory sheet/panel, endpoint definition, units, treatment, mouse or
source-row ID, experiment, section/well nesting, exclusions, reported n,
reported test and reported direct comparison. Distinguish an original mouse ID
from a row identifier created solely for traceability. Reconcile SVZ versus
olfactory-bulb n and the cognition exclusions; a common row order is not a join.

**Output/decision:** a source-qualification report and explicit eligible
comparisons. Unresolved aliases hold only the affected dose comparison.
Unrecoverable mouse keys prohibit cross-assay matching; a clearly documented
independent mouse-level panel may still be analyzed on its own.

## Step 2 — Register and freeze each executable stage

Follow [research governance](../../docs/RESEARCH_GOVERNANCE.md#prospective-contract-and-execution).
Before new scientific scripts/tables or numerical work, register an article-local
candidate and its relation to Sx10/A25/A26/A27, then create stage-specific
versioned contracts with exact source/code hashes, units, exclusions,
comparisons, methods, multiplicity, exposure record and stop rules. Preserve
the separate ungated namespace and all existing question status.

Use metadata-recovery framing for object qualification and exposed
reproduction/descriptive framing for numerical reuse, as allowed by the
current schema. Record missing precision or identifiability honestly. No
biologically meaningful effect margin can yet be justified from this review.
Freeze and commit before the repository runner; verify and register receipts
afterward. Do not run the original overwrite-prone author scripts in place.

**Output/decision:** valid preflight for the specific stage, not approval of a
biological claim. Later choices that change frozen comparisons require a new
version and amendment/exposure record.

## Step 3 — Reproduce the animal-level outcome evidence first

S4 is small and can change interpretation more directly than a new clustering
analysis. Keep all reported eligible contrasts, including unfavorable and null
ones; the priority order below does not license selective reporting.

1. **Cognition (Fig. 7F–H):** reconstruct final denominators and exclusion
   reasons; check the published direct D25K-versus-vehicle tests for Y-maze
   discrimination index and NOR novel-object percentage. Reproduce chance
   tests separately and label them as such. There is no WT cognition contrast.
2. **Neurogenesis (Fig. 6G–J):** reconstruct each mouse's reported DCX,
   DCX/EdU and NeuN/EdU endpoint, retaining region, area normalization, cohort
   and averaging of six olfactory-bulb sections. Inspect the direct D25K–WT
   comparison as well as both vehicle contrasts. NeuN/EdU is a newborn-neuron
   marker endpoint, not demonstrated integration or lesion repair.
3. **Nesting (Fig. 7B/C) and immune protein readouts:** retain ordinal nest
   scores and the distinct RIPR cohort. For FACS, preserve each mouse's MFI
   and the documented experiment-control normalization; technical cell counts
   are not n. Keep culture wells, primary preparations and animals distinct.

First reproduce the authors' exact reported tests and correction conventions;
record any unresolved test options or discrepancy without silently replacing
them. For an added descriptive effect summary, predefine D25K-minus-comparator
mean differences in each continuous endpoint's original units, and a rank-based
effect for ordinal nesting. Interval calculations must resample independent
mice, retaining known experiment blocks and task dependence. If unit/block
metadata do not support an interval, report the point description and the
precision limit instead of treating sections or wells as replicates.

Any new inferential layer needs an explicit contract: separate the two
behavioral endpoints from the neurogenesis endpoint/contrast family, specify
multiplicity treatment before calculation, and retain the original unadjusted
results as reproduction evidence. Do not use post-hoc power or invent an
equivalence/noninferiority margin. Nonsignificance is not equivalence.

**Output/decision:** panel-to-source audit, mouse-level plots, effect and
reported-test reconciliation, and attrition/precision statement. Direct
between-group support would strengthen that endpoint only. Uncertain or
contrary contrasts narrow the claim; they do not trigger a search for a more
favorable score.

## Step 4 — Qualify the main processed RNA object

Download **only `IL10_svz_seurat.rds` initially** (2,188,161,276 bytes), validate
the Zenodo checksum, and record SHA-256, R/Seurat versions and available memory.
Do not start with all five objects or FASTQs. Inspect serialization and slots
without making a dense whole-transcriptome copy or rerunning integration.

Under the metadata contract, inventory actual metadata columns, condition
levels, barcodes, cell-type labels, RNA count/normalized layers, original
identifiers, QC measures, exclusions and any true donor-demultiplexing fields.
Verify matrix/metadata alignment, barcode uniqueness, label completeness and
retained cells per condition/type. Trace later cluster exclusions as well as
the initial QC thresholds. Resolve the deposited filename versus the
`_IL10.rds` filename used by several scripts.

Treat hypothetical donor fields as unknown until inspected. Recoverable mouse
labels require provenance showing that molecules/cells were assigned to mice;
pool-size metadata alone do not establish this. If actual donor assignment
changes the known design, amend the interpretation prospectively rather than
silently upgrading the analysis.

**Output/decision:** immutable metadata inventory and qualified six-arm
crosswalk, or explicit unresolved additional/absent arms. Stop affected
comparisons if the dose, assay layer or retained-cell identity is uncertain.

## Step 5 — Describe the immune-response separation at verified doses

Use the published cell-type annotations initially. Preserve microglia and T
cells as distinct populations; retain combined astrocyte/qNSC and aNSC/NPC
labels unless independent annotation evidence supports separation.

For each verified dose, report D25K–WT and each treatment–old-vehicle contrasts
for two separate measured components:

- Microglial suppression-associated/IL-10-related RNA and microglial IFN-related
  RNA, with exact published marker lists and provenance frozen before execution.
  These are transcript measurements, not direct secretion or pathway flux.
- T-cell Ifng/Gzmb expression and recovery, retaining all T cells and the
  separate Gzmb-positive subset denominator. The reported nine old-control T
  cells make this branch especially sensitive to sampling.

The concrete primary summaries are mean expression on the verified author RNA
normalization scale, fraction with detected counts, and cells recovered per
library/type. Show each marker, denominator and direction; do not optimize a
combined beneficial-aging score. The young vehicle is a reference only.
Equal-cell downsampling may be a fixed-seed measurement sensitivity, not an
animal-level test. Cell-level permutation P values and bootstrap intervals
cannot supply between-mouse uncertainty.

Report within-annotation expression and recovered composition separately.
Marker-based subtype sensitivity may expose composition dependence but cannot
rule out unmeasured states or capture bias. Two doses are separate exposure
conditions, not replicate mice. A concordant pattern is within-study
consistency; a discordant pattern must remain visible.

**Output/decision:** dose-specific descriptive contrasts with zero/sparse
denominators and selection qualifications. This stage can verify the deposited
measurement pattern; it cannot estimate a population D25K treatment effect.

## Step 6 — Use auxiliary sources only for a defined unresolved comparison

- Qualify `WT_IL10_svz_seurat.rds` only if the WT response needs a separate
  cohort check. Keep its 27-month/2022-12-14 identity distinct. It supplies no
  independent D25K–WT comparison.
- RIPR cohorts can contextualize increased immune activation without improved
  outcomes; brain/lung pools can contextualize tissue-associated T-cell states.
  Neither repairs the main IL-10 replication or age-factorial design.
- Reused Dulken/Liu/Buckley/Sun sources can test whether a baseline age-associated
  description depends on atlas or region, after resolving mouse/source overlap.
  They cannot be appended as untreated exchangeable controls for this surgery
  and intervention, or counted as new replications of their own source data.

Each optional acquisition requires a stated unresolved question and its own
eligibility decision. Aging-clock refitting, broad ligand–receptor scoring and
new trajectory analyses are not needed for the present objective.

## Step 7 — Synthesize evidence and define what new data would be needed

Produce a compact evidence map: published finding → reproduced measurement →
remaining uncertainty → next informative comparison. Keep RNA, secreted
protein, tissue markers and behavior as separate layers. Without explicit
shared-mouse keys and a suitable design, do not fit cross-assay prediction,
correlation or causal mediation from their group averages.

| Intended extension | Required comparison; what current metadata cannot supply |
|---|---|
| Does aging modify cytokine selectivity? | Same D25K–WT contrast in independently sampled young and old units at matched exposure; estimate the difference between age-specific contrasts. Include age-matched vehicle when effects relative to baseline are part of the question |
| Does an intervention restore function after damage? | Defined injury, treatment timing and functional recovery endpoint, with age context and appropriate injury controls; the present physiological-aging study does not supply this design |
| Does the proposed immune route cause neurogenesis or cognition improvement? | A fit-for-purpose perturbation/measurement that discriminates the route for the specified endpoint; co-culture IFN evidence alone does not establish in-vivo mediation |

These are future design requirements, not launched experiments or adopted RQs.
Any material RQ development follows the repository's
[literature workflow](../../docs/governance/LITERATURE_WORKFLOW.md), including closest
precedents and contrary findings. Update README/context and the owning dossier
if a candidate is registered; preserve all frozen versions and unfavorable
results. Review of source fidelity and scientific interpretation remains
separate from a successful run receipt.

## Current handoff

**S1/S4 have now been recovered and the animal stage executed.** Follow
[RESULTS.md](RESULTS.md) and [STAGE_STATUS.md](STAGE_STATUS.md) for direct tests,
source discrepancies and pending RNA work. The next dependency is a suitable
executor for main-object qualification, followed by resolving actual code/dose
aliases and layers before any within-dose RNA description. No age
interaction, repair claim, hidden replicate or definitive cognitive superiority
over WT can be manufactured by further analysis of these deposits.
