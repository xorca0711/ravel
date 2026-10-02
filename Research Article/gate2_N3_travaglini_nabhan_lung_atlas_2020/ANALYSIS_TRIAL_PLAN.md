# Staged analysis plan

**Current analysis label: Nb4.** This planning document precedes execution; see the [completed evidence and gallery](README.md) and [RQ derivation](reports/RQ_DERIVATION.md). Historical TN2020 run identifiers are preserved.

**Planning version 1, 2 October 2026.** Source-informed after paper, note,
supplement and code inspection. TN0 is implemented and run; TN1's metadata
validator is implemented but has no real cell input yet. TN2-TN5 are specified
future work, not completed analyses. Machine-readable state:
[pipeline_v1.json](config/pipeline_v1.json).

## TN0: source identity and design intake

**Decision:** identify usable source materials and constraints before numerical
expression work. Hash source inputs, inventory all workbook sheets, tabulate
Table 2 by donor/assay/type, reconcile independent totals, and inspect library
design. Preserve dash/blank absence markers. Separate published, recomputed
and currently unresolved values. Complete with an evidence-linked intake
report even if exact arithmetic or biological coverage fails.

**Delivered:** [intake report](reports/INTAKE.md), immutable
[run record](runs/intake_v1/run_record.json), schema and coverage tables.

## TN1: processed-data eligibility and unit map

Retrieve versioned Synapse cell metadata and file metadata first. Resolve the
historical FACS corrections, assay identifiers, healthy/tumor filtering,
donor/library nesting and region vocabulary. Document the mapping instead of
inferring anatomy from a label. Run the metadata validator on the resulting TSV.
Only then choose the smallest matching expression object.

**Outputs:** source-version crosswalk; cell and library coverage; exclusions;
donor-by-assay-by-region contrast eligibility; matrix join audit. Three donors
with at least 20 cells in each arm within the same assay and anatomical region
is a planning eligibility floor, not a power guarantee. Show 10/30/50-cell
sensitivity. Regions, replicate libraries and two technologies do not create
additional biological donors. A failed count gate precludes a population
contrast but can still permit explicitly donor-specific displays.

**Stop:** unresolved donor identity, mixed source releases, missing matrix-cell
joins or assay/count-unit confusion. Region-confounded contrasts can only be
reported as joint subtype/location associations. TN1 passing metadata does
not pass raw-count or biological-inference gates.

## TN2: bounded source reconstruction

**Question:** can the selected published identities and displays be recovered
from the declared source release? Use author labels as the primary reproduction
target. Reconcile label counts with Table 2 and record every release/filter
difference. Preserve the original per-donor/per-assay clustering design if
attempting source clustering. A modern Scanpy/Seurat approximation gets its own
name and parameters, not an exact-reproduction label.

Before a fit, freeze an execution contract containing: input hashes and layers;
gene universe and symbol mapping; assay-specific QC/normalization; population;
score definition; sampling seed if applicable; donor aggregation; output
directory; source panel and quantitative agreement criterion.

**Priority displays:** Fig. 1c AT2 markers; Fig. 1e stromal identity markers;
ED5 MYRF/TBX5 expression context. Resolve panel-specific assay from captions
and notebooks; do not apply the 10x and SS2 scales interchangeably. Reproduce
source means/detection fractions first, then show donor-separated views.
Source marker p-values remain source cell-level statistics, not locally
estimated donor-level significance. Table 4-selected genes cannot independently
validate the same source labels.

**Stop or narrow:** missing source definitions, unresolved count release or
insufficient donor coverage. Report concordance as partial when appropriate;
do not tune filters until the figure resembles the paper.

## TN3: focused descriptive extensions

| Question | Measurement and comparator | Rival checks | Decision |
|---|---|---|---|
| AT2-s versus AT2 | Within-donor, assay- and region-matched expression/detection differences for a frozen source panel; raw-count pseudobulk only when eligible | Detection depth, sorting fraction, donor dominance, ambient RNA, alternative label definitions | Current Table 2 gate fails; retain source/donor-specific descriptions until new eligible coverage exists |
| Alveolar versus adventitial fibroblasts | Within-donor subtype contrast on a fixed identity panel; separately inspect the existing A13/A22 chemokine questions | Region and subtype confounding, fibroblast abundance, endothelial/mural contamination, donor omission | Eligible coverage may support normal-tissue subtype context; no inference of injury-induced recruitment |
| MYRF specificity | AT1 versus other epithelial populations, with per-donor expression and detection; source label is an exposed definition | AT1 depth/fragility, doublets, general epithelial expression, circular marker selection | Repeated specificity motivates external validation; it does not prove maturation control |
| TBX5 specificity | Pericytes versus vascular smooth muscle, airway smooth muscle and fibroblasts | Mural misannotation, region enrichment, sparse detection | Narrow a pericyte-associated candidate; do not infer contractility or perfusion |

For raw-count pseudobulk, aggregate libraries within the declared donor,
assay, region and label after verifying count compatibility. Equal-weight
donor summaries are primary; cell-weighted summaries are descriptive sensitivity.
Use donor estimates, observed range and leave-one-donor-out direction first.
With only three eligible donors, report low precision and avoid strong population
generalization. A formal model or equivalence test requires a separate exact
estimand, meaningful-effect margin and justified uncertainty procedure.

Prefer individual gene effects and a clearly specified fixed panel over searching
for a favorable score. Preserve cell identity panels separately from tested
pathway panels; record overlap and results with shared genes omitted. Any
exploratory genome-wide testing needs a defined test family and multiplicity
correction in the execution contract. No p-value is currently being generated.

## TN4: species transfer and independent-data gate

Start with Tables 6-9 and source code, not a concatenated human-mouse embedding.
Resolve each mouse's source study, age, sex, assay and annotation; the combined
mouse material includes ageing-atlas animals. Use a pinned one-to-one orthology
map and list unmapped/ambiguous genes. Match compartments and comparable ages
where possible; do not convert a species/age/technology mixture into a pure
species effect. Table 7 comparisons and evolutionary classes are published
results, not new estimates.

Audit whether an external human reference contains these same donors before
claiming replication. Use donors excluded from model fitting or a separate
study for independent evaluation. Annotation agreement does not validate a
Wnt mechanism, AT2-s stemness or an injury-transition identity. Failure of a
human AT2-s/mouse stem-cell correspondence is informative and remains recorded.

## TN5: interpretation and RQ routing

Each completed stage produces its question, inputs/exposure, unit, measurement,
result, strongest rival, missing evidence and proceed/narrow/stop decision.
Figures link to tables and run hashes. Attach useful findings to existing
A1/A4/A8/A13/A22 only when the population and measurement match their contracts.
New global questions require checking the current canonical register and remote
allocation; this older local checkout is not sufficient for assigning an ID.

**Success for the initial package:** a trustworthy source map, explicit failures,
an executable intake/metadata gate, and a concrete next input. It does not
require making all candidate questions estimable from this small atlas.
