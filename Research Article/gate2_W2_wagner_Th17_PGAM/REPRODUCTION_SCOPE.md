# Wp-R01: staged source reproduction

**Status (4 October 2026).** Four stages have run under the governed runner with
verified receipts: [Wp-R0](R0_RESULTS.md), [Wp-R3](R3_RESULTS.md),
[Wp-R1](R1_RESULTS.md) and [Wp-R4](R4_RESULTS.md) (v1 plus a v2 amendment).
**Wp-R2** is open as a labelled version sensitivity only — the solver licence now
works, but the published input (scVI-imputed expression) was never deposited.
**Wp-R5 is closed, not executed:** the owner judged author contact implausible on
4 October 2026 and declined figure digitisation, so the non-RNA panels stay as
cited published evidence.

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

A discrepancy recorded during qualification and not yet reconciled with the
authors: the EAE incidence table (10/12 versus 0/12) gives a two-sided Fisher
p = 6.7e-5 (one-sided 3.4e-5, Barnard 8.4e-6, Boschloo 1.4e-5) against the
published 1.1e-4. Our value is smaller, so the published figure is the more
conservative of the two and the conclusion is unaffected; the test the authors
used is not stated.

## Wp-R1: single-cell reconstruction

Only after Wp-R0. Since the supplementary tables were recovered, the module and
signature definitions are **exact**; what remains substituted is the embedding and
the cell set. Each choice must still be named in the contract before it runs:

1. **Module gene lists — now exact.** Table S1 supplies 116 pro-inflammatory and
   68 pro-regulatory genes with an `is_HVG` flag marking the 63 and 30 the paper
   actually scored. Use the authors' flags rather than recomputing variability on
   a re-derived embedding, and report both the flagged score and a
   locally-recomputed-HVG variant, since the two differ by construction.
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

Partially unblocked. The Gurobi WLS licence was obtained on 4 October 2026 and
verified in the analysis kernel, and Compass 1.0.0 (the authors' own
wagnerlab-berkeley fork, `--optimizer gurobi`) installs and runs. What remains
unmet is the input: the published run used scVI-imputed expression whose model and
matrix are not deposited, so any run here is a **version-and-input sensitivity**,
never the paper's Figure 1. The original three requirements were: a Gurobi WLS licence; a decision
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

## Claim-by-claim outcome, 4 October 2026

| Paper claim | Stage | Outcome |
|---|---|---|
| Deposits support the published design (8 libraries, 2 crossed animals; 79 bulk libraries; 12 human donors) | Wp-R0 | Reproduced, with the suffix-to-library mapping undeclared and the analysed 5,192-cell set not deposited |
| Suffix-to-condition assignment implied by the GEO order | Wp-R1 | Reproduced independently from markers, 8/8 agree |
| Pathogenicity score rises at low glucose through loss of the pro-regulatory arm | Wp-R1 | Reproduced in direction and mechanism, 4/4 animal-paired; cell-level effect small (SMD +0.13 to +0.27) |
| N1 is the least pathogenic programme | Wp-R1 | Reproduced, 12/12 library-metric checks, and again after removing shared marker genes |
| Figure 3D glucose-by-condition genes | Wp-R1 | All 6 directional claims reproduce in sign; no gene survives BH across 10,732; 69 at the paper's p < 0.001 |
| Table S3 bulk EGCG and DHEA contrasts | Wp-R3 | Reproduced on the first-division gate (log2FC r 0.83-0.92); Th17n EGCG materially weaker (recall 0.405) |
| EGCG raises the pathogenic programme in Th17n | Wp-R3 | Single genes yes (IL17A +1.96, IL17F +1.19); at module level **not selective** once the global shift is centred out (Mann-Whitney p = 0.97) |
| DHEA promotes the regulatory programme only in Th17p | Wp-R3 | Partly: the selective shift toward Th17p-associated genes appears in Th17n DHEA (p = 4e-4), not Th17p DHEA (p = 0.22) |
| Both modules up in MS CSF (Fig. S4) | Wp-R4 | **Not reproduced** — every score flat in CSF (BH >= 0.93) |
| Both modules up in MS blood; N1/P1/P4 higher | Wp-R4 | Numerically reproduced for the modules, N1 and P4 (not P1), but **a matched-size random gene set separates the cohorts equally well**, so the effect is a donor-level axis, not the module |
| Compass reaction-level prediction (Fig. 1) | Wp-R2 | Not reproducible as published (input never deposited). As a declared sensitivity ([R2_RESULTS.md](R2_RESULTS.md)) the **sign reproduces** - PGAM forward rho -0.29 against pathogenicity, serine arm -0.26 - but PGAM ranks 11/83 and fails BH, while lactate dehydrogenase reaches rho -0.52 |
| Flow cytometry, 13C labelling, Legendplex, EAE courses, histology | Wp-R5 | Closed; no numeric values deposited |
