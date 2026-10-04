# R3 initial bulk RNA results — 4 October 2026

**All four processed matrices were recovered; source/matrix qualification and
an initial animal-paired descriptive analysis are complete.** Exact reconstruction
of the paper's exact limma-selected genes remains unresolved. The subsequent
[source-aligned limma reconstruction](MODEL_RESULTS.md) has now executed; this
page preserves the distinct initial CPM endpoint. Read the
[identifier amendment](BULK_AMENDMENT_v2.md) before the original analysis contract.

Wg-R01 owns this stage. It supplies an aggregate RNA endpoint for Wg-P03/P04:
which within-animal responses are visible, and which additional functional
measurements are needed before interpreting them as conversion or JMJD3
dependence. The strongest rival is altered selection, survival, proliferation or
mixture, combined with relative RNA composition and sampling differences.

## Sources and eligibility

The [GSE162300 deposit](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162300)
explicitly states that each library was sequenced twice on the same day.
[GSE162382](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162382) supplies
the separate WT/JMJD3 conditional-KO experiment. The [primary paper](https://doi.org/10.1016/j.cell.2021.05.045),
Figure 6 legend and STAR Methods, identify the 68-hour RNA endpoint and the
limma/within-dataset program-selection methods. These primary-source statements
are distinct from the repository calculations below.

| Qualified source | Deposited matrix | Analysis units and allocation |
|---|---|---|
| GSE162300 | 20,817 unique gene symbols × 36 run columns, in both TPM and expected-count files | 18 libraries; 3 source animal labels × Th17p/Th17n/iTreg × vehicle/DFMO. Same-library counts are summed; runs are never independent replicates. |
| GSE162382 | 20,891 unique gene symbols × 28 columns, in both files | 4 WT and 3 KO animal labels × Th17n/iTreg × control/DFMO. There is no Th17p group. |

All 128 matrix-column occurrences join exactly to 64 GEO sample records.
Gene and column identities agree between the two scales within each experiment;
all values are finite and nonnegative. Independent parsers agree on every value.
The animal-blocked candidate designs have full rank; adding a genotype main
effect alongside individual-animal fixed effects creates the expected alias.
Physical specimen independence is not independently audited. WT labels do not
establish cross-series pairing. Figure 6H's n=4 legend does not supply a fourth KO.

The scripted download attempts returned access errors/challenge HTML. The normal
GEO browser links succeeded for all four files, without a challenge, and each
download matched GEO's listed byte size and passed gzip CRC verification. The
[successful acquisition manifest](../../analysis/research/runs/wg_bulk_qualification_v1/source_manifest.json)
records hashes and links; the earlier failed acquisition manifest remains in the
ignored source cache. This was a route-specific acquisition problem, not missing
deposited data.

## Measured endpoint and observed patterns

The analysis sums fractional expected counts from technical repeats, normalizes
by each library's deposited-gene total, and computes **DFMO − control in
log₂(CPM + 1)** within each source animal. All genes remain in the tables. Twelve
genes were named before outcome computation for display. No DEG calls, p values,
biological importance cutoff or population confidence interval is supplied.

Selected lineage-marker means in GSE162300 are shown below. Every Th17p and
Th17n animal has the indicated direction for these three genes (3/3 per group).

| Gene | Th17p mean paired change | Th17n mean paired change |
|---|---:|---:|
| Foxp3 | +0.810 | +2.973 |
| Rorc | −0.900 | −0.306 |
| Il17a | −4.570 | −1.204 |

These are relative bulk transcript changes on the declared offset scale, not
fold changes in enzyme activity or evidence of tracked Treg conversion. The
full display also retains the iTreg groups, metabolic genes and all individual
animals, including heterogeneous responses. See [Figure 5](FIGURES.md#figure-5-animal-paired-rna-changes)
and its [276 animal-by-gene observations](../../analysis/research/runs/wg_bulk_paired_descriptive_v2/prespecified_gene_animal_changes.tsv).

In GSE162382 Th17n, the mean Foxp3 response is +1.939 in WT and +2.352 in KO;
the directly calculated KO-minus-WT response difference is +0.414. This point
estimate does not establish an interaction or mediation. The full
[genotype-response table](../../analysis/research/runs/wg_bulk_paired_descriptive_v2/prespecified_genotype_response_differences.tsv)
retains all twelve genes and both lineages. No inference is made from
“significant here, not there.” Kdm6b gene-level abundance does not verify deletion
of a targeted functional exon.

An additional [untreated Th17p-minus-Th17n table](../../analysis/research/runs/wg_bulk_paired_descriptive_v2/prespecified_baseline_p_vs_n.tsv)
shows the bulk baseline comparison in the three paired animals. It is a
68-hour bulk experiment; the 48-hour cell-level Compass score contrasts in
Figure 3 are a different measurement and sample set.

The [two RNA figure plates](FIGURES.md#figure-4-bulk-rna-context) show all-gene
PCA and individual-animal responses. PCA uses 18,276/19,191 nonconstant genes
with centered log₂(CPM + 1), without variance scaling. It is not the source's
PCA on 3,414 DEG-selected genes. Plots retain each study's separate axes and units.

## Reproducible evidence and limits

- [Qualification contract](config/bulk_qualification_v1.json), frozen at `895883a`;
  [receipt](../../analysis/research/runs/wg_bulk_qualification_v1/receipt.json),
  [matrix inventory](../../analysis/research/runs/wg_bulk_qualification_v1/matrix_inventory.tsv),
  [design ranks](../../analysis/research/runs/wg_bulk_qualification_v1/candidate_designs.tsv).
- [Current numerical contract](config/bulk_paired_descriptive_v2.json), frozen at
  `62140a1`; [receipt](../../analysis/research/runs/wg_bulk_paired_descriptive_v2/receipt.json)
  and [independent checks](../../analysis/research/runs/wg_bulk_paired_descriptive_v2/results.json).
  The prior run stopped before contrasts on uppercase source identifiers and is
  preserved. The same twelve genes are retained through an explicit identity map.
- Independent raw-file scalar calculations verify technical aggregation,
  normalization and paired differences: maximum absolute discrepancy
  **1.60 × 10⁻¹⁴**, below the frozen 10⁻¹⁰ tolerance. SVD and Gram-matrix PCA
  eigenvalues agree. This is numerical verification, not biological replication.
- [Current rendering contract](config/bulk_figures_v1.json), frozen at `04d1c4d`;
  the [render receipt](../../analysis/research/runs/wg_bulk_figures_v1/receipt.json)
  records a layout-only successor to the embedded v2 figures. The original
  figures remain frozen; numerical analysis was not rerun for the layout change.

CPM is compositional and uses only the deposited gene universe. It is not
absolute RNA per cell, TPM or TMM/voom. The +1 CPM offset affects near-zero
magnitudes. These descriptive estimates cannot establish fate, suppression,
pathogenicity, direct demethylation or formal mediation. No scientific
acceptance, claim promotion or human retain/reject decision is recorded.

## Remaining R3 work

Qualify an R/limma runtime and freeze source-aligned count normalization,
filtering, blocked designs and explicit gene-wise multiplicity families.
Rscript was not found in the checked standard locations this session. The paper
allows limma-trend or limma-voom depending on library-size variability; its exact
historical assignment/settings still need recovery or a stated approximation.
Reconstruct the untreated lineage comparisons, source-selected PCA and within-
dataset Th17/Treg programs, then estimate treatment/genotype effects without
calling reused control-selected programs independent validation. R2, R4, R5 and
functional adjudication of P03/P04 remain separate jobs.
