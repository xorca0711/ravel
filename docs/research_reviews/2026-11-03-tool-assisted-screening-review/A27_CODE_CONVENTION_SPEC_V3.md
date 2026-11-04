# A27: source-code qualification, chain coverage and exact descriptive proposal v3

4 November 2026. Review-ready preparation; no clone identities, clone frequencies or concentration have been calculated. This follows [source intake v2](A27_SOURCE_FOLLOWTHROUGH_V2.md) and the coordinator's scoped source/coverage authorization. The unfavorable earlier atlas result remains unchanged.

## Source-label construction: what is known and still unknown

The linked author CD8 notebook at revision 7b2714071eec19d0db91162c97b6fd0b68ffcc09 loads an already curated RNA/ADT object. Its figure outline interprets I/J/K in acute-effector context, E/F/G/H in circulating-memory context and Q in resident-memory context, while marker plots use existing cluster labels. It does not reconstruct all labels. Its separate Ag_spe_v2 metadata explicitly prioritize TCR-seq for P14 identification; receptor-aware metadata therefore exist. The reference TOTALVI script uses RNA/protein inputs, but this is insufficient to prove that final curated labels never used receptor information.

The author's linked CD8 and reference manuscripts were identified through official version metadata (both now version3). Their full-text routes were inaccessible and the official linked XML requests returned HTTP429. No retry loop, full-methods claim or absence claim follows. [Exact notebook cells, file/blob hashes, code locators, manuscript versions and access limits](prerequisites/A27_STATE_CONSTRUCTION_QUALIFICATION_V2.json).

Accordingly, use the exact deposited CD8 level2 codes as **nominal source annotations**, with partial author interpretations only. Do not relabel all codes as independently validated naive/effector/memory states or transfer a later manuscript's interpretation automatically onto the February annotation table. A code-conditioned description is possible; the stronger question of concentration within independently defined RNA states versus biological state redistribution remains limited by this provenance gap.

## Source mapping correction and eligibility coverage

[Source join v3](prerequisites/A27_IGT29_SOURCE_JOIN_V3.tsv) fills a specific omission in v2: 354 receptor-only records had valid I29H1-I29H9 hashtags but blank derived mouse/age/sex fields. They now map through the already verified exact hashtag map. [Versioned correction/provenance](prerequisites/A27_IGT29_SOURCE_JOIN_V3.json) and [reproduction script](prerequisites/A27_join_receptor_only_mice_v3.py) preserve all earlier versions. These records still lack separate state annotations and remain outside GEX/CD8 denominators; no cell state or additional animal was invented.

The separate GEX annotation identifies 6,293 CD8 cells, including 218 without a receptor record. Receptor records represent 6,075 of them. The source labels span20 codes, including CD8.wV recovered among GEX-only annotations. Exactly3,252 cells have one complete productive alpha and one complete productive beta slot. Including all complete productive chain sets yields3,792 cells, adding540 cells whose exclusion could induce selection. Coverage varies across mice and codes. Of the fixed9 mice x20 codes,97 strict-pair strata and102 set strata have at least2 eligible cells; that is mathematical computability, not adequate precision or power.

| Mouse | Age weeks / sex | RNA CD8 | Receptor record | Single pair | Complete set | Receptor-only, all lineages |
|---|---|---:|---:|---:|---:|---:|
| mouse0088 | 8 / male | 759 | 741 | 399 | 479 | 34 |
| mouse0089 | 8 / female | 650 | 637 | 345 | 396 | 23 |
| mouse0090 | 24 / male | 687 | 665 | 358 | 402 | 34 |
| mouse0091 | 24 / female | 833 | 802 | 407 | 481 | 47 |
| mouse0092 | 48 / male | 838 | 803 | 408 | 483 | 41 |
| mouse0093 | 48 / female | 744 | 726 | 385 | 459 | 39 |
| mouse0094 | 72 / male | 802 | 756 | 399 | 463 | 54 |
| mouse0095 | 72 / female | 733 | 701 | 380 | 421 | 51 |
| mouse0096 | 108 / male | 247 | 244 | 171 | 208 | 31 |

[All cell-level coverage flags](prerequisites/A27_CELL_CHAIN_COVERAGE_V2.tsv), [per-mouse/source-code coverage](prerequisites/A27_MOUSE_STATE_CHAIN_COVERAGE_V2.tsv), [mouse summary](prerequisites/A27_CD8_MOUSE_CHAIN_COVERAGE_V2.tsv), [definitions/input hashes](prerequisites/A27_CHAIN_COVERAGE_MANIFEST_V2.json) and [source-only computation](prerequisites/A27_chain_coverage_v2.py) retain every category. Among the6,293 RNA CD8 cells, source flags include1,933 beta-only,300 alpha-only,40 with no source-annotated productive slot,23 with a nonstandard functionality value and3 with an incomplete productive slot. Some flags overlap; use the cell table's ordered exclusive disposition when partitioning. Productive V/J ambiguity occurs in1,481 cells. No duplicate productive slot record occurred within a cell. Missing or unproductive source records do not establish a receptor's biological absence. These are processed-table representation fractions, not verified assembly success or technical capture efficiency.

## Exact proposed conventions and primary endpoint

Propose the strict **single observed productive alpha/beta pair** as the primary convention, with complete productive-chain sets as a prespecified sensitivity. The primary fixes a comparably observed pair but discards540 otherwise complete multi-slot cells; the sensitivity exposes that selection and additional-chain-detection sensitivity. Choose these conventions before outcomes and retain both even if they disagree. Neither convention identifies an antigen-specific biological lineage with certainty.

A productive slot must have functionality exactly productive, a nonempty A/C/G/T nucleotide junction, and nonempty source-consistent TRA or TRB V/J tokens. Any incomplete productive slot or nonstandard functionality excludes a cell from both conventions, with the reason retained. Empty, no-result, no-rearrangement and explicitly unproductive secondary slots remain distinct flags; one detected productive pair is not proof of one biological receptor pair. Never select the highest-read chain or impute a missing chain.

For a complete slot, retain its uppercase junction and canonical sorted set of the source pipe-delimited V calls and J calls. Do not choose one ambiguous gene call. The single-pair operational key is mouse plus the exact alpha and beta slot records. For the set sensitivity, use mouse plus the sorted unique complete alpha records and sorted unique complete beta records; within-cell duplicate records would collapse, without collapsing distinct chains. Exact source call sets may split otherwise similar junctions when ambiguous assignments differ; nucleotide convergence and incomplete observation also limit lineage interpretation. Amino-acid-only or similarity matching is a different estimand and is not included. No cross-mouse clone is formed.

Proposed endpoint for each convention, mouse and nominal source code is the fraction of unordered distinct eligible cell pairs carrying the same operational receptor key:

`C = sum_k n_k * (n_k - 1) / (N * (N - 1))`.

Also describe the all-source-CD8 eligible pool within each mouse. This pair-collision concentration is a defined captured-cell endpoint; it is not the earlier atlas's depth-five rarefied-diversity estimand, so no exact numerical replication claim follows. A higher C means more repeated operational receptor labels among the observed cells. No frequency table or C has yet been calculated.

## Denominators, support, uncertainty and informative outcomes

Keep all9 source mice and their ages8/24/48/72/108 weeks and sex; do not pool ages or fit an aging effect. The RNA denominator for a code's representation is all6,293 source-labelled RNA CD8 cells split by actual mouse, including labelled GEX-only cells. The receptor-representation numerator is the code's cells with a receptor record; eligibility numerators follow each convention. Within-code concentration uses only eligible cells in that same mouse/code. The354 receptor-only cells have no code and stay outside these denominators. The25 GEX cells without a separate annotation remain visible in whole-GEX missingness and cannot be silently assigned to CD8.

Fix all20 codes from the source annotation and emit the full9x20 grid, including zero support. N<2 gives NA concentration and an explicit unsupported status, never zero. N>=2 permits only the finite observed-pair description; report N, N*(N-1)/2 observed pairs, representation/eligibility fractions and the single-collision resolution2/[N*(N-1)]. This is not a power floor. No p-values, population confidence intervals, age-group means or ranking is proposed. Cell pairs share cells and clones; treating them as independent binomial trials would fabricate precision. Low-support zero collision means no observed repeated key, not biological diversity certainty. Fixed conventions plus coverage tables disclose sampling/selection uncertainty without inventing population inference.

The numerical output would contain nine lineage-level and180 source-code rows per convention, with complete support tables and fixed-order plots showing each mouse's concentration beside source-code representation and eligibility. No dominant-clone selection or source-code pooling is permitted. A pattern retained within well-represented codes across both conventions would nominate a code context for further label qualification. Broad-pool differences with changes in representation but little supported within-code difference would be compatible with redistribution; this is not a formal decomposition, especially with shared keys across codes. Convention-sensitive or unsupported patterns would narrow or leave the question unresolved. Without independently qualified state construction, none of these outcomes establishes biological state redistribution, antigen selection, function or causal aging.

Coordinator review must clear these exact conventions, endpoint and support/uncertainty rules before a numerical contract, freeze or repertoire run. A positive-looking coverage result does not itself authorize that run. No new broad source search is proposed; inaccessible full construction methods and source-version correspondence remain explicit dependent limits.
