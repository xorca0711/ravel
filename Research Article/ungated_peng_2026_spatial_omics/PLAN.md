# Stepwise plan: Pg1-P01 and existing-question extensions

## Authorized public-data branches — prospective amendment, 8 November

The owner reports Zenodo access requested, approval pending. Continue accessible
public data now: **A**, existing A12 cell-level candidate configuration, then **B**,
Pg1-P01/C3 lattice-based Visium RNA organization. See [fixed cell specification](PUBLIC_CELLS_SPEC_V1.md)
and [targeted literature/context](PUBLIC_DATA_CONTEXT.md). These new exposed
descriptions use existing public counts; they do not relax author-dependent stages
3–6 or replace pathology with expression scores. The historical statement that
tables alone do not enable expression work remains true. Branch A has executed with 7,677 independent checks and exact old-count parity.
Branch B now has its [fixed lattice specification](PUBLIC_SPATIAL_SPEC_V1.md)
and registered input-bound contract, pending its committed freeze/run. Measured
result plots and a separately labeled rationale figure will be stored with receipts.


8 November 2026. The owner requested source recovery, ungated placement and then
execution in a separate technical chat. This plan authorizes progression through
eligible steps with prospective contracts; it does not make missing inputs
available or certify scientific acceptance. [Actual source status](SOURCE_RECOVERY.md).

**Execution status:** [Original GEO metadata](RESULTS.md) remains frozen in its
run. The [supplementary qualification](SUPPLEMENTS_RESULTS.md) completes the newly
eligible S1 clinical/participation reconciliation, S2–S4 list definitions, S5/S6
published assay summaries and aggregate TMA portion of stage 6. Actual annotation,
geometry, exact section/core maps and measured-panel requirements still hold
stages 3–6. Stage 7 still lacks linked functional inputs. The next input-driven
contract must qualify those exports before any reproduction or A12 calculation.

## Purpose, comparison and limits

Pg1-P01 asks whether author sample, pathology and ROI definitions can be recovered
and joined sufficiently for faithful spatial reproduction. The comparison is
between deposited identifiers/annotations, the published methods, and existing
C3 source inventories. Endpoint: recoverable joins, disagreements, ambiguous
mappings and annotation coverage. The validity threat is a plausible but false
identity match, particularly across serial sections or independent cohorts.
Patients are biological units; metadata records are the immediate audited units.
No mechanism, effect margin or sample-size justification is invented for this
metadata task. The paper, notes and reused results have already been seen.

## Execution sequence

| Step | Work and owner | Deliverable and decision |
|---|---|---|
| 0 — source ledger | Pg1-P01: reuse recovered public metadata, previous C3 inventories and source access receipts. Record version/URL/hash; verify downloads are their claimed format. | Source manifest with successful, restricted, unresolved and failed routes. GEO v3 and supplement v2 manifests complete for received sources; new access only for a named remaining gap. |
| 1 — sample joins | Pg1-P01: parse the three GEO SOFT records; compare exact author library aliases, GSMs and demographics with existing crosswalks. Qualify WES separately; reconcile S1 if obtained. | `samples.csv`, `crosswalk.csv`, `join_issues.csv`, `summary.json`. One row per actual library/section, no fabricated Xenium records. Accept patient-level matches at that level only; unresolved specimen relationships stay unknown. |
| 2 — pathology/ROI recovery | Pg1-P01: inspect documented public supplemental/author products and existing member inventories. Obtain permitted exports if available; distinguish published definitions from actual geometry/labels. | Annotation inventory and schema, exact recovered files, missing-data specification. If exports are inaccessible, retain the hold on region-specific analysis while completing metadata work. Do not repeatedly download the known 9.4 GB archive. |
| 3 — coordinate and annotation qualification | Pg1-P01, conditional on exports: check sample/barcode uniqueness, polygon membership, units/orientation, image dimensions, transforms, label dictionaries, QC and category totals against author figures. | A bounded alignment/QC report with overlays from measured data, exact disagreements and exclusion counts. Failures hold only affected sections/analyses. No score-derived replacement for missing pathology. |
| 4 — faithful source description | Pg1-P01, conditional on step 3: reconstruct one prespecified pathology/state composition and one 80-micrometer neighborhood comparison, using supplied author cell states and known panel. | Source-reproduction report, author-versus-reproduced differences, patient/section contributions, density/edge sensitivity. Name departures explicitly. No new causal or progression claim. |
| 5 — contextual discrimination | A12 owns a new exposed exploratory contract: compare an independently specified epithelial RNA endpoint with local IL1B-high myeloid abundance within qualified state/pathology strata. | Estimate a within-state contextual association, with patient-level summaries/uncertainty and nested sections. If state independence or endpoint coverage is missing, record unestimated; preserve prior A12 results. |
| 6 — transport/boundary | Qualify the reported independent TMA cohort, then freeze a compatible procedure only if cohort identity, panel and core nesting support it. | Independent-source validation only for the endpoint actually measured. Smaller-panel proxy substitution requires an explicit new rationale/contract; no automatic validation of the original A12 index. |
| 7 — functional bridge | Existing A1/A8/A14 (and relevant source owners) retain longitudinal state, mature-output and withdrawal questions. | A later experiment design needs actual linked output, timing and feasible model/precision. Human snapshots, growth or loss of KACs do not complete this step. |

## Required join schema

Keep separate fields for `cohort_id`, `patient_id_author`, `lesion_id_author`,
`block_id`, `section_id`, `platform`, `GSE`, `GSM`, `library_name_author`,
`histology_original`, `histology_reviewed`, `ROI_id`, `core_id`, `cell_or_spot_id`,
`coordinate_frame`, `annotation_source`, `source_locator`, `join_level`, and
`join_status`. Unknown fields remain empty with an explicit reason; parsed
aliases get separate fields and a stated parsing rule. Source-qualified joins
must be unique at their declared level. Multiple candidate matches are reported,
not silently resolved. Normal tissue, adjacent normal and lesion-bearing sections
remain distinguishable. Cohort-qualified IDs prevent discovery/TMA collisions.

## Step 5 scientific specification before execution

The proposed hypothesis is that local inflammatory context is associated with
epithelial inflammatory RNA variation **within a comparable state and pathology
stratum**. Main alternatives are epithelial mixture, tissue density/edge effects,
state-label circularity, shared patient context, reverse recruitment and other
signals. An association does not establish ligand secretion or receptor activation.

Freeze the actual state definition, source-cell definition, measured endpoint,
panel coverage and exclusions after source qualification and before calculation.
Audit overlap between annotation features and endpoint genes, including the IL-1
genes used by the existing healthy-reference transfer. Prefer an independent
state definition where support exists; an endpoint-exclusion label sensitivity is
not by itself independent validation. Do not impute unmeasured panel genes as zero.

Use patients for inference or holdout, retain nested section/ROI identities, and
account for density, tissue boundaries and overlapping neighborhoods. Do not
turn millions of cells into independent replicates. Document the finite observed
patient set and precision limits; no arbitrary eligibility count is a power claim.

| Observed outcome | What it would change |
|---|---|
| Within-state association consistent across patients | Supports spatial context beyond broad mixture in this cohort; remains an association and shared-source follow-up. |
| Attenuation with state/density qualification | Narrows the previous contextual interpretation; does not establish IL-1 irrelevance. |
| Contrary or heterogeneous patient results | Retain them and reconsider transport/sampling; do not search alternative scores until positive. |
| Incompatible annotations/panel or too little precision | Endpoint unestimated or imprecise, not a biological null or equivalence. |

## Execution and stopping rules

Every new numerical stage requires a registered, frozen, committed contract with
exact input/code hashes, honest exposure and an immutable runner receipt. Stage 1
is metadata; stage 4 is descriptive reproduction; stage 5 is exploratory; stage 6
is not confirmatory without a defensible unexposed design and justified precision.
Verify joins and arithmetic independently before interpreting output.

Complete all accessible work, then name the narrow missing input for held steps.
Do not change frozen definitions, claim grades, canonical questions or governance
to clear a hold. Follow a newly documented public source when it could resolve a
specific gap; do not retry the same failed routes indefinitely. Contacting authors
or requesting restricted access is a separate external action, not authorized
by the local execution plan. [Technical handoff](TECHNICAL_HANDOFF.md).
