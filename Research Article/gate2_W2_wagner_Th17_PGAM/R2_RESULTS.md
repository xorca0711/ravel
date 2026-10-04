# Wp-R2 result: the PGAM sign survives, its distinctiveness does not

**This is a declared version-and-input sensitivity, not a reproduction of
Figure 1.** Contract
[config/compass_sensitivity_v1.json](config/compass_sensitivity_v1.json),
receipt
[analysis/research/runs/wp_compass_sensitivity_v1_rerun/receipt.json](../../analysis/research/runs/wp_compass_sensitivity_v1_rerun/receipt.json),
verified clean. A first attempt under the same contract failed immediately and is
not kept: it was launched with an interpreter in which Compass is not installed,
which is a tooling mistake rather than a scientific result. Its only content was
an import traceback.

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
| PGM_neg | 2PG → 3PG | −0.006 | 0.97 | 0.99 | 51 |
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

## Limits

- Pools are not independent replicates; the correlation describes this deposit.
- Reaction scope is 2 of the model's subsystems, so no statement about the
  published ranking is possible.
- Compass scores are reaction-level model outputs from RNA, not flux
  measurements.
- Two animals; nothing here is animal-level inference.
- The 60 pools are a seed-fixed stratified subsample of 146 eligible pools, taken
  for runtime, not for an outcome.
