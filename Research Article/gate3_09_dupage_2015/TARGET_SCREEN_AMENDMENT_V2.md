# Target-screen amendment 2: qualify the protein-coding view

7 November 2026, after inspection of v1, before calculating v2 ranks.
**V1 is retained in full.** This is a prospective, exposed annotation restriction
for a protein-target question, not a repair to obtain a favorable outcome.

The unrestricted v1 reading frontier contains 26 distinct loci, dominated by
Mir/Snor/Scarna labels. Source GSE58998 SOFT sample extract protocols explicitly
describe Illumina TruSeq 2 **poly-A selection**. This is not a mature-small-RNA
assay. Those labels may reflect precursors, overlaps or mapping/quantification
limitations; the current data cannot distinguish them. Stability to sample
omission does not establish correct molecular identity. Do not infer mature
miRNA abundance or activity from these values.

The separate protein-coding view will annotate every v1 locus using the NCBI
mouse gene_info bulk file, retrieved 7 November 2026 from
[NCBI Gene](https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Mus_musculus.gene_info.gz).
HTTP Last-Modified: `Sat, 07 Nov 2026 08:31:40 GMT`; 3,936,540 bytes;
SHA-256 `38c16681b79cf9277ff5969e91093cd9c84ba852e7c6bb4fae525fb6aceb1719`.
This is current annotation, not the authors' historical annotation. Raw source
and retrieval metadata are preserved under ignored raw data.

Match exact case-sensitive symbol, mouse taxonomy 10090, a unique NCBI GeneID,
and matching chromosome label (mm10 `chrM` corresponds to NCBI `MT`). Do not
resolve aliases, fuzzy matches or retired symbols silently; retain unmatched,
ambiguous and chromosome-discordant entries in the audit. This is a symbol and
chromosome identity screen, not a coordinate conversion or transcript validation.
Only exact unique chromosome-compatible `protein-coding` entries enter v2 ranks.
Retain the original v1 numeric estimates, stability rules, sort keys and 10-per-
signed-track reading budget. Protein-coding is a target-class restriction, not
evidence of causality or an assertion that noncoding regulation is unimportant.

Outputs retain all annotated v1 genes, the annotated v1 frontier, a new protein
frontier, separately annotated anchors and summary counts. V1 ranks remain
available beside new coding ranks. No expression model is rerun and no thresholds
are tuned. Stop on source hash mismatch, duplicate v1 identities or unsupported
annotation structure. Empty or uninformative results remain reportable.

Exposure: all v1 displayed genes and the 19 anchors are known, including positive
Pde3b/Bach2/Klf2/Bcl2 and negative Il10/Prdm1 contrasts. Selection of the protein
view is prompted by assay compatibility, not ignorance of those outcomes.
No new protein-only ranks were inspected before this amendment's freeze.
