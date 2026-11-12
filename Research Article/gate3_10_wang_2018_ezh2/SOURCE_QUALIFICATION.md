# Wang 2018 source qualification

## Deposited libraries and source methods

Retrieved 12 November 2026. The estimand is relative RNA abundance in day-4
bulk libraries from initially CD62L-high mouse Tregs after in-vitro activation.
Wang's supplement, PDF p. 2, documents the 96-hour culture and STAR counts
restricted to uniquely assigned reads, aggregated by Ensembl GRCm38 release 78
gene. The main paper's Mice section reports littermate or age-matched controls
generally. GEO and BioSample identify the exact alleles in the nine libraries.
Neither records mouse or pool membership, aliquot relationships, sex, age, a
littermate crosswalk, post-culture selection, or sample-specific culture,
library-preparation or sequencing blocks. Distinct BioSample and SRR accessions
establish distinct submitted library records. Inference to an independent mouse
or preparation population requires the missing experimental unit and batch
records. [Main article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6094952/) ·
[GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114298).

| Public source | Local ignored file | Bytes |
|---|---|---:|
| [GEO count matrix](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114298/suppl/GSE114298_counts.STARMOUSE.GEO_05_08_2018.txt.gz) | GSE114298_counts.STARMOUSE.GEO_05_08_2018.txt.gz | 442689 |
| [GEO family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114298/soft/GSE114298_family.soft.gz) | GSE114298_family.soft.gz | 2770 |
| [ENA read-run TSV](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA470833&result=read_run&fields=run_accession,experiment_accession,sample_accession,secondary_sample_accession,experiment_alias,sample_title,library_name,library_layout&format=tsv) | PRJNA470833-ENA.tsv | 794 |
| [NCBI BioSample records](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=9111997,9112005,9112004,9112003,9112002,9112001,9112000,9111999,9111998) | biosamples.xml | 15415 |
| [Publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf) | wang-elsevier-mmc1.pdf | 10776359 |
| [Europe PMC article XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6094952/fullTextXML) | wang.xml | 146157 |
| [Historical Ensembl GTF](https://ftp.ensembl.org/pub/release-78/gtf/mus_musculus/Mus_musculus.GRCm38.78.gtf.gz) | Mus_musculus.GRCm38.78.gtf.gz | 23117167 |
| [Mouse MSigDB Hallmarks 2025.1.Mm](https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2025.1.Mm/mh.all.v2025.1.Mm.symbols.gmt) | mh.all.v2025.1.Mm.symbols.gmt | 48008 |

Files reside under `raw_data/wang_20261112/`. S1–S3 contracts hold input
SHA-256 values. Publisher PDF SHA-256 is
`9970ec30cc729e2d61e00dc8da9e6ef23847437532fb0229c14c56c8d8817bc8`.
Europe PMC XML SHA-256 is
`c39272f41c62cf288cfdbc8f80532e4e8948bc2429356fc61bccc275d75afada`.
Direct PMC returned a challenge. Europe PMC's supplement ZIP contained only
an empty JPEG entry. The publisher PDF supplied the methods and panel.

## S3B–C replay eligibility

Supplement PDF p. 5, S3B shows the positive TNFA_SIGNALING_VIA_NFKB and
INFLAMMATORY_RESPONSE Hallmark curves. Supplement PDF p. 2 names Java GSEA,
1,000 gene-set permutations and MSigDB 5.1 Hallmarks. The specific input
normalization, ranking/tie rules, mouse-to-Hallmark identifier translation and
complete run configuration are unresolved. S3C gives normalized reads, an
unpaired t-test and plotted means/SEM for Il10, Tgfb1, Il2, Tnf, Ifng, Prf1 and
Gzmb. S3C marks lower Il10/Tgfb1 and higher Il2; Tnf, Ifng, Prf1 and Gzmb are
marked nonsignificant. Its legend labels all five black points fl/+.
The deposited metadata label only D4_WT_1 fl/+ and the other four +/+.
Which exact sample labels and normalization produced S3C therefore remain
unresolved. The adaptation uses the deposited labels and reports all seven
genes including sparse ones. Figure S3A uses MC38 tumor Treg protein staining,
a separate comparison and endpoint from the in-vitro RNA libraries.
