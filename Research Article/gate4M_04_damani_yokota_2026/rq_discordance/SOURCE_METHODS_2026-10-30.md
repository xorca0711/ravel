# External reference source assessment

30 October 2026, Asia/Seoul. DY1-P02 E1 metadata qualification. The original
N. brasiliensis-history/later-IAV study motivates the measurement question; this
reference uses cultured macrophage measurements under non-infectious conditions.
Source and published outcomes are exposed. This note records source assertions,
not newly fitted biological effects or a NAM-memory validation.

The [Deochand 2024 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11489752/)
was accessible through PMC on this date. Figure 1a identifies three RNA biological
replicates (mice); Figure 2a identifies four ATAC biological replicates. The RNAseq
and ATACseq Data analysis subsections describe gene counts and counts over a
merged peak universe. These statements support biological replicate meaning
within source groups. They do not establish which cultures share a mouse across
conditions, cross-assay pairing, or recorded processing batches. The stated
experimental comparison is at 24 hours; no withdrawal/time-course inference is
appropriate. Exact replay of the author's normalization/model is a separate task.

GEO landing pages were challenged, but the public bulk endpoints supplied the
two matrices and complete SOFT records for [GSE247223](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE247223)
and [GSE248042](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE248042).
Retrieval records retain response metadata and exact SHA-256. The RNA file is the
listed Updated version; no equality to the older differential workbook is assumed.
The ATAC annotation-bearing differential table was acquired solely for its
identifier/coordinate/annotation fields; no effect or significance columns enter
source qualification. BioSample XML was retrieved for the GEO-listed accessions.

The ATAC vehicle titles say `24h` while their characteristic says exactly
`treatment: Vehicle, 25 hours`. Both survive in the sample map. This unresolved
source conflict prevents claiming a verified pure duration-matched contrast;
it need not block a clearly labelled descriptive comparison. Similarly, repeat
labels are source-local labels, not a proof of repeated aliquots or independent
animals across conditions. Unknown dependence requires conditional uncertainty
or bounded descriptive spread, not unqualified population confidence intervals.

Both assay records declare mm10. The RNA Methods/metadata say “GENCODE release 27”
without an exact annotation file. The official [GENCODE release history](https://www.gencodegenes.org/mouse/releases.html)
places mouse M27 on GRCm39. The source wording therefore does not establish an
unambiguous compatible annotation version; it does not prove which file was
actually used. Author-provided Ensembl IDs and region annotations can be audited
for explicit joins without silently repairing this provenance gap. A nearest-gene
or nearest-TSS assignment remains an association rule, not evidence of regulation.

The frozen metadata run will report integer/identifier structure, all exact
sample-column joins, BioSample attribute coverage, interval/annotation agreement
and missing design information. All source rows remain in the audit. A metadata
pass supplies neither biological effect estimates nor permission to equate RNA
and ATAC scales. Original NAM unit, count, state and temporal holds are unchanged.
