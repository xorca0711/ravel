# Source qualification and exposure record

31 October 2026, Asia/Seoul. Governing plan: [README](README.md). Article-local candidate **Sx22-P01** owns exposed source reproduction and recipient-context description. It does not alter A14/A19/A22/A2/A1/A8 or execute Niethamer/S1. See [prior reading](../../docs/research_reviews/2026-10-31-saxton-il22/README.md).

## RNA identity and units

Authoritative [GEO SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160217/soft/GSE160217_family.soft.gz) and [supplement directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160217/suppl/) retrieved 31 October. Series last update 26 October 2021. Both tables are gzipped tab-delimited text despite their `.xls` names; never interpreted as Excel. Source annotation is mm10, deposited Ensembl IDs/symbols, exact annotation release unreported. Methods in the supplied published PDF, p. 23/e9, report two independent biological RNA samples. All six distinct GEO/BioSample records are colon C57BL/6 with a six-hour treatment.

| GEO | Table column | Treatment | BioSample |
|---|---|---|---|
| GSM4869228 | PBS_1 | PBS | SAMN16563502 |
| GSM4869229 | PBS_2 | PBS | SAMN16563631 |
| GSM4869230 | LH5_1 | WT IL-22 | SAMN16563630 |
| GSM4869231 | LH5_2 | WT IL-22 | SAMN16563629 |
| GSM4869232 | LH30_1 | 22-B3 | SAMN16563628 |
| GSM4869233 | LH30_2 | 22-B3 | SAMN16563627 |

GEO labels LH5 as WT and LH30 as B3; these mappings are not inferred from filenames or effect direction. Independent biological replication is source-reported and consistent with separate BioSamples; individual mouse identifiers, allocation, sex and library batch are not supplied. BioSample SAMN16563630 was checked through NCBI efetch and supplies no additional animal key. No pairing between suffix 1/2 across groups is asserted. A conditional unpaired model may use the source-reported n=2 per group, with small-n and unreported-batch limits; it cannot audit animal independence beyond the deposited report. qPCR triplicates do not create RNA-seq units.

## Access record

GEO web view returned a browser challenge; its ordinary public FTP-over-HTTPS endpoints supplied SOFT, read-count and FPKM files. Supplied 23-page final published PDF was copied without alteration to ignored `raw_data/Sx22/saxton_supplied.pdf` (SHA256 437f76f8f63e3c4282de61959b34d86d1fd04f585aa0cc9e04066f4e3f9b578d). PMC article text was read with web tools; direct local download and supplement link returned HTML challenge pages, never treated as PDFs. Publisher supplement endpoint returned HTTP 403. Europe PMC fullTextXML returned 500; PMC OA endpoint returned 404. Crossref resolves published PII S1074761321001205. No access controls bypassed; no credentials or private notes are copied.

## Assay audit

Main final PDF pages 6-11 and 22-23; [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8054646/) Figs. 3-7 and relevant methods. Figure 6 was visually checked; plotted units use micrograms, despite text extraction corrupting the micro sign.

| Panels | Endpoint / reported units | Replication and reconstruction boundary |
|---|---|---|
| 3D/E | HT-29 pSTAT fluorescence normalized to the same analyte's WT maximum | Three replicates; biological preparation mapping unspecified. A displayed Emax description may be digitized; raw curves/replicate keys needed for new curve fits or intervals. Unlike antibody channels cannot be divided. |
| 3F; 4A-C; 5B-E,G-I | Immunoblots from cell preparations or tissue lysates | Representative bands; no qualified raw intensity/replicate series. No new densitometry or STAT ratio. Fig. 4D/5J are models. |
| 5F | Relative receptor qPCR, Gapdh normalization | n=3, mean SEM in legend; whole-tissue transcript is not surface abundance. Raw animal values absent. |
| 6A/B/D | Bulk colon RNA, six hours | Six qualified libraries, n=2 source-reported biological units per arm. This is the numerical reproduction source. |
| 6C/E | Colon qPCR | Two independent biological samples, each technical triplicate; raw Ct and nesting absent. Cannot reproduce tests from bars. |
| 7A/B | Organoid MTT viability / Lgr5 and Olfm4 qPCR | n=3 mice per group; wells/organoids nested, preparation linkage not provided. MTT is metabolic viability, not mature output. |
| 7C | Ileal crypt number per circumference / average depth | n=3 / n=8 mice respectively. Points and SEM displayed, crypt-level mapping absent. |
| 7D | Serum lipase / amylase in acute pancreatitis | n=5 mice per group, SEM. Separate acute injury markers, not chronic recovery. |
| 7E/G/H | Tissue qPCR | n=2 biological samples with triplicates. The figure labels G liver/H skin but legend says G skin/H liver; these panels require an explicit discrepancy hold. |
| 7F | Serum SAA1/2 and haptoglobin at 24 hours | n=3 biological samples, SEM; two displayed treatment doses. Systemic output distinct from epithelial repair. |

Published outcomes, figure panels and related repository summaries were read before freezing. The subsequent contracts are exposed reproduction/exploration. No outcome-driven exclusions are permitted. R1 performs source and matrix QC before any model, retaining failures and ambiguous identifiers.
