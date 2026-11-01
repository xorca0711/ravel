# C0 source qualification

31 October 2026 (Asia/Seoul). C0 qualifies for the bounded descriptive run.

The existing restored `figure1_descriptive.h5ad` was opened read-only in this
worktree; no copy, preprocessing or relabeling was necessary. Its SHA-256 is
`6d2ab27a98543d3f03c941907729af69ca9ce22295e51cff67e329ce8c1644ca`, matching
the [original receipt](../../../analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327/receipt.json).
The receipt itself matches the scientific review's SHA-256
`24aaaaef907519391ba3c8650f96795ebe2dff4a27cd4ad9e9977852cdc5974b`.
The saved cell-state and composition files also match their receipt bindings.

The H5AD contains 11,683 cells and 27,998 unique saved feature symbols. Exact
case-sensitive mapping finds `Il22ra1` once at zero-based column 7,863 and
`Il10rb` once at column 24,495. These are saved symbol identities, not a newly
verified Ensembl mapping or annotation-release claim. No alias expansion is used.
`layers/counts` is CSR with 23,319,487 stored entries and float32 storage. The
[scientific review](../../gate1_02_choi_2020/weft_pilot_v1/SCIENTIFIC_REVIEW.md)
previously verified positive integer values and matching saved cell totals; the
new run will enforce these properties again before using the counts.

All ordered cell identifiers and all `library`, `gsm`, `timepoint` and `state`
values agree exactly with `cell_states.csv`. Its `sample_prefixed_cell_id` maps to
H5AD `obs/barcode`. The 24 observed library/label composition strata agree with
the saved composition file, including the source's non-contaminant denominators.

| Literal library | GSM | Saved time label | Retained cells | Non-contaminants including unassigned |
|---|---|---|---:|---:|
| PBS_AT2_Tomato | GSM4304609 | PBS | 4,319 | 4,236 |
| Day14_AT2_Tomato | GSM4304611 | day 14 | 3,790 | 3,592 |
| Day28_AT2_Tomato | GSM4304613 | day 28 | 3,574 | 2,571 |

The eight observed labels are retained literally. The source rule additionally
allows `pAT2`, `unassigned` and `contaminant_endothelium`, absent here; each will
receive an explicit empty-stratum row. Their absence is a pipeline/coverage
fact, not biological absence. The source's exact non-contaminant rule is
`not state.startswith('contaminant_')`; unassigned cells would remain included.
No library or label is treated as an independently replicated animal group.

## Exposure and runtime

Prior source outcomes, marker tables, composition and annotation limitations were
already exposed. C0 read schema, identifiers and metadata only: neither count
data nor `X`, feature means or variances was read. The two selected transcripts'
values were not inspected during this C0. The study remains exposed/descriptive;
this statement does not claim historically unexposed outcomes.

The installed Python 3.12 ARM64 lacked h5py. An isolated h5py 3.16.0 wheel was
installed without dependencies into ignored `.tools/sx22_e1a_runtime`; existing
NumPy/SciPy/Matplotlib are reused. No global runtime or source file changed.
A temporary metadata reader initially used `barcode` as the CSV field name and
raised `KeyError`; using the actual `sample_prefixed_cell_id` field completed
the exact join above. This was a reader mismatch, not a failed source join or
content restriction. No scientific calculation occurred before freeze.
