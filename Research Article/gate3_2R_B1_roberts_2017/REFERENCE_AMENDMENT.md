# Reference identity amendment

The paper and GEO metadata report GRCm38 release 79. The deposited transcript quantifications qualify differently by experiment.

| Libraries | Target audit | Eligible treatment |
|---|---|---|
| GSM2462968–70 | Each file has 344,513 accession-style targets with zero matches to the versioned Ensembl 84 cDNA targets. None of the fixed-panel release-79 transcripts match either. | Requantify the accession-matched reads. Keep the original deposit and qualification receipt. |
| GSM2462971–81 | Each file matches all 96,626 versioned IDs of Ensembl release 84 mouse cDNA in the same order. Release-79 versions match only 49,221 IDs. | Use the exact released target headers for transcript-to-gene assignment. Retain the earlier stable-ID replay as superseded. |

The amended replay binds the Ensembl GRCm38 release 84 `cdna.all` FASTA and validates the full target order and transcript lengths against it. Exact headers supply transcript and gene identifiers. TPM summed over the indexed gene transcripts is described on the same offset scale and with the same fixed panel as specified before outcomes. The released TPM scale and raw-read recovery do not reproduce the paper's Sleuth/DESeq2 inference. [Ensembl reference archive](https://ftp.ensembl.org/pub/release-84/fasta/mus_musculus/cdna/) · [GEO series](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE93820)

Experiment 1 records GSM2462968, GSM2462969 and GSM2462970 match ENA runs SRR5186277, SRR5186278 and SRR5186279 by SRX2502229–31. Requantification uses ENA checksum-verified reads, the release-84 cDNA reference, cutadapt 4.9 with the GEO quality and minimum-length options, and Kallisto 0.43.1 with the documented single-end fragment parameters and a 31-mer index. This adapts the reported 0.43.3 pipeline and omits bootstraps for the descriptive TPM endpoint. Preregistered use of the exact reference was triggered by target identifiers and lengths, while earlier TPM-based directions remain recorded as exposed. As recorded in the contracts, unit nesting remains unknown.
