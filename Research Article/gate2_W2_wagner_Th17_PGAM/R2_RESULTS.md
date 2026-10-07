# Wp-R2 result: the PGAM sign survives, its distinctiveness does not

**Supersession — 7 October 2026:** the [versioned correction report](CORRECTIONS_2026-10-07.md) owns current Compass and human-score interpretation. The numerical values and conclusions below describe the earlier run and must not be reused as current corrected evidence. Original contracts, scripts, receipts and tables are preserved.

> **Interpretation correction, 7 October 2026:** the current v2 script correlates raw Compass penalties, whose direction is opposite to consistency scores. The claim that the PGAM sign survives is unsupported. See the [artifact audit](../../docs/audits/2026-10-07-pr140/REPORT.md#p1--wp-r2-interprets-penalties-with-the-wrong-direction). Frozen values below are retained; a new governed correction is still required.

**This is a declared version-and-input sensitivity, not a reproduction of
Figure 1.** Contract
[config/compass_sensitivity_v1.json](config/compass_sensitivity_v1.json),
receipt
[analysis/research/runs/wp_compass_sensitivity_v1_rerun/receipt.json](../../analysis/research/runs/wp_compass_sensitivity_v1_rerun/receipt.json),
verified clean. A first attempt under the same contract is not kept: it was
launched with an interpreter in which Compass is not installed, which is a tooling
mistake rather than a scientific result. It completed its own pooling and wrote
`pool_scores.csv`, `pool_expression.tsv` and a `results.json` recording
`status: compass_failed`; the Compass call itself produced only an import
traceback, so no reaction score exists in it.

Compass's own raw reaction matrix (`reactions.tsv`, 97,121 bytes, sha256
`8112f133b2abf814931cab518a98b4b4e7f6ae031b6a2fe943ef62eea1dc7e8d`) is not
tracked in the repository — the run directory keeps the governed analysis outputs
(`reaction_correlations.csv`, `named_reactions.csv`, `pool_scores.csv`) and the
raw matrix is held in the local raw cache as
`wp_compass_sensitivity_v1_rerun_reactions.tsv`. The pooled input matrix
(`pool_expression.tsv`, 7,711,146 bytes) is likewise untracked: it is a run
intermediate rather than a declared output, and it is regenerable from the
contract's inputs - subject to the pooling defect recorded below.

Four deviations from the published run, all unavoidable or host-imposed:

| Deviation | Why | Consequence |
|---|---|---|
| Input is micropooled CP10K counts, not scVI-imputed expression | the fitted scVI model and imputed matrix were never deposited | pooling and imputation are both information sharing but not the same operator; `lambda 0` kept as published |
| Reaction scope restricted to glycolysis/gluconeogenesis and glycine/serine/alanine/threonine metabolism | one solver minute per pool on this host | Figure 1A's ranking over ~900 reactions is **out of scope**; only within-subset position is observable |
| Compass 1.0.0 (authors' wagnerlab-berkeley fork, Gurobi) | the 2025 version is not pinned in the paper | version sensitivity by construction |
| Serial pool shim ([scripts/compass_serial_runner_v1.py](scripts/compass_serial_runner_v1.py)) | this host denies `CreateNamedPipe`, so `multiprocessing.Pool` fails even with `--num-processes 1` | execution-only; same functions, same arguments, same order |

Unit: micropool of about 50 Wp-R1 Th17n cells (60 pools, 3,355 cells, 4
libraries, 2 animals). Pools within a library share the animal and the culture,
so the nominal degrees of freedom of a 60-point correlation overstate the
information and no confidence statement is made.

## The paper's prediction, as far as it can be tested here

83 of the scored reaction directions had non-zero variance across pools.
Spearman correlation with the pool mean pathogenicity score:

| Reaction | Meaning | ρ | p | BH | Rank (most negative first) |
|---|---|---|---|---|---|
| **PGM_pos** | **3PG → 2PG, the PGAM step** | **−0.291** | 0.024 | 0.18 | **11 / 83** |
| PGCD_pos | 3PG → 3-phosphohydroxypyruvate (PHGDH) | −0.258 | 0.046 | 0.18 | 17 |
| PSERT_pos | phosphoserine aminotransferase | −0.258 | 0.046 | 0.18 | 17 |
| PSP_L_pos | phosphoserine phosphatase | −0.258 | 0.046 | 0.18 | 17 |
| PGK_neg | phosphoglycerate kinase, reverse | −0.241 | 0.064 | 0.24 | 18 |
| GHMT2r_pos | serine hydroxymethyltransferase | −0.159 | 0.23 | 0.50 | 24 |
| PGM_neg | 2PG → 3PG | +0.006 | 0.97 | 0.99 | 51 |
| DPGM_pos | diphosphoglycerate mutase | −0.006 | 0.97 | 0.99 | 47 |

**The published sign reproduces.** Under a different Compass version, a different
input and a restricted reaction set, the forward PGAM reaction still correlates
*negatively* with the Th17n pathogenicity score, and so does the whole
3PG→serine arm (PGCD, PSERT, PSP_L) — the paper's two Figure 1 statements about
direction. The reverse direction (PGM_neg) carries no signal, which is what a
flux-direction-specific association should look like.

**Its distinctiveness does not reproduce.** The paper argues PGAM "sets it apart
from other enzymes belonging to the glycolysis pathway". In this restricted set
PGAM is 11th most negative of 83, and the strongest negatives are elsewhere:
lactate dehydrogenase in both directions and the r0173/r0202 lactate reactions at
ρ −0.50 to −0.52 (BH 5 × 10⁻⁴), and threonine dehydratase at −0.54. Only 7
reactions survive BH ≤ 0.05 and PGAM is not among them (BH 0.18). Across all 83
reactions the mean ρ is −0.057 with a spread of 0.21, so PGAM sits beyond the
central tendency but inside the range that several other reactions occupy more
strongly.

Two readings are compatible with this. Either the published reaction ranking
depended on the scVI imputation and the full ~900-reaction model — both missing
here — or the PGAM result is one of several negatively-associated reactions and
was selected for follow-up on grounds the Compass ranking alone does not
establish. This sensitivity cannot distinguish them, and it is not evidence
against the paper's biology: the EGCG, sgRNA and EAE experiments are independent
of the Compass step entirely.

PGAM's Compass score does **not** correlate with the Table S3 EGCG signature
score across pools (ρ = 0.075 on the HVG-restricted version, 0.207 on the full
gene set), which is worth noting next to the Wp-R1 finding that the EGCG
signature and the pathogenicity score are themselves strongly correlated.

## Bearing on Wp-P02

The serine arm reproduces with the paper's sign: 3PG→serine reactions are
*negatively* associated with pathogenicity, i.e. aligned with the pro-regulatory
side. Godfrey et al. 2025 report the opposite causal direction in Tregs, where
PGAM inhibition suppresses regulatory character *through* 3PG-derived serine and
one-carbon metabolism. The conflict therefore survives this run intact, now with
both a transcript-level result (Wp-R3: all serine and one-carbon genes fall under
EGCG) and a reaction-level one (here: the serine arm tracks the regulatory side)
that are consistent with each other and still cannot resolve the direction,
because neither measures flux. The discriminating experiment named on
[the branch card](branches/P02_serine_one_carbon_direction.md) is unchanged.

## Known defect in this run's reproducibility

The micropools are not bit-reproducible across environments. The k-means seed is
fixed, but the preceding truncated SVD (`scipy.sparse.linalg.svds`) is started
from an unseeded random vector, so pool membership can differ between BLAS
builds — the preserved failed run and this run produced `pool_expression.tsv`
files of 7,711,383 and 7,711,146 bytes from the same seed. The fix is to pass an
explicit `v0` to `svds`; it is recorded here rather than applied silently,
because the code hash is bound to this receipt. Any future rerun of this contract
should be treated as a *new* sampling of pools, not a replication of these
numbers.

### Resolved 6 October 2026 — and the v1 numbers are vindicated

The defect was measured rather than assumed. Three repeats of the v1 pooling
code: **one of two repeat pairs differed**, at adjusted Rand 0.989 against an
identical count of 146 eligible pools, so the unseeded start moves a handful of
cells between micropools rather than reorganising them. Three repeats with a
fixed constant unit start vector were bit-identical.

`compass_sensitivity_v2`
([config](config/compass_sensitivity_v2.json) ·
[receipt](../../analysis/research/runs/wp_compass_sensitivity_v2_rerun/receipt.json),
`verify` clean) passes that start vector and changes nothing else — same seed,
pool size, eligibility floor, pool target, reaction scope, Compass 1.0.0
wagnerlab-berkeley fork and Gurobi.

**v2 reproduces v1 exactly.** All 83 reactions across all 16 numeric columns
agree to 0.000 × 10⁰, and the 60 scored pool identifiers are the same set. PGAM
(`PGM_pos`) is ρ −0.2912, p 0.0240, BH 0.1808, rank 11 of 83 in both.

Two consequences, and the second matters more:

1. The caution above — treat any rerun as a new sampling of pools — **no longer
   applies**. The contract is re-derivable, and these numbers have now been
   independently re-derived rather than merely re-asserted.
2. The v1 run happened to land on the same pooling the seeded code reaches, so
   **the defect never affected the reported values**. That is luck, not design:
   the probe shows a different draw was available, and a reader on a different
   BLAS build had no way to know which they would get. The fix converts a number
   that was right by chance into one that is right by construction.

v1's run and receipt are preserved. v2 supersedes it for reporting only; no
Wp-R2 conclusion changes, because no value did.

## Limits

- Pools are not independent replicates; the correlation describes this deposit.
- Reaction scope is 2 of the model's subsystems, so no statement about the
  published ranking is possible.
- Compass scores are reaction-level model outputs from RNA, not flux
  measurements.
- Two animals; nothing here is animal-level inference.
- The 60 pools are a seed-fixed stratified subsample of 146 eligible pools, taken
  for runtime, not for an outcome.
