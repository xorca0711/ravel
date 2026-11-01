# Source and access manifest

31 October 2026 (Asia/Seoul). Download timestamps below are UTC. Public metadata
and source documents only; no SRA sequence/read file was downloaded. Ignored
source files remain in this worktree for originating review. Exact successful
X1/X2 input hashes are also bound by their immutable receipts.

## Reused X1/X2 sources

| Source | Provenance and use | SHA-256 |
|---|---|---|
| [GSE160217_family.soft.gz](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160217/soft/GSE160217_family.soft.gz) | Original R1 cache retrieved 31 October; X2: all six GEO sample records and original cross-references | `dd5c728e3a8a4128d3c64674ff56b54a24ed3585e3bc9707f33245dbe6a0b273` |
| [GSE160217_060120_22_readcount_genename.xls.gz](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160217/suppl/GSE160217_060120_22_readcount_genename.xls.gz) | Original R1 cache retrieved 31 October; X1: nine annotation fields only; no expression fields selected | `26a63db90cbb1c65614205b05a1a957b37f0783b67df72ad4801b48c5bc0646d` |
| [GSE160217_060120_22_fpkm_genename.xls.gz](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE160nnn/GSE160217/suppl/GSE160217_060120_22_fpkm_genename.xls.gz) | Original R1 cache retrieved 31 October; X1: nine annotation fields only; no expression fields selected | `69dd439dc048fe6ff0e4d343d403e2fe277ea004beb4bc10b80c2f0daa7027f1` |

## Newly requested records/documents

| Cache filename / requested source | Accessed UTC | Outcome / bytes | SHA-256 |
|---|---|---|---|
| [biosamples.xml](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=SAMN16563502,SAMN16563631,SAMN16563630,SAMN16563629,SAMN16563628,SAMN16563627&retmode=xml) | 2026-10-31T13:21:52.732333+00:00 | HTTP 200; text/xml; charset=UTF-8; 10,130 bytes | `8a66251613a05fa38bdfe9a45b6eccfb2547e76a8079f6ddb77e3b5d5967f6fd` |
| [sra_packages.xml](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id=SRX9372917,SRX9372918,SRX9372919,SRX9372920,SRX9372921,SRX9372922&retmode=xml) | 2026-10-31T13:21:53.956464+00:00 | HTTP 200; text/xml; 47,276 bytes | `17ea82a07b7f0e1332acde84b0e75d075385ae776852e6ec75fc7619544cc840` |
| [cineus_supplement_pmc_response](https://pmc.ncbi.nlm.nih.gov/articles/instance/12133592/bin/41590_2025_2149_MOESM1_ESM.pdf) | 2026-10-31T13:21:55.172089+00:00 | HTTP 200; text/html; charset=utf-8; 21,513 bytes; HTML, rejected as PDF | `983162ec401ca7de831b6bcd9d7842007dc7e0c551bb42fd12d8afaabf597fc6` |
| [cineus_supplement_publisher.pdf](https://static-content.springer-cdn.com/esm/art%3A10.1038%2Fs41590-025-02149-z/MediaObjects/41590_2025_2149_MOESM1_ESM.pdf) | 2026-10-31T13:21:55.956286+00:00 | <urlopen error [Errno 11001] getaddrinfo failed> | `no file retrieved` |
| [cineus_supplement_springer.pdf](https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-025-02149-z/MediaObjects/41590_2025_2149_MOESM1_ESM.pdf) | 2026-10-31T13:22:46.609519+00:00 | HTTP 200; application/pdf; 41,137,168 bytes | `96dc5adaf01a669ac89b1e3ed5fbb8fe293bdb5ddda7099f79547f90ec4e8bc8` |
| [cineus_fulltext_epmc.xml](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12133592/fullTextXML) | 2026-10-31T13:22:51.587379+00:00 | HTTP 200; application/xml; 231,739 bytes | `8c98508159d685b4a7716fff02cf42eb85c5ce5895a4437b8294958ae9eae66c` |
| [cineus_reporting.pdf](https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-025-02149-z/MediaObjects/41590_2025_2149_MOESM2_ESM.pdf) | 2026-10-31T13:28:16.789671+00:00 | HTTP 200; application/pdf; 101,337 bytes | `000d500055509d91effcecbf90fba04c8fbed32e3af606ac375ca9ec5f14322c` |
| [cineus_tables.xlsx](https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-025-02149-z/MediaObjects/41590_2025_2149_MOESM4_ESM.xlsx) | 2026-10-31T13:28:17.628326+00:00 | HTTP 200; application/octet-stream; 12,918,625 bytes | `305f9b3965f019e78cd3793c770f5d5e10e4fdcbd091f5b65a3d4dcdae1ef245` |

The filenames above reside under `raw_data/Sx22/extensions_20261031/`. Original
`acquisition_v1.json`, `acquisition_v2.json` and `acquisition_v3.json` retain request
URLs, final URLs where returned, status, content type, bytes and hashes without
overwriting previous attempts. The first manifest is an X2 input; its two XML
entries are preserved in the run's `source_access.json`. The PDF/XML/ZIP signatures
were checked before source interpretation. The supplied `.xls.gz` files remain
gzip-compressed tab-separated text rather than Excel workbooks.

## Item coverage

| Item | Inspected content | Limit |
|---|---|---|
| GEO SOFT | All six saved GSM records, titles, attributes and linked accessions | Reused authoritative family export; individual GEO browser pages were not needed |
| BioSample XML | All six declared SAMN records, primary/reverse IDs, titles and attributes | Database identities do not verify animal independence |
| SRA XML | All six SRX packages, SRS identities, SRR links, member references, layout, attributes and source narrative context | No sequence download; run/layout/member labels do not certify animal relationships |
| MOESM1 supplementary PDF | Visually inspected PDF pp. 23–24, Figure S5e/caption; text matched to renders | Other panels reviewed only to avoid borrowing their n; other supplement contents not exhaustively inspected |
| MOESM2 reporting summary | Text inspection of pp. 2 and 4 for replication/unit-reporting context | Study-wide practices are not an exported panel-specific unit key |
| MOESM4 supplementary workbook | Read-only sheet inventory and leading rows/index headers | Published result/reagent rows were not recalculated or used for targeting; no exhaustive workbook audit claimed |
| Europe PMC article XML | Source-file advertisement/filenames and article identity | Availability statement is not a source-unit linkage export |
| MOESM3 peer review file | Advertisement only | Contents not assessed |
| MOESM5 / MOESM6 | Advertisement identifies Figure 4a/d and Extended Data 7b–d blot files | Files not inspected; not treated as S5e qPCR sources |

Web-tool attempts on PMC MOESM1/MOESM4 returned cache misses; the Nature main-page
request redirected to an inaccessible identity-provider page. Neither supplied
usable source files. The later successful ordinary publisher requests supersede
the file-access limitation only for the named inspected sources. No new search,
author contact, credential use or access-control bypass occurred.

## Evidence locators

- [X1 receipt](../../../analysis/research/runs/sx22_x1_annotation_v1/receipt.json)
- [X2 receipt](../../../analysis/research/runs/sx22_x2_provenance_v1/receipt.json)
- [X2 access records](../../../analysis/research/runs/sx22_x2_provenance_v1/source_access.json)
- [X3 panel and endpoint review](X3_SOURCE_LINKAGE.md)
- [Results and interpretation limits](RESULTS.md)
