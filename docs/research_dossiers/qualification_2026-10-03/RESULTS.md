# Fresh deposited-metadata results

The source snapshots and hashes are in [SOURCES.md](SOURCES.md). These conclusions combine the registered metadata inventories with primary-paper and current repository interpretation. Parsing proves neither biological independence nor scientific acceptance. The superseries and paired-assay checks confirm source accounting already present in the underlying article records; their value here is an explicit, reproducible qualification boundary.

| Owning question and linked uses | Frozen metadata run | Inventory | Sample identities |
|---|---|---|---|
| A2 / A9 | [Receipt](../../../analysis/research/runs/a2_source_qualification_v1/receipt.json) | [Inventory](../../../analysis/research/runs/a2_source_qualification_v1/inventory.json) | [Sample table](../../../analysis/research/runs/a2_source_qualification_v1/samples.tsv) |
| A5 | [Receipt](../../../analysis/research/runs/a5_source_qualification_v1/receipt.json) | [Inventory](../../../analysis/research/runs/a5_source_qualification_v1/inventory.json) | [Sample table](../../../analysis/research/runs/a5_source_qualification_v1/samples.tsv) |
| A7 / ES1 | [Receipt](../../../analysis/research/runs/a7_source_qualification_v1/receipt.json) | [Inventory](../../../analysis/research/runs/a7_source_qualification_v1/inventory.json) | [Sample table](../../../analysis/research/runs/a7_source_qualification_v1/samples.tsv) |
| A22 / A10 | [Receipt](../../../analysis/research/runs/a22_source_qualification_v1/receipt.json) | [Inventory](../../../analysis/research/runs/a22_source_qualification_v1/inventory.json) | [Sample table](../../../analysis/research/runs/a22_source_qualification_v1/samples.tsv) |

## A2 and A9: MesSTIM identifies recipient populations, not preparations

[GSE169125](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE169125) contains 18 RNA-seq sample records: Col13, Col14 and Myo title groups, each with untreated, AREG and EGF labels and two records per group. The characteristic fields are cell type, strain and treatment. They do not provide a mouse, pool or preparation identifier. The terminal numeric title suffix is therefore not an animal ID. The identified processed file is `GSE169125_MesSTIM_counts.csv.gz`; its expression contents were not downloaded.

The [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9767680/) already reports differential recipient responses in Figure 6. Its full text was recovered through Europe PMC after the PMC browser challenge. The generic statistical statement about repeated experiments does not supply the 18-sample-to-preparation crosswalk needed here. Source figure evidence should not be dismissed, but it cannot be converted into a verified independent-unit design for a new reanalysis by assumption.

**Decision:** suitable for metadata/source interpretation and a possible future bounded descriptive expression question after a new contract and input audit. Population inference remains held until unit identities and relationships are recovered. A delivery mechanism is not identified: these are supplied-ligand comparisons, not source-to-recipient delivery measurements. A receptor-competence claim additionally needs a justified receptor/activity endpoint; an RNA response alone is insufficient. The existing A2/A9 discovery studies are not relabeled as replicated by this source.

## A5: the library inventory is stable, but the enabling joins are still absent

[GSE303646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE303646) has 56 RNA-seq records. All accession/title pairs exactly match the preserved [28 September crosswalk](../../../RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/GSE303646_library_crosswalk.tsv). GEO characteristics include age, batch, cell type, genotype and treatment; those fields do not recover the missing animal identities or per-barcode state map. The listed `GSE303646_RAW.tar` is a file locator, not an inspected matrix.

The [prior source audit](../../../RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/REPORT.md) identified the author object `230111_Bleo_Ageing_annotated_final.h5ad`, a 55-mouse statement and 56 library identifiers. This pass confirms the deposited identifiers without resolving that distinction. It does not repeat the earlier author-code/browser search or infer that no export exists elsewhere.

**Decision:** retain the unchanged replication hold. The exact enabling export is a library/barcode-to-mouse and original author-state table, with pooling/splitting explained and count alignment established. No new classifier, relaxed eligibility threshold or expression score was substituted for the missing metadata.

## A7: CEBPA and AP-1 are distinct sources

[GSE247130](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247130) contains 12 assay records: six RNA and six ATAC. Genotype fields name Cebpa, and sex fields explicitly describe pooled male/female material. The titles pair assays across six condition contexts. [GSE310539](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310539) contains eight assay records: four RNA and four ATAC, with AP-1-related mutant/control contexts. It is not another set of Cebpa-loss replicates.

The [ES1 analysis](../../../Research%20Article/epithelial_state_specificity/README.md) uses six CEBPA-source plus four AP-1-source multiome condition wells. Thus neither twenty assay records nor ten condition wells means twenty or ten independent CEBPA biological units. No infection data were reanalyzed or experimental procedures specified in this stage.

**Decision:** preserve conditional within-source descriptions. An animal/preparation-level genotype-by-starting-state comparison remains unsupported by these pooled condition records. Any additional sample independence must be demonstrated, not inferred from assay suffixes or source aggregation. The current dossier now names this source split explicitly.

## A10 and A22: a superseries is not a common population of replicates

[GSE307351](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE307351) has 890 sample records: 886 belong to the organoid screen GSE307112 and four to the spatial study GSE307128. Each screen record names both mouse and human organisms; these are the two compartments of the mixed-species material, not two biological replicates. The spatial records are blocks 8/16 WT and 10/15 NKX2.1 KO, with a common deposited batch label; an animal-to-block map is still required.

This confirms the article's [existing dataset inventory](../../../Research%20Article/gate2_N2_nabhan_2026/DATASETS.md). The [current A22 report](../../../RQ_Specified/A22_epithelial_identity_niche_response/reports/identity_amount_v2/RESULTS.md) owns the analysis denominator: 771 paired-species QC wells, then 672 noncontrol wells and 201 targets. The 890-record total must not replace those denominators. Deposit membership alone does not recover independent epithelial preparations, fibroblast donors, imaging joins or spatial animal/section nesting.

**Decision:** keep same-screen findings at their recorded scope and the spatial causal comparison held. Plate/batch transport is not automatically transport between biological preparations. The previously noted spatial treatment/context discrepancy requires a sample-specific source reconciliation; this metadata inventory does not resolve it.
