# Wp-R01: staged source reproduction

**Status:** [Wp-R0 executed 4 October 2026](R0_RESULTS.md) under the governed
runner, with a verified receipt. Wp-R1 to Wp-R5 are specified here and have no
contract yet; Wp-R0's result decided which of them may open.

**Decision this ladder serves:** which of the paper's findings can be
reconstructed from what was deposited, at which evidential level, before any of
its biological interpretation is extended.

**Strongest rival to apparent success:** a reconstruction that looks like the
published figure because both are driven by the same dominant axis — activation,
proliferation or library depth — while the specific reaction-level and
program-level claims are not reproduced at all. **Units:** animals and donors
for inferential contrasts; cells, libraries and genes are nested measurements.
**Interpretation limit:** this is reanalysis of the source's own data. Agreement
is reproduction, never independent replication.

## Wp-R0: source and design qualification

Verify the deposited records and matrix headers against recorded hashes;
inventory samples, animal labels, aggregation suffixes, bulk design cells, the
TPM column join and the human donor map; decide per-stage eligibility. No
expression value is read.

**Completion:** a hash-verified manifest, one-to-one joins where they exist, an
explicit `unresolved` marker where they do not, and a stage eligibility table.
Entrypoint [scripts/qualify_sources_v1.py](scripts/qualify_sources_v1.py),
contract [config/source_qualification_v1.json](config/source_qualification_v1.json).
**Done:** see the [result](R0_RESULTS.md) and its
[receipt](../../analysis/research/runs/wp_source_qualification_v1/receipt.json).

## Wp-R1: single-cell reconstruction

Only after Wp-R0. This stage is a **reconstruction with declared substitutions**,
and each must be named in the contract before it runs:

1. **Module gene lists.** Table S1 is unavailable, so the pro-inflammatory and
   pro-regulatory modules come from the cited 2015 source (Gaublomme et al.,
   Figure 4B). Record how many genes are recovered and how many survive the
   paper's highly-variable-gene restriction, which reduced 116 and 68 published
   genes to the 63 and 30 actually scored.
2. **Score direction.** Fix the sign to pro-inflammatory minus pro-regulatory,
   matching the Results text and figure behaviour, and record that the Methods
   sentence states the opposite.
3. **Condition labels.** Derive them from markers as specified in
   [Datasets](DATASETS.md#single-cell-aggregation-order-is-the-binding-unknown);
   report the assumed `aggr` order and whether the data agree with it.
4. **Embedding.** The paper used 1,429 HVGs, a 30-dimension scVI latent space
   with animal and cell-cycle phase as nuisance covariates, phase regressed out,
   an SNN graph and Leiden resolution 0.8 with a documented exclusion of three
   clusters. Re-deriving this yields *different* cells, clusters and numbers,
   because the final 5,192-cell set and its exclusions are not deposited.

Products: the arm-wise pathogenicity-score decomposition across glucose and
differentiation conditions, the metabolic-transcript fraction, a re-derived
cluster set mapped to N1–N3/P1–P4 by marker concordance, and the glucose-by-condition
interaction gene list. Every panel is classified as reproduced, qualitatively
concordant, discordant or not assessable. Cell-wise p values are reported as
library-level descriptions, not animal-level inference.

## Wp-R2: Compass reaction scores

Held. Three requirements, all currently unmet: a Gurobi WLS licence; a decision
on the imputed input, since the published run used scVI-normalised imputed
expression with `lambda 0` and no meta-reactions, and neither the model nor the
imputed matrix is deposited; and a bounded smoke run under its own frozen
contract before any full run. A modern Compass version is a declared sensitivity,
not the paper's run. Nothing in Wp-R1 depends on this stage.

## Wp-R3: bulk EGCG and DHEA contrasts

Eligible descriptively now. Use the 79-library TPM matrix with the library as the
unit. Fit within each cell type and gating arm: EGCG versus DMSO, DHEA versus
methanol, and the DMSO Th17p-versus-Th17n partition that defines the three gene
groups (BH ≤ 0.05 and |log2 FC| ≥ 1.5). Derive the EGCG and DHEA response
signatures with the published thresholds (|log FC| ≥ log2 1.5, BH ≤ 0.05).

Scale discipline: TPM is not counts, so use a method valid for continuous
normalised values (log2 TPM with limma-trend, or a rank method) and say which.
Do not round TPM into a count model. Division arms are different populations;
contrasts stay within an arm. Report the gene-group logFC distributions as
distributions with per-gene points available, not as summary bars.

## Wp-R4: human donor-level transport

Eligible descriptively. Rebuild CD4 pseudobulk per donor and tissue from
`GSE138266_RAW.tar`, using the 12 recovered donor codes, and test the module
scores, the EGCG signature and the program signatures across disease within
tissue, paired where both tissues exist. Because the published analysis found
*both* modules elevated in MS, a generalised activation score must enter the same
model as a competing explanation; without it, a module difference cannot be
attributed to the Th17 axis. Signatures derived in Wp-R1/R3 are exposed, so this
is transport of an exposed signature, not validation.

## Wp-R5: non-RNA panels

Not reproducible. No numeric values are deposited for flow cytometry, 13C
labelling, Legendplex, EAE courses or histology. These panels are cited as
published evidence only. If the owner later authorises digitisation, it is a
separate approximate reconstruction with stated extraction uncertainty and is
never described as raw data.

## Completion and failure reporting

Each stage reports per-panel outcome (exact-input reproduction, processed-output
reproduction, qualitative concordance, discordant, unavailable), its biological
unit, and what the result would and would not license. Stages may complete with a
hold. The paper is not "reproduced" because Wp-R0 and Wp-R3 run; the Compass
prediction that motivates the whole study sits in the one stage that is blocked.
