# A27 exact source-code execution specification v4

4 November 2026. The coordinator cleared this narrow descriptive implementation, prospective freeze and governed run after reviewing [v3's source/convention/endpoint proposal](../A27_CODE_CONVENTION_SPEC_V3.md). This addendum fixes outputs and incorporates the required interpretation and internal-parity clarifications. It supersedes any broader interpretation of v3; v3 and earlier source versions remain preserved.

## Decision and fixed comparison

Describe where repeated operational receptor keys occur among nominal source codes, and whether processed-table representation or chain inclusion changes that nomination, to guide later label qualification. All20 codes remain nominal. Partial author biological comments are context only; receptor-independent RNA-state concentration, biological redistribution and an age effect remain unestablished. A flat, zero or sparse code-conditioned result is not equivalence. No broad source search or positive-target expansion follows automatically.

Primary: strict single observed complete productive alpha/beta pair. Sensitivity: all complete productive alpha/beta chain sets. Exact nucleotide junction plus canonical full source V/J call sets within mouse define each slot; retain ambiguous calls, collapse duplicate identical slot records only in a complete set, never choose highest reads. Incomplete productive or nonstandard slots exclude a cell from either convention. Empty/unproductive/no-result slots retain their distinct flags. The eligibility rules and per-source-cell coverage are fixed in A27_CHAIN_COVERAGE_MANIFEST_V2.json and A27_CELL_CHAIN_COVERAGE_V2.tsv.

The conventions have different eligible populations. Differences combine inclusion, matching and chain-observation effects; they are neither an isolated algorithm effect nor independent replication. Assert identical same-key partitions on shared strict-eligible cells. That is internal validation, not another biological endpoint. Do not include source code in the key: a receptor label shared across codes must remain the same label in the mouse-wide pool. Do not combine keys across mice.

Endpoint: observed same-key unordered pairs / all observed unordered distinct eligible-cell pairs, equivalently sum n_k*(n_k-1) / [N*(N-1)]. Emit N<2 as NA, distinct from observed zero. Report N, number of observed pairs, collision count, observed key count and single-collision resolution. No binomial pair independence, confidence interval, age pooling, test, rank or causal inference. RNA/CD8 and receptor/eligibility denominators and remaining missingness follow v3 exactly. Mouse-wide pooling is not a weighted within-code attribution; code-shared keys create cross-code collisions.

Fixed mouse order: mouse0088 through mouse0096, preserving source ages and sex. Fixed source-code order: CD8.A, B, C, D, E, F, G, H, I, J, K, P, Q, R, S, T, wM, wV, wX, wY. ALL_CD8 is the first, separate lineage row. Both conventions retain the full9x20 grid plus9 lineage rows, including unsupported rows.

## Exact run outputs and schemas

All outputs are new, under the runner's prospective run directory; no old source/table/figure is overwritten.

- `cell_assignments.tsv`: all13,332 union cell IDs, source mouse/age/sex, join disposition, separate annotation level1/2, GEX/source-CD8 flags, primary/sensitivity eligibility and SHA-256 operational keys, followed by all13 source-chain coverage flags. Only GEX-labelled CD8 cells receive analysis keys. No nucleotide sequence is duplicated into this output.
- `clone_counts.tsv`: convention, mouse, source_code (including ALL_CD8), operational_key, cell_count. Deterministic mouse/code/key order, never frequency ranking. Lineage and per-code rows reuse cells; they are not independent counts.
- `concentration_by_mouse_code.tsv`: exactly378 rows. Convention, scope, mouse/age/sex, source_code, mouse_gex_CD8_total, gex_code_cells, receptor_record_cells, eligible_cells, observed_keys, same_key_pairs, observed_pairs, concentration, single_collision_resolution, support_status, RNA_fraction_of_mouse_CD8, receptor_representation_fraction, eligible_fraction_of_GEX and eligible_fraction_of_receptor_records. Fraction with zero denominator is NA.
- `support_by_mouse_code.tsv`: exactly189 rows. Mouse/age/sex/code, mouse_gex_CD8_total, gex_cells, all13 source-chain flags summed, RNA fraction, receptor representation and primary/sensitivity eligibility fractions. Flags overlap and must not be summed as a partition.
- `source_disposition_by_mouse.tsv`: nine rows. Mouse/age/sex, all-lineage GEX cells, GEX-only cells, receptor-only unannotated cells, GEX separate-annotation missingness and source-labelled CD8_GEX cells. The354 receptor-only cells retain v3's exact hashtag-derived mice and stay outside RNA/code denominators; the25 GEX cells without annotation are not assigned to CD8.
- `concentration_by_source_code.png`: primary and sensitivity side by side, identical fixed rows/columns and shared[0,1] scale. Every tile labels N; N<2 is grey NA, not zero. Titles/caption flag nominal codes, differing eligible populations and coarse small-N observations.
- `representation_and_eligibility.png`: same fixed rows/columns, three shared[0,1] panels for code-RNA/all-RNA-CD8, strict eligibility/code-RNA and set eligibility/code-RNA. Tile text shows numerator/denominator. Zero denominator is grey NA. These are processed-table representation, not assembly success or capture efficiency.
- `summary.json`: exact input/output dimensions and rosters, source-coverage scalar parity, strict-subset partition parity, computable-stratum counts and interpretation scope. No new inferential summary.

Plots have no effect-based row/column order, axis score, clustering or clipped concentration scale. A small-N extreme is not a confident biological lead. The source-disposition/support tables remain alongside every concentration interpretation.

## Freeze, validation and stop conditions

The contract must bind the portable raw IGT29 receptor-subset hash, entrypoint and all metadata/declaration dependencies. Preserve the original full-member source integrity and source-annotation versions. Fixtures cover known pair-collision arithmetic, zero/single-cell NA, cross-mouse separation, shared keys across codes, reordered/duplicated ambiguous V/J calls, duplicate/distinct secondary slots, incomplete/nonstandard chains and known strict-subset partitions. No source concentration is calculated in preparation.

Execution verifies each source coverage flag against the previously qualified13,332-row metadata; keeps9 mice/20 codes and all189/378 grid rows; verifies count reconstruction, valid pair arithmetic, code support partition and strict-subset same-key partition. Stop for any input/hash/source-identity/eligibility/partition failure rather than relax a rule. Independent numerical, visual and biological review of the new results precedes canonical A27 updates. Execution does not grant scientific acceptance or claim promotion.

The machine-readable [output schema](A27_OUTPUT_SCHEMA_V1.json) fixes exact TSV column names/order, paths, fixed row counts and NA/empty-key conventions; execution checks it before writing tables.
