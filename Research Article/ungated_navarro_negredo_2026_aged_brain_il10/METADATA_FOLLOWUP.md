# Metadata follow-up — 8 November 2026

Owner-requested follow-up to [DATA_USAGE.md](DATA_USAGE.md). This records a
bounded inspection of source metadata, methods and code; no expression matrix,
supplementary workbook cells or biological estimates were analyzed. The
[stepwise analysis plan](ANALYSIS_PLAN.md) uses these findings. Placement remains
**ungated**, outside the ordered roadmap, with no new registered candidate or
scientific acceptance.

**Finding:** additional metadata improve source identity, exposure timing and
unit definitions. They do not recover independent mice from pre-sequencing
pools, add young treatment arms, or establish injury repair. The most useful
unread sources remain S1 (mouse/sequence metadata) and S4 (individual outcomes
and statistics).

## Recovered public experiment metadata

NCBI BioSample E-utilities returned all six accessions below. All record male
C57Bl/6 NIA mice and Stanford collection. Dates are the submitted
`collection_date` attribute, not inferred sequencing dates or proof of an
independent replicate. The [existing ENA mapping](DATA_USAGE.md#deposits-that-were-actually-checked)
identifies their run blocks.

| BioSample | Experiment block | Deposited age | Collection date | What this supplements |
|---|---|---|---|---|
| [SAMN53298929](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298929) | Brain T cells | 22–25 months | 2019-11-04 | Same age/date as lung; consistent with the paper's matched donor pool, not individual pairing |
| [SAMN53298930](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298930) | Lung T cells | 22–25 months | 2019-11-04 | Old-only tissue contrast remains |
| [SAMN53298931](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298931) | RIPR cohort 1 | 24–25 months | 2021-04-28 | Separate experimental cohort; preserve its identity |
| [SAMN53298932](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298932) | RIPR cohort 2 | 24 months | 2020-09-23 | Cohort numbers are not chronological order; no donor identities recovered |
| [SAMN53298933](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298933) | Main IL-10 experiment | mixed | 2023-05-25 | Age is experiment-level, not a per-library numerical age; use the figure/methods crosswalk |
| [SAMN53298934](https://www.ncbi.nlm.nih.gov/biosample/SAMN53298934) | Separate WT IL-10 experiment | 27 months | 2022-12-14 | Different date/age context from main experiment; WT-only replication cannot supply D25K replication |

SRA experiment records **SRX31137323–SRX31137326** identify WT-high,
Mut-high, WT-low and Mut-low libraries, respectively. They specify 10x Genomics
Chromium Single Cell 3-prime v3.1 gene expression and Illumina NovaSeq 6000.
The inspected records do not provide mouse IDs, numeric dose or a donor-to-cell
key. Chemistry helps qualify processing; four library names are not four
replicated animals.

The refreshed [Zenodo API record](https://zenodo.org/api/records/17594828)
still lists the same five RDS files and the unresolved GEO accession `XXX`.
It provides no separate small cell-metadata file. Its manifest does not reveal
the actual RDS columns. Those columns remain uninspected; neither their absence
nor hidden animal replication is inferred.

## Methods metadata that changes the analysis order

Primary source: supplied final-format PDF, physical page numbers below;
cross-checked against [PMC accepted-manuscript text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12927632/).
Paragraph IDs are XML locators in the source snapshot, not new measurements.

| Recovered detail and exact locator | Consequence for reuse |
|---|---|
| Fig. 3B legend, PDF p. 8; XML P154: Figs. 3/4 and S4B/C/E use **0.02 mg/mL**; S4H–K use **0.1 mg/mL** | Numeric figure exposure is known, but its mapping to code aliases and deposited libraries must still be verified |
| Olfactory-bulb methods, PDF p. 31; P92: **0.1 mg/mL**, 24–27-month old mice, two cohorts; six sections averaged per mouse | Mouse, not section, is the outcome unit. Do not treat this as the same exposure/cohort as cognition or the main RNA figures |
| Same methods: young n=5, old control n=9, WT n=10, D25K n=8; Fig. 6G SVZ legend reports young n=4 and old n=8–9 | Preserve endpoint-specific denominators. S4 must distinguish assayed/analyzable mice, regions and exclusions; do not silently force a common n or assume a typographical error |
| Cognitive testing, PDF pp. 32–33; P101–103: 21-month males, **0.02 mg/mL**, one week infusion then one week recovery; random treatment assignment | Supports a treatment comparison in the old cognition cohort. It supplies neither a WT cognition arm nor a young-treatment comparison |
| Imaging methods P86; nesting PDF p. 32/P100 | Image acquisition and nest scoring are explicitly blinded. This does not establish blinding of every assay or every analysis |
| NOR methods, PDF p. 33/P103 | Object identity and location counterbalanced. Per-mouse assignments were not recovered, so they cannot yet be used as covariates |
| General statistics, PDF p. 33/P104 | Alternating sample processing is reported for most experiments. Exact batch/allocation keys are still needed before modeling batch |
| Cognitive methods vs general statistics, pp. 32–33/P101/P104 | Cognition reports a power calculation with alpha 0.05/power 0.8; general statistics says no bona fide power analysis. Scope may explain the wording, but no numerical effect/variance assumptions were recovered. Do not claim documented adequate precision or invent an equivalence margin |

The behavioral exclusion record is available in Methods even without S4:
15 mice initially per arm; two control deaths; Y-maze excludes two additional
controls and one D25K mouse (final 11/14); NOR excludes three D25K mice for
insufficient exploration and one for a health problem (final 13/11).
Different exclusions mean the two behavioral panels are not independent
cohorts or necessarily identical analyzed subsets. Mouse IDs are required for
within-animal joins. S4 is needed to verify the direct between-group tests,
rather than infer them from each group's comparison with chance.

## Code helps identify ambiguity; it does not resolve it

Inspected source: [frozen author archive v1.0.0](https://doi.org/10.5281/zenodo.18174039),
commit prefix `c08010b`; SHA-256 in [DATA_USAGE.md](DATA_USAGE.md).

- `IL10/1.Seurat.R:23–41` maps C1–C8 to Control, WT1, Mut1, WT5,
  Mut5, WT50, Mut50 and Young. Barcode prefixes encode these conditions.
  They are not demonstrated mouse IDs or numeric doses.
- `IL10/2.Microglia.R:49–57` selects WT5/Mut5 for one plotting block;
  lines 107–110 use WT1/Mut1 for “other concentrations.” Alongside Fig. 3B's
  numeric doses, this makes guessing `1 = low, 5 = high` unsafe. No alias-to-dose
  assignment is accepted here.
- `IL10/1.Seurat.R:48–49` records initial thresholds of nCount_RNA > 1,000,
  nFeature_RNA > 500 and mitochondrial fraction < 10%. Later cluster-based
  exclusions require their own trace. The actual saved object's retained cells
  cannot be certified from these thresholds alone.
- `IL10/3.Tcells.R:66–70` explicitly restricts one Gzmb plot to positive cells.
  Future analysis must keep both all-T-cell and Gzmb-positive denominators.
- The eight code labels versus six deposited main-experiment RNA libraries,
  filename discrepancy, and missing clock-model files remain as recorded in
  the initial audit. Unused labels are not evidence for an undeclared dose arm.

## Supplement access: precise remaining limit

S1 and S4 are present in the article attachment manifest, but no workbook
contents were recovered. Direct HTTP routes returned HTML; publisher routes
returned 403. A normal article-page download attempt timed out, and clicking
the S4 link led to a reCAPTCHA browser-verification page. No challenge was
solved or bypassed. The user-specified local Saxton folder contained the article
PDF but no accompanying supplementary workbook.

The retired PMC OA API is not evidence that the article lacks supplements.
[PMC's replacement cloud service](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/)
was checked. Its exact article prefix lists only JSON, XML and text; the
[article JSON](https://pmc-oa-opendata.s3.amazonaws.com/PMC12927632.1/PMC12927632.1.json)
marks this version as an author manuscript with `license_code: TDM`, without
media URLs. PMC documents that non-Creative-Commons manuscript media are
excluded from this service. This limitation belongs to the checked manuscript
distribution, not necessarily the publisher's final-version license.

If a readable supplement is subsequently obtained, first validate XLSX ZIP
structure, provenance and sheet names. Do not use a 200-status HTML response
as evidence of a downloaded workbook. If an author query is later authorized,
request S1/S4, a C1–C8/dose/library crosswalk, actual cell metadata, endpoint
mouse/cohort IDs, exclusion flags and any basis for donor demultiplexing. No
contact was made in this task. Physical pooling cannot be reversed by relabeling.

## Follow-up search and snapshot record

Actual access date: **8 November 2026, Asia/Seoul**. Reused the initial
literature scan; this follow-up did not attempt a new novelty review. Sources:
six BioSample records, four SRA experiment records, Zenodo API, frozen author
code, supplied PDF/PMC XML, PMC cloud docs and exact article prefix, article
download UI, and the supplied local directory. Focused web queries were
`"S1074761326000385" "supplementary"` and
`"Navarro Negredo" "IL-10" "Table S4"`; no alternate readable table resulted.

Public retrievals:

- BioSample: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=biosample&id=SAMN53298929,SAMN53298930,SAMN53298931,SAMN53298932,SAMN53298933,SAMN53298934&retmode=xml`
- SRA: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id=SRX31137323,SRX31137324,SRX31137325,SRX31137326&retmode=xml`
- Cloud listing: `https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=PMC12927632.`

| Local response snapshot | SHA-256 |
|---|---|
| Six BioSample records, `biosample_all.xml` | `8cbd89be8c5f089e9ce224e6971a72b428ccef944b19111ba0349b275328dee4` |
| Four SRA records, `sra.txt` | `52e5e9bf6f6759d654160060bd09d8ca3211b26d086d4f883353fb24ab9c5f30` |
| Zenodo processed-data API, `zenodo.txt` | `eec7b9ab0eb16034fc36e643c79c709c4e040f2988857e1cea2a220c15df44bb` |
| PMC cloud article JSON, `cloud_metadata.json` | `6d18029d550bee2a4a4ea8e3a43efc2f59cd6abbd27a9a8ac51b55d3b479dbb4` |

Snapshots and status/size/hash retrieval manifests are in this chat's local
`navarro_metadata_followup` artifact directory. No raw biological file was
added to the repository. The initial [data audit](DATA_USAGE.md) remains the
source for accession counts and original inspection history; this follow-up
supplements its access status and metadata qualifications.
