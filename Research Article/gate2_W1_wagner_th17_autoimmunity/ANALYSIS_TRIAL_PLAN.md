# Execution structure and next handoff

**Current checkpoint:** the first R0 source-identity pass is [executed](RESULTS.md)
under a [frozen contract](config/source_qualification_v1.json). Its precise remaining
work is in the [handoff](HANDOFF_2026-10-04.md). The stage table below remains a
plan; it does not imply that R1–R5 have executed.

The original structure below was a documentation-stage plan.
Do not interpret planned filenames as existing artifacts. The registered owner
for source reproduction is Wg-R01; branch owners are Wg-P01 through Wg-P06.

| Stage | Dependency and decision | Planned output under a new immutable run |
|---|---|---|
| R0 metadata | Public source records, file hashes, units, exact cell joins and environment | Input manifest; sample/unit map; exclusions; per-stage eligibility report |
| R1 source scores | Qualified author outputs and exact postprocessing | Panel 2C/2E comparisons; reaction/metareaction crosswalk; mismatch report |
| R2 full Compass | R0 environment and expression fidelity; R1 reference | Versioned penalties; solver logs; numeric concordance and version differences |
| R3 RNA | Qualified GSE162300/GSE162382 design; independent of R2 compute | Gene-level contrasts; program partitions; per-unit summaries; design diagnostics |
| R4 ATAC | Qualified GSE165088 and external annotations; does not require R2 | Accessibility contrasts; enrichment universe; aggregate RNA/ATAC comparison |
| R5 other assays | Numeric source tables and actual biological units | Assay-specific contrasts and explicit unreproduced panels |
| Exploratory branches | Branch-specific eligibility after source reproduction | Bounded hypothesis/rival report, including null/discordant/held outcomes |

## Before the first substantive run

1. Create a versioned R0 metadata entrypoint and contract from
   [the template](../../analysis/research/contract.template.json). Declare source
   identity and feasibility as the endpoint. Unknown independence is allowed
   for metadata recovery, not population inference.
2. Register the contract in [the registry](../../analysis/research/registry.json),
   binding exact code/input hashes and portable paths. Include this package and
   its literature context in evidence references. Record prior outcome exposure.
3. For later stages, freeze actual contrast, population, denominator, exclusions,
   multiplicity, transformations, tolerances and stop rules. No automatic effect
   margin or sample-size floor is supplied here. Confirmation would need new
   independent units, justified precision and appropriate outcome exposure.
4. Preflight, freeze and commit the contract and code; run with
   [the governed runner](../../docs/RESEARCH_GOVERNANCE.md#prospective-contract-and-execution).
   Give every run a new ID. Verify the receipt and perform a separate mechanical
   endpoint check before interpretation. Use versioned amendments for changes.

Future implementation belongs in this paper's `scripts/` and `config/`, with
large source inputs under ignored `raw_data/`. Run-owned output belongs in
`analysis/research/runs/<new-run-id>/`; register receipts and link their result
reports from this package. Do not replay historical scripts into frozen outputs.
Create these paths when an eligible implementation exists, not empty scaffolds
that suggest an analysis has been implemented.

## Efficient order

R0 then R1 provides the smallest reviewable result without requiring a full
solver run. R3/R4 can proceed on their own qualified designs while R2 awaits
environment/source fidelity. R5 is limited by raw numerical assay data. Do not
download all parent-series raw libraries before checking subset and processed
input availability. No compute cost or runtime estimate is asserted without
measurement. Later extensions are exposed exploration until independently
qualified; published functional results are not newly generated endpoints.

**Exact next action:** qualify the scientific runtime and implement/freeze R1
source-score reproduction using the already hashed author example and 290 exact
cell-to-GSM joins. Animal/preparation maps remain unknown for the sorted cells;
population inference remains held. Full historical environment, source assay
values and solver availability remain open. Host laboratory access is unconfirmed.
