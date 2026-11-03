# A12 independent source qualification: no cohort admitted

3 November 2026. Fixed-procedure replication was selected; no pilot coefficients
were serialized, and GSE308103 remains closed. [Source/search specification](A12_SOURCE_SPEC_V1.md),
[contract](../../../analysis/cut_fill_20261103/a12_source_v1.json),
[receipt](../../../analysis/research/runs/cut_fill_a12_source_v1_20261103/receipt.json).
Freeze: `750f7bb`. This is source qualification, not a new predictive result.

The bounded search inspected three new primary-source candidates. Previous
Kim/Laughney/Wu failures remain unchanged and were not recycled.

| Source and inspected locator | Observed qualification | Disposition |
|---|---|---|
| [De Zuani et al., 2024](https://www.nature.com/articles/s41467-024-48700-8), Results atlas and Data availability; [E-MTAB-13526](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-13526), current study/info, IDF/SDRF and h5ad headers | 81 deposited sample records from 24 patients plus two healthy donors. Twelve patients are explicitly LUAD; five have CD235a-depleted tumour and adjacent-normal libraries. | Hold exact AT2/macrophage/patient/full-count mapping and >=10 eligible pairs. CD45 enrichment is not treated as proof of zero AT2. |
| [GSE304587](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304587), Overall design; [Kim et al., 2026](https://pubmed.ncbi.nlm.nih.gov/41673764/), abstract | Two LUAD patients, T255/T264. This is a different study from the earlier rejected Kim source. | Below the unchanged ten-pair floor; no expression analysis. |
| [Han et al., 2024](https://www.nature.com/articles/s41586-024-07113-9), abstract/Results and Methods epithelial sorting | Sixteen patients with an epithelial-enriched atlas and multiple matched normal samples. No qualified paired macrophage source export recovered. | Not admitted to the joint source-recipient procedure; no matrix analysis or inferred macrophage absence. |

For De Zuani, the exact five capture-supported LUAD patients are **15, 16, 21, 22, 24**.
The gate uses explicit sampling-site characteristics (`tumor` and `normal tissue
adjacent to tumor`), not guessed sample-name suffixes. These are capture
opportunities, not measured eligible AT2/macrophage intersections. The publication
reports 25 patients / 13 LUAD, whereas the IDF states 24 and the deposited SDRF identifies
24/12. That source discrepancy is retained; no missing patient is invented.

Both public annotated h5ad headers were recovered with bounded HTTP206 reads.
The tumour object is 58,739,231,180 bytes and the background object 45,505,872,062
bytes; the whole objects were not downloaded. Their observed schema contains
patient, sample, sorting and successive author cell-type columns, through tumour
v25 and background v12. Initial header requests timed out; a cached retry succeeded.
Subsequent row-metadata extraction requests timed out for both objects. This is an
access/recovery limit, not evidence that those annotations do not exist. No expression
values, new signature, reference classifier or predictive outcome was opened.

[Acquisition attempts](../../../analysis/research/runs/cut_fill_a12_source_v1_20261103/access_attempts.json)
record exact object URLs, sizes, observed ETags, requested range hashes, recovered
schemas and errors. These are partial-source provenance, not whole-object hashes.
[Sample inventory](../../../analysis/research/runs/cut_fill_a12_source_v1_20261103/de_zuani_samples.csv)
and [qualification](../../../analysis/research/runs/cut_fill_a12_source_v1_20261103/qualification.json)
preserve the actual deposited coverage. Checks passed for technical-row deduplication
and nonconflicting sample/individual/disease/capture/site fields.

**Disposition:** bounded source search complete, replication held. The enabling
input is a provenance-verified full-count/state/patient mapping with at least ten
eligible paired AT2/macrophage units under the unchanged 50-cell rule, supported
monocyte-derived source fraction and predictor/endpoint coverage. The five intended
nonimmune-inclusive pairs alone cannot meet that gate; whether other libraries
supply valid recipients remains unverified. Independence from the pilot, author
annotation correspondence and endpoint-gene coverage were not certified.

No absolute prediction errors, recipient increment or fibroblast result is claimed
for this pass. The original epithelial gain and unfavorable fibroblast outcome
remain in the pilot. Any qualified later run must retain fixed index, gene-disjoint
TNF/NFkB endpoint, alpha 1, training-only processing, identical patient holdouts and
both source-plus-TNF/training-mean baselines. General inflammatory RNA is not an
IL1-specific mechanism. Search date, exact queries and completed versus unrecovered
reads are recorded in the linked specification; no global absence claim is made.
