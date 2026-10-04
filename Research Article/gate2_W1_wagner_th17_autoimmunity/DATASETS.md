# Input families and biological-unit qualification

**Current status:** the [R0 source-identity result](RESULTS.md) supersedes the
initial access statements below. Both author matrix headers now match all 290
cells, with exact author-SRX/GEO joins. Bulk/ATAC animal labels were recovered;
expression values, assay matrix joins and sorted-cell biological units remain
unqualified. The following catalogue is preserved as the initial intake.

Public GEO brief records were retrieved directly on 4 October 2026. Counts
below count listed GSM records; they are **not independent animal counts**.
No expression matrix, peak matrix or individual GSM/BioSample map has been
qualified in this session. Accession/title matching establishes a source lead,
not the design needed for inference.

| Source | Record-level inventory | Intended role |
|---|---|---|
| [GSE74833](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE74833) | 768 GSM records, nine child series; mixes population and single-cell experiments | Parent locator for previously published data reused by Wagner |
| [GSE75109](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75109) | 139 listed libraries; sorted pathogenic-condition single cells | Intended Th17p source; prove exact cell-ID mapping to author input |
| [GSE75111](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75111) | 151 listed libraries; sorted non-pathogenic-condition single cells | Intended Th17n source; prove exact cell-ID mapping to author input |
| [GSE75110](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75110) | 130 listed libraries, non-pathogenic condition without the same sorted title | Exclude from the primary intended subset; don't add cells to improve apparent precision |
| [GSE164999](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164999) | 76 GSM records across three children | 2021 bulk RNA/ATAC umbrella; never count parent and children as independent studies |
| [GSE162300](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162300) | 36 listed libraries; DFMO/Th17/iTreg RNA; TPM and estimated-count files | Fig. 6A-C reproduction |
| [GSE162382](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162382) | 28 listed libraries; JMJD3/DFMO RNA; TPM and estimated-count files | Fig. 6H/S6E-F; qualify actual lineage/genotype/treatment support |
| [GSE165088](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE165088) | 12 listed libraries; ATAC; raw-count table listed | Fig. 6D-F; genome build, peak definitions, units and external annotations still needed |

STAR Methods, supplied PDF p. 22, explicitly retain **151 Th17n and 139 Th17p
IL-17A/GFP-positive cells**. That supports the intended GSE75111/GSE75109 subset,
but numerical agreement is not an exact cell-identity join. The paper reprocessed
older libraries with an updated pipeline and SCONE normalization; an arbitrary
GEO expression table is not necessarily the matrix used by Compass.

Listed processed filenames for later acquisition:

- `GSE162300_DFMO_RNA_TPMs.csv.gz`, `GSE162300_DFMO_RNA_est_counts.csv.gz`
- `GSE162382_DFMO_JMJD3_TPMs.csv.gz`, `GSE162382_DFMO_JMJD3_est_counts.csv.gz`
- `GSE165088_Raw_Count_Data.csv.gz`
- The 2015 child records list `GSE75109_RAW.tar` and `GSE75111_RAW.tar`.

## Required source joins

The metadata stage must produce study, accession, library/cell ID, animal or
pool/preparation ID, lineage/condition, treatment, genotype, assay, collection
time, processing block, pairing and source-locator columns. Keep unknowns
explicit. Verify one-to-one matrix-column joins and exclusions; distinguish
technical repeats, split cultures and independent biological preparations.
Only use a block/pair when the source actually establishes it.

For the 290 cells, cells are observations nested within source animals/cultures;
the number and cross-condition allocation of those biological units is unresolved.
For bulk/ATAC, library numbers and figure-level n do not substitute for the full
unit map. Raw estimated counts are not UMI counts. Preserve fractional values
and use the documented assay-appropriate method; do not round them into a
different measurement model merely to fit a preferred implementation.

Stop population inference if biological independence, treatment allocation or
design rank cannot be established. A labelled descriptive source reproduction
can still be useful. Cross-assay concordance remains aggregate unless the
same-preparation linkage is verified; it is never paired single-cell multiome
data by inference.
