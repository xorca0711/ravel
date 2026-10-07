# Wp-R1 result: the single-cell claims, re-derived from the only deposited matrix

Executed 4 October 2026 under the governed runner. Contract
[config/singlecell_reproduction_v1.json](config/singlecell_reproduction_v1.json),
script [scripts/singlecell_reproduction_v1.py](scripts/singlecell_reproduction_v1.py),
receipt [analysis/research/runs/wp_singlecell_reproduction_v1/receipt.json](../../analysis/research/runs/wp_singlecell_reproduction_v1/receipt.json).
`verify` returned `{"ok": true, "errors": []}`.

**Unit.** 8 libraries nested in 2 animals, with the animals crossed over all four
cell type × glucose conditions, so an animal-paired difference exists at *n* = 2
and is reported as four paired values without a p value. Cells are nested in
libraries; no cell-wise p value is treated as population inference. The paper's
analysed 5,192-cell set and its scVI model were never deposited, so cell
membership necessarily differs: 15,830 of 19,203 barcodes pass our QC.

## 1. The undeclared library-to-condition mapping is recoverable

GSE289733 deposits one aggregated matrix with eight suffixes and never says which
suffix is which library (Wp-R0). Deriving the labels from the data rather than
trusting the GEO order:

- cell type from a Th17p-minus-Th17n marker contrast on library pseudobulk:
  Th17n libraries −3.33 to −3.77, Th17p libraries +1.54 to +1.91 — a gap with no
  intermediate case;
- glucose from TXNIP, the canonical glucose-induced transcript: between-group gap
  1.91 log2 CPM in Th17n and 3.80 in Th17p, against a within-group spread of at
  most 0.52.

**All eight derived labels agree with the GEO sample order.** The order is
therefore usable, and this is the first result that licenses any downstream
analysis of this deposit. Animal identity cannot be derived from expression and
is carried as prior-only throughout.

Per-library QC: 1,239–2,404 cells retained of 1,595–2,890 barcodes, median
3,098–3,709 genes, median mitochondrial fraction 1.3–2.2 %.

## 2. The pathogenicity score rises at low glucose, and the pro-regulatory arm is why

Animal-paired low-minus-high glucose differences in library mean score
(1 mM − 25 mM), authors' Table S1 HVG gene sets:

| Cell type | Animal | Pro-inflammatory | Pro-regulatory | Pathogenicity | Proliferation |
|---|---|---|---|---|---|
| Th17n | Mo1 | −0.053 | **−0.187** | **+0.133** | −0.611 |
| Th17n | Mo2 | +0.020 | **−0.089** | **+0.109** | −0.637 |
| Th17p | Mo1 | −0.132 | **−0.175** | **+0.044** | −0.641 |
| Th17p | Mo2 | −0.093 | **−0.152** | **+0.059** | −0.521 |

The pathogenicity difference is positive in 4/4 animal × cell-type pairs, and in
all four the pro-regulatory arm falls at low glucose while the pro-inflammatory
arm does not rise (it falls in three of four). **This reproduces both the paper's
direction and its stated mechanism — the score moves because the regulatory arm
is lost, not because the inflammatory arm is gained.** Cell-level standardised
mean differences are small, +0.13 to +0.27 for pathogenicity against −0.29 to
−0.79 for the pro-regulatory arm, which is worth stating next to the published
two-sample t test p < 10⁻³³: that p value reflects thousands of cells, not a
large per-cell separation.

Proliferation is *higher* at 25 mM in all four pairs (difference −0.52 to −0.64),
so the pathogenicity shift runs opposite to the proliferation shift rather than
with it. Within libraries, the pathogenicity score correlates weakly and
negatively with the proliferation score (Spearman −0.02 to −0.17) and weakly with
sequencing depth (|ρ| ≤ 0.13). Both readings are post-hoc readouts of the
governed cell-level output, flagged as such. They weaken, but do not eliminate,
the rival that the score tracks growth or depth: the cell-cycle structure the
paper regressed out was removed from our analysis by neither of us, and no
protein or functional measurement is involved.

## 3. N1 is the least pathogenic programme, and not because of gene overlap

Assigning each cell to the programme whose Table S5 markers it scores highest
within its derived cell type, N1 has the lowest median pathogenicity score **and**
the lowest median EGCG-signature score in every Th17n library — 12 of 12 library ×
metric checks, and again 12 of 12 after removing every marker gene shared with
Table S1 or with the EGCG signature (N1 median pathogenicity −0.36 to −0.52
against a next-lowest programme of −0.03 to +0.19). Programme assignment agrees
with the all-marker version for 86.2 % of cells after that removal, so the
ordering is not an artefact of shared genes.

The programme *composition* is strongly glucose-dependent (in Th17n, N2 is
58–65 % of cells at 1 mM and 1–5 % at 25 mM, with N1 and N3 taking its place),
but our programme labels come from marker scoring, not from the authors'
clustering, so composition is not comparable to their figure and is reported
descriptively only.

## 4. Figure 3D interaction genes

Glucose-by-cell-type interaction on library pseudobulk with animal as a
covariate (3 residual df), 10,732 genes at 1 CPM in at least half the libraries.
All ten genes the paper names are present and every stated direction reproduces:

| Cell type | Paper's claim | Gene | 25 mM − 1 mM | p (interaction) | Median library CPM |
|---|---|---|---|---|---|
| Th17p | up with glucose | TBX21 | +1.21 | 0.034 | 5.9 |
| Th17p | up with glucose | CCL5 | +3.74 | 0.048 | 5.5 |
| Th17p | up with glucose | IL23R | +1.77 | 0.026 | 1.6 |
| Th17p | up with glucose | IL22 | +1.45 | 0.62 | 51.3 |
| Th17p | down with glucose | CSF2 | −0.63 | 1.0 × 10⁻⁵ | 20.9 |
| Th17p | down with glucose | GZMB | −1.67 | 0.28 | 13.3 |
| Th17n | glucose-sensitive | FOXP3 | +1.31 | 0.044 | 2.3 |
| Th17n | glucose-sensitive | CTLA4 | +0.43 | 0.74 | 287 |
| Th17n | glucose-sensitive | IL2RA | +0.62 | 0.44 | 599 |
| Th17n | glucose-sensitive | TSC22D3 | −0.81 | 0.0053 | 29 |

6/6 of the directional claims (the Th17p genes) reproduce in sign. No gene
survives BH ≤ 0.05 across 10,732 genes; 69 reach the paper's unadjusted
p < 0.001. With two animals and 3 residual degrees of freedom that is the
expected ceiling, and it means the Figure 3D gene list is a description of these
two animals, not an estimated gene set.

Our first dry run used a 10 CPM floor and silently dropped TBX21, CCL5, IL23R and
FOXP3 — the four lowest-expressed genes in the list. The floor was lowered to
1 CPM on principle before freezing, and the per-gene median CPM is now an output
column so any future exclusion is visible. This is recorded in the contract's
exposure record.

### 4a. What the expression floor costs and buys

Because that floor was chosen *knowing* which genes a higher one removes, it was
swept across its whole range under its own contract
([config](config/r1_floor_sensitivity_v1.json) ·
[receipt](../../analysis/research/runs/wp_r1_floor_sensitivity_v1/receipt.json),
`verify` clean). The sweep reproduces the table above at the frozen floor to
6 × 10⁻¹⁷.

**The floor changes nothing about any individual gene.** Every per-gene effect
and raw interaction p is *exactly* floor-invariant — maximum drift 0.0 across
seven floors, asserted by the run, which fails if it is not. The floor's entire
influence is which genes are testable and how large the multiplicity correction
is:

| Floor (CPM) | Genes tested | p < 0.001 | BH ≤ 0.05 | Named genes lost |
|---|---|---|---|---|
| 0 | 18,500 | 163 | **18** | — |
| 0.5 | 11,492 | 73 | 0 | — |
| **1 (frozen)** | **10,732** | **69** | **0** | **—** |
| 2 | 9,960 | 64 | 0 | — |
| 5 | 8,678 | 58 | 0 | FOXP3, IL23R |
| 10 | 7,226 | 52 | 0 | + CCL5, TBX21 |
| 20 | 5,374 | 40 | 0 | + CCL5, TBX21 |

Two things follow, in opposite directions.

**Raising the floor erases the reproduction without touching the data.** At
5 CPM two of the ten named genes become untestable and at 10 CPM four do. A run
at 10 CPM would have reported 6 of 10 genes "not expressed" and the Figure 3D
reproduction as 60 % complete, when the four missing genes are present,
directionally correct, and simply below an arbitrary line. No gene ever changes
*direction* with the floor, which distinguishes this from a genuinely unstable
estimate.

**Removing the floor manufactures significance.** At floor 0 the universe grows
by 7,768 genes and **18 cross BH ≤ 0.05, of which 16 are never detected at 1 CPM
in any of the eight libraries** (median library CPM exactly 0.000 — mostly `Gm*`
predicted loci). With four residual degrees of freedom their residual variance
is numerically zero, so their p values are zero to floating point. Their mass of
near-zero p values then makes BH less conservative for everything else, dragging
the two genuinely expressed genes in the list across the threshold: CSF2 from
BH 0.112 at the frozen floor to 0.011, and MYO1C to 0.041.

So the honest statement about §4 is not "no gene survives BH correction" but
**"no gene survives BH correction at any defensible floor, and the only
configuration that produces hits is the one that admits undetected genes."** The
full list is in
[`unfiltered_bh_hits.csv`](../../analysis/research/runs/wp_r1_floor_sensitivity_v1/unfiltered_bh_hits.csv).
The frozen 1 CPM floor is retained; no new floor is nominated and no Wp-R1 value
is revised.

## 5. Is the EGCG signature just the pathogenicity score?

Within Th17n cells, the Table S3 Th17n-EGCG signature score correlates with the
pathogenicity score at Pearson 0.66 (Spearman 0.68) pooled, 0.63–0.73 per
library; the DHEA signature much less (0.19–0.33). Removing the 43 of 395 scored
EGCG-signature genes that also sit in Table S1 lowers the correlation only to
0.54. The secondary signature re-derived in Wp-R3 behaves the same way (0.51–0.61).

So the two readouts are substantially but not trivially redundant: a cell ranked
high by the EGCG signature tends to be ranked high by pathogenicity even with the
shared genes removed. For Wp-P01 this matters — the paper's claim that PGAM
inhibition shifts cells "toward pathogenicity" is partly a statement about two
overlapping scores built from the same expression axis.

Agreement with the authors' own Table S4 correlations: 1,428 shared genes,
Pearson 0.81 on the marginal correlation and 0.92 on the partial correlation,
sign agreement 0.83.

## 6. Independent arithmetic check

Three checks outside the pipeline, from different output files: library mean
scores recomputed from the per-cell table (maximum absolute deviation 2.8 × 10⁻⁸,
cell counts identical); animal-paired differences recomputed from the library
means (3.2 × 10⁻⁸); and the pathogenicity identity, score = pro-inflammatory −
pro-regulatory, confirmed at 1.6 × 10⁻⁷. All deviations are CSV rounding.

## 7. Limits

- Two animals. Every paired difference is four numbers; nothing here is a
  population estimate.
- The analysed cell set is not the paper's. Our 15,830 cells include barcodes the
  authors excluded by criteria they did not deposit.
- Animal identity is prior-only; it enters the interaction model as a covariate
  that cannot be independently verified.
- Scores are RNA. Nothing here measures PGAM activity, metabolite level or
  protein.
- Programme labels are marker-score assignments, not the authors' clusters.
- Sections 2 (correlation sub-analysis) and the per-library confound
  correlations are post-hoc readouts of the governed output, flagged in place.
