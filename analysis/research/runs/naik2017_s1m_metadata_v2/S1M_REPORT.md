# S1M molecular metadata execution

Analysis: `Nk17-P01.s1m_metadata_v2`. These are source and structure observations, not expression effects.

GEO libraries: 28; SRA experiments: 28; ENA runs: 28; BioSample records: 28.
Count files: 16; shared gene IDs: 47729; union: 47729.
Join issues: 0; label issues: 0; count-structure failures: 0.

| Assay | Day label | Wound-hour label | History label | Libraries | Instrument models | Reference metadata |
|---|---|---|---|---:|---|---|
| ATAC-seq | 180 |  | control | 2 | Illumina HiSeq 2500 | mm10 |
| ATAC-seq | 180 |  | prior_inflammation | 2 | Illumina HiSeq 2500 | mm10 |
| ATAC-seq | 30 |  | control | 2 | Illumina HiSeq 4000 | mm10 |
| ATAC-seq | 30 |  | prior_inflammation | 2 | Illumina HiSeq 4000 | mm10 |
| ATAC-seq | 6 |  | control | 2 | Illumina HiSeq 4000 | mm10 |
| ATAC-seq | 6 |  | prior_inflammation | 2 | Illumina HiSeq 4000 | mm10 |
| RNA-seq | 30 |  | control | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 30 |  | prior_inflammation | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 30 | 12 | control | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 30 | 12 | prior_inflammation | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 30 | 6 | control | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 30 | 6 | prior_inflammation | 2 | Illumina HiSeq 2500 | mm10 |
| RNA-seq | 6 |  | control | 2 | Illumina HiSeq 4000 | mm10 |
| RNA-seq | 6 |  | prior_inflammation | 2 | Illumina HiSeq 4000 | mm10 |

## Eligibility interpretation pending source review

Explicit accessions establish a metadata join, not independent animals. The existing paper review attributes pooled duplicate preparations to the assays; exact animal identities, overlap and cross-assay pairing are not supplied by a replicate suffix.

Within-time control/history groups with qualified structure can support a descriptive processed-count comparison. Formal inference requires an explicit assessment of pool/preparation evidence. Platform/time associations qualify cross-time effects without automatically invalidating within-time comparisons. Raw-layout conflicts restrict exact raw replay, not automatically processed-count use.

Column selection, feature universe, normalization and the exact comparison must be frozen in a separate S2 contract after review. No normalization, differential expression, statistical testing, equivalence claim or functional inference was performed.

This stage does not qualify source workbooks, functional measurements, chromatin signal normalization or whole-paper methods. The original restrictions and remaining stages are retained.
