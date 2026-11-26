# Reference identity amendment

The paper and GEO metadata report GRCm38 release 79. The deposited transcript quantifications qualify differently by experiment.

| Libraries | Target audit | Eligible treatment |
|---|---|---|
| GSM2462968–70 | Each file has 344,513 accession-style targets with zero matches to the versioned Ensembl 84 cDNA targets. None of the fixed-panel release-79 transcripts match either. | Requantify the accession-matched reads. Keep the original deposit and qualification receipt. |
| GSM2462971–81 | Each file matches all 96,626 versioned IDs of Ensembl release 84 mouse cDNA in the same order. Release-79 versions match only 49,221 IDs. | Use the exact released target headers for transcript-to-gene assignment. Retain the earlier stable-ID replay as superseded. |

The amended replay binds the Ensembl GRCm38 release 84 `cdna.all` FASTA and validates the full target order and transcript lengths against it. Exact headers supply transcript and gene identifiers. TPM summed over the indexed gene transcripts is described on the same offset scale and with the same fixed panel as specified before outcomes. The released TPM scale and raw-read recovery do not reproduce the paper's Sleuth/DESeq2 inference. [Ensembl reference archive](https://ftp.ensembl.org/pub/release-84/fasta/mus_musculus/cdna/) · [GEO series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE93820)

Experiment 1 records GSM2462968, GSM2462969 and GSM2462970 match ENA runs SRR5186277, SRR5186278 and SRR5186279 by SRX2502229–31. Requantification uses accession-matched reads, the release-84 cDNA reference, cutadapt 4.9 with the GEO quality and minimum-length options, and Kallisto 0.43.1 with the documented single-end fragment parameters and a 31-mer index. This adapts the reported 0.43.3 pipeline and omits bootstraps for the descriptive TPM endpoint. The exact-reference quantification was frozen after checking target identifiers and lengths, while earlier TPM-based directions remain recorded as exposed. As recorded in the contracts, unit nesting remains unknown.

| GEO sample | Preparation | ENA run | ENA compressed FASTQ MD5 |
|---|---|---|---|
| GSM2462968 | Immediate ex vivo | SRR5186277 | `61661ac3b9fa8d1d923f073ad53691f2` |
| GSM2462969 | 60 h library 1 | SRR5186278 | `29cce7e06ba05aff327385ca5f49c52c` |
| GSM2462970 | 60 h library 2 | SRR5186279 | `6ce292ef978ace139861b63a5054c120` |

Archive retrieval uses the ENA run report for SRP097011. The first experiment 1 run generates the release-84 index. Subsequent quantifications reuse those exact index bytes, bound by SHA-256 in their contracts. This avoids rebuilding the index while libraries are processed sequentially.

The first 60 h library, GSM2462969, was recovered from the full-quality NCBI SRA archive after the ENA range transfer stalled. SRA Toolkit validated the archive's embedded MD5 checks, then emitted 80,928,225 biological reads, matching the ENA run report. ENA later completed and passed its compressed MD5. The first 1,000 sequence and quality records agreed between the two routes. The frozen quantification uses the SRA recovery and records its validation log. [NCBI archive](https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5186278/SRR5186278)
