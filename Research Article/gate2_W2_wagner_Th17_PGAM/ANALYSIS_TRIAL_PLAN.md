# Execution structure and next handoff

**Current execution and interpretation — 7 October 2026:** see [corrections](CORRECTIONS_2026-10-07.md) and [the current README](README.md). Dated stage plans, intake states and derivation counts below remain historical. A28–A30 are now registered; the full portfolio is A0–A30.

**Current state, 4 October 2026:** structuring complete and [Wp-R0 executed](R0_RESULTS.md)
under the governed runner, with its contract, receipt and the six branch owners
registered. The registered owner for source reproduction is **Wp-R01**; branch
owners are **Wp-P01** to **Wp-P06**. Steps 1 and 2 below are therefore done; they
are retained because they are the prerequisites every later stage repeats.

Planned filenames in this document are not existing artifacts.

| Stage | Dependency and decision | Planned output under a new immutable run |
|---|---|---|
| Wp-R0 metadata | Recorded GEO records and matrix headers; decides which later stage may open | Sample and library inventory, aggregation-suffix table, bulk column join, human donor map, stage eligibility |
| Wp-R1 single cell | Wp-R0; needs the count matrix and substituted module lists | Score decomposition by arm and condition, metabolic fraction, re-derived programs with marker-concordance mapping, interaction gene list, panel-by-panel concordance report |
| Wp-R2 Compass | Solver licence plus an imputation decision; independent of R1 results | Reaction penalties and scores with version differences, correlation ranking, solver logs |
| Wp-R3 bulk | Wp-R0; independent of R1 and R2 | Within-arm treatment contrasts, three-group logFC distributions, re-derived EGCG and DHEA signatures |
| Wp-R4 human | Wp-R0 and the signatures from R1/R3; needs `GSE138266_RAW.tar` | Donor-level pseudobulk scores by tissue and disease, with an activation score in the same model |
| Wp-R5 other assays | Author-supplied numeric values | Currently nothing; explicit unreproduced-panel list |
| Wp-P01…P06 | Branch-specific eligibility after the stages they depend on | Bounded hypothesis and rival report, including null, discordant and held outcomes |

## Before the first substantive run

1. Add **Wp-R01** and **Wp-P01** to **Wp-P06** to `article_candidates` and the
   Wp-R0 contract path to `contracts` in
   [the registry](../../analysis/research/registry.json). Both are prerequisites,
   not bookkeeping: `contract_errors` rejects an unregistered owner with
   "Unknown question/candidate owner", and `execute` refuses with "Execution
   requires a registered contract".
2. Freeze [config/source_qualification_v1.json](config/source_qualification_v1.json)
   (`status: frozen`), commit it with the hash-bound entrypoint, then
   `research_gate.py preflight … --inputs`, `run --run-id wp_source_qualification_v1`
   and `verify`, and register the receipt. The run needs a checkout where `git`
   is available and `raw_data/wagner_pgam_w2_20261004/` is present with the
   recorded hashes.
3. For Wp-R1 and Wp-R3, freeze the substitutions *before* execution: module gene
   source and recovered-gene count, score sign, label-derivation rule, embedding
   settings, TPM-appropriate method, gene-group thresholds, multiplicity family
   and the stop rule. These are reconstructions of exposed results; the exposure
   record says so explicitly and a later freeze does not undo it.
4. Wp-R4 needs its own acquisition manifest for the human deposit and a frozen
   definition of CD4 identity, pseudobulk inclusion (minimum cells per donor and
   tissue) and the activation score, all fixed before the disease contrast is seen.

## Efficient order

Wp-R0 then Wp-R3 is the smallest reviewable result: both are eligible now, and
Wp-R3 produces the signature definitions that Wp-R1 and Wp-R4 consume. Wp-R1
needs the count matrix download and the substituted module lists, so it comes
third. Wp-R4 is last among the reproduction stages because it depends on R1/R3
signatures. Wp-R2 opens only when a solver licence exists and does not block
anything else.

Among the branches, [Wp-P02](branches/P02_serine_one_carbon_direction.md) is the
one that can change a scientific conclusion, because it tests a direction the
source and an independent 2025 study disagree about. It is deliberately not
ranked above the others as a decision; it is identified as the highest-information
candidate.

## Exact next action

Freeze and execute **Wp-R3**. It is eligible now, needs no further download, and
produces the EGCG and DHEA signature definitions that Wp-R1 and Wp-R4 consume, so
running it later would mean running those twice. The five supplementary tables
were recovered on 4 October 2026, so its contract binds the authors' own Table S1
and S3 definitions rather than substitutions, and the re-derived signatures can be
compared gene-for-gene against Table S3.

Wp-R1 follows, and needs the single-cell count matrix downloaded and hashed under
a new acquisition manifest. Do not start it before deciding the label-derivation
rule, because the condition labels every single-cell endpoint depends on are the
one thing Wp-R0 could not resolve.

**Known external blockers:** no Gurobi licence (Wp-R2); no numeric assay data
(Wp-R5); no animal field in the bulk deposit, and only two animals in the
single-cell deposit even though they are crossed with every condition, so no
stage can reach population inference from the mouse data. None of these is
resolvable by more analysis. The supplementary-table hold is **closed**: all five
were recovered from the NIH PMC Cloud open-data package.

**What the reproduction ladder is and is not for.** Wp-R0 to Wp-R5 re-derive the
source's own results and freeze its definitions; agreement is reproduction of one
evidence lineage, never independent support. The analyses that could add something
are the branch cards, and they consume these stages' outputs: Wp-P01 and Wp-P03
need Wp-R1's score arms and programme labels, Wp-P02's first arm needs the same,
and Wp-P05 needs Wp-R3's signatures. That dependency, not reproduction for its own
sake, is why the ladder runs first — and the minimum that unlocks all four is
Wp-R3 then Wp-R1.
