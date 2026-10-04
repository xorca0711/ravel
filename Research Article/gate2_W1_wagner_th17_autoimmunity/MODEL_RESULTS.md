# Source-aligned bulk RNA results — 4 October 2026

The animal-blocked RNA reconstruction has executed and passed independent
arithmetic checks. It supplements the [initial paired CPM analysis](BULK_RESULTS.md).
It is **outcome-exposed, source-aligned reanalysis**, not an exact reconstruction
of the authors' undisclosed implementation or independent biological replication.
The complete pre-RQ disposition is in [PRE_RQ_EVIDENCE.md](PRE_RQ_EVIDENCE.md).

## Question and design

Wg-R01 asks which published treatment/program patterns and direct
genotype-by-treatment differences can be reconstructed before developing new
questions. The strongest rival to a within-cell lineage interpretation remains
selection, proliferation, survival or changing bulk composition. The measured
endpoint is relative bulk RNA abundance, not tracked conversion or function.

[Wagner 2021, STAR Methods and Figure 6](https://pmc.ncbi.nlm.nih.gov/articles/PMC8621950/)
uses limma-trend or voom and source thresholds of BH q ≤ 0.05 and absolute fold
change ≥ 1.5. Its exact filtering, trend/voom choice, design and genotype pooling
are not fully specified. S4–S6 were located but valid workbook bytes were not
retrieved; no numerical concordance with these tables is claimed.

| Experiment | Qualified units and conditions | Model |
|---|---|---|
| GSE162300 (A) | Three WT animal labels; 18 cultures across Th17p, Th17n and iTreg, vehicle/DFMO; two technical sequencing runs per library summed | Animal effects, lineage baselines and lineage-specific DFMO responses; rank 8, residual df 10 |
| GSE162382 (B) | Four WT and three JMJD3 conditional-KO labels; 28 cultures across Th17n and iTreg, control/DFMO; no Th17p | Animal effects, genotype-specific lineage baselines and four treatment responses; rank 13, residual df 15 |

RNA was collected at 68 hours. Animal labels are verified against source
metadata, but physical specimen independence is not independently audited.
No labels are paired across studies. Genotype main effects are absorbed by
animal effects; the within-animal treatment-by-genotype contrast is estimable.

## Frozen methods

[Contract](config/bulk_limma_v1.json), frozen with both scripts at **5a50fb8**;
[receipt](../../analysis/research/runs/wg_bulk_limma_v1/receipt.json).
R 4.6.1, limma 3.68.5 and edgeR 4.10.5 are recorded in the
[runtime record](../../analysis/research/runs/wg_bulk_limma_v1/R_session.txt).

- Retain genes with unnormalized deposited-gene CPM ≥ 1 in at least three
  libraries per series. No samples are excluded. Recompute library totals after
  filtering, apply TMM normalization and default voom precision weights.
- Fit animal-blocked models. Reparameterize each contrast with `contrastAsCoef`
  before `lmFit` and empirical Bayes moderation, so weighted contrast standard
  errors are exact for the declared design. No outcome-driven model selection.
- BH correction spans all retained genes **within each of 16 contrasts**.
  Source DEG classification additionally requires |log2FC| ≥ log2(1.5).
  Conditional 95% model intervals are not simultaneous or FDR-adjusted intervals.
- A-study primary Th17/Treg programs use equally weighted Th17p/n versus iTreg
  vehicle contrasts. The fixed sensitivity uses Th17n alone. B-study primary
  programs equally weight WT/KO vehicle lineage contrasts; the fixed sensitivity
  uses WT alone. This explicit choice does not establish the authors' pooling.
- A-study PCA uses the union of baseline pairwise lineage DE sets, centered
  voom log-CPM without gene variance scaling. Program CDFs count genes; they do
  not use genes as independent animals or provide population-level p values.

All genes, contrasts, program assignments, sensitivities and animal-level program
responses are retained in the [run directory](../../analysis/research/runs/wg_bulk_limma_v1).
Shared vehicle measurements select the programs and contribute to later DFMO
contrasts; those summaries are therefore dependent descriptions.

## Results

| Quantity | A: GSE162300 | B: GSE162382 |
|---|---:|---:|
| Deposited genes | 20,817 | 20,891 |
| Genes retained for modelling | 11,512 | 12,668 |
| Primary Th17 program | 1,159 | 1,743 |
| Primary Treg program | 1,301 | 1,397 |
| Genes changing program category under the fixed sensitivity | 1,150 | 1,034 |

These counts come from the [model summary](../../analysis/research/runs/wg_bulk_limma_v1/model_summary.json).
The sizable program-definition sensitivity is retained. The A-study baseline
PCA selects **3,879 genes**, versus **3,414** in the paper. No threshold was
adjusted to recover the published count. Its PC1/PC2 explain **45.1%/17.7%**
of variance in the selected transformed genes; this differs from the all-gene
CPM PCA in Figure 4.

The [contrast table](../../analysis/research/runs/wg_bulk_limma_v1/contrast_summary.tsv)
contains all source-threshold calls:

| DFMO contrast | Higher RNA | Lower RNA |
|---|---:|---:|
| A, Th17n WT | 1,596 | 2,018 |
| A, Th17p WT | 877 | 1,445 |
| A, iTreg WT | 929 | 1,779 |
| B, Th17n WT | 1,807 | 2,072 |
| B, Th17n KO | 1,816 | 1,942 |
| B, iTreg WT | 1,558 | 1,805 |
| B, iTreg KO | 1,325 | 1,525 |

Figure 6 shows the same-data Th17n program distributions: the reconstructed Th17
program shifts toward lower RNA and the Treg program toward higher RNA under
DFMO in both studies, including the KO condition. This supports an aggregate
RNA pattern in these source cultures. It does not show cell conversion or
independence of all RNA effects from JMJD3.

The **direct KO-minus-WT treatment interaction**, rather than a comparison of
two significance labels, has 6 positive/52 negative source-threshold genes in
Th17n and 3 positive/39 negative genes in iTreg. All results are retained.
None of the twelve previously specified display genes meets q ≤ 0.05 for either
interaction. This is not an equivalence result.

For example, the Th17n Foxp3 interaction is **+0.508 log2 units**,
95% conditional interval **−0.453 to +1.469**, q **0.820**. The iTreg Foxp3
interaction is **+0.485**, interval **+0.145 to +0.826**, q **0.228**.
An unadjusted interval can exclude zero while the all-gene BH decision does not.
The [complete prespecified-gene table](../../analysis/research/runs/wg_bulk_limma_v1/prespecified_gene_models.tsv)
also retains the broad iTreg Il17a interval and other unfavorable/uncertain estimates.
Gene-level Kdm6b abundance does not validate deletion of its functional exon.

## Verification and interpretation

[Independent checks](../../analysis/research/runs/wg_bulk_limma_v1/verification.json)
solve weighted normal equations in Python for 113 predetermined genes in each
series, across every contrast. Maximum coefficient/SE errors are
6.04e-14/1.15e-14. Independent all-gene t-tail, BH and interval arithmetic passes
the frozen tolerances. Empirical Bayes priors and voom weights remain limma
estimates; arithmetic agreement is not biological replication.

Both new plates were visually inspected; PNG, vector PDF/SVG and a
[combined PDF](../../analysis/research/runs/wg_bulk_limma_v1/Wagner_R3_limma_figures.pdf)
are saved. The [gallery](FIGURES.md#figure-6-source-aligned-rna-programs)
defines every axis, sample condition and statistical symbol.

Wg-P03 now has model-based aggregate RNA evidence but its selection/conversion
rival remains unresolved. Wg-P04 now has direct RNA interactions; the source
120-hour protein/function observations are a different endpoint from these
68-hour measurements. No universal mediation, suppressive function, durable
lineage or lung mechanism follows. No branch is accepted/rejected and no new
RQ or claim grade is created.
