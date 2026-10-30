# Temporal-reference input assessment

30 October 2026, Asia/Seoul. DY1-P02 E6. The existing Daniel 2018/2020 sources
are exposed reference systems, distinct from the original NAM immune-history
and later-IAV context. This assessment does not reconstruct a NAM time course.

The coordinating primary-source review identifies the [2018 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6197058/)
and [2020 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7608752/) as existing
regulatory precedents. Published temporal evidence is assay-specific. The source
qualification here concerns exact downloadable tables and metadata; literature
figures are not substituted for new repository measurements.

The GSE115505 umbrella includes several systems. GSE115504 is the cultured BMDM
RNA subseries with first/second-stimulation labels. Its memory supplement is
explicitly an averaged CPM table, with four WT and four KO group columns. The
metadata attributes those values to Cufflinks and calls them CPM; this remains
the author's normalization label, not independently reconstructed normalization.
Two sample records per group do not restore replicate-level values or variance.
Only an explicitly descriptive WT group-average comparison is proposed; no
genotype screen, effective biological n, confidence interval or target ranking.

GSE115502 is muscle-injury RNA and is excluded from the cultured comparison.
GSE115085 mixes macrophage systems and lists BEDGRAPH signals. GSE110465 contains
older cistrome-related subseries and may share evidence with subsequent papers.
Superseries/subseries occurrences are deduplicated by GSM; an accession umbrella
does not establish matched assays, independent preparations or repeated measures.

GSE151015 supplies a raw RNA matrix, with a missing first-column header retained
and parsed explicitly. RNA sample labels cover control and 24-hour groups;
early ChIP labels do not create early RNA or ATAC observations. The metadata
specifies gene-level featureCounts with multi-overlap allowed and GENCODE M21;
these counts must not be relabelled unique fragments. Chromatin supplements are
normalized tracks, not the missing matched temporal region-count matrix.

The metadata contract audits source membership, explicit condition labels,
available files, both RNA tables and exact column joins. It preserves all raw
metadata and acquisition records. No large archives or sequencing reads were
downloaded. Qualification of a group-average description does not establish
within-sample time evolution, regulatory causation, post-cessation NAM memory
or a paired cross-assay trajectory.
