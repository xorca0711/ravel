# Dp1-AM01: result-guided descriptive and chromatin route

7 November 2026; prospective before S3 computation. Supersedes only the exact
reference-replay requirement for the adapted S3 branch in
[version-1 plan](ANALYSIS_PLAN.md#dp1-s3--ask-which-regulation-is-disrupted).
The original comparison, unavailable exact-replay branch and all outcomes remain.
No governance or interpretation boundary is relaxed.

S0 qualifies per-library FPKM, not count/population inference. S1/S2 show modest
global low-state divergence that is sensitive to sparse preparations. S2 therefore
instantiates the plan's descriptive fallback. Its mixed result is preserved;
no sample is deleted or significance threshold introduced.

The 2015 supplement and exact Gavin/Hill/Samstein selection remain unrecovered.
However, Arvey's complete primary text, Table 6 and GEO assay/processing README
are now recovered. The latter supplies **explicitly log2(RPKM+0.3), quantile-
normalized H3K27me3 signal**, with named activated/resting Treg columns. This
is preferable for an adapted association to guessing the supplement's transform.
Do not log-transform it again, mix it with DuPage FPKM, or interpret it as global
methylation abundance. The Arvey context is Treg activation after DT-induced
inflammation, not DuPage healthy mosaic CD62L sorting or an Ezh2 KO chromatin assay.

**New S3 implementation:** retain the entire fixed S1 universe; separate HET
activation-down and activation-up classes while explicitly recording mathematical
coupling to the interaction. Use the external activated-minus-resting H3K27me3
signal to ask whether signed RNA interactions align with local chromatin context.
Map mm9 domains to mm9 RefGene transcript-body overlaps, collapse duplicate
transcripts to gene/domain pairs, and join exact same-chromosome mouse symbols
to qualified DuPage features. No coordinate is joined across mm9 and mm10.
The pinned annotation is a later UCSC dump, not the original authors' mapping.
Domains can overlap multiple genes; use a median over domains per gene and retain
counts/edges. Show the single-gene-domain subset as a mapping sensitivity, not
as a post-hoc replacement. Exclude boundary-sensitive pairs under the two
plausible start-coordinate conventions; do not assert a convention absent from
the table. Retain all uncovered genes as uncovered, never unmarked or zero.

Report descriptive continuous associations, positive/nonpositive chromatin-signal
groups, and expression-stratified summaries (five equal-count bins of HET/high
mean log expression). These are coverage/detectability checks, not causal
adjustment or independent-gene significance tests. No p-values, enrichments or
specific winning target are selected. Exact Foxp3-loss/binding/signature replay
remains held; no replacement gene list will be labelled as the published list.

Positive association could support locus-associated consistency only; weak or
discordant results weaken a general repression account. Broad multi-gene-domain
mapping, sample selection and indirect regulation remain alternatives in either
case. S4 requires a specific unresolved discriminator beyond an already published
broad loss/gain comparison; if S3 does not supply one, record S4 as not informative
and continue to S5's endpoint map.

Source version/access, hashes and exact methods are frozen in the
[S3 contract](contracts/Dp1.S3.regulatory_context_v1.json). This is initial S3
numerical execution under a plan amendment, not a revised run of S2. Prior outcome
exposure includes the published papers, S0–S2 and source headers/README.
