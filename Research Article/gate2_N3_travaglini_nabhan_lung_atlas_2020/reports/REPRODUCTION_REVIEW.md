# Nb4: bounded source reproduction

**Executed 2 October 2026.** Targeted reconstruction uses a pinned CELLxGENE
release and fixed author labels. The complete 58-type clustering, MAST fits,
images and mouse–human analysis were not rerun.
[Source paper](https://www.nature.com/articles/s41586-020-2922-4).

## Source and count reconciliation

Inspected the annotated PDF, owner Notion notes, all nine supplementary tables,
three figure-source workbooks, supplementary figure PDF, reporting summary,
six author library metadata files and pinned author code. Documents were
treated as source material; downloaded notebooks were not executed. Private
planning and Notion pages were not modified.

Anonymous Synapse file access returned 403. The public
[CELLxGENE collection](https://cellxgene.cziscience.com/collections/5d445965-6f1a-4b68-ba3a-b8f765155d3a)
provided separately curated 10x and SS2 objects.
[Versions and hashes](../config/expression_sources_v1.json).

| Quantity | Observed |
|---|---:|
| 10x / SS2 cells | 65,662 / 9,409 |
| Curated total / sum of Table 2 population rows | 75,071 |
| Printed paper/Table 2 total | 75,066 |
| Normal lung / blood cells | 69,650 / 5,421 |
| Numeric donor/type entries matching Table 2 | 224/225 |

Ten cells have a broad deposited Dendritic label instead of the source Myeloid
Dendritic Type 1 label. Explicit aliases resolve other spelling differences;
these ten were not relabeled. Table 2's last-row donor columns also disagree
with its population rows. No five-cell deletion or source correction was
invented. [Concordance](../runs/source_concordance_v1/summary.json) and
[full comparison](../runs/source_concordance_v1/table2_count_concordance.tsv).

## Measurement contract

Every stored raw/X value passed nonnegative, finite integer checks; all
libraries had positive sums. Assays remain separate; donor, anatomy and type
define a unit. Contrasts use lung only, at least 20 cells per arm, and a
three-donor gate for the planned description. Fewer donors remain coverage holds.

Per-cell normalization uses the curated full-gene sum, CP10K for 10x or CPM
for SS2, then log1p. Pseudobulk differences are **log2(CPM + 1), left minus
right**, not exact unregularized log-fold changes. Deposited X means remain
separate. Curated raw totals differ slightly from source nUMI/nReads; mapped
SS2 reads are not assigned gene counts. No extra QC cut was retrofitted.

Of 88 requested unique symbols, 87 occur in 10x and 78 in SS2. SS2 lacks AGER,
CFB, CFD, HSPA1A, HSPA1B, KIAA1324, MYH11, PTPRC, RGS5 and SERPINF1 in the
imported raw universe; 10x lacks KIAA1324. Missing features are **not zeros**.
[Gene mapping](../runs/reproduction_v1/gene_mapping.tsv) and
[normalization audit](../runs/reproduction_v1/matrix_semantics.json).

## Recoveries and limits

| Distal contrast | Mean 10x difference | Mean SS2 difference | Donors per assay |
|---|---:|---:|---|
| MYRF: AT1 minus AT2 | +5.58 | +7.34 | 3 / 3 |
| TBX5: pericyte minus alveolar fibroblast | +2.73 | +2.86 | 3 / 3 |
| C3: alveolar minus adventitial fibroblast | −2.92 | −3.73 | 2 / 2; hold |

All listed donor effects share their assay mean's sign. These are RNA identity
descriptions, not causal regulators or repair outcomes. SPINT2/SFRP2 recover
opposing fibroblast subtype directions.
[Every donor effect](../runs/reproduction_v1/paired_effects.tsv).

The AT2 dot plot uses both assays because the source caption, scale and notebook
disagree on assay. Pooling permits a source display, not donor inference.
Distal AT2-s comparisons have only P3 in 10x and P1 in SS2 at the primary floor.
WIF1 is lower in both available units, while WNT5A has opposite signs; those
units are different donors. Human AT2-s–mouse Wnt-stem-cell equivalence remains
provisional. Imaging 20/203 (9.85%) and sequencing 870/5,444 have different
denominators and are not pooled.

Table 7's incorrect worksheet dimensions were reset for reading. Source-selected
species results are catalogued, but individual animal age, study and orthology
remain unresolved for a new comparison.
[Mouse design hold](../runs/source_concordance_v1/mouse_design_gate.json).
See [Figures 1–4](../FIGURES.md) and the historical [intake audit](INTAKE.md).
