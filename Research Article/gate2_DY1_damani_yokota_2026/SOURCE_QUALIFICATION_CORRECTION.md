# Source qualification: superseding documentation correction

29 October 2026. This note supersedes the interpretations listed below in
[source_v1 output](../../analysis/research/runs/DY1_source_v1/source_qualification.json).
The [contract](config/source_v1.json), [script](scripts/qualify_sources_v1.py),
[receipt](../../analysis/research/runs/DY1_source_v1/receipt.json) and every frozen
output remain byte-for-byte preserved. No v2 run occurred.

## Two corrections

1. **The blank naive CMO label is a parser artifact.** The public
   `GSM9964564_feature_reference.csv` header is `multiplexed_sample ` with a trailing
   space. V1 looked up `multiplexed_sample` without stripping header whitespace.
   Direct CSV inspection shows the condition label `Naive`, with CMO301-303.
   The trained baseline reference lists CMO304-306. The future parser correction
   would trim headers and values in a new version, never overwrite v1.
2. **Condition-library confounding is unresolved, not established by GSM titles.**
   V1's `scRNA_condition_batch` field says one expression GSM per condition and
   asserts confounding. Both baseline feature tables contain CMO301-306; that
   is compatible with, but does not establish, mixed-condition libraries. Feature
   row presence does not distinguish meaningful assigned cells from ambient or
   background tags. The challenge feature tables contain CMO301-304/309-310 in
   both libraries. Actual counts, barcode assignments and condition-to-library
   support were not analysed. Reused tag names are library-local identifiers.

The coordinating review independently identified both issues from the cached
public files. They affect qualification, not previously computed biological
effects: no such effects were generated. Source titles remain faithful metadata
transcriptions but are not verified biological-unit assignments.

## Confirmed source constraints

- GEO GSE280183 contains eight ATAC library records. The sample records were
  updated 27 July 2026. Their processing narrative describes
  Seq-N-Slide/Bowtie2/edgeR with GC correction; the article describes
  seq2science/bwa-mem2/DiffBind-DESeq2. Which narrative generated the replaced
  files is unresolved. NarrowPeak signal and peak presence are not raw read counts.
- The six bulk RNA files have 406,850 Ensembl exon-bin rows and 47,911 gene
  prefixes each, plus five count-summary rows, as recorded by source_v1.
  Summing exon-bin hits cannot silently become unique gene-level fragment counts.
- The four expression matrices contain Gene Expression and Antibody Capture
  features, including the CMO identifiers above. No author cell-state labels or
  verified tag-to-animal/pool crosswalk was recovered in the inspected sources.
- Article main Methods describes individual tagging; Extended Data 8c says each
  biological replicate pools cells from 3-6 animals. Bulk RNA Methods also
  describes pooling. These are unresolved design facts, not grounds to invent n.
- Inspected bulk/scRNA BioSample records did not resolve animal/pool identity.
  Both Code Ocean capsules returned HTTP 403 on the repeated public-access check.
  The publisher response recorded as HTTP 200 was a client-challenge page,
  not successful access to article code, supplements or source data.
- GSE136831 is an already-used Ravel source. Local reuse does not establish
  independent human replication. No new human biological analysis ran.

These facts constrain individual comparisons. They do not establish that all
remaining stages are impossible. The outstanding work stopped because of the
platform restriction and subsequent documentation-only instruction, not a
completed scientific feasibility adjudication.

Primary records: [GSE280183](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE280183),
[GSE343897](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE343897),
[GSM9964564](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9964564),
and [the article](https://doi.org/10.1038/s41586-026-11060-y).
The [prior methods/figure review](../../docs/research_reviews/2026-10-29-nam-memory/README.md)
and [literature note](LITERATURE_CONTEXT.md) retain their stated access limits.
