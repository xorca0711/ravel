# A12 bounded source qualification specification

3 November 2026. Fixed-procedure replication is selected before new expression
outcomes; the closed pilot and prior Kim/Laughney/Wu failures remain unchanged.

Search coverage: primary-source search on 3 November for `lung adenocarcinoma
single cell paired normal 2024 2025 AT2 GEO patients`; follow-up searches for
`s41467-024-48700-8 data availability GSE`, that DOI with `cellxgene`,
`Single-nucleus multi-omics delineates patients`, `GSE304587`, and
`s41586-024-07113-9 EPCAM` / `s41586-024-07113-9 GSE`.
Three new source records are considered: De Zuani2024 E-MTAB-13526;
Kim2026 GSE304587 (distinct from the previously rejected Kim cohort);
Han2024 epithelial atlas. Indexed abstracts/methods identified their respective
paired mixed-cell, two-patient and epithelial-enriched designs. These are scoped
candidate checks, not a systematic review or a novelty assessment.

Before this freeze, BioStudies study/info, IDF/SDRF and remote h5ad headers were
read; thus source counts and metadata structure are exposed. Both annotated
objects support HTTP206 range access, but metadata row extraction timed out.
Exact source requests, cached ranges and attempts are retained in ignored
raw_data/cut_fill_20261103. Neither full 45.5/58.7 GB object nor expression values
were downloaded. The h5ad version is qualified by its URL/size/ETag and acquired
range hashes, not a claimed full-object checksum. Headers have successive author
annotation fields through tumour v25 and background v12; none was re-labelled.

This run deduplicates SDRF technical FASTQ rows using exact Source Name and
requires agreement of individual, disease, FACS and sampling-site fields. Counts
refer to actual source records. Count paired CD235a-depleted LUAD libraries using
the explicit `tumor` / `normal tissue adjacent to tumor` sampling-site values,
not guessed sample-name suffixes. These are candidate capture opportunities,
not measured AT2/macrophage cell counts or an eligibility certification.

Preserve the publication/deposit patient-count discrepancy. Do not infer AT2
absence from CD45 enrichment; a missing row map is unknown. Stop if the exact
patient/author-state/full-count map and >=10 eligible pairs at the unchanged
50-cell floor cannot be established. The other two source records are bounded
primary-source exclusions/limitations, not a further matrix search.

If a later source qualifies, use the original fixed recipient index, gene-disjoint
197-gene TNF/NFkB endpoint at70% coverage, alpha1 baseline ladder, training-only
processing and patient holdouts. Compare absolute prediction errors and recipient
increment over source-plus-TNF and training mean; retain fibroblast secondary
outcomes. No model is fit in this source run. General inflammatory RNA is not an
IL1-specific mechanism, and missing maps cannot be repaired with outcome-trained
reference labels. No biological effect margin or confirmatory power is invented.
