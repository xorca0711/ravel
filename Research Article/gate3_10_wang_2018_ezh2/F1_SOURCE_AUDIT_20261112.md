# F1 source audit for Wang 2018

12 November 2026, Asia/Seoul. The question was whether additional public
records identify the biological units and processing blocks behind the
day-four deficient-versus-control Treg RNA contrast, reconcile the control
labels, or permit exact replay of Figure S3B–C. The existing
[results](RESULTS_V1.md), [execution amendment](EXECUTION_AMENDMENT_V1.md)
and [review](REVIEW_20261112.md) define the starting evidence. F1 is a
documentary source audit. It produced no new expression estimates or
metadata analysis outputs. Published and repository outcomes were already known.

## SRA adds a facility-manifest lead

NCBI SRA returned nine experiment packages for SRP145275, brokered by GEO
under SRA701882. The NCBI experiment alias, sample identifier and run
records agree with the existing S1 manifest. The archived submission lists
one single-end HiSeq 4000 run per submitted SRS and specifies the same
TruSeq stranded mRNA library construction as GEO. The public
`SAMPLE_ATTRIBUTE` fields are source name, cell type, genotype and strain.
Each `Pool/Member` repeats that package's SRS, GSM and BioSample identifiers.
It carries no contributing mouse IDs, pool membership or preparation history.
Likewise, the BioProject's study-level `sample_scope=eMultiisolate` supplies
no per-library allocation. [NCBI experiment packages](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&retmode=xml&id=5548915,5548914,5548913,5548912,5548911,5548910,5548909,5548908,5548907) ·
[BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA470833).

The `RUN/SRAFiles/SRAFile` entries marked `Original` retain facility-style
filenames. All share the `DuPage_667` prefix. For example, D4_Ez_1
(GSM3138951/SRR7142658) is `DuPage_667__D4_Ez_1___S42_R1_001.fastq.gz`
and D4_WT_1 (GSM3138955/SRR7142662) is
`DuPage_667__D4_WT_1___S313_R1_001.fastq.gz`. These names give the authors
or facility a key to locate a manifest. Their common prefix and different
`S` indices leave sort, culture, extraction, library-preparation, flowcell
and lane allocation unresolved. The timestamps in those entries are
archive file metadata. ENA independently exposes the records but repeats
the same submission. Its experiment aliases and platform agree, its library
name is blank, and its experiment attributes carry GEO accession and ENA
status. No additional processing assignments were found.
[ENA experiment XML](https://www.ebi.ac.uk/ena/browser/api/xml/SRX4063422,SRX4063423,SRX4063424,SRX4063425,SRX4063426,SRX4063427,SRX4063428,SRX4063429,SRX4063430).

The SRA genotype field repeats the deposited labels of four fl/fl, one fl/+
(D4_WT_1), and four +/+ (D4_WT_2–5). GEO, SRA and BioSample agreement
traces the same submitter metadata. Figure S3C labels the control dots fl/+.
The main article's Mice section gives a study-wide littermate or age-matched
control statement without identifying the mice or pools used for these
libraries. The actual alleles, group membership behind the panels, paired
or split preparations, sex and age remain unresolved. No data support
assigning independence or processing balance from the accession pattern,
filenames, count similarity or PCA. [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE114298) ·
[Wang article](https://doi.org/10.1016/j.celrep.2018.05.050) ·
[Publisher Figure S3](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf).

## S3B shows the rank metric

The bottom panels of both original enrichment plots on supplement PDF
p. 5 explicitly label the ranked-list metric `Signal2Noise`, with
`Ezh2KO` positively correlated, `WT` negatively correlated, and a zero
crossing at rank 5609. The methods on p. 2 specify standalone Java GSEA,
1,000 gene-set permutations and MSigDB 5.1 Hallmarks. This identifies the
published ranking metric and supplies a visual checkpoint for a future
replay. The exact expression input, per-column phenotype assignment, feature
filter, Ensembl-to-Hallmark ID or orthology mapping and collapse rules remain
unknown, as do the Java build and full run settings. The plot cannot supply
the ranked list or establish which normalization preceded it. S3C supplies
normalized-read plots, means/SEM and unpaired t-test labels without the
normalization procedure or library-to-dot crosswalk. The eight-page
publisher supplement contains methods and S1–S6; its later pages add plotted
functional summaries. [Publisher supplement](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc1.pdf).

The [MSigDB 5.1 release notes](https://docs.gsea-msigdb.org/MSigDB/Release_Notes/MSigDB_5.1/)
date that release to January 2016. The [archive page](https://www.gsea-msigdb.org/gsea/downloads_archive.jsp)
redirected to login, the historic download endpoint returned a web cache
miss, and the analogous public Broad CDN file path returned HTTP 404.
No version-matched GMT was recovered on these routes. Even an authenticated
5.1 copy would leave the authors' mouse-to-input mapping and sample-specific
analysis inputs unresolved.

## Access record

New byte-preserved responses are in ignored `raw_data/wang_20261112/f1/`.
They were read directly for this audit. The original supplement, Europe PMC
article XML, GEO family SOFT and BioSample records were reused with the
[original acquisition record](SOURCE_QUALIFICATION.md).

| Response and exact route | Bytes | SHA-256 |
|---|---:|---|
| `sra-esearch.json`, [SRA ESearch SRP145275](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term=SRP145275&retmax=20&retmode=json) | 377 | `4a79af1728769212b54913e8695986d269b780012e03f911f807dd19564c86e1` |
| `sra-packages.xml`, [SRA EFetch for the nine returned UIDs](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&retmode=xml&id=5548915,5548914,5548913,5548912,5548911,5548910,5548909,5548908,5548907) | 79031 | `f07137b9f5a12396e200fcad6ca0322fbc7079a1c6f56a33537049ce4a23d7b3` |
| `bioproject.xml`, [BioProject EFetch UID 470833](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=bioproject&id=470833&retmode=xml) | 3636 | `3ef144195739adcadb761f5b34db1e42cbe74a80a7adc80bd3ca28d8be32421b` |
| `ena-experiments.xml`, [ENA XML for SRX4063422–SRX4063430](https://www.ebi.ac.uk/ena/browser/api/xml/SRX4063422,SRX4063423,SRX4063424,SRX4063425,SRX4063426,SRX4063427,SRX4063428,SRX4063429,SRX4063430) | 25909 | `9da9735e66e0bfc9ffd221d3e67061b8061579eac09304b0d90f4afd7cdbc82b` |
| `geo-supp-list.html`, [GEO supplemental directory](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114298/suppl/) | 667 | `0b6682d066acf0a72165cf661ce1a3d770b555ba27be69a66b745d73ff79f8e2` |

The GEO supplemental directory lists the deposited count matrix as its sole
file. The article's Data and Software Availability section points to GEO.
Web queries combined GSE114298, SRP145275 and the study title with S3 source
data, normalized counts, and `DuPage_667`. The targeted filename search of
the stored paper folder for Wang, GSE114298, `DuPage_667`, S3B or S3C
returned the previously read main-paper PDF only. The ScienceDirect page
and publisher `mmc2` URL returned 403. The UC repository page challenged
the browser and its OAI record request returned 403. These route outcomes
bound what could be verified. The missing unit/block crosswalk and panel
settings reside in sample sheets and analysis records, so F1 used archive
metadata without downloading the FASTQs. [Publisher landing page](https://www.sciencedirect.com/science/article/pii/S2211124718307964) ·
[Publisher mmc2 route](https://ars.els-cdn.com/content/image/1-s2.0-S2211124718307964-mmc2.pdf) ·
[UC repository](https://escholarship.org/uc/item/62n0r4sq) ·
[UC OAI request](https://escholarship.org/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:escholarship.org:ark:/13030/qt62n0r4sq).

## Eligibility after F1

| Scope | Decision |
|---|---|
| Population inference | Held. Obtain the mouse/pool and preparation crosswalk and processing blocks, verify allele labels, then check whether the intended genotype contrast is estimable at the biological-unit level. |
| Exact S3B–C replay | Held. The Signal2Noise label, phenotype orientation and released method narrow the replay specification. Exact inputs, mapping and settings for S3B, and normalization and library-to-dot assignment for S3C, remain missing. |
| Qualified description | The nine-library scope remains supported. An exposed, descriptive analysis using the recovered rank metric could only be assessed under a new contract and checkpoint authorization. The existing effects and Hallmark outputs remain the current estimates. |
| Functional reconstruction | Held. The public supplements show aggregate or representative panels. Numerical reconstruction requires panel-linked per-animal flow files with gates and denominators, or individual longitudinal tumor measurements with cohort and treatment assignments, depending on the endpoint. |

The next decision is whether existing source records can be recovered with
the [draft request](F1_AUTHOR_REQUEST_DRAFT.md). A source crosswalk would
address independence and processing, but the biological distinction between
recovery/composition and within-state RNA requires linked absolute viable
recovery and state-resolved measurements from identified preparations.
The relevant comparisons would distinguish total recovered population
differences from RNA differences among cells in matched observed states.
Conditioning on a state measured after perturbation does not by itself
identify a direct genotype effect. No F2 execution or new study was opened.
