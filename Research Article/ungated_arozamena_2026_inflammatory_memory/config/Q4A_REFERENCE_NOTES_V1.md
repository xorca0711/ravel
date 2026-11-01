# Frozen Q4a reference documentation record

Read 1 November 2026 by the technical and originating reviewers. This is a dated
source-reading record bound to the numerical contract, not a byte-identical
archive of the web pages. The direct raw-HTML request for the ARC fragment page
returned HTTP 429; that acquisition failure is preserved separately. Prior
official page reading succeeded, and no access workaround is needed to use it.

- [ARC 2.1 fragments](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/outputs/fragments-file), Format and Column definitions: BGZF rows represent collapsed unique fragments. Coordinates are zero-based, end-exclusive; fields are chromosome, start, end, barcode, readSupport and strand. Read support includes duplicate reads and is not a fragment-count weight. Header lines describe pipeline and reference. Sixth-column strand records fragment origin, not gene annotation strand.
- [ARC 2.1 matrices](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/feature-barcode-matrices), Gene Expression feature definition: source IDs/names come from reference GTF. Columns 4–6 span selected transcript TSSs in zero-based BED format; basic-tagged transcripts are used when available, otherwise all. The span does not certify one promoter or a gene body.
- [ARC 2.1 ATAC BAM](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/analysis/atac-barcoded-bam), barcode tags/translation: CB is corrected and translated to the paired GEX barcode. The fragment barcode corresponds to CB. Therefore use exact deposited barcode strings; do not apply a second translation. Observed file joins still require validation.
- [ARC 2.1 algorithm overview](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/algorithms-overview/algorithms-overview), ATAC duplicate marking: read pairs are grouped by adjusted start/end and hashed barcode; one is unique and the remaining pairs are duplicates. Only the unique eligible pair is emitted as a fragment. Thus the prospective unexpected-duplicate key is chromosome/start/end/barcode. Different readSupport or sixth-column strand does not legitimize a repeated key. The [2.1 release notes](https://www.10xgenomics.com/support/software/cell-ranger-arc/2.1/release-notes/release-notes) separately describe the added strand field. This primary algorithm source, rather than inference from the six-column schema alone, supports the check. A repeated key stops that source; no silent collapsing or repair occurs.
- [ARC 2024-A reference build notes](https://www.10xgenomics.com/support/software/cell-ranger-arc/downloads/ref-build-steps), Mouse GRCm39 section: the public source uses Ensembl release-110 GRCm39 FASTA and `gencode.vM33.primary_assembly.annotation.gtf.gz`, removing ID-version suffixes and applying documented biotype/readthrough filtering. This does not prove equality to the study's custom TdTomato reference/hash.
- [GENCODE M33](https://www.gencodegenes.org/mouse/release_M33.html) and [GTF format](https://www.gencodegenes.org/pages/data_format.html): versioned GRCm39 gene/transcript annotation, gene/transcript attributes and repeated tags. GTF start/end are one-based inclusive. Convert [start,end] to [start-1,end); positive-strand TSS is start-1 and negative-strand TSS is end-1.

The fragment-local GRCm39/ARC2.1 headers govern this deposited-data adaptation;
article/GEO mm10/ARC2.0.2 statements remain an unresolved source conflict. No
liftOver, source-header relabelling, motif analysis or reconstruction of the
paper's integrated consensus-peak object is part of this work.
